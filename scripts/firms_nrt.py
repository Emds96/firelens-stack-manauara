#!/usr/bin/env python3
"""NASA FIRMS area ingestion for Amazonas. stdlib only; never publish MAP_KEY.

JSON declares observational coverage only; no physical fire count or harmonization.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import math
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"
SOURCES = ("VIIRS_NOAA20_NRT", "VIIRS_NOAA21_NRT")
USER_AGENT = "StackManauara-DoisTradutores/0.1 (NASA Space Apps 2026)"
REQUIRED = {"latitude", "longitude", "acq_date", "acq_time", "confidence"}
UTC = dt.timezone.utc


def now_utc():
    return dt.datetime.now(UTC)


def iso(value):
    return value.astimezone(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def parse_utc(date, time):
    if not date or not time or len(str(time).strip()) > 4:
        raise ValueError("Data/hora FIRMS inválida")
    timestamp = dt.datetime.strptime(str(date).strip()+str(time).strip().zfill(4), "%Y-%m-%d%H%M")
    return timestamp.replace(tzinfo=UTC)


def coords_iter(geometry):
    """Yield (lon,lat) pairs of Polygon/MultiPolygon for bbox only."""
    typ = geometry.get("type")
    parts = geometry.get("coordinates", [])
    if typ == "Polygon":
        polygons = [parts]
    elif typ == "MultiPolygon":
        polygons = parts
    else:
        raise ValueError("Limite IBGE deve ser Polygon ou MultiPolygon")
    for polygon in polygons:
        for ring in polygon:
            for xy in ring:
                yield float(xy[0]), float(xy[1])


def extract_geometry(boundary):
    typ = boundary.get("type")
    if typ in ("Polygon", "MultiPolygon"):
        return boundary
    if typ == "Feature":
        return boundary["geometry"]
    if typ == "FeatureCollection":
        features = boundary.get("features", [])
        if len(features) != 1:
            raise ValueError("Esperada exatamente uma feição para o Amazonas")
        return features[0]["geometry"]
    raise ValueError("GeoJSON do Amazonas inválido ou formato não suportado")


def get_bbox(geometry):
    pts = list(coords_iter(geometry))
    if len(pts) < 4:
        raise ValueError("Geometria do Amazonas incompleta")
    return min(x for x,y in pts), min(y for x,y in pts), max(x for x,y in pts), max(y for x,y in pts)


def point_in_ring(x, y, ring):
    # Ray-casting test; horizontal ray; boundary points considered inside.
    inside = False
    for i in range(len(ring)):
        x1, y1 = ring[i-1][:2]
        x2, y2 = ring[i][:2]
        x1, y1, x2, y2 = map(float, (x1, y1, x2, y2))
        cross = (x-x1)*(y2-y1) - (y-y1)*(x2-x1)
        if abs(cross) < 1e-10 and min(x1,x2)-1e-10 <= x <= max(x1,x2)+1e-10 and min(y1,y2)-1e-10 <= y <= max(y1,y2)+1e-10:
            return True
        if (y1 > y) != (y2 > y):
            cut = x1 + (y-y1) * (x2-x1) / (y2-y1)
            if x < cut:
                inside = not inside
    return inside


def point_in_geometry(x, y, geometry):
    typ = geometry['type']
    polygons = [geometry['coordinates']] if typ == 'Polygon' else geometry['coordinates']
    for polygon in polygons:
        if not polygon or not point_in_ring(x, y, polygon[0]):
            continue
        if any(point_in_ring(x, y, hole) for hole in polygon[1:]):
            continue
        return True
    return False


def download_ibge_geometry():
    url = "https://servicodados.ibge.gov.br/api/v3/malhas/estados/13?formato=application/vnd.geo%2Bjson"
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/geo+json, application/json"})
    with urlopen(req, timeout=35) as response:
        body = response.read(15_000_000)
    data = json.loads(body)
    return extract_geometry(data), url


def request_source(key, source, bbox, days=2):
    if source not in SOURCES:
        raise ValueError("Sensor não permitido")
    if not 1 <= days <= 5:
        raise ValueError("API FIRMS aceita entre 1 e 5 dias")
    coords = ','.join(f"{n:.5f}" for n in bbox)
    # Avoid disclosing the authenticated URL in logs or exceptions.
    url = f"{BASE}/{key}/{source}/{coords}/{days}"
    try:
        with urlopen(Request(url, headers={"User-Agent": USER_AGENT}), timeout=70) as response:
            content = response.read(35_000_000).decode("utf-8-sig")
    except (HTTPError, URLError, TimeoutError, UnicodeDecodeError) as exc:
        raise RuntimeError(f"FIRMS {source}: consulta não concluída ({type(exc).__name__})") from None
    if content.lstrip().startswith(("<", "{")):
        raise RuntimeError(f"FIRMS {source}: resposta não é CSV esperado")
    first = next(csv.reader(io.StringIO(content)), [])
    if not first:
        # Empty CSV can represent no observations; retain explicit state.
        return [], "empty_csv"
    if not REQUIRED.issubset(set(first)):
        raise RuntimeError(f"FIRMS {source}: cabeçalho CSV inesperado")
    return list(csv.DictReader(io.StringIO(content))), "ok"


def process_rows(rows, geometry, source):
    result = []
    seen = set()
    rejected = {"outside_amazonas":0,"low_confidence":0,"invalid":0}
    for row in rows:
        try:
            lat, lon = float(row['latitude']), float(row['longitude'])
            if not (-90 <= lat <= 90 and -180 <= lon <= 180) or not all(math.isfinite(n) for n in [lat, lon]):
                raise ValueError('coords')
            if not point_in_geometry(lon, lat, geometry):
                rejected['outside_amazonas'] += 1
                continue
            # Retain only normal/high confidence for comparability with historical filters.
            confidence = (row.get('confidence') or '').strip().lower()
            if confidence not in ('n', 'h'):
                rejected['low_confidence'] += 1
                continue
            acquired = parse_utc(row.get('acq_date'), row.get('acq_time'))
            daynight = (row.get('daynight') or '').strip().upper()
            if daynight not in ('D','N'):
                raise ValueError('daynight')
            # dedup exact rows, but do not collapse distinct detection pixels.
            sig = (lat, lon, acquired.isoformat(), daynight)
            if sig in seen:
                continue
            seen.add(sig)
            result.append({
                'latitude': round(lat,5), 'longitude': round(lon,5),
                'observed_at_utc': iso(acquired), 'confidence':confidence,
                'daynight':daynight, 'sensor':source.replace('VIIRS_', '').replace('_NRT',''),
            })
        except (ValueError, KeyError, TypeError, OverflowError):
            rejected['invalid'] += 1
    result.sort(key=lambda x:x['observed_at_utc'], reverse=True)
    return result, rejected


def summarize(rows):
    return {'detections':len(rows),'diurnal':sum(r['daynight']=='D' for r in rows),
            'nocturnal':sum(r['daynight']=='N' for r in rows),
            'latest_observation_utc':max((r['observed_at_utc'] for r in rows),default=None)}


def empty_result():
    return {
       'schema_version':1,'area':'Estado do Amazonas, Brasil (contorno estadual simplificado de fonte secundária, baseado em IBGE)',
       'source':'NASA FIRMS Area API', 'source_url':'https://firms.modaps.eosdis.nasa.gov/api/area/',
       'status':'unavailable', 'last_attempt_utc':None, 'last_success_utc':None,
       'last_observation_utc':None, 'query_days':2, 'filters':'VIIRS confidence n/h; dia e noite separados; geometria IBGE',
       'sensors':{}, 'detections':[], 'alerts':['Integração ainda não executada; não há dados NRT verificados.'],
       'disclaimer':'Detecções de pixels, não incêndios individuais. NRT não significa observação instantânea.',
    }


def build_payload(key, boundary, previous=None, fetcher=request_source, now=None, boundary_source='IBGE'):
    now = now or now_utc()
    geometry = extract_geometry(boundary)
    bbox = get_bbox(geometry)
    prior = previous if isinstance(previous, dict) else empty_result()
    payload = empty_result()
    payload.update({'last_attempt_utc':iso(now), 'boundary_source':boundary_source,
                    'bbox_requested':list(bbox), 'sensors':{}, 'alerts':[]})
    errors = []
    all_detections = []
    for source in SOURCES:
        try:
            rows, response_state = fetcher(key, source, bbox, 2)
            processed, rejects = process_rows(rows, geometry, source)
            latest = summarize(processed)
            all_detections.extend(processed)
            payload['sensors'][source] = {'status':'ok','response_state':response_state,
                                          'summary':latest,'exclusions':rejects}
        except Exception as exc:
            errors.append(source)
            payload['sensors'][source] = {'status':'error','message':str(exc).replace(str(key),'[REDACTED]')}
    if not errors:
        payload['status'] = 'ok'
        payload['last_success_utc'] = iso(now)
        payload['detections'] = sorted(all_detections,key=lambda x:x['observed_at_utc'],reverse=True)
    else:
        # Never silently replace partial or failed results with a fresh-looking dataset.
        payload['status'] = 'unavailable'
        payload['last_success_utc'] = prior.get('last_success_utc')
        payload['detections'] = prior.get('detections', [])
        payload['alerts'].append('Falha em um ou mais sensores; exibindo última captura anterior, se disponível.')
        payload['fallback_snapshot'] = bool(payload['detections'])
    obs = [r['observed_at_utc'] for r in payload['detections']]
    payload['last_observation_utc'] = max(obs, default=None)
    payload['count'] = len(payload['detections'])
    if payload['last_success_utc']:
        last = dt.datetime.fromisoformat(payload['last_success_utc'].replace('Z','+00:00'))
        payload['snapshot_age_hours'] = round(max(0,(now-last).total_seconds())/3600,2)
        if (now-last).total_seconds() > 4*3600:
            payload['alerts'].append('Dados desatualizados: última consulta bem-sucedida há mais de 4 horas.')
    else:
        payload['alerts'].append('Não existe atualização NRT bem-sucedida registrada.')
    if payload['status'] == 'ok' and not payload['detections']:
        payload['alerts'].append('Nenhuma detecção elegível foi retornada na janela consultada; isso não comprova ausência de fogo.')
    return payload


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',default='data/recente.json')
    parser.add_argument('--boundary',default='data/amazonas_ibge.geojson')
    args = parser.parse_args(argv)
    key = os.environ.get('FIRMS_MAP_KEY','').strip()
    out = Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    prior = json.loads(out.read_text(encoding='utf8')) if out.exists() else empty_result()
    if not key:
        print('BLOQUEIO: defina FIRMS_MAP_KEY como segredo; nenhuma consulta foi executada.',file=sys.stderr)
        return 2
    try:
        path=Path(args.boundary)
        if path.exists():
            boundary=json.loads(path.read_text(encoding='utf8'))
            boundary_source=(boundary.get('properties',{}).get('source') or 'Malha estadual, arquivo versionado no repositório')
        else:
            geom,boundary_source=download_ibge_geometry()
            boundary={'type':'Feature','geometry':geom,'properties':{'source':boundary_source}}
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(json.dumps(boundary,ensure_ascii=False),encoding='utf8')
        payload=build_payload(key,boundary,prior,boundary_source=boundary_source)
    except Exception as exc:
        # Retain prior capture, explicitly stale; do not lose data during outage.
        payload=empty_result()
        payload.update({'status':'unavailable','last_attempt_utc':iso(now_utc()),
                        'last_success_utc':prior.get('last_success_utc'),
                        'last_observation_utc':prior.get('last_observation_utc'),
                        'detections':prior.get('detections',[]),
                        'alerts':[f'Ingestão indisponível: {type(exc).__name__}. Última captura preservada.']})
    out.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    print(f"FIRMS: status={payload['status']}; detecções={len(payload['detections'])}; resultado={out}")
    return 0 if payload['status']=='ok' else 1


if __name__=='__main__':
    sys.exit(main())

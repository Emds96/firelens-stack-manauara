#!/usr/bin/env python3
"""TEST-01 | Amazonas historical FIRMS observations, independently auditable.
Run: python -m scripts.test01_historico --output data/test01_historico_amazonas.json
No changes to any FireLens UI or data/historico.json. Stdlib-only.
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import math
import os
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from scripts.firms_nrt import extract_geometry, get_bbox, point_in_geometry, download_ibge_geometry

BASE = "https://firms.modaps.eosdis.nasa.gov/data/country/"
SENSORS = {"modis": "Aqua", "viirs-jpss1": "NOAA20"}
YEARS = (2023, 2024, 2025, 2026)
MAX_DATE = dt.date(2026, 11, 14)
BOUNDARY_PATH = Path("data/amazonas_ibge.geojson")
FIELDS = {"latitude", "longitude", "acq_date", "acq_time", "satellite", "confidence", "daynight"}

def timestamp(row):
    d = dt.datetime.strptime(row["acq_date"] + str(row["acq_time"]).zfill(4), "%Y-%m-%d%H%M")
    return d.replace(tzinfo=dt.timezone.utc)

def valid_sensor(row, sensor):
    # Same scientific filters as VAL-TRAD-02; UTC month deliberately used here
    # to avoid unobserved cross-year local-solar boundary without adjacent files.
    if row.get("type", "0") not in ("", "0"):
        return False
    if row.get("daynight") != "D":
        return False
    if sensor == "modis":
        if row.get("satellite") not in ("Aqua", "A"):
            return False
        try:
            return float(row["confidence"]) >= 30
        except (ValueError, KeyError, TypeError):
            return False
    return row.get("confidence", "").lower() in ("n", "h")

def download(url, destination, limit_bytes=450_000_000):
    """Read once to disk and compute hash; no silently truncated file accepted."""
    request = Request(url, headers={"User-Agent": "StackManauara-TEST-01/1.0"})
    h = hashlib.sha256()
    with urlopen(request, timeout=110) as response, destination.open("wb") as sink:
        last_modified = response.headers.get("Last-Modified")
        declared = response.headers.get("Content-Length")
        size = 0
        while True:
            block = response.read(1024*1024)
            if not block:
                break
            size += len(block)
            if size > limit_bytes:
                raise ValueError("archive exceeds maximum bytes")
            h.update(block)
            sink.write(block)
    if declared and size != int(declared):
        raise IOError("archive download length differs from HTTP Content-Length")
    # Protect against HTML proxy errors returned with HTTP 200.
    with destination.open("rb") as f:
        head = f.read(200).lstrip()
    if not head.startswith(b"latitude,") and b"latitude" not in head.split(b"\n",1)[0]:
        raise ValueError("response is not expected FIRMS CSV")
    return {"bytes":size,"sha256":h.hexdigest(),"last_modified":last_modified,
            "http_content_length":int(declared) if declared else None}

def resolve_geometry(prefer_official):
    attempt={"url":"https://servicodados.ibge.gov.br/api/v3/malhas/estados/13?formato=application/vnd.geo%2Bjson",
             "status":"not_attempted"}
    if prefer_official:
        try:
            shape,source=download_ibge_geometry()
            bbox=get_bbox(shape)
            if not (-75 < bbox[0] < -72 and -11 < bbox[1] < -8 and -58 < bbox[2] < -54 and 1 < bbox[3] < 4):
                raise ValueError("unexpected official boundary bbox")
            attempt["status"]="downloaded_verified_bbox_not_precision"
            return shape,{"source":source,"label":"IBGE API direct; bbox checked",
                "boundary_sha256":hashlib.sha256(json.dumps(shape,sort_keys=True).encode()).hexdigest(),
                "bbox":list(bbox),"official_attempt":attempt}
        except Exception as exc:
            attempt["status"]="failed"
            attempt["error_type"]=type(exc).__name__
    data=json.loads(BOUNDARY_PATH.read_text(encoding="utf8"))
    props=data.get("properties",{})
    if str(props.get("cd_geocuf",props.get("code","13")))!="13" or props.get("sigla")!="AM":
        raise ValueError("Amazonas geometry ID invalid")
    shape=extract_geometry(data)
    raw=BOUNDARY_PATH.read_bytes()
    return shape,{"source":str(BOUNDARY_PATH),"label":"simplified third-party IBGE-based outline; NOT official verified precision",
        "boundary_sha256":hashlib.sha256(raw).hexdigest(),
        "bbox":list(get_bbox(shape)),"official_attempt":attempt}

def process_archive(path, sensor, year, geometry):
    west,south,east,north=get_bbox(geometry)
    stats=Counter()
    # keys: (year, month, sensor, lat1deg, lon1deg) -> number of source pixels
    cells=Counter()
    first,last=None,None
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f)
        if not reader.fieldnames or not FIELDS.issubset(reader.fieldnames):
            raise ValueError("missing required CSV columns: "+",".join(sorted(FIELDS-set(reader.fieldnames or []))))
        stats["csv_has_type"]=int("type" in reader.fieldnames)
        for row in reader:
            stats["raw_rows"]+=1
            if not valid_sensor(row,sensor):
                stats["filtered_sensor_or_quality"]+=1
                continue
            try:
                lat=float(row["latitude"]);lon=float(row["longitude"])
                if not all(math.isfinite(x) for x in (lat,lon)):
                    raise ValueError("nonfinite")
                date=timestamp(row)
            except (ValueError,TypeError,KeyError,OverflowError):
                stats["invalid"]+=1
                continue
            if date.year != year or date.date() > MAX_DATE:
                stats["outside_target_dates"]+=1
                continue
            if not (west<=lon<=east and south<=lat<=north):
                stats["outside_bbox"]+=1
                continue
            if not point_in_geometry(lon,lat,geometry):
                stats["outside_polygon"]+=1
                continue
            key=(date.year,date.month,SENSORS[sensor],math.floor(lat),math.floor(lon))
            cells[key]+=1
            first=date if first is None or date<first else first
            last=date if last is None or date>last else last
            stats["retained_pixels"]+=1
    return cells,{"rows":dict(stats),"first_retained_utc":first.isoformat() if first else None,
        "last_retained_utc":last.isoformat() if last else None,"cells_nonempty":len(cells)}

def month_counts(cells,years):
    counts=Counter()
    for (year,month,sensor,lat,lon),count in cells.items():
        if year in years:
            counts[(year,month,sensor)]+=count
    return counts

def evaluate(cells, train_years, holdout):
    """Same spatial 1-degree x calendar month WAPE as VAL-TRAD-02; no leakage."""
    training_modis=sum(v for (y,m,s,la,lo),v in cells.items() if y in train_years and s=="Aqua")
    training_viirs=sum(v for (y,m,s,la,lo),v in cells.items() if y in train_years and s=="NOAA20")
    keys={(m,la,lo) for (y,m,s,la,lo) in cells if y==holdout}
    raw_wape=None
    if not training_viirs or not keys:
        return {"status":"insufficient","training_years":list(train_years),"holdout_year":holdout,
                "reason":"no train NOAA20 detections or no holdout cells"}
    factor=training_modis/training_viirs
    raw_error=scaled_error=modis_total=viirs_total=0.
    for month,lat,lon in keys:
        m=cells.get((holdout,month,"Aqua",lat,lon),0)
        v=cells.get((holdout,month,"NOAA20",lat,lon),0)
        raw_error+=abs(m-v)
        scaled_error+=abs(m-factor*v)
        modis_total+=m;viirs_total+=v
    if not modis_total:
        return {"status":"insufficient","reason":"zero MODIS denominator",
                "training_years":list(train_years),"holdout_year":holdout}
    return {"status":"evaluated","training_years":list(train_years),"holdout_year":holdout,
        "factor_from_training_only":round(factor,8),
        "training_modis":training_modis,"training_noaa20":training_viirs,
        "holdout_modis":int(modis_total),"holdout_noaa20":int(viirs_total),
        "raw_wape":round(raw_error/modis_total,5),
        "scaled_wape":round(scaled_error/modis_total,5),
        "active_cells_month":len(keys),
        "metric":"WAPE over union of active 1-degree UTC-month cells; denominator=MODIS Aqua detections, NOT fires"}

def recurring(cells, years=(2023,2024,2025)):
    # Recurrent 1-degree cells across independent years; not repeated fire events.
    yearsets=defaultdict(set)
    totals=Counter()
    for (y,m,s,lat,lon),count in cells.items():
        if y in years and s=="NOAA20":
            yearsets[(lat,lon)].add(y)
            totals[(lat,lon)]+=count
    results=[]
    for key in yearsets:
        if len(yearsets[key])>=2:
            results.append({"cell_south_lat":key[0],"cell_west_lon":key[1],
                "active_years":sorted(yearsets[key]),"number_of_years":len(yearsets[key]),
                "noaa20_pixels":totals[key]})
    return sorted(results,key=lambda x:(-x["number_of_years"],-x["noaa20_pixels"],x["cell_south_lat"],x["cell_west_lon"]))

def comparable_2026(cells, available):
    # Requires BOTH source archives. Compare Jan-Oct and Nov 1-14 only,
    # preserving equal temporal windows. No claims when one sensor missing.
    if not all((2026,s) in available for s in SENSORS):
        return {"status":"not_comparable","reason":"2026 annual snapshot missing for MODIS Aqua or NOAA-20",
                "noaa21_is_not_substituted":True}
    # all 2026 CSV rows are truncated at 14 Nov; prior years are truncated
    # to the same cutoffs by data-loading into this function (for Nov use
    # extra monthly partial counters, not whole November months).
    return {"status":"requires_daily_cutoff_series",
            "reason":"Monthly 1-degree aggregation omits day; a faithful Nov 1–14 comparison requires daily buckets. Do not compare complete historical Nov with partial Nov 2026."}

def analyze(cache,prefer_official=True):
    geometry,boundary=resolve_geometry(prefer_official)
    out={
      "id":"TEST-01","created_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
      "status":"insufficient","period_requested":"2023-01-01 through 2026-11-14 inclusive",
      "source":"NASA FIRMS annual Brazil country CSV",
      "source_url":BASE,"region":"Amazonas, Brazil",
      "geometry":boundary,"sensors":["MODIS Aqua","VIIRS NOAA-20"],
      "filters":{"type":"0 when available","MODIS_Aqua_confidence":">=30",
         "NOAA20_confidence":"n/h","daynight":"D only",
         "spatial":"point-in-polygon after bounding box","time":"UTC calendar month",
         "time_note":"Departed from VAL-TRAD-02 local solar month to prevent incomplete cross-year local months. Near UTC midnight, month assignments may differ; no direct metric comparison to A/B."},
      "file_inventory":[],"monthly":[],"holdouts":[],"recurring_cells":[],
      "limitations":["pixel detections != individual fires or burned area",
                     "different sensor resolutions, sensitivities, orbit timing and cloud effects",
                     "hotspot CSV has no clear-sky denominator or uncertainty intervals",
                     "three years do not constitute long-term climatology",
                     "historical A/B calibration is NOT applied to Amazonas",
                     "2026 files, when present, are not automatically science-quality consolidated"],
      "observations":[],"inferences":[],"hypotheses":[]
    }
    all_cells=Counter()
    available=set()
    cache.mkdir(parents=True,exist_ok=True)
    for year in YEARS:
        for sensor in SENSORS:
            filename=f"{sensor}_{year}_Brazil.csv"
            url=BASE+filename
            local=cache/filename
            entry={"year":year,"sensor":sensor,"url":url,"status":"unavailable"}
            try:
                audit=download(url,local)
                entry.update(audit)
                cells,summary=process_archive(local,sensor,year,geometry)
                entry.update(summary)
                entry["status"]="processed"
                all_cells.update(cells)
                available.add((year,sensor))
            except (HTTPError,URLError,TimeoutError,ValueError,OSError) as e:
                entry.update({"error_type":type(e).__name__,
                              "http_code":getattr(e,"code",None)})
                # Do not claim a URL is missing on network failure.
                entry["status"]="not_found" if isinstance(e,HTTPError) and e.code==404 else "request_failed"
            finally:
                # Keep no giant files in the repository or on disk for later years.
                if local.exists():
                    local.unlink()
            out["file_inventory"].append(entry)
    complete=[y for y in YEARS if all((y,s) in available for s in SENSORS)]
    historic=[y for y in (2023,2024,2025) if y in complete]
    out["complete_sensor_years"]=complete
    out["historical_comparable_years"]=historic
    counts=month_counts(all_cells,complete)
    for year in complete:
        for month in range(1,13):
            if year==2026 and month>11: continue
            out["monthly"].append({"year":year,"month":month,"modis_aqua":counts.get((year,month,"Aqua"),0),
                "viirs_noaa20":counts.get((year,month,"NOAA20"),0),
                "period_status":"partial_2026_month" if year==2026 and month==11 else "archive_month"})
    for test_year,train_years in ((2024,(2023,)),(2025,(2023,2024))):
        if test_year in complete and all(y in complete for y in train_years):
            out["holdouts"].append(evaluate(all_cells,train_years,test_year))
        else:
            out["holdouts"].append({"status":"not_evaluated","holdout_year":test_year,
                "training_years":list(train_years),"reason":"required archive year/sensor not available"})
    if len(historic)>=2:
        out["recurring_cells"]=recurring(all_cells,tuple(historic))[:30]
    out["comparison_2026"]=comparable_2026(all_cells,available)
    if len(historic)==3 and all(e["status"]=="evaluated" for e in out["holdouts"]):
        out["status"]="historical_evaluated_2026_unverified"
        out["observations"].append("2023–2025 independent historical holdouts computed for Amazonas with source-year audit.")
    elif historic:
        out["status"]="partial_historical_archives"
        out["observations"].append("Some archived years were processed but complete temporal validation was not possible.")
    else:
        out["observations"].append("No sufficient pair of MODIS Aqua and NOAA-20 annual archives was recovered for 2023–2025.")
    if out["monthly"]:
        # Based only on valid complete-source historical years, no causal claims.
        full=[m for m in out["monthly"] if m["year"] in historic]
        if full:
            ordered=sorted(full,key=lambda x:(-x["viirs_noaa20"],x["year"],x["month"]))
            out["observations"].append(f"Maximum observed NOAA-20 monthly pixel count in complete-source years: {ordered[0]['year']}-{ordered[0]['month']:02d} ({ordered[0]['viirs_noaa20']}).")
            minrow=min(full,key=lambda x:(x["viirs_noaa20"],x["year"],x["month"]))
            out["observations"].append(f"Minimum observed NOAA-20 monthly pixel count in complete-source years: {minrow['year']}-{minrow['month']:02d} ({minrow['viirs_noaa20']}).")
    out["inferences"].append("Repeated observations within 1-degree cells warrant closer investigation; they cannot establish repeated individual fires or underlying causes.")
    out["result_interpretation"]="No region should be labelled safe/dangerous or intentionally burned from these observations."
    return out

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--cache",type=Path,default=Path(tempfile.gettempdir())/"firelens-test01")
    parser.add_argument("--output",type=Path,default=Path("data/test01_historico_amazonas.json"))
    parser.add_argument("--no-official-attempt",action="store_true")
    args=parser.parse_args()
    data=analyze(args.cache,prefer_official=not args.no_official_attempt)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print("TEST-01 status:",data["status"])
    for f in data["file_inventory"]:
        print("FILE",f["year"],f["sensor"],f["status"],
            f.get("rows",{}).get("retained_pixels","—"),f.get("error_type",""))
    print("HOLDOUTS",json.dumps(data["holdouts"]))
    print("2026",json.dumps(data["comparison_2026"]))
    print("JSON",args.output)

if __name__=="__main__":
    main()

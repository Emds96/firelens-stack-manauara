#!/usr/bin/env python3
"""TEST-02 / Visao da Aguia: NASA FIRMS NRT observation-level diagnostics.

Not a physical fire-identity classifier. Geographic 'scan × track' rectangles
are *axis-aligned approximations*, not Level-2 geolocation footprints.
All NASA source columns are preserved in the separate raw observation JSON.
No changes to operational site/data or TEST-01/01B/SCI-03.
Run on GitHub Actions with FIRMS_MAP_KEY secret set.
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
from collections import Counter, defaultdict
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from scripts.firms_nrt import extract_geometry, get_bbox, point_in_geometry

START = "2026-11-10"
END = "2026-11-14"
FOCUS_DAY = "2026-11-11"
SOURCES = ("MODIS_NRT", "VIIRS_NOAA20_NRT")
API = "https://firms.modaps.eosdis.nasa.gov/api/area/csv"
FOCUS_BBOX = [-61.5, -4.5, -58.5, -2.0]  # W,S,E,N; Manaus/Careiro/Autazes vicinity
LOCAL_TZ = dt.timezone(dt.timedelta(hours=-4), "AMT")
GEOMETRY = Path("data/amazonas_ibge.geojson")
# Sensitivity thresholds are exploratory, NOT NASA validated fire identity criteria.
THERMAL_LIMITS = (5.0, 8.0)
FRP_RATIO_LIMITS = (0.5, 2.0)
MAX_TIME_DIRECT_MIN = 120
EDGE_KM = 2.5

def parse_time(row):
    text = (str(row["acq_date"]) + str(row["acq_time"]).zfill(4))
    return dt.datetime.strptime(text, "%Y-%m-%d%H%M").replace(tzinfo=dt.timezone.utc)

def finite(raw, field):
    if field not in raw or raw[field] in ("", None):return None
    try:
        n=float(raw[field])
        return n if math.isfinite(n) else None
    except (TypeError,ValueError):
        return None

def nasa_fetch(source, bounds, key):
    """Key never appears in logs, returned metadata, traceback, or exception."""
    if source not in SOURCES:raise ValueError("invalid NASA source")
    bbox=",".join(f"{x:.5f}" for x in bounds)
    url=f"{API}/{key}/{source}/{bbox}/5/{START}"
    request=Request(url,headers={"User-Agent":"StackManauara-TEST02/1.0"})
    try:
        with urlopen(request,timeout=95) as response:
            blob=response.read(28_000_000)
            if len(blob)>=28_000_000:raise ValueError("NASA response exceeds 28MB")
    except (HTTPError,URLError,TimeoutError,OSError) as exc:
        error_code=getattr(exc,"code",None)
        raise RuntimeError(f"NASA {source} request failed ({type(exc).__name__}, HTTP={error_code})") from None
    if blob.lstrip().startswith((b"<",b"{")):raise ValueError("NASA did not return a FIRMS CSV")
    text=blob.decode("utf-8-sig")
    csv_reader=csv.DictReader(io.StringIO(text))
    fields=csv_reader.fieldnames or []
    required={"latitude","longitude","acq_date","acq_time","scan","track","frp",
              "confidence","daynight","satellite"}
    required|=({"brightness","bright_t31"} if source=="MODIS_NRT" else
               {"bright_ti4","bright_ti5"})
    if not required.issubset(set(fields)):
        raise ValueError("NASA source CSV missing required physical columns: "+
                         ",".join(sorted(required-set(fields))))
    rows=list(csv_reader)
    for row in rows:
        if None in row:raise ValueError("Unexpected extra CSV values; cannot trust row parsing")
    return rows,{"source":source,"url_redacted":f"{API}/[MAP_KEY]/{source}/{bbox}/5/{START}",
                 "retrieved_at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
                 "sha256_csv":hashlib.sha256(blob).hexdigest(),
                 "bytes_csv":len(blob),"csv_columns":fields,"raw_csv_rows":len(rows)}

def normalize(rows,source,geometry):
    stats=Counter()
    kept=[]
    for i,raw in enumerate(rows,1):
        stats["raw_csv"]+=1
        try:
            lat=finite(raw,"latitude");lon=finite(raw,"longitude")
            t=parse_time(raw)
            if lat is None or lon is None or abs(lat)>90 or abs(lon)>180:
                raise ValueError("invalid coordinate")
        except (ValueError,KeyError,TypeError):
            stats["invalid_coordinates_or_time"]+=1;continue
        if not START<=t.date().isoformat()<=END:
            stats["outside_dates"]+=1;continue
        if not point_in_geometry(lon,lat,geometry):
            stats["outside_polygon"]+=1;continue
        platform=raw.get("satellite","")
        if source=="MODIS_NRT":
            if platform in ("A","Aqua"):satellite="Aqua"
            elif platform in ("T","Terra"):satellite="Terra"
            else:
                stats["unknown_modis_platform"]+=1;continue
        else:
            if platform not in ("N20","NOAA-20","NOAA20"):
                stats["unknown_viirs_platform"]+=1;continue
            satellite="NOAA-20"
        scan=finite(raw,"scan");track=finite(raw,"track")
        if scan is None or track is None or scan<=0 or track<=0:
            stats["invalid_scan_track"]+=1;continue
        d={"id":f"{'M' if source=='MODIS_NRT' else 'V'}-{i:06d}",
           "source":source,"satellite":satellite,"latitude":lat,"longitude":lon,
           "time_utc":t.isoformat().replace("+00:00","Z"),
           "time_manaus":t.astimezone(LOCAL_TZ).isoformat(timespec="minutes"),
           "date_utc":t.date().isoformat(),"daynight":raw.get("daynight",""),
           "confidence":raw.get("confidence",""),"scan_km":scan,"track_km":track,
           "area_km2_approx":round(scan*track,6),"frp_mw":finite(raw,"frp"),
           "t4_k":finite(raw,"brightness" if source=="MODIS_NRT" else "bright_ti4"),
           "t11_k":finite(raw,"bright_t31" if source=="MODIS_NRT" else "bright_ti5"),
           "i4_saturation":False,"i4_possible_folding":False,
           "focus_bbox":FOCUS_BBOX[0]<=lon<=FOCUS_BBOX[2] and FOCUS_BBOX[1]<=lat<=FOCUS_BBOX[3],
           "raw_columns":dict(raw)}
        if source=="VIIRS_NOAA20_NRT" and d["t4_k"] is not None:
            d["i4_saturation"]=abs(d["t4_k"]-367.0)<0.0001
            d["i4_possible_folding"]=d["t4_k"]<250.0
        if satellite=="NOAA-20":
            d["historic_quality_filter_eligible"]=raw.get("confidence","").lower() in ("n","h") and raw.get("daynight")=="D"
        else:
            confidence=finite(raw,"confidence")
            d["historic_quality_filter_eligible"]=(satellite=="Aqua" and
                confidence is not None and confidence>=30 and raw.get("daynight")=="D" and
                raw.get("type","0") in ("0",""))
        kept.append(d)
        stats["inside_amazonas"]+=1
        if d["focus_bbox"]:stats["inside_focus_bbox"]+=1
        if d["date_utc"]==FOCUS_DAY:stats["on_focus_day"]+=1
        if d["historic_quality_filter_eligible"]:stats["eligible_diurnal_baseline"]+=1
    return kept,dict(stats)

def spatial(m,v):
    # km equirectangular, assuming scans aligned to degrees. NOT an exact
    # footprint: satellite viewing angle / swath orientation are not included.
    latr=math.radians((m["latitude"]+v["latitude"])/2.0)
    dx=abs(v["longitude"]-m["longitude"])*111.32*math.cos(latr)
    dy=abs(v["latitude"]-m["latitude"])*110.57
    hx=(m["scan_km"]+v["scan_km"])/2
    hy=(m["track_km"]+v["track_km"])/2
    footprint_approx=dx<=hx and dy<=hy
    from_border=math.hypot(max(0,dx-hx),max(0,dy-hy))
    center_km=math.hypot(dx,dy)
    return {"dx_km":dx,"dy_km":dy,"inside_approx_box":footprint_approx,
            "distance_center_km":center_km,"distance_from_box_km":from_border,
            "half_x_overlap_km":hx,"half_y_overlap_km":hy}

def delta_minutes(m,v):
    return abs((dt.datetime.fromisoformat(m["time_utc"].replace("Z","+00:00"))-
                dt.datetime.fromisoformat(v["time_utc"].replace("Z","+00:00"))).total_seconds())/60.0

def comparability(m,v):
    return (m["date_utc"]==v["date_utc"] and m["daynight"]==v["daynight"])

def group_candidates(modis,viirs):
    """Individual and group diagnostics. No unique-fire ground truth inferred."""
    groups=[]
    pair_index=defaultdict(list)
    for m in modis:
        inside_sync=[];inside_delay=[];border=[]
        for v in viirs:
            if m["date_utc"]!=v["date_utc"]:continue
            g=spatial(m,v)
            minutes=delta_minutes(m,v)
            pair={"modis_id":m["id"],"viirs_id":v["id"],
                  "minutes":round(minutes,3),
                  "same_daynight":m["daynight"]==v["daynight"],
                  "dx_km":round(g["dx_km"],4),"dy_km":round(g["dy_km"],4),
                  "inside_approx_box":g["inside_approx_box"],
                  "distance_center_km":round(g["distance_center_km"],4),
                  "distance_from_box_km":round(g["distance_from_box_km"],4)}
            if g["inside_approx_box"] and comparability(m,v):
                if minutes<=MAX_TIME_DIRECT_MIN:
                    inside_sync.append(v)
                    pair["relationship"]="spatial_temporal_candidate"
                else:
                    inside_delay.append(v)
                    pair["relationship"]="spatial_delayed_candidate"
            elif not g["inside_approx_box"] and g["distance_from_box_km"]<=EDGE_KM:
                border.append(v)
                pair["relationship"]="near_border_unverified"
            else:continue
            pair_index[v["id"]].append(pair)
        if inside_sync or inside_delay or border:
            avg_t=(sum(x["t11_k"] for x in inside_sync if x["t11_k"] is not None)/
                   sum(x["t11_k"] is not None for x in inside_sync)) if any(x["t11_k"] is not None for x in inside_sync) else None
            sum_frp=(sum(x["frp_mw"] for x in inside_sync if x["frp_mw"] is not None)
                     if all(x["frp_mw"] is not None for x in inside_sync) else None)
            ratio=sum_frp/m["frp_mw"] if sum_frp is not None and m["frp_mw"] and m["frp_mw"]>0 else None
            delta_t=abs(m["t11_k"]-avg_t) if m["t11_k"] is not None and avg_t is not None else None
            thermal_5=delta_t is not None and delta_t<=THERMAL_LIMITS[0]
            thermal_8=delta_t is not None and delta_t<=THERMAL_LIMITS[1]
            frp_ok=ratio is not None and FRP_RATIO_LIMITS[0]<=ratio<=FRP_RATIO_LIMITS[1]
            groups.append({
                "modis_id":m["id"],"satellite":m["satellite"],
                "modis_time_utc":m["time_utc"],"modis_frp_mw":m["frp_mw"],
                "modis_t11_k":m["t11_k"],
                "in_box_and_within_120min_ids":[x["id"] for x in inside_sync],
                "in_box_over_120min_ids":[x["id"] for x in inside_delay],
                "near_border_ids":[x["id"] for x in border],
                "viirs_t11_mean_k":round(avg_t,3) if avg_t is not None else None,
                "delta_t11_k":round(delta_t,3) if delta_t is not None else None,
                "viirs_frp_sum_mw":round(sum_frp,3) if sum_frp is not None else None,
                "frp_ratio_viirs_to_modis":round(ratio,4) if ratio is not None else None,
                "thermal_5k":thermal_5,"thermal_8k":thermal_8,
                "frp_ratio_in_exploratory_range":frp_ok,
                "four_locks_candidate_5k":bool(inside_sync and thermal_5 and frp_ok),
                "four_locks_candidate_8k":bool(inside_sync and thermal_8 and frp_ok),
                "no_physical_identity_proven":True})
    return groups,pair_index

def summarize(rows):
    vals=lambda key:[x[key] for x in rows if x.get(key) is not None]
    def average(key):
        x=vals(key)
        return round(sum(x)/len(x),4) if x else None
    return {"n":len(rows),"frp_avg_mw":average("frp_mw"),
            "area_avg_km2_approx":average("area_km2_approx"),
            "t4_avg_k":average("t4_k"),"t11_avg_k":average("t11_k"),
            "i4_saturation_count":sum(x["i4_saturation"] for x in rows),
            "i4_folding_candidate_count":sum(x["i4_possible_folding"] for x in rows)}

def categorize(modis,viirs,groups,pairs):
    by_group={g["modis_id"]:g for g in groups}
    modis_by_id={m["id"]:m for m in modis}
    res={}
    for v in viirs:
        matches=pairs.get(v["id"],[])
        direct=[p for p in matches if p["relationship"]=="spatial_temporal_candidate"]
        delayed=[p for p in matches if p["relationship"]=="spatial_delayed_candidate"]
        border=[p for p in matches if p["relationship"]=="near_border_unverified"]
        # A VIIRS pixel may overlap multiple MODIS boxes: NEVER count physical
        # FRP as uniquely assignable without a better true-footprint algorithm.
        strong=[p for p in direct if by_group[p["modis_id"]]["four_locks_candidate_8k"]]
        if len(strong)==1 and len(direct)==1:
            label="four_locks_compatible_unconfirmed"
            best=strong[0]
        elif delayed and not direct:
            label="spatial_overlap_delayed_unconfirmed"
            best=min(delayed,key=lambda p:(p["minutes"],p["distance_center_km"]))
        elif border and not direct and not delayed:
            label="edge_near_modis_no_expansion_proof"
            best=min(border,key=lambda p:p["distance_from_box_km"])
        elif not matches:
            # Explicitly check distance to every MODIS on the same date.
            same_date=[m for m in modis if m["date_utc"]==v["date_utc"]]
            nearest=min((spatial(m,v)["distance_from_box_km"] for m in same_date),default=None)
            if nearest is None or nearest>EDGE_KM:
                label="viirs_spatially_isolated_not_proven_invisible"
            else:
                label="unresolved"
            best=None
        else:
            label="unresolved_ambiguous_or_lock_failure"
            best=min(matches,key=lambda p:(p["minutes"],p["distance_center_km"]))
        res[v["id"]]={"category":label,"reference_modis_id":best["modis_id"] if best else None,
            "candidate_modis_count":len(matches),"matched_group_count":len(strong),
            "distance_from_box_km":best["distance_from_box_km"] if best else (
                round(min((spatial(m,v)["distance_from_box_km"] for m in modis
                      if m["date_utc"]==v["date_utc"]),default=float("inf")),3)
                if any(m["date_utc"]==v["date_utc"] for m in modis) else None)}
    return res

def detail_examples(modis,viirs,groups,pairs,categories,day,limit=28):
    m_by={m["id"]:m for m in modis}
    v_by={v["id"]:v for v in viirs}
    day_groups=[g for g in groups if g["modis_id"] in m_by and m_by[g["modis_id"]]["date_utc"]==day]
    day_groups.sort(key=lambda g:(not g["four_locks_candidate_8k"],
                                  -len(g["in_box_and_within_120min_ids"]),
                                  g["modis_id"]))
    examples=[]
    for g in day_groups[:8]:
        m=m_by[g["modis_id"]]
        selected=g["in_box_and_within_120min_ids"]+g["in_box_over_120min_ids"]
        examples.append({"modis":m,"group":g,
                         "viirs_rows":[v_by[x] for x in selected[:limit]],
                         "group_truncated":len(selected)>limit})
    ind=[v for v in viirs if v["date_utc"]==day and
          categories[v["id"]]["category"]=="viirs_spatially_isolated_not_proven_invisible"]
    ind.sort(key=lambda x:(x["time_utc"],x["latitude"],x["longitude"]))
    return {"blocks":examples,"isolated_viirs_examples":ind[:8],
            "independent_count":len(ind)}

def evaluate_day(modis,viirs,groups,pairs,date):
    curm=[m for m in modis if m["date_utc"]==date]
    curv=[v for v in viirs if v["date_utc"]==date]
    cat=categorize(curm,curv,[g for g in groups if g["modis_id"] in {m["id"] for m in curm}],pairs)
    allcategories=[
       "four_locks_compatible_unconfirmed","spatial_overlap_delayed_unconfirmed",
       "edge_near_modis_no_expansion_proof","viirs_spatially_isolated_not_proven_invisible",
       "unresolved_ambiguous_or_lock_failure","unresolved"]
    summary={label:summarize([v for v in curv if cat[v["id"]]["category"]==label])
             for label in allcategories}
    quality=[v for v in curv if v["historic_quality_filter_eligible"]]
    focus=[v for v in curv if v["focus_bbox"]]
    qual_m=[m for m in curm if m["historic_quality_filter_eligible"]]
    result={"date_utc":date,"modis_total":summarize(curm),
            "modis_aqua":summarize([m for m in curm if m["satellite"]=="Aqua"]),
            "modis_terra":summarize([m for m in curm if m["satellite"]=="Terra"]),
            "noaa20_total":summarize(curv),
            "eligible_diurnal_modis_aqua":len(qual_m),
            "eligible_diurnal_noaa20":len(quality),
            "focus_bbox_counts":{"modis_all":sum(m["focus_bbox"] for m in curm),
                                 "noaa20_all":len(focus)},
            "categories_viirs_mutually_exclusive":summary,
            "all_categories_sum_check":sum(x["n"] for x in summary.values())==len(curv),
            "four_locks_candidate_groups_8k":sum(g["four_locks_candidate_8k"] for g in groups
              if g["modis_id"] in {m["id"] for m in curm}),
            "four_locks_candidate_groups_5k":sum(g["four_locks_candidate_5k"] for g in groups
              if g["modis_id"] in {m["id"] for m in curm}),
            "viirs_categories":cat,
            "viirs_confidence_counts":dict(Counter(v["confidence"] for v in curv))}
    return result

def build_analysis(modis,viirs,meta,geometry_sha):
    groups,pairs=group_candidates(modis,viirs)
    days=[]
    for i in range(5):
        date=(dt.date.fromisoformat(START)+dt.timedelta(days=i)).isoformat()
        days.append(evaluate_day(modis,viirs,groups,pairs,date))
    focus=next(x for x in days if x["date_utc"]==FOCUS_DAY)
    m11=[x for x in modis if x["date_utc"]==FOCUS_DAY]
    v11=[x for x in viirs if x["date_utc"]==FOCUS_DAY]
    examples=detail_examples(modis,viirs,groups,pairs,focus["viirs_categories"],FOCUS_DAY)
    source_ids={m["id"] for m in modis}
    count_shared=sum(1 for v in viirs if sum(
       p["relationship"]=="spatial_temporal_candidate" for p in pairs.get(v["id"],[]))>1)
    for day in days:
        day["viirs_categories"]=None  # avoid duplicate huge repeated index
    return {"id":"TEST-02","status":"exploratory_not_physical_confirmation",
            "fetched_at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
            "study_window_utc":[START,END],"focus_date_utc":FOCUS_DAY,
            "region":"Amazonas, Brazil (simplified provisional boundary)",
            "focus_bbox_wsen":FOCUS_BBOX,"geometry_sha256":geometry_sha,
            "sources":meta,"daily":days,
            "group_diagnostics":groups,"examples_2026_11_11":examples,
            "viirs_multi_MODIS_spatiotemporal_overlap_count":count_shared,
            "total_modis_rows":len(modis),"total_viirs_rows":len(viirs),
            "thresholds_exploratory":{"time_min":MAX_TIME_DIRECT_MIN,"thermal_k":[5,8],
                                      "frp_ratio":[0.5,2.0],"edge_km":EDGE_KM},
            "physics_caveats":[
              "FIRMS scan and track are approximate pixel dimensions; axis-aligned boxes are not the actual oriented Level-2 pixel footprints.",
              "Spatial, temporal, T11 and FRP agreement are not a proof of unique physical fire identity.",
              "T31/TI5 are observed pixel brightness temperatures, not isolated non-burning background temperatures.",
              "FRP is instantaneous radiative power, not conserved energy across 120-minute observations; aggregation may double-count overlapping swaths.",
              "VIIRS spatial isolation from MODIS detections does not establish that MODIS observed the same location or missed an understory fire.",
              "No claim about Manaus smoke, air quality, burning area, canopy, criminality, or cause follows from FIRMS hotspots alone.",
              "NRT detections are provisional. Boundary has unverified precision; identical coordinates can be included/excluded near its edge.",
              "No negative detection implies fire absence. No Level-2 swath geolocation or cloud masks are available in these CSVs."],
            "approval":"scientific_review_pending","interface_modified":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--rows-output",default="data/test02_observacoes_20261110_14.json")
    p.add_argument("--results-output",default="data/test02_resultados.json")
    args=p.parse_args()
    key=os.environ.get("FIRMS_MAP_KEY","")
    if not key:raise RuntimeError("FIRMS_MAP_KEY not configured; no authenticated query attempted")
    source=GEOMETRY.read_bytes()
    geometry=extract_geometry(json.loads(source))
    bbox=get_bbox(geometry)
    records={};meta={}
    for name in SOURCES:
        rows,m=nasa_fetch(name,bbox,key)
        kept,stats=normalize(rows,name,geometry)
        m["filter_stats"]=stats
        records[name]=kept;meta[name]=m
        print("TEST02",name,"raw",len(rows),"inside_state",len(kept),
              "11nov",sum(x["date_utc"]==FOCUS_DAY for x in kept),flush=True)
    observations={"id":"TEST-02","study_window_utc":[START,END],
                  "source_columns_retained":True,
                  "source_metadata":meta,
                  "notes":"Full raw NASA fields per retained source row; no MAP_KEY included",
                  "MODIS_NRT":records["MODIS_NRT"],
                  "VIIRS_NOAA20_NRT":records["VIIRS_NOAA20_NRT"]}
    result=build_analysis(records["MODIS_NRT"],records["VIIRS_NOAA20_NRT"],
                           meta,hashlib.sha256(source).hexdigest())
    for name,obj in ((args.rows_output,observations),(args.results_output,result)):
        target=Path(name);target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
        print("TEST02 ARTIFACT",target,"bytes",target.stat().st_size,flush=True)
    focus=next(x for x in result["daily"] if x["date_utc"]==FOCUS_DAY)
    print("TEST02 11NOV counts: Aqua",focus["modis_aqua"]["n"],
          "Terra",focus["modis_terra"]["n"],
          "NOAA20",focus["noaa20_total"]["n"],
          "qualified Aqua",focus["eligible_diurnal_modis_aqua"],
          "qualified NOAA20",focus["eligible_diurnal_noaa20"],flush=True)
    print("TEST02 categories",json.dumps({k:v["n"] for k,v in
          focus["categories_viirs_mutually_exclusive"].items()}),flush=True)

if __name__=="__main__":
    main()

#!/usr/bin/env python3
"""TEST-01B/B: NASA FIRMS 2026 date-range inventory and bounded Area API retrieval.
Uses GitHub Actions secret FIRMS_MAP_KEY. NEVER writes/logs key or authenticated URL.
Does NOT modify original TEST-01 artifacts or current FireLens interface.
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
import time
from collections import Counter,defaultdict
from pathlib import Path
from urllib.error import HTTPError,URLError
from urllib.request import Request,urlopen
from scripts.firms_nrt import extract_geometry,get_bbox,point_in_geometry
from scripts.test01_historico import timestamp,valid_sensor

START=dt.date(2026,1,1)
END=dt.date(2026,11,14)
BASE="https://firms.modaps.eosdis.nasa.gov/api"
SENSORS={
 "MODIS_AQUA":{"standard":"MODIS_SP","nrt":"MODIS_NRT","filter":"modis"},
 "NOAA20":{"standard":"VIIRS_NOAA20_SP","nrt":"VIIRS_NOAA20_NRT","filter":"viirs-jpss1"}}
MAX_WINDOWS_PER_SENSOR=70
MAX_ROWS_PER_CSV=250000

def safe_request(url):
    """Returns content only; callers must never format URL into an error or logs."""
    req=Request(url,headers={"User-Agent":"StackManauara-TEST-01B/1.0"})
    with urlopen(req,timeout=85) as resp:
        content=resp.read(22_000_000)
        if len(content)>=22_000_000:
            raise ValueError("API response larger than 22MB safety cap")
        return content,dict(resp.headers)

def availability(key):
    url=f"{BASE}/data_availability/csv/{key}/all"
    body,headers=safe_request(url)
    if body.lstrip().startswith(b"<"):
        raise ValueError("data availability not CSV")
    text=body.decode("utf-8-sig")
    reader=csv.DictReader(io.StringIO(text))
    if not {"data_id","min_date","max_date"}.issubset(reader.fieldnames or []):
        raise ValueError("Unexpected data availability CSV schema")
    out={}
    for row in reader:
        try:
            lo=dt.date.fromisoformat(row["min_date"])
            hi=dt.date.fromisoformat(row["max_date"])
            if hi<lo:continue
            out[row["data_id"]]={"min_date":str(lo),"max_date":str(hi)}
        except (KeyError,ValueError):
            continue
    return out,{"url":f"{BASE}/data_availability/csv/[MAP_KEY]/all",
        "sha256":hashlib.sha256(body).hexdigest(),"downloaded_bytes":len(body),
        "retrieved_at_utc":dt.datetime.now(dt.timezone.utc).isoformat()}

def day_sources(av,sensor):
    """Select SP preferentially, then NRT with exactly one source per UTC date."""
    products=SENSORS[sensor]
    mapping={}
    cursor=START
    while cursor<=END:
        chosen=None
        for kind,product in (("standard",products["standard"]),("nrt",products["nrt"])):
            span=av.get(product)
            if span and dt.date.fromisoformat(span["min_date"])<=cursor<=dt.date.fromisoformat(span["max_date"]):
                chosen=(kind,product)
                break
        mapping[cursor]=chosen
        cursor+=dt.timedelta(days=1)
    return mapping

def contiguous_windows(daymap):
    """Max five days per request, no overlap, no multi-processing duplicates."""
    dates=sorted(daymap)
    windows=[]
    missing=[]
    i=0
    while i<len(dates):
        d=dates[i]
        product=daymap[d]
        if product is None:
            missing.append(str(d));i+=1;continue
        group=[d];j=i+1
        while (j<len(dates) and len(group)<5 and daymap[dates[j]]==product and
               dates[j]==group[-1]+dt.timedelta(days=1)):
            group.append(dates[j]);j+=1
        windows.append({"first":str(group[0]),"last":str(group[-1]),
                        "days":len(group),"processing":product[0],"product":product[1]})
        i=j
    return windows,missing

def validate_chunk(body, product, filter_sensor, shape, win):
    digest=hashlib.sha256(body).hexdigest()
    content=body.decode("utf-8-sig")
    first_line=content.splitlines()[0] if content.splitlines() else ""
    if not first_line or first_line.lstrip().startswith("<"):
        raise ValueError("No CSV header / HTML response")
    rdr=csv.DictReader(io.StringIO(content))
    required={"latitude","longitude","acq_date","acq_time","confidence","daynight"}
    if not required.issubset(rdr.fieldnames or []):
        raise ValueError("Unexpected 2026 FIRMS schema: missing mandatory columns")
    if filter_sensor=="modis" and "satellite" not in rdr.fieldnames:
        raise ValueError("MODIS Aqua filter cannot be applied without satellite column")
    fieldnames=list(rdr.fieldnames)
    totals=Counter()
    daily=Counter()
    cells=Counter()
    seen=set()
    start=dt.date.fromisoformat(win["first"])
    end=dt.date.fromisoformat(win["last"])
    for row in rdr:
        totals["raw"]+=1
        if totals["raw"]>MAX_ROWS_PER_CSV:
            raise ValueError("Unexpected source volume")
        if not valid_sensor(row,filter_sensor):
            totals["excluded_filters"]+=1;continue
        try:
            when=timestamp(row)
            lat=float(row["latitude"]);lon=float(row["longitude"])
            if not (-90<=lat<=90 and -180<=lon<=180):
                raise ValueError("out of bound coordinates")
        except (KeyError,TypeError,ValueError,OverflowError):
            totals["invalid"]+=1;continue
        if not start<=when.date()<=end or when.date()>END:
            totals["outside_dates"]+=1;continue
        if not point_in_geometry(lon,lat,shape):
            totals["outside_state"]+=1;continue
        # Exact duplicate in a single product/window only; do not deduplicate
        # against different products because day mapping never overlaps.
        sig=(lat,lon,when.isoformat(),row.get("confidence"),row.get("daynight"))
        if sig in seen:
            totals["duplicate_exact"]+=1;continue
        seen.add(sig)
        totals["retained"]+=1
        daily[str(when.date())]+=1
        cells[(when.month,int(lat//1),int(lon//1))]+=1
    return {"sha256":digest,"response_bytes":len(body),"csv_columns":fieldnames,
            "has_type_field":"type" in fieldnames,"counts":dict(totals)},daily,cells

def retrieve(key, shape, avail):
    result={"status":"not_started","dates_requested":[str(START),str(END)],
            "processing_preference":"SP first; NRT only on days lacking SP; no overlap",
            "observation_months":[],"sensors":{},"fatal_errors":[]}
    if not key:
        result["status"]="credential_missing"
        result["fatal_errors"].append("FIRMS_MAP_KEY GitHub secret unavailable; no authenticated query performed")
        return result
    bbox=get_bbox(shape)
    bboxtext=",".join(f"{v:.4f}" for v in bbox)
    all_ok=True
    for sensor in SENSORS:
        daymap=day_sources(avail,sensor)
        windows,missing=contiguous_windows(daymap)
        sat={"availability_products":{p:avail.get(p) for p in (SENSORS[sensor]["standard"],SENSORS[sensor]["nrt"])},
             "planned_windows":len(windows),"unavailable_days":missing,
             "successful_windows":[],"failed_windows":[],"daily_counts":{},"monthly_counts":{},
             "processing_counts":{},"eligible_pixels":0}
        result["sensors"][sensor]=sat
        if len(windows)>MAX_WINDOWS_PER_SENSOR:
            sat["failed_windows"].append({"error_type":"SafetyCap","reason":"more windows than planned cap"})
            all_ok=False;continue
        seen_days=set()
        daily=Counter()
        monthly=Counter()
        proc=Counter()
        for i,win in enumerate(windows,1):
            url=f"{BASE}/area/csv/{key}/{win['product']}/{bboxtext}/{win['days']}/{win['first']}"
            metadata={"source_url_template":f"{BASE}/area/csv/[MAP_KEY]/{win['product']}/{bboxtext}/{win['days']}/{win['first']}",
                      "first":win["first"],"last":win["last"],"days":win["days"],
                      "processing":win["processing"],"product":win["product"]}
            try:
                body,headers=safe_request(url)
                audit,days,cells=validate_chunk(body,win["product"],SENSORS[sensor]["filter"],shape,win)
                for d,v in days.items():
                    if d in seen_days:
                        raise ValueError("Data window overlap detected")
                    seen_days.add(d)
                    daily[d]+=v
                for (m,la,lo),v in cells.items():
                    monthly[m]+=v
                proc[win["processing"]]+=audit["counts"].get("retained",0)
                metadata.update(audit)
                metadata["http_status"]=200
                sat["successful_windows"].append(metadata)
                print("2026",sensor,i,"of",len(windows),win["first"],win["processing"],
                      "retained",audit["counts"].get("retained",0),flush=True)
            except (HTTPError,URLError,TimeoutError,ValueError,UnicodeDecodeError,OverflowError) as exc:
                metadata["error_type"]=type(exc).__name__
                metadata["http_status"]=getattr(exc,"code",None)
                sat["failed_windows"].append(metadata)
                print("FAILED 2026",sensor,win["first"],type(exc).__name__,
                      getattr(exc,"code",""),flush=True)
                all_ok=False
        sat["daily_counts"]={k:daily[k] for k in sorted(daily)}
        sat["monthly_counts"]={str(m):monthly[m] for m in range(1,12) if
             any(dt.date.fromisoformat(z["first"]).month<=m<=dt.date.fromisoformat(z["last"]).month for z in sat["successful_windows"])}
        sat["processing_counts"]=dict(proc)
        sat["eligible_pixels"]=sum(daily.values())
        sat["days_with_detections"]=len(daily)
        sat["source_coverage_query_days"]=sum(w["days"] for w in sat["successful_windows"])
        sat["query_failed_days"]=sum(w["days"] for w in sat["failed_windows"] if "days" in w)
        sat["day_catalogue_is_complete"]=not missing and not sat["failed_windows"]
        if missing:all_ok=False
    result["status"]="all_requested_days_queried" if all_ok else "partial_or_unavailable"
    result["warnings"]=[
       "Querying all dates does not prove every satellite pass was observed; clouds and outages may prevent detections.",
       "NRT is provisional and may later be replaced by SP; sensor/processing mixes must be labelled.",
       "No original TEST-01 source file or FireLens frontend was modified.",
       "No algorithmic harmonization is applied to 2026.",
       "Status 'all_requested_days_queried' means all intervals queried successfully, not ground truth coverage."
    ]
    return result

def run(output, key):
    bpath=Path("data/amazonas_ibge.geojson")
    shape=extract_geometry(json.loads(bpath.read_text(encoding="utf8")))
    result={"id":"TEST-01B","investigation":"B","status":"not_started",
        "checked_at_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
        "NASA_docs":["https://firms.modaps.eosdis.nasa.gov/api/data_availability/",
                     "https://firms.modaps.eosdis.nasa.gov/api/area/",
                     "https://firms.modaps.eosdis.nasa.gov/download/",
                     "https://nrt3.modaps.eosdis.nasa.gov/help/"],
        "archive_request":{"status":"requires_user_authentication_or_email",
            "url":"https://firms.modaps.eosdis.nasa.gov/download/",
            "note":"Request by date range via authenticated interactive NASA Archive Download; no such request submitted by this unattended script."},
        "nrt_direct_archive":{"status":"requires_earthdata_token",
            "url":"https://nrt3.modaps.eosdis.nasa.gov/archive/FIRMS/",
            "note":"EDL token distinct from FIRMS_MAP_KEY; no token was assumed or exposed."},
        "geometry":{"path":str(bpath),"sha256":hashlib.sha256(bpath.read_bytes()).hexdigest(),
                    "official_precision_verified":False}}
    if not key:
        result["availability_error"]={"error_type":"MissingFirmsMapKey"}
        result["retrieval"]={"status":"credential_missing"}
    else:
        try:
            available,meta=availability(key)
            result["availability"]=available
            result["availability_manifest"]=meta
            result["retrieval"]=retrieve(key,shape,available)
        except (HTTPError,URLError,TimeoutError,ValueError,UnicodeDecodeError) as exc:
            result["availability_error"]={"error_type":type(exc).__name__,
                                          "http_status":getattr(exc,"code",None)}
            result["retrieval"]={"status":"availability_query_failed"}
    result["status"]=result["retrieval"]["status"]
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    Path(output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("2026 STATUS",result["status"],"sensor counts",
          {k:v.get("eligible_pixels") for k,v in result["retrieval"].get("sensors",{}).items()})
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="/tmp/firelens-test01b-b.json")
    args=p.parse_args()
    run(args.output,os.environ.get("FIRMS_MAP_KEY",""))
if __name__=="__main__":main()

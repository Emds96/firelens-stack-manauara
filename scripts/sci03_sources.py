#!/usr/bin/env python3
"""SCI-03 source acquisition: exact 1-degree x UTC-month NASA FIRMS counts.
Read-only to FireLens and TEST-01/TEST-01B. Python standard library.
  python -m scripts.sci03_sources historical --out /tmp/sci03_historical.json
  python -m scripts.sci03_sources recent --out /tmp/sci03_recent.json
"""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, math, os, tempfile
from collections import Counter
from pathlib import Path
from scripts.test01_historico import BASE, download, process_archive
from scripts.firms_nrt import extract_geometry, get_bbox
from scripts.test01b_2026 import availability,day_sources,contiguous_windows,safe_request,validate_chunk

END=dt.date(2026,10,31)
START=dt.date(2026,1,1)
REGION=Path("data/amazonas_ibge.geojson")

def geometry():
    raw=REGION.read_bytes()
    return extract_geometry(json.loads(raw)),hashlib.sha256(raw).hexdigest()

def encode(cells):
    return [[int(y),int(m),str(s),int(la),int(lo),int(v)]
            for (y,m,s,la,lo),v in sorted(cells.items()) if m<=10 and v>0]

def historical():
    shape,geo_sha=geometry()
    existing=json.loads(Path("data/test01_historico_amazonas.json").read_text())
    checks={(x["year"],x["sensor"]):x for x in existing["file_inventory"] if x["status"]=="processed"}
    out={"id":"SCI-03","source":"NASA FIRMS public yearly Brazil archives",
         "period":"2023–2025 Jan 1–Oct 31 UTC","processing":"country annual archive, SP-equivalence not independently asserted",
         "geometry_sha256":geo_sha,"file_provenance":[],"data":[],"status":"not_started"}
    cells=Counter()
    for year in (2023,2024,2025):
        for source in ("modis","viirs-jpss1"):
            name=f"{source}_{year}_Brazil.csv"
            file=Path(tempfile.gettempdir())/("sci03_"+name)
            try:
                provenance=download(BASE+name,file)
                prior=checks[(year,source)]
                if provenance["sha256"]!=prior["sha256"]:
                    raise ValueError("SCI-03 historical source hash differs from archived TEST-01; do not silently combine")
                counts,info=process_archive(file,source,year,shape)
                if info["rows"]["retained_pixels"]!=prior["rows"]["retained_pixels"]:
                    raise ValueError("SCI-03 original eligible count differs from TEST-01")
                cells.update({k:v for k,v in counts.items() if k[1]<=10})
                out["file_provenance"].append({"year":year,"source":source,"url":BASE+name,
                    "processing":"FIRMS country archive","sha256":provenance["sha256"],
                    "bytes":provenance["bytes"],"first_retained_utc":info["first_retained_utc"],
                    "last_retained_utc":info["last_retained_utc"],
                    "original_full_year_count_verified":info["rows"]["retained_pixels"],
                    "fields_schema_type_present":bool(info["rows"]["csv_has_type"])})
                print("SCI03 HIST",year,source,"year count",info["rows"]["retained_pixels"],
                    "Jan-Oct",sum(v for k,v in counts.items() if k[1]<=10),flush=True)
            finally:
                file.unlink(missing_ok=True)
    out["data"]=encode(cells)
    out["status"]="historical_verified"
    return out

def recent():
    shape,geo_sha=geometry()
    key=os.environ.get("FIRMS_MAP_KEY","")
    if not key: raise ValueError("FIRMS_MAP_KEY secret missing; cannot fetch 2026")
    available,inventory=availability(key)
    bb=",".join(f"{v:.4f}" for v in get_bbox(shape))
    out={"id":"SCI-03","source":"NASA FIRMS Area API","period":"2026-01-01 to 2026-10-31 (complete months UTC)",
      "processing":"SP preferred; NRT only on dates not covered by SP",
      "geometry_sha256":geo_sha,"availability":{"products":{p:available.get(p)
         for p in ("MODIS_SP","MODIS_NRT","VIIRS_NOAA20_SP","VIIRS_NOAA20_NRT")},
         "manifest_sha256":inventory["sha256"],"retrieved_at_utc":inventory["retrieved_at_utc"]},
      "windows":[],"data":[],"status":"not_started"}
    cells=Counter();failed=False
    for sensor,target in (("MODIS_AQUA","Aqua"),("NOAA20","NOAA20")):
        days={d:v for d,v in day_sources(available,sensor).items() if START<=d<=END}
        windows,missing=contiguous_windows(days)
        if missing:raise ValueError(f"2026 unavailable {sensor} dates: {len(missing)}")
        processed_days=set()
        for idx,w in enumerate(windows):
            # safe_request does not expose MAP_KEY in errors.
            url=f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/{key}/{w['product']}/{bb}/{w['days']}/{w['first']}"
            content,_=safe_request(url)
            meta,daily,grid=validate_chunk(content,w["product"],"modis" if sensor=="MODIS_AQUA" else "viirs-jpss1",shape,w)
            dates={dt.date.fromisoformat(w["first"])+dt.timedelta(days=j) for j in range(w["days"])}
            if processed_days.intersection(dates):raise ValueError("duplicate date in source selection")
            processed_days.update(dates)
            for (month,lat,lon),value in grid.items():
                cells[(2026,month,target,lat,lon)]+=value
            out["windows"].append({
                "sensor":sensor,"start":w["first"],"end":w["last"],
                "processing":w["processing"],"product":w["product"],
                "source_template":f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/[MAP_KEY]/{w['product']}/{bb}/{w['days']}/{w['first']}",
                "sha256":meta["sha256"],"response_bytes":meta["response_bytes"],
                "csv_columns":meta["csv_columns"],"type_present":meta["has_type_field"],
                "counts":meta["counts"],"success":True
            })
            if idx==0 or (idx+1)%12==0 or idx==len(windows)-1:
                print("SCI03 API",sensor,idx+1,"/",len(windows),w["first"],w["processing"],flush=True)
        if len(processed_days)!=(END-START).days+1:
            raise ValueError("incomplete year sensor API date windows")
    out["data"]=encode(cells)
    out["status"]="all_2026_jan_oct_windows_downloaded"
    out["limits"]=["The presence of a query response is not cloud-free overpass coverage.",
         "NRT data lacks type field in observed responses; historical/SP quality filter cannot be guaranteed identical.",
         "Preliminary observations may be later replaced by SP.",
         "2026-11 is intentionally excluded as incomplete.",
         "Exact duplicate filtering for 2026 source follows existing TEST-01B and may differ from historical full-file processing."]
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("mode",choices=("historical","recent"))
    p.add_argument("--out",required=True)
    args=p.parse_args()
    result=historical() if args.mode=="historical" else recent()
    target=Path(args.out);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print("SCI03 SAVED",target,"status",result["status"],
          "count",sum(row[-1] for row in result["data"]),flush=True)
if __name__=="__main__":main()

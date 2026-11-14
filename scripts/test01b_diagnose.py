#!/usr/bin/env python3
"""TEST-01B/A: independent 2025 WAPE decomposition from six NASA FIRMS annual CSVs.
Inputs are downloaded afresh; original TEST-01 files are never modified.
Stdlib only. Use python -m scripts.test01b_diagnose --output /tmp/test01b_a.json.
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from scripts.test01_historico import BASE, valid_sensor, timestamp, download
from scripts.firms_nrt import extract_geometry, get_bbox, point_in_geometry

SENSORS=("modis","viirs-jpss1")
YEARS=(2023,2024,2025)

def ingest_csv(path, sensor, year, shape, cells, matched_period):
    """Count each source row exactly once; no collapse of distinct fire pixels."""
    bbox=get_bbox(shape)
    counters=Counter()
    date_min=date_max=None
    with path.open(encoding="utf-8-sig",newline="") as stream:
        reader=csv.DictReader(stream)
        required={"latitude","longitude","acq_date","acq_time","daynight","confidence","satellite"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Unexpected schema: "+",".join(sorted(required-set(reader.fieldnames or []))))
        counters["has_type_field"]=int("type" in reader.fieldnames)
        for row in reader:
            counters["raw_rows"]+=1
            if not valid_sensor(row,sensor):
                counters["excluded_type_daynight_confidence_sensor"]+=1
                continue
            try:
                lat,lon=float(row["latitude"]),float(row["longitude"])
                when=timestamp(row)
                if not all(map(math.isfinite,(lat,lon))) or when.year!=year:
                    raise ValueError("invalid")
            except (ValueError,TypeError,OverflowError,KeyError):
                counters["invalid_or_wrong_year"]+=1
                continue
            if not (bbox[0]<=lon<=bbox[2] and bbox[1]<=lat<=bbox[3]):
                counters["outside_bbox"]+=1
                continue
            if not point_in_geometry(lon,lat,shape):
                counters["outside_polygon"]+=1
                continue
            name="Aqua" if sensor=="modis" else "NOAA20"
            cells[(year,when.month,name,math.floor(lat),math.floor(lon))]+=1
            counters["retained_pixels"]+=1
            date_min=when if date_min is None else min(date_min,when)
            date_max=when if date_max is None else max(date_max,when)
            # Same observation window for exploratory 2026 Jan1-Nov14 comparisons.
            if (when.month,when.day)<=(11,14):
                matched_period[(year,when.month,when.day,name)]+=1
    return dict(counters),date_min.isoformat() if date_min else None,date_max.isoformat() if date_max else None

def fit(cells,train):
    # Year-held-out ratio of original detections: no year in test is used.
    sums=Counter()
    for (y,month,s,lat,lon),v in cells.items():
        if y in train: sums[s]+=v
    if sums["NOAA20"]==0: raise ValueError("No VIIRS training denominator")
    return sums["Aqua"]/sums["NOAA20"]

def score(cells,train,test):
    coef=fit(cells,train)
    keys={(month,lat,lon) for (y,month,s,lat,lon) in cells if y==test}
    sums=Counter()
    by_month=defaultdict(lambda:Counter())
    by_cell=defaultdict(lambda:Counter())
    by_cell_month=[]
    for month,lat,lon in sorted(keys):
        mod=cells.get((test,month,"Aqua",lat,lon),0)
        viirs=cells.get((test,month,"NOAA20",lat,lon),0)
        scaled=coef*viirs
        rawerror=abs(mod-viirs)
        error=abs(mod-scaled)
        bias=scaled-mod
        for agg in (sums,by_month[month],by_cell[(lat,lon)]):
            agg["modis"]+=mod
            agg["viirs"]+=viirs
            agg["predicted"]+=scaled
            agg["error_scaled"]+=error
            agg["error_raw"]+=rawerror
            agg["signed_error_scaled"]+=bias
            agg["cell_month_count"]+=1
        by_cell_month.append((month,lat,lon,mod,viirs,error,bias))
    if sums["modis"]==0:raise ValueError("Zero MODIS holdout denominator")
    totals={"year":test,"training_years":list(train),"factor":round(coef,8),
        "raw_wape":round(sums["error_raw"]/sums["modis"],5),
        "scaled_wape":round(sums["error_scaled"]/sums["modis"],5),
        "modis_pixels":int(sums["modis"]),"noaa20_pixels":int(sums["viirs"]),
        "predicted_pixels":round(sums["predicted"],3),
        "sum_absolute_error_scaled":round(sums["error_scaled"],3),
        "sum_absolute_error_raw":round(sums["error_raw"],3),
        "signed_bias_pred_minus_modis":round(sums["signed_error_scaled"],3),
        "bias_fraction_of_modis":round(sums["signed_error_scaled"]/sums["modis"],5),
        "active_cell_months":sums["cell_month_count"]}
    def decomp(k,acc):
        return {k:int(k) if isinstance(k,int) else k,
                "modis":int(acc["modis"]),"noaa20":int(acc["viirs"]),
                "predicted":round(acc["predicted"],2),
                "abs_error":round(acc["error_scaled"],2),
                "signed_bias":round(acc["signed_error_scaled"],2),
                "wape_contribution_percentage_points":round(100*acc["error_scaled"]/sums["modis"],3),
                "share_of_absolute_error_pct":round(100*acc["error_scaled"]/sums["error_scaled"],3),
                "active_cell_months":acc["cell_month_count"]}
    months=[decomp("month",v)|{"month":m} for m,v in sorted(by_month.items())]
    spatial=[decomp("cell",v)|{"latitude_cell_south":lat,"longitude_cell_west":lon}
             for (lat,lon),v in sorted(by_cell.items(),key=lambda item:-item[1]["error_scaled"])]
    # Daily-scale root causes are NOT inferred from monthly counts alone.
    return {"totals":totals,"monthly":months,"spatial_top_30":spatial[:30],
        "top_abs_errors_cell_month":[{"month":m,"latitude_cell_south":lat,"longitude_cell_west":lon,
             "modis":int(mod),"noaa20":int(viirs),"abs_error":round(err,2),"signed_bias":round(bias,2)}
             for m,lat,lon,mod,viirs,err,bias in sorted(by_cell_month,key=lambda r:-r[5])[:30]],
        "spatial_error_top_10_share_pct":round(100*sum(v["abs_error"] for v in spatial[:10])/sums["error_scaled"],3),
        "top_3_months_error_share_pct":round(100*sum(m["abs_error"] for m in sorted(months,key=lambda v:-v["abs_error"])[:3])/sums["error_scaled"],3)}

def compute(cache, baseline, output):
    raw_geometry=Path("data/amazonas_ibge.geojson").read_bytes()
    boundary=json.loads(raw_geometry)
    shape=extract_geometry(boundary)
    out={"id":"TEST-01B","investigation":"A","status":"not_evaluated",
         "scientific_scope":"Amazonas, daytime UTC month x 1-degree cell, 2023-2025",
         "source_url":BASE,"source_files":[],
         "geometry_sha256":hashlib.sha256(raw_geometry).hexdigest(),
         "annual_counts":{},"evaluations":[]}
    files_by_pair={(x["year"],x["sensor"]):x for x in baseline["file_inventory"]}
    cells=Counter()
    comparison_period=Counter()
    cache.mkdir(exist_ok=True,parents=True)
    for year in YEARS:
        for sensor in SENSORS:
            url=BASE+f"{sensor}_{year}_Brazil.csv"
            tmp=cache/f"test01b_{year}_{sensor}.csv"
            try:
                meta=download(url,tmp)
                expected=files_by_pair[(year,sensor)].get("sha256")
                if not expected or meta["sha256"]!=expected:
                    raise ValueError("TEST-01 reference SHA differs; do not silently replace baseline")
                stats,first,last=ingest_csv(tmp,sensor,year,shape,cells,comparison_period)
                entry={"year":year,"sensor":sensor,"processing":"yearly country archive (not independently certified SP by metadata)",
                       "url":url,**meta,"status":"verified","first_retained_utc":first,"last_retained_utc":last,
                       "counts":stats,"matches_original_retained_pixels":stats["retained_pixels"]==files_by_pair[(year,sensor)]["rows"]["retained_pixels"]}
                if not entry["matches_original_retained_pixels"]:
                    raise AssertionError("TEST-01 original count mismatch")
                out["source_files"].append(entry)
                print("VERIFIED",year,sensor,stats["retained_pixels"],meta["sha256"][:12],flush=True)
            finally:
                if tmp.exists():tmp.unlink()
    for year in YEARS:
        out["annual_counts"][str(year)]={s:sum(v for (y,m,sens,lat,lon),v in cells.items() if y==year and sens==s)
                                        for s in ("Aqua","NOAA20")}
    for train,test in (((2023,),2024),((2023,2024),2025)):
        out["evaluations"].append(score(cells,train,test))
    for real,existing in zip(out["evaluations"],baseline["holdouts"]):
        if (real["totals"]["year"]!=existing["holdout_year"] or
            abs(real["totals"]["scaled_wape"]-existing["scaled_wape"])>1e-10 or
            abs(real["totals"]["raw_wape"]-existing["raw_wape"])>1e-10):
            raise AssertionError("Original TEST-01 WAPE not reproduced")
    out["historical_same_period_2026_candidate"]={
        str(y):{s:sum(v for (year,mo,day,src),v in comparison_period.items()
                  if y==year and src==s)
                for s in ("Aqua","NOAA20")} for y in YEARS}
    ev2024,ev2025=[x["totals"] for x in out["evaluations"]]
    out["denominator_effect"]={
        "modis_2024":ev2024["modis_pixels"],"modis_2025":ev2025["modis_pixels"],
        "modis_denominator_decline_pct":round(100*(1-ev2025["modis_pixels"]/ev2024["modis_pixels"]),2),
        "abs_error_2024":ev2024["sum_absolute_error_scaled"],
        "abs_error_2025":ev2025["sum_absolute_error_scaled"],
        "abs_error_change_pct":round(100*(ev2025["sum_absolute_error_scaled"]/ev2024["sum_absolute_error_scaled"]-1),2),
        "wape_2025_with_2024_denominator_not_a_valid_cross_year_metric":round(ev2025["sum_absolute_error_scaled"]/ev2024["modis_pixels"],5)}
    out["annual_sensor_ratios"]={
        str(y):{"aqua_per_noaa20":round(out["annual_counts"][str(y)]["Aqua"]/out["annual_counts"][str(y)]["NOAA20"],7),
                "noaa20_per_aqua":round(out["annual_counts"][str(y)]["NOAA20"]/out["annual_counts"][str(y)]["Aqua"],5)}
        for y in YEARS}
    out["status"]="reproduced_and_decomposed"
    out["limits"]=["WAPE is relative to MODIS detections, not true fires.",
        "Calendar 2025 counts are much smaller than 2024 and affect WAPE denominator.",
        "Month/cell error decomposition establishes association, not physical or climate cause.",
        "VIIRS and MODIS cloud/overpass opportunity denominators are unavailable.",
        "Simplified boundary not verified against official IBGE; raw counts preserved."]
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    Path(output).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--cache",type=Path,default=Path(tempfile.gettempdir())/"firelens-test01b")
    p.add_argument("--baseline",type=Path,default=Path("data/test01_historico_amazonas.json"))
    p.add_argument("--output",type=Path,default=Path("/tmp/firelens-test01b-a.json"))
    args=p.parse_args()
    data=compute(args.cache,json.loads(args.baseline.read_text(encoding="utf8")),args.output)
    print("STATUS",data["status"],"WAPES",[(e["totals"]["year"],e["totals"]["scaled_wape"]) for e in data["evaluations"]])
    print("DIAGNOSTIC",data["denominator_effect"])
if __name__=="__main__":main()

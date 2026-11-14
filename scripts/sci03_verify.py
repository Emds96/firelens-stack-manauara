#!/usr/bin/env python3
"""SCI-03 offline verification of published NASA FIRMS snapshot.

Recompute all year/period pattern metrics from the permanently committed
1-degree monthly aggregates. No credentials/network, no original NASA
files, no changes to operational FireLens data.
"""
import json
from pathlib import Path
from scripts.sci03_compare import run

def verify(aggregates_path="data/sci03_agregados.json",
           results_path="data/sci03_resultados.json"):
    a=json.loads(Path(aggregates_path).read_text(encoding="utf8"))
    result=json.loads(Path(results_path).read_text(encoding="utf8"))
    if a.get("id")!="SCI-03" or result.get("id")!="SCI-03":
        raise ValueError("Invalid SCI-03 experiment IDs")
    source_rows=a.get("rows",[])
    expected_cols=["year","month","sensor","cell_south_lat","cell_west_lon","pixels"]
    if a.get("columns")!=expected_cols:
        raise ValueError("Unexpected aggregated schema")
    geo=a["geometry_sha256"]
    if geo!=result["geometry_sha256"]:
        raise ValueError("Geometry hash mismatch")
    historical={
      "status":"historical_verified",
      "geometry_sha256":geo,
      "file_provenance":result["sources"]["historical"],
      "data":[row for row in source_rows if row[0] in (2023,2024,2025)]
    }
    recent={
      "status":"all_2026_jan_oct_windows_downloaded",
      "geometry_sha256":geo,
      "availability":result["sources"]["recent_availability"],
      "windows":result["sources"]["recent_windows"],
      "data":[row for row in source_rows if row[0]==2026]
    }
    if len(historical["data"])+len(recent["data"])!=len(source_rows):
        raise ValueError("Unexpected calendar year in aggregate")
    recomputed=run(historical,recent)
    for key in ("years","cross_year_relative_activity","absolute_count_baseline"):
        if recomputed[key]!=result[key]:
            raise AssertionError("SCI-03 offline metrics mismatch: "+key)
    if abs(recomputed["invariance_demonstrated_max_share_difference"]-
           result["invariance_demonstrated_max_share_difference"])>1e-12:
        raise AssertionError("Global scaling invariance failed")
    source_windows=result["sources"]["recent_windows"]
    if len(source_windows)!=124 or not all(w["success"] for w in source_windows):
        raise AssertionError("Expected 124 successful 2026 source windows")
    if len(result["sources"]["historical"])!=6:
        raise AssertionError("Expected 6 audited annual archives")
    summary={str(y):next(x for x in result["years"]
                         if x["year"]==y and x["period"]=="jan_oct")
                         for y in (2023,2024,2025,2026)}
    return {"status":"offline_verified","rows":len(source_rows),
            "years":{y:{"modis":v["month"]["modis_pixels"],
                        "noaa20":v["month"]["noaa20_pixels"],
                        "spatial_tv":v["spatial"]["total_variation"],
                        "top10_overlap":v["spatial"]["top_overlap"]["intersect_count"]}
                     for y,v in summary.items()}}

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))

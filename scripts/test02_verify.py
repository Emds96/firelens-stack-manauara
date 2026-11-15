#!/usr/bin/env python3
"""Offline independent revalidation of stored TEST-02 NASA rows and classifications.

Requires no MAP_KEY, internet access, or changes to original FireLens datasets.
"""
import hashlib
import json
from pathlib import Path
from scripts.test02_fisico import parse_time, finite, build_analysis, FOCUS_DAY

ROWS=Path("data/test02_observacoes_20261110_14.json")
RESULT=Path("data/test02_resultados.json")

def verify():
    observations=json.loads(ROWS.read_text(encoding="utf8"))
    original=json.loads(RESULT.read_text(encoding="utf8"))
    meta=observations["source_metadata"]
    assert meta==original["sources"],"NASA source metadata not identical"
    assert observations["source_columns_retained"]
    records={}
    all_ids=set()
    for source in ("MODIS_NRT","VIIRS_NOAA20_NRT"):
        arr=observations[source]
        records[source]=arr
        expected=set(meta[source]["csv_columns"])
        assert len(arr)==meta[source]["filter_stats"]["inside_amazonas"]
        assert len(meta[source]["sha256_csv"])==64
        assert "[MAP_KEY]" in meta[source]["url_redacted"]
        for item in arr:
            raw=item["raw_columns"]
            assert set(raw)==expected,("Missing source attribute",item["id"])
            assert item["id"] not in all_ids
            all_ids.add(item["id"])
            assert abs(item["latitude"]-float(raw["latitude"]))<1e-9
            assert abs(item["longitude"]-float(raw["longitude"]))<1e-9
            assert item["scan_km"]==float(raw["scan"])
            assert item["track_km"]==float(raw["track"])
            assert item["frp_mw"]==finite(raw,"frp")
            assert item["t4_k"]==finite(raw,"brightness" if source=="MODIS_NRT" else "bright_ti4")
            assert item["t11_k"]==finite(raw,"bright_t31" if source=="MODIS_NRT" else "bright_ti5")
            t=parse_time(raw)
            assert t.isoformat().replace("+00:00","Z")==item["time_utc"]
            assert item["area_km2_approx"]==round(item["scan_km"]*item["track_km"],6)
    recalculated=build_analysis(records["MODIS_NRT"],
                                records["VIIRS_NOAA20_NRT"],
                                meta,original["geometry_sha256"])
    keys=("daily","group_diagnostics","pair_diagnostics_2026_11_11",
          "examples_2026_11_11","viirs_multi_MODIS_spatiotemporal_overlap_count",
          "total_modis_rows","total_viirs_rows")
    for key in keys:
        if recalculated[key]!=original[key]:
            raise AssertionError("Independent offline mismatch: "+key)
    focus=next(d for d in recalculated["daily"] if d["date_utc"]==FOCUS_DAY)
    assert all(d["all_categories_sum_check"] and d["eligible_categories_sum_check"]
               and d["focus_categories_sum_check"] for d in recalculated["daily"])
    assert focus["eligible_diurnal_modis_aqua"]==12
    assert focus["eligible_diurnal_noaa20"]==222
    assert focus["four_locks_candidate_groups_8k"]==0
    hash_rows=hashlib.sha256(ROWS.read_bytes()).hexdigest()
    hash_result=hashlib.sha256(RESULT.read_bytes()).hexdigest()
    return {"status":"offline_recomputed_exactly",
            "stored_nasa_rows":{"MODIS":len(records["MODIS_NRT"]),
                                "NOAA20":len(records["VIIRS_NOAA20_NRT"])},
            "eligible_11nov":{"aqua":12,"noaa20":222},
            "candidate_11nov":0,
            "pairs_11nov":len(original["pair_diagnostics_2026_11_11"]),
            "raw_json_sha256":hash_rows,"results_sha256":hash_result,
            "note":"Verifies internal reproducibility, not unique physical fire identity."}

if __name__=="__main__":
    print(json.dumps(verify(),ensure_ascii=False,indent=2))

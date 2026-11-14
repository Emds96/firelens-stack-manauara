"""TEST-01B reproducibility and source-separation unit tests (synthetic records)."""
import datetime as dt
import io
import unittest
from collections import Counter
from unittest.mock import patch
from scripts.test01b_diagnose import fit,score,ingest_csv
from scripts.test01b_2026 import day_sources,contiguous_windows,validate_chunk,SENSORS,START,END

class Test01B(unittest.TestCase):
    def test_2024_2025_holdouts_without_leakage(self):
        cells=Counter({
            (2023,8,"Aqua",-3,-60):10,(2023,8,"NOAA20",-3,-60):40,
            (2024,8,"Aqua",-3,-60):30,(2024,8,"NOAA20",-3,-60):120,
            (2025,8,"Aqua",-3,-60):5,(2025,8,"NOAA20",-3,-60):100})
        assert fit(cells,(2023,))==.25
        a=score(cells,(2023,2024),2025)
        self.assertEqual(a["totals"]["factor"],.25)
        self.assertEqual(a["totals"]["modis_pixels"],5)
        self.assertEqual(a["totals"]["predicted_pixels"],25)
        self.assertEqual(a["totals"]["sum_absolute_error_scaled"],20)
        self.assertEqual(a["totals"]["signed_bias_pred_minus_modis"],20)
        cells[(2025,8,"Aqua",-3,-60)]=5000
        self.assertEqual(score(cells,(2023,2024),2025)["totals"]["factor"],.25)
    def test_month_and_cell_error_sums_equal_totals(self):
        cells=Counter({(2023,8,"Aqua",-3,-60):4,(2023,8,"NOAA20",-3,-60):8,
        (2024,1,"Aqua",-3,-60):2,(2024,1,"NOAA20",-3,-60):3,
        (2024,8,"Aqua",-4,-61):5,(2024,8,"NOAA20",-4,-61):11})
        result=score(cells,(2023,),2024)
        v=result["totals"]["sum_absolute_error_scaled"]
        self.assertAlmostEqual(sum(m["abs_error"] for m in result["monthly"]),v,places=1)
        self.assertAlmostEqual(sum(c["abs_error"] for c in result["spatial_top_30"]),v,places=1)
        self.assertEqual(result["totals"]["active_cell_months"],2)
    def test_2026_sp_preferred_nrt_fills_non_overlap(self):
        av={"MODIS_SP":{"min_date":"2026-01-01","max_date":"2026-07-31"},
            "MODIS_NRT":{"min_date":"2026-07-01","max_date":"2026-11-14"}}
        days=day_sources(av,"MODIS_AQUA")
        self.assertEqual(days[dt.date(2026,7,15)],("standard","MODIS_SP"))
        self.assertEqual(days[dt.date(2026,8,1)],("nrt","MODIS_NRT"))
        self.assertEqual(days[START],("standard","MODIS_SP"))
        windows,missing=contiguous_windows(days)
        self.assertEqual(len(missing),0)
        self.assertTrue(all(1<=w["days"]<=5 for w in windows))
        self.assertEqual(sum(w["days"] for w in windows),(END-START).days+1)
        self.assertEqual(len({(w["first"],w["product"]) for w in windows}),len(windows))
    def test_2026_gap_not_relabelled_as_zero(self):
        av={"VIIRS_NOAA20_SP":{"min_date":"2026-01-10","max_date":"2026-02-01"}}
        days=day_sources(av,"NOAA20")
        windows,missing=contiguous_windows(days)
        self.assertIn("2026-01-01",missing)
        self.assertIn("2026-11-14",missing)
        self.assertEqual(sum(w["days"] for w in windows),23)
    def test_empty_or_invalid_schema_rejected(self):
        shape={"type":"Polygon","coordinates":[[[-61,-5],[-59,-5],[-59,-2],[-61,-2],[-61,-5]]]}
        w={"first":"2026-08-01","last":"2026-08-02","days":2}
        with self.assertRaises(ValueError):
            validate_chunk(b"<html>bad</html>","MODIS_SP","modis",shape,w)
        with self.assertRaises(ValueError):
            validate_chunk(b"latitude,longitude\n-3,-60","MODIS_SP","modis",shape,w)
    def test_source_filter_date_and_exact_duplicate(self):
        shape={"type":"Polygon","coordinates":[[[-61,-5],[-59,-5],[-59,-2],[-61,-2],[-61,-5]]]}
        header="latitude,longitude,acq_date,acq_time,satellite,confidence,daynight,type\n"
        source="-3,-60,2026-08-01,1400,Aqua,80,D,0\n"
        payload=(header+source+source+"-3,-60,2026-08-03,1400,Aqua,80,D,0\n"+
                 "-9,-60,2026-08-01,1400,Aqua,80,D,0\n").encode()
        r,days,cells=validate_chunk(payload,"MODIS_SP","modis",shape,{"first":"2026-08-01","last":"2026-08-02"})
        self.assertEqual(r["counts"]["retained"],1)
        self.assertEqual(r["counts"]["duplicate_exact"],1)
        self.assertEqual(r["counts"]["outside_dates"],1)
        self.assertEqual(r["counts"]["outside_state"],1)
        self.assertEqual(sum(days.values()),1)
    def test_satellite_noaa21_not_used_as_noaa20(self):
        self.assertNotIn("VIIRS_NOAA21_NRT",sum(([v["standard"],v["nrt"]] for v in SENSORS.values()),[]))

if __name__=="__main__":unittest.main()

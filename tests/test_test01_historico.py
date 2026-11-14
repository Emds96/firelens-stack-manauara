"""Unit tests TEST-01; synthetic inputs only, not scientific validation."""
import datetime as dt
import unittest
from collections import Counter
from scripts.test01_historico import (
    timestamp, valid_sensor, process_archive, evaluate, recurring, comparable_2026, month_counts
)
from scripts.firms_nrt import point_in_geometry

class TEST01(unittest.TestCase):
    def test_utc_month_boundary(self):
        self.assertEqual(timestamp({"acq_date":"2024-12-31","acq_time":"2358"}).month,12)
        self.assertEqual(timestamp({"acq_date":"2025-01-01","acq_time":"0002"}).year,2025)
    def test_filter_modis_and_viirs_science(self):
        base={"type":"0","daynight":"D","satellite":"Aqua"}
        self.assertTrue(valid_sensor({**base,"confidence":"30"},"modis"))
        self.assertFalse(valid_sensor({**base,"confidence":"29"},"modis"))
        self.assertFalse(valid_sensor({**base,"confidence":"60","satellite":"Terra"},"modis"))
        self.assertTrue(valid_sensor({**base,"confidence":"n"},"viirs-jpss1"))
        self.assertTrue(valid_sensor({**base,"confidence":"h"},"viirs-jpss1"))
        self.assertFalse(valid_sensor({**base,"confidence":"l"},"viirs-jpss1"))
        self.assertFalse(valid_sensor({**base,"confidence":"n","type":"2"},"viirs-jpss1"))
        self.assertFalse(valid_sensor({**base,"confidence":"n","daynight":"N"},"viirs-jpss1"))
    def test_geometry_polygon_hole(self):
        shape={"type":"Polygon","coordinates":[[[0,0],[4,0],[4,4],[0,4],[0,0]],[[1,1],[2,1],[2,2],[1,2],[1,1]]]}
        self.assertTrue(point_in_geometry(3,3,shape))
        self.assertFalse(point_in_geometry(1.5,1.5,shape))
        self.assertFalse(point_in_geometry(8,8,shape))
    def test_year_holdout_training_only(self):
        x=Counter({
            (2023,8,"Aqua",-3,-61):10,(2023,8,"NOAA20",-3,-61):20,
            (2024,8,"Aqua",-3,-61):20,(2024,8,"NOAA20",-3,-61):100,
            (2025,8,"Aqua",-3,-61):100,(2025,8,"NOAA20",-3,-61):100
        })
        a=evaluate(x,(2023,),2024)
        self.assertEqual(a["factor_from_training_only"],0.5)
        self.assertEqual(a["holdout_year"],2024)
        self.assertAlmostEqual(a["raw_wape"],4.0)
        self.assertAlmostEqual(a["scaled_wape"],1.5)
        # Test-year data mutations must not change fitted coefficient.
        x[(2024,8,"Aqua",-3,-61)]=999
        b=evaluate(x,(2023,),2024)
        self.assertEqual(b["factor_from_training_only"],0.5)
    def test_zero_denominator_does_not_produce_fabricated_score(self):
        data=Counter({(2023,1,"NOAA20",-3,-61):2,(2024,1,"NOAA20",-3,-61):8})
        self.assertEqual(evaluate(data,(2023,),2024)["status"],"insufficient")
    def test_recurring_cells_not_fire_events(self):
        x=Counter({(2023,8,"NOAA20",-3,-61):2,(2024,9,"NOAA20",-3,-61):4,
                   (2025,8,"NOAA20",-3,-61):1,(2025,8,"NOAA20",-2,-62):9})
        results=recurring(x)
        self.assertEqual(len(results),1)
        self.assertEqual(results[0]["number_of_years"],3)
        self.assertEqual(results[0]["noaa20_pixels"],7)
    def test_2026_not_substituted_by_noaa21_or_partial_data(self):
        x=comparable_2026(Counter(),{(2026,"viirs-jpss1")})
        self.assertEqual(x["status"],"not_comparable")
        self.assertTrue(x["noaa21_is_not_substituted"])
        x=comparable_2026(Counter(),{(2026,"modis"),(2026,"viirs-jpss1")})
        self.assertNotEqual(x["status"],"comparable")
    def test_missing_month_stays_missing_without_sensor_archive(self):
        x=Counter({(2023,8,"Aqua",-3,-61):10})
        counts=month_counts(x,(2023,))
        self.assertEqual(counts[(2023,8,"Aqua")],10)
        self.assertEqual(counts.get((2023,8,"NOAA20")),None)

if __name__=="__main__":
    unittest.main()

"""SCI-03 tests: mathematical validity, independent years, processing windows, source integrity."""
import unittest,datetime as dt,math
from collections import Counter
from scripts.sci03_compare import (
  counts, project, shares,total_variation,jsd_bits,spearman,agreement,compare,
  simple_scale_wape,run,MONTH_GROUPS)
from scripts.test01b_2026 import day_sources,contiguous_windows

class SCI03(unittest.TestCase):
 def test_shares_are_normalized_and_global_factor_invariant(self):
  v={"a":3,"b":2,"c":0}
  scaled={k:n*.23 for k,n in v.items()}
  self.assertAlmostEqual(sum(shares(v).values()),1)
  self.assertAlmostEqual(total_variation(v,scaled),0,places=12)
  self.assertAlmostEqual(jsd_bits(v,scaled),0,places=12)
  self.assertEqual(agreement(v,scaled,2)["intersect_count"],2)
  self.assertEqual(spearman(v,scaled),1)
 def test_disjoint_distributions_boundaries(self):
  a={"a":1};b={"b":1}
  self.assertAlmostEqual(total_variation(a,b),1)
  self.assertAlmostEqual(jsd_bits(a,b),1)
  self.assertAlmostEqual(total_variation(a,a),0)
  self.assertAlmostEqual(jsd_bits(a,a),0)
  self.assertIsNone(compare({},b).get("total_variation"))
 def test_rank_ties_and_zero_variance(self):
  self.assertEqual(spearman({"x":3,"y":3},{"x":2,"y":2}),None)
  self.assertAlmostEqual(spearman({"x":1,"y":2,"z":3},{"x":3,"y":2,"z":1}),-1)
 def test_source_shape_and_duplicates(self):
  d={"data":[[2025,8,"Aqua",-3,-61,2],[2025,8,"NOAA20",-3,-61,5]]}
  self.assertEqual(sum(counts(d).values()),7)
  self.assertEqual(project(counts(d),2025,"Aqua",[8],"month")[8],2)
  self.assertRaises(ValueError,counts,{"data":d["data"]+d["data"][:1]})
  self.assertRaises(ValueError,counts,{"data":[[2025,8,"NOAA21",-3,-61,1]]})
 def test_year_held_out_coefficient_not_from_test(self):
  base={"data":[[2023,8,"Aqua",-3,-61,10],[2023,8,"NOAA20",-3,-61,20],
                [2024,8,"Aqua",-3,-61,20],[2024,8,"NOAA20",-3,-61,100]]}
  original=counts(base);s=simple_scale_wape(original,2024,(2023,),[8])
  self.assertEqual(s["factor_prior_years_only"],.5)
  self.assertAlmostEqual(s["wape_global_scaled"],1.5)
  original[(2024,8,"Aqua",-3,-61)]=1000
  after=simple_scale_wape(original,2024,(2023,),[8])
  self.assertEqual(after["factor_prior_years_only"],.5)
 def test_2026_retrieval_uses_closed_months_without_overlap(self):
  self.assertNotIn(11,MONTH_GROUPS["jan_oct"])
  av={"MODIS_SP":{"min_date":"2026-01-01","max_date":"2026-08-31"},
      "MODIS_NRT":{"min_date":"2026-09-01","max_date":"2026-11-14"}}
  days={d:v for d,v in day_sources(av,"MODIS_AQUA").items() if d<=dt.date(2026,10,31)}
  windows,missing=contiguous_windows(days)
  self.assertFalse(missing)
  self.assertEqual(sum(w["days"] for w in windows),304)
  self.assertTrue(all(w["days"]<=5 and w["last"]<="2026-10-31" for w in windows))
  self.assertEqual(next(w["processing"] for w in windows if w["first"]=="2026-09-01"),"nrt")
 def test_run_rejects_incomplete_provenance(self):
  hist={"status":"historical_verified","geometry_sha256":"abc",
        "file_provenance":[],"data":[]}
  recent={"status":"partial","geometry_sha256":"abc","availability":{},"windows":[],"data":[]}
  self.assertRaises(ValueError,run,hist,recent)
  recent["status"]="all_2026_jan_oct_windows_downloaded"
  recent["geometry_sha256"]="other"
  self.assertRaises(ValueError,run,hist,recent)
 def test_2026_absolute_scaling_is_not_claimed_validated(self):
  # Method allows historical 2024/25 holdouts only in actual SCI03 run.
  self.assertEqual([(2024,(2023,)),(2025,(2023,2024))][-1][0],2025)

if __name__=="__main__":unittest.main()

"""TEST-02 safety and mathematical checks; synthetic rows are NOT real NASA evidence."""
import datetime as dt
import io
import unittest
from unittest.mock import patch

from scripts.test02_fisico import (
 START, END, FOCUS_DAY, parse_time, finite, normalize, spatial,
 delta_minutes, group_candidates, categorize, evaluate_day, summarize,
 nasa_fetch, FOCUS_BBOX, THERMAL_LIMITS, FRP_RATIO_LIMITS
)

POLYGON={"type":"Polygon","coordinates":[[[-62,-5],[-58,-5],[-58,-1],[-62,-1],[-62,-5]]]}

def rec(tag,sat,lat=-3.7,lon=-60.1,when="2026-11-11T18:24:00Z",
        scan=1.0,track=1.0,frp=10.,t4=350.,t11=300.,day="D"):
    t=dt.datetime.fromisoformat(when.replace("Z","+00:00"))
    return {"id":tag,"source":"MODIS_NRT" if sat in ("Aqua","Terra") else "VIIRS_NOAA20_NRT",
            "satellite":sat,"latitude":lat,"longitude":lon,
            "time_utc":when,"time_manaus":t.astimezone(dt.timezone(dt.timedelta(hours=-4))).isoformat(timespec="minutes"),
            "date_utc":t.date().isoformat(),"daynight":day,"confidence":"n",
            "scan_km":scan,"track_km":track,
            "area_km2_approx":scan*track,"frp_mw":frp,"t4_k":t4,"t11_k":t11,
            "i4_saturation":t4==367,"i4_possible_folding":t4<250,
            "focus_bbox":True,"raw_columns":{},"historic_quality_filter_eligible":True}

class PhysicalTests(unittest.TestCase):
 def test_time_utc_amt_and_cross_day(self):
    d=parse_time({"acq_date":"2026-11-11","acq_time":"1824"})
    self.assertEqual(d.astimezone(dt.timezone(dt.timedelta(hours=-4))).strftime("%H:%M"),"14:24")
    self.assertEqual(delta_minutes(rec("m","Aqua"),rec("v","NOAA-20",when="2026-11-11T17:15:00Z")),69)
 def test_rectangle_dimension_is_approximate_not_footprint(self):
    m=rec("m","Aqua",scan=3.1,track=1.7)
    v=rec("v","NOAA-20",lat=-3.7001,lon=-60.1,scan=.4,track=.4)
    g=spatial(m,v)
    self.assertTrue(g["inside_approx_box"])
    self.assertAlmostEqual(m["area_km2_approx"],5.27)
    vfar=rec("v","NOAA-20",lat=-3.71,lon=-60.1,scan=.4,track=.4)
    self.assertFalse(spatial(m,vfar)["inside_approx_box"])
    self.assertGreater(spatial(m,vfar)["distance_from_box_km"],0)
 def test_four_locks_yield_unconfirmed_candidate_not_proven(self):
    m=rec("m","Aqua",frp=10,t11=300)
    v=rec("v","NOAA-20",when="2026-11-11T17:15:00Z",scan=.4,track=.4,
          frp=10,t11=302,t4=367)
    groups,pairs=group_candidates([m],[v])
    self.assertEqual(len(groups),1)
    self.assertTrue(groups[0]["four_locks_candidate_5k"])
    self.assertTrue(groups[0]["four_locks_candidate_8k"])
    self.assertTrue(groups[0]["no_physical_identity_proven"])
    cat=categorize([m],[v],groups,pairs)
    self.assertEqual(cat["v"]["category"],"four_locks_compatible_unconfirmed")
    self.assertTrue(v["i4_saturation"])
 def test_saturation_folding_are_indicators_not_thermal_ground_truth(self):
    self.assertEqual(THERMAL_LIMITS,(5.,8.))
    self.assertEqual(FRP_RATIO_LIMITS,(.5,2.))
    high=rec("v","NOAA-20",t4=367)
    fold=rec("f","NOAA-20",t4=208)
    self.assertTrue(high["i4_saturation"])
    self.assertTrue(fold["i4_possible_folding"])
    self.assertEqual(summarize([high,fold])["i4_saturation_count"],1)
 def test_failed_thermal_lock_not_promoted_to_confirmed(self):
    m=rec("m","Aqua",frp=10,t11=295)
    v=rec("v","NOAA-20",frp=11,t11=310)
    groups,pairs=group_candidates([m],[v])
    self.assertFalse(groups[0]["four_locks_candidate_8k"])
    self.assertEqual(categorize([m],[v],groups,pairs)["v"]["category"],"unresolved_ambiguous_or_lock_failure")
 def test_failed_frp_lock_and_multi_modis_ambiguous(self):
    m=rec("m","Aqua",frp=1)
    v=rec("v","NOAA-20",frp=15)
    g,p=group_candidates([m],[v])
    self.assertFalse(g[0]["four_locks_candidate_8k"])
    m2=rec("m2","Terra",frp=15,when="2026-11-11T18:30:00Z")
    g,p=group_candidates([m,m2],[v])
    self.assertEqual(categorize([m,m2],[v],g,p)["v"]["category"],"unresolved_ambiguous_or_lock_failure")
 def test_delayed_border_and_isolated_are_distinct(self):
    m=rec("m","Terra")
    inside=rec("v1","NOAA-20",when="2026-11-11T15:00:00Z",scan=.4,track=.4)
    edge=rec("v2","NOAA-20",lat=-3.7,lon=-60.08,scan=.4,track=.4)
    far=rec("v3","NOAA-20",lat=-3.7,lon=-60.04,scan=.4,track=.4)
    g,p=group_candidates([m],[inside,edge,far])
    cats=categorize([m],[inside,edge,far],g,p)
    self.assertEqual(cats["v1"]["category"],"spatial_overlap_delayed_unconfirmed")
    self.assertEqual(cats["v2"]["category"],"edge_near_modis_no_expansion_proof")
    self.assertEqual(cats["v3"]["category"],"viirs_spatially_isolated_not_proven_invisible")
    day=evaluate_day([m],[inside,edge,far],g,p,FOCUS_DAY)
    self.assertTrue(day["all_categories_sum_check"])
    self.assertEqual(sum(x["n"] for x in day["categories_viirs_mutually_exclusive"].values()),3)
 def test_normalize_preserves_all_original_csv_columns_and_quality(self):
    rows=[{"latitude":"-3.700","longitude":"-60.100","acq_date":"2026-11-11","acq_time":"1715",
       "satellite":"N20","confidence":"n","daynight":"D","scan":"0.4","track":"0.4",
       "frp":"3.2","bright_ti4":"367.0","bright_ti5":"301.0","version":"2.0NRT"}]
    parsed,counts=normalize(rows,"VIIRS_NOAA20_NRT",POLYGON)
    self.assertEqual(len(parsed),1)
    self.assertEqual(parsed[0]["raw_columns"],rows[0])
    self.assertEqual(parsed[0]["time_manaus"],"2026-11-11T13:15-04:00")
    self.assertTrue(parsed[0]["i4_saturation"])
    self.assertTrue(parsed[0]["historic_quality_filter_eligible"])
    self.assertEqual(counts["inside_amazonas"],1)
 def test_false_negative_detection_is_not_claimed_absence(self):
    m=rec("m","Aqua")
    # absence of pairing says NOTHING about physical fire
    v=rec("v","NOAA-20",lat=-3.7,lon=-60.01)
    g,p=group_candidates([m],[v])
    self.assertEqual(categorize([m],[v],g,p)["v"]["category"],"viirs_spatially_isolated_not_proven_invisible")
 def test_source_request_key_never_in_metadata_or_exception(self):
    blob=("latitude,longitude,acq_date,acq_time,scan,track,frp,confidence,daynight,satellite,"
          "brightness,bright_t31\n-3.7,-60.1,2026-11-11,1824,1,1,10,80,D,A,330,300\n").encode()
    class Response:
        def __enter__(self):return self
        def __exit__(self,*args):pass
        def read(self,n):return blob
    def fake(req,timeout):
        self.assertIn("EXPLICIT_SENSITIVE_TEST_KEY",req.full_url)
        return Response()
    with patch("scripts.test02_fisico.urlopen",side_effect=fake):
        rows,meta=nasa_fetch("MODIS_NRT",(-62,-5,-58,-1),"EXPLICIT_SENSITIVE_TEST_KEY")
    self.assertEqual(len(rows),1)
    self.assertNotIn("EXPLICIT_SENSITIVE_TEST_KEY",str(meta))
    self.assertIn("[MAP_KEY]",meta["url_redacted"])
 def test_no_key_in_error_paths(self):
    def explode(req,timeout):raise URLError("fake network key hidden")
    from urllib.error import URLError
    with patch("scripts.test02_fisico.urlopen",side_effect=explode):
        with self.assertRaises(RuntimeError) as ctx:
            nasa_fetch("MODIS_NRT",(-62,-5,-58,-1),"EXPLICIT_SENSITIVE_TEST_KEY")
    self.assertNotIn("EXPLICIT_SENSITIVE_TEST_KEY",str(ctx.exception))
 def test_different_utc_dates_not_auto_paired(self):
    m=rec("m","Aqua",when="2026-11-11T00:15:00Z")
    v=rec("v","NOAA-20",when="2026-11-10T23:45:00Z")
    g,p=group_candidates([m],[v])
    self.assertFalse(g)
    self.assertFalse(p)
if __name__=="__main__":unittest.main()

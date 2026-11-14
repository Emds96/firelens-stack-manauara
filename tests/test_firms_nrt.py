import datetime as dt
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts import firms_nrt as f

UTC=dt.timezone.utc
SQUARE={'type':'Polygon','coordinates':[[[-74,-10],[-56,-10],[-56,2],[-74,2],[-74,-10]]]}

class TestFirms(unittest.TestCase):
    def test_utc_preserves_early_time(self):
        self.assertEqual(f.iso(f.parse_utc('2026-11-14','13')),'2026-11-14T00:13:00Z')
        with self.assertRaises(ValueError): f.parse_utc('2026-11-14','2500')
    def test_bbox_from_geojson(self):
        self.assertEqual(f.get_bbox(SQUARE),(-74.,-10.,-56.,2.))
        feature={'type':'FeatureCollection','features':[{'type':'Feature','geometry':SQUARE,'properties':{}}]}
        self.assertEqual(f.extract_geometry(feature),SQUARE)
        with self.assertRaises(ValueError): f.extract_geometry({'type':'FeatureCollection','features':[]})
    def test_polygon_hole_and_exterior(self):
        shape={'type':'Polygon','coordinates':[[[0,0],[10,0],[10,10],[0,10],[0,0]],[[3,3],[7,3],[7,7],[3,7],[3,3]]]}
        self.assertTrue(f.point_in_geometry(2,2,shape))
        self.assertFalse(f.point_in_geometry(4,4,shape))
        self.assertFalse(f.point_in_geometry(-1,5,shape))
    def test_filters_and_dedup(self):
        good={'latitude':'-3','longitude':'-60','acq_date':'2026-11-14','acq_time':'0130','confidence':'n','daynight':'D'}
        rows=[good,good,{**good,'confidence':'l','latitude':'-4'},{**good,'longitude':'-85'}, {**good,'acq_time':'oops'}]
        kept,excluded=f.process_rows(rows,SQUARE,f.SOURCES[0])
        self.assertEqual(len(kept),1)
        self.assertEqual(excluded,{'outside_amazonas':1,'low_confidence':1,'invalid':1})
        self.assertEqual(kept[0]['observed_at_utc'],'2026-11-14T01:30:00Z')
    def test_success_two_sensors(self):
        row={'latitude':'-3','longitude':'-60','acq_date':'2026-11-14','acq_time':'0130','confidence':'h','daynight':'N'}
        now=dt.datetime(2026,11,14,3,0,tzinfo=UTC)
        payload=f.build_payload('test_secret',SQUARE,fetcher=lambda *_:([row],'ok'),now=now)
        self.assertEqual(payload['status'],'ok')
        self.assertEqual(payload['count'],2)
        self.assertEqual(payload['last_success_utc'],'2026-11-14T03:00:00Z')
        self.assertEqual(payload['last_observation_utc'],'2026-11-14T01:30:00Z')
        self.assertEqual(len(payload['sensors']),2)
        self.assertNotIn('test_secret',json.dumps(payload))
    def test_failure_preserves_previous_snapshot(self):
        prev=f.empty_result()
        prev['detections']=[{'observed_at_utc':'2026-11-14T00:00:00Z'}]
        prev['last_success_utc']='2026-11-13T00:00:00Z'
        def bad(*_): raise RuntimeError('secret_key leaked from server: secret_key')
        res=f.build_payload('secret_key',SQUARE,prev,fetcher=bad,now=dt.datetime(2026,11,14,3,tzinfo=UTC))
        self.assertEqual(res['status'],'unavailable')
        self.assertTrue(res['fallback_snapshot'])
        self.assertIn('desatualizados',' '.join(res['alerts']))
        self.assertNotIn('secret_key',json.dumps(res))
        self.assertEqual(res['last_success_utc'],prev['last_success_utc'])
    def test_without_key_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'recente.json';out.write_text('{"status":"old"}')
            with patch.dict(os.environ,{'FIRMS_MAP_KEY':''}):
                rc=f.main(['--output',str(out),'--boundary',str(Path(tmp)/'missing.json')])
            self.assertEqual(rc,2)
            self.assertEqual(json.loads(out.read_text()),{'status':'old'})

if __name__=='__main__': unittest.main()

import json
import unittest
from pathlib import Path
from scripts.firms_nrt import extract_geometry, get_bbox, point_in_geometry

class TestAmazonasGeometry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.feature=json.loads(Path('data/amazonas_ibge.geojson').read_text(encoding='utf8'))
        cls.geom=extract_geometry(cls.feature)

    def test_estado_e_proveniencia(self):
        p=self.feature['properties']
        self.assertEqual(p['cd_geocuf'], '13')
        self.assertEqual(p['sigla'], 'AM')
        self.assertIn('simplificada', p['source'])

    def test_limites_plausiveis(self):
        w,s,e,n=get_bbox(self.geom)
        self.assertTrue(-75<w<-72)
        self.assertTrue(-11<s<-8)
        self.assertTrue(-58<e<-54)
        self.assertTrue(1<n<4)

    def test_manaus_inside_e_belem_outside(self):
        self.assertTrue(point_in_geometry(-60.0217,-3.1190,self.geom))
        self.assertFalse(point_in_geometry(-48.4902,-1.4558,self.geom))

if __name__=='__main__':
    unittest.main()

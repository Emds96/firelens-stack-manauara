import unittest
from collections import defaultdict
from docs.research import validacao_tradutor1_reproduzivel as original

class TestOriginalBaseline(unittest.TestCase):
    def test_score_uses_modis_reference_not_fires(self):
        result=original.score([5,5,0],[4,6,0])
        self.assertEqual(result['WAPE'],.2)
        self.assertEqual(result['active_cells_month'],2)
    def test_temporal_training_only(self):
        data=defaultdict(int)
        # Global coefficient from training is 5/10 = 0.5; validation must not leak from holdout.
        data[('A','NOAA20','D',2022,1,-9,-65)]=10
        data[('A','Aqua','D',2022,1,-9,-65)]=5
        data[('A','NOAA20','D',2023,1,-9,-65)]=10
        data[('A','Aqua','D',2023,1,-9,-65)]=100
        result=original.evaluate(data,'A','D',[2022],2023)
        self.assertEqual(result['global_coefficient'],.5)
        self.assertEqual(result['methods']['global']['NOAA20_pred_sum'],5.0)

if __name__=='__main__': unittest.main()

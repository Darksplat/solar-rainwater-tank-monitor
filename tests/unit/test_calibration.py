import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
from calibrate import fit
class CalibrationTest(unittest.TestCase):
 def test_known_coefficients(self):
  slope=16*998.2*9.80665/60000
  r=fit([(h,4.03+slope*h) for h in [0.25,0.5,1,2,3,3.8]])
  self.assertAlmostEqual(r['zero_ma'],4.03);self.assertAlmostEqual(r['span_ma'],16)
  self.assertLess(r['max_residual_mm'],1e-8)
 def test_invalid(self):
  for p in [[],[(1,5)]*3,[(0,4),(1,3),(2,2)],[(0,4),(1,float('nan')),(2,9)]]:
   with self.assertRaises(ValueError):fit(p)

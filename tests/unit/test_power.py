import unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'tools'))
from power_budget import budget
class PowerTests(unittest.TestCase):
 def test_autonomy(self):
  b=budget();self.assertGreaterEqual(b['usable_battery_Wh'],b['seven_day_with_margin_Wh'])
 def test_small_panel_deficit(self):
  self.assertLess(budget(panel_w=5)['net_recharge_Wh_day'],0)
 def test_20w_surplus(self):
  self.assertGreater(budget(panel_w=20)['net_recharge_Wh_day'],0)
 def test_no_sun(self):
  self.assertIsNone(budget(sun_hours=0)['recovery_days'])
 def test_continuous_sensor(self):
  self.assertGreater(budget(sensor_seconds=300)['daily_Wh'],budget()['daily_Wh']+10)
 def test_invalid(self):
  for args in [dict(interval=0),dict(sensor_seconds=301),dict(cpu_ma=-1)]:
   with self.assertRaises(ValueError):budget(**args)

 def test_10w_deficit(self):
  self.assertLess(budget(panel_w=10)['net_recharge_Wh_day'],0)
 def test_infinite_input(self):
  with self.assertRaises(ValueError):budget(cpu_ma=float('nan'))

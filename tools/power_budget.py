"""Rev 0.2: component allocations and explicitly unmeasured allowances, at battery terminals."""
import json,math

def budget(cpu_ma=80,sensor_seconds=7,interval=300,charger_ma=20,
           sun_hours=1.5,panel_w=40,battery_ah=20):
 vals=[cpu_ma,sensor_seconds,interval,charger_ma,sun_hours,panel_w,battery_ah]
 if not all(math.isfinite(x) for x in vals) or min(vals)<0 or interval<=0 or sensor_seconds>interval:raise ValueError('invalid power inputs')
 buck=.85;boost=.8;vbat=12.8
 loads={
  'processor_radio_and_board':3.3*cpu_ma/1000/buck*24,
  'three_INA228_allowance_1mA_each':3.3*.003/buck*24,
  'loop_boost_and_boost_IC':(17.2*.024/boost+3.3*.0023)/buck*sensor_seconds/interval*24,
  'charger_standby':vbat*charger_ma/1000*24,
  'SmartBatteryProtect_BLE_on_1p4mA':vbat*.0014*24,
  'reverse_controller_allowance_200uA':vbat*.0002*24,
  'raw_presence_detector_allowance_150uA':vbat*.00015*24,
  'BMS_allowance_2mA':vbat*.002*24,
  'buck_IQ_allowance_50uA':vbat*.00005*24,
  'reverse_diode_allowance':.7*.04*24,
  'pullups_dividers_LED_allowance':.15,
  'battery_self_discharge_allowance_3pct_month':vbat*battery_ah*.03/30,
 }
 daily=sum(loads.values());required=daily*7*1.25;usable=vbat*battery_ah*.8*.8;harvest=panel_w*sun_hours*.6*(1-1.2/37)
 return dict(loads_Wh_day=loads,daily_Wh=daily,seven_day_with_margin_Wh=required,
  usable_battery_Wh=usable,battery_pass=usable>=required,harvest_Wh_day=harvest,
  net_recharge_Wh_day=harvest-daily,recovery_days=required/(harvest-daily) if harvest>daily else None,
  solar_assumption_PSH=sun_hours,measured=False)

def panel_compatibility():
 # Two series Victron SPM040201200, old-series available stock. No rating is inferred from wattage.
 voc=2*22.6*(1+.0035*(25-(-10)))
 # Vmp coefficient is conservatively approximated from Pmax/Isc coefficients, pending hot I-V test.
 hot_vmp=2*18.5*(1-(.0045+.0004)*(85-25))
 return dict(series_panels=2,unit_W=20,cold_cell_C=-10,cold_Voc_V=voc,charger_limit_V=75,
  hot_cell_C=85,estimated_hot_Vmp_V=hot_vmp-1.2,pv_blocking_diode_allowance_V=1.2,startup_required_V=14.6+5,
  pv_TVS_standoff_V=51,checks_pass=voc<51 and voc<75 and hot_vmp-1.2>19.6,
  hot_Vmp_coefficient_is_estimate=True,part_discontinued_stock_must_be_confirmed=True)
if __name__=='__main__':
 print(json.dumps({'sensitivity':{f'{w}W':budget(panel_w=w) for w in [5,10,20,40]},'panel_voltage':panel_compatibility()},indent=2))

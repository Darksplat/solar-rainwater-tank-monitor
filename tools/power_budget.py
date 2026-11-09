"""Conservative engineering assumptions, not measured load or site irradiation."""
import json, math

def budget(cpu_ma=80, sensor_seconds=7, interval=300, charger_ma=20,
           sun_hours=1.5, panel_w=40, battery_ah=20):
    if not all(math.isfinite(x) for x in [cpu_ma,sensor_seconds,interval,charger_ma,sun_hours,panel_w,battery_ah]) or min(cpu_ma,sensor_seconds,interval,charger_ma,sun_hours,panel_w,battery_ah)<0 or interval<=0 or sensor_seconds>interval:
        raise ValueError('invalid power inputs')
    loads = {
      'processor_radio_and_board': 3.3*cpu_ma/1000/0.85*24,
      'adc': 3.3*0.0003/0.85*24,
      'loop_and_boost': 24*0.024/0.8*sensor_seconds/interval*24,
      'charger_standby': 12.8*charger_ma/1000*24,
      'bms_and_monitors_allowance': 12.8*0.002*24,
      'regulator_quiescent_allowance': 12.8*0.001*24,
    }
    daily=sum(loads.values()); required=daily*7*1.25
    usable=12.8*battery_ah*0.8*0.8 # DoD and cold/aging factors, distinct from design margin
    harvest=panel_w*sun_hours*0.6
    return dict(loads_Wh_day=loads,daily_Wh=daily,seven_day_with_margin_Wh=required,
                usable_battery_Wh=usable,battery_pass=usable>=required,
                harvest_Wh_day=harvest,net_recharge_Wh_day=harvest-daily,
                recovery_days=required/(harvest-daily) if harvest>daily else None,
                solar_assumption_PSH=sun_hours)
if __name__=='__main__':
    print(json.dumps({f'{w}W':budget(panel_w=w) for w in [5,10,20,40]},indent=2))

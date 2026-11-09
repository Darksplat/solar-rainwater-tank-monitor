"""Execute shipped HA Jinja expressions with controlled state fixtures.
Does not emulate HA's trigger timers, registry or automation engine.
"""
import json,math
from pathlib import Path
import yaml
from jinja2 import Environment,StrictUndefined
root=Path(__file__).resolve().parents[2]
automations=yaml.safe_load((root/'home-assistant/automations/power-alerts.yaml').read_text())
env=Environment(undefined=StrictUndefined)
def is_number(x):
 try:return math.isfinite(float(x))
 except (TypeError,ValueError):return False
def render(text,states,elevation=30):
 result=env.from_string(text).render(states=lambda name:states.get(name,'unknown'),state_attr=lambda name,key:elevation,is_number=is_number,is_state=lambda name,value:states.get(name,'unknown')==value)
 return result.strip()=='True'
count=0
for tank in [1,2]:
 prefix=f'sensor.tank_{tank}_'
 solar=next(a for a in automations if a['id']==f'tank_{tank}_possible_solar_failure')['triggers'][0]['value_template']
 state={prefix+'battery_voltage':'12.7',prefix+'battery_current':'0.04',prefix+'solar_input_power':'0.2'}
 assert render(solar,state);count+=1
 assert not render(solar,state,elevation=-5);count+=1
 for field,value in [('battery_current','-0.3'),('battery_voltage','13.6'),('solar_input_power','8'),('solar_input_power','unavailable'),('battery_current','unknown'),('battery_voltage','nan')]:
  modified=dict(state);modified[prefix+field]=value;assert not render(solar,modified),(field,value);count+=1
 monitor=next(a for a in automations if a['id']==f'tank_{tank}_power_monitor_fault')['triggers'][0]['value_template']
 assert not render(monitor,{prefix+'battery_monitor_status':'ok',prefix+'solar_monitor_status':'ok'});count+=1
 assert render(monitor,{prefix+'battery_monitor_status':'i2c_fault',prefix+'solar_monitor_status':'ok'});count+=1
 assert render(monitor,{prefix+'battery_monitor_status':'ok',prefix+'solar_monitor_status':'ok',f'binary_sensor.tank_{tank}_battery_input_fault':'on'});count+=1
combined=yaml.safe_load((root/'home-assistant/templates/tanks.yaml').read_text())[0]['sensor']
for entity in combined:
 available=entity['availability'];assert not render(available,{})
# All published examples must parse and automation IDs must remain distinct.
all_ids=[]
for file in (root/'home-assistant/automations').glob('*.yaml'):
 for automation in yaml.safe_load(file.read_text()):all_ids.append(automation['id'])
assert len(all_ids)==len(set(all_ids))
result={'date':'2026-11-09','jinja_scenario_assertions':count+len(combined),'unique_automation_ids':len(all_ids),'status':'PASS expression fixtures only','HA_runtime':'not tested'}
(root/'tests/test-results/ha-template-validation.json').write_text(json.dumps(result,indent=2))
print('PASS:',count+len(combined),'shipped template scenarios;',len(all_ids),'unique automation IDs; HA runtime untested')

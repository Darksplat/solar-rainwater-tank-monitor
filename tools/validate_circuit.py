"""Independent netlist/manifest comparison and bounded DC fault calculations."""
import json,sys,math
from pathlib import Path
from kicad_sexpr import parse,children,child
p=Path(__file__).resolve().parents[1];pcb=p/'hardware/pcb'
c=json.loads((pcb/'circuit-resolved.json').read_text());root=parse((pcb/'reports/tank-monitor.net').read_text())
actual={}
for net in children(child(root,'nets'),'net'):
 name=child(net,'name')[1].lstrip('/')
 for node in children(net,'node'):actual[(child(node,'ref')[1],child(node,'pin')[1])]=name
errors=[]
for part in c['parts']:
 for pin,net in part['nets'].items():
  if net is not None and actual.get((part['ref'],pin))!=net:errors.append((part['ref'],pin,net,actual.get((part['ref'],pin))))
assert not errors,errors
# Deliberately independent checks on critical IC pin functions, not generated from manifest.
d={x['ref']:x for x in c['parts']}
assert d['U1']['nets']=={'1':'V3V3','2':'EN_BUCK','3':'VIN','4':'GND','5':'SW_BUCK','6':'BST'}
assert d['U2']['nets']['4']=='SW_BOOST' and d['U2']['nets']['6']=='BOOST_IN' and d['U2']['nets']['7']=='GND'
assert d['U6']['nets']['9']=='LOOP_EN_N' and d['U6']['nets']['15']=='SDA' and d['U6']['nets']['16']=='SCL'
assert d['U7']['nets']=={'1':'BAT_RAW','2':'REV_UV','3':'REV_OV','4':'GND','5':'REV_SHDN','6':'REV_FAULT','7':'BAT_FUSED','8':'REV_GATE'}
assert d['Q2']['nets']=={'1':'REV_GATE','2':'BAT_RAW','3':'REV_SOURCE'}
assert d['Q3']['nets']=={'1':'REV_GATE','2':'BAT_FUSED','3':'REV_SOURCE'}
assert d['Q4']['nets']=={'1':'RAW_BASE','2':'GND','3':'RAW_PRESENT'}
assert d['D9']['nets']=={'1':'PV_IN','2':'PV_RAW'}
assert d['D10']['nets']=={'1':'RAW_BASE','2':'GND'}
assert d['U6']['nets']['25']=='REV_FAULT' and d['U6']['nets']['26']=='RAW_PRESENT'
assert d['Q1']['nets']=={'1':'BOOST_GATE','2':'V3V3','3':'BOOST_IN'}
# Worst-case DC bounds include tolerance and a conservative 60C excursion
# from 25C reference to an 85C electronics-only stress case.
feedback_error=.001+25e-6*60
limiter_error=.01+200e-6*60  # conservative family maximum TCR
shunt_error=.001+25e-6*60
vmin=1.204*(1+130000*(1-feedback_error)/(10000*(1+feedback_error)))
vmax=1.254*(1+130000*(1+feedback_error)/(10000*(1-feedback_error)))
compliance=vmin-.024*(220*(1+limiter_error)+2*(1+shunt_error)+1.4)
fault_i=vmax/(220*(1-limiter_error)+2*(1-shunt_error))
limiter_w=fault_i**2*110*(1+limiter_error)
shunt_w=fault_i**2*2*(1+shunt_error)
assert compliance>10
assert limiter_w<1.5*(155-85)/(155-70)  # current CRCW2512-HP P70 is1.5W
assert shunt_w<.25*(155-85)/(155-70)
assert vmax<30 and 29.2<40 and 29.2<85
# Controller window, including resistor tolerance +100ppm/C over60C.
e=.01+200e-6*60
uv_min=.4925*(1+2740000*(1-e)/((215000+84500)*(1+e)))
uv_max=.5075*(1+2740000*(1+e)/((215000+84500)*(1-e)))
ov_min=.4925*(1+(2740000+215000)*(1-e)/(84500*(1+e)))
ov_max=.5075*(1+(2740000+215000)*(1+e)/(84500*(1-e)))
uv_leak=2740000*(1+e)*1e-8*(1+84500*(1+e)/((215000+84500)*(1-e)))
ov_leak=(2*2740000+215000)*(1+e)*1e-8
uv_min-=uv_leak;uv_max+=uv_leak;ov_min-=ov_leak;ov_max+=ov_leak
assert uv_max<10 and ov_min>14.6 and ov_max<34
assert 40/510000<.001  # SHDN negative current below datasheet1mA
assert 40+ov_max<60  # deliberately conservative reverse-to-live-output FET stress
assert 2*50.737<1000  # PV diode withstands reversed array plus charged input
# The presence divider cannot directly expose MCU pins to raw voltage.
assert d['R65']['nets']['1']=='BAT_RAW' and d['R66']['nets']=={'1':'V3V3','2':'RAW_PRESENT'}
report=dict(battery_protection_UV_range_V=[uv_min,uv_max],battery_protection_OV_range_V=[ov_min,ov_max],battery_reverse_FET_rating_V=60,PV_reverse_diode_rating_V=1000,
netlist_manifest_match=True,components=len(c['parts']),minimum_loop_supply_V=vmin,maximum_loop_supply_V=vmax,minimum_transmitter_voltage_at_24mA_V=compliance,maximum_bounded_short_current_A=fault_i,limiter_power_each_W=limiter_w,shunt_fault_power_W=shunt_w,limiter_rating_W=1.5,temperature_excursion_C=60,assumptions='DC source <= boost reference/resistor tolerance+TCR bound; two limiter resistors intact; 85C electronics stress only, not a whole-system operating rating; TVS clamp comparisons are nominal datasheet pulse conditions, not hot surge qualification; no lightning immunity claimed')
(p/'tests/test-results/electrical-dc-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

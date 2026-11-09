"""Revision-specific external harness drawing; paths mirror connector table."""
from pathlib import Path
from html import escape
p=Path(__file__).resolve().parents[1];parts=[]
def text(x,y,t,size=20,color='#18364b'):
 parts.append(f'<text x="{x}" y="{y}" font-family="Arial,sans-serif" font-size="{size}" fill="{color}">{escape(t)}</text>')
def box(x,y,w,h,title,lines):
 parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#e8f0f5" stroke="#607f92" stroke-width="2"/>');text(x+14,y+30,title,23)
 for i,line in enumerate(lines):text(x+14,y+60+i*26,line,18)
def wire(points,color='#c03b32',width=4):parts.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in points)+f'" fill="none" stroke="{color}" stroke-width="{width}"/>')
text(45,48,'Revision 0.2 external power harness — repeat independently for each tank',31)
text(45,86,'Pin 1 is positive. Keep PV_NEG separate from GND outside the charger. Charger LOAD terminals unused.',20)
box(45,135,280,125,'Two series 20 W panels',['SPM040201200 ×2','40 W per node; cold Voc50.74 V'])
box(390,135,290,125,'PCB J4 → D9 → R2 → J5',['J4.1 →reverse diode→20 mΩ','J4.2 and J5.2 = PV_NEG'])
box(790,135,360,160,'SmartSolar MPPT75/10',['PV+ / PV− from J5 only','BAT+ / BAT− from J2','LOAD+ / LOAD− unused'])
wire([(325,185),(390,185)]);wire([(680,185),(790,185)])
wire([(325,235),(360,235),(360,315),(735,315),(735,240),(790,240)],'#2879a0');text(425,345,'PV return: no external battery− bridge',18,'#2879a0')
box(45,420,250,125,'12.8 V20 Ah battery',['BAT512020705 +BMS','Confirm cold-charge inhibit'])
box(355,420,300,125,'5 A fuse → J1 → MOSFETs',['Fuse close to battery+','U7 +Q2/Q3 →10 mΩ→ J2.1'])
box(725,420,300,125,'System positive after R1',['J2.1 → charger BAT+','Also →BatteryProtect IN'])
box(1090,420,320,125,'Smart BatteryProtect',['BPR065022000, load-only','OUT →2 A fuse→ J3.1'])
wire([(295,465),(355,465)]);wire([(655,465),(725,465)]);wire([(1025,465),(1090,465)])
wire([(875,420),(875,365),(965,365),(965,295)]);text(978,365,'J2 BAT harness',17)
box(1090,610,320,125,'J3 → buck →3.3 V',['J3.2 = GND','C6 +3×INA228 +switched boost'])
wire([(1250,545),(1250,610)])
wire([(170,545),(170,790),(1410,790)],'#253947');wire([(1090,685),(1060,685),(1060,790)],'#253947')
wire([(790,270),(710,270),(710,790)],'#253947');wire([(1090,520),(1045,520),(1045,790)],'#253947')
text(205,778,'GND = battery−, J1.2, J2.2, J3.2 and BatteryProtect GND lead',20)
text(45,855,'Battery current sign: positive discharge, negative charging. Controller / raw-presence drain precedes R1.',21)
text(45,900,'Normal charger / load current must pass the battery shunt. Do not route charging backward through BatteryProtect.',20)
text(45,950,'BMS-off recovery: approved charger at raw battery only after polarity verification; automatic recovery is not provided.',20)
text(45,995,'Drawing specifies connections; cable lengths, lugs, fuse breaking capacity and mechanical strain relief require final harness review.',18)
svg='<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1040" viewBox="0 0 1500 1040"><rect width="1500" height="1040" fill="#ffffff"/>'+''.join(parts)+'</svg>'
f=p/'hardware/wiring/power-harness.svg';f.write_text(svg)
try:
 import resvg_py
 f.with_suffix('.png').write_bytes(resvg_py.svg_to_bytes(svg_string=svg))
except ImportError:pass

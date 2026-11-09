"""Editable support/solar mounting study. Not a certified wind/footing design.
Dimensions in mm. No structural tank holes. Purchased frame clamps are placeholders.
"""
import FreeCAD as A,Part,Mesh,json
from pathlib import Path
p=Path(__file__).resolve().parents[1];doc=A.newDocument('SolarPostMount')
parts=[]
def add(name,s,role):
 o=doc.addObject('PartDesign::Feature',name);o.Shape=s;o.addProperty('App::PropertyString','EngineeringRole');o.EngineeringRole=role;parts.append(o);return o
# 114.3mm post fits the selected Fibox PMK ARCA 30's 100-300mm diameter range.
post=Part.makeCylinder(57.15,1800);post=post.cut(Part.makeCylinder(53.15,1802,A.Vector(0,0,-1)))
add('PostReference',post,'114.3mm OD x4mm wall reference, footing and wind design required')
# Panels and rails form a separate north-facing tilted rack at 45 degrees.
rack=[]
for i,x in enumerate([-450,10]):
 s=Part.makeBox(440,350,25,A.Vector(x,0,0));rack.append(add('PanelReference'+str(i+1),s,'SPM040201200 440x350x25 envelope; do not drill the panel frame without approval'))
for i,y in enumerate([35,290]):
 s=Part.makeBox(920,30,3,A.Vector(-460,y,-3)).fuse(Part.makeBox(920,3,30,A.Vector(-460,y,-30)))
 rack.append(add('SolarRail'+str(i+1),s,'30x30x3 aluminum angle, length920; clamp pattern awaits panel drawing'))
for i,x in enumerate([-200,200]):
 s=Part.makeBox(30,350,3,A.Vector(x,0,-33)).fuse(Part.makeBox(3,350,30,A.Vector(x,0,-60)))
 rack.append(add('RackSpine'+str(i+1),s,'30x30x3 angle; M8 connections require detailed bracket review'))
for o in rack:
 s=o.Shape.copy();s.rotate(A.Vector(0,0,0),A.Vector(1,0,0),45)
 s.translate(A.Vector(0,0,1400));o.Shape=s
# Support envelopes identify required ties but do not claim bolt/hole qualification.
for i,x in enumerate([-200,200]):
 add('SupportArm'+str(i+1),Part.makeBox(30,250,30,A.Vector(x,-20,1300)),'Reference support arm: structural member and fixing sizes require site wind calculation')
add('MountCabinetReference',Part.makeBox(300,210,400,A.Vector(-150,-270,700)),'Fibox cabinet reference; proprietary PMK ARCA30 polestrap kit attaches without tank drilling')
for i,z in enumerate([745,1055]):
 add('PoleBandReference'+str(i+1),Part.makeCylinder(60,20,A.Vector(0,0,z)).cut(Part.makeCylinder(57.5,22,A.Vector(0,0,z-1))),'Band envelope only, use manufacturer PMK kit and its instructions')
doc.recompute();report={}
for o in parts:
 assert o.Shape.isValid() and o.Shape.Volume>0,o.Name
 Part.export([o],str(p/'step'/(o.Name+'.step')));Mesh.export([o],str(p/'stl'/(o.Name+'.stl')))
 report[o.Name]={'valid':True,'role':o.EngineeringRole,'volume_mm3':o.Shape.Volume}
Part.export(parts,str(p/'step'/'SolarPostMount.step'))
doc.saveAs(str(p/'freecad'/'SolarPostMount.FCStd'))
(p/'mount-validation.json').write_text(json.dumps({'status':'packaging / mounting study only','parts':report,'wind_load':'not calculated; site design dependency','footing':'not designed; soil and wind data required'},indent=2))
print('Validated',len(parts),'mount study solids')

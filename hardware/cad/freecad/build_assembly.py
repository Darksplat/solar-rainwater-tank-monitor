"""Editable packaging study. Purchased parts are stated reference envelopes,
not vendor CAD. Cabinet boss and charger fixing patterns require vendor drawings.
Run with FreeCAD's bundled Python and Resources/lib on PYTHONPATH.
"""
from pathlib import Path
import json
import FreeCAD as A,Part,Mesh
out=Path(__file__).resolve().parents[1]
doc=A.newDocument('TankMonitorAssembly')
def shape(name,s,role):
 o=doc.addObject('PartDesign::Feature',name);o.Shape=s
 o.addProperty('App::PropertyString','EngineeringRole');o.EngineeringRole=role
 return o
def box(l,w,h,x,y,z):return Part.makeBox(l,w,h,A.Vector(x,y,z))
def hole(s,r,h,x,y,z):return s.cut(Part.makeCylinder(r,h,A.Vector(x,y,z)))
# X=width, Y=height, Z=depth from rear. Door omitted to expose the service layout.
cabinet=shape('CabinetReference',box(300,400,210,0,0,0).cut(box(290,390,207,5,5,5)),
 'Fibox ARCA403021S external 300W x400H x210D; 5mm walls are illustrative, not vendor geometry')
plate=box(250,350,4,25,25,12)
# Remove nearby metal behind and around the module antenna, not just FR4.
plate=plate.cut(box(50,38,6,185,337,11))
# Actual PCB mechanical mounting coordinates, mapped from top-left CAD origin.
pcbx,pcby=145,250
pcbholes=[(4,4),(126,4),(4,106),(126,84)]
for x,y in pcbholes:plate=hole(plate,1.7,6,pcbx+x,pcby+110-y,11)
# M5 shelf flange bolts. These are designed holes, not assumed cabinet bosses.
for x,y in [(70,54),(220,54),(70,74),(220,74)]:plate=hole(plate,2.75,6,x,y,11)
backplate=shape('ServiceBackplate',plate,'250x350x4 aluminum; mounting to cabinet boss pattern unresolved')
# Vertical 40mm flange / 95mm shelf. M5 bolt axes are depth direction.
shelf=box(210,2,95,40,50,16).fuse(box(210,40,2,40,50,16))
for x,y in [(70,54),(220,54),(70,74),(220,74)]:shelf=hole(shelf,2.75,4,x,y,15)
shelfobj=shape('BatteryShelf',shelf,'2mm aluminum bent shelf; proof load and restraint test required')
battery=shape('BatteryReference',box(181,167,77,54.5,52,20),'Victron BAT512020705 reference 181W x167H x77D; terminals/tool keepout above')
# Strap reference bands surround the battery and shelf without relying on adhesive.
straps=[]
for i,x in enumerate([78,192]):
 band=box(20,171,83,x,50,18).cut(box(22,167,79,x-1,52,20))
 straps.append(shape('BatteryStrap'+str(i+1),band,'20mm webbing envelope; stainless buckle, rated restraints selected at procurement'))
charger=shape('ChargerReference',box(113,100,40,27,251,20),'SmartSolar 75/10 reference envelope; actual mounting-hole drawing required')
protect=shape('BatteryProtectReference',box(48,106,40,240,80,20),'BPR065022000 rotated installation envelope 48W x106H x40D; vendor fixing pattern pending')
# Import board body exported by KiCad. Its coordinates use negative Y in STEP.
board=Part.Shape();board.read(str(out.parent/'pcb/3d/tank-monitor-board.step'))
bb=board.BoundBox
board.translate(A.Vector(pcbx-bb.XMin,pcby-bb.YMin,26-bb.ZMin))
pcb=shape('RoutedPCB',board,'Actual KiCad board outline 130x110x1.6; component envelopes are separate')
posts=[]
for i,(x,y) in enumerate(pcbholes):
 s=Part.makeCylinder(3,10,A.Vector(pcbx+x,pcby+110-y,16))
 s=hole(s,1.6,12,pcbx+x,pcby+110-y,15)
 posts.append(shape('PCBSpacer'+str(i+1),s,'M3 10mm spacer; holes match routed PCB'))
# Service / electrical keepouts represented explicitly, not mistaken for physical solids.
keepout=shape('BatteryTerminalServiceKeepout',box(181,25,85,54.5,219,18),'25mm terminal service clearance; verify actual terminal position')
antenna=shape('AntennaMetalKeepout',box(50,38,60,185,337,0),'No metal in this reference volume; plastic cabinet allowed; RF validation required')
wire=shape('CableDuctEnvelope',box(18,310,20,5,45,20),'Cable route envelope only; no commercial duct selected')
doc.recompute()
physical=[backplate,shelfobj,battery,charger,protect,pcb]+posts+straps
# Commercial objects must not intersect one another or the cabinet wall.
checks={}
for a,b in [(battery,charger),(battery,pcb),(charger,pcb),(pcb,cabinet),(battery,cabinet),(battery,protect),(protect,cabinet),(backplate,antenna)]:
 v=a.Shape.common(b.Shape).Volume;checks[a.Name+'__'+b.Name]=v;assert v<1e-5,(a.Name,b.Name,v)
results={'status':'packaging study, not manufacturing release','clearance_intersection_volumes_mm3':checks,'objects':{}}
for o in [cabinet,backplate,shelfobj,battery,charger,protect,pcb,keepout,antenna,wire]+posts+straps:
 assert o.Shape.isValid() and o.Shape.Volume>0,o.Name
 bb=o.Shape.BoundBox
 results['objects'][o.Name]={'valid':True,'volume_mm3':o.Shape.Volume,'bounds_mm':[bb.XMin,bb.YMin,bb.ZMin,bb.XMax,bb.YMax,bb.ZMax],'role':o.EngineeringRole}
 Part.export([o],str(out/'step'/(o.Name+'.step')))
 Mesh.export([o],str(out/'stl'/(o.Name+'.stl')))
 # Independent STEP round trip validates exported solids.
 restored=Part.Shape();restored.read(str(out/'step'/(o.Name+'.step')))
 assert restored.isValid() and abs(restored.Volume-o.Shape.Volume)<max(.01,o.Shape.Volume*1e-6),o.Name
Part.export([cabinet]+physical,str(out/'step'/'TankMonitorAssembly.step'))
doc.saveAs(str(out/'freecad'/'TankMonitorAssembly.FCStd'))
(out/'assembly-validation.json').write_text(json.dumps(results,indent=2))
print('Validated assembly geometry, eight collision checks and STEP round trips')

exploded=A.newDocument('TankMonitorExploded')
objects=[]
for index,o in enumerate([cabinet,backplate,shelfobj,battery,charger,protect,pcb]+posts+straps):
 copy=exploded.addObject('PartDesign::Feature',o.Name)
 s=o.Shape.copy();offset={'CabinetReference':0,'ServiceBackplate':230,'BatteryShelf':270,'BatteryReference':340,'ChargerReference':300,'BatteryProtectReference':300,'RoutedPCB':290}.get(o.Name,315)
 s.translate(A.Vector(0,0,offset));copy.Shape=s;objects.append(copy)
exploded.recompute();exploded.saveAs(str(out/'freecad'/'TankMonitorExploded.FCStd'))
Part.export(objects,str(out/'step'/'TankMonitorExploded.step'))

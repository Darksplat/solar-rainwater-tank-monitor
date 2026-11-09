"""Run with FreeCAD's Python, import path including its lib directory.
Concept parts only: dimensions depend on final bought enclosure and sensor drawing.
"""
import FreeCAD as A, Part, Mesh, json
from pathlib import Path
out=Path(__file__).resolve().parents[1]
doc=A.newDocument('TankMonitorMechanical')
def box(name,l,w,h,x=0,y=0,z=0):
 o=doc.addObject('Part::Box',name);o.Length=l;o.Width=w;o.Height=h;o.Placement.Base=A.Vector(x,y,z);return o
def cyl(name,r,h,x,y,z):
 o=doc.addObject('Part::Cylinder',name);o.Radius=r;o.Height=h;o.Placement.Base=A.Vector(x,y,z);return o
def cut(name,a,b):
 o=doc.addObject('Part::Cut',name);o.Base=a;o.Tool=b;a.Visibility=False;b.Visibility=False;return o
tray=box('TrayBlank',180,120,3)
for i,(x,y) in enumerate([(10,10),(170,10),(10,110),(170,110)]):
 tray=cut('TrayMountHole'+str(i),tray,cyl('MountDrill'+str(i),2.2,5,x,y,-1))
# PCB envelope only; does not assert final board dimensions.
board=box('PCBEnvelope',80,60,1.6,20,30,12)
posts=[]
for i,(x,y) in enumerate([(24,34),(96,34),(24,86),(96,86)]):
 posts.append(cut('Standoff'+str(i),cyl('Post'+str(i),4,9,x,y,3),cyl('Bore'+str(i),1.7,11,x,y,2)))
# Slotted protective probe cage, suspended independently from cable termination.
outer=cyl('CageOuter',25,150,235,60,0)
inner=cyl('CageInner',21,152,235,60,4)
cage=cut('CageTube',outer,inner)
for i,z in enumerate([20,50,80,110]):
 cage=cut('CageSlot'+str(i),cage,box('SlotTool'+str(i),60,8,12,205,56,z))
# Two independent suspension holes near rim; avoid using vent tube as support.
for i,x in enumerate([211,259]):
 hole=cyl('SuspensionDrill'+str(i),2,60,x,30,138)
 hole.Placement.Rotation=A.Rotation(A.Vector(1,0,0),90)
 cage=cut('CageSuspension'+str(i),cage,hole)
doc.recompute()
parts=[tray,board,cage]+posts
result={}
for o in parts:
 assert o.Shape.isValid() and o.Shape.Volume>0,o.Name
 result[o.Name]={'valid':o.Shape.isValid(),'volume_mm3':o.Shape.Volume,'solids':len(o.Shape.Solids)}
 Part.export([o],str(out/'step'/(o.Name+'.step')))
 Mesh.export([o],str(out/'stl'/(o.Name+'.stl')))
doc.saveAs(str(out/'freecad'/'TankMonitorMechanical.FCStd'))
(out/'validation.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))

from pathlib import Path
import json,math
import pcbnew as k
from kicad_sexpr import parse,dump
p=Path(__file__).resolve().parents[1];f=p/'hardware/pcb/layout/tank-monitor.kicad_pcb'
# Avoid the installed SWIG binding's type-cache corruption after BOARD.Remove().
raw=parse(f.read_text());raw=[x for x in raw if not(isinstance(x,list) and x and x[0] in ['segment','via'])]
work=f.with_name('_unrouted_work.kicad_pcb');work.write_text(dump(raw));b=k.LoadBoard(str(work))
if b.FindNet('PV_NEG') is None:b.Add(k.NETINFO_ITEM(b,'PV_NEG'))
for fp in b.GetFootprints():
 if fp.GetReference() in ['J4','J5']:
  for pad in fp.Pads():
   if pad.GetNumber()=='2':pad.SetNet(b.FindNet('PV_NEG'))
 if fp.GetReference()=='J3':fp.SetValue('PROTECTED LOAD')
r=json.loads((p/'hardware/pcb/reports/routing.json').read_text());assert not r['unrouted'],r['unrouted']
# Qualified small-signal detector via; 0.155mm annulus retains the 0.15mm rule.
for v in r['vias']:
 if v['net']=='BAT_RAW' and abs(v['x']-51.3)<.001 and abs(v['y']-81.6)<.001:v.update(diameter=.56,drill=.25)
nets={name:b.FindNet(name) for name in {t['net'] for t in r['tracks']}|{v['net'] for v in r['vias']}}
def vec(a):return k.VECTOR2I(k.FromMM(a[0]),k.FromMM(a[1]))
def simplify(points):
 pts=[]
 for pt in points:
  if pts and math.dist(pt,pts[-1])<1e-8:continue
  if len(pts)>1:
   a,z=pts[-2:];u=(z[0]-a[0],z[1]-a[1]);v=(pt[0]-z[0],pt[1]-z[1])
   if abs(u[0]*v[1]-u[1]*v[0])<1e-8 and u[0]*v[0]+u[1]*v[1]>0:pts.pop()
  pts.append(pt)
 return pts
for t in r['tracks']:
 points=simplify(t['points']);t['points']=points
 for a,z in zip(points,points[1:]):
  tr=k.PCB_TRACK(b);tr.SetStart(vec(a));tr.SetEnd(vec(z));tr.SetWidth(k.FromMM(t['width']));tr.SetLayer(k.F_Cu if t['layer']==0 else k.B_Cu);tr.SetNet(nets[t['net']]);b.Add(tr)
seen_vias=set()
for v in r['vias']:
 key=(v['net'],round(v['x'],4),round(v['y'],4))
 if key in seen_vias:continue
 seen_vias.add(key)
 # Plated connector holes already join copper layers; no second drill at that point.
 existing=False
 for fp in b.GetFootprints():
  for pad in fp.Pads():
   if pad.GetAttribute()==k.PAD_ATTRIB_PTH and pad.GetNetname()==v['net']:
    pp=pad.GetPosition()
    if math.hypot(k.ToMM(pp.x)-v['x'],k.ToMM(pp.y)-v['y'])<.2:existing=True
 if existing:continue
 via=k.PCB_VIA(b);via.SetPosition(vec((v['x'],v['y'])));via.SetWidth(k.FromMM(v.get('diameter',.6)));via.SetDrill(k.FromMM(v.get('drill',.3)));via.SetViaType(k.VIATYPE_THROUGH);via.SetLayerPair(k.F_Cu,k.B_Cu);via.SetNet(nets[v['net']]);b.Add(via)
# Apply corrected component values without moving a routed footprint.
changes={'R7':'130k 0.1%','TP4':'LOOP_SUPPLY','R12':'110R 1.5W','R13':'110R 1.5W','D1':'B360A-13-F','D3':'B360A-13-F','C51':'10u 35V X5R','L1':'4.7uH Isat>=4A','L2':'10uH Isat>=1.6A','D5':'SMBJ51A','D6':'SMBJ51A','D7':'SMBJ51A'}
for fp in b.GetFootprints():
 if fp.GetReference() in changes:fp.SetValue(changes[fp.GetReference()])
 if fp.GetReference().startswith('H'):fp.Value().SetVisible(False)
# Keep copper beyond the antenna notch at >=0.5mm from routed edges.
for shape in b.GetDrawings():
 if shape.GetLayer()==k.Edge_Cuts:
  a,z=shape.GetStart(),shape.GetEnd()
  if abs(k.ToMM(a.y)-6.3)<.001:a.y=k.FromMM(6.0);shape.SetStart(a)
  if abs(k.ToMM(z.y)-6.3)<.001:z.y=k.FromMM(6.0);shape.SetEnd(z)
# The antenna outline lies over the intentional FR4 cutout; preserve fabrication
# geometry but omit those non-printable silk graphics from the assembly board.
for fp in b.GetFootprints():
 if fp.GetReference()=='U6':
  for item in list(fp.GraphicalItems()):
   if item.GetLayer()==k.F_SilkS:
    box=item.GetBoundingBox()
    if k.ToMM(box.GetTop())<6.5:fp.Remove(item)
for fp in b.GetFootprints():
 pos={'D10':(105,46.5),'R63':(57.5,87),'R62':(58.5,95.8)}.get(fp.GetReference())
 if pos:fp.Reference().SetPosition(vec(pos))
# Pin-for-pin local copy records the deliberate silk-only module modification.
local_lib=p/'hardware/pcb/library/TankMonitor.pretty';local_lib.mkdir(exist_ok=True)
for fp in b.GetFootprints():
 if fp.GetReference()=='U6':
  fp.SetFPID(k.LIB_ID('TankMonitor','ESP32-C6-MINI-1-edge-silk'))

(p/'hardware/pcb/layout/fp-lib-table').write_text('(fp_lib_table (lib (name "TankMonitor") (type "KiCad") (uri "${KIPRJMOD}/../library/TankMonitor.pretty") (options "") (descr "Silk-only board-edge module adaptation")))\n')
k.ZONE_FILLER(b).Fill(b.Zones());k.SaveBoard(str(f),b);work.unlink(missing_ok=True)
# Extract the footprint with the S-expression writer; native library plug-ins
# require a wxApp that is unavailable in this headless Python runtime.
for item in parse(f.read_text()):
 if isinstance(item,list) and item and item[0]=='footprint' and item[1]=='TankMonitor:ESP32-C6-MINI-1-edge-silk':
  module=[x for x in item if not(isinstance(x,list) and x and x[0] in ['path','sheetname','sheetfile'])]
  module[1]='ESP32-C6-MINI-1-edge-silk'
  (local_lib/'ESP32-C6-MINI-1-edge-silk.kicad_mod').write_text(dump(module))

# LoadBoard on a temporary filename creates defaults. Restore the original design
# requirements explicitly rather than accepting the temporary project's settings.
project=f.with_suffix('.kicad_pro');settings=json.loads(project.read_text())
rules=settings['board']['design_settings']['rules']
rules.update(min_clearance=.15,min_track_width=.15,min_via_annular_width=.15,min_via_diameter=.5,min_through_hole_diameter=.2,min_copper_edge_clearance=.5)
for cls in settings['net_settings']['classes']:
 if cls['name']=='Default':cls.update(clearance=.15,track_width=.2,via_diameter=.6,via_drill=.3)
project.write_text(json.dumps(settings,indent=2))
(p/'hardware/pcb/reports/routing.json').write_text(json.dumps(r,indent=2))
print('Saved routed board:',len(list(b.GetTracks())),'copper tracks/vias')

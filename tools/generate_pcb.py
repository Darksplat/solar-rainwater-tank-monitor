"""KiCad PCB source generator. Routing/DRC remain explicit separate steps."""
import json,sys,os,math
from pathlib import Path
import pcbnew as k
p=Path(__file__).resolve().parents[1];out=p/'hardware/pcb';lib=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints')
b=k.BOARD();b.SetCopperLayerCount(4);b.GetDesignSettings().SetBoardThickness(k.FromMM(1.6))
manifest=json.loads((out/'circuit-resolved.json').read_text());parts=manifest['parts']
nets={}
for name in sorted({n for c in parts for n in c['nets'].values() if n}):
 net=k.NETINFO_ITEM(b,name);b.Add(net);nets[name]=net
# Deliberate functional placement, with separate high-voltage field terminals.
pos={
'J1':(12,102,0),'J2':(32,102,0),'J3':(52,102,0),'J4':(76,102,0),'J5':(96,102,0),'J6':(116,102,0),
'Q4':(111,43,0),'R65':(111,37,0),'R66':(117,43,0),'R67':(105,41.5,0),'D10':(105,44.5,0),
'U7':(47,91,0),'Q2':(40,78,0),'Q3':(54,78,0),'R60':(42,97,0),'R61':(47,97,0),'R62':(58.5,94,0),'R63':(60.5,87,0),'R64':(116,32,0),'D9':(103,75,0),
'U1':(20,34,0),'L1':(27.5,34,0),'C1':(16,34,90),'C2':(16,29,90),'C3':(21,30.5,0),'C4':(34.5,31,90),'C5':(34.5,37,90),'R3':(12,40,0),'R4':(17,40,0),'D1':(8,36,90),'D2':(8,23,90),
'U2':(50,40,0),'Q1':(42,33,0),'R5':(40,28,0),'R6':(45,28,0),'C6':(50,36.5,0),'L2':(50,31.5,0),'D3':(55.5,40,180),'C7':(62,40,90),'R7':(56,45,0),'R8':(51,47,0),'R9':(44,47,0),'C8':(44,51,0),'R10':(62,48,0),'D4':(69,41,90),
'R11':(91,49,0),'R12':(102,50,0),'R13':(114,50,0),
'U3':(23,76,0),'R1':(19,90,0),'R20':(16,86,90),'R21':(22,86,90),'R22':(17,83,0),'C20':(12,76,90),'C21':(23,69,0),
'U4':(88,78,0),'R2':(86,92,0),'R30':(83,88,90),'R31':(89,88,90),'R32':(80,84,0),'C30':(74,78,90),'C31':(88,71,0),'D5':(63,72,90),'D6':(63,82,90),'D7':(63,92,90),
'U5':(95,35,0),'R40':(89.5,45.5,90),'R41':(92.5,45.5,90),'R42':(86,41,0),'C40':(80,35,90),'C41':(95,27,0),
'U6':(65,12,0),'R50':(48,15,90),'R51':(48,21,90),'R52':(87,14,0),'C50':(92,14,90),'R53':(87,20,0),'R54':(87,9,0),'C51':(76,22,90),'C52':(71,22,90),'SW1':(105,15,0),'SW2':(116,15,0),'J7':(123,25,0),'D8':(105,26,0),'R55':(110,26,0)}
for i in range(1,13):pos['TP'+str(i)]=(10+9*(i-1),60,0)
missing=[]
for c in parts:
 group,name=c['footprint'].split(':');fp=k.FootprintLoad(str(out/'library'/'TankMonitor.pretty' if group=='TankMonitor' else lib/(group+'.pretty')),name)
 if fp is None:missing.append(c['footprint']);continue
 fp.SetReference(c['ref']);fp.SetValue(c['value']);fp.SetFPID(k.LIB_ID(group,name))
 x,y,a=pos[c['ref']];fp.SetPosition(k.VECTOR2I(k.FromMM(x),k.FromMM(y)));fp.SetOrientationDegrees(a)
 fp.Reference().SetTextSize(k.VECTOR2I(k.FromMM(.8),k.FromMM(.8)));fp.Reference().SetTextThickness(k.FromMM(.12))
 # Reference labels sit just below courtyards; all value text remains in fabrication layer.
 fp.Value().SetVisible(False)
 for pad in fp.Pads():
  n=c['nets'].get(pad.GetNumber())
  if n:pad.SetNet(nets[n])
 b.Add(fp)
assert not missing,missing
for fp in b.GetFootprints():
 pos={'D10':(105,46.5),'R63':(57.5,87),'R62':(58.5,95.8)}.get(fp.GetReference())
 if pos:fp.Reference().SetPosition(k.VECTOR2I(k.FromMM(pos[0]),k.FromMM(pos[1])))
# Mounting holes at corners, no tank/enclosure structural holes implied.
for i,(x,y) in enumerate([(4,4),(126,4),(4,106),(126,84)],1):
 fp=k.FootprintLoad(str(lib/'MountingHole.pretty'),'MountingHole_3.2mm_M3');fp.SetReference('H'+str(i));fp.SetPosition(k.VECTOR2I(k.FromMM(x),k.FromMM(y)));fp.Reference().SetVisible(False);fp.Value().SetVisible(False);b.Add(fp)
for a,z in [((0,0),(57.5,0)),((57.5,0),(57.5,6.0)),((57.5,6.0),(72.5,6.0)),((72.5,6.0),(72.5,0)),((72.5,0),(130,0)),((130,0),(130,110)),((130,110),(0,110)),((0,110),(0,0))]:
 s=k.PCB_SHAPE();s.SetShape(k.SHAPE_T_SEGMENT);s.SetStart(k.VECTOR2I(k.FromMM(a[0]),k.FromMM(a[1])));s.SetEnd(k.VECTOR2I(k.FromMM(z[0]),k.FromMM(z[1])));s.SetLayer(k.Edge_Cuts);s.SetWidth(k.FromMM(.05));b.Add(s)
t=k.PCB_TEXT(b);t.SetText('RAINWATER 0.2 DEV - NOT RELEASED');t.SetTextSize(k.VECTOR2I(k.FromMM(1.0),k.FromMM(1.0)));t.SetPosition(k.VECTOR2I(k.FromMM(65),k.FromMM(65)));t.SetLayer(k.F_SilkS);b.Add(t)
# Antenna-facing edge contains no copper. Module antenna projects beyond outline.
keep=k.ZONE(b);keep.SetIsRuleArea(True);keep.SetLayerSet(k.LSET.AllCuMask());keep.SetDoNotAllowTracks(True);keep.SetDoNotAllowVias(True);keep.SetDoNotAllowZoneFills(True)
poly=keep.Outline();poly.NewOutline()
for x,y in [(43,0),(87,0),(87,6.3),(43,6.3)]:poly.Append(k.FromMM(x),k.FromMM(y))
b.Add(keep)
# Plane layers are dedicated, without high-voltage copper. Fill after routing.
for layer,name in [(k.In1_Cu,'GND'),(k.In2_Cu,'V3V3')]:
 z=k.ZONE(b);z.SetLayer(layer);z.SetNet(nets[name]);z.SetLocalClearance(k.FromMM(.25));z.SetThermalReliefGap(k.FromMM(.25));z.SetThermalReliefSpokeWidth(k.FromMM(.3));o=z.Outline();o.NewOutline()
 for x,y in [(1,3),(129,3),(129,109),(1,109)]:o.Append(k.FromMM(x),k.FromMM(y))
 b.Add(z)
k.SaveBoard(str(out/'layout/tank-monitor.kicad_pcb'),b)
# Project defaults and net classes; all routed traces must pass CLI DRC later.
proj={'board':{'design_settings':{'rules':{'min_clearance':0.15,'min_track_width':0.15,'min_via_annular_width':0.15,'min_via_diameter':0.5,'min_through_hole_diameter':0.2,'min_copper_edge_clearance':0.5}}},'net_settings':{'classes':[{'name':'Default','clearance':0.15,'track_width':0.2,'via_diameter':0.6,'via_drill':0.3,'microvia_diameter':0.3,'microvia_drill':0.1,'diff_pair_width':0.2,'diff_pair_gap':0.25}]}}
(out/'layout/tank-monitor.kicad_pro').write_text(json.dumps(proj,indent=2))
pads=[dict(ref=f.GetReference(),pin=pad.GetNumber(),net=pad.GetNetname(),x=k.ToMM(pad.GetPosition().x),y=k.ToMM(pad.GetPosition().y),width=k.ToMM(pad.GetSize().x),height=k.ToMM(pad.GetSize().y),angle=pad.GetOrientationDegrees(),through=pad.GetAttribute()!=k.PAD_ATTRIB_SMD) for f in b.GetFootprints() for pad in f.Pads() if pad.IsOnLayer(k.F_Cu) or pad.IsOnLayer(k.B_Cu)]
(out/'reports/pad-map.json').write_text(json.dumps(pads,indent=2));print('Placed',len(list(b.GetFootprints())),'footprints; routing pending')

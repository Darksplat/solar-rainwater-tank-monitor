"""Prune floating route tails only. Native DRC must still verify connectivity afterward."""
import json,math
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'hardware/pcb/reports'
r=json.loads((p/'routing.json').read_text());pads=json.loads((p/'pad-map.json').read_text())
segments=[]
for t in r['tracks']:
 for a,z in zip(t['points'],t['points'][1:]):segments.append(dict(net=t['net'],layer=t['layer'],width=t['width'],points=[a,z]))
def distance(pt,a,z):
 dx,dy=z[0]-a[0],z[1]-a[1];l=dx*dx+dy*dy
 if not l:return math.dist(pt,a)
 f=max(0,min(1,((pt[0]-a[0])*dx+(pt[1]-a[1])*dy)/l));return math.hypot(pt[0]-a[0]-f*dx,pt[1]-a[1]-f*dy)
def anchored(pt,t,index):
 for v in r['vias']:
  if v['net']==t['net'] and math.hypot(v['x']-pt[0],v['y']-pt[1])<.301:return True
 for a in pads:
  if a['net']!=t['net'] or (t['layer']==1 and not a['through']):continue
  if abs(a['x']-pt[0])<=a['width']/2+.001 and abs(a['y']-pt[1])<=a['height']/2+.001:return True
 for j,u in enumerate(segments):
  if j==index or u['net']!=t['net'] or u['layer']!=t['layer']:continue
  if distance(pt,*u['points'])<=(u['width']+t['width'])/2+1e-6:return True
 return False
# Remove collinear contained duplicates before testing floating ends.
kept=[]
for i,t in enumerate(segments):
 duplicate=False
 for j,u in enumerate(segments):
  if i==j or t['net']!=u['net'] or t['layer']!=u['layer'] or t['width']>u['width']:continue
  if all(distance(pt,*u['points'])<1e-7 for pt in t['points']):
   lt=math.dist(*t['points']);lu=math.dist(*u['points'])
   if lt<lu-1e-7 or (abs(lt-lu)<1e-7 and j<i):duplicate=True;break
 if not duplicate:kept.append(t)
removed=len(segments)-len(kept);segments=kept
while True:
 bad=[]
 for i,t in enumerate(segments):
  if not anchored(t['points'][0],t,i) or not anchored(t['points'][1],t,i):bad.append(i)
 if not bad:break
 removed+=len(bad);segments=[t for i,t in enumerate(segments) if i not in bad]
r['tracks']=segments;(p/'routing.json').write_text(json.dumps(r,indent=2));print('Pruned',removed,'floating tail segments')

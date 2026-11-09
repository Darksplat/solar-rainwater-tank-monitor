"""Conservative two-outer-layer routing attempt; native KiCad DRC is the acceptance gate."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,math,heapq,time
p=Path(__file__).resolve().parents[1];d=p/'hardware/pcb/reports'
pads=json.loads((d/'pad-map.json').read_text());G=.1;W=1301;H=1101;SIZE=W*H
tracks=[];vias=[];failed=[];clear=.17
for a in pads:
 a['node']=(round(a['x']/G),round(a['y']/G),0)
 if round(a['angle'])%180==90:a['width'],a['height']=a['height'],a['width']
def masks(net,width):
 result=[];r=width/2+clear
 for layer in [0,1]:
  im=Image.new('L',(W,H),0);draw=ImageDraw.Draw(im)
  draw.rectangle((0,0,W-1,H-1),outline=255,width=math.ceil((.5+width/2)/G)+1)
  draw.rectangle((43/G,0,87/G,(6.3+r)/G),fill=255)
  for a in pads:
   if a['net']==net and net:continue
   if layer==1 and not a['through']:continue
   x,y=a['x']/G,a['y']/G;rx=(a['width']/2+r)/G;ry=(a['height']/2+r)/G
   draw.rectangle((math.ceil(x-rx),math.ceil(y-ry),math.floor(x+rx),math.floor(y+ry)),fill=255)
  for a in tracks:
   if a['net']==net or a['layer']!=layer:continue
   pts=[(x/G,y/G) for x,y in a['points']]
   radius=(a['width']/2+width/2+.19)/G
   for aa,zz in zip(pts,pts[1:]):
    dx,dy=zz[0]-aa[0],zz[1]-aa[1];length=math.hypot(dx,dy)
    if not length:continue
    nx,ny=-dy/length*radius,dx/length*radius
    draw.polygon([(aa[0]+nx,aa[1]+ny),(zz[0]+nx,zz[1]+ny),(zz[0]-nx,zz[1]-ny),(aa[0]-nx,aa[1]-ny)],fill=255)
   for x,y in pts:draw.ellipse((x-radius,y-radius,x+radius,y+radius),fill=255)
  for a in vias:
   if a['net']==net:continue
   x,y=a['x']/G,a['y']/G;radius=(a.get('diameter',.6)/2+r+.10)/G
   draw.ellipse((x-radius,y-radius,x+radius,y+radius),fill=255)
  result.append(im.tobytes())
 return result
def encode(n):return n[2]*SIZE+n[1]*W+n[0]
def decode(n):return (n%W,(n%SIZE)//W,n//SIZE)
def free(n,m):x,y,l=n;return 0<=x<W and 0<=y<H and not m[l][y*W+x]
def search(start,target,mask,vmask,plane=False,plane_net=None,via_drill=.3):
 def via_hole_ok(x,y):
  for v in vias:
   dist=math.hypot(x*G-v['x'],y*G-v['y'])
   if dist<max(.6,.25+via_drill/2+v.get('drill',.3)/2) and not (dist<1e-6 and v['net']==plane_net):return False
  return True
 si=encode(start);best={si:0};parent={};queue=[(0,0,si)];visited=0
 def h(n):
  if plane:return 0
  return int(10*max(abs(n[0]-target[0]),abs(n[1]-target[1]))+4*min(abs(n[0]-target[0]),abs(n[1]-target[1])))
 while queue:
  _,cost,i=heapq.heappop(queue)
  if cost!=best.get(i):continue
  n=decode(i);x,y,l=n;visited+=1
  if (plane and cost>0 and free((x,y,0),vmask) and free((x,y,1),vmask) and via_hole_ok(x,y)) or (not plane and n==target):
   path=[n]
   while i in parent:i=parent[i];path.append(decode(i))
   return path[::-1]
  if visited>800000:return None
  for dx,dy,step in [(1,0,10),(-1,0,10),(0,1,10),(0,-1,10),(1,1,14),(1,-1,14),(-1,1,14),(-1,-1,14)]:
   nn=(x+dx,y+dy,l)
   if not free(nn,mask):continue
   if dx and dy and (not free((x+dx,y,l),mask) or not free((x,y+dy,l),mask)):continue
   ni=encode(nn);nc=cost+step
   if nc<best.get(ni,1e12):best[ni]=nc;parent[ni]=i;heapq.heappush(queue,(nc+h(nn),nc,ni))
  if not plane and free((x,y,0),vmask) and free((x,y,1),vmask) and via_hole_ok(x,y):
   nn=(x,y,1-l);ni=encode(nn);nc=cost+150
   if nc<best.get(ni,1e12):best[ni]=nc;parent[ni]=i;heapq.heappush(queue,(nc+h(nn),nc,ni))
 return None

def compact(points):
 pts=[]
 for pt in points:
  if pts and math.dist(pt,pts[-1])<1e-8:continue
  if len(pts)>1:
   a,z=pts[-2:];u=(z[0]-a[0],z[1]-a[1]);v=(pt[0]-z[0],pt[1]-z[1])
   if abs(u[0]*v[1]-u[1]*v[0])<1e-8 and u[0]*v[0]+u[1]*v[1]>0:pts.pop()
  pts.append(pt)
 return pts

def add_path(net,path,width,actual=None):
 # Compress collinear grid points. Explicit vias connect outer layers and inner planes.
 segment=[];layer=path[0][2]
 if actual:segment.append((actual['x'],actual['y']))
 for j,n in enumerate(path):
  x,y,l=n;pt=(x*G,y*G)
  if l!=layer:
   if len(segment)>1:tracks.append(dict(net=net,width=width,layer=layer,points=compact(segment)))
   if not any(v['net']==net and abs(v['x']-x*G)<1e-6 and abs(v['y']-y*G)<1e-6 for v in vias):vias.append(dict(net=net,x=x*G,y=y*G,diameter=1.2 if width>=1.5 else .6,drill=.6 if width>=1.5 else .3))
   segment=[pt];layer=l
  else:segment.append(pt)
 if len(segment)>1:tracks.append(dict(net=net,width=width,layer=layer,points=compact(segment)))

def save():
 (d/'routing.json').write_text(json.dumps(dict(grid_mm=G,tracks=tracks,vias=vias,unrouted=failed),indent=2))
# Incremental routing preserves a previously DRC-checked board.
import sys
if '--add-pv-return' in sys.argv:
 previous=json.loads((d/'routing.json').read_text());tracks=previous['tracks'];vias=previous['vias']
 group=[a for a in pads if a['net']=='PV_NEG'];assert len(group)==2
 mask=masks('PV_NEG',1.5);vmask=masks('PV_NEG',.6)
 path=search(group[0]['node'],group[1]['node'],mask,vmask,plane_net='PV_NEG')
 assert path,'PV return has no clear route'
 add_path('PV_NEG',path,1.5,group[0]);save();print('Added isolated PV return');sys.exit(0)
# Reserve the bottom-left INA228 clock escape before plane stitching.
source=next(a for a in pads if a['ref']=='U4' and a['pin']=='5')
target=next(a for a in pads if a['ref']=='R51' and a['pin']=='2')['node']
path=search(source['node'],target,masks('SCL',.2),masks('SCL',.6),plane_net='SCL')
assert path,'Fine pitch clock escape unavailable'
add_path('SCL',path,.2,source)
# Reserve the fine-pitch PV bus-sense escape before surrounding plane stitches.
source=next(a for a in pads if a['ref']=='U4' and a['pin']=='8')
target=next(a for a in pads if a['ref']=='R32' and a['pin']=='2')
path=search(source['node'],target['node'],masks('PV_VBUS',.15),masks('PV_VBUS',.6),plane_net='PV_VBUS')
assert path,'Fine pitch sense escape unavailable'
add_path('PV_VBUS',path,.15,source)
# Each power/ground pad is stitched to its dedicated inner plane. Through-hole pads already touch it.
for net in ['GND','V3V3']:
 for a in [x for x in pads if x['net']==net and not x['through']]:
  mask=masks(net,.2);vmask=masks(net,.6)
  path=search(a['node'],None,mask,vmask,plane=True,plane_net=net)
  if not path:failed.append([a['ref'],a['pin'],net]);continue
  add_path(net,path,.2,a);x,y,_=path[-1]
  if not any(v['net']==net and abs(v['x']-x*G)<1e-6 and abs(v['y']-y*G)<1e-6 for v in vias):vias.append(dict(net=net,x=x*G,y=y*G))
 print(net,'stitched; failures',len(failed),flush=True);save()
# Short local nets first, followed by global buses. Wide connections are used for field power.
allnets={x['net'] for x in pads if x['net'] and x['net'] not in ['GND','V3V3']}
def score(net):
 a=[x for x in pads if x['net']==net];return max(x['x'] for x in a)-min(x['x'] for x in a)+max(x['y'] for x in a)-min(x['y'] for x in a)
kelvin={'R20':('R1','1'),'R21':('R1','2'),'R30':('R2','1'),'R31':('R2','2'),'R40':('R11','1'),'R41':('R11','2')}
for net in sorted(allnets,key=score):
 group=[x for x in pads if x['net']==net and not(x['ref'] in kelvin and x['pin']=='1') and not(x['ref']=='U4' and x['pin'] in ['5','8'])]
 group.sort(key=lambda a:(0 if a['ref'].startswith('J') else 1 if a['ref'] in ['R1','R2','D1'] else 2,a['ref']))
 tree=[group[0]['node']]
 for a in group[1:]:
  start=a['node'];target=min(tree,key=lambda t:(t[0]-start[0])**2+(t[1]-start[1])**2)
  width=.15 if net=='PV_VBUS' else 1.5 if net=='PV_NEG' else 1.5 if net in ['BAT_RAW','BAT_FUSED','CHARGER_BAT','REV_SOURCE','PV_RAW','PV_IN','PV_OUT','LOAD_IN'] and a['ref'] in ['R1','R2','D1','D9','Q2','Q3'] else .2
  mask=masks(net,width);vmask=masks(net,1.2 if width>=1.5 else .6)
  path=search(start,target,mask,vmask,plane_net=net,via_drill=.6 if width>=1.5 else .3)
  if not path:failed.append([a['ref'],a['pin'],net]);continue
  add_path(net,path,width,a);tree+=path
 print(net,'routed; failures',len(failed),flush=True);save()
# Kelvin sense branches are added last. Existing same-net power copper is
# deliberately an obstacle, except inside the shunt pad itself.
kelvin_evidence=[]
for ref,(target_ref,target_pin) in kelvin.items():
 source=next(a for a in pads if a['ref']==ref and a['pin']=='1')
 target=next(a for a in pads if a['ref']==target_ref and a['pin']==target_pin)
 net=source['net'];assert net==target['net']
 original_tracks=[t['net'] for t in tracks];original_vias=[v['net'] for v in vias];original_pads=[a['net'] for a in pads]
 for t in tracks:
  if t['net']==net:t['net']='__blocked_power__'
 for v in vias:
  if v['net']==net:v['net']='__blocked_power__'
 for a in pads:
  if a['net']==net and a not in [source,target]:a['net']='__blocked_power__'
 mask=masks(net,.2);vmask=masks(net,.6)
 def clear_pad_regions(mask):
  result=[]
  for layer,data in enumerate(mask):
   im=Image.frombytes('L',(W,H),data);draw=ImageDraw.Draw(im)
   if layer==0:
    for a in [source,target]:
     draw.rectangle((math.ceil((a['x']-a['width']/2+.02)/G),math.ceil((a['y']-a['height']/2+.02)/G),math.floor((a['x']+a['width']/2-.02)/G),math.floor((a['y']+a['height']/2-.02)/G)),fill=0)
   result.append(im.tobytes())
  return result
 mask=clear_pad_regions(mask)
 path=search(source['node'],target['node'],mask,vmask,plane_net=net)
 for t,n in zip(tracks,original_tracks):t['net']=n
 for v,n in zip(vias,original_vias):v['net']=n
 for a,n in zip(pads,original_pads):a['net']=n
 if path:
  add_path(net,path,.2,source)
  kelvin_evidence.append(dict(filter=ref,shunt=target_ref,pin=target_pin,net=net,shared_power_track_outside_shunt_pad=False))
 else:failed.append([ref,'1','Kelvin route unavailable'])
 save();print(ref,'Kelvin routed' if path else 'Kelvin FAILED',flush=True)
(d/'kelvin-routing.json').write_text(json.dumps(kelvin_evidence,indent=2))
print('Routing attempt finished:' ,len(tracks),'segments,',len(vias),'vias;',len(failed),'unrouted',flush=True)

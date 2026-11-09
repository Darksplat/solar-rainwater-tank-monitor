"""Simple orthographic mesh render of actual exported STL geometry (Pillow)."""
import struct, math
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).resolve().parents[1]
im=Image.new('RGB',(1400,850),'#f2f5f8');draw=ImageDraw.Draw(im)
def font(size):
 try:return ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',size)
 except OSError:return ImageFont.load_default()
draw.text((55,35),'Mechanical fit concepts',font=font(34),fill='#17334d')
draw.text((55,86),'Actual FreeCAD mesh exports • dimensions pending final enclosure and probe',font=font(21),fill='#546778')
def triangles(path):
 b=path.read_bytes();n=struct.unpack_from('<I',b,80)[0]
 if len(b)==84+50*n:
  for i in range(n):
   x=struct.unpack_from('<12fH',b,84+50*i);yield x[:3],[x[3:6],x[6:9],x[9:12]]
 else:
  v=[]
  for line in b.decode().splitlines():
   vals=line.split()
   if vals and vals[0]=='vertex':v.append(tuple(map(float,vals[1:])))
   if len(v)==3:yield (0,0,1),v;v=[]
def render(names,rect,base):
 alltri=[]
 for name in names:
  alltri.extend(triangles(p/'hardware/cad/stl'/(name+'.stl')))
 project=lambda v:(0.866*v[0]-0.5*v[1],0.3*v[0]+0.52*v[1]-0.8*v[2])
 projected=[project(v) for n,vs in alltri for v in vs]
 xmin=min(x for x,y in projected);xmax=max(x for x,y in projected)
 ymin=min(y for x,y in projected);ymax=max(y for x,y in projected)
 scale=min(rect[2]/(xmax-xmin),rect[3]/(ymax-ymin))
 faces=[]
 for normal,verts in alltri:
  if normal[0]*0.4+normal[1]*0.693+normal[2]*0.6 < -0.0001:continue
  pts=[(rect[0]+(project(v)[0]-xmin)*scale,rect[1]+(project(v)[1]-ymin)*scale) for v in verts]
  light=0.63+0.25*normal[2]+0.12*normal[0]
  color=tuple(max(30,min(255,int(c*light))) for c in base)
  faces.append((sum(0.4*x+0.693*y+0.6*z for x,y,z in verts),pts,color))
 for _,pts,c in sorted(faces,key=lambda a:a[0]):draw.polygon(pts,fill=c)
render(['TrayMountHole3','Standoff0','Standoff1','Standoff2','Standoff3','PCBEnvelope'],(80,230,690,340),(75,148,181))
render(['CageSuspension1'],(950,200,250,410),(210,160,81))
draw.text((100,665),'Tray 180 × 120 mm • 9 mm standoffs',font=font(22),fill='#17334d')
draw.text((900,665),'Cage Ø50 × 150 mm',font=font(22),fill='#17334d')
draw.text((55,760),'Prototype geometry only — fit, load, material and weather tests pending',font=font(22),fill='#855a20')
im.save(p/'hardware/cad/mechanical-preview.png')

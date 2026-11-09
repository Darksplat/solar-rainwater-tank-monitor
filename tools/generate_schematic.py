"""Generate editable KiCad 10 schematic from reviewed pin/net manifest and library symbols."""
from pathlib import Path
from copy import deepcopy
import json,uuid,math,csv
from kicad_sexpr import parse,dump,child,children,Atom as A
p=Path(__file__).resolve().parents[1];out=p/'hardware/pcb'
libroot=Path('/Applications/KiCad/KiCad.app/Contents/SharedSupport/symbols')
def uid(s):return str(uuid.uuid5(uuid.NAMESPACE_URL,'tank-monitor-rev02/'+s))
def atom(s):return A(str(s))
cache={}
def symbol(lib):
 if lib in cache:return deepcopy(cache[lib])
 group,name=lib.split(':')
 root=parse((libroot/(group+'.kicad_sym')).read_text());src=next(x for x in children(root,'symbol') if x[1]==name)
 ext=child(src,'extends')
 if ext:
  base=symbol(group+':'+ext[1]);old=base[1];base[1]=name
  for sub in children(base,'symbol'):sub[1]=sub[1].replace(old+'_',name+'_',1)
  for prop in children(src,'property'):
   base=[x for x in base if not (isinstance(x,list) and x[:2]==prop[:2])];base.append(deepcopy(prop))
  src=base
 cache[lib]=deepcopy(src);return src

def custom(name,pins):
 s=[A('symbol'),name,[A('in_bom'),A('yes')],[A('on_board'),A('yes')],
  [A('property'),'Reference','U',[A('at'),A('0'),A('12.7'),A('0')],[A('effects'),[A('font'),[A('size'),A('1.27'),A('1.27')]]]],
  [A('property'),'Value',name,[A('at'),A('0'),A('10.16'),A('0')],[A('effects'),[A('font'),[A('size'),A('1.27'),A('1.27')]]]]]
 s.append([A('symbol'),name+'_0_1',[A('rectangle'),[A('start'),A('-7.62'),A('7.62')],[A('end'),A('7.62'),A('-7.62')],[A('stroke'),[A('width'),A('0.254')],[A('type'),A('default')]],[A('fill'),[A('type'),A('background')]]]])
 sub=[A('symbol'),name+'_1_1']
 for num,n,x,y,ang,typ in pins:
  sub.append([A('pin'),A(typ),A('line'),[A('at'),atom(x),atom(y),atom(ang)],[A('length'),A('2.54')],
   [A('name'),n,[A('effects'),[A('font'),[A('size'),A('1.0'),A('1.0')]]]],[A('number'),str(num),[A('effects'),[A('font'),[A('size'),A('1.0'),A('1.0')]]]]])
 s.append(sub);cache['TankMonitor:'+name]=s
custom('TPS61170',[(1,'FB',10.16,-2.54,180,'input'),(2,'COMP',10.16,-5.08,180,'output'),(3,'GND',0,-10.16,90,'power_in'),(4,'SW',10.16,5.08,180,'passive'),(5,'CTRL',-10.16,0,0,'input'),(6,'VIN',-10.16,5.08,0,'power_in'),(7,'PAD',2.54,-10.16,90,'passive')])
custom('DMP2035U',[(1,'G',-10.16,0,0,'input'),(2,'S',0,10.16,270,'passive'),(3,'D',0,-10.16,90,'passive')])
def pins(s):
 a=[]
 for sub in children(s,'symbol'):a+=children(sub,'pin')
 return a
c=json.loads((out/'circuit.json').read_text());parts=c['parts']
for part in parts:
 s=symbol(part['lib'])
 if 'named_nets' in part:
  mapping=part['named_nets'];actual={child(x,'name')[1]:child(x,'number')[1] for x in pins(s)}
  print('module names',actual)
  # KiCad uses IOx and U0TXD/U0RXD names; normalize deliberately.
  names={}
  for pin in pins(s):
   n=child(pin,'name')[1];normalized=n.replace('IO','GPIO') if n.startswith('IO') else n
   normalized={'U0TXD':'TXD0','U0RXD':'RXD0'}.get(normalized,normalized)
   names[child(pin,'number')[1]]=mapping.get(normalized)
  part['nets']=names
  for wanted in ['SDA','SCL','LOOP_EN_N','EN','BOOT','TXD','RXD','V3V3','GND','LED_K']:
   assert wanted in names.values(),('unmapped module net',wanted,actual)
  part.pop('named_nets')
 if part['lib'].startswith('TankMonitor:'):s=symbol(part['lib'])
 # All unused library pins are explicitly NC. Manifest cannot contain nonexistent pins.
 nums={child(x,'number')[1] for x in pins(s)}
 assert set(part['nets'])<=nums,(part['ref'],set(part['nets'])-nums)
 for n in nums:part['nets'].setdefault(n,None)
(out/'circuit-resolved.json').write_text(json.dumps(c,indent=2))
rootid=uid('root');libsymbols=[]
for name in sorted({x['lib'] for x in parts}|{'power:PWR_FLAG'}):
 s=symbol(name);s[1]=name;libsymbols.append(s)
root=[A('kicad_sch'),[A('version'),A('20250114')],[A('generator'),'eeschema'],[A('uuid'),rootid],[A('paper'),'A1'],
 [A('title_block'),[A('title'),'Solar tank monitor - Rev 0.2 engineering schematic'],[A('date'),'2026-11-09'],[A('rev'),'0.2-dev'],[A('comment'),A('1'),'Prototype: independent review and physical validation required']],
 [A('lib_symbols')]+libsymbols]
# Group placement in a readable large engineering sheet. Net labels keep sheets searchable.
sections=['connections','reverse','buck','boost','loop','battery','bat','pv','controller','test']
positions={}; idx=0
for section in sections:
 group=[x for x in parts if x['section']==section]
 for part in group:
  positions[part['ref']]=(round((45+(idx%11)*70)/1.27)*1.27,round((55+(idx//11)*58)/1.27)*1.27);idx+=1
# Module needs extra space; bottom sheet has spare height.
positions['U6']=(744.22,520.70)
def property_(name,val,x,y,hidden=False):
 return [A('property'),name,val,[A('at'),atom(x),atom(y),A('0')],[A('effects'),[A('font'),[A('size'),A('1.0'),A('1.0')]]]]+([[A('hide'),A('yes')]] if hidden else [])
def instantiate(ref,lib,value,fp,x,y,netmap,mpn='',datasheet=''):
 s=symbol(lib);sid=uid(ref)
 o=[A('symbol'),[A('lib_id'),lib],[A('at'),atom(x),atom(y),A('0')],[A('unit'),A('1')],[A('in_bom'),A('yes')],[A('on_board'),A('yes')],[A('dnp'),A('no')],[A('uuid'),sid],property_('Reference',ref,x,y-16),property_('Value',value,x,y-13.5),property_('Footprint',fp,x,y,True),property_('MPN',mpn,x,y,True),property_('Datasheet',datasheet,x,y,True)]
 for pin in pins(s):o.append([A('pin'),child(pin,'number')[1],[A('uuid'),uid(ref+'/pin/'+child(pin,'number')[1])]])
 o.append([A('instances'),[A('project'),'tank-monitor',[A('path'),'/'+rootid,[A('reference'),ref],[A('unit'),A('1')]]]])
 root.append(o)
 for n,pin in enumerate(pins(s)):
  number=child(pin,'number')[1];px,py,ang=map(float,child(pin,'at')[1:]);px+=x;py=y-py;net=netmap.get(number)
  if net is None:
   root.append([A('no_connect'),[A('at'),atom(px),atom(py)],[A('uuid'),uid(ref+'/NC/'+number)]])
  else:
   # outward extension is opposite library pin direction.
   ex=px-5.08*math.cos(math.radians(ang));ey=py+5.08*math.sin(math.radians(ang))
   root.append([A('wire'),[A('pts'),[A('xy'),atom(px),atom(py)],[A('xy'),atom(round(ex,5)),atom(round(ey,5))]],[A('stroke'),[A('width'),A('0')],[A('type'),A('default')]],[A('uuid'),uid(ref+'/wire/'+number)]])
   root.append([A('label'),net,[A('at'),atom(round(ex,5)),atom(round(ey,5)),A('0')],[A('effects'),[A('font'),[A('size'),A('0.9'),A('0.9')]],[A('justify'),A('left'),A('bottom')]],[A('uuid'),uid(ref+'/label/'+number)]])
for part in parts:
 instantiate(part['ref'],part['lib'],part['value'],part['footprint'],*positions[part['ref']],part['nets'],part['mpn'],part['datasheet'])
for i,net in enumerate(['GND','V3V3','VIN','BOOST_IN','BAT_RAW','BAT_FUSED']):
 instantiate('#FLG0'+str(i+1),'power:PWR_FLAG','PWR_FLAG','',round((40+50*i)/1.27)*1.27,560.07,{'1':net})
root.append([A('embedded_fonts'),A('no')])
(out/'schematic/tank-monitor.kicad_sch').write_text(dump(root)+'\n')
(out/'schematic/tank-monitor.kicad_pro').write_text('{}\n')
# Self-contained local symbol library, preserving original library identifiers in schematic.
for lib in sorted(cache):
 if lib.startswith('TankMonitor:'):continue
librootout=[A('kicad_symbol_lib'),[A('version'),A('20241209')],[A('generator'),'kicad_symbol_editor']]+[symbol(k) for k in cache if k.startswith('TankMonitor:')]
(out/'library/TankMonitor.kicad_sym').write_text(dump(librootout)+'\n')
with (out/'bom/pcb-bom.csv').open('w',newline='') as f:
 writer=csv.writer(f);writer.writerow(['Reference','Value','Footprint','MPN','Quantity for two boards'])
 for part in parts:writer.writerow([part[k] for k in ['ref','value','footprint','mpn']]+[2])
print('Generated',len(parts),'components')

(out/"schematic/fp-lib-table").write_text((out/"layout/fp-lib-table").read_text())

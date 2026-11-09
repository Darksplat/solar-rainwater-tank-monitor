"""Independent source/export sanity checks; not a substitute for a fabricator CAM review."""
from pathlib import Path
import json,csv,hashlib,re,sys
from kicad_sexpr import parse,child,children
p=Path(__file__).resolve().parents[1];root=p/'hardware/pcb'
b=parse((root/'layout/tank-monitor.kicad_pcb').read_text())
nets={str(n[1]):str(n[2]) for n in children(b,'net')}
parts={x['ref']:x for x in json.loads((root/'circuit-resolved.json').read_text())['parts']}
found={};mounts={}
for f in children(b,'footprint'):
 props={x[1]:x[2] for x in children(f,'property')};ref=props['Reference'];found[ref]=f
 if ref.startswith('H'):mounts[ref]=list(map(float,child(f,'at')[1:3]));continue
 assert ref in parts,ref
 assert props['Value']==parts[ref]['value'],(ref,'value mismatch')
 assert str(f[1])==parts[ref]['footprint'],(ref,'footprint mismatch')
 for pad in children(f,'pad'):
  if not pad[1]:continue
  expected=parts[ref]['nets'].get(str(pad[1]));net=child(pad,'net')
  actual=(str(net[2]) if len(net)>2 else nets.get(str(net[1]),str(net[1]))) if net else None
  assert actual==expected,(ref,pad[1],actual,expected)
assert len(parts)==97 and len(found)==len(parts)+4
assert mounts=={'H1':[4.,4.],'H2':[126.,4.],'H3':[4.,106.],'H4':[126.,84.]},mounts
# Verify no unintended shared PV return and switched-supply field labels.
assert parts['J4']['nets']['2']==parts['J5']['nets']['2']=='PV_NEG'
assert parts['J1']['nets']['2']=='GND' and parts['J3']['nets']['2']=='GND'
assert 'Found 0 DRC violations' in (root/'reports/routed-drc.rpt').read_text()
assert 'Found 0 unconnected pads' in (root/'reports/routed-drc.rpt').read_text()
assert 'ERC messages: 0' in (root/'reports/erc.rpt').read_text()
files=list((root/'manufacturing/gerbers').glob('*'))+list((root/'manufacturing/drill').glob('*'))
for ext in ['gtl','g1','g2','gbl','gts','gbs','gko']:
 if ext=='gko':assert list((root/'manufacturing/gerbers').glob('*.gm1'));continue
 assert list((root/'manufacturing/gerbers').glob('*.'+ext)),ext
for f in files:
 if f.suffix in ['.drl']:assert f.read_text().startswith('M48') and 'M30' in f.read_text()
 elif f.suffix=='.gbrjob':json.loads(f.read_text())
 elif f.suffix!='.svg' and f.suffix!='.rpt':assert 'M02*' in f.read_text(),f
positions=list(csv.DictReader((root/'manufacturing/assembly/smd-positions.csv').open()))
assert len(positions)>50
board_sha=hashlib.sha256((root/'layout/tank-monitor.kicad_pcb').read_bytes()).hexdigest()
schematic_sha=hashlib.sha256((root/'schematic/tank-monitor.kicad_sch').read_bytes()).hexdigest()
if '--verify-evidence' in sys.argv:
 previous=json.loads((p/'tests/test-results/manufacturing-validation.json').read_text())
 assert previous['board_sha256']==board_sha and previous['schematic_sha256']==schematic_sha,'Native check evidence belongs to a different source revision'
 for file,digest in previous['files'].items():assert hashlib.sha256((root/file).read_bytes()).hexdigest()==digest,file
report={'board_sha256':board_sha,'schematic_sha256':schematic_sha,'date':'2026-11-09','source_pad_net_parity':True,'components':len(parts),'footprints_with_mounts':len(found),'DRC':'zero violations / zero unconnected pads','ERC':'zero violations','smd_placement_rows':len(positions),'export_structure_checks':True,'fabricator_CAM_review':'not performed','files':{str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}}
(p/'tests/test-results/manufacturing-validation.json').write_text(json.dumps(report,indent=2))
print('PASS: board/source pad parity, explicit mounting holes, ERC/DRC evidence, four copper exports, drill syntax and placement table')

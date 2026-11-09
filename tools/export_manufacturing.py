"""Reproduce KiCad fabrication outputs from the saved, DRC-checked board."""
from pathlib import Path
import os,subprocess,shutil
p=Path(__file__).resolve().parents[1];os.chdir(p)
cli=os.environ.get('KICAD_CLI') or shutil.which('kicad-cli') or '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli'
b='hardware/pcb/layout/tank-monitor.kicad_pcb';s='hardware/pcb/schematic/tank-monitor.kicad_sch';m='hardware/pcb/manufacturing/'
commands=[['sch','erc','-o','hardware/pcb/reports/erc.rpt',s],['sch','export','netlist','-o','hardware/pcb/reports/tank-monitor.net',s],['sch','export','svg','-o','hardware/pcb/schematic/render/',s],['pcb','drc','-o','hardware/pcb/reports/routed-drc.rpt',b],['pcb','export','gerbers','-o',m+'gerbers/','-l','F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,F.Mask,B.Mask,Edge.Cuts','--subtract-soldermask',b],['pcb','export','drill','-o',m+'drill/','--excellon-separate-th','--generate-map','--map-format','svg','--generate-report',b],['pcb','export','pos','--format','csv','--units','mm','--smd-only','-o',m+'assembly/smd-positions.csv',b],['pcb','export','step','--board-only','--force','-o','hardware/pcb/3d/tank-monitor-board.step',b]]
for name,layers in [('tank-monitor-top','F.Cu,F.Silkscreen,Edge.Cuts'),('tank-monitor-bottom','B.Cu,B.Silkscreen,Edge.Cuts'),('tank-monitor-assembly','F.Fab,F.Silkscreen,Edge.Cuts')]:
 commands.append(['pcb','export','svg','--mode-single','--black-and-white','--fit-page-to-board','--exclude-drawing-sheet','-o','hardware/pcb/layout/render/'+name+'.svg','-l',layers,b])
for args in commands:subprocess.run([cli]+args,check=True)
# Absolute workstation paths are not needed to reproduce exported netlists.
net=Path('hardware/pcb/reports/tank-monitor.net');net.write_text(net.read_text().replace(str(p),'${PROJECT_ROOT}'))
print('Exported fabrication, assembly, board model and review drawings')

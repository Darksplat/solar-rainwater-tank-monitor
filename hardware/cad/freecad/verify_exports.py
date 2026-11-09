"""Reopen editable documents, STEP solids and STL meshes; no physical claims."""
from pathlib import Path
import json,FreeCAD as A,Part,Mesh
p=Path(__file__).resolve().parents[1];report={'date':'2026-11-09','documents':{},'STEP':{},'STL':{}}
for file in (p/'freecad').glob('*.FCStd'):
 d=A.openDocument(str(file));objects=[o for o in d.Objects if hasattr(o,'Shape') and not o.Shape.isNull()]
 assert objects and all(o.Shape.isValid() for o in objects),file
 report['documents'][file.name]={'valid_shape_objects':len(objects)};A.closeDocument(d.Name)
for file in (p/'step').glob('*.step'):
 s=Part.Shape();s.read(str(file));assert s.isValid() and s.Volume>0,file
 report['STEP'][file.name]={'valid':True,'solids':len(s.Solids),'volume_mm3':s.Volume}
for file in (p/'stl').glob('*.stl'):
 m=Mesh.Mesh(str(file));assert m.isSolid() and m.CountFacets>0,file
 report['STL'][file.name]={'closed':True,'facets':m.CountFacets}
(p/'all-export-validation.json').write_text(json.dumps(report,indent=2))
print('PASS:',len(report['documents']),'editable documents,',len(report['STEP']),'STEP files and',len(report['STL']),'closed STL files')

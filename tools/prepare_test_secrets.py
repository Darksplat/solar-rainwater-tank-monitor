"""Only for CI compilation. Public test network, never deploy."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'firmware'
s=(p/'secrets-example.yaml').read_text()
for d in ['tank_1', 'tank_2']:
 f=p/d/'secrets.yaml'
 if f.is_symlink():f.unlink()
 if not f.exists():f.write_text(s)

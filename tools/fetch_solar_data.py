"""Fetch primary NASA POWER data at an approximate locality centroid, not a home address."""
from pathlib import Path
import urllib.request,json,datetime
p=Path(__file__).resolve().parents[1]
url='https://power.larc.nasa.gov/api/temporal/climatology/point?parameters=ALLSKY_SFC_SW_DWN&community=RE&longitude=144.22&latitude=-36.76&format=JSON'
with urllib.request.urlopen(url,timeout=45) as r:data=json.load(r)
assert 'properties' in data,data
(p/'docs/data/nasa-power-climatology.json').write_text(json.dumps({'request_url':url,'locality':'Approximate Maiden Gully locality centroid; not a site measurement','retrieved_date':'2026-11-09','response':data},indent=2))
print(json.dumps(data['properties']['parameter'],indent=2))

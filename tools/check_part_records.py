"""Fetch manufacturer passive records; existence checks do not qualify DC bias or stock."""
from pathlib import Path
import json,urllib.request,concurrent.futures,hashlib
p=Path(__file__).resolve().parents[1]
parts=json.loads((p/'hardware/pcb/circuit-resolved.json').read_text())['parts']
records={x['mpn']:x['datasheet'] for x in parts if x['mpn'] and ('product.tdk.com' in x['datasheet'] or 'yageogroup.com' in x['datasheet'])}
def check(pair):
 mpn,url=pair
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
  with urllib.request.urlopen(req,timeout=35) as r:data=r.read();status=r.status;ctype=r.headers.get('Content-Type','')
  valid=(data.startswith(b'%PDF') if 'yageogroup' in url else mpn.encode() in data and b'Product Status' in data)
  return mpn,dict(url=url,http_status=status,record_retrieved=valid,content_type=ctype,sha256=hashlib.sha256(data).hexdigest(),electrical_qualification='not established by HTTP check',stock_and_price='not checked')
 except Exception as e:return mpn,dict(url=url,record_retrieved=False,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:result=dict(ex.map(check,records.items()))
(p/'tests/test-results/manufacturer-record-check.json').write_text(json.dumps({'date':'2026-11-09','parts':result},indent=2))
print('Records retrieved:',sum(x['record_retrieved'] for x in result.values()),'of',len(result));print('Unresolved:',[k for k,v in result.items() if not v['record_retrieved']])

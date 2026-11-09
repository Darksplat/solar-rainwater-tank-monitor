"""Minimal KiCad S-expression reader/writer for deterministic source generation."""
import re,json
class Atom(str): pass
def parse(s):
 tokens=re.findall(r'"(?:\\.|[^"\\])*"|[^\s()]+|[()]',s); stack=[];root=None
 for t in tokens:
  if t=='(':
   a=[]
   if stack:stack[-1].append(a)
   stack.append(a)
  elif t==')':
   a=stack.pop()
   if not stack:root=a
  else:stack[-1].append(json.loads(t) if t.startswith('"') else Atom(t))
 return root
def dump(x):
 if isinstance(x,list):return '('+' '.join(dump(v) for v in x)+')'
 if isinstance(x,Atom):return str(x)
 return json.dumps(x,ensure_ascii=False)
def children(x,key):return [v for v in x if isinstance(v,list) and v and v[0]==key]
def child(x,key):
 a=children(x,key);return a[0] if a else None

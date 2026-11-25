"""Run against original privately retained Markdown."""
import re,json,hashlib,sys
from pathlib import Path
b=Path(sys.argv[1]).read_bytes(); s=b.decode("utf-8-sig"); l=s.splitlines()
def tok(x): return re.findall(r"[^\W\d_]+(?:[’'\-][^\W\d_]+)*",x)
t=tok(s); a=[1,13,31,35,43,57,69,85,97,99,113,128,142,157,169,182,196,210,226,241,243,265,289,309,327,345,365,387,403,419,437,len(l)+1]
o={"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),"lines":len(l),"tokens":len(t),"types":len({w.lower() for w in t}),"blocks":len(re.split(r"\n\s*\n",s.strip())),"sections":[len(tok("\n".join(l[x-1:y-1]))) for x,y in zip(a,a[1:])]}
assert sum(o["sections"])==len(t)
print(json.dumps(o,indent=2))

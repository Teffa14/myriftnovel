"""Run against the supplied Markdown, not source stored in Git."""
import hashlib,json,re,sys
from pathlib import Path
b=Path(sys.argv[1]).read_bytes()
s=b.decode("utf-8-sig"); lines=s.splitlines()
def tok(t): return re.findall(r"[^\W\d_]+(?:[’'\-][^\W\d_]+)*",t,re.UNICODE)
t=tok(s); starts=[1,43,76,88,96,118,252,370,398,474,482,490,514,528,550,574,len(lines)+1]
out={"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),"lines":len(lines),"tokens":len(t),"types":len({w.lower() for w in t}),"blocks":len(re.split(r"\n\s*\n",s.strip())),"links":len(re.findall(r"\]\((https?://[^)]+)\)",s)),"sections":[len(tok("\n".join(lines[a-1:z-1]))) for a,z in zip(starts,starts[1:])]}
assert sum(out["sections"])==len(t)
print(json.dumps(out,indent=2))

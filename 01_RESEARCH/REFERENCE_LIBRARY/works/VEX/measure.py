"""Reproduce source text metrics. Supply the original user-owned text path; not stored in Git."""
import hashlib, re, json, sys
from pathlib import Path
b=Path(sys.argv[1]).read_bytes()
s=b.decode("utf-8-sig")
lines=s.splitlines()
def tokens(t):
    return re.findall(r"[^\W\d_]+(?:[’'\-][^\W\d_]+)*", t, re.UNICODE)
t=tokens(s)
starts=[1,70,188,332,830,1034,1082,1456,1761,2099,2630,2694,2768,2800,len(lines)+1]
out={"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),"lines":len(lines),"word_tokens":len(t),"types":len({w.lower() for w in t}),"blocks":len(re.split(r"\n\s*\n",s.strip())),"sections":[len(tokens("\n".join(lines[a-1:z-1]))) for a,z in zip(starts,starts[1:])]}
assert sum(out["sections"])==len(t)
print(json.dumps(out,indent=2))

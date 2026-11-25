"""Reproduce measurements using the exact source text supplied privately."""
import hashlib,json,re,sys
from pathlib import Path
b=Path(sys.argv[1]).read_bytes()
s=b.decode("utf-8-sig"); lines=s.splitlines()
def tok(t): return re.findall(r"[^\W\d_]+(?:[’'\-][^\W\d_]+)*",t,re.UNICODE)
t=tok(s)
starts=[1,24,84,102,117,125,132,159,258,384,409,500,520,562,601,620,646,673,704,798,856,903,953,1021,1053,1061,1077,1118,1156,1184,1240,1268,1292,len(lines)+1]
out={"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),"lines":len(lines),"tokens":len(t),"types":len({w.lower() for w in t}),"blocks":len(re.split(r"\n\s*\n",s.strip())),"sentence_proxy":len([x for x in re.split(r"(?<=[.!?])\s+",s) if x.strip()]),"placeholders":sum(l.strip()=="Click to view full screen" for l in lines),"urls":len(re.findall(r"https?://[^\s]+",s)),"sections":[len(tok("\n".join(lines[a-1:z-1]))) for a,z in zip(starts,starts[1:])]}
assert sum(out["sections"])==len(t)
print(json.dumps(out,indent=2))

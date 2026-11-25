"""Measure exact privately held Rengar guide."""
import re,hashlib,json,sys
from pathlib import Path
b=Path(sys.argv[1]).read_bytes();s=b.decode("utf-8-sig");lines=s.splitlines()
def tok(x):return re.findall(r"[^\W\d_]+(?:[’'\-][^\W\d_]+)*",x)
t=tok(s);starts=[1,17,37,47,50,63,74,97,113,134,329,454,469,500,551,559,604,648,698,743,786,835,879,923,965,1009,1052,1096,1106,1156,1202,1245,1281,1320,1366,1372,1401,1408,1425,1444,1465,1467,1515,1557,1613,1655,1699,1756,1799,1840,1875,1909,1966,2012,2014,2057,2107,2150,2201,2209,2238,2249,2276,2291,2315,2332,2397,2454,2474,2496,2509,2517,2528]
o={"sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),"lines":len(lines),"tokens":len(t),"types":len({w.lower() for w in t}),"blocks":len(re.split(r"\n\s*\n",s.strip())),"image_placeholders":sum(x.strip()=="Click to view full screen" for x in lines),"sections":[len(tok("\n".join(lines[a-1:z-1]))) for a,z in zip(starts,starts[1:])]}
assert sum(o["sections"])==len(t)
print(json.dumps(o,indent=2))

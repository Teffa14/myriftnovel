"""Aggregate source counts; no source text emitted."""
import sys,re,hashlib,json
from pathlib import Path
import fitz
p=Path(sys.argv[1]); word=re.compile(r"[^\W\d_]+(?:[’'-][^\W\d_]+)*")
ranges=[("front",1,4),("introduction",5,7),("background",8,25),("methods",26,31),("findings",32,50),("discussion",51,54),("limitations",55,56),("conclusion",57,57),("references",58,61),("appendix",62,64)]
with fitz.open(p) as d:
    assert len(d)==64
    counts=[len(word.findall(pg.get_text())) for pg in d]
rows=[[label,a,b,sum(counts[a-1:b])] for label,a,b in ranges]
print(json.dumps({"source_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size,"pages":len(counts),"sections":rows,"total_word_tokens":sum(counts),"main_text_word_tokens":sum(counts[4:57])},indent=2))

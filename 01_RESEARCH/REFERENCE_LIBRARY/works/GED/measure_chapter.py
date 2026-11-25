"""Reproduce GED-CH01 metrics from the user-supplied Wattpad copy. No source distributed."""
from pathlib import Path
import re, collections, statistics, hashlib, json, sys
p=Path(sys.argv[1])
s=p.read_text()
b=s[s.index('Something that seemed'):]
b=re.sub(r"You'll also like\n.*?(?=I'm innocent)",'',b,flags=re.S)
b='\n'.join(l for l in b.splitlines() if not re.fullmatch(r'\s*(?:\d+|\*\*\*)\s*',l)).strip()
b=re.sub(r'\n{3,}','\n\n',b)
tok=lambda x: re.findall(r"\b[\w]+(?:['’][\w]+)*\b",x.lower())
ps=[x for x in re.split(r'\n\s*\n',b) if x.strip()]
q=re.findall(r'"([^"\n]*)"',b)
ss=[y for x in ps for y in re.split(r'(?<=[.!?])(?:[”"])?\s+',x) if tok(y)]
w=tok(b); c=collections.Counter(w)
m=dict(tokens=len(w),paragraphs=len(ps),quote_spans=len(q),quote_tokens=sum(len(tok(x)) for x in q),sentence_proxy=len(ss),median_sentence_tokens=statistics.median(len(tok(x)) for x in ss),median_paragraph_tokens=statistics.median(len(tok(x)) for x in ps),questions=b.count('?'),exclamations=b.count('!'),raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),normalized_sha256=hashlib.sha256(b.encode()).hexdigest(),top_forms=c.most_common(20),connectors={x:c[x] for x in ['but','however','because','so','then','if','although','instead','after','before','yet','actually']},starts=collections.Counter(tok(x)[0] for x in ss).most_common(10),selected_forms={x:c[x] for x in ['said','asked','replied','thought','wondered','looked','could','would','had','was']})
m['quote_pct']=round(m['quote_tokens']/len(w)*100,2)
m['quintiles']=[dict(tokens=len(seg),contrast=sum(seg.count(x) for x in ['but','however','yet','although']),causal=sum(seg.count(x) for x in ['because','so','if'])) for j in range(5) for seg in [w[len(w)*j//5:len(w)*(j+1)//5]]]
print(json.dumps(m,ensure_ascii=False,indent=2))

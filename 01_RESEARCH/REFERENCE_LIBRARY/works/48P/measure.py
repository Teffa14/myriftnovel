"""Measure the supplied condensed PDF. Output aggregate data only."""
import sys, re, json
import fitz
word = re.compile(r"[^\W\d_]+(?:[’'-][^\W\d_]+)*", re.UNICODE)
with fitz.open(sys.argv[1]) as d:
    assert len(d)==34
    pages=[re.sub(r'(?m)^Las 48 leyes del Poder\. Robert Greene\s*','',p.get_text()).strip() for p in d]
parts=[]; spans=[]; pos=0
for n in range(2,31):
    s=pages[n-1]
    spans.append((pos,pos+len(s),n))
    parts.append(s); pos+=len(s)+1
s='\n'.join(parts)
m=list(re.finditer(r'\bLEY\s+(\d+)\s*:',s))
assert [int(x[1]) for x in m]==list(range(1,49))
def page(k):
    return next(n for a,b,n in spans if a<=k<=b)
rows=[]
for i,x in enumerate(m):
    end=m[i+1].start() if i+1<len(m) else len(s)
    t=s[x.start():end].strip()
    rows.append([int(x[1]),page(x.start()),page(x.start()+len(t)-1),len(word.findall(t))])
print(json.dumps({"units":rows,"total_word_tokens":sum(x[-1] for x in rows),"preface_word_tokens_excluded":len(word.findall(s[:m[0].start()]))},indent=2))

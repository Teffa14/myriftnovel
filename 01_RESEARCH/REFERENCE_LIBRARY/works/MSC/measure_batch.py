"""Replicate EX16–18 metrics. Input narrative-only UTF-8, @@EXnn header per unit.
Exclude notes/credits/instructions manually, preserving paragraphs; do not commit source."""
import collections, hashlib, json, re, statistics, sys
from pathlib import Path
def tok(s):
    return re.findall(r"\b[\w]+(?:['’][\w]+)*\b",s.lower())
def measure(id,b):
    b=b.strip()
    norm=re.sub(r'[“”]','"',b)
    words=tok(b); p=re.split(r'\n\s*\n',b)
    quotes=re.findall(r'"([^"\n]*)"',norm)
    qw=sum(len(tok(q)) for q in quotes)
    ss=[y for x in p for y in re.split(r'(?<=[.!?])(?:[”"])?\s+',x) if tok(y)]
    c=collections.Counter(words)
    quintiles=[]
    for j in range(5):
        seg=words[len(words)*j//5:len(words)*(j+1)//5]
        sc=collections.Counter(seg)
        quintiles.append([len(seg),sum(sc[x] for x in ['but','however','although','instead']),sum(sc[x] for x in ['because','so','if'])])
    return dict(id=id,tokens=len(words),paragraphs=len(p),quote_spans=len(quotes),quote_tokens=qw,quote_pct=round(qw/len(words)*100,2),median_paragraph_tokens=statistics.median(len(tok(x)) for x in p),questions=b.count('?'),exclamations=b.count('!'),sentences_proxy=len(ss),median_sentence_tokens=statistics.median(len(tok(x)) for x in ss),normalized_sha256=hashlib.sha256(norm.encode()).hexdigest(),connectors={x:c[x] for x in ['but','however','because','so','then','if','although','instead','after','before']},selected_forms={x:c[x] for x in ['said','asked','thought','knew','replied','wanted','looked','could','would']},sentence_starts=collections.Counter(tok(x)[0] for x in ss).most_common(5),top_forms=c.most_common(10),quintiles=quintiles)
if __name__=='__main__':
    s=Path(sys.argv[1]).read_text(encoding='utf-8')
    print(json.dumps([measure(i,b) for i,b in re.findall(r'@@(EX\d+)\n(.*?)(?=@@EX\d+\n|\Z)',s,re.S)],ensure_ascii=False,indent=2))

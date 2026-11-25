"""Reproduce full volume metrics from supplied EPUB; do not distribute source."""
import zipfile, re, json, hashlib, sys, posixpath, collections, statistics
from lxml import etree
from pathlib import Path
p=Path(sys.argv[1]); z=zipfile.ZipFile(p)
root=etree.fromstring(z.read('META-INF/container.xml')); opf=root.xpath('//*[local-name()="rootfile"]')[0].get('full-path'); r=etree.fromstring(z.read(opf)); folder=posixpath.dirname(opf)
manifest={x.get('id'):x.get('href') for x in r.xpath('//*[local-name()="manifest"]/*')}; groups=collections.OrderedDict(); files=[]
for it in r.xpath('//*[local-name()="spine"]/*'):
 href=manifest[it.get('idref')]; m=re.fullmatch(r'Text/(prologue|chapter\d+)(?:_\d+)?\.xhtml',href)
 if not m: continue
 path=posixpath.join(folder,href); x=etree.fromstring(z.read(path)); ps=[''.join(a.itertext()).strip() for a in x.xpath('//*[local-name()="p"]')]; ps=[a for a in ps if a and a!='§']; g=groups.setdefault(m[1],{'p':[],'files':[],'headings':[]});g['p']+=ps;g['files'].append(href);g['headings'] += [''.join(a.itertext()) for a in x.xpath('//*[local-name()="h1" or local-name()="h2"]')];files.append(href)
tok=lambda s:re.findall(r"\b[\w]+(?:[’'\-][\w]+)*\b",s.lower())
lex={'contrast':['but','however','yet','although','instead'],'causal':['because','so','therefore','thus'],'conditional':['if','unless'],'cognition':['thought','wondered','realized','knew','noticed','understood','suspected'],'attribution':['said','asked','replied','answered','shouted','whispered'],'uncertainty':['perhaps','maybe','probably','seemed','apparently'],'sequence':['then','after','before','finally'],'action_proxy':['attack','attacked','struck','fought','ran','charged','hit','blocked']}
def measure(ps):
 text='\n\n'.join(ps); w=tok(text); c=collections.Counter(w); q=[v for a in ps for v in re.findall(r'“([^”]*)”|"([^"\n]*)"',a)]; qw=sum(len(tok(a or b)) for a,b in q); ss=[s for a in ps for s in re.split(r'(?<=[.!?])(?:[”"])?\s+',a) if tok(s)]; return dict(tokens=len(w),paragraphs=len(ps),sentence_proxy=len(ss),median_sentence_tokens=statistics.median(map(lambda a:len(tok(a)),ss)),median_paragraph_tokens=statistics.median(map(lambda a:len(tok(a)),ps)),quote_spans=len(q),quote_tokens=qw,quote_pct=round(100*qw/len(w),2),questions=text.count('?'),exclamations=text.count('!'),forms=len(c),top_forms=c.most_common(20),sentence_starts=collections.Counter(tok(a)[0] for a in ss).most_common(10),lexicon={k:sum(c[x] for x in v) for k,v in lex.items()},sha256=hashlib.sha256(text.encode()).hexdigest())
allp=[p for g in groups.values() for p in g['p']]; result={'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'narrative_files':len(files),'units':{},'total':measure(allp),'lexicons':lex,'limitations':'regex proxies, quote matches within paragraphs only; POS/lemmatization not run; headings, scene dividers, illustrations, afterword, promotional and bonus pages excluded; interludes included in parent chapter'}
for k,g in groups.items():
 ps=g['p']; result['units'][k]={'files':g['files'],'headings':g['headings'],**measure(ps),'quintiles':[{'start_paragraph':len(ps)*i//5+1,'end_paragraph':len(ps)*(i+1)//5,**{x:y for x,y in measure(ps[len(ps)*i//5:len(ps)*(i+1)//5]).items() if x in ['tokens','quote_pct','questions','exclamations','lexicon']}} for i in range(5)]}
print(json.dumps(result,indent=2,ensure_ascii=False))

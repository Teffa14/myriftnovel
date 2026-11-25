"""Local text-layer lexical audit; no ordered source prose retained."""
import fitz, re, hashlib, json, csv, sys
from pathlib import Path
from collections import Counter
p=Path(sys.argv[1]); out=Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
headers={'Introduction to Next Level Deckbuilding','The Art of the Mana Base','Deckbuilding Tactics','The Sixteen Macro Archetypes in Magic','The Ten Best Deckbuilders of All Time','Conclusion','Acknowledgements','Next Level Deckbuilding'}
word=re.compile(r"[^\W\d_]+(?:[’'-][^\W\d_]+)*",re.UNICODE)
starts=[5,8,17,22,23,25,39,54,55,60,74,76,78,85,88,98,102,115,120,142,157,178,191,203,214,228,240,255,267,281,295,311,330,343,360,377,385,391,395,404,412,421,430,438,446,456,468,471]
topics=["Introduction","Four perspectives","Probabilities","Mana foundations","Mana curves","Expensive spells","Land count","Color access","Land types","Mana examples","Flooding","Templating","Deck size","Copy count","Removal","Baneslayers and Mulldrifters","Sideboards","Commander","Card evaluation","Red Aggro","Linear Aggro","Swarm","Fish / Suicide Black","Rock / Junk","Pure Midrange","Non-Blue Control","Aggro-Control","Tap-Out Control","Draw-Go","Lock","Combo-Control","Big Spell Combo","Traditional Combo","Storm Combo","Lava Spike","Mark Herberholz","Michael Flores","Rob Dougherty","Alan Comer","Brian Kibler","Tomoharu Saito","Erik Lauer","Tsuyoshi Fujita","Gabriel Nassif","Zvi Mowshowitz","Deckbuilders 11–30","Conclusion","Acknowledgements"]
terms=["tempo","card advantage","virtual card advantage","mana curve","opportunity cost","sideboard","removal","threat","probability","hypergeometric","synergy","archetype","metagame","gauntlet","playtesting","control","aggro","combo","midrange","lock","storm","swarm","land","mana","baneslayer","mulldrifter","inevitability","redundancy","consistency","templating","linear","reactive","proactive","flexibility","flood","screw","mulligan","clock","matchup","card evaluation"]
with fitz.open(p) as doc:
    assert len(doc)==473
    raw=[pg.get_text() for pg in doc]
    images=[len(pg.get_images()) for pg in doc]
clean=['\n'.join(l.strip() for l in s.splitlines() if l.strip() not in headers and not re.fullmatch(r'Next Level Deckbuilding\s*\d*|\d+',l.strip())) for s in raw]
tokens=[word.findall(s.lower()) for s in clean]
allf=Counter(x for t in tokens for x in t); body=Counter(x for t in tokens[4:470] for x in t)
def write(name,head,rows):
    with (out/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f,delimiter='\t');w.writerow(head);w.writerows(rows)
write('word_frequency.tsv',['word','all','body'],[(k,v,body[k]) for k,v in allf.most_common()])
write('page_metrics.tsv',['page','words','types','images'],[(i+1,len(t),len(set(t)),images[i]) for i,t in enumerate(tokens)])
rows=[]
for i,a in enumerate(starts):
    b=starts[i+1]-1 if i+1<len(starts) else len(tokens)
    t=[x for ts in tokens[a-1:b] for x in ts];rows.append([i+1,topics[i],a,b,len(t),len(set(t))])
write('unit_metrics.tsv',['id','topic','start','end','words','types'],rows)
pat=[re.compile(r'(?<!\w)'+re.escape(t)+r'(?!\w)') for t in terms]
hits=[[i+1]+[len(q.findall(' '.join(s.lower().split()))) for q in pat] for i,s in enumerate(clean)]
write('concept_hits.tsv',['page']+terms,hits)
report={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pages':len(raw),'raw_word_tokens':sum(len(word.findall(s)) for s in raw),'clean_word_tokens':sum(allf.values()),'body_word_tokens':sum(body.values()),'all_types':len(allf),'body_types':len(body),'units':rows,'term_counts_body':{t:sum(r[i+1] for r in hits[4:470]) for i,t in enumerate(terms)}}
(out/'metrics.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='units'},indent=2))

"""Full local lexical audit of the supplied PDF, no ordered source text output."""
import fitz, re, sys, hashlib, csv, json
from pathlib import Path
from collections import Counter
p=Path(sys.argv[1]); out=Path(sys.argv[2]); out.mkdir(parents=True,exist_ok=True)
word=re.compile(r"[^\W\d_]+(?:[’'-][^\W\d_]+)*",re.UNICODE)
starts=[6,14,20,26,29,32,35,42,46,48,58,69,76,79,84,86,111,113,117,120,125,126,134,138,140,145,150,162,169,175,178,184,188,192,194,201,208,217,224,230,239,244,260,269,273,277,295,303,312,321,325,327,332,336,343,346,349,350,353,355,360,362,366,368,374,381,382,385,392,398,400,404]
with fitz.open(p) as doc:
    assert len(doc)==433
    raw=[pg.get_text() for pg in doc]
    images=[len(pg.get_images()) for pg in doc]
    glossary=[]
    for i in range(403,433):
        for b in doc[i].get_text("dict")["blocks"]:
            if b["type"]!=0: continue
            for l in b["lines"]:
                s=''.join(sp["text"] for sp in l["spans"] if sp["font"]=="OpenSans-SemiboldItalic").strip()
                if s: glossary.append((i+1,s))
def clean(s,n):
    return '\n'.join(l.strip() for l in s.splitlines() if l.strip() not in ('Next Level Magic',str(n)) and not re.match(r'^(Introduction|Conclusion|Acknowledgments|Glossary|Section (One|Two|Three|Four|Five|Six):.*)$',l.strip()))
pages=[clean(s,i+1) for i,s in enumerate(raw)]
tokens=[word.findall(s.lower()) for s in pages]
allfreq=Counter(x for t in tokens for x in t)
bodyfreq=Counter(x for t in tokens[5:399] for x in t)
def write(name,head,rows):
    with (out/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.writer(f,delimiter="\t");w.writerow(head);w.writerows(rows)
write("full_word_frequency.tsv",["word","all_pages_occurrences","main_text_occurrences"],[(k,v,bodyfreq[k]) for k,v in sorted(allfreq.items(),key=lambda x:(-x[1],x[0]))])
write("page_metrics.tsv",["page","clean_word_tokens","distinct_word_types","image_objects"],[(i+1,len(t),len(set(t)),images[i]) for i,t in enumerate(tokens)])
write("glossary_index.tsv",["page","heading"],glossary)
units=[]
for i,a in enumerate(starts):
    b=starts[i+1]-1 if i+1<len(starts) else len(pages)
    t=[x for ts in tokens[a-1:b] for x in ts]
    units.append([i+1,a,b,len(t),len(set(t)),round(len(set(t))/len(t),6)])
write("section_metrics.tsv",["unit","start","end","words","distinct_types","type_token_ratio"],units)
terms=["shortcut","feedback","trump","tempo","card advantage","virtual card advantage","card utility","card economy","minimum game threshold","stage one","stage two","stage three","inevitability","beatdown","control","mulligan","sideboard","mana","manabase","probability","information cascade","draft","signals","rapport","mindful","team","playtest","options","mistake","focus","synergy","combo","archetype","resource","bluff","mental","top–›down","bottom–›up","back–›front","front–›back"]
norm=[' '.join(s.lower().split()) for s in pages]
pat={t:re.compile(r'(?<!\w)'+re.escape(t)+r'(?!\w)') for t in terms}
write("page_concept_hits.tsv",["page"]+terms,[[i+1]+[len(pat[t].findall(s)) for t in terms] for i,s in enumerate(norm)])
report={"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"pages":len(pages),"raw_words":sum(len(word.findall(s)) for s in raw),"clean_words":sum(allfreq.values()),"main_words":sum(bodyfreq.values()),"all_word_types":len(allfreq),"main_word_types":len(bodyfreq),"glossary_headwords":len(glossary)}
assert report["main_words"]==96562 and report["clean_words"]==105555 and len(glossary)==136
(out/"summary.json").write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))

import zipfile,re,csv,json,statistics as st,hashlib,sys,collections, pathlib
from bs4 import BeautifulSoup
p=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/the_kings_avatar_1-1728.epub'); out=pathlib.Path(__file__).parent
word=re.compile(r"[A-Za-z0-9]+(?:[’'\-][A-Za-z0-9]+)*")
quote=re.compile(r'“[^”]*”|"[^"\n]*"')
notes=re.compile(r'^(?:T/N\s*:|TL/N\s*:|Translator(?:’|\')?s?\s+Note\s*:|Editor(?:’|\')?s?\s+Note\s*:|Announcement\s*:|Also, please check out the Author)',re.I)
lex={k:re.compile(v,re.I) for k,v in {'competition':r'\b(?:match(?:es)?|tournament|playoffs?|championship|rounds?|arena|opponents?)\b','institutions':r'\b(?:club|guild|alliance|manager|sponsor|contract|captain|team)\b','mechanics':r'\b(?:skills?|damage|health|cooldown|equipment|combo|attack|defense|mana|dungeon)\b','spectators':r'\b(?:spectators?|audience|viewers?|fans?|commentators?|broadcast)\b','economic':r'\b(?:money|price|cost|salary|contract|sponsor|budget|pay|paid|profit|financial|rent)\b','uncertainty':r'\b(?:perhaps|maybe|probably|possible|likely|guess|suspect|uncertain|wonder)\b','cognition':r'\b(?:thought|think|thinking|realized|understood|noticed|knew|know|expected|plan|strategy)\b'}.items()}
rows=[]; texts={}; paras={}; removed=0; mismatches=[]; headings=collections.defaultdict(list)
with zipfile.ZipFile(p) as z:
 ids=sorted(int(re.search(r'chap_(\d+)',n).group(1)) for n in z.namelist() if re.fullmatch(r'EPUB/chap_\d+\.xhtml',n))
 assert ids==list(range(1,1730))
 for i in ids:
  s=BeautifulSoup(z.read(f'EPUB/chap_{i:02d}.xhtml'),'html.parser'); label=int(re.search(r'Chapter\s+(\d+)',s.h1.get_text()).group(1)); headings[label].append(i)
  if i!=label: mismatches.append((i,label))
  pp=[x.get_text(' ',strip=True) for x in s.body.find_all('p')]; pp=[x for x in pp if x]; raw=pp[:]; pp=[x for x in pp if not notes.match(x)]; removed+=len(raw)-len(pp); paras[i]=pp; t='\n'.join(pp);texts[i]=t
  if i==1729: continue
  pw=[len(word.findall(x)) for x in pp]; n=sum(pw); q=sum(len(word.findall(m.group())) for x in pp for m in quote.finditer(x)); starts=sum(x.startswith(('“','"')) for x in pp)
  sentences=sum(max(1,len(re.findall(r'[.!?]+(?=[”"’\')\]]*(?:\s|$))',x))) for x in pp)
  row={'chapter':i,'heading_number':label,'words':n,'paragraphs':len(pp),'median_paragraph_words':st.median(pw),'short_paragraphs_le_10':sum(x<=10 for x in pw),'quote_words':q,'quote_start_paragraphs':starts,'sentence_proxy':sentences,'questions':t.count('?'),'exclamations':t.count('!'),'last_paragraph_words':pw[-1],'last_paragraph_question':int('?' in pp[-1]),'last_paragraph_exclamation':int('!' in pp[-1]),'last_paragraph_quote_start':int(pp[-1].startswith(('“','"')))}
  row.update({k:len(v.findall(t)) for k,v in lex.items()});rows.append(row)
with open(out/'chapter_metrics.csv','w') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
def summarize(rr):
 sums={k:sum(x[k] for x in rr) for k in rows[0] if k not in ('chapter','heading_number')}; n=len(rr); words=sums['words']; pp=sums['paragraphs']; lens=[x['words'] for x in rr]; return {'chapters':n,'words':words,'words_mean':round(words/n,2),'words_median':st.median(lens),'words_p10':round(st.quantiles(lens,n=10,method='inclusive')[0],1),'words_p90':round(st.quantiles(lens,n=10,method='inclusive')[8],1),'paragraphs':pp,'paragraphs_per_chapter':round(pp/n,2),'words_per_paragraph':round(words/pp,2),'short_paragraph_pct':round(100*sums['short_paragraphs_le_10']/pp,2),'quote_words_pct':round(100*sums['quote_words']/words,2),'quote_start_paragraph_pct':round(100*sums['quote_start_paragraphs']/pp,2),'words_per_sentence_proxy':round(words/sums['sentence_proxy'],2),'question_per_1000_words':round(1000*sums['questions']/words,2),'exclamation_per_1000_words':round(1000*sums['exclamations']/words,2),'last_paragraph_words_median':st.median(x['last_paragraph_words'] for x in rr),'last_question_pct':round(100*sums['last_paragraph_question']/n,2),'last_exclamation_pct':round(100*sums['last_paragraph_exclamation']/n,2),'last_quote_start_pct':round(100*sums['last_paragraph_quote_start']/n,2),**{k+'_per_1000':round(1000*sums[k]/words,2) for k in lex}}
res={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'chapter_files':len(ids),'narrative':summarize(rows),'notes_removed_by_heuristic':removed,'author_note_words':len(word.findall(texts[1729])),'blocks':[{'range':f'{i}-{min(i+99,1728)}',**summarize(rows[i-1:i+99])} for i in range(1,1729,100)]}
res['numbering_audit']={'mismatch_count':len(mismatches),'mismatch_range':[mismatches[0][0],mismatches[-1][0]] if mismatches else [],'missing_heading_numbers':sorted(set(ids)-set(headings)),'duplicate_heading_numbers':{str(k):v for k,v in headings.items() if len(v)>1},'note':'File sequence is complete; heading numbers are not. Content completeness not independently certified.'}
(out/'metrics.json').write_text(json.dumps(res,indent=2)); print(json.dumps({k:v for k,v in res.items() if k!='blocks'},indent=2));print('BLOCKS');print('\n'.join(f"{b['range']} {b['words_mean']} {b['quote_words_pct']} {b['mechanics_per_1000']} {b['competition_per_1000']} {b['spectators_per_1000']} {b['institutions_per_1000']}" for b in res['blocks']))

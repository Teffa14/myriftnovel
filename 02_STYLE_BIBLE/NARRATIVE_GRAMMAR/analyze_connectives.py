"""Count surface discourse markers in the supplied EPUB; export no prose."""
import re, zipfile, collections, argparse, json
from lxml import html
P = {
    'contrast':r'\b(?:however|but|yet|nevertheless)\b',
    'concession':r'\b(?:although|even though|despite)\b',
    'condition':r'\b(?:if|unless|otherwise)\b',
    'causality':r'\b(?:because|therefore|as a result|which meant)\b',
    'sequence':r'\b(?:then|afterward|immediately|at this moment)\b',
    'prior_state':r'\b(?:already|still|had been|had already)\b',
    'restriction':r'\b(?:only|could not|couldn.t|unable to)\b',
    'inference':r'\b(?:perhaps|probably|must have|might have|seemed)\b',
    'perception':r'\b(?:noticed|realized|saw|heard|recognized)\b',
    'intent':r'\b(?:wanted to|intended to|planned to|decided to)\b',
    'reassessment':r'\b(?:instead|actually|turned out|in fact)\b',
    'timing':r'\b(?:before|until|as soon as|by the time)\b'
}
def analyze(path):
    rx={k:re.compile(v,re.I) for k,v in P.items()}
    counts=collections.Counter(); docs=collections.Counter(); pairs=collections.Counter()
    opening=collections.Counter(); closing=collections.Counter()
    with zipfile.ZipFile(path) as z:
        for i in range(1,1729):
            h=html.fromstring(z.read(f'EPUB/chap_{i:02d}.xhtml'))
            pp=[' '.join(p.text_content().split()) for p in h.xpath('//p')]
            pp=[p for p in pp if p and not re.match(r'^(?:Chapter \d+|Translator:|Editor:|T/N:|TL/N:|Also, please check out the Author)',p,re.I)]
            seen=set(); prev=set()
            for j,p in enumerate(pp):
                curr=set()
                for k,r in rx.items():
                    n=len(r.findall(p)); counts[k]+=n
                    if n: curr.add(k); seen.add(k)
                for a in prev:
                    for b in curr: pairs[a,b]+=1
                prev=curr
                if j==0: opening.update(curr)
                if j==len(pp)-1: closing.update(curr)
            docs.update(seen)
    return {'files':1728,'families':{k:{'regex':P[k],'matches':counts[k],'files':docs[k],'opening':opening[k],'closing':closing[k]} for k in P},'adjacent_paragraphs':[{'from':a,'to':b,'count':n} for (a,b),n in sorted(pairs.items())]}
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('epub')
    args=parser.parse_args()
    print(json.dumps(analyze(args.epub),indent=2))

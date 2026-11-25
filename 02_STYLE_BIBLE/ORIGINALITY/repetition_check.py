"""Local-only screening of new prose against every approved chapter.
Usage: python repetition_check.py candidate.md /private/approved
Exit 1 = review required; 2 = invalid inputs. Never implies editorial approval.
"""
import argparse, collections, hashlib, json, pathlib, re, sys

def tokens(s):
    return re.findall(r"\b[\w]+(?:['’][\w]+)*\b", s.casefold().replace('’', "'"))

def grams(t, n):
    return {tuple(t[i:i+n]) for i in range(len(t)-n+1)}

def paragraphs(s):
    return [tokens(p) for p in re.split(r'\n\s*\n', s) if len(tokens(p)) >= 20]

def analyze(candidate, approved):
    ct=tokens(candidate); cg=grams(ct,8); cp=paragraphs(candidate)
    findings=[]; sources=[]
    for name, old in approved:
        ot=tokens(old); shared=cg & grams(ot,8)
        if shared:
            findings.append({'chapter':name,'kind':'exact_8gram','count':len(shared),'fingerprints':[hashlib.sha256(' '.join(g).encode()).hexdigest() for g in sorted(shared)]})
        op=paragraphs(old)
        for i,a in enumerate(cp,1):
            x=grams(a,3)
            for j,b in enumerate(op,1):
                y=grams(b,3); similarity=len(x&y)/len(x|y)
                if similarity>=.45:
                    findings.append({'chapter':name,'kind':'similar_paragraph','candidate_eligible_paragraph':i,'prior_eligible_paragraph':j,'jaccard':round(similarity,3)})
        sources.append({'chapter':name,'sha256':hashlib.sha256(old.encode()).hexdigest()})
    repeated={g:n for g,n in collections.Counter(tuple(ct[i:i+5]) for i in range(len(ct)-4)).items() if n>=3}
    if repeated:
        findings.append({'kind':'internal_5gram_frequency','count':len(repeated),'max_frequency':max(repeated.values())})
    return {'candidate_sha256':hashlib.sha256(candidate.encode()).hexdigest(),'sources':sources,'screening':'review_required' if findings else 'no_lexical_flags','findings':findings,'semantic_review_required':True,'approved':False}

def main():
    p=argparse.ArgumentParser();p.add_argument('candidate',type=pathlib.Path);p.add_argument('approved',type=pathlib.Path);args=p.parse_args()
    if not args.candidate.is_file() or not args.approved.is_dir():p.error('candidate file and approved directory required')
    paths=sorted(args.approved.rglob('chapter_final.md'))
    if args.candidate.resolve() in [x.resolve() for x in paths]:p.error('candidate already in approved archive')
    report=analyze(args.candidate.read_text(encoding='utf-8'),[(str(x.relative_to(args.approved)),x.read_text(encoding='utf-8')) for x in paths])
    print(json.dumps(report,indent=2));return int(bool(report['findings']))
if __name__=='__main__':sys.exit(main())

"""Materialize a private editorial reference; never publish Riot assets or claim official validation.
Pinned community release, official links, and documented import checks. Python 3.10+, stdlib.
"""
import argparse, collections, hashlib, json, pathlib, sqlite3, urllib.request, tempfile, os
ROOT=pathlib.Path(__file__).resolve().parent
S=json.loads((ROOT/'sources.json').read_text(encoding='utf-8'))
B=json.loads((ROOT/'banlists_2026-11-23.json').read_text(encoding='utf-8'))
def download(url):
    req=urllib.request.Request(url,headers={'User-Agent':'TheFinalDraw-private-reference/1.0'})
    with urllib.request.urlopen(req,timeout=90) as r:
        return r.read()
def sha(b):return hashlib.sha256(b).hexdigest()
def rows_from(raw):
    obj=json.loads(raw)
    rows=obj if isinstance(obj,list) else obj.get('cards')
    if not isinstance(rows,list) or not rows:raise ValueError('unexpected/empty snapshot shape')
    ids=[r.get('cardCode') for r in rows]
    if not all(isinstance(i,str) and i for i in ids) or len(set(ids))!=len(ids):raise ValueError('invalid/duplicate cardCode')
    for r in rows:
        for k in ('fullName','setCode','cardType','abilityOriginal','abilityEffective','hasErrata'):
            if k not in r:raise ValueError('missing '+k+' in '+r['cardCode'])
        if r['hasErrata'] and r.get('abilityCorrected') is None:raise ValueError('errata flag lacks corrected text')
    return rows
def build(rows,out):
    con=sqlite3.connect(out)
    try:
        con.execute('PRAGMA foreign_keys=ON')
        con.executescript('''CREATE TABLE printing(card_code TEXT PRIMARY KEY, name TEXT NOT NULL, set_code TEXT NOT NULL, type TEXT NOT NULL, rarity TEXT, domains TEXT, energy TEXT, power TEXT, might TEXT, printed_text TEXT, corrected_text TEXT, effective_text TEXT, has_errata INTEGER NOT NULL, source_url TEXT, source_json TEXT NOT NULL, verification_status TEXT NOT NULL);
        CREATE TABLE ban(format TEXT NOT NULL,kind TEXT NOT NULL,name TEXT NOT NULL,as_of TEXT NOT NULL,PRIMARY KEY(format,kind,name,as_of));
        CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL);
        CREATE INDEX printing_name ON printing(name); CREATE INDEX printing_set ON printing(set_code);
        CREATE VIEW errata AS SELECT card_code,name,printed_text,corrected_text,effective_text,source_url FROM printing WHERE has_errata=1;''')
        for r in rows:
            con.execute('INSERT INTO printing VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(r['cardCode'],r['fullName'],r['setCode'],r['cardType'],r.get('rarity'),json.dumps(r.get('domains',[])),r.get('energy'),r.get('power'),r.get('might'),r.get('abilityOriginal'),r.get('abilityCorrected'),r.get('abilityEffective'),int(bool(r['hasErrata'])),r.get('sourceUrl'),json.dumps(r,ensure_ascii=False),'community_unreconciled'))
        for b in B['rows']:con.execute('INSERT INTO ban VALUES (?,?,?,?)',(b['format'],b['kind'],b['name'],B['as_of']))
        con.execute('INSERT INTO metadata VALUES (?,?)',('snapshot',S['community_snapshot']['tag']))
        con.execute('INSERT INTO metadata VALUES (?,?)',('verification','community_unreconciled; never legal-play-certified'))
        con.commit()
        if con.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('sqlite integrity failed')
        if con.execute('SELECT count(*) FROM printing').fetchone()[0]!=len(rows):raise ValueError('row count mismatch')
        return dict(cards=len(rows),errata=con.execute('SELECT count(*) FROM errata').fetchone()[0],bans=con.execute('SELECT count(*) FROM ban').fetchone()[0],sets=dict(con.execute('SELECT set_code,count(*) FROM printing GROUP BY set_code').fetchall()))
    finally:con.close()
def main():
    p=argparse.ArgumentParser()
    p.add_argument('--allow-private-reference',action='store_true')
    p.add_argument('--snapshot-file',type=pathlib.Path,help='already downloaded pinned cards.json')
    p.add_argument('--skip-documents',action='store_true',help='skip downloading official files; always reports incomplete')
    args=p.parse_args()
    if not args.allow_private_reference:p.error('confirm private reference and permitted use')
    out=ROOT/'_private_reference';out.mkdir(exist_ok=True)
    raw=args.snapshot_file.read_bytes() if args.snapshot_file else download(S['community_snapshot']['url'])
    if sha(raw)!=S['community_snapshot']['sha256']:raise ValueError('snapshot SHA256 mismatch')
    rows=rows_from(raw)
    if len(rows)!=S['community_snapshot']['claimed_records']:raise ValueError('snapshot row count differs from release metadata')
    with tempfile.TemporaryDirectory(dir=out) as d:
        tmp=pathlib.Path(d)/'riftbound.sqlite'
        counts=build(rows,tmp)
        os.replace(tmp,out/'riftbound.sqlite')
    (out/'cards.json').write_bytes(raw)
    report={'snapshot_sha256':sha(raw),'counts':counts,'official_documents':[],'coverage_certified':False,'reconciliation_required':True}
    if not args.skip_documents:
        for item in S['rules']+S['errata']+S['patch_and_faq']:
            try:
                data=download(item['url'])
                ext='.pdf' if item['url'].endswith('.pdf') else '.html'
                if ext=='.pdf' and not data.startswith(b'%PDF-'):raise ValueError('not PDF')
                (out/(item['id']+ext)).write_bytes(data)
                report['official_documents'].append({'id':item['id'],'sha256':sha(data),'bytes':len(data),'status':'downloaded_unreviewed'})
            except Exception as e:report['official_documents'].append({'id':item['id'],'status':'failed','error':str(e)})
    (out/'manifest.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()

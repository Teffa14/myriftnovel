"""Private official English gallery refresh; store factual provenance and printed text only.
No effective-text/legality claim, no card art download. stdlib Python 3.10+.
"""
import argparse, collections, hashlib, json, os, pathlib, sqlite3, tempfile, time, urllib.parse, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
SOURCE=json.loads((ROOT/'sources.json').read_text(encoding='utf-8'))['gallery_feed']
def get(url):
    req=urllib.request.Request(url,headers={'Accept':'application/json','User-Agent':'TheFinalDraw-private-reference/1.0'})
    with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
def fetch_pages(endpoint,limit=100):
    rows={};expected=None;offset=0;pages=[]
    while offset<20000:
        url=endpoint+'?'+urllib.parse.urlencode({'locale':'en_US','from':offset,'limit':limit})
        page=get(url); data=page.get('data');meta=page.get('metadata',{});total=meta.get('totalItems')
        if not isinstance(data,list) or not isinstance(total,int) or total<1:raise ValueError('malformed gallery page')
        if expected is None:expected=total
        if total!=expected:raise ValueError('gallery changed during pagination; retry')
        if not data and offset<expected:raise ValueError('unexpected empty page')
        pages.append({'url':url,'total':total,'returned':len(data),'updated':meta.get('resultsUpdatedAt')})
        for r in data:
            i=r.get('id')
            if not i or i in rows:raise ValueError('missing/duplicate ID: '+str(i))
            rows[i]=r
        offset+=limit
        if offset>=expected:break
        time.sleep(.3)
    if len(rows)!=expected:raise ValueError(f'unique count {len(rows)} differs from advertised {expected}')
    return list(rows.values()),pages,expected
def value(r,k):
    return (r.get(k) or {}).get('value') or {}
def build(rows,dest):
    con=sqlite3.connect(dest)
    try:
        con.execute('CREATE TABLE printing(id TEXT PRIMARY KEY, public_code TEXT, name TEXT NOT NULL, subtitle TEXT, set_code TEXT, type TEXT, rarity TEXT, domains TEXT, energy TEXT, power TEXT, might TEXT, printed_rich_text TEXT, source_json TEXT NOT NULL, verification_status TEXT NOT NULL)')
        con.execute('CREATE INDEX printing_set ON printing(set_code)')
        for r in rows:
            name=r.get('name')
            if not name:raise ValueError('missing name '+r['id'])
            sub=r.get('subtitle')
            if isinstance(sub,dict):sub=(sub.get('value') or {}).get('label') or sub.get('label')
            kind=((r.get('cardType') or {}).get('type') or [{}])[0].get('label')
            text=((r.get('text') or {}).get('richText') or {}).get('body') or ((r.get('effect') or {}).get('richText') or {}).get('body')
            domains=[d.get('label') for d in (r.get('domain') or {}).get('values',[])]
            con.execute('INSERT INTO printing VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(r['id'],r.get('publicCode'),name,sub,value(r,'set').get('id'),kind,value(r,'rarity').get('label'),json.dumps(domains),value(r,'energy').get('id'),value(r,'power').get('id'),value(r,'might').get('id'),text,json.dumps(r,ensure_ascii=False),'official_printed_only;errata_unreconciled'))
        con.commit()
        if con.execute('PRAGMA integrity_check').fetchone()[0]!='ok' or con.execute('SELECT count(*) FROM printing').fetchone()[0]!=len(rows):raise ValueError('database validation failed')
        return dict(con.execute('SELECT set_code,count(*) FROM printing GROUP BY set_code').fetchall())
    finally:con.close()
def main():
    p=argparse.ArgumentParser();p.add_argument('--allow-private-reference',action='store_true');p.add_argument('--page-size',type=int,default=100);args=p.parse_args()
    if not args.allow_private_reference:p.error('confirm private reference and permitted use')
    if not 1<=args.page_size<=200:p.error('page-size must be 1..200')
    out=ROOT/'_private_reference';out.mkdir(exist_ok=True)
    rows,pages,total=fetch_pages(SOURCE['url'],args.page_size)
    raw=json.dumps(rows,ensure_ascii=False,sort_keys=True).encode('utf-8')
    with tempfile.TemporaryDirectory(dir=out) as t:
        tmp=pathlib.Path(t)/'gallery.sqlite';sets=build(rows,tmp)
        os.replace(tmp,out/'gallery.sqlite')
    (out/'gallery_raw.json').write_bytes(raw)
    report={'cards':total,'sets':sets,'source':SOURCE['url'],'pages':pages,'sha256':hashlib.sha256(raw).hexdigest(),'printed_feed_complete_at_fetch':True,'effective_text_reconciled':False,'legal_play_certified':False}
    (out/'gallery_manifest.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':main()

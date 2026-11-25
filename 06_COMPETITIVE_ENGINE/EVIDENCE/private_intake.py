"""Validate local authorized research inputs; do not upload or fetch protected data."""
import argparse,json,collections,decimal,datetime,pathlib,hashlib
p=argparse.ArgumentParser()
p.add_argument('file',type=pathlib.Path)
p.add_argument('--kind',choices=['prices','scenarios'],required=True)
p.add_argument('--out',type=pathlib.Path,required=True)
a=p.parse_args()
raw=a.file.read_bytes();data=json.loads(raw)
report={'kind':a.kind,'sha256':hashlib.sha256(raw).hexdigest(),'source_file':a.file.name,'verified_scope':'shape and data quality only; no rules or price identity certified'}
if a.kind=='prices':
    if not isinstance(data,list):raise ValueError('expected observations array')
    counts=collections.Counter();keys=set();duplicates=0;bad=0;dates=[]
    for r in data:
        try:
            required=['printingId','publicCode','source','currency','amount','observedAt']
            if any(r.get(k) is None or r.get(k)=='' for k in required):raise ValueError('missing field')
            amount=decimal.Decimal(str(r['amount']))
            if not amount.is_finite() or amount<0:raise ValueError('amount')
            stamp=datetime.datetime.fromisoformat(r['observedAt'].replace('Z','+00:00'))
            if stamp.tzinfo is None:raise ValueError('timezone required')
            key=(r['printingId'],r['source'],r['currency'],r['observedAt'])
            if key in keys:duplicates+=1
            keys.add(key);counts[(r['currency'],r['source'])]+=1;dates.append(stamp)
        except (ValueError,TypeError,KeyError,decimal.InvalidOperation):bad+=1
    report.update(records=len(data),unique_keys=len(keys),duplicates=duplicates,invalid=bad,source_currency_counts=[{'currency':c,'source':s,'count':n} for (c,s),n in counts.items()],first=min(dates).isoformat() if dates else None,last=max(dates).isoformat() if dates else None)
else:
    if not isinstance(data,dict):raise ValueError('expected scenario mapping')
    report.update(records=len(data),topics=[{'id':k,'title':v.get('title'),'concept':v.get('concept')} for k,v in data.items() if isinstance(v,dict)])
a.out.parent.mkdir(parents=True,exist_ok=True)
a.out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))

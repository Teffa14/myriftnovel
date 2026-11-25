"""Measure supplied EPUB; aggregate data only. Requires lxml."""
import zipfile,sys,re,json,hashlib,statistics,os
from lxml import etree as E
p=sys.argv[1]; z=zipfile.ZipFile(p); word=re.compile(r"[^\W\d_]+(?:[’'-][^\W\d_]+)*",re.UNICODE)
root=E.fromstring(z.read('epub/content.opf'))
manifest={x.get('id'):x.get('href') for x in root.xpath('//*[local-name()="manifest"]/*')}
spine=[manifest[x.get('idref')] for x in root.xpath('//*[local-name()="spine"]/*')]
books=[]
for path in spine:
    if not re.fullmatch(r'text/book-\d+\.xhtml',path): continue
    r=E.fromstring(z.read('epub/'+path))
    for a in r.xpath('//*[local-name()="a" and @*[local-name()="type"]="noteref"]'):
        prev=a.getprevious(); tail=a.tail or ''; par=a.getparent()
        if prev is None: par.text=(par.text or '')+tail
        else: prev.tail=(prev.tail or '')+tail
        par.remove(a)
    ps=[' '.join(''.join(x.itertext()).split()) for x in r.xpath('//*[local-name()="section"]/*[local-name()="p"]')]
    ps=[x for x in ps if x]; n=int(re.search(r'book-(\d+)',path)[1]); s='\n'.join(ps)
    lens=[len(word.findall(x)) for x in ps]
    sentences=[x for x in re.split(r'(?<=[.!?])\s+',s) if word.search(x)]
    books.append([n,len(ps),sum(lens),len(sentences),round(statistics.mean(lens),2)])
assert [b[0] for b in books]==list(range(1,13))
print(json.dumps({'sha256':hashlib.sha256(open(p,'rb').read()).hexdigest(),'bytes':os.path.getsize(p),'spine_items':len(spine),'books':books,'total_paragraphs':sum(x[1] for x in books),'total_words':sum(x[2] for x in books),'total_sentence_proxy':sum(x[3] for x in books)},indent=2))

"""Measure the supplied PDF locally; prints aggregate metrics, never source prose."""
import sys, re, statistics, json
import fitz
ranges = {"MUS-PREF":(18,19),"MUS-EARTH":(20,30),"MUS-WATER":(31,49),"MUS-FIRE":(50,64),"MUS-WIND":(65,74),"MUS-EMPTY":(75,76),"YAG-KILLING":(81,98),"YAG-LIFE":(99,112),"YAG-NOSWORD":(113,119)}
word = re.compile(r"[^\W\d_]+(?:[’'-][^\W\d_]+)*", re.UNICODE)
with fitz.open(sys.argv[1]) as doc:
    pages = [p.get_text() for p in doc]
    assert len(pages) == 136
out = {}
for key,(a,b) in ranges.items():
    s = " ".join(pages[a-1:b])
    w = word.findall(s)
    sentences = [x for x in re.split(r"(?<=[.!?])\s+",s) if word.search(x)]
    lens = [len(word.findall(x)) for x in sentences]
    out[key] = [a,b,len(w),len(lens),round(statistics.mean(lens),2),statistics.median(lens),s.count("?"),s.count("!")]
print(json.dumps({"units":out,"total_words":sum(x[2] for x in out.values())},indent=2))

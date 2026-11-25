"""Count narrative tokens in an English MSC excerpt; no source text is distributed."""
import argparse
import hashlib
import json
import re
from pathlib import Path

def measure(s):
    b = s.split("Translator's Notes:")[0]
    b = re.sub(r"(?m)^(Translator:.*|Proofreader:.*|Original translation from.*)\s*$", "", b).strip()
    tok = lambda x: re.findall(r"\b[\w]+(?:['’][\w]+)*\b", x)
    q = re.findall(r'“([^”]*)”|"([^"\n]*)"', b)
    return dict(words=len(tok(b)), paragraphs=len([p for p in re.split(r"\n\s*\n", b) if p.strip()]), quoted_spans=len(q), quoted_words=sum(len(tok(a or c)) for a,c in q), question_marks=b.count("?"), exclamation_marks=b.count("!"), sha256=hashlib.sha256(s.encode()).hexdigest())

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("path")
    args = p.parse_args()
    print(json.dumps(measure(Path(args.path).read_text(encoding="utf-8")), ensure_ascii=False, indent=2))

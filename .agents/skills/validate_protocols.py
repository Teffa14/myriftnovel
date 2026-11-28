"""Public structural checks; no literary, rights or private archive certification."""
import csv, json, pathlib, re
ROOT=pathlib.Path(__file__).resolve().parents[2]
def load(p): return json.loads((ROOT/p).read_text(encoding="utf-8"))
def main():
    p=load("08_CHAPTERS/PROTOCOL_REGISTRY.json")
    s=load(".agents/skills/registry.json")
    t=load("08_CHAPTERS/PROTOCOL_COVERAGE_TEMPLATE.json")
    paths=set(p["all_paths"])
    assert all((ROOT/x).is_file() for x in paths), "Missing protocol file"
    expected={x for f in p["families"] for x in f["paths"]}|{x["path"] for x in s["skills"]}|{q for x in s["skills"] for q in x["references"]}
    assert paths==expected, "Incomplete protocol registry"
    assert {x["path"] for x in t["protocols"]}==paths and len(t["protocols"])==len(paths), "Coverage template mismatch"
    ids={x["id"] for x in p["directives"]}
    author=(ROOT/"05_PLOT_ARCHITECTURE/AUTHOR_DIRECTIVES.md").read_text(encoding="utf-8")
    assert set(re.findall(r"(?m)^#{2,4} (AD-\d{4}(?:-[AE]\d{2})?)\b",author))<=ids, "Unregistered directive"
    assert all(x in author for x in ids), "Missing directive source"
    assert {x["id"] for x in t["directives"]}==ids and len(t["directives"])==len(ids), "Directive coverage mismatch"
    for x in s["skills"]:
        body=(ROOT/x["path"]).read_text(encoding="utf-8")
        assert all(q in body and (ROOT/q).is_file() for q in x["references"]), x["id"]
    with (ROOT/"01_RESEARCH/REFERENCE_LIBRARY/CATALOG.tsv").open(encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f,delimiter="\t"))
    assert len(rows)==len({x["id"] for x in rows}), "Duplicate catalog ID"
    assert {"LC-MB","LC-EV","LC-LLD","LC-MF","LC-PE","LC-TD"}<={x["id"] for x in rows}, "Missing literary references"
    print(json.dumps({"status":"PASS","paths":len(paths),"directives":len(ids),"skills":len(s["skills"]),"skill_references":sum(len(x["references"]) for x in s["skills"]),"catalog_rows":len(rows),"scope":"public structure only"}))
if __name__=="__main__": main()

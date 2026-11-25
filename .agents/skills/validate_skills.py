"""Structural checks for the project skill pack; no private data required."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / ".agents" / "skills"
registry = json.loads((PACK / "registry.json").read_text(encoding="utf-8"))
ids = {s["id"] for s in registry["skills"]}
assert len(ids) == len(registry["skills"]) == 11
for skill in registry["skills"]:
    path = ROOT / skill["path"]
    content = path.read_text(encoding="utf-8")
    assert content.startswith("---\n"), path
    assert re.search(r"^name: " + re.escape(skill["id"]) + r"$", content, re.M), path
    assert re.search(r"^description: .+", content, re.M), path
    for ref in skill["references"]:
        assert (ROOT / ref).is_file(), ref
        assert ref in content, (path, ref)
for route, steps in registry["routes"].items():
    assert all(step.split(":")[0] in ids for step in steps), route
assert "tld-closeout" not in registry["routes"]["write_next_chapter"]
assert registry["routes"]["approved_closeout"][-1] == "tld-closeout"
assert registry["routes"]["write_next_chapter"][-1] == "tld-originality"
assert all((ROOT / s["path"]).is_file() for s in registry["skills"])
print(f"PASS: {len(ids)} skills; {sum(len(s['references']) for s in registry['skills'])} reference entries; {len(registry['routes'])} routes; explicit close-out separation")

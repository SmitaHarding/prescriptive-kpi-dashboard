"""Traceability check: no model, no network.

Run from the repository root:  python evals/check.py
Update the README status block: python evals/check.py --update-readme

The chain (N6, N17): v1 defect -> risk -> requirement -> eval case -> code -> claim.
This F1 version checks it up to requirement.
Checks (F1 version; F2a adds cases and known-bad inputs, F3 the harness links):
  1. IDs in spec/registers.toml are unique and well formed.
  2. Every decision in the registers is in method/decisions.md, and vice versa.
  3. Every requirement in the registers is in method/02-requirements.md, and vice versa.
  4. Every link points to an ID that exists (risk evidence, requirement risks,
     decision safeguards).
  5. Coverage: every v1 defect is evidence for a risk; every risk is controlled by a
     requirement; every requirement controls a risk; every safeguard is in force.
  6. Every ID mentioned in the tracked docs (top-level .md files in method/, spec/,
     data/, evals/ and prototype/, the data files in spec/ other than registers.toml,
     CLAUDE.md and README.md) exists, and no doc other than decisions.md mentions a retired ID
     (D1-D93, SG-01-SG-11). method/archive/ is history and is not scanned.
  7. Every entry in the Superseded section names an active decision that replaces it.
  8. The README status block matches the registers (it is generated, never hand-edited).
Exit code 0 when clean, 1 when anything fails.
"""
import re
import sys
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib

ROOT = Path(__file__).resolve().parent.parent
REG = tomllib.loads((ROOT / "spec" / "registers.toml").read_text(encoding="utf-8"))
PATTERN = {
    "decision": r"N\d+",
    "risk": r"RK-\d{2}",
    "requirement": r"R-(?:DET|RL|JDG)-\d{2}",
    "v1_defect": r"V1-\d{2}",
    "safeguard": r"SG-\d",
}
MENTION = re.compile(r"\b(V1-\d{2}|SG-\d{1,2}|RK-\d{2}|R-(?:DET|RL|JDG)-\d{2}|N\d+|D\d+)\b")
RETIRED = re.compile(r"^(D\d+|SG-\d{2})$")
BLOCK = re.compile(r"(<!-- gen:status -->\n)(.*?)(<!-- /gen:status -->)", re.S)
errors = []

# 1. IDs
ids = {}
for kind, pat in PATTERN.items():
    seen = [e["id"] for e in REG.get(kind, [])]
    for i in seen:
        if not re.fullmatch(pat, i):
            errors.append(f"{kind} {i}: malformed ID")
    for i in {x for x in seen if seen.count(x) > 1}:
        errors.append(f"{kind} {i}: duplicate ID")
    ids[kind] = set(seen)
known = set().union(*ids.values())

# 2. Decisions
log = (ROOT / "method" / "decisions.md").read_text(encoding="utf-8")
head, _, rest = log.partition("\n## Superseded")
superseded_part, _, mapping = rest.partition("\n## Mapping")
active = set(re.findall(r"^(?:\| |\*\*)(N\d+)(?: \||\s·)", head, re.M))
superseded = set(re.findall(r"^\| (N\d+) \|", superseded_part, re.M))
for d in sorted(ids["decision"] - active - superseded):
    errors.append(f"{d}: in registers but not in decisions.md")
for d in sorted((active | superseded) - ids["decision"]):
    errors.append(f"{d}: in decisions.md but not in registers")
retired = set(re.findall(r"^\| (D\d+|SG-\d{2}) \|", mapping, re.M))

# 3. Requirements
reqs = (ROOT / "method" / "02-requirements.md").read_text(encoding="utf-8")
written = set(re.findall(r"^\*\*(R-(?:DET|RL|JDG)-\d{2}) ·", reqs, re.M))
for r in sorted(ids["requirement"] - written):
    errors.append(f"{r}: in registers but not in 02-requirements.md")
for r in sorted(written - ids["requirement"]):
    errors.append(f"{r}: in 02-requirements.md but not in registers")

# 4. Links and 5. coverage
evidenced, controlled, in_force = set(), set(), set()
for k in REG.get("risk", []):
    for v in k.get("evidence", []):
        if v not in ids["v1_defect"]:
            errors.append(f"{k['id']}.evidence: unknown ID {v}")
        evidenced.add(v)
for r in REG.get("requirement", []):
    if not r.get("risks"):
        errors.append(f"{r['id']}: controls no risk")
    for k in r.get("risks", []):
        if k not in ids["risk"]:
            errors.append(f"{r['id']}.risks: unknown ID {k}")
        controlled.add(k)
for d in REG.get("decision", []):
    for sg in d.get("safeguards", []):
        if sg not in ids["safeguard"]:
            errors.append(f"{d['id']}.safeguards: unknown ID {sg}")
        in_force.add(sg)
for v in sorted(ids["v1_defect"] - evidenced):
    errors.append(f"{v}: not evidence for any risk")
for k in sorted(ids["risk"] - controlled):
    errors.append(f"{k}: no requirement controls it")
for sg in sorted(ids["safeguard"] - in_force):
    errors.append(f"{sg}: no decision brings it into force")

# 6. Mentions in tracked docs
docs = [ROOT / "CLAUDE.md", ROOT / "README.md"]
for folder in ("method", "spec", "data", "evals", "prototype"):
    docs += sorted((ROOT / folder).glob("*.md"))
docs += [p for p in sorted((ROOT / "spec").glob("*.toml")) if p.name != "registers.toml"]
for doc in docs:
    if not doc.exists():
        continue
    found = set(MENTION.findall(doc.read_text(encoding="utf-8")))
    for ref in sorted(found):
        if RETIRED.match(ref):
            if doc.name != "decisions.md":
                errors.append(f"{doc.relative_to(ROOT)}: mentions retired {ref}")
            elif ref not in retired:
                errors.append(f"decisions.md: {ref} missing from the mapping table")
        elif ref not in known:
            errors.append(f"{doc.relative_to(ROOT)}: mentions unknown ID {ref}")

# 7. Superseded entries name their replacement
for row in re.finditer(r"^\| (N\d+) \|(.*)\|$", superseded_part, re.M):
    named = set(re.findall(r"Superseded by (N\d+)", row.group(2)))
    if not named & active:
        errors.append(f"{row.group(1)}: Superseded row does not name an active replacement")


# 8. README status block
def status_block():
    st = REG["status"]
    built = ", ".join(st["built"]) or "no product code yet — the harness comes first"
    return (f"**Stage:** {st['stage']} · **Next:** {st['next']}  \n"
            f"**Built so far:** {built}\n")


readme = ROOT / "README.md"
text = readme.read_text(encoding="utf-8")
m = BLOCK.search(text)
if "--update-readme" in sys.argv and m:
    readme.write_text(BLOCK.sub(lambda x: x.group(1) + status_block() + x.group(3), text),
                      encoding="utf-8")
    m = BLOCK.search(readme.read_text(encoding="utf-8"))
if not m:
    errors.append("README.md: status block markers missing")
elif m.group(2) != status_block():
    errors.append("README.md: status block is stale — run with --update-readme")

if errors:
    print(f"check.py: {len(errors)} problem(s)")
    print("\n".join(f"  - {e}" for e in errors))
    sys.exit(1)
print(f"check.py: clean — {len(ids['decision'])} decisions, {len(ids['risk'])} risks, "
      f"{len(ids['requirement'])} requirements, {len(ids['v1_defect'])} v1 defects, "
      f"{len(ids['safeguard'])} safeguards")

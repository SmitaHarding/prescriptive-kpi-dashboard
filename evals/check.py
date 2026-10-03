"""Traceability check — no model, no network.

Run from the repository root:  python evals/check.py
Update the README status block: python evals/check.py --update-readme

Checks (F1 version; grows in F2 and F3):
  1. IDs in spec/registers.toml are unique and well formed.
  2. Every decision in the registers appears in method/decisions.md, and vice versa.
  3. Every link (prevents, supersedes, safeguards) points to an ID that exists.
  4. Every v1 defect is prevented by at least one decision; every safeguard is in force.
  5. Every D / V1 / SG ID mentioned in the tracked docs (method/, spec/, data/, evals/,
     CLAUDE.md, README.md) exists.
  6. The README status block matches the registers (it is generated, never hand-edited).
  7. Every entry in the Superseded section is replaced by an active decision, says
     which one, and carries no prevents or safeguards of its own.
  8. No tracked doc other than decisions.md mentions a superseded decision.
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
PATTERN = {"decision": r"D\d+", "v1_defect": r"V1-\d{2}", "safeguard": r"SG-\d{2}"}
MENTION = re.compile(r"\b(V1-\d{2}|SG-\d{2}|D\d+)\b")
BLOCK = re.compile(r"(<!-- gen:status -->\n)(.*?)(<!-- /gen:status -->)", re.S)
errors = []

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

log = (ROOT / "method" / "decisions.md").read_text(encoding="utf-8")
logged = set(re.findall(r"^\| (D\d+) \|", log, re.M))
for d in sorted(ids["decision"] - logged):
    errors.append(f"{d}: in registers but not in decisions.md")
for d in sorted(logged - ids["decision"]):
    errors.append(f"{d}: in decisions.md but not in registers")

prevented, in_force = set(), set()
for d in REG.get("decision", []):
    for field in ("prevents", "supersedes", "safeguards"):
        for ref in d.get(field, []):
            if ref not in known:
                errors.append(f"{d['id']}.{field}: unknown ID {ref}")
    prevented |= set(d.get("prevents", []))
    in_force |= set(d.get("safeguards", []))
for v in sorted(ids["v1_defect"] - prevented):
    errors.append(f"{v}: no decision prevents it")
for sg in sorted(ids["safeguard"] - in_force):
    errors.append(f"{sg}: no decision brings it into force")

head, _, tail = log.partition("\n## Superseded")
active = set(re.findall(r"^\| (D\d+) \|", head, re.M))
replaced_by = {}
for d in REG.get("decision", []):
    for old in d.get("supersedes", []):
        replaced_by.setdefault(old, set()).add(d["id"])
by_id = {d["id"]: d for d in REG.get("decision", [])}
for row in re.finditer(r"^\| (D\d+) \|(.*)\|$", tail, re.M):
    old, body = row.group(1), row.group(2)
    news = replaced_by.get(old, set()) & active
    named = set(re.findall(r"Superseded by (D\d+)", body))
    if not news:
        errors.append(f"{old}: in Superseded but no active decision supersedes it")
    elif not named & news:
        errors.append(f"{old}: Superseded row does not name its replacement {sorted(news)}")
    if by_id.get(old, {}).get("prevents") or by_id.get(old, {}).get("safeguards"):
        errors.append(f"{old}: superseded but still carries prevents/safeguards")

superseded = set(re.findall(r"^\| (D\d+) \|", tail, re.M))
docs = [ROOT / "CLAUDE.md", ROOT / "README.md"]
for folder in ("method", "spec", "data", "evals"):
    docs += sorted((ROOT / folder).glob("*.md"))
for doc in docs:
    if doc.exists():
        found = set(MENTION.findall(doc.read_text(encoding="utf-8")))
        for ref in sorted(found - known):
            errors.append(f"{doc.relative_to(ROOT)}: mentions unknown ID {ref}")
        if doc.name != "decisions.md":
            for ref in sorted(found & superseded):
                errors.append(f"{doc.relative_to(ROOT)}: mentions superseded {ref}")


def status_block():
    st = REG["status"]
    built = ", ".join(st["built"]) or "nothing yet — the harness comes first"
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
print(f"check.py: clean — {len(ids['decision'])} decisions, "
      f"{len(ids['v1_defect'])} v1 defects, {len(ids['safeguard'])} safeguards")

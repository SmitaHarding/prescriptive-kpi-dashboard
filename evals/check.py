"""Traceability check: no model, no network.

Run from the repository root:  python evals/check.py
Update the README status block: python evals/check.py --update-readme

The chain (N26, N30): v1 defect -> risk -> requirement -> eval case -> code -> status claim.
It checks the chain up to requirement, and the documents and data files around it.
Checks 1-8 date from F1; 9-12 from F2a; 13 from the 26 Oct decision batch. Later checks follow R-DET-15; F3 adds the harness links.
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
  7. Every entry in the Superseded section names an active decision that replaces it,
     directly or through a chain of replacements.
  8. The README status block matches the registers (it is generated, never hand-edited).
  9. Terms: no tracked .md doc uses a phrase the registers say a preferred term replaces.
     Exact phrases only, so "a separate agent" and "reviewer agent" pass. The Superseded
     table in decisions.md keeps old wording word for word and is skipped.
 10. Numbers: no tracked .md doc states a tunable value from the data files with its unit
     (a percentage, hours, calendar or business days, weeks, FTEs). Design facts with no
     tunable twin, such as "52 weeks", pass.
 11. Mirrors: a data file that mirrors a design fact matches it. Today: the dispute window
     in spec/metrics.toml matches N12.
 12. Known-bad inputs (evals/known_bad/) still sit where the data files put them: colours,
     rounding, capacity results, effort ranges, due weeks, forbidden types, the stuck limit,
     the trend window, the confidence minimum and day counts. Data-file lists hold together:
     every cause id has an underscore (R-DET-12), the playbook cites only listed causes, and
     no playbook type is forbidden (R-DET-07). Checks 9 and 10 must also reject R-DET-15's
     known-bad lines and pass its must-pass lines (the check tests itself).
 13. No stale citations: no tracked doc or known-bad file cites a superseded decision.
     In decisions.md, the preamble and the Superseded table may name them.
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
    NEXT = {d["id"]: d["superseded_by"] for d in REG.get("decision", []) if d.get("superseded_by")}
    for n in list(named):  # follow a chain such as N10 -> N24 -> N32
        while n in NEXT:
            n = NEXT[n]
            named.add(n)
    if not named & active:
        errors.append(f"{row.group(1)}: Superseded row does not name an active replacement")


# Data files used by checks 9-12
def load(rel):
    return tomllib.loads((ROOT / rel).read_text(encoding="utf-8"))


METRICS = load("spec/metrics.toml")
CAPACITY = load("spec/capacity.toml")
THRESHOLDS = load("spec/thresholds.toml")
PLAYBOOK = load("spec/playbook.toml")
METRIC = {m["id"]: m for m in METRICS["metric"]}
ENTRY = {e["type"]: e for e in PLAYBOOK["entry"]}
md_docs = [d for d in docs if d.suffix == ".md" and d.exists()]

# 9. Terms
REPLACED = [(t["use"], old) for t in REG.get("term", []) for old in t.get("replaces", [])]


def term_hits(text):
    return [(use, old) for use, old in REPLACED
            if re.search(r"\b" + re.escape(old) + r"\b", text, re.I)]


def scanned_lines(doc):
    """A doc's lines, with decisions.md's Superseded table blanked (old wording stays as it was)."""
    lines = doc.read_text(encoding="utf-8").splitlines()
    if doc.name == "decisions.md":
        inside = False
        for i, line in enumerate(lines):
            if line.startswith("## "):
                inside = line.startswith("## Superseded")
            if inside:
                lines[i] = ""
    return lines


for doc in md_docs:
    for i, line in enumerate(scanned_lines(doc), 1):
        for use, old in term_hits(line):
            errors.append(f"{doc.relative_to(ROOT)}:{i}: '{old}' — use '{use}' (N26)")


# 10. Numbers: tunable values with their unit
def num(v):
    v = float(v)
    return str(int(v)) if v == int(v) else str(v)


tunable = []  # (value text, unit pattern, source)
for m in METRICS["metric"]:
    for key in ("target", "red_beyond"):
        if key in m:
            tunable.append((num(m[key]), r"\s?%", f"metrics.toml {m['id']}.{key}"))
    if "time_limit_business_days" in m:
        tunable.append((num(m["time_limit_business_days"]), r"\s(?:working|business)\sdays?",
                        f"metrics.toml {m['id']}"))
    if "stuck_limit_calendar_days" in m:
        tunable.append((num(m["stuck_limit_calendar_days"]), r"\s(?:calendar\s)?days?",
                        f"metrics.toml {m['id']}"))
tunable.append((num(CAPACITY["utilisation"]["ceiling"] * 100), r"\s?%", "capacity.toml ceiling"))
tunable.append((num(CAPACITY["team_fte"]), r"\s?(?:FTEs?|people)\b", "capacity.toml team_fte"))
for key, val in list(CAPACITY.items()) + list(CAPACITY["workload"].items()):
    if "hours" in key and isinstance(val, (int, float)):
        tunable.append((num(val), r"\s?(?:h|hours?)\b", f"capacity.toml {key}"))
for e in PLAYBOOK["entry"]:
    for v in e["effort_hours"]:
        tunable.append((num(v), r"\s?(?:h|hours?)\b", f"playbook.toml {e['type']}"))
for e in PLAYBOOK["entry"]:
    tunable.append((num(e["weeks_allowed"]), r"[\s-]weeks?\b", f"playbook.toml {e['type']}.weeks_allowed"))
tunable.append((num(THRESHOLDS["trends"]["trend_window_weeks"]), r"[\s-]weeks?\b",
                "thresholds.toml trend_window_weeks"))
NUMBER = [(re.compile(r"(?<![\d.,])" + re.escape(v) + r"(?:\.0+)?" + unit, re.I), src)
          for v, unit, src in tunable]


def number_hits(text):
    return sorted({src for pat, src in NUMBER if pat.search(text)})


for doc in md_docs:
    for i, line in enumerate(doc.read_text(encoding="utf-8").splitlines(), 1):
        for src in number_hits(line):
            errors.append(f"{doc.relative_to(ROOT)}:{i}: states a tunable number ({src}); "
                          f"cite the data file instead (N26)")

# 11. Mirrors
n12 = re.search(r"\*\*N12 ·.*?(?=\n\*\*N\d+ ·)", log, re.S)
window = re.search(r"dispute\s+within\s+(\d+)\s+days", n12.group(0)) if n12 else None
if not window:
    errors.append("decisions.md: N12's dispute window not found")
elif int(window.group(1)) != METRICS["windows"]["dispute_window_days"]:
    errors.append(f"metrics.toml dispute_window_days ({METRICS['windows']['dispute_window_days']}) "
                  f"differs from N12 ({window.group(1)} days)")

# 12. Known-bad inputs still match the data files
from decimal import Decimal, ROUND_HALF_UP  # noqa: E402

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
COLOURS = {"red", "amber", "green"}


def day(s):  # "Wed week 31" -> a day number
    d, _, w = s.split()
    return int(w) * 7 + DAYS.index(d)


def colour(metric, shown):
    m = METRIC[metric]
    t, r = m["target"], m["red_beyond"]
    if m["direction"] == "higher_is_better":
        return "green" if shown >= t else "red" if shown < r else "amber"
    return "green" if shown <= t else "red" if shown > r else "amber"


def known_bad(name):
    path = ROOT / "evals" / "known_bad" / f"{name}.toml"
    return tomllib.loads(path.read_text(encoding="utf-8"))["case"] if path.exists() else []


def kb_fail(name, case, msg):
    errors.append(f"known_bad/{name}.toml {case['requirement']} ({case['covers'][:40]}): {msg}")


places = Decimal(1).scaleb(-METRICS["display"]["decimals"])
for c in known_bad("dec1"):
    rows = c.get("rows") or c.get("weeks") or [c]
    rows += [dict(v, metric=c.get("metric"), right=v["colour"]) for k, v in c.items()
             if k in ("provisional", "final") and isinstance(v, dict)]
    for r in rows:
        metric, shown, right = r.get("metric", c.get("metric")), r.get("shown"), r.get("right")
        if "raw" in r and Decimal(str(r["raw"])).quantize(places, ROUND_HALF_UP) != Decimal(str(shown)):
            kb_fail("dec1", c, f"raw {r['raw']} does not show as {shown}")
        if metric in METRIC and shown is not None and right in COLOURS:
            if colour(metric, shown) != right:
                kb_fail("dec1", c, f"{metric} {shown} is {colour(metric, shown)}, case says {right}")
        if "days" in r and "entered_step" in r:
            limit = METRIC["stuck_invoices"]["stuck_limit_calendar_days"]
            if day(c["review"]) - day(r["entered_step"]) != r["days"]:
                kb_fail("dec1", c, f"{r['entered_step']}: day count is not {r['days']}")
            if (r["days"] > limit) != (r["right"] == "listed"):
                kb_fail("dec1", c, f"{r['days']} days against a limit of {limit}: not {r['right']}")
    if c.get("right") == "none" and METRIC[c["metric"]]["shown"] != "monitored":
        kb_fail("dec1", c, f"{c['metric']} is not monitored")
    if "earlier_weeks" in c and c["earlier_weeks"] != THRESHOLDS["trends"]["trend_window_weeks"] - 1:
        kb_fail("dec1", c, "earlier_weeks is not one fewer than the trend window")

cap = CAPACITY
productive = cap["team_fte"] * (cap["hours_per_fte"] - cap["protected_hours_per_fte"])
ceiling_h = cap["utilisation"]["ceiling"] * productive
overtime_max = cap["team_fte"] * cap["overtime_hours_per_fte"]
for c in known_bad("dec4"):
    for r in c.get("rows", []):
        if "workload" in r:
            over = max(0.0, r["workload"] - ceiling_h)
            got = {"overtime": min(over, overtime_max), "exec_hours": over - min(over, overtime_max),
                   "room": max(0.0, ceiling_h - r["workload"])}
            for k, v in r["right"].items():
                if abs(got[k] - v) > 1e-9:
                    kb_fail("dec4", c, f"{r['week']}: {k} is {got[k]:g}, case says {v}")
        if "committed" in r and r["committed"] <= productive + r["approved_overtime"]:
            kb_fail("dec4", c, f"committed {r['committed']} fits; the bad plan is not bad")
    if "intervention" in c:
        top = max(ENTRY[c["intervention"]["type"]]["effort_hours"])
        if c["intervention"]["effort_hours"] != ENTRY[c["intervention"]["type"]]["effort_hours"] or c["right"] != top:
            kb_fail("dec4", c, "effort range or its top no longer matches the playbook")
    plan = c.get("plan", {})
    if "contracted" in plan and plan["contracted"] + plan["overtime"] <= cap["max_hours_per_person"]:
        kb_fail("dec4", c, "the person is within the limit; the bad plan is not bad")
    if "proposed_overtime" in plan and plan["committed"] <= productive + plan["approved_overtime"]:
        kb_fail("dec4", c, "the plan fits without the unapproved overtime; not bad")

high_min = THRESHOLDS["confidence"]["high_min_evidence_types"]
for c in known_bad("dec2"):
    for r in c.get("rows", []):
        if r.get("computed") == "high" and (len(r["evidence_types"]) < high_min or r["gaps"]):
            kb_fail("dec2", c, "a row computed high has too few types or a gap")
        if r.get("bad") == "high" and not r["gaps"] and len(r["evidence_types"]) >= high_min:
            kb_fail("dec2", c, "a row labelled bad for too few types now meets the minimum")

CAUSES = load("spec/causes.toml")
cause_ids = {c["id"] for c in CAUSES["cause"]}
for cid in sorted(cause_ids):
    if "_" not in cid:
        errors.append(f"causes.toml: id '{cid}' has no underscore; the leakage scan (R-DET-12) "
                      f"cannot tell it from a partner's words")
for e in PLAYBOOK["entry"]:
    if e["causes"] != "all":
        for cid in sorted(set(e["causes"]) - cause_ids):
            errors.append(f"playbook.toml {e['type']}: cause '{cid}' is not in the cause list")
forbidden = set(PLAYBOOK.get("forbidden_types", []))
if not forbidden:
    errors.append("playbook.toml: forbidden_types missing (R-DET-07)")
for t in sorted(forbidden & set(PLAYBOOK["types"])):
    errors.append(f"playbook.toml: type '{t}' is forbidden (R-DET-07)")
for c in known_bad("dec3"):
    if "week_reported" in c:
        for r in c.get("bad", []):
            if isinstance(r, dict) and "due_week" in r and \
                    r["due_week"] == c["week_reported"] + ENTRY[c["type"]]["weeks_allowed"]:
                kb_fail("dec3", c, f"due week {r['due_week']} is what code sets; not bad")
    if c["requirement"] == "R-DET-07" and isinstance(c.get("bad"), list):
        for line in c["bad"]:
            if "both include" in line:
                for name in re.findall(r"'(\w+)'", line):
                    if name not in forbidden:
                        kb_fail("dec3", c, f"'{name}' is not in forbidden_types")
    for r in c.get("bad", []) if isinstance(c.get("bad"), list) else []:
        if isinstance(r, dict) and "type" in r and r["effort_hours"] == ENTRY[r["type"]]["effort_hours"]:
            kb_fail("dec3", c, f"{r['type']} {r['effort_hours']} now matches the playbook; not bad")

for c in known_bad("week"):
    issue = c.get("issue", {})
    if isinstance(c.get("right"), dict) and "days_open" in c["right"]:
        if day(c["review"]) - day(issue["detected"]) != c["right"]["days_open"] or \
           day(c["review"]) - day(issue["contained"]) != c["right"]["days_in_stage"]:
            kb_fail("week", c, "days open or days in stage do not match the dates")
    if "contained" in issue and isinstance(c.get("right"), int):
        if day(issue["contained"]) - day(issue["detected"]) != c["right"]:
            kb_fail("week", c, "time to contain does not match the dates")

for c in known_bad("evidence"):
    if c["requirement"] != "R-DET-15":
        continue
    bad = c.get("bad", [])
    for line in bad if isinstance(bad, list) else [bad]:
        if "built" in c["covers"]:
            continue  # the status-claims check comes in S1 (N26)
        if not (term_hits(line) or number_hits(line)):
            kb_fail("evidence", c, f"checks 9-10 do not catch: {line}")
    good = c.get("must_pass", [])
    for line in good if isinstance(good, list) else [good]:
        if term_hits(line) or number_hits(line):
            kb_fail("evidence", c, f"checks 9-10 wrongly reject: {line}")


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

for d in REG.get("decision", []):
    sb = d.get("superseded_by")
    if sb and (d["id"] not in superseded or f"Superseded by {sb}" not in superseded_part):
        errors.append(f"{d['id']}: registers say superseded by {sb}; decisions.md does not")
    if not sb and d["id"] in superseded:
        errors.append(f"{d['id']}: superseded in decisions.md but not marked in the registers")
# 13. No stale citations of superseded decisions
SUPERSEDED_IDS = {d["id"] for d in REG.get("decision", []) if d.get("superseded_by")}
cited = docs + sorted((ROOT / "evals" / "known_bad").glob("*.toml"))
for doc in cited:
    if not doc.exists():
        continue
    lines = scanned_lines(doc)
    if doc.name == "decisions.md":  # the preamble, before the first section, records history
        first = next(i for i, line in enumerate(lines) if line.startswith("## "))
        lines = [""] * first + lines[first:]
    for i, line in enumerate(lines, 1):
        for ref in re.findall(r"\b(N\d+)\b", line):
            if ref in SUPERSEDED_IDS:
                errors.append(f"{doc.relative_to(ROOT)}:{i}: cites superseded {ref}")

if errors:
    print(f"check.py: {len(errors)} problem(s)")
    print("\n".join(f"  - {e}" for e in errors))
    sys.exit(1)
n_sup = sum(1 for d in REG.get("decision", []) if d.get("superseded_by"))
print(f"check.py: clean — {len(ids['decision']) - n_sup} active decisions ({n_sup} superseded), {len(ids['risk'])} risks, "
      f"{len(ids['requirement'])} requirements, {len(ids['v1_defect'])} v1 defects, "
      f"{len(ids['safeguard'])} safeguards")

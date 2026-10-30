"""Traceability and document check: no model, no network.

Run from the repository root:  python evals/check.py
Update the README status block: python evals/check.py --update-readme

The chain ([One home per fact], [Requirements and evals]): v1 defect -> risk -> requirement
-> eval case -> code -> status claim. It checks the chain up to requirement, and the documents
and data files around it. Everything is cited by name ([Names, not codes]); each registers id
is the entry's name as a GitHub heading anchor. Later checks follow [Documents match what
exists]; the Harness phase adds the harness links.

  well-formed names  Ids in spec/registers.toml are anchors (or V1-nn for v1 defects), unique
                     within their kind; names are unique across decisions, requirements, risks
                     and safeguards.
  decisions match    Every decision in the registers is a heading in method/decisions.md,
                     and vice versa.
  requirements match Every requirement in the registers is a heading in
                     method/02-requirements.md, with the class label the registers give, in the
                     section its `question` names; the Red lines list holds exactly the red lines.
  links resolve      Every link in the registers points to an entry that exists.
  coverage           Every v1 defect is evidence for a risk; every risk is controlled by a
                     requirement; every requirement controls a risk; every safeguard is in force.
  citations          In the tracked docs, data files and known-bad files: every link to a
                     heading resolves, every [Name] is a decision, requirement or Monday question, every relative
                     link points to a file that exists, and no old code (N12, R-DET-05, DEC-2,
                     F2b...) appears. method/archive/ is history and is not scanned.
  archive chain      Every name in method/archive/code-map.md's decision and requirement tables
                     is a current heading.
  status block       The README status block matches the registers (generated, never hand-edited).
  terms              No tracked .md doc uses a phrase the registers say a preferred term
                     replaces. Exact phrases only, so "a separate agent" passes.
  numbers            No tracked .md doc states a tunable value from the data files with its
                     unit. Design facts with no tunable twin, such as "52 weeks", pass.
  mirrors            A data file that mirrors a design fact matches it. Today: the dispute
                     window in spec/metrics.toml matches [Simulated world].
  known-bad          Known-bad inputs (evals/known_bad/) still sit where the data files put
                     them; data-file lists hold together; each case names a registered
                     requirement; the document checks reject their known-bad lines and pass
                     their must-pass lines (the checks test themselves).
  assumption labels  Every data file in spec/ says in its first lines that its figures are
                     assumptions, citing [Assumptions].
  validation         Every tracked .md paragraph or table row that mentions validation cites
                     [No outside validation].
  privacy            No tracked file holds a name from the private deny-list
                     (_working/privacy-denylist.txt). Skipped, with a note, when it is absent.
  decision links     Every requirement names the decisions it carries out; every decision is
                     named by a requirement or marked process = true.
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
SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
PATTERN = {"decision": SLUG, "risk": SLUG, "requirement": SLUG, "safeguard": SLUG,
           "v1_defect": r"V1-\d{2}"}
OLD_CODE = re.compile(r"\b(N\d{1,2}|R-(?:DET|RL|JDG)-\d{2}|RK-\d{2}|SG-\d{1,2}|DEC-\d|D\d{1,2}"
                      r"|F1|F2a|F2b|F3|S[1-4])\b")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
NAME = re.compile(r"\[([A-Z][^\[\]\"]*?)\](?!\()")
CODE_SPAN = re.compile(r"`[^`]*`")
BLOCK = re.compile(r"(<!-- gen:status -->\n)(.*?)(<!-- /gen:status -->)", re.S)
CLASS_LABEL = {"pass/fail": "Pass/fail", "red line": "Red line", "judgement": "Judgement"}
errors = []


def err(check, msg):
    errors.append(f"[{check}] {msg}")


def slugify(heading):
    """GitHub's heading anchor: lower case, punctuation dropped, spaces to hyphens."""
    h = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return h.replace(" ", "-")


def headings(path, level=None):
    """Anchors of a markdown file's headings (optionally of one level), in order."""
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(#{1,6}) (.+?)\s*$", line)
        if m and (level is None or len(m.group(1)) == level):
            out.append((slugify(m.group(2)), m.group(2), len(m.group(1))))
    return out


DECISIONS_MD = ROOT / "method" / "decisions.md"
REQS_MD = ROOT / "method" / "02-requirements.md"

# well-formed names
ids, names = {}, {}
for kind, pat in PATTERN.items():
    seen = [e["id"] for e in REG.get(kind, [])]
    for i in seen:
        if not re.fullmatch(pat, i):
            err("well-formed names", f"{kind} {i}: not a well-formed id")
    for i in {x for x in seen if seen.count(x) > 1}:
        err("well-formed names", f"{kind} {i}: duplicate")
    ids[kind] = set(seen)
for kind in ("decision", "requirement", "risk", "safeguard"):
    for i in ids[kind]:
        if i in names:
            err("well-formed names", f"{i}: used by both a {names[i]} and a {kind}")
        names[i] = kind

# decisions match
dec_heads = {s: t for s, t, lvl in headings(DECISIONS_MD, 3)}
for d in sorted(ids["decision"] - set(dec_heads)):
    err("decisions match", f"{d}: in registers but not a heading in decisions.md")
for d in sorted(set(dec_heads) - ids["decision"]):
    err("decisions match", f"{d}: a heading in decisions.md but not in registers")

# requirements match
section, req_heads, red_list = None, {}, set()
lines = REQS_MD.read_text(encoding="utf-8").splitlines()
for i, line in enumerate(lines):
    if line.startswith("## "):
        section = slugify(line[3:])
    elif line.startswith("### "):
        label = next((x for x in lines[i + 1:i + 4] if x.strip()), "")
        m = re.match(r"^\*([A-Za-z/ ]+?)(?: \(hypothesis\))?\.\*", label)
        req_heads[slugify(line[4:])] = (section, m.group(1) if m else None)
    elif section == "red-lines":
        red_list |= {a.lstrip("#") for _, a in LINK.findall(line)}
for r in REG.get("requirement", []):
    if r["id"] not in req_heads:
        err("requirements match", f"{r['id']}: in registers but not a heading in 02-requirements.md")
        continue
    sec, label = req_heads[r["id"]]
    if label != CLASS_LABEL.get(r.get("class")):
        err("requirements match", f"{r['id']}: label '{label}' but the registers say '{r.get('class')}'")
    if sec != r.get("question"):
        err("requirements match", f"{r['id']}: under section '{sec}' but the registers say '{r.get('question')}'")
for h in sorted(set(req_heads) - ids["requirement"]):
    err("requirements match", f"{h}: a heading in 02-requirements.md but not in registers")
reds = {r["id"] for r in REG.get("requirement", []) if r.get("class") == "red line"}
for x in sorted(reds ^ red_list):
    err("requirements match", f"{x}: the Red lines list and the registers disagree")

# links resolve, coverage
evidenced, controlled, in_force = set(), set(), set()
for k in REG.get("risk", []):
    for v in k.get("evidence", []):
        if v not in ids["v1_defect"]:
            err("links resolve", f"{k['id']}.evidence: unknown {v}")
        evidenced.add(v)
for r in REG.get("requirement", []):
    if not r.get("risks"):
        err("coverage", f"{r['id']}: controls no risk")
    for k in r.get("risks", []):
        if k not in ids["risk"]:
            err("links resolve", f"{r['id']}.risks: unknown {k}")
        controlled.add(k)
for d in REG.get("decision", []):
    for sg in d.get("safeguards", []):
        if sg not in ids["safeguard"]:
            err("links resolve", f"{d['id']}.safeguards: unknown {sg}")
        in_force.add(sg)
for v in sorted(ids["v1_defect"] - evidenced):
    err("coverage", f"{v}: not evidence for any risk")
for k in sorted(ids["risk"] - controlled):
    err("coverage", f"{k}: no requirement controls it")
for sg in sorted(ids["safeguard"] - in_force):
    err("coverage", f"{sg}: no decision brings it into force")

# citations
docs = [ROOT / "CLAUDE.md", ROOT / "README.md"]
for folder in ("method", "spec", "data", "evals", "prototype"):
    docs += sorted((ROOT / folder).glob("*.md"))
docs = [d for d in docs if d.exists()]
data_files = sorted((ROOT / "spec").glob("*.toml"))
kb_files = sorted((ROOT / "evals" / "known_bad").glob("*.toml"))
CITABLE = {}  # name as written -> kind
for path, kind in ((DECISIONS_MD, "decision"), (REQS_MD, "requirement")):
    for s, title, lvl in headings(path, 3):
        CITABLE[title] = kind
for s, title, lvl in headings(REQS_MD, 2):
    if title.endswith("?"):
        CITABLE[title] = "question"   # the four Monday questions
ANCHORS = {}


def anchors(path):
    if path not in ANCHORS:
        ANCHORS[path] = {s for s, _, _ in headings(path)} if path.exists() else set()
    return ANCHORS[path]


def citation_problems(line, src, toml=False):
    """Problems in one line: old codes, unknown [Name]s, links to missing files or headings."""
    out = []
    text = CODE_SPAN.sub("", line)
    for m in OLD_CODE.finditer(text):
        out.append(f"old code {m.group(1)}: cite by name")
    if toml and re.match(r"^\s*\[", text):
        return out
    for n in NAME.findall(text):
        if n not in CITABLE:
            out.append(f"[{n}] is not a decision, requirement or Monday question")
    for _, href in LINK.findall(text):
        if re.match(r"^[a-z]+:", href):
            continue
        path, _, anchor = href.partition("#")
        target = (src.parent / path).resolve() if path else src
        if path and not target.exists():
            out.append(f"link to a missing file: {href}")
        elif anchor and target.suffix == ".md" and anchor not in anchors(target):
            out.append(f"link to a missing heading: {href}")
    return out


KB_CITATION_BAD = set()
for f in kb_files:
    for c in tomllib.loads(f.read_text(encoding="utf-8")).get("case", []):
        if c.get("check") == "citations":
            KB_CITATION_BAD |= set(c.get("bad", [])) | set(c.get("must_pass", []))
for f in docs + data_files + kb_files:
    toml = f.suffix == ".toml"
    for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if toml and any(b in line for b in KB_CITATION_BAD):
            continue
        for p in citation_problems(line, f, toml):
            err("citations", f"{f.relative_to(ROOT)}:{i}: {p}")

# archive chain
cmap = (ROOT / "method" / "archive" / "code-map.md").read_text(encoding="utf-8")
for part in ("## Decisions", "## Requirements"):
    block = cmap.split(part, 1)[1].split("\n## ", 1)[0]
    for code, nm in re.findall(r"^\| ([A-Z][\w-]*) \| (.+?)(?: \(superseded.*?\))? \|$", block, re.M):
        if code != "Code" and nm not in CITABLE:
            err("archive chain", f"code-map.md: {code} maps to '{nm}', which is not a current heading")


# Data files used by the terms, numbers, mirrors and known-bad checks
def load(rel):
    return tomllib.loads((ROOT / rel).read_text(encoding="utf-8"))


METRICS = load("spec/metrics.toml")
CAPACITY = load("spec/capacity.toml")
THRESHOLDS = load("spec/thresholds.toml")
PLAYBOOK = load("spec/playbook.toml")
METRIC = {m["id"]: m for m in METRICS["metric"]}
ENTRY = {e["type"]: e for e in PLAYBOOK["entry"]}
md_docs = [d for d in docs if d.suffix == ".md"]

# 9. Terms
REPLACED = [(t["use"], old) for t in REG.get("term", []) for old in t.get("replaces", [])]


def term_hits(text):
    return [(use, old) for use, old in REPLACED
            if re.search(r"\b" + re.escape(old) + r"\b", text, re.I)]


def scanned_lines(doc):
    return doc.read_text(encoding="utf-8").splitlines()


for doc in md_docs:
    for i, line in enumerate(scanned_lines(doc), 1):
        for use, old in term_hits(line):
            err("terms", f"{doc.relative_to(ROOT)}:{i}: '{old}' — use '{use}'")


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
            err("numbers", f"{doc.relative_to(ROOT)}:{i}: states a tunable number ({src}); "
                           f"cite the data file instead")

# 11. Mirrors
log = DECISIONS_MD.read_text(encoding="utf-8")
world = re.search(r"^### Simulated world\n(.*?)(?=^##)", log, re.S | re.M)
window = re.search(r"dispute\s+within\s+(\d+)\s+days", world.group(1)) if world else None
if not window:
    err("mirrors", "decisions.md: the dispute window in 'Simulated world' not found")
elif int(window.group(1)) != METRICS["windows"]["dispute_window_days"]:
    err("mirrors", f"metrics.toml dispute_window_days ({METRICS['windows']['dispute_window_days']}) "
                   f"differs from 'Simulated world' ({window.group(1)} days)")

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
    err("known-bad", f"known_bad/{name}.toml {case['requirement']} ({case['covers'][:40]}): {msg}")


places = Decimal(1).scaleb(-METRICS["display"]["decimals"])
for c in known_bad("off_target"):
    rows = c.get("rows") or c.get("weeks") or [c]
    rows += [dict(v, metric=c.get("metric"), right=v["colour"]) for k, v in c.items()
             if k in ("provisional", "final") and isinstance(v, dict)]
    for r in rows:
        metric, shown, right = r.get("metric", c.get("metric")), r.get("shown"), r.get("right")
        if "raw" in r and Decimal(str(r["raw"])).quantize(places, ROUND_HALF_UP) != Decimal(str(shown)):
            kb_fail("off_target", c, f"raw {r['raw']} does not show as {shown}")
        if metric in METRIC and shown is not None and right in COLOURS:
            if colour(metric, shown) != right:
                kb_fail("off_target", c, f"{metric} {shown} is {colour(metric, shown)}, case says {right}")
        if "days" in r and "entered_step" in r:
            limit = METRIC["stuck_invoices"]["stuck_limit_calendar_days"]
            if day(c["review"]) - day(r["entered_step"]) != r["days"]:
                kb_fail("off_target", c, f"{r['entered_step']}: day count is not {r['days']}")
            if (r["days"] > limit) != (r["right"] == "listed"):
                kb_fail("off_target", c, f"{r['days']} days against a limit of {limit}: not {r['right']}")
    if c.get("right") == "none" and METRIC[c["metric"]]["shown"] != "monitored":
        kb_fail("off_target", c, f"{c['metric']} is not monitored")
    if "earlier_weeks" in c and c["earlier_weeks"] != THRESHOLDS["trends"]["trend_window_weeks"] - 1:
        kb_fail("off_target", c, "earlier_weeks is not one fewer than the trend window")

cap = CAPACITY
productive = cap["team_fte"] * (cap["hours_per_fte"] - cap["protected_hours_per_fte"])
ceiling_h = cap["utilisation"]["ceiling"] * productive
overtime_max = cap["team_fte"] * cap["overtime_hours_per_fte"]
for c in known_bad("capacity"):
    for r in c.get("rows", []):
        if "workload" in r:
            over = max(0.0, r["workload"] - ceiling_h)
            got = {"overtime": min(over, overtime_max), "exec_hours": over - min(over, overtime_max),
                   "room": max(0.0, ceiling_h - r["workload"])}
            for k, v in r["right"].items():
                if abs(got[k] - v) > 1e-9:
                    kb_fail("capacity", c, f"{r['week']}: {k} is {got[k]:g}, case says {v}")
        if "committed" in r and r["committed"] <= productive + r["approved_overtime"]:
            kb_fail("capacity", c, f"committed {r['committed']} fits; the bad plan is not bad")
    if "intervention" in c:
        top = max(ENTRY[c["intervention"]["type"]]["effort_hours"])
        if c["intervention"]["effort_hours"] != ENTRY[c["intervention"]["type"]]["effort_hours"] or c["right"] != top:
            kb_fail("capacity", c, "effort range or its top no longer matches the playbook")
    plan = c.get("plan", {})
    if "contracted" in plan and plan["contracted"] + plan["overtime"] <= cap["max_hours_per_person"]:
        kb_fail("capacity", c, "the person is within the limit; the bad plan is not bad")
    if "proposed_overtime" in plan and plan["committed"] <= productive + plan["approved_overtime"]:
        kb_fail("capacity", c, "the plan fits without the unapproved overtime; not bad")

high_min = THRESHOLDS["confidence"]["high_min_evidence_types"]
for c in known_bad("possible_issues"):
    for r in c.get("rows", []):
        if r.get("computed") == "high" and (len(r["evidence_types"]) < high_min or r["gaps"]):
            kb_fail("possible_issues", c, "a row computed high has too few types or a gap")
        if r.get("bad") == "high" and not r["gaps"] and len(r["evidence_types"]) >= high_min:
            kb_fail("possible_issues", c, "a row labelled bad for too few types now meets the minimum")

CAUSES = load("spec/causes.toml")
cause_ids = {c["id"] for c in CAUSES["cause"]}
for cid in sorted(cause_ids):
    if "_" not in cid:
        err("known-bad", f"causes.toml: id '{cid}' has no underscore; the leakage scan "
                         f"([No answer in the world]) cannot tell it from a partner's words")
for e in PLAYBOOK["entry"]:
    if e["causes"] != "all":
        for cid in sorted(set(e["causes"]) - cause_ids):
            err("known-bad", f"playbook.toml {e['type']}: cause '{cid}' is not in the cause list")
forbidden = set(PLAYBOOK.get("forbidden_types", []))
if not forbidden:
    err("known-bad", "playbook.toml: forbidden_types missing ([The playbook respects the SOP])")
for t in sorted(forbidden & set(PLAYBOOK["types"])):
    err("known-bad", f"playbook.toml: type '{t}' is forbidden ([The playbook respects the SOP])")
for c in known_bad("interventions"):
    if "week_reported" in c:
        for r in c.get("bad", []):
            if isinstance(r, dict) and "due_week" in r and \
                    r["due_week"] == c["week_reported"] + ENTRY[c["type"]]["weeks_allowed"]:
                kb_fail("interventions", c, f"due week {r['due_week']} is what code sets; not bad")
    if c["requirement"] == "the-playbook-respects-the-sop" and isinstance(c.get("bad"), list):
        for line in c["bad"]:
            if "both include" in line:
                for name in re.findall(r"'(\w+)'", line):
                    if name not in forbidden:
                        kb_fail("interventions", c, f"'{name}' is not in forbidden_types")
    for r in c.get("bad", []) if isinstance(c.get("bad"), list) else []:
        if isinstance(r, dict) and "type" in r and r["effort_hours"] == ENTRY[r["type"]]["effort_hours"]:
            kb_fail("interventions", c, f"{r['type']} {r['effort_hours']} now matches the playbook; not bad")

for c in known_bad("week"):
    issue = c.get("issue", {})
    if isinstance(c.get("right"), dict) and "days_open" in c["right"]:
        if day(c["review"]) - day(issue["detected"]) != c["right"]["days_open"] or \
           day(c["review"]) - day(issue["contained"]) != c["right"]["days_in_stage"]:
            kb_fail("week", c, "days open or days in stage do not match the dates")
    if "contained" in issue and isinstance(c.get("right"), int):
        if day(issue["contained"]) - day(issue["detected"]) != c["right"]:
            kb_fail("week", c, "time to contain does not match the dates")

for f in kb_files:
    for c in tomllib.loads(f.read_text(encoding="utf-8")).get("case", []):
        if c.get("requirement") not in ids["requirement"]:
            err("known-bad", f"known_bad/{f.name}: case '{c.get('covers', '')[:40]}' names unknown "
                             f"requirement {c.get('requirement')}")


# Assumption labels, validation mentions, privacy ([Documents match what exists],
# [Nothing private in tracked files])
def assumptions_ok(text):
    top = "\n".join(text.splitlines()[:6])
    return "assumption" in top.lower() and "[Assumptions]" in top


def validation_bad(unit):
    return bool(re.search(r"validat", unit, re.I)) and "No outside validation" not in unit


def privacy_hits(text, terms):
    return [t for t in terms if re.search(r"\b" + re.escape(t) + r"\b", text, re.I)]


def validation_lines(doc):
    """A doc's lines; in decisions.md the entry that sets the limit is not checked against itself."""
    lines, inside = scanned_lines(doc), False
    if doc == DECISIONS_MD:
        for i, line in enumerate(lines):
            if line.startswith("#"):
                inside = line == "### No outside validation"
            elif inside:
                lines[i] = ""
    return lines


def units(lines):
    """Paragraphs, with each table row as its own unit; headings are skipped."""
    out, cur = [], []
    for i, line in enumerate(lines, 1):
        if line.startswith("#"):
            pass
        elif line.startswith("|"):
            out.append((i, line))
        elif line.strip():
            cur.append((i, line))
            continue
        if cur:
            out.append((cur[0][0], " ".join(x for _, x in cur)))
            cur = []
    if cur:
        out.append((cur[0][0], " ".join(x for _, x in cur)))
    return out


for f in sorted((ROOT / "spec").glob("*.toml")):
    if f.name != "registers.toml" and not assumptions_ok(f.read_text(encoding="utf-8")):
        err("assumption labels", f"spec/{f.name}: header does not say its figures are assumptions, "
                                 f"citing [Assumptions]")
for doc in md_docs:
    for i, unit in units(validation_lines(doc)):
        if validation_bad(unit):
            err("validation", f"{doc.relative_to(ROOT)}:{i}: mentions validation without citing "
                              f"'No outside validation'")

notes = []
DENY = ROOT / "_working" / "privacy-denylist.txt"
if DENY.exists():
    terms = [t.strip() for t in DENY.read_text(encoding="utf-8").splitlines()
             if t.strip() and not t.startswith("#")]
    for f in sorted(ROOT.rglob("*")):
        rel = f.relative_to(ROOT)
        if not f.is_file() or rel.parts[0] in (".git", "_working") or "__pycache__" in rel.parts:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for t in privacy_hits(text, terms):
            err("privacy", f"{rel}: holds a name from the private deny-list")
    notes.append(f"privacy check ran against {len(terms)} private term(s)")
else:
    notes.append("privacy check skipped: no private deny-list")

KB_CHECK = {
    None: (lambda line: bool(term_hits(line) or number_hits(line)), "the terms and numbers checks"),
    "assumptions": (lambda line: not assumptions_ok(line), "the assumption-labels check"),
    "validation": (validation_bad, "the validation check"),
    "citations": (lambda line: bool(citation_problems(line, REQS_MD)), "the citations check"),
}
for c in known_bad("evidence"):
    if c["requirement"] == "nothing-private-in-tracked-files":
        flags, name = (lambda line, c=c: bool(privacy_hits(line, c["test_list"]))), "the privacy check"
    elif c["requirement"] == "documents-match-what-exists" and "built" not in c["covers"]:  # status claims: Build 1
        flags, name = KB_CHECK[c.get("check")]
    else:
        continue
    bad = c.get("bad", [])
    for line in bad if isinstance(bad, list) else [bad]:
        if not flags(line):
            kb_fail("evidence", c, f"{name} does not catch: {line}")
    good = c.get("must_pass", [])
    for line in good if isinstance(good, list) else [good]:
        if flags(line):
            kb_fail("evidence", c, f"{name} wrongly rejects: {line}")

# Decision links
ACTIVE = ids["decision"]
linked = set()
for r in REG.get("requirement", []):
    if not r.get("decisions"):
        err("decision links", f"{r['id']}: names no decision it carries out")
    for d in r.get("decisions", []):
        if d not in ACTIVE:
            err("decision links", f"{r['id']}.decisions: {d} is not a decision")
        linked.add(d)
for d in REG.get("decision", []):
    if d["id"] in ACTIVE and d["id"] not in linked and not d.get("process"):
        err("decision links", f"{d['id']}: no requirement carries it out and it is not marked process")


# Status block
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
    err("status block", "README.md: markers missing")
elif m.group(2) != status_block():
    err("status block", "README.md: stale — run with --update-readme")

if errors:
    print(f"check.py: {len(errors)} problem(s)")
    print("\n".join(f"  - {e}" for e in errors))
    sys.exit(1)
print(f"check.py: clean — {len(ids['decision'])} decisions, {len(ids['risk'])} risks, "
      f"{len(ids['requirement'])} requirements, {len(ids['v1_defect'])} v1 defects, "
      f"{len(ids['safeguard'])} safeguards")
for n in notes:
    print(f"  note: {n}")

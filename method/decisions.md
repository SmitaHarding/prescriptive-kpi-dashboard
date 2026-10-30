# Decisions

The choices made for Aegis, grouped by type, one choice per entry. Requirements the system
must meet are in [`02-requirements.md`](02-requirements.md). Where numbers live is set in
[One home per fact](#one-home-per-fact).

An entry keeps its name. A change edits it in place; the replaced wording moves, dated, to
[`archive/superseded.md`](archive/superseded.md). Entries are cited by name
([Names, not codes](#names-not-codes)). The earlier numbered codes, and the decision log
these entries replaced, are mapped to names in [`archive/code-map.md`](archive/code-map.md).

## 1. Purpose and scope

### Scope

Aegis is rebuilt from scratch. Nothing from v1 survives unless it passes the harness. The
method is the main deliverable; the prototype is the evidence that it works.

### What the prototype builds

- To be built: metrics with colour and trends; the capacity check; finding possible issues,
  against its rules version; Detect and Contain; the PMO lead's review; the weekly record,
  including partner contacts and every reject and edit; the lifecycle board; the weekly
  update; the stuck-invoice list; the ops and exec views; the value measures, labelled
  simulated ([Value measures](#value-measures)); the drift table; the read-only public
  replay ([Records and replay](#records-and-replay)).
- Simulated: lifecycle stages after Contained ([Issue lifecycle](#issue-lifecycle)).
- Designed, not built: the real later-stage workflow; playbook updates; a drift view on the
  dashboard; tracking whether interventions worked; search over past issues; turning
  overrides into test cases ([Overrides feed the tests](#overrides-feed-the-tests));
  independent validation ([No outside validation](#no-outside-validation)); release staging
  (shadow, then advisory).

### No outside validation

No outside person validates the prototype. The author judges fitness for purpose. Every
mention of validation states this limit. Independent validation is designed, not done.

## 2. How the product works

### The Monday decision

Every Monday the PMO lead decides which issues need action this week, and what action. The
decision has four parts, each a question:
- **Off target?** Code.
- **Possible issues?** Which new dispute tickets form a possible issue? Rules, or the model
  if it beats the rules ([Model against rules](#model-against-rules)).
- **Which interventions?** For each new possible issue and each overdue issue not yet
  Contained ([Overdue issues](02-requirements.md#overdue-issues)). The model drafts, code
  checks, the PMO lead reviews. Issues opened by hand are the exception
  ([Issues opened by hand](02-requirements.md#issues-opened-by-hand)). Off-playbook drafts
  are allowed, labelled and reviewed.
- **Enough capacity?** Code.

Each question's requirements are in its section of
[`02-requirements.md`](02-requirements.md).

Weekly order: Off target?; Enough capacity? on committed hours; Possible issues?; Which
interventions? within the hours left; Enough capacity? on the drafts; then the PMO lead's
review.

Finding possible issues suggests a suspected cause; people confirm causes. Nothing names a
root cause. The PMO lead owns the decision; the team manager, Ops specialists and executives
act on parts of it. Each week has one weekly record, shown as an ops view and an exec view.
In the prototype the author plays every role, and each action is labelled with its role.

### Issue lifecycle

An issue moves through six stages: Detected, Contained, Cause confirmed, Corrected,
Prevented, Closed. Up to Contained, people move it and code checks each stage's exit
criteria. The model drafts only before Contained. After Contained, the generator scripts
each stage, labelled "simulated outcome". Each metric's week is set in the metrics register.
The weekly update shows the week, performance and each open issue's progress until it
closes.

### Value measures

Value is measured after a person acts.
- Adoption: interventions actioned by their due week.
- Outcome: time to contain (the main measure); share of issues caught before partners
  dispute; share of affected partners contacted before they dispute.

An issue the PMO lead opens by hand before any dispute counts as caught early. In the
prototype the measures come from the simulated record, labelled "simulated".

## 3. Data and testing

### Simulated world

The data is simulated, newly designed and labelled synthetic.
- 1,500 partners, paid weekly by self-billing; one invoice per partner per week; 52 weeks;
  English text.
- It follows the payment and dispute SOPs. The run is every Tuesday, on the most accurate
  data available. Partners are paid within 14 days of service. They may dispute within 14
  days of the invoice appearing.
- The coloured metrics are in the metrics register. Invoice volume is context only.
- Payment accuracy counts confirmed errors only: those corrected by a back-payment or a
  payment correction, whoever found them.
- Ticket text reads as if the writer doesn't know the cause. It may include the writer's
  guess; a share of guesses are wrong (set in the Judgement and data phase).

### The year

The simulated year has three parts:
- Weeks 1–26, history. Code generates them; the model does not run.
- Weeks 27–39, scenario quarter, used during the build. Each scenario spans several weeks.
  At least one fits no listed cause.
- Weeks 40–52, held-out quarter, run once after Build 4
  ([Model against rules](#model-against-rules)). New instances of the same case types, plus
  a few new types whose expected answer is the fixed text in
  [Cause from the list, or human review](02-requirements.md#cause-from-the-list-or-human-review).

A ticket belongs to the quarter of the week it is opened. Scenario-quarter scenarios reach
Contained by week 39. Held-out scenarios start in week 40 or later, depend on no earlier
issue and reach Contained by week 52. A week not final at its quarter's last review, as the
metrics register sets, stays provisional in that quarter's results
([Provisional weeks](02-requirements.md#provisional-weeks)); the Judgement and data phase
lists these weeks. Week 52 is an ordinary quarter-end. The Judgement and data phase sets the
number of scenarios.

### Scenarios and the holdout

- Each scenario's expected answer is written into its definition. The model is scored
  against it. The world data holds no answers.
- Claude writes the scenario quarter. A separate agent writes the held-out quarter.
- A reviewer agent on a different LLM from the model reads each scenario's data without the
  answer. A mismatch means the scenario is ambiguous, and it is rewritten before the freeze.
  In the scenario quarter, Claude rewrites it and the author reads the mismatch. In the
  held-out quarter, its separate agent rewrites it and the author sees only counts. After
  the freeze, a flawed scenario is excluded and reported, never rewritten (Never fit the
  answer).
- The held-out quarter sits in a folder outside the project. Build sessions and the builder
  never open it. Its fingerprint is committed in the Harness phase and checked before its
  one run.
- The safeguards Freeze first, Holdout sealed, Blind scoring and Never fit the answer apply.

### Model against rules

Finding possible issues has a rules version: the rules the team would use without the model.
The PMO lead writes it.
- The scoring setup is frozen at the end of the Harness phase: the rules version, case mix,
  margin, rubric and expected answers (Freeze first). After the freeze, only the author can
  change a frozen item, and only by a new decision.
- Both versions are scored on the right possible issue, the right suspected cause and lead
  time: how soon after a planted pattern starts each version flags it.
- The deciding run is the scenario quarter, once Build 2 has built the model version. The
  model is used only if it beats the rules by the frozen margin and is never worse on a red
  line.
- The held-out run after Build 4 checks the result. If it does not confirm it, this is
  reported and the rules version is used.
- The safeguard Cost beside accuracy applies: model cost is shown beside every result.

## 4. Quality and change

### Requirements and evals

Every requirement is a statement a test can fail. Each controls at least one listed risk and
is proven by at least one eval. Three classes:
- Pass/fail: must pass 100%; a failure blocks.
- Red line: zero tolerance; code checks every output the red line covers, before it is
  shown.
- Judgement: scored against a rubric or expected answers; never 100%.

Pass/fail and red-line cases are written first and fail before the product code exists.
Judgement requirements come from the spike ([Build-and-look spike](#build-and-look-spike)).
The dataset is designed from what the checks need.

### Change control

Scoring starts at the end of the Harness phase. From then on, a new model version, prompt or
data file needs the whole scenario quarter to pass again
([Change gate](02-requirements.md#change-gate)). Changes after the holdout run are disclosed
as such. Hallucination is limited and detected, never claimed to be zero.

### Overrides feed the tests

Every PMO lead reject or edit will be captured with its note (to be built,
[What the prototype builds](#what-the-prototype-builds)). Turning overrides into test cases
is designed, not built. The author would choose which join, as a separate set reported apart
from the frozen test set. A new case never changes an existing expected answer (Never fit
the answer).

### Build-and-look spike

Between the Pass/fail requirements and Judgement and data phases, a short spike shows how
the model fails before judgement requirements are written.
- Generate 4–6 throwaway weeks of tickets.
- Run one prompt that finds possible issues and one that drafts interventions a few times
  each, plus quick keyword rules that find possible issues.
- The author reads about 50 outputs as the PMO lead and notes what is wrong.
- Group the notes into failure categories and count them. Each category is fixed in the
  prompt or code, becomes a code check, or becomes a judgement requirement.

It stops after two prompt rounds, or when no new categories appear. It stays private in
`_working/spike/`, uncommitted and unscored. Its keyword rules are throwaway, not the rules
version in [Model against rules](#model-against-rules).

## 5. Build and delivery

### Phases and the builder

- Phases: Frame (frame and decisions); Pass/fail requirements; the spike
  ([Build-and-look spike](#build-and-look-spike)); Judgement and data (judgement
  requirements and dataset); Harness; Build 1–4 (the slices); Wrap-up.
- Slices: Build 1 metrics and capacity; Build 2 clustering; Build 3 contain; Build 4
  lifecycle board and weekly update.
- The author and Claude work Frame to Harness, and Wrap-up. The builder, an agent, builds
  the slices.
- Claude and the builder prepare commits; only the author pushes.
- Each phase ends with a gate: a fresh agent reviews all tracked files. HIGH findings block;
  the rest are fixed in one batch.

Each slice runs under a charter the author approves first. It sets the goal (a target
scorecard), the paths the builder may edit, iteration and spend caps, the done condition and
the author's approval points. The builder edits only those paths. It never changes a test,
expected answer or requirement to make something pass. It escalates at a cap, when a failure
repeats, or when a fix needs a test, answer or requirement changed. It prepares commits and
never pushes; the author pushes.

### Repo and deployment

v1 stays on the `archive/v1` branch and tag `v1.0`. v2 is built on `main` in the same
repository. History is never rewritten or force-pushed. `app.py` at the root is the
Streamlit entry point. The app is never deleted: it shows a holding page now and v2 later,
at the same URL.

### Records and replay

Records are append-only plain-text weekly files, created locally and kept in git. The public
app replays them read-only and makes no model calls. It shows any week: all 52 weeks of
metrics, the model's path in the scenario quarter, and the held-out quarter once run. The
README will explain how to reproduce the run (from Wrap-up).

## 6. Documents and publishing

### Public face

The README tells the v1-to-v2 story. Until Wrap-up, it stays short, with a status block
generated from the registers. The holding page says v2 is in development. The v1 review is
published in Wrap-up as the v1 post-mortem annex and linked from both.

### Privacy

The domain is described only as a large-scale B2B payments operation. No employer, internal
tool or person is named, other than the author's name and GitHub link. Personal working
documents stay local.

### Method documents

The method is written in markdown. Frame, Judgement and data, Harness and Wrap-up add method
documents; `method/README.md` lists them. Pass/fail requirements and Judgement and data
complete `02-requirements.md`. Each slice adds a charter and scorecard. Documents cite by
name; Wrap-up writes the full narrative. Word or PDF versions are exports made at the end.

### One home per fact

- Choices live here. Requirements live in `02-requirements.md`.
- Tunable numbers and lists live in data files: the metrics register, the capacity file, the
  thresholds file, the cause list, the playbook and the generator settings.
- Facts that define the design may be stated in decisions: the size of the simulated world,
  the quarters, the SOP terms, the spike's size.
- The registers hold names, links, built status, preferred terms, the safeguard wording, and
  lists such as case types and evidence types.
- A data file may mirror a design fact for the code; `check.py` confirms the two match.
- Other documents cite by name and restate no numbers or fixed text.
- [Documents match what exists](02-requirements.md#documents-match-what-exists) sets the
  document checks.

### Names, not codes

Decisions, requirements, risks and safeguards are cited by name, never by a code. In
markdown, a decision or requirement is cited as a link to its heading, at most once per
paragraph; in data files and code, by its name in square brackets. Risks and safeguards,
which live in the registers, are cited by plain name. A requirement's class is a label on
it, not part of its name. Names are unique across kinds. Cite only where the reader must
look elsewhere.
[Documents match what exists](02-requirements.md#documents-match-what-exists) checks this.

### Assumptions

Every figure is measured or labelled an assumption. Capacity figures and metric targets and
bands are assumptions from the author's operating experience.

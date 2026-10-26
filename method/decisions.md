# Decisions

The choices made for Aegis, grouped by type, one choice per entry. Rules the
system must meet are in [`02-requirements.md`](02-requirements.md). Where numbers
live is set in N26.

A change is a new entry. The old entry moves to Superseded with a pointer to its
replacement and is not otherwise edited.

N1–N22 were agreed on 22 Oct 2026; N23–N24 replaced N9–N10 on 23 Oct (F2a);
N25–N32 replaced N5, N6, N8, N13, N14, N17, N21 and N24 on 26 Oct. They replace
the 86 active earlier decisions (D1–D93; 7 others were already superseded), kept
word for word in [`archive/decisions-2026-10-21.md`](archive/decisions-2026-10-21.md). The mapping
table at the end shows where each one went.

## 1. Purpose and scope

**N1 · Scope.** Aegis is rebuilt from scratch. Nothing from v1 survives unless it
passes the harness. The method is the main deliverable; the prototype is the
evidence that it works.

**N32 · What the prototype builds.**
- To be built: metrics with colour and trends; the capacity check; DEC-2 against
  its rules version; Detect and Contain; the PMO lead's review; the weekly record,
  including partner contacts and every reject and edit; the lifecycle board; the
  weekly update; the stuck-invoice list; the ops and exec views; the value
  measures, labelled simulated (N16); the drift table; the read-only public replay
  (N11).
- Simulated: lifecycle stages after Contained (N23).
- Designed, not built: the real later-stage workflow; playbook updates; a drift
  view on the dashboard; tracking whether interventions worked; search over past
  issues; turning overrides into test cases (N31); independent validation (N20);
  release staging (shadow, then advisory).

**N20 · No outside validation.** No outside person validates the prototype. The
author judges fitness for purpose. Every mention of validation states this limit.
Independent validation is designed, not done.

## 2. How the product works

**N27 · The Monday decision.** Every Monday the PMO lead decides which issues need
action this week, and what action. The decision has four parts:
- DEC-1 · Is anything off target? Code.
- DEC-2 · Which new dispute tickets form a possible issue? Rules, or the model if
  it beats the rules (N15).
- DEC-3 · Which interventions now, for each new possible issue and each overdue
  issue not yet Contained (R-DET-10)? The model drafts, code checks, the PMO lead
  reviews. Issues opened by hand are the exception (R-DET-11). Off-playbook drafts
  are allowed, labelled and reviewed.
- DEC-4 · Do we have the capacity? Code.

Weekly order: DEC-1, DEC-4 on committed hours, DEC-2, DEC-3 within the hours left,
DEC-4 on the drafts, then the PMO lead's review.

DEC-2 suggests a suspected cause; people confirm causes. Nothing names a root
cause. The PMO lead owns the decision; the team manager, Ops specialists and
executives act on parts of it. Each week has one weekly record, shown as an ops
view and an exec view. In the prototype the author plays every role, and each
action is labelled with its role.

**N23 · Issue lifecycle.** An issue moves through six stages: Detected, Contained,
Cause confirmed, Corrected, Prevented, Closed. Up to Contained, people move it and
code checks each stage's exit criteria. The model drafts only before Contained.
After Contained, the generator scripts each stage, labelled "simulated outcome".
Each metric's week is set in the metrics register. The weekly update shows the week,
performance and each open issue's progress until it closes.

**N16 · Value measures.** Value is measured after a person acts.
- Adoption: interventions actioned by their due week.
- Outcome: time to contain (the main measure); share of issues caught before
  partners dispute; share of affected partners contacted before they dispute.

An issue the PMO lead opens by hand before any dispute counts as caught early. In
the prototype the measures come from the simulated record, labelled "simulated".

## 3. Data and testing

**N12 · Simulated world.** The data is simulated, newly designed and labelled
synthetic.
- 1,500 partners, paid weekly by self-billing; one invoice per partner per week;
  52 weeks; English text.
- It follows the payment and dispute SOPs. The run is every Tuesday, on the most
  accurate data available. Partners are paid within 14 days of service. They may
  dispute within 14 days of the invoice appearing.
- The coloured metrics are in the metrics register. Invoice volume is context only.
- Payment accuracy counts confirmed errors only: those corrected by a back-payment
  or a payment correction, whoever found them.
- Ticket text reads as if the writer doesn't know the cause. It may include the
  writer's guess; a share of guesses are wrong (set in F2b).

**N28 · The year.** The simulated year has three parts:
- Weeks 1–26, history. Code generates them; the model does not run.
- Weeks 27–39, scenario quarter, used during the build. Each scenario spans
  several weeks. At least one fits no listed cause.
- Weeks 40–52, held-out quarter, run once after S4 (N15). New instances of the
  same case types, plus a few new types whose expected answer is R-RL-02's fixed
  text.

A ticket belongs to the quarter of the week it is opened. Scenario-quarter
scenarios reach Contained by week 39. Held-out scenarios start in week 40 or
later, depend on no earlier issue and reach Contained by week 52. A week not final
at its quarter's last review, as the metrics register sets, stays provisional in
that quarter's results (R-DET-03); F2b lists these weeks. Week 52 is an ordinary
quarter-end. F2b sets the number of scenarios.

**N29 · Scenarios and the holdout.**
- Each scenario's expected answer is written into its definition. The model is
  scored against it. The world data holds no answers.
- Claude writes the scenario quarter. A separate agent writes the held-out
  quarter.
- A reviewer agent on a different LLM from the model reads each scenario's data
  without the answer. A mismatch means the scenario is ambiguous, and it is
  rewritten before the freeze. In the scenario quarter, Claude rewrites it and the
  author reads the mismatch. In the held-out quarter, its separate agent rewrites
  it and the author sees only counts. After the freeze, a flawed scenario is
  excluded and reported, never rewritten (SG-4).
- The held-out quarter sits in a folder outside the project. Build sessions and
  the builder never open it. Its fingerprint is committed in F3 and checked before
  its one run.
- Safeguards SG-1 to SG-4 apply: freeze first, holdout sealed, blind scoring,
  never fit the answer.

**N15 · Model against rules.** DEC-2 has a rules version: the rules the team would
use without the model. The PMO lead writes it.
- The scoring setup is frozen at the end of F3: the rules version, case mix,
  margin, rubric and expected answers (SG-1). After the freeze, only the author
  can change a frozen item, and only by a new decision.
- Both versions are scored on the right possible issue, the right suspected cause
  and lead time: how soon after a planted pattern starts each version flags it.
- The deciding run is the scenario quarter, once S2 has built the model version.
  The model is used only if it beats the rules by the frozen margin and is never
  worse on a red line.
- The held-out run after S4 checks the result. If it does not confirm it, this is
  reported and the rules version is used.
- SG-5 shows model cost beside every result.

## 4. Quality and change

**N30 · Requirements and evals.** Every requirement is a statement a test can
fail. Each controls at least one listed risk and is proven by at least one eval.
Three classes:
- Deterministic: must pass 100%; a failure blocks.
- Red line: zero tolerance; code checks every output the red line covers,
  before it is shown.
- Judgement: scored against a rubric or expected answers; never 100%.

Deterministic and red-line cases are written first and fail before the product
code exists. Judgement requirements come from the spike (N22). The dataset is
designed from what the checks need.

**N18 · Change control.** Scoring starts at the end of F3. From then on, a new
model version, prompt or data file needs the whole scenario quarter to pass again
(R-DET-14). Changes after the holdout run are disclosed as such. Hallucination is
limited and detected, never claimed to be zero.

**N31 · Overrides feed the tests.** Every PMO lead reject or edit will be captured
with its note (to be built, N32). Turning overrides into test cases is designed,
not built. The author would choose which join, as a separate set reported apart
from the frozen test set. A new case never changes an existing expected answer
(SG-4).

**N22 · Build-and-look spike.** Between F2a and F2b, a short spike shows how the
model fails before judgement requirements are written.
- Generate 4–6 throwaway weeks of tickets.
- Run one DEC-2 prompt and one DEC-3 prompt a few times each, plus quick keyword
  rules for DEC-2.
- The author reads about 50 outputs as the PMO lead and notes what is wrong.
- Group the notes into failure categories and count them. Each category is fixed
  in the prompt or code, becomes a code check, or becomes a judgement requirement.

It stops after two prompt rounds, or when no new categories appear. It stays
private in `_working/spike/`, uncommitted and unscored. Its keyword rules are
throwaway, not N15's rules version.

## 5. Build and delivery

**N19 · Phases and the builder.**
- Phases: F1 frame and decisions; F2a pass/fail requirements; the spike (N22);
  F2b judgement requirements and dataset; F3 harness; S1–S4 slices; W wrap-up.
- Slices: S1 metrics and capacity; S2 clustering; S3 contain; S4 lifecycle board
  and weekly update.
- The author and Claude work F1–F3 and W. The builder, an agent, builds S1–S4.
- Claude and the builder prepare commits; only the author pushes.
- Each phase ends with a gate: a fresh agent reviews all tracked files. HIGH
  findings block; the rest are fixed in one batch.

Each slice runs under a charter the author approves first. It sets the goal (a
target scorecard), the paths the builder may edit, iteration and spend caps, the
done condition and the author's approval points. The builder edits only those
paths. It never changes a test, expected answer or requirement to make something
pass. It escalates at a cap, when a failure repeats, or when a fix needs a test,
answer or requirement changed. It prepares commits and never pushes; the author
pushes.

**N2 · Repo and deployment.** v1 stays on the `archive/v1` branch and tag `v1.0`.
v2 is built on `main` in the same repository. History is never rewritten or
force-pushed. `app.py` at the root is the Streamlit entry point. The app is never
deleted: it shows a holding page now and v2 later, at the same URL.

**N11 · Records and replay.** Records are append-only plain-text weekly files,
created locally and kept in git. The public app replays them read-only and makes
no model calls. It shows any week: all 52 weeks of metrics, the model's path in
the scenario quarter, and the held-out quarter once run. The README will explain
how to reproduce the run (from W).

## 6. Documents and publishing

**N3 · Public face.** The README tells the v1-to-v2 story. Until W, it stays
short, with a status block generated from the registers. The holding page says v2
is in development. The v1 review is published in W as the v1 post-mortem annex
and linked from both.

**N4 · Privacy.** The domain is described only as a large-scale B2B payments
operation. No employer, internal tool or person is named, other than the author's
name and GitHub link. Personal working documents stay local.

**N25 · Method documents.** The method is written in markdown. F1, F2b, F3 and W
add method documents; `method/README.md` lists them. F2a and F2b complete
`02-requirements.md`. Each slice adds a charter and scorecard. Documents cite IDs;
W writes the full narrative. Word or PDF versions are exports made at the end.

**N26 · One home per fact.**
- Choices live here. Rules live in `02-requirements.md`.
- Tunable numbers and lists live in data files: the metrics register, the capacity
  file, the thresholds file, the cause list, the playbook and the generator settings.
- Facts that define the design may be stated in decisions: the size of the
  simulated world, the quarters, the SOP terms, the spike's size.
- The registers hold IDs, links, built status, preferred terms, the safeguard
  wording, and lists such as case types and evidence types.
- A data file may mirror a design fact for the code; `check.py` confirms the two
  match.
- Other documents cite IDs and restate no numbers or fixed text.
- R-DET-15 sets the document checks.

**N7 · Assumptions.** Every figure is measured or labelled an assumption. Capacity
figures and metric targets and bands are assumptions from the author's operating
experience.

## Superseded

Each replaced entry, word for word (line breaks flattened for the table), and what replaces it.

| ID | Entry | Replaced |
|---|---|---|
| N5 | **Method documents.** The method is written in markdown. F1, F2b, F3 and W each add a section; F2a and F2b complete `02-requirements.md`. Each slice adds a charter and scorecard. Sections cite IDs; W writes the full narrative. Word or PDF versions are exports made at the end. | Superseded by N25 (26 Oct 2026, decision batch): W adds three files, not one section; `method/README.md` lists the documents. |
| N6 | **One home per fact.** - Choices live here. Rules live in `02-requirements.md`. - Tunable numbers and lists live in data files: the metrics register, the capacity file, the thresholds file, the cause list and the playbook. - Facts that define the design may be stated in decisions: the size of the simulated world, the quarters, the SOP terms, the spike's size. - The registers hold IDs, links, built status, preferred terms, the safeguard wording, and lists such as case types and evidence types. - A data file may mirror a design fact for the code; `check.py` confirms the two match (from F2a). - Other documents cite IDs and restate no numbers; a script copies any wording that must appear. - R-DET-15 sets the document checks: terms and numbers from F2a, review stamps from F3, claims from S1. | Superseded by N26 (26 Oct 2026, decision batch): adds the generator settings; leaves the check phasing to R-DET-15; drops the wording-copy script, which does not exist. |
| N8 | **The Monday decision.** Every Monday the PMO lead decides which issues need action this week, and what action. The decision has four parts: - DEC-1 · Is anything off target? Code. - DEC-2 · Which new dispute tickets form a possible issue? Rules, or the model if it beats the rules (N15). - DEC-3 · Which interventions now, for each open issue and each new possible issue? The model drafts, code checks, the PMO lead reviews. Off-playbook drafts are allowed, labelled and reviewed. - DEC-4 · Do we have the capacity? Code. Weekly order: DEC-1, DEC-4 on committed hours, DEC-2, DEC-3 within the hours left, DEC-4 on the drafts, then the PMO lead's review. DEC-2 suggests a suspected cause; people confirm causes. Nothing names a root cause. The PMO lead owns the decision; the team manager, Ops specialists and executives act on parts of it. Each week has one decision record, shown as an ops view and an exec view. In the prototype the author plays every role, and each action is labelled with its role. | Superseded by N27 (26 Oct 2026, decision batch): DEC-3 drafts only for new possible issues and overdue issues not yet Contained, never for issues opened by hand; one weekly record. |
| N9 | **Issue lifecycle.** An issue moves through six stages: Detected, Contained, Cause confirmed, Corrected, Prevented, Closed. Up to Contained, people move it and code checks each stage's exit criteria. The model drafts only before Contained. After Contained, the generator scripts each stage, labelled "simulated outcome". Metrics are tracked per invoice week. The weekly update shows the week, performance and each open issue's progress until it closes. | Superseded by N23 (23 Oct 2026, F2a): each metric's week is set in the metrics register; dispute resolution is keyed to the week a ticket is opened, not the invoice week. |
| N10 | **What the prototype builds.** - To be built: metrics with colour and trends; the capacity check; DEC-2 against its rules version; Detect and Contain; the PMO lead's review; the audit record, including partner contacts and every reject and edit; the lifecycle board; the weekly update; the drift table. - Simulated: lifecycle stages after Contained (N9). - Designed, not built: the real later-stage workflow; playbook updates; a drift view on the dashboard; tracking whether interventions worked; search over past issues; turning overrides into test cases (N21); independent validation (N20); release staging (shadow, then advisory). | Superseded by N24 (23 Oct 2026, F2a): adds the stuck-invoice list, the ops and exec views and the value measures to what is built (R-DET-16, R-DET-18, R-DET-19). N24 was in turn superseded by N32 (26 Oct 2026). |
| N13 | **The year.** The simulated year has three parts: - Weeks 1–26, history. Code generates them; the model does not run. - Weeks 27–39, scenario quarter, used during the build. Each scenario spans several weeks. At least one fits no listed cause. - Weeks 40–52, held-out quarter, run once after S4 (N15). New instances of the same case types, plus a few new types whose answer is "requires human review: no matching cause". A ticket belongs to the quarter of the week it is opened. Scenario-quarter scenarios reach Contained by week 39. Held-out scenarios start in week 40 or later, depend on no earlier issue and reach Contained by week 52. Dispute rates for weeks 38–39 stay provisional until the final run. Week 52 is an ordinary quarter-end. F2b sets the number of scenarios. | Superseded by N28 (26 Oct 2026, decision batch): weeks not final at a quarter's last review follow the metrics register and are listed in F2b; cites R-RL-02's fixed text instead of copying it. |
| N14 | **Scenarios and the holdout.** - Each scenario's expected answer is written into its definition. The model is scored against it. The world data holds no answers. - Claude writes the scenario quarter. A separate agent writes the held-out quarter. - A reviewer agent on a different model reads each scenario's data without the answer. A mismatch means the scenario is ambiguous, and it is rewritten before the freeze. In the scenario quarter, Claude rewrites it and the author reads the mismatch. In the held-out quarter, its separate agent rewrites it and the author sees only counts. After the freeze, a flawed scenario is excluded and reported, never rewritten (SG-4). - The held-out quarter sits in a folder outside the project. Build sessions and the builder never open it. Its fingerprint is committed in F3 and checked before its one run. - Safeguards SG-1 to SG-4 apply: freeze first, holdout sealed, blind scoring, never fit the answer. | Superseded by N29 (26 Oct 2026, decision batch): the reviewer agent runs on a different LLM, so "the model" keeps one meaning. |
| N17 | **Requirements and evals.** Every requirement is a statement a test can fail. Each controls at least one listed risk and is proven by at least one eval. Three classes: - Deterministic: must pass 100%; a failure blocks. - Red line: zero tolerance; code checks every model output before it is shown. - Judgement: scored against a rubric or expected answers; never 100%. Deterministic and red-line cases are written first and fail before the product code exists. Judgement requirements come from the spike (N22). The dataset is designed from what the checks need. | Superseded by N30 (26 Oct 2026, decision batch): red lines also cover code and data output, not only model output. |
| N21 | **Overrides feed the tests.** Every PMO lead reject or edit will be captured with its note (to be built, N10). Turning overrides into test cases is designed, not built. The author would choose which join, as a separate set reported apart from the frozen test set. A new case never changes an existing expected answer (SG-4). | Superseded by N31 (26 Oct 2026, decision batch): cites N32; N10 was superseded. |
| N24 | **What the prototype builds.** - To be built: metrics with colour and trends; the capacity check; DEC-2 against its rules version; Detect and Contain; the PMO lead's review; the audit record, including partner contacts and every reject and edit; the lifecycle board; the weekly update; the stuck-invoice list; the ops and exec views; the value measures, labelled simulated (N16); the drift table. - Simulated: lifecycle stages after Contained (N23). - Designed, not built: the real later-stage workflow; playbook updates; a drift view on the dashboard; tracking whether interventions worked; search over past issues; turning overrides into test cases (N21); independent validation (N20); release staging (shadow, then advisory). | Superseded by N32 (26 Oct 2026, decision batch): adds the read-only public replay; "weekly record" replaces "audit record". |

## Mapping from the earlier log

Every earlier entry and safeguard, and where it lives now. Full wording: [`archive/decisions-2026-10-21.md`](archive/decisions-2026-10-21.md).

| Earlier | Title | Now |
|---|---|---|
| D1 | Full rebuild | N1 |
| D2 | Front door | N1 |
| D3 | Dataset | N12 |
| D4 | v1 kept | N2 |
| D5 | Where v2 lives | N2 |
| D6 | README | N3 |
| D7 | Streamlit app | N2 |
| D8 | Requirement classes | N30; red-line list now in 02-requirements.md |
| D9 | Answer key kept apart | N29 |
| D10 | Labels are applied cold by someone who did not write the case; one third is held out and not looked at during the build (already superseded) | N29 |
| D11 | Operating model | N25 |
| D12 | Baselines | N7 |
| D13 | Value metric: interventions actioned within the week (already superseded) | N16 |
| D14 | Domain | N4 |
| D15 | Clean main | N2 |
| D16 | Holding page | N3 |
| D17 | Private documents | N4 |
| D18 | Format | N25 |
| D19 | Entry point | N2 |
| D20 | Slices | N30 |
| D21 | Charter | N19 |
| D22 | Document checks | N26 |
| D23 | Requirements, checks, data | N30; outside validation dropped (N20) |
| D24 | Model drafts | N18 |
| D25 | Roles and views | N27 |
| D26 | Colour rule | R-DET-01; bands in the metrics register |
| D27 | Capacity (already superseded) | R-DET-05, R-RL-01; figures in the capacity file |
| D28 | Interventions and the record | R-DET-06, R-DET-09, R-RL-07; N31 |
| D29 | Playbook | R-DET-07; playbook format in 02-requirements.md |
| D30 | Confidence and gaps | R-RL-04, R-DET-08 |
| D31 | Simulated data | N12; metrics register |
| D32 | Test cases are written by Claude, except the holdout, which a separate agent writes (already superseded) | N29 |
| D33 | Git history | N2 |
| D34 | Model against rules | N15 |
| D35 | Issue lifecycle | N23, R-DET-03 |
| D36 | Framing and slices | N27, N19 |
| D37 | Value measures | N16 |
| D38 | Prototype scope | N32 |
| D39 | Records and replay | N11 |
| D40 | No AI calls in public | N11 |
| D41 | Holdout (already superseded) | N28 |
| D42 | README status | N3 |
| D43 | Document checks are phased in: no copied facts from F1, generated blocks and review stamps from F3, the claims check from S1 (already superseded) | N26 |
| D44 | Phasing | N19 |
| D45 | Stalled issues | R-DET-10 |
| D46 | Overtime | R-DET-05 |
| D47 | Labelling and holdout: test cases are written by Claude, except the holdout, which a separate agent writes (already superseded) | N29 |
| D48 | Capacity | R-DET-05, R-RL-01 (now runs every week); figures in the capacity file |
| D49 | Measured confidence | R-RL-04, R-JDG-02 |
| D50 | Month-end and quarter-end | R-DET-02 |
| D51 | Colour is the level | R-DET-01 |
| D52 | Colour triggers nothing | R-DET-04, R-DET-11; N16 |
| D53 | No numbers from the model | R-RL-05 |
| D54 | No impact forecast | R-RL-05 |
| D55 | Ticket text | N12, R-DET-12 |
| D56 | Claims in tickets | R-RL-03 |
| D57 | Derived figures | R-RL-04 |
| D58 | Escaping | R-RL-06 |
| D59 | One home for rules | N26 |
| D60 | Planned or built | N26 |
| D61 | Terms | N26; terms in the registers |
| D62 | Measures are simulated | N32, N16 |
| D63 | The year | N28, N11 |
| D64 | Unrecognised patterns | R-RL-02 |
| D65 | Two labellers | N29 (one reviewer agent replaces two labellers) |
| D66 | Sealing the held-out quarter | N29 |
| D67 | Quarter boundary | N28 |
| D68 | Failed checks | R-DET-08 |
| D69 | Cause list | R-RL-02; cause list format in 02-requirements.md |
| D70 | Metrics register | R-DET-01; metrics register format in 02-requirements.md |
| D71 | Assumptions | N7 |
| D72 | Issues opened by hand | R-DET-11 |
| D73 | Where the model stops | N23 |
| D74 | Year-end | R-DET-02, N28 |
| D75 | Due week | R-RL-05 |
| D76 | Labelling the held-out quarter | N29 (author's blind labelling of the holdout dropped) |
| D77 | Phases and gates | N19 |
| D78 | Labelling guide | N29 (dropped with the two labellers) |
| D79 | Full test set | N18 |
| D80 | Rules and data files | N26 |
| D81 | What each phase adds | N25 |
| D82 | No outside validation | N20 |
| D83 | Answer sheet | N29, SG-4 |
| D84 | Red lines | Red lines R-RL-01 to R-RL-07 |
| D85 | Builder limits | N19 |
| D86 | Charter contents | N19 |
| D87 | Privacy | N4 |
| D88 | Definitions | Glossary in the registers; N12, N15 |
| D89 | Holdout | N28, N29 |
| D90 | Labelling | N29 |
| D91 | Overrides as candidate cases | N31 |
| D92 | Rules baseline roles | N15 |
| D93 | Weekly order | N27 |

| Earlier safeguard | Title | Now |
|---|---|---|
| SG-01 | Rules baseline written by the PMO lead and frozen by the author before any scoring | SG-1 |
| SG-02 | Both versions also scored on the held-out quarter, once, after S4 | SG-2 |
| SG-03 | Blind, shuffled scoring wherever a person judges | SG-3 |
| SG-04 | Case mix fixed before any results; results reported per case type | SG-1 |
| SG-05 | Margin set before results, calibrated once from run-to-run variation | SG-1 (calibration from run-to-run variation dropped; the margin is set in F3) |
| SG-06 | Model cost shown alongside accuracy | SG-5 |
| SG-07 | Spot-check a sample of the labels both labellers agreed on | Dropped with the two labellers (N29) |
| SG-08 | Holdout written by a separate agent and sealed from the build | SG-2 |
| SG-09 | 'The case is flawed' is an allowed outcome; labels never changed to fit | SG-4 |
| SG-10 | Judgement labels are acceptable options plus rubric points | SG-1 |
| SG-11 | Disagreements answered before seeing the two labels | Dropped with the two labellers (N29) |

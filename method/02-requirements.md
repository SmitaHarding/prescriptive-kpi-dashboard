# 02 · Requirements

**Draft** (F1, 22 Oct 2026); completed in F2a and F2b. Every rule the system must meet is stated
here, once (N6, N17). F2a adds to each deterministic and red-line requirement a
failure example, a known-bad input, a threshold and a stage (CI or local). The
judgement requirements are hypotheses: the spike (N22) confirms, replaces or
extends them, and F2b writes them in full.

Each requirement controls at least one risk. Risks and the v1 defects behind them
are in [`../spec/registers.toml`](../spec/registers.toml). Classes (N17): **DET**
deterministic, **RL** red line, **JDG** judgement. Tunable numbers live in the
data files listed at the end; none are stated here.

## DEC-1: is anything off target? (code)

**R-DET-01 · Colour shows the level.** Each coloured metric is green at or better
than its target, amber inside its amber band, and red beyond, by its direction. A
metric beyond red is red whether worsening or recovering; it leaves red only when
back inside the threshold. Beside the colour, never changing it: the
week-over-week change; the change against the trend-window average
(like-for-like while a dispute window is open); a sparkline over the trend window;
and "n/a" until a full window exists. On the chart the trend line is neutral, and
only amber and red weeks carry a coloured dot. No graded states, no persistence
rule, no seasonal targets.
*Risks:* RK-01. *Check:* unit tests over register values, including a recovering
red week. *Cases:* recovery week.

**R-DET-02 · Cycle weeks.** Month-end and quarter-end weeks are marked in the data
and coloured against the normal targets (R-DET-01). Before DEC-2 proposes a
possible issue in a cycle week, it compares the week with the same point in
earlier cycles, and proposes only a pattern beyond the usual cycle. A cycle week
with too few earlier cycles is labelled "no cycle comparison available", and any
pattern in it is left to the PMO lead. The comparison rule is set in F2b.
*Risks:* RK-01. *Check:* unit tests on cycle weeks. *Cases:* false-positive bait.

**R-DET-03 · Provisional dispute rate.** The dispute rate is the share of a week's
invoices disputed within the dispute window. Until the window closes, it is
coloured on its current value and labelled "window open — provisional". The next
update restates the final value and any change of colour.
*Risks:* RK-01. *Check:* unit test across the window close. *Cases:* provisional
week.

**R-DET-04 · Colour triggers nothing.** A colour never opens an issue or creates
an intervention. An issue opens only when the PMO lead accepts a possible issue
or opens one by hand (R-DET-11).
*Risks:* RK-01. *Check:* every issue in the record traces to an accepted proposal
or a manual entry. *Cases:* red week with no tickets.

## DEC-4: do we have the capacity? (code)

**R-DET-05 · Capacity check.** Workload is the weekly payment run, plus time per
dispute (counted in the week it is opened), per exception and per stuck invoice,
from the capacity file, plus the effort of reported interventions, from the
playbook. Productive hours are team hours minus protected time. Utilisation is
workload divided by productive hours, compared with the ceiling in the capacity
file. Absence is not modelled; the team manager confirms availability. The check
runs every week. Above the ceiling it proposes overtime first, which the team
manager approves within the weekly limit, then extra FTEs, which need exec
authority. An overtime proposal is a capacity proposal, not an intervention. Both
views show the improvement time remaining: productive hours minus workload. When
DEC-4 runs again on the drafts (N8), it adds each draft's effort from its playbook
entry.
*Risks:* RK-05. *Check:* unit tests on boundary weeks. *Cases:*
capacity-infeasible week.

**R-RL-01 · Working-time limit.** No plan shown puts anyone above the weekly hours
limit, or commits more hours than are available with approved overtime.
*Risks:* RK-05. *Check:* code check on every plan; a known-bad plan must fail.
*Cases:* capacity-infeasible week.

## DEC-2: which new dispute tickets form a possible issue?

**R-JDG-01 · Detection against rules (hypothesis).** Possible issues match the
planted patterns and are found no later than the rules version finds them. The
model version is used only as N15 sets out.
*Risks:* RK-02, RK-15. *Check:* scorer against expected answers: recall,
precision, suspected-cause accuracy, lead time and cost, per case type. *Cases:*
all case types.

**R-RL-02 · Cause from the list, or human review.** A suspected cause comes only
from the cause list. When a pattern matches no cause, none is proposed: the item
shows the fixed text "requires human review: no matching cause", with the tickets
and the counts code computed. "No issue this week" is also a valid answer.
*Risks:* RK-03. *Check:* schema and list check. *Cases:* unrecognised pattern.

**R-RL-03 · Ticket claims are claims.** A cause stated in ticket text is its
writer's claim. It is recorded as "claimed in tickets", with a count from code,
and shown on the review screen as a starting point. It never counts as evidence
for confidence. It never appears in the ops or exec view, or as the basis of an
intervention, unless the PMO lead confirms it. The model adds nothing the tickets
do not say.
*Risks:* RK-03. *Check:* code check on evidence IDs and fields. *Cases:*
misleading partner guess.

**R-RL-04 · Confidence is measured.** Every suspected cause the rules or model
version proposes carries a confidence
level (low, medium or high) and its evidence gaps. Code computes the highest level
the evidence supports. High: at least the thresholds file's minimum number of
independent evidence types agree, with no gaps. Medium: fewer types, or minor
gaps. Low: thin or conflicting evidence. Code also computes cluster size, field
agreement and run-to-run consistency. The evidence types are a fixed list, set in
F2b. Metrics that move together by construction count as one type. Derived
figures, such as workload and utilisation, and ticket claims never count. A label
above the computed level, or high confidence with any gap, fails.
*Risks:* RK-04. *Check:* code check against the computed level. *Cases:* thin
evidence, contradictory evidence.

**R-JDG-02 · Calibration (hypothesis).** High-confidence calls are right more
often than medium ones, and medium more often than low. The model holds back where
the scenario expects it to. Calibration is shown in the drift table.
*Risks:* RK-04. *Check:* scorer against expected answers. *Cases:* thin evidence,
contradictory evidence, unrecognised pattern.

## DEC-3: which interventions now? (the model drafts, code checks, the PMO lead reviews)

**R-RL-05 · No invented figures or dates.** Every number in a draft is already in
the evidence code gave the model, or in the playbook entry. Ticket references and
week numbers quoted from the evidence are allowed. No intervention shows an
expected impact: it states what it addresses and its effort, and value is measured
afterwards (N16). Code sets each due week: the week reported plus the time allowed
in the playbook entry. The PMO lead may change it in review. The model sets no
dates.
*Risks:* RK-07. *Check:* number-grounding checker; a known-bad draft must fail.
*Cases:* every model case.

**R-DET-06 · Coverage without padding.** Every suspected cause has at least one
intervention, or a deferral with a reason. A cause and stage may have several
interventions when each meets a different need, never two of the same playbook
type. Each intervention names its cause and stage and cites its evidence. Capacity
is the overall limit (R-DET-05).
*Risks:* RK-06. *Check:* code check on every draft. *Cases:* two causes, thin
evidence.

**R-DET-07 · The playbook respects the SOP.** Interventions come from the
playbook, which code pre-filters by suspected cause; there is no retrieval step.
Every playbook entry has a type from the playbook's fixed list. The list holds no
type that stops or delays the weekly payment run (N12) or skips the approval chain.
Off-playbook interventions are allowed; they are labelled and shown only after
review. If the spike shows the model proposing changes to the payment run,
off-playbook interventions must also carry a listed type, and this becomes a red
line.
*Risks:* RK-12. *Check:* check when the playbook loads; rubric item in R-JDG-03.
*Cases:* SOP-breaking bait.

**R-JDG-03 · Practical and proportionate (hypothesis).** Interventions fit the
suspected cause and stage, have a realistic owner, respect the payment and dispute
SOPs, and give the right detail for the ops and exec views.
*Risks:* RK-06, RK-12. *Check:* the author scores blind against a rubric (SG-3).
*Cases:* happy path, two causes.

**R-DET-08 · Failed checks are never repaired.** A draft that fails any code check
is rejected and not shown, and the model is asked once more. If the second draft
also fails, the item shows the fixed text "requires human review: failed check"
and the name of the check. Code never repairs a draft. Every rejected draft is
kept in the weekly record, and the rejection rate is a drift measure.
*Risks:* RK-03 to RK-07. *Check:* inject failing drafts. *Cases:* known-bad
drafts.

## Across the week

**R-RL-06 · Escaping and injection.** All text from the model or from data (model
output, ticket text, playbook steps, notes) is shown as plain text and escaped
before rendering, in the local run and in the replay. Instructions inside ticket
text change nothing in the output.
*Risks:* RK-08. *Check:* rendering test; each injection case compared with a clean
twin. *Cases:* prompt injection.

**R-RL-07 · Review before anything is shown.** Nothing the model drafts appears in
the ops or exec view until the PMO lead has reviewed it. Drafts and ticket claims
appear first on the review screen. A possible issue becomes an issue only when the
PMO lead accepts it.
*Risks:* RK-09. *Check:* record and view check. *Cases:* every model case.

**R-DET-09 · Append-only record.** Every draft, edit and decision is kept in an
append-only weekly record, with its status (pending review, reported, rejected,
deferred), the reviewer's role and the time. Every reject or edit needs a note. An
intervention that contacts partners records which partners and when. The replay
rebuilds any week from the record.
*Risks:* RK-10. *Check:* the replay matches the record. *Cases:* every week.

**R-DET-10 · Stalled issues.** Code counts the days an issue has spent in its
current stage, from the recorded stage dates, and compares them with that stage's
limit in the thresholds file. An issue over its limit is marked overdue on the
board and in the weekly update. For an overdue issue not yet Contained, the model
proposes a next action, reviewed like any other draft, unless the PMO lead opened
the issue by hand (R-DET-11).
*Risks:* RK-11. *Check:* unit tests on stage dates. *Cases:* stalled issue.

**R-DET-11 · Issues opened by hand.** For an issue the PMO lead opens by hand,
with or without dispute tickets, the PMO lead picks the suspected cause from the
cause list or marks it "under investigation". Code shows the playbook entries for
that cause. The PMO lead selects from them or writes their own, with effort and
due week. The model drafts nothing for this issue. The cause is labelled "entered
by PMO lead" and carries no confidence level. The capacity check applies. When
later tickets form a pattern, the PMO lead may attach them to the existing issue
in review; the model never merges issues.
*Risks:* RK-02, RK-09. *Check:* record check. *Cases:* issue opened by hand.

## The evidence: harness and documents

**R-DET-12 · No answer in the world.** No cause label, expected answer or weekly
metric value appears in ticket text; code scans every generated ticket before the
data is accepted. Prototype code cannot read the scenario definitions.
*Risks:* RK-13. *Check:* leakage scan; import check. *Cases:* every generated
ticket.

**R-DET-13 · The holdout stays sealed.** The held-out quarter's fingerprint
matches the committed one before its single run (N14).
*Risks:* RK-14. *Check:* fingerprint check. *Cases:* held-out quarter.

**R-DET-14 · Change gate.** A new model version, prompt or data file is used only
after the whole scenario quarter passes with no regression and the drift table is
inside the limits in the thresholds file (N18).
*Risks:* RK-16. *Check:* scorecard comparison. *Cases:* whole scenario quarter.

**R-DET-15 · Documents match what exists.** A document calls something built only
when the registers mark it built and its requirements pass. Tunable numbers appear
only in data files (N6). Preferred terms are used.
*Risks:* RK-17. *Check:* `check.py`, added in stages: terms and numbers in F2a,
review stamps in F3, claims in S1 (N6). *Cases:* every tracked document.

## Data files

The PMO lead owns these files and approves changes; each change is versioned and
re-tested (R-DET-14). Items frozen under SG-1, such as the N15 margin, change only
as N15 sets out. All figures are assumptions (N7).

| File | Holds | Status |
|---|---|---|
| [`../spec/metrics.toml`](../spec/metrics.toml) | Each metric's definition, direction, target and amber band | v0: definitions and the relative band; targets and the other bands in F2a |
| [`../spec/capacity.toml`](../spec/capacity.toml) | Team, hours, protected time, overtime, the weekly hours limit, effort per item, the utilisation ceiling | v0: figures; ceiling in F2a |
| [`../spec/thresholds.toml`](../spec/thresholds.toml) | Trend window, evidence minimum for high confidence, the N15 margin, drift limits, stage limits, cycle minimum | v0: trend window and evidence minimum; the rest in F2b and F3 |
| Cause list (`spec/causes.toml`) | Each cause's name, a short description, and the ticket fields or metrics that support it | First version in F2a |
| Playbook (`spec/playbook.toml`) | Each entry's type (from a fixed list), owner role, effort range, the causes it fits, whether it needs exec authority, the time allowed, and best-practice steps shown word for word. The model may only propose changes, through a workflow designed, not built (N10) | First version in F2a |
| Generator settings (`spec/generator.toml`) | The share of wrong partner guesses (N12); the number and layout of scenarios (N13) | F2b |

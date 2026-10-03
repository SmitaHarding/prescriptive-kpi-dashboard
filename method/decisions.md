# Decisions

The single record of **what** has been decided. One line per decision. A change
is a new entry that supersedes an old one — entries are never edited to say
something different. Other documents refer to these IDs instead of restating
them. A fully replaced entry moves, unchanged apart from its pointer, to the
Superseded section at the end; it is never erased.

Status of D25–D44: agreed at the close of the F1 decision pass (30 Sep 2026).
D45–D50: agreed in the F1 review (1 Oct 2026).

| ID | Decision |
|----|----------|
| D1 | Full rebuild, from the frame through monitoring. Nothing is lifted from v1 without passing the harness. |
| D2 | The operating model is the front door; the prototype is the evidence. |
| D3 | The dataset is simulated — redesigned, not reused from v1. |
| D4 | v1 is preserved on the `archive/v1` branch and tag `v1.0`, not deleted. |
| D5 | v2 is built on a clean `main` in the same repository. |
| D6 | The README carries the arc; the v1 review is one click deep. |
| D7 | The Streamlit app is never deleted: holding page now, v2 later, same URL. |
| D8 | Requirements are failable statements in three classes: deterministic (100%, blocking), red-line (zero tolerance, checked in code on model output), judgement (rubric-scored, never 100%). |
| D9 | The golden set is kept apart from the world data; the data carries no answer key. |
| D11 | The operating model is written one section per session. |
| D12 | Baselines are measured, or explicitly labelled as assumptions. |
| D14 | The domain is described as a large-scale B2B payments operation; the employer is not named. |
| D15 | "Clean main" means clean contents: v1 removed and v2 added without force-pushing, so the history stays visible. |
| D16 | The holding page states the position; the v1 review is linked when the operating model ships. |
| D17 | Personal working documents stay local and are never published. |
| D18 | The method is written in markdown; any Word or PDF pack is an export at the end. |
| D19 | `app.py` at the repository root is the Streamlit entry point. |
| D20 | Slice-based build: each slice's test cases are written, and fail, before its code. |
| D21 | Every build slice runs under a charter approved before it starts. The agent never edits a test, label or requirement to make something pass. |
| D22 | Document content is checked, not just versioned: no copied facts, generated blocks, content-review stamps, and a claims check. |
| D23 | Requirements and their checks are designed together; a validation plan names who outside the project judges fitness for purpose; the dataset follows from what the checks need. |
| D24 | The AI's drafts are constrained, checked in code before a human sees them, and monitored for drift. Hallucination is bounded and detected, never claimed to be zero. A new model version, prompt or playbook is used only after the full test set passes. |
| D25 | One decision owner — the PMO lead — with several actors: team manager, Ops specialists and executives. One decision record per week, shown by code as an ops view and an exec view, each with only the fields tagged for it. The prototype has one user acting in every role, each action labelled by role. |
| D26 | Colour against target, per metric and direction: "higher is better" rates are amber up to 2% worse than target (relative to the target), red beyond; low rates, counts and days use a band set per metric. Shown alongside: week-over-week change and change against the previous 4-week average (like-for-like while a dispute window is open), a 4-week sparkline, and "n/a" for the first 4 weeks. No graded states, no persistence rule, no seasonal targets. |
| D28 | Every cause has at least one intervention or a deferral with a reason. Several are allowed per cause and stage when each addresses a different need — no two of the same playbook type for the same cause and stage. Each names its cause and stage and cites its evidence; capacity is the overall limit. Nothing the AI drafts is shown until the PMO lead has reviewed it. Every draft, edit and decision is kept in an append-only weekly record with status (pending review, reported, rejected, deferred), reviewer, time, and a required note on reject or edit. |
| D29 | Interventions come from a playbook: a data file the PMO lead edits, each entry with owner role, effort range, the causes it fits, whether it needs exec authority, and best-practice steps shown word for word. Code pre-filters entries by suspected cause; there is no retrieval step. Off-playbook interventions are allowed, labelled, and shown only after review. Playbook changes are approved by the PMO lead, versioned and re-tested; the agent may only propose them. |
| D30 | Every proposed cause carries a confidence level (low, medium, high) and its evidence gaps. Evidence gaps together with high confidence is a red line: rejected, retried once, then shown as "needs human review". Whether the model held back when it should have is a judgement metric. |
| D31 | Simulated data: 1,500 partners, one invoice each per week, 52 weeks, English-only text, labelled as synthetic. Coloured metrics: payment accuracy, dispute rate, exception rate, dispute resolution within 5 days, processing cycle days, stuck invoices; invoice volume is shown as context. Payment accuracy counts confirmed errors only. |
| D33 | The git history is not rewritten. |
| D34 | The AI's clustering is compared with a rules-only baseline on the same dispute tickets, scored against the confirmed cause and on lead time. The model is used for a part only where it beats the rules by an agreed margin and is never worse on red lines. Safeguards SG-01 to SG-06 apply; decisions are routinely compared against the safeguard register. |
| D35 | Issues move from Detected through Contained, Cause confirmed, Corrected and Prevented to Closed, with exit criteria checked in code; people move stages, the AI proposes actions and flags stalls. Metrics are tracked per invoice week. The dispute rate is the share of a week's invoices disputed within the two-week window, coloured on its current value and labelled "window open — provisional" until the week closes; the next update restates the final values and any colour change. The weekly ops and exec update shows the week number, performance, and each open issue's progress until it closes. |
| D36 | The product is framed around issues: the AI spots patterns across dispute tickets and never names a root cause; people confirm causes after investigation. Build slices: S1 metrics and capacity, S2 clustering, S3 contain, S4 lifecycle board and weekly update. |
| D37 | Value is measured two ways. Adoption: reported interventions actioned by their due week. Outcome: time to contain (primary), share of issues caught proactively, share of affected partners contacted before they disputed. Replaces D13. |
| D38 | Prototype scope. Built: metrics with colour and trends; capacity check; clustering against the rules baseline; Detect and Contain; review gate and audit record; weekly update; drift table in the scorecard. Illustrative, scripted by the generator and labelled "simulated outcome": Cause confirmed, Corrected, Prevented. Designed, not built: the real later-stage workflow, a playbook update workflow, a dashboard drift view, outcome tracking, retrieval over past issues. |
| D39 | Records are plain-text, append-only weekly files, created locally and stored in git. The public app is a read-only replay that can show the state as of any week. |
| D40 | The public app makes no AI calls. The README explains how to reproduce the run locally. |
| D41 | Holdout: the last quarter of simulated tickets (weeks 40–52), scored once per slice; about 15 week-level scenarios, 5 of them held out and also used by an outside practitioner for validation. |
| D42 | A short README with a generated status block, from F1 until the overview is written in W. |
| D43 | Document checks are phased in: no copied facts from F1, generated blocks and review stamps from F3, the claims check from S1. |
| D44 | F1 runs in one session in slimmer form; later documents and registers are added when first used; S4's size is set in its charter. |
| D45 | Stalled issues are detected by code: days in the current stage, from the recorded stage dates, against a limit per stage set in F2; an issue over its limit is marked overdue on the board and in the weekly update. The AI only proposes the next action for an overdue issue, reviewed like any other draft. Replaces the part of D35 that had the AI flag stalls. |
| D46 | Overtime is approved by the team manager, within the 48-hour limit; extra FTEs remain an exec decision (D48). |
| D47 | Labelling and holdout: test cases are written by Claude, except the holdout, which a separate agent writes. A fresh agent with no project context labels them cold; the PMO lead decides disagreements and labels the holdout. The holdout is set by D41 and is not looked at during the build. Safeguards SG-07 to SG-11 apply. Replaces D10 and D32. |
| D48 | Capacity: a baseline team of 5 FTE × 40 h, less 4 h protected time each for meetings and admin, gives 180 productive hours a week; 220 h with overtime; 48 h per person is a red line. Absence is not modelled — the team manager confirms availability. Workload = 60 h weekly payment run + 2 h per dispute (counted in the week it is opened) + 15 min per exception + 30 min per stuck invoice + the effort of reported issue interventions. Utilisation = workload ÷ productive hours, against a target ceiling set in F2. The check runs every week with open issues or amber or red metrics; above the ceiling it proposes overtime first, then extra FTEs, which need exec authority. Improvement time remaining is shown on both views. Replaces D27. |
| D49 | Confidence is measured, not asserted: high = at least two independent evidence types agree and there are no gaps; medium = one evidence type or minor gaps; low = thin or conflicting evidence. Code computes cluster size, field agreement and run-to-run consistency, and the model's label is checked against them. Calibration is measured on the test set and shown in the drift table. Exact rules are set in F2. Refines D30. |
| D50 | Month-end and quarter-end weeks are marked in the data. Before proposing an issue, clustering compares a cycle week with the same point in earlier cycles; only a pattern beyond the usual cycle is proposed. Colours stay on target (D26: no seasonal targets). The comparison rule is set in F2. |

## Superseded

Kept for traceability. Each entry names the decision that replaced it.

| ID | Decision |
|----|----------|
| D10 | Labels are applied cold by someone who did not write the case; one third is held out and not looked at during the build. **Superseded by D47.** |
| D13 | Value metric: interventions actioned within the week. **Superseded by D37.** |
| D27 | Capacity: a baseline team of 5 × 40 h = 200 h a week, 240 h with overtime; 48 h per person is a red line. Absence is not modelled — the team manager confirms availability. Required hours = 60 h weekly payment run + 20 h protected meetings and admin + 2 h per dispute + 15 min per exception + 30 min per stuck invoice + the effort of reported issue interventions. The capacity check runs every week with open issues or amber or red metrics: overtime first, then extra FTEs, which need exec authority. Improvement time remaining is shown on both views. **Superseded by D48.** |
| D32 | Test cases are written by Claude, except the holdout, which a separate agent writes. A fresh agent with no project context labels them; the PMO lead decides disagreements and labels the holdout. Safeguards SG-07 to SG-11 apply. **Superseded by D47.** |

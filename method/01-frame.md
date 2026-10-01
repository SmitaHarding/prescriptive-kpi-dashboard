# 01 · Frame

What the system exists to improve, who acts on it, and where code ends and the
model begins. Numbers and thresholds are not restated here; each point refers
to its entry in [`decisions.md`](decisions.md) (D22: no copied facts).

## The decision

*Every Monday, the PMO lead decides which operational problems need action this
week, and what that action should be* — for a large-scale B2B payments
operation (D14).

The problems surface in two ways:

- **Reactive:** partners dispute an invoice with a short, often unclear text;
  Ops opens a case, investigates with the partner, confirms the cause and
  resolves it.
- **Proactive:** Ops spots an error before partners dispute, works out who is
  affected, confirms the cause and correction, and contacts the partners first.
  The metrics may not move, but the issue is real.

The root cause is only known **after** an investigation. So the system never
names a root cause. It spots patterns across dispute tickets and proposes where
to look; people confirm (D36). A proposed cluster carries a **suspected cause**
— a hypothesis taken from the cause list below, always marked unconfirmed. The
root cause is set only by a person, when the issue reaches *Cause confirmed*.

Common root causes, used as the cause list for confirmed issues: input errors by
internal teams or partners · incorrect activity data behind an invoice · delayed
reporting from external suppliers · a pricing or calculation error · a stuck
invoice · a partner disputing because the payment was unclear.

## Four sub-decisions

Each is answered by code wherever code can answer it — the least AI that works.

| | Question | Input | Output | Answered by | Confirmed by |
|---|---|---|---|---|---|
| **DEC-1** | Is anything off target? | Weekly metrics per invoice week (D31, D35) | Colour, trends, provisional status (D26, D35) | Code | — (a fact) |
| **DEC-2** | Which new dispute tickets form a possible issue? | The week's new tickets: fixed fields and free text | Proposed clusters of ticket IDs, each with a suspected cause, a confidence level and evidence gaps (D30); counts computed by code (D24) | Two parts, each done by rules or by the model (see below) | PMO lead confirms → an issue is created |
| **DEC-3** | What action now, and next, for each open issue? | Open issues with stage, playbook entries pre-filtered by cause in code (D29), hours still available (DEC-4) | Interventions per cause and stage (D28) | Model drafts from the pre-filtered entries; code runs the checks below | PMO lead reviews before anything is shown (D28) |
| **DEC-4** | Do we have the capacity? | Workload and the effort of reported interventions (D27) | Hours needed against hours available; overtime, then extra FTEs | Code | Team manager confirms availability and approves overtime (D46); execs approve extra FTEs (D27) |

### DEC-2: rules or model, part by part

DEC-2 has two parts: **grouping** the tickets into clusters, and giving each
cluster a **suspected cause**. For each part, a rules-only version and the
model produce the same output — cluster, suspected cause, confidence, evidence
gaps — and pass the same red lines, checked in code: every cited ticket ID
exists, counts are computed by code, no high confidence alongside evidence gaps
(D30). The model is used for a part only if it beats
the rules on that part by the agreed margin and is never worse on red lines
(D34). The margin is set in F2, before any results, and recorded as a D entry
(SG-05). Until a part has passed that test, the rules version runs.

### DEC-3: checks run in code before the PMO lead sees a draft

- Every number in the draft appears in the evidence given to the model (D24).
- Every cited ticket, evidence and cause ID exists.
- Every intervention names its cause and stage; every cause has an intervention
  or a deferral with a reason; no two interventions of the same playbook type for
  the same cause and stage (D28).
- Total effort fits the hours available, and nobody goes above the 48-hour
  limit (D27).
- No high confidence alongside evidence gaps (D30).
- Instructions inside ticket text have no effect (D24) — ticket text is passed
  to the model only as data, and planted injection cases in the test set prove it.

A failed check rejects the draft — one retry, then "needs human review". An
off-playbook intervention may be drafted by the model or written by the PMO
lead; either way it is labelled and passes the same checks (D29).

### Order within a week

DEC-1, then DEC-4 computes the hours already committed (payment run, protected
admin, problem work, interventions already reported). DEC-2 proposes clusters;
DEC-3 drafts within the hours left; DEC-4 runs again on the drafted
interventions before the PMO lead reviews them.

## Issue lifecycle

Detected → Contained → Cause confirmed → Corrected → Prevented → Closed (D35).
Each stage has exit criteria checked in code; people move an issue forward, and
code refuses a move whose criteria are not met. Code marks an issue overdue when
it has been in a stage longer than that stage's limit (D45); the model only
proposes next actions, and never moves a stage. In the prototype, the stages
after Contained are illustrative, scripted by the data generator and labelled as
simulated outcomes (D38).

## Who does what

| Role | Acts on |
|---|---|
| PMO lead | Owns the Monday decision; confirms clusters; reviews every drafted intervention; owns the weekly update |
| Team manager | Confirms team availability; approves overtime (D46); assigns owners; marks interventions actioned |
| Ops specialists | Investigate; contact partners; move issues through stages |
| Executives | Approve extra FTEs and anything needing their authority |

One decision record per week, shown as an ops view and an exec view by code
(D25). In the prototype one user acts in every role, each action labelled by
role.

## How value is judged

Two measures, both on the far side of the human (D37): whether people act on
what is proposed (adoption), and whether operations improve (outcome).
Baselines are measured or labelled as assumptions (D12).

## Open for F2

- The margin for the rules-vs-model test in DEC-2 (SG-05).
- Which value of a playbook entry's effort range the capacity check uses.
- The time limit for each stage, after which an issue is marked overdue (D45).

## What the prototype is

A replay of a year of simulated operation, run and reviewed locally and
published read-only (D39, D40). Scope — what is built, illustrative, and
designed but not built — is fixed in D38. Nothing is described as built unless
its requirement passes (D22).

# 01 · Frame

What Aegis exists to improve, who acts, and where code ends and the model begins.
This page explains; it decides nothing. Choices are in
[`decisions.md`](decisions.md), rules in [`02-requirements.md`](02-requirements.md).
Where they differ from this page, they win.

## The operation

A large-scale B2B payments operation pays its partners weekly for completed
services by self-billing: it calculates each payment, issues the invoice and pays
it (N12). Partners may dispute an invoice within a fixed window. Errors that slip
through the weekly run surface later as dispute tickets, or as corrections Ops
specialists find themselves.

## The decision

Aegis supports the PMO lead's Monday decision (N27).

Issues arrive two ways:

- **Reactive:** dispute tickets form a pattern (DEC-2).
- **Proactive:** the PMO lead opens an issue by hand before partners dispute
  (R-DET-11).

A metric's colour opens nothing (R-DET-04). A cause is known only after people
investigate, so DEC-2 proposes a suspected cause from the cause list, or says the
pattern matches none (R-RL-02). People confirm causes.

## Code where possible, the model where needed

Each part of the decision goes to code wherever code can do it.

| | Question | Done by | Checked by | Requirements |
|---|---|---|---|---|
| **DEC-1** | Is anything off target? | Code | Nobody: it is a fact | R-DET-01 to R-DET-04, R-DET-16 |
| **DEC-2** | Which new dispute tickets form a possible issue? | The rules version, or the model version if it wins (N15) | Code; the PMO lead accepts or rejects | R-JDG-01, R-RL-02 to R-RL-04, R-JDG-02 |
| **DEC-3** | Which interventions now, for new possible issues and overdue issues? | The model drafts, mostly from playbook entries code has pre-filtered | Code checks every draft; the PMO lead reviews | R-RL-05, R-DET-06 to R-DET-08, R-JDG-03 |
| **DEC-4** | Do we have the capacity? | Code | The team manager (availability, overtime); executives (extra FTEs) | R-DET-05, R-RL-01 |

**DEC-2.** Dispute reasons are free text, so reading them for one underlying
problem is where the model can add value. The rules version and the model version
produce the same output and face the same red lines. N15 sets how they are
compared and when the model is used.

**DEC-3.** The model adds no numbers, dates or impact forecasts (R-RL-05). A draft
that fails a check is rejected, never repaired (R-DET-08). An off-playbook
intervention is labelled and shown only after review (R-DET-07). For an issue
opened by hand, the model drafts nothing (R-DET-11).

The weekly order of the four parts is in N27.

## Issue lifecycle

People move an issue up to Contained, where the model's part ends. Later stages
are simulated and labelled so (N23, R-DET-22). Code marks an issue overdue when it stays in a stage too long
(R-DET-10).

## Who does what

| Role | Acts on | IDs |
|---|---|---|
| PMO lead | Owns the Monday decision; accepts possible issues; reviews every draft; may open an issue by hand | N27, R-RL-07, R-DET-11 |
| Team manager | Confirms availability; approves overtime | R-DET-05 |
| Ops specialists | Investigate; contact affected partners; remedy stuck invoices | N27, N16, R-DET-16 |
| Executives | Approve extra FTEs and anything needing exec authority | R-DET-05 |
| The author | Owns the project; plays every role in the prototype; judges fitness for purpose | N27, N20 |

## Value and validation

Value is measured after a person acts (N16). No outside person validates the
prototype; this is a stated limitation (N20).

## Risks

The risks the requirements control, and the v1 defects that show they are real,
are in [`../spec/registers.toml`](../spec/registers.toml). `check.py` confirms
every v1 defect maps to a risk and every risk has a requirement.

## Open for the spike and F2b

- **Spike (N22):** how the model actually fails on DEC-2 and DEC-3.
- **F2b:** the judgement requirements; the final case types; evidence types, and
  what counts as a gap and a minor gap (R-RL-04); the cycle comparison rule and
  minimum, and which weeks are month-ends (R-DET-02); stage limits and exit criteria
  (R-DET-10); which weeks stay provisional at the quarter boundary (N28), including the held-out
  quarter's last weeks, which no later review shows; the share
  of wrong partner guesses; the number and layout of scenarios; runs per case; how
  affected partners are identified (R-DET-18); what the history weeks contain; line
  types and lines per invoice.

## What the prototype is

A local run: the model drafts, code checks, and the author reviews in every role.
The public app is a read-only replay of that run (N11). N32 sets what is to be
built, simulated, or designed but not built. Nothing is called built until R-DET-15
allows it.

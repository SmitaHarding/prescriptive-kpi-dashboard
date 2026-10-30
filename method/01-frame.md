# 01 · Frame

What Aegis exists to improve, who acts, and where code ends and the model begins.
This page explains; it decides nothing. Choices are in
[`decisions.md`](decisions.md), requirements in [`02-requirements.md`](02-requirements.md).
Where they differ from this page, they win.

## The operation

A large-scale B2B payments operation pays its partners weekly for completed
services by self-billing: it calculates each payment, issues the invoice and pays
it ([Simulated world](decisions.md#simulated-world)). Partners may dispute an invoice
within a fixed window. Errors that slip through the weekly run surface later as dispute
tickets, or as corrections Ops specialists find themselves.

## The decision

Aegis supports the PMO lead's [Monday decision](decisions.md#the-monday-decision).

Issues arrive two ways:

- **Reactive:** dispute tickets form a pattern ("Possible issues?").
- **Proactive:** the PMO lead opens an issue by hand before partners dispute
  ([Issues opened by hand](02-requirements.md#issues-opened-by-hand)).

A metric's colour opens nothing ([Colour triggers nothing](02-requirements.md#colour-triggers-nothing)).
A cause is known only after people investigate, so "Possible issues?" proposes a suspected
cause from the cause list, or says the pattern matches none
([Cause from the list, or human review](02-requirements.md#cause-from-the-list-or-human-review)).
People confirm causes.

## Code where possible, the model where needed

Each of the four Monday questions goes to code wherever code can do it.

| Question | Done by | Checked by | Requirements |
|---|---|---|---|
| **Off target?** | Code | Nobody: it is a fact | [Off target?](02-requirements.md#off-target) |
| **Possible issues?** Which new dispute tickets form a possible issue? | The rules version, or the model version if it wins ([Model against rules](decisions.md#model-against-rules)) | Code; the PMO lead accepts or rejects | [Possible issues?](02-requirements.md#possible-issues) |
| **Which interventions?** For new possible issues and overdue issues | The model drafts, mostly from playbook entries code has pre-filtered | Code checks every draft; the PMO lead reviews | [Which interventions?](02-requirements.md#which-interventions) |
| **Enough capacity?** | Code | The team manager (availability, overtime); executives (extra FTEs) | [Enough capacity?](02-requirements.md#enough-capacity) |

**Possible issues?** Dispute reasons are free text, so reading them for one underlying
problem is where the model can add value. The rules version and the model version
produce the same output and face the same [red lines](02-requirements.md#red-lines).
[Model against rules](decisions.md#model-against-rules) sets how they are compared and
when the model is used.

**Which interventions?** The model adds no numbers, dates or impact forecasts
([No invented figures or dates](02-requirements.md#no-invented-figures-or-dates)). A draft
that fails a check is rejected, never repaired
([Failed checks are never repaired](02-requirements.md#failed-checks-are-never-repaired)).
An off-playbook intervention is labelled and shown only after review
([The playbook respects the SOP](02-requirements.md#the-playbook-respects-the-sop)). For an
issue opened by hand, the model drafts nothing.

The weekly order of the four questions is in the [Monday decision](decisions.md#the-monday-decision).

## Issue lifecycle

People move an issue up to Contained, where the model's part ends. Later stages
are simulated and labelled so ([Issue lifecycle](decisions.md#issue-lifecycle),
[Simulated is labelled](02-requirements.md#simulated-is-labelled)). Code marks an issue
overdue when it stays in a stage too long ([Overdue issues](02-requirements.md#overdue-issues)).

## Who does what

| Role | Acts on |
|---|---|
| PMO lead | Owns the Monday decision; accepts possible issues; reviews every draft before anything is shown; may open an issue by hand |
| Team manager | Confirms availability; approves overtime |
| Ops specialists | Investigate; contact affected partners; remedy stuck invoices |
| Executives | Approve extra FTEs and anything needing exec authority |
| The author | Owns the project; plays every role in the prototype; judges fitness for purpose |

## Value and validation

Value is measured after a person acts ([Value measures](decisions.md#value-measures)). No
outside person validates the prototype; this is a stated limitation
([No outside validation](decisions.md#no-outside-validation)).

## Risks

The risks the requirements control, and the v1 defects that show they are real,
are in [`../spec/registers.toml`](../spec/registers.toml). `check.py` confirms
every v1 defect maps to a risk and every risk has a requirement.

## Open for the spike and the judgement phase

- **Spike ([Build-and-look spike](decisions.md#build-and-look-spike)):** how the model
  actually fails on "Possible issues?" and "Which interventions?".
- **Judgement and data:** the judgement requirements; the final case types; evidence types,
  and what counts as a gap and a minor gap; the cycle comparison rule and minimum, and which
  weeks are month-ends; stage limits and exit criteria; which weeks stay provisional at the
  quarter boundary, including the held-out quarter's last weeks, which no later review shows;
  the share of wrong partner guesses; the number and layout of scenarios; runs per case; how
  affected partners are identified; what the history weeks contain; line types and lines per
  invoice.

## What the prototype is

A local run: the model drafts, code checks, and the author reviews in every role.
The public app is a read-only replay of that run ([Records and replay](decisions.md#records-and-replay)).
[What the prototype builds](decisions.md#what-the-prototype-builds) sets what is to be built,
simulated, or designed but not built. Nothing is called built until
[Documents match what exists](02-requirements.md#documents-match-what-exists) allows it.

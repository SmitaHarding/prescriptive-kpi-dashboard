# evals/

The harness: scenarios with their expected answers, the checks, the runner and the
scorecard. So far: `check.py`, and known-bad inputs in `known_bad/`, one file per section of
02-requirements (from the Pass/fail requirements phase). Scenarios come in the Judgement and
data and Harness phases; the runner and scorecard in the Harness phase
([Phases and the builder](../method/decisions.md#phases-and-the-builder)).

**How it works.** Every requirement controls a named risk and will be proven by an eval
([Requirements and evals](../method/decisions.md#requirements-and-evals)). How cases are
ordered against the spike is set in Requirements and evals and
[Build-and-look spike](../method/decisions.md#build-and-look-spike). The model is scored
against the expected answer in each scenario, which the world data never contains
([Scenarios and the holdout](../method/decisions.md#scenarios-and-the-holdout),
[No answer in the world](../method/02-requirements.md#no-answer-in-the-world)).

**Refilling it.** PMO lead rejects and edits will be captured (to be built,
[What the prototype builds](../method/decisions.md#what-the-prototype-builds)). Turning them
into a separate set of test cases is designed, not built
([Overrides feed the tests](../method/decisions.md#overrides-feed-the-tests)).

**The year.** History, a scenario quarter used during the build, and a held-out quarter that
is sealed and run once after Build 4 ([The year](../method/decisions.md#the-year),
[Scenarios and the holdout](../method/decisions.md#scenarios-and-the-holdout),
[Holdout fingerprint check](../method/02-requirements.md#holdout-fingerprint-check)). The
safeguards (Freeze first, Holdout sealed, Blind scoring, Never fit the answer, Cost beside
accuracy) protect the comparison and the holdout.

**Case types** (starter list; the Judgement and data phase sets the final list and moves it
to the registers, [One home per fact](../method/decisions.md#one-home-per-fact)):

- happy path
- thin evidence: the tickets do not explain the change
- contradictory evidence: metrics and tickets disagree
- two causes at once
- recovery week: beyond the red threshold but improving
  ([Colour shows the level](../method/02-requirements.md#colour-shows-the-level))
- false-positive bait: month-end and quarter-end weeks
  ([Cycle weeks](../method/02-requirements.md#cycle-weeks))
- provisional week: a metric not yet final
  ([Provisional weeks](../method/02-requirements.md#provisional-weeks))
- capacity-infeasible week: no set of interventions fits the hours
  ([Weekly hours limit](../method/02-requirements.md#weekly-hours-limit))
- prompt injection inside ticket text ([Escaping](../method/02-requirements.md#escaping),
  [Injection resistance](../method/02-requirements.md#injection-resistance))
- misleading partner guess in the ticket text
  ([Ticket claims are claims](../method/02-requirements.md#ticket-claims-are-claims))
- unrecognised pattern
  ([Cause from the list, or human review](../method/02-requirements.md#cause-from-the-list-or-human-review))
- issue opened by hand before partners dispute
  ([Issues opened by hand](../method/02-requirements.md#issues-opened-by-hand))
- stalled issue ([Overdue issues](../method/02-requirements.md#overdue-issues))
- stuck invoice: one day either side of the stuck limit
  ([Stuck-invoice list](../method/02-requirements.md#stuck-invoice-list))
- SOP-breaking bait: tickets push for holding the payment run
  ([The playbook respects the SOP](../method/02-requirements.md#the-playbook-respects-the-sop))
- red week with no tickets
  ([Colour triggers nothing](../method/02-requirements.md#colour-triggers-nothing))

**`check.py`** is the traceability check. It runs without a model or network: `python
evals/check.py`. Its docstring lists what it checks.

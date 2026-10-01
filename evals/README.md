# evals/

The harness: the golden set, the constraint gates, the runner, the scorecard.

Requirements enter here as cases. A build is admitted by passing. Monitoring
refills it — every operator override in production becomes a candidate case.

Case types, each present deliberately:

- happy path
- thin evidence — the tickets do not explain the deterioration
- contradictory evidence — metrics and tickets disagree
- two causes at once
- recovery week — breaching but improving
- false-positive bait — month-end and quarterly cycles
- capacity-infeasible week — no set of interventions fits the available hours
- prompt injection attempt inside a ticket text

Held out and not looked at during development: the last quarter of dispute
tickets and 5 of the week-level scenarios (D41). Labels are applied cold,
by someone who did not write the case (D32).

`check.py` is the traceability check: `python evals/check.py`.

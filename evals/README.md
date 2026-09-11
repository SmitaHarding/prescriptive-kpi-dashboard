# evals/

The harness: the golden set, the constraint gates, the runner, the scorecard.

Requirements enter here as cases. A build is admitted by passing. Monitoring
refills it — every operator override in production becomes a candidate case.

Case types, each present deliberately:

- happy path
- thin evidence — the notes do not explain the deterioration
- contradictory evidence — metrics and notes disagree
- multiple co-present causes requiring attribution weighting
- recovery week — breaching but improving
- false-positive bait — month-end and quarterly billing cycles
- capacity-infeasible week — no intervention set fits the available hours
- prompt injection attempt inside the operational notes

One third of the set is held out and not looked at during development.
Labels are applied cold, by someone who did not author the case.

# data/

The world: the simulated operating history the system observes.

This folder contains **no answers**. A year of weekly metrics, dispute
tickets and issue events, all simulated (D31). Ticket texts read like real
partner messages and ticket descriptions — short, partial, sometimes wrong — and
never restate KPI values. Month-end and quarter-end weeks are marked, so
cycles can be told apart from issues (D50).

What the right answer was for any given week lives in `evals/`, deliberately
apart. v1's central mistake was seed data that carried its own answer key,
which made the reasoning layer look capable when it was paraphrasing.

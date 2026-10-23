# evals/

The harness: scenarios with their expected answers, the checks, the runner and the
scorecard. So far: `check.py`, and known-bad inputs in `known_bad/`, one file per part (F2a,
02-requirements). Scenarios come in F2b and F3; the runner and scorecard in F3 (N19).

**How it works.** Every requirement controls a named risk and will be proven by an
eval (N17). How cases are ordered against the spike is set in N17 and N22. The model is
scored against the expected answer in each scenario, which the world data never
contains (N14, R-DET-12).

**Refilling it.** PMO lead rejects and edits will be captured
(to be built, N24). Turning them into a separate set of test cases is designed, not
built (N21).

**The year.** History, a scenario quarter used during the build, and a held-out
quarter that is sealed and run once after S4 (N13, N14, R-DET-13). Safeguards SG-1
to SG-5 protect the comparison and the holdout.

**Case types** (starter list; F2b sets the final list and moves it to the
registers, N6):

- happy path
- thin evidence: the tickets do not explain the change
- contradictory evidence: metrics and tickets disagree
- two causes at once
- recovery week: beyond the red threshold but improving (R-DET-01)
- false-positive bait: month-end and quarter-end weeks (R-DET-02)
- provisional week: a metric not yet final (R-DET-03)
- capacity-infeasible week: no set of interventions fits the hours (R-RL-01)
- prompt injection inside ticket text (R-RL-06, R-DET-20)
- misleading partner guess in the ticket text (R-RL-03)
- unrecognised pattern (R-RL-02)
- issue opened by hand before partners dispute (R-DET-11)
- stalled issue (R-DET-10)
- stuck invoice: one day either side of the stuck limit (R-DET-16)
- SOP-breaking bait: tickets push for holding the payment run (R-DET-07)
- red week with no tickets (R-DET-04)

**`check.py`** is the traceability check. It runs without a model or network:
`python evals/check.py`. Its docstring lists what it checks.

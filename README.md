# Project Aegis

An AI-native operational governance agent for a large-scale B2B payments operation.
It detects SLA breaches and week-over-week deterioration, attributes them to
documented operational causes, and prescribes interventions ahead of the weekly
operating review.

**v1 shipped in June 2026 and was retired in September**, after an adversarial review
found twenty-one defects — chief among them a severity model with no concept of
trajectory, and a reasoning layer that prescribed interventions nobody had the capacity
to execute. **v2 is being rebuilt from the frame up** against a documented operating
model: the decision the system exists to improve, requirements written as executable
evaluations, and a harness the build must pass before it ships.

[**→ Live**](https://project-aegis-kpi.streamlit.app) · v1 preserved on the
[`archive/v1`](../../tree/archive/v1) branch

---

## Why the process is the point

In deterministic software you specify, build, then verify. That does not work where a
reasoning layer is involved: *"the interventions must be practical"* is not something
you can inspect in code review. So the evaluation case **is** the requirement — it is
also the acceptance test and the regression suite.

v1 demonstrates the cost of skipping that. Its PRD required a prompt prohibiting
speculative extrapolation. The prompt was never written, and nothing ever failed as a
result.

## Repository

| Path | Contents |
|------|----------|
| [`method/`](method/) | The operating model — one section per stage, written as the work proceeds |
| [`spec/`](spec/) | Requirements as failable statements: deterministic, red-line, judgement |
| [`data/`](data/) | The world — seed generator and operational notes, carrying no answers |
| [`evals/`](evals/) | The harness — golden set, constraint gates, runner, scorecard |
| [`prototype/`](prototype/) | v2 application code |

## Status

**Planning.** Six sessions — frame, value, requirements, dataset, golden set, harness —
precede any code. Each closes by committing a section of the operating model, so this
repository is the running record of decisions rather than a write-up produced at the end.

---

*Built with assistance from Claude.*

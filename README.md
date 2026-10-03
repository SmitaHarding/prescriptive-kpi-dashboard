# Project Aegis

An AI-assisted operational governance tool for a large-scale B2B payments operation.
Each Monday it shows which metrics are off target, groups new partner disputes into
possible issues, and drafts containment actions from a playbook — within the team's
real capacity, and only after the PMO lead has reviewed them. The AI spots patterns;
people confirm causes.

**v1 shipped in June 2026 and was retired in September**, after an adversarial review
raised twenty-one findings (the twelve structural defects are tracked in
[`spec/registers.toml`](spec/registers.toml)) — chief among them a severity model with
no concept of trajectory, and a reasoning layer that prescribed interventions nobody had
the capacity to execute. **v2 is being rebuilt from the frame up** against a documented
operating model: the decision the system exists to improve, requirements written as
executable evaluations, and a harness the build must pass before it ships.

[**→ Live**](https://project-aegis-kpi.streamlit.app) (holding page until v2) · v1 preserved on the
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
| [`method/`](method/) | The operating model — [decisions](method/decisions.md) and the [frame](method/01-frame.md) so far, one section per session |
| [`spec/`](spec/) | Requirements as failable statements, and the registers the checks read |
| [`data/`](data/) | The simulated world — weeks, dispute tickets and issues, carrying no answers |
| [`evals/`](evals/) | The harness — test cases, red-line gates, runner, scorecard; `check.py` runs today |
| [`prototype/`](prototype/) | v2 application code — empty until the harness exists |
| [`CLAUDE.md`](CLAUDE.md) | Standing rules for the AI build loop |

## Status

<!-- gen:status -->
**Stage:** F1 complete · **Next:** F2 — requirements, checks and dataset spec  
**Built so far:** nothing yet — the harness comes first
<!-- /gen:status -->

Eight sessions: three foundations (frame, requirements with their checks, harness),
four build slices, and a wrap-up. Each session closes by committing its section of the
operating model, so this repository is the running record of decisions rather than a
write-up produced at the end. The status line above is generated from
[`spec/registers.toml`](spec/registers.toml) by `evals/check.py`.

---

*Built with assistance from Claude.*

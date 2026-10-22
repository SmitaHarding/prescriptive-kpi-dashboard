# Project Aegis

An operational governance tool for a large-scale B2B payments operation, being
rebuilt. Each Monday, v2 will show which metrics are off target, group new dispute
tickets into possible issues, and draft interventions, mostly from a playbook,
within the team's real capacity. Drafts are shown only after the PMO lead has
reviewed them. Code or the
model proposes; people confirm causes.

**v1 shipped in June 2026 and was retired in September.** An adversarial review
found structural defects, now tracked in [`spec/registers.toml`](spec/registers.toml). Chief among them: a severity model
with no sense of trajectory, and interventions nobody had the capacity to carry
out. **v2 is being rebuilt from the frame up:** the decision it exists to improve,
requirements proven by evaluation cases, and a harness the build must pass before
it ships.

[**→ Live**](https://project-aegis-kpi.streamlit.app) (holding page until v2) · v1 preserved on the
[`archive/v1`](../../tree/archive/v1) branch

---

## Why the process is the point

In ordinary software you specify, build, then verify. That breaks down once a
model is involved: *"the interventions must be practical"* cannot be checked in
code review. So each requirement will be proven by evaluation cases, which also
serve as the acceptance test and the regression suite.

v1 shows the cost of skipping this. Its PRD required a prompt that forbade
speculative extrapolation. The prompt was never written, and nothing failed.

## Repository

| Path | Contents |
|------|----------|
| [`method/`](method/) | The operating model: [decisions](method/decisions.md), the [frame](method/01-frame.md) and the draft [requirements](method/02-requirements.md), built up phase by phase |
| [`spec/`](spec/) | The registers the checks read, and the data files for metrics, capacity and thresholds |
| [`data/`](data/) | The simulated world, designed in F2b and generated in F3. Empty today |
| [`evals/`](evals/) | The harness, built from F2a to F3. Today only the traceability check, `check.py` |
| [`prototype/`](prototype/) | v2 application code. Empty until the harness exists |
| [`CLAUDE.md`](CLAUDE.md) | Standing rules for Claude and the builder |

## Status

<!-- gen:status -->
**Stage:** F1 gate passed (pass with fixes); fixes applied · **Next:** F1 commit, then F2a — complete the pass/fail requirements and data files  
**Built so far:** no product code yet — the harness comes first
<!-- /gen:status -->

The phases: the frame; requirements with a clear pass or fail; a short private
spike to see how the model actually fails; judgement requirements and the dataset;
the harness; four build slices; a wrap-up (N19). The status line is generated from
[`spec/registers.toml`](spec/registers.toml) by `evals/check.py`.

---

*Built with assistance from Claude.*

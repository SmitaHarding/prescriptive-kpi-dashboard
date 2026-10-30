# method/

The operating model, built up phase by phase
([Method documents](decisions.md#method-documents)). Markdown, so it is version-controlled,
diffable and readable on GitHub; any Word or PDF pack is an export at the end.

| File | Section | Written in |
|------|---------|------------|
| [`decisions.md`](decisions.md) | Every choice, stated once; earlier codes map to names in `archive/code-map.md` | Frame, then as needed |
| [`01-frame.md`](01-frame.md) | The decision the system supports, the four Monday questions, roles, lifecycle, value | Frame; updated Pass/fail requirements |
| [`02-requirements.md`](02-requirements.md) | Every requirement, in three classes, each controlling a risk and with its check | Drafted Frame; Pass/fail requirements, Judgement and data |
| `03-dataset.md` | The simulated world: weeks, dispute tickets, issues, and why answers are kept apart | Judgement and data |
| `04-harness.md` | Generator, runner, scorecard, holdout | Harness |
| `00-overview.md` | How to read this, and the shape of the process | W |
| `05-release-monitor.md` | Replay, release staging, drift | W |
| `annex-v1-postmortem.md` | What v1 got wrong, and which risk and requirement now covers each defect | W |
| [`archive/`](archive/) | The earlier decisions log, kept word for word | Archived 22 Oct 2026 |

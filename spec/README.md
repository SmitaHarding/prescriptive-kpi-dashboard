# spec/

The registers and data files the checks read. Rules themselves are stated once, in
[`../method/02-requirements.md`](../method/02-requirements.md) (N6).

| File | Holds |
|---|---|
| [`registers.toml`](registers.toml) | IDs and links: decisions, risks, requirements, v1 defects, safeguards, terms; the status line |
| [`metrics.toml`](metrics.toml) | The metrics register: definitions, directions, targets and bands (targets and lower-is-better bands from F2a) |
| [`capacity.toml`](capacity.toml) | The capacity file: team, hours, effort per item, limits |
| [`thresholds.toml`](thresholds.toml) | Tunable limits: trend window, confidence minimum, comparison margin, drift and stage limits, cycle minimum |

The cause list (`causes.toml`) and playbook (`playbook.toml`) are added in F2a,
the generator settings (`generator.toml`) in F2b.
Charters for each build slice are added under `charters/` from S1 (N19).

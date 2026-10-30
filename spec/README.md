# spec/

The registers and data files the checks read. Rules themselves are stated once, in
[`../method/02-requirements.md`](../method/02-requirements.md)
([One home per fact](../method/decisions.md#one-home-per-fact)).

| File | Holds |
|---|---|
| [`registers.toml`](registers.toml) | Names and links: decisions, risks, requirements, v1 defects, safeguards, terms; the status line |
| [`metrics.toml`](metrics.toml) | The metrics register: definitions, directions, targets, bands and when each week is final |
| [`capacity.toml`](capacity.toml) | The capacity file: team, hours, effort per item, limits |
| [`causes.toml`](causes.toml) | The cause list: what each suspected cause means and what can support it |
| [`playbook.toml`](playbook.toml) | The playbook: intervention types and entries, by stage |
| [`thresholds.toml`](thresholds.toml) | Tunable limits: trend window, confidence minimum, comparison margin, drift and stage limits, cycle minimum |

The generator settings (`generator.toml`) are added in the Judgement and data phase.
Charters for each build slice are added under `charters/` from Build 1
([Phases and the builder](../method/decisions.md#phases-and-the-builder)).

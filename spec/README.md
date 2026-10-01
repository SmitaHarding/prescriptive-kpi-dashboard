# spec/

Requirements, written so that a case can fail them. If a statement cannot be
failed by a test, it belongs in `method/` as intent — not here.

Three classes, because each is verified by different means:

**Deterministic** — colours and trends, capacity, lifecycle exit criteria,
rendering, persistence. Ordinary unit tests. Bar: 100%, blocking.

**Red-line** — what must never happen. Recommendations exceeding available
capacity, working hours above the legal cap, numeric claims not derivable from
the input, unescaped model output reaching the DOM, high confidence alongside
populated evidence gaps. Checked programmatically against model output. Bar:
zero tolerance.

**Judgement** — is the attributed cause right, is the intervention
proportionate, is the register appropriate to the audience. Scored against a
rubric. Never 100%; tracked as a number per release.

`registers.toml` holds the IDs and links the traceability check reads
(decisions, v1 defects, safeguards). Decision wording lives only in
`method/decisions.md`.

# CLAUDE.md — standing rules for the build loop

Read `method/decisions.md` and `method/01-frame.md` first, then the session
handover in `_working/`, if present. Decisions are referenced by ID; do not
restate their numbers elsewhere (D22). Entries in the Superseded section of
`decisions.md` are history only; apply the decision that replaced them.

**Always**
- Say, before writing to a tracked folder, that the file will be public on GitHub.
  Private material goes to `_working/` (gitignored).
- Describe the domain only as a large-scale B2B payments operation. Never name
  the employer, internal tools or people (D14, D17).
- Run `python evals/check.py` before proposing a commit; it must be clean.
  End each commit message with the check.py result line.
- When a decision is added, changed or superseded, update every file it affects
  in the same change: `decisions.md`, `spec/registers.toml`, the method docs,
  the folder READMEs, `CLAUDE.md`, and the private handover and plan in
  `_working/`. Search for the old ID and its topic, not just the ID; list the
  files touched in the session summary. `check.py` catches stale IDs, not
  stale wording.
- Close every session with the routine: re-read changed docs; compare each
  decision added or changed in the session against every active decision, the
  frame and the safeguards (SG-01 to SG-11), and report "conflicts: none" or list
  them; update the handover.
- At every gate (end of each foundation and slice), a fresh agent with no project
  history reads all tracked docs and reports contradictions and stale wording.
  Findings are fixed or logged as open before the gate passes.

**During a build slice** (charter approved first — D21)
- Edit `prototype/` only, unless the charter names other paths (D21).
- Never edit a test, label or requirement to make something pass. A requirement
  change goes to the PMO lead and becomes a new D entry.
- Never read the holdout (D41, D47). Add no dependency without asking.
- A red-line failure is rejected, never silently repaired (D24).
- Use a new model version, prompt or playbook only after the full test set
  passes (D24).
- Stop and escalate at the iteration or spend cap, on the same failure twice,
  or when a fix would need a test or requirement change.

**Never**
- Push. Claude prepares commits; the owner pushes.
- Add a model call to the deployed app (D40).
- Rewrite git history, or force-push (D33).

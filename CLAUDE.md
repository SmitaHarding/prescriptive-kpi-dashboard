# CLAUDE.md — standing rules for the build loop

Read `method/decisions.md` and `method/01-frame.md` first. Decisions are
referenced by ID; do not restate their numbers elsewhere (D22).

**Always**
- Say, before writing to a tracked folder, that the file will be public on GitHub.
  Private material goes to `_working/` (gitignored).
- Describe the domain only as a large-scale B2B payments operation. Never name
  the employer, internal tools or people (D14, D17).
- Run `python evals/check.py` before proposing a commit; it must be clean.
- Close every session with the routine: re-read changed docs, compare the
  session's decisions against the safeguards (SG-01 to SG-11), update the handover.

**During a build slice** (charter approved first — D21)
- Edit `prototype/` only.
- Never edit a test, label or requirement to make something pass. A requirement
  change goes to the PMO lead and becomes a new D entry.
- Never read the holdout (D32, D41). Add no dependency without asking.
- A red-line failure is rejected, never silently repaired (D24).
- Stop and escalate at the iteration or spend cap, on the same failure twice,
  or when a fix would need a test or requirement change.

**Never**
- Push. Claude prepares commits; the owner pushes.
- Add a model call to the deployed app (D40).

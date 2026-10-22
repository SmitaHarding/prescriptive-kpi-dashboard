# CLAUDE.md — standing rules for this repository

Read `method/decisions.md`, then `method/02-requirements.md`, then
`method/01-frame.md`, then the private handover in `_working/`, if present.
Choices, rules and numbers each have one home (N6); cite their IDs and restate
nothing. `method/archive/` is history only.

Rules with an ID come from a decision or requirement. Rules marked *(practice)*
are working practice; the author agrees any change to them.

**Always**
- Before writing to a tracked folder, say the file will be public on GitHub.
  Private material goes to `_working/`, which is gitignored *(practice)*.
- Follow the privacy rule (N4).
- Use the preferred terms in `spec/registers.toml` (N6).
- Call nothing built unless the registers mark it built and its requirements pass
  (N6, R-DET-15).
- Run `python evals/check.py` before proposing a commit. It must be clean, and the
  commit message ends with its result line *(practice)*.
- When a decision or requirement changes, update every file it affects in the same
  change, including the private handover. Search for the topic as well as the ID:
  `check.py` catches stale IDs, not stale wording *(practice)*.
- Close each session by checking every changed decision or requirement against the
  others and the risk register; report "conflicts: none" or list them; update the
  handover *(practice)*.
- End each phase with a fresh-agent gate review (N19).

**During a build slice** (the builder, under an approved charter — N19)
- Edit only the paths the charter names.
- Never edit a test, expected answer or requirement to make something pass;
  escalate instead.
- Never read the held-out quarter or open its folder (N14).
- Handle a failing draft as R-DET-08 sets out. The red lines are R-RL-01 to
  R-RL-07.
- Follow the change gate (N18, R-DET-14).
- Stop and escalate in the cases N19 lists.
- Add no dependency without asking the author *(practice)*.

**During the spike** (N22)
- Keep everything in `_working/spike/`; commit nothing from it, and score nothing.

**Never**
- Push. The author pushes (N19).
- Add a model call to the public app (N11).
- Rewrite git history or force-push (N2).

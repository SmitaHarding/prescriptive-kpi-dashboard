# CLAUDE.md — standing rules for this repository

Read `method/decisions.md`, then `method/02-requirements.md`, then `method/01-frame.md`,
then the private handover in `_working/`, if present. Choices, requirements and numbers each
have one home ([One home per fact](method/decisions.md#one-home-per-fact)); cite them by
name ([Names, not codes](method/decisions.md#names-not-codes)) and restate nothing.
`method/archive/` is history only.

Rules that cite a decision or requirement come from it. Rules marked *(practice)* are
working practice; the author agrees any change to them.

**Always**
- Before writing to a tracked folder, say the file will be public on GitHub. Private
  material goes to `_working/`, which is gitignored *(practice)*.
- Follow the privacy rule ([Privacy](method/decisions.md#privacy)).
- Use the preferred terms in `spec/registers.toml`
  ([One home per fact](method/decisions.md#one-home-per-fact)).
- Call nothing built unless the registers mark it built and its requirements pass
  ([One home per fact](method/decisions.md#one-home-per-fact),
  [Documents match what exists](method/02-requirements.md#documents-match-what-exists)).
- Run `python evals/check.py` before proposing a commit. It must be clean, and the commit
  message ends with its result line *(practice)*.
- When a decision or requirement changes, update every file it affects in the same change,
  including the private handover. Search for the topic as well as the name: `check.py`
  catches stale names, not stale wording *(practice)*.
- Close each session by checking every changed decision or requirement against the others
  and the risk register; report "conflicts: none" or list them; update the handover
  *(practice)*.
- End each phase with a fresh-agent gate review
  ([Phases and the builder](method/decisions.md#phases-and-the-builder)).

**During a build slice** (the builder, under an approved charter —
[Phases and the builder](method/decisions.md#phases-and-the-builder))
- Edit only the paths the charter names.
- Never edit a test, expected answer or requirement to make something pass; escalate
  instead.
- Never read the held-out quarter or open its folder
  ([Scenarios and the holdout](method/decisions.md#scenarios-and-the-holdout)).
- Handle a failing draft as
  [Failed checks are never repaired](method/02-requirements.md#failed-checks-are-never-repaired)
  sets out. The red lines are listed in
  [`method/02-requirements.md`](method/02-requirements.md#red-lines).
- Follow the change gate ([Change control](method/decisions.md#change-control),
  [Change gate](method/02-requirements.md#change-gate)).
- Stop and escalate in the cases
  [Phases and the builder](method/decisions.md#phases-and-the-builder) lists.
- Add no dependency without asking the author *(practice)*.

**During the spike** ([Build-and-look spike](method/decisions.md#build-and-look-spike))
- Keep everything in `_working/spike/`; commit nothing from it, and score nothing.

**Never**
- Push. The author pushes
  ([Phases and the builder](method/decisions.md#phases-and-the-builder)).
- Add a model call to the public app
  ([Records and replay](method/decisions.md#records-and-replay)).
- Rewrite git history or force-push
  ([Repo and deployment](method/decisions.md#repo-and-deployment)).

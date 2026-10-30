# Code map

History, not scanned by `check.py`. From 30 Oct 2026 everything is cited by name ([Names, not codes](../decisions.md#names-not-codes)). Older files, commit messages and gate reports use the codes below.

## Decisions (N)

| Code | Name |
|---|---|
| N1 | Scope |
| N2 | Repo and deployment |
| N3 | Public face |
| N4 | Privacy |
| N5 | Method documents (superseded by N25) |
| N6 | One home per fact (superseded by N26) |
| N7 | Assumptions |
| N8 | The Monday decision (superseded by N27) |
| N9 | Issue lifecycle (superseded by N23) |
| N10 | What the prototype builds (superseded by N32) |
| N11 | Records and replay |
| N12 | Simulated world |
| N13 | The year (superseded by N28) |
| N14 | Scenarios and the holdout (superseded by N29) |
| N15 | Model against rules |
| N16 | Value measures |
| N17 | Requirements and evals (superseded by N30) |
| N18 | Change control |
| N19 | Phases and the builder |
| N20 | No outside validation |
| N21 | Overrides feed the tests (superseded by N31) |
| N22 | Build-and-look spike |
| N23 | Issue lifecycle |
| N24 | What the prototype builds (superseded by N32) |
| N25 | Method documents |
| N26 | One home per fact |
| N27 | The Monday decision |
| N28 | The year |
| N29 | Scenarios and the holdout |
| N30 | Requirements and evals |
| N31 | Overrides feed the tests |
| N32 | What the prototype builds |
| N33 | Names, not codes |

## Requirements (R-DET pass/fail, R-RL red line, R-JDG judgement)

| Code | Name |
|---|---|
| R-DET-01 | Colour shows the level |
| R-DET-02 | Cycle weeks |
| R-DET-03 | Provisional weeks |
| R-DET-04 | Colour triggers nothing |
| R-DET-05 | Capacity check |
| R-DET-06 | Coverage without padding |
| R-DET-07 | The playbook respects the SOP |
| R-DET-08 | Failed checks are never repaired |
| R-DET-09 | Append-only record |
| R-DET-10 | Overdue issues |
| R-DET-11 | Issues opened by hand |
| R-DET-12 | No answer in the world |
| R-DET-13 | Holdout fingerprint check |
| R-DET-14 | Change gate |
| R-DET-15 | Documents match what exists |
| R-DET-16 | Stuck-invoice list |
| R-DET-17 | Read-only public app |
| R-DET-18 | Measuring value |
| R-DET-19 | Two views, one record |
| R-DET-20 | Injection resistance |
| R-DET-21 | Nothing private in tracked files |
| R-DET-22 | Simulated is labelled |
| R-JDG-01 | Detection against rules |
| R-JDG-02 | Calibration |
| R-JDG-03 | Practical and proportionate |
| R-RL-01 | Weekly hours limit |
| R-RL-02 | Cause from the list, or human review |
| R-RL-03 | Ticket claims are claims |
| R-RL-04 | Confidence is measured |
| R-RL-05 | No invented figures or dates |
| R-RL-06 | Escaping |
| R-RL-07 | Review before anything is shown |

## Risks (RK)

| Code | Name |
|---|---|
| RK-01 | False alarm |
| RK-02 | Missed or late issue |
| RK-03 | Wrong cause |
| RK-04 | Overconfidence |
| RK-05 | Infeasible plan |
| RK-06 | Padding |
| RK-07 | Invented figures |
| RK-08 | Unsafe text |
| RK-09 | Unreviewed output |
| RK-10 | No trail |
| RK-11 | Stalled issue |
| RK-12 | Breaks the SOP |
| RK-13 | Leaky test |
| RK-14 | Overfitting |
| RK-15 | Model not earning its place |
| RK-16 | Drift |
| RK-17 | Docs overclaim or contradict |
| RK-18 | Missed stuck invoice |
| RK-19 | Views disagree |
| RK-20 | Privacy leak |

## Safeguards (SG)

| Code | Name |
|---|---|
| SG-1 | Freeze first |
| SG-2 | Holdout sealed |
| SG-3 | Blind scoring |
| SG-4 | Never fit the answer |
| SG-5 | Cost beside accuracy |

## Monday questions (DEC)

| Code | Name |
|---|---|
| DEC-1 | Off target? |
| DEC-2 | Possible issues? |
| DEC-3 | Which interventions? |
| DEC-4 | Enough capacity? |

## Phases

| Code | Name |
|---|---|
| F1 | Frame |
| F2a | Pass/fail requirements |
| F2b | Judgement and data |
| F3 | Harness |
| S1 | Build 1 |
| S2 | Build 2 |
| S3 | Build 3 |
| S4 | Build 4 |
| W | Wrap-up |

## Checks in `check.py`

| Number | Name |
|---|---|
| 1 | well-formed names |
| 2 | decisions match |
| 3 | requirements match |
| 4 | links resolve |
| 5 | coverage |
| 6 | citations |
| 7 | archive chain |
| 8 | status block |
| 9 | terms |
| 10 | numbers |
| 11 | mirrors |
| 12 | known-bad |
| 13 | citations |
| 14 | assumption labels |
| 15 | validation mentions |
| 16 | privacy |
| 17 | decision links |

## The decision log before 22 Oct 2026 (D1–D93, SG-01–SG-11)

Full wording: [`decisions-2026-10-21.md`](decisions-2026-10-21.md). "Then" is where each went on 26 Oct; "Now" gives the names.

| Earlier | Title | Then | Now |
|---|---|---|---|
| D1 | Full rebuild | N1 | Scope |
| D2 | Front door | N1 | Scope |
| D3 | Dataset | N12 | Simulated world |
| D4 | v1 kept | N2 | Repo and deployment |
| D5 | Where v2 lives | N2 | Repo and deployment |
| D6 | README | N3 | Public face |
| D7 | Streamlit app | N2 | Repo and deployment |
| D8 | Requirement classes | N30; red-line list now in 02-requirements.md | Requirements and evals; red-line list now in 02-requirements.md |
| D9 | Answer key kept apart | N29 | Scenarios and the holdout |
| D10 | Labels are applied cold by someone who did not write the case; one third is held out and not looked at during the build (already superseded) | N29 | Scenarios and the holdout |
| D11 | Operating model | N25 | Method documents |
| D12 | Baselines | N7 | Assumptions |
| D13 | Value metric: interventions actioned within the week (already superseded) | N16 | Value measures |
| D14 | Domain | N4 | Privacy |
| D15 | Clean main | N2 | Repo and deployment |
| D16 | Holding page | N3 | Public face |
| D17 | Private documents | N4 | Privacy |
| D18 | Format | N25 | Method documents |
| D19 | Entry point | N2 | Repo and deployment |
| D20 | Slices | N30 | Requirements and evals |
| D21 | Charter | N19 | Phases and the builder |
| D22 | Document checks | N26 | One home per fact |
| D23 | Requirements, checks, data | N30; outside validation dropped (N20) | Requirements and evals; outside validation dropped (No outside validation) |
| D24 | Model drafts | N18 | Change control |
| D25 | Roles and views | N27 | The Monday decision |
| D26 | Colour rule | R-DET-01; bands in the metrics register | Colour shows the level; bands in the metrics register |
| D27 | Capacity (already superseded) | R-DET-05, R-RL-01; figures in the capacity file | Capacity check, Weekly hours limit; figures in the capacity file |
| D28 | Interventions and the record | R-DET-06, R-DET-09, R-RL-07; N31 | Coverage without padding, Append-only record, Review before anything is shown; Overrides feed the tests |
| D29 | Playbook | R-DET-07; playbook format in 02-requirements.md | The playbook respects the SOP; playbook format in 02-requirements.md |
| D30 | Confidence and gaps | R-RL-04, R-DET-08 | Confidence is measured, Failed checks are never repaired |
| D31 | Simulated data | N12; metrics register | Simulated world; metrics register |
| D32 | Test cases are written by Claude, except the holdout, which a separate agent writes (already superseded) | N29 | Scenarios and the holdout |
| D33 | Git history | N2 | Repo and deployment |
| D34 | Model against rules | N15 | Model against rules |
| D35 | Issue lifecycle | N23, R-DET-03 | Issue lifecycle, Provisional weeks |
| D36 | Framing and slices | N27, N19 | The Monday decision, Phases and the builder |
| D37 | Value measures | N16 | Value measures |
| D38 | Prototype scope | N32 | What the prototype builds |
| D39 | Records and replay | N11 | Records and replay |
| D40 | No AI calls in public | N11 | Records and replay |
| D41 | Holdout (already superseded) | N28 | The year |
| D42 | README status | N3 | Public face |
| D43 | Document checks are phased in: no copied facts from F1, generated blocks and review stamps from F3, the claims check from S1 (already superseded) | N26 | One home per fact |
| D44 | Phasing | N19 | Phases and the builder |
| D45 | Stalled issues | R-DET-10 | Overdue issues |
| D46 | Overtime | R-DET-05 | Capacity check |
| D47 | Labelling and holdout: test cases are written by Claude, except the holdout, which a separate agent writes (already superseded) | N29 | Scenarios and the holdout |
| D48 | Capacity | R-DET-05, R-RL-01 (now runs every week); figures in the capacity file | Capacity check, Weekly hours limit (now runs every week); figures in the capacity file |
| D49 | Measured confidence | R-RL-04, R-JDG-02 | Confidence is measured, Calibration |
| D50 | Month-end and quarter-end | R-DET-02 | Cycle weeks |
| D51 | Colour is the level | R-DET-01 | Colour shows the level |
| D52 | Colour triggers nothing | R-DET-04, R-DET-11; N16 | Colour triggers nothing, Issues opened by hand; Value measures |
| D53 | No numbers from the model | R-RL-05 | No invented figures or dates |
| D54 | No impact forecast | R-RL-05 | No invented figures or dates |
| D55 | Ticket text | N12, R-DET-12 | Simulated world, No answer in the world |
| D56 | Claims in tickets | R-RL-03 | Ticket claims are claims |
| D57 | Derived figures | R-RL-04 | Confidence is measured |
| D58 | Escaping | R-RL-06 | Escaping |
| D59 | One home for rules | N26 | One home per fact |
| D60 | Planned or built | N26 | One home per fact |
| D61 | Terms | N26; terms in the registers | One home per fact; terms in the registers |
| D62 | Measures are simulated | N32, N16 | What the prototype builds, Value measures |
| D63 | The year | N28, N11 | The year, Records and replay |
| D64 | Unrecognised patterns | R-RL-02 | Cause from the list, or human review |
| D65 | Two labellers | N29 (one reviewer agent replaces two labellers) | Scenarios and the holdout (one reviewer agent replaces two labellers) |
| D66 | Sealing the held-out quarter | N29 | Scenarios and the holdout |
| D67 | Quarter boundary | N28 | The year |
| D68 | Failed checks | R-DET-08 | Failed checks are never repaired |
| D69 | Cause list | R-RL-02; cause list format in 02-requirements.md | Cause from the list, or human review; cause list format in 02-requirements.md |
| D70 | Metrics register | R-DET-01; metrics register format in 02-requirements.md | Colour shows the level; metrics register format in 02-requirements.md |
| D71 | Assumptions | N7 | Assumptions |
| D72 | Issues opened by hand | R-DET-11 | Issues opened by hand |
| D73 | Where the model stops | N23 | Issue lifecycle |
| D74 | Year-end | R-DET-02, N28 | Cycle weeks, The year |
| D75 | Due week | R-RL-05 | No invented figures or dates |
| D76 | Labelling the held-out quarter | N29 (author's blind labelling of the holdout dropped) | Scenarios and the holdout (author's blind labelling of the holdout dropped) |
| D77 | Phases and gates | N19 | Phases and the builder |
| D78 | Labelling guide | N29 (dropped with the two labellers) | Scenarios and the holdout (dropped with the two labellers) |
| D79 | Full test set | N18 | Change control |
| D80 | Rules and data files | N26 | One home per fact |
| D81 | What each phase adds | N25 | Method documents |
| D82 | No outside validation | N20 | No outside validation |
| D83 | Answer sheet | N29, SG-4 | Scenarios and the holdout, Never fit the answer |
| D84 | Red lines | Red lines R-RL-01 to R-RL-07 | The Red lines list in 02-requirements.md |
| D85 | Builder limits | N19 | Phases and the builder |
| D86 | Charter contents | N19 | Phases and the builder |
| D87 | Privacy | N4 | Privacy |
| D88 | Definitions | Glossary in the registers; N12, N15 | Glossary in the registers; Simulated world, Model against rules |
| D89 | Holdout | N28, N29 | The year, Scenarios and the holdout |
| D90 | Labelling | N29 | Scenarios and the holdout |
| D91 | Overrides as candidate cases | N31 | Overrides feed the tests |
| D92 | Rules baseline roles | N15 | Model against rules |
| D93 | Weekly order | N27 | The Monday decision |
| SG-01 | Rules baseline written by the PMO lead and frozen by the author before any scoring | SG-1 | Freeze first |
| SG-02 | Both versions also scored on the held-out quarter, once, after S4 | SG-2 | Holdout sealed |
| SG-03 | Blind, shuffled scoring wherever a person judges | SG-3 | Blind scoring |
| SG-04 | Case mix fixed before any results; results reported per case type | SG-1 | Freeze first |
| SG-05 | Margin set before results, calibrated once from run-to-run variation | SG-1 (calibration from run-to-run variation dropped; the margin is set in F3) | Freeze first (calibration from run-to-run variation dropped; the margin is set in Harness) |
| SG-06 | Model cost shown alongside accuracy | SG-5 | Cost beside accuracy |
| SG-07 | Spot-check a sample of the labels both labellers agreed on | Dropped with the two labellers (N29) | Dropped with the two labellers (Scenarios and the holdout) |
| SG-08 | Holdout written by a separate agent and sealed from the build | SG-2 | Holdout sealed |
| SG-09 | 'The case is flawed' is an allowed outcome; labels never changed to fit | SG-4 | Never fit the answer |
| SG-10 | Judgement labels are acceptable options plus rubric points | SG-1 | Freeze first |
| SG-11 | Disagreements answered before seeing the two labels | Dropped with the two labellers (N29) | Dropped with the two labellers (Scenarios and the holdout) |

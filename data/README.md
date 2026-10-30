# data/

The simulated operating history the system observes. **Empty today.** The dataset is
designed in the Judgement and data phase and generated in the Harness phase.

It will hold the history and scenario quarters
([The year](../method/decisions.md#the-year)): weekly metrics and dispute tickets, all
simulated ([Simulated world](../method/decisions.md#simulated-world)), and **no answers**.
The held-out quarter stays sealed outside the project until its single run
([Scenarios and the holdout](../method/decisions.md#scenarios-and-the-holdout)). Ticket
texts will read like real partner messages: short, partial, sometimes wrong, never restating
metric values
([No answer in the world](../method/02-requirements.md#no-answer-in-the-world)). Month-end
and quarter-end weeks will be marked, so cycles can be told apart from issues
([Cycle weeks](../method/02-requirements.md#cycle-weeks)).

The expected answer for each scenario lives in its definition, kept apart
([Scenarios and the holdout](../method/decisions.md#scenarios-and-the-holdout)). One of v1's
mistakes was seed data that carried its own answer key, which made the reasoning layer look
capable when it was paraphrasing.

# data/

The simulated operating history the system observes. **Empty today.** The dataset
is designed in F2b and generated in F3.

It will hold the history and scenario quarters (N28): weekly metrics and dispute
tickets, all simulated (N12), and **no answers**. The held-out quarter stays sealed outside
the project until its single run (N29). Ticket texts will read like real partner
messages: short, partial, sometimes wrong, never restating metric values
(R-DET-12). Month-end and quarter-end weeks will be marked, so cycles can be told
apart from issues (R-DET-02).

The expected answer for each scenario lives in its definition, kept apart (N29). One of v1's mistakes was seed data that carried its own answer key, which
made the reasoning layer look capable when it was paraphrasing.

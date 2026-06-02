"""
demo_responses.py
=================
Pre-generated AI governance briefings for all flagged weeks.

Used when DEMO_MODE=true to serve realistic responses without making live
Claude API calls — eliminating per-visitor API costs on the public deployment.

Structure:
    DEMO_RESPONSES[week_number] = {
        "cos": { ...Executive Copilot response... },
        "cia": { ...Operations Copilot response... },
    }

Each response matches the JSON schema returned by ai_agent.py:
    {
        "week_label":          str,
        "severity":            "CRITICAL" | "WARNING",
        "executive_summary":   str,
        "interventions": [
            {"title": str, "rationale": str, "action": str, "expected_impact": str},
            ...  (exactly 3)
        ],
        "risk_if_unaddressed": str,
    }
"""

DEMO_RESPONSES = {

    # ── W07 — Early warning: junior cover + new client volume ─────────────────
    7: {
        "cos": {
            "week_label": "2025-W07",
            "severity": "WARNING",
            "executive_summary": (
                "Week W07 shows early-stage deterioration driven by planned leave and a new client "
                "onboarding occurring in the same week. Manual processing hours climbed 24 hours "
                "week-on-week to 156 hours — still within SLA but the fastest single-week escalation "
                "this quarter. The first SLA breach of the quarter has occurred, with one invoice "
                "missing the contractual 7-day payment window. First-pass resolution has dipped below "
                "the 95% SLA to 94.8%, attributable to reduced senior processing coverage "
                "during a period of concurrent planned leave."
            ),
            "interventions": [
                {
                    "title": "Restrict concurrent leave during active client onboarding periods",
                    "rationale": (
                        "The co-occurrence of two senior processors on leave during a new client "
                        "go-live created a capacity gap that reduced senior coverage could not "
                        "fully absorb. This is a governance oversight in leave planning."
                    ),
                    "action": (
                        "Director of Operations to mandate a minimum coverage rule: no more than one "
                        "senior processor absent at any time during active client onboarding periods. "
                        "Policy to be documented and enforced from the following week."
                    ),
                    "expected_impact": (
                        "Prevents recurrence of first-pass resolution dips and manual hour spikes "
                        "caused by simultaneous senior staff absence during critical operational periods."
                    ),
                },
                {
                    "title": "Resolve the new client invoice template mismatch this week",
                    "rationale": (
                        "The new logistics client's invoice format is generating exceptions that "
                        "the format mismatch is generating exceptions that require escalation to "
                        "resolve, increasing cycle time and manual processing effort."
                    ),
                    "action": (
                        "Operations Lead to review the new client's invoice template against the "
                        "standard validation ruleset by end of week. Flag any non-standard fields "
                        "to the client's accounts contact and request correction before the next "
                        "billing cycle."
                    ),
                    "expected_impact": (
                        "Reduces exception rate and manual hours attributable to the new client "
                        "from the following week onwards, preventing a recurring source of overhead."
                    ),
                },
                {
                    "title": "Brief VP Operations on the SLA breach with context and remediation trail",
                    "rationale": (
                        "With one SLA breach on record for the first time this quarter, the VP "
                        "Operations governance log requires an update. Proactive escalation is "
                        "preferable to retrospective explanation."
                    ),
                    "action": (
                        "Chief of Staff to include a one-paragraph briefing in the Monday governance "
                        "update: one SLA breach, cause confirmed as temporary coverage gap, corrective "
                        "actions in place. No further escalation required unless breach count increases."
                    ),
                    "expected_impact": (
                        "SLA breach is contextualised and documented with a clear remediation trail "
                        "before the weekly executive review, reducing reputational exposure."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "If leave planning is not tightened and the new client exception pattern is not "
                "resolved, the combination of reduced senior capacity and growing exception volume "
                "will push processing hours and SLA breach counts materially higher in the "
                "following weeks."
            ),
        },
        "cia": {
            "week_label": "2025-W07",
            "severity": "WARNING",
            "executive_summary": (
                "The week's deterioration has two identifiable process causes: reduced senior "
                "processing coverage due to concurrent planned leave, and a new logistics client "
                "introducing invoice formats that are generating higher exception flags than standard "
                "templates. Neither cause is structural, but both will worsen if not addressed before "
                "full team capacity is restored. Manual processing hours reached 156 hours — 24 hours "
                "higher than the prior week — driven by the exception-heavy new client volume and "
                "the additional handling steps required for non-standard invoice formats."
            ),
            "interventions": [
                {
                    "title": "Document new client exception patterns before senior processors return",
                    "rationale": (
                        "Without a documented exception log, the team returning from leave will "
                        "need to re-triage the same issues from scratch. Capturing exception types "
                        "now creates a reusable playbook that reduces handling time going forward."
                    ),
                    "action": (
                        "Operations team lead to maintain a running exception log for the new client "
                        "this week: exception type, cause, and resolution step for each flagged "
                        "invoice. Share with the full team at Monday's handover."
                    ),
                    "expected_impact": (
                        "Reduces time-per-invoice for the new client by eliminating repeated "
                        "re-learning, and cuts the exception rate toward baseline within two weeks."
                    ),
                },
                {
                    "title": "Escalate the invoice template mismatch to the new client this week",
                    "rationale": (
                        "If the client's invoice format is generating non-standard exceptions, the "
                        "source of friction should be resolved at origin rather than absorbed by the "
                        "processing team each week."
                    ),
                    "action": (
                        "Operations team lead to contact the new client's accounts payable contact "
                        "by end of week. Share the specific exception fields causing validation "
                        "failures and request a template correction before the next billing cycle."
                    ),
                    "expected_impact": (
                        "Reduces new-client exception volume at source. First-pass resolution rate "
                        "recovers toward SLA once the template is corrected."
                    ),
                },
                {
                    "title": "Clear the single SLA-breached invoice before close of business today",
                    "rationale": (
                        "One invoice has missed the 7-day contractual payment window. The obligation "
                        "remains outstanding and compounds reputational risk with the affected "
                        "logistics partner for every additional day it remains unpaid."
                    ),
                    "action": (
                        "Processing team lead to identify and personally clear the SLA-breached "
                        "invoice today. Confirm payment release and notify the affected logistics "
                        "company with an apology and confirmation of corrected payment."
                    ),
                    "expected_impact": (
                        "Breach invoice is resolved within the week. Relationship with the affected "
                        "logistics partner is preserved and no formal dispute is raised."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "If the new client exception pattern is not resolved before senior processors return, "
                "the exception backlog will accumulate and manual hours will continue to rise, pushing "
                "the processing team toward capacity limits in W08."
            ),
        },
    },

    # ── W08 — CRITICAL: ERP upgrade failure ───────────────────────────────────
    8: {
        "cos": {
            "week_label": "2025-W08",
            "severity": "CRITICAL",
            "executive_summary": (
                "Week W08 represents the most severe operational failure on record. An ERP upgrade "
                "defect mis-routed approximately 140 invoices, triggering a cascade across every "
                "monitored metric. Six invoices have breached the contractual 7-day payment deadline — "
                "each a formal contractual default — and 150 logistics partners have raised formal "
                "disputes against incorrect payment amounts. Payment accuracy has fallen to 93.1%, the "
                "lowest recorded, and manual processing hours have reached 427 hours — more than double "
                "the 200-hour SLA — as three teams work to identify, reroute, and correct affected invoices."
            ),
            "interventions": [
                {
                    "title": "Activate P1 incident governance with VP Operations and Director of Technology",
                    "rationale": (
                        "Six contractual defaults and 150 active disputes represent material financial "
                        "and reputational exposure. This incident requires VP-level governance, not "
                        "operational management alone. Incident ticket #INC-2024-0892 is already raised."
                    ),
                    "action": (
                        "VP Operations to convene an incident review with Director of Technology and "
                        "Director of Operations by Wednesday. Incident elevated to P1. Written resolution "
                        "commitment to all affected logistics partners to be issued within 48 hours."
                    ),
                    "expected_impact": (
                        "Contractual exposure is formally managed at the appropriate level. Partners "
                        "receive timely communication, and the organisation demonstrates governance-level "
                        "accountability for the failure."
                    ),
                },
                {
                    "title": "Secure and validate vendor patch deployment before the next invoice cycle",
                    "rationale": (
                        "The ERP routing defect remains the root cause of all downstream failures. "
                        "Until the vendor patch is deployed and the custom routing configuration "
                        "restored, new invoices will continue to mis-route."
                    ),
                    "action": (
                        "Director of Technology to secure a vendor patch commitment with a deadline "
                        "no later than end of business Thursday. IT team to test the patch in a "
                        "non-production environment against the full multi-currency routing ruleset "
                        "before deploying to production. Written sign-off required before go-live."
                    ),
                    "expected_impact": (
                        "New invoices processed from Friday onwards route correctly, halting the "
                        "accumulation of additional exceptions, breaches, and disputes."
                    ),
                },
                {
                    "title": "Authorise structured overtime and temporary resource reallocation",
                    "rationale": (
                        "At 427 manual processing hours with only two senior processors available, "
                        "the team cannot clear the backlog without additional resource. ArbZG "
                        "compliance requires any overtime to be formally authorised within legal "
                        "daily hour limits."
                    ),
                    "action": (
                        "Director of Operations to authorise a structured overtime programme: maximum "
                        "10 hours per processor per day, formal written authorisation. Assign a "
                        "temporary resource from another operations team to triage the dispute "
                        "correspondence queue this week and next."
                    ),
                    "expected_impact": (
                        "Backlog clearance accelerates by an estimated 30-40%, reducing stuck invoice "
                        "count and dispute response time in the following two weeks."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "If the vendor patch is not deployed and authorised resource is not allocated this "
                "week, the backlog will continue to compound, formal disputes will escalate into "
                "contractual claims, and the reputational damage to logistics partner relationships "
                "will take significantly longer to recover."
            ),
        },
        "cia": {
            "week_label": "2025-W08",
            "severity": "CRITICAL",
            "executive_summary": (
                "The root cause of this week's failures is a single ERP configuration defect: the "
                "upgrade deployed Monday morning overwrote the custom multi-currency invoice routing "
                "ruleset in place since 2023. Approximately 140 invoices routed to the wrong approval "
                "queue and sat unprocessed for multiple days before the mis-routing was identified. "
                "All downstream failures — payment errors, stuck invoices, formal disputes — trace "
                "back to this single change. Without the vendor patch, new invoices entering the "
                "system will continue to mis-route alongside the existing backlog."
            ),
            "interventions": [
                {
                    "title": "Triage and manually reroute all 127 stuck invoices by priority this week",
                    "rationale": (
                        "Each stuck invoice is an unprocessed invoice. Clearing the stuck queue is "
                        "the single highest-impact action available this week — it stops SLA breaches "
                        "accumulating and reduces the dispute pipeline."
                    ),
                    "action": (
                        "Senior processors to triage the full stuck queue by priority: SLA-breached "
                        "invoices first, then those within 24 hours of the 7-day deadline. Each invoice "
                        "to be manually rerouted to the correct approval queue and processed before "
                        "end of business Friday. Team lead to track progress hourly."
                    ),
                    "expected_impact": (
                        "Stuck invoice count falls from 127 toward single digits by end of W09 as the "
                        "backlog is cleared. SLA breach count stops increasing."
                    ),
                },
                {
                    "title": "Establish a daily dispute triage to resolve 30 cases per day",
                    "rationale": (
                        "150 active disputes represent 150 logistics partners who received incorrect "
                        "payment amounts. Each unresolved case risks formal contractual claims and "
                        "damages ongoing partner relationships."
                    ),
                    "action": (
                        "Dispute resolution team to implement a daily morning triage: sort disputes "
                        "by financial value, prioritise the top 20 by value for same-day resolution. "
                        "Each requires a correction notice, revised payment, and confirmation email "
                        "to the logistics partner. Target: 30 disputes resolved per day."
                    ),
                    "expected_impact": (
                        "Dispute resolution rate recovers from 61.4% toward 80%+ within two weeks "
                        "as the highest-value disputes are cleared first."
                    ),
                },
                {
                    "title": "Version-control and protect the routing configuration after patch deployment",
                    "rationale": (
                        "The configuration overwritten had been in place since 2023 and was not "
                        "version-controlled. Without documentation, the same defect could recur on "
                        "the next upgrade cycle."
                    ),
                    "action": (
                        "IT team to export and version-control the full routing configuration after "
                        "the vendor patch restores it. Add configuration documentation to the change "
                        "management register. Create and mandate a pre-deployment configuration "
                        "validation checklist for all future ERP upgrade cycles."
                    ),
                    "expected_impact": (
                        "Prevents recurrence of the same defect. Reduces the risk of configuration "
                        "loss from future upgrades from certain to near-zero."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "Without clearing the stuck invoice queue and resolving active disputes this week, "
                "the backlog will continue generating new exception flags, manual hours will remain "
                "above 400 hours into W09, and formal dispute claims will escalate beyond the "
                "operations team's capacity to manage."
            ),
        },
    },

    # ── W09 — CRITICAL: ERP recovery underway ─────────────────────────────────
    9: {
        "cos": {
            "week_label": "2025-W09",
            "severity": "CRITICAL",
            "executive_summary": (
                "Recovery from the ERP incident is underway but incomplete. Manual processing hours "
                "remain critically elevated at 332 hours as the team works through the inherited "
                "exception and dispute backlog. Four invoices breached the contractual deadline this "
                "week, bringing the two-week cumulative total to ten contractual defaults. The dispute "
                "backlog has partially reduced from 150 to 113 active cases, but the 72.3% dispute "
                "resolution rate remains critically below the 90% SLA. The vendor patch was deployed "
                "Thursday and automated routing is now restored for new invoices."
            ),
            "interventions": [
                {
                    "title": "Report two-week cumulative SLA breach exposure to the board",
                    "rationale": (
                        "Ten contractual defaults across two consecutive weeks constitutes a pattern. "
                        "The VP Operations governance log must reflect this, and the board should be "
                        "briefed before a logistics partner formally escalates."
                    ),
                    "action": (
                        "Chief of Staff to prepare a one-page board briefing note by Monday: incident "
                        "cause, two-week breach count, recovery trajectory, and expected week of full "
                        "SLA restoration. VP Operations to distribute to the audit committee chair "
                        "before the end-of-month board meeting."
                    ),
                    "expected_impact": (
                        "Board is proactively informed, reducing reputational risk if a logistics "
                        "partner escalates. Recovery governance is formally on record."
                    ),
                },
                {
                    "title": "Set a formal target week for return to 97% payment accuracy",
                    "rationale": (
                        "Payment accuracy at 94.8% means approximately one in nineteen invoices "
                        "processed this week carried a payment error. Without a specific target, "
                        "recovery tracking is informal and may drift."
                    ),
                    "action": (
                        "Director of Operations to establish a formal recovery tracker with a target "
                        "of payment accuracy above 97% by week W11. Weekly progress reported at "
                        "the Monday governance review with red/amber/green status."
                    ),
                    "expected_impact": (
                        "Recovery has a defined endpoint and clear accountability, reducing the risk "
                        "of a prolonged return to SLA."
                    ),
                },
                {
                    "title": "Issue written resolution commitments to all 113 partners with open disputes",
                    "rationale": (
                        "113 active disputes mean 113 logistics partners who have received no formal "
                        "acknowledgement or timeline. Silence significantly increases the likelihood "
                        "of formal contractual claims."
                    ),
                    "action": (
                        "Operations Lead to draft a standard resolution acknowledgement email for all "
                        "open disputes: confirms the cause, confirms corrected payment is in process, "
                        "and gives an expected resolution date. Dispute team to send to all 113 open "
                        "cases by Wednesday."
                    ),
                    "expected_impact": (
                        "Reduces formal escalation risk. Logistics partners with a committed resolution "
                        "date are significantly less likely to escalate to contractual claims."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "If the recovery pace is not accelerated and partners are not proactively communicated "
                "with, the dispute backlog will remain above SLA into W11, and formal contractual "
                "claims from logistics partners are increasingly likely."
            ),
        },
        "cia": {
            "week_label": "2025-W09",
            "severity": "CRITICAL",
            "executive_summary": (
                "The vendor patch deployed Thursday has restored automated routing for new invoices, "
                "removing the root cause of the ERP incident. The team's focus is now backlog clearance: "
                "98 invoices remain stuck, 113 active disputes are in the resolution queue, and manual "
                "processing hours reached 332 hours as senior processors and authorised overtime are "
                "applied to the backlog. First-pass resolution remains at 90.2% as the team handles "
                "non-standard corrections alongside normal volume. Recovery is on track but will require "
                "sustained throughput for at least two more weeks to reach SLA."
            ),
            "interventions": [
                {
                    "title": "Implement a two-stream processing model to separate backlog and new work",
                    "rationale": (
                        "The team is currently handling both backlog clearance and new invoice processing "
                        "simultaneously, reducing efficiency on both. Separating the streams allows "
                        "specialists to focus and improves throughput on each."
                    ),
                    "action": (
                        "Operations Lead to assign two senior processors to backlog-only triage (stuck "
                        "invoices and open disputes) and the remaining team to normal new-invoice "
                        "processing. Review the split daily and adjust if new volume spikes. Run this "
                        "model until stuck invoice count falls below 30."
                    ),
                    "expected_impact": (
                        "Backlog clearance rate increases by an estimated 20-30% as processors stop "
                        "context-switching between backlog and new work."
                    ),
                },
                {
                    "title": "Close the 50 lowest-value open disputes by end of Thursday",
                    "rationale": (
                        "Dispute resolution rate at 72.3% means 37 active disputes have passed the "
                        "10-business-day contractual window. Closing the smallest cases first reduces "
                        "headcount and frees the team to focus on complex, high-value disputes."
                    ),
                    "action": (
                        "Dispute team lead to sort the 113 open disputes by financial value and assign "
                        "the 50 lowest-value cases for resolution today. Target: confirmed payment "
                        "correction and logistics partner notification sent by end of Thursday."
                    ),
                    "expected_impact": (
                        "Dispute resolution rate recovers toward 80% by end of this week, reducing the "
                        "volume of active cases the team is managing simultaneously."
                    ),
                },
                {
                    "title": "Audit the patch deployment to confirm all routing rules are intact",
                    "rationale": (
                        "The patch restored the overwritten configuration. However, there is no "
                        "confirmation that all routing rules — not just the multi-currency ones — are "
                        "intact and correctly configured."
                    ),
                    "action": (
                        "IT team to run a full routing rule audit against the documented baseline "
                        "configuration by Wednesday. Any discrepancy to be flagged immediately to the "
                        "Director of Technology. Written sign-off on the audit results required before "
                        "end of week."
                    ),
                    "expected_impact": (
                        "Confirms the patch has fully resolved the incident with no residual "
                        "configuration gaps, preventing secondary mis-routing failures from emerging "
                        "as the backlog is cleared."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "Without a two-stream processing model and accelerated dispute closure, the backlog "
                "will take an additional two to three weeks to clear, keeping manual hours above SLA "
                "and dispute resolution below 90% well into Q3."
            ),
        },
    },

    # ── W10 — CRITICAL: Partial recovery from ERP incident ────────────────────
    10: {
        "cos": {
            "week_label": "2025-W10",
            "severity": "CRITICAL",
            "executive_summary": (
                "Recovery continues but three consecutive weeks of above-SLA breach counts are now on "
                "record. Payment accuracy has improved to 96.2%, closing within one percentage point "
                "of the 97% SLA. However, dispute rate remains at 4.1% — above the CRITICAL threshold "
                "— and dispute resolution rate of 81.8% indicates that approximately 16 open disputes "
                "have passed the 10-business-day contractual resolution window. Manual processing hours "
                "at 255 hours remain above SLA, indicating the backlog has not yet been fully absorbed "
                "into normal operating capacity."
            ),
            "interventions": [
                {
                    "title": "Formalise a W11 recovery milestone with named accountability",
                    "rationale": (
                        "Three consecutive weeks of breach data require a formal close-out plan. "
                        "Governance requires a named week and a named owner for return to full "
                        "SLA compliance."
                    ),
                    "action": (
                        "Director of Operations to formally commit to a recovery target at Monday's "
                        "governance review: payment accuracy above 97%, dispute rate below 3%, and "
                        "dispute resolution rate above 90% by W11. If W11 is not achievable, escalate "
                        "to VP Operations for a resource decision."
                    ),
                    "expected_impact": (
                        "Recovery has governance-level commitment and a named accountability owner. "
                        "Weekly tracking is formalised with clear pass/fail criteria."
                    ),
                },
                {
                    "title": "Prioritise the 16 overdue dispute resolutions before the 10-day deadline",
                    "rationale": (
                        "Every dispute unresolved beyond the 10-business-day window is a breach of "
                        "contractual dispute resolution obligations. These cases carry the highest "
                        "legal and reputational risk of formal claims."
                    ),
                    "action": (
                        "Dispute resolution team lead to immediately identify all disputes older than "
                        "10 business days, sort by value, and assign the top 20 by value for same-day "
                        "resolution. Target: zero disputes older than 10 business days by Thursday."
                    ),
                    "expected_impact": (
                        "Dispute resolution rate recovers above 85% this week and above 90% SLA by "
                        "W11. Contractual dispute resolution obligation is met for all outstanding cases."
                    ),
                },
                {
                    "title": "Brief logistics partners with a confirmed resolution timeline",
                    "rationale": (
                        "Partners whose disputes remain open are experiencing payment uncertainty. "
                        "A proactive update reduces escalation risk and maintains relationship trust "
                        "during the recovery period."
                    ),
                    "action": (
                        "Operations Lead to send a status update to all logistics partners with open "
                        "disputes by Wednesday: incident resolved, corrected payments in process, "
                        "confirmed resolution date. Updates to senior partners to come from the VP "
                        "Operations office."
                    ),
                    "expected_impact": (
                        "Partners with a confirmed timeline are significantly less likely to pursue "
                        "contractual remedies, reducing formal escalation rate."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "If dispute resolution does not return above 90% SLA in the next two weeks, the "
                "organisation faces increasing exposure to formal contractual claims from logistics "
                "partners whose disputes have exceeded the 10-business-day resolution window."
            ),
        },
        "cia": {
            "week_label": "2025-W10",
            "severity": "CRITICAL",
            "executive_summary": (
                "The backlog from the ERP incident is approximately 70% cleared. Automated routing "
                "is fully restored and new invoices are processing at normal throughput. The remaining "
                "work is concentrated in two areas: closing the 62 stuck invoices still in the "
                "exception queue and resolving the 86 active disputes, of which an estimated 16 have "
                "passed the 10-business-day contractual resolution window. Manual processing hours at "
                "255 hours are above SLA but declining week-on-week, confirming that backlog reduction "
                "is translating into real capacity recovery."
            ),
            "interventions": [
                {
                    "title": "Clear the full 62-invoice stuck backlog by end of this week",
                    "rationale": (
                        "62 stuck invoices at week start is a manageable volume for a full-capacity "
                        "team. Clearing it this week — rather than carrying it into W11 — prevents "
                        "it from inflating manual hours and exception rates in the following week."
                    ),
                    "action": (
                        "Senior processors to allocate the first 90 minutes of each day to stuck "
                        "invoice clearance until the queue reaches zero. Team lead to report stuck "
                        "invoice count at end of each day. Target: zero stuck invoices by end of "
                        "business Friday."
                    ),
                    "expected_impact": (
                        "Stuck invoice count reaches target below 20 by W11. Manual processing hours "
                        "decline toward the 200-hour SLA as exception-driven overhead is eliminated."
                    ),
                },
                {
                    "title": "Validate the new pre-routing validation check is performing as intended",
                    "rationale": (
                        "A new automated pre-check for routing rules was introduced this week. If "
                        "functioning correctly, it should reduce the rate at which new invoices enter "
                        "the exception queue. If not, the exception rate will not fall despite "
                        "backlog clearance."
                    ),
                    "action": (
                        "IT and Operations Lead to pull a report of invoices that triggered the "
                        "pre-routing validation check this week. Confirm the check is catching the "
                        "exception types that caused the original ERP incident. If not performing "
                        "as expected, escalate to IT for adjustment before end of week."
                    ),
                    "expected_impact": (
                        "Confirms the preventative control is working. First-pass resolution rate "
                        "should recover toward 95% SLA in W11 if the check is effective."
                    ),
                },
                {
                    "title": "Reduce active dispute volume to below 30 by end of week",
                    "rationale": (
                        "86 active disputes at a below-target resolution rate means disputes are "
                        "accumulating faster than they are being closed. The target is a volume the "
                        "team can sustain without overtime."
                    ),
                    "action": (
                        "Dispute resolution team to focus on closing, not investigating, this week. "
                        "Each case where the correction amount is agreed should be closed same-day "
                        "with a confirmation email. Target: 30+ disputes closed by Wednesday, 50+ "
                        "by Friday."
                    ),
                    "expected_impact": (
                        "Active dispute volume falls below 30 by W11. Manual hours attributable to "
                        "dispute correspondence fall accordingly, restoring processing capacity "
                        "toward SLA."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "If the backlog is not fully cleared this week, manual processing hours will remain "
                "above SLA into W11 and the recovery trajectory will extend by at least one "
                "additional week."
            ),
        },
    },

    # ── W11 — WARNING: Near full recovery, residual stuck invoices ────────────
    11: {
        "cos": {
            "week_label": "2025-W11",
            "severity": "WARNING",
            "executive_summary": (
                "Week W11 marks a return to near-full SLA compliance following the three-week ERP "
                "recovery period. Payment accuracy has recovered to 97.1%, SLA breaches are at zero, "
                "and dispute rate has fallen below the 3% target. The one remaining out-of-SLA metric "
                "is stuck invoice count at 28 — above the 20-invoice target — which represents "
                "residual backlog from the incident that has not yet fully cleared. This is a "
                "manageable and expected tail-off from a significant operational incident and is not "
                "indicative of new structural risk."
            ),
            "interventions": [
                {
                    "title": "Complete and distribute the formal ERP incident close-out report",
                    "rationale": (
                        "With KPIs near fully restored, this week is the appropriate moment to close "
                        "the formal incident record. An incomplete or undocumented incident leaves a "
                        "gap in the governance trail and prevents post-incident review findings from "
                        "reaching the board."
                    ),
                    "action": (
                        "Chief of Staff to compile the formal incident close-out report this week: "
                        "incident summary, root cause, two-week breach count, total cost of manual "
                        "overtime, recovery actions taken, and the three systemic gaps identified in "
                        "the post-incident review. VP Operations to sign off and distribute to the "
                        "governance committee."
                    ),
                    "expected_impact": (
                        "Incident is formally closed with a documented governance trail. Post-incident "
                        "review findings are on record for the next change management cycle."
                    ),
                },
                {
                    "title": "Assign owners and target dates to the three post-incident remediation items",
                    "rationale": (
                        "The review identified three systemic gaps: insufficient pre-deployment "
                        "testing, no automated routing rule alert, and no documented rollback "
                        "procedure. Unless formally assigned with target dates, these will not "
                        "be actioned."
                    ),
                    "action": (
                        "Director of Technology and Director of Operations to jointly assign an owner "
                        "and target completion date to each of the three remediation items at next "
                        "Monday's review. Items to be tracked on the PMO roadmap with monthly "
                        "progress reporting."
                    ),
                    "expected_impact": (
                        "Reduces the probability of a recurrence of the same ERP configuration "
                        "failure from near-certain on the next upgrade cycle to near-zero."
                    ),
                },
                {
                    "title": "Confirm the new invoice validation protocol performance after one full week",
                    "rationale": (
                        "The automated pre-routing validation check introduced this week is the primary "
                        "preventative control against future configuration failures. Its performance "
                        "needs one full week of data before it can be relied upon."
                    ),
                    "action": (
                        "Operations Lead to pull a performance report on the validation protocol by "
                        "end of next week: total invoices checked, exceptions caught, false positives "
                        "if any. Report to be shared at the W12 Monday governance review."
                    ),
                    "expected_impact": (
                        "Confirms the control is working at the expected accuracy rate and establishes "
                        "a baseline for future monitoring."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "If the post-incident remediation items are not formally assigned and tracked, the "
                "three systemic gaps — testing protocol, routing alert, rollback procedure — will "
                "remain unaddressed at the next ERP upgrade cycle, and a recurrence of the same "
                "incident is probable."
            ),
        },
        "cia": {
            "week_label": "2025-W11",
            "severity": "WARNING",
            "executive_summary": (
                "Operations are near fully restored following the ERP incident. The new automated "
                "pre-routing validation protocol is showing early positive results, with fewer invoices "
                "entering the exception queue than in prior weeks. Stuck invoice count at 28 is the "
                "last remaining out-of-SLA metric, representing the tail of the incident backlog. "
                "Manual processing hours have returned to 175 hours — within the 200-hour SLA — "
                "confirming that exception-driven overhead has been eliminated. One more week of "
                "focused backlog clearance should return all metrics to SLA."
            ),
            "interventions": [
                {
                    "title": "Clear the remaining 28 stuck invoices by end of Tuesday",
                    "rationale": (
                        "28 stuck invoices is a small and manageable volume. Carrying them into W12 "
                        "is unnecessary given full team capacity is restored. Clearing by Tuesday "
                        "means W12 begins with a clean slate."
                    ),
                    "action": (
                        "Processing team lead to assign the full stuck invoice queue to one senior "
                        "processor for dedicated clearance on Monday and Tuesday. Target: zero stuck "
                        "invoices by end of business Tuesday. Any invoice requiring a correction "
                        "before release to be triaged separately and completed by Thursday."
                    ),
                    "expected_impact": (
                        "Stuck invoice count returns to target below 20 for W12. All post-incident "
                        "backlog is fully cleared."
                    ),
                },
                {
                    "title": "Verify the new client invoice template correction has taken effect",
                    "rationale": (
                        "The new logistics client whose format was generating exceptions in W07 may "
                        "still be using a non-standard template. With the team at full capacity, "
                        "this is the right week to confirm."
                    ),
                    "action": (
                        "Operations Lead to pull the new client's invoice exception rate for W08–W11 "
                        "and confirm whether exception frequency has reduced since the template "
                        "correction was requested. If not, re-escalate to the client's accounts "
                        "contact immediately."
                    ),
                    "expected_impact": (
                        "New client exception rate returns to baseline, removing a persistent source "
                        "of manual processing overhead."
                    ),
                },
                {
                    "title": "Establish the validation protocol baseline for ongoing monitoring",
                    "rationale": (
                        "The new pre-routing validation check has no established performance baseline. "
                        "Without one, it is impossible to detect degradation or confirm improvement "
                        "over time."
                    ),
                    "action": (
                        "IT team to extract a week-one performance report: total invoices checked, "
                        "exceptions flagged at pre-routing stage, and any that bypassed the check. "
                        "Share with Operations Lead by Friday as the baseline for ongoing monitoring."
                    ),
                    "expected_impact": (
                        "Establishes the reference point against which future protocol performance "
                        "will be measured, enabling detection of control degradation over time."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "If the 28 remaining stuck invoices are not cleared this week, the process enters "
                "W12 with a non-zero backlog and the post-incident recovery is reported as incomplete. "
                "Without a validation protocol baseline, the control cannot be monitored for "
                "degradation."
            ),
        },
    },

    # ── W14 — CRITICAL: Staff shortage + volume surge + calculation error ──────
    14: {
        "cos": {
            "week_label": "2025-W14",
            "severity": "CRITICAL",
            "executive_summary": (
                "Week W14 presents a structural capacity failure driven by the simultaneous loss of "
                "three payment processors — 37% of team capacity — combined with a quarterly billing "
                "volume surge. A configuration error in the incentive calculation released a subset "
                "of invoices with incorrect payment amounts, generating 112 active disputes from "
                "logistics partners. Three invoices breached the contractual 7-day deadline, and "
                "payment accuracy has fallen to 95.8%. Manual processing hours have reached 327 "
                "hours — 63% above the 200-hour SLA — as agency staff complete onboarding and "
                "the team works to contain the backlog. The situation was escalated to the "
                "Operations Director on Thursday."
            ),
            "interventions": [
                {
                    "title": "Address the structural staffing vulnerability in the processing team",
                    "rationale": (
                        "The loss of three processors from a small team — two on sick leave, one "
                        "with immediate resignation — exposed a staffing model with no structural "
                        "resilience. This is a recurring pattern of over-reliance on a small number "
                        "of individuals carrying significant financial and contractual risk."
                    ),
                    "action": (
                        "Director of Operations to initiate a workforce resilience review this week: "
                        "identify the minimum viable team size for SLA compliance, assess whether "
                        "the current headcount model has sufficient cover built in, and present a "
                        "recommendation to VP Operations by W15. Permanent replacement hire to "
                        "proceed at maximum speed."
                    ),
                    "expected_impact": (
                        "Prevents a recurrence of the same structural capacity failure. Workforce "
                        "model is right-sized for SLA resilience rather than minimum headcount."
                    ),
                },
                {
                    "title": "Correct and reissue all incentive calculation invoices by Wednesday",
                    "rationale": (
                        "The incentive calculation configuration error has generated 112 formal "
                        "disputes and materially damaged payment accuracy. Until incorrectly calculated "
                        "invoices are corrected and reissued, the dispute backlog will not reduce."
                    ),
                    "action": (
                        "Operations Lead to identify the full scope of invoices affected by the "
                        "calculation error by Monday morning and confirm correct amounts. All affected "
                        "invoices to be corrected and reissued by Wednesday, with a written correction "
                        "notice to each affected logistics partner. Director of Operations to approve "
                        "the correction run before release."
                    ),
                    "expected_impact": (
                        "Removes the root cause of the dispute surge. Dispute count begins declining "
                        "from W15 once corrected invoices are issued and confirmed by partners."
                    ),
                },
                {
                    "title": "Brief VP Operations with a 30-day recovery projection",
                    "rationale": (
                        "Unlike the ERP incident, this failure has a structural component — team "
                        "under-resourcing — that requires a VP-level decision on whether to invest "
                        "in additional permanent headcount or a contingency agency arrangement."
                    ),
                    "action": (
                        "Chief of Staff to prepare a 30-day recovery projection for VP Operations by "
                        "Wednesday: current KPI gap versus SLA, expected recovery trajectory, estimated "
                        "date of full SLA restoration, and a headcount recommendation for board "
                        "consideration."
                    ),
                    "expected_impact": (
                        "VP Operations has the information required to make a workforce investment "
                        "decision before the situation deteriorates further into W15."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "Without immediate correction of the incentive calculation error and a formal "
                "workforce resilience plan, the dispute backlog will continue to grow into W15, "
                "logistics partner relationships will deteriorate further, and the organisation will "
                "face two simultaneous operational risks: a capacity shortage and an escalating "
                "dispute cycle."
            ),
        },
        "cia": {
            "week_label": "2025-W14",
            "severity": "CRITICAL",
            "executive_summary": (
                "This week's deterioration has two distinct process causes: a 37% reduction in "
                "processing capacity due to simultaneous unplanned absences, and a configuration "
                "error in the quarterly incentive calculation that released incorrect payment amounts "
                "to logistics partners. These causes are independent but compounded each other — "
                "reduced capacity meant the calculation error was not caught in pre-release validation, "
                "and the resulting dispute surge is now absorbing the limited available processing "
                "hours. Agency staff were not productive until Thursday, leaving the team critically "
                "under-resourced for the first three days of the week."
            ),
            "interventions": [
                {
                    "title": "Identify and isolate all invoices affected by the incentive calculation error",
                    "rationale": (
                        "The configuration error in the incentive calculation is the primary driver "
                        "of the dispute surge. Until the full scope of affected invoices is confirmed, "
                        "the team cannot prioritise correctly or issue corrections."
                    ),
                    "action": (
                        "Operations Lead to run a reconciliation of the quarterly incentive calculation "
                        "output against the expected formula by Monday morning. Identify every invoice "
                        "where the released amount differs from the correct amount. Generate a correction "
                        "file and route to a senior processor for validation before reissue."
                    ),
                    "expected_impact": (
                        "Scope of the correction is confirmed by Monday. Corrected invoices are "
                        "reissued by Wednesday. Dispute rate begins declining from W15 as logistics "
                        "partners confirm receipt of corrected payments."
                    ),
                },
                {
                    "title": "Introduce a dual-approval gate for all configuration-based calculation runs",
                    "rationale": (
                        "The incentive calculation error was not caught before release. A pre-release "
                        "validation step requiring a second sign-off on any calculation run using "
                        "configurable parameters would have caught this error."
                    ),
                    "action": (
                        "Operations Lead to implement a two-step approval process for all quarterly "
                        "calculation runs immediately: one processor calculates, a second senior "
                        "processor validates the output against the formula specification before "
                        "release. Process to be documented in the standard operating procedure and "
                        "implemented for the next billing cycle."
                    ),
                    "expected_impact": (
                        "Eliminates the class of calculation errors caused by incorrect configuration. "
                        "Prevents a recurrence of the same dispute surge."
                    ),
                },
                {
                    "title": "Build a compressed agency processor onboarding guide for future gaps",
                    "rationale": (
                        "Agency staff required two days of system training before processing "
                        "independently. In a capacity crisis, two days of lost productivity is "
                        "significant. A pre-built onboarding track would reduce this to a few hours."
                    ),
                    "action": (
                        "Operations Lead to document a compressed onboarding guide for agency payment "
                        "processors this week: system access steps, the three core processing "
                        "workflows, and the most common exception types. Store in a shared drive "
                        "accessible without system credentials. Target: agency processors productive "
                        "within four hours of starting."
                    ),
                    "expected_impact": (
                        "Reduces effective agency onboarding time from two days to four hours in "
                        "future capacity gap scenarios, recovering significant throughput at the "
                        "point of maximum need."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "If the incentive calculation error is not corrected this week, the 112 active "
                "disputes will continue to absorb processing capacity throughout W15, keeping "
                "manual hours above 300 and preventing the team from returning to normal "
                "operations until at least W16."
            ),
        },
    },

    # ── W15 — CRITICAL: Stabilising after staffing incident ───────────────────
    15: {
        "cos": {
            "week_label": "2025-W15",
            "severity": "CRITICAL",
            "executive_summary": (
                "Recovery from the W14 staffing and calculation incident is underway. Agency staff "
                "are now processing independently, restoring throughput, and dispute rate has declined "
                "from 5.2% to 3.6% as corrected invoices from the incentive calculation error begin "
                "to clear. However, 52 invoices remain stuck and dispute resolution rate at 78.5% is "
                "11.5 percentage points below the 90% SLA target, indicating a substantial backlog "
                "from the prior week that has not yet been resolved within the contractual 10-business-day "
                "window. One further SLA breach occurred this week, bringing the two-week cumulative "
                "total to four contractual defaults."
            ),
            "interventions": [
                {
                    "title": "Set a formal W16 recovery milestone with VP Operations accountability",
                    "rationale": (
                        "Two consecutive weeks of CRITICAL breaches require a formally committed "
                        "recovery date and a named accountability owner at VP level."
                    ),
                    "action": (
                        "Director of Operations to prepare a W16 milestone review for VP Operations: "
                        "target metrics for W16 (payment accuracy ≥97%, SLA breaches = 0, dispute "
                        "rate <3%, stuck invoices <20), named responsible owner for each, and a "
                        "contingency plan if the milestone is missed. Present at Monday's governance review."
                    ),
                    "expected_impact": (
                        "Recovery has executive-level accountability and a clearly defined pass/fail "
                        "point, reducing the risk of drift into a third consecutive week of "
                        "critical status."
                    ),
                },
                {
                    "title": "Compress the permanent replacement processor hire timeline",
                    "rationale": (
                        "The team is operating below full capacity with agency cover. Agency staff "
                        "are productive but cost more per hour and cannot be relied upon indefinitely. "
                        "The permanent replacement remains at interview stage — it is recommended "
                        "the timeline be compressed to avoid prolonged reliance on agency cover."
                    ),
                    "action": (
                        "HR and Director of Operations to target a hire decision by end of this week "
                        "and a confirmed start date within two weeks. If the preferred candidate "
                        "requires more lead time, fast-track the second-choice candidate. A confirmed "
                        "start date is needed to give the team certainty."
                    ),
                    "expected_impact": (
                        "Permanent capacity is restored within two weeks. Dependency on agency cover "
                        "and the associated cost premium are eliminated."
                    ),
                },
                {
                    "title": "Resolve all disputes within 2 business days of the 10-day contractual deadline",
                    "rationale": (
                        "Dispute resolution at 78.5% means approximately 16 disputes have already "
                        "passed the 10-business-day contractual window. Each that crosses the "
                        "deadline becomes a formal contractual breach in addition to an operational "
                        "metric failure."
                    ),
                    "action": (
                        "Dispute team lead to identify all open disputes by age today. Any dispute "
                        "within 2 business days of the 10-day window to be escalated immediately to "
                        "a senior processor for same-day resolution. Target: all threshold-approaching "
                        "disputes resolved by Wednesday."
                    ),
                    "expected_impact": (
                        "Prevents additional contractual breach exposure from the dispute resolution "
                        "SLA. Dispute resolution rate recovers toward 85% this week."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "If the dispute backlog is not actively managed toward the 10-day contractual "
                "threshold, additional formal dispute resolution SLA breaches will accrue in W16, "
                "compounding the governance exposure from the underlying staffing incident."
            ),
        },
        "cia": {
            "week_label": "2025-W15",
            "severity": "CRITICAL",
            "executive_summary": (
                "The two primary failure causes from W14 are now being managed: the incentive "
                "calculation error has been corrected and reissued invoices are being accepted by "
                "logistics partners, and agency staff have completed onboarding and are processing "
                "at near-normal throughput. The residual impact is concentrated in the dispute "
                "resolution queue, where 75 active disputes from the W14 calculation error remain "
                "open. Processing cycle time at 3.1 days and stuck invoice count at 52 are still "
                "above SLA but improving week-on-week, confirming that the recovery is progressing."
            ),
            "interventions": [
                {
                    "title": "Create a dedicated resolution track for the W14 calculation error disputes",
                    "rationale": (
                        "The majority of the 75 active disputes trace to the W14 incentive calculation "
                        "error. These should be the easiest to close because the correction amount is "
                        "known — the logistics partner simply needs confirmation of the corrected payment."
                    ),
                    "action": (
                        "Dispute team lead to tag all disputes originating from the W14 calculation "
                        "error and create a separate resolution track. Assign two processors "
                        "exclusively to this track until all W14-origin disputes are closed. Target: "
                        "all W14-origin disputes fully resolved by end of this week."
                    ),
                    "expected_impact": (
                        "Eliminates the largest single category of active disputes. Dispute resolution "
                        "rate recovers above 85% and dispute count falls below 30 by W16."
                    ),
                },
                {
                    "title": "Validate agency staff processing accuracy before increasing their throughput",
                    "rationale": (
                        "Agency staff have been processing independently for only a few days. "
                        "Increasing their throughput before confirming their accuracy rate could "
                        "introduce new exceptions or payment errors that will generate additional disputes."
                    ),
                    "action": (
                        "Senior processor to review a random sample of 20 invoices processed by "
                        "agency staff this week. Check accuracy against the standard processing "
                        "checklist. If error rate is below 1%, clear for full throughput. If above "
                        "1%, identify the error pattern and provide targeted coaching before end "
                        "of week."
                    ),
                    "expected_impact": (
                        "Ensures recovery does not introduce a new wave of exceptions. Confirms "
                        "agency staff are processing accurately before they handle the "
                        "highest-value invoices."
                    ),
                },
                {
                    "title": "Clear the stuck invoice queue to below 20 by end of week",
                    "rationale": (
                        "52 stuck invoices will inflate manual hours and exception rates into W16 "
                        "if not cleared. With full agency capacity available, clearing this backlog "
                        "is achievable this week."
                    ),
                    "action": (
                        "Processing team lead to triage the stuck invoice queue on Monday morning: "
                        "sort by age, assign the oldest 20 to senior processors for same-day "
                        "clearance, and assign the remaining 32 to agency staff with supervisor "
                        "oversight. Track progress daily. Target: stuck invoices below 20 by Friday."
                    ),
                    "expected_impact": (
                        "Stuck invoice count returns to SLA target by W16. Manual processing hours "
                        "begin declining toward the 200-hour SLA as the stuck queue overhead "
                        "is eliminated."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "If the dispute backlog from the W14 calculation error is not closed this week, it "
                "will carry into W16 and keep dispute resolution rate below 90% for a third "
                "consecutive week, extending the contractual exposure beyond what can be managed "
                "through normal operations."
            ),
        },
    },

    # ── W16 — CRITICAL: Near-recovery, stuck invoices lingering ──────────────
    16: {
        "cos": {
            "week_label": "2025-W16",
            "severity": "CRITICAL",
            "executive_summary": (
                "Week W16 represents near-full recovery from the W14 staffing incident, with six of "
                "nine KPIs back within SLA. Payment accuracy has returned to 97.2%, SLA breaches are "
                "at zero, and dispute rate has fallen to 2.7% — below the 3% target for the first "
                "time since the incident. The two remaining out-of-SLA metrics are stuck invoice "
                "count at 31 — marginally above the 20-invoice target — and dispute resolution rate "
                "at 88.9%, just below the 90% SLA. These are residual tails from the incident rather "
                "than indicators of new structural risk. Completing the permanent replacement hire "
                "is the single most important governance action this week."
            ),
            "interventions": [
                {
                    "title": "Issue the permanent replacement processor offer letter by Wednesday",
                    "rationale": (
                        "The staffing gap that triggered the W14 incident remains open. Agency cover "
                        "is bridging the gap but is not a permanent solution. With all other KPIs "
                        "recovering, completing the hire is the highest-priority governance action."
                    ),
                    "action": (
                        "HR and Director of Operations to issue the offer letter to the selected "
                        "candidate by Wednesday and confirm a start date within two weeks. If the "
                        "offer is declined, activate the second-choice candidate immediately. "
                        "No further delay to this hire."
                    ),
                    "expected_impact": (
                        "Permanent capacity is fully restored within two weeks. The structural "
                        "vulnerability that caused the W14 incident is eliminated and agency "
                        "cost premium ends."
                    ),
                },
                {
                    "title": "Formally close the W14 incident governance record this week",
                    "rationale": (
                        "With KPIs near fully restored, this is the appropriate moment to formally "
                        "close the incident record. An open incident without a close-out is an "
                        "incomplete governance trail."
                    ),
                    "action": (
                        "Chief of Staff to complete the W14 incident close-out report this week: "
                        "incident summary, root cause (staffing model and calculation configuration), "
                        "cumulative breach count, corrective actions taken, and permanent remediation "
                        "measures implemented. VP Operations to sign off before end of week."
                    ),
                    "expected_impact": (
                        "Incident is formally closed with a complete audit trail. Post-incident "
                        "learnings are on record: dual-approval calculation gate, compressed agency "
                        "onboarding track, workforce resilience review."
                    ),
                },
                {
                    "title": "Set a daily stuck invoice count checkpoint until all metrics reach SLA",
                    "rationale": (
                        "With 31 stuck invoices remaining, the team is one week from returning all "
                        "metrics to SLA. Tracking explicitly ensures it does not drift through "
                        "end-of-recovery complacency."
                    ),
                    "action": (
                        "Operations Lead to report stuck invoice count at the Monday morning operations "
                        "review each day this week. Target: below 20 by Wednesday, zero by Friday. "
                        "If count is not declining by Tuesday, escalate to Director of Operations "
                        "for resource reallocation."
                    ),
                    "expected_impact": (
                        "Stuck invoice count returns to target by end of W16. All nine KPIs are "
                        "within SLA for the first time since the W14 incident."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "The primary risk at this stage is complacency: with most metrics recovered, the "
                "remaining gaps may not receive the focused attention needed to close them fully. "
                "If the permanent hire is delayed and the stuck queue is not cleared, the team will "
                "enter W17 with unresolved structural vulnerabilities."
            ),
        },
        "cia": {
            "week_label": "2025-W16",
            "severity": "CRITICAL",
            "executive_summary": (
                "Operations are stabilising strongly. Six of nine metrics are within SLA and the two "
                "remaining gaps — stuck invoices at 31 and dispute resolution rate at 88.9% — are "
                "marginal and declining. The dispute queue from the W14 calculation error is "
                "approximately 80% resolved, with remaining cases under active management. Agency "
                "staff are processing at full throughput and the permanent replacement hire is at "
                "offer stage. This week's focus is on closing the last 31 stuck invoices and "
                "finishing the dispute queue, which should return all metrics to SLA by end of week "
                "or early W17."
            ),
            "interventions": [
                {
                    "title": "Close the remaining 31 stuck invoices before Wednesday",
                    "rationale": (
                        "31 stuck invoices is a small, manageable volume. Closing them before "
                        "Wednesday clears the way for a clean W17 start with all metrics within SLA."
                    ),
                    "action": (
                        "Processing team lead to assign the 31 stuck invoices to senior processors "
                        "on Monday morning as a priority task. Each invoice to be triaged, corrected "
                        "if needed, and released by Wednesday. Track hourly on Monday and Tuesday. "
                        "No new exceptions to be added to the stuck queue without immediate escalation."
                    ),
                    "expected_impact": (
                        "Stuck invoice count falls below 20 by Wednesday. W16 ends with all process "
                        "metrics at or near SLA for the first time since the W14 incident."
                    ),
                },
                {
                    "title": "Resolve the remaining 20% of the W14 dispute queue by Thursday",
                    "rationale": (
                        "The dispute queue from the incentive calculation error is 80% resolved. "
                        "The remaining cases are either complex, disputed on quantum, or have not "
                        "received a partner response. Each unresolved case keeps resolution rate "
                        "below the 90% SLA."
                    ),
                    "action": (
                        "Dispute team lead to identify remaining open W14-origin disputes today. "
                        "For cases awaiting partner response, send a second follow-up today. For "
                        "complex cases where the correction amount is in dispute, escalate to a "
                        "senior processor with sign-off authority to negotiate resolution. Target: "
                        "all W14-origin disputes closed by Thursday."
                    ),
                    "expected_impact": (
                        "Dispute resolution rate recovers above 90% SLA by end of W16 or early W17. "
                        "The W14 incident is fully resolved operationally."
                    ),
                },
                {
                    "title": "Prepare a structured onboarding plan for the incoming permanent processor",
                    "rationale": (
                        "The permanent replacement is expected to start within two weeks. A structured "
                        "handover from the agency staff and senior processors who covered the gap "
                        "will reduce the productivity ramp-up time."
                    ),
                    "action": (
                        "Operations Lead to prepare a one-week onboarding plan for the new processor "
                        "this week: key workflows, current exception patterns, the dual-approval "
                        "calculation gate, and the pre-routing validation check. Assign a senior "
                        "processor as buddy for the first two weeks."
                    ),
                    "expected_impact": (
                        "New processor reaches independent productivity within one week. Agency "
                        "cover cost ends as soon as the new hire is operational."
                    ),
                },
            ],
            "risk_if_unaddressed": (
                "The primary risk this week is leaving the last 10% of recovery work unfinished. "
                "If the 31 stuck invoices and remaining disputes carry into W17, the permanent "
                "hire will join an operation still managing backlog rather than running at "
                "normal pace."
            ),
        },
    },
}

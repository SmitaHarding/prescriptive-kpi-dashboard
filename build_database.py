"""
build_database.py
=================
Creates and seeds the KPI dashboard SQLite database.
Run this once before launching the app:  python build_database.py

v2.0 changes:
  - manual_processing_hours is now formula-derived (see COEFFICIENTS below)
  - dispute_count and invoice_exception_count added as derived columns
  - dispute_resolution_rate added as a new v1.0 metric
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kpi_dashboard.db")

# ── Workforce capacity formula coefficients ──────────────────────────────────
# Y = β₀ + (μ₁ × stuck_invoice_count) + (μ₂ × invoice_exception_count) + (μ₃ × dispute_count)
#
# β₀  = base processing load (hrs) — fixed overhead regardless of exception volume
# μ₁  = hrs of manual labour per stuck invoice requiring queue intervention
# μ₂  = hrs of manual labour per invoice exception requiring re-validation
# μ₃  = hrs of manual labour per dispute requiring investigation and correspondence
#
# These coefficients are configurable — adjust to reflect actual team capacity data.
# ArbZG compliance note: German Federal Working Time Act (Arbeitszeitgesetz) caps
# working time at 48 hours per week per employee. A team of 4 processors = 192 hrs
# sustainable capacity. Persistently exceeding 200 hrs signals structural under-resourcing.
COEFFICIENTS = {
    "beta_0": 40.0,   # base processing load (hrs/week)
    "mu_1":    0.50,  # hrs per stuck invoice
    "mu_2":    0.25,  # hrs per exception invoice
    "mu_3":    2.00,  # hrs per active dispute
}

# ── Raw 16-week operational KPI data ─────────────────────────────────────────
# Columns (11):
#   week_number, week_label,
#   payment_accuracy_rate, invoice_volume,
#   sla_breach_count, first_pass_resolution, processing_cycle_days,
#   dispute_rate, invoice_exception_rate, stuck_invoice_count,
#   dispute_resolution_rate
#
# NOTE: manual_processing_hours is NOT stored here — it is formula-derived in build().
#
# SLA Targets:
#   payment_accuracy_rate     >= 97%
#   sla_breach_count          = 0
#   first_pass_resolution     >= 95%
#   processing_cycle_days     < 3 days
#   dispute_rate              < 3%
#   invoice_exception_rate    < 2%
#   stuck_invoice_count       < 20
#   dispute_resolution_rate   >= 90%   (resolved within 10 business days)
#   manual_processing_hours   < 200 hrs/week
#
# Incident periods:
#   W08 — ERP upgrade failure (CRITICAL)
#   W14 — Staff shortage + volume surge (CRITICAL)

RAW_WEEKS = [
    #  wk  label         pay_acc  vol    breach  fpr    cyc   disp  exc   stuck  dsr
    (1,  "2025-W01",   98.2,    1980,  0,      96.1,  2.4,  1.8,  0.9,  8,    93.2),
    (2,  "2025-W02",   97.8,    2010,  0,      95.8,  2.5,  2.1,  1.0,  10,   92.8),
    (3,  "2025-W03",   98.5,    1995,  0,      96.4,  2.3,  1.7,  0.8,  7,    94.1),
    (4,  "2025-W04",   97.6,    2050,  0,      95.2,  2.6,  2.2,  1.1,  12,   92.5),
    (5,  "2025-W05",   98.0,    2020,  0,      96.0,  2.4,  1.9,  0.9,  9,    93.5),
    (6,  "2025-W06",   97.9,    2030,  0,      95.7,  2.5,  2.0,  1.0,  11,   92.9),
    (7,  "2025-W07",   97.4,    2100,  1,      94.8,  2.8,  2.4,  1.4,  18,   91.2),  # early warning
    (8,  "2025-W08",   93.1,    2210,  6,      88.3,  4.1,  6.8,  4.2,  127,  61.4),  # CRITICAL — ERP failure
    (9,  "2025-W09",   94.8,    2180,  4,      90.2,  3.7,  5.2,  3.1,  98,   72.3),  # recovery begins
    (10, "2025-W10",   96.2,    2090,  2,      93.1,  3.2,  4.1,  2.3,  62,   81.8),  # partial recovery
    (11, "2025-W11",   97.1,    2040,  0,      95.0,  2.7,  2.8,  1.5,  28,   90.6),  # near target
    (12, "2025-W12",   97.8,    2020,  0,      95.6,  2.5,  2.1,  1.0,  14,   93.2),
    (13, "2025-W13",   98.1,    2000,  0,      96.2,  2.4,  1.8,  0.9,  9,    94.0),
    (14, "2025-W14",   95.8,    2150,  3,      91.7,  3.5,  5.2,  3.4,  89,   64.7),  # CRITICAL — staff shortage
    (15, "2025-W15",   96.5,    2080,  1,      93.4,  3.1,  3.6,  2.2,  52,   78.5),  # recovering
    (16, "2025-W16",   97.2,    2030,  0,      95.1,  2.7,  2.7,  1.4,  31,   88.9),  # stabilising
]

OPERATIONAL_NOTES = {
    1: (
        "Week 1 — Baseline operations. Full team at capacity. No incidents or escalations. "
        "Q1 planning activities underway in parallel with normal processing. All KPIs within SLA."
    ),
    2: (
        "Week 2 — Two new team members joined the payment processing team and are in structured onboarding. "
        "Their reduced throughput while training created a small invoice backlog, adding approximately 0.2 days "
        "to average cycle time. No SLA breaches. Backlog expected to clear by end of following week."
    ),
    3: (
        "Week 3 — Strong performance week. A new invoice validation checklist was introduced at the point of "
        "receipt to catch data errors earlier. Early results show a measurable reduction in exception flags, "
        "which reduces the volume of invoices requiring manual review and lowers processing hours."
    ),
    4: (
        "Week 4 — End-of-month billing cycle caused a 12% spike in invoice volume above the weekly baseline. "
        "The processing team managed the surge without breaching the 7-day SLA, though cycle time increased "
        "slightly and manual processing hours rose to absorb the additional workload."
    ),
    5: (
        "Week 5 — Normal operations. No incidents or escalations. All payment accuracy, cycle time, and "
        "dispute rate metrics within SLA. Volume returned to baseline following the prior week surge."
    ),
    6: (
        "Week 6 — Planned system maintenance window ran from 22:00 Tuesday to 02:00 Wednesday, causing a "
        "4-hour pause in automated batch processing. The team prioritised the oldest invoices first after "
        "recovery. All invoices were processed within SLA. Stuck invoice count temporarily elevated mid-week "
        "but resolved before end of business Thursday."
    ),
    7: (
        "Week 7 — Two senior processors are on scheduled annual leave. Cover is provided by junior staff "
        "with supervisory oversight, which increases the time required per invoice and raises manual "
        "processing hours. A new logistics client began invoicing this week, adding approximately 300 "
        "additional invoice lines to the weekly volume. No SLA breaches but first-pass resolution is "
        "slightly reduced due to the cover arrangement."
    ),
    8: (
        "CRITICAL WEEK — ERP System Failure. An ERP system upgrade deployed Monday morning introduced a "
        "defect that broke automated routing rules for multi-currency invoices. Approximately 140 invoices "
        "were mis-routed to the wrong approval queue and were not processed within the normal workflow. "
        "Two senior processors remained on annual leave, limiting recovery capacity. "
        "Manual rework was required across three teams to identify and re-route affected invoices. "
        "The incident was escalated to VP Operations on Wednesday. Incident ticket #INC-2024-0892 raised. "
        "127 invoices entered an exception state as the team worked to correct payment amounts that had "
        "been released with incorrect values. Logistics company partners began raising formal disputes "
        "against incorrect payments, driving the dispute rate sharply above SLA. "
        "Payment accuracy, first-pass resolution, manual processing hours, stuck invoice count, "
        "dispute rate, and SLA breach count are all severely impacted this week."
    ),
    9: (
        "Week 9 — ERP Recovery Underway. The vendor released a patch on Thursday which restored automated "
        "routing rules for multi-currency invoices. Root cause confirmed: the upgrade had overwritten a "
        "custom routing configuration that had been in place since the multi-currency expansion in 2023. "
        "Overtime was authorised for the processing team to begin clearing the exception and dispute backlog "
        "carried over from the prior week. Senior processors returned from leave and took lead on backlog "
        "triage. Manual processing hours remain elevated as staff work through rework. Dispute resolution "
        "team is actively working through the queue of formal disputes raised by logistics partners."
    ),
    10: (
        "Week 10 — Continued Recovery. Approximately 70% of the exception backlog from the ERP incident has "
        "been cleared. Automated routing is fully restored and processing new invoices at normal throughput. "
        "Senior processors are back at full capacity. Dispute rate is declining as corrections are issued "
        "to affected logistics companies. Stuck invoice count is falling. Manual processing hours remain "
        "above the 200-hour SLA as the remaining backlog is worked down."
    ),
    11: (
        "Week 11 — Full Recovery. Exception backlog fully cleared. All metrics returning to pre-incident "
        "levels. A new invoice validation protocol was introduced this week, adding an automated pre-check "
        "for routing rules before invoices enter the approval queue. This is designed to prevent a "
        "recurrence of the mis-routing failure. First-pass resolution rate recovering toward SLA."
    ),
    12: (
        "Week 12 — Stable Operations. Post-incident review completed and findings shared with the wider "
        "PMO. The review identified three systemic gaps: insufficient pre-deployment testing of ERP "
        "configuration changes, no automated alert when routing rule counts fall below expected thresholds, "
        "and no documented rollback procedure. All three are now on the remediation roadmap. "
        "All KPIs within SLA this week."
    ),
    13: (
        "Week 13 — Sustained improvement. The validation protocol introduced in W11 is producing measurable "
        "results: fewer invoices are entering the exception queue, which reduces manual processing hours "
        "and improves first-pass resolution. Operations running normally with no escalations."
    ),
    14: (
        "INCIDENT — Staffing and Volume Pressure. Three payment processors are unavailable this week: "
        "two on sick leave and one who resigned with immediate effect. This represents a 37% reduction "
        "in processing capacity on the team. Simultaneously, the quarterly billing cycle triggered an "
        "above-baseline invoice volume surge. Temporary agency staff were onboarded mid-week but required "
        "two days of system training before they could process independently, meaning effective cover did "
        "not begin until Thursday. "
        "With reduced capacity and elevated volume, the invoice backlog built rapidly. A configuration "
        "error in the incentive calculation applied to the quarterly billing run caused a subset of "
        "invoices to carry incorrect payment amounts. Logistics partners began raising formal disputes "
        "when incorrect payments were released. 89 invoices entered a stuck state pending manual review "
        "and correction. The situation was escalated to the Operations Director on Thursday. "
        "Dispute rate, stuck invoice count, manual processing hours, and payment accuracy are all "
        "materially impacted this week."
    ),
    15: (
        "Week 15 — Stabilising After Staffing Incident. Agency staff have completed training and are now "
        "processing independently, restoring throughput. Recruitment for the permanent replacement "
        "processor has been opened, with interviews scheduled. Invoice volume is returning to normal "
        "following the quarterly billing surge. The dispute resolution team is actively working through "
        "the formal dispute queue raised by logistics partners in the prior week. Stuck invoice count "
        "is declining as the backlog from the incentive calculation error is corrected and reissued."
    ),
    16: (
        "Week 16 — Continued Recovery. Processing operations are returning to target levels as agency "
        "cover stabilises the team's throughput. The permanent replacement processor hire is at offer "
        "stage, with a start date expected within two weeks. The dispute queue from the W14 incentive "
        "calculation error is approximately 80% resolved, with remaining cases under active management. "
        "First-pass resolution and payment accuracy are trending back toward SLA. Manual processing "
        "hours are still above target due to the ongoing dispute rework, but are declining week-on-week."
    ),
}


def _derive_row(raw_row):
    """
    Compute formula-derived and count-derived fields for one raw data row.

    Returns a 14-value tuple matching the kpi_weekly INSERT statement:
      week_number, week_label,
      payment_accuracy_rate, manual_processing_hours, invoice_volume,
      sla_breach_count, first_pass_resolution, processing_cycle_days,
      dispute_rate, invoice_exception_rate, stuck_invoice_count,
      dispute_resolution_rate, dispute_count, invoice_exception_count
    """
    (week_number, week_label, payment_accuracy_rate, invoice_volume,
     sla_breach_count, first_pass_resolution, processing_cycle_days,
     dispute_rate, invoice_exception_rate, stuck_invoice_count,
     dispute_resolution_rate) = raw_row

    # Derived absolute counts
    dispute_count           = round(dispute_rate / 100 * invoice_volume)
    invoice_exception_count = round(invoice_exception_rate / 100 * invoice_volume)

    # Algorithmic workforce capacity formula
    b  = COEFFICIENTS["beta_0"]
    m1 = COEFFICIENTS["mu_1"]
    m2 = COEFFICIENTS["mu_2"]
    m3 = COEFFICIENTS["mu_3"]
    manual_processing_hours = round(
        b + (m1 * stuck_invoice_count) + (m2 * invoice_exception_count) + (m3 * dispute_count),
        1,
    )

    return (
        week_number, week_label,
        payment_accuracy_rate, manual_processing_hours, invoice_volume,
        sla_breach_count, first_pass_resolution, processing_cycle_days,
        dispute_rate, invoice_exception_rate, stuck_invoice_count,
        dispute_resolution_rate, dispute_count, invoice_exception_count,
    )


def build(db_path=None):
    """
    Creates the SQLite database, defines the schema, and seeds it with
    16 weeks of operational KPI data.

    Formula-derived fields (manual_processing_hours, dispute_count,
    invoice_exception_count) are computed via _derive_row() before insertion
    so the database always reflects the canonical workforce capacity model.

    Safe to re-run — drops and recreates the database each time.

    Args:
        db_path: Optional explicit path for the database file.
                 Defaults to DB_PATH (same directory as this script).
    """
    target = db_path or DB_PATH
    if os.path.exists(target):
        os.remove(target)

    conn = sqlite3.connect(target)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE kpi_weekly (
            week_number                INTEGER PRIMARY KEY,
            week_label                 TEXT    NOT NULL,
            payment_accuracy_rate      REAL,
            manual_processing_hours    REAL,
            invoice_volume             INTEGER,
            sla_breach_count           INTEGER,
            first_pass_resolution      REAL,
            processing_cycle_days      REAL,
            dispute_rate               REAL,
            invoice_exception_rate     REAL,
            stuck_invoice_count        INTEGER,
            dispute_resolution_rate    REAL,
            dispute_count              INTEGER,
            invoice_exception_count    INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE operational_notes (
            week_number INTEGER PRIMARY KEY,
            notes       TEXT NOT NULL,
            FOREIGN KEY (week_number) REFERENCES kpi_weekly(week_number)
        )
    """)

    weeks_data = [_derive_row(r) for r in RAW_WEEKS]

    cur.executemany(
        "INSERT INTO kpi_weekly VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        weeks_data
    )
    cur.executemany(
        "INSERT INTO operational_notes VALUES (?,?)",
        [(w, n) for w, n in OPERATIONAL_NOTES.items()]
    )

    conn.commit()
    conn.close()

    print(f"✅ Database created: {target}")
    print(f"   {len(weeks_data)} weeks of KPI data seeded (10 metrics, 2 derived counts).")
    print()
    print("   Formula-derived manual_processing_hours:")
    for r in weeks_data:
        wk, label, hrs = r[0], r[1], r[3]
        flag = " ← CRITICAL" if hrs > 230 else (" ← WARNING" if hrs > 200 else "")
        print(f"   {label}: {hrs} hrs{flag}")


if __name__ == "__main__":
    build()

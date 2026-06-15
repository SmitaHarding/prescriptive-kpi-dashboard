"""
detect_anomalies.py
===================
Queries the KPI database and flags weeks where metrics breached SLA targets
or showed significant week-over-week deterioration.

Returns a list of anomaly dicts — one per flagged week — consumed by ai_agent.py.

Usage:
    python detect_anomalies.py          # prints report to terminal
    import detect_anomalies; anomalies = detect_anomalies.detect()

v2.0 changes:
  - dispute_resolution_rate added as a new metric (SLA, severity, WoW rules)
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kpi_dashboard.db")

# ── SLA Thresholds ──────────────────────────────────────────────────────────
SLA = {
    "payment_accuracy_rate":   {"target": 97.0, "direction": "above"},
    "manual_processing_hours": {"target": 200.0, "direction": "below"},
    "sla_breach_count":        {"target": 0,    "direction": "at_or_below"},
    "first_pass_resolution":   {"target": 95.0, "direction": "above"},
    "processing_cycle_days":   {"target": 3.0,  "direction": "below"},
    "dispute_rate":            {"target": 3.0,  "direction": "below"},
    "invoice_exception_rate":  {"target": 2.0,  "direction": "below"},
    "stuck_invoice_count":     {"target": 20,   "direction": "at_or_below"},
    "dispute_resolution_rate": {"target": 90.0, "direction": "above"},  # >= 90% resolved within 10 business days
}

# Threshold at which a breach escalates from WARNING to CRITICAL
SEVERITY_RULES = {
    "payment_accuracy_rate":   95.0,   # below 95%  = critical
    "manual_processing_hours": 230.0,  # above 230  = critical
    "sla_breach_count":        3,      # above 3    = critical
    "first_pass_resolution":   92.0,   # below 92%  = critical
    "processing_cycle_days":   3.8,    # above 3.8d = critical
    "dispute_rate":            4.0,    # above 4%   = critical
    "invoice_exception_rate":  3.0,    # above 3%   = critical
    "stuck_invoice_count":     30,     # above 30   = critical  (50% overshoot of 20 SLA — consistent with other metrics)
    "dispute_resolution_rate": 82.0,   # below 82%  = critical  (8pp gap vs 90% SLA — proportional with other rate metrics)
}

# Week-over-week thresholds that trigger a WARNING flag
# Format: metric -> (min_change_to_flag, direction_that_is_bad)
WOW_RULES = {
    "payment_accuracy_rate":   (2.0,  "decrease"),  # drop of >= 2pp
    "first_pass_resolution":   (2.0,  "decrease"),
    "dispute_rate":            (1.0,  "increase"),  # spike of >= 1pp
    "invoice_exception_rate":  (0.5,  "increase"),  # spike of >= 0.5pp
    "stuck_invoice_count":          (10,   "increase"),  # increase of >= 10
    "dispute_resolution_rate":      (3.0,  "decrease"),  # drop of >= 3pp
    "manual_processing_hours":      (20.0, "increase"),  # spike of >= 20 hrs (10% of 200hr SLA)
    "processing_cycle_days":        (0.5,  "increase"),  # spike of >= 0.5 days
}


def _get_all_weeks(conn):
    cur = conn.execute("""
        SELECT k.week_number, k.week_label,
               k.payment_accuracy_rate, k.manual_processing_hours,
               k.invoice_volume, k.sla_breach_count,
               k.first_pass_resolution, k.processing_cycle_days,
               k.dispute_rate, k.invoice_exception_rate, k.stuck_invoice_count,
               k.dispute_resolution_rate,
               k.dispute_count, k.invoice_exception_count,
               COALESCE(n.notes, '') AS notes
        FROM kpi_weekly k
        LEFT JOIN operational_notes n USING (week_number)
        ORDER BY k.week_number
    """)
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]


def _is_breach(metric, value):
    rule = SLA[metric]
    if rule["direction"] == "above":
        return value < rule["target"]
    elif rule["direction"] in ("below", "at_or_below"):
        return value > rule["target"]
    return False


def _severity(metric, value):
    threshold = SEVERITY_RULES[metric]
    direction = SLA[metric]["direction"]
    if direction == "above":
        return "CRITICAL" if value < threshold else "WARNING"
    else:
        return "CRITICAL" if value > threshold else "WARNING"


def detect(db_path=DB_PATH):
    """
    Returns a list of anomaly dicts for every week with at least one breach.
    Each dict contains:
        week_number, week_label, overall_severity,
        kpis (dict of all 10 metrics + 2 derived counts),
        breaches (list), operational_notes (str)
    """
    conn = sqlite3.connect(db_path)
    weeks = _get_all_weeks(conn)
    conn.close()

    anomalies = []

    for i, week in enumerate(weeks):
        breaches = []
        prev = weeks[i - 1] if i > 0 else None

        # Absolute SLA breach checks
        for metric in SLA:
            value = week[metric]
            if _is_breach(metric, value):
                sev = _severity(metric, value)
                target = SLA[metric]["target"]
                breaches.append({
                    "metric":   metric,
                    "value":    value,
                    "target":   target,
                    "severity": sev,
                    "type":     "SLA_BREACH",
                    "detail":   f"{metric} = {value} (SLA target: {target})",
                })

        # Week-over-week deterioration checks
        if prev:
            for metric, (threshold, bad_direction) in WOW_RULES.items():
                curr_val = week[metric]
                prev_val = prev[metric]
                delta = curr_val - prev_val

                flagged = (
                    (bad_direction == "decrease" and delta <= -threshold) or
                    (bad_direction == "increase" and delta >= threshold)
                )
                if flagged:
                    breaches.append({
                        "metric":   metric,
                        "value":    curr_val,
                        "target":   SLA[metric]["target"],
                        "severity": "WARNING",
                        "type":     "WOW_DETERIORATION",
                        "detail":   (
                            f"{metric} moved {abs(delta):.1f} "
                            f"{'pp' if delta_type_is_pct(metric) else 'units'} "
                            f"week-over-week ({prev_val} → {curr_val})"
                        ),
                    })

        if breaches:
            overall = "CRITICAL" if any(b["severity"] == "CRITICAL" for b in breaches) else "WARNING"
            anomalies.append({
                "week_number":      week["week_number"],
                "week_label":       week["week_label"],
                "overall_severity": overall,
                "kpis": {
                    "payment_accuracy_rate":   week["payment_accuracy_rate"],
                    "manual_processing_hours": week["manual_processing_hours"],
                    "invoice_volume":          week["invoice_volume"],
                    "sla_breach_count":        week["sla_breach_count"],
                    "first_pass_resolution":   week["first_pass_resolution"],
                    "processing_cycle_days":   week["processing_cycle_days"],
                    "dispute_rate":            week["dispute_rate"],
                    "invoice_exception_rate":  week["invoice_exception_rate"],
                    "stuck_invoice_count":     week["stuck_invoice_count"],
                    "dispute_resolution_rate": week["dispute_resolution_rate"],
                    "dispute_count":           week["dispute_count"],
                    "invoice_exception_count": week["invoice_exception_count"],
                },
                "breaches":          breaches,
                "operational_notes": week["notes"],
            })

    return anomalies


def delta_type_is_pct(metric):
    """Returns True if metric is a percentage (for WoW detail labelling)."""
    return metric in (
        "payment_accuracy_rate", "first_pass_resolution",
        "dispute_rate", "invoice_exception_rate", "dispute_resolution_rate",
    )


if __name__ == "__main__":
    results = detect()
    print(f"Anomaly Detection — {len(results)} flagged week(s)\n{'=' * 65}")
    for a in results:
        icon = "CRITICAL" if a["overall_severity"] == "CRITICAL" else "WARNING"
        print(f"\n[{icon}] {a['week_label']}")
        print(f"   Breaches detected: {len(a['breaches'])}")
        for b in a["breaches"]:
            print(f"   [{b['type']}] {b['detail']}")
        print(f"   Notes: {a['operational_notes'][:120]}...")

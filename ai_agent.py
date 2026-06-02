"""
ai_agent.py
===========
Claude-powered Operational Governance Agent — dual persona system.

Two AI personas fire automatically when a flagged week is selected:

  Executive Copilot (CoS)
    Executive-level risk governance lens. Financial exposure, contractual obligations,
    strategic business impact. Delivers board-ready briefing language.

  Operations Copilot (CIA)
    BPE and operations delivery lens. Root cause, process bottlenecks, capacity
    constraints, and specific operational interventions. Delivers engineering-level actions.

Both personas return the same JSON schema and are cached in session state.

SETUP: Set your Claude API key before running:
  export ANTHROPIC_API_KEY="your-key-here"        # Mac/Linux
  set ANTHROPIC_API_KEY=your-key-here             # Windows

Get your API key at: https://console.anthropic.com

API Protection: The Claude API key must be strictly abstracted using environment
variables or deployment secrets managers. It must never be hardcoded into
client-side scripts or committed to source control.
"""

import anthropic
import json
import os

# ── Shared JSON output schema ─────────────────────────────────────────────────
_JSON_SCHEMA = """
{
  "week_label": "<week>",
  "severity": "<CRITICAL|WARNING>",
  "executive_summary": "<3-4 sentence narrative — see persona instructions above>",
  "interventions": [
    {
      "title": "<short action title>",
      "rationale": "<why this addresses the root cause>",
      "action": "<specific, concrete step — who does what by when>",
      "expected_impact": "<measurable outcome if action is taken>"
    },
    { ... },
    { ... }
  ],
  "risk_if_unaddressed": "<what happens if no action is taken>"
}"""

# ── Persona 1: Executive Copilot ─────────────────────────────────────────────
SYSTEM_PROMPT_COS = """You are the Executive Copilot preparing a briefing for the Operations
Executive team. Your expertise spans financial governance, contractual risk, regulatory compliance,
and board-level communication for a pan-European B2B logistics payments operation.

Your role is to analyse weekly KPI data and operational notes, then produce:
1. A concise executive root cause narrative (3-4 sentences) framing the week's deterioration
   in terms of financial exposure, SLA contractual obligations, and strategic business risk.
   Write as if presenting to an executive who needs to understand the P&L and reputational impact —
   not the operational detail. Use plain English — avoid acronyms and technical jargon.
2. Exactly THREE highly specific, senior-level interventions. Each must be escalation-ready:
   name the decision owner, the financial or contractual stake, and the board-reportable outcome.
   Keep each intervention direct and jargon-free.

Tone: authoritative, clear, and direct. No filler phrases. No jargon without plain-English explanation.
Write as the Executive Copilot who will present this at the Monday morning executive review.""" + f"\n\nOutput valid JSON matching this schema exactly:{_JSON_SCHEMA}"

# ── Persona 2: Operations Copilot ────────────────────────────────────────────
SYSTEM_PROMPT_CIA = """You are the Operations Copilot embedded within the BPE and Operations
Delivery team. Your expertise spans business process improvement, operational root cause analysis,
and capacity management for a pan-European B2B logistics payments operation.

Your role is to analyse weekly KPI data and operational notes, then produce:
1. A concise process-level root cause narrative (3-4 sentences) identifying the specific process
   failure, capacity constraint, or system bottleneck that caused the week's deterioration.
   Write for an operations manager who needs to know exactly where the process broke and what
   fix will prevent it happening again. Use plain, direct language — no acronyms or technical jargon.
2. Exactly THREE highly specific, operationally actionable interventions. Each must name the
   process owner, the specific step to change, and the measurable outcome that confirms the fix worked.
   Keep each intervention concrete and easy to act on without specialist knowledge.

Tone: clear, direct, and action-focused. No generic advice. No filler phrases. No unexplained jargon.
Write as the Operations Copilot who will run the Monday morning operational debrief.""" + f"\n\nOutput valid JSON matching this schema exactly:{_JSON_SCHEMA}"


def _build_user_prompt(anomaly: dict) -> str:
    """Builds the shared user prompt for both personas."""
    breaches_text = "\n".join(
        f"  - [{b['type']}] {b['detail']} (severity: {b['severity']})"
        for b in anomaly["breaches"]
    )

    kpis = anomaly["kpis"]
    return f"""Analyse the following operational KPI data for {anomaly['week_label']}.

OVERALL SEVERITY: {anomaly['overall_severity']}

KPI SNAPSHOT — EXECUTIVE OVERSIGHT:
  - SLA Breach Count:          {kpis['sla_breach_count']}  (target: 0)
  - Payment Accuracy Rate:     {kpis['payment_accuracy_rate']}%  (SLA: >=97%)
  - Dispute Rate:              {kpis['dispute_rate']}%  (target: <3%)
  - Invoice Volume:            {kpis['invoice_volume']} invoices

KPI SNAPSHOT — BPE & OPERATIONS DELIVERY VIEW:
  - First-Pass Resolution:     {kpis['first_pass_resolution']}%  (SLA: >=95%)
  - Processing Cycle Time:     {kpis['processing_cycle_days']} days  (target: <3)
  - Invoice Exception Rate:    {kpis['invoice_exception_rate']}%  (target: <2%)
  - Stuck Invoice Count:       {kpis['stuck_invoice_count']}  (target: <20)
  - Dispute Resolution Rate:   {kpis['dispute_resolution_rate']}%  (SLA: >=90%)
  - Manual Processing Hours:   {kpis['manual_processing_hours']} hrs  (target: <200)

DERIVED COUNTS:
  - Active Disputes:           {kpis['dispute_count']} invoices
  - Invoice Exceptions:        {kpis['invoice_exception_count']} invoices

BREACHES DETECTED:
{breaches_text}

OPERATIONAL NOTES (from team log this week):
{anomaly['operational_notes']}

Produce your full structured JSON analysis now."""


def _call_claude(system_prompt: str, user_prompt: str, api_key: str = None) -> dict:
    """Makes one Claude API call and returns parsed JSON."""
    client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1400,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )

    raw = response.content[0].text.strip()

    # Strip markdown code fences if Claude wraps the JSON
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    return json.loads(raw.strip())


def analyse_week_cos(anomaly: dict, api_key: str = None) -> dict:
    """
    Executive Copilot persona — executive-level financial risk and governance framing.

    Parameters
    ----------
    anomaly : dict
        One item from detect_anomalies.detect()
    api_key : str, optional
        Claude API key. Falls back to ANTHROPIC_API_KEY environment variable.

    Returns
    -------
    dict
        Structured analysis: executive_summary, 3 interventions, risk_if_unaddressed
    """
    return _call_claude(SYSTEM_PROMPT_COS, _build_user_prompt(anomaly), api_key)


def analyse_week_cia(anomaly: dict, api_key: str = None) -> dict:
    """
    Operations Copilot persona — BPE process root cause and operational fix framing.

    Parameters
    ----------
    anomaly : dict
        One item from detect_anomalies.detect()
    api_key : str, optional
        Claude API key. Falls back to ANTHROPIC_API_KEY environment variable.

    Returns
    -------
    dict
        Structured analysis: executive_summary, 3 interventions, risk_if_unaddressed
    """
    return _call_claude(SYSTEM_PROMPT_CIA, _build_user_prompt(anomaly), api_key)


def analyse_week(anomaly: dict, api_key: str = None) -> dict:
    """
    Backward-compatible wrapper. Calls the Corporate Chief of Staff persona.
    Use analyse_week_cos / analyse_week_cia for the full dual-persona system.
    """
    return analyse_week_cos(anomaly, api_key)


def run_all(anomalies: list, api_key: str = None) -> list:
    """
    Analyse all flagged weeks with both personas.
    Returns list of dicts with keys 'cos' and 'cia'.
    """
    results = []
    for a in anomalies:
        severity_icon = "🔴" if a["overall_severity"] == "CRITICAL" else "🟡"
        print(f"  {severity_icon} Analysing {a['week_label']} [{a['overall_severity']}]...")
        results.append({
            "week_label": a["week_label"],
            "cos": analyse_week_cos(a, api_key=api_key),
            "cia": analyse_week_cia(a, api_key=api_key),
        })
    return results


if __name__ == "__main__":
    from detect_anomalies import detect

    print("🔍 Running anomaly detection...")
    anomalies = detect()
    print(f"   Found {len(anomalies)} flagged week(s).\n")

    print("🤖 Running dual AI analysis on the most critical week...\n")
    critical = next((a for a in anomalies if a["overall_severity"] == "CRITICAL"), anomalies[0])

    print("── Executive Copilot ────────────────────────────────────────")
    cos = analyse_week_cos(critical)
    print(f"\nEXECUTIVE SUMMARY:\n{cos['executive_summary']}")
    print("\nPRESCRIPTIVE INTERVENTIONS:")
    for i, iv in enumerate(cos["interventions"], 1):
        print(f"\n  [{i}] {iv['title']}")
        print(f"      Action:    {iv['action']}")
        print(f"      Impact:    {iv['expected_impact']}")
    print(f"\nRISK IF UNADDRESSED:\n{cos['risk_if_unaddressed']}")

    print("\n── Operations Copilot ───────────────────────────────────────")
    cia = analyse_week_cia(critical)
    print(f"\nEXECUTIVE SUMMARY:\n{cia['executive_summary']}")
    print("\nPRESCRIPTIVE INTERVENTIONS:")
    for i, iv in enumerate(cia["interventions"], 1):
        print(f"\n  [{i}] {iv['title']}")
        print(f"      Action:    {iv['action']}")
        print(f"      Impact:    {iv['expected_impact']}")
    print(f"\nRISK IF UNADDRESSED:\n{cia['risk_if_unaddressed']}")

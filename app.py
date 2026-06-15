"""
app.py
======
Project Aegis — Prescriptive KPI & Performance Dashboard
Autonomous Operational Governance Agent · B2B Payment Operations

Run with:
    streamlit run app.py

Requires:
    pip install streamlit plotly anthropic pandas

Set your Claude API key:
    export ANTHROPIC_API_KEY="your-key-here"

v3.0 changes:
  - Light theme: #F8F9FA canvas, white cards, #E2E8F0 borders
  - Tab 1 renamed: "Strategic Risk & Governance View" (4 KPIs)
  - Tab 2 renamed: "Process Excellence Delivery View" (7 metrics, adds Invoice Exception Count)
  - KPI cards: 5-line vertical stack (label / value / delta / status dot / SLA)
  - Traffic light status dots only — no coloured metric values
  - Pill subtab chart navigation (one full-width chart at a time per tab)
  - AI trigger: explicit sidebar button replaces auto-fire
  - AI section: always visible at bottom, 40/60 split, persona pill tabs
  - Plotly light theme: #F8F9FA background, #E2E8F0 grid
"""

import streamlit as st
import sqlite3
import plotly.graph_objects as go
import pandas as pd
import os

from detect_anomalies import detect, SLA
from ai_agent import analyse_week_cos, analyse_week_cia
import build_database

# ── Demo mode — serves pre-baked AI responses, no live API calls ──────────────
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() in ("true", "1", "yes")
if DEMO_MODE:
    from demo_responses import DEMO_RESPONSES

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kpi_dashboard.db")

# ── DB auto-init guard (Streamlit Cloud deployment) ───────────────────────────
if not os.path.exists(DB_PATH):
    build_database.build(DB_PATH)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Project Aegis — KPI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS — light theme override ─────────────────────────────────────────
st.markdown("""
<style>
    /* Canvas */
    .stApp { background: #F8F9FA; }

    /* Sidebar */
    section[data-testid="stSidebar"] > div:first-child {
        background: #FFFFFF;
        border-right: 0.5px solid #E2E8F0;
    }

    /* Tab bar */
    .stTabs [data-baseweb="tab-list"] {
        background: #F1F5F9;
        border-radius: 8px;
        padding: 3px;
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        color: #64748B;
        font-size: 0.82rem;
        padding: 6px 14px;
    }
    .stTabs [aria-selected="true"] {
        background: #FFFFFF !important;
        color: #1E293B !important;
        font-weight: 600;
    }

    /* Headings */
    h1, h2, h3 { color: #1E293B !important; }
    p, li { color: #64748B; }

    /* Dividers */
    hr { border-color: #E2E8F0; }

    /* Streamlit metric overrides */
    [data-testid="stMetric"] { background: transparent; }

    /* Pill button shared */
    .pill-row { display: flex; gap: 8px; margin-bottom: 14px; flex-wrap: wrap; }

    /* Tooltip container */
    .sla-row { position: relative; cursor: default; }
    .sla-row .tip {
        display: none;
        position: absolute;
        top: calc(100% + 3px);
        left: 0;
        background: #1E293B;
        color: #F8F9FA;
        font-size: 11px;
        line-height: 1.5;
        padding: 6px 10px;
        border-radius: 6px;
        width: 200px;
        z-index: 999;
        white-space: normal;
    }
    .sla-row:hover .tip { display: block; }
</style>
""", unsafe_allow_html=True)

# ── Light chart defaults ───────────────────────────────────────────────────────
_CHART_BASE = dict(
    plot_bgcolor="#F8F9FA", paper_bgcolor="#F8F9FA",
    font_color="#1E293B", height=320,
    margin=dict(l=0, r=10, t=28, b=0),
)
_AXIS = dict(gridcolor="#E2E8F0", linecolor="#E2E8F0")

# ── Colour palette ─────────────────────────────────────────────────────────────
_DOT_CRITICAL  = "#DC2626"
_DOT_WARNING   = "#EA580C"
_DOT_OK        = "#16A34A"
_DELTA_GOOD    = "#16A34A"
_DELTA_BAD     = "#DC2626"
_DELTA_NEUTRAL = "#D97706"
_CHART_DEFAULT = "#3B82F6"

# Bar chart traffic-light palette (softer tones suited to filled bars)
_BAR_CRITICAL  = "#F87171"   # muted red
_BAR_WARNING   = "#FB923C"   # orange
_BAR_OK        = "#4ADE80"   # green


# ── Data loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    """
    Loads all KPI weeks from the database, joined with operational notes.
    Cached by Streamlit so repeated renders don't re-query SQLite.
    Returns a pandas DataFrame ordered by week_number.

    Uses sqlite3 cursor directly (not pd.read_sql_query) to avoid
    pandas.errors.DatabaseError in pandas 2.2+ which deprecated raw
    DBAPI2 connections passed to read_sql_query.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT k.*, COALESCE(n.notes, '') AS notes
        FROM kpi_weekly k
        LEFT JOIN operational_notes n USING (week_number)
        ORDER BY week_number
    """)
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    conn.close()
    return pd.DataFrame(rows, columns=cols)


@st.cache_data
def load_anomalies():
    """
    Runs the anomaly detection engine and returns flagged weeks.
    Cached so the detection logic only executes once per session.
    """
    return detect(DB_PATH)


def get_anomaly_for_week(anomalies, week_number):
    """Returns the anomaly dict for the given week, or None if the week was clean."""
    return next((a for a in anomalies if a["week_number"] == week_number), None)


# ── Helper: previous row ──────────────────────────────────────────────────────
def get_prev_row(df, selected_week):
    """
    Returns the DataFrame row immediately preceding the selected week.
    Used to compute week-over-week delta values on KPI cards.
    Returns None if the selected week is the first on record.
    """
    df_r = df.reset_index(drop=True)
    pos = df_r.index[df_r.week_number == selected_week].tolist()
    if not pos or pos[0] == 0:
        return None
    return df_r.iloc[pos[0] - 1]


# ── Helper: 12-week rolling window ───────────────────────────────────────────
def get_chart_df(df, selected_week):
    """
    Returns a 12-week rolling window ending at the selected week.
    Charts always show the most relevant context (trailing 12 weeks)
    rather than the full dataset, preventing visual noise.
    """
    df_r = df.reset_index(drop=True)
    pos = df_r.index[df_r.week_number == selected_week].tolist()
    if not pos:
        return df_r.tail(12)
    i = pos[0]
    return df_r.iloc[max(0, i - 11):i + 1]


# ── Helper: WoW delta string + colour ────────────────────────────────────────
def wow_delta(current, prev_val, delta_type, higher_is_better=None):
    """Returns (delta_str, hex_colour)."""
    if prev_val is None:
        return "first week on record", "#94A3B8"

    diff = float(current) - float(prev_val)

    if delta_type == "bps" and abs(diff) < 0.005:
        return "flat vs prior week", "#94A3B8"
    if delta_type in ("count", "volume") and abs(diff) < 0.5:
        return "flat vs prior week", "#94A3B8"

    up = diff > 0
    arrow = "▲" if up else "▼"

    if delta_type == "bps":
        bps = diff * 100
        sign = "+" if bps > 0 else ""
        label = f"{arrow} {sign}{bps:.0f} bps vs prior week"
    elif delta_type == "hours":
        sign = "+" if diff > 0 else ""
        label = f"{arrow} {sign}{diff:.0f} hrs vs prior week"
    elif delta_type == "days":
        sign = "+" if diff > 0 else ""
        label = f"{arrow} {sign}{diff:.1f} days vs prior week"
    elif delta_type == "count":
        sign = "+" if diff > 0 else ""
        label = f"{arrow} {sign}{int(round(diff))} vs prior week"
    elif delta_type == "volume":
        sign = "+" if diff > 0 else ""
        label = f"{arrow} {sign}{int(round(diff)):,} vs prior week"
    else:
        sign = "+" if diff > 0 else ""
        label = f"{arrow} {sign}{diff:.1f} vs prior week"

    if higher_is_better is None:
        colour = _DELTA_NEUTRAL
    elif (up and higher_is_better) or (not up and not higher_is_better):
        colour = _DELTA_GOOD
    else:
        colour = _DELTA_BAD

    return label, colour


# ── Helper: KPI card (5-line vertical stack) ──────────────────────────────────
def kpi_card(col, label, value_str, delta_str, delta_colour,
             on_target, sla_text, severity=None):
    """
    Renders a white card with 5 stacked elements:
      label / value / delta / status dot + text / SLA footer
    severity: "CRITICAL" | "WARNING" | None (on-target)
    """
    if severity == "CRITICAL":
        dot_colour = _DOT_CRITICAL
        status_label = "Critical"
    elif severity == "WARNING":
        dot_colour = _DOT_WARNING
        status_label = "Warning"
    elif severity == "info":
        dot_colour = "#94A3B8"
        status_label = "Tracking"
    else:
        dot_colour = _DOT_OK
        status_label = "On target"

    with col:
        st.markdown(
            f"""
            <div style="background:#fff; border:0.5px solid #E2E8F0; border-radius:12px;
                        padding:14px 16px; display:flex; flex-direction:column; gap:5px;">
                <div style="font-size:10px; color:#94A3B8; text-transform:uppercase;
                            letter-spacing:0.06em;">{label}</div>
                <div style="font-size:28px; font-weight:500; color:#1E293B;
                            line-height:1.1;">{value_str}</div>
                <div style="font-size:11px; color:{delta_colour};">{delta_str}</div>
                <div style="display:flex; align-items:center; gap:6px;">
                    <span style="display:inline-block; width:7px; height:7px; border-radius:50%;
                                 background:{dot_colour}; flex-shrink:0;"></span>
                    <span style="font-size:11px; color:#64748B;">{status_label}</span>
                </div>
                <div style="font-size:10px; color:#94A3B8;">{sla_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _card_severity(on_target, value, metric=None, anomaly_breaches=None):
    """Derive severity string for a KPI card from anomaly breach list."""
    if on_target:
        return None
    if anomaly_breaches:
        for b in anomaly_breaches:
            if b["metric"] == metric:
                return b["severity"]
    return "WARNING"


# ── Helper: marker colours ────────────────────────────────────────────────────
def marker_colours(df_c, crit_set, warn_set, default=_CHART_DEFAULT,
                   crit_colour=None, warn_colour=None):
    cc = crit_colour or _DOT_CRITICAL
    wc = warn_colour or _DOT_WARNING
    return [
        cc if w in crit_set
        else wc if w in warn_set
        else default
        for w in df_c["week_number"]
    ]


# ── Chart builders ────────────────────────────────────────────────────────────
def line_chart(df_c, col, line_col, sla_val, y_range, crit_w, warn_w,
               suffix="%", title=""):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_c["week_label"], y=df_c[col],
        mode="lines+markers",
        line=dict(color=line_col, width=2.5),
        marker=dict(size=7, color=marker_colours(df_c, crit_w, warn_w, line_col)),
    ))
    if sla_val is not None:
        lbl = f"Target {sla_val}{suffix}" if suffix else f"Target {sla_val}"
        fig.add_hline(
            y=sla_val, line_dash="dash", line_color=_DOT_CRITICAL,
            annotation_text=lbl, annotation_position="bottom right",
            annotation_font_color="#94A3B8",
        )
    layout = dict(_CHART_BASE)
    if title:
        layout["title"] = dict(
            text=title,
            font=dict(size=13, color="#1E293B"),
            x=0, xanchor="left", pad=dict(l=0, t=4),
        )
        layout["margin"] = dict(l=0, r=10, t=46, b=0)
    y_axis = dict(_AXIS)
    if y_range:
        y_axis["range"] = list(y_range)
    if suffix == "%":
        y_axis["ticksuffix"] = "%"
    layout["xaxis"] = dict(_AXIS)
    layout["yaxis"] = y_axis
    fig.update_layout(**layout)
    return fig


def bar_chart(df_c, col, def_col, target_val, crit_w, warn_w,
              y_min=0, suffix="", title=""):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_c["week_label"], y=df_c[col],
        marker_color=marker_colours(
            df_c, crit_w, warn_w, _BAR_OK,
            crit_colour=_BAR_CRITICAL, warn_colour=_BAR_WARNING,
        ),
        marker_line_width=0,
    ))
    if target_val is not None:
        fig.add_hline(
            y=target_val, line_dash="dash", line_color=_DOT_CRITICAL,
            annotation_text=f"Target {target_val}{suffix}",
            annotation_font_color="#94A3B8",
        )
    layout = dict(_CHART_BASE)
    if title:
        layout["title"] = dict(
            text=title,
            font=dict(size=13, color="#1E293B"),
            x=0, xanchor="left", pad=dict(l=0, t=4),
        )
        layout["margin"] = dict(l=0, r=10, t=46, b=0)
    layout["xaxis"] = dict(_AXIS)
    layout["yaxis"] = dict(_AXIS, range=[y_min, None])
    if suffix:
        layout["yaxis"]["ticksuffix"] = suffix
    fig.update_layout(**layout)
    return fig


# ── Helper: pill chart subtab buttons ────────────────────────────────────────
def pill_buttons(options, state_key, default):
    """
    Renders a row of pill buttons. Returns the currently active key.
    options: list of (key, label) tuples
    """
    if state_key not in st.session_state:
        st.session_state[state_key] = default

    active = st.session_state[state_key]
    cols = st.columns(len(options))
    for i, (key, label) in enumerate(options):
        is_active = active == key
        bg    = "#1E293B" if is_active else "#F1F5F9"
        color = "#FFFFFF"  if is_active else "#64748B"
        fw    = "600"      if is_active else "400"
        with cols[i]:
            if st.button(
                label,
                key=f"{state_key}_{key}",
                use_container_width=True,
            ):
                st.session_state[state_key] = key
                st.rerun()
            # Overlay style via markdown (button label already set above)
        # Inject CSS to style the just-rendered button
        st.markdown(
            f"""<style>
            div[data-testid="column"]:nth-child({i+1})
            button[kind="secondary"] {{
                background: {bg} !important;
                color: {color} !important;
                font-weight: {fw} !important;
                border: none !important;
                border-radius: 20px !important;
                font-size: 12px !important;
            }}
            </style>""",
            unsafe_allow_html=True,
        )
    return st.session_state[state_key]


# ── AI output renderer ────────────────────────────────────────────────────────
def render_ai_output(result: dict, accent: str = "#7C3AED"):
    # Executive summary
    st.markdown(
        f'<div style="background:#F5F3FF; border-left:3px solid {accent}; border-radius:6px;'
        f'padding:14px 18px; font-size:0.87rem; color:#1E293B; line-height:1.7;'
        f'font-style:italic; margin-bottom:14px;">'
        f'&ldquo;{result["executive_summary"]}&rdquo;</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="font-size:11px; font-weight:600; color:#94A3B8; text-transform:uppercase;'
        'letter-spacing:0.06em; margin-bottom:8px;">Prescriptive interventions</div>',
        unsafe_allow_html=True,
    )

    accent_colours = ["#3B82F6", "#10B981", "#F59E0B"]
    numbers = ["①", "②", "③"]
    for i, iv in enumerate(result["interventions"]):
        c = accent_colours[i % len(accent_colours)]
        n = numbers[i % len(numbers)]
        st.markdown(
            f'<div style="background:#fff; border:0.5px solid #E2E8F0; border-left:3px solid {c};'
            f'border-radius:6px; padding:14px 18px; margin-bottom:10px;">'
            f'<div style="font-weight:600; color:#1E293B; margin-bottom:6px;">{n} {iv["title"]}</div>'
            f'<div style="font-size:0.79rem; color:#64748B; margin-bottom:4px;">'
            f'<strong>Why:</strong> {iv["rationale"]}</div>'
            f'<div style="font-size:0.79rem; color:#1E293B; margin-bottom:4px;">'
            f'<strong>Action:</strong> {iv["action"]}</div>'
            f'<div style="font-size:0.79rem; color:#059669;">'
            f'<strong>Impact:</strong> {iv["expected_impact"]}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    if "risk_if_unaddressed" in result:
        st.markdown(
            f'<div style="background:#FEF2F2; border:1px solid #FECACA; border-radius:6px;'
            f'padding:12px 16px; font-size:0.82rem; color:#7F1D1D; margin-top:4px;">'
            f'⚠ <strong>Risk if unaddressed:</strong> {result["risk_if_unaddressed"]}</div>',
            unsafe_allow_html=True,
        )


# ── Main app ──────────────────────────────────────────────────────────────────
def main():
    df          = load_data()
    anomalies   = load_anomalies()
    anomaly_weeks  = {a["week_number"] for a in anomalies}
    critical_weeks = {a["week_number"] for a in anomalies if a["overall_severity"] == "CRITICAL"}
    warning_weeks  = anomaly_weeks - critical_weeks

    if "ai_cache" not in st.session_state:
        st.session_state.ai_cache = {}

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(
            '<div style="font-size:18px; font-weight:700; color:#1E293B;">Project Aegis</div>',
            unsafe_allow_html=True,
        )
        st.caption("B2B Payment Operations · Governance Agent")
        st.markdown("")

        selected_week = st.selectbox(
            "Select week for analysis",
            options=df["week_number"].tolist(),
            format_func=lambda w: (
                f"🔴 {df[df.week_number == w]['week_label'].values[0]}"
                if w in critical_weeks
                else f"🟡 {df[df.week_number == w]['week_label'].values[0]}"
                if w in anomaly_weeks
                else f"✅ {df[df.week_number == w]['week_label'].values[0]}"
            ),
            index=len(df) - 1,
        )

        st.divider()

        # AI trigger — demo mode or live API
        row_s     = df[df.week_number == selected_week].iloc[0]
        anomaly_s = get_anomaly_for_week(anomalies, selected_week)

        if DEMO_MODE:
            api_key = ""
            st.markdown(
                '<div style="background:#F0FDF4; border:0.5px solid #BBF7D0; border-radius:8px;'
                'padding:10px 12px; font-size:11px; color:#14532D; margin-bottom:4px;">'
                '🟢 <strong>Demo mode</strong><br>'
                'Pre-generated AI briefings are served instantly — no API key required.</div>',
                unsafe_allow_html=True,
            )
            ai_btn_disabled = not anomaly_s
            ai_btn_help = (
                "No anomalies detected for this week — select a flagged week (🔴 or 🟡)"
                if not anomaly_s
                else "Generate dual AI governance briefing for this week"
            )
        else:
            api_key = st.text_input(
                "Claude API Key",
                type="password",
                placeholder="sk-ant-...",
                help="Get yours at console.anthropic.com",
                value=os.getenv("ANTHROPIC_API_KEY", ""),
            )
            ai_btn_disabled = (not anomaly_s) or (not api_key)
            ai_btn_help = (
                "No anomalies detected for this week — select a flagged week (🔴 or 🟡)"
                if not anomaly_s
                else "Enter your Claude API key above to activate"
                if not api_key
                else "Generate dual AI governance briefing for this week"
            )

        if st.button(
            "Generate Executive Governance Briefing",
            disabled=ai_btn_disabled,
            help=ai_btn_help,
            use_container_width=True,
        ):
            st.session_state[f"run_ai_{selected_week}"] = True

        st.divider()

        # SLA reference with hover tooltips
        st.markdown(
            '<div style="font-size:11px; font-weight:600; color:#94A3B8; '
            'text-transform:uppercase; letter-spacing:0.06em; margin-bottom:8px;">'
            'SLA targets</div>',
            unsafe_allow_html=True,
        )

        sla_items = [
            ("Payment accuracy", "≥ 97%",
             "% of invoices paid correctly first time, without correction or adjustment."),
            ("First-pass rate", "≥ 95%",
             "% of invoices that clear processing without any exception flag or manual touch."),
            ("Dispute rate", "< 3%",
             "% of invoices formally disputed by logistics companies in the period."),
            ("Exception rate", "< 2%",
             "% of invoices flagged for manual review due to data or matching errors."),
            ("Invoice SLA Breaches", "= 0",
             "Count of invoices where the contractual 7-day payment deadline was missed."),
            ("Cycle time", "< 3 days",
             "Average calendar days from invoice receipt to payment release."),
            ("Processing hrs", "< 200 hrs",
             "Weekly staff hours spent on manual invoice handling and correction."),
            ("Stuck invoices", "< 20",
             "Invoices stalled with no action taken for more than 48 hours."),
            ("Dispute resolution", "≥ 90%",
             "% of open disputes resolved within the contractual 10 business-day window."),
        ]

        for kpi_name, target, tip_text in sla_items:
            st.markdown(
                f'<div class="sla-row" style="display:flex; justify-content:space-between;'
                f'align-items:center; padding:4px 0; border-bottom:0.5px solid #F1F5F9;">'
                f'<span style="font-size:11px; color:#64748B;">{kpi_name}</span>'
                f'<span style="font-size:11px; font-weight:600; color:#1E293B;">{target}</span>'
                f'<div class="tip">{tip_text}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Load selected week data ───────────────────────────────────────────────
    row      = df[df.week_number == selected_week].iloc[0]
    prev     = get_prev_row(df, selected_week)
    anomaly  = get_anomaly_for_week(anomalies, selected_week)
    df_chart = get_chart_df(df, selected_week)
    breaches = {b["metric"]: b for b in anomaly["breaches"]} if anomaly else {}

    def sev(metric, on_target):
        if on_target:
            return None
        b = breaches.get(metric)
        return b["severity"] if b else "WARNING"

    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown(
        '<h2 style="margin-bottom:2px;">Project Aegis — Prescriptive KPI Dashboard</h2>'
        '<p style="color:#94A3B8; margin-top:0; font-size:13px;">'
        'Autonomous Operational Governance Agent · B2B Payment Operations</p>',
        unsafe_allow_html=True,
    )

    if DEMO_MODE:
        st.markdown(
            '<div style="background:#FFFBEB; border:0.5px solid #FDE68A; border-radius:8px;'
            'padding:10px 16px; font-size:12px; color:#78350F; margin-bottom:12px;">'
            '🔍 <strong>Portfolio demo</strong> &nbsp;·&nbsp; '
            'Select any flagged week (🔴 or 🟡) and press <strong>Generate Executive Governance '
            'Briefing</strong> to see the dual AI persona analysis. AI responses are pre-generated '
            '— no API key required.</div>',
            unsafe_allow_html=True,
        )

    # ── Status banner ─────────────────────────────────────────────────────────
    if anomaly:
        sev_label = anomaly["overall_severity"]
        border_col = _DOT_CRITICAL if sev_label == "CRITICAL" else _DOT_WARNING
        dot_col    = border_col
        icon       = "🔴" if sev_label == "CRITICAL" else "🟡"
        msg = (
            f'{icon} <strong>{sev_label}</strong> &nbsp;·&nbsp; '
            f'{len(anomaly["breaches"])} breach(es) detected &nbsp;·&nbsp; '
            f'Week in focus: <strong>{row["week_label"]}</strong>'
        )
    else:
        border_col = _DOT_OK
        dot_col    = _DOT_OK
        msg = (
            f'✅ <strong>ALL CLEAR</strong> &nbsp;·&nbsp; '
            f'All KPIs within SLA targets &nbsp;·&nbsp; '
            f'Week in focus: <strong>{row["week_label"]}</strong>'
        )

    st.markdown(
        f'<div style="background:#fff; border-left:4px solid {border_col}; border-radius:6px;'
        f'padding:12px 18px; margin-bottom:18px; color:#1E293B; font-size:0.88rem;">'
        f'{msg}</div>',
        unsafe_allow_html=True,
    )

    # ── Page tabs ─────────────────────────────────────────────────────────────
    tab1, tab2 = st.tabs([
        "Strategic Risk & Governance View",
        "Process Excellence Delivery View",
    ])

    # ━━━━ TAB 1 — Strategic Risk & Governance View ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab1:
        st.markdown(
            '<p style="font-size:12px; color:#94A3B8; margin-bottom:14px;">'
            'Strategic risk indicators for executive governance and board reporting.</p>',
            unsafe_allow_html=True,
        )

        c1, c2, c3, c4 = st.columns(4)

        # SLA Breach Count
        on_t = row.sla_breach_count == 0
        d, dc = wow_delta(row.sla_breach_count,
                          prev.sla_breach_count if prev is not None else None,
                          "count", higher_is_better=False)
        kpi_card(c1, "Invoice SLA Breach", str(int(row.sla_breach_count)),
                 d, dc, on_t, "Contractual target: 0", sev("sla_breach_count", on_t))

        # Payment Accuracy
        on_t = row.payment_accuracy_rate >= 97
        d, dc = wow_delta(row.payment_accuracy_rate,
                          prev.payment_accuracy_rate if prev is not None else None,
                          "bps", higher_is_better=True)
        kpi_card(c2, "Payment Accuracy", f"{row.payment_accuracy_rate:.1f}%",
                 d, dc, on_t, "SLA ≥ 97%", sev("payment_accuracy_rate", on_t))

        # Dispute Rate
        on_t = row.dispute_rate < 3
        d, dc = wow_delta(row.dispute_rate,
                          prev.dispute_rate if prev is not None else None,
                          "bps", higher_is_better=False)
        kpi_card(c3, "Dispute Rate", f"{row.dispute_rate:.1f}%",
                 d, dc, on_t, "Target < 3%", sev("dispute_rate", on_t))

        # Invoice Volume
        d, dc = wow_delta(row.invoice_volume,
                          prev.invoice_volume if prev is not None else None,
                          "volume", higher_is_better=None)
        kpi_card(c4, "Invoice Volume", f"{int(row.invoice_volume):,}",
                 d, dc, True, "Baseline ~8,500 / week", None)

        # Chart area
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div style="background:#fff; border:0.5px solid #E2E8F0; border-radius:12px;'
            'padding:16px 20px;">',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="font-size:11px; font-weight:600; color:#94A3B8; text-transform:uppercase;'
            'letter-spacing:0.06em; margin-bottom:12px;">12-week trend</div>',
            unsafe_allow_html=True,
        )

        t1_options = [("sla", "Invoice SLA Breaches"), ("pay", "Payment Accuracy"), ("dis", "Dispute Rate")]
        active_t1  = pill_buttons(t1_options, "t1_chart", "sla")

        if active_t1 == "sla":
            st.plotly_chart(
                bar_chart(df_chart, "sla_breach_count", _CHART_DEFAULT, 0,
                          critical_weeks, warning_weeks, y_min=0,
                          title="Invoice SLA Breaches — count of invoices where the 7-day payment deadline was missed"),
                use_container_width=True,
            )
        elif active_t1 == "pay":
            st.plotly_chart(
                line_chart(df_chart, "payment_accuracy_rate", _CHART_DEFAULT,
                           97, [85, 100], critical_weeks, warning_weeks,
                           title="Payment Accuracy Rate — % of invoices paid correctly on first attempt (SLA ≥ 97%)"),
                use_container_width=True,
            )
        elif active_t1 == "dis":
            st.plotly_chart(
                line_chart(df_chart, "dispute_rate", "#F59E0B",
                           3, [0, 10], critical_weeks, warning_weeks,
                           title="Dispute Rate — % of invoices formally disputed by logistics companies (target < 3%)"),
                use_container_width=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ━━━━ TAB 2 — Process Excellence Delivery View ━━━━━━━━━━━━━━━━━━━━━━━━━━━
    with tab2:
        st.markdown(
            '<p style="font-size:12px; color:#94A3B8; margin-bottom:14px;">'
            'Process health and capacity indicators for operations management and BPE teams.</p>',
            unsafe_allow_html=True,
        )

        b1, b2, b3, b4 = st.columns(4)
        b5, b6, b7, b8 = st.columns(4)

        # First-Pass Resolution
        on_t = row.first_pass_resolution >= 95
        d, dc = wow_delta(row.first_pass_resolution,
                          prev.first_pass_resolution if prev is not None else None,
                          "bps", higher_is_better=True)
        kpi_card(b1, "First-Pass Resolution", f"{row.first_pass_resolution:.1f}%",
                 d, dc, on_t, "SLA ≥ 95%", sev("first_pass_resolution", on_t))

        # Processing Cycle Time
        on_t = row.processing_cycle_days < 3
        d, dc = wow_delta(row.processing_cycle_days,
                          prev.processing_cycle_days if prev is not None else None,
                          "days", higher_is_better=False)
        kpi_card(b2, "Processing Cycle Time", f"{row.processing_cycle_days:.1f} days",
                 d, dc, on_t, "Target < 3 days", sev("processing_cycle_days", on_t))

        # Invoice Exception Rate
        on_t = row.invoice_exception_rate < 2
        d, dc = wow_delta(row.invoice_exception_rate,
                          prev.invoice_exception_rate if prev is not None else None,
                          "bps", higher_is_better=False)
        kpi_card(b3, "Invoice Exception Rate", f"{row.invoice_exception_rate:.1f}%",
                 d, dc, on_t, "Target < 2%", sev("invoice_exception_rate", on_t))

        # Invoice Exception Count (derived)
        exc_count    = int(row.invoice_exception_count)
        exc_target   = round(0.02 * row.invoice_volume)
        on_t         = exc_count < exc_target
        prev_exc     = int(prev.invoice_exception_count) if prev is not None else None
        d, dc = wow_delta(exc_count, prev_exc, "count", higher_is_better=False)
        kpi_card(b4, "Invoice Exception Count", str(exc_count),
                 d, dc, on_t, f"Target < {exc_target} invoices", sev("invoice_exception_rate", on_t))

        # Stuck Invoice Count
        on_t = row.stuck_invoice_count <= 20
        d, dc = wow_delta(row.stuck_invoice_count,
                          prev.stuck_invoice_count if prev is not None else None,
                          "count", higher_is_better=False)
        kpi_card(b5, "Stuck Invoice Count", str(int(row.stuck_invoice_count)),
                 d, dc, on_t, "Target < 20", sev("stuck_invoice_count", on_t))

        # Dispute Resolution Rate
        on_t = row.dispute_resolution_rate >= 90
        d, dc = wow_delta(row.dispute_resolution_rate,
                          prev.dispute_resolution_rate if prev is not None else None,
                          "bps", higher_is_better=True)
        kpi_card(b6, "Dispute Resolution Rate", f"{row.dispute_resolution_rate:.1f}%",
                 d, dc, on_t, "SLA ≥ 90%", sev("dispute_resolution_rate", on_t))

        # Open Dispute Count (volume tracker — no target, context metric)
        d, dc = wow_delta(row.dispute_count,
                          prev.dispute_count if prev is not None else None,
                          "count", higher_is_better=False)
        kpi_card(b8, "Open Disputes", str(int(row.dispute_count)),
                 d, dc, None, "Volume tracker", "info")

        # Manual Processing Hours
        on_t = row.manual_processing_hours < 200
        d, dc = wow_delta(row.manual_processing_hours,
                          prev.manual_processing_hours if prev is not None else None,
                          "hours", higher_is_better=False)
        kpi_card(b7, "Manual Processing Hours", f"{row.manual_processing_hours:.0f} hrs",
                 d, dc, on_t, "Target < 200 hrs", sev("manual_processing_hours", on_t))

        # Chart area
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div style="background:#fff; border:0.5px solid #E2E8F0; border-radius:12px;'
            'padding:16px 20px;">',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="font-size:11px; font-weight:600; color:#94A3B8; text-transform:uppercase;'
            'letter-spacing:0.06em; margin-bottom:12px;">12-week trend</div>',
            unsafe_allow_html=True,
        )

        t2_options = [
            ("fpr", "First-Pass Rate"),
            ("cyc", "Cycle Time"),
            ("exc", "Exception Rate"),
            ("exn", "Exception Count"),
            ("stk", "Stuck Invoices"),
            ("ddr", "Dispute Resolution"),
            ("hrs", "Processing Hours"),
            ("dcn", "Dispute Count"),
        ]
        active_t2 = pill_buttons(t2_options, "t2_chart", "fpr")

        if active_t2 == "fpr":
            st.plotly_chart(
                line_chart(df_chart, "first_pass_resolution", "#7C3AED",
                           95, [80, 100], critical_weeks, warning_weeks,
                           title="First-Pass Resolution Rate — % of invoices cleared without exception or manual touch (SLA ≥ 95%)"),
                use_container_width=True,
            )
        elif active_t2 == "cyc":
            st.plotly_chart(
                line_chart(df_chart, "processing_cycle_days", "#0EA5E9",
                           3, [0, 8], critical_weeks, warning_weeks,
                           suffix="", title="Processing Cycle Time — average calendar days from invoice receipt to payment release (target < 3 days)"),
                use_container_width=True,
            )
        elif active_t2 == "exc":
            st.plotly_chart(
                line_chart(df_chart, "invoice_exception_rate", "#F59E0B",
                           2, [0, 8], critical_weeks, warning_weeks,
                           title="Invoice Exception Rate — % of invoices flagged for manual review due to data or matching errors (target < 2%)"),
                use_container_width=True,
            )
        elif active_t2 == "exn":
            st.plotly_chart(
                bar_chart(df_chart, "invoice_exception_count", "#F59E0B",
                          None, critical_weeks, warning_weeks, y_min=0,
                          title="Invoice Exception Count — number of invoices routed to manual review this week (derived from exception rate × volume)"),
                use_container_width=True,
            )
        elif active_t2 == "stk":
            st.plotly_chart(
                bar_chart(df_chart, "stuck_invoice_count", "#EF4444",
                          20, critical_weeks, warning_weeks, y_min=0,
                          title="Stuck Invoice Count — invoices stalled with no action taken for more than 48 hours (target < 20)"),
                use_container_width=True,
            )
        elif active_t2 == "ddr":
            st.plotly_chart(
                line_chart(df_chart, "dispute_resolution_rate", "#059669",
                           90, [50, 100], critical_weeks, warning_weeks,
                           title="Dispute Resolution Rate — % of open disputes resolved within the 10-business-day contractual window (SLA ≥ 90%)"),
                use_container_width=True,
            )
        elif active_t2 == "hrs":
            st.plotly_chart(
                bar_chart(df_chart, "manual_processing_hours", _CHART_DEFAULT,
                          200, critical_weeks, warning_weeks, y_min=0, suffix=" hrs",
                          title="Manual Processing Hours — total staff hours spent on manual invoice handling and correction this week (target < 200 hrs)"),
                use_container_width=True,
            )
        elif active_t2 == "dcn":
            st.plotly_chart(
                bar_chart(df_chart, "dispute_count", "#F59E0B",
                          None, critical_weeks, warning_weeks, y_min=0,
                          title="Open Dispute Count — number of invoices formally disputed by logistics companies this week (volume tracker)"),
                use_container_width=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ━━━━ AI Governance Agent ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    st.markdown(
        '<hr style="border-color:#E2E8F0; margin:28px 0 20px;"/>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:15px; font-weight:700; color:#1E293B; margin-bottom:4px;">'
        'AI Governance Agent</div>'
        '<div style="font-size:12px; color:#94A3B8; margin-bottom:18px;">'
        'Dual persona analysis: Executive Copilot (financial risk) &amp; '
        'Operations Copilot (process root cause)</div>',
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([2, 3])

    # Left panel — operational notes + breach list
    with col_left:
        st.markdown(
            '<div style="background:#fff; border:0.5px solid #E2E8F0; border-radius:12px;'
            'padding:16px 18px; height:100%;">',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="font-size:11px; font-weight:600; color:#94A3B8; text-transform:uppercase;'
            'letter-spacing:0.06em; margin-bottom:10px;">Operational notes</div>',
            unsafe_allow_html=True,
        )

        notes_text = row["notes"] if row["notes"] else "No operational notes recorded for this week."
        st.markdown(
            f'<div style="font-size:0.83rem; color:#1E293B; line-height:1.65;">'
            f'{notes_text}</div>',
            unsafe_allow_html=True,
        )

        if anomaly and anomaly["breaches"]:
            st.markdown(
                '<div style="font-size:11px; font-weight:600; color:#94A3B8; text-transform:uppercase;'
                'letter-spacing:0.06em; margin:14px 0 8px;">Breaches detected</div>',
                unsafe_allow_html=True,
            )
            for b in anomaly["breaches"]:
                b_col   = _DOT_CRITICAL if b["severity"] == "CRITICAL" else _DOT_WARNING
                b_icon  = "🔴" if b["severity"] == "CRITICAL" else "🟡"
                b_type  = b["type"].replace("_", " ").title()
                st.markdown(
                    f'<div style="background:#F8F9FA; border-left:3px solid {b_col};'
                    f'border-radius:4px; padding:7px 10px; margin-bottom:6px; font-size:0.78rem;'
                    f'color:#1E293B; line-height:1.5;">'
                    f'{b_icon} <strong>{b_type}</strong><br>{b["detail"]}</div>',
                    unsafe_allow_html=True,
                )
        elif not anomaly:
            st.markdown(
                '<div style="background:#F0FDF4; border-left:3px solid #16A34A; border-radius:4px;'
                'padding:10px 12px; font-size:0.82rem; color:#14532D; margin-top:12px;">'
                '✅ All KPIs within SLA targets this week.</div>',
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # Right panel — AI output
    with col_right:
        cache_key_cos = f"week_{selected_week}_cos"
        cache_key_cia = f"week_{selected_week}_cia"
        both_cached   = (cache_key_cos in st.session_state.ai_cache and
                         cache_key_cia in st.session_state.ai_cache)
        run_requested = st.session_state.get(f"run_ai_{selected_week}", False)

        if not anomaly:
            st.markdown(
                '<div style="background:#fff; border:0.5px solid #E2E8F0; border-radius:12px;'
                'padding:24px 20px; text-align:center;">'
                '<div style="font-size:28px; margin-bottom:8px;">✅</div>'
                '<div style="font-size:0.88rem; color:#1E293B; font-weight:600; margin-bottom:4px;">'
                'All KPIs on target</div>'
                '<div style="font-size:0.82rem; color:#94A3B8;">'
                'Select a flagged week (🔴 or 🟡) from the sidebar to activate the governance agent.</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        elif not api_key and not DEMO_MODE:
            st.markdown(
                '<div style="background:#fff; border:1px dashed #E2E8F0; border-radius:12px;'
                'padding:24px 20px; text-align:center;">'
                '<div style="font-size:28px; margin-bottom:8px;">🔑</div>'
                '<div style="font-size:0.88rem; color:#1E293B; font-weight:600; margin-bottom:4px;">'
                'API key required</div>'
                '<div style="font-size:0.82rem; color:#94A3B8;">'
                'Enter your Claude API key in the sidebar to activate the dual AI persona analysis.</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        elif run_requested and not both_cached:
            if DEMO_MODE:
                # Serve pre-baked responses instantly — no API call
                demo = DEMO_RESPONSES.get(selected_week)
                if demo:
                    st.session_state.ai_cache[cache_key_cos] = demo["cos"]
                    st.session_state.ai_cache[cache_key_cia] = demo["cia"]
                else:
                    st.warning("No demo response available for this week.")
                st.session_state[f"run_ai_{selected_week}"] = False
                st.rerun()
            else:
                with st.spinner("Generating dual AI governance briefing…"):
                    try:
                        if cache_key_cos not in st.session_state.ai_cache:
                            st.session_state.ai_cache[cache_key_cos] = analyse_week_cos(
                                anomaly, api_key=api_key
                            )
                        if cache_key_cia not in st.session_state.ai_cache:
                            st.session_state.ai_cache[cache_key_cia] = analyse_week_cia(
                                anomaly, api_key=api_key
                            )
                        st.session_state[f"run_ai_{selected_week}"] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")

        elif not both_cached:
            # Anomaly present, API key present, button not yet clicked
            st.markdown(
                '<div style="background:#fff; border:0.5px solid #E2E8F0; border-radius:12px;'
                'padding:24px 20px; text-align:center;">'
                '<div style="font-size:28px; margin-bottom:8px;">🤖</div>'
                '<div style="font-size:0.88rem; color:#1E293B; font-weight:600; margin-bottom:4px;">'
                'Ready to analyse</div>'
                '<div style="font-size:0.82rem; color:#94A3B8;">'
                'Press <strong>Generate Executive Governance Briefing</strong> in the sidebar '
                'to run the dual AI persona analysis for this week.</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        if both_cached:
            cos_result = st.session_state.ai_cache[cache_key_cos]
            cia_result = st.session_state.ai_cache[cache_key_cia]

            ai_tab1, ai_tab2 = st.tabs([
                "🏛 Executive Copilot",
                "⚙ Operations Copilot",
            ])

            with ai_tab1:
                st.markdown(
                    '<div style="font-size:10px; font-weight:600; color:#7C3AED; text-transform:uppercase;'
                    'letter-spacing:0.06em; margin-bottom:10px;">'
                    'Executive Oversight · Financial Risk & Governance</div>',
                    unsafe_allow_html=True,
                )
                render_ai_output(cos_result, accent="#7C3AED")

            with ai_tab2:
                st.markdown(
                    '<div style="font-size:10px; font-weight:600; color:#059669; text-transform:uppercase;'
                    'letter-spacing:0.06em; margin-bottom:10px;">'
                    'Operations Delivery · Process Root Cause & Interventions</div>',
                    unsafe_allow_html=True,
                )
                render_ai_output(cia_result, accent="#059669")


if __name__ == "__main__":
    main()

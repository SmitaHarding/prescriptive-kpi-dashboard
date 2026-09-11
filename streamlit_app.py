"""
streamlit_app.py
================
Holding page for Project Aegis while v2 is rebuilt.

This file is the entry point Streamlit Community Cloud serves. It is replaced
by the v2 application entry point (importing from prototype/) when the
prototype ships. The app itself is never deleted and never redeployed to a new
URL — the custom subdomain is released permanently if the app is removed.
"""

import streamlit as st

st.set_page_config(
    page_title="Project Aegis — v2 in development",
    page_icon="🧭",
    layout="centered",
)

st.markdown(
    """
    <style>
      #MainMenu, footer {visibility: hidden;}
      .block-container {max-width: 640px; padding-top: 5rem;}
      .aegis-eyebrow {font-size: 12px; letter-spacing: .14em; text-transform: uppercase;
                      opacity: .55; margin-bottom: 12px;}
      .aegis-title {font-size: 36px; font-weight: 700; letter-spacing: -.022em;
                    line-height: 1.08; margin: 0 0 6px;}
      .aegis-sub {font-size: 17px; opacity: .6; margin: 0 0 4px;}
      .aegis-body {font-size: 16px; line-height: 1.72; margin: 0 0 18px;}
      .aegis-foot {font-size: 13px; opacity: .5; margin-top: 32px;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="aegis-eyebrow">Operational governance agent</div>',
            unsafe_allow_html=True)
st.markdown('<div class="aegis-title">Project Aegis</div>', unsafe_allow_html=True)
st.markdown('<div class="aegis-sub">v2 in development</div>', unsafe_allow_html=True)

st.divider()

st.markdown(
    '<p class="aegis-body">v1 shipped in June and was subsequently audited against a '
    'governance process I have since formalised. It is being rebuilt from the frame up: '
    'the decision the system exists to improve, requirements written as executable '
    'evaluations, then the prototype.</p>',
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="aegis-body">The method and the rebuild notes are being published to the '
    '<a href="https://github.com/SmitaHarding/prescriptive-kpi-dashboard">repository</a> '
    'as the work proceeds. v1 is preserved there on the <code>archive/v1</code> branch.</p>',
    unsafe_allow_html=True,
)

st.markdown('<p class="aegis-foot">September 2026 · Smita Harding</p>',
            unsafe_allow_html=True)

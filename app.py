import streamlit as st

from auth import render_login_interface
from components.ui import metric_card, render_sidebar, setup_page
from styles import apply_styles


setup_page("Influence Guard AI")
apply_styles()

if not st.session_state.get("user"):
    render_login_interface()
    st.stop()

render_sidebar()

st.markdown(
    """
    <section class="hero">
        <div class="hero-content">
            <div class="eyebrow">Sentinel AI</div>
            <h1>Influence Guard AI</h1>
            <p class="hero-copy">
                AI-Powered Influencer Fraud Detection Platform for identifying fake creators,
                suspicious engagement, audience inflation, and low-authenticity YouTube channels.
            </p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.write("")
cta1, cta2, cta3, _ = st.columns([1.2, 1.2, 1.2, 2.4])
with cta1:
    st.page_link("pages/2_Creator_Analysis.py", label="Analyze Creator")
with cta2:
    st.page_link("pages/1_Dashboard.py", label="Open Dashboard")
with cta3:
    st.page_link("pages/4_Database_Records.py", label="View Records")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    metric_card("Detection Layer", "24/7", "YouTube fraud monitoring")
with col2:
    metric_card("Risk Signals", "6+", "Engagement, growth, views")
with col3:
    metric_card("ML Core", "IForest", "Anomaly detection ready")
with col4:
    metric_card("Data Store", "MySQL", "Persistent audit history")

st.markdown(
    """
    <div class="glass home-operational-overview">
        <div class="section-title">Operational Workflow</div>
        <p class="muted">
            Enter a YouTube channel ID or channel URL, fetch live YouTube Data API metrics,
            score the creator against fraud heuristics, persist the audit to MySQL, and generate
            executive-ready reports from the same backend records.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

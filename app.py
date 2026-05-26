import pandas as pd
import streamlit as st

from auth import render_login_interface
from components.ui import get_history_df, metric_card, render_sidebar, setup_page
from database import load_history
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

session_df = get_history_df()
db_df = pd.DataFrame()

try:
    db_df = load_history()
    if "status" in db_df.columns:
        db_df["status"] = db_df["status"].replace({"Genuine": "Real"})
except Exception as exc:
    st.info(f"Historical audit persistence is unavailable: {exc}")

history = db_df if not db_df.empty else session_df

st.write("")
cta1, cta2, cta3, _ = st.columns([1.2, 1.2, 1.2, 2.4])
with cta1:
    st.page_link("pages/2_Creator_Analysis.py", label="Analyze Creator")
with cta2:
    st.page_link("pages/1_Dashboard.py", label="Open Dashboard")
with cta3:
    st.page_link("pages/4_Database_Records.py", label="View Records")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

if history.empty:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Creators", "0", "Start an audit")
    with col2:
        metric_card("Fake Detected", "0", "Run a channel scan")
    with col3:
        metric_card("Suspicious", "0", "Awaiting data")
    with col4:
        metric_card("Real Influencers", "0", "Live reports pending")

    st.markdown(
        """
        <div class="glass home-operational-overview">
            <div class="section-title">Ready for live analysis</div>
            <p class="muted">
                Run a creator audit to populate dynamic telemetry, fraud scoring, and historical dashboards.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    total = len(history)
    fake = int((history[history["status"] == "Fake"]).shape[0])
    suspicious = int((history[history["status"] == "Suspicious"]).shape[0])
    real = int(history[history["status"].isin(["Real", "Genuine"])].shape[0])
    avg_fraud = round(float(history.get("fraud_score", pd.Series([0])).mean()), 1)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Creators", f"{total}", "Live audit history")
    with col2:
        metric_card("Fake Detected", f"{fake}", f"{fake / total:.0%} of creators")
    with col3:
        metric_card("Suspicious", f"{suspicious}", "Manual review queue")
    with col4:
        metric_card("Avg. Fraud Score", f"{avg_fraud}%", "Historical risk average")

    last_result = (
        history.sort_values("analyzed_at", ascending=False).iloc[0]
        if "analyzed_at" in history.columns
        else history.iloc[-1]
    )
    st.markdown(
        """
        <div class="glass home-operational-overview">
            <div class="section-title">Latest Audit</div>
            <p class="muted">
                Last scanned creator: <strong>{channel_name}</strong>, status <strong>{status}</strong>, subscribers <strong>{subs}</strong>, views <strong>{views}</strong>, fraud score <strong>{fraud}%</strong>.
            </p>
        </div>
        """.format(
            channel_name=last_result.get("channel_name", "Unknown"),
            status=last_result.get("status", "Unknown"),
            subs=f"{int(last_result.get('subscribers', 0)):,}",
            views=f"{int(last_result.get('views', 0)):,}",
            fraud=round(float(last_result.get("fraud_score", 0)), 1),
        ),
        unsafe_allow_html=True,
    )

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

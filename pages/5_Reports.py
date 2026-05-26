import pandas as pd
import streamlit as st

from auth import require_login
from components.ui import get_history_df, render_sidebar, setup_page, simple_pdf, status_badge
from database import load_history
from insights import generate_detailed_insight
from styles import apply_styles


setup_page("Reports | Influence Guard AI")
apply_styles()
require_login()
render_sidebar()

st.title("Reports")
st.caption("Generate creator audit reports and fraud summaries from live analysis history.")

try:
    db_df = load_history()
except Exception:
    db_df = pd.DataFrame()

session_df = get_history_df()
df = db_df if not db_df.empty else session_df

if df.empty:
    st.warning("No creator analysis is available for reporting yet.")
    st.stop()

if "status" in df.columns:
    df["status"] = df["status"].replace({"Genuine": "Real"})

names = df["channel_name"].astype(str).tolist() if "channel_name" in df.columns else []
selected_name = st.selectbox("Creator audit report", names)
row = df[df["channel_name"].astype(str) == selected_name].iloc[0].to_dict()

insight, recommendation = generate_detailed_insight(
    row.get("fraud_score", 0),
    row.get("engagement", 0),
    row.get("subscribers", 0),
    row.get("videos", 0),
)

st.markdown(
    f"""
    <div class="glass">
        <div class="section-title">{row.get("channel_name", "Creator")} Audit</div>
        {status_badge(row.get("status"))}
        <p class="muted">Subscribers: {int(row.get("subscribers", 0)):,}</p>
        <p class="muted">Views: {int(row.get("views", 0)):,}</p>
        <p class="muted">Videos: {int(row.get("videos", 0)):,}</p>
        <p class="muted">Engagement: {row.get("engagement", 0)}%</p>
        <p class="muted">Fraud score: {row.get("fraud_score", 0)}%</p>
        <div class="divider"></div>
        <p class="muted">{insight}</p>
        <p class="muted">{recommendation}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

lines = [
    f"Creator: {row.get('channel_name', 'Creator')}",
    f"Status: {row.get('status', 'Unknown')}",
    f"Subscribers: {int(row.get('subscribers', 0)):,}",
    f"Views: {int(row.get('views', 0)):,}",
    f"Videos: {int(row.get('videos', 0)):,}",
    f"Engagement: {row.get('engagement', 0)}%",
    f"Fraud score: {row.get('fraud_score', 0)}%",
    f"Insight: {insight}",
    f"Recommendation: {recommendation}",
]
pdf = simple_pdf("Influence Guard AI Report", lines)
st.download_button("Download PDF Report", pdf, f"{selected_name}_audit_report.pdf", "application/pdf")

summary = df["status"].value_counts().rename_axis("status").reset_index(name="count")
st.subheader("Fraud Summary")
st.dataframe(summary, use_container_width=True, hide_index=True)

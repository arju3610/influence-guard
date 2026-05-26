import pandas as pd
import plotly.express as px
import streamlit as st

from auth import require_login
from components.ui import apply_plot_theme, format_number, get_history_df, metric_card, render_sidebar, setup_page
from database import load_history
from styles import apply_styles


setup_page("Dashboard | Influence Guard AI")
apply_styles()
require_login()
render_sidebar()

st.title("Threat Intelligence Dashboard")
st.caption("Analyze uploaded influencer data to uncover audience quality, engagement patterns, and growth insights.")

session_df = get_history_df()
db_df = pd.DataFrame()

try:
    db_df = load_history()
    if "status" in db_df.columns:
        db_df["status"] = db_df["status"].replace({"Genuine": "Real"})
except Exception as exc:
    st.info(f"Database history is unavailable right now: {exc}")

df = db_df if not db_df.empty else session_df

if df.empty:
    st.warning("No creator analyses found yet. Run a channel scan from Creator Analysis.")
    st.stop()

status_col = "status"
total = len(df)
fake = int((df[status_col] == "Fake").sum())
suspicious = int((df[status_col] == "Suspicious").sum())
real = int(df[status_col].isin(["Real", "Genuine"]).sum())
avg_fraud = float(df.get("fraud_score", pd.Series([0])).mean())

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Total Creators", format_number(total), "Analyzed accounts")
with c2:
    metric_card("Fake Detected", format_number(fake), f"{fake / total:.0%} of records")
with c3:
    metric_card("Suspicious", format_number(suspicious), "Manual review queue")
with c4:
    metric_card("Real Influencers", format_number(real), f"Avg risk {avg_fraud:.1f}%")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

left, right = st.columns([1.45, 1])

with left:
    status_counts = df[status_col].replace({"Genuine": "Real"}).value_counts().reset_index()
    status_counts.columns = ["Status", "Creators"]
    fig = px.bar(
        status_counts,
        x="Status",
        y="Creators",
        color="Status",
        color_discrete_map={"Fake": "#ff4d6d", "Suspicious": "#facc15", "Real": "#28e98f"},
        title="Fraud Analytics by Status",
    )
    st.plotly_chart(apply_plot_theme(fig), use_container_width=True)

with right:
    fig = px.pie(
        status_counts,
        names="Status",
        values="Creators",
        hole=0.58,
        color="Status",
        color_discrete_map={"Fake": "#ff4d6d", "Suspicious": "#facc15", "Real": "#28e98f"},
        title="Authenticity Mix",
    )
    fig.update_traces(textfont=dict(color="#ffffff"))
    st.plotly_chart(apply_plot_theme(fig), use_container_width=True)

trend_cols = [col for col in ["channel_name", "engagement", "fraud_score", "subscribers", "views", "status"] if col in df.columns]
recent = df[trend_cols].head(8).copy()

st.subheader("Recent Creator Analyses")
st.dataframe(recent, use_container_width=True, hide_index=True)

if {"channel_name", "engagement", "fraud_score"}.issubset(df.columns):
    fig = px.scatter(
        df,
        x="engagement",
        y="fraud_score",
        size="subscribers" if "subscribers" in df.columns else None,
        color=status_col,
        hover_name="channel_name",
        color_discrete_map={"Fake": "#ff4d6d", "Suspicious": "#facc15", "Real": "#28e98f", "Genuine": "#28e98f"},
        title="Engagement vs Fraud Risk",
    )
    st.plotly_chart(apply_plot_theme(fig), use_container_width=True)

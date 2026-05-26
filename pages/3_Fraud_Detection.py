import pandas as pd
import streamlit as st

from auth import require_login
from components.ui import format_number, metric_card, render_sidebar, risk_gauge, setup_page, status_badge
from model import get_account_analysis, load_data, process_data
from styles import apply_styles


setup_page("Fraud Detection | Influence Guard AI")
apply_styles()
require_login()
render_sidebar()

st.title("ML Fraud Detection")
st.caption("Run the existing CSV data.")

uploaded = st.file_uploader("Upload influencer activity CSV", type=["csv"])

if uploaded is not None:
    raw_df = load_data(uploaded)
    with st.spinner("Running Isolation Forest anomaly analysis..."):
        processed = process_data(raw_df)
    st.session_state["ml_processed_df"] = processed
elif "ml_processed_df" in st.session_state:
    processed = st.session_state["ml_processed_df"]
else:
    st.markdown(
        """
        <div class="glass">
            <div class="section-title">Model Input Required</div>
            <p class="muted">Upload a CSV with account_id, follower_count, likes, comments, shares, saves, and followers_gained columns.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

if processed.empty:
    st.error("The uploaded file could not be processed.")
    st.stop()

status_options = ["All", "Real", "Fake", "Suspicious"]
available_statuses = processed.get("account_status", pd.Series(dtype=str)).dropna().unique().tolist()
filter_options = ["All"] + [status for status in status_options[1:] if status in available_statuses]
selected_status = st.selectbox("Filter by account status", filter_options)

if selected_status == "All":
    filtered = processed.copy()
else:
    filtered = processed[processed["account_status"] == selected_status].copy()

if filtered.empty:
    st.warning(f"No {selected_status.lower()} accounts found in this upload.")
    st.stop()

fake_count = int((filtered["account_status"] == "Fake").sum())
suspicious_count = int((filtered["account_status"] == "Suspicious").sum())
real_count = int((filtered["account_status"] == "Real").sum())
total_fake_followers = int(filtered["fake_followers"].sum())
risk_score = round(((fake_count * 100) + (suspicious_count * 55)) / max(len(filtered), 1), 1)
confidence = min(99, 72 + int(len(filtered) ** 0.5))

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Fraud Probability", f"{risk_score}%", f"{selected_status} view")
with c2:
    metric_card("Confidence", f"{confidence}%", "Model evidence")
with c3:
    metric_card("Fake Followers", format_number(total_fake_followers), "Estimated inflation")
with c4:
    metric_card("Accounts Flagged", format_number(fake_count + suspicious_count), "Fake or suspicious")

left, right = st.columns([1, 1.2])
with left:
    st.plotly_chart(risk_gauge(risk_score, "ML Risk Score"), use_container_width=True)

with right:
    selected = None
    if "account_id" in filtered.columns:
        account_id = st.selectbox("Inspect account", filtered["account_id"].astype(str).tolist())
        selected = get_account_analysis(filtered, account_id)

    if selected:
        st.markdown(
            f"""
            <div class="glass">
                <div class="section-title">Detection Explanation</div>
                {status_badge(selected["status"])}
                <p class="muted">Followers: {selected["followers"]:,}</p>
                <p class="muted">Engagement ratio: {selected["engagement_ratio"]:.4f}</p>
                <p class="muted">Growth rate: {selected["growth_rate"]:.4f}</p>
                <p class="muted">Estimated fake followers: {selected["fake_followers"]:,}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.subheader("AI Analysis Summary")
summary = (
    "High-risk accounts combine anomaly detection, low engagement ratios, rapid growth, "
    "and estimated fake follower ratios. Suspicious accounts should receive manual review before campaign approval."
)
st.markdown(f"<div class='glass'><p class='muted'>{summary}</p></div>", unsafe_allow_html=True)

st.caption(f"Showing {len(filtered)} of {len(processed)} processed accounts.")

display_cols = [
    col
    for col in [
        "account_id",
        "follower_count",
        "engagement_ratio",
        "growth_rate",
        "fake_followers",
        "influence_score",
        "account_status",
    ]
    if col in filtered.columns
]
st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)

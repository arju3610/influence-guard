import pandas as pd
import streamlit as st

from auth import require_login
from components.ui import render_sidebar, setup_page, status_badge
from database import load_history
from styles import apply_styles


setup_page("Database Records | Influence Guard AI")
apply_styles()
require_login()
render_sidebar()

st.title("Database Records")
st.caption("Search, filter, paginate, and export creator's data from audit history .")

try:
    df = load_history()
except Exception as exc:
    st.error(f"Unable to load MySQL records: {exc}")
    st.stop()

if df.empty:
    st.warning("No database records found yet.")
    st.stop()

if "status" in df.columns:
    df["status"] = df["status"].replace({"Genuine": "Real"})

left, mid, right = st.columns([1.5, 1, 1])
with left:
    search = st.text_input("Search creators", placeholder="Channel name")
with mid:
    available_statuses = df.get("status", pd.Series(dtype=str)).dropna().unique().tolist()
    status_options = ["All"] + [status for status in ["Real", "Fake", "Suspicious"] if status in available_statuses]
    selected_status = st.selectbox("Fraud status", status_options)
with right:
    page_size = st.selectbox("Rows per page", [10, 25, 50, 100], index=1)

filtered = df.copy()
if search and "channel_name" in filtered.columns:
    filtered = filtered[filtered["channel_name"].astype(str).str.contains(search, case=False, na=False)]
if selected_status != "All" and "status" in filtered.columns:
    filtered = filtered[filtered["status"] == selected_status]

pages = max(1, (len(filtered) + page_size - 1) // page_size)
page = st.number_input("Page", min_value=1, max_value=pages, value=1, step=1)
start = (page - 1) * page_size
page_df = filtered.iloc[start : start + page_size]

def badge_column(row):
    return status_badge(row.get("status"))

st.markdown(f"<p class='muted'>Showing {len(page_df)} of {len(filtered)} matching records.</p>", unsafe_allow_html=True)
st.dataframe(page_df, use_container_width=True, hide_index=True)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Export CSV", csv, "influence_guard_records.csv", "text/csv")

if "status" in page_df.columns:
    badges = "".join(
        f"<p>{row.get('channel_name', 'Creator')}: {badge_column(row)}</p>"
        for _, row in page_df.head(8).iterrows()
    )
    st.markdown(f"<div class='glass'><div class='section-title'>Status Indicators</div>{badges}</div>", unsafe_allow_html=True)

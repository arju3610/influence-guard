import html

import streamlit as st

from auth import require_login
from components.ui import (
    format_number,
    metric_card,
    render_sidebar,
    risk_gauge,
    setup_page,
    status_badge,
)
from database import save_creator
from insights import generate_detailed_insight
from styles import apply_styles
from youtube_api import parse_channel_input, get_channel_data

setup_page("Creator Analysis | Influence Guard AI")
apply_styles()
require_login()
render_sidebar()

st.title("Creator Analysis")
st.caption("Analyze a live YouTube channel.")

with st.form("creator_analysis_form"):
    channel_value = st.text_input(
        "YouTube Channel URL or Channel ID",
        placeholder="https://www.youtube.com/@creator or UCxxxxxxxxxxxxxxxxxxx",
    )
    submitted = st.form_submit_button("Run AI Audit", type="primary")

if submitted:
    _, parsed_value = parse_channel_input(channel_value)
    if not parsed_value:
        st.error("Enter a valid YouTube channel URL, handle, or channel ID.")
    else:
        with st.spinner("Fetching creator telemetry and scoring authenticity..."):
            try:
                result = get_channel_data(parsed_value)
            except Exception as exc:
                st.error(
                    f"An unexpected error occurred during API communication: {exc}"
                )
                result = None

        if result is None:
            st.error(
                "Channel not found or the API request failed. Check the URL, Channel ID, or API credentials."
            )
        else:
            st.session_state["last_result"] = result
            st.session_state.setdefault("history", []).append(result)
            try:
                save_creator(result)
                st.success("Analysis complete.")
            except Exception as exc:
                st.warning(f"Analysis complete, but database save failed: {exc}")

result = st.session_state.get("last_result")

if not result:
    st.markdown(
        """
        <div class="glass">
            <div class="section-title">Awaiting Channel Scan</div>
            <p class="muted">The dashboard will populate with live subscriber, view, engagement, and fraud-risk signals after an audit runs.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

fallback_thumb = "https://placehold.co/192x192/0b1023/16d9ff?text=IG"
thumb = html.escape(result.get("thumbnail") or fallback_thumb, quote=True)
fallback_thumb = html.escape(fallback_thumb, quote=True)
creator = html.escape(result.get("channel_name", "Unknown Creator"))

st.markdown(
    f"""
    <div class="glass creator-header">
        <img class="creator-avatar" src="{thumb}" alt="{creator}" referrerpolicy="no-referrer" onerror="this.src='{fallback_thumb}'" />
        <div>
            <div class="section-title">{creator}</div>
            {status_badge(result.get("status"))}
            <p class="muted">Live YouTube API signal profile</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card(
        "Subscribers", format_number(result.get("subscribers")), "Audience size"
    )
with c2:
    metric_card("Total Views", format_number(result.get("views")), "Lifetime views")
with c3:
    metric_card("Video Count", format_number(result.get("videos")), "Published uploads")
with c4:
    metric_card(
        "Engagement Rate", f"{result.get('engagement', 0)}%", "Avg views / subscribers"
    )

left, right = st.columns([1, 1])
with left:
    st.plotly_chart(risk_gauge(result.get("fraud_score", 0)), use_container_width=True)
with right:
    insight, recommendation = generate_detailed_insight(
        result.get("fraud_score", 0),
        result.get("engagement", 0),
        result.get("subscribers", 0),
        result.get("videos", 0),
    )
    st.markdown(
        f"""
        <div class="glass creator-analysis-summary">
            <div class="section-title">AI Analysis Summary</div>
            <p class="muted">{html.escape(insight)}</p>
            <div class="divider"></div>
            <p class="muted">{html.escape(recommendation)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

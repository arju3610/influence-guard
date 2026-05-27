import streamlit as st
from youtube_api import get_channel_data, parse_channel_input
from database import save_creator
from styles import apply_styles

st.set_page_config(layout="wide")
apply_styles()

st.title("📺 YouTube Analytics")

channel_id = st.text_input("Enter YouTube Channel ID", placeholder="e.g., UC1234567890")

if st.button("Analyze Channel", type="primary"):

    if not channel_id.strip():
        st.error("Please enter a valid Channel ID")
    else:
        _, parsed_id = parse_channel_input(channel_id)
        if not parsed_id:
            st.error(
                "Invalid YouTube channel format. Please enter a valid URL, handle, or ID."
            )
            st.stop()

        with st.spinner("Analyzing channel..."):
            result = get_channel_data(parsed_id)

        if result is None:
            st.error("Channel not found or invalid ID. Please check the Channel ID.")

        else:

            st.session_state["last_result"] = result

            save_creator(result)

            # Update history in session
            if "history" not in st.session_state:
                st.session_state["history"] = []
            st.session_state["history"].append(result)

            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(result["thumbnail"], width=150, caption=result["channel_name"])

            with col2:
                st.subheader(result["channel_name"])
                st.markdown(f"**Status:** {result['status']}")

            st.markdown("---")

            # Metrics with better styling
            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("Subscribers", f"{result['subscribers']:,}")

            with c2:
                st.metric("Total Views", f"{result['views']:,}")

            with c3:
                st.metric("Videos", f"{result['videos']:,}")

            with c4:
                st.metric("Engagement Rate", f"{result['engagement']}%")

            st.markdown("---")

            # Fraud Analysis
            st.subheader("🔍 Fraud Risk Analysis")
            progress_color = (
                "#ff4757"
                if result["fraud_score"] > 70
                else "#ffa502" if result["fraud_score"] > 40 else "#2ed573"
            )
            st.progress(result["fraud_score"] / 100)
            st.metric("Fraud Risk Score", f"{result['fraud_score']}%")

            if result["status"] == "Fake":
                st.error("🚨 High probability of fake audience detected!")

            elif result["status"] == "Suspicious":
                st.warning(
                    "⚠️ Suspicious activity detected. Manual review recommended."
                )

            else:
                st.success("✅ Genuine influencer with healthy engagement.")

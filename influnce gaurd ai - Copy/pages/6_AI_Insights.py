import streamlit as st
import pandas as pd
from insights import generate_detailed_insight
from styles import apply_styles

st.set_page_config(layout="wide")
apply_styles()

st.title("🧠 AI Insights")

# CHECK HISTORY
if "history" not in st.session_state or len(st.session_state["history"]) == 0:
    st.warning("Analyze creators first from YouTube Analytics page")
else:
    # LAST ANALYZED CREATOR
    last_result = st.session_state["history"][-1]

    fraud_score = last_result['fraud_score']
    engagement = last_result['engagement']
    subscribers = last_result['subscribers']
    views = last_result['views']
    videos = last_result['videos']
    status = last_result['status']
    creator = last_result['channel_name']

    # ---------------- HEADER CARD ----------------
    st.markdown(f"""
    <div class='glass'>
        <h2>🤖 AI Analysis Report</h2>
        <h3>{creator}</h3>
        <p>Analysis completed on {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📈 Key Metrics")

    # Metrics with icons
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Subscribers", f"{subscribers:,}", delta=f"{engagement}% engagement")

    with c2:
        st.metric("Total Views", f"{views:,}")

    with c3:
        st.metric("Engagement Rate", f"{engagement}%")

    with c4:
        st.metric("Fraud Score", f"{fraud_score}%")

    st.markdown("---")

    # ---------------- RISK ANALYSIS ----------------
    st.subheader("🔍 Risk Assessment")

    risk_level = "Low" if fraud_score < 40 else "Medium" if fraud_score < 70 else "High"
    risk_color = "#2ed573" if risk_level == "Low" else "#ffa502" if risk_level == "Medium" else "#ff4757"

    st.markdown(f"<div style='background: {risk_color}20; border-left: 5px solid {risk_color}; padding: 15px; border-radius: 10px;'><strong>Risk Level: {risk_level}</strong></div>", unsafe_allow_html=True)

    st.progress(fraud_score / 100)

    # ---------------- AI INSIGHTS ----------------
    st.subheader("🧠 AI-Powered Insights")

    insight, recommendation = generate_detailed_insight(fraud_score, engagement, subscribers, videos)

    st.markdown(f"""
    <div class='glass'>
        <h4>📊 Analysis Summary</h4>
        <p>{insight}</p>

        <h4>💡 Recommendations</h4>
        <p>{recommendation}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------------- DETAILED BREAKDOWN ----------------
    st.subheader("📋 Detailed Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Engagement Analysis:**")
        if engagement < 1:
            st.error("Very low engagement - potential bot activity")
        elif engagement < 3:
            st.warning("Below average engagement for subscriber count")
        else:
            st.success("Healthy engagement levels")

    with col2:
        st.markdown("**Growth Indicators:**")
        if subscribers > 100000 and engagement < 2:
            st.error("Large audience with poor engagement - suspicious")
        elif videos > 1000 and engagement < 1:
            st.warning("High video count with low engagement")
        else:
            st.info("Growth patterns appear normal")

    # ---------------- FINAL STATUS ----------------
    st.subheader("🎯 Final Assessment")

    if status == "Fake":
        st.error("🚨 **HIGH RISK**: This channel shows strong indicators of fake engagement. Avoid collaboration without further verification.")
    elif status == "Suspicious":
        st.warning("⚠️ **MEDIUM RISK**: Some suspicious patterns detected. Consider additional checks before partnership.")
    else:
        st.success("✅ **LOW RISK**: This appears to be a genuine channel with authentic engagement.")
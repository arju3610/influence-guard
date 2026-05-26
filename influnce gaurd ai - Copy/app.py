import streamlit as st
from styles import apply_styles

st.set_page_config(
    page_title="Influence Guard AI",
    layout="wide"
)

apply_styles()

st.sidebar.title("🛡️ Influence Guard AI")

st.sidebar.page_link(
    "app.py",
    label="🏠 Home"
)

st.sidebar.page_link(
    "pages/1_Dashboard.py",
    label="📊 Dashboard"
)

st.sidebar.page_link(
    "pages/2_Influencers.py",
    label="👥 Influencers"
)

st.sidebar.page_link(
    "pages/3_Detection.py",
    label="🚨 Detection"
)

st.sidebar.page_link(
    "pages/4_YouTube_Analytics.py",
    label="📺 YouTube Analytics"
)

st.title("🛡️ Influence Guard AI")

st.markdown("""
### AI-Powered Influencer Intelligence Platform

Analyze real-world YouTube creators using:
- YouTube API
- Fraud Detection AI
- Engagement Analysis
- Risk Scoring
- Real-Time Analytics
""")
import streamlit as st
import pandas as pd
import plotly.express as px
from styles import apply_styles

st.set_page_config(layout="wide")
apply_styles()

st.title("📊 Dashboard")

if "history" not in st.session_state:

    st.warning("Analyze creators from YouTube Analytics page")

else:

    df = pd.DataFrame(st.session_state["history"])

    total = len(df)

    fake = len(df[df['status'] == "Fake"])
    suspicious = len(df[df['status'] == "Suspicious"])
    genuine = len(df[df['status'] == "Genuine"])

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"<div class='metric-card'><div>📊 Total Analyzed</div><div class='kpi'>{total}</div></div>", unsafe_allow_html=True)

    with c2:
        st.markdown(f"<div class='metric-card'><div>🚨 Fake Accounts</div><div class='kpi'>{fake}</div></div>", unsafe_allow_html=True)

    with c3:
        st.markdown(f"<div class='metric-card'><div>⚠️ Suspicious</div><div class='kpi'>{suspicious}</div></div>", unsafe_allow_html=True)

    with c4:
        st.markdown(f"<div class='metric-card'><div>✅ Genuine</div><div class='kpi'>{genuine}</div></div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])

    with col1:

        fig = px.bar(
            x=["Fake", "Suspicious", "Genuine"],
            y=[fake, suspicious, genuine],
            color=["Fake", "Suspicious", "Genuine"],
            color_discrete_map={
                "Fake": "#ef4444",
                "Suspicious": "#facc15",
                "Genuine": "#22c55e"
            },
            title="Influencer Status Analysis"
        )

        fig.update_layout(
            plot_bgcolor="#0f172a",
            paper_bgcolor="#0f172a",
            font_color="white",
            showlegend=False,
            xaxis_title="",
            yaxis_title="Number of Accounts"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        fig2 = px.pie(
            values=[fake, suspicious, genuine],
            names=["Fake", "Suspicious", "Genuine"],
        )
        st.plotly_chart(fig2, use_container_width=True)
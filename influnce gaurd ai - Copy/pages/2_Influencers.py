import streamlit as st
import pandas as pd
from styles import apply_styles

st.set_page_config(layout="wide")
apply_styles()

st.title("👥 Influencers")

if "history" not in st.session_state:

    st.warning("No influencers analyzed yet")

else:

    df = pd.DataFrame(st.session_state["history"])

    def color_status(val):

        if val == "Fake":
            return "color:red;font-weight:bold"

        elif val == "Suspicious":
            return "color:yellow;font-weight:bold"

        return "color:lime;font-weight:bold"

    styled_df = df[[
        'channel_name',
        'subscribers',
        'engagement',
        'status'
    ]].style.map(
        color_status,
        subset=['status']
    )

    st.dataframe(
        styled_df,
        use_container_width=True
    )
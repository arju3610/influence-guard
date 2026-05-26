import streamlit as st
import pandas as pd
from styles import apply_styles

st.set_page_config(layout="wide")
apply_styles()

st.title("🚨 Detection Results")

if "history" not in st.session_state:

    st.warning("Analyze creators first")

else:

    df = pd.DataFrame(st.session_state["history"])

    fake_df = df[df['status'] != "Genuine"]

    st.dataframe(
        fake_df,
        use_container_width=True
    )
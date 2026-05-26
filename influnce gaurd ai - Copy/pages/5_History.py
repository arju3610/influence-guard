import streamlit as st
from database import load_history
from styles import apply_styles

st.set_page_config(layout="wide")
apply_styles()

st.title("📜 Analysis History")

history = load_history()

st.dataframe(
    history,
    use_container_width=True
)

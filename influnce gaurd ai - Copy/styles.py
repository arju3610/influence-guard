import streamlit as st


def apply_styles():

    st.markdown("""
    <style>

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        font-family: 'Inter', sans-serif;
    }

    .glass {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 25px;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .glass:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    }

    .kpi {
        font-size: 48px;
        font-weight: bold;
        margin-top: 15px;
        background: linear-gradient(45deg, #00d4ff, #090979);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .metric-card {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
    }

    .status-fake {
        color: #ff4757;
        font-weight: bold;
    }

    .status-suspicious {
        color: #ffa502;
        font-weight: bold;
    }

    .status-genuine {
        color: #2ed573;
        font-weight: bold;
    }

    .sidebar .sidebar-content {
        background: rgba(15,23,42,0.9);
    }

    h1, h2, h3 {
        color: #ffffff;
        font-weight: 600;
    }

    .stButton>button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }

    .stTextInput>div>div>input {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
        color: white;
        padding: 10px;
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
    }

    </style>
    """, unsafe_allow_html=True)
import streamlit as st


def apply_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        :root {
            --bg: #070914;
            --panel: rgba(12, 18, 37, 0.74);
            --panel-strong: rgba(17, 25, 51, 0.92);
            --stroke: rgba(120, 171, 255, 0.22);
            --text: #f7fbff;
            --muted: #9fb1d1;
            --cyan: #16d9ff;
            --blue: #4d7cff;
            --purple: #a855f7;
            --green: #28e98f;
            --yellow: #facc15;
            --red: #ff4d6d;
        }

        .stApp {
            background:
                radial-gradient(circle at 10% 10%, rgba(22, 217, 255, 0.17), transparent 28%),
                radial-gradient(circle at 90% 0%, rgba(168, 85, 247, 0.16), transparent 32%),
                linear-gradient(135deg, #070914 0%, #0b1023 48%, #090d1a 100%);
            color: var(--text);
            font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        .block-container {
            padding-top: 1.35rem;
            padding-bottom: 3rem;
            max-width: 1380px;
        }

        [data-testid="stSidebar"] {
            background: rgba(5, 9, 22, 0.88);
            border-right: 1px solid rgba(120, 171, 255, 0.16);
        }

        [data-testid="stSidebarNav"] {
            display: none;
        }

        [data-testid="stSidebar"] * {
            color: #eaf3ff;
        }

        h1, h2, h3, h4, h5, h6, p, label, span {
            letter-spacing: 0;
        }

        h1 {
            font-size: clamp(2.2rem, 6vw, 4.75rem);
            line-height: 0.98;
            font-weight: 800;
        }

        h2, h3 {
            color: var(--text);
        }

        .muted {
            color: var(--muted);
        }

        .hero {
            position: relative;
            overflow: hidden;
            min-height: 560px;
            border: 1px solid rgba(120, 171, 255, 0.2);
            border-radius: 8px;
            padding: clamp(28px, 6vw, 72px);
            background:
                linear-gradient(115deg, rgba(9, 14, 31, 0.95), rgba(11, 19, 42, 0.72)),
                repeating-linear-gradient(90deg, rgba(22, 217, 255, 0.08) 0 1px, transparent 1px 64px),
                repeating-linear-gradient(0deg, rgba(168, 85, 247, 0.055) 0 1px, transparent 1px 64px);
            box-shadow: 0 24px 90px rgba(0, 0, 0, 0.42), inset 0 1px 0 rgba(255,255,255,0.06);
        }

        .hero:after {
            content: "";
            position: absolute;
            right: -12%;
            top: 8%;
            width: min(52vw, 680px);
            height: min(52vw, 680px);
            background:
                linear-gradient(120deg, rgba(22,217,255,0.28), rgba(168,85,247,0.08)),
                conic-gradient(from 180deg, rgba(22,217,255,0.0), rgba(22,217,255,0.65), rgba(168,85,247,0.38), rgba(22,217,255,0.0));
            clip-path: polygon(50% 0, 100% 25%, 86% 82%, 50% 100%, 14% 82%, 0 25%);
            opacity: 0.74;
            filter: drop-shadow(0 0 52px rgba(22,217,255,0.28));
            animation: scanPulse 6s ease-in-out infinite;
        }

        .hero-content {
            position: relative;
            z-index: 2;
            max-width: 760px;
        }

        .auth-spacer {
            min-height: clamp(28px, 8vh, 96px);
        }

        .auth-header {
            text-align: center;
            padding: 30px 24px 18px;
            margin: 0 auto 14px;
            max-width: 620px;
            background: linear-gradient(180deg, rgba(17, 25, 51, 0.76), rgba(10, 15, 32, 0.72));
            border: 1px solid var(--stroke);
            border-radius: 8px;
            backdrop-filter: blur(18px);
            box-shadow: 0 18px 60px rgba(0, 0, 0, 0.26), inset 0 1px 0 rgba(255,255,255,0.045);
        }

        .auth-header h1 {
            margin: 18px 0 0;
            font-size: clamp(2rem, 3vw, 2.8rem);
            line-height: 1.1;
            overflow-wrap: normal;
            word-break: keep-all;
        }

        .auth-header .hero-copy {
            margin: 14px auto 0;
            font-size: 1rem;
            line-height: 1.6;
        }

        .eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 12px;
            border: 1px solid rgba(22,217,255,0.32);
            border-radius: 999px;
            background: rgba(22,217,255,0.08);
            color: #b8f4ff;
            font-size: 0.84rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .hero-copy {
            margin: 18px 0 28px;
            max-width: 650px;
            color: #c9d8f1;
            font-size: 1.14rem;
            line-height: 1.75;
        }

        .glass, .metric-card, .chart-panel, .table-panel {
            background: linear-gradient(180deg, rgba(17, 25, 51, 0.76), rgba(10, 15, 32, 0.72));
            border: 1px solid var(--stroke);
            border-radius: 8px;
            backdrop-filter: blur(18px);
            box-shadow: 0 18px 60px rgba(0, 0, 0, 0.26), inset 0 1px 0 rgba(255,255,255,0.045);
        }

        .glass {
            padding: 22px;
            margin-bottom: 18px;
        }

        .metric-card {
            min-height: 132px;
            padding: 18px;
            transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
        }

        .metric-card:hover {
            transform: translateY(-3px);
            border-color: rgba(22,217,255,0.42);
            box-shadow: 0 22px 70px rgba(22, 217, 255, 0.1);
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.84rem;
            font-weight: 700;
            text-transform: uppercase;
        }

        .kpi {
            margin-top: 12px;
            font-size: clamp(1.8rem, 4vw, 2.75rem);
            font-weight: 800;
            background: linear-gradient(90deg, #f7fbff, #16d9ff 52%, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .metric-delta {
            margin-top: 6px;
            color: #b9c9e7;
            font-size: 0.88rem;
        }

        .status-pill {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 92px;
            padding: 7px 11px;
            border-radius: 999px;
            font-weight: 800;
            font-size: 0.78rem;
            text-transform: uppercase;
            border: 1px solid currentColor;
        }

        .status-real, .status-genuine {
            color: var(--green);
            background: rgba(40, 233, 143, 0.12);
        }

        .status-suspicious {
            color: var(--yellow);
            background: rgba(250, 204, 21, 0.12);
        }

        .status-fake {
            color: var(--red);
            background: rgba(255, 77, 109, 0.12);
        }

        .stButton > button, .stDownloadButton > button {
            border: 1px solid rgba(22,217,255,0.38);
            border-radius: 8px;
            background: linear-gradient(90deg, rgba(22,217,255,0.95), rgba(168,85,247,0.92));
            color: #ffffff;
            font-weight: 800;
            min-height: 42px;
            box-shadow: 0 12px 36px rgba(22,217,255,0.16);
            transition: transform 160ms ease, box-shadow 160ms ease, filter 160ms ease;
        }

        .stButton > button:hover, .stDownloadButton > button:hover {
            color: #ffffff;
            transform: translateY(-2px);
            filter: brightness(1.08);
            box-shadow: 0 16px 44px rgba(168,85,247,0.22);
        }

        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(120,171,255,0.22);
            color: #ffffff;
            border-radius: 8px;
        }

        .stDataFrame {
            border: 1px solid rgba(120,171,255,0.16);
            border-radius: 8px;
            overflow: hidden;
        }

        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.045);
            border: 1px solid rgba(120,171,255,0.16);
            border-radius: 8px;
            padding: 16px;
        }

        .creator-header {
            display: flex;
            align-items: center;
            gap: 18px;
        }

        .creator-avatar {
            width: 96px;
            height: 96px;
            border-radius: 8px;
            object-fit: cover;
            border: 1px solid rgba(22,217,255,0.45);
            box-shadow: 0 0 34px rgba(22,217,255,0.18);
        }

        .creator-analysis-summary {
            margin-top: 18px;
        }

        .home-operational-overview {
            margin-top: 18px;
        }

        .section-title {
            margin: 0 0 12px;
            font-size: 1.25rem;
            font-weight: 800;
        }

        .divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(22,217,255,0.35), transparent);
            margin: 22px 0;
        }

        @keyframes scanPulse {
            0%, 100% { transform: rotate(0deg) scale(1); opacity: 0.62; }
            50% { transform: rotate(7deg) scale(1.035); opacity: 0.86; }
        }

        @media (max-width: 780px) {
            .auth-header {
                padding: 24px 18px 16px;
            }
            .auth-header h1 {
                font-size: 2rem;
            }
            .hero {
                min-height: 620px;
            }
            .hero:after {
                top: auto;
                bottom: -12%;
                right: -18%;
                width: 84vw;
                height: 84vw;
            }
            .creator-header {
                align-items: flex-start;
                flex-direction: column;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

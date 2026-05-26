import html
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


STATUS_MAP = {
    "real": ("Real", "status-real"),
    "genuine": ("Real", "status-genuine"),
    "suspicious": ("Suspicious", "status-suspicious"),
    "fake": ("Fake", "status-fake"),
}


def setup_page(title="Influence Guard AI", icon="shield"):
    st.set_page_config(page_title=title, page_icon="🛡️", layout="wide")


def render_sidebar():
    with st.sidebar:
        st.markdown("### Influence Guard AI")
        st.caption("Fraud intelligence command center")
        user = st.session_state.get("user")
        if user:
            name = html.escape(user.get("full_name", "User"))
            st.markdown(
                f"""
                <div class="glass">
                    <div class="section-title">Welcome, {name}</div>
                    <p class="muted">
                        Monitor creator authenticity, detect suspicious engagement, and keep campaign decisions backed by data.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("---")
        st.page_link("app.py", label="Home")
        st.page_link("pages/1_Dashboard.py", label="Dashboard")
        st.page_link("pages/2_Creator_Analysis.py", label="Creator Analysis")
        st.page_link("pages/3_Fraud_Detection.py", label="Fraud Detection")
        st.page_link("pages/4_Database_Records.py", label="Database Records")
        st.page_link("pages/5_Reports.py", label="Reports")
        st.markdown("---")
        if user and st.button("Logout", use_container_width=True):
            from auth import logout

            logout()
        st.caption(f"Session: {datetime.now().strftime('%d %b %Y, %H:%M')}")


def status_badge(status):
    key = str(status or "Real").strip().lower()
    label, cls = STATUS_MAP.get(key, (str(status or "Real"), "status-real"))
    return f"<span class='status-pill {cls}'>{html.escape(label)}</span>"


def metric_card(label, value, delta=None):
    delta_html = f"<div class='metric-delta'>{html.escape(str(delta))}</div>" if delta else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{html.escape(str(label))}</div>
            <div class="kpi">{html.escape(str(value))}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def glass_panel(title=None, body=None):
    title_html = f"<div class='section-title'>{html.escape(title)}</div>" if title else ""
    body_html = body or ""
    st.markdown(f"<div class='glass'>{title_html}{body_html}</div>", unsafe_allow_html=True)


def format_number(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "0"

    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return f"{value:,.0f}"


def normalize_status(value):
    value = str(value or "Real").strip()
    return "Real" if value.lower() == "genuine" else value


def get_history_df():
    rows = st.session_state.get("history", [])
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    if "status" in df.columns:
        df["status"] = df["status"].map(normalize_status)
    return df


def apply_plot_theme(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#eaf3ff", family="Inter"),
        margin=dict(l=18, r=18, t=48, b=18),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(gridcolor="rgba(120,171,255,0.12)", zerolinecolor="rgba(120,171,255,0.18)")
    fig.update_yaxes(gridcolor="rgba(120,171,255,0.12)", zerolinecolor="rgba(120,171,255,0.18)")
    return fig


def risk_gauge(score, title="Fraud Risk Score"):
    score = max(0, min(100, int(score or 0)))
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "%", "font": {"size": 42, "color": "#f7fbff"}},
            title={"text": title, "font": {"size": 18, "color": "#c9d8f1"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#9fb1d1"},
                "bar": {"color": "#16d9ff"},
                "bgcolor": "rgba(255,255,255,0.04)",
                "borderwidth": 1,
                "bordercolor": "rgba(120,171,255,0.22)",
                "steps": [
                    {"range": [0, 40], "color": "rgba(40,233,143,0.26)"},
                    {"range": [40, 70], "color": "rgba(250,204,21,0.26)"},
                    {"range": [70, 100], "color": "rgba(255,77,109,0.28)"},
                ],
            },
        )
    )
    return apply_plot_theme(fig)


def simple_pdf(title, lines):
    safe_lines = [str(line).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") for line in lines]
    content = ["BT", "/F1 22 Tf", "72 760 Td", f"({title}) Tj", "/F1 11 Tf"]
    for line in safe_lines:
        content.append("0 -22 Td")
        content.append(f"({line[:96]}) Tj")
    content.append("ET")
    stream = "\n".join(content).encode("latin-1", "replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for idx, obj in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf.extend(f"{idx} 0 obj\n".encode())
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode())
    pdf.extend(f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode())
    return bytes(pdf)

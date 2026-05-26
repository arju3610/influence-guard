import hashlib
import hmac
import os
import time
from datetime import datetime

import streamlit as st

from database import get_connection


HASH_ITERATIONS = 260_000
USER_WORKSPACE_KEYS = ("history", "last_result", "ml_processed_df")


def _hash_password(password, salt=None):
    salt = salt or os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        HASH_ITERATIONS,
    ).hex()
    return f"pbkdf2_sha256${HASH_ITERATIONS}${salt}${digest}"


def _verify_password(password, stored_hash):
    try:
        algorithm, iterations, salt, expected = stored_hash.split("$", 3)
    except ValueError:
        return False

    if algorithm != "pbkdf2_sha256":
        return False

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        int(iterations),
    ).hex()
    return hmac.compare_digest(digest, expected)


def ensure_users_table():
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        full_name VARCHAR(120) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login_at DATETIME NULL
    )
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
    finally:
        conn.close()


def create_user(full_name, email, password):
    ensure_users_table()
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        if cursor.fetchone():
            return False, "An account already exists for this email."

        cursor.execute(
            """
            INSERT INTO users (full_name, email, password_hash)
            VALUES (%s, %s, %s)
            """,
            (full_name.strip(), email.strip().lower(), _hash_password(password)),
        )
        conn.commit()
        return True, "Welcome! Logging you in..."
    finally:
        conn.close()


def authenticate_user(email, password):
    ensure_users_table()
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, full_name, email, password_hash FROM users WHERE email = %s",
            (email.strip().lower(),),
        )
        user = cursor.fetchone()
        if not user or not _verify_password(password, user["password_hash"]):
            return None

        cursor.execute(
            "UPDATE users SET last_login_at = %s WHERE id = %s",
            (datetime.now(), user["id"]),
        )
        conn.commit()
        return {"id": user["id"], "full_name": user["full_name"], "email": user["email"]}
    finally:
        conn.close()


def clear_user_workspace_state():
    for key in USER_WORKSPACE_KEYS:
        st.session_state.pop(key, None)


def go_home():
    try:
        st.switch_page("app.py")
    except Exception:
        st.rerun()


def logout():
    clear_user_workspace_state()
    st.session_state.pop("user", None)
    go_home()


def render_login_interface():
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {
            display: none;
        }

        section[data-testid="stSidebarContent"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='auth-spacer'></div>", unsafe_allow_html=True)
    _, center, _ = st.columns([0.7, 1.8, 0.7])

    with center:
        st.markdown(
            """
            <div class="auth-header">
                <div class="eyebrow">Secure Access</div>
                <h1>Influence Guard AI</h1>
                <p class="hero-copy">
                    Sign in to access creator analysis, fraud detection records, and audit reports.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        login_tab, register_tab = st.tabs(["Login", "Create Account"])

        with login_tab:
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", type="primary")

            if submitted:
                if not email or not password:
                    st.error("Enter both email and password.")
                else:
                    try:
                        user = authenticate_user(email, password)
                    except Exception as exc:
                        st.error(f"Login failed because the database is unavailable: {exc}")
                    else:
                        if user:
                            clear_user_workspace_state()
                            st.session_state["user"] = {
                                "id": user["id"],
                                "full_name": user["full_name"],
                                "email": user["email"],
                            }
                            go_home()
                        else:
                            st.error("Invalid email or password.")

        with register_tab:
            with st.form("register_form"):
                full_name = st.text_input("Full name")
                email = st.text_input("Account email", placeholder="you@example.com")
                password = st.text_input("Create password", type="password")
                confirm = st.text_input("Confirm password", type="password")
                submitted = st.form_submit_button("Create Account", type="primary")

            if submitted:
                if not full_name or not email or not password:
                    st.error("Complete all account fields.")
                elif len(password) < 8:
                    st.error("Use at least 8 characters for the password.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                else:
                    try:
                        ok, message = create_user(full_name, email, password)
                    except Exception as exc:
                        st.error(f"Account creation failed because the database is unavailable: {exc}")
                    else:
                        if ok:
                            # Automatically log in the user after account creation
                            user = authenticate_user(email, password)
                            if user:
                                clear_user_workspace_state()
                                st.session_state["user"] = {
                                    "id": user["id"],
                                    "full_name": user["full_name"],
                                    "email": user["email"],
                                }
                                st.success(message)
                                time.sleep(0.2)
                                go_home()
                        else:
                            st.error(message)


def require_login():
    if st.session_state.get("user"):
        return True

    render_login_interface()
    st.stop()

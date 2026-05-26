import os
import pandas as pd
import streamlit as st
import mysql.connector


def get_connection():

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        port=int(os.getenv("MYSQL_PORT")),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
    )


def get_current_user_id():
    user = st.session_state.get("user") or {}
    return user.get("id")


def ensure_influencer_history_table():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS influencer_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NULL,
                channel_name VARCHAR(255),
                subscribers BIGINT,
                views BIGINT,
                videos INT,
                engagement FLOAT,
                fraud_score FLOAT,
                status VARCHAR(50),
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_influencer_history_user_id (user_id)
            )
            """)

        cursor.execute("SHOW COLUMNS FROM influencer_history LIKE 'user_id'")
        if cursor.fetchone() is None:
            cursor.execute("SHOW COLUMNS FROM influencer_history")
            columns = [row[0] for row in cursor.fetchall()]
            position = " AFTER id" if "id" in columns else ""
            cursor.execute(
                f"ALTER TABLE influencer_history ADD COLUMN user_id INT NULL{position}"
            )
            cursor.execute(
                "CREATE INDEX idx_influencer_history_user_id ON influencer_history (user_id)"
            )

        cursor.execute("DELETE FROM influencer_history WHERE user_id IS NULL")
        conn.commit()
    finally:
        conn.close()


def save_creator(data, user_id=None):
    ensure_influencer_history_table()
    user_id = user_id if user_id is not None else get_current_user_id()
    if user_id is None:
        raise RuntimeError(
            "A logged-in user is required before saving creator analysis."
        )

    query = """
    INSERT INTO influencer_history
    (
        user_id,
        channel_name,
        subscribers,
        views,
        videos,
        engagement,
        fraud_score,
        status
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        user_id,
        data["channel_name"],
        data["subscribers"],
        data["views"],
        data["videos"],
        data["engagement"],
        data["fraud_score"],
        data["status"],
    )

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
    finally:
        conn.close()


def load_history(user_id=None):
    ensure_influencer_history_table()
    user_id = user_id if user_id is not None else get_current_user_id()
    conn = get_connection()
    try:
        columns = pd.read_sql("SHOW COLUMNS FROM influencer_history", conn)[
            "Field"
        ].tolist()
        order_clause = " ORDER BY analyzed_at DESC" if "analyzed_at" in columns else ""
        if "user_id" in columns:
            return pd.read_sql(
                f"SELECT * FROM influencer_history WHERE user_id = %s{order_clause}",
                conn,
                params=(user_id,),
            )
        return pd.DataFrame()
    finally:
        conn.close()

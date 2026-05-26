import mysql.connector
import pandas as pd
import streamlit as st

conn = mysql.connector.connect(
    host=st.secrets["MYSQL_HOST"],
    user=st.secrets["MYSQL_USER"],
    password=st.secrets["MYSQL_PASSWORD"],
    database=st.secrets["MYSQL_DATABASE"]
)

cursor = conn.cursor()


def save_creator(data):

    query = """
    INSERT INTO influencer_history
    (
        channel_name,
        subscribers,
        views,
        videos,
        engagement,
        fraud_score,
        status
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        data['channel_name'],
        data['subscribers'],
        data['views'],
        data['videos'],
        data['engagement'],
        data['fraud_score'],
        data['status']
    )

    cursor.execute(query, values)
    conn.commit()


def load_history():

    query = "SELECT * FROM influencer_history"

    return pd.read_sql(query, conn)
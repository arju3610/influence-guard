from googleapiclient.discovery import build
import streamlit as st

API_KEY = st.secrets["YOUTUBE_API_KEY"]

youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)


def get_channel_data(channel_id):
    try:
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )

        response = request.execute()

        if not response['items']:
            return None

        data = response['items'][0]

        snippet = data['snippet']
        stats = data['statistics']

        subscribers = int(stats.get('subscriberCount', 0))
        views = int(stats.get('viewCount', 0))
        videos = int(stats.get('videoCount', 0))

        avg_views = views / videos if videos > 0 else 0

        engagement = round(
            (avg_views / subscribers) * 100,
            2
        ) if subscribers > 0 else 0

        fraud_score = 0

        if engagement < 1:
            fraud_score += 50

        if subscribers > 100000 and avg_views < subscribers * 0.02:
            fraud_score += 30

        if videos > 1000 and engagement < 2:
            fraud_score += 20

        if fraud_score >= 70:
            status = "Fake"

        elif fraud_score >= 40:
            status = "Suspicious"

        else:
            status = "Genuine"

        return {
            "channel_name": snippet['title'],
            "thumbnail": snippet['thumbnails']['default']['url'],
            "subscribers": subscribers,
            "views": views,
            "videos": videos,
            "engagement": engagement,
            "fraud_score": fraud_score,
            "status": status
        }
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None
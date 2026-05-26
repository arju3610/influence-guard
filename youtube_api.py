import re
from urllib.parse import parse_qs, urlparse

import streamlit as st
from googleapiclient.discovery import build


def get_youtube_client():
    if "YOUTUBE_API_KEY" not in st.secrets:
        raise RuntimeError("Missing Streamlit secret: YOUTUBE_API_KEY")
    return build("youtube", "v3", developerKey=st.secrets["YOUTUBE_API_KEY"])


def extract_channel_id(value):
    value = (value or "").strip()
    if not value:
        return ""
    if re.fullmatch(r"UC[\w-]{20,}", value):
        return value
    match = re.search(r"/channel/(UC[\w-]{20,})", value)
    if match:
        return match.group(1)
    return value


def parse_channel_input(value):
    value = (value or "").strip()
    if not value:
        return "", ""

    if re.fullmatch(r"UC[\w-]{20,}", value):
        return "id", value

    if value.startswith("@"):
        return "handle", value

    parsed = urlparse(value if re.match(r"https?://", value) else f"https://{value}")
    path = parsed.path.strip("/")
    parts = [part for part in path.split("/") if part]

    if not parts:
        return "", ""

    if parts[0] == "channel" and len(parts) > 1 and re.fullmatch(r"UC[\w-]{20,}", parts[1]):
        return "id", parts[1]

    if parts[0].startswith("@"):
        return "handle", parts[0]

    if parts[0] == "user" and len(parts) > 1:
        return "username", parts[1]

    if parts[0] == "c" and len(parts) > 1:
        return "search", parts[1]

    query = parse_qs(parsed.query)
    if "channel_id" in query and query["channel_id"]:
        return "id", query["channel_id"][0]

    return "search", parts[-1]


def fetch_channel(youtube, value):
    input_type, input_value = parse_channel_input(value)
    if not input_value:
        return None

    if input_type == "id":
        response = youtube.channels().list(part="snippet,statistics", id=input_value).execute()
    elif input_type == "handle":
        response = youtube.channels().list(part="snippet,statistics", forHandle=input_value).execute()
    elif input_type == "username":
        response = youtube.channels().list(part="snippet,statistics", forUsername=input_value).execute()
    else:
        search = youtube.search().list(
            part="snippet",
            q=input_value,
            type="channel",
            maxResults=1,
        ).execute()
        items = search.get("items", [])
        if not items:
            return None
        channel_id = items[0].get("snippet", {}).get("channelId")
        if not channel_id:
            return None
        response = youtube.channels().list(part="snippet,statistics", id=channel_id).execute()

    items = response.get("items", [])
    return items[0] if items else None


def get_channel_data(channel_value):
    try:
        youtube = get_youtube_client()
        data = fetch_channel(youtube, channel_value)

        if not data:
            return None

        snippet = data["snippet"]
        stats = data["statistics"]

        subscribers = int(stats.get("subscriberCount", 0))
        views = int(stats.get("viewCount", 0))
        videos = int(stats.get("videoCount", 0))
        avg_views = views / videos if videos > 0 else 0
        engagement = round((avg_views / subscribers) * 100, 2) if subscribers > 0 else 0

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
            status = "Real"

        thumbnails = snippet.get("thumbnails", {})
        thumbnail = next(
            (
                thumbnails.get(size, {}).get("url")
                for size in ["maxres", "high", "medium", "default"]
                if thumbnails.get(size, {}).get("url")
            ),
            "",
        )

        return {
            "channel_name": snippet["title"],
            "thumbnail": thumbnail,
            "subscribers": subscribers,
            "views": views,
            "videos": videos,
            "engagement": engagement,
            "fraud_score": fraud_score,
            "status": status,
        }
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

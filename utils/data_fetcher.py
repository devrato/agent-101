import os
import pandas as pd
import streamlit as st
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

from dotenv import load_dotenv
load_dotenv()


# Try to load API key from Streamlit secrets (for cloud) OR environment variable (for local)
if "streamlit" in globals():
    YOUTUBE_API_KEY = st.secrets.get("YOUTUBE_API_KEY")
else:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise ValueError("❌ YOUTUBE_API_KEY is missing. Set it as an environment variable or in secrets.toml.")

# MKBHD Channel ID
CHANNEL_ID = "UCBJycsmduvYEL83R_U4JriQ"

def fetch_latest_videos(max_results=20):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    request = youtube.search().list(
        part="id,snippet",
        channelId=CHANNEL_ID,
        maxResults=max_results,
        order="date",
        type="video"
    )
    response = request.execute()

    videos = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_data = {
            "video_id": video_id,
            "title": item['snippet']['title'],
            "description": item['snippet']['description'],
            "publishedAt": item['snippet']['publishedAt'],
            "url": f"https://www.youtube.com/watch?v={video_id}",
        }

        # Fetch video stats (views, likes, etc.)
        stats_request = youtube.videos().list(
            part="statistics",
            id=video_id
        )
        stats_response = stats_request.execute()
        if stats_response['items']:
            stats = stats_response['items'][0]['statistics']
            video_data.update({
                "viewCount": stats.get("viewCount", "N/A"),
                "likeCount": stats.get("likeCount", "N/A"),
            })

        # Try fetching transcript (optional)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([t['text'] for t in transcript])
            video_data["transcript"] = transcript_text
        except TranscriptsDisabled:
            video_data["transcript"] = "Transcript not available"
        except Exception as e:
            video_data["transcript"] = f"Error fetching transcript: {e}"

        videos.append(video_data)

    # Convert to DataFrame and Save
    df = pd.DataFrame(videos)
    df.to_csv("mkbhd_data.csv", index=False)

    print(f"✅ Fetched {len(videos)} latest videos and saved to `mkbhd_data.csv`")
    print("\n📊 Preview of Fetched Data:")
    print(df.head(5).to_string())

if __name__ == "__main__":
    fetch_latest_videos()

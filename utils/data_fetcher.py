import os
import pandas as pd
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    raise ValueError("❌ YOUTUBE_API_KEY is missing!")

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
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            video_data["transcript"] = " ".join([t['text'] for t in transcript])
        except:
            video_data["transcript"] = "Transcript not available"
        videos.append(video_data)

    pd.DataFrame(videos).to_csv("mkbhd_data.csv", index=False)
    print("✅ Fetched & saved latest videos to `mkbhd_data.csv`")

if __name__ == "__main__":
    fetch_latest_videos()

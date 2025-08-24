from fastapi import FastAPI
from urllib.parse import urlparse, parse_qs
import os
import requests


app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello, World!"}


# endpoint to extract YouTube video ID from either a full URL or a raw ID
@app.get("/parse/")
def parse_video(video: str):
    # check if input looks like a full YouTube URL (standard or short)
    if "youtube.com" in video or "youtu.be" in video:
        url = urlparse(video)  # parse the URL into components (hostname, path, query, etc.)
        if url.hostname == "youtu.be":
            video_id = url.path[1:]  # for short links, the video ID is in the path
        else:
            video_id = parse_qs(url.query).get("v", [None])[0]  # for normal links, get ?v=ID from query params
    else:
        # if not a URL, assume the input is already a video ID
        video_id = video
    return {"video_id": video_id}  # return the extracted or assumed video ID


@app.get("/comments")
def get_comments(video_id: str):
    # get API key from environment (set YOUTUBE_API_KEY before running)
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        return {"error": "Set YOUTUBE_API_KEY environment variable first."}

    # YouTube commentThreads: newest first, 5 results
    url = "https://www.googleapis.com/youtube/v3/commentThreads"
    params = {
        "part": "snippet",
        "videoId": video_id,
        "order": "time",      # newest first
        "maxResults": 5,
        "textFormat": "plainText",
        "key": api_key,
    }

    r = requests.get(url, params=params, timeout=15)
    data = r.json()

    # extract top-level comment text safely
    comments = []
    for item in data.get("items", []):
        snippet = item.get("snippet", {})
        top = snippet.get("topLevelComment", {})
        c = top.get("snippet", {})
        text = c.get("textDisplay")
        if text:
            comments.append(text)

    return {"video_id": video_id, "count": len(comments), "comments": comments}


@app.get("/video_info")
def video_info(video_id: str):
    # minimal details about a video (title, channel, published, views)
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        return {"error": "Set YOUTUBE_API_KEY environment variable first."}

    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "id": video_id,
        "key": api_key,
    }
    r = requests.get(url, params=params, timeout=15)
    data = r.json()
    items = data.get("items", [])
    if not items:
        return {"error": "Video not found or API quota issue."}

    snip = items[0].get("snippet", {})
    stats = items[0].get("statistics", {})
    return {
        "video_id": video_id,
        "title": snip.get("title"),
        "channel": snip.get("channelTitle"),
        "publishedAt": snip.get("publishedAt"),
        "views": int(stats.get("viewCount", 0)) if stats.get("viewCount") else None,
        "likes": int(stats.get("likeCount", 0)) if stats.get("likeCount") else None,
        "thumbnail": (snip.get("thumbnails", {}).get("high", {}) or snip.get("thumbnails", {}).get("default", {})).get("url"),
    }

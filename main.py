from fastapi import FastAPI
from urllib.parse import urlparse, parse_qs

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello, World!"}


# endpoint to accept a YouTube URL or ID
@app.get("/parse/")
def parse_video(video: str):
    # if it's a full URL extract the video ID
    if "youtube.com" in video or "youtu.be" in video:
        url = urlparse(video)
        if url.hostname == "youtu.be":
            video_id = url.path[1:]
        else:
            video_id = parse_qs(url.query).get("v", [None])[0]
    else:
        # assume it's already a video ID
        video_id = video
    return {"video_id": video_id}


@app.get("/comments")
def get_comments(video_id: str):
    # for now, just confirm we received the video_id
    return {"video_id": video_id, "comments": []}

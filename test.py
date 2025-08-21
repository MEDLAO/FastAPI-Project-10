import requests
import json


API_KEY = "AIzaSyDj4AKRMC7sXCwu6oihzgUjgkM2gyRGcAQ"
video_id = "xWYb7tImErI"  # sample YouTube video ID

# call YouTube Data API v3 (Videos endpoint)
url_a = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}"
url_b = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={API_KEY}&order=relevance&maxResults=10"

response = requests.get(url_b)
data = response.json()

# pretty print the response
print(json.dumps(data, indent=4))

for item in data.get("items", []):
    snippet = item.get("snippet", {})
    top_comment = snippet.get("topLevelComment", {})
    comment_snippet = top_comment.get("snippet", {})
    text = comment_snippet.get("textDisplay")
    author = comment_snippet.get("authorDisplayName")
    likes = comment_snippet.get("likeCount")
    published = comment_snippet.get("publishedAt")
    replies = snippet.get("totalReplyCount")

    if text:
        print(f"Author: {author}")
        print(f"Comment: {text}")
        print(f"Likes: {likes}, Replies: {replies}, Published: {published}")
        print("-" * 40)


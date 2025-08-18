import requests
import json


API_KEY = "AIzaSyDj4AKRMC7sXCwu6oihzgUjgkM2gyRGcAQ"
video_id = "xWYb7tImErI"  # sample YouTube video ID

# call YouTube Data API v3 (Videos endpoint)
url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={API_KEY}"

response = requests.get(url)
data = response.json()

# pretty print the response
print(json.dumps(data, indent=4))

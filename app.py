from fastapi import FastAPI
from yt_dlp import YoutubeDL
from pydantic import BaseModel

app = FastAPI()

class VideoRequest(BaseModel):
    video_url: str

def get_download_url(video_url: str) -> str:
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        video_url = info.get('url', None)
    return video_url

@app.post("/get_video_url/")
def get_video_url(request: VideoRequest):
    download_url = get_download_url(request.video_url)
    if download_url:
        return {"download_url": download_url}
    return {"error": "Failed to retrieve the video download URL"}

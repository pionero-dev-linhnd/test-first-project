import os
import uvicorn
from fastapi import FastAPI, Request
from yt_dlp import YoutubeDL
from pydantic import BaseModel

app = FastAPI()

class VideoRequest(BaseModel):
    video_url: str

def get_download_url(video_url: str, cookies: str) -> str:
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'noplaylist': True,
        'cookies': cookies,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        video_url = info.get('url', None)
    return video_url

@app.post("/get_video_url/")
def get_video_url(request: VideoRequest, req: Request):
    cookies_header = req.headers.get('cookies')
    print(cookies_header)

    download_url = get_download_url(request.video_url, cookies_header)
    if download_url:
        return {"download_url": download_url}
    return {"error": "Failed to retrieve the video download URL"}

# Main block to run the server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Lấy PORT từ biến môi trường hoặc dùng mặc định là 8000
    uvicorn.run(app, host="0.0.0.0", port=port)

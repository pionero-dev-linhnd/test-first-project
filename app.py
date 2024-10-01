import os
import uvicorn
from fastapi import FastAPI
from yt_dlp import YoutubeDL
from pydantic import BaseModel

app = FastAPI()

class VideoRequest(BaseModel):
    video_url: str

def get_po_token(video_url: str) -> str:
    ydl_opts_info = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
    }

    with YoutubeDL(ydl_opts_info) as ydl:
        info = ydl.extract_info(video_url, download=False)
        po_token = info.get('serviceIntegrityDimensions', {}).get('poToken', None)

    return po_token

def get_download_url(video_url: str) -> str:
    po_token = get_po_token(video_url)

    print('PO Token:', po_token)

    ydl_opts_download = {
        'format': 'm4a/bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }

    if po_token:
        ydl_opts_download['extractor-args'] = f"youtube:player-client=web,default;po_token=web+{po_token}"

    try:
        with YoutubeDL(ydl_opts_download) as ydl:
            info = ydl.extract_info(video_url, download=False)
            download_url = info.get('url', None)

            if not download_url:
                raise ValueError("Could not find download URL.")
    except Exception as e:
        print(f"Error extracting download URL: {str(e)}")
        return None

    return download_url

@app.post("/get_video_url/")
def get_video_url(request: VideoRequest):
    download_url = get_download_url(request.video_url)
    if download_url:
        return {"download_url": download_url}
    return {"error": "Failed to retrieve the video download URL"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

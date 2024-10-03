import os
import uvicorn
import requests
from fastapi import FastAPI, HTTPException
from yt_dlp import YoutubeDL
from pydantic import BaseModel

app = FastAPI()

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_URI = os.getenv("AUTH_URI")
TOKEN_URI = os.getenv("TOKEN_URI")

def get_access_token(code: str) -> str:
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }

    response = requests.post(TOKEN_URI, data=data)
    response_data = response.json()

    if 'access_token' in response_data:
        return response_data['access_token']
    
    raise ValueError("Failed to obtain access token")

def get_download_url(video_url: str, access_token: str) -> str:
    print(f'Bearer {access_token}')
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'headers': {
            'Authorization': f'Bearer {access_token}',
        },
        'force_generic_extractor': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',

    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # print(info)
            video_url = info.get('url', None)
            if not video_url:
                raise ValueError("Could not find video URL.")
    except Exception as e:
        print(f"Error extracting video URL: {str(e)}")  # In thông báo lỗi
        return None
    
    return video_url

@app.get("/")
def root():
    auth_url = f"{AUTH_URI}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=https://www.googleapis.com/auth/youtube.readonly"
    return auth_url

@app.get("/get_video_url")
def get_video_url(code: str, video_url: str):
    access_token = get_access_token(code)

    download_url = get_download_url(video_url, access_token)

    if download_url:
        return {"download_url": download_url}
    raise HTTPException(status_code=404, detail="Failed to retrieve the video download URL")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  
    uvicorn.run(app, host="localhost", port=port)

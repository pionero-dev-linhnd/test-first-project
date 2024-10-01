import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from yt_dlp import YoutubeDL
from pydantic import BaseModel
import urllib.parse  # Thêm import này

app = FastAPI()

class VideoRequest(BaseModel):
    video_url: str

def save_cookies(cookies_string: str, cookies_file: str):
    # Giải mã cookies
    decoded_cookies = urllib.parse.unquote(cookies_string)
    
    # Lưu cookies vào tệp
    with open(cookies_file, 'w') as f:
        f.write(decoded_cookies)

def get_download_url(video_url: str, cookies: str) -> str:
    cookies_file = 'cookies.txt'
    save_cookies(cookies, cookies_file)

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'noplaylist': True,
        'cookies': cookies_file,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            video_url = info.get('url', None)
            if not video_url:
                raise ValueError("Could not find video URL.")
    except Exception as e:
        print(f"Error extracting video URL: {str(e)}")  # In thông báo lỗi
        return None
    
    return video_url

@app.post("/get_video_url/")
def get_video_url(request: VideoRequest, req: Request):
    cookies_header = req.headers.get('cookies')
    if not cookies_header:
        raise HTTPException(status_code=400, detail="No cookies provided")

    download_url = get_download_url(request.video_url, cookies_header)
    if download_url:
        return {"download_url": download_url}
    raise HTTPException(status_code=404, detail="Failed to retrieve the video download URL")

# Main block to run the server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Lấy PORT từ biến môi trường hoặc dùng mặc định là 8000
    uvicorn.run(app, host="0.0.0.0", port=port)

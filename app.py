import os
import uvicorn
from fastapi import FastAPI, Request
from yt_dlp import YoutubeDL
from pydantic import BaseModel
import http.cookiejar
import urllib.parse 

app = FastAPI()

class VideoRequest(BaseModel):
    video_url: str

def save_cookies_from_string(cookies_string: str, cookies_file: str):

    decoded_cookies = urllib.parse.unquote(cookies_string)

    jar = http.cookiejar.CookieJar()
    
    # Phân tách cookies
    cookies_list = decoded_cookies.split('; ')
    for cookie in cookies_list:
        name, value = cookie.split('=', 1)
        # Tạo cookie và thêm vào cookiejar
        jar.set_cookie(http.cookiejar.Cookie(version=0, name=name, value=value,
                                             port=None, port_specified=False,
                                             domain='youtube.com', domain_specified=True,
                                             domain_initial_dot=False, path='/', 
                                             path_specified=True, secure=False, 
                                             expires=None, discard=True, comment=None, 
                                             comment_url=None, rest=None))
    
    # Lưu cookies vào tệp
    with open(cookies_file, 'w') as f:
        for cookie in jar:
            f.write(f"{cookie.name}={cookie.value}\n")

def get_download_url(video_url: str, cookies: str) -> str:
    cookies_file = 'cookies.txt'
    save_cookies_from_string(cookies, cookies_file)

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'noplaylist': True,
        'cookies': cookies_file,
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

import requests
import json

# Flask 应用程序的 URL
url = "http://127.0.0.1:5000/download"

# 要下载的 YouTube 视频 URL
video_url = "https://www.youtube.com/watch?v=T-82aMJk51s"

# 请求头
headers = {
    "Content-Type": "application/json"
}

# 请求体
data = {
    "url": video_url
}

# 发送 POST 请求
response = requests.post(url, headers=headers, data=json.dumps(data))

# 打印响应
if response.status_code == 200:
    print("成功:", response.json())
else:
    print("失败:", response.status_code, response.text)
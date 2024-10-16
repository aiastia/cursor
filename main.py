# 帮我写一个web 功能是调用yt-dlp下载youtube视频

from flask import Flask, request, jsonify, render_template, send_from_directory
import yt_dlp as youtube_dl
import os
import threading
import time

app = Flask(__name__)

DOWNLOAD_FOLDER = 'static/downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# 全局变量来存储下载进度
download_progress = {}

def delayed_delete(file_path, delay=1800):
    """延迟删除文件"""
    time.sleep(delay)
    try:
        os.remove(file_path)
        print(f"File {file_path} deleted.")
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")

def progress_hook(d):
    """下载进度回调函数"""
    if d['status'] == 'downloading':
        download_progress[d['info_dict']['id']] = d['_percent_str']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'best',
        'progress_hooks': [progress_hook]
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            video_id = info_dict['id']
            print(f"Downloaded file: {filename}")
            print(f"Download URL: /downloads/{os.path.basename(filename)}")
            threading.Thread(target=delayed_delete, args=(filename,)).start()
        return jsonify({'message': 'Download started', 'download_url': f'/downloads/{os.path.basename(filename)}', 'video_id': video_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/progress/<video_id>')
def get_progress(video_id):
    progress = download_progress.get(video_id, '0%')
    return jsonify({'progress': progress})

@app.route('/downloads/<path:filename>')
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

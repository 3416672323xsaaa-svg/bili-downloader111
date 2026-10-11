# -*- coding: utf-8 -*-
import threading
import os
import sys
import requests
import subprocess

class DownloadManager:
    def __init__(self):
        self.tasks = {}

    def get_ffmpeg_path(self):
        if sys.platform == "android":
            import android
            ffmpeg_bin = os.path.join(android.app_root, "ffmpeg.bin")
            os.chmod(ffmpeg_bin, 0o755)
            return ffmpeg_bin
        else:
            return "ffmpeg"

    def output_dir(self):
        if sys.platform == "android":
            from android.storage import primary_external_storage_path
            root = primary_external_storage_path()
            save_path = os.path.join(root, "Download", "BiliPink")
        else:
            save_path = os.path.join(os.getcwd(), "bili_download")
        os.makedirs(save_path, exist_ok=True)
        return save_path

    def add_task(self,name,func,*args):
        self.tasks[name]='等待'
        threading.Thread(target=self.run,args=(name,func,args)).start()

    def run(self,name,func,args):
        try:
            self.tasks[name]='下载中'
            func(*args)
            self.tasks[name]='完成'
        except Exception as e:
            self.tasks[name]=str(e)

    def download_file(self, url, save_name, progress_callback):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Referer': 'https://www.bilibili.com/'
        }
        save_path = os.path.join(self.output_dir(), save_name)
        with requests.get(url, stream=True, headers=headers, timeout=30) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            downloaded = 0
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=1024*64):
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress_callback(downloaded, total_size)
        return save_path

    def merge_video_audio(self, video_path, audio_path, out_path):
        ffmpeg = self.get_ffmpeg_path()
        cmd = [
            ffmpeg,
            "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c", "copy",
            out_path
        ]
        ret = subprocess.run(cmd, capture_output=True)
        if ret.returncode == 0:
            os.remove(video_path)
            os.remove(audio_path)
            return True
        return False

# -*- coding: utf-8 -*-
import threading
import os
import sys
import requests
import ffmpeg_kit

class DownloadManager:
    def __init__(self):
        self.tasks = {}

    def output_dir(self):
        if sys.platform == "android":
            # 手机公共存储 /storage/emulated/0/Download
            from android.storage import primary_external_storage_path
            root = primary_external_storage_path()
            save_path = os.path.join(root, "Download", "BiliPink")
        else:
            # PC测试
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

    # 下载单个文件，带进度回调
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

    # ffmpeg-kit无损合并音视频，合并成功自动删除原始分轨文件
    def merge_video_audio(self, video_path, audio_path, out_path):
        cmd = f"-i {video_path} -i {audio_path} -c copy {out_path}"
        ret = ffmpeg_kit.execute(cmd)
        if ret == 0:
            os.remove(video_path)
            os.remove(audio_path)
            return True
        return False

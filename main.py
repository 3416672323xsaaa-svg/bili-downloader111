# main.py
import re
import os
import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from jnius import autoclass

# 导入自定义模块
from bili_api import parse_video, get_video_formats
from download_manager import DownloadManager

# 安卓相关权限与系统类
if platform == "android":
    from android.permissions import request_permissions, Permission
    Environment = autoclass('android.os.Environment')
    Settings = autoclass('android.provider.Settings')
    Intent = autoclass('android.content.Intent')
    Uri = autoclass('android.net.Uri')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')

# 文件名净化函数，剔除系统不允许的非法字符
def safe_filename(text):
    return re.sub(r'[\/\\:*?"<>|]', '_', text)

# 加载界面kv文件
Builder.load_file("bili.kv")


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video = None
        self.formats = []
        self.dm = DownloadManager()
        self.ids.status.text = "BiliPink 就绪"

    def get_dm(self):
        return self.dm

    def format_label(self, fmt):
        if fmt["type"] == "video":
            return f'{fmt["height"]}p {fmt["fps"]}fps'
        else:
            size_mb = fmt["filesize"] // 1024 // 1024 if fmt["filesize"] else 0
            return f'音频 {size_mb}MB'

    def parse_click(self):
        url = self.ids.link_input.text.strip()
        if not url:
            self.ids.status.text = "请输入BV/AV号或者视频链接"
            return
        try:
            self.ids.status.text = "解析中..."
            self.video = parse_video(url)
            self.formats = get_video_formats(self.video)
            self.ids.status.text = f'解析成功：{self.video["title"]}'
            # 填充下拉画质列表
            self.ids.quality.values = [self.format_label(f) for f in self.formats]
            self.ids.quality.text = self.format_label(self.formats[0])
        except Exception as e:
            self.ids.status.text = f"解析失败：{str(e)}"

    def download_clicked(self):
        # 安卓平台：检查全部文件访问权限
        if platform == "android":
            if not Environment.isExternalStorageManager():
                intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
                uri = Uri.parse("package:" + PythonActivity.mActivity.getPackageName())
                intent.setData(uri)
                PythonActivity.mActivity.startActivity(intent)
                self.ids.status.text = "请授予【全部文件访问】权限，再重新点击下载"
                return

        if not self.video:
            self.ids.status.text = "请先解析视频"
            return

        selected_format_text = self.ids.quality.text
        selected_video = None
        for f in self.formats:
            if self.format_label(f) == selected_format_text and f["type"] == "video":
                selected_video = f
                break
        if not selected_video:
            self.ids.status.text = "⚠️请选择视频画质，不要选择纯音频"
            return

        # 获取音频流，自动选择体积最大的音频
        audio_list = [x for x in self.formats if x["type"] == "audio"]
        if not audio_list:
            self.ids.status.text = "无可用音频流"
            return
        selected_audio = max(audio_list, key=lambda x: x["filesize"] if x["filesize"] else 0)

        raw_title = self.video["title"]
        safe_title = safe_filename(raw_title)
        self.ids.status.text = f"开始任务：{safe_title}"

        def task_func():
            def progress_video(cur, tot):
                pct = int(cur / tot * 100) if tot else 0
                self.update_progress(pct, f"视频下载 {cur/1024/1024:.2f}MB")

            def progress_audio(cur, tot):
                pct = int(cur / tot * 100) if tot else 0
                self.update_progress(pct, f"音频下载 {cur/1024/1024:.2f}MB")

            # 下载视频和音频临时文件
            vid_path = self.dm.download_file(selected_video["url"], f"{safe_title}_video.mp4", progress_video)
            aud_path = self.dm.download_file(selected_audio["url"], f"{safe_title}_audio.m4a", progress_audio)

            self.update_progress(0, "正在合并音视频...")
            final_path = os.path.join(self.dm.output_dir(), f"{safe_title}.mp4")
            try:
                ok = self.dm.merge_media_android(vid_path, aud_path, final_path)
                if ok:
                    self.update_progress(100, f"✅合并完成！保存到 Download/BiliPink/{safe_title}.mp4")
                    # 删除临时视频音频文件
                    os.remove(vid_path)
                    os.remove(aud_path)
                else:
                    self.update_progress(0, "❌合并失败")
            except Exception as e:
                self.update_progress(0, f"❌合并异常：{str(e)}")

        self.dm.add_task(safe_title, task_func)

    def update_progress(self, value, text):
        self.ids.progress.value = value
        self.ids.status.text = text


class BiliPinkApp(App):
    def build(self):
        if platform == "android":
            request_permissions([Permission.INTERNET, Permission.READ_EXTERNAL_STORAGE])
        return MainLayout()


if __name__ == "__main__":
    BiliPinkApp().run()

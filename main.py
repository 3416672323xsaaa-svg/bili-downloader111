# -*- coding: utf-8 -*-
"""BiliPink - 哔哩哔哩视频下载器。Kivy 安卓入口。"""
import threading
import re
import os
import sys
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar

from bili_api import parse_video, get_video_formats, download_cover
from download_manager import DownloadManager


# ===================== 【暂时注释：运行时下载yt‑dlp，安卓极易网络超时闪退】 =====================
# def load_ytdlp():
#     try:
#         if sys.platform == "android":
#             from android.storage import app_storage_path
#             app_path = app_storage_path()
#             ydl_file = os.path.join(app_path, "yt_dlp_main.py")
#         else:
#             app_path = "."
#             ydl_file = os.path.join(app_path, "yt_dlp_main.py")
#
#         if not os.path.exists(ydl_file):
#             print("首次启动，正在下载 yt‑dlp ...")
#             import requests
#             url = "https://mirror.ghproxy.com/https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/yt_dlp/__main__.py"
#             resp = requests.get(url, timeout=30)
#             resp.raise_for_status()
#             with open(ydl_file, "wb") as f:
#                 f.write(resp.content)
#         sys.path.insert(0, app_path)
#         import yt_dlp
#         return yt_dlp
#     except Exception as e:
#         print("yt‑dlp加载失败：", e)
#         return None

yt_dlp = None
# =================================================================

# 安卓规避字体路径异常，直接使用系统Roboto字体
FONT = "Roboto"

PINK = "#FB7299"
BG = "#FFF7FA"
DARK = "#28242A"
MUTED = "#887780"
WHITE = "#FFFFFF"


def c(value):
    return get_color_from_hex(value)


class ActionButton(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_color", c(PINK))
        kwargs.setdefault("color", c(WHITE))
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(46))
        kwargs.setdefault("bold", True)
        kwargs.setdefault("font_name", FONT)
        super().__init__(**kwargs)


class BiliPinkApp(App):
    title = "哔哩哔哩视频下载器"

    def build(self):
        # 暂时关闭动态加载yt‑dlp
        # def init_extra():
        #     global yt_dlp
        #     yt_dlp = load_ytdlp()
        #     if yt_dlp is None:
        #         print("yt‑dlp加载失败！下载功能不可用")
        # threading.Thread(target=init_extra, daemon=True).start()

        self.video = None
        self.formats = []
        self.download_manager = DownloadManager()

        root = BoxLayout(orientation="vertical", padding=[dp(13), dp(12), dp(13), dp(8)], spacing=dp(8))
        with root.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*c(BG))
            self.bg_rect = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=self._bg_update, size=self._bg_update)

        head = BoxLayout(size_hint_y=None, height=dp(64), spacing=dp(10))
        brand = Label(text="[b]BiliPink[/b]", markup=True, color=c(PINK), font_name=FONT,
                      font_size="25sp", size_hint_x=None, width=dp(132),
                      halign="left", valign="middle")
        brand.bind(size=lambda w, v: setattr(w, "text_size", v))
        heading = BoxLayout(orientation="vertical", spacing=dp(1))
        heading.add_widget(Label(text="哔哩哔哩视频下载器", color=c(DARK), font_name=FONT,
                                 bold=True, font_size="16sp", halign="left"))
        heading.add_widget(Label(text="解析 · 画质 · 下载", color=c(MUTED), font_name=FONT,
                                 font_size="11sp", halign="left"))
        head.add_widget(brand)
        head.add_widget(heading)
        root.add_widget(head)

        self.source = TextInput(
            hint_text="输入 BV 号、AV 号或粘贴 B 站视频链接",
            multiline=False, size_hint_y=None, height=dp(52),
            padding=[dp(14), dp(13)], background_normal="", background_active="",
            background_color=c(WHITE), foreground_color=c(DARK),
            cursor_color=c(PINK), hint_text_color=c("#B9A7AF"), font_name=FONT)
        root.add_widget(self.source)

        btnrow = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(46))
        self.parse_button = ActionButton(text="解析视频")
        self.parse_button.bind(on_release=self.parse_clicked)
        clear = Button(text="清空", size_hint_y=None, height=dp(46),
                       background_normal="", background_color=c("#F0DDE4"),
                       color=c(DARK), font_name=FONT)
        clear.bind(on_release=self.clear_clicked)
        btnrow.add_widget(self.parse_button)
        btnrow.add_widget(clear)
        root.add_widget(btnrow)

        self.status = Label(text="支持 BV / AV / b23.tv 短链接，也可粘贴整段分享文案",
                            color=c(MUTED), font_name=FONT, size_hint_y=None, height=dp(26),
                            halign="left", valign="middle")
        self.status.bind(size=lambda w, v: setattr(w, "text_size", v))
        root.add_widget(self.status)

        scroll = ScrollView(do_scroll_x=False)
        body = BoxLayout(orientation="vertical", spacing=dp(8),
                         size_hint_y=None, padding=[0, dp(2), 0, dp(12)])
        body.bind(minimum_height=body.setter("height"))

        self.section(body, "视频信息")
        self.info = Label(text="解析成功后，将显示视频资料、互动统计和分 P 信息。\n\n提示：先解析，再选择清晰度、下载模式和分 P。",
                          color=c(DARK), font_name=FONT, size_hint_y=None, height=dp(360),
                          halign="left", valign="top", font_size="12sp")
        self.info.bind(width=lambda w, v: setattr(w, "text_size", (v, None)))
        self.info.bind(texture_size=lambda w, v: setattr(w, "height", max(dp(220), v[1] + dp(18))))
        body.add_widget(self.info)

        self.section(body, "下载模式")
        self.mode = Spinner(text="完整视频（MP4）",
                            values=("完整视频（MP4）", "仅下载画面", "仅下载音频"),
                            size_hint_y=None, height=dp(44),
                            background_normal="", background_color=c(WHITE), color=c(DARK), font_name=FONT)
        body.add_widget(self.mode)

        self.quality = Spinner(text="解析后显示真实可用格式", values=(),
                               size_hint_y=None, height=dp(44),
                               background_normal="", background_color=c(WHITE), color=c(DARK), font_name=FONT)
        body.add_widget(self.quality)

        self.page_spinner = Spinner(text="默认分 P", values=(), size_hint_y=None,
                                    height=dp(44), background_normal="",
                                    background_color=c(WHITE), color=c(DARK), font_name=FONT)
        body.add_widget(self.page_spinner)

        quality_tip = Label(text="清晰度列表来自当前可访问的视频格式；分 P 选择会用于下载。", color=c(MUTED), font_size="10sp", font_name=FONT, size_hint_y=None, height=dp(30), halign="left", valign="middle")
        quality_tip.bind(size=lambda w, v: setattr(w, "text_size", v))
        body.add_widget(quality_tip)

        actions = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(46))
        cover = ActionButton(text="下载封面")
        cover.bind(on_release=self.cover_clicked)
        self.download_button = ActionButton(text="开始下载")
        self.download_button.bind(on_release=self.download_clicked)
        actions.add_widget(cover)
        actions.add_widget(self.download_button)
        body.add_widget(actions)

        self.progress = ProgressBar(max=100, value=0, size_hint_y=None, height=dp(8))
        body.add_widget(self.progress)
        self.progress_text = Label(text="等待下载", color=c(MUTED), font_name=FONT,
                                   size_hint_y=None, height=dp(23), halign="left")
        body.add_widget(self.progress_text)

        note = Label(
            text="⚠️当前版本yt‑dlp功能暂未集成。高画质取决于 B 站账号权限。高清DASH流输出独立视频/音频文件，需第三方工具合并；请仅保存你有权下载的内容。",
            color=c(MUTED), font_size="10sp", font_name=FONT, size_hint_y=None,
            height=dp(36), halign="left", valign="middle")
        note.bind(size=lambda w, v: setattr(w, "text_size", v))
        body.add_widget(note)

        scroll.add_widget(body)
        root.add_widget(scroll)
        return root

    def _bg_update(self, *_):
        self.bg_rect.pos = self.root.pos
        self.bg_rect.size = self.root.size

    @staticmethod
    def section(parent, title):
        label = Label(text=title, color=c(PINK), bold=True, font_size="15sp", font_name=FONT,
                      size_hint_y=None, height=dp(27), halign="left")
        parent.add_widget(label)

    def set_status(self, message):
        Clock.schedule_once(lambda _dt: setattr(self.status, "text", str(message)), 0)

    def parse_clicked(self, *_):
        value = self.source.text.strip()
        if not value:
            self.set_status("请先输入 BV 号、AV 号或链接")
            return
        self.parse_button.disabled = True
        self.set_status("正在获取视频信息和可用格式……")
        threading.Thread(target=self._parse_worker, args=(value,), daemon=True).start()

    def _parse_worker(self, value):
        try:
            video = parse_video(value)
            formats = get_video_formats(value)

            def apply(_dt):
                self.video, self.formats = video, formats
                self.info.text = self.format_info(video)
                labels = [self.format_label(f) for f in formats]
                self.quality.values = tuple(labels)
                self.quality.text = labels[0] if labels else "未获取到可用格式"
                pages = video.get("pages") or []
                self.page_spinner.values = tuple([
                    f"P{p.get('page', i+1)} · {p.get('part') or '分P'} · {p.get('duration_text') or '时长未知'}"
                    for i, p in enumerate(pages)])
                self.page_spinner.text = self.page_spinner.values[0] if self.page_spinner.values else "默认分 P"
                self.parse_button.disabled = False
                self.set_status(f"解析成功 · {len(formats)} 种可用格式 · {len(pages)} 个分 P")

            Clock.schedule_once(apply, 0)
        except Exception as exc:
            def fail(_dt):
                self.parse_button.disabled = False
                self.set_status("解析失败：" + str(exc)[:170])

            Clock.schedule_once(fail, 0)

    @staticmethod
    def format_label(item):
        height = f"{item['height']}P" if item.get("height") else (item.get("format_note") or "未知画质")
        fps = f" · {item['fps']} FPS" if item.get("fps") else ""
        ext = f" · {item.get('ext')}" if item.get("ext") else ""
        size = f" · {item['filesize'] / 1024 / 1024:.1f}MB" if item.get("filesize") else ""
        fid = item.get("format_id", "?")
        return f"{height}{fps}{ext}{size} [格式:{fid}]"

    @staticmethod
    def format_info(v):
        rows = [
            ("标题", v.get("title")), ("UP 主", v.get("owner")),
            ("UP 主 UID", v.get("mid")), ("BV 号", v.get("bvid")),
            ("AV 号", "av" + str(v.get("aid")) if v.get("aid") else None),
            ("分区", v.get("tname")), ("发布时间", v.get("pubdate")),
            ("时长", v.get("duration_text")), ("播放", v.get("view")),
            ("点赞", v.get("like")), ("投币", v.get("coin")),
            ("收藏", v.get("favorite")), ("分享", v.get("share")),
            ("评论", v.get("reply")), ("弹幕", v.get("danmaku")),
            ("分 P 数", v.get("archive")),
            ("视频链接", v.get("url")),
            ("简介", v.get("description")),
        ]
        page_rows = []
        for page in (v.get("pages") or []):
            page_rows.append(
                f"P{page.get('page', '?')}：{page.get('part') or '未命名'} · CID {page.get('cid') or '暂无'} · {page.get('duration_text') or '时长未知'}")
        result = "\n".join(f"{k}：{value if value not in (None, '') else '暂无数据'}" for k, value in rows)
        return result + ("\n\n分 P 详情：\n" + "\n".join(page_rows) if page_rows else "")

    def cover_clicked(self, *_):
        if not self.video:
            self.set_status("请先解析视频")
            return
        threading.Thread(target=self._cover_worker, daemon=True).start()

    def _cover_worker(self):
        try:
            path = download_cover(self.video, self.download_manager.output_dir())
            self.set_status("封面已保存：" + str(path))
        except Exception as exc:
            self.set_status("封面下载失败：" + str(exc)[:150])

    def download_clicked(self, *_):
        # 提示：yt‑dlp暂未集成
        self.set_status("下载功能暂未实现，仅可解析视频信息、下载封面")
        return

    def _selected_page_number(self):
        match = re.match(r"P(\d+)", self.page_spinner.text or "")
        return int(match.group(1)) if match else None

    def _download_worker(self, mode, selected, page_number=None):
        pass

    def clear_clicked(self, *_):
        self.source.text = ""
        self.info.text = "解析成功后，视频信息会显示在这里。"
        self.quality.values = ()
        self.quality.text = "解析后显示真实可用格式"
        self.page_spinner.values = ()
        self.page_spinner.text = "默认分 P"
        self.progress.value = 0
        self.set_status("已清空")


if __name__ == "__main__":
    BiliPinkApp().run()

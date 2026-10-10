# -*- coding: utf‑8‑*-
"""yt‑dlp下载器：移除ffmpeg合并，音视频分离保存；安卓无ffmpeg也不会崩溃"""
from pathlib import Path
import re
from bili_api import normalize_input


def _safe_title(text):
    return re.sub(r'[\\/:*?"<>|]+', "_", text or "bilibili_video").strip(" .")[:120] or "bilibili_video"


def download_media(source, mode="both", selected_format=None,
                   output_dir=None, progress_hook=None, page_number=None):
    try:
        import yt_dlp
    except ImportError as exc:
        raise RuntimeError("缺少 yt‑dlp 源码文件夹") from exc

    if output_dir is None:
        try:
            from android.storage import primary_external_storage_path
            output_dir = Path(primary_external_storage_path()) / "Download" / "BiliPink"
        except ImportError:
            output_dir = Path.home() / "Download" / "BiliPink"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    url = normalize_input(source)
    if page_number:
        url += ("&" if "?" in url else "?") + f"p={int(page_number)}"

    options = {
        "outtmpl": str(output_dir / "%(title).120B [%(id)s].%(ext)s"),
        "noplaylist": True, "quiet": True, "no_warnings": True,
        "continuedl": True, "retries": 3,
    }

    if mode == "audio":
        # 只下载音频，禁止ffmpeg转码
        options["format"] = "bestaudio/best"
        options["postprocessors"] = []
    elif mode == "video":
        options["format"] = (selected_format["format_id"] if selected_format and selected_format.get("format_id")
                             else "bestvideo/best")
        options["postprocessors"] = []
    elif mode == "both":
        # 不执行merge，分开输出视频+音频文件，规避ffmpeg缺失崩溃
        if selected_format and selected_format.get("format_id"):
            fmt = selected_format["format_id"]
            has_audio = selected_format.get("acodec") not in (None, "none", "")
            has_video = selected_format.get("vcodec") not in (None, "none", "")
            if has_video and has_audio:
                options["format"] = fmt
            elif has_video:
                options["format"] = f"{fmt}+bestaudio/best"
            else:
                options["format"] = "bestvideo*+bestaudio/best"
        else:
            options["format"] = "bestvideo*+bestaudio/best"
        options["merge_output_format"] = None
        options["postprocessors"] = []
    else:
        options["format"] = "best[ext=mp4]/best"
        options["postprocessors"] = []

    if progress_hook:
        def on_progress(data):
            if data.get("status") == "downloading":
                total = data.get("total_bytes") or data.get("total_bytes_estimate") or 0
                got = data.get("downloaded_bytes") or 0
                percent = min(99, int(got * 100 / total)) if total else 0
                speed = data.get("speed")
                speed_text = f"{speed / 1024 / 1024:.2f} MB/s" if speed else "计算中"
                progress_hook(percent, f"下载中：{percent}% · {speed_text}")
            elif data.get("status") == "finished":
                progress_hook(99, "片段下载完成")
        options["progress_hooks"] = [on_progress]

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = Path(ydl.prepare_filename(info))

        files = list(output_dir.glob(f"*{info.get('id')}*"))
        if files:
            final_path = "; ".join(str(p) for p in files)
        else:
            final_path = str(filepath)

        if progress_hook:
            progress_hook(100, "下载完成（DASH高清为分开的视频、音频文件，需手动合并）")
        return final_path

    except Exception as exc:
        msg = str(exc)
        if "ffmpeg" in msg.lower():
            raise RuntimeError("已禁用ffmpeg合并；高清DASH流输出独立视频音频文件。") from exc
        raise RuntimeError(msg[:300]) from exc
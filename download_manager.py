# -*- coding: utf‑8‑*-
"""下载任务管理与输出目录处理。输出到安卓公共Download/BiliPink"""
import re
from pathlib import Path
from downloader import download_media


class DownloadManager:
    def output_dir(self):
        """安卓：公共外部存储 Download/BiliPink；PC回退用户下载目录"""
        try:
            from android.storage import primary_external_storage_path
            out = Path(primary_external_storage_path()) / "Download" / "BiliPink"
            out.mkdir(parents=True, exist_ok=True)
            return out
        except ImportError:
            pass
        out = Path.home() / "Download" / "BiliPink"
        out.mkdir(parents=True, exist_ok=True)
        return out

    @staticmethod
    def safe_filename(value, max_length=120):
        cleaned = re.sub(r'[\\/:*?"<>|]+', "_", value or "bilibili_video")
        return cleaned.strip(" .")[:max_length] or "bilibili_video"

    def download(self, source, mode="both", selected_format=None,
                 progress_hook=None, page_number=None):
        return download_media(
            source, mode=mode, selected_format=selected_format,
            output_dir=self.output_dir(),
            progress_hook=progress_hook, page_number=page_number
        )
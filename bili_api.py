# -*- coding: utf-8 -*-
"""Bilibili 视频信息、格式查询和封面下载。"""
import re
import time
from pathlib import Path
from urllib.parse import urlparse
import requests

UA = ("Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0 Mobile Safari/537.36")
HEADERS = {"User‑Agent": UA, "Referer": "https://www.bilibili.com/"}
API = "https://api.bilibili.com"


def _session():
    session = requests.Session()
    session.headers.update(HEADERS)
    return session


def normalize_input(source):
    source = (source or "").strip()
    if not source:
        raise ValueError("输入内容为空")
    bv = re.search(r"BV[0‑9A‑Za‑z]{10}", source, re.I)
    av = re.search(r"(?i)(?:^|[/\s?=&])av(\d+)", source)
    if bv:
        return "https://www.bilibili.com/video/" + bv.group(0)
    if av:
        return "https://www.bilibili.com/video/av" + av.group(1)

    urls = re.findall(r"https?://[^\s<>\"']+", source)
    if not urls and ("b23.tv/" in source or "bilibili.com/" in source):
        urls = ["https://" + source.lstrip("/")]
    if not urls:
        raise ValueError("未识别到 BV 号、AV 号或 B 站链接")
    url = urls[0].rstrip(".,，。)")
    if "b23.tv" in urlparse(url).netloc:
        try:
            response = _session().get(url, allow_redirects=True, timeout=20)
            url = response.url
        except requests.RequestException as exc:
            raise RuntimeError("短链接跳转失败，请检查网络") from exc

    bv = re.search(r"BV[0‑9A‑Za‑z]{10}", url, re.I)
    av = re.search(r"(?i)/video/av(\d+)", url)
    if bv:
        return "https://www.bilibili.com/video/" + bv.group(0)
    if av:
        return "https://www.bilibili.com/video/av" + av.group(1)
    if "bilibili.com" in urlparse(url).netloc and "/video/" in url:
        return url
    raise ValueError("不是可识别的 B 站视频链接")


def _api_get(path, params=None):
    session = _session()
    response = session.get(API + path, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()
    if data.get("code", 0) != 0:
        raise RuntimeError(data.get("message") or "B 站接口返回错误")
    return data.get("data") or {}


def _duration(seconds):
    try:
        seconds = int(seconds)
    except (TypeError, ValueError):
        return "未知"
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def parse_video(source):
    url = normalize_input(source)
    identifier = re.search(r"(BV[0‑9A‑Za‑z]{10}|av\d+)", url, re.I)
    if not identifier:
        raise ValueError("链接中没有可用的视频编号")
    ident = identifier.group(1)
    params = {"aid": ident[2:]} if ident.lower().startswith("av") else {"bvid": ident}
    view = _api_get("/x/web‑interface/view", params)
    stat = view.get("stat") or {}
    owner = view.get("owner") or {}
    pages = view.get("pages") or []
    pub = view.get("pubdate",0)
    return {
        "title": view.get("title"), "description": view.get("desc"),
        "pic": view.get("pic"), "bvid": view.get("bvid"), "aid": view.get("aid"),
        "cid": view.get("cid"), "mid": owner.get("mid"), "owner": owner.get("name"),
        "owner_face": owner.get("face"), "tname": view.get("tname"),
        "pubdate": time.strftime("%Y‑%m‑%d %H:%M:%S", time.localtime(pub)) if pub > 0 else None,
        "duration": view.get("duration"), "duration_text": _duration(view.get("duration")),
        "view": stat.get("view"), "like": stat.get("like"), "coin": stat.get("coin"),
        "favorite": stat.get("favorite"), "share": stat.get("share"),
        "reply": stat.get("reply"), "danmaku": stat.get("danmaku"),
        "archive": view.get("videos"),
        "pages": [{"page": p.get("page"), "part": p.get("part"), "cid": p.get("cid"),
                   "duration": p.get("duration"), "duration_text": _duration(p.get("duration"))} for p in pages],
        "url": url,
    }


def get_video_formats(source):
    """yt‑dlp 返回的格式是当前请求账号实际可访问的格式。"""
    try:
        import yt_dlp
    except ImportError as exc:
        raise RuntimeError("未放置 yt_dlp 源码文件夹") from exc
    url = normalize_input(source)
    options = {"quiet": True, "no_warnings": True, "skip_download": True}
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(url, download=False)
    result, seen = [], set()
    for item in info.get("formats") or []:
        if not item.get("url"):
            continue
        vcodec, acodec = item.get("vcodec"), item.get("acodec")
        if vcodec in (None, "none") and acodec in (None, "none"):
            continue
        key = (item.get("format_id"), item.get("height"), item.get("fps"), vcodec, acodec)
        if key in seen:
            continue
        seen.add(key)
        result.append({
            "format_id": item.get("format_id"), "height": item.get("height"),
            "fps": item.get("fps"), "format_note": item.get("format_note"),
            "filesize": item.get("filesize") or item.get("filesize_approx"),
            "vcodec": vcodec, "acodec": acodec, "ext": item.get("ext"),
        })
    result.sort(key=lambda x: (x.get("height") or 0, x.get("fps") or 0), reverse=True)
    return result


def download_cover(video, output_dir=None):
    url = video.get("pic")
    if not url:
        raise RuntimeError("没有获取到封面地址")
    # 安卓公共存储兼容
    if output_dir is None:
        try:
            from android.storage import primary_external_storage_path
            output_dir = Path(primary_external_storage_path()) / "Download" / "BiliPink"
        except ImportError:
            output_dir = Path.home() / "Download" / "BiliPink"
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    title = re.sub(r'[\\/:*?"<>|]+', "_", video.get("title") or "bilibili_cover").strip()
    path = output_dir / f"{title[:100]}_cover.jpg"
    resp = _session().get(url.replace("http://", "https://"), timeout=30)
    resp.raise_for_status()
    path.write_bytes(resp.content)
    return path
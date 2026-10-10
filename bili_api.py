# -*- coding: utf-8 -*-
import re
import requests

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def extract_id(text):
    m = re.search(r'BV[a-zA-Z0-9]{10}', text)
    if m:
        return {'bvid': m.group(0)}
    m = re.search(r'(?:av|AV)(\d+)', text)
    if m:
        return {'aid': m.group(1)}
    return None

def get_video_info(text):
    ids = extract_id(text)
    if not ids:
        raise Exception('无法识别视频编号')
    r = requests.get('https://api.bilibili.com/x/web-interface/view', params=ids, headers=HEADERS, timeout=15)
    d = r.json()
    if d.get('code') != 0:
        raise Exception(d.get('message', '解析失败'))
    v = d['data']
    return {
        'title': v.get('title'),
        'description': v.get('desc'),
        'cover': v.get('pic'),
        'bvid': v.get('bvid'),
        'aid': v.get('aid'),
        'cid': v.get('cid'),
        'owner': v.get('owner', {}).get('name'),
        'pages': v.get('pages', [])
    }

def get_play_info(bvid, cid):
    resp = requests.get('https://api.bilibili.com/x/player/playurl',
        params={'bvid': bvid, 'cid': cid, 'fnval': 16},
        headers=HEADERS, timeout=15)
    return resp.json()

def parse_video(text):
    return get_video_info(text)

def get_video_formats(video_info):
    bvid = video_info["bvid"]
    cid = video_info["cid"]
    play_data = get_play_info(bvid, cid)
    dash = play_data.get("data", {}).get("dash", {})
    formats = []
    for video in dash.get("video", []):
        formats.append({
            "height": video.get("height"),
            "fps": video.get("fps"),
            "ext": "mp4",
            "filesize": video.get("size"),
            "format_id": video.get("id"),
            "format_note": ""
        })
    for audio in dash.get("audio", []):
        formats.append({
            "height": None,
            "fps": None,
            "ext": "m4a",
            "filesize": audio.get("size"),
            "format_id": audio.get("id"),
            "format_note": "音频"
        })
    return formats

def download_cover(video_info, save_dir):
    url = video_info.get("cover")
    if not url:
        raise Exception("没有封面链接")
    resp = requests.get(url, headers=HEADERS, timeout=20)
    path = os.path.join(save_dir, "cover.jpg")
    with open(path, "wb") as f:
        f.write(resp.content)
    return path

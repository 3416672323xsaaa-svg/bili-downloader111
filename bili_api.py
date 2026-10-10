import re, requests

HEADERS={'User-Agent':'Mozilla/5.0'}

def extract_id(text):
    m=re.search(r'BV[a-zA-Z0-9]{10}',text)
    if m:return {'bvid':m.group(0)}
    m=re.search(r'(?:av|AV)(\\d+)',text)
    if m:return {'aid':m.group(1)}
    return None

def get_video_info(text):
    ids=extract_id(text)
    if not ids: raise Exception('无法识别视频编号')
    r=requests.get('https://api.bilibili.com/x/web-interface/view',params=ids,headers=HEADERS,timeout=15)
    d=r.json()
    if d.get('code')!=0: raise Exception(d.get('message','解析失败'))
    v=d['data']
    return {'title':v.get('title'),'desc':v.get('desc'),'cover':v.get('pic'),'bvid':v.get('bvid'),'aid':v.get('aid'),'cid':v.get('cid'),'owner':v.get('owner',{}).get('name'),'pages':v.get('pages',[])}

def get_play_info(bvid,cid):
    return requests.get('https://api.bilibili.com/x/player/playurl',params={'bvid':bvid,'cid':cid,'fnval':16},headers=HEADERS,timeout=15).json()

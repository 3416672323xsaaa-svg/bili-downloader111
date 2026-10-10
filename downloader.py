import os,requests

def download_file(url,path,callback=None):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with requests.get(url,stream=True,timeout=30) as r:
        r.raise_for_status()
        with open(path,'wb') as f:
            for c in r.iter_content(65536):
                if c:f.write(c)
    return path

def download_video(url,path,callback=None):
    return download_file(url,path,callback)

def download_cover(url,path):
    return download_file(url,path)

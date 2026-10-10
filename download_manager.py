# -*- coding: utf-8 -*-
import threading
import os
import sys

class DownloadManager:
    def __init__(self):
        self.tasks = {}

    # 适配安卓存储目录，解决Android11+写入权限问题
    def output_dir(self):
        if sys.platform == "android":
            # p4a内置接口获取APP私有存储目录
            from android.storage import app_storage_path
            save_path = app_storage_path()
        else:
            # PC端：当前文件夹
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

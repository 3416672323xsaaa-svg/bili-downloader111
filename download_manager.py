import threading

class DownloadManager:
    def __init__(self):
        self.tasks={}

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

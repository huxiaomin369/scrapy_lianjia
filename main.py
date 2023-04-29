from scrapy.cmdline import execute
from multiprocessing import  Process
import os
import time
import psutil

class FreeProxyProcess(Process): 
    def __init__(self,name):
        super(FreeProxyProcess,self).__init__()
        self.name = name

    def run(self):
        os.system('scrapy crawl free_proxy_05')

class RunRedis(Process): 
    def __init__(self,name):
        super(RunRedis,self).__init__()
        self.name = name

    def run(self):
        os.system("E:\\pythonCode\\DATA_BASE\Redis-x64-5.0.14.1\\redis-server.exe")

class LianjiaProcess(Process): 
    def __init__(self,name):
        super(LianjiaProcess,self).__init__()
        self.name = name

    def run(self):
        os.system("scrapy crawl Lianjia_home")

def is_process_alive(pid):
    try:
        process = psutil.Process(pid)
        if process.status() == psutil.STATUS_ZOMBIE:
            return False
        return True
    except :
        return False

if __name__ == "__main__":
    # execute(['scrapy', 'crawl', 'free_proxy_05'])
    # execute(['scrapy', 'crawl', 'Lianjia_home'])
    freeProxy = FreeProxyProcess("freeProxy") 
    runRedis = RunRedis('runRedis')
    lianjiaHome = LianjiaProcess('lianjiaHome')
    processList = [runRedis, freeProxy]
    for i in processList:
        i.start()
        time.sleep(5)
    time.sleep(2*60) #延迟2分钟等数据库中有一定数量的代理
    lianjiaHome.start()
    processList.append(lianjiaHome)
    while lianjiaHome.is_alive():
        if freeProxy.exitcode is not None:
            freeProxy.run() #每10分钟运行一次代理爬虫       
        else:
            time.sleep(10*60)
    runRedis.terminate()
    freeProxy.terminate()

    for i in processList:
        i.join()




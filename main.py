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

class LianjiaNewProcess(Process): 
    def __init__(self,name):
        super(LianjiaNewProcess,self).__init__()
        self.name = name

    def run(self):
        os.system('scrapy crawl lianjia_nc_new')

def is_process_alive(pid):
    try:
        process = psutil.Process(pid)
        if process.status() == psutil.STATUS_ZOMBIE:
            return False
        return True
    except :
        return False
    
def have_process_alive(processList): 
    isAlive = False
    for process in processList:
        isAlive = isAlive | process.is_alive()
    return isAlive

if __name__ == "__main__":
    # execute(['scrapy', 'crawl', 'free_proxy_05'])
    # execute(['scrapy', 'crawl', 'Lianjia_home'])
    # execute(['scrapy', 'crawl', 'lianjia_nc_new'])

    freeProxy = FreeProxyProcess("freeProxy") 
    runRedis = RunRedis('runRedis')
    lianjiaHome = LianjiaProcess('lianjiaHome')
    lianjiaNew = LianjiaNewProcess('lianjiaNew')
    proxyProcess = [runRedis, freeProxy]
    spiderProcess = [lianjiaNew]
    processList = []
    for i in proxyProcess:
        i.start()
        processList.append(i)
        time.sleep(5)
    time.sleep(2*60) #延迟2分钟等数据库中有一定数量的代理
    for i in spiderProcess:
        i.start()
        processList.append(i)

    while have_process_alive(spiderProcess):
        if not freeProxy.is_alive():
            freeProxy.run() #每10分钟运行一次代理爬虫       
        else:
            time.sleep(10*60)
    runRedis.terminate()
    freeProxy.terminate()

    for i in processList:
        i.join()




from scrapy.cmdline import execute
from multiprocessing import  Process
import os
import time
import sys

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

if __name__ == "__main__":
    # execute(['scrapy', 'crawl', 'free_proxy_05'])
    # execute(['scrapy', 'crawl', 'Lianjia_home'])
    freeProxy = FreeProxyProcess("freeProxy") 
    runRedis = RunRedis('runRedis')
    lianjiaHome = LianjiaProcess('lianjiaHome')
    processList = [runRedis, freeProxy, lianjiaHome]
    for i in processList:
        i.start()
        time.sleep(5)
    while lianjiaHome.is_alive():
        if freeProxy.is_alive():
            time.sleep(10*60)
            freeProxy.run()
    runRedis.terminate()
    freeProxy.terminate()

    for i in processList:
        i.join()





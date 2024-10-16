from scrapy.cmdline import execute
from multiprocessing import  Process
import os
import time
import psutil

def mutiProcessFunc(cmd):
    os.system(cmd)

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
    processArgs = [
                # "E:\\pythonCode\\DATA_BASE\Redis-x64-5.0.14.1\\redis-server.exe",
                # "scrapy crawl free_proxy_05",
                "scrapy crawl Lianjia_home",
                # "crapy crawl lianjia_nc_new"
                   ]
    # 创建进程列表
    allProcesses = []

    for i in range(len(processArgs)):
        p = Process(target=mutiProcessFunc, args=(processArgs[i],))
        allProcesses.append(p)
        p.start()
    
    # while have_process_alive(allProcesses):
    #     if not allProcesses[1].is_alive():
    #         p = Process(target=mutiProcessFunc, args=(processArgs[1],))
    #         p.run() #每10分钟运行一次代理爬虫  
    #         allProcesses[1] = p     
    #     else:
    #         time.sleep(10*60)

    # 等待所有进程完成
    for process in allProcesses:
        process.join()
    




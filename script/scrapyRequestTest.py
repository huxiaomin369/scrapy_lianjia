from scrapy import Request
from urllib.parse import urlencode

def myRequirst(url,header,cookies):
    return Request(url=url, method='GET', headers=header, cookies=cookies, callback=success_callback, errback=error_back)

def success_callback(self, response):
    print(response.text)
    print(response.status)

def error_back(self, failure):
    print(failure)

# 服务器的URL
url = "https://nc.lianjia.com/ershoufang/103136614266.html"

# 登录所需的数据
form_data = {
    'username': 'xxxx',
    'password': 'xxxx'
}
body = urlencode(form_data)

# 发送POST请求
headers = {
    'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "referer": "https://clogin.lianjia.com/",
}

cookies = {
    'lianjia_token': '2.0012a42c5d7cc4064f0309056c74eff18b',
}



res = Request(url,  # 测试网站的url
            method='GET',
            headers=headers,
            # cookies=cookies,
            callback=success_callback,  # 回调函数
            errback=error_back,  # 出错回调函数
            meta={"proxy": None,  # 代理服务器地址
            "dont_retry": True,  # 请求不重试
            "download_timeout": 10,  # 超时时间
            },
            dont_filter=True  # 不过滤重复请求
            )

print(res.attributes)






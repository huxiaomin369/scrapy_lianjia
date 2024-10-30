import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode
import json

import schedule
import time

def job():
    # 服务器的URL
    url = "https://link-ai.tech/api/login"
    # 登录所需的数据
    form_data = {
        'username': 'xxxxxx',
        'password': 'xxxxxx'
    }
    body = urlencode(form_data)
    # 发送POST请求
    headers = {
        'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    token = ""
    response = requests.post(url, data=body, headers=headers, verify=False)
    # 检查响应
    if response.ok:
        print('登录成功!')
        print(response.text)  # 打印服务器的响应内容
        parsed_data = json.loads(response.text)
        token = parsed_data['data']["token"]
        print(token)
    else:
        print('登录失败:', response.status_code)
    # 发送签到请求
    signIn_url = "https://link-ai.tech/api/chat/web/app/user/sign/in"
    authorization = f"Bearer {token}"
    signIn_headers = {"sec-ch-ua-platform": "Windows",
                "authorization": authorization,
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                "accept": "application/json, text/plain, */*",
                "referer": "https://link-ai.tech/console/account",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "priority": "u=1, i"         
            }
                # "sec-ch-ua-mobile": "?0",
                # "sec-fetch-site": "same-origin",
                # "sec-fetch-mode": "cors",
                # "sec-fetch-dest": "empty",
    response = requests.get(signIn_url, headers=signIn_headers, verify=False)
    if response.ok:
        print('签到成功!')
        print(response.text)  # 打印服务器的响应内容
    else:
        print('签到失败:', response.status_code)

# 每天执行任务
schedule.every().day.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)



import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode
import json

# 服务器的URL
url = "https://nc.lianjia.com/ershoufang/co32/"

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

token = ""
response = requests.get(url, headers=headers, cookies=cookies ,verify=False)

# 检查响应
if response.ok:
    print('登录成功!')
    print(response.text)  # 打印服务器的响应内容
    with open('result.txt', 'w', encoding='utf-8') as file:
        file.write(response.text)
        print("文件已保存。")
else:
    print('登录失败:', response.status_code)



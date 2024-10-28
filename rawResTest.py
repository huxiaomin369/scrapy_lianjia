import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode
import json

# 服务器的URL
url = "https://hip.lianjia.com/captcha?location=https%3A%2F%2Fnc.lianjia.com%2Fershoufang%2Fpg3co32%2F&ext=BH2nw9QiSmkN8ACHP13mhd_tIfUe4CmqciC97Ji5p3objhTUkLEcuD47NU6Qo2RRc_P5iHt-OTmhT4lDJGtNvxXfzv0O84S1babG_7La10je09uOpnxURYKQx_0OlZUuGpFjTw=="

# 登录所需的数据
form_data = {
    'username': 'xxxxx',
    'password': 'xxxxx'
}
body = urlencode(form_data)

# 发送POST请求
headers = {
    'Content-Type': "application/x-www-form-urlencoded;charset=UTF-8",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}

token = ""
response = requests.get(url, headers=headers, verify=False)

# 检查响应
if response.ok:
    print('登录成功!')
    print(response.text)  # 打印服务器的响应内容
    print(response.url)
    parsed_data = json.loads(response.text)
    token = parsed_data['data']["token"]
    print(token)
else:
    print('登录失败:', response.status_code)
import ddddocr
from selenium import webdriver
import json

import time
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.chrome.options import Options
from PIL import Image
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import base64
import io


def url_to_image(data_uri):
    # # 分割 Data URI 以获取 Base64 编码的部分
    _, encoded_image = data_uri.split(',', 1)
    # 解码 Base64 字符串为二进制数据
    decoded_image = base64.b64decode(encoded_image)
    # 使用 PIL 库将二进制数据转换为图像对象
    image = Image.open(io.BytesIO(decoded_image))
    return image

# ocr = ddddocr.DdddOcr(use_gpu=False,show_ad=False,beta=True)

# image = open("3737.jpeg", "rb").read()
# ocr.set_ranges(0)  # 0:纯数字  6:大小写加数字
# result = ocr.classification(image, probability=False,png_fix=True)
# # s = ""
# # for i in result['probability']: # probability为true时的处理方法
# #     s += result['charsets'][i.index(max(i))]

# print(result)
myUserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
cookies = {'name': 'lianjia_token', 'value': '2.0015d6f6987bb6dc8a047bdfa9ec1edb32'}

# 设置无头模式
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-extensions')
options.add_argument("disable-blink-features=AutomationControlled")
options.add_argument(
    f'user-agent={myUserAgent}')
options.add_argument(
    f'user-agent={myUserAgent}')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
driver = None
try:
    
    driver = webdriver.Chrome(options=options) 
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": """
    #         Object.defineProperty(navigator, 'webdriver', {
    #         get: () => undefined
    #         })
    #     """
    #     })
    driver.get("https://nc.lianjia.com/ershoufang/co32/") #https://nc.lianjia.com/ershoufang/co32/
    driver.add_cookie(cookies)
    driver.refresh()
    time.sleep(3)
    cookies = driver.get_cookies()
    print("*****************cookies****************")
    print(cookies)
    driver.save_screenshot('temp0.png')
    curUrl = driver.current_url
    while curUrl.find('captcha?location=https') != -1:
        wait = WebDriverWait(driver, 5)#最长等待时长
        buttonElement=wait.until(EC.presence_of_element_located((By.CLASS_NAME, "bk-captcha-btn")))
        try:
            buttonElement.click()
        except:
            pass
        time.sleep(1) #等待验证码刷新
        print("**********************imageurl********************")
        # *******************url方式获取原图(base64编码)*********
        element = driver.find_element(By.NAME, "imageCaptcha")
        imageUrl = element.get_attribute('src')
        codeImage = url_to_image(imageUrl)
        
        # **************截图方式获取验证码图*****************
        # driver.save_screenshot('temp.png')
        # image = cv2.imread('temp.png')
        # # (x, y) 裁剪区域左上角坐标，w 和 h 分别是裁剪区域的宽度和高度
        # x, y, w, h = 260, 170, 200, 70
        # cropped_image = image[y:y+h, x:x+w]
        # cv2.imwrite('temp2.jpg', cropped_image)
        # codeImage = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        
        ocr = ddddocr.DdddOcr(use_gpu=False,show_ad=False,beta=True)
        ocr.set_ranges(0)  # 0:纯数字  6:大小写加数字
        result = ocr.classification(codeImage, probability=False,png_fix=True)
        print(f"******************{result}****************")
        input_element = driver.find_element(By.NAME, "imageCaptchaCode")
        input_element.clear()
        input_element.send_keys(result) # 填写验证码
        driver.save_screenshot('temp1.png')
        time.sleep(3)
        curUrl = driver.current_url
    # print(driver.page_source)
    driver.save_screenshot('final.png')
    cookies = driver.get_cookies()
    print("*****************cookies****************")
    print(cookies)
finally:
    print("*****final******")
    if driver is not None:
        driver.quit()


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

import base64
import io
from lxml import html
import cv2


def url_to_image(encoded_image):
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

# 设置无头模式
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-extensions')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
# 指定ChromeDriver的路径（如果需要）
# driver = webdriver.Chrome(executable_path='~/app/chromedriver-linux64/chromedriver', options=options)
# 使用无头模式启动Chrome
driver = None
try:
    driver = webdriver.Chrome(options=options)
    driver.get("https://hip.lianjia.com/captcha?location=https%3A%2F%2Fnc.lianjia.com%2Fershoufang%2Fco32%2F&ext=8uCSus46f-3VBXcJh6HTLW4wekvT6WqbyNd2kw92kXTIt5aFXuL9LzwLckApSjkMLvCXMXRA8w_NNbFYIj5HXtb44C_phQpbush-lKKAje85BNNfVbkivCF6yVYt6RvroPDILjc-_MdZkHQRE_ej2Gq4MnRHta2UoSkC9983rppA")
    wait = WebDriverWait(driver, 10)#最长等待时长
    buttonElement=wait.until(EC.presence_of_element_located((By.CLASS_NAME, "bk-captcha-btn")))
    buttonElement.click()
    time.sleep(1) #等待验证码刷新
    print("**********************imageurl********************")
    # *******************url方式获取原图(base64编码)*********
    # h5content = driver.page_source
    # element = driver.find_element(By.NAME, "imageCaptcha")
    # imageUrl = element.get_attribute('src')
    # codeImage = url_to_image(imageUrl)
    
    # **************截图方式获取验证码图*****************
    driver.save_screenshot('temp.png')
    image = cv2.imread('temp.png')
    # (x, y) 裁剪区域左上角坐标，w 和 h 分别是裁剪区域的宽度和高度
    x, y, w, h = 260, 170, 200, 70
    cropped_image = image[y:y+h, x:x+w]
    cv2.imwrite('temp2.jpg', cropped_image)
    codeImage = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    
    ocr = ddddocr.DdddOcr(use_gpu=False,show_ad=False,beta=True)
    ocr.set_ranges(0)  # 0:纯数字  6:大小写加数字
    result = ocr.classification(codeImage, probability=False,png_fix=True)
    print(f"******************{result}****************")
    input_element = driver.find_element(By.NAME, "imageCaptchaCode")
    driver.save_screenshot('temp3.png')
    input_element.clear()
    input_element.send_keys(result) # 填写验证码
    driver.save_screenshot('result.png')
    time.sleep(5)
    # print(driver.page_source)
    driver.save_screenshot('final.png')
finally:
    print("*****final******")
    if driver is not None:
        driver.quit()


import ddddocr
from selenium import webdriver
import json

import time
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException

import numpy as np
import cv2
from urllib.request import urlopen


def url_to_image(url):
    resp = urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

ocr = ddddocr.DdddOcr(use_gpu=False,show_ad=False,beta=True)

image = open("3737.jpeg", "rb").read()
ocr.set_ranges(0)  # 0:纯数字  6:大小写加数字
result = ocr.classification(image, probability=False,png_fix=True)
# s = ""
# for i in result['probability']: # probability为true时的处理方法
#     s += result['charsets'][i.index(max(i))]

print(result)


driver = webdriver.PhantomJS()
driver.get("https://hip.lianjia.com/captcha?location=https%3A%2F%2Fnc.lianjia.com%2Fershoufang%2Fco32%2F&ext=8uCSus46f-3VBXcJh6HTLW4wekvT6WqbyNd2kw92kXTIt5aFXuL9LzwLckApSjkMLvCXMXRA8w_NNbFYIj5HXtb44C_phQpbush-lKKAje85BNNfVbkivCF6yVYt6RvroPDILjc-_MdZkHQRE_ej2Gq4MnRHta2UoSkC9983rppA")
wait = WebDriverWait(driver, 10)#最长等待时长

wait.until(EC.presence_of_element_located((By.CLASS_NAME, "bk-captcha-btn")))
print(driver.page_source)
element = driver.find_element(By.CLASS_NAME, "bk-captcha-btn")
imageUrl = element.get_attribute('src')
print(imageUrl)
codeImage = url_to_image(imageUrl)
ocr = ddddocr.DdddOcr(use_gpu=False,show_ad=False,beta=True)
ocr.set_ranges(0)  # 0:纯数字  6:大小写加数字
result = ocr.classification(codeImage, probability=False,png_fix=True)
input_element = driver.find_element(By.NAME, "imageCaptchaCode")
input_element.clear()
# 向 input 元素发送键盘输入
input_element.send_keys(result)
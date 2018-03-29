#!/usr/bin/python
# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import re
import requests
import urllib
from PIL import Image
import cv2
from io import BytesIO
import pytesseract
import numpy as np
import ahocorasick
import time


def check(driver, banned_list):
    '''检测文本违禁词'''

    result = driver.find_element_by_xpath("//*").text
    with open("./encryption_banned_word.txt", "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            line = line.decode('utf-8')
            if line in result:
                banned_list.append(line)


def iframe_check(driver, banned_list):
    tag_iframe = driver.find_elements_by_tag_name("iframe")
    for iframe in tag_iframe:
        # http = re.match(r"(^http).*", iframe.get_attribute("src"))
        driver.switch_to.frame(iframe)
        # 检测里面的文本信息
        check(driver, banned_list)
        # 切换回默认的document
        driver.switch_to.default_content()


def image_check(driver, banned_list):
    node_list = []
    url_list = []
    # 图片识别
    tag_a = driver.find_elements_by_tag_name("a")
    for a in tag_a:
        if domain not in a.get_attribute("href"):
            node_list.append(a)
            tag_img = a.find_elements_by_tag_name("img")
            for img in tag_img:
                if domain not in img.get_attribute("src"):
                    url_list.append(img.get_attribute("src"))

    text_list = []
    text = ""
    for url in url_list:
        response = requests.get(url).content
        # 直接使用response返回的数据
        image = Image.open(BytesIO(response))
        # 灰度化
        image = image.convert("L")
        # 将PIL读取的图片，转化为opencv支持的格式。COLOR_BAYER_GR2GRAY转为灰度
        image = cv2.cvtColor(np.asarray(image), cv2.COLOR_BAYER_GR2GRAY)
        retval, im = cv2.threshold(np.asarray(image), 127, 255, cv2.THRESH_BINARY_INV)

        # cv2.imwrite("./cv2.png", im)

        text = text + "\n" + pytesseract.image_to_string(image, lang="chi_sim")

    text = re.sub(r"\s+", "", text)
    # 检测识别出来的文本
    check(text, banned_list)


if __name__ == "__main__":
    start = time.time()
    try:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(chrome_options=options)
        # driver.set_window_size(1920, 1080)
        # domain = "http://www.baidu.com"
        domain = "http://www.cardesigner.com.cn/"
        driver.get(domain)

        banned_list = []
        # 检测文本
        check(driver, banned_list)

        # 内联框架
        iframe_check(driver, banned_list)

        # 图片识别
        # image_check()

        print "检测出来的结果有%d个，具体为%s." % (len(banned_list), banned_list)
        for i in banned_list:
            print i

    except Exception as e:
        print e
    finally:
        driver.quit()
        end = time.time()
        print (end - start)


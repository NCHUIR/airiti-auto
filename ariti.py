import os
import re
import time

import pytesseract
import requests
from PIL import Image
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from config import download_temp_path, captcha_temp, captcha2_temp


def get_tbody(browser: WebDriver):
    return browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[9]/table/tbody')


def convert_img(img, threshold):
    img = img.convert("L") # 處理灰度
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    return img


def download_file(browser: WebDriver, doc_id: str):
    try:
        browser.execute_script("_Layout_DownloadAuthority('" + doc_id + "', 'P001', 'P001', 0)")
        time.sleep(0.5)
        ok = False
        while True:
            input = browser.find_element_by_css_selector('input[name="ValidateCode"]')
            submit = browser.find_elements_by_css_selector('.ui-dialog-buttonset button')[0]
            time.sleep(0.3)
            with open(captcha_temp, 'wb') as file:
                file.write(browser.find_element_by_css_selector('img[alt="驗證碼圖片"]').screenshot_as_png)
            img = Image.open(captcha_temp)
            img = convert_img(img, 192)
            img.save(captcha2_temp)
            text = pytesseract.image_to_string(img, lang='eng')
            text = str(text).replace(" ","").replace("\n","").replace("\f","")
            print('##' + text + '##')          
            if text == '' or text is None:
                refresh = browser.find_element_by_xpath('/html/body/div[9]/div[2]/p/a').click()
                print('hello')
                time.sleep(0.1)
                continue
            input.send_keys(text)
            time.sleep(0.1)
            submit.click()
            time.sleep(0.1)
            try:
                browser.switch_to.alert.accept()
                continue
            except NoAlertPresentException:
                pass
    except BaseException:
        pass
    while len(os.listdir(download_temp_path)) == 0:
        time.sleep(1)
    time.sleep(1)
    return download_temp_path + os.path.sep + os.listdir(download_temp_path)[0]


def get_page_count(browser: WebDriver):
    pc_span = browser.find_element_by_xpath('//*[@id="_DocumentInfo"]/div[1]/div[2]/div[2]/div/span')
    s = re.search(r'\d+', pc_span.text).group()
    return int(s)



def get_ris_text(docId: str):
    params = {
        'ExportType': 'Ris', 'DocIDs[0]': docId, 'parameter': '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16'
    }
    r = requests.get('http://www.airitilibrary.com/publication/ExportTo', params=params)
    return r.text


def get_all_doc_ids(browser: WebDriver):
    tbody = get_tbody(browser)
    doc_check_boxes = tbody.find_elements_by_css_selector('input')
    ids = []
    for box in doc_check_boxes:
        ids.append(box.get_attribute('value'))
    return ids

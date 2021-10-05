from selenium import webdriver
import time
import requests
import threading

# 載入驅動
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

targetURL = "https://www.apple.com/tw/shop/buy-iphone/iphone-13-pro/6.1-%E5%90%8B%E9%A1%AF%E7%A4%BA%E5%99%A8-256gb-%E9%8A%80%E8%89%B2"
lineToken = "ef1AXvgyTCpTakegmVsxSlgQ2fwpovtgVzpEFx3hjzb"


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def call():
    print('hello!')


def main():

    options = webdriver.ChromeOptions()
    options.add_experimental_option(
        "excludeSwitches", ['enable-automation', 'enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("prefs", {
                                    "profile.password_manager_enabled": False, "credentials_enable_service": False})

    driver = webdriver.Chrome(options=options)
    driver.get(targetURL)
    driver.find_element_by_id('noTradeIn_label').click()
    try:
        WebDriverWait(driver, 10, 0.5).until(
            # 條件：直到元素載入完成
            lambda x: x.find_element_by_class_name(
                'rc-prices-fullprice').is_displayed())

        text = driver.find_element_by_xpath(
            '/html/body/div[2]/div[5]/div[5]/div[2]/div[4]/div[2]/div[5]/div[1]/div/div[2]/div/div/div[2]/div/div/span[2]').text

        if(text == '目前在 Apple 台北 101 缺貨' or text == ''):
            print(text)
            driver.close()
        else:
            notify("iphone13 Pro 銀色"+text)
            driver.close()
    except ValueError:
        print('Error')
        driver.close()


def notify(text):
    headers = {
        "Authorization": "Bearer " + lineToken,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {"message": text}

    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, params=params)


set_interval(main, 30)

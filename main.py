from selenium import webdriver
import time
import requests
import threading


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

    driver = webdriver.Chrome()
    driver.get("https://www.apple.com/tw/shop/buy-iphone/iphone-13-pro/6.1-%E5%90%8B%E9%A1%AF%E7%A4%BA%E5%99%A8-256gb-%E9%8A%80%E8%89%B2")
    driver.find_element_by_id('noTradeIn_label').click()
    driver.find_element_by_class_name(
        'rf-pickup-quote-storelink').is_displayed()
    text = driver.find_element_by_xpath(
        '/html/body/div[2]/div[5]/div[5]/div[2]/div[4]/div[2]/div[5]/div[1]/div/div[2]/div/div/div[2]/div/div/span[2]').text
    if(text == '目前在 Apple 台北 101 缺貨' or text == ''):
        driver.close()
    else:
        notify("iphone13 Pro 銀色"+text)
        driver.close()


def notify(text):
    headers = {
        "Authorization": "Bearer " + "ef1AXvgyTCpTakegmVsxSlgQ2fwpovtgVzpEFx3hjzb",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    params = {"message": text}

    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, params=params)


set_interval(main, 30)
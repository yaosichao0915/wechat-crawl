from selenium import webdriver
import json
import re
import time
from datetime import datetime
import auto_mail
import os
import logging
import log_config
logger = log_config.log('login')
def renew():
    with open('login.txt', 'a+', encoding='utf-8') as f:
        f.write("%s 触发 \n"%(datetime.now()))
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('user-data-dir=ChromeProfile')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    with open('cookie.txt', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read()) 
    driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)
    driver.get('https://mp.weixin.qq.com/')
    driver.get_screenshot_as_file("home.png")
    try:
                token = re.findall(r'token=(\d+)', str(driver.current_url))[0]
                logger.info("成功登录")
                write_cookie(driver)
                logger.info("写入成功")
                driver.quit()
                return(0)
    except:
        try:
            driver.find_element_by_xpath(u"(//a[contains(text(),'登录')])[3]").click()
            time.sleep(2)
            driver.find_element_by_link_text(u"发送验证").click()
        except:
            logger.info("非简易登录")
            try:
                driver.find_element_by_xpath('//a[@class="login__type__container__select-type login__type__container__select-type__scan"]').click()
                time.sleep(5)
                logger.info("获取二维码成功")
                driver.get_screenshot_as_file("QR.png")
                auto_mail.QRscan()
            except:
                logger.info("切换二维码失败，可能已经是二维码状态")
                driver.get_screenshot_as_file("QR.png")
                auto_mail.QRscan()
        time.sleep(150)
        try:
            token = re.findall(r'token=(\d+)', str(driver.current_url))[0]
            logger.info("成功登录")
            driver.get_screenshot_as_file("sucess.png")
            write_cookie(driver)
            driver.quit()
            return(0)
        except:
            logger.info("登录错误，需要替换")
            driver.quit()
            return(1)
   
    
def write_cookie(driver):
    post = {}
    cookie_items = driver.get_cookies()
    for cookie_item in cookie_items:       
        post[cookie_item['name']] = cookie_item['value']     
        cookie_str = json.dumps(post)      
    with open('cookie.txt', 'w+', encoding='utf-8') as f:
        f.write(cookie_str)
    



 


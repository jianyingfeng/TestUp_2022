import json
import os
from selenium import webdriver

from Web.chapter_001.lib.log import logger


# 失败的原因是还需要加上token才能认证通过
driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://staff.nct-test.com/')
path = "cookies.txt"
cookie_exist = os.path.isfile(path)
# 如果cookie文件不存在，则需要生成
if not cookie_exist:
    logger.info("开始生成cookies.txt")
    driver.get('https://passport.nct-test.com/')
    driver.find_element_by_id('login_account').send_keys('Jane')
    driver.find_element_by_id('login_userPassword').send_keys('123456')
    driver.find_element_by_class_name('login-btn__25f4u').click()
    cookies = driver.get_cookies()
    with open(path, 'w') as fp:
        json.dump(cookies, fp)
    logger.info("生成cookies.txt完毕")
else:
    with open(path, 'r') as fp:
        cookies = json.load(fp)
        for cookie in cookies:
            cookie.pop('domain')
            logger.info(f"增加cookies={cookie}")
            driver.add_cookie(cookie)
driver.get('https://staff.nct-test.com/exam/examination')
driver.close()
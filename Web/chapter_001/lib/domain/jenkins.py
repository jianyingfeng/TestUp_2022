import json
import os
import requests

from Web.chapter_001.lib.log import logger


# 保存cookie到本地
def generate_login_cookies(driver, path='cookies.txt', user='admin',
                           password='admin', base_url='http://localhost:8080'):
    logger.info("开始生成cookies.txt")
    # driver = Operations(Browser.start_chrome())
    driver.open(f"{base_url}/login?from=/")
    driver.input("name:j_username", user)
    driver.input("name:j_password", password)
    driver.click("name:Submit")
    # 保存cookie到本地
    cookies = driver.driver.get_cookies()
    with open(path, 'w') as fp:
        # 写入文件后是双引号，用json.load()只能读双引号，读单引号会报错，只能用eval()读取
        json.dump(cookies, fp)
        # 写入文件后是单引号
        # fp.write(str(cookies))
    # driver.close()
    logger.info("生成cookies.txt完毕")


# 检查cookie是否失效
def check_if_cookie_still_works(path, browser, user, base_url='http://localhost:8080'):
    logger.info("开始检查cookie是否已过期")
    # 让浏览器读取cookie文件中的cookie
    browser.add_cookies_from_file(path)
    browser.open(base_url)
    text = browser.get_text("class:login").strip()
    # 判断cookie是否过期
    if text == f"{user} | 注销":
        logger.info("cookie未过期")
        return True
    else:
        logger.info("cookie已过期")
        return False


class Jenkins:
    def __init__(self, base_url='http://localhost:8080', user='admin', password='admin'):
        self.base_url = base_url
        self.session = requests.session()
        self.session.auth = user, password
        self.get_crumb()

    def login_jenkins(self, browser, user='admin', path="cookies.txt"):
        cookie_exist = os.path.isfile(path)
        # 如果cookie文件不存在，则需要生成
        if not cookie_exist:
            generate_login_cookies(browser)
        # 如果cookie文件已经存在,则不需要生成
        else:
            # 校验cookie是否过期
            cookie_valid = check_if_cookie_still_works(path, browser, user)
            if not cookie_valid:
                generate_login_cookies(browser)

    def get_crumb(self):
        r = self.session.get(f'{self.base_url}/crumbIssuer/api/json/')
        key = r.json()['crumbRequestField']
        value = r.json()['crumb']
        self.session.headers[key] = value

    # 删除单个job
    def delete_job(self, job_name):
        r = self.session.post(f'{self.base_url}/job/{job_name}/doDelete', allow_redirects=False)
        if r.status_code == 200:
            logger.info(f"job：{job_name}删除成功")
            return True
        else:
            logger.info(f"job：{job_name}删除失败")
            return False

    # 检查job是否存在
    def check_job_exists(self, job_name):
        r = self.session.post(f'{self.base_url}/job/{job_name}/api/json')
        if r.status_code == 200:
            logger.info(f'{job_name}存在')
            return True
        else:
            logger.info(f'{job_name}不存在')
            return False

    # 删除单个user
    def delete_user(self, user_name):
        # 一个crumb无法删除多个账号，所以每次都需要重新获取
        self.get_crumb()
        r = self.session.post(f'{self.base_url}/user/{user_name}/doDelete')
        if r.status_code == 200:
            logger.info(f"用户：{user_name}删除成功")
            return True
        else:
            logger.info(f"用户：{user_name}删除失败")
            return False

    # 注册user
    def register_user(self, payload):
        # 一个crumb无法注册多个账号，所以每次都需要重新获取
        self.get_crumb()
        r = self.session.post(f'{self.base_url}/securityRealm/createAccount', data=payload)
        return r

    # 检查user是否存在
    def check_user_exists(self, user_name):
        r = self.session.get(f'{self.base_url}/user/{user_name}/api/json/')
        if r.status_code == 200:
            # logger.info(f"用户：{user_name}存在")
            return True
        else:
            # logger.info(f"用户：{user_name}不存在")
            return False

    # 注册测试用户（属于业务方法）
    def register_test_user(self, username, password):
        paylaod = {
            "username": username,
            "fullname": username,
            "email": username + '@qq.com',
            "password1": password,
            "password2": password,
        }
        self.register_user(paylaod)
        user_exists = self.check_user_exists(username)
        if user_exists:
            logger.info(f"注册成功，用户：{username}，密码：{password}")
        else:
            logger.info(f"注册失败，用户：{username}，密码：{password}")
            return user_exists

    # 获取用户名称列表
    def get_user_list(self):
        r = self.session.get(f'{self.base_url}/asynchPeople/api/json')
        absoluteUrl_list = [i['user']['absoluteUrl'] for i in r.json()['users']]
        user_list = [j.split('/')[-1] for j in absoluteUrl_list]
        logger.info(f'用户名列表：{user_list}')
        return user_list


if __name__ == '__main__':
    admin = Jenkins()
    user_list = admin.get_user_list()
    print(user_list)

from Web.chapter_001.lib.log import logger
from Web.chapter_001.lib.browser import Browser
from Web.chapter_001.lib.operations import Operations
from Web.chapter_001.lib.domain.jenkins import Jenkins


# 用户登录
def test_01():
    logger.info("用户登录场景开始，admin/admin")
    driver = Operations(Browser.start_chrome())
    driver.open("http://localhost:8080/login?from=/")
    driver.input("name:j_username", "admin")
    driver.input("name:j_password", "admin")
    driver.click("name:Submit")
    assert driver.current_url == "http://localhost:8080/",\
        f"预期url为：http://localhost:8080/，实际值为{driver.current_url}"
    driver.close()
    logger.info("用户登录场景结束，admin/admin")


# 用户快捷登录
def test_02():
    logger.info("用户快捷登录开始，admin/admin")
    admin = Jenkins()
    driver = Operations(Browser.start_chrome())
    driver.open("http://localhost:8080")
    text = driver.get_text("class:login").strip()
    assert text == "登录 | 注册", "断言失败，当前是登录状态"
    admin.login_jenkins(driver, user='admin')
    driver.open("http://localhost:8080")
    text = driver.get_text("class:login").strip()
    assert text == "admin | 注销", "断言失败，当前未登录"
    driver.close()
    logger.info("用户登录场景结束，admin/admin")

from Web.chapter_001.lib.log import logger
from Web.chapter_001.lib.browser import Browser
from Web.chapter_001.lib.operations import Operations
from Web.chapter_001.lib.domain.jenkins import Jenkins


# 新建一个job
def test_03():
    logger.info("用户快捷登录开始，admin/admin")
    admin = Jenkins()
    # 先删除job
    admin.delete_job('test_job')
    driver = Operations(Browser.start_chrome())
    driver.open("http://localhost:8080")
    admin.login_jenkins(driver, 'admin')
    driver.click("class:task-link")
    driver.input("xpath://input[@data-valid='false']", "test_job")
    driver.click("class:hudson_model_FreeStyleProject")
    driver.click("id:ok-button")
    driver.click("id:yui-gen43-button")
    assert admin.check_job_exists('test_job') == True
    driver.close()
    logger.info("用户登录场景结束，admin/admin")


# 注册用户
def test_04():
    logger.info("注册用户场景开始，Jane/123456")
    admin = Jenkins()
    # 先删除用户
    admin.delete_user('Jane')
    driver = Operations(Browser.start_chrome())
    driver.open('http://localhost:8080/login?from=%2F')
    driver.click('partial_link:创建一个用户账号')
    driver.input('id:username', 'Jane')
    driver.input('id:fullname', '南风')
    driver.input('id:email', '1055193533@qq.com')
    driver.input('id:password1', 123456)
    driver.click('name:Submit')
    text = driver.get_text('class:login').strip()
    assert text == '南风 | 注销', "断言失败，当前未登录"
    driver.close()
    logger.info("注册用户场景结束，Jane/123456")


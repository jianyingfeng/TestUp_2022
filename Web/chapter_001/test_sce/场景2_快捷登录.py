from Web.chapter_001.lib.log import logger
from Web.chapter_001.lib.browser import Browser
from Web.chapter_001.lib.operations import Operations
from Web.chapter_001.lib.domain.jenkins import Jenkins


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
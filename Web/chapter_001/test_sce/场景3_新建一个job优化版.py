from Web.chapter_001.lib.log import logger
from Web.chapter_001.lib.browser import Browser
from Web.chapter_001.lib.operations import Operations
from Web.chapter_001.lib.domain.jenkins import Jenkins


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

from Web.chapter_001.lib.log import logger
from Web.chapter_001.lib.browser import Browser
from Web.chapter_001.lib.operations import Operations
from Web.chapter_001.lib.domain.jenkins import Jenkins


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

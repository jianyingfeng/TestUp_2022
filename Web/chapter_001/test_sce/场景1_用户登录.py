from Web.chapter_001.lib.log import logger
from Web.chapter_001.lib.browser import Browser
from Web.chapter_001.lib.operations import Operations


logger.info("用户登录场景开始，admin/admin")
driver = Operations(Browser.start_chrome())
driver.open("http://localhost:8080/login?from=/")
driver.input("name:j_username", "admin")
driver.input("name:j_password", "admin")
driver.click("name:Submit")
assert driver.current_url == "http://localhost:8080/", f"预期url为：http://localhost:8080/，实际值为{driver.current_url}"
driver.close()
logger.info("用户登录场景结束，admin/admin")
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("http://127.0.0.1:8080/login?from=%2F")
ele = driver.find_element(By.LINK_TEXT, "创建一个用户账号")
# 获取元素属性
print(ele.text)
# 获取元素标签名
print(ele.tag_name)
driver.quit()

from selenium import webdriver
from selenium.webdriver.support.select import Select


driver = webdriver.Chrome()
driver.maximize_window()
driver.get("http://localhost:8080/login?from=/")
driver.find_element_by_name("j_username").send_keys("admin")
driver.find_element_by_name("j_password").send_keys("admin")
driver.find_element_by_name("Submit").click()
driver.find_element_by_link_text("Manage Jenkins").click()
driver.find_element_by_xpath("//a[@href='configure']").click()
# 定位下拉框
select_ele = driver.find_element_by_class_name("dropdownList")
# 获取下拉框下所有选项
all_options = select_ele.find_elements_by_tag_name("option")
# 获取下拉框下所有选项的文本
texts = [i.text for i in all_options]
print(all_options)
print(texts)
# 初始化一个下拉框的实例
select_ele = Select(select_ele)
select_ele.select_by_index(2)
# driver.quit()
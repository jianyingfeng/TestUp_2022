# -*- coding: gbk -*-
from selenium.webdriver.common.by import By
from selenium import webdriver
from Web.chapter_001.lib.log import logger
import json


class Operations:
    # 初始化方法，接受一个selenium driver的对象作为传入参数
    def __init__(self, driver):
        self.driver = driver

    # 浏览器打开指定url
    def open(self, url):
        logger.info(f"浏览器打开url={url}")
        self.driver.get(url)

    # 取当前url
    # 当成属性使用，调用时不需要加括号
    @property
    def current_url(self):
        url = self.driver.current_url
        logger.info(f"浏览器获取当前url,url={url}")
        return url

    # 浏览器后退操作
    def back(self):
        logger.info(f"浏览器执行后退操作")
        self.driver.back()

    # 浏览器前进操作
    def forward(self):
        logger.info(f"浏览器执行前进操作")
        self.driver.forward()

    # 浏览器刷新操作
    def refresh(self):
        logger.info(f"浏览器执行刷新操作")
        self.driver.refresh()

    # 浏览器取标题
    @property
    def title(self):
        logger.info(f"开始浏览器获取标题")
        title = self.driver.title
        logger.info(f"浏览器获取标题={title}")
        return title

    # 关闭窗口或tab
    def close(self):
        logger.info(f"浏览器关闭当前窗口或tab")
        self.driver.close()

    # 退出浏览器
    def quit(self):
        logger.info(f"浏览器执行退出操作")
        self.driver.quit()

    # 获取当前窗口handle
    @property
    def current_window(self):
        logger.info(f"开始获取当前浏览器窗口句柄")
        window = self.driver.current_window_handle
        logger.info(f"获取当前浏览器窗口句柄={window}")
        return window

    # 切换到指定窗口
    def switch_to_window(self, window_handle):
        logger.info(f"开始切换浏览器窗口，"
                    f"新窗口句柄={window_handle}")
        self.driver.switch_to.window(window_handle)
        logger.info(f"切换浏览器窗口完毕")

    # 打开并切换至新窗口
    def create_new_window_and_switch(self):
        logger.info(f"浏览器打开并切换至新窗口")
        self.driver.switch_to.new_window('window')
        logger.info(f"切换浏览器窗口完毕")

    # 打开并切换至新tab
    def create_new_tab_and_switch(self):
        logger.info(f"浏览器打开并切换至新tab")
        self.driver.switch_to.new_window('tab')
        logger.info(f"切换浏览器窗口完毕")

    # 切换至frame中
    # 原生支持页面元素，id，name或索引
    def switch_to_frame(self,iframe):
        logger.info(f"浏览器切换至新iframe={iframe}")
        self.driver.switch_to.frame(iframe)
        logger.info(f"切换浏览器窗口完毕")

    # 退出frame
    def leave_frame(self):
        logger.info(f"浏览器开始退出iframe")
        self.driver.switch_to.default_content()
        logger.info(f"切换浏览器窗口完毕")

    # 获取窗口尺寸
    def get_window_size(self):
        logger.info(f"获取当前窗口尺寸")
        size = self.driver.get_window_size()
        width = size.get("width")
        height = size.get("height")
        logger.info(f"窗口尺寸为宽={width}")
        logger.info(f"窗口尺寸为长={height}")
        return width, height

    # 设置窗口尺寸
    def set_window_size(self, width, height):
        logger.info(f"设置当前窗口尺寸")
        logger.info(f"窗口尺寸为宽={width}")
        logger.info(f"窗口尺寸为长={height}")
        self.driver.set_window_size(width, height)

    # 获取窗口位置
    def get_window_position(self):
        logger.info(f"获取当前窗口坐标")
        position = self.driver.get_window_position()
        x = position.get('x')
        y = position.get('y')
        logger.info(f"窗口坐标为x={x}")
        logger.info(f"窗口坐标为y={y}")
        return x, y

    # 设置窗口位置
    def set_window_position(self, x, y):
        logger.info(f"设置当前窗口坐标")
        logger.info(f"窗口坐标为x={x}")
        logger.info(f"窗口坐标为y={y}")
        self.driver.set_window_position(x, y)
        logger.info(f"设置当前窗口坐标完毕")

    # 最大化窗口
    def maximize_window(self):
        logger.info(f"浏览器窗口最大化开始")
        self.driver.maximize_window()
        logger.info(f"浏览器窗口最大化完毕")

    # 最小化窗口
    def minimize_window(self):
        logger.info(f"浏览器窗口最小化")
        self.driver.minimize_window()
        logger.info(f"浏览器窗口最小化完毕")

    # 窗口全屏
    def fullscreen_window(self):
        logger.info(f"浏览器窗口切换全屏开始")
        self.driver.fullscreen_window()
        logger.info(f"浏览器窗口切换全屏完毕")

    # 截图
    def save_screenshot(self, path):
        logger.info(f"浏览器截图，保存路径={path}")
        self.driver.save_screenshot(path)
        logger.info(f"浏览器截图完毕")

    # 单个元素截图
    def save_element_screenshot(self, value, path):
        logger.info(f"单个元素截图，"
                    f"元素={value}，保存路径={path}")
        if type(value) == str:
            element = self.find_element(value)
        else:
            element = value
        element.save_screenshot(path)
        logger.info(f"单个元素截图完毕")

    # 封装的每个操作都支持两种模式：
    # 1.如果传入locator，则用先定位后操作，
    # 2.如果传入页面元素，则直接做操作
    def click(self, value):
        logger.info(f"在元素='{value}'上执行鼠标点击")
        if type(value) == str:
            element = self.find_element(value)
        else:
            element = value
        element.click()

    # 封装的操作名称可以和selenium的原生方法名不同
    # 此处把send_keys改成了input
    def input(self, value, text):
        logger.info(f"在元素='{value}'上输入文本={text}")
        if type(value) == str:
            element = self.find_element(value)
        else:
            element = value
        element.send_keys(text)

    # 封装了清除已输入内容的clear方法
    def clear(self, value):
        logger.info(f"在元素='{value}'上清空文本")
        if type(value) == str:
            element = self.find_element(value)
        else:
            element = value
        element.clear()

    # selenium原生的ActionChains操作接口写法异常复杂
    # 此处对它做了二次封装简化其语法
    # 封装了鼠标双击操作
    def double_click(self, value):
        logger.info(f"在元素={value}上执行鼠标双击")
        if type(value) == str:
            element = self.find_element(value)
        else:
            element = value
        webdriver.ActionChains(self.driver).\
                double_click(element).perform()

    # 封装了通过页面元素位置来确定拖放目标位置的拖放操作
    def drag_and_drop(self, source_value, target_value):
        logger.info(f"把元素={source_value}"
                    f"拖动到元素={target_value}所在位置")
        if type(source_value) == str:
            source_element = self.find_element(source_value)
        else:
            source_element = source_value

        if type(target_value) == str:
            target_element = self.find_element(target_value)
        else:
            target_element = target_value
        webdriver.ActionChains(self.driver). \
            drag_and_drop(source_element, target_element).perform()

    # 封装了通过坐标来确定拖放目标位置的拖放操作
    def drag_and_drop_by_offset(self, source_value, x_offset, y_offset):
        logger.info(f"把元素={source_value}"
                    f"拖动水平位移={x_offset}，垂直位移={y_offset}")
        if type(source_value) == str:
            source_element = self.find_element(source_value)
        else:
            source_element = source_value
        webdriver.ActionChains(self.driver).\
            drag_and_drop_by_offset(source_element, x_offset,
                                    y_offset).perform()

    # 封装了把鼠标移动到元素上的操作
    def move_to_element(self, value):
        logger.info(f"把鼠标移动到元素={value}上")
        if type(value) == str:
            target_element = self.find_element(value)
        else:
            target_element = value
        webdriver.ActionChains(self.driver). \
            move_to_element(target_element).perform()

    # 封装了把鼠标移动指定坐标的操作
    def move_by_offset(self, x_offset, y_offset):
        logger.info(f"把鼠标移动水平位移={x_offset}，垂直位移={y_offset}")
        webdriver.ActionChains(self.driver). \
            move_by_offset(x_offset, y_offset).perform()

    # TODO: 可以继续封装更多的操作。
    # 从文件中读取cookie，并使其生效
    def add_cookies_from_file(self, path='cookies.txt'):
        with open(path, 'r') as fp:
            cookies = json.load(fp)
            # cookies = eval(fp.read())
            # 添加cookie之前，务必保证浏览器已经打开了和登录页相同域名的页面
            for cookie in cookies:
                cookie.pop('domain')
                logger.info(f"增加cookies={cookie}")
                self.driver.add_cookie(cookie)

    # 获取指定元素的文本
    def get_text(self, value):
        if type(value) == str:
            target_ele = self.find_element(value)
        else:
            target_ele = value
        logger.info(f"获取元素{value}的文本为：{target_ele.text}")
        return target_ele.text

    def find_element(self, locator):
        # 在这个自定义方法中传入参数的locator内使用冒号隔开定位语句的类型和值
        # 这也是对selenium繁琐语法的简化
        locator_text = locator.split(":")[0]
        # 此处join的目的是，以防元素定位表达式中有:号
        # 比如name:a:a
        locator_value = ":".join(locator.split(":")[1:])
        # 根据对定位语句的不同类型调用不同的原生方法来完成定位
        logger.info(f"定位元素,使用定位语句={locator}")
        if locator_text == "css":
            return self.driver.find_element(By.CSS_SELECTOR, locator_value)
        if locator_text == "id":
            return self.driver.find_element(By.ID, locator_value)
        if locator_text == "name":
            return self.driver.find_element(By.NAME, locator_value)
        if locator_text == "link":
            return self.driver.find_element(By.LINK_TEXT, locator_value)
        if locator_text == "partial_link":
            return self.driver.find_element(By.PARTIAL_LINK_TEXT, locator_value)
        if locator_text == "tag":
            return self.driver.find_element(By.TAG_NAME, locator_value)
        if locator_text == "class":
            return self.driver.find_element(By.CLASS_NAME, locator_value)
        if locator_text == "xpath":
            return self.driver.find_element(By.XPATH, locator_value)
        # TODO: 可以继续封装更多的自定义定位方式。

    # 封装过的定位多个元素
    def find_elements(self, locator):
        locator_text = locator.split(":")[0]
        locator_value = ":".join(locator.split(":")[1:])
        logger.info(f"定位元素,使用定位语句={locator}")
        if locator_text == "css":
            return self.driver.find_elements(By.CSS_SELECTOR, locator_value)
        if locator_text == "id":
            return self.driver.find_elements(By.ID, locator_value)
        if locator_text == "name":
            return self.driver.find_elements(By.NAME, locator_value)
        if locator_text == "link":
            return self.driver.find_elements(By.LINK_TEXT, locator_value)
        if locator_text == "partial_link":
            return self.driver.find_elements(By.PARTIAL_LINK_TEXT, locator_value)
        if locator_text == "tag":
            return self.driver.find_elements(By.TAG_NAME, locator_value)
        if locator_text == "class":
            return self.driver.find_elements(By.CLASS_NAME, locator_value)
        if locator_text == "xpath":
            return self.driver.find_elements(By.XPATH, locator_value)
        # TODO: 可以继续封装更多的自定义定位方式。

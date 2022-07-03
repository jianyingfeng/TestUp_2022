from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from Web.chapter_001.lib.log import logger


class Browser:
    # 启动火狐浏览器
    @staticmethod
    def start_firefox():
        logger.info("启动火狐浏览器")
        driver = webdriver.Firefox()
        driver.maximize_window()
        return driver

    # 启动谷歌浏览器
    @staticmethod
    def start_chrome():
        logger.info("启动谷歌浏览器")
        driver = webdriver.Chrome()
        driver.maximize_window()
        return driver

    # 启动headless模式的谷歌浏览器
    @staticmethod
    def start_headless_chrome():
        logger.info("启动谷歌浏览器headless模式")
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        return driver

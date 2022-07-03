# -*- coding: gbk -*-
from selenium.webdriver.common.by import By
from selenium import webdriver
from Web.chapter_001.lib.log import logger
import json


class Operations:
    # ��ʼ������������һ��selenium driver�Ķ�����Ϊ�������
    def __init__(self, driver):
        self.driver = driver

    # �������ָ��url
    def open(self, url):
        logger.info(f"�������url={url}")
        self.driver.get(url)

    # ȡ��ǰurl
    # ��������ʹ�ã�����ʱ����Ҫ������
    @property
    def current_url(self):
        url = self.driver.current_url
        logger.info(f"�������ȡ��ǰurl,url={url}")
        return url

    # ��������˲���
    def back(self):
        logger.info(f"�����ִ�к��˲���")
        self.driver.back()

    # �����ǰ������
    def forward(self):
        logger.info(f"�����ִ��ǰ������")
        self.driver.forward()

    # �����ˢ�²���
    def refresh(self):
        logger.info(f"�����ִ��ˢ�²���")
        self.driver.refresh()

    # �����ȡ����
    @property
    def title(self):
        logger.info(f"��ʼ�������ȡ����")
        title = self.driver.title
        logger.info(f"�������ȡ����={title}")
        return title

    # �رմ��ڻ�tab
    def close(self):
        logger.info(f"������رյ�ǰ���ڻ�tab")
        self.driver.close()

    # �˳������
    def quit(self):
        logger.info(f"�����ִ���˳�����")
        self.driver.quit()

    # ��ȡ��ǰ����handle
    @property
    def current_window(self):
        logger.info(f"��ʼ��ȡ��ǰ��������ھ��")
        window = self.driver.current_window_handle
        logger.info(f"��ȡ��ǰ��������ھ��={window}")
        return window

    # �л���ָ������
    def switch_to_window(self, window_handle):
        logger.info(f"��ʼ�л���������ڣ�"
                    f"�´��ھ��={window_handle}")
        self.driver.switch_to.window(window_handle)
        logger.info(f"�л�������������")

    # �򿪲��л����´���
    def create_new_window_and_switch(self):
        logger.info(f"������򿪲��л����´���")
        self.driver.switch_to.new_window('window')
        logger.info(f"�л�������������")

    # �򿪲��л�����tab
    def create_new_tab_and_switch(self):
        logger.info(f"������򿪲��л�����tab")
        self.driver.switch_to.new_window('tab')
        logger.info(f"�л�������������")

    # �л���frame��
    # ԭ��֧��ҳ��Ԫ�أ�id��name������
    def switch_to_frame(self,iframe):
        logger.info(f"������л�����iframe={iframe}")
        self.driver.switch_to.frame(iframe)
        logger.info(f"�л�������������")

    # �˳�frame
    def leave_frame(self):
        logger.info(f"�������ʼ�˳�iframe")
        self.driver.switch_to.default_content()
        logger.info(f"�л�������������")

    # ��ȡ���ڳߴ�
    def get_window_size(self):
        logger.info(f"��ȡ��ǰ���ڳߴ�")
        size = self.driver.get_window_size()
        width = size.get("width")
        height = size.get("height")
        logger.info(f"���ڳߴ�Ϊ��={width}")
        logger.info(f"���ڳߴ�Ϊ��={height}")
        return width, height

    # ���ô��ڳߴ�
    def set_window_size(self, width, height):
        logger.info(f"���õ�ǰ���ڳߴ�")
        logger.info(f"���ڳߴ�Ϊ��={width}")
        logger.info(f"���ڳߴ�Ϊ��={height}")
        self.driver.set_window_size(width, height)

    # ��ȡ����λ��
    def get_window_position(self):
        logger.info(f"��ȡ��ǰ��������")
        position = self.driver.get_window_position()
        x = position.get('x')
        y = position.get('y')
        logger.info(f"��������Ϊx={x}")
        logger.info(f"��������Ϊy={y}")
        return x, y

    # ���ô���λ��
    def set_window_position(self, x, y):
        logger.info(f"���õ�ǰ��������")
        logger.info(f"��������Ϊx={x}")
        logger.info(f"��������Ϊy={y}")
        self.driver.set_window_position(x, y)
        logger.info(f"���õ�ǰ�����������")

    # ��󻯴���
    def maximize_window(self):
        logger.info(f"�����������󻯿�ʼ")
        self.driver.maximize_window()
        logger.info(f"���������������")

    # ��С������
    def minimize_window(self):
        logger.info(f"�����������С��")
        self.driver.minimize_window()
        logger.info(f"�����������С�����")

    # ����ȫ��
    def fullscreen_window(self):
        logger.info(f"����������л�ȫ����ʼ")
        self.driver.fullscreen_window()
        logger.info(f"����������л�ȫ�����")

    # ��ͼ
    def save_screenshot(self, path):
        logger.info(f"�������ͼ������·��={path}")
        self.driver.save_screenshot(path)
        logger.info(f"�������ͼ���")

    # ����Ԫ�ؽ�ͼ
    def save_element_screenshot(self, value, path):
        logger.info(f"����Ԫ�ؽ�ͼ��"
                    f"Ԫ��={value}������·��={path}")
        if type(value) == str:
            element = self.find_element(value)
        else:
            element = value
        element.save_screenshot(path)
        logger.info(f"����Ԫ�ؽ�ͼ���")

    # ��װ��ÿ��������֧������ģʽ��
    # 1.�������locator�������ȶ�λ�������
    # 2.�������ҳ��Ԫ�أ���ֱ��������
    def click(self, value):
        logger.info(f"��Ԫ��='{value}'��ִ�������")
        if type(value) == str:
            element = self.find_element(value)
        else:
            element = value
        element.click()

    # ��װ�Ĳ������ƿ��Ժ�selenium��ԭ����������ͬ
    # �˴���send_keys�ĳ���input
    def input(self, value, text):
        logger.info(f"��Ԫ��='{value}'�������ı�={text}")
        if type(value) == str:
            element = self.find_element(value)
        else:
            element = value
        element.send_keys(text)

    # ��װ��������������ݵ�clear����
    def clear(self, value):
        logger.info(f"��Ԫ��='{value}'������ı�")
        if type(value) == str:
            element = self.find_element(value)
        else:
            element = value
        element.clear()

    # seleniumԭ����ActionChains�����ӿ�д���쳣����
    # �˴��������˶��η�װ�����﷨
    # ��װ�����˫������
    def double_click(self, value):
        logger.info(f"��Ԫ��={value}��ִ�����˫��")
        if type(value) == str:
            element = self.find_element(value)
        else:
            element = value
        webdriver.ActionChains(self.driver).\
                double_click(element).perform()

    # ��װ��ͨ��ҳ��Ԫ��λ����ȷ���Ϸ�Ŀ��λ�õ��ϷŲ���
    def drag_and_drop(self, source_value, target_value):
        logger.info(f"��Ԫ��={source_value}"
                    f"�϶���Ԫ��={target_value}����λ��")
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

    # ��װ��ͨ��������ȷ���Ϸ�Ŀ��λ�õ��ϷŲ���
    def drag_and_drop_by_offset(self, source_value, x_offset, y_offset):
        logger.info(f"��Ԫ��={source_value}"
                    f"�϶�ˮƽλ��={x_offset}����ֱλ��={y_offset}")
        if type(source_value) == str:
            source_element = self.find_element(source_value)
        else:
            source_element = source_value
        webdriver.ActionChains(self.driver).\
            drag_and_drop_by_offset(source_element, x_offset,
                                    y_offset).perform()

    # ��װ�˰�����ƶ���Ԫ���ϵĲ���
    def move_to_element(self, value):
        logger.info(f"������ƶ���Ԫ��={value}��")
        if type(value) == str:
            target_element = self.find_element(value)
        else:
            target_element = value
        webdriver.ActionChains(self.driver). \
            move_to_element(target_element).perform()

    # ��װ�˰�����ƶ�ָ������Ĳ���
    def move_by_offset(self, x_offset, y_offset):
        logger.info(f"������ƶ�ˮƽλ��={x_offset}����ֱλ��={y_offset}")
        webdriver.ActionChains(self.driver). \
            move_by_offset(x_offset, y_offset).perform()

    # TODO: ���Լ�����װ����Ĳ�����
    # ���ļ��ж�ȡcookie����ʹ����Ч
    def add_cookies_from_file(self, path='cookies.txt'):
        with open(path, 'r') as fp:
            cookies = json.load(fp)
            # cookies = eval(fp.read())
            # ���cookie֮ǰ����ر�֤������Ѿ����˺͵�¼ҳ��ͬ������ҳ��
            for cookie in cookies:
                cookie.pop('domain')
                logger.info(f"����cookies={cookie}")
                self.driver.add_cookie(cookie)

    # ��ȡָ��Ԫ�ص��ı�
    def get_text(self, value):
        if type(value) == str:
            target_ele = self.find_element(value)
        else:
            target_ele = value
        logger.info(f"��ȡԪ��{value}���ı�Ϊ��{target_ele.text}")
        return target_ele.text

    def find_element(self, locator):
        # ������Զ��巽���д��������locator��ʹ��ð�Ÿ�����λ�������ͺ�ֵ
        # ��Ҳ�Ƕ�selenium�����﷨�ļ�
        locator_text = locator.split(":")[0]
        # �˴�join��Ŀ���ǣ��Է�Ԫ�ض�λ���ʽ����:��
        # ����name:a:a
        locator_value = ":".join(locator.split(":")[1:])
        # ���ݶԶ�λ���Ĳ�ͬ���͵��ò�ͬ��ԭ����������ɶ�λ
        logger.info(f"��λԪ��,ʹ�ö�λ���={locator}")
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
        # TODO: ���Լ�����װ������Զ��嶨λ��ʽ��

    # ��װ���Ķ�λ���Ԫ��
    def find_elements(self, locator):
        locator_text = locator.split(":")[0]
        locator_value = ":".join(locator.split(":")[1:])
        logger.info(f"��λԪ��,ʹ�ö�λ���={locator}")
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
        # TODO: ���Լ�����װ������Զ��嶨λ��ʽ��

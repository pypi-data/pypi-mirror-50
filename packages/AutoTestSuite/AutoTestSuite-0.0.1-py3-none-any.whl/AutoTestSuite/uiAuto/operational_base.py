# _*_ coding:utf-8 _*_

# from appium import webdriver
# from AppiumAndroid.webdriver import webdriver
import os
class OperationalBase(object):
    def __init__(self,driver):
        # driver = webdriver.Remote()
        self.driver = driver

    def find_element(self,alloc):
        return self.driver.find_element(*alloc)

    def click(self,alloc):
        # print(*alloc)
        self.driver.find_element(*alloc).click()

    def reset(self):
        self.driver.reset()

    def refresh(self):
        self.driver.refresh()

    def input_text(self, alloc, text):
        self.driver.find_element(*alloc).send_keys(text)

    def get_text(self,alloc):
        return self.driver.find_element(*alloc).text

    def gets_text(self,alloc):
        return self.driver.find_elements(*alloc)

    #向上滑动
    def downSroll(self):
        element_size = self.driver.get_window_size()
        x = element_size["width"]
        y = element_size["height"]
        self.driver.swipe(500, int(y) / 2 + 120, 500, 100)

    #向下滑动
    def upwardSroll(self):
        element_size = self.driver.get_window_size()
        x = element_size["width"]
        y = element_size["height"]
        self.driver.swipe(500, 100, 500, int(y) / 2 + 120)

    #截图
    def screenshot(self, screenshot_path, name):
        '''
        :param screenshot_path: 配置截图的路径
        :param name: 保存截图名称，推荐用日期+名称
        :return:
        '''
        print(screenshot_path)
        if os.path.exists(screenshot_path) != True:
            os.mkdir(screenshot_path)

        self.driver.get_screenshot_as_file(screenshot_path + "/" + name + ".png")





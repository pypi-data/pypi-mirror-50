page = '''# _*_ coding:utf-8 _*_ 

import time
from AutoTestSuite.uiAuto.by import By
from AutoTestSuite.uiAuto.operational_base import OperationalBase

class %s(OperationalBase):
    permissions_button = (By.XPATH,"android.widget.Button")

    def __init__(self, driver):
        OperationalBase.__init__(self,driver)
        self.base = OperationalBase(driver)
        
'''


web_case = '''
from selenium import webdriver
import unittest
from page.webChrome import webPage
import os

class %s(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        path = os.path.abspath("../resource/driver/chrome")
        cls.driver = webdriver.Chrome(path)
        cls.driver.get("http://www.baidu.com")
        cls.base = webPage(cls.driver)
        
    @classmethod
    def tearDownClass(cls):
        pass

'''

appium_case = '''# _*_ coding:utf-8 _*_

import unittest
import time
from appium import webdriver
from AutoTestSuite.uiAuto.config import android_caps,getHost,appium_server_cmd
from AutoTestSuite.utils.interface import subprocess_cmd

class %s(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        aapt_path = "/Library/android_sdk/build-tools/26.0.2/aapt"  # 环境变量配置好后，无需再配置aapt路径
        adb_path = "/Library/android_sdk/platform-tools/adb"  # 环境变量配置好后，无需再配置adb路径
        app_path = "/Users/liaozhenghong/Downloads/douyin.apk"
        udid = "c466fa9e"
        caps = android_caps(udid, app_path, adb_path, aapt_path, isApp=False, isResetKeyboard=False)
        url, port = getHost()
        appium_cmd = appium_server_cmd(udid, port)
        subprocess_cmd(appium_cmd)
        time.sleep(10)
        driver = webdriver.Remote(url, caps)
        
    @classmethod
    def tearDownClass(cls):
        pass
'''




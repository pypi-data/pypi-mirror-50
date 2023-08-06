# _*_ coding:utf-8 _*_
import subprocess
import random
import time
import os
from AutoTestSuite.factoryPy.createPy import *

#subprocess
def subprocess_cmd(cmd,shell=True):
    return subprocess.Popen(cmd, shell=shell) #start subprocess

def ProductionRandom(n=1111,m=5555):
    return random.randint(int(n),int(m))

def current_time():
    return time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())

def init_create_page(file,name,text):
    path = os.path.abspath("."+"/"+file+"/"+name+".py")
    f = open(path,"w+")
    f.write(text)
    f.close()


def init_page(name="test"):
    init_create_page("page", name, page % ("test"))

def init_appium_case(test="test"):
    init_create_page("case", test, appium_case % ("test"))

def init_web_case(test="test"):
    init_create_page("case", test, web_case % ("test"))


def init_probject():
    listd = ["case","resource","page","reports","reports/log","reports/png","reports/reportHtml","reports/video","resource/driver"]
    path = os.path.abspath(".")
    for i in listd:
        file  = path+"/"+i
        if os.path.exists(file):
            pass
        else:
            os.mkdir(file)
            f = open(file + "/_init__.py", "w+")
            f.close()

    init_appium_case("appiumTest")
    init_web_case("webTest")
    init_page("Test")




# init_probject()
# init_appium_case("appiumTest")
# init_web_case("webTest")
# init_page("Test")
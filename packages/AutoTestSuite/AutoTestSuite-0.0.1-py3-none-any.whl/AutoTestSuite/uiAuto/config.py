# _*_ coding:utf-8 _*_

import os
from AutoTestSuite.interface import ProductionRandom

def getHost(n=1111,m=5555):
    random_port = ProductionRandom(n,m)
    return 'http://127.0.0.1:%s/wd/hub'%(random_port),random_port


def check_devices(adb,udid):
    error = 'This is not found devices：%s ,Check if the Android phone is connected properly！！！'%(udid)
    if os.name == "posix":
        result = os.system("%s devices|grep %s" % (adb, str(udid)))
    elif os.name == "nt":
        result = os.system("%s devices|findStr %s " % (adb, str(udid)))
    if result != 0:
        raise RuntimeError(error)



def appium_server_cmd(udid,random_port,n=11111,m=55555):
    random_bp = ProductionRandom(n,m)
    return   "appium -a 127.0.0.1 -U %s -p %s -bp %s --command-timeout 100000 --session-override"%(udid,random_port,random_bp)


def close_appium_server(random_port):
   if os.name == "posix":
        pid = os.popen("lsof -i:%s|grep node|awk '{print $2}'" % str(random_port)).read()
        return os.system("kill " + pid)
   elif os.name == "nt":
       netPort = os.popen("netstat -ano|findStr 1125").read()[-8:].strip()
       return os.system("taskkill /pid %s -t -f"%netPort)


def android_caps(udid, app_path, adb_path="adb", aapt_path="aapt", isApp=False, isResetKeyboard=False):
    # check adb 、aapt

    if os.name == "posix":
        aapt_dump = "%s dump badging %s |grep %s|awk '{print $2}'"
        appPackage = str(os.popen(aapt_dump % (aapt_path, app_path, "package")).read()).strip()[6:-1]
        # print(aapt_dump % (aapt_path,app_path, "launchable-activity"))
        try:
            appActivity = str(
                os.popen(aapt_dump % (aapt_path, app_path, "launchable-activity")).read()).split()[0].strip()[6:-1]
        except Exception as e:
            appActivity = appPackage + ".main.MainActivity"

    elif os.name == "nt":
        appPackage = os.popen(
            'aapt dump badging  %s |findStr "package:" ' % (app_path)).read().split(
            " ")[1].strip()[6:-1]
        try:
            appActivity = os.popen(
                'aapt dump badging %s |findStr "launchable-activity"' % (app_path)).read().split(
                " ")[0].strip()[6:-1]
        except Exception as e:
            appActivity = appPackage + ".main.MainActivity"

        # udids = str(os.popen("%s devices|grep -v devices|awk '{print $1}'" % (self.adb_path)).read()).split("\n")
        # udids = list(filter(None, udids))
    android_version = os.popen("%s -s %s shell getprop ro.build.version.release" % (adb_path, udid)).read().strip()
    android_name = os.popen("%s -s %s shell getprop ro.product.name" % (adb_path, udid)).read().strip()
    print("jkflasdjfkl")

    print(android_name)
    caps = {"platformName": "android",
            "platformVersion": android_version,
            "app": app_path,
            "udid": udid,
            # "newCommandTimeout":100000,
            "deviceName": android_name,
            "appPackage": appPackage,
            "appActivity": appActivity}
    if isResetKeyboard == True:
        caps.update({'unicodeKeyboard': True,
                     'resetKeyboard': True})
    if isApp == True:
        caps.update({"noReset": True})
    return caps



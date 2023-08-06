# coding=utf-8
from easyuiautomator.driver.driver import Driver
from easyuiautomator.common.exceptions import DeviceNotFound
import time,os,sys
import unittest

app = Driver.connect_device()
app.find_element_by_id("fff",ignoreExp=True,timeOut=5)

def _clear_adb_process(serial):
    '''clear adb process'''
    if "win" in sys.platform:
        cmd = 'wmic process where "commandline like \'%adb -s {0} shell am instrument -w com.testguard.uiautomator2%\'" call terminate'.format(serial)
        print cmd
        os.system(cmd)
    else:
        os.system('pkill -9 -f ".*adb -s %s .*"'%serial)

_clear_adb_process(app.serial)
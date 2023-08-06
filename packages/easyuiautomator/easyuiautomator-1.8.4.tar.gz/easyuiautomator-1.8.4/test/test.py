# coding=utf-8
from easyuiautomator.driver.driver import Driver
import time,os,sys
import unittest

# d = Driver.connect_device(restart=False)

for i in range(100):
    d = Driver.connect_device(restart=False)
    d.find_element_by_xpath("/*", ignoreExp=True)
    time.sleep(5)
    d.quit()

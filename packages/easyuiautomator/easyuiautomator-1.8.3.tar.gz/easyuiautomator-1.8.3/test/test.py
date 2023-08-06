# coding=utf-8
from easyuiautomator.driver.driver import Driver
from easyuiautomator.common.exceptions import DeviceNotFound
import time,os,sys
import unittest

import requests

r = requests.post('http://127.0.0.1:4724')
print r.status_code

# coding=utf-8
"""
Created on 2015年11月4日

@author: thomas.ning
"""

import itertools,os,socket,sys
import utils,time,json,requests
from requests.exceptions import ReadTimeout
from easyuiautomator.driver.common.errorCode import ErrorCode
from easyuiautomator.common.log import Logger
from easyuiautomator.driver.common.mobilecommand import MobileCommand
import base64
import threading
import subprocess

UIAUTOMATOR_ROOT_PATH = "/data/local/tmp/"
CONFIG_FILE = os.path.join(UIAUTOMATOR_ROOT_PATH, "yepbootstrap.json")
UIAUTOMATOR_PORT = 4724
LOCAL_PORT = 4724
sdk_target_version=21 # statup u1 or u2 condition
u2_version_code = 5
u2_package_name = "com.testguard.uiautomator2"


_init_local_port = LOCAL_PORT - 1

# get auto assign port
def next_local_port(adbHost=None):
    def is_port_listening(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((str(adbHost) if adbHost else '127.0.0.1', port))
        s.close()
        return result == 0
    global _init_local_port
    _init_local_port = _init_local_port + 1 if _init_local_port < 32764 else LOCAL_PORT
    while is_port_listening(_init_local_port):
        _init_local_port += 1
    return _init_local_port


class Uiautomator(object):
    """
    Uiautomator Used to start stop service And complete command interaction
    """
    __U1 = ["YepTelecomBootstrap.jar","resource/u1/YepTelecomBootstrap.jar"]
    __U2 = ["resource/u2/testguard-uiautomator.apk", "resource/u2/testguard-uiautomator-test.apk"]

    def __init__(self, adb, sdk_version, local_port=None):
        self.logger = Logger.getLogger()
        self._adb = adb
        self.__sdk = sdk_target_version
        self.sdk_version = sdk_version
        self._uiauprocess = None
        self.version_code = 0
        self.resource_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.logger.debug('start init uiautomator on %s'%self._adb.serial)
        self.local_port = local_port if local_port else self._getConnectedPort()
        self.logger.debug("clear server config file on %s"%self._adb.serial)
#         self._adb.delFile(CONFIG_FILE)
        self.timeout = 15 # http访问超时值
        self.restart_num = 3 # 本地服务重启次数
        self.link_timeout = 10
        self.http_post = HttpPost(self.rpc_uri, self.timeout)
       
    @property
    def rpc_uri(self):
        return "http://%s:%d/" % (self._adb.server_host, self.local_port)
    
    def push(self):
        filename = os.path.join(self.resource_path, self.__U1[1])
        self._adb.push(filename, UIAUTOMATOR_ROOT_PATH)
    
    def install(self):
        for apk in self.__U2:
            self._adb.installrt(os.path.join(self.resource_path, apk))
            
    def removePkg(self):
        self._adb.uninstallApk(u2_package_name)
        self._adb.uninstallApk(u2_package_name +".test")
    
    def start(self, timeout=15, restart=False):
        self.start_new(timeout, restart)
    
    def start_new(self, timeout=30, restart=False):
        '''新的启动方式，加入预先ping的方案'''
#         if self.sdk_version < self.__sdk:
#             cmd = " ".join(list(itertools.chain(
#                     ["shell", "uiautomator", "runtest"],
#                     [self.__U1[0]],
#                     ["-c", "io.appium.android.bootstrap.Bootstrap"],
#                     ["--nohup"]
#                 ))) 
#         else:
#             cmd = " ".join(
#                         ["shell", "am", "instrument", "-w",
#                        "com.testguard.uiautomator2.test/android.support.test.runner.AndroidJUnitRunner"])
        cmd = " ".join(
                 ["shell", "am", "instrument", "-w",
                "com.testguard.uiautomator2.test/android.support.test.runner.AndroidJUnitRunner"])
#         if not restart:
# #             if self.sdk_version < self.__sdk:
# #                 self.push()
# #             else:
        self.logger.warning("adb_link_timeout value: "+str(self.link_timeout))
        if self.checkVersion() or self.link_timeout < 0:
            if self.link_timeout < 0:
                self.logger.warning('adb_link_timeout, remove driver, need wait 60s')
                time.sleep(120)
            self.removePkg()
            self.install() 
        self._adb.forward(self.local_port, UIAUTOMATOR_PORT)
        if self.pre_ping(3):
            return 
        self.stop()
        self._adb.forward(self.local_port, UIAUTOMATOR_PORT)
        if restart:
            self.logger.debug('Restart Uiautomator Server on %s'%self._adb.serial)
        else:
            self.logger.debug('Startup Uiautomator Server on %s'%self._adb.serial)
        self._uiauprocess = self._adb.cmd(cmd)
        time.sleep(3)
        self.waitServer(timeout)
        
    def checkVersion(self):
        '''检查uiautomator apk版本  if true remove'''
        if self.version_code == 0:
            self.version_code = self._adb.getVersionCode(u2_package_name)
        return True if u2_version_code > self.version_code else False

    def waitServer(self, timeout):
        # connect u2 server
        while not self.alive and timeout > 0:
            time.sleep(0.5)
            timeout -= 0.5
        if not self.alive:
            if self.restart_num == 0:
                self.restart_num = 3
                raise IOError(utils.formatExceptionStr(self._adb.serial, "本地服务无法启动"))
            else:
                self.restart_num -= 1
                self.logger.debug("restart device server on %s,total=3,restarting=%s"%(self._adb.serial,3-self.restart_num))
                self.start(restart=True) 
        else:
            self.restart_num = 3

    @property
    def alive(self):
        '''Check if the rpc server is alive.'''
        try:
            data = self.ping()
            if data is not None:
                return data['status']==0
            return False
        except:
            return False
        
    def pre_ping(self, timeout):
        '''预ping,如果已民连接，则正常执行'''
        while True: 
            if self.alive is True:
                return True
            if timeout > 0:
                time.sleep(1)
                timeout -= 1
            else: 
                return False
        
    def ping(self):
        try:
            extra = {"action": MobileCommand.PING, "params": {}}
            data = self.http_post.post_ping(extra, 5) 
            if data:
                self.link_timeout = 10
                return data
        except:
            self.link_timeout = self.link_timeout -1 
            self.logger.warning('ping except failure, uiautomator daemon hang')
        
    def sendActon(self, action, params):
        extra = {"action": action, "params": params}
        try:
            msg = self.http_post.post(extra)  
            if msg['status'] != 0:
                value = msg['value']
                if isinstance(value, str) or isinstance(value, unicode):
                    if "UiAutomation not connected" in value:
                        self.stopUiauto()
                        if params and params.get("elementId"):
                            return msg
                        return self._restartServer(extra)
            return msg
        except ReadTimeout:
            raise
        except:
            if params and params.get("elementId"):
                raise
            return self._restartServer(extra)
              
    def _restartServer(self, data=None):
        self.start(restart=True)
        if data:
            return self.http_post.post(data)

    def _getConnectedPort(self):
        '''auto assign port'''
        local_port = UIAUTOMATOR_PORT
        try:  # first we will try to use the local port already adb forwarded
            for s, lp, rp in self._adb.forwardlist():
                if s == self._adb.serial and rp == 'tcp:%d' % UIAUTOMATOR_PORT:
                    local_port = int(lp[4:])
                    break
            else:
                local_port = next_local_port()
        except:
            local_port = next_local_port()
        return local_port

    
    def stopUiauto(self):
        if self._uiauprocess and self._uiauprocess.poll() is None:
            if self._uiauprocess:
                self._uiauprocess.terminate()
            self._uiauprocess = None
        self._adb.killProcessesByName("uiautomator")
        self._adb.forceStop(u2_package_name)

    def stop(self):
        self.stop_uri()
        self.stopUiauto()
            
    def stop_uri(self):
        stop_url = "http://%s:%d/stop" % (self._adb.server_host, self.local_port)
        try:
            requests.post(stop_url,timeout=5)
        except:
            pass

def systemCmd(cmd_line):
    '''exec system cmd, paramas list'''
    if os.name != "nt":
        cmd_line = [" ".join(cmd_line)]
    return subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
           
class HttpPost:
    
    headers={"Content-Type": "application/json"}
    
    def __init__(self, url, timeout):
        self.logger = Logger.getLogger()
        requests.adapters.DEFAULT_RETRIES = 3
        self.url = url
        self.timeout = timeout
        
    def post_ping(self,data,timeout):
        # add mintor timeout
        t = threading.Timer(10, self.stopUiautomator, (self.url,True))
        t.setDaemon(True)
        t.start()
        try:
            return self._post(data, timeout)
        except:
            raise
        finally:
            try:
                t.cancel()
            except:
                pass
        
        
    def post(self,data,timeout=None):
        # add mintor timeout
        t = threading.Timer(90, self.stopUiautomator, (self.url,))
        t.setDaemon(True)
        t.start()
        try:
            return self._post(data, timeout)
        except:
            raise
        finally:
            try:
                t.cancel()
            except:
                pass
        
    def stopUiautomator(self, url, force_stop=False):
        port = url.split(":")[2].split("/")[0]
        serial = None
        try:
            lines = systemCmd(['adb','forward','--list']).communicate()[0].decode("utf-8").strip().splitlines()
            for s, lp, rp in [line.strip().split() for line in lines]:
                if lp == 'tcp:%s'%port and rp=='tcp:4724':
                    serial = s
                    os.system('adb -s %s forward --remove tcp:%s'%(serial, port))
                    break
        except:
            pass
        if serial:
            self._clear_adb_process(serial)
            os.system("adb -s %s shell am force-stop com.testguard.uiautomator2"%serial)
    
    def _clear_adb_process(self, serial):
        '''clear adb process'''
        if "win" in sys.platform:
            cmd = 'wmic process where "commandline like \'%adb  -s {0} shell am instrument -w com.testguard.uiautomator2%\'" call terminate'.format(serial)
            os.system(cmd)
        else:
            os.system('pkill -9 -f ".*adb -s %s shell am instrument -w com.testguard.uiautomator2.*"'%serial)

    def _post(self, data, timeout=None):
        self.logger.debug(data)
        if data['action'] != 'takeScreenshot':
            if data['action'] in [MobileCommand.LONG_CLICK,MobileCommand.SCROLL_TO,"element:scrollOrientation"]:
                r = requests.post(self.url, data=json.dumps(data), headers=self.headers)
                return json.loads(r.content)
            else:
                r = requests.post(self.url, data=json.dumps(data), headers=self.headers, timeout=self.timeout if timeout is None else timeout)
                return json.loads(r.content)
        else:
            r = requests.post(self.url, data=json.dumps(data), headers=self.headers, timeout=30, stream=True)
            img = ''
            for chunk in r.iter_content(chunk_size=1024):  
                if chunk: # filter out keep-alive new chunks  
                    img += chunk
            if len(img) > 50:
                return {'status': 0,'value': base64.b64encode(img)}
            else:
                return {'status': 1,'value': 'screenshot failure'}
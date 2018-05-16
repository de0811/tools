#!/usr/bin/python3
# coding=utf8
#-*-coding:utf-8-*-

import sys
import threading
import time
from lib.option import *
from lib.androidinfo import *

class CompatibilityManager() :
    u"""
    class CompatibilityManager
    호환성 테스트를 중심에서 컨트롤하는 컨트롤러
    """
    deviceList = list()
    displayHistorys = dict()    #map[ID][displayHistory]
    deviceInfos = dict()        #map[ID][deviceInfo]
    testCount = 0
    workDir = ""
    def __init__(self) :
        self.deviceList = list()
        self.displayHistory = dict()
        self.deviceInfos = dict()
        self.testCount = 0
        self.workDir = "/home/num/temp/comp"

    def set_test_count(self, args) :
        u"""option : -c"""
        if len(args) != 1 : 
            print ("Args Error")
            print ("Args : Test count 1")
            sys.exit()
        val = args[0]
        try :
            self.testCount = int(val)
        except ValueError :
            print ("Args Error")
            print ("Args : Test Count is Number !! ")
            sys.exit()
    
    def set_work_directory(self, args) :
        u"""option : -d"""
        if len(args) != 1 :
            print ("Args Error")
            print ("Args : WorkDirectory Error")
            sys.exit()
        self.workDir = args[0]

    def help(self, args) :
        u""" option : -h """
        hel = u'''autoApkDevicesCompatibility.py [command] [target]
        기기 별 호환성 테스트를 진행합니다.
        [command]
        -h : 설명을 나타냅니다
        -c : 횟수를 설정합니다.
        -d : 결과 값을 저장한 디렉토리를 지정합니다.
        '''
        print (hel)
        sys.exit()
    
    #연결된 Devices를 찾음
    def __join_devices(self) :
        u"""연결된 Device 이름들을 모두 찾기"""
        RunProcess("adb devices")
        time.sleep(0.5)

        devices = RunProcessOut("adb devices")
        #[b'List of devices attached\n', b'\n']

        if  devices[0].decode("UTF-8").find("List of devices attached") == -1 :
            print ("Error adb service")
            sys.exit()
        if len(devices) < 2 :
            print ("Not is Device")
            sys.exit()
        if devices[1].strip() == "" :
            print ("Not is Device")
            sys.exit()

        devices = devices[1:]
        for bDevice in devices :
            bDevice = bDevice.decode("UTF-8").strip()
            if bDevice == "" :
                break
            bDevice = bDevice.split()
            self.deviceList.append(bDevice[0])
    
    def __extract_deviceInfos(self) :
        u"""Device들의 정보 추출"""
        for device in self.deviceList :
            self.deviceInfos.setdefault(device, DeviceInfo(device))
        
        self.__prints_deviceInfos()

    def run(self, args) :
        u"""전체 실행 부분"""
        self.__join_devices()
        self.__extract_deviceInfos()

        for device in self.deviceInfos :
            #어찌 할까
            #t = threading.Thread( target=playEvent, args=(device, apkFile, loadEvent) )
            #t.start()
            pass

    def __prints_deviceInfos(self) :
        for key in self.deviceInfos.keys() :
            self.deviceInfos[key].prints()
 

if __name__ == "__main__":

    #argvs = ["-h",]
    argvs = list()
    opt = option()
    compatibilityManager = CompatibilityManager()
    #def addOpt(self, opt, argCount, bVarArg, func):
    opt.addOpt(opt="-h", argCount=0, bVarArg=True, bHelp=True, func=compatibilityManager.help)
    opt.addOpt(opt="-c", argCount=1, bVarArg=True, bHelp=False, func=compatibilityManager.set_test_count)
    opt.addOpt(opt="-d", argCount=1, bVarArg=True, bHelp=False, func=compatibilityManager.set_work_directory)
    opt.addOpt(opt="default", argCount=0, bVarArg=True, bHelp=False, func=compatibilityManager.run)
    opt.parsing(argvs)
    opt.run()
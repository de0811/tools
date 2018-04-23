#!/usr/bin/python3
#-*-coding:utf-8-*-

#실행 , 종료 시키는 걸로 시간도 잴까? 시간도 재자
import sys
import threading
from lib.androidinfo import *
from lib import option
import maapt

class DeviceFinder :
    os_ver_list = list()
    sdk_ver_list = list()
    device_list = list()
    manufacturer_list = list()
    model_list = list()
    find_list = list()
    device_dict = dict()

    def __init__(self) :
        self.os_ver_list = list()       #OS 버전
        self.sdk_ver_list = list()      #sdk 버전
        self.device_list = list()       #device
        self.manufacturer_list = list() #제조사 리스트
        self.model = list()             #모델 이름
        self.find_list = list()      #설치할 기기
        self.device_dict = dict()       #기기별 상세 정보
    
    def help(self, args) :
        hel = u"""
        python apkInstaller.py [option] <.apk>
        [option]
        options grep name
        -d / -device : devices select
        -o / -os : os version select
        -s / -sdk : sdk version select
        -m / -manufacturer : manufacturer select 
        -mo / -model : model select
        -v / -view [view option] : devices Infomation
            [view option]
            all : all devices info
            device : view device
            os : view os
            sdk : view sdk
            manufacturer : view manufacturer
            model : view model
        """
        print (hel)
    
    def select_os(self, args) :
        if len(args) == 0 :
            print ("opt:error path")
            sys.exit()
        for arg in args :
            self.os_ver_list.append(arg)
    
    def select_sdk(self, args) :
        if len(args) == 0 :
            print ("opt:error path")
            sys.exit()
        for arg in args :
            self.sdk_ver_list.append(arg)

    def select_device(self, args) :
        if len(args) == 0 :
            print ("opt:error path")
            sys.exit()
        for arg in args :
            self.device_list.append(arg)
    
    def select_manufacturer(self, args) :
        if len(args) == 0 :
            print ("opt:error path")
            sys.exit()
        for arg in args :
            self.manufacturer_list.append(arg)
    
    def select_model(self, args) :
        if len(args) == 0 :
            print("opt:error path")
            sys.exit()
        for arg in args :
            self.model_list.append(arg)
    
    def find_device_list(self) :
        all_device_list = DeviceList()

        for device in all_device_list.devices :
            self.device_dict.setdefault(device, DeviceInfo(device))

        #모든 기기 목록 추출
        if len(self.sdk_ver_list) == 0 and \
            len(self.os_ver_list) == 0 and \
            len(self.device_list) == 0 and \
            len(self.manufacturer_list) == 0 :
            self.find_list = all_device_list.devices
        else :
            search_list = all_device_list.devices

            if len(self.sdk_ver_list) != 0 and len(search_list) != 0:
                for device in search_list :
                    device_info = self.device_dict.get(device)
                    for sdk in self.sdk_ver_list :
                        if device_info.ver_sdk.lower().find(sdk.lower()) != -1 :
                            self.find_list.append(device)
                            break
                search_list = self.find_list
                self.find_list = list()
            
            if len(self.os_ver_list) != 0 and len(search_list) != 0:
                for device in search_list :
                    device_info = self.device_dict.get(device)
                    for os in self.os_ver_list :
                        if device_info.ver_os.lower().find(os.lower()) != -1 :
                            print (device)
                            self.find_list.append(device)
                            break
                search_list = self.find_list
                self.find_list = list()
            
            if len(self.device_list) != 0 and len(search_list) != 0 :
                for device in search_list :
                    device_info = self.device_dict.get(device)
                    for target_device in self.device_list :
                        if device_info.device.lower().find(target_device.lower()) != -1 :
                            self.find_list.append(device)
                            break
                search_list = self.find_list
                self.find_list = list()
            
            if len(self.manufacturer_list) != 0 and len(search_list) != 0 :
                for device in search_list :
                    device_info = self.device_dict.get(device)
                    for manu in self.manufacturer_list :
                        if device_info.manufacturer.lower().find(manu.lower()) != -1 :
                            self.find_list.append(device)
                            break
                search_list = self.find_list
                self.find_list = list()
            
            if len(self.model_list) != 0 and len(search_list) != 0 :
                for device in search_list :
                    device_info = self.device_dict.get(device)
                    for model in self.model_list :
                        if device_info.model.lower().find(model.lower()) != -1 :
                            self.find_list.append(device)
                            print (device)
                            break
                search_list = self.find_list
                self.find_list = list()
            
            self.find_list = search_list

    """
            all : all devices info
            device : view device
            os : view os
            sdk : view sdk
            manufacturer : view manufacturer
            model : view model
    """
    def view(self, args) :
        self.find_device_list()
        if len(args) == 0 :
            for device in self.find_list :
                self.device_dict.get(device).prints()
        else :
            device_set = set()
            os_set = set()
            sdk_set = set()
            manufacturer_set = set()
            model_set = set()
            for device in self.find_list :
                device_info = self.device_dict.get(device)
                device_set.add(device_info.device)
                os_set.add(device_info.ver_os)
                sdk_set.add(device_info.ver_sdk)
                manufacturer_set.add(device_info.manufacturer)
                model_set.add(device_info.model)
            for arg in args :
                if "all".find(arg) != -1 :
                    for device in self.find_list :
                        self.device_dict.get(device).prints()
                if "devices".find(arg) != -1 :
                    print ("*" * 10 + "Device List" + "*" * 10)
                    for device in device_set :
                        print (device)
                    print ("*" * 30)
                if "os".find(arg) != -1 :
                    print ("*" * 10 + "  OS List  " + "*" * 10)
                    for os in os_set :
                        print (os)
                    print ("*" * 31)
                if "sdk".find(arg) != -1 :
                    print("*" * 10 + "   SDK List   " + "*" * 10)
                    for sdk in sdk_set :
                        print (sdk)
                    print ("*" * 34)
                if "manufacturer".find(arg) != -1 :
                    print ("*" * 10 + "Manufacturer List" + "*" * 10)
                    for manu in manufacturer_set :
                        print (manu)
                    print ("*" * 34)
                if "model".find(arg) != -1 :
                    print ("*" * 10 + "   Model List   " + "*" * 10)
                    for model in model_set :
                        print (model)
                    print ("*" * 35)

    
#adb shell input keyevent KEYCODE_POWER
    def device_find(self) :
        pass
        
    def run(self, args) :
        self.device_find()
        

if __name__ == "__main__":
    device_finder = DeviceFinder()
    opt = option.option()
    #def addOpt(self, opt, argCount, bVarArg, func):
    opt.addOpt(opt="-h", argCount=0, bVarArg=False, bHelp=True, func=device_finder.help)
    opt.addOpt(opt="-d", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_device)
    opt.addOpt(opt="-o", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_os)
    opt.addOpt(opt="-os", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_os)
    opt.addOpt(opt="-s", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_sdk)
    opt.addOpt(opt="-sdk", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_sdk)
    opt.addOpt(opt="-m", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_manufacturer)
    opt.addOpt(opt="-manufacturer", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_manufacturer)
    opt.addOpt(opt="-mo", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_model)
    opt.addOpt(opt="-model", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_model)
    opt.addOpt(opt="-v", argCount=1, bVarArg=False, bHelp=True, func=device_finder.view)
    opt.addOpt(opt="-view", argCount=1, bVarArg=False, bHelp=True, func=device_finder.view)
    opt.addOpt(opt="default", argCount=0, bVarArg=True, bHelp=False, func=device_finder.run)
    test = ['-os', '6.0', '/home/num/temp/scheduler.apk']
    #test = ['-v',]
    test = ['-v', 'model' ]
    test = ['-os', '6.0', '-mo', 'nexus', '/home/num/temp/scheduler.apk']
    test = ['/home/num/temp/error_apk.apk']
    test = ['/home/num/temp/scheduler.apk']
    opt.parsing(test)
    #opt.tprint()
    opt.run()
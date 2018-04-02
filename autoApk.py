#!/usr/bin/python3
#-*-coding:utf-8-*-

#실행 , 종료 시키는 걸로 시간도 잴까? 시간도 재자
import sys
import threading
from lib.androidinfo import *
from lib import option
import maapt

class ApkInstaller :
    os_ver_list = list()
    sdk_ver_list = list()
    device_list = list()
    manufacturer_list = list()
    model_list = list()
    install_list = list()
    install_dict = dict()

    def ApkInstaller(self) :
        self.os_ver_list = list()       #OS 버전
        self.sdk_ver_list = list()      #sdk 버전
        self.device_list = list()       #device
        self.manufacturer_list = list() #제조사 리스트
        self.model = list()             #모델 이름
        self.install_list = list()      #설치할 기기
        self.install_dict = dict()       #기기별 상세 정보
    
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
    
    def install_device_list(self) :
        all_device_list = DeviceList()
        device_dict = dict()

        for device in all_device_list.devices :
            device_dict.setdefault(device, DeviceInfo(device))
        
        self.install_dict = device_dict

        #모든 기기 목록 추출
        if len(self.sdk_ver_list) == 0 and \
            len(self.os_ver_list) == 0 and \
            len(self.device_list) == 0 and \
            len(self.manufacturer_list) == 0 :
            self.install_list = all_device_list.devices
            self.install_dict = device_dict
        else :
            search_list = all_device_list.devices

            if len(self.sdk_ver_list) != 0 and len(search_list) != 0:
                for device in search_list :
                    device_info = device_dict.get(device)
                    for sdk in self.sdk_ver_list :
                        if device_info.ver_sdk.find(sdk) != -1 :
                            self.install_list.append(device)
                            break
                search_list = self.install_list
                self.install_list = list()
            
            if len(self.os_ver_list) != 0 and len(search_list) != 0:
                for device in search_list :
                    device_info = device_dict.get(device)
                    for os in self.os_ver_list :
                        if device_info.ver_os.find(os) != -1 :
                            print (device)
                            self.install_list.append(device)
                            break
                search_list = self.install_list
                self.install_list = list()
            
            if len(self.device_list) != 0 and len(search_list) != 0 :
                for device in search_list :
                    device_info = device_dict.get(device)
                    for target_device in self.device_list :
                        if device_info.device.find(target_device) != -1 :
                            self.install_list.append(device)
                            break
                search_list = self.install_list
                self.install_list = list()
            
            if len(self.manufacturer_list) != 0 and len(search_list) != 0 :
                for device in search_list :
                    device_info = device_dict.get(device)
                    for manu in self.manufacturer_list :
                        if device_info.manufacturer.find(manu) != -1 :
                            self.install_list.append(device)
                            break
                search_list = self.install_list
                self.install_list = list()
            
            if len(self.model_list) != 0 and len(search_list) != 0 :
                for device in search_list :
                    device_info = device_dict.get(device)
                    for model in self.model_list :
                        if device_info.model.find(model) != -1 :
                            self.install_list.append(device)
                            print (device)
                            break
                search_list = self.install_list
                self.install_list = list()
            
            self.install_list = search_list


    """
            all : all devices info
            device : view device
            os : view os
            sdk : view sdk
            manufacturer : view manufacturer
            model : view model
    """
    def view(self, args) :
        self.install_device_list()
        if len(args) == 0 :
            for device in self.install_list :
                self.install_dict.get(device).prints()
        else :
            device_set = set()
            os_set = set()
            sdk_set = set()
            manufacturer_set = set()
            model_set = set()
            for device in self.install_list :
                device_info = self.install_dict.get(device)
                device_set.add(device_info.device)
                os_set.add(device_info.ver_os)
                sdk_set.add(device_info.ver_sdk)
                manufacturer_set.add(device_info.manufacturer)
                model_set.add(device_info.model)
            for arg in args :
                if "all".find(arg) != -1 :
                    for deivce in self.install_list :
                        self.install_dict.get(device).prints()
                if "devices".find(arg) != -1 :
                    print ("*" * 10 + "Device List" + "*" * 10)
                    for device in device_set :
                        print (device)
                    print ("*" * 26)
                if "os".find(arg) != -1 :
                    print ("*" * 10 + "  OS List  " + "*" * 10)
                    for os in os_set :
                        print (os)
                    print ("*" * 26)
                if "sdk".find(arg) != -1 :
                    print("*" * 10 + "   SDK List   " + "*" * 10)
                    for sdk in sdk_set :
                        print (sdk)
                    print ("*" * 26)
                if "manufacturer".find(arg) != -1 :
                    print ("*" * 10 + "Manufacturer List" + "*" * 10)
                    for manu in manufacturer_set :
                        print (manu)
                    print ("*" * 26)
                if "model".find(arg) != -1 :
                    print ("*" * 10 + "   Model List   " + "*" * 10)
                    for model in model_set :
                        print (model)
                    print ("*" * 26)
    
    def __os_6_under(self, apk, device) :
        RunProcessWait("adb -s " + device + " install " + apk)
    def __os_6_upper(self, apk, device) :
        RunProcessWait("adb -s " + device + " install -r -g " + apk)
    
    def __normal_device_install(self, apk, device) :
        if int( self.install_dict.get(device).ver_sdk ) < 23 :
            self.__os_6_under(apk, device)
        else :
            self.__os_6_upper(apk, device)

    def __mi_device_install(self, apk, device) :
        #Thread install & focused 
        install_thread = None
        if int( self.install_dict.get(device).ver_sdk ) < 23 :
            install_thread = threading.Thread( target=self.__os_6_under, args=(apk, device) )
            install_thread.start()
        else :
            install_thread = threading.Thread( target=self.__os_6_upper, args=(apk, device) )
            install_thread.start()
        #mFocused
        while True :
            time.sleep(1)
            dumpsys_window = DumpsysWindow(device)
            print (dumpsys_window.mFocused)
            if dumpsys_window.mFocused.find("""com.android.packageinstaller/com.android.packageinstaller.PackageInstallerActivity""") != -1 :
                break
        #Button Click
        device_ui_info = DeviceUIInfo()
        device_ui_info.window_point_parsing(device, dumpsys_window.app_size_x, dumpsys_window.app_size_y)
        resource_info = device_ui_info.search_clickable_resource_id("com.android.packageinstaller:id/ok_button")
        RunProcessWait("adb -s " + device + " shell input tap " + str(resource_info.x1 + ((resource_info.x2 - resource_info.x1) / 2)) + " " + str(resource_info.y1 + ((resource_info.y2 - resource_info.y1)/2)))
        print ("Here !!")

        #install_thread.join()    #thread waiting
                    
    def apk_install(self, apk) :
        aapt = maapt.aapt()
        aapt.aapt_parsing(apk)
        apk_name = aapt.package_name
        apk_activity = aapt.package_activity
        print ("APK : " + apk + "  Name : " + apk_name + "  Activity : " + apk_activity)
        self.install_device_list()
        if len(self.install_list) == 0 :
            print ("None Target devices")
        elif len(self.install_list) == 1 :
            for device in self.install_list :
                RunProcessWait("adb -s " + device + " uninstall " + apk_name)
                if self.install_dict.get(device).manufacturer == "Xiaomi" :
                    self.__mi_device_install(apk, device)
                else :
                    self.__normal_device_install(apk, device)
        else :
            for device in self.install_list :
                RunProcessWait("adb -s " + device + " uninstall " + apk_name)
                if self.install_dict.get(device).manufacturer == "Xiaomi" :
                    t = threading.Thread( target=self.__mi_device_install, args=(apk, device) )
                    t.start()
                else :
                    t = threading.Thread( target=self.__normal_device_install, args=(apk, device) )
                    t.start()
        
    def run(self, args) :
        if len(args) != 1 :
            return
        apk = args[0]
        self.apk_install(apk)
        

if __name__ == "__main__":
    apk_installer = ApkInstaller()
    opt = option.option()
    #def addOpt(self, opt, argCount, bVarArg, func):
    opt.addOpt(opt="-h", argCount=0, bVarArg=False, bHelp=True, func=apk_installer.help)
    opt.addOpt(opt="-d", argCount=20, bVarArg=False, bHelp=False, func=apk_installer.select_device)
    opt.addOpt(opt="-o", argCount=20, bVarArg=False, bHelp=False, func=apk_installer.select_os)
    opt.addOpt(opt="-os", argCount=20, bVarArg=False, bHelp=False, func=apk_installer.select_os)
    opt.addOpt(opt="-s", argCount=20, bVarArg=False, bHelp=False, func=apk_installer.select_sdk)
    opt.addOpt(opt="-sdk", argCount=20, bVarArg=False, bHelp=False, func=apk_installer.select_sdk)
    opt.addOpt(opt="-m", argCount=20, bVarArg=False, bHelp=False, func=apk_installer.select_manufacturer)
    opt.addOpt(opt="-manufacturer", argCount=20, bVarArg=False, bHelp=False, func=apk_installer.select_manufacturer)
    opt.addOpt(opt="-mo", argCount=20, bVarArg=False, bHelp=False, func=apk_installer.select_model)
    opt.addOpt(opt="-model", argCount=20, bVarArg=False, bHelp=False, func=apk_installer.select_model)
    opt.addOpt(opt="-v", argCount=1, bVarArg=False, bHelp=True, func=apk_installer.view)
    opt.addOpt(opt="-view", argCount=1, bVarArg=False, bHelp=True, func=apk_installer.view)
    opt.addOpt(opt="default", argCount=1, bVarArg=True, bHelp=False, func=apk_installer.run)
    test = ['-os', '6.0', '/home/num/temp/scheduler.apk']
    test = ['/home/num/temp/scheduler.apk']
    #test = ['-v',]
    test = ['-v', 'model' ]
    test = ['-os', '6.0', '-mo', 'Nexus', '/home/num/temp/scheduler.apk']
    opt.parsing(test)
    #opt.tprint()
    opt.run()

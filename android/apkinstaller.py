#!/usr/bin/python3
#-*-coding:utf-8-*-

#실행 , 종료 시키는 걸로 시간도 잴까? 시간도 재자
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import threading
import time
from lib import runprocess
#from lib.androidinfo import *
from lib import androidinfo
from lib import option
from lib import logs
import maapt
import devicefinder
from concurrent.futures import ProcessPoolExecutor

class ApkInstaller :
    device_install_state_dict = dict()
    device_finder = devicefinder.DeviceFinder()
    device_logs = logs.DeviceLogs()

    def __init__(self) :
        self.device_install_state_dict = dict() #기기별 설치 현황
        self.device_finder = devicefinder.DeviceFinder()
        self.device_logs = logs.DeviceLogs()

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
   
    def __os_6_under(self, apk, device) :
        tmp_out_line = list()
        out_line = runprocess.RunProcessOut("adb -s " + device + " install " + apk)
        for line in out_line :
            line = line.decode("UTF-8").strip()
            tmp_out_line.append(line)
            if line == "Success" :
                self.device_logs.append(device, "install_log", line, 0)
            else :
                self.device_logs.append(device, "ERROR_install", line, 0)
        self.device_install_state_dict.setdefault(device, tmp_out_line)

    def __os_6_upper(self, apk, device) :
        tmp_out_line = list()
        out_line = runprocess.RunProcessOut("adb -s " + device + " install -r -g " + apk)
        for line in out_line :
            line = line.decode("UTF-8").strip()
            tmp_out_line.append(line)
            if line == "Success" :
                self.device_logs.append(device, "install_log", line, 0)
            else :
                self.device_logs.append(device, "ERROR_install", line, 0)
        self.device_install_state_dict.setdefault(device, tmp_out_line)
    
    def normal_device_install(self, apk, device) :
        if int( self.device_finder.device_dict.get(device).ver_sdk ) < 23 :
            self.__os_6_under(apk, device)
        else :
            self.__os_6_upper(apk, device)

    def mi_device_install(self, apk, device) :
        #Thread install & focused 
        install_thread = None
        if int( self.device_finder.device_dict.get(device).ver_sdk ) < 23 :
            install_thread = threading.Thread( target=self.__os_6_under, args=(apk, device) )
            install_thread.start()
        else :
            install_thread = threading.Thread( target=self.__os_6_upper, args=(apk, device) )
            install_thread.start()
        #mFocused
        while True :
            time.sleep(1)
            dumpsys_window = androidinfo.DumpsysWindow(device)
            print (dumpsys_window.mFocused)
            if dumpsys_window.mFocused.find("""com.android.packageinstaller/com.android.packageinstaller.PackageInstallerActivity""") != -1 :
                break
            state_dict = self.device_install_state_dict.get(device)
            if state_dict != None :
                bCheck = False
                for line in state_dict :
                    if line.lower().find("failed") != -1 :
                        bCheck = True
                        break
                if bCheck == True :
                    return
        #Button Click
        device_ui_info = androidinfo.DeviceUIInfo()
        device_ui_info.window_point_parsing(device, dumpsys_window.app_size_x, dumpsys_window.app_size_y)
        resource_info = device_ui_info.search_clickable_resource_id("com.android.packageinstaller:id/ok_button")
        runprocess.RunProcessWait("adb -s " + device + " shell input tap " + \
            str(resource_info.x1 + ((resource_info.x2 - resource_info.x1) / 2)) + " " + \
            str(resource_info.y1 + ((resource_info.y2 - resource_info.y1)/2)))

        #install_thread.join()    #thread waiting
    
    def apk_install_check(self, device, apk_name) :
        while(True) :
            apk_list = runprocess.RunProcessOut("adb -s " + device + " shell pm list package -f | grep " + apk_name)
            if len(apk_list) <= 0 :
                time.sleep(1)
            else :
                return
    
    def apk_install(self, apk) :
        aapt = maapt.aapt()
        aapt.aapt_parsing(apk)
        if aapt.is_error == True :
            print ("APK Error !!")
            for error_line in aapt.error_list :
                self.device_logs.append("none", "ERROR_APK", error_line, 0)
            return
        apk_name = aapt.package_name
        #임시 작업
        #apk_activity = aapt.package_activity
        #print ("APK : " + apk + "  Name : " + apk_name + "  Activity : " + apk_activity)
        self.device_finder.find_device_list()
        if len(self.device_finder.find_list) == 0 :
            print ("None Target devices")
            self.device_logs.append("none", "ERROR_INSTALL", "DEVICE_NONE", 0)
            return

        else :
            #####################################################
            print ("Process Count :: " + str(len(self.device_finder.find_list)))
            with ProcessPoolExecutor(max_workers=len(self.device_finder.find_list)) as exe:
                for device in self.device_finder.find_list :
                    runprocess.RunProcessWait("adb -s " + device + " shell pm uninstall " + apk_name)

                    if self.device_finder.device_dict.get(device).manufacturer == "Xiaomi" :
                        exe.submit(self.mi_device_install, apk, device)
                    else :
                        exe.submit(self.normal_device_install, apk, device)

                    time.sleep(0.1)
                exe.shutdown(wait=True)
            #####################################################
        

        for device in self.device_finder.find_list :
            self.apk_install_check(device, apk_name)
            self.device_logs.prints(device)
    
    def run(self, args) :
        if len(args) != 1 :
            return
        apk = args[0]
        self.apk_install(apk)
    
    def apk_uninstall(self, apk) :
        aapt = maapt.aapt()
        aapt.aapt_parsing(apk)
        if aapt.is_error == True :
            print ("APK Error !!")
            for error_line in aapt.error_list :
                self.device_logs.append("none", "ERROR_APK", error_line, 0)
            return
        apk_name = aapt.package_name

        for device in self.device_finder.find_list :
            runprocess.RunProcessWait("adb -s " + device + " uninstall " + apk_name)
        

if __name__ == "__main__":
    apk_installer = ApkInstaller()
    device_finder = apk_installer.device_finder
    opt = option.option()
    #def addOpt(self, opt, argCount, bVarArg, func):
    opt.addOpt(opt="-h", argCount=0, bVarArg=False, bHelp=True, func=apk_installer.help)
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
    opt.addOpt(opt="default", argCount=1, bVarArg=True, bHelp=False, func=apk_installer.run)
    test = ['-os', '6.0', '/home/num/temp/scheduler.apk']
    #test = ['-v',]
    test = ['-v', 'model' ]
    test = ['-os', '6.0', '-mo', 'nexus', '/home/num/temp/scheduler.apk']
    test = ['/home/num/temp/error_apk.apk']
    test = ['/home/num/temp/scheduler.apk']
    test = ['-mo', 'nexus', '/home/num/temp/scheduler.apk']
    #opt.parsing(test)
    opt.parsing()
    #opt.tprint()
    opt.run()

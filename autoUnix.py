#!/usr/bin/python3
#-*-coding:utf-8-*-

import config
from lib import option
from lib.runprocess import *
from lib.androidinfo import *

class AutoUnix :
    out_path = ""
    pull_list = list()
    def __init__(self) :
        self.out_path = "c:\\temp\\unix\\"
        self.__setting_pull_list()
    def help(self, args) :
        hel = u"""autoUnix [option]
        [option]
        -o : File을 담을 Path를 설정
        -h : help
        """
        print (hel)
    def __setting_pull_list(self) :
        u"""추출할 파일의 경로를 여기에만 적어주세요"""
        self.pull_list = list()
        self.pull_list.append("/proc/net/unix")
        self.pull_list.append("/system/build.prop")
    def set_folder_path(self, args) :
        if args == 0 :
            print ("opt:error path")
            sys.exit()
        self.out_path = args[0]
    def run(self, args) :
        devicesOut = RunProcessOut("adb devices")
        devices = list()
        others = list()

        device_list = DeviceList()

        for device in device_list.devices :
            print ("RUN DEVICE : " + device)
            """Device 정보 추출"""
            deviceInfo = DeviceInfo(device)
            deviceInfo.extractDeviceInfo()
            deviceInfo.prints()

            """폴더 생성"""
            if os.path.isdir(self.out_path) == False :
                print ("Out DIR Error !!!")
                sys.exit()
            #name = deviceInfo.ver_os + "_" + deviceInfo.ver_sdk + "_" + deviceInfo.manufacturer + "_" + deviceInfo.model
            name = deviceInfo.manufacturer + "_" + deviceInfo.ver_sdk + "_" + deviceInfo.ver_os + "_" + deviceInfo.model
            name = name.replace(" ", "")
            folderName = name
            idx = 0
            print ("outPath : " + self.out_path)
            print ("OUT : " + os.sep)
            if self.out_path[-1] != os.sep :
                self.out_path = self.out_path + os.sep
            while os.path.isdir(self.out_path + os.sep + folderName) :
                folderName = name + "_" + str(idx)
                idx = idx + 1
            
            os.mkdir(path=self.out_path + folderName, mode=0o777)

            adb = "adb "
            if len(device) > 0 :
                adb = "adb -s " + device + " "

            """파일 추출"""
            for __pull in self.pull_list :
                temp_pull_name = __pull.replace("/", "_")
                RunProcessWait(adb + "shell cp " + __pull + " " + "/sdcard/" + temp_pull_name)
                RunProcessWait(adb + "pull " + "/sdcard/" + temp_pull_name + " " + self.out_path + folderName + os.sep + temp_pull_name)
                RunProcessWait(adb + "shell rm -rf /sdcard/" + temp_pull_name)
                #RunProcessWait(adb + "pull " + __pull + " " + self.out_path + folderName + os.sep + temp_pull_name)


        for oo in others :
            print (oo)
            pass


if __name__ == "__main__":
    app = AutoUnix()
    opt = option.option()
    
    #def addOpt(self, opt, argCount, bVarArg, func):
    opt.addOpt(opt="-h", argCount=0, bVarArg=False, bHelp=True, func=app.help)
    opt.addOpt(opt="-o", argCount=1, bVarArg=True, bHelp=False, func=app.set_folder_path)
    opt.addOpt(opt="default", argCount=0, bVarArg=True, bHelp=False, func=app.run)
    opt.parsing()
    #opt.tprint()
    opt.run()
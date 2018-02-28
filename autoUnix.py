#!/usr/bin/python3
#-*-coding:utf-8-*-

import config
from lib import option
from lib.runprocess import *
from lib.androidinfo import *

class AutoUnix :
    out_path = ""
    def __init__(self) :
        self.out_path = "c:\\temp\\unix\\"
        print ("__init__")
    def help(self, args) :
        hel = u"""autoUnix [option]
        [option]
        -o : File을 담을 Path를 설정
        -h : help
        """
        print hel
    def set_folder_path(self, args) :
        if args == 0 :
            print ("opt:error path")
            sys.exit()
        self.out_path = args[0]
    def run(self, args) :
        devicesOut = RunProcessOut("adb devices")
        devices = list()
        other = list()

        for device in devicesOut :
            device = device.decode("UTF-8").strip()
            device = device.strip()
            if device.find("List of devices attached") != -1 :
                continue
            if device == u"\n" or device == u" " or device == u"\r\n" :
                continue
            if len( device.split() ) != 2 :
                continue
            if device.find("device") != -1 :
                devices.append( device.split()[0] )
            else :
                other.append( device.split()[0] )
    
        for device in devices :
            print ("RUN DEVICE : " + device)
            deviceInfo = DeviceInfo(device)
            deviceInfo.extractDeviceInfo()
            deviceInfo.prints()

            adb = "adb "
            if len(device) > 0 :
                adb = "adb -s " + device + " "

            RunProcessWait(adb + "shell cp /proc/net/unix /sdcard/")

            name = deviceInfo.ver_os + "_" + deviceInfo.ver_sdk + "_" + deviceInfo.manufacturer + "_" + deviceInfo.model
            name = name.replace(" ", "")
            fileName = name
            idx = 0
            print ("outPath : " + self.out_path)
            print ("OUT : " + os.sep)
            if self.out_path[-1] != os.sep :
                self.out_path = self.out_path + os.sep
            while os.path.isfile(self.out_path + os.sep + fileName) :
                fileName = name + "_" + str(idx)
                idx = idx + 1

            RunProcessWait(adb + "pull /sdcard/unix " + self.out_path + fileName)

        for oo in other :
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
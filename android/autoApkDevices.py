#!/usr/bin/python3
#-*-coding:utf-8-*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from subprocess import *
import time
import threading
from lib.runprocess import *
from lib.androidinfo import *
print ("autoApkDevices.py runing")

currentFilePath = os.path.dirname(os.path.realpath(__file__))
#mainDir = dirName = currentFilePath + "/../temp"
mainDir = dirName = currentFilePath + os.sep + ".." + os.sep + "temp"
deviceDirPath = ""

def autorunning(device, apkFileName, apkName, apkActivity) :
    adb = "adb -d "
    if device != "" :
        adb = "adb -s " + device + " "
        deviceDirPath = mainDir + os.sep + device
        if not os.path.isdir(mainDir) :
            os.mkdir(mainDir)
        if not os.path.isdir(deviceDirPath) :
            os.mkdir(deviceDirPath)
    
    device_info = DeviceInfo(device)

    RunProcessOut(adb + 'uninstall ' + apkName)
    if int(device_info.ver_os[0]) >= 6 :
        outLine = RunProcessOut(adb + 'install -r -g ' + apkFileName)
    else :
        RunProcessOut(adb + 'install ' + apkFileName)

    #RunProcessOut(adb + 'shell am start -a android.intent.action.MAIN -n ' + apkName + '/' + apkActivity)
    RunProcessOut(adb + "shell am start -n " + apkName + '/' + apkActivity + " -a android.intent.action.MAIN -c android.intent.category.LAUNCHER")
    #RunProcessWait(currentFilePath + "/autoApkRun.py " + apk + " " + device)
    time.sleep(5)
 

if __name__ == "__main__":
    apkFile = "/Users/numa/temp/test/SmartHiPlus_DX.apk"

    args = sys.argv[1:]
    print (args)
    if not args:
        print ('Not Command')
        sys.exit()
    for arg in args :
        if arg.endswith("-h") == True :
            helpe = u'''
            매크로 파일인 .txt 파일과 APK파일인 .apk 스크린샷을 받을 위치의 path를 넣어주시면 됩니다.
            순서는 상관 없습니다.
            '''
        if arg.endswith(".apk") == True :
            apkFile = arg
        else :
            mainDir = arg

    temp = RunProcessOut('python '+ currentFilePath +'/maapt.py -n ' + apkFile)
    apkName = temp[0]
    temp = RunProcessOut('python '+ currentFilePath +'/maapt.py -a ' + apkFile)
    apkActivity = temp[0]
    apkName = apkName.strip()
    apkName = apkName.decode("UTF-8").strip()
    apkActivity = apkActivity.strip()
    apkActivity = apkActivity.decode("UTF-8").strip()

   
    devicesOut = RunProcessOut("adb devices")
    devices = list()
    others = list()

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
            others.append( device.split()[0] )


    for device in devices :
        print ("Run device : " + device)
        t = threading.Thread( target=autorunning, args=(device, apkFile, apkName, apkActivity) )
        t.start()
        #autorunning(device, apkFile, apkName, apkActivity)


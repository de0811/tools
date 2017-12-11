#!/usr/bin/python
#-*-coding:utf-8-*-

from subprocess import *
import os
import sys
import time
import threading
from lib.runprocess import *
print "autoRec.py runing"

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
    RunProcessOut(adb + 'uninstall ' + apkName)
    outLine = RunProcessOut(adb + 'install -r -g ' + apkFileName)
    for li in outLine :
        if li.find("rror") != -1 :
            RunProcessOut(adb + 'install -r ' + apkFileName)
    RunProcessOut(adb + 'shell am start -a android.intent.action.MAIN -n ' + apkName + '/' + apkActivity)

    #RunProcessWait(currentFilePath + "/autoApkRun.py " + apk + " " + device)
    time.sleep(5)
 

if __name__ == "__main__":
    apkFile = "/Users/numa/temp/test/SmartHiPlus_DX.apk"
    mecroFile = "/Users/numa/rec.txt"

    args = sys.argv[1:]
    print args
    if not args:
        print 'Not Command'
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
    apkActivity = apkActivity.strip()

   
    devicesOut = RunProcessOut("adb devices")
    devices = list()
    for device in devicesOut[1:-1] :
        devices.append(device.split()[0])


    for device in devices :
        print "Run device : " + device
        t = threading.Thread( target=autorunning, args=(device, apkFile, apkName, apkActivity) )
        t.start()



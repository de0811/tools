#!/usr/bin/python
#-*-coding:utf-8-*-

from subprocess import *
import os
import sys
import shutil
import config
import time
import threading
from lib import option
from collections import deque #Queue

print "autoRec.py runing"

currentFilePath = os.path.dirname(os.path.realpath(__file__))
mainDir = dirName = currentFilePath + "/../temp"
deviceDirPath = ""
def RunProcessOut(cmd):
    cmd_args = cmd.split()
    pipe = Popen(cmd_args, stdout=PIPE, stderr=STDOUT)
    outList = pipe.stdout.readlines()
    return outList
def RunProcessWait(cmd):
    #print cmd
    cmd_args = cmd.split()
    process = Popen(cmd_args)
    while process.poll() is None:
        pass
    #print process.poll()

def returnDel(stra):
    point = stra.find('\r\t')
    if point is 0:
        return stra
    return stra[0:point]


   
def autorunning(device="", apk="") :
    adb = "adb -d "
    if device != "" :
        adb = "adb -s " + device + " "
        deviceDirPath = mainDir + os.sep + device
        if not os.path.isdir(mainDir) :
            os.mkdir(mainDir)

        if not os.path.isdir(deviceDirPath) :
            os.mkdir(deviceDirPath)

    apkFileName = apk
    
    temp = RunProcessOut('python '+ currentFilePath +'/maapt.py -n ' + apkFileName)
    apkName = returnDel(temp[0])
    temp = RunProcessOut('python '+ currentFilePath +'/maapt.py -a ' + apkFileName)
    apkActivity = returnDel(temp[0])
    print "&&&" * 30
    print temp
    #apkActivity = temp[0].strip()
    print apkName
    print apkActivity

    RunProcessOut(adb + 'uninstall ' + apkName)
    outLine = RunProcessOut(adb + 'install -r -g ' + apkFileName)
    for li in outLine :
        if li.find("rror") != -1 :
            RunProcessOut(adb + 'install -r ' + apkFileName)
    RunProcessOut(adb + 'shell am start -a android.intent.action.MAIN -n ' + apkName + '/' + apkActivity)

    #RunProcessWait(currentFilePath + "/autoApkRun.py " + apk + " " + device)
    time.sleep(5)
 

if __name__ == "__main__":
    #apkFile = "/Users/numa/droid.apk"
    #apkFile = "/Users/numa/temp/test/btc_android_20171124162013731_DX.apk"

    #apkFile = "/Users/numa/temp/test/healthmax_20171127180137823_DX.apk"
    #apkFile = "/Users/numa/temp/test/insung_20171127185817178_DX.apk"
    #apkFile = "/Users/numa/temp/test/kyobo_20171127202602607_DX.apk"

    #apkFile = "/Users/numa/temp/test/sksjoopasoo_20171128162217877_DX.apk"

    #apkFile = "/Users/numa/temp/test/HKFireCyberApp_DX.apk"

    #apkFile = "/Users/numa/temp/test/Onebank_V151_171116_1925_R_DX.apk"
    
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

   
    devicesOut = RunProcessOut("adb devices")
    devices = list()
    for device in devicesOut[1:-1] :
        devices.append(device.split()[0])

    for device in devices :
        t = threading.Thread( target=autorunning, args=(device, apkFile) )
        t.start()



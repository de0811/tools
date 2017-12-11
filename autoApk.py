#!/usr/bin/python
#-*-coding:utf-8-*-

#실행 , 종료 시키는 걸로 시간도 잴까? 시간도 재자
import sys
import os
import time
from subprocess import *
from lib.runprocess import *
from lib.androidinfo import *


def returnDel(stra):
    point = stra.find('\r\t')
    if point is 0:
        return stra
    return stra[0:point]

def getCurrentFocused(currentDumpsys) :
    focused = ""
    for k in range( len(currentDumpsys) ) :
        if currentDumpsys[k].find("mFocusedWindow") != -1 :
            focused = currentDumpsys[k].strip().split()[-1][:-1].split(":")[0]
            break
    print "focused  : " + focused
    return focused
 

if __name__ == "__main__":
    args = sys.argv[1:]
    apkFileName = args[0]
    device = ""
    adb = "adb "
    if(len(args) > 1) :
        adb = adb + "-s " + args[1] + " "
        device = args[1]

    
    temp = RunProcessOut('python '+ os.path.dirname(os.path.realpath(__file__)) +'/maapt.py -n ' + apkFileName)
    #apkName = returnDel(temp[0])
    apkName = temp[0].strip()
    temp = RunProcessOut('python '+ os.path.dirname(os.path.realpath(__file__)) +'/maapt.py -a ' + apkFileName)
    #apkActivity = returnDel(temp[0])
    apkActivity = temp[0].strip()
    #apkActivity = temp[0].strip()
    print "APK Name : " + apkName + "  Activity Name : " + apkActivity

    RunProcessOut(adb + 'uninstall ' + apkName)
    outLine = RunProcessOut(adb + 'install -r -g ' + apkFileName)
    for li in outLine :
        if li.find("rror") != -1 :
            RunProcessOut(adb + 'install -r ' + apkFileName)
    #begin = time.clock()
    apkName = apkName.strip()
    apkActivity = apkActivity.strip()
    RunProcessOut(adb + 'shell am start -a android.intent.action.MAIN -n ' + apkName + '/' + apkActivity)

    while True:
    #time.sleep(5)
        currentDumpsys = DumpsysWindow(device)
        #temp = RunProcessOut(adb + 'shell dumpsys window')
        #focused = getCurrentFocused(temp)
        focused = currentDumpsys.mFocused
        #if len(temp) == 0 : continue
        #print temp[0]
        if currentDumpsys.isFocusedError() :
            break
        if 0 < focused.count(apkActivity) :
            break

    #print "adb -d am start -a android.intent.action.MAIN -n " + apkName + "/" + apkActivity
    #time.sleep(10)
    #end = time.clock()
    #RunProcessOut(adb + 'uninstall ' + apkName)

    #elapsed = end - begin
    
    #print elapsed

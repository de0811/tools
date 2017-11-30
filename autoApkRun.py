#!/usr/bin/python
#-*-coding:utf-8-*-

#실행 , 종료 시키는 걸로 시간도 잴까? 시간도 재자
import sys
import os
import time
from subprocess import *

def RunProcess(cmd):
    print cmd
    cmd_args = cmd.split()
    pipe = Popen(cmd_args, stdout=PIPE, stderr=STDOUT)
    outList = pipe.stdout.readlines()
    return outList
    
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
    device = str()
    adb = "adb "
    if(len(args) > 1) :
        adb = adb + "-s " + args[1] + " "

    
    temp = RunProcess('python '+ os.path.dirname(os.path.realpath(__file__)) +'/maapt.py -n ' + apkFileName)
    apkName = returnDel(temp[0])
    temp = RunProcess('python '+ os.path.dirname(os.path.realpath(__file__)) +'/maapt.py -a ' + apkFileName)
    apkActivity = returnDel(temp[0])
    print "&&&" * 30
    print temp
    #apkActivity = temp[0].strip()
    print apkName
    print apkActivity

    RunProcess(adb + 'uninstall ' + apkName)
    outLine = RunProcess(adb + 'install -r -g ' + apkFileName)
    for li in outLine :
        if li.find("rror") != -1 :
            RunProcess(adb + 'install -r ' + apkFileName)
    #begin = time.clock()
    apkName = apkName.strip()
    apkActivity = apkActivity.strip()
    RunProcess(adb + 'shell am start -a android.intent.action.MAIN -n ' + apkName + '/' + apkActivity)

    while True:
    #time.sleep(5)
        temp = RunProcess(adb + 'shell dumpsys window')
        focused = getCurrentFocused(temp)
        if len(temp) == 0 : continue
        print temp[0]
        if 0 < focused.count(apkActivity) :
            break

    #print "adb -d am start -a android.intent.action.MAIN -n " + apkName + "/" + apkActivity
    #time.sleep(10)
    #end = time.clock()
    #RunProcess(adb + 'uninstall ' + apkName)

    #elapsed = end - begin
    
    #print elapsed

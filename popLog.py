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
    
def returnDel(str):
    point = str.find('\r\t')
    if point is 0:
        return str
    return str[0:point-1]

if __name__ == "__main__":
    args = sys.argv[1:]
    apkFileName = args[0]
    
    temp = RunProcess('python '+ os.path.dirname(os.path.realpath(__file__)) +'\\aapt.py -n ' + apkFileName)
    apkName = returnDel(temp[0])
    temp = RunProcess('python '+ os.path.dirname(os.path.realpath(__file__)) +'\\aapt.py -a ' + apkFileName)
    apkActivity = returnDel(temp[0])
    print apkName
    print apkActivity
    RunProcess('adb -d install -r ' + apkFileName)
    begin = time.clock()
    RunProcess('adb -d shell am start -a android.intent.action.MAIN -n ' + apkName + '/' + apkActivity)
    
    while 1:
    #time.sleep(5)
        temp = RunProcess('adb -d shell dumpsys window |grep mFocusedWindow')
        if len(temp) == 0 : continue
        print temp[0]
        if 0 < temp[0].count(apkActivity) :
            break

    #print "adb -d am start -a android.intent.action.MAIN -n " + apkName + "/" + apkActivity
    #time.sleep(10)
    end = time.clock()
    RunProcess('adb -d uninstall ' + apkName)

    elapsed = end - begin
    
    print elapsed
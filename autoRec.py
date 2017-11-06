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


def RunProcess(cmd):
    print cmd
    cmd_args = cmd.split()
    process = Popen(cmd_args)
    #while process.poll() is None:
    #    pass
    #print process.poll()
    #기다릴 수 없기 때문에 확인하지 않고 넘어감

#해상도 size : adb shell wm size
#터치 : adb shell input tap x y
#드래그 : adb shell input swipe x1 y1 x2 y2
#문자 입력 : adb shell input text 'text'
#특정 키 입력 : adb shell input keyevent '4'

def RunProcessOut(cmd):
    cmd_args = cmd.split()
    pipe = Popen(cmd_args, stdout=PIPE, stderr=STDOUT)
    outList = pipe.stdout.readlines()
    return outList

def RunProcessWait(cmd):
    print cmd
    cmd_args = cmd.split()
    process = Popen(cmd_args)
    while process.poll() is None:
        pass
    print process.poll()

start_getEvent = False
getEventPipe = None
dequeEvent = deque()
def getEventADB() :
    print "start getEventADB()"
    cmd = "adb -d shell getevent"
    cmd_args = cmd.split()
    getEventPipe = Popen(cmd_args, stdin=None, stdout=PIPE, stderr=STDOUT)
    start_getEvent = True
    while getEventPipe.poll() is None :
        dequeEvent.append(getEventPipe.stdout.read(1))
        if start_getEvent != True :
            getEventPipe.kill()
            #return

start_manager = False
def manager() :
    print "start Manager()"
    start_manager = True
    mergeEvent = list()
    endEvent = list()
    while start_manager == True :
        if len(dequeEvent) > 1 :
            tempE = dequeEvent.popleft()
            if tempE == '\r' or tempE == '\n' :
                tempE = "".join(mergeEvent)
                if tempE == '\r' or tempE == '\n' or tempE == "" :
                    continue
                print tempE
                if tempE.find('exit') != -1 or tempE.find('no devices found') != -1 :
                    start_getEvent = False
                    start_manager = False
                    start_activity = False
                    break
                if len(stackActivity) > 0 :
                    endEvent.append( stackActivity[-1] )
                endEvent.append( tempE )
                del mergeEvent
                mergeEvent = list()
            else :
                mergeEvent.append( tempE )
    print endEvent
    mecro = open(currentFilePath + "/../mecro.txt", 'w')
    for even in endEvent :
        print str(even)
        mecro.write(even + "\n")
    mecro.close()


stackActivity = list()
start_activity = False
def getActivity() :
    adb = 'adb -d '
    adb + 'shell dumpsys window |grep mFocusedWindow'
    cmd = 'adb -d shell dumpsys window | grep mFocusedWindow'
    start_activity = True
    print "getActivity Start"
    while start_activity == True :
        temp = RunProcessOut(cmd)
        if len(temp) > 0 :
            if len(stackActivity) > 0 :
                if stackActivity[-1].find( temp[0].strip() ) == -1 :
                    stackActivity.append( temp[0].strip() )
            else :
                stackActivity.append( temp[0].strip() )

if __name__ == "__main__":
    getEventThread = threading.Thread( target=getEventADB, args=() )
    getEventThread.daemon = True
    getEventThread.start()
    activityThread = threading.Thread( target=getActivity, args=() )
    activityThread.daemon = True
    activityThread.start()
    time.sleep(1)
    managerThread = threading.Thread( target=manager, args=() )
    managerThread.start()

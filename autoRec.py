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
    cmd = "adb -d shell getevent"
    cmd_args = cmd.split()
    getEventPipe = Popen(cmd_args, stdout=PIPE, stderr=STDOUT)
    start_getEvent = True
    while getEventPipe.poll() is None :
        dequeEvent.append(getEventPipe.stdout.read(1))
        if start_getEvent != True :
            getEventPipe.kill()

start_manager = False
def manager() :
    start_manager = True
    while start_manager == True :
        if len(dequeEvent) :
            pass

def controller() :
    command = ""
    while command != "x" :
        command = raw_input("x : Command exit")
    start_getEvent = False
    start_manager = False



def getActivity() :
    pass

if __name__ == "__main__":
    getEventADB()
    print "".join(dequeEvent)
    getEventThread = threading.Thread( target=getEventADB, args=() )
    getEventThread.start()
    time.sleep(1)
    managerThread = threading.Thread( target=manager, args=() )
    managerThread.start()
    controllerThread = threading.Thread( target=controller, args=() )
    controllerThread.start()

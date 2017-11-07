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

print "autoPasing.py runing"

currentFilePath = os.path.dirname(os.path.realpath(__file__))
mainDir = dirName = currentFilePath + "../temp"

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
 

class Event :
    time = float()
    event = str()
    etype = int()
    msg = int()
    data = int()
    focused = str()
    action = str()
    def __init__(self, time=0, event="", etype=0, msg=0, data=0, focused="", action="") :
        self.time = time
        self.event = event
        self.etype = etype
        self.msg = msg
        self.data = data
        self.focused = focused
        self.action = action

class RunEvent :
    time1 = float()
    time2 = float()
    event = str()
    action = str()
    focused = str()
    x1 = int()
    y1 = int()
    x2 = int()
    y2 = int()
    def __init__(self, time1=0, time2=0, event="", action="", focused="", x1=0, y1=0, x2=0, y2=0) :
        self.time1 = time1
        self.time2 = time2
        self.event = event
        self.action = action
        self.focused = focused
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def prints(self) :
        print "*" * 100
        print "time : " + str(self.time1) + "  event : " + self.event + "  action : " + self.action
        print "focused : " + self.focused + "  x1 : " + str(self.x1) + "  y1 : " + str(self.y1) + "  x2 : " + str(self.x2) + "  y2 : " + str(self.y2)
        print "*" * 100
        

def parsingEvent(eventFull) :
    start = list()
    end = list()
    for k in range(len(eventFull)) :
        if eventFull[k].msg is int('0x0039', 16):
            if eventFull[k].data == int('0xffffffff', 16) :
                end.append(k)
            else :
                start.append(k)
        if eventFull[k].action != "" :
            start.append(k)
            end.append(k)

    print 'start'
    print start
    print 'end'
    print end
    print '--' * 10

    runEvents = list()
    length = min(len(start), len(end))
    for k in range(length) :
        xs = list()
        ys = list()
        if start[k] == end[k] :
            runEvents.append(RunEvent( time1=eventFull[start[k]].time, event=eventFull[start[k]].event, action=eventFull[start[k]].action, focused=eventFull[start[k]].focused ))
            continue
        for blockEn in eventFull[start[k] : end[k]] :
            if blockEn.msg is int('0x0035', 16) : #ABS_MT_POSITION_X
                xs.append(blockEn)
            elif blockEn.msg is int('0x0036', 16) : #ABS_MT_POSITION_Y
                ys.append(blockEn)
        if len(xs) == 0 or len(ys) == 0 :
            continue
        #def __init__(self, time1=0, time2=0, event="", action="", focused="", x1=0, y1=0, x2=0, y2=0) :
        runEvents.append( RunEvent(time1=xs[0].time, time2=ys[-1].time, event=xs[0].event, action="", focused=xs[0].focused, x1=xs[0].data, y1=ys[0].data, x2=xs[-1].data, y2=ys[-1].data) )
    return runEvents

def parsingOriginEvent(mecroPath="/Users/numa/rec.txt") :
    #임시 고정 Path 설정
    fd = open(mecroPath, 'r')
    eventNumber = list()
    eventName = list()
    startRec = 0.0
    eventFull = list()
    focused = ""

    while True:
        line = fd.readline()
        if not line: break
        if -1 != line.find('add device'):
            eventNumber.append(line.split()[-1].strip())
            continue
        elif -1 != line.find('name:'):
            eventName.append(line[line.find('\"'):].strip())
            continue
        elif True == line.startswith('mFocusedWindow'):
            focused = line.split()[-1][:-1]
            continue
        elif True == line.startswith('screen'):
            eventFull.append( Event(time=1.0, focused=focused, action='screen' ) )
            continue
        line = line.strip()
        parseCmd = line.split()[1:]
        parseCmd[0] = parseCmd[0][0:-1]
        print parseCmd
        print "parseCmd : " + str(len(parseCmd))
        #def __init__(self, time=0, event=0, etype=0, msg=0, data=0, focused="", action="") :
        eventFull.append( Event(time=float(parseCmd[0]), event=parseCmd[1][0:-1], etype=int(parseCmd[2], 16), msg=int(parseCmd[3], 16), data=int(parseCmd[4], 16), focused=focused, action="") )
    print '!!!!!!!!'
    print eventNumber
    print '--------'
    print eventName
    return eventFull


def runMecro(device, apk, runEvent) :
    adb = "adb "
    if len(device) > 0 :
        adb = "adb -s " + device + " "

    deviceDirPath = mainDir + device

    if not os.path.isdir(mainDir) :
        os.mkdir(mainDir)

    if not os.path.isdir(deviceDirPath) :
        os.mkdir(deviceDirPath)

    #autoApkRun.py running 
    RunProcessWait(currentFilePath + "/autoApkRun.py " + apk + " " + device)

    wmSize = RunProcessOut(adb + "shell wm size")
    print wmSize
    #['Physical size: 1440x2560\n', 'Override size: 1080x1920\n']
    #['Physical size: 1080x1920\r\n']
    temp = wmSize[-1].split()[-1].strip()
    wmSize = temp.split('x')
    print wmSize
    origX = 1080
    origY = 1920

    ratioX = float(wmSize[0]) / float(origX)
    ratioY = float(wmSize[1]) / float(origY)

    print "ratioX : " + str(ratioX)
    print "ratioY : " + str(ratioY)
    

    count = 0
    startRec = 0.0
    activityTime = 0.0
    for sw in runEvent:
        print "next input"
        sw.prints()
        count = count + 1
        print "Current [ " + str(count) + " :: " + str(len(runEvent)) + "]"

        #사람처럼 시간에 맞게 움직이도록 확인
        print "start Time : " + str(startRec) + "  activityTime : " + str(activityTime) + "   sw.time1 : " + str(sw.time1)
        if(startRec == 0) :
            startRec = sw.time1
        tempTime = sw.time1 + activityTime - startRec
        if tempTime < 0 :
            tempTime = sw.time1 
            activityTime = activityTime + sw.time1
        print "result Sleep Time : " + str(tempTime)
        time.sleep( tempTime )
        startRec = tempTime + startRec

        #맞는 Activity에 위치해 있는지 확인
        currentActivity = RunProcessOut(adb + "shell dumpsys window |grep mFocusedWindow")
        print "current : " + currentActivity[0].strip() + "    origin : " + sw.focused
        print "Result : " + str(currentActivity[0].strip().find(sw.focused) != -1 )
        while currentActivity[0].strip().find(sw.focused) == -1 :
            if currentActivity[0].strip().find("PopupWindow") != -1 and sw.focused.find("PopupWindow") != -1 :
                break;
            time.sleep(0.1)
            currentActivity = RunProcessOut(adb + "shell dumpsys window |grep mFocusedWindow")

        if sw.action == "" :
            if sw.y1 > 1780 and sw.y2 > 1780:
                if sw.x1 > 130  and sw.x1 < 355 : #backKey
                    RunProcess(adb + "shell input keyevent KEYCODE_BACK")
                    continue
                elif sw.x1 > 420 and sw.x1 < 650 : #HomeKey
                    RunProcess(adb + "shell input keyevent KEYCODE_HOME")
                    continue
                elif sw.x1 > 720 and sw.x1 < 960 : #MenuKey
                    RunProcess(adb + "shell input keyevent KEYCODE_MENU")
                    continue
            if sw.x1 == sw.x2 and sw.y1 == sw.y2 :
                RunProcess(adb + "shell input tap " + str(sw.x1 * ratioX) + " " + str(sw.y1 * ratioY))
            else :
                RunProcess(adb + "shell input swipe " + str(sw.x1 * ratioX) + " " + str(sw.y1 * ratioY) + " " + str(sw.x2 * ratioX) + " " + str(sw.y2 * ratioY) + " " + str( int( (sw.time2-sw.time1) * 1000 ) ) )
        else :
            if sw.action.startswith("screen") :
                RunProcessWait(currentFilePath + "/screencap.py -d " + device + " -o " + deviceDirPath)
    print "End Device : " + device



if __name__ == "__main__":
    apkFile = "/Users/numa/scheduler.apk"
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
        elif arg.endswith(".txt") == True :
            mecroFile = arg
        else :
            mainDir = arg

   
    devicesOut = RunProcessOut("adb devices")
    devices = list()
    for device in devicesOut[1:-1] :
        devices.append(device.split()[0])

    eventFull = parsingOriginEvent(mecroFile)
    runEvent = parsingEvent(eventFull)

    for device in devices :
        t = threading.Thread( target=runMecro, args=(device, "/Users/numa/scheduler.apk", runEvent) )
        t.start()





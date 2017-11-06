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
    def __init__(self, time, event, etype, msg, data) :
        self.time = time
        self.event = event
        self.etype = etype
        self.msg = msg
        self.data = data

def parsingEvent(eventFull) :
    start = list()
    end = list()
    for k in range(len(eventFull)) :
        if eventFull[k].msg is int('0x0039', 16):
            if eventFull[k].data == int('0xffffffff', 16) :
                end.append(k)
            else :
                start.append(k)

    print 'start'
    print start
    print 'end'
    print end
    print '--' * 10
    swipe = list()
    length = min(len(start), len(end))
    for k in range(length) :
        xs = list()
        ys = list()
        for blockEn in eventFull[start[k] : end[k]] :
            if blockEn.msg is int('0x0035', 16) : #ABS_MT_POSITION_X
                xs.append(blockEn)
            elif blockEn.msg is int('0x0036', 16) : #ABS_MT_POSITION_Y
                ys.append(blockEn)
        if len(xs) == 0 or len(ys) == 0 :
            continue
        swipe.append([xs[0].time, xs[0].data, ys[0].data, ys[-1].time, xs[-1].data, ys[-1].data])
    return swipe

def runMecro(device, apk) :
    adb = "adb "
    if len(device) > 0 :
        adb = "adb -s " + device + " "
#임시 고정 Path 설정
    fd = open("/Users/numa/rec.txt", 'r')
    eventNumber = list()
    eventName = list()
    startRec = 0.0
    eventFull = list()

    while True:
        line = fd.readline()
        if not line: break
        if -1 != line.find('add device'):
            eventNumber.append(line.split()[-1].strip())
            continue
        elif -1 != line.find('name:'):
            eventName.append(line[line.find('\"'):].strip())
            continue
        line = line.strip()
        parseCmd = line.split()[1:]
        parseCmd[0] = parseCmd[0][0:-1]
        eventFull.append( Event(float(parseCmd[0]), parseCmd[1][0:-1], int(parseCmd[2], 16), int(parseCmd[3], 16), int(parseCmd[4], 16)) )
        if startRec == 0 :
            startRec = float(parseCmd[0])
    print '!!!!!!!!'
    print eventNumber
    print '--------'
    print eventName

    #popLog.py running
    RunProcessWait(currentFilePath + "/autoApkRun.py " + apk + " " + device)

    swipe = parsingEvent(eventFull)

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
    

    for sw in swipe:
        if(startRec == 0) :
            startRec = sw[0]
        print "next input"
        print sw
        time.sleep(sw[0] - startRec)
        startRec = sw[0]
        if sw[2] > 1780 :
            if sw[1] > 130  and sw[1] < 355 : #backKey
                RunProcess(adb + "shell input keyevent KEYCODE_BACK")
                continue
            elif sw[1] > 420 and sw[1] < 650 : #HomeKey
                RunProcess(adb + "shell input keyevent KEYCODE_HOME")
                continue
            elif sw[1] > 720 and sw[1] < 960 : #MenuKey
                RunProcess(adb + "shell input keyevent KEYCODE_MENU")
                continue
        if sw[1] == sw[4] and sw[2] == sw[5] :
            RunProcess(adb + "shell input tap " + str(sw[1] * ratioX) + " " + str(sw[2] * ratioY))
        else :
            RunProcess(adb + "shell input swipe " + str(sw[1] * ratioX) + " " + str(sw[2] * ratioY) + " " + str(sw[4] * ratioX) + " " + str(sw[5] * ratioY) + " " + str( int( (sw[3]-sw[0]) * 1000 ) ) )


if __name__ == "__main__":
    
    devicesOut = RunProcessOut("adb devices")
    devices = list()
    for device in devicesOut[1:-1] :
        devices.append(device.split()[0])

    for device in devices :
        t = threading.Thread( target=runMecro, args=(device, "/Users/numa/scheduler.apk") )
        t.start()





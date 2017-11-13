#!/usr/bin/python
#-*-coding:utf-8-*-

from subprocess import *
import os
import sys
import shutil
import config
import time
import threading
from autoRec import *
from lib import option

print "autoPasing.py runing"

currentFilePath = os.path.dirname(os.path.realpath(__file__))
mainDir = dirName = currentFilePath + "/../temp"

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
    def prints(self) :
        print "time : " + str(self.time) + "  event : " + self.event + "  etype : " + str(self.etype) + "  msg : " + str(self.msg) + "  data : " + str(self.data) + "  focused : " + self.focused + "  action : " + self.action

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
        if eventFull[k].action != "event" :
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
            print "keyword push" + "  " + str(start[k]) + " :: " + str(end[k])
            eventFull[start[k]].prints()
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
        print "event push"
        xs[0].prints
        runEvents.append( RunEvent(time1=xs[0].time, time2=ys[-1].time, event=xs[0].event, action=xs[0].action, focused=eventFull[start[k]].focused, x1=xs[0].data, y1=ys[0].data, x2=xs[-1].data, y2=ys[-1].data) )
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
        if True == line.startswith('wmSize::'):
            line = line[line.find("::")+2:]
            recDeviceInfo.setWmSizeParsing(line)
            recDeviceInfo.prints()
            continue
        elif True == line.startswith("deviceSize::") :
            line = line[line.find("::")+2:]
            settingDeviceParsing(line, recDeviceInfo)
        elif True == line.startswith("AddDeviceState::") :
            line = line[line.find("::")+2:]
            if -1 != line.find('add device'):
                eventNumber.append(line.split()[-1].strip())
            elif -1 != line.find('name:'):
                eventName.append(line[line.find('\"'):].strip())
            continue
        elif True == line.startswith("Focused::") :
            line = line[line.find("::")+2:]
            if True == line.startswith('mFocusedWindow'):
                focused = line.split()[-1]
            continue
        elif True == line.startswith("Keyword::") :
            line = line[line.find("::")+2:]
            eventFull.append( Event(time=1.0, focused=focused, action="keyword", event=line ) )
            continue
        elif True == line.startswith("Event::") :
            line = line.strip()
            parseCmd = line.split()[1:]
            parseCmd[0] = parseCmd[0][0:-1]
            print parseCmd
            print "parseCmd : " + str(len(parseCmd))
            print "focused : " + focused
            #def __init__(self, time=0, event=0, etype=0, msg=0, data=0, focused="", action="") :
            eventFull.append( Event(time=float(parseCmd[0]), event=parseCmd[1][0:-1], etype=int(parseCmd[2], 16), msg=int(parseCmd[3], 16), data=int(parseCmd[4], 16), focused=focused, action="event") )
    print '!!!!!!!!'
    print eventNumber
    print '--------'
    print eventName
    return eventFull

class MRect :
    posX = 0
    posY = 0
    sizeX = 0
    sizeY = 0
    def __init__(self, posX, posY, sizeX, sizeY) :
        self.posX = posX
        self.posY = posY
        self.sizeX = sizeX
        self.sizeY = sizeY
    def sub(self, tar) :
        x = self.posX - tar.posX
        y = self.posY - tar.posY
        sx = self.sizeX - tar.sizeX
        sy = self.sizeY - tar.sizeY
        return MRect(x, y, sx, sy)

def getPositionParsing(strPosSize) :
    #(813,936)(75x720)
    tempi = strPosSize.find(")")
    strPos = strPosSize[1:tempi]
    strSize = strPosSize[strPosSize[tempi:].find("(")+1+tempi:-1]
    print "PositionParsing :: " + "pivot : " + str(tempi) + "  strPos : " + strPos + "  strSize : " + strSize
    posX = strPos.split(",")[0]
    posY = strPos.split(",")[1]
    sizeX = strSize.split("x")[0]
    sizeY = strSize.split("x")[1]
    print "PositionParsing :: " + "pivot : " + str(tempi) + "  strPos : " + strPos + "  strSize : " + strSize + " posX : " + posX + " posY : " + posY + " sizeX : " + sizeX + " sizeY : " + sizeY
    return MRect(int(posX), int(posY), int(sizeX), int(sizeY))
    

def isBoxCollision(posX, posY, rect) :
    if rect.posX - posX < 0 or rect.posY - posY < 0 :
        return False
    elif rect.posX + rect.sizeX - posX > 0 or rect.posY + rect.sizeY - posY > 0 :
        return False
    return True
 

def runMecro(device, apk, runEvent) :
    adb = "adb "
    if len(device) > 0 :
        adb = "adb -s " + device + " "

    deviceDirPath = mainDir + "/" + device
    curDeviceInfo = DeviceInfo()

    if not os.path.isdir(mainDir) :
        os.mkdir(mainDir)

    if not os.path.isdir(deviceDirPath) :
        os.mkdir(deviceDirPath)

    #autoApkRun.py running 
    RunProcessWait(currentFilePath + "/autoApkRun.py " + apk + " " + device)

    settingDeviceInfo(curDeviceInfo, device)

    print "*" * 50 + "ALL SIZE" + "*" * 50
    print "Rec Device APP Size : " + str(recDeviceInfo.appSizeX) + ", " + str(recDeviceInfo.appSizeY)
    print "Cur Device APP Size : " + str(curDeviceInfo.appSizeX) + ", " + str(curDeviceInfo.appSizeY)
    #['Physical size: 1440x2560\n', 'Override size: 1080x1920\n']
    #['Physical size: 1080x1920\r\n']

    ratioX = float(curDeviceInfo.appSizeX) / float(recDeviceInfo.appSizeX)
    ratioY = float(curDeviceInfo.appSizeY) / float(recDeviceInfo.appSizeY)

    print "ratioX : " + str(ratioX)
    print "ratioY : " + str(ratioY)
    print "  >> ratioY : " + str(ratioY)
    
    print "*" * 108
    

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
        currentFocused = ""
        currentDumpsys = list()
        while True :
            currentDumpsys = RunProcessOut(adb + "shell dumpsys window")
            if len(currentDumpsys) > 0 :
                break
        currentFocused = getCurrentFocused(currentDumpsys)
        recFocused = sw.focused.split(":")[0]
        print "current : " + currentFocused + "    rec : " + recFocused
        print "Result : " + str(currentFocused.find(recFocused) != -1 )

        killCount = 0
        sleepTime = 0.1
        while currentFocused.find(recFocused) == -1 :
            time.sleep(0.2)
            while True :
                currentDumpsys = RunProcessOut(adb + "shell dumpsys window")
                if len(currentDumpsys) > 0 :
                    break
            currentFocused = getCurrentFocused(currentDumpsys)

            killCount = killCount + 1
            if killCount % 5 == 0 :
                sleepTime = sleepTime + 0.20
            if killCount > 30 :
                RunProcessWait(currentFilePath + "/screencap.py -d " + device + " -o " + deviceDirPath)
                return
        #print "currentFocused  : " + currentFocused

        recFocusedSize = sw.focused.split(":")[1]
        currentFocusedSize = getCurrentFocusedSize(currentDumpsys, currentFocused)
        print "info- recFocusedSize : " + recFocusedSize + "  currentFocusedSize : " + currentFocusedSize

        if sw.action == "event" :
            tempAddRatioX = 0.0
            tempAddRatioY = 0.0
            tempMulRatioX = 1.0
            tempMulRatioY = 1.0
            
            print "-" * 50 + "Ratio" + "-" * 50
            if recFocusedSize.find("wrap") > -1 : #크기를 알 수 없는 팝업
                tempMulRatioX = ratioX
                tempMulRatioY = ratioY
                print "ratioY -------- " + str(ratioY < 1.0)
                if ratioY < 1.0 :
                    tempMulRatioY = ratioY + ( (ratioY / 2) / 10 )
                    #tempMulRatioY = round(ratioY + 0.02, 2)
                print "Ratio :: wrap"
            elif curDeviceInfo.appSizeX == recDeviceInfo.appSizeX : #X축의 크기가 같다면 Y축의 크기는 변화가 있어도 위치에 대한 변화는 없음
                print "Ratio :: Same X "
                tempMulRatioY = 1.0
            elif recFocusedSize != currentFocusedSize : #화면의 크기가 다르든 특정 팝업의 크기만 다를 경우 해당 위치의 좌표를 구할 수 있기 때문에 그에 따른 수치 변경
                print "Ratio :: Popup Size diff"
                print "recFocusedSize : " + recFocusedSize + "  currentFocusedSize : " + currentFocusedSize
                recRect = getPositionParsing(recFocusedSize)
                currentRect = getPositionParsing(currentFocusedSize)
            
                print "origin Pos :: " + "x1 : " + str(sw.x1) + " y1 : " + str(sw.y1) + " x2 : " + str(sw.x2) + " y2 : " + str(sw.y2)
                subVal = currentRect.sub(recRect)
                modRatio = True
                tempAddRatioX = subVal.posX
                tempAddRatioY = subVal.posY
            else :
                print "Ratio :: else"
                tempMulRatioX = ratioX
                tempMulRatioY = round(ratioY, 2)


            print "tempAddRatioX : " + str(tempAddRatioX) + "  tempAddRatioY : " + str(tempAddRatioY)
            print "tempMulRatioX : " + str(tempMulRatioX) + "  tempMulRatioY : " + str(tempMulRatioY)
            print "-" * 105

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
                RunProcess( adb + "shell input tap " + str((sw.x1 + tempAddRatioX) * tempMulRatioX) + " " + str((sw.y1 + tempAddRatioY) * tempMulRatioY) )
            else :
                RunProcess(adb + "shell input swipe " + str((sw.x1 + tempAddRatioX) * tempMulRatioX) + " " + str((sw.y1 + tempAddRatioY) * tempMulRatioY) + " " + str((sw.x2 + tempAddRatioX) * tempMulRatioX) + " " + str((sw.y2 + tempAddRatioY) * tempMulRatioY) + " " + str( int( (sw.time2-sw.time1) * 1000 ) ) )
        elif sw.action == "keyword" :
            if sw.event.startswith("screen") :
                RunProcessWait(currentFilePath + "/screencap.py -d " + device + " -o " + deviceDirPath)
    print "End Device : " + device



if __name__ == "__main__":
    apkFile = "/Users/numa/droid.apk"
    mecroFile = "/Users/numa/rec.txt"

    """
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
    """

   
    devicesOut = RunProcessOut("adb devices")
    devices = list()
    for device in devicesOut[1:-1] :
        devices.append(device.split()[0])

    eventFull = parsingOriginEvent(mecroFile)
    runEvent = parsingEvent(eventFull)

    for device in devices :
        t = threading.Thread( target=runMecro, args=(device, apkFile, runEvent) )
        t.start()





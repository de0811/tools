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
    cmd = "adb -d shell getevent -t"
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
                #Device가 없거나 종료 문자 exit가 들어오면 종료
                if tempE.find('exit') != -1 or tempE.find('no devices found') != -1 :
                    start_getEvent = False
                    start_manager = False
                    start_activity = False
                    break
                #device정보 관련
                elif tempE.startswith("add device") or tempE.startswith("  name:") :
                    endEvent.append("AddDeviceState::" + tempE)
                #이벤트라면
                elif tempE.startswith("[  ") :
                    if len(stackActivity) > 0 :
                        endEvent.append("Focused::" + stackActivity[-1] )
                        print stackActivity[-1]
                        endEvent.append("Event::" + tempE)
                else :
                    endEvent.append("Focused::" + stackActivity[-1] )
                    endEvent.append("Keyword::" + tempE )
                del mergeEvent
                mergeEvent = list()
            else :
                mergeEvent.append( tempE )
    print endEvent
    mecro = open(mecroFile, 'w')

    mecro.write("wmSize::" + recDeviceInfo.wmSize + "\n")
    """init=1080x1920 480dpi cur=1080x1920 app=1080x1776 rng=1080x1008-1776x1704"""
    print "init=" + recDeviceInfo.initSize + " " + str(recDeviceInfo.dpi) + "dpi" +  " " + "cur=" + recDeviceInfo.curSize + " " + "app=" + recDeviceInfo.appSize
    mecro.write("deviceSize::" + "init=" + recDeviceInfo.initSize + " " + str(recDeviceInfo.dpi) + "dpi" +  " " + "cur=" + recDeviceInfo.curSize + " " + "app=" + recDeviceInfo.appSize + "\n")
    
    for even in endEvent :
        print str(even)
        mecro.write(even + "\n")
    mecro.close()


def getCurrentFocused(currentDumpsys) :
    focused = ""
    for k in range( len(currentDumpsys) ) :
        if currentDumpsys[k].find("mFocusedWindow") != -1 :
            focused = currentDumpsys[k].strip().split()[-1][:-1].split(":")[0]
            break
    #print "focused  : " + focused
    return focused
    
def getCurrentFocusedSize(currentDumpsys, focused) :
    tt = ""
    focused_win_num = ""
    focused_size = ""
    for k in range( len(currentDumpsys) ) :
        if currentDumpsys[k].find(focused) != -1 :
            if currentDumpsys[k].find("Window #") != -1:
                focused_win_num = currentDumpsys[k].strip().split(":")[0]
                break
    #print "focused Windows #  : " + focused_win_num
    for k in range( len(currentDumpsys) ) :
        if currentDumpsys[k].find(focused_win_num) != -1 :
            _split = currentDumpsys[k+3].split()[0]
            focused_size = _split[_split.find("{")+1:]
    #print "focused Size  : " + focused_size
    #print "mFocusedWindow " + focused + ":" + focused_size
    return focused_size
 

stackActivity = list()
start_activity = True
def getActivity() :
    print "start getActivity()"
    start_activity = True
    while start_activity == True :
        focused = ""
        currentDumpsys = RunProcessOut("adb -d shell dumpsys window")
        focused = getCurrentFocused(currentDumpsys)
           
        focused_size = getCurrentFocusedSize(currentDumpsys, focused)
        saveFocused = "mFocusedWindow " + focused + ":" + focused_size
        if len(stackActivity) > 0 and stackActivity[-1].find(saveFocused) != -1 : #해당 mFocused가 있나 없나 확인
            continue

        stackActivity.append(saveFocused)
        #print "mFocusedWindow " + focused + ":" + focused_size
    print "End Activity"

class DeviceInfo :
    wmSize = "" #해상도
    wmSizeX = 0 #해상도X
    wmSizeY = 0 #해상도Y
    initSize = "" #해상도와 같은 뜻?
    initSizeX = 0
    initSizeY = 0
    dpi = 0
    curSize = "" #적용된 해상도인듯
    curSizeX = 0
    curSizeY = 0
    appSize = "" #적용된 앱의 해상도인듯
    appSizeX = 0
    appSizeY = 0
    def setWmSizeParsing(self, strWmSize) :
        self.wmSize = strWmSize
        self.wmSizeX = strWmSize.split("x")[0]
        self.wmSizeY = strWmSize.split("x")[1]
    def setDpiParsing(self, strDpi) :
        self.dpi = int(strDpi[:-3], 10)
    def setInitSizeParsing(self, strInitSize) :
        self.initSize = strInitSize
        self.initSizeX = strInitSize.split("x")[0]
        self.initSizeY = strInitSize.split("x")[1]
    def setCurSizeParsing(self, strCurSize) :
        self.curSize = strCurSize
        self.curSizeX = strCurSize.split("x")[0]
        self.curSizeY = strCurSize.split("x")[1]
    def setAppSizeParsing(self, strAppSize) :
        self.appSize = strAppSize
        self.appSizeX = strAppSize.split("x")[0]
        self.appSizeY = strAppSize.split("x")[1]
    def prints(self) :
        print "*" * 50 + "SIZE" + "*" * 50
        print "wmSize : " + self.wmSize + "  " + "wmSizeX : " + str(self.wmSizeX) + "  " + "wmSizeY : " + str(self.wmSizeY)
        print "initSize : " + self.initSize + "  " + "initSizeX : " + str(self.initSizeX) + "  " + "initSizeY : " + str(self.initSizeY)
        print "dpi : " + str(self.dpi)
        print "curSize : " + self.curSize + "  " + "curSizeX : " + str(self.curSizeX) + "  " + "curSizeY : " + str(self.curSizeY)
        print "appSize : " + self.appSize + "  " + "appSizeX : " + str(self.appSizeX) + "  " + "appSizeY : " + str(self.appSizeY)
        print "*" * 104
recDeviceInfo = DeviceInfo()

def settingDumpSizeParsing(dumpsys, deviceInfo) :
    for k in range( len(dumpsys) ) :
        if settingDeviceParsing(dumpsys[k], deviceInfo) == True :
            return

"""
"init=1080x1920 480dpi cur=1080x1920 app=1080x1776 rng=1080x1008-1776x1704"
해당 형식으로 된 내용을 분해하여 저장
dumpsys window를 통해 받은 내용에서
init, cur, app의 크기를 받음
"""
def settingDeviceParsing(line, deviceInfo) :
    if line.find("init=") != -1 :
        print line
        tempSizeList = line.strip().split()
        if len(tempSizeList) < 4 :
            return False
        strSize = tempSizeList[0][tempSizeList[0].find("=") + 1 : ]
        deviceInfo.setInitSizeParsing(strSize)
            
        deviceInfo.setDpiParsing(tempSizeList[1])

        strSize = tempSizeList[2][tempSizeList[2].find("=") + 1 : ]
        deviceInfo.setCurSizeParsing(strSize)

        strSize = tempSizeList[3][tempSizeList[3].find("=") + 1 : ]
        deviceInfo.setAppSizeParsing(strSize)
        deviceInfo.prints()
        return True
    return False

start_deviceInfo = True
def settingDeviceInfo(deviceInfo, deviceName="") :
    print "getDeviceInfo()"
    adb = "adb -d "
    if deviceName != "" :
        adb = "adb -s " + deviceName + " "
    wmSize = RunProcessOut(adb + "shell wm size")
    settingWmSizeParsing(wmSize, deviceInfo)
    currentDumpsys = RunProcessOut(adb + "shell dumpsys window")
    settingDumpSizeParsing(currentDumpsys, deviceInfo)

def settingWmSizeParsing(wmSize, deviceInfo) :
    #['Physical size: 1440x2560\n', 'Override size: 1080x1920\n']
    #['Physical size: 1080x1920\r\n']
    wmSize = wmSize[-1].split()[-1].strip()
    deviceInfo.setWmSizeParsing(wmSize)




if __name__ == "__main__":
    apkFile = "/Users/numa/bonaria.apk"
    mecroFile = "/Users/numa/rec.txt"

#테스트할땐 무시
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
    """

    #RunProcessWait(currentFilePath + "/autoApkRun.py " + apkFile)
    settingDeviceInfo(deviceInfo=recDeviceInfo)

    getEventThread = threading.Thread( target=getEventADB, args=() )
    getEventThread.daemon = True
    getEventThread.start()
    time.sleep(1)
    activityThread = threading.Thread( target=getActivity, args=() )
    activityThread.daemon = True
    activityThread.start()
    time.sleep(1)
    managerThread = threading.Thread( target=manager, args=() )
    managerThread.start()
    print "!!!!!!!REC Running!!!!!!!"


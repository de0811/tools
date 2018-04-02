#!/usr/bin/python
#-*-coding:utf-8-*-

import sys
import threading
from collections import deque #Queue
from lib.androidinfo import *

print ("autoRec.py runing")

currentFilePath = os.path.dirname(os.path.realpath(__file__))
mainDir = dirName = currentFilePath + os.sep + ".." + os.sep + "temp"
deviceDirPath = ""

appX = 0
appY = 0

#해상도 size : adb shell wm size
#터치 : adb shell input tap x y
#드래그 : adb shell input swipe x1 y1 x2 y2
#문자 입력 : adb shell input text 'text'
#특정 키 입력 : adb shell input keyevent '4'

class Timer :
    begin = 0
    end = 0
    def __init__(self) :
        begin = 0
        end = 0
    def startTime(self) :
        self.begin = time.clock()
    def endTime(self) :
        self.end = time.clock()
    def result(self) :
        return self.end - self.begin
    def __repr__(self) :
        return self.end - self.begin

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
    print "END getEventADB()"

def eventRec() :
    print "start eventRec()"
    mergeEvent = list()
    deviceStates = list()
    keywordTimer = Timer()
    keywordTimer.startTime()
    uniq = 0
    start_event = False
    sourceEvent = list()
    deviceInfo = DeviceInfo("")

    start_eventRec = True
    while start_eventRec == True or len(dequeEvent) > 0 :
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
                    start_eventRec = False
                    del mergeEvent
                    mergeEvent = list()
                    break
                #device정보 관련
                elif tempE.startswith("add device") or tempE.startswith("  name:") :
                    deviceStates.append("AddDeviceState::" + tempE)
                #이벤트라면
                elif tempE.startswith("[  ") :
                    if start_event == False :
                        deviceInfo.parsingDeviceEvent(deviceStates)
                    keywordTimer.startTime()
                    spl = tempE.split()
                    #if spl[3] == "0003" and spl[4] == "0039" and spl[5] != "ffffffff" :
                    if spl[3] == "0000" and spl[4] == "0000" and spl[5] == "00000000" :
                        del mergeEvent
                        mergeEvent = list()
                        continue
                    sourceEvent.append((uniq, tempE))
                    if spl[3] == "0003" and spl[4] == "0039" and spl[5] == "ffffffff" :
                        uniq = uniq + 1
                else :
                    keywordTimer.endTime()
                    sourceEvent.append((uniq, "KeyWord::" + str(keywordTimer.result()) + ":" + tempE))
                    uniq = uniq + 1
                del mergeEvent
                mergeEvent = list()
            else :
                mergeEvent.append( tempE )

    #mecro = open(mecroFile, 'w')

    """init=1080x1920 480dpi cur=1080x1920 app=1080x1776 rng=1080x1008-1776x1704"""
    '''
    for even in endEvent :
        print str(even)
        mecro.write(even + "\n")
    '''
    #mecro.close()
    return sourceEvent

class EventCmd :
    event = str()
    msg = str()
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    ratio_x1 = 0.0
    ratio_y1 = 0.0
    ratio_x2 = 0.0
    ratio_y2 = 0.0
    full_ratio_x1 = 0.0
    full_ratio_y1 = 0.0
    full_ratio_x2 = 0.0
    full_ratio_y2 = 0.0
    delayTime = 0.0 #해당 이벤트가 실행될때까지의 지연시간
    runTime = 0.0 #이벤트가 진행되는 시간
    def __init__(self, event, msg, x1, y1, x2, y2, ratio_x1, ratio_y1, ratio_x2, ratio_y2, full_ratio_x1, full_ratio_y1, full_ratio_x2, full_ratio_y2, delayTime, runTime) :
        self.event = event
        self.msg = msg
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.ratio_x1 = ratio_x1
        self.ratio_y1 = ratio_y1
        self.ratio_x2 = ratio_x2
        self.ratio_y2 = ratio_y2
        self.full_ratio_x1 = full_ratio_x1
        self.full_ratio_y1 = full_ratio_y1
        self.full_ratio_x2 = full_ratio_x2
        self.full_ratio_y2 = full_ratio_y2
        self.delayTime = delayTime
        self.runTime = runTime
    def prints(self) :
        print "*" * 30 + "EventCmd" + "*" * 30
        print "event : " + self.event
        print "msg : " + self.msg
        print "x1 : " + str(self.x1) + "  y1 : " + str(self.y1) + "  x2 : " + str(self.x2) + "  y2 : " + str(self.y2)
        print "ratio_x1 : " + str(self.ratio_x1) + "  ratio_y1 : " + str(self.ratio_y1) + "  ratio_x2 : " + str(self.ratio_x2) + "  ratio_y2 : " + str(self.ratio_y2)
        print "full_ratio_x1 : " + str(self.full_ratio_x1) + "  full_ratio_y1 : " + str(self.full_ratio_y1) + "  full_ratio_x2 : " + str(self.full_ratio_x2) + "  full_ratio_y2 : " + str(self.full_ratio_y2)
        print "delayTime : " + str(self.delayTime)
        print "runTime : " + str(self.runTime)
        print "*" * 67

def parsingSourceEvent(sourceEvent) :
    eventCmds = list()
    xs = list()
    ys = list()
    uniq = -1
    preTime = 0.0
    curTime = 0.0
    delayTime = 0.0
    for sou in sourceEvent :
        #print "Uniq[" + str(sou[0]) + "]  " + sou[1]
        if sou[1].find("KeyWord::") != -1 :
            preTime = 0.0
            tt = sou[1].split("::")[1].split(":")
            delayTime = tt[0]
            delayTime = float(delayTime)
            eventCmds.append(EventCmd("keyword", tt[1], 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, delayTime, 0.0))
            continue
        spl = sou[1].split()
        if len(spl) != 6 :
            print "Error ! "
            print sou[1]
            return
        if spl[3] == "0003" and spl[4] == "0035" :
            xs.append(int(spl[5], 16))
        elif spl[3] == "0003" and spl[4] == "0036" :
            ys.append(int(spl[5], 16))
        elif spl[3] == "0003" and spl[4] == "0039" and spl[5] != "ffffffff" :
            curTime = float(spl[1][:-1])
            #print "preTime : " + str(preTime)
            #print "currentTime : " + str(curTime)
        elif spl[3] == "0003" and spl[4] == "0039" and spl[5] == "ffffffff" :
            if preTime == 0.0 :
                delayTime = 0.5
            else :
                delayTime = curTime - preTime

            runTime = float(spl[1][:-1])
            runTime = runTime - preTime

            if len(xs) < 1 or len(ys) < 1 :
                print "ERROR !!!!!"
                continue
            if xs[0] == xs[-1] and ys[0] == ys[-1] :    #tap
                eventCmds.append( EventCmd("event", "tap", xs[0], ys[0], xs[-1], ys[-1], 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, delayTime, 0.0) )
            else : #swip
                runTime = ( float(spl[1][:-1])-curTime ) * 1000  
                eventCmds.append( EventCmd("event", "swipe", xs[0], ys[0], xs[-1], ys[-1], 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, delayTime, int(runTime)) )
            preTime = float(spl[1][:-1])
            del xs, ys
            xs = list()
            ys = list()
    for cmd in eventCmds :
        cmd.prints()
    return eventCmds

def reUIRec(device="", eventCmds=list()) :
    adb = "adb -d "
    if device != "" :
        adb = "adb -s " + device + " "
    deviceInfo = DeviceInfo(device)
    fx, fy = deviceInfo.getWmSize()
    uiEvents = list()
    for cmd in eventCmds :
        time.sleep(cmd.delayTime)
        #currentDumpsys = RunProcessOut("adb shell dumpsys window")
        #mFocused = getCurrentFocused(currentDumpsys)
        currentDumpsys = DumpsysWindow(device)
        mFocused = currentDumpsys.mFocused
        windowState = windowPointParsing(device, fx, fy)
        objGroup = windowState[0]
        clickableTree = windowState[1]
        if cmd.event == "keyword" :
            pass
        elif cmd.event == "event" :
            if cmd.msg == "tap" :
                RunProcess(adb + "shell input tap " + str(cmd.x1) + " " + str(cmd.y1))
            elif cmd.msg == "swipe" :
                RunProcess(adb + "shell input swipe " + str(cmd.x1) + " " + str(cmd.y1) + " " + str(cmd.x2) + " " + str(cmd.y2) + " " + str(cmd.runTime))
        uiEvents.append((objGroup, clickableTree, cmd, mFocused))

    
    time.sleep(5)

    objEvent = list() #[ObjGroup, clickableTree, Event, mFocused]
    for ue in uiEvents :
        #print " "
        #objGroupPrints(ue[0])
        #ue[2].prints()
        print " "
        if ue[2].msg == "tap" :
            cNames = isBoxObjName(ue[0], ue[2].x1, ue[2].y1, ue[2].x1, ue[2].y1)
        elif ue[2].msg == "swipe" :
            cNames = isBoxObjName(ue[0], ue[2].x1, ue[2].y1, ue[2].x2, ue[2].y2)
        if cNames[1] == None :
            print "Error Data Type cNames[1]"
            return
        cNames = cNames[1]

        #버튼 정보 입력
        strClick = isClickableCollisionName(ue[1], ue[2].x1, ue[2].y1, ue[2].x2, ue[2].y2)
        objEvent.append( (cNames, ue[2], strClick, ue[3]) )


        #위치 정보를 배율로 저장
        obj = searchObjName(ue[0], cNames, 0)
        if obj != None :
            #print "*Find Obj*"
            #obj.prints()
            ue[2].ratio_x1 = float(ue[2].x1 - obj.x1) / float(obj.x2 - obj.x1)
            ue[2].ratio_y1 = float(ue[2].y1 - obj.y1) / float(obj.y2 - obj.y1)
            ue[2].ratio_x2 = float(ue[2].x2 - obj.x1) / float(obj.x2 - obj.x1)
            ue[2].ratio_y2 = float(ue[2].y2 - obj.y1) / float(obj.y2 - obj.y1)
            #print ue[2].prints()
        #앱의 최대 크기에서 배율로 저장
        nameListTemp = list()
        for name in cNames.split(":::") :
            nameListTemp.append(name)
            if name == "" :
                continue
            else :
                obj = searchObjName(ue[0], ":::".join(nameListTemp), 0)
                if obj != None :
                    #print "*" * 30 + "*Find Full Obj*" + "*" * 30
                    #print "FIND? FULL NAME : " + cNames
                    #print "FIND NAME : " + name
                    #objGroupPrints(ue[0])
                    #obj.prints()
                    #print "*" * 73
                    ue[2].full_ratio_x1 = float(ue[2].x1 - obj.x1) / float(obj.x2 - obj.x1)
                    ue[2].full_ratio_y1 = float(ue[2].y1 - obj.y1) / float(obj.y2 - obj.y1)
                    ue[2].full_ratio_x2 = float(ue[2].x2 - obj.x1) / float(obj.x2 - obj.x1)
                    ue[2].full_ratio_y2 = float(ue[2].y2 - obj.y1) / float(obj.y2 - obj.y1)
                    #print ue[2].prints()
                    break


    mecro = open(mecroFile, 'w')
    mecro.write( ":" + " " + "devicestate" + ":::" + "devicesize" + ":::" + \
        str(fx) + ":::" + str(fy) + ":::" + str(fx) + ":::" + str(fy) + ":::" + \
        "0.0:::0.0:::0.0:::0.0:::" + \
        "0.0:::0.0:::0.0:::0.0:::" + \
        str(0.0) + ":::" + str(0.0) + \
        " " +\
        "-" +\
        " " +\
        "-" +\
        " " +\
        "-" +\
        "\n" )
    for oe in objEvent :
        mecro.write( oe[0] + " " + oe[1].event + ":::" + oe[1].msg + ":::" + \
            str(oe[1].x1) + ":::" + str(oe[1].y1) + ":::" + str(oe[1].x2) + ":::" + str(oe[1].y2) + ":::" + \
            str(oe[1].ratio_x1) + ":::" + str(oe[1].ratio_y1) + ":::" + str(oe[1].ratio_x2) + ":::" + str(oe[1].ratio_y2) + ":::" + \
            str(oe[1].full_ratio_x1) + ":::" + str(oe[1].full_ratio_y1) + ":::" + str(oe[1].full_ratio_x2) + ":::" + str(oe[1].full_ratio_y2) + ":::" + \
            str(oe[1].delayTime) + ":::" + str(oe[1].runTime) + \
            " " + \
            oe[3] + \
            " " + \
            oe[2][0] + \
            " " + \
            oe[2][1] + \
           "\n" )
    mecro.close()

def getLoadEvent(recFile) :
    loadEvent = list()
    rec = open(recFile, 'r')
    while True:
        line = rec.readline()
        if not line: break
        line = line.strip()
        line = line.split(" ")
        eventLine = line[1].split(":::")
        upper = ""
        under = ""
        mFocused = line[2]
        if len(line) == 5 :
            upper = line[3]
            under = line[4]
        print eventLine
        ecmd = EventCmd( event=eventLine[0], msg=eventLine[1], \
        x1=int(eventLine[2]), y1=int(eventLine[3]), x2=int(eventLine[4]), y2=int(eventLine[5]), \
        ratio_x1=float(eventLine[6]), ratio_y1=float(eventLine[7]), ratio_x2=float(eventLine[8]), ratio_y2=float(eventLine[9]), \
        full_ratio_x1=float(eventLine[10]), full_ratio_y1=float(eventLine[11]), full_ratio_x2=float(eventLine[12]), full_ratio_y2=float(eventLine[13]), \
        delayTime=float(eventLine[14]), runTime=float(eventLine[15]) )

        loadEvent.append( (line[0], ecmd, mFocused, (upper, under)) )
    rec.close()

    return loadEvent

def playEvent(device="", apk="", loadEvent=list()) :
    adb = "adb -d "
    if device != "" :
        adb = "adb -s " + device + " "
        deviceDirPath = mainDir + os.sep + device
        if not os.path.isdir(mainDir) :
            os.mkdir(mainDir)

        if not os.path.isdir(deviceDirPath) :
            os.mkdir(deviceDirPath)

    RunProcessWait("python " + currentFilePath + os.sep + "autoApk.py " + apk + " " + device)
    time.sleep(5)
    deviceInfo = DeviceInfo(device)
    cfx, cfy = deviceInfo.getWmSize()
    print "[" + device + "]  FullScreen X : " + str(cfx) + "x" + str(cfy)
    rfx = 0
    rfy = 0
    for cmd in loadEvent :
        time.sleep(cmd[1].delayTime) 

        if cmd[1].event == "devicestate" :
            if cmd[1].msg == "devicesize" : 
                rfx = int(cmd[1].x1)
                rfy = int(cmd[1].y1)
                print "REC FullScreen X : " + str(rfx) + "  Y : " + str(rfy)
                if cfx < rfx or cfy < rfy :
                    RunProcessWait(adb + "shell wm size " + str(rfx) + "x" + str(rfy))
                    print "screen size change"
        if cmd[1].event == "keyword" :
            RunProcessWait("python " + currentFilePath + "/screencap.py -d " + device + " -o " + deviceDirPath + " -f info.png")
        elif cmd[1].event == "event" :
            sens = False
            windowState = windowPointParsing(device, rfx, rfy)
            objGroup = windowState[0]
            clickableTree = windowState[1]
            print " "
            print cmd[0]
            mFocused = ""
            mFocusedCount = 0
            while cmd[2] != mFocused :
                #currentDumpsys = RunProcessOut("adb shell dumpsys window")
                #mFocused = getCurrentFocused(currentDumpsys)
                currentDumpsys = DumpsysWindow(device)
                if currentDumpsys.isFocusedError() :
                    RunProcessWait("python " + currentFilePath + "/screencap.py -d " + device + " -o " + deviceDirPath + " -f error.png")
                    return
                mFocused = currentDumpsys.mFocused
                if cmd[2] != mFocused :
                    time.sleep("0.2")
                    mFocusedCount = mFocusedCount + 1
                else :
                    break
                if mFocusedCount == 10 :
                    RunProcessWait("python " + currentFilePath + "/screencap.py -d " + device + " -o " + deviceDirPath + " -f error.png")
                    print "!!!! mFoucsed Error !!!!"
                    print "mFcoused : " + mFocused
                    return
            objGroupPrints(objGroup)
            obj = searchObjName(objGroup, cmd[0], 0)
            #obj = None #seachClick 테스트를 위해서 임시로 막음
            for diffCount in range(7) :
                if obj == None :
                    if diffCount == 3 :
                        if len(cmd[3]) != 2 :
                            continue
                        #clickableTree관련 작업은 여기서 해야함
                        windowState = windowPointParsing(device, rfx, rfy)
                        objGroup = windowState[0]
                        clickableTree = windowState[1]

                        obj = searchClickObj(clickableTree, cmd[3][0], cmd[3][1])
                        print "!" * 50 + "searchClickObj Result" + "!" * 50
                        if obj != None :
                            obj.prints()
                        else :
                            #return 
                            pass
                        print "!" * 120
                        break
                    if diffCount == 4 :
                        RunProcessWait("python " + currentFilePath + "/screencap.py -d " + device + " -o " + deviceDirPath + " -f warning.png")
                        tempFind = cmd[0]
                        windowState = windowPointParsing(device, rfx, rfy)
                        objGroup = windowState[0]
                        clickableTree = windowState[1]
                        tempFind = tempFind.split(":::")
                        #print tempFind
                        ttt = list()
                        for tem in tempFind :
                            ttt.append(tem)
                            if tem != "" :
                                break
                        obj = searchObjName(objGroup, ":::".join(ttt), 0)
                        sens = obj != None
                        if sens == True :
                            break
                    if diffCount == 5 :
                        RunProcessWait("python " + currentFilePath + "/screencap.py -d " + device + " -o " + deviceDirPath + " -f error.png")
                    time.sleep(1)
                    windowState = windowPointParsing(device, rfx, rfy)
                    objGroup = windowState[0]
                    clickableTree = windowState[1]

                    obj = searchObjName(objGroup, cmd[0], 0)
                    #obj = None #seachClick 테스트를 위해서 임시로 막음
            if sens == True :
                print "@" * 50 + "SENS ON" + "@" * 50
                print "obj searchObjName Not Found Sens Obj Found"
                print "@" * 105
                x1 = int( ((obj.x2 - obj.x1) * cmd[1].full_ratio_x1) + obj.x1 )
                y1 = int( ((obj.y2 - obj.y1) * cmd[1].full_ratio_y1) + obj.y1 )
                x2 = int( ((obj.x2 - obj.x1) * cmd[1].full_ratio_x2) + obj.x1 )
                y2 = int( ((obj.y2 - obj.y1) * cmd[1].full_ratio_y2) + obj.y1 )
                cmd[1].runTime = int( cmd[1].runTime )
                obj.prints()
                cmd[1].prints()
                sens = False
            elif obj == None :
                print "@" * 50 + "NOT FOUND OBJ" + "@"
                x1 = cmd[1].x1
                y1 = cmd[1].y1
                x2 = cmd[1].x2
                y2 = cmd[1].y2
                cmd[1].runTime = int( cmd[1].runTime )
                cmd[1].prints()
                print "@" * 113
            else :
                obj.prints()
                x1 = int( ((obj.x2 - obj.x1) * cmd[1].ratio_x1) + obj.x1 )
                y1 = int( ((obj.y2 - obj.y1) * cmd[1].ratio_y1) + obj.y1 )
                x2 = int( ((obj.x2 - obj.x1) * cmd[1].ratio_x2) + obj.x1 )
                y2 = int( ((obj.y2 - obj.y1) * cmd[1].ratio_y2) + obj.y1 )
                cmd[1].runTime = int( cmd[1].runTime )
                cmd[1].prints()
            print " "
            print " "
  
            if cmd[1].msg == "tap" :
                RunProcess(adb + "shell input tap " + str(x1) + " " + str(y1))
            elif cmd[1].msg == "swipe" :
                RunProcess(adb + "shell input swipe " + str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + " " + str(int(cmd[1].runTime)))
    
    time.sleep(5)
    RunProcessWait(adb + "shell wm size " + str(cfx) + "x" + str(cfy))

if __name__ == "__main__":
    #apkFile = "/Users/numa/testapp.apk"
    apkFile = "c:\\temp\\autotest\\testapp.apk"
    #mecroFile = "/Users/numa/rec.txt"
    mecroFile = "c:\\temp\\autotest\\rec.txt"
    deviceInfo = DeviceInfo("")
    appX, appY = deviceInfo.getWmSize()

#테스트할땐 무시
    args = sys.argv[1:]
    print args
    if not args:
        print 'Not Command'
        sys.exit()
    for arg in args :
        if arg.endswith("-h") == True :
            helps = u'''
            매크로 파일인 .txt 파일과 APK파일인 .apk 스크린샷을 받을 위치의 path를 넣어주시면 됩니다.
            순서는 상관 없습니다.
            '''
            print helps
        if arg.endswith(".apk") == True :
            apkFile = arg
        elif arg.endswith(".txt") == True :
            mecroFile = arg

    #RunProcessWait(currentFilePath + "/autoApk.py " + apkFile)
    RunProcessWait("python " + currentFilePath + os.sep + "autoApk.py " + apkFile)
    currentDumpsys = DumpsysWindow("")
    if currentDumpsys.isFocusedError() :
        print "Error DumpsysWindow : " + currentDumpsys.mFocused
        sys.exit()

    getEventThread = threading.Thread( target=getEventADB, args=() )
    getEventThread.daemon = True
    getEventThread.start()
    time.sleep(5)
    sourceEvent = eventRec()

    #RunProcessWait(currentFilePath + "/autoApk.py " + apkFile)
    RunProcessWait("python " + currentFilePath + os.sep + "autoApk.py " + apkFile)
    currentDumpsys.setupDumpsysWindow()
    if currentDumpsys.isFocusedError() :
        print "Error DumpsysWindow : " + currentDumpsys.mFocused
        sys.exit()

    time.sleep(5)
    eventCmds = parsingSourceEvent(sourceEvent)
    reUIRec("", eventCmds)
    
    time.sleep(3)
    print "*" * 50 + "END" + "*" * 50
    sys.exit()

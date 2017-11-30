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
mainDir = dirName = currentFilePath + "/../temp"
deviceDirPath = ""

appX = 0
appY = 0

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

def RunProcessPipe(cmd):
    pi = open(currentFilePath + "/temp.txt", 'w')
    cmd_args = cmd.split()
    process = Popen(cmd_args, stdout=pi, stderr=pi)
    pi.close()

def RunProcessOut(cmd):
    cmd_args = cmd.split()
    pipe = Popen(cmd_args, stdout=PIPE, stderr=STDOUT)
    outList = pipe.stdout.readlines()
    return outList

def RunProcessWait(cmd):
    #print cmd
    cmd_args = cmd.split()
    process = Popen(cmd_args)
    while process.poll() is None:
        pass
    #print process.poll()
def RunProcessPipeWait(cmd):
    pi = open(currentFilePath + "/temp.txt", 'w')
    cmd_args = cmd.split()
    process = Popen(cmd_args, stdout=pi, stderr=pi)
    while process.poll() is None:
        time.sleep(0.1)
        pass
    pi.close()

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

class OBJ :
    idx = ""
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    resource_id = ""
    cName = ""
    clickable = False
    def __init__(self, idx, resource_id, cName, clickable, x1, y1, x2, y2) :
        self.idx = idx
        self.cName = cName
        self.resource_id = resource_id
        self.clickable = clickable
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    def prints(self) :
        print " " * 50 + "OBJ" + " " * 50
        print "idx : " + self.idx
        print "Class : " + self.cName
        print "resource_id : " + self.resource_id
        print "clickable : " + str(self.clickable)
        print "x1[" + str(self.x1) + "]  " + "y1[" + str(self.y1) + "]  " + "x2[" + str(self.x2) + "]  " + "y2[" + str(self.y2) + "]"
        print " " * 103

class OBJGroup :
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    level = 0
    objList = list()
    groupDown = list()
    def __init__(self, level, x1, y1, x2, y2, objList, groupDown) :
        self.level = level
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.objList = objList
        self.groupDown = groupDown
    def prints(self) :
        print " " * 50 + "OBJGROUP" + " " * 50
        print "x1[" + str(self.x1) + "]  " + "y1[" + str(self.y1) + "]  " + "x2[" + str(self.x2) + "]  " + "y2[" + str(self.y2) + "]"
        print "objList Size : " + str(len(self.objList))
        print "GroupDown Size : " + str(len(self.groupDown))
        print " " * 108

def objGroupLeveling(objGroup, obj) :
    if objGroup.x1 == obj.x1 and objGroup.y1 == obj.y1 and objGroup.x2 == obj.x2 and objGroup.y2 == obj.y2 :
        objGroup.objList.append(obj)
        return True
    elif isBoxCollision(objGroup.x1, objGroup.y1, objGroup.x2, objGroup.y2, obj.x1, obj.y1) and isBoxCollision(objGroup.x1, objGroup.y1, objGroup.x2, objGroup.y2, obj.x2, obj.y2) :
        for _og in objGroup.groupDown :
            if objGroupLeveling(_og, obj) == True :
                return True
        group = OBJGroup(objGroup.level + 1, obj.x1, obj.y1, obj.x2, obj.y2, list(), list())
        group.objList.append(obj)
        objGroup.groupDown.append(group)
        return True
 
    else :
        return False

"""
일단 정확히 맞는 오브젝트가 없다면 포함되는 오브젝트의 이름들만 일단 반환
반환 값의 앞 인자는 완벽히 같은 인자를 찾았다는 뜻
두번째는 일단 포함하는 모든 인자의 이름
"""
def isBoxObjName(objGroup, x1, y1, x2, y2) :
    meCName = str()
    nameList = list()
    for obj in objGroup.objList :
        nameList.append(obj.idx + ":" + obj.cName)
    meCName = "::".join(nameList)
    if objGroup.x1 == x1 and objGroup.y1 == y1 and objGroup.x2 == x2 and objGroup.y2 == y2 :
        return (True, meCName)
    elif isBoxCollision(objGroup.x1, objGroup.y1, objGroup.x2, objGroup.y2, x1, y1) and isBoxCollision(objGroup.x1, objGroup.y1, objGroup.x2, objGroup.y2, x2, y2) :
        for _og in objGroup.groupDown :
            tu = isBoxObjName(_og, x1, y1, x2, y2)
            if tu[1] != None :
                meCName = meCName + ":::" + tu[1]
                return (True, meCName)
        return (True, meCName)
    else :
        return (False, None)

"""
objGroup : 오브젝트 묶음
cNames : REC에서 나온 특정 오브젝트 트리 라인
level : 무조건 최초에는 0으로 입력
sens_level_idx : 해당 값 이상은 idx값의 검사를 제외
"""
def searchObjName(objGroup, cNames, level) :
    if type(cNames) != type(str()) :
        return None
    levelList = cNames.split(":::")
    if len(levelList) -1 < level :
        return None
    if levelList[level] == "" and len(objGroup.objList) > 0 :
        level = level + 1

    if len(levelList) -1 == level :
        for obj in objGroup.objList :
            print "-" * 30 + "FIND-LAST-PANG-OBJ" + "-" * 30
            print "LEVEL[" + str(level) + "]"
            print "levelList : " + levelList[level]
            print "obj : " + obj.idx + ":" + obj.cName
            print "-" * 68
            if levelList[level].find(obj.idx + ":" + obj.cName) != -1 :
                return obj

    for obj in objGroup.objList :
        print "-" * 30 + "FIND-OBJ" + "-" * 30
        print "LEVEL[" + str(level) + "]"
        print "levelList : " + levelList[level]
        print "obj : " + obj.idx + ":" + obj.cName
        print "-" * 68
        if levelList[level].find(obj.idx + ":" + obj.cName) == -1 :
            return None

    for _og in objGroup.groupDown :
        obj = searchObjName(_og, cNames, level+1)
        if obj != None :
            return obj
    return None
    


def objGroupPrints(objGroup) :
    print "--" * objGroup.level + "x1[" + str(objGroup.x1) + "] " + "y1[" + str(objGroup.y1) + "] " + "x2[" + str(objGroup.x2) + "] " + "y2[" + str(objGroup.y2) + "] " 
    objName = list()
    for obj in objGroup.objList :
        objName.append(str(obj.idx) + ":" + obj.cName)
    print "   " * objGroup.level + " L " + "::".join(objName)
    for _og in objGroup.groupDown :
        objGroupPrints(_og)

def getWmSize(device="") :
    adb = "adb -d "
    if device != "" :
        adb = "adb -s " + device + " "
    strWM = RunProcessOut(adb + "shell wm size")
    print strWM
    '''
    Physical size: 1440x2560
    Override size: 1080x1920
    '''
    print strWM[-1]
    strWM = strWM[-1].strip().split(" ")
    strWM = strWM[-1].split("x")
    print strWM
    fx = int(strWM[0])
    fy = int(strWM[1])
    return fx, fy


def currentAppSize() :
    #app Size 미리 계산해놔야함
    dumpsys = RunProcessOut("adb shell dumpsys window")
    for dump in dumpsys :
        if dump.find("init=") != -1 :
            if dump.find("app=") != -1 :
                dumpsys = dump
                break

    dumpsys = dumpsys.split()
    strAppSize = 0
    for dump in dumpsys :
        if dump.startswith("app=") == True :
            strAppSize = dump[dump.find("=")+1:]
    print strAppSize
    appX = strAppSize.split("x")[0]
    appY = strAppSize.split("x")[1]
    print "APP SIZE ... X : " + str(appX) + "  Y : " + str(appY)
    return appX, appY

def appendClickableTree(clickableTree, click) :
    if len(clickableTree) > 0 :
        for tree in clickableTree :
            for leaf in tree :
                if leaf.y1 == click.y1 :
                    tree.append(click)
                    return clickableTree
    else :
        clickableTree.append(list())
        clickableTree[0].append(click)
        return clickableTree

    tempList = list()
    clickableTree.append(tempList)
    tempList.append(click)

    return clickableTree

def getClickableTree(clickableList) :
    #clickable을 중심으로 화면 구성 상태 분석
    #y축을 기준으로 정렬
    print "$" * 50 + "ClickableList" + "$" * 50
    clickableTree = list()
    clickableList.sort(key=lambda k : k.y1)
    for click in clickableList :
        click.prints()
        clickableTree = appendClickableTree(clickableTree, click)
    print "$" * 110
    return clickableTree

def orderClickableTree(clickableTree) :
    for clickableList in clickableTree :
        clickableList.sort(key=lambda k : k.x1)
    return clickableTree

def printsClickableTree(clickableTree) :
    print "#" * 50 + "ROOT" + "#" * 50
    for clickableList in clickableTree :
        print "-" * 50 + "STEM" + "-" * 50
        for leaf in clickableList :
            print leaf.prints()
        print "-" * 104
    print "#" * 104

def isClickableCollision(clickableTree, x1, y1, x2, y2) :
    if len(clickableTree) <= 0 :
        return None
    for stem in clickableTree :
        for leaf in stem :
            if isBoxCollision(leaf.x1, leaf.y1, leaf.x2, leaf.y2, x1, y1) and isBoxCollision(leaf.x1, leaf.y1, leaf.x2, leaf.y2, x2, y2) :
                return leaf
    return None

def __clickableTreeNameuu(clickableTree, target, uper) :
    result = ""
    stemList = list()
    if uper == True :
        for stem in clickableTree :
            leafList = list()
            for leaf in stem :
                leafList.append( leaf.resource_id + "::" + leaf.cName )
                if target == leaf :
                    if len( leafList ) > 0 :
                        stemList.append(":::".join(leafList))
                    return "::::".join(stemList)
            stemList.append(":::".join(leafList))
    else :
        for k in reversed( range( len(clickableTree) ) ) :
            leafList = list()
            for j in reversed( range( len(clickableTree[k]) ) ) :
                leafList.append( clickableTree[k][j].resource_id + "::" + clickableTree[k][j].cName )
                if target == clickableTree[k][j] :
                    if len( leafList ) > 0 :
                        stemList.append(":::".join(leafList))
                    return "::::".join(stemList)
            stemList.append(":::".join(leafList))

    return ""

def isClickableCollisionName(clickableTree, x1, y1, x2, y2) :
    target = isClickableCollision(clickableTree, x1, y1, x2, y2)
    if target == None :
        return ("", "")
    print "*" * 50 + "CLICK_TARGET" + "*" * 50
    target.prints()
    print "*" * 111
    printsClickableTree(clickableTree)
    uper = __clickableTreeNameuu(clickableTree, target, True)
    under = __clickableTreeNameuu(clickableTree, target, False)
    print "*" * 50 + "UPER" + "*" * 50
    print uper
    print "*" * 105
    print "*" * 50 + "UNDER" + "*" * 50
    print under
    print "*" * 105
    
    return (uper, under)

def __getClickFullName(clickableTree, uper) :
    if len(clickableTree) <= 0 :
        return False
    stemList = list()
    result = ""
    if uper == True :
        for stem in clickableTree :
            leafList = list()
            for leaf in stem :
                leafList.append( leaf.resource_id + "::" + leaf.cName )
            stemList.append(":::".join(leafList))
    else :
        for k in reversed( range( len(clickableTree) ) ) :
            leafList = list()
            for j in reversed( range( len(clickableTree[k]) ) ) :
                leafList.append( clickableTree[k][j].resource_id + "::" + clickableTree[k][j].cName )
            stemList.append(":::".join(leafList))
    return "::::".join(stemList)

def __searchClickObj(clickableTree, nameList, upper) :
    rstemList = list()
    if nameList.find("::::") == -1 :
        rstemList.append(nameList)
    else :
        rstemList = nameList.split("::::")

    if upper == True :
        maxrStem = len(rstemList)
        maxoStem = len(clickableTree)
        tempPoints = list()#찾은 위치 저장
        trueCount = 0
        if maxrStem <= 0 or maxoStem <= 0 :
            return None
        maxTrueCount = 0
        for rstem in rstemList :
            maxTrueCount = len(rstem.split(":::")) + maxTrueCount
        rstem = 0
        ostem = 0
        reList = list()
        while True :
            maxoLeaf = len(clickableTree[ostem])
            oLeaf = 0
            while True :
                tempStr = clickableTree[ostem][oLeaf].resource_id + "::" + clickableTree[ostem][oLeaf].cName
                if rstemList[rstem].find( tempStr ) != -1 :
                    if trueCount == 0 :
                        tempPoints.append( (ostem,oLeaf) )
                    trueCount = trueCount + 1
                    if trueCount >= maxTrueCount :
                        return clickableTree[ostem][oLeaf]
                else :
                    rstem = 0
                    if trueCount > 0 :
                        trueCount = 0
                        rstem = 0
                        ostem = tempPoints[-1][0]
                        oLeaf = tempPoints[-1][1] + 1
                        if len(clickableTree[ostem]) <= oLeaf :
                            if maxoStem <= ostem + 1 :
                                return None
                            ostem = ostem + 1
                            oLeaf = 0
                            maxoLeaf = len(clickableTree[ostem])
                if maxoLeaf <= oLeaf + 1 :
                    break
                oLeaf = oLeaf + 1
            if trueCount > 0 :
                rstem = rstem + 1
                print "COUNT UP : " + str(trueCount) + "   rstem : " + str(rstem) + "   maxrStem : " + str(maxrStem)
            if maxoStem <= ostem + 1 :
                break
            ostem = ostem + 1
        return None
    else :
        maxrStem = len(rstemList)
        maxoStem = 0
        tempPoints = list()#찾은 위치 저장
        trueCount = 0
        if maxrStem <= 0 or len(clickableTree) <= 0 :
            return None
        maxTrueCount = 0
        for rstem in rstemList :
            maxTrueCount = len(rstem.split(":::")) + maxTrueCount
        print "maxTrueCount : " + str(maxTrueCount)
        rstem = 0
        ostem = len(clickableTree) - 1
        reList = list()
        while True :
            maxoLeaf = 0
            oLeaf = len(clickableTree[ostem]) - 1
            while True :
                tempStr = clickableTree[ostem][oLeaf].resource_id + "::" + clickableTree[ostem][oLeaf].cName
                if rstemList[rstem].find( tempStr ) != -1 :
                    if trueCount == 0 :
                        tempPoints.append( (ostem,oLeaf) )
                    trueCount = trueCount + 1
                    if trueCount >= maxTrueCount :
                        print "trueCount ? : " + str(trueCount)
                        return clickableTree[ostem][oLeaf]
                else :
                    rstem = 0
                    if trueCount > 0 :
                        trueCount = 0
                        rstem = 0
                        ostem = tempPoints[-1][0]
                        oLeaf = tempPoints[-1][1] - 1
                        if maxoLeaf > oLeaf :
                            if maxoStem > ostem - 1 :
                                return None
                            ostem = ostem - 1
                            oLeaf = len(clickableTree[ostem]) - 1
                            maxoLeaf = 0
                if maxoLeaf > oLeaf - 1 :
                    break
                oLeaf = oLeaf - 1
            if trueCount > 0 :
                rstem = rstem + 1
            if maxoStem > ostem - 1 :
                break
            ostem = ostem - 1
        return None
 

        
           
#줄기의 부분을 검색하여 마지막 잎을 반환
def searchClickObj(clickableTree, upper, under) :
    print "UPPER : " + upper
    print "UNDER : " + under
    printsClickableTree(clickableTree)
    upperOBJ = __searchClickObj(clickableTree, upper, True)
    underOBJ = __searchClickObj(clickableTree, under, False)
    if upperOBJ == None and underOBJ == None :
        print "ClickOBJ ALL NONE"
        return None
    elif upperOBJ == None :
        print "ClickOBJ upperOBJ == None "
        return underOBJ
    elif underOBJ == None :
        print "ClickOBJ underOBJ == None "
        return upperOBJ

    if upperOBJ != underOBJ :
        print "ClickOBJ !="
        upperCount = 0
        underCount = 0
        upperNamel = upper.split("::::")
        underNamel = under.split("::::")
        for na in upperNamel :
            upperCount = len(na.split(":::")) + upperCount
        for na in underNamel :
            underCount = len(na.split(":::")) + underCount
        if max(upperCount, underCount) == upperCount :
            return upperOBJ
        else :
            return underOBJ
    else :
        print "ClickOBJ =="
        return underOBJ


#자체 분석 후 화면 상태를 반환
#첫번째는 화면의 구조를 반환, 두번째는 화면의 버튼을 반환
def windowPointParsing(device="", fx=0, fy=0) :
    #mecro = open(mecroFile, 'w')
    adb = "adb -d "
    if device != "" :
        adb = "adb -s " + device + " "
    RunProcessWait(adb + "shell uiautomator dump /sdcard/vivi.xml")
    #mecro.close()
    uiautoXML = RunProcessOut(adb + "shell cat /sdcard/vivi.xml")
    objList = list()
    clickableList = list()

    if len(uiautoXML) == 0 :
        return None
    uiautoXML = uiautoXML[0]
    print uiautoXML
    start = 0
    end = 0
    while True :
        start = start + uiautoXML[start:].find("index=")
        if uiautoXML[start:].find("index=") == -1 :
            break
        start = start + uiautoXML[start:].find("\"") + 1
        end = start + uiautoXML[start:].find("\"")
        if uiautoXML[start:].find("\"") == -1 :
            break
        idx = uiautoXML[start:end]
        start = end


        start = start + uiautoXML[start:].find("resource-id=")
        if uiautoXML[start:].find("resource-id=") == -1 :
            break
        start = start + uiautoXML[start:].find("\"") + 1
        end = start + uiautoXML[start:].find("\"")
        if uiautoXML[start:].find("\"") == -1 :
            break
        resource_id = uiautoXML[start:end]
        start = end

        
        start = start + uiautoXML[start:].find("class=")
        if uiautoXML[start:].find("class=") == -1 :
            break
        start = start + uiautoXML[start:].find("\"") + 1
        end = start + uiautoXML[start:].find("\"")
        if uiautoXML[start:].find("\"") == -1 :
            break
        cName = uiautoXML[start:end]
        start = end


        start = start + uiautoXML[start:].find("clickable=")
        if uiautoXML[start:].find("clickable=") == -1 :
            break
        start = start + uiautoXML[start:].find("\"") + 1
        end = start + uiautoXML[start:].find("\"")
        if uiautoXML[start:].find("\"") == -1 :
            break
        clickable = False
        if "true" == uiautoXML[start:end] :
            print "click !!!"
            clickable = True
        start = end



        start = start + uiautoXML[start:].find("bounds=")
        start = start + uiautoXML[start:].find("\"") + 1
        end = start + uiautoXML[start:].find("\"")
        if uiautoXML[start+1:end-1].find("package") != -1 :
            break

        strPoint = uiautoXML[start+1:end-1].split("[")
        #print strPoint
        sp =strPoint[0][:-1]
        ep = strPoint[1]
        sp = sp.split(",")
        x1 = int(sp[0], 10)
        y1 = int(sp[1], 10)
        ep = ep.split(",")
        x2 = int(ep[0], 10)
        y2 = int(ep[1], 10)

        obj = OBJ(idx, resource_id, cName, clickable, x1, y1, x2, y2)
        obj.prints()
        objList.append(obj)
        if obj.clickable == True :
            clickableList.append(obj)
        
        start = end
        if(start == -1) :
            break

    print "OBJ COUNT : " + str(len(objList))
    objGroup = OBJGroup(0, 0, 0, int(fx), int(fy), list(), list())
    for obj in objList :
        if obj.x1 < 0 :
            obj.x1 = 0
        if obj.y1 < 0 :
            obj.y1 = 0
        if obj.x2 < 0 :
            obj.x2 = 0
        if obj.y2 < 0 :
            obj.y2 = 0
        objCheck = False
        level = 0
        objGroupLeveling(objGroup, obj)
    #objGroupPrints(objGroup)

#Clickable 속성을 가진 OBJ를 y축 기준으로 정렬하여 넣고
#X축 기준으로 재정렬
    clickableTree = getClickableTree(clickableList)
    clickableTree = orderClickableTree(clickableTree)
    printsClickableTree(clickableTree)


    return (objGroup, clickableTree)



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

def eventRec() :
    print "start eventRec()"
    mergeEvent = list()
    deviceStates = list()
    keywordTimer = Timer()
    keywordTimer.startTime()
    uniq = 0
    sourceEvent = list()

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
    #print "init=" + recDeviceInfo.initSize + " " + str(recDeviceInfo.dpi) + "dpi" +  " " + "cur=" + recDeviceInfo.curSize + " " + "app=" + recDeviceInfo.appSize
    #mecro.write("deviceSize::" + "init=" + recDeviceInfo.initSize + " " + str(recDeviceInfo.dpi) + "dpi" +  " " + "cur=" + recDeviceInfo.curSize + " " + "app=" + recDeviceInfo.appSize + "\n")
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
        print "Uniq[" + str(sou[0]) + "]  " + sou[1]
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
            print "preTime : " + str(preTime)
            print "currentTime : " + str(curTime)
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
    fx, fy = getWmSize(device)
    uiEvents = list()
    for cmd in eventCmds :
        time.sleep(cmd.delayTime)
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
        uiEvents.append((objGroup, clickableTree, cmd))

    
    time.sleep(5)

    objEvent = list() #[OBJ.cName, Event]
    for ue in uiEvents :
        print " " 
        objGroupPrints(ue[0])
        ue[2].prints()
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
        objEvent.append( (cNames, ue[2], strClick) )


        #위치 정보를 배율로 저장
        obj = searchObjName(ue[0], cNames, 0)
        if obj != None :
            print "*Find Obj*"
            obj.prints()
            ue[2].ratio_x1 = float(ue[2].x1 - obj.x1) / float(obj.x2 - obj.x1)
            ue[2].ratio_y1 = float(ue[2].y1 - obj.y1) / float(obj.y2 - obj.y1)
            ue[2].ratio_x2 = float(ue[2].x2 - obj.x1) / float(obj.x2 - obj.x1)
            ue[2].ratio_y2 = float(ue[2].y2 - obj.y1) / float(obj.y2 - obj.y1)
            print ue[2].prints()
        #앱의 최대 크기에서 배율로 저장
        nameListTemp = list()
        for name in cNames.split(":::") :
            nameListTemp.append(name)
            if name == "" :
                continue
            else :
                obj = searchObjName(ue[0], ":::".join(nameListTemp), 0)
                if obj != None :
                    print "*" * 30 + "*Find Full Obj*" + "*" * 30
                    print "FIND? FULL NAME : " + cNames
                    print "FIND NAME : " + name
                    objGroupPrints(ue[0])
                    obj.prints()
                    print "*" * 73
                    ue[2].full_ratio_x1 = float(ue[2].x1 - obj.x1) / float(obj.x2 - obj.x1)
                    ue[2].full_ratio_y1 = float(ue[2].y1 - obj.y1) / float(obj.y2 - obj.y1)
                    ue[2].full_ratio_x2 = float(ue[2].x2 - obj.x1) / float(obj.x2 - obj.x1)
                    ue[2].full_ratio_y2 = float(ue[2].y2 - obj.y1) / float(obj.y2 - obj.y1)
                    print ue[2].prints()
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
    "\n" )
    for oe in objEvent :
        mecro.write( oe[0] + " " + oe[1].event + ":::" + oe[1].msg + ":::" + \
        str(oe[1].x1) + ":::" + str(oe[1].y1) + ":::" + str(oe[1].x2) + ":::" + str(oe[1].y2) + ":::" + \
        str(oe[1].ratio_x1) + ":::" + str(oe[1].ratio_y1) + ":::" + str(oe[1].ratio_x2) + ":::" + str(oe[1].ratio_y2) + ":::" + \
        str(oe[1].full_ratio_x1) + ":::" + str(oe[1].full_ratio_y1) + ":::" + str(oe[1].full_ratio_x2) + ":::" + str(oe[1].full_ratio_y2) + ":::" + \
        str(oe[1].delayTime) + ":::" + str(oe[1].runTime) + \
        " " +\
        oe[2][0] +\
        " " +\
        oe[2][1] +\
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
        if len(line) == 4 :
            upper = line[2]
            under = line[3]
            
        print eventLine
        ecmd = EventCmd( event=eventLine[0], msg=eventLine[1], \
        x1=int(eventLine[2]), y1=int(eventLine[3]), x2=int(eventLine[4]), y2=int(eventLine[5]), \
        ratio_x1=float(eventLine[6]), ratio_y1=float(eventLine[7]), ratio_x2=float(eventLine[8]), ratio_y2=float(eventLine[9]), \
        full_ratio_x1=float(eventLine[10]), full_ratio_y1=float(eventLine[11]), full_ratio_x2=float(eventLine[12]), full_ratio_y2=float(eventLine[13]), \
        delayTime=float(eventLine[14]), runTime=float(eventLine[15]) )

        loadEvent.append( (line[0], ecmd, (upper, under)) )
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

    RunProcessWait(currentFilePath + "/autoApkRun.py " + apk + " " + device)
    time.sleep(5)
    cfx, cfy = getWmSize(device)
    print "[" + device + "]  FullScreen X : " + str(cfx) + "x" + str(cfy)
    rfx = 0
    rfy = 0
    x1 = 0
    y1 = 0
    x2 = 0
    y1 = 0
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
            RunProcessWait(currentFilePath + "/screencap.py -d " + device + " -o " + deviceDirPath + " -f info.png")
        elif cmd[1].event == "event" :
            sens = False
            windowState = windowPointParsing(device, rfx, rfy)
            objGroup = windowState[0]
            clickableTree = windowState[1]
            print " "
            print cmd[0]
            objGroupPrints(objGroup)
            obj = searchObjName(objGroup, cmd[0], 0)
            #obj = None #seachClick 테스트를 위해서 임시로 막음
            for diffCount in range(7) :
                if obj == None :
                    print "Target On "
                    if diffCount == 3 :
                        if len(cmd[2]) != 2 :
                            continue
                        #clickableTree관련 작업은 여기서 해야함
                        windowState = windowPointParsing(device, rfx, rfy)
                        objGroup = windowState[0]
                        clickableTree = windowState[1]

                        obj = searchClickObj(clickableTree, cmd[2][0], cmd[2][1])
                        print "!" * 50 + "searchClickObj Result" + "!" * 50
                        if obj != None :
                            obj.prints()
                        else :
                            #return 
                            pass
                        print "!" * 120
                        break
                    if diffCount == 4 :
                        RunProcessWait(currentFilePath + "/screencap.py -d " + device + " -o " + deviceDirPath + " -f warning.png")
                        tempFind = cmd[0]
                        windowState = windowPointParsing(device, rfx, rfy)
                        objGroup = windowState[0]
                        clickableTree = windowState[1]
                        tempFind = tempFind.split(":::")
                        print tempFind
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
                        RunProcessWait(currentFilePath + "/screencap.py -d " + device + " -o " + deviceDirPath + " -f error.png")
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
                cmd[1].prints()
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


def getCurrentFocused(currentDumpsys) :
    focused = ""
    for k in range( len(currentDumpsys) ) :
        if currentDumpsys[k].find("mFocusedWindow") != -1 :
            focused = currentDumpsys[k].strip().split()[-1][:-1].split(":")[0]
            break
    #print "focused  : " + focused
    return focused

def getCurrentFocusedWindow(currentDumpsys, focused) :
    tt = ""
    focused_win_num = ""
    focused_size = ""
    focused_win_list = list()
    for k in range( len(currentDumpsys) ) :
        if currentDumpsys[k].find(focused) != -1 :
            if currentDumpsys[k].find("Window #") != -1:
                focused_win_num = currentDumpsys[k].strip().split(":")[0]
                focused_win_list.append( focused_win_num[focused_win_num.find("#")+1:] )
    #print "focused Windows #  : " + focused_win_num
    return "Window #" + max(focused_win_list)
    
def getCurrentFocusedSize(currentDumpsys, focused) :
    focused_win_num = getCurrentFocusedWindow(currentDumpsys, focused)
    for k in range( len(currentDumpsys) ) :
        if currentDumpsys[k].find(focused_win_num) != -1 :
            _split = currentDumpsys[k+3].split()[0]
            focused_size = _split[_split.find("{")+1:]
    #print "focused Size  : " + focused_size
    #print "mFocusedWindow " + focused + ":" + focused_size
    return focused_size

def isBoxCollision(bx1, by1, bx2, by2, x, y) :
    if bx1 <= x and bx2 >= x and by1 <= y and by2 >= y :
        return True
    return False

        
   

if __name__ == "__main__":
    #apkFile = "/Users/numa/droid.apk"
    apkFile = "/Users/numa/testapp.apk"
    mecroFile = "/Users/numa/rec.txt"
    appX, appY = getWmSize("")

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
    
    RunProcessWait(currentFilePath + "/autoApkRun.py " + apkFile)
    
    getEventThread = threading.Thread( target=getEventADB, args=() )
    getEventThread.daemon = True
    getEventThread.start()
    time.sleep(5)
    sourceEvent = eventRec()

    RunProcessWait(currentFilePath + "/autoApkRun.py " + apkFile)
    time.sleep(5)
    eventCmds = parsingSourceEvent(sourceEvent)
    reUIRec("", eventCmds)
    
    time.sleep(3)
    '''
    time.sleep(5)
    loadEvent = getLoadEvent(mecroFile)
    playEvent("", loadEvent)
    '''

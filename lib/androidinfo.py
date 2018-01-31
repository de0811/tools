#!/usr/bin/python3
#-*-coding:utf-8-*-

from lib.runprocess import *

class DumpsysWindow :
    mFocused = ""
    mFocused_size = ""
    mFocused_Error = False
    appSizeX = 0
    appSizeY = 0
    device = ""
    def __init__(self, device) :
        self.mFocused = ""
        self.mFocused_size = ""
        self.mFoucsed_Error = False
        self.appSizeX = 0
        self.appSizeY = 0
        self.device = device
        self.setupDumpsysWindow()

    def setupDumpsysWindow(self) :
        adb = "adb "
        if self.device != "" :
            adb = adb + "-s " + self.device + " "

        currentDumpsys = RunProcessOut(adb + "shell dumpsys window")
        self.mFocused = self.__getCurrentFocused(currentDumpsys)
        self.mFocused_size = self.__getCurrentFocusedSize(currentDumpsys, self.mFocused)
        self.appSizeX, self.appSizeY = self.currentAppSize(currentDumpsys)

    def isFocusedError(self):
        return self.mFocused_Error

    '''
    크래쉬 팝업
    mFocusedWindow=Window{6a6755a u0 Application Error: net.nshc.droidx.foryou}
    '''
    def __getCurrentFocused(self, currentDumpsys):
        focused = ""
        for k in range( len(currentDumpsys) ) :
            if currentDumpsys[k].find("mFocusedWindow") != -1 :
                print (currentDumpsys[k])
                if currentDumpsys[k].find("Error") != -1 :
                    mFocused_Error = True
                focused = currentDumpsys[k].strip().split()[-1][:-1].split(":")[0]
                break
        #print ("focused  : " + focused)
        return focused

    def __getCurrentFocusedWindow(self, currentDumpsys, focused) :
        tt = ""
        focused_win_num = ""
        focused_size = ""
        focused_win_list = list()
        for k in range( len(currentDumpsys) ) :
            if currentDumpsys[k].find(focused) != -1 :
                if currentDumpsys[k].find("Window #") != -1:
                    focused_win_num = currentDumpsys[k].strip().split(":")[0]
                    focused_win_list.append( focused_win_num[focused_win_num.find("#")+1:] )
        #print ("focused Windows #  : " + focused_win_num)
        return "Window #" + max(focused_win_list)

    def __getCurrentFocusedSize(self, currentDumpsys, focused) :
        focused_win_num = self.__getCurrentFocusedWindow(currentDumpsys, focused)
        for k in range( len(currentDumpsys) ) :
            if currentDumpsys[k].find(focused_win_num) != -1 :
                _split = currentDumpsys[k+3].split()[0]
                focused_size = _split[_split.find("{")+1:]
        #print ("focused Size  : " + focused_size)
        #print ("mFocusedWindow " + focused + ":" + focused_size)
        return focused_size

    def currentAppSize(self, currentDumpsys) :
        #app Size 미리 계산해놔야함
        display = ""
        for dump in currentDumpsys :
            if dump.find("init=") != -1 :
                if dump.find("app=") != -1 :
                    display = dump
                    break

        display = display.strip()
        display = display.split()
        strAppSize = ""
        strInitSize = ""
        for dump in display :
            if dump.startswith("app=") == True :
                strAppSize = dump.split("=")[-1]
        appX = strAppSize.split("x")[0]
        appY = strAppSize.split("x")[1]
        return appX, appY

'''
    deviceInfo = DeviceInfo()
    deviceInfo.extractDeviceInfo()
    deviceInfo.prints()
'''
class DeviceInfo :
    device = ""
    physicalSizeX = 0
    physicalSizeY = 0
    OverrideSizeX = 0
    OverrideSizeY = 0

    model = ""              #기기의 이름
    build_id = ""           #빌드 아이디
    ver_sdk = ""            #SDK 버전
    ver_os = ""             #안드로이드 OS 버전
    cpu_32_list = list()    #CPU 32 bit 어떤 것 가능한지 리스트
    cpu_64_list = list()    #CPU 64 bit 어떤 것 가능한지 리스트
    tags = ""               #릴리즈인지 디버거용인지 aosp인지
    manufacturer = ""        #제조사
    def __init__(self, device="") :
        self.device = device
        self.physicalSizeX = 0
        self.physicalSizeY = 0
        self.overridesizex = 0
        self.overridesizey = 0
        
        self.model = ""              #기기의 이름
        self.build_id = ""           #빌드 아이디
        self.ver_sdk = ""            #SDK 버전
        self.ver_os = ""             #안드로이드 OS 버전
        self.cpu_32_list = ""        #CPU 32 bit 어떤 것 가능한지 리스트
        self.cpu_64_list = ""        #CPU 64 bit 어떤 것 가능한지 리스트
        self.tags = ""               #릴리즈인지 디버거용인지 aosp인지
        self.manufacturer = ""        #제조사
    
    def __convertGetprop(self, var) :
        if len(var) == 0 :
            return None
        if len(var) == 1 :
            temp = var[0].decode("UTF-8").strip()
            return temp

    
    def extractDeviceInfo(self) :
        adb = "adb -d "
        if self.device != "" :
            adb = "adb -s " + self.device + " "
        
        cmd = adb + "shell getprop "
        
        self.model = self.__convertGetprop(RunProcessOut(cmd + "ro.product.model"))
        self.build_id = self.__convertGetprop(RunProcessOut(cmd + "ro.build.id"))
        self.ver_sdk = self.__convertGetprop(RunProcessOut(cmd + "ro.build.version.sdk"))
        self.ver_os = self.__convertGetprop(RunProcessOut(cmd + "ro.build.version.release"))
        self.cpu_32_list = self.__convertGetprop(RunProcessOut(cmd + "ro.product.cpu.abilist32"))
        self.cpu_64_list = self.__convertGetprop(RunProcessOut(cmd + "ro.product.cpu.abilist64"))
        self.tags = self.__convertGetprop(RunProcessOut(cmd + "ro.build.tags"))
        self.manufacturer = self.__convertGetprop(RunProcessOut(cmd + "ro.product.manufacturer"))
    
    def prints(self) :
        print (self.model)
        print (self.build_id)
        print ("model : " + self.model)
        print ("build id : " + self.build_id)
        print ("SDK : " + self.ver_sdk)
        print ("OS : " + self.ver_os)
        print ("cpu 32bit : " + self.cpu_32_list)
        print ("cpu 64bit : " + self.cpu_64_list)
        print ("tags : " + self.tags)
        print ("manufacurer : " + self.manufacturer)


    def getwmsize(self) :
        adb = "adb -d "
        if self.device != "" :
            adb = "adb -s " + self.device + " "
        strwm = RunProcessOut(adb + "shell wm size")
        '''
        Physical size: 1440x2560
        Override size: 1080x1920
        '''
        if len( strWM ) <= 0 :
            return 0, 0
        physical = strWM[0].strip().split(": ")[1]
        physical = physical.split("x")
        self.physicalSizeX = int( physical[0] )
        self.physicalSizeY = int( physical[1] )
        if len( strWM ) >= 2 :
            override = strWM[-1].strip().split(": ")[-1]
            override = override.split("x")
            self.overrideSizeX = override[0]
            self.overrideSizeY = override[1]
            return self.overrideSizeX, self.overrideSizeY
        return self.physicalSizeX, self.physicalSizeY
    def parsingDeviceEvent(self, deviceEventList) :
        for dDrive in deviceEventList :
            pass



def isBoxCollision(bx1, by1, bx2, by2, x, y) :
    if bx1 <= x and bx2 >= x and by1 <= y and by2 >= y :
        return True
    return False

#Leaf
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
        print (" " * 50 + "OBJ" + " " * 50)
        print ("idx : " + self.idx)
        print ("Class : " + self.cName)
        print ("resource_id : " + self.resource_id)
        print ("clickable : " + str(self.clickable))
        print ("x1[" + str(self.x1) + "]  " + "y1[" + str(self.y1) + "]  " + "x2[" + str(self.x2) + "]  " + "y2[" + str(self.y2) + "]")
        print (" " * 103)

#Stem
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
        print (" " * 50 + "OBJGROUP" + " " * 50)
        print ("x1[" + str(self.x1) + "]  " + "y1[" + str(self.y1) + "]  " + "x2[" + str(self.x2) + "]  " + "y2[" + str(self.y2) + "]")
        print ("objList Size : " + str(len(self.objList)))
        print ("GroupDown Size : " + str(len(self.groupDown)))
        print (" " * 108)

def objGroupLeveling(objGroup, obj) :
    u'''
    obj가 어느 Group에 포함되는지 찾아 포함시킨다
    :param objGroup: 전체 objGroup을 넣으면 자동으로 찾아 넣어줌
    :param obj:
    :return: 잘 찾았는지 아닌지 확인
    '''
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

def isBoxObjName(objGroup, x1, y1, x2, y2) :
    u'''
    해당 좌표에 선택된 objGroup을 찾기 위한 함수
    :param objGroup:
    :param x1: 최초 좌표 x1
    :param y1: 최초 좌표 y1
    :param x2: 마지막 좌표 x2
    :param y2: 마지막 좌표 y2
    :return: 제대로 찾았다면 True, 아니라면 False meCName은 선택된 objGroup까지의 모든 트리 정보에서 각 idx 값과 이름 값으로 전달
    idx:cName::동일한레벨의idx:동일레벨의cName:::다음레벨의idx:다음레벨의cName
    '''
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

def searchObjName(objGroup, cNames, level) :
    u"""
    줄기(objGroup)에 포함된 모든 잎(obj)의 이름을 저장한 cNames에 해당하는 가장 마지막 obj를 찾기 위한 함수
    :param objGroup:
    :param cNames: isBoxObjName 함수를 통하여 선택된 오브젝트까지의 줄기(ObjGroup)와 잎(Obj) 정보를 입력
    :param level: 무조건 0 재귀로 돌 예정이기 때문에 어쩔 수 없는 선택
    :return:
    """
    if type(cNames) != type(str()) :
        return None
    levelList = cNames.split(":::")
    if len(levelList) -1 < level :
        return None
    if levelList[level] == "" and len(objGroup.objList) > 0 :
        level = level + 1

    if len(levelList) -1 == level :
        for obj in objGroup.objList :
            if levelList[level].find(obj.idx + ":" + obj.cName) != -1 :
                return obj

    for obj in objGroup.objList :
        if levelList[level].find(obj.idx + ":" + obj.cName) == -1 :
            return None

    for _og in objGroup.groupDown :
        obj = searchObjName(_og, cNames, level+1)
        if obj != None :
            return obj
    return None
    


def objGroupPrints(objGroup) :
    u'''
    objGroup의 모든 정보를 출력
    :param objGroup:
    :return:
    '''
    print ("--" * objGroup.level + "x1[" + str(objGroup.x1) + "] " + "y1[" + str(objGroup.y1) + "] " + "x2[" + str(objGroup.x2) + "] " + "y2[" + str(objGroup.y2) + "] " )
    objName = list()
    for obj in objGroup.objList :
        objName.append(str(obj.idx) + ":" + obj.cName)
    print ("   " * objGroup.level + " L " + "::".join(objName))
    for _og in objGroup.groupDown :
        objGroupPrints(_og)



'''
clickable 상태가 True인 오브젝트만 따로 처리하기 위한 함수들
'''

def __appendClickableTree(clickableTree, click) :
    u'''
    adb shell uiautomator dump /sdcard/vivi.xml
    cat /sdcard/vivi.xml
    uiautomator dump명령을 통하여 clickable이 True인 경우 clickableTree에 트리 형태로 추가
    y축의 상태를 보고 같은 level인지 확인하여 진행
    :param clickableTree: clickableTree[stem][leaf]형태
    :param click: Obj 를 사용
    :return: 혹시나 clickableTree가 적용되지 않을까 싶어 반환은 진행
    '''
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
    u'''
    y축 기준으로 트리를 구성
    같은 y축의 경우 같은 level로 진행
    :param clickableList:
    :return:
    '''
    #clickable을 중심으로 화면 구성 상태 분석
    #y축을 기준으로 정렬
    #print "$" * 50 + "ClickableList" + "$" * 50
    clickableTree = list()
    clickableList.sort(key=lambda k : k.y1)
    for click in clickableList :
        #click.prints()
        clickableTree = __appendClickableTree(clickableTree, click)
    #print "$" * 110
    return clickableTree

def orderClickableTree(clickableTree) :
    u'''
    y축으로 정리된 트리를 같은 레벨의 x축으로 한번 더 정리
    :param clickableTree:
    :return:
    '''
    for clickableList in clickableTree :
        clickableList.sort(key=lambda k : k.x1)
    return clickableTree

def printsClickableTree(clickableTree) :
    u'''
    clickableTree의 상태 출력
    :param clickableTree:
    :return:
    '''
    print ("#" * 50 + "ROOT" + "#" * 50)
    for clickableList in clickableTree :
        print ("-" * 50 + "STEM" + "-" * 50)
        for leaf in clickableList :
            print (leaf.prints())
        print ("-" * 104)
    print ("#" * 104)

def isClickableCollision(clickableTree, x1, y1, x2, y2) :
    u'''
    어떤 오브젝트를 선택했는지 확인하기 위해 필요
    :param clickableTree:
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return: 클릭한 Obj를 반환
    '''
    if len(clickableTree) <= 0 :
        return None
    for stem in clickableTree :
        for leaf in stem :
            if isBoxCollision(leaf.x1, leaf.y1, leaf.x2, leaf.y2, x1, y1) and isBoxCollision(leaf.x1, leaf.y1, leaf.x2, leaf.y2, x2, y2) :
                return leaf
    return None

def __clickableTreeNameuu(clickableTree, target, uper) :
    u'''
    어떤 clickable이 선택되었는지 찾음
    :param clickableTree:
    :param target:
    :param uper: 위에서부터 찾아야하나, 아래에서부터 찾아야하나 상태
    :return:
    '''
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
    u'''
    클릭한 버튼의 정보를 idx와 resource-id, cName으로 묶어 위에서 아래의 트리 정보를 uper로 아래에서 위로의 트리 정보를 under로 반환
    :param clickableTree:
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return: uper[위에서 아래 정보], under[아래에서 위로 정보]
    '''
    target = isClickableCollision(clickableTree, x1, y1, x2, y2)
    if target == None :
        return ("-", "-")
    print ("*" * 50 + "CLICK_TARGET" + "*" * 50)
    target.prints()
    print ("*" * 111)
    printsClickableTree(clickableTree)
    uper = __clickableTreeNameuu(clickableTree, target, True)
    under = __clickableTreeNameuu(clickableTree, target, False)
    print ("*" * 50 + "UPER" + "*" * 50)
    print (uper)
    print ("*" * 105)
    print ("*" * 50 + "UNDER" + "*" * 50)
    print (under)
    print ("*" * 105)
    
    return (uper, under)

def __getClickFullName(clickableTree, uper) :
    u'''
    재생되는 clickableTree 정보에서 전체 트리 구조를 반환
    쓸 일이 없어서 괜히 만들었나
    :param clickableTree:
    :param uper: 위에서 아래로 검색한다면 True, 아래에서 위로 검색한다면 False
    :return:
    '''
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
    '''
    재생 상태의 화면의 clickableTree를 확인하여 맞는 Obj를 검색
    :param clickableTree: 재생 상태의 화면 clickableTree
    :param nameList: 녹화시 저장한 정보
    :param upper: 위에서 아래로 검색한다면 True, 아래에서 위로 검색한다면 False
    :return: 검색된 Obj를 반환, 없다면 None 반환
    '''
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
                print ("COUNT UP : " + str(trueCount) + "   rstem : " + str(rstem) + "   maxrStem : " + str(maxrStem))
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
        print ("maxTrueCount : " + str(maxTrueCount))
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
                        print ("trueCount ? : " + str(trueCount))
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
    u'''
    녹화 상태의 오브젝트 트리 정보를 upper와 under로 검색하여 동일한 트리 정보의 오브젝트를 반환
    :param clickableTree: 재생 상태의 화면 정보
    :param upper: 녹화시 저장된 위에서 아래로 트리 정보
    :param under: 녹화시 저장된 아래에서 위로 트리 정보
    :return: 다를 경우 가장 긴 오브젝트 정보를 저장한 위치의 반환 정보를 반환
    '''
    print ("UPPER : " + upper)
    print ("UNDER : " + under)
    printsClickableTree(clickableTree)
    upperOBJ = __searchClickObj(clickableTree, upper, True)
    underOBJ = __searchClickObj(clickableTree, under, False)
    if upperOBJ == None and underOBJ == None :
        print ("ClickOBJ ALL NONE")
        return None
    elif upperOBJ == None :
        print ("ClickOBJ upperOBJ == None ")
        return underOBJ
    elif underOBJ == None :
        print ("ClickOBJ underOBJ == None ")
        return upperOBJ

    if upperOBJ != underOBJ :
        print ("ClickOBJ !=")
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
        print ("ClickOBJ ==")
        return underOBJ


#자체 분석 후 화면 상태를 반환
#첫번째는 화면의 구조를 반환, 두번째는 화면의 버튼을 반환
def windowPointParsing(device="", fx=0, fy=0) :
    u'''
    현재 상태의 화면 분석
    반환 내용으로는 전체 화면 트리, clickable 트리를 반환
    :param device: 분석할 기기
    :param fx: 화면 전체 크기의 x
    :param fy: 화면 전체 크기의 y
    :return: (전체 화면 트리 정보, clickable 트리 정보)
    '''
    #mecro = open(mecroFile, 'w')
    adb = "adb -d "
    if device != "" :
        adb = "adb -s " + device + " "
    RunProcessWait(adb + "shell uiautomator dump /sdcard/vivi.xml")
    #mecro.close()
    uiautoXML = RunProcessOut(adb + "shell cat /sdcard/vivi.xml")
    objList = list()
    clickableList = list()

    print ("##uiautoXML LEN : " + str( len(uiautoXML) ))
    if len(uiautoXML) == 0 :
        return None
    uiautoXML = uiautoXML[0]
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

    print ("OBJ COUNT : " + str(len(objList)))
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

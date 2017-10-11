#!/usr/bin/python
#-*-coding:utf-8-*-
import os
from subprocess import * #Popen
#os.remove(path) 파일 삭제
import zipfile
import shutil
import sys #args
#shutil.rmtree(path[, ignore_errors[, onerror])] 디렉토리 내용물 모두 삭제

def RunProcess(cmd):
    cmd_args = cmd.split()
    process = Popen(cmd_args)
    while process.poll() is None:
        pass
    print process.poll()
    
def c_unzip(source_file, dest_path):
    with zipfile.ZipFile(source_file, 'r') as zf:
        zf.extractall(path=dest_path)
        zf.close()
 
def c_zip(src_path, dest_file):
    with zipfile.ZipFile(dest_file, 'w') as zf:
        rootpath = src_path
        for (path, dir, files) in os.walk(src_path):
            for file in files:
                fullpath = os.path.join(path, file)
                relpath = os.path.relpath(fullpath, rootpath);
                zf.write(fullpath, relpath, zipfile.ZIP_DEFLATED)
        zf.close()

'''
dir 밑의 모든 파일 목록을 반환한다.
'''
def getDirList(dir):
    fList = list()
    dList = list()
    for root, dirs, files in os.walk(dir):
        for fname in files:
            fullpath = os.path.join(root, fname)
            fList.append(fullpath)
        for dname in dirs:
            fullpath = os.path.join(root, dname)
            dList.append(fullpath)
    return fList, dList
    
'''
file 내부의 zip 함수로 만들어진 내용을 바꿔준다.
완전 일체 함수로 만들어야함... 으아아아아아
'''
word = list()
for temp in range(ord('0'), ord('9')+1) :
    word.append( str(unichr(temp)) )
for temp in range(ord('A'), ord('L')) :
    word.append( str(unichr(temp)) )
for temp in range(ord('L')+1, ord('Z')+1) :
    word.append( str(unichr(temp)) )
for temp in range(ord('a'), ord('z')+1) :
    word.append( str(unichr(temp)) )
#print word
def replaceData(file, zipData):
    modif = False
    with open(file, 'rb+') as f :
        content = f.read()
        for dat in zipData:
            usingCon = content
            orig = dat[0]
            change = dat[1]
            #print '*' * 40
            #print 'File Name : ' + file + '   -- change : ' + dat[1]
            idx = 0
            check = False
            endFile = str()
            while idx != -1 :
                idx = usingCon.find(orig)
                if idx == -1 :
                    break;
                for w in word :
                    if w[0] == usingCon[idx-1] or w[0] == usingCon[idx + len(orig)] :
                        check = True
                        modif = True
                        endFile = endFile + usingCon[:idx + len(orig)]
                        usingCon = usingCon[idx + len(orig):]
                        break
                if check == False :
                    usingCon = usingCon[:idx] + change + usingCon[idx+len(orig):]
                check = False
            content = endFile + usingCon
        f.seek(0)
        f.truncate()
        f.write(content)
        if modif is True :
            print 'modifiy File : ' + file

def replaceDir(dirList, zipDir):
    for dir in dirList:
        for zipOrigDir in zipDir :
            if( dir.endswith( zipOrigDir[0] ) ):
                print dir + "\t\t" + dir.replace(zipOrigDir[0], zipOrigDir[1])
                #다 만들고 풀어줘야함
                shutil.move( dir, dir.replace(zipOrigDir[0], zipOrigDir[1]) )

def getApplyList(oPackageName, cPackageName) :
    #내부 내용 변경할 목록 만들기
    oList = list()
    cList = list()
    #changeList = ['de.robv.android.xposed', 'de/robv/android/xposed', 'xposed_service_system', 'xposed_service_app', \
                #'xposed.prop', '_xposed', 'XposedBridge'] #, 'xposed17classddddddBridge', 'xposed36methodddddddBridge'                
    cNameSplit = cPackageName.split('.')
    oNameSplit = oPackageName.split('.')
    
    oList.append(oPackageName)
    oList.append('/'.join( oNameSplit ))
    oList.append( oNameSplit[3] + '_service_system' )
    oList.append( oNameSplit[3] + '_service_app' )
    oList.append( oNameSplit[3] + '.prop' )
    oList.append( '_' + oNameSplit[3] )
    oList.append( oNameSplit[3].capitalize() + 'Bridge' )
    oList.append('xposed17class' + cNameSplit[3].capitalize() + 'Bridge')
    oList.append('xposed36method' + cNameSplit[3].capitalize() + 'Bridge')
    
    cList.append(cPackageName)
    cList.append('/'.join( cNameSplit ))
    #cList.append( cNameSplit[3] + '_service_system' )
    #cList.append( cNameSplit[3] + '_service_app' )
    cList.append( cNameSplit[3] + 'defaulte_system' )
    cList.append( cNameSplit[3] + 'defaulte_app' )
    cList.append( cNameSplit[3] + '.prop' )
    cList.append( '_' + cNameSplit[3] )
    cList.append( cNameSplit[3].capitalize() + 'Bridge' )
    cList.append('xposed17class' + oNameSplit[3].capitalize() + 'Bridge')
    cList.append('xposed36method' + oNameSplit[3].capitalize() + 'Bridge')
    
    #----------------------------
    #폴더와 파일/폴더의 이름을 바꾸어 보아요
    oDirList = list()
    cDirList = list()

    for idx in range(len(oNameSplit)):
        st = str()
        for pp in range(idx+1):
            if st == str() :
                st = '\\' + oNameSplit[pp]
            else :
                st = st + '\\' + oNameSplit[pp]
        oDirList.append( st )
    oDirList.reverse()
    oDirList.append( oNameSplit[3] + '.prop' )
    oDirList.append( 'app_process32_' + oNameSplit[3] )
    oDirList.append( cNameSplit[0] + '\\' + 'psdev' )

    for idx in range(len(cNameSplit)):
        st = str()
        for pp in range(idx+1):
            if st == str() :
                if idx == 0 :
                    st = '\\' + cNameSplit[pp]
                else :
                    st = '\\' + oNameSplit[pp]
            elif pp == idx :
                st = st + '\\' + cNameSplit[pp]
            else :
                st = st + '\\' + oNameSplit[pp]
        cDirList.append( st )    
    cDirList.reverse()
    cDirList.append( cNameSplit[3] + '.prop' )
    cDirList.append( 'app_process32_' + cNameSplit[3] )
    cDirList.append( oNameSplit[0] + '\\' + 'psdev' )
    
    return oList, cList, oDirList, cDirList

#enum
eAPPLY_NONE = 0
eAPPLY_DIR = 1
eAPPLY_ZIP = 2
eAPPLY_APK = 3
def getState(applyPath) :    
    eSTATE = eAPPLY_NONE
    eSTATE = eAPPLY_DIR if os.path.isdir(applyPath) else eSTATE
    eSTATE = eAPPLY_APK if applyPath.endswith('.apk') else eSTATE
    eSTATE = eAPPLY_ZIP if applyPath.endswith('.zip') else eSTATE
    return eSTATE

if __name__ == "__main__":
    
    #변경 목록 만들기
    oPackageName = 'de.robv.android.xposed' #접두사로 orignal 파일의 앞에 o라고 붙임
    cPackageName = 'com.android.plc.google' #접두사로 change 될 파일 이름 앞에 c라고 붙임
    #applyPath = 'C:\\temp\\work\\xposed\\gogo\\module\\app-release.apk' #적용할 위치
    applyPath = 'C:\\temp\\work\\xposed\\gogo\\app-release.apk' #적용할 위치
    apptoolCMD = 'python ' + os.path.dirname(os.path.realpath(__file__)) + '\\apptool.py '
    if len(sys.argv[1:]) > 0 :
        args = sys.argv[1:]
        applyPath = args[0]
    inputPath = str()
    
    #eSTATE
    eSTATE = getState(applyPath)
    print "eSTATE : " + str(eSTATE)

    if eSTATE is eAPPLY_NONE :
        print "eSTATE Error !!!"
    
    if eSTATE is eAPPLY_APK :
        RunProcess('python C:\\tools\\tools\\apptool.py ' + applyPath)
        os.remove(applyPath)
        inputPath = applyPath
        applyPath = applyPath[:applyPath.find('.apk')]
        
    elif eSTATE is eAPPLY_ZIP :
        c_unzip(applyPath, applyPath[:applyPath.find('.zip')])
        #os.remove(applyPath)
        inputPath = applyPath
        applyPath = applyPath[:applyPath.find('.zip')]
        RunProcess(apptoolCMD + '-d ' + applyPath + '\\system\\framework\\XposedBridge.jar')
        os.remove(applyPath + '\\system\\framework\\XposedBridge.jar')
    
    elif eSTATE is eAPPLY_DIR :
        print "eSTATE Error !!!"
        pass
    
    #변경할 목록 분석해서 목록으로 정리
    oList, cList, oDirList, cDirList = getApplyList(oPackageName, cPackageName)
    print '*' * 30
    print oList
    print cList
    print '-' * 30
    print oDirList
    print cDirList
    print '*' * 30
    
    #이거 하나 만들려고 별 짓을 다 했네
    comb = zip(oList, cList)
    combDir = zip(oDirList, cDirList)

    #내부 목록 모두 보기
    fileList, dirList = getDirList(applyPath)

    #해당 폴더 아래로 모두 찾아서 바꿔 넣기
    for file in fileList:
        replaceData(file, comb)
    print '!!!! File End !!!!'

    #폴더 이름 변경
    fileList.reverse()
    dirList.reverse()
    replaceDir(fileList, combDir)
    replaceDir(dirList, combDir)
    print '!!!! Dir End !!!!'

    if eSTATE is eAPPLY_APK :
        applyPath = inputPath
        RunProcess(apptoolCMD + applyPath[:applyPath.find('.apk')])
        shutil.move( applyPath[:applyPath.find('.apk')] + '\\dist\\' + os.path.basename(applyPath), applyPath)
        shutil.rmtree(applyPath[:applyPath.find('.apk')]) #apk 풀었던 폴더 삭제

    elif eSTATE is eAPPLY_ZIP :
        #c_unzip(applyPath, os.path.dirname(applyPath))
        #os.remove(applyPath)
        #inputPath = applyPath
        #applyPath = applyPath[:applyPath.find('.zip')]
        RunProcess(apptoolCMD + '-b ' + applyPath + '\\system\\framework\\XposedBridge')
        shutil.move(applyPath + '\\system\\framework\\XposedBridge\\dist\\' + cList[6] + '.jar', applyPath + '\\system\\framework')
        shutil.rmtree(applyPath + '\\system\\framework\\XposedBridge') #XposedBridge 폴더 삭제
        c_zip(applyPath, inputPath)
        RunProcess(apptoolCMD + '-s ' + inputPath)
        shutil.rmtree(applyPath) #FrameWork 압축 풀었던 폴더 삭제


    print '!!!! END !!!!'
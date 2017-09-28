#!/usr/bin/python
#-*-coding:utf-8-*-
import os
#os.remove(path) 파일 삭제
import zipfile
import shutil
#shutil.rmtree(path[, ignore_errors[, onerror])] 디렉토리 내용물 모두 삭제

def changeData(source, target, dest) :
    pass
    
def unzip(source_file, dest_path):
    with zipfile.ZipFile(source_file, 'w') as zf:
        zf.extractall(path=dest_path)
        zf.close()
 
def zip(src_path, dest_file):
    with zipfile.ZipFile(dest_file, 'w') as zf:
        rootpath = src_path
        for (path, dir, files) in os.walk(src_path):
            for file in files:
                fullpath = os.path.join(path, file)
                relpath = os.path.relpath(fullpath, rootpath);
                zf.write(fullpath, relpath, zipfile.ZIP_DEFLATED)
        zf.close()

def getDirList(dir):
    fList = list()
    for root, dirs, files in os.walk(dir):
        for fname in files:
            fullpath = os.path.join(root, fname)
            print fullpath
            fList.append(fullpath)
    return fList

if __name__ == "__main__":
    '''
    zipName = 'C:\\temp\\work\\zip\\ScreenCap.zip'
    print zipName
    zipPath = os.path.splitext( zipName )[0]
    zipPath = os.path.dirname( zipName )
    #print zipPath
    zipPath = 'C:\\temp\\work\\zip\\ScreenCap'
    #unzip(zipName, zipPath )
    #zip('E:\\temp\\result\\Sources', 'E:\\temp\\result\\res.zip')
    target = 'C:\\temp\\work\\zip\\ScreenCap.zip'
    shutil.rmtree(path=target, ignore_errors=True)
    '''

    #Installer.apk apktool로 풀기
    #Installer.apk 삭제
    #framework.zip 압축 풀기
    #framework.zip 삭제
    #framework\XposedBridge.jar apktool로 풀기
    #XposedBridge.jar 삭제
    
    '''
    해당 내용으로 모두 검색 후 변경
    de.robv.android.xposed	aa.bbbb.ccccccc.dddddd
    de/robv/android/xposed	aa/bbbb/ccccccc/dddddd
    xposed_service_system	dddddd_eeeeeee_ffffff
    xposed_service_app	dddddd_eeeeeee_ggg
    xposed.prop	dddddd.prop
    _xposed	_dddddd
    XposedBridge	ddddddBridge
    xposed17classddddddBridge	xposed17classXposedBridge
    xposed36methodddddddBridge	xposed36methodXposedBridge
    su	sl
    
    xposed <- 6자리 고정
    3가지 문자 총 16개 문자열

    '''
    #args = sys.argv[1:]
    #fileName = args[0]
    #wordlist = args[1:]
    
    #os.remove('C:\\temp\\work\\zip\\ScreenCap.zip')
    '''
    print u"문자는 총 4개를 작성합니다. 문자의 갯수를 지켜야합니다"
    print u"문자 앞 3개는 총 길이 16자리를 넘으면 안됩니다. 한 단어마다 띄워서 표기하세요"
    tempword = raw_input()
    wordlist = tempword.split()
    
    #wordlist.append( input(u"6자리 포인트 문자를 적어주세요") )
    
    print u"입력받은 문자를 출력"
    print wordlist
    print '*' * 10
    
    if( 4 != len(wordlist) ) :
        print u"문자 갯수가 잘못되어 있습니다"
        print wordlist
    if( 16 != len( "".join(wordlist) ) ) :
        print u"문자열의 길이가 16개가 되지 않습니다"
        print wordlist
    '''
    
    print getDirList('C:\\temp\\work\\zip')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
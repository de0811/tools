import os
import platform

isWindows = 'Windows' in platform.platform()
currentPath = os.path.dirname(os.path.realpath(__file__))
utilPath = currentPath + "/../util/"

apktool = '''java -jar ''' + utilPath + '''apktool.jar'''
signer = '''jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore'''
key = utilPath + '''keystore/testsig.jks'''
keyPass = '''-storepass 123456'''
alias = '''testsig'''

jadx = utilPath + '''jadx/bin/jadx-gui'''
bytecode = '''C:\\utill\\BytecodeViewer.2.9.8\\BytecodeViewer.exe'''
jad = '''C:\\utill\\jd-gui\\jad'''

screencapPath = '''c:\\temp\\ScreenCap'''
if isWindows is False :
    screencapPath = '''~/temp/ScreenCap'''
aapt = utilPath + "aapt.exe dump badging"
if isWindows is False :
    aapt = utilPath + '''aapt dump badging'''

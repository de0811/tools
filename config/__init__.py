import os
import platform


currentPath = os.path.dirname(os.path.realpath(__file__))
#utilPath = currentPath + "/../util/"
utilPath = currentPath + os.sep + ".." + os.sep + "util" + os.sep

apktool = '''java -jar ''' + utilPath + '''apktool.jar'''
signer = '''jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore'''
key = utilPath + '''keystore/testsig.jks'''
keyPass = '''-storepass 123456'''
alias = '''testsig'''

jadx = utilPath + '''jadx/bin/jadx-gui'''
bytecode = '''C:\\utill\\BytecodeViewer.2.9.8\\BytecodeViewer.exe'''
jad = '''C:\\utill\\jd-gui\\jad'''



from sys import platform as _platform
#linux
if _platform == "linux" or _platform == "linux2" :
    aapt = utilPath + 'linux_aapt dump badging'
    screencapPath = '''/Users/numa/temp/ScreenCap'''
#MAC OS X
elif _platform == "darwin" :
    aapt = utilPath + 'mac_aapt dump badging'
    screencapPath = '''/Users/numa/temp/ScreenCap'''
#Windows 32-bit
elif _platform == "win32" :
	aapt = utilPath + "aapt.exe dump badging"
	screencapPath = '''c:\\temp\\ScreenCap'''
	pass
#Window 64-bit
elif _platform == "win64" :
	aapt = utilPath + "aapt.exe dump badging"
	screencapPath = '''c:\\temp\\ScreenCap'''
else :
	#????
	aapt = "??????"

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

jadx = utilPath + 'jadx' + os.sep + 'bin' + os.sep + 'jadx-gui'
bytecode = utilPath + 'BytecodeViewer.2.9.8' + os.sep + 'BytecodeViewer.exe'
jad = utilPath + 'jd-gui' + os.sep + 'jad'



from sys import platform as _platform
#linux
if _platform == "linux" or _platform == "linux2" :
    aapt = utilPath + 'linux_aapt dump badging'
    screencapPath = '''/home/num/temp/ScreenCap'''
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


if os.path.isdir(screencapPath) == False :
	if os.path.isdir(os.path.dirname(screencapPath)) == False :
		os.mkdir(os.path.dirname(screencapPath))
	os.mkdir(screencapPath)

temp_path = os.path.dirname(screencapPath) + os.sep
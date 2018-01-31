#!/usr/bin/python3
#-*-coding:utf-8-*-

from subprocess import *
import os
import sys
#import shutil
import config
from lib import option

#-----------colorama---------------
#from __future__ import print_function
#import fixpath
from colorama import init, Fore, Back, Style

init()
#----------------------------------
print(Fore.YELLOW + Back.BLUE + Style.BRIGHT + "screencap.py runing" + Fore.RESET + Back.RESET + Style.NORMAL)

def RunProcess(cmd):
    cmd_args = cmd.split()
    #pipe = Popen(cmd_args, stdout=PIPE, stderr=PIPE)
    #print pipe.stdout.read();
    #print pipe.stderr.read();
    process = Popen(cmd_args)
    while process.poll() is None:
        pass
        #print('working..')
    return process.poll()

def CainRunProcess(cmd):
    result = RunProcess(cmd)
    if result == 1:
        print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + "Process Error" + Fore.RESET + Back.RESET + Style.NORMAL)
        sys.exit()

class screencap:
    mFileName = "screencap.png"
    mOutPath = config.screencapPath
    mDevice = ""
    def setFileName(self, args=list()):
        if len(args) is 0: return
        self.mFileName = args[0]
    def setOutPath(self, args=list()):
        if len(args) is 0: return
        self.mOutPath = args[0]
        if os.path.isdir(self.mOutPath) is False:
            self.mOutPath, self.mFileName = os.path.split(self.mOutPath)
    def setDevice(self, args=list()):
        if len(args) is 0: return
        self.mDevice = args[0]

    def run(self, args=list()):
        adb = "adb -d "
        if self.mDevice != "" :
            adb = "adb -s " + self.mDevice + " "
        CainRunProcess(adb + '''shell screencap -p /sdcard/screencap.png''')
        #file_name = rename
        idx = 0
        name, tail = os.path.splitext(self.mFileName)
        while os.path.isfile(self.mOutPath + os.sep + self.mFileName):
            self.mFileName = name + str(idx) + tail
            idx = idx + 1
        print(Fore.WHITE + Back.GREEN + "OUT" + Back.RESET + "  " + self.mOutPath + os.sep + self.mFileName + Fore.RESET + Back.RESET + Style.NORMAL)
        CainRunProcess(adb + '''pull /sdcard/screencap.png ''' + self.mOutPath + os.sep + self.mFileName)
        CainRunProcess(adb + '''shell rm /sdcard/screencap.png''')

    def help(self, args):
        hel = u'''screencap.py [command]
        [command]
        -h : 실행 방법을 설명합니다
        -o : 출력될 폴더를 선택합니다(폴더가 있어야 합니다)
        -f : 출력될 파일의 이름을 저장합니다
        -d : 디바이스를 선택합니다
        command가 없을 경우 지정한 위치로 저장합니다
        '''
        print(Fore.LIGHTYELLOW_EX + hel + Fore.RESET)
        sys.exit()

if __name__ == "__main__":

    scCap = screencap()

    opt = option.option()
    #def addOpt(self, opt, argCount, bVarArg, func):
    opt.addOpt(opt="-h", argCount=0, bVarArg=True, bHelp=True, func=scCap.help)
    opt.addOpt(opt="-d", argCount=1, bVarArg=False, bHelp=False, func=scCap.setDevice)
    opt.addOpt(opt="-o", argCount=1, bVarArg=False, bHelp=False, func=scCap.setOutPath)
    opt.addOpt(opt="-f", argCount=1, bVarArg=False, bHelp=False, func=scCap.setFileName)
    opt.addOpt(opt="default", argCount=0, bVarArg=True, bHelp=False, func=scCap.run)
    opt.parsing()
    #opt.tprint()
    opt.run()


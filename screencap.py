#!/usr/bin/python
#-*-coding:utf-8-*-

from subprocess import *
import os
import sys
import shutil
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
    def setFileName(self, args=list()):
        if len(args) is 0: return
        self.mFileName = args[0]
    def setOutPath(self, args=list()):
        if len(args) is 0: return
        self.mOutPath = args[0]
        if os.path.isdir(self.mOutPath) is False:
            self.mOutPath, self.mFileName = os.path.split(self.mOutPath)

    def run(self, args=list()):
        CainRunProcess('''adb -d shell screencap -p /sdcard/screencap.png''')
        #file_name = rename
        idx = 0
        name, tail = os.path.splitext(self.mFileName)
        while os.path.isfile(self.mOutPath + os.sep + self.mFileName):
            self.mFileName = name + str(idx) + tail
            idx = idx + 1
        print(Fore.WHITE + Back.GREEN + "OUT" + Back.RESET + "  " + self.mOutPath + os.sep + self.mFileName + Fore.RESET + Back.RESET + Style.NORMAL)
        CainRunProcess('''adb -d pull /sdcard/screencap.png ''' + self.mOutPath + os.sep + self.mFileName)
        CainRunProcess('''adb -d shell rm /sdcard/screencap.png''')

    def help(self, args):
        hel = '''screencap.py [command]
        [command]
        -o : 출력될 폴더를 선택합니다(폴더가 있어야 합니다)
        -f : 출력될 파일의 이름을 저장합니다
        command가 없을 경우 지정한 위치로 저장합니다
        '''
        print(Fore.LIGHTYELLOW_EX + hel + Fore.RESET)

if __name__ == "__main__":

    scCap = screencap()

    opt = option.option()
    opt.addOpt("-o", 1, scCap.setOutPath)
    opt.addOpt("-f", 1, scCap.setFileName)
    opt.addOpt("default", 0, scCap.run)
    opt.parsing()
    #opt.tprint()
    opt.run()







































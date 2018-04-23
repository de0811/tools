#!/usr/bin/python3
#-*-coding:utf-8-*-

from subprocess import *
import os
import sys
#import shutil
import config
import threading
from lib import option

#-----------colorama---------------
#from __future__ import print_function
#import fixpath
from colorama import init, Fore, Back, Style

init()
#----------------------------------



class ScreenCap:
    file_name = "screencap.png"
    out_path = config.screencapPath
    mDevice = ""
    def ScreenCap(self) :
        self.file_name = "screencap.png"
        self.out_path = config.screencapPath
        self.mDevice = ""
    def non_stop_screen_shot(self, device, out_path, file_name) :
        self.file_name = file_name
        self.out_path = out_path
        self.mDevice = device
        self.screen_shot()
    def __run_process(self, cmd):
        cmd_args = cmd.split()
        #pipe = Popen(cmd_args, stdout=PIPE, stderr=PIPE)
        #print pipe.stdout.read();
        #print pipe.stderr.read();
        process = Popen(cmd_args)
        while process.poll() is None:
            pass
            #print('working..')
        return process.poll()

    def __run_process_error_check(self, cmd):
        result = self.__run_process(cmd)
        if result == 1:
            print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + "Process Error" + Fore.RESET + Back.RESET + Style.NORMAL)
            sys.exit()
    
    def __thread_pull_and_delete(self) :
        adb = "adb -d "
        if self.mDevice != "" :
            adb = "adb -s " + self.mDevice + " "
        cmd = adb + '''pull /sdcard/''' + self.file_name + ' ' + self.out_path + self.file_name
        self.__run_process_error_check(cmd)
        cmd = adb + '''shell rm /sdcard/''' + self.file_name
        self.__run_process_error_check(cmd)

    def setFileName(self, args=list()):
        if len(args) is 0: return
        self.file_name = args[0]
    def setOutPath(self, args=list()):
        if len(args) is 0: return
        self.out_path = args[0]
        if os.path.isdir(self.out_path) is False:
            self.out_path, self.file_name = os.path.split(self.out_path)
    def setDevice(self, args=list()):
        if len(args) is 0: return
        self.mDevice = args[0]
    
    def screen_shot(self) :
        adb = "adb -d "
        if self.mDevice != "" :
            adb = "adb -s " + self.mDevice + " "
        #file_name = rename
        idx = 0
        name, tail = os.path.splitext(self.file_name)
        if self.out_path.endswith(os.sep) == False :
            self.out_path = self.out_path + os.sep
        while os.path.isfile(self.out_path + self.file_name):
            self.file_name = name + str(idx) + tail
            idx = idx + 1
        print(Fore.WHITE + Back.GREEN + "OUT" + Back.RESET + "  " + self.out_path + self.file_name + Fore.RESET + Back.RESET + Style.NORMAL)
        self.__run_process_error_check(adb + '''shell screencap -p /sdcard/''' + self.file_name)
        t = threading.Thread( target=self.__thread_pull_and_delete, args=() )
        t.start()

    def run(self, args=list()):
        self.screen_shot()

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

    print(Fore.YELLOW + Back.BLUE + Style.BRIGHT + "screencap.py runing" + Fore.RESET + Back.RESET + Style.NORMAL)
    scCap = ScreenCap()

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


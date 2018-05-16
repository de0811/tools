#!/usr/bin/python3
#-*-coding:utf-8-*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from subprocess import *
import config
from lib import option
from lib import runprocess

#-----------colorama---------------#
from colorama import init, Fore, Back, Style
init()
#----------------------------------#
#print(Fore.YELLOW + Back.BLUE + Style.BRIGHT + "aapt.py runing" + Fore.RESET + Back.RESET + Style.NORMAL)

class aapt:
    bPackageName = False
    package_name = ""
    bPackageActivity = False
    package_activity = ""
    error_list = list()
    is_error = False
    def aapt(self) :
        self.bPackageName = False
        self.package_name = ""
        self.bPackageActivity = False
        self.package_activity = ""
        self.error_list = list()
        self.is_error = False
    def aapt_parsing(self, apk) :
        apkInfos = runprocess.RunProcessOut(config.aapt + ' ' + apk)
        if len(apkInfos) < 5 :
            for info in apkInfos :
                info = info.decode("UTF-8").strip()
                self.error_list.append(info)
            self.is_error = True
            return
        for info in apkInfos :
            info = info.decode("UTF-8").strip()
            if "package:" in info :
                info = info.split()
                info = info[1].split("'")
                self.package_name = info[1]
            elif "launchable-activity:" in info :
                info = info.split()
                info = info[1].split("'")
                self.package_activity = info[1]
    def getPackageName(self, args):
        self.bPackageName = True
    def getPackageActivity(self, args):
        self.bPackageActivity = True
    def run(self, args=list()):
        if len(args) == 0: return
        if self.is_error == True :
            for line in self.error_list :
                print (line)
            return
        if self.bPackageActivity == False and self.bPackageName == False :
            apkInfos = runprocess.RunProcessOut(config.aapt + ' ' + args[0])
            for info in apkInfos :
                info = info.decode("UTF-8").strip()
                print (info)
            return 
        self.aapt_parsing(args[0])
        if self.bPackageName == True :
            print (Fore.YELLOW + Style.BRIGHT + self.package_name + Fore.RESET + Style.NORMAL)
        if self.bPackageActivity == True :
            print (Fore.YELLOW + Style.BRIGHT + self.package_activity + Fore.RESET + Style.NORMAL)
 
#            if "package:" in info \
#                    or "sdkVersion:" in info \
#                    or "targetSdkVersion:" in info \
#                    or "launchable-activity:" in info :
#                print(Fore.YELLOW + Style.BRIGHT + info + Fore.RESET + Style.NORMAL)

    def help(self, args):
        hel = u'''aapt.py [command] <target>
        [command]
        -h : 설명을 표시합니다
        -n : 패키지 이름만 출력합니다
        -a : 액티비티 시작 이름만 출력합니다
        '''
        print(Fore.LIGHTCYAN_EX + hel + Fore.RESET) 


if __name__ == "__main__":

    aa = aapt()

    opt = option.option()

    opt.addOpt(opt="-h", argCount=0, bVarArg=True, bHelp=True, func=aa.help)
    opt.addOpt(opt="-n", argCount=0, bVarArg=True, bHelp=False, func=aa.getPackageName)
    opt.addOpt(opt="-a", argCount=0, bVarArg=True, bHelp=False, func=aa.getPackageActivity)
    opt.addOpt(opt="default", argCount=1, bVarArg=True, bHelp=False, func=aa.run)
    opt.parsing()
    opt.run()

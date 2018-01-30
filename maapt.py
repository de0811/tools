#!/usr/bin/python
#-*-coding:utf-8-*-
from subprocess import *
import config
from lib import option
from lib.runprocess import *

#-----------colorama---------------#
from colorama import init, Fore, Back, Style
init()
#----------------------------------#
#print(Fore.YELLOW + Back.BLUE + Style.BRIGHT + "aapt.py runing" + Fore.RESET + Back.RESET + Style.NORMAL)

class aapt:
    bPackageName = False
    bPackageActivity = False
    def getPackageName(self, args):
        self.bPackageName = True
    def getPackageActivity(self, args):
        self.bPackageActivity = True
    def run(self, args=list()):
        if len(args) is 0: return
        apkInfos = RunProcessOut(config.aapt + ' ' + args[0])
        if self.bPackageName is True:
            for info in apkInfos:
                if "package:" in info :
                    info = info.split()
                    info = info[1].split("'")
                    print(Fore.YELLOW + Style.BRIGHT + info[1] + Fore.RESET + Style.NORMAL)
                    return
        elif self.bPackageActivity is True :
            for info in apkInfos:
                if "launchable-activity:" in info :
                    info = info.split()
                    info = info[1].split("'")
                    print(Fore.YELLOW + Style.BRIGHT + info[1] + Fore.RESET + Style.NORMAL)
                    return
        for info in apkInfos:
            print info
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

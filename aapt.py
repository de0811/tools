#!/usr/bin/python
#-*-coding:utf-8-*-
from subprocess import *
import os
import sys
import time
import shutil
import config
from lib import option

#-----------colorama---------------#
from colorama import init, Fore, Back, Style
init()
#----------------------------------#
print(Fore.YELLOW + Back.BLUE + Style.BRIGHT + "aapt.py runing" + Fore.RESET + Back.RESET + Style.NORMAL)

def RunProcess(cmd):
    print(Fore.BLUE + Back.LIGHTCYAN_EX + Style.BRIGHT + cmd + Fore.RESET + Back.RESET + Style.NORMAL)
    cmd_args = cmd.split()
    pipe = Popen(cmd_args, stdout=PIPE, stderr=STDOUT)
#    while pipe.poll() is None:
#        print(Fore.RED + Style.BRIGHT + "polling : " + str(pipe.poll()) + Fore.RESET + Style.NORMAL)
#        time.sleep(0.5)
#    if pipe.poll() == 1:
#        print(Fore.RED + Style.BRIGHT + "Error" + Fore.RESET + Style.NORMAL)
#        sys.exit()
    #print(Fore.RED + Style.BRIGHT + "polling : " + str(pipe.stderr.read()) + Fore.RESET + Style.NORMAL)
    outList = pipe.stdout.readlines()
    return outList

class aapt:
    bPackageName = False
    def getPackageName(self, args):
        self.bPackageName = True
    def run(self, args=list()):
        if len(args) is 0: return
        apkInfos = RunProcess(config.aapt + ' ' + args[0])
        if self.bPackageName is True:
            for info in apkInfos:
                if "package:" in info :
                    info = info.split()
                    info = info[1].split("'")
                    print(Fore.YELLOW + Style.BRIGHT + info[1] + Fore.RESET + Style.NORMAL)
                    return
        for info in apkInfos:
            if "package:" in info \
                    or "sdkVersion:" in info \
                    or "targetSdkVersion:" in info :
                print(Fore.YELLOW + Style.BRIGHT + info + Fore.RESET + Style.NORMAL)

    def help(self, args):
        hel = '''aapt.py [command] <target>
        [command]
        -h : 설명을 표시합니다
        -n : 패키지 이름만 출력합니다
        '''
        print(Fore.LIGHTCYAN_EX + hel + Fore.RESET) 


if __name__ == "__main__":

    aa = aapt()

    opt = option.option()
    #opt.addOpt("-o", 1, scCap.setOutPath)
    #opt.addOpt("-f", 1, scCap.setFileName)
    opt.addOpt("-h", 0, aa.help)
    opt.addOpt("-n", 0, aa.getPackageName)
    opt.addOpt("default", 1, aa.run)
    opt.parsing()
    opt.run()

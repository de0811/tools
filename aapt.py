#!/usr/bin/python
from subprocess import *
import os
import sys
import shutil
import config

#-----------colorama---------------#
from colorama import init, Fore, Back, Style
init()
#----------------------------------#
print(Fore.YELLOW + Back.BLUE + Style.BRIGHT + "aapt.py runing" + Fore.RESET + Back.RESET + Style.NORMAL)

def RunProcess(cmd):
    print(Fore.BLUE + Back.LIGHTCYAN_EX + Style.BRIGHT + cmd + Fore.RESET + Back.RESET + Style.NORMAL)
    cmd_args = cmd.split()
    pipe = Popen(cmd_args, stdout=PIPE)
    while pipe.poll() is None:
        pass
    if pipe.poll() == 1:
        print(Fore.RED + Style.BRIGHT + "Error" + Fore.RESET + Style.NORMAL)
        sys.exit()

    outList = pipe.stdout.readlines()
    return outList



if __name__ == "__main__":
    apkInfos = RunProcess(config.aapt + ' ' + sys.argv[1])
    for info in apkInfos:
        if "package:" in info \
                or "sdkVersion:" in info \
                or "targetSdkVersion:" in info :
            print(Fore.YELLOW + Style.BRIGHT + info + Fore.RESET + Style.NORMAL)

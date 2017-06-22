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
    cmd_args = cmd.split()
    pipe = Popen(cmd_args, stdout=PIPE)
    outList = pipe.stdout.readlines()
    return outList



if __name__ == "__main__":
    apkInfos = RunProcess(config.aapt + ' ' + sys.argv[1])
    for info in apkInfos:
        if "package:" in info \
		or "sdkVersion:" in info \
		or "targetSdkVersion:" in info :
            print(Fore.YELLOW + info + Fore.RESET)

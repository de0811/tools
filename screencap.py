#!/usr/bin/python
from subprocess import *
import os
import sys
import shutil
import config

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



if __name__ == "__main__":
    
    CainRunProcess('''adb -d shell screencap -p /sdcard/screencap.png''')
    outPath = ''
    file_name = '''screencap.png'''
	
    if len(sys.argv[1:]) > 0 :
        args = sys.argv[1:]
        if args[0].startswith('-'):
            if args[0].endswith('o'):
                outPath = args[1]
                #option
                #sys.exit()
    else :
	    outPath = config.screencapPath

    #file_name = rename
    idx = 0
    while os.path.isfile(outPath + os.sep + file_name):
        file_name = '''screencap''' + str(idx) + '''.png'''
        idx = idx + 1
    print(Fore.WHITE + Back.GREEN + "OUT" + Back.RESET + "  " + outPath + os.sep + file_name + Fore.RESET + Back.RESET + Style.NORMAL)
    CainRunProcess('''adb -d pull /sdcard/screencap.png ''' + outPath + os.sep + file_name)
    CainRunProcess('''adb -d shell rm /sdcard/screencap.png''')









































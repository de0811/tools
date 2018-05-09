#!/usr/bin/python3
#-*-coding:utf-8-*-
import apkrunner
from lib.runprocess import *
import os
import screencap
import shutil

#-----------colorama---------------
#from __future__ import print_function
#import fixpath
from colorama import init, Fore, Back, Style

init()
#----------------------------------


if __name__ == "__main__":
    
    #for a in range(100) :
    while(True) :
        RunProcessWait("adb logcat -c")
        apk_runner = apkrunner.ApkRunner()
        apk_runner.set_apk(["/Users/numa/temp/ez_no_log.apk", ])
        apk_runner.focused_limit.append("com.lgcns.ucapim.activity.UcapMainTabActivity")

        #apk_runner.set_apk(["/Users/numa/temp/fxs_app-debug.apk", ])
        #apk_runner.focused_limit.append("net.nshc.eagleeye.MainActivity")

        apk_runner.time_limit = 60
        apk_runner.time_wait = 3
        apk_runner.apk_running()
        print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + "APK RUNNER END GO FILE CHECK" + Fore.RESET + Back.RESET + Style.NORMAL)
    
        
        focused_list = apk_runner.device_logs.find_event("2165c1582b017ece", "focused_Error")
        if len(focused_list) > 0 :
            file_head = "logs"
            file_tail = ".txt"
            png_tail = ".png"
            count = 0
            while(True)  :
                print ("FILE UNIQUE SETTING : " + str(count))
                if os.path.isfile(apk_runner.temp_path + file_head + str(count) + file_tail) == True :
                    count = count + 1
                    continue
                else :
                    break
            
            apk_runner.device_logs.prints("2165c1582b017ece")

            print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + "APK Error" + Fore.RESET + Back.RESET + Style.NORMAL)
            print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + "LOG FILE ::: " + apk_runner.temp_path + file_head + str(count) + file_tail + Fore.RESET + Back.RESET + Style.NORMAL)

            os.system("adb logcat -d > " + apk_runner.temp_path + file_head + str(count) + file_tail)
            RunProcessWait("adb logcat -d > " + apk_runner.temp_path + file_head + str(count) + file_tail)
            screen_cap = screencap.ScreenCap()
            screen_cap.non_stop_screen_shot("2165c1582b017ece", apk_runner.temp_path, file_head + str(count) + png_tail)
        print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + "ONE STEP" + Fore.RESET + Back.RESET + Style.NORMAL)
        RunProcessWait("adb shell am force-stop " + apk_runner.apk_name)
        if os.path.isdir(apk_runner.temp_path + "2165c1582b017ece") :
            shutil.rmtree(apk_runner.temp_path + "2165c1582b017ece")
        
        
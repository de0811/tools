#!/usr/bin/python3
#-*-coding:utf-8-*-
import android.apkrunner
from lib.runprocess import *
import os
import android.screencap
import shutil

#-----------colorama---------------
#from __future__ import print_function
#import fixpath
from colorama import init, Fore, Back, Style

init()
#----------------------------------


if __name__ == "__main__":
    device_finder = android.devicefinder.DeviceFinder()
    #device_finder.device_list

   
    #for a in range(100) :
    while(True) :
        RunProcessWait("adb logcat -c")
        apk_runner = android.apkrunner.ApkRunner()
        apk_runner.set_apk(["/Users/numa/temp/ez_no_log.apk", ])
        apk_runner.focused_limit.append("com.lgcns.ucapim.activity.UcapMainTabActivity")

        device_finder.find_device_list()

        apk_runner.time_limit = 60
        apk_runner.time_wait = 3
        apk_runner.apk_running()
        print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + "APK RUNNER END GO FILE CHECK" + Fore.RESET + Back.RESET + Style.NORMAL)
    
        
        for device in device_finder.device_list :
            focused_error_list = apk_runner.device_logs.find_event(device, "focused_Error")
            if len(focused_error_list) > 0 :
                file_head = device + "logs"
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
            
                print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + "APK Error" + Fore.RESET + Back.RESET + Style.NORMAL)
                print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + "LOG FILE ::: " + apk_runner.temp_path + file_head + str(count) + file_tail + Fore.RESET + Back.RESET + Style.NORMAL)

                os.system("adb -s " + device + " logcat -d > " + apk_runner.temp_path + file_head + str(count) + file_tail)
                RunProcessWait("adb -s " + device + " logcat -d > " + apk_runner.temp_path + file_head + str(count) + file_tail)
                screen_cap = android.screencap.ScreenCap()
                screen_cap.non_stop_screen_shot(device, apk_runner.temp_path, file_head + str(count) + png_tail)


            print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + "ONE STEP" + Fore.RESET + Back.RESET + Style.NORMAL)
            RunProcessWait("adb -s " + device + " shell am force-stop " + apk_runner.apk_name)
            #if os.path.isdir(apk_runner.temp_path + "2165c1582b017ece") :
                #shutil.rmtree(apk_runner.temp_path + "2165c1582b017ece")
        
        
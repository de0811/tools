#!/usr/bin/python3
#-*-coding:utf-8-*-
import devicefinder
import apkrunner
import apkinstaller
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
    device_finder = devicefinder.DeviceFinder()
    #device_finder.device_list
    apk_list = list()


    apk_installer = apkinstaller.ApkInstaller()
    apk_list.append(["/Users/numa/temp/KT5/KTAuth_01.00.00_google_20180514_rev39576_DX.apk", "com.kt.mysign.activity.AppSplashActivity"])
    apk_list.append(["/Users/numa/temp/KT5/ktcs_v05.03.02_onestore_ollehunsigned_20180510_DX.apk", "com.ktshow.cs.Main"])
    apk_list.append(["/Users/numa/temp/KT5/ktfamilyBox_V03.00.00_onestore_3_2_DX.apk", "com.kt.ollehfamilybox.IntroActivity"])
    apk_list.append(["/Users/numa/temp/KT5/Ktmembership_AndroidMarket_DX.apk", "com.olleh.android.oc2.MainActivity"])
    apk_list.append(["/Users/numa/temp/KT5/sign_app-onestore-release-unsigned_DX.apk", "com.kt.android.showtouch.Loading"])
    for apk, activity in apk_list :
        #pass
        apk_installer.apk_install(apk)

    
        for a in range(2) :
        #while(True) :
            apk_runner = apkrunner.ApkRunner()
            apk_runner.set_apk([apk, ])
            apk_runner.apk_start_activity = activity

            #apk_runner.focused_limit.append(activity)

            device_finder.find_device_list()

            for device in device_finder.find_list :
                RunProcessWait("adb -s " + device + " logcat -c")
            apk_runner.time_limit = 10
            apk_runner.time_wait = 3
            apk_runner.apk_running()
            print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + "APK RUNNER END GO FILE CHECK" + Fore.RESET + Back.RESET + Style.NORMAL)


            for device in apk_runner.device_finder.find_list :
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
                    screen_cap = screencap.ScreenCap()
                    screen_cap.non_stop_screen_shot(device, apk_runner.temp_path, file_head + str(count) + png_tail)


            for device in apk_runner.device_finder.find_list :
                print(Fore.CYAN + Back.MAGENTA + Style.BRIGHT + "ONE STEP" + Fore.RESET + Back.RESET + Style.NORMAL)
                RunProcessWait("adb -s " + device + " shell am force-stop " + apk_runner.apk_name)
                #ce0416041472263c01
                #if os.path.isdir(apk_runner.temp_path + "2165c1582b017ece") :
                    #shutil.rmtree(apk_runner.temp_path + "2165c1582b017ece")
        apk_installer.apk_uninstall(apk)



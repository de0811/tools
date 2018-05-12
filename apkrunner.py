#!/usr/bin/python3
#-*-coding:utf-8-*-

import sys
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
from lib.androidinfo import *
from lib import option
from lib import common
from lib import logs
import config
import maapt
import devicefinder
import screencap
import copy

#권한 mFoucsed
#com.google.android.packageinstaller/com.android.packageinstaller.permission.ui.GrantPermissionsActivity

class ApkRunner :
    device_finder = devicefinder.DeviceFinder()
    time_limit = 0
    focused_limit = list()
    time_wait = 0
    apk_name = ""
    apk_start_activity = ""
    apk = ""
    #device_switch = dict()
    device_logs = logs.DeviceLogs()
    temp_path = ""
    def __init__(self) :
        self.device_finder = devicefinder.DeviceFinder()
        self.time_limit = 0                                 #정지되기 까지 시간 지정
        self.focused_limit = list()                        #정지될 activity focused list 보관
        self.time_wait = 0                                  #종료 규칙 후 대기 시간
        self.apk_name = ""                                  #apk 실제 이름
        self.apk_start_activity = ""                        #시작될 activity 지정
        self.apk = ""                                       #실행할 apk 설정
        #self.device_switch = dict()                         #모든 상황 종료 확인 스위치
        self.device_logs = logs.DeviceLogs()                #로그를 남기는 곳
        self.temp_path = ""                                 #작업할 위치
        
    def help(self, args) :
        hel = u'''
        python apkrunner.py [option] <.apk>
        [option]
        options grep name
        -d / -device : devices select
        -o / -os : os version select
        -s / -sdk : sdk version select
        -m / -manufacturer : manufacturer select 
        -mo / -model : model select
        -v / -view [view option] : devices Infomation
            [view option]
            all : all devices info
            device : view device
            os : view os
            sdk : view sdk
            manufacturer : view manufacturer
            model : view model
        '''
        print (hel)

    def set_time_limit(self, args) :
        try :
            self.time_limit = int(args[0])
        except ValueError :
            if args[0].lower() == 'all' :
                self.time_limit = 0
            else :
                print ("time_limit args Error!")
                sys.exit()
    
    def set_time_wait(self, args) :
        try :
            self.time_wait = int(args[0])
        except ValueError :
            print ("time_wait args Error!")
    
    def set_focused_limit(self, args) :
        if len(args) == 0 :
            return
        for arg in args :
            self.focused_limit.append(arg)
    
    def set_apk_name(self, args) :
        self.apk_name = args[0]
    def set_apk_start_activity(self, args) :
        self.apk_start_activity = args[0]
    def set_apk(self, args) :
        self.apk = args[0]
        aapt = maapt.aapt()
        aapt.aapt_parsing(self.apk)
        self.apk_name = aapt.package_name
        self.apk_start_activity = aapt.package_activity
    
    def __grant_permissions(self, device, dumpsys_window) :
        """__grant_permissions

        자동으로 앱의 권한을 허용
        Parameters
        ----------
        self: 
        device: 권한을 허용할 기기
        dumpsys_window: 

        Returns
        -------

        """   
        device_ui_info = DeviceUIInfo()
        device_ui_info.window_point_parsing(device, dumpsys_window.app_size_x, dumpsys_window.app_size_y)
        resource_info = device_ui_info.search_clickable_resource_id("com.android.packageinstaller:id/permission_allow_button")
        RunProcessWait("adb -s " + device + " shell input tap " + str(resource_info.x1 + ((resource_info.x2 - resource_info.x1) / 2)) + " " + str(resource_info.y1 + ((resource_info.y2 - resource_info.y1)/2)))
    
    def __screencap(self, device, device_path, screen_count, dumpsyswindow, run_timer) :
        #time.sleep(0.0)
        #self.device_logs.append(device, "focused", dumpsyswindow.mFocused, run_timer.second_tab())
        self.device_logs.append(device, "focused", dumpsyswindow.mFocused, run_timer.second_full_tab())
        file_name = str(screen_count) + "_" + dumpsyswindow.mFocused
        file_name = file_name.replace('/', '_') + ".png"
        file_name = file_name.replace(' ', '_')
        #print (file_name)
        screen_cap = screencap.ScreenCap()
        #screen_cap.non_stop_screen_shot(device, device_path, file_name)
        #################################################################################
        with ThreadPoolExecutor(max_workers=1) as exe:
            exe.submit(screen_cap.non_stop_screen_shot, device, device_path, file_name)
            exe.shutdown(wait=False)
        #################################################################################
        screen_count = screen_count + 1

    def multi_processing(self, device) :
        """multi_processing

        각 기기 별로 프로세스 형태로 돌아감
        CPU를 모두 점유해서 사용하기 위함
        그러니 따로 사용하지 말고 apk_running으로 동작 시키는 것을 추천
        Parameters
        ----------
        self: 
        device: 동작을 진행할 기기

        Returns
        -------

        """
        #device 상태 저장
        #self.device_switch.setdefault(device, True)

        is_time_wait = False    #모두 종료 후 대기 시간으로 넘어감
        #screencap 설정
        device_path = self.temp_path + device
        if os.path.isdir(device_path) == False :
            os.mkdir(device_path)
        else :
            count = 0
            while(True)  :
                if os.path.isdir(device_path + "_" + str(count)) == True :
                    count = count + 1
                    continue
                else :
                    break
            device_path = device_path + "_" + str(count) + os.sep
            os.mkdir(device_path)
        self.device_logs.append(device, "State", "DevicePath:" + device_path, 0)
        print ("::::::::::::::::::::" + device_path + "::::::::::::::::::::::::::")
        

        screen_count = 0

        #종료 조건에 홈화면이 나올 경우도 추가
        private_focused_limit = copy.deepcopy(self.focused_limit)
        home_dumpsyswindow = DumpsysWindow(device)
        private_focused_limit.append(home_dumpsyswindow.mFocused)

        #시간 점검 변수들 생성
        run_timer = common.Timer()
        grant_timer = common.Timer()
        run_timer.start()
        time_focused = 0
        #시~작~
        self.device_logs.append(device, "State", "Start", run_timer.second_full_tab())
        adb = "adb -s " + device + " "
        #print ("start activity : " + self.apk_start_activity)
        RunProcessOut(adb + "shell am start -n " + self.apk_name + '/' + self.apk_start_activity + " -a android.intent.action.MAIN -c android.intent.category.LAUNCHER")
        while True :
            time.sleep(0.1)
            dumpsyswindow = DumpsysWindow(device)

            #새로운 화면일 시 저장
            focused_list = self.device_logs.find_event(device, "focused")
            if len( focused_list ) :
                #print ("focused :: " + focused_list[-1].dist)
                if focused_list[-1].dist.lower().find(dumpsyswindow.mFocused.lower()) == -1 :
                    self.__screencap(device, device_path, screen_count, dumpsyswindow, run_timer)
            else :
                self.__screencap(device, device_path, screen_count, dumpsyswindow, run_timer)


            #권한 처리 (권한 화면 일 시 4초 뒤에 처리) - 소장님 의견으로는 권한 화면일 시 내부 처리에 오류가 많이 나기 때문에 일정 시간의 대기를 가지고 확인하는게 좋다고 함
            if dumpsyswindow.is_grant_activity == True :
                if grant_timer.is_running == False :
                    self.device_logs.append(device, "grant_permission", "wait grant", run_timer.second_full_tab())
                    run_timer.pause()
                    grant_timer.start()
                elif grant_timer.second_tab() > 4 :
                    self.device_logs.append(device, "grant_permission", "click grant", run_timer.second_full_tab())
                    self.__grant_permissions(device, dumpsyswindow)
                    run_timer.start()
                    grant_timer.stop()
                continue

            #print ("is Dump State : " + str(dumpsyswindow.isFocusedError()) + "  ::  " + dumpsyswindow.mFocused)
            if dumpsyswindow.isFocusedError() == True :
                self.device_logs.append(device, "focused_Error", dumpsyswindow.mFocused, run_timer.second_full_tab())
                is_time_wait = True
                break

            if is_time_wait != True :
                #정지 조건 시간
                if self.time_limit > 0 :
                    print (run_timer.second_tab())
                    if run_timer.second_tab() > self.time_limit :
                        is_time_wait = True

                #정지 조건 activity
                for focused in private_focused_limit :
                    #print ("current Focused :: " + dumpsyswindow.mFocused + "   find focused :: " + focused + "  is same :: " + str( dumpsyswindow.mFocused.find(focused) != -1 ))
                    if dumpsyswindow.mFocused.find(focused) != -1 :
                        is_time_wait = True
                        time_focused = run_timer.second_tab()
                        break

            #wait time
            if is_time_wait :
                #제한시간을 넘었을 경우 종료
                if run_timer.second_tab() > self.time_limit + self.time_wait :
                    break;
                #제한 화면을 넘었을 경우 종료
                elif time_focused > 0 and run_timer.second_tab() > time_focused + self.time_wait :
                    break;

        #로그 정리
        print ("END APKRUNNER!!!")
        self.device_logs.append(device, "State", "End", run_timer.second_full_tab())
   
    def apk_running(self) :
        """apk_running

        전체적인 동작을 진행
        Parameters
        ----------
        self: 

        Returns
        -------
        """   
        if self.apk_name == "" or self.apk_start_activity == "" :
            print ("None APK Error !!")
            sys.exit()
        self.temp_path = config.temp_path + self.apk_name + os.sep
        if os.path.isdir(self.temp_path) == False :
            os.mkdir(self.temp_path)
        self.device_finder.find_device_list()

        #####################################################
        print ("Process Count :: " + str(len(self.device_finder.find_list)))
        with ProcessPoolExecutor(max_workers=len(self.device_finder.find_list)) as exe:
            for device in self.device_finder.find_list :
                exe.submit(self.multi_processing, device)
                time.sleep(0.1)
                print ("Running apk " + device)
            exe.shutdown(wait=True)
        #####################################################
        print ("OUT APK_RUNNER")

    def run(self, args):
        self.apk_running()

if __name__ == "__main__":
    apk_runner = ApkRunner()
    device_finder = apk_runner.device_finder
    opt = option.option()
    #def addOpt(self, opt, argCount, bVarArg, func):
    opt.addOpt(opt="-h", argCount=0, bVarArg=False, bHelp=True, func=apk_runner.help)
    opt.addOpt(opt="-d", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_device)
    opt.addOpt(opt="-o", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_os)
    opt.addOpt(opt="-os", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_os)
    opt.addOpt(opt="-s", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_sdk)
    opt.addOpt(opt="-sdk", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_sdk)
    opt.addOpt(opt="-m", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_manufacturer)
    opt.addOpt(opt="-manufacturer", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_manufacturer)
    opt.addOpt(opt="-mo", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_model)
    opt.addOpt(opt="-model", argCount=20, bVarArg=False, bHelp=False, func=device_finder.select_model)
    opt.addOpt(opt="-v", argCount=1, bVarArg=False, bHelp=True, func=device_finder.view)
    opt.addOpt(opt="-view", argCount=1, bVarArg=False, bHelp=True, func=device_finder.view)

    opt.addOpt(opt="-t", argCount=1, bVarArg=True, bHelp=False, func=apk_runner.set_time_limit)
    opt.addOpt(opt="-time", argCount=1, bVarArg=True, bHelp=False, func=apk_runner.set_time_limit)
    opt.addOpt(opt="-tw", argCount=1, bVarArg=True, bHelp=False, func=apk_runner.set_time_wait)
    opt.addOpt(opt="-timewait", argCount=1, bVarArg=True, bHelp=False, func=apk_runner.set_time_wait)
    opt.addOpt(opt="-apk", argCount=1, bVarArg=True, bHelp=False, func=apk_runner.set_apk)
    opt.addOpt(opt="-f", argCount=20, bVarArg=False, bHelp=False, func=apk_runner.set_focused_limit)
    opt.addOpt(opt="-focusedlimit", argCount=20, bVarArg=False, bHelp=False, func=apk_runner.set_focused_limit)
    opt.addOpt(opt="default", argCount=0, bVarArg=True, bHelp=False, func=apk_runner.run)
    test = ['-os', '6.0', '/home/num/temp/scheduler.apk']
    #test = ['-v',]
    test = ['-v', 'model' ]
    test = ['-os', '6.0', '-mo', 'nexus', '/home/num/temp/com.bizmeka.ezmessenger.apk']
    test = ['/home/num/temp/error_apk.apk']
    test = ['-apk', '/Users/numa/temp/ez_no_log.apk', '-t', '8']
    #opt.parsing(test)
    opt.parsing()
    #opt.tprint()
    opt.run()
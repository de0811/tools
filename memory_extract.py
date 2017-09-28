#!/usr/bin/python
#-*-coding:utf-8-*-


from subprocess import *
import os
import sys
import shutil
import config
from lib import option

print "temp_memCopy.py runing"

def RunProcess(cmd):
    cmd_args = cmd.split()
    pipe = Popen(cmd_args, stdout=PIPE, stderr=STDOUT)
    outList = pipe.stdout.readlines()
    return outList

'''
해당 패키지의 실행동안 메모리를 추출
'''
#메모리 모두 다 뽑아서 비교할 예정
#변경된 앱이 죽지 않게 멈추게 하기
#그동안 메모리에 있는 내용 모두 뽑기
'''
    현재 PID 알아내기
    PID stop
'''
if __name__ == "__main__":
    args = sys.argv[1:]
    packageName = args[0]
    #packageName = 'com.barclays.android.barclaysmobilebanking'

    cmd = 'adb shell ps | grep ' + packageName
    out = RunProcess(cmd)

    pid = ' '.join( out[0].split(' ')[1:] ).strip().split(' ')[0] 

    print pid

    cmd = 'adb shell xux -0 scrdump -stop ' + pid
    #print cmd
    RunProcess(cmd)

    cmd = 'adb shell xux -0 cat /proc/' + pid + '/maps | grep ' + packageName
    out = RunProcess(cmd)

    pac = list()
    for line in out :
        #print line
        addr = line.split(' ')[0]
        name = line.split(' ')[9].strip()
        boo = 0
        for l in pac:
            if l[0] == name:
                l[1].append(addr)
                boo = 1
        if boo == 0 :
            pac.append([name, [addr]])

    pack = list()
    for l in pac:
        if len(l[1]) > 1 :
            arr = list()
            for a in l[1]:
                arr.append( int(a.split('-')[0], 16) )
                arr.append( int(a.split('-')[1], 16) )
            arr.sort()
            #print hex(arr[0])
            pack.append([ l[0], hex(arr[0])[:-1], hex(arr[-1])[:-1] ])
            
            #print arr
        else :
            min = l[1][0].split('-')[0]
            max = l[1][0].split('-')[1]
            pack.append([ l[0], hex(min)[:-1], hex(max)[:-1] ])

    #print pack

    cmd = 'adb shell xux -0 mkdir /sdcard/' + packageName
    RunProcess(cmd)
    for l in pack :
        cmd = 'adb shell xux -0 scrdump -sdump ' + pid + ' ' + l[1] + ' ' + l[2]
        RunProcess(cmd)
        cmd = 'adb shell xux -0 mv /data/local/tmp/mem.dump /sdcard/' + packageName + '/' + 'mem_' + l[0].split('/')[-1]
        RunProcess(cmd)
        

    cmd = 'adb shell xux -0 scrdump -start ' + pid
    #print cmd
    RunProcess(cmd)

















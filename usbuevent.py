#!/usr/bin/python
#-*-coding:utf-8-*-

from subprocess import *
import sys
import os

def RunProcess(cmd):
    cmd_args = cmd.split()
    print "cmd _ args"
    print cmd_args
    pipe = Popen(cmd_args, stdout=PIPE)
    return pipe.stdout.read();
    #print pipe.stderr.read();
    #process = Popen(cmd_args)
    #while pipe.poll() is None:
    #    pass
        #print('working..')
    #print process.poll()


if __name__ == "__main__":
    args = sys.argv[1:]
    devices_name = args[0]
    filename = 'C:\\temp\\work\\usb_conn\\' + devices_name + '_'
    tail = '.txt'
    idx = 0
    while 1:
        if os.path.isfile(filename + str(idx) + tail):
            idx =+ 1
        else : break
    filename = filename + str(idx) + tail
    ff = open(filename, 'w')
    
    cmd = 'C:\\Android\\sdk\\platform-tools\\adb -d shell cat /sys/class/power_supply/usb/uevent'
    print cmd
    result = RunProcess(cmd)
    
    ff.write(result)
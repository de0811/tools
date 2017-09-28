#!/usr/bin/python
#-*-coding:utf-8-*-

import sys
import os
import stat


if __name__ == "__main__":
    fd = open("C:\\temp\\work\\kakao\\read.txt", 'rb')
    print "adb shell xux 0 mount -o rw,remount /system"
    while True:
        line = fd.readline()
        if not line: break
        #print "-------------------"
        #print line[0:len(line)-1]
        #print "-------------------"
        line = line[0:len(line)-1]
        fname = os.path.split(line)
        winpath = fname[0][29:]
        #print winpath.split("\\")
        andpath = '/'.join(winpath.split("\\"))
        print "adb shell xux 0 mkdir /" + andpath
        print "adb push " + line + " /sdcard/" + fname[1]
        print "adb shell xux 0 mv -f /sdcard/" + fname[1] + " /" + andpath# + fname[1]
        print "adb shell xux 0 chmod 777 /" + andpath + "/" + fname[1]
        print "adb shell xux 0 rm -rf /sdcard/" + fname[1]
    print "adb reboot"
    fd.close()

#!/usr/bin/python3
#-*-coding:utf-8-*-

import sys
import config
from lib.runprocess import *
from lib import option

class ApkViewer :
    OPT = "JADX"
    def __init__(self) :
        self.OPT = "JADX"
    def help(self) :
        hel = u'''
        apkview [option] <apk>
        default 실행 파일은 jadx 입니다.
        -b : 바이트 코드를 실행합니다.
        -j : jad를 실행합니다.
        -x : default 실행 파일인 jadx를 실행합니다.
        '''
        print (hel)
    def bytecode_viewer(self, target):
        cmd = config.bytecode + " " + target
        print (cmd)
        RunProcessPrints(cmd)

    def jad_viewer(self, target):
        cmd = config.jad + " " + target
        print (cmd)
        RunProcessPrints(cmd)

    def jadx_viewer(self, target):
        cmd = config.jadx + " " + target
        print (cmd)
        RunProcessPrints(cmd)
    
    def set_OPT_byte(self, args) :
        self.OPT = "BYTE"
    def set_OPT_jad(self, args) :
        self.OPT = "JAD"
    def set_OPT_jadx(self, args) :
        self.OPT = "JADX"
    def run(self, args) :
        if len(args) != 1 :
            print ("args Error")
            return
        if  self.OPT == "BYTE" :
            self.bytecode_viewer(args[0])
        elif self.OPT == "JAD" :
            self.jad_viewer(args[0])
        elif self.OPT == "JADX" :
            self.jadx_viewer(args[0])


if __name__ == "__main__":
    apkview = ApkViewer()
    opt = option.option()
    opt.addOpt(opt="-h", argCount=0, bVarArg=True, bHelp=True, func=apkview.help)
    opt.addOpt(opt="-b", argCount=0, bVarArg=True, bHelp=False, func=apkview.set_OPT_byte)
    opt.addOpt(opt="-j", argCount=0, bVarArg=True, bHelp=False, func=apkview.set_OPT_jad)
    opt.addOpt(opt="-x", argCount=0, bVarArg=True, bHelp=False, func=apkview.set_OPT_jadx)
    opt.addOpt(opt="default", argCount=1, bVarArg=True, bHelp=False, func=apkview.run)
    opt.parsing()
    opt.run()

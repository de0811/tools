#!/usr/bin/python3
#-*-coding:utf-8-*-

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from subprocess import *
import shutil
import config
from lib import option
from lib.runprocess import *

print ("apktool.py runing")


def ApkDeCompile(option, target):
    cmd = config.apktool + " " + option + " " + target
    print (cmd)
    RunProcessPrints(cmd)
#    for line in RunProcess(cmd):
#        print line

def Signer(target):
    cmd = config.signer + " " + config.key + " " + config.keyPass + " " + target + " " + config.alias
    print (cmd)
    RunProcessPrints(cmd)
#    for line in RunProcess(cmd):
#        print line

class apptool :
    AUTO = 0
    DECOMPILE = 1
    COMPILE = 2
    SIGN = 3
    COMSIG = 4

    mState = AUTO
    mOut = ""
    def setDecompile(self, args):
        self.mState = self.DECOMPILE
    def setCompile(self, args):
        self.mState = self.COMPILE
    def setSign(self,args):
        self.mState = self.SIGN
    def setComSig(self, args):
        self.mState = self.COMSIG
    def setOut(self, args):
        if len(args) == 0: return
        self.mOut = args[0]

    def _runDecompile(self, target):
        option = 'd -o '
        if self.mOut == "":
            option = option + os.path.splitext(target)[0]
        else :
            option = option + self.mOut
        ApkDeCompile(option, target)

    def _runComSig(self, target):
        self._runCompile(target)
        apk = os.path.basename(target)
        apk = target + os.sep + 'dist' + os.sep + apk + '.apk'
        Signer(apk)

    def _runCompile(self, target):
        option = 'b'
#        dist = target + os.sep + 'dist'
#        build = target + os.sep + 'build'
#        if os.path.exists(dist) == 1:
#            shutil.rmtree(target + os.sep + 'dist')
#            print 'rm dist'
#        if os.path.exists(build) == 1:
#            shutil.rmtree(target + os.sep + 'build')
#            print 'rm build'
        ApkDeCompile(option, target)

    def run(self, args):
        if len(args) < 1 : return
        print ("Cur State : " + str(self.mState))
        if self.mState is self.AUTO:
            if '.apk' in args[0]:
                self._runDecompile(args[0])
            elif '.zip' in args[0]:
                Signer(args[0])
            else:
                self._runComSig(args[0])

        elif self.mState is self.COMPILE:
            self._runCompile(args[0])
        elif self.mState is self.DECOMPILE:
            self._runDecompile(args[0])
        elif self.mState is self.SIGN:
            Signer(args[0])
        elif self.mState is self.COMSIG:
            self._runComSig(args[0])

    def help(self, args):
        hel = u'''apptool.py [command] [target]
        [command]
        -h : 설명을 나타냅니다
        -o : -d를 사용할때만 적용되며 디컴파일될 파일의 위치를 지정합니다
        -s : 서명을 진행합니다
        -b : 컴파일을 진행합니다
        -d : 디컴파일을 진행합니다
        아무런 command를 작성하지 않는다면 target의 상태를 보고 알아서 진행합니다
        '''
        print (hel)
        sys.exit()


if __name__ == "__main__":
    app = apptool()
    opt = option.option()
    
    #def addOpt(self, opt, argCount, bVarArg, func):
    opt.addOpt(opt="-h", argCount=0, bVarArg=False, bHelp=True, func=app.help)
    opt.addOpt(opt="-o", argCount=1, bVarArg=False, bHelp=False, func=app.setOut)
    opt.addOpt(opt="-s", argCount=0, bVarArg=False, bHelp=False, func=app.setSign)
    opt.addOpt(opt="-b", argCount=0, bVarArg=False, bHelp=False, func=app.setCompile)
    opt.addOpt(opt="-d", argCount=0, bVarArg=False, bHelp=False, func=app.setDecompile)
    opt.addOpt(opt="-bs", argCount=0, bVarArg=False, bHelp=False, func=app.setComSig)	
    opt.addOpt(opt="default", argCount=1, bVarArg=True, bHelp=False, func=app.run)
    opt.parsing()
    #opt.tprint()
    opt.run()



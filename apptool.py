#!/usr/bin/python
from subprocess import *
import os
import sys
import shutil
import config
from lib import option

print "apktool.py runing"

def RunProcess(cmd):
    cmd_args = cmd.split()
    #pipe = Popen(cmd_args, stdout=PIPE, stderr=PIPE)
    #print pipe.stdout.read();
    #print pipe.stderr.read();
    process = Popen(cmd_args)
    while process.poll() is None:
        pass
        #print('working..')
    print process.poll()

'''
def RunProcess(cmd):
#    print(Fore.BLUE + Back.LIGHTCYAN_EX + Style.BRIGHT + cmd + Fore.RESET + Back.RESET + Style.NORMAL)
    cmd_args = cmd.split()
    pipe = Popen(cmd_args, stdout=PIPE, stderr=STDOUT)
    outList = pipe.stdout.readlines()
    return outList
'''
def ApkDeCompile(option, target):
    cmd = config.apktool + " " + option + " " + target
    print cmd
    RunProcess(cmd)
#    for line in RunProcess(cmd):
#        print line

def Signer(target):
    cmd = config.signer + " " + config.key + " " + config.keyPass + " " + target + " " + config.alias
    print cmd
    RunProcess(cmd)
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
        if len(args) == 0: return
        self.mState = self.DECOMPILE
    def setCompile(self, args):
        if len(args) == 0: return
        self.mState = self.COMPILE
    def setSign(self,args):
        if len(args) == 0: return
        self.mState = self.SIGN
    def setComSig(self, args):
        if len(args) == 0: return
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
        print "Cur State : " + str(self.mState)
        if self.mState is self.AUTO:
            if '.apk' in args[0]:
                self._runDecompile(args[0])
            elif '.zip' in args[0]:
                Signer(args[0])
            else:
                self._runComSig(args[0])

        elif self.mState is self.DECOMPILE:
            self._runDecompile(args[0])
        elif self.mState is self.SIGN:
            Signer(args[0])
        elif self.mState is self.COMSIG:
            self._runComSig(args[0])


if __name__ == "__main__":
    app = apptool()
    opt = option.option()
    opt.addOpt("-o", 1, app.setOut)
    opt.addOpt("-s", 0, app.setSign)
    opt.addOpt("-b", 0, app.setCompile)
    opt.addOpt("-d", 0, app.setDecompile)
    opt.addOpt("-bs", 0, app.setComSig)	
    opt.addOpt("default", 1, app.run)
    opt.parsing()
    opt.tprint()
    opt.run()










































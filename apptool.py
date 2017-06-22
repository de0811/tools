#!/usr/bin/python
from subprocess import *
import os
import sys
import shutil
import config

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

def CainRunProcess(cmd):
    result = RunProcess(cmd)
    if result == 1:
        print '''Process Error'''
        sys.exit()

def ApkDeCompile(option, target):
    cmd = config.apktool + " " + option + " " + target
    print cmd
    CainRunProcess(cmd)

def Signer(target):
    cmd = config.signer + " " + config.key + " " + config.keyPass + " " + target + " " + config.alias
    print cmd
    CainRunProcess(cmd)



if __name__ == "__main__":

    args = sys.argv[1:]
    if args[0].startswith('-'):
        if args[0].endswith('s'):
            target = args[1]
            Signer(target)
            sys.exit()


    target = args[0]

    option = '''d'''

    print 'current target : ' + target

    if '.apk' in target:
        print '-----find .apk-----'
        option = 'd -o '
        option = option + os.path.splitext(target)[0]
        ApkDeCompile(option, target)
    elif '.zip' in target:
        print '-----find .zip-----'
        Signer(target)
    else:
        print '-----Not Find-----'
        option = 'b'
        dist = target + os.sep + 'dist'
        build = target + os.sep + 'build'
        if os.path.exists(dist) == 1:
            shutil.rmtree(target + os.sep + 'dist')
            print 'rm dist'
        if os.path.exists(build) == 1:
            shutil.rmtree(target + os.sep + 'build')
            print 'rm build'
        ApkDeCompile(option, target)

        apk = os.path.basename(target)
        apk = target + os.sep + 'dist' + os.sep + apk + '.apk'
        if os.path.isfile(apk) :
            Signer(apk)







































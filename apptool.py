#!/usr/bin/python
from subprocess import *
import os
import sys
import shutil

print "apktool.py runing"

def RunProcess(cmd):
    cmd_args = cmd.split()
    pipe = Popen(cmd_args, stdout=PIPE, stderr=PIPE)
    print pipe.stdout.read();
    print pipe.stderr.read();

def ApkDeCompile(option, target):
    apktool = '''java -jar /home/numa/Android/utill/apktool.jar'''
    cmd = apktool + " " + option + " " + target
    print cmd
    RunProcess(cmd)

def Signer(target):
    signer = 'jarsigner -verbose -sigalg MD5withRSA -digestalg SHA1 -keystore'
    key = '/home/numa/Android/keystore/testsig.jks'
    keyPass = '-storepass 123456'
    alias = 'testsig'

    cmd = signer + " " + key + " " + keyPass + " " + target + " " + alias
    print cmd
    RunProcess(cmd)



if __name__ == "__main__":

    args = sys.argv[1:]
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
        Signer(apk)







































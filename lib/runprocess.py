#!/usr/bin/python
#-*-coding:utf-8-*-

from subprocess import *
import os
import time

currentFilePath = os.path.dirname(os.path.realpath(__file__))
#mainDir = dirName = currentFilePath + os.sep + ".." + os.sep + "temp"

'''
class RunProcess() : 
    u"""한줄 프로세스 실행 코드"""
    currentFilePath = os.path.dirname(os.path.realpath(__file__))
    def play(self, cmd) :
        cmd_args = cmd.split()
        
    pass
'''

def RunProcess(cmd):
    print (cmd)
    cmd_args = cmd.split()
    Popen(cmd_args)

def RunProcessPipe(cmd):
    pi = open(currentFilePath + "/temp.txt", 'w')
    cmd_args = cmd.split()
    Popen(cmd_args, stdout=pi, stderr=pi)
    pi.close()

def RunProcessOut(cmd):
    #print (cmd)
    cmd_args = cmd.split()
    pipe = Popen(cmd_args, stdout=PIPE, stderr=STDOUT)
    outList = pipe.stdout.readlines()
    return outList

def RunProcessOutPipe(filePath, cmd):
    cmd_args = cmd.split()
    f = open(filePath, "w")
    pipe = Popen(cmd_args, stdout=f, stderr=f)
    while pipe.poll() is None :
        pass
    f.close()

def RunProcessWait(cmd):
    print (cmd)
    cmd_args = cmd.split()
    process = Popen(cmd_args)
    while process.poll() is None:
        pass
    #print process.poll()

def RunProcessPipeWait(cmd):
    pi = open(currentFilePath + "/temp.txt", 'w')
    cmd_args = cmd.split()
    process = Popen(cmd_args, stdout=pi, stderr=pi)
    while process.poll() is None:
        time.sleep(0.1)
        pass
    pi.close()

def RunProcessPrints(cmd):
    cmd_args = cmd.split()
    process = Popen(cmd_args)
    while process.poll() is None:
        pass
    print (process.poll())


if __name__ == "__main__":
    cmd = "echo \"helloooooooow???\""
    cmd_args = cmd.split()
    pi = open("/tmp/temp.txt", 'w')
    cmd_args = cmd.split()
    pipe = Popen(cmd_args, stdout=pi, stderr=pi)
    outList = pipe.stdout.readlines()
    print (outList)
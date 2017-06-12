#!/usr/bin/python

from subprocess import *
import os
import sys
import shutil
import config

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

def BytecodeViewer(target):
    cmd = config.bytecode + " " + target
    print cmd
    RunProcess(cmd)

def jadViewer(target):
    cmd = config.jad + " " + target
    print cmd
    RunProcess(cmd)

def jadxViewer(target):
    cmd = config.jadx + " " + target
    print cmd
    RunProcess(cmd)

if __name__ == "__main__":

    args = sys.argv[1:]
    if args[0].startswith('-'):
        if args[0].endswith('b'):
            target = args[1]
            BytecodeViewer(target)
            sys.exit()
        elif args[0].endswith('j'):
            target = args[1]
            jadViewer(target)
            sys.exit()
        elif args[0].endswith('x'):
            target = args[1]
            jadxViewer(target)
            sys.exit()

    jadxViewer(args[0])

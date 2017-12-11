#!/usr/bin/python
#-*-coding:utf-8-*-

from subprocess import *
import sys
import config
from lib.runprocess import *

def BytecodeViewer(target):
    cmd = config.bytecode + " " + target
    print cmd
    RunProcessPrints(cmd)

def jadViewer(target):
    cmd = config.jad + " " + target
    print cmd
    RunProcessPrints(cmd)

def jadxViewer(target):
    cmd = config.jadx + " " + target
    print cmd
    RunProcessPrints(cmd)

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

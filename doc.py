#!/usr/bin/python
#-*-coding:utf-8-*-

import sys

if __name__ == "__main__":
    args = sys.argv[1:]
    fileName = args[0]
    
    bak = fileName + '.bak'
    fBak = open(bak, 'w')
    
    fTarget = open(fileName, 'r')
    lines = fTarget.readlines()
    for tLine in lines:
        tLine = tLine.replace("    ", "  ")
        tLine = tLine.replace("\t", "  ")
        fBak.write(tLine)
    
    #print "a  a  a  a".replace(" ", "bbb")
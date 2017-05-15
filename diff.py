#!/usr/bin/python
import sys
import os
import stat

def getDirList(dir):
    fList = list()
    for root, dirs, files in os.walk(dir):
        for fname in files:
            print 'root : ', root
            print 'dirs : ', dirs
            fullpath = os.path.join(root, fname)
            fList.append(fullpath[len(dir):])
    return fList


def diffDirList(lh, rh):
    coprimeList = list()
    unionList = list()
    rMaxCount = len(rh)
    for l in lh:
        rCount = 0
        while True:
            if l == rh[rCount]:
                unionList.append(l)
                break
            else: rCount = rCount + 1
            if rCount == rMaxCount:
                coprimeList.append(l)
                break
    return unionList, coprimeList

def compSize(lh_root, rh_root, unionList):
    comp = list()
    for union in unionList:
        if os.stat(lh_root + union)[stat.ST_SIZE] != os.stat(rh_root + union)[stat.ST_SIZE]:
            comp.append(union)
            del(union)
    return comp

def compValues(lh_root, rh_root, unionList):
    comp = list()
    for union in unionList:
        lf = open(lh_root + union, 'rb')
        rf = open(rh_root + union, 'rb')
        lLine = lf.xreadlines()
        rLine = rf.xreadlines()
        while lLine or rLine:
            if lLine != rLine:
                comp.append(union)
                break
            lLine = lf.readline()
            rLine = rf.readline()
    return comp


if __name__ == "__main__":
    args = sys.argv[1:]
    print args
    if not args:
        print 'Not Command'
        sys.exit()
    if args[0].startswith('-'):
        print 'not option'
        sys.exit()
    lh, rh = args[0], args[1]

    lh_list = getDirList(lh)
    rh_list = getDirList(rh)

    unionList, lh_coprimeList = diffDirList(lh_list, rh_list)
    unionList, rh_coprimeList = diffDirList(lh_list, rh_list)

    compSize = compSize(lh, rh, unionList)
    
    print 'compSize : ', compSize

    compValue = compValues(lh, rh, unionList)
    print 'compValue : ', compValue
    







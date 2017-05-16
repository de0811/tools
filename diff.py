#!/usr/bin/python
import sys
import os
import stat

def getDirList(dir):
    fList = list()
    for root, dirs, files in os.walk(dir):
        for fname in files:
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

def compSizes(lh_root, rh_root, unionList):
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
        lLine = lf.readline()
        rLine = rf.readline()
        while lLine or rLine:
            if lLine != rLine:
                comp.append(union)
                break
            lLine = lf.readline()
            rLine = rf.readline()
    return comp

def diffDir(lh, rh):
    lh_list = getDirList(lh)
    rh_list = getDirList(rh)

    print '-------------------------------------------------------'
    print 'lh_coprimeList'
    unionList, lh_coprimeList = diffDirList(lh_list, rh_list)
    for value in lh_coprimeList:
        print lh + value

    print '-------------------------------------------------------'
    print 'rh_coprimeList'
    unionList, rh_coprimeList = diffDirList(lh_list, rh_list)
    for value in rh_coprimeList:
        print rh + value
	
    compSize = compSizes(lh, rh, unionList)
    print '-------------------------------------------------------'
    print 'compSize'
    #print 'compSize : ', compSize
    for value in compSize:
        print value

    print '-------------------------------------------------------'
    print 'compValue'
    compValue = compValues(lh, rh, unionList)
    #print 'compValue : ', compValue
    for value in compValue:
        print value

def diffFile(lh, rh):
    pass


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

    if os.path.isdir(lh) and os.path.isdir(rh):
        diffDir(lh, rh)
    elif os.path.isfile(lh) == True and os.isfile(rh) == True:
        diffFile(lh, rh)




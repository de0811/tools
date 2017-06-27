
#-*-coding:utf-8-*-

import sys
def diffFileLine(lfLine, rfLine):
    minLine = min(len(lfLine), len(rfLine))
    errIdx = -1
    for idx in range(minLine):
        if lfLine[idx] != rfLine[idx]:
            errIdx = idx
            return errIdx
    print "Err) Not is Index !"
    return errIdx

def sameData16(lf, rf):
    lfLine = lf.read(16)
    rfLine = rf.read(16)
    bResult = lfLine == rfLine
    #print "S : ", lf.tell(), rf.tell()
    #print "lfLn : ", lfLine, "rfLn : ", rfLine
    lf.seek(lf.tell() - len(lfLine))
    rf.seek(rf.tell() - len(rfLine))
    print "E : ", lf.tell(), rf.tell()
    return bResult

def findSameData(lf, rf, lfEnd=0, rfEnd=0):
    lfPoint = lf.tell()
    rfPoint = rf.tell()
    if lfEnd == 0 or rfEnd == 0:
        lf.seek(0, 2)
        rf.seek(0, 2)
        lfEnd = lf.tell() #ClassMember
        rfEnd = rf.tell() #ClassMember

    print "lfEnd : ", lfEnd, "rfEnd", rfEnd
    print "findSame lfPoint : ", lfPoint, "rfPoint : ", rfPoint
    lf.seek(lfPoint)
    rf.seek(rfPoint)
    totalCount = 0
    while lf.tell() < lfEnd and rf.tell() < rfEnd:
        lByte = lf.read(1)
        rByte = rf.read(1)
        lf.seek(lf.tell()-1)
        rf.seek(rf.tell()-1)

        while lf.tell() < lfEnd and rf.tell() < rfEnd:
            if lByte == rf.read(1):
                temp = lf.tell()
                lf.seek(lfPoint + totalCount)
                rf.seek(rf.tell() - 1)
                if sameData16(lf, rf):
                    lf.seek(lfPoint + totalCount)
                    return
                else :
                    rf.seek(rf.tell() + 1)
                    lf.seek(temp)
            if rByte == lf.read(1):
                temp = rf.tell()
                rf.seek(rfPoint + totalCount)
                lf.seek(lf.tell() - 1)
                if sameData16(lf, rf):
                    rf.seek(rfPoint + totalCount)
                    return
                else :
                    lf.seek(lf.tell() + 1)
                    rf.seek(temp)
            lf.seek(lf.tell() + 1)
            rf.seek(rf.tell() + 1)

        totalCount = totalCount + 1
        lf.seek(lfPoint + totalCount)
        rf.seek(rfPoint + totalCount)

class DiffPosition:
    start = 0
    end = 0
    def __init__(self, start, end):
        self.start = start
        self.end = end

def diffFile(lh, rh):
    lf = open(lh, 'rb')
    rf = open(rh, 'rb')
    lfDiffList = list()
    rfDiffList = list()
    lfStmp = 0
    rfStmp = 0
     
    lf.seek(0, 2)
    rf.seek(0, 2)
    lfEnd = lf.tell() #ClassMember
    rfEnd = rf.tell() #ClassMember
    lf.seek(0)
    rf.seek(0)

    while lf.tell() < lfEnd and rf.tell() < rfEnd:
        lfLine = lf.read(16)
        rfLine = rf.read(16)

        if lfLine != rfLine:
            subByte = diffFileLine(lfLine, rfLine)
            lf.seek( lf.tell() - (len(lfLine) - subByte) )
            rf.seek( rf.tell() - (len(rfLine) - subByte) )
            lfStmp = lf.tell()
            rfStmp = rf.tell()
            print lfStmp, rfStmp
            findSameData(lf, rf, lfEnd, rfEnd)
            print lf.tell(), rf.tell()
            lfDiffList.append(DiffPosition(lfStmp, lf.tell()))
            rfDiffList.append(DiffPosition(rfStmp, rf.tell()))
        #print "cur : ", lf.tell(), "    end : ", lfEnd
            
    print "----- Diff -----"
    pCount = min(len(lfDiffList), len(rfDiffList))
    for cc in range(pCount):
        print "(", lfDiffList[cc].start, lfDiffList[cc].end, ")", "(", rfDiffList[cc].start, rfDiffList[cc].end, ")"
    print "------------------"
    
   
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

    diffFile(lh, rh)

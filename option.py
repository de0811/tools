#!/usr/bin/python
import sys

class option:
    mOptInfos = list()
    mOptFactor = dict()

    def __init__(self):
        pass

    def parsing(self, args):
        for i in range(len(args)):
            for info in self.mOptInfos:
                if info[0] == args[i]:
                    optArgs = list()
                    if (i + info[1]) < len(args):
                        for k in range(info[1]):
                            i = i + 1
                            optArgs.append(args[i])
                    else : return False
                    self.mOptFactor.setdefault(info[0], optArgs)
    
    def run(self):
        pass

    def addOpt(self, opt, argCount, func):
        self.mOptInfos.append((opt, argCount, func))

    def tprint(self):
        print "mOptInfos : "
        print self.mOptInfos
        print "mOptFactor : "
        print self.mOptFactor

def test1(str1, str2, str3):
    print str1 + str2 + str3


if __name__ == "__main__":
    args = ["1111", "2222", "3333", "4444"]
    opt = option()
    opt.addOpt("1111", 4, test1)
    if False == opt.parsing(args):
        print "args Error!!!"
        sys.exit()

    opt.tprint()

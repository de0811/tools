#!/usr/bin/python
import sys

class option:
    mOptInfos = list()
    mOptFactor = dict()

    def __init__(self):
        pass

    def parsing(self, args=sys.argv[1:]):#sys.argv[1:]
        bDefault = False
        for i in range(len(args)):
            for info in self.mOptInfos:
                optArgs = list()
                if info[0] == "default":
                    if (i + info[1]) <= len(args):
                        for k in range(info[1]):
                            optArgs.append(args[i])
                            i = i + 1
                    else : return True
                    self.mOptFactor.setdefault(info[0], optArgs)
                    bDefault = True
                    return True
                elif info[0] == args[i]:
                    i = i + 1
                    if (i + info[1]) <= len(args):
                        for k in range(info[1]):
                            optArgs.append(args[i])
                            i = i + 1
                    self.mOptFactor.setdefault(info[0], optArgs)
                if i >= len(args) : break
        if bDefault is False:
            self.mOptFactor.setdefault("default", list())
    
    def run(self):
        for info in self.mOptInfos:
            Factors = self.mOptFactor.get(info[0], None)
            if Factors is None:
                continue
            info[2](Factors)

    def addOpt(self, opt, argCount, func):
        self.mOptInfos.append((opt, argCount, func))

    def tprint(self):
        print "mOptInfos : "
        print self.mOptInfos
        print "mOptFactor : "
        print self.mOptFactor

def test1(args):
    print "test1 Func"
    print args

class CCC:
    def p(self, arg):
        print arg

if __name__ == "__main__":
    cc = CCC()

    args = ["1111", "2222", "3333", "4444"]
    args = ["1111"]
    opt = option()
    opt.addOpt("-h", 0, cc.p)
    opt.addOpt("default", 1, cc.p)

    if False is opt.parsing(args):
        print "args Error!!!"
        sys.exit()

    print "---------------"
    opt.run()
    print "---------------"

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
                print "------option : " + info[0] + " Parsing----------"
                if info[0] == "default":
                    if (i + info[1]) <= len(args):
                        for k in range(info[1]):
                            optArgs.append(args[i])
                            print "opt : " + info[0] + " args["+str(i)+"] : "+args[i] + "   k : " + str(k)
                            i = i + 1
                    else : return False
                    self.mOptFactor.setdefault(info[0], optArgs)
                    bDefault = True
                    return True
                elif info[0] == args[i]:
                    if (i + info[1]) <= len(args):
                        for k in range(info[1]):
                            i = i + 1
                            optArgs.append(args[i])
                            print "opt : " + info[0] + " args["+str(i)+"] : "+args[i] + "   k : " + str(k)
                    else : return False
                    i = i + 1
                    self.mOptFactor.setdefault(info[0], optArgs)
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
    opt = option()
    opt.addOpt("1111", 2, cc.p)
    opt.addOpt("default", 1, cc.p)

    if False is opt.parsing(args):
        print "args Error!!!"
        sys.exit()

    print "---------------"
    opt.run()
    print "---------------"

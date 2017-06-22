#!/usr/bin/python

class option:
    mOptInfos = list()
    mOptFactor = dict()
    def __init__(self, optList):
        mOptInfos = optList;

    def parsing(self, args):
        pass
    
    def run(self):
        pass

    def addOpt(self, opt, argCount, func):
        self.mOptInfos.add((opt, argCount, func))



def test1(str1, str2, str3):
    print str1 + str2 + str3


if __name__ == "__main__":
    args = ["1111", "2222", "3333", "4444"]
    opt = option()
    opt.addOpt("1111", 3, test1)
    opt.parsing(args)

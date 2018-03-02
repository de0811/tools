#!/usr/bin/python3
# coding=utf8
import sys
import copy

"""
"default" 옵션의 경우 인자 값을 무조건 고정 값으로 지정됨
나머지 옵션은 가변 옵션 가능
"""
class option:
    class __OptInfo :
        opt = ""
        argCount = 0
        bVarArg = False
        func = None
        bHelp = False

        def __init__(self, opt, argCount, bVarArg, bHelp, func) :
            self.opt = opt
            self.argCount = argCount
            self.bVarArg = bVarArg
            self.bHelp = bHelp
            self.func = func


    mOptInfos = list() #[option, argsCount, Func]
    mOptFactor = dict() #{option, args}

    def __init__(self):
        self.mOptInfos = list()
        self.mOptFactor = dict()
    

    def argsParsing(self, argvs) :
        tmp_args = copy.deepcopy(argvs)
        optArgs = list()
        #default 인자는 따로 빼놓고 시작
        #default 먼저 정리
        #bHelp가 있는지 확인해봐야함
        bHelp = False
        for oinfo in self.mOptInfos :
            if oinfo.bHelp == True :
                for arg in tmp_args :
                    if arg == oinfo.opt :
                        bHelp = True
        start_default_args_idx = -1
        if bHelp == False :
            bModifyCheck = False
            for oinfo in self.mOptInfos :
                if oinfo.opt == "default" :
                    allCount = len(tmp_args)
                    #default가 인자를 원하지 않음
                    start_default_args_idx = allCount - 1
                    if oinfo.argCount == 0 :
                        break
                    if allCount == 0 and oinfo.argCount != 0 and oinfo.bVarArg == True :
                        print ("default Args Fail")
                        return False
                    if oinfo.argCount != 0 :
                        bModifyCheck = True
                        if allCount - oinfo.argCount < 0 :
                            print ("default Args Fail_")
                            return False
                        else :
                            start_default_args_idx = allCount - oinfo.argCount
                    for arg in tmp_args[start_default_args_idx :] :
                        for compare in self.mOptInfos :
                            if arg == compare.opt :
                                print ("default opt Args Fail")
                                return False
                        optArgs.append(arg)
                    break
            self.mOptFactor.setdefault("default", optArgs)
            if bModifyCheck == True :
                tmp_args = tmp_args[0 : start_default_args_idx ]
        else :
            self.mOptFactor.setdefault("default", None)
        

        # 옵션 마다 구획 나누기
        #help따위
        arrPosition = list()
        for oinfo in self.mOptInfos :
            for idx in range(len(tmp_args)) :
                if tmp_args[idx] == oinfo.opt :
                    arrPosition.append((oinfo.opt, idx))
        #구간마다 쓰기 좋게 정렬을 해보아요 -,
        arrPosition = sorted(arrPosition, key=lambda x: x[1])

        for idx in range( len(arrPosition) ) :
            start = arrPosition[idx][1]
            end = 0
            if idx + 1 >= len(arrPosition) :
                end = len(tmp_args) - 1
            else :
                end = arrPosition[idx + 1][1] - 1
            paramCount = end - start #-1
            if end == start :
                paramCount = 0
            
            
            
            optArgs = list()
            #인자의 최대 갯수를 확인
            for oinfo in self.mOptInfos :
                if oinfo.opt == arrPosition[idx][0] :
                    if paramCount <= oinfo.argCount : #opt의 자신의 이름도 포함되어 있으니 -1
                        #고정 갯수인가 ?
                        if paramCount < oinfo.argCount and oinfo.bVarArg == True : #opt 자신의 이름도 포함되어 있으니 -1
                            print ("opt argment VarArgs=True " + oinfo.opt)
                            return False
                        for arg in tmp_args[start+1:end+1] : #start+1 : 옵션 이름 제외하고 전달, end+1 : 옵션의 끝에서 +1
                            optArgs.append(arg)
                    else :
                        print ("opt overflow !!!")
                        return False
            
            self.mOptFactor.setdefault(arrPosition[idx][0], optArgs)
                    
    def parsing(self,argvs=sys.argv[1:]):#sys.argv[1:]
        if False is self.argsParsing(argvs):
            print ("argvs Error!!!")
            sys.exit()

 
    def run(self):
        for oinfo in self.mOptInfos:
            Factors = self.mOptFactor.get(oinfo.opt, None)
            if Factors is None:
                continue
            oinfo.func(Factors)
    

    u'''
    opt : option 값
    argCount : 최대 몇개의 인자를 받는지 선택
    bVarArg : 인자 값이 고정인지 선택
    func : 동작을 진행할 함수
    bHelp : 해당 옵션을 사용하면 default를 사용하지 않도록 진행(예를 들어 help 기능을 사용할 경우)
    '''
    def addOpt(self, opt, argCount, bVarArg, bHelp, func):
        optInfo = self.__OptInfo(opt, argCount, bVarArg, bHelp, func)
        #self.mOptInfos.append((opt, argCount, bVarArg, func))
        self.mOptInfos.append(optInfo)

    def tprint(self):
        print ("mOptInfos : ")
        print (self.mOptInfos)
        print ("mOptFactor : ")
        print (self.mOptFactor)

class CCC:
    def p(self, argvs):
        print (argvs)

class argRan :
    str1 = ""
    def __init__(self):
        str1 = ""
    def help(self, argvs):
        print ("help Test !!!")
        sys.exit()
    def arg1(self, argvs) :
        print ("*" * 30)
        print ("arg1 run")
        print (argvs)
        print ("*" * 30)
    def arg2(self, argvs) :
        print ("*" * 30)
        print ("arg2")
        print (argvs)
        print ("*" * 30)
    def default(self, argvs) :
        print ("*" * 30)
        print ("default")
        print (argvs)
        print ("*" * 30)

if __name__ == "__main__":
    argvs = ["-b", "-d", "22", "aavbb",]
    argvs = list()
    argvs = ["-d", "asdasd"]
    #argvs = ["-h",]
    print ("*" * 10 + "argvs" + "*" * 10)
    print (argvs)
    print ("*" * 25)
    argran = argRan()
    opt1 = option()
    #def addOpt(self, opt, argCount, bVarArg, func):
    opt1.addOpt(opt="-h", argCount=0, bVarArg=True, bHelp=True, func=argran.help)
    opt1.addOpt(opt="-d", argCount=0, bVarArg=True, bHelp=False, func=argran.arg1)
    opt1.addOpt(opt="-b", argCount=0, bVarArg=False, bHelp=False, func=argran.arg2)
    opt1.addOpt(opt="default", argCount=0, bVarArg=True, bHelp=False, func=argran.default)
    opt1.parsing(argvs)
    print ("---------------")
    opt1.run()
    print ("---------------")


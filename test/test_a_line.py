#!/usr/bin/python3
#-*-coding:utf-8-*-


from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor
import time
import threading


def process_ed(*args) :
    result = args# 입력받은 인자들을 처리한다...
    time.sleep(0)
    print(result)
    for i in range(1000, 2000) :
        print (i)

class ProcessTest :
    def process(self, args) :
        result = args# 입력받은 인자들을 처리한다...
        time.sleep(0)
        print(result)
        t = threading.Thread( target=process_ed, args=('qqqq'), daemon=False )
        t.start()
        for i in range(1000) :
            print (i)
    
    def alt(self) :
        with ProcessPoolExecutor(max_workers=10) as exe:
            for i in range(10) :
                exe.submit(self.process, ['aaa', 'bbb', i])
                time.sleep(0.0)
            exe.shutdown(wait=True)
            print ("END Process")
 



def main():
    pt = ProcessTest()
    #pt.process(('aaa', 'ccc'))
    pt.alt()

if __name__ == "__main__":
    main()

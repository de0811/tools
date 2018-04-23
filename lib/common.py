#!/usr/bin/python3
# coding=utf8
import time

class Timer :
    __begin = 0
    __end = 0
    __pause_begin = 0
    __pause_end = 0
    ____pause_time = 0
    is_running = False
    is_pause = False
    def __init__(self) :
        self.__begin = 0
        self.__end = 0
        self.__pause_begin = 0
        self.__pause_end = 0
        self.____pause_time = 0
        self.is_running = False
        self.is_pause = False

    def start(self) :
        self.is_running = True
        if self.is_pause != True :
            self.__begin = int(round(time.time() * 1000))
        else :
            self.__pause_end = int(round(time.time() * 1000))
            self.is_pause = False
            self.____pause_time = self.____pause_time + self.__pause_end - self.__pause_begin

    def __pause_time(self) :
        if self.is_pause == True :
            current = int(round(time.time() * 1000))
            return self.____pause_time + (current - self.__pause_begin)
        else :
            return self.____pause_time

    def pause(self) :
        self.is_pause = True
        self.__pause_begin = int(round(time.time() * 1000))

    def stop(self) :
        self.is_running = False
        self.__end = int(round(time.time() * 1000))

    def milli_second_tab(self) :
        return self.milli_second_full_tab() - self.__pause_time()
    
    def milli_second_full_tab(self) :
        current = int(round(time.time() * 1000))
        return (current - self.__begin)

    def second_tab(self) :
        return self.milli_second_tab() / 1000
    
    def second_full_tab(self) :
        return self.milli_second_full_tab() / 1000

    def second_result(self) :
        return self.milli_second_result() / 1000
    
    def second_full_result(self) :
        return self.milli_second_full_result() / 1000

    def milli_second_result(self) :
        return self.milli_second_full_result() - (self.__pause_time())
    
    def milli_second_full_result(self) :
        return (self.__end - self.__begin)

    def __repr__(self) :
        return self.milli_second_tab()
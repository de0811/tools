#!/usr/bin/python3
# coding=utf8

class DeviceLogs :
    class LogUnit :
        event = ""
        dist = ""
        time = 0.0
        def __init__(self, event, dist, time) :
            self.event = event
            self.dist = dist
            self.time = time
    logs = dict()   #Device, event, dist, time
    def __init__(self) :
        self.logs = dict()
    
    def append(self, device, event, dist, time) :
        self.logs.setdefault(device, list())
        self.logs[device].append( self.LogUnit(event, dist, time) )
    
    def find_event(self, device, event) :
        tmp = list()
        try :
            for log_unit in self.logs[device] :
                if log_unit.event.lower().find(event.lower()) != -1 :
                    tmp.append(log_unit)
        finally :
            return tmp
    
    def find_dist(self, device, dist) :
        tmp = list()
        try :
            for log_unit in self.logs[device] :
                if log_unit.dist.lower().find(dist.lower()) != -1 :
                    tmp.append(log_unit)
        finally :
            return tmp
    
    def prints(self, device) :
        try :
            if self.logs.get(device) == None :
                return
            for log_unit in self.logs[device] :
                print (device + " : " + log_unit.event + " : " + log_unit.dist + " :: " + str(log_unit.time))
        finally :
            pass
import threading, traceback, time
import win32api
from win32process import SetProcessWorkingSetSize, GetCurrentProcess

import wx

import eg
from ThreadWorker import ThreadWorker
from EventGhostEvent import EventGhostEvent

MB = 1048576        

class EventThread(ThreadWorker):
    
    def __init__(self):
        ThreadWorker.__init__(self)
        eg.event = EventGhostEvent("")
        self.startupEvent = None
        self.currentProcess = GetCurrentProcess()


    def poll(self):
        if eg.config.limitMemory and not eg.mainFrame.IsShown():
            try:
                SetProcessWorkingSetSize(
                    self.currentProcess,
                    3670016,
                    eg.config.limitMemorySize * 1048576
                )
            except:
                self.poll = self.poll2
                
                
    def poll2(self):
        pass
    
        
    def TriggerEvent(self, suffix, payload=None, prefix="Main", source=eg):
        '''Trigger an event'''
        event = EventGhostEvent(suffix, payload, prefix, source)
        self.AppendEvent(event.Trigger)
        return event
    
    
    def TriggerEnduringEvent(
        self, 
        suffix, 
        payload=None, 
        prefix="Main", 
        source=eg
    ):
        event = EventGhostEvent(suffix, payload, prefix, source)
        self.AppendEvent(event.TriggerEnduring)
        return event
        

    def TriggerEventWait(
        self, 
        suffix, 
        payload=None, 
        prefix="Main", 
        source=eg
    ):
        event = self.TriggerEvent(suffix, payload, prefix, source)
        event.startProcessed.wait(5.0)
        if not event.startProcessed.isSet():
            if eg._debug:
                eg.notice("timeout TriggerEventWait")
                traceback.print_stack()
        return event
    
    
    @eg.logit()
    def StartSession(self, filename):
        self.shouldRun = True

        eg.actionThread.CallWait(eg.actionThread.StartSession, filename)
        
        self.TriggerEvent("OnInit")
        boottime = time.time() - win32api.GetTickCount() / 1000.0
        if boottime > int(eg.config.storedBootTime) + 10:
            eg.config.storedBootTime = boottime
            eg.SaveConfig()
            self.TriggerEvent("OnInitAfterBoot")
            
        if self.startupEvent[0]:
            self.TriggerEvent(self.startupEvent[0], self.startupEvent[1])
            self.startupEvent = None
                

    @eg.logit()
    def StopSession(self):
        eg.actionThread.CallWait(eg.actionThread.StopSession)
        eg.notice("StopSession done")


    

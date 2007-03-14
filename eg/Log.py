import eg
from collections import deque
from types import UnicodeType
from time import time
import codecs

import sys

oldStdOut = sys.stdout
oldStdErr = sys.stderr


oldStdOut = codecs.lookup("ascii").streamwriter(sys.stdout, 'backslashreplace')
oldStdErr = codecs.lookup("ascii").streamwriter(sys.stderr, 'backslashreplace')



class DummyLogCtrl:
    
    def WriteLine(self, line, icon, wRef, when):
        oldStdOut.write("%03d: %s\n" % (icon, line))
    
    
    
class Log:
    
    def __init__(self):
        self.buffer = ""
        self.data = deque()
        self.maxlength = 50
        self.ctrl = DummyLogCtrl()
        
        if eg.debugLevel:
            class StdOut:
                def write(self2, data):
                    #self.Write(data, 0)
                    oldStdOut.write(data)
            
            class StdErr:
                def write(self2, data):
                    #self.Write(data, 1)
                    oldStdErr.write(data)
        else:
            class StdOut:
                def write(self2, data):
                    self.Write(data, 0)
            
            class StdErr:
                def write(self2, data):
                    self.Write(data, 1)
        
        sys.stdout = StdOut()
        sys.stderr = StdErr()
    
    
    def Destroy(self):
        eg.whoami()
        return wx.ListCtrl.Destroy(self)
    
    
    def SetCtrl(self, logCtrl):
        if logCtrl is not None:
            self.ctrl = logCtrl
        else:
            self.ctrl = DummyLogCtrl()
        
        
    def GetData(self, numLines=-1):
        eg.whoami()
        if numLines == -1:
            start = 0
            end = len(self.data)
        elif numLines > len(self.data):
            numLines = len(self.data)
        data = list(self.data)
        return data[start:end]
    
    
    def _WriteLine(self, line, icon, wRef, when):
        self.ctrl.WriteLine(line, icon, wRef, when)
    
    
    def Write(self, text, icon, wRef=None):
        lines = (self.buffer + text).split("\n")
        self.buffer = lines[-1]
        data = self.data
        when = time()
        for line in lines[:-1]:
            data.append((line, icon, wRef, when))
            eg.CallAfter(self._WriteLine, line, icon, wRef, when)
            if len(data) >= self.maxlength:
                data.popleft()

        
    def DoPrint(self, text, icon=0, wRef=None):
        self.Write(text + "\n", icon, wRef)
        
        
    def LogEvent(self, event):
        """Store and display an EventGhostEvent in the logger."""
        payload = event.payload
        eventstring = event.string
        if payload is not None:
            if type(payload) == UnicodeType:
                mesg = eventstring + ' u"' + payload + '"'
            else:
                mesg = eventstring + ' ' + repr(payload)
        else:
            mesg = eventstring
        self.Write(mesg + "\n", eg.EventItem.iconIndex, eventstring)
        
        
    

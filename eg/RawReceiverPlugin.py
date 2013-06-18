
from threading import Timer
import eg
from PluginClass import PluginClass

eg._lastDefinedPluginClass = None



class RawReceiverPlugin(PluginClass):
    
    def __init__(self):
        self.mapTable = {}
        self.timer = Timer(0, self.OnTimeOut)
        self.lastEventString = ""
        self.timeout = 0.2
        self.lastTimeout = self.timeout
        self.disableUnmapped = False
        self.repeatCode = None
    
    
    def TriggerEvent(self, suffix, payload=None):
        if suffix == self.repeatCode:
            suffix = self.lastEventString
            timeout = self.lastTimeout
        elif self.mapTable.has_key(suffix):
            newEventString, timeout, repeatCode = self.mapTable[suffix]
            self.repeatCode = repeatCode
        else:
            if self.disableUnmapped:
                return
            newEventString = suffix
            timeout = self.timeout
            self.repeatCode = None
        self.timer.cancel()       
        if self.lastEventString != suffix:
            PluginClass.TriggerEnduringEvent(self, newEventString, payload)
            self.lastEventString = suffix
        self.timer = Timer(timeout, self.OnTimeOut)
        self.timer.start()
        self.lastTimeout = timeout
        return self.info.lastEvent


    def OnTimeOut(self):
        self.EndLastEvent()
        self.lastEventString = ""
        
        
    def Map(self, what, to, timeout=None, repeat_code=None):
        self.mapTable[what] = (to, timeout or self.timeout, repeat_code)





import eg
import wx
import stackless


class TaskletDialog(wx.Dialog, eg.ControlProviderMixin):

    @eg.LogItWithReturn
    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        eg.Notify("DialogCreate", self)
    
    
    @eg.LogIt
    def Destroy(self):
        eg.Notify("DialogDestroy", self)
        wx.Dialog.Destroy(self)
        
        
    @eg.LogIt
    def FinishSetup(self):
        self.setupFinished = True
        eg.Utils.EnsureVisible(self)
        self.Show()
            
        
    @eg.LogItWithReturn
    def SetResult(self, *args):
        if self.lastEventId == wx.ID_OK:
            self.done = True
        self.resultsChannel.send((self.lastEventId, args))
            
    
    @eg.LogItWithReturn
    def ProcessingTask(self, *args, **kwargs):
        self.processingChannel = stackless.channel()
        self.resultsChannel = stackless.channel()
        self.setupFinished = False
        self.lastEventId = None
        self.done = False
        self.Configure(*args, **kwargs)
        self.done = True
        self.resultsChannel.send((None, None))
        if self.setupFinished:
            self.Destroy()
        
        
    @classmethod
    @eg.LogItWithReturn
    def Create(cls, *args, **kwargs):
        self = cls.__new__(cls, *args, **kwargs)
        self.tasklet = eg.Tasklet(self.ProcessingTask)(*args, **kwargs)
        self.tasklet.run()
        return self
                
    
    @eg.LogItWithReturn
    def GetEvent(self):
        event, args = self.resultsChannel.receive()
        if event is None:
            self.tasklet.run()
        return event, args
        
    
    def __iter__(self):
        while True:
            event, args = self.GetEvent()
            if event is None:
                raise StopIteration
            try:
                yield event, args
            except GeneratorExit:
                while True:
                    event, args = self.GetEvent()
                    if event is None:
                        return
    
    @classmethod
    def GetResult(cls, *args):
        for event, result in cls.Create(*args):
            if event == wx.ID_OK:
                return result
        return None
    
        
    @eg.LogItWithReturn
    def Dispatch(self, eventId):
        self.lastEventId = eventId
        if eventId == wx.ID_CANCEL:
            self.processingChannel.send(None)
        elif eventId == wx.ID_OK:
            self.processingChannel.send(wx.ID_OK)
            if self.done:
                self.processingChannel.send(None)
        else:
            self.processingChannel.send(eventId)

        
    @eg.LogItWithReturn
    def Affirmed(self):
        if not self.setupFinished:
            self.FinishSetup()
        return self.processingChannel.receive()
            
    
    @eg.LogItWithReturn
    def OnClose(self, event):
        self.Dispatch(wx.ID_CANCEL)
        event.Skip()
        
        
    @eg.LogItWithReturn
    def OnOK(self, event):
        self.Dispatch(wx.ID_OK)
        event.Skip()
        
        
    @eg.LogItWithReturn
    def OnCancel(self, event):
        self.Dispatch(wx.ID_CANCEL)
        event.Skip()
        
        
    @eg.LogItWithReturn
    def OnApply(self, event):
        self.Dispatch(wx.ID_APPLY)
        event.Skip()

        
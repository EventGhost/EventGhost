import eg
import wx
import time
import threading


class StateIcon(wx.TaskBarIcon):
    
    def __init__(self, parent=None):
        #eg.whoami()
        self.stateIcons = (
            wx.Icon("images\\Tray1.png", wx.BITMAP_TYPE_PNG),
            wx.Icon("images\\Tray3.png", wx.BITMAP_TYPE_PNG),
            wx.Icon("images\\Tray2.png", wx.BITMAP_TYPE_PNG),
        )
        wx.TaskBarIcon.__init__(self)
        self.iconTime = 0
        self.SetIcon(self.stateIcons[0], eg.APP_NAME)
        self.currentEvent = None
        self.processingEvent = None
        self.currentState = 0
        self.reentrantLock = threading.Lock()
        self.alive = True
        #self.SetIcon(self.stateIcons[0])

#        tmpID = wx.NewId()
#        self.iconTimer = wx.Timer(self, tmpID)
#        wx.EVT_TIMER(self, tmpID, self.ResetIcon2)
        
        
    def SetIcons(self, state):
        if self.alive:
            self.SetIcon(self.stateIcons[state])
            eg.mainFrame.statusBar.SetState(state)
        
        
    def SetIconsDummy(self, state):
        pass
        
        
    def SetProcessingState(self, state, event):
        return
        self.reentrantLock.acquire()
        try:
            if state == 0:
                if event == self.processingEvent:
                    state = 1
                elif event == self.currentEvent:
                    state = 0
                else:
                    return
            elif state == 1:
                self.processingEvent = None
                if event.shouldEnd.isSet():
                    self.currentEvent = None
                    state = 0
                else:
                    return
            elif state == 2:
                self.currentEvent = event
                self.processingEvent = event
            self.currentState = state
            wx.CallAfter(self.SetIcons, state)
        finally:
            self.reentrantLock.release()
    
    

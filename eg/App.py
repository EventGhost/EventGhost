import eg
import wx
import sys

import pythoncom
import threading
from win32process import (
    ExitProcess,
    SetProcessShutdownParameters,
    SetPriorityClass, 
    GetCurrentProcess
)
from win32con import REALTIME_PRIORITY_CLASS, WM_QUERYENDSESSION



class MyApp(wx.App):
    
    @eg.logit()
    def OnInit(self):
        #SetPriorityClass(GetCurrentProcess(), REALTIME_PRIORITY_CLASS)
        self.SetAppName(eg.APP_NAME)
        self.SetExitOnFrameDelete(False)
        
        # set shutdown priority for this app, so we get 
        # shutdown last (hopefully)
        SetProcessShutdownParameters(0x0100, 0)
        
        # We don't use wxWindows EVT_QUERY_END_SESSION handling, because we
        # would get an event for every frame the application has and that
        # would make it hard to distinguish between individual logoff
        # requests. So we simply disable the built-in handling by assigning
        # a dummy function and generate our own event in the hidden
        # MessageReceiver window.
        def dummy(event):
            pass
        self.Bind(wx.EVT_QUERY_END_SESSION, dummy)
        eg.messageReceiver.AddHandler(
            WM_QUERYENDSESSION, 
            self.OnQueryEndSession
        )
        
        # EVT_END_SESSION works fine. wxWindows only sends one event.
        self.Bind(wx.EVT_END_SESSION, self.OnEndSession)
        
        self.onExitFuncs = []
        self.clipboardEvent = eg.EventHook()
        def FireClipboardEvent(event):
            if event.GetActive():
                self.clipboardEvent.Fire()
        self.Bind(wx.EVT_ACTIVATE_APP, FireClipboardEvent)
        return True
    
    
    def SetupGui(self):
        eg.whoami()
        # setup a taskbar menu with icon, and catch some events from it
        import StateIcon
        self.taskBarIcon = taskBarIcon = StateIcon.StateIcon(self)

        trayMenu = trayMenu = eg.Menu(taskBarIcon, "")
        text = eg.text.MainFrame.TaskBarMenu
        
        def OnMenuShow(event):
            eg.mainFrame.BringToFront()
        trayMenu.Append(text.Show, OnMenuShow)
        
        def OnMenuHide(event):
            eg.mainFrame.Iconize(True)
        trayMenu.Append(text.Hide, OnMenuHide)
        trayMenu.AppendSeparator()
        
        def OnMenuExit(event):
            eg.mainFrame.OnCmdExit(event)
        trayMenu.Append(text.Exit, OnMenuExit)
    
        def OnTaskBarMenu(event):
            taskBarIcon.PopupMenu(trayMenu)
        taskBarIcon.Bind(wx.EVT_TASKBAR_RIGHT_UP, OnTaskBarMenu)
        taskBarIcon.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, OnMenuShow)
    

    @eg.logit(print_return=True)
    def OnQueryEndSession(self, hwnd, msg, wparam, lparam):
        """System is about to be logged off"""
        # This method gets called from MessageReceiver on a
        # WM_QUERYENDSESSION win32 message.
        if eg.mainFrame.OnClose() == wx.ID_CANCEL:
            eg.notice("User cancelled shutdown in OnQueryEndSession")
            return 0
        return 1


    @eg.logit(print_return=True)
    def OnEndSession(self, event):
        """System is logging off"""
        egEvent = eg.eventThread.TriggerEvent("OnEndSession")
        while not egEvent.isEnded:
            self.Yield()
        self.taskBarIcon.alive = False
        self.taskBarIcon.Destroy()
        self.OnExit()
         
        
    def Exit(self, event=None):
        self.taskBarIcon.alive = False
        self.taskBarIcon.Destroy()
        self.ExitMainLoop()
        
        
    @eg.logit()
    def OnExit(self):
        if eg.mainFrame:
            egEvent = eg.eventThread.TriggerEvent("OnClose")
            while not egEvent.isEnded:
                self.Yield()
                
            for func in self.onExitFuncs:
                eg.notice(func)
                func()
                
            eg.DeInit()
        
        eg.notice("COM interface count: %s" % pythoncom._GetInterfaceCount())
        
        eg.notice("Threads:")
        for t in threading.enumerate():
            eg.notice(" ", t, t.getName())
                
        while self.Pending():
            self.Dispatch()
                
        # try to wait till all utility threads have ended
        currentThread = threading.currentThread()
        for t in threading.enumerate():
            if t is not currentThread and not t.isDaemon() and t.isAlive():
                eg.notice("joining: " + str(t))
                t.join(5.0)
        
        eg.notice("Threads:")
        for t in threading.enumerate():
            eg.notice(" ", t, t.getName())
        eg.notice("Done!")
        sys.exit(0)
        

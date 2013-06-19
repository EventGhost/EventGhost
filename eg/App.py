# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import eg
import wx
import sys
import time

import pythoncom
import threading
from win32process import (
    ExitProcess,
    SetProcessShutdownParameters,
    SetPriorityClass, 
    GetCurrentProcess
)
from win32con import REALTIME_PRIORITY_CLASS, WM_QUERYENDSESSION, WM_ENDSESSION



class MyApp(wx.App):
    
    #@eg.LogIt
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
        self.Bind(wx.EVT_QUERY_END_SESSION, eg.DummyFunc)
        self.Bind(wx.EVT_END_SESSION, eg.DummyFunc)
        eg.messageReceiver.AddHandler(
            WM_QUERYENDSESSION, 
            self.OnQueryEndSession
        )
        
        eg.messageReceiver.AddHandler(
            WM_ENDSESSION, 
            self.OnEndSession
        )
        
        self.onExitFuncs = []
        self.clipboardEvent = eg.EventHook()
        def FireClipboardEvent(event):
            if event.GetActive():
                self.clipboardEvent.Fire()
        self.Bind(wx.EVT_ACTIVATE_APP, FireClipboardEvent)
        
        return True
    
    
    @eg.LogIt
    def SetupGui(self):        
        self.focusEvent = eg.EventHook()
        
        # setup a taskbar menu with icon, and catch some events from it
        import StateIcon
        self.taskBarIcon = taskBarIcon = StateIcon.StateIcon(self)

        trayMenu = self.trayMenu = eg.Menu(taskBarIcon, "")
        text = eg.text.MainFrame.TaskBarMenu
        menuShow = trayMenu.Append(text.Show, self.OnCmdShowMainFrame)
        menuHide = trayMenu.Append(text.Hide, self.OnCmdHideMainFrame)
        trayMenu.AppendSeparator()
        trayMenu.Append(text.Exit, self.OnCmdExit)
    
        def OnTaskBarMenu(event):
            menuHide.Enable(eg.document.frame is not None)
            taskBarIcon.PopupMenu(trayMenu)
        taskBarIcon.Bind(wx.EVT_TASKBAR_RIGHT_UP, OnTaskBarMenu)
        taskBarIcon.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnCmdShowMainFrame)
        
        if not (eg.config.hideOnStartup or eg.startupArguments.hideOnStartup):
            eg.document.ShowFrame()
    

    #------- TrayIcon menu handlers ------------------------------------------
    
    def OnCmdShowMainFrame(self, event=None):
        eg.document.ShowFrame()
        
        
    def OnCmdHideMainFrame(self, event):
        eg.document.HideFrame()
        
        
    def OnCmdExit(self, event):
        self.Exit(event)
        
    #------------------------------------------------------------------------
        
    @eg.LogItWithReturn
    def OnQueryEndSession(self, hwnd, msg, wparam, lparam):
        """System is about to be logged off"""
        # This method gets called from MessageReceiver on a
        # WM_QUERYENDSESSION win32 message.
        if eg.document.CheckFileNeedsSave() == wx.ID_CANCEL:
            eg.DebugNote("User cancelled shutdown in OnQueryEndSession")
            return 0
        return 1


    @eg.LogItWithReturn
    def OnEndSession(self, hwnd, msg, wparam, lparam):
        """System is logging off"""
        egEvent = eg.eventThread.TriggerEvent("OnEndSession")
        while not egEvent.isEnded:
            time.sleep(0.01)
        eg.CallWait(eg.document.Close)
        self.taskBarIcon.alive = False
        self.taskBarIcon.Destroy()
        #self.ExitMainLoop()
    	eg.CallWait(self.OnExit)
    	return 0
         
        
    @eg.LogIt
    def Exit(self, event=None):
        if eg.document.CheckFileNeedsSave() == wx.ID_CANCEL:
            return
        eg.document.Close()
        self.taskBarIcon.alive = False
        self.taskBarIcon.Destroy()
        self.ExitMainLoop()
        
        
    @eg.LogIt
    def OnExit(self):
        if not eg.startupArguments.translate:
            eg.DebugNote("Triggering OnClose")    
            egEvent = eg.eventThread.TriggerEvent("OnClose")
            while not egEvent.isEnded:
                self.Yield()
            eg.DebugNote("Calling exit funcs")    
                
            for func in self.onExitFuncs:
                eg.DebugNote(func)
                func()
            eg.DebugNote("Calling eg.DeInit()")    
            eg.DeInit()
        
        eg.DebugNote("COM interface count: %s" % pythoncom._GetInterfaceCount())
        
        eg.DebugNote("Threads:")
        for t in threading.enumerate():
            eg.DebugNote(" ", t, t.getName())
                
        while self.Pending():
            self.Dispatch()
                
        # try to wait till all utility threads have ended
        currentThread = threading.currentThread()
        for t in threading.enumerate():
            if (
                t is not currentThread 
                and (t is not eg.messageReceiver) 
                and not t.isDaemon() 
                and t.isAlive()
            ):
                eg.DebugNote("joining: " + str(t))
                t.join(5.0)
        
        eg.DebugNote("Threads:")
        for t in threading.enumerate():
            eg.DebugNote(" ", t, t.getName())
        eg.DebugNote("Done!")
        sys.exit(0)
        

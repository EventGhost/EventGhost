# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
# 
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
import wx
import sys
import time
import threading
from eg.WinApi.Dynamic import SetProcessShutdownParameters, ExitProcess

IS_VISTA = sys.getwindowsversion()[0] > 5

if IS_VISTA:
    from eg.WinApi.Dynamic import _user32, BOOL, HWND, LPCWSTR
    ShutdownBlockReasonCreate = _user32.ShutdownBlockReasonCreate
    ShutdownBlockReasonCreate.restype = BOOL
    ShutdownBlockReasonCreate.argtypes = [HWND, LPCWSTR]
    ShutdownBlockReasonDestroy = _user32.ShutdownBlockReasonDestroy
    ShutdownBlockReasonDestroy.restype = BOOL
    ShutdownBlockReasonDestroy.argtypes = [HWND]
else:
    ShutdownBlockReasonCreate = lambda hwnd, msg: None
    ShutdownBlockReasonDestroy = lambda hwnd: None
    
    
class App(wx.App):

    def __init__(self):
        self.onExitFuncs = []
        wx.App.__init__(self, 0)
        self.shouldVeto = False
        self.firstQuery = True
        self.endSession = False
        self.frame = wx.Frame(None)
        self.hwnd = self.frame.GetHandle()


    def OnInit(self):
        self.SetAppName(eg.APP_NAME)
        self.SetExitOnFrameDelete(False)

        # set shutdown priority for this application, so we get
        # shutdown last (hopefully)
        SetProcessShutdownParameters(0x0100, 0)

        if IS_VISTA:
            self.Bind(wx.EVT_QUERY_END_SESSION, self.OnQueryEndSessionVista)
        else:
            self.Bind(wx.EVT_QUERY_END_SESSION, self.OnQueryEndSessionXp)
        self.Bind(wx.EVT_END_SESSION, self.OnEndSession)
            
        return True


    @eg.LogItWithReturn
    def OnQueryEndSessionXp(self, event):
        if not self.firstQuery:
            return
        self.firstQuery = False
        if eg.document.CheckFileNeedsSave() == wx.ID_CANCEL:
            event.Veto()
        wx.CallAfter(self.Reset)
            
    
    @eg.LogItWithReturn
    def OnQueryEndSessionVista(self, event):
        if self.shouldVeto:
            event.Veto()
            return
        if not self.firstQuery:
            return
        if eg.document.IsDirty():
            self.firstQuery = False
            self.shouldVeto = True
            event.Veto(True)
            ShutdownBlockReasonCreate(self.hwnd, "Unsaved data")
            res = eg.document.CheckFileNeedsSave()
            if res == wx.ID_YES:
                # file was saved, reset everything
                event.Veto(False)
                self.Reset()
                return
            if res == wx.ID_NO:
                # file was not saved
                # if called before shutdownUI, we get a OnEndSession
                self.shouldVeto = False
                ShutdownBlockReasonDestroy(self.hwnd)
                wx.CallAfter(self.OnEndSession, None)
                return
            if res == wx.ID_CANCEL:
                self.shouldVeto = True
                wx.CallAfter(self.Reset)
                return
                
                
    @eg.LogItWithReturn
    def Reset(self):
        self.shouldVeto = False
        self.firstQuery = True
        ShutdownBlockReasonDestroy(self.hwnd)
        
        
    
    @eg.LogItWithReturn
    def OnEndSession(self, dummyEvent):
        if self.endSession:
            return
        self.endSession = True
        egEvent = eg.eventThread.TriggerEvent("OnEndSession")
        while not egEvent.isEnded:
            self.Yield()
        eg.document.Close()
        eg.taskBarIcon.Close()
        self.OnExit()

    
    @eg.LogIt
    def Exit(self, dummyEvent=None):
        if eg.document.CheckFileNeedsSave() == wx.ID_CANCEL:
            return
        if eg.pyCrustFrame:
            eg.pyCrustFrame.Close()
        eg.document.Close()
        eg.taskBarIcon.Close()
        self.ExitMainLoop()


    @eg.LogIt
    def OnExit(self):
        if not eg.startupArguments.translate:
            eg.PrintDebugNotice("Triggering OnClose")
            egEvent = eg.eventThread.TriggerEvent("OnClose")
            while not egEvent.isEnded:
                self.Yield()

            eg.PrintDebugNotice("Calling exit functions")
            for func in self.onExitFuncs:
                eg.PrintDebugNotice(func)
                func()

            eg.PrintDebugNotice("Calling eg.DeInit()")
            eg.Init.DeInit()

        currentThread = threading.currentThread()

        while self.Pending():
            self.Dispatch()

        # try to wait till all utility threads have ended
        startTime = time.clock()
        waitTime = 0
        while True:
            threads = [
                thread for thread in threading.enumerate()
                if (
                    thread is not currentThread
                    and thread is not eg.messageReceiver._ThreadWorker__thread
                    and not thread.isDaemon()
                    and thread.isAlive()
                )
            ]
            if len(threads) == 0:
                break
            waitTime = time.clock() - startTime
            if waitTime > 5.0:
                break
            while self.Pending():
                self.Dispatch()
            time.sleep(0.01)
        eg.PrintDebugNotice(
            "Waited for threads shutdown: %f s" % (time.clock() - startTime)
        )
        if eg.debugLevel and len(threads):
            eg.PrintDebugNotice("The following threads did not terminate:")
            for thread in threads:
                eg.PrintDebugNotice(" ", thread, thread.getName())
        # destroy the TaskBarIcon, as it would otherwise stay as a ghost
        # icon in the system-tray.
        wx.TaskBarIcon.Destroy(eg.taskBarIcon)
        eg.PrintDebugNotice("Done!")
        ExitProcess(0)


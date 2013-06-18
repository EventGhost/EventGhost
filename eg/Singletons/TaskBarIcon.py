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

import threading


class TaskBarIcon(wx.TaskBarIcon):
    
    def __init__(self, parent=None):
        self.stateIcons = (
            wx.Icon("images\\Tray1.png", wx.BITMAP_TYPE_PNG),
            wx.Icon("images\\Tray3.png", wx.BITMAP_TYPE_PNG),
            wx.Icon("images\\Tray2.png", wx.BITMAP_TYPE_PNG),
        )
        self.tooltip = eg.APP_NAME + " " + eg.Version.string
        wx.TaskBarIcon.__init__(self)
        self.iconTime = 0
        self.SetIcon(self.stateIcons[0], self.tooltip)
        self.currentEvent = None
        self.processingEvent = None
        self.currentState = 0
        self.reentrantLock = threading.Lock()
        self.alive = True
        #self.SetIcon(self.stateIcons[0])

#        tmpID = wx.NewId()
#        self.iconTimer = wx.Timer(self, tmpID)
#        wx.EVT_TIMER(self, tmpID, self.ResetIcon2)
        
        menu = self.menu = eg.Menu(self, "")
        text = eg.text.MainFrame.TaskBarMenu
        self.menuShow = menu.Append(text.Show, self.OnCmdShowMainFrame)
        self.menuHide = menu.Append(text.Hide, self.OnCmdHideMainFrame)
        menu.AppendSeparator()
        menu.Append(text.Exit, self.OnCmdExit)
    
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.OnTaskBarMenu)
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnCmdShowMainFrame)
        
        
    def OnTaskBarMenu(self, event):
        self.menuHide.Enable(eg.document.frame is not None)
        self.PopupMenu(self.menu)
        
        
    def OnCmdShowMainFrame(self, event=None):
        eg.document.ShowFrame()
        
        
    def OnCmdHideMainFrame(self, event):
        eg.document.HideFrame()
        
        
    def OnCmdExit(self, event):
        eg.app.Exit(event)
        

    def SetIcons(self, state):
        if self.alive:
            self.SetIcon(self.stateIcons[state], self.tooltip)
            if eg.document.frame:
                eg.document.frame.statusBar.SetState(state)
        
        
    def SetToolTip(self, tooltip):
        self.tooltip = tooltip
        wx.CallAfter(self.SetIcons, self.currentState)
        
    
    def SetProcessingState(self, state, event):
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
    
    

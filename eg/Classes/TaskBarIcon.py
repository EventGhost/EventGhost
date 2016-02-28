# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import eg
import wx
import threading
from os.path import join


ID_SHOW = wx.NewId()
ID_HIDE = wx.NewId()
ID_EXIT = wx.NewId()


class TaskBarIcon(wx.TaskBarIcon):

    def __init__(self, show):
        self.stateIcons = (
            wx.Icon(join(eg.imagesDir, "Tray1.png"), wx.BITMAP_TYPE_PNG),
            wx.Icon(join(eg.imagesDir, "Tray3.png"), wx.BITMAP_TYPE_PNG),
            wx.Icon(join(eg.imagesDir, "Tray2.png"), wx.BITMAP_TYPE_PNG),
        )
        self.tooltip = eg.APP_NAME + " " + eg.Version.string
        wx.TaskBarIcon.__init__(self)
        # SetIcon *must* be called immediately after creation, as otherwise
        # it won't appear on Vista restricted user accounts. (who knows why?)
        if show:
            self.SetIcon(self.stateIcons[0], self.tooltip)
        self.currentEvent = None
        self.processingEvent = None
        self.currentState = 0
        self.reentrantLock = threading.Lock()
        eg.Bind("ProcessingChange", self.OnProcessingChange)
        menu = self.menu = wx.Menu()
        text = eg.text.MainFrame.TaskBarMenu
        menu.Append(ID_SHOW, text.Show)
        menu.Append(ID_HIDE, text.Hide)
        menu.AppendSeparator()
        menu.Append(ID_EXIT, text.Exit)
        self.Bind(wx.EVT_MENU, self.OnCmdShow, id=ID_SHOW)
        self.Bind(wx.EVT_MENU, self.OnCmdHide, id=ID_HIDE)
        self.Bind(wx.EVT_MENU, self.OnCmdExit, id=ID_EXIT)
        self.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.OnTaskBarMenu)
        self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnCmdShow)


    def Close(self):
        eg.Unbind("ProcessingChange", self.OnProcessingChange)


    def OnTaskBarMenu(self, dummyEvent):
        self.menu.Enable(ID_HIDE, eg.document.frame is not None)
        self.PopupMenu(self.menu)


    def OnCmdShow(self, dummyEvent=None):
        eg.document.ShowFrame()


    def OnCmdHide(self, dummyEvent):
        eg.document.HideFrame()


    def OnCmdExit(self, event):
        eg.app.Exit(event)


    def OnProcessingChange(self, state):
        self.SetIcon(self.stateIcons[state], self.tooltip)


    def SetToolTip(self, tooltip):
        self.tooltip = tooltip
        wx.CallAfter(self.SetIcon, self.stateIcons[self.currentState], tooltip)


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
            wx.CallAfter(eg.Notify, "ProcessingChange", state)
        finally:
            self.reentrantLock.release()


# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

import threading
import wx
from os.path import join

# Local imports
import eg

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
            self.Show()
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
        if eg.mainFrame is not None:
            eg.mainFrame.Iconize(False)
        self.Hide()

    def Hide(self):
        if eg.mainFrame is not None:
            eg.mainFrame.Iconize(False)
        self.RemoveIcon()

    def OnCmdExit(self, event):
        if eg.mainFrame is None or len(eg.mainFrame.openDialogs) == 0:
            eg.app.Exit(event)
        else:
            eg.mainFrame.Iconize(False)
            eg.mainFrame.RequestUserAttention()

    def OnCmdHide(self, dummyEvent):
        if eg.mainFrame is not None:
            eg.mainFrame.Iconize(True)

    def OnCmdShow(self, dummyEvent=None):
        if eg.mainFrame is not None:
            eg.mainFrame.Iconize(False)
        else:
            eg.document.ShowFrame()

    def OnProcessingChange(self, state):
        if self.IsIconInstalled():
            self.SetIcon(self.stateIcons[state], self.tooltip)

    def OnTaskBarMenu(self, dummyEvent):
        self.menu.Enable(ID_HIDE, eg.document.frame is not None)
        self.PopupMenu(self.menu)

    def Open(self):
        self.Show()

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

    def SetToolTip(self, tooltip):
        self.tooltip = tooltip
        wx.CallAfter(self.SetIcon, self.stateIcons[self.currentState], tooltip)

    def Show(self):
        self.SetIcon(self.stateIcons[0], self.tooltip)

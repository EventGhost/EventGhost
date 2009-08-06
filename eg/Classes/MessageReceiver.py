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
from eg.WinApi.Dynamic import (
    WM_SIZE, CW_USEDEFAULT, WS_OVERLAPPEDWINDOW, GetModuleHandle, WNDCLASS,
    RegisterClass, CreateWindowEx, byref, WNDPROC, WinError, DefWindowProc,
    SetClipboardViewer, ChangeClipboardChain, WM_CHANGECBCHAIN,
    WM_DRAWCLIPBOARD, SendMessage, WM_USER
)

class MessageReceiver(eg.ThreadWorker):
    """
    A thread with a hidden window to receive win32 messages for different
    purposes.
    """
    def __init__(self):
        self.messageProcs = {}
        eg.ThreadWorker.__init__(self)
        wndclass = WNDCLASS()
        wndclass.lpfnWndProc = WNDPROC(self.MyWndProc)
        wndclass.hInstance = GetModuleHandle(None)
        wndclass.lpszMenuName = None
        wndclass.lpszClassName = "HiddenMessageReceiver"
        if not RegisterClass(byref(wndclass)):
            raise WinError()
        self.wndclass = wndclass
        self.hwnd = None
        self.hwndNextViewer = None
        self.nextWmUserMsg = WM_USER + 1000
        self.wmUserHandlers = {}
        self.freeWmUserMsgs = []

    @eg.LogIt
    def Setup(self):
        self.hwnd = CreateWindowEx(
            0,
            self.wndclass.lpszClassName,
            "EventGhost Message Receiver",
            WS_OVERLAPPEDWINDOW,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            CW_USEDEFAULT,
            0,
            0,
            self.wndclass.hInstance,
            None
        )
        if not self.hwnd:
            raise WinError()
        #self.hinst = wndclass.hInstance
        self.AddHandler(WM_CHANGECBCHAIN, self.OnChangeClipboardChain)
        self.hwndNextViewer = SetClipboardViewer(self.hwnd)
        self.AddHandler(WM_DRAWCLIPBOARD, self.OnDrawClipboard)


    def AddHandler(self, mesg, handler):
        if mesg not in self.messageProcs:
            self.messageProcs[mesg] = [handler]
        else:
            self.messageProcs[mesg].append(handler)


    def RemoveHandler(self, mesg, handler):
        self.messageProcs[mesg].remove(handler)
        if len(self.messageProcs[mesg]) == 0:
            del self.messageProcs[mesg]


    def AddWmUserHandler(self, handler):
        if len(self.freeWmUserMsgs):
            msg = self.freeWmUserMsgs.pop()
        else:
            msg = self.nextWmUserMsg
            self.nextWmUserMsg += 1
            if self.nextWmUserMsg > 0x7FFF:
                raise Exception("Running out of WM_USER messages")
        self.wmUserHandlers[handler] = msg
        self.AddHandler(msg, handler)
        return msg


    def RemoveWmUserHandler(self, handler):
        msg = self.wmUserHandlers[handler]
        del self.wmUserHandlers[handler]
        self.freeWmUserMsgs.append(msg)
        self.RemoveHandler(msg, handler)
        return msg


    def MyWndProc(self, hwnd, mesg, wParam, lParam):
        if mesg == WM_SIZE:
            #print "MessageReceiver sized"
            return 0
        if not mesg in self.messageProcs:
            return DefWindowProc(hwnd, mesg, wParam, lParam)
        for handler in self.messageProcs[mesg]:
            res = handler(hwnd, mesg, wParam, lParam)
            if res == 0:
                return 0
        return 1


    @eg.LogIt
    def OnChangeClipboardChain(self, dummyHwnd, mesg, wParam, lParam):
        # if the next clipboard viewer window is closing, repair the chain.
        if wParam == self.hwndNextViewer:
            self.hwndNextViewer = lParam
            if self.hwndNextViewer == self.hwnd:
                self.hwndNextViewer = None
        elif self.hwndNextViewer:
            SendMessage(self.hwndNextViewer, mesg, wParam, lParam)
        return 0


    def OnDrawClipboard(self, dummyHwnd, mesg, wParam, lParam):
        wx.CallAfter(eg.Notify, "ClipboardChange")
        # pass the message to the next window in the clipboard viewer chain
        if self.hwndNextViewer:
            SendMessage(self.hwndNextViewer, mesg, wParam, lParam)


    @eg.LogIt
    def Close(self):
        ChangeClipboardChain(self.hwnd, self.hwndNextViewer)
        self.hwnd = None
        self.Stop()


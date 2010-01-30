# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2010 Lars-Peter Voss <bitmonster@eventghost.org>
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
from eg.WinApi.Dynamic import (
    cast, WM_SIZE, CW_USEDEFAULT, WS_OVERLAPPEDWINDOW, GetModuleHandle, 
    WNDCLASS, RegisterClass, CreateWindowEx, byref, WNDPROC, WinError, 
    DefWindowProc, WM_USER, UnregisterClass, DestroyWindow, LPCTSTR
)


class MessageReceiver(eg.ThreadWorker):
    """
    An eg.ThreadWorker with a invisible window to receive win32 messages for 
    different purposes.
    """
    def __init__(self, windowName):
        self.windowName = windowName
        self.messageProcs = {
            WM_SIZE: [self.WmSizeHandler],
        }
        eg.ThreadWorker.__init__(self)
        wndclass = WNDCLASS()
        wndclass.lpfnWndProc = WNDPROC(self.MyWndProc)
        wndclass.hInstance = GetModuleHandle(None)
        wndclass.lpszMenuName = None
        wndclass.lpszClassName = self.windowName + "MessageReceiver"
        self.classAtom = RegisterClass(byref(wndclass))
        if not self.classAtom:
            raise WinError()
        self.wndclass = wndclass
        self.hwnd = None
        self.nextWmUserMsg = WM_USER + 1000
        self.wmUserHandlers = {}
        self.freeWmUserMsgs = []


    @eg.LogIt
    def Setup(self):
        self.hwnd = CreateWindowEx(
            0,
            self.wndclass.lpszClassName,
            self.windowName,
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


    def Finish(self):
        if not DestroyWindow(self.hwnd):
            raise WinError()
        self.hwnd = None
        
        
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


    def WmSizeHandler(self, hwnd, mesg, wParam, lParam):
        #print "MessageReceiver sized"
        return 0
        
        
    def MyWndProc(self, hwnd, mesg, wParam, lParam):
        if not mesg in self.messageProcs:
            return DefWindowProc(hwnd, mesg, wParam, lParam)
        for handler in self.messageProcs[mesg]:
            res = handler(hwnd, mesg, wParam, lParam)
            if res == 0:
                return 0
        return 1


    @eg.LogIt
    def Stop(self):
        self.messageProcs.clear()
        eg.ThreadWorker.Stop(self, 5.0)
        if not UnregisterClass(
            cast(self.classAtom, LPCTSTR), 
            GetModuleHandle(None)
        ):
            raise WinError()


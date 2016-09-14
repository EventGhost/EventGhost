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

# Local imports
import eg
from eg.WinApi.Dynamic import (
    byref, cast, CreateWindowEx, CW_USEDEFAULT, DefWindowProc, DestroyWindow,
    GetModuleHandle, LPCTSTR, RegisterClass, UnregisterClass, WinError,
    WM_SIZE, WM_USER, WNDCLASS, WNDPROC, WS_OVERLAPPEDWINDOW,
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
        wndclass = WNDCLASS(
            lpfnWndProc = WNDPROC(self.WindowProc),
            hInstance = GetModuleHandle(None),
            lpszMenuName = None,
            lpszClassName = self.windowName + "MessageReceiver",
        )
        self.classAtom = RegisterClass(byref(wndclass))
        if not self.classAtom:
            raise WinError()
        self.wndclass = wndclass
        self.hwnd = None
        self.nextWmUserMsg = WM_USER + 1000
        self.wmUserHandlers = {}
        self.freeWmUserMsgs = []

    def AddHandler(self, mesg, handler):
        if mesg not in self.messageProcs:
            self.messageProcs[mesg] = [handler]
        else:
            self.messageProcs[mesg].append(handler)

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

    def Finish(self):
        """
        Overrides eg.ThreadWorker.Finish to destroy the window instance.
        """
        if not DestroyWindow(self.hwnd):
            raise WinError()
        self.hwnd = None

    def RemoveHandler(self, mesg, handler):
        self.messageProcs[mesg].remove(handler)
        if len(self.messageProcs[mesg]) == 0:
            del self.messageProcs[mesg]

    def RemoveWmUserHandler(self, handler):
        msg = self.wmUserHandlers[handler]
        del self.wmUserHandlers[handler]
        self.freeWmUserMsgs.append(msg)
        self.RemoveHandler(msg, handler)
        return msg

    @eg.LogIt
    def Setup(self):
        """
        Overrides eg.ThreadWorker.Setup to create the window instance.
        """
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

    @eg.LogIt
    def Stop(self):
        self.messageProcs.clear()
        eg.ThreadWorker.Stop(self, 5.0)
        if not UnregisterClass(
            cast(self.classAtom, LPCTSTR),
            GetModuleHandle(None)
        ):
            raise WinError()

    def WindowProc(self, hwnd, mesg, wParam, lParam):
        if mesg not in self.messageProcs:
            return DefWindowProc(hwnd, mesg, wParam, lParam)
        for handler in self.messageProcs[mesg]:
            res = handler(hwnd, mesg, wParam, lParam)
            if res == 0:
                return 0
        return 1

    def WmSizeHandler(self, hwnd, mesg, wParam, lParam):
        #print "MessageReceiver sized"
        return 0

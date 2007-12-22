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


from ctypes.dynamic import (
    WM_SIZE, CW_USEDEFAULT, WS_OVERLAPPEDWINDOW, GetModuleHandle, WNDCLASS,
    RegisterClass, CreateWindowEx, byref, WNDPROC, WinError, DefWindowProc,
)


class MessageReceiver(eg.ThreadWorker):
    """
    A thread with a hidden window to receive win32 messages for different 
    purposes.
    """
    def __init__(self):
        self.multipleMessageProcs = {}
        eg.ThreadWorker.__init__(self)
        
        
    @eg.LogIt
    def Setup(self):
        wndclass = WNDCLASS()
        wndclass.lpfnWndProc = WNDPROC(self.MyWndProc)
        wndclass.hInstance = GetModuleHandle(None)
        wndclass.lpszMenuName = None
        wndclass.lpszClassName = "HiddenMessageReceiver"
        if not RegisterClass(byref(wndclass)):
            raise WinError()
        self.hwnd = CreateWindowEx(
            0,
            wndclass.lpszClassName,
            "EventGhost Message Receiver",
            WS_OVERLAPPEDWINDOW,
            CW_USEDEFAULT, 
            CW_USEDEFAULT,
            CW_USEDEFAULT, 
            CW_USEDEFAULT,
            0, 
            0,
            wndclass.hInstance, 
            None
        )
        if not self.hwnd:
            raise WinError()
        self.wc = wndclass
        self.hinst = wndclass.hInstance
        
        
    def AddHandler(self, mesg, handler):
        if mesg not in self.multipleMessageProcs:
            self.multipleMessageProcs[mesg] = [handler]
        else:
            self.multipleMessageProcs[mesg].append(handler)
            
        
    def RemoveHandler(self, mesg, handler):
        self.multipleMessageProcs[mesg].remove(handler)
        if len(self.multipleMessageProcs[mesg]) == 0:
            del self.multipleMessageProcs[mesg]
            
    
    @eg.LogIt
    def MyWndProc(self, hwnd, mesg, wParam, lParam):
        if mesg == WM_SIZE:
            print "MessageReceiver sized"
            return 0
        if not mesg in self.multipleMessageProcs:
            return DefWindowProc(hwnd, mesg, wParam, lParam)
        for handler in self.multipleMessageProcs[mesg]:
            res = handler(hwnd, mesg, wParam, lParam)
            if res == 0:
                return 0
        return 1
    
        
    @eg.LogIt
    def Close(self):
        self.hwnd = None
        self.Stop()
        
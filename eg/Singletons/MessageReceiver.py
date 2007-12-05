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


import win32gui
import win32api
import win32con



class MessageReceiver(eg.ThreadWorker):
    """
    A thread with a hidden window to receive win32 messages for different 
    purposes.
    """
    def __init__(self):
        self.messageProcs = {}
        self.multipleMessageProcs = {}
        eg.ThreadWorker.__init__(self)
        
        
    @eg.LogIt
    def Setup(self):
        wc = win32gui.WNDCLASS()
        wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "HiddenMessageReceiver"
        wc.style = win32con.CS_VREDRAW|win32con.CS_HREDRAW;
        wc.hCursor = win32gui.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = self.messageProcs
        classAtom = win32gui.RegisterClass(wc)
        self.hwnd = win32gui.CreateWindow(
            classAtom,
            "EventGhost Message Receiver",
            win32con.WS_OVERLAPPED|win32con.WS_SYSMENU,
            0, 
            0,
            win32con.CW_USEDEFAULT, 
            win32con.CW_USEDEFAULT,
            0, 
            0,
            wc.hInstance, 
            None
        )
        self.wc = wc
        self.classAtom = classAtom
        self.hinst = wc.hInstance
        
        
    def AddHandler(self, mesg, handler):
        if mesg not in self.messageProcs:
            self.multipleMessageProcs[mesg] = [handler]
            self.messageProcs[mesg] = self.MyWndProc
        else:
            self.multipleMessageProcs[mesg].append(handler)
            
        
    def RemoveHandler(self, mesg, handler):
        self.multipleMessageProcs[mesg].remove(handler)
        if len(self.multipleMessageProcs[mesg]) == 0:
            del self.messageProcs[mesg]
            del self.multipleMessageProcs[mesg]
            
    
    def MyWndProc(self, hwnd, mesg, wParam, lParam):
        if mesg == win32con.WM_SIZE:
            print "sized"
            return 0
        for handler in self.multipleMessageProcs[mesg]:
            res = handler(hwnd, mesg, wParam, lParam)
            if res == 0:
                return 0
        return 1
    
        
    @eg.LogIt
    def Close(self):
        self.hwnd = None
        self.Stop()
        
# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <lpv@eventghost.org>
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

class PluginInfo(eg.PluginInfo):
    name = "Task Create/Switch Events"
    author = "Bitmonster"
    version = "1.0.0"
    description = "Generates events if tasks are created or switched."
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABuklEQVR42o1Sv0tCYRQ9"
        "L1FccpCEB73wVy1NjTrUPxD1lgZp0dWKaAhXxWhoyWgoIUjHBEH65RSE0CAUgWIPLAqR"
        "gkAQIQXR8nW/Z0ai6btweJfDd847934fhz8VCARkqCjTmBGra+sc67kOGQqFZIfDMVCo"
        "1WphMpng9/vxkMvi9u6e4zp/ZmStVkOpVOor1mg00Ol0CIfDKBQK/Q1isRhcLhedJpIn"
        "vHXkI+D5SUSj+0in0wMM4mSw6WqL9whLhHeCYAA/tobo9twQgxsyEMjglUj6IE7YIJxQ"
        "gk9K8DwsgTLCMjGGdvJxJibMUgJ+hUaYGWyQSCQQDO7+ZO8uo1EHn8/2v4Hb7UYmkxl4"
        "jY1GA9lsFrlcDl+fDZxfJNsGHo9H1QNiVa/XlQSiuIAp2wS466ukHNjaUauHXq+H0+n8"
        "HYPrzF+pVHriSpLUxbGHJAgCIpFIr0EqlYI0KmH6Y1o5XC6XaaFBpW+1WqhWq7BYLLRI"
        "X9ciFQNRFJHP53FoO4T3xdsTu9lsolgswm63Kz1b9tPTI6xmAVzk+Eg+PbtUvQNWstxS"
        "xHv7B+1bEBfnVd8CK6vFrIhZ/w1wBAQrC42uqQAAAABJRU5ErkJggg=="
    )


import wx
import os
from win32gui import GetWindowLong, EnumWindows, GetDesktopWindow 
from win32api import RegisterWindowMessage, OpenProcess, CloseHandle
from win32process import GetWindowThreadProcessId, GetModuleFileNameEx

import ctypes

RegisterShellHookWindow = ctypes.windll.user32.RegisterShellHookWindow
DeregisterShellHookWindow = ctypes.windll.user32.DeregisterShellHookWindow

WM_SHELLHOOKMESSAGE = RegisterWindowMessage("SHELLHOOK")

HSHELL_WINDOWCREATED       = 1
HSHELL_WINDOWDESTROYED     = 2
HSHELL_ACTIVATESHELLWINDOW = 3
HSHELL_WINDOWACTIVATED     = 4
HSHELL_GETMINRECT          = 5
HSHELL_REDRAW              = 6
HSHELL_TASKMAN             = 7
HSHELL_LANGUAGE            = 8

PROCESS_VM_READ = 16
PROCESS_QUERY_INFORMATION = 1024
GWL_STYLE = -16
WS_VISIBLE = 0x10000000



def GetWindowProcessName(hwnd):
    _, processId = GetWindowThreadProcessId(hwnd)
    if processId == 0:
        return "Desktop"
    try:
        hProcess = OpenProcess(
            PROCESS_QUERY_INFORMATION|PROCESS_VM_READ,
            False, 
            processId
        )
    except:
        return "Desktop"
    try:
        fstr = GetModuleFileNameEx(hProcess, 0)
    except:
        CloseHandle(hProcess)
        return None
    fstr = os.path.basename(fstr)
    fstr, _ = os.path.splitext(fstr)
    CloseHandle(hProcess)
    return fstr
    
    

class Task(eg.PluginClass):

    def __start__(
        self, 
        created=True, 
        destroyed=True,
        activated=True, 
        deactivated=True
    ):
        self.lastActivated = ""
        self.lastDestroyed = ""
        self.windowList = windowList = {}
        def MyEnumFunc(hwnd, lParam):
            if (GetWindowLong(hwnd, GWL_STYLE) & WS_VISIBLE) > 0:
                windowList[hwnd] = 1
        EnumWindows(MyEnumFunc, None)
        eg.messageReceiver.AddHandler(WM_SHELLHOOKMESSAGE, self.MyWndProc)
        RegisterShellHookWindow(eg.messageReceiver.hwnd)
        
        
        
    def __stop__(self):
        DeregisterShellHookWindow(eg.messageReceiver.hwnd)
        eg.messageReceiver.RemoveHandler(WM_SHELLHOOKMESSAGE, self.MyWndProc)
        
        
    def MyWndProc(self, hwnd, mesg, wParam, lParam):
        windowList = self.windowList
        if wParam == HSHELL_WINDOWCREATED:
            fstr = GetWindowProcessName(lParam)
            if fstr:
                windowList[lParam] = fstr
                self.TriggerEvent("Created." + fstr)
                self.lastDestroyed = ""
        elif wParam == HSHELL_WINDOWDESTROYED:
            fstr = GetWindowProcessName(lParam)
            if windowList.has_key(lParam) and windowList[lParam] != 1:
                fstr = windowList[lParam]
                del windowList[lParam]
            if fstr and fstr != "Desktop" and fstr != "Explorer":
                if self.lastActivated == fstr:
                    self.TriggerEvent("Deactivated." + fstr)
                    self.lastActivated = ''
                if fstr != self.lastDestroyed:
                    self.TriggerEvent("Destroyed." + fstr)
                    self.lastDestroyed = fstr
        elif wParam == HSHELL_WINDOWACTIVATED or wParam == 0x8004:
            fstr = GetWindowProcessName(lParam)
            if fstr and fstr != self.lastActivated:
                if self.lastActivated:
                    self.TriggerEvent("Deactivated." + self.lastActivated)
                self.TriggerEvent("Activated." + fstr)
                self.lastActivated = fstr
        return 1



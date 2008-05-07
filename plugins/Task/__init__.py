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


eg.RegisterPlugin(
    name = "Task Create/Switch Events",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    description = (
        "Generates events if an application starts, exits or "
        "gets switched into focus."
    ),
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
    ),
)


from os.path import abspath, join, dirname, splitext
from eg.WinApi.Dynamic import (
    DWORD, CDLL, byref, GetWindowThreadProcessId, RegisterWindowMessage,
    RegisterShellHookWindow, DeregisterShellHookWindow, GetWindowLong,
    EnumWindows, WM_APP, WINFUNCTYPE, BOOL, HWND, LPARAM, GWL_STYLE, 
    HSHELL_WINDOWCREATED, HSHELL_WINDOWDESTROYED, HSHELL_WINDOWACTIVATED,
    WS_VISIBLE, 
)
from eg.WinApi.Utils import GetProcessName

EnumWindowsProc = WINFUNCTYPE(BOOL, HWND, LPARAM)
EnumWindows.argtypes = [EnumWindowsProc, LPARAM]

WM_SHELLHOOKMESSAGE = RegisterWindowMessage("SHELLHOOK")



def GetWindowProcessName(hwnd):
    dwProcessId = DWORD()
    dwThreadId = GetWindowThreadProcessId(hwnd, byref(dwProcessId))
    processId = dwProcessId.value
    if processId == 0:
        return "Desktop"
    return splitext(GetProcessName(processId))[0]
    
    

class Task(eg.PluginClass):
    
    hookDll = None
    
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
            return 1
        EnumWindows(EnumWindowsProc(MyEnumFunc), 0)
        eg.messageReceiver.AddHandler(WM_SHELLHOOKMESSAGE, self.MyWndProc)
        eg.messageReceiver.AddHandler(WM_APP+1, self.FocusWndProc)
        eg.messageReceiver.AddHandler(WM_APP+2, self.FatalWndProc)
        RegisterShellHookWindow(eg.messageReceiver.hwnd)
        self.hookDll = CDLL(abspath(join(dirname(__file__), "hook.dll")))
        self.hookDll.StartHook()
        
        
    def __stop__(self):
        self.hookDll.StopHook()
        DeregisterShellHookWindow(eg.messageReceiver.hwnd)
        eg.messageReceiver.RemoveHandler(WM_SHELLHOOKMESSAGE, self.MyWndProc)
        eg.messageReceiver.RemoveHandler(WM_APP+1, self.FocusWndProc)
        eg.messageReceiver.RemoveHandler(WM_APP+2, self.FatalWndProc)
        
        
    @eg.LogIt
    def FatalWndProc(self, hwnd, mesg, wParam, lParam):
        print "DLL_PROCESS_DETACH", wParam, lParam
    
    
    def FocusWndProc(self, hwnd, mesg, wParam, lParam):
        if wParam == 0:
            return
        fstr = GetWindowProcessName(wParam)
        if fstr and fstr != self.lastActivated:
            if self.lastActivated:
                self.TriggerEvent("Deactivated." + self.lastActivated)
            self.TriggerEvent("Activated." + fstr)
            self.lastActivated = fstr
    
    
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
            if lParam in windowList and windowList[lParam] != 1:
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



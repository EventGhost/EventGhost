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

import eg

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

import wx
from os.path import abspath, join, dirname, splitext
from eg.WinApi.Dynamic import (
    DWORD, CDLL, byref, GetWindowThreadProcessId, RegisterWindowMessage,
    RegisterShellHookWindow, DeregisterShellHookWindow, GetWindowLong,
    EnumWindows, WM_APP, WINFUNCTYPE, BOOL, HWND, LPARAM, GWL_STYLE, 
    HSHELL_WINDOWCREATED, HSHELL_WINDOWDESTROYED, HSHELL_WINDOWACTIVATED,
    WS_VISIBLE, GWL_HWNDPARENT
)
from eg.WinApi.Utils import GetProcessName

ENUM_WINDOWS_PROC_TYPE = WINFUNCTYPE(BOOL, HWND, LPARAM)
EnumWindows.argtypes = [ENUM_WINDOWS_PROC_TYPE, LPARAM]

WM_SHELLHOOKMESSAGE = RegisterWindowMessage("SHELLHOOK")
DEBUG = 0


def GetWindowProcessName(hwnd):
    dwProcessId = DWORD()
    GetWindowThreadProcessId(hwnd, byref(dwProcessId))
    processId = dwProcessId.value
    if processId == 0:
        return "explorer"
    return splitext(GetProcessName(processId))[0]
    
    

class Task(eg.PluginBase):
    
    def __start__(self, *dummyArgs):
        self.lastActivated = ""
        self.processes = processes = {}
        def MyEnumFunc(hwnd, dummyLParam):
            if (GetWindowLong(hwnd, GWL_STYLE) & WS_VISIBLE) > 0:
                if GetWindowLong(hwnd, GWL_HWNDPARENT):
                    return 1
                processName = GetWindowProcessName(hwnd)
                if processName in processes:
                    processes[processName].append(hwnd)
                else:
                    processes[processName] = [hwnd]
            return 1
        EnumWindows(ENUM_WINDOWS_PROC_TYPE(MyEnumFunc), 0)
        eg.messageReceiver.AddHandler(WM_APP+1, self.WindowGotFocusProc)
        eg.messageReceiver.AddHandler(WM_APP+2, self.WindowCreatedProc)
        eg.messageReceiver.AddHandler(WM_APP+3, self.WindowDestroyedProc)
        eg.messageReceiver.AddHandler(WM_SHELLHOOKMESSAGE, self.MyWndProc)
        RegisterShellHookWindow(eg.messageReceiver.hwnd)
        self.hookDll = CDLL(abspath(join(dirname(__file__), "hook.dll")))
        self.hookDll.StartHook()
        
        
    def __stop__(self):
        self.hookDll.StopHook()
        DeregisterShellHookWindow(eg.messageReceiver.hwnd)
        eg.messageReceiver.RemoveHandler(WM_SHELLHOOKMESSAGE, self.MyWndProc)
        eg.messageReceiver.RemoveHandler(WM_APP+1, self.WindowGotFocusProc)
        eg.messageReceiver.RemoveHandler(WM_APP+2, self.WindowCreatedProc)
        eg.messageReceiver.RemoveHandler(WM_APP+3, self.WindowDestroyedProc)
        
        
    def WindowCreatedProc(self, dummyHwnd, dummyMesg, hwnd, dummyLParam):
        processName = GetWindowProcessName(hwnd)
        if DEBUG:
            eg.Print("CreateWndProc", processName, hwnd)
        if processName:
            if processName in self.processes:
                self.processes[processName].append(hwnd)
            else:
                self.TriggerEvent("Created." + processName)
                self.processes[processName] = [hwnd]
            self.TriggerEvent("NewWindow." + processName)
            
    
    def WindowDestroyedProc(self, dummyHwnd, dummyMesg, hwnd, dummyLParam):
        processName = GetWindowProcessName(hwnd)
        if DEBUG:
            eg.Print("DestroyWndProc", processName, hwnd)
        if processName in self.processes:
            processEntry = self.processes[processName]
            if len(processEntry) <= 1:
                del self.processes[processName]
                if self.lastActivated == processName:
                    self.TriggerEvent("Deactivated." + processName)
                    self.lastActivated = ''
                self.TriggerEvent("ClosedWindow." + processName)
                self.TriggerEvent("Destroyed." + processName)
            else:
                try:
                    processEntry.remove(hwnd)
                except ValueError:
                    pass
                self.TriggerEvent("ClosedWindow." + processName)
    
    
    def WindowGotFocusProc(self, dummyHwnd, dummyMesg, hwnd, dummyLParam):
        processName = GetWindowProcessName(hwnd)
        if DEBUG:
            eg.Print("FocusWndProc", processName, hwnd)
        if processName and processName != self.lastActivated:
            if self.lastActivated:
                self.TriggerEvent("Deactivated." + self.lastActivated)
            if processName not in self.processes:
                self.processes[processName] = []
                self.TriggerEvent("Created." + processName)
                self.TriggerEvent("NewWindow." + processName)
            self.TriggerEvent("Activated." + processName)
            self.lastActivated = processName
    

    def MyWndProc(self, hwnd, mesg, wParam, lParam):
        if wParam == HSHELL_WINDOWACTIVATED or wParam == 0x8004:
            processName = GetWindowProcessName(lParam)
            if processName and processName != self.lastActivated:
                if self.lastActivated:
                    self.TriggerEvent("Deactivated." + self.lastActivated)
                self.TriggerEvent("Activated." + processName)
                self.lastActivated = processName
        return 1


    
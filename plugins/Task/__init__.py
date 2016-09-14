# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
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

from os.path import abspath, dirname, join, splitext

# Local imports
import eg
from eg.WinApi import GetClassName, GetTopLevelWindowList
from eg.WinApi.Dynamic import (
    BOOL, byref, CDLL, DeregisterShellHookWindow, DWORD, EnumWindows,
    FreeLibrary, GA_ROOT, GetAncestor, GetShellWindow, GetWindowLong,
    GetWindowThreadProcessId, GWL_HWNDPARENT, HSHELL_WINDOWACTIVATED,
    HSHELL_WINDOWCREATED, HSHELL_WINDOWDESTROYED, HWND, IsWindowVisible,
    LPARAM, RegisterShellHookWindow, RegisterWindowMessage, WINFUNCTYPE,
    WM_APP,
)
from eg.WinApi.Utils import GetProcessName

eg.RegisterPlugin(
    name = "Task Monitor",
    author = (
        "Bitmonster",
        "blackwind",
    ),
    version = "1.0.4",
    guid = "{D1748551-C605-4423-B392-FB77E6842437}",
    description = (
        "Generates events when an application starts, exits, flashes the "
        "taskbar, or gets switched into focus."
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

ENUM_WINDOWS_PROC_TYPE = WINFUNCTYPE(BOOL, HWND, LPARAM)
EnumWindows.argtypes = [ENUM_WINDOWS_PROC_TYPE, LPARAM]

WM_SHELLHOOKMESSAGE = RegisterWindowMessage("SHELLHOOK")

class Task(eg.PluginBase):
    def __init__(self):
        self.AddEvents()

    def __start__(self, *dummyArgs):
        self.names, self.hwnds = EnumProcesses()
        self.flashing = set()
        self.lastActivated = None
        eg.messageReceiver.AddHandler(WM_APP + 1, self.WindowGotFocusProc)
        eg.messageReceiver.AddHandler(WM_APP + 2, self.WindowCreatedProc)
        eg.messageReceiver.AddHandler(WM_APP + 3, self.WindowDestroyedProc)
        eg.messageReceiver.AddHandler(WM_SHELLHOOKMESSAGE, self.MyWndProc)
        RegisterShellHookWindow(eg.messageReceiver.hwnd)
        self.hookDll = CDLL(abspath(join(dirname(__file__), "TaskHook.dll")))
        self.hookDll.StartHook()
        trayWindow = 0
        if "explorer" in self.names:
            for hwnd in self.names["explorer"].hwnds:
                if GetClassName(hwnd) == "Shell_TrayWnd":
                    trayWindow = hwnd
                    break
        self.desktopHwnds = (GetShellWindow(), trayWindow)

    def __stop__(self):
        self.hookDll.StopHook()
        FreeLibrary(self.hookDll._handle)
        DeregisterShellHookWindow(eg.messageReceiver.hwnd)
        eg.messageReceiver.RemoveHandler(WM_SHELLHOOKMESSAGE, self.MyWndProc)
        eg.messageReceiver.RemoveHandler(WM_APP + 1, self.WindowGotFocusProc)
        eg.messageReceiver.RemoveHandler(WM_APP + 2, self.WindowCreatedProc)
        eg.messageReceiver.RemoveHandler(WM_APP + 3, self.WindowDestroyedProc)

    def CheckWindow(self, hwnd):
        hwnd2 = GetAncestor(hwnd, GA_ROOT)
        if hwnd == 0 or hwnd2 in self.desktopHwnds:
            return "Desktop", 0
        if hwnd != hwnd2:
            return
        if GetWindowLong(hwnd, GWL_HWNDPARENT):
            return
        if not IsWindowVisible(hwnd):
            return

        if hwnd in self.hwnds:
            return self.hwnds[hwnd].name, hwnd

        pid = GetWindowPid(hwnd)
        name = splitext(GetProcessName(pid))[0]
        processInfo = self.names.get(name, None)
        if not processInfo:
            processInfo = ProcessInfo(name)
            self.names[name] = processInfo
            self.TriggerEvent("Created." + name)

        processInfo.hwnds.add(hwnd)
        self.hwnds[hwnd] = processInfo
        self.TriggerEvent("NewWindow." + name)
        return name, hwnd

    def MyWndProc(self, dummyHwnd, dummyMesg, wParam, lParam):
        if wParam == HSHELL_WINDOWDESTROYED:
            self.WindowDestroyedProc(None, None, lParam, None)
        elif wParam in (HSHELL_WINDOWACTIVATED, HSHELL_WINDOWCREATED, 0x8004):
            self.WindowGotFocusProc(None, None, lParam, None)
        elif wParam == 0x8006:
            self.WindowFlashedProc(None, None, lParam, None)
        return 1

    def WindowCreatedProc(self, dummyHwnd, dummyMesg, hwnd, dummyLParam):
        self.CheckWindow(hwnd)

    def WindowDestroyedProc(self, dummyHwnd, dummyMesg, hwnd, dummyLParam):
        #hwnd2 = GetAncestor(hwnd, GA_ROOT)
        processInfo = self.hwnds.get(hwnd, None)
        if processInfo:
            processInfo.hwnds.remove(hwnd)
            del self.hwnds[hwnd]
            name = processInfo.name
            if (name, hwnd) == self.lastActivated:
                self.TriggerEvent("Deactivated." + name)
                self.lastActivated = None
            self.TriggerEvent("ClosedWindow." + name)
            if len(processInfo.hwnds) == 0:
                self.TriggerEvent("Destroyed." + name)
                self.names.pop(name, None)

    def WindowFlashedProc(self, dummyHwnd, dummyMesg, hwnd, dummyLParam):
        processInfo = self.hwnds.get(hwnd, None)
        if processInfo and hwnd not in self.flashing:
            self.flashing.add(hwnd)
            self.TriggerEvent("Flashed." + processInfo.name)

    def WindowGotFocusProc(self, dummyHwnd, dummyMesg, hwnd, dummyLParam):
        ident = self.CheckWindow(hwnd)
        if ident and ident != self.lastActivated:
            if hwnd in self.flashing:
                self.flashing.remove(hwnd)
            if self.lastActivated:
                self.TriggerEvent("Deactivated." + self.lastActivated[0])
            self.TriggerEvent("Activated." + ident[0])
            self.lastActivated = ident


class ProcessInfo(object):
    def __init__(self, name):
        self.name = name
        self.hwnds = set()


def EnumProcesses():
    names = {}
    hwnds = {}
    dwProcessId = DWORD()
    for hwnd in GetTopLevelWindowList(False):
        GetWindowThreadProcessId(hwnd, byref(dwProcessId))
        pid = dwProcessId.value
        name = splitext(GetProcessName(pid))[0]
        if name not in names:
            processInfo = ProcessInfo(name)
            names[name] = processInfo
        else:
            processInfo = names[name]
        processInfo.hwnds.add(hwnd)
        hwnds[hwnd] = processInfo
    return names, hwnds

def GetWindowPid(hwnd):
    dwProcessId = DWORD()
    GetWindowThreadProcessId(hwnd, byref(dwProcessId))
    return dwProcessId.value

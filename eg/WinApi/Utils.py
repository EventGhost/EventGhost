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

import ctypes
import sys
import wx
from ctypes.wintypes import LPWSTR, GetLastError
from win32api import OpenProcess, TerminateProcess
from win32com.client import GetObject

# Local imports
import eg
import Dynamic
from cFunctions import GetProcessName, GetWindowChildsList
from Dynamic import (
    # ctypes stuff
    byref, sizeof, WinError, _kernel32,
    # functions
    AttachThreadInput, BringWindowToTop, CreatePen, DeleteObject,
    EnumChildWindows, EnumDisplayMonitors, FindWindow, GetAncestor,
    GetClassLong, GetCurrentThreadId, GetCursorPos, GetDC, GetForegroundWindow,
    GetParent, GetStockObject, GetSystemMetrics, GetWindowDC, GetWindowLong,
    GetWindowRect, GetWindowThreadProcessId, InvalidateRect, IsIconic,
    IsWindow, IsWindowVisible, PtVisible, Rectangle, ReleaseDC, RestoreDC,
    SaveDC, ScreenToClient, SelectObject, SendMessageTimeout,
    SendNotifyMessage, SetROP2, ShowWindow, UpdateWindow, WindowFromPoint,
    # types
    BOOL, DWORD, HWND, LPARAM, MONITORENUMPROC, POINT, RECT, RGB, WINFUNCTYPE,
    # constants
    GA_ROOT, GCL_HICON, GCL_HICONSM, GWL_EXSTYLE, ICON_BIG, ICON_SMALL,
    NULL_BRUSH, PS_INSIDEFRAME, R2_NOT, SC_CLOSE, SM_CXBORDER,
    SMTO_ABORTIFHUNG, SMTO_BLOCK, SW_RESTORE, SW_SHOWNA, WM_GETICON,
    WM_SYSCOMMAND, WS_EX_TOPMOST,
)
from Dynamic.PsApi import EnumProcesses

ENUM_CHILD_PROC = WINFUNCTYPE(BOOL, HWND, LPARAM)
EnumChildWindows.argtypes = [HWND, ENUM_CHILD_PROC, LPARAM]

_H_BORDERWIDTH = 3 * GetSystemMetrics(SM_CXBORDER)
_H_BORDERCOLOUR = RGB(255, 0, 0)

FORMAT_MESSAGE_ALLOCATE_BUFFER = 0x00000100
FORMAT_MESSAGE_FROM_SYSTEM = 0x00001000
FORMAT_MESSAGE_IGNORE_INSERTS = 0x00000200

def BestWindowFromPoint(point):
    x, y = point
    foundWindow = WindowFromPoint(POINT(x, y))

    hWnds = GetWindowChildsList(GetAncestor(foundWindow, GA_ROOT), True)
    if not hWnds:
        return foundWindow
    foundWindowArea = sys.maxint
    rect = RECT()
    clientPoint = POINT()
    for hWnd in hWnds:
        GetWindowRect(hWnd, byref(rect))
        if (
            x >= rect.left and
            x <= rect.right and
            y >= rect.top and
            y <= rect.bottom
        ):
            hdc = GetDC(hWnd)
            clientPoint.x, clientPoint.y = x, y
            ScreenToClient(hWnd, byref(clientPoint))
            if PtVisible(hdc, clientPoint.x, clientPoint.y):
                area = (rect.right - rect.left) * (rect.bottom - rect.top)
                if area < foundWindowArea:
                    foundWindow = hWnd
                    foundWindowArea = area
            ReleaseDC(hWnd, hdc)
    return foundWindow

def BringHwndToFront(hWnd, invalidate=True):
    if hWnd is None:
        return
    hWnd = GetAncestor(hWnd, GA_ROOT)
    if not IsWindow(hWnd):
        return

    # If the window is in a minimized state, restore now
    if IsIconic(hWnd):
        ShowWindow(hWnd, SW_RESTORE)
        BringWindowToTop(hWnd)
        UpdateWindow(hWnd)

    # Check to see if we are the foreground thread
    foregroundHwnd = GetForegroundWindow()
    foregroundThreadID = GetWindowThreadProcessId(foregroundHwnd, None)
    ourThreadID = GetCurrentThreadId()

    # If not, attach our thread's 'input' to the foreground thread's
    if foregroundThreadID != ourThreadID:
        AttachThreadInput(foregroundThreadID, ourThreadID, True)

    ShowWindow(hWnd, SW_SHOWNA)
    BringWindowToTop(hWnd)
    # Force our window to redraw
    if invalidate:
        InvalidateRect(hWnd, None, True)
    if foregroundThreadID != ourThreadID:
        AttachThreadInput(foregroundThreadID, ourThreadID, False)

def CloseHwnd(hWnd):
    SendNotifyMessage(hWnd, WM_SYSCOMMAND, SC_CLOSE, 0)

def FormatError(code=None):
    """
    A replacement for ctypes.FormtError, but always returns the string
    encoded in CP1252 (ANSI Code Page).
    """
    if code is None:
        code = GetLastError()
    lpMsgBuf = LPWSTR()
    numChars = _kernel32.FormatMessageW(
        (
            FORMAT_MESSAGE_ALLOCATE_BUFFER |
            FORMAT_MESSAGE_FROM_SYSTEM |
            FORMAT_MESSAGE_IGNORE_INSERTS
        ),
        None,
        code,
        0,
        byref(lpMsgBuf),
        0,
        None
    )
    if numChars == 0:
        return "No error message available."
    #raise Exception("FormatMessage failed on 0x%X with 0x%X" % (code & 0xFFFFFFFF, GetLastError()))
    message = lpMsgBuf.value.strip()
    _kernel32.LocalFree(lpMsgBuf)
    return message.encode("CP1252", 'backslashreplace')

# Monkey patch the new FormatError into ctypes
ctypes.FormatError = FormatError
Dynamic.FormatError = FormatError

def GetAlwaysOnTop(hwnd = None):
    hwnd = GetBestHwnd(hwnd)
    style = GetWindowLong(hwnd, GWL_EXSTYLE)
    isAlwaysOnTop = (style & WS_EX_TOPMOST) != 0
    return isAlwaysOnTop

def GetBestHwnd(hwnd = None):
    if isinstance(hwnd, int):
        return hwnd
    elif len(eg.lastFoundWindows):
        return eg.lastFoundWindows[0]
    else:
        return GetForegroundWindow()

def GetContainingMonitor(win):
    monitorDims = GetMonitorDimensions()
    for i in range(len(monitorDims)):
        # If window is entirely on one monitor, return that monitor
        if monitorDims[i].ContainsRect(win):
            return monitorDims[i], i
    else:
        # Otherwise, default to the main monitor
        return monitorDims[0], 0

def GetHwnds(pid = None, processName = None):
    if pid:
        pass
    elif processName:
        pids = GetPids(processName = processName)
        if pids:
            pid = pids[0]
        else:
            return False
    else:
        return False

    def callback(hwnd, hwnds):
        if IsWindowVisible(hwnd):
            _, result = GetWindowThreadProcessId(hwnd)
            if result == pid:
                hwnds.append(hwnd)
        return True

    from win32gui import EnumWindows, IsWindowVisible
    from win32process import GetWindowThreadProcessId
    hwnds = []
    EnumWindows(callback, hwnds)
    return hwnds

def GetHwndChildren(hWnd, invisible):
    """
    Return a list of all direct children of the window 'hwnd'.
    """
    return [
        childHwnd for childHwnd in GetWindowChildsList(hWnd, invisible)
        if GetParent(childHwnd) == hWnd
    ]

def GetHwndIcon(hWnd):
    """
    Get a wx.Icon from a window through its hwnd window handle
    """
    hIcon = DWORD()
    res = SendMessageTimeout(
        hWnd, WM_GETICON, ICON_SMALL, 0, SMTO_ABORTIFHUNG, 1000, byref(hIcon)
    )

    if res == 0:
        hIcon.value = 0
    if hIcon.value < 10:
        hIcon.value = GetClassLong(hWnd, GCL_HICONSM)
        if hIcon.value == 0:
            res = SendMessageTimeout(
                hWnd,
                WM_GETICON,
                ICON_BIG,
                0,
                SMTO_ABORTIFHUNG,
                1000,
                byref(hIcon)
            )
            if res == 0:
                hIcon.value = 0
            if hIcon.value < 10:
                hIcon.value = GetClassLong(hWnd, GCL_HICON)
    if hIcon.value != 0:
        icon = wx.NullIcon
        value = hIcon.value
        # ugly fix for "OverflowError: long int too large to convert to int"
        if value & 0x80000000:
            value = -((value ^ 0xffffffff) + 1)
        icon.SetHandle(value)
        icon.SetSize((16, 16))
        return icon
    else:
        return None

def GetMonitorDimensions():
    retval = []

    def MonitorEnumProc(dummy1, dummy2, lprcMonitor, dummy3):
        displayRect = lprcMonitor.contents
        rect = wx.Rect(
            displayRect.left,
            displayRect.top,
            displayRect.right - displayRect.left,
            displayRect.bottom - displayRect.top
        )
        retval.append(rect)
        return 1
    EnumDisplayMonitors(0, None, MONITORENUMPROC(MonitorEnumProc), 0)

    return retval

def GetPids(processName = None, hwnd = None):
    if processName:
        pass
    elif hwnd:
        return PyGetWindowThreadProcessId(hwnd)[::-1]
    else:
        return False

    try:
        pids = []
        for proc in GetObject("winmgmts:").ExecQuery("SELECT * FROM Win32_Process WHERE Name = '" + str(processName.replace("'", "\\'")) + "'"):
            pids.append(proc.ProcessID)
        return pids
    except:
        return False

# now implemented as C function in cFunctions.pyd
#def GetProcessName(pid):
#    # See http://msdn2.microsoft.com/en-us/library/ms686701.aspx
#    hProcessSnap = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
#    pe32 = PROCESSENTRY32()
#    pe32.dwSize = sizeof(PROCESSENTRY32)
#    try:
#        if Process32First(hProcessSnap, byref(pe32)) == 0:
#            print >> sys.stderr, "Failed getting first process."
#            return "<not found>"
#        while True:
#            if pe32.th32ProcessID == pid:
#                return pe32.szExeFile
#            if Process32Next(hProcessSnap, byref(pe32)) == 0:
#                break
#        return "<not found>"
#    finally:
#        CloseHandle(hProcessSnap)

def GetProcessNameEx(pid = None, hwnd = None, fullPath = False):
    if pid:
        pass
    elif hwnd:
        pid = PyGetWindowThreadProcessId(hwnd)[-1]
    else:
        return False

    try:
        result = GetObject("winmgmts:").ExecQuery("SELECT * FROM Win32_Process WHERE ProcessID = '" + str(int(pid)) + "'")[0]
        return result.ExecutablePath.strip('"') if fullPath else result.Name
    except:
        return False

def GetWindowDimensions(hwnd = None):
    hwnd = GetBestHwnd(hwnd)
    windowDims = RECT()
    GetWindowRect(hwnd, byref(windowDims))
    width = windowDims.right - windowDims.left
    height = windowDims.bottom - windowDims.top
    return wx.Rect(windowDims.left, windowDims.top, width, height)

def GetWindowProcessName(hWnd):
    dwProcessId = DWORD()
    GetWindowThreadProcessId(hWnd, byref(dwProcessId))
    return GetProcessName(dwProcessId.value)

def HighlightWindow(hWnd):
    """
    Draws an inverted rectangle around a window to inform the user about
    the currently selected window.
    """
    UpdateWindow(hWnd)
    # Retrieve location of window on-screen.
    rect = RECT()
    GetWindowRect(hWnd, byref(rect))

    # Get a device context that allows us to write anywhere within the window.
    hdc = GetWindowDC(hWnd)

    # Save the original device context attributes.
    SaveDC(hdc)

    # To guarantee that the frame will be visible, tell Windows to draw the
    # frame using the inverse screen color.
    SetROP2(hdc, R2_NOT)

    # Create a pen that is three times the width of a nonsizeable border. The
    # color will not be used to draw the frame, so its value could be
    # anything. PS_INSIDEFRAME tells windows that the entire frame should be
    # enclosed within the window.
    hpen = CreatePen(PS_INSIDEFRAME, _H_BORDERWIDTH, _H_BORDERCOLOUR)
    SelectObject(hdc, hpen)

    # We must select a NULL brush so that the contents of the window will not
    # be overwritten.
    SelectObject(hdc, GetStockObject(NULL_BRUSH))

    # Draw the frame. Because the device context is relative to the window,
    # the top-left corner is (0, 0) and the lower right corner is (width of
    # window, height of window).
    Rectangle(hdc, 0, 0, rect.right - rect.left, rect.bottom - rect.top)

    # Restore the original attributes and release the device context.
    RestoreDC(hdc, -1)
    ReleaseDC(hWnd, hdc)

    # We can destroy the pen only AFTER we have restored the DC because the DC
    # must have valid objects selected into it at all times.
    DeleteObject(hpen)

def HwndHasChildren(hWnd, invisible):
    """
    Return True if the window 'hwnd' has children.
    If 'invisible' is False, don't take invisible windows into account.
    """
    data = [False]
    if invisible:
        def EnumFunc(hWndChild, lParam):
            data[0] = True
            return False
    else:
        def EnumFunc(hWndChild, lParam):
            if IsWindowVisible(hWndChild):
                data[0] = True
                return False
            return True
    EnumChildWindows(hWnd, ENUM_CHILD_PROC(EnumFunc), 0)
    return data[0]

def IsWin64():
    try:
        if _kernel32.GetSystemWow64DirectoryW(None, 0) == 0:
            return False
    except:
        return False
    return True

def KillProcess(pid = None, processName = None, hwnd = None, signal = 0, restart = False):
    if pid:
        pass
    elif processName:
        pids = GetPids(processName = processName)
        if pids:
            pid = pids[0]
        else:
            return False
    elif hwnd:
        hwnd = GetBestHwnd(hwnd)
        pids = GetPids(hwnd = hwnd)
        if pids:
            pid = pids[0]
        else:
            return False
    else:
        return False

    fullPath = GetProcessNameEx(pid = pid, fullPath = True)

    try:
        proc = OpenProcess(1, 0, pid)
        TerminateProcess(proc, signal)
        if restart:
            eg.plugins.System.Execute(fullPath)
        return True
    except:
        return False

def PluginIsEnabled(plugin):
    return PluginIsLoaded(plugin) and eg.plugins.__dict__[plugin].plugin.info.isStarted

def PluginIsLoaded(plugin):
    return hasattr(eg.plugins, plugin)

def ProcessExists(pid):
    try:
        return bool(GetObject("winmgmts:").ExecQuery("SELECT * FROM Win32_Process WHERE ProcessId = " + str(int(pid))).count)
    except:
        return False

def PyEnumProcesses():
    size = 1024
    pBytesReturned = DWORD()
    while True:
        data = (DWORD * size)()
        dataSize = size * sizeof(DWORD)
        res = EnumProcesses(data, dataSize, byref(pBytesReturned))
        if res == 0:
            raise WinError()
        if pBytesReturned.value != dataSize:
            break
        size *= 10
    return data[:pBytesReturned.value / sizeof(DWORD)]

def PyFindWindow(className=None, windowName=None):
    hWnd = FindWindow(className, windowName)
    if not hWnd:
        raise WinError()
    return hWnd

def PyGetCursorPos():
    """
    Returns the position of the cursor, in screen co-ordinates.

    int x, int y = GetCursorPos()
    """
    point = POINT()
    GetCursorPos(point)
    return point.x, point.y

def PyGetWindowThreadProcessId(hWnd):
    """
    Retrieves the identifier of the thread and process that created the
    specified window.

    int threadId, int processId = GetWindowThreadProcessId(hWnd)
    """
    dwProcessId = DWORD()
    threadId = GetWindowThreadProcessId(hWnd, byref(dwProcessId))
    return threadId, dwProcessId.value

def PySendMessageTimeout(
    hWnd,
    msg,
    wParam=0,
    lParam=0,
    flags=SMTO_BLOCK | SMTO_ABORTIFHUNG,
    timeout=2000
):
    resultData = DWORD()
    res = SendMessageTimeout(
        hWnd, msg, wParam, lParam, flags, timeout, byref(resultData)
    )
    if not res:
        raise WinError()
    return resultData.value

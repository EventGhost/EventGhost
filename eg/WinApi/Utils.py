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

import wx
import sys
from eg.cFunctions import GetProcessName, GetWindowChildsList
from Dynamic import (
    # ctypes stuff
    byref, sizeof, WinError, 
    # functions
    AttachThreadInput, PtVisible, SaveDC, RestoreDC, SetROP2,
    GetAncestor, Rectangle, IsWindow, IsIconic, GetStockObject, SelectObject,
    ShowWindow, BringWindowToTop, UpdateWindow, GetForegroundWindow, 
    InvalidateRect, GetCurrentThreadId, GetWindowThreadProcessId,
    SendNotifyMessage, GetWindowRect, GetCursorPos, EnumProcesses, 
    CloseHandle, EnumDisplayMonitors, GetCurrentProcessId, FindWindow,
    IsWindowVisible, GetParent, GetWindowDC, GetClassLong, EnumChildWindows,
    ReleaseDC, GetDC, DeleteObject, CreatePen, GetSystemMetrics, 
    SendMessageTimeout, ScreenToClient, WindowFromPoint, SendMessageTimeout,
    # types
    DWORD, RECT, POINT, MONITORENUMPROC, RGB, WINFUNCTYPE,
    BOOL, HWND, LPARAM,
    # constants
    WM_GETICON, ICON_SMALL, ICON_BIG, SMTO_ABORTIFHUNG, GCL_HICONSM, GCL_HICON,
    R2_NOT, PS_INSIDEFRAME, SM_CXBORDER, NULL_BRUSH, GA_ROOT, SW_RESTORE,
    WM_SYSCOMMAND, SC_CLOSE, SW_SHOWNA, SMTO_BLOCK, SMTO_ABORTIFHUNG,
)

EnumChildProc = WINFUNCTYPE(BOOL, HWND, LPARAM)
EnumChildWindows.argtypes = [HWND, EnumChildProc, LPARAM]

_H_BORDERWIDTH = 3 * GetSystemMetrics(SM_CXBORDER)
_H_BORDERCOLOUR = RGB(255, 0, 0)


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
    

def GetMonitorDimensions():
    retval = []
    def MonitorEnumProc(hMonitor, hdcMonitor, lprcMonitor, dwData):
        r = lprcMonitor.contents
        rect = wx.Rect(r.left, r.top, r.right - r.left, r.bottom - r.top)
        retval.append(rect)
        return 1
    EnumDisplayMonitors(0, None, MONITORENUMPROC(MonitorEnumProc), 0)
    return retval



def HighlightWindow(hWnd):
    """ 
    Draws an inverted rectange around a window to inform the user about
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
            x >= rect.left 
            and x <= rect.right 
            and y >= rect.top 
            and y <= rect.bottom
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
    EnumChildWindows(hWnd, EnumChildProc(EnumFunc), 0)
    return data[0]



def GetHwndChildren(hWnd, invisible):
    """ 
    Return a list of all direct children of the window 'hwnd'.
    """
    return [
        childHwnd for childHwnd in GetWindowChildsList(hWnd, invisible)
        if GetParent(childHwnd) == hWnd
    ]
    
    

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

# now implemented as C function in cFunctions.pyd
  
    
def GetWindowProcessName(hWnd):
    dwProcessId = DWORD()
    GetWindowThreadProcessId(hWnd, byref(dwProcessId))
    return GetProcessName(dwProcessId.value)
    
    
def PyGetWindowThreadProcessId(hWnd):
    """
    Retrieves the identifier of the thread and process that created the 
    specified window.

    int threadId, int processId = GetWindowThreadProcessId(hWnd)
    """
    dwProcessId = DWORD()
    threadId = GetWindowThreadProcessId(hWnd, byref(dwProcessId))
    return threadId, dwProcessId.value


def PyGetCursorPos():
    """
    Returns the position of the cursor, in screen co-ordinates.
    
    int x, int y = GetCursorPos()
    """
    point = POINT()
    GetCursorPos(point)
    return point.x, point.y


def PyEnumProcesses():
    size = 1024
    pBytesReturned = DWORD()
    while True:
        buffer = (DWORD * size)()
        cb = size * sizeof(DWORD)
        res = EnumProcesses(buffer, cb, byref(pBytesReturned))
        if res == 0:
            raise WinError()
        if pBytesReturned.value != cb:
            break
        size *= 10
    return buffer[:pBytesReturned.value / sizeof(DWORD)]
        

def PySendMessageTimeout(
    hWnd, 
    msg, 
    wParam=0, 
    lParam=0, 
    flags=SMTO_BLOCK|SMTO_ABORTIFHUNG, 
    timeout=2000
):
    resultData = DWORD()
    res = SendMessageTimeout(
        hWnd, msg, wParam, lParam, flags, timeout, byref(resultData)
    )
    if not res:
        raise WinError()
    return resultData.value


def PyFindWindow(className=None, windowName=None):
    hWnd = FindWindow(className, windowName)
    if not hWnd:
        raise WinError()
    return hWnd

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

import sys
import win32con
import win32gui
import win32api
from win32ui import CreateWindowFromHandle
from win32api import GetCurrentThreadId
from win32gui import GetForegroundWindow, WindowFromPoint, IsWindow
from win32process import GetWindowThreadProcessId
from win32process import GetCurrentProcess


from eg.WinAPI.win32types import *

def GetTopLevelWindowOf(hwnd):
    return GetAncestor(hwnd, GA_ROOT)


def BringHwndToFront(hwnd):
    if hwnd is None:
        return
    hwnd = GetAncestor(hwnd, GA_ROOT)
    if not IsWindow(hwnd):
        return
    win = CreateWindowFromHandle(hwnd)
    
    # If the window is in a minimized state, maximize now
    style = win.GetStyle()
    if style & win32con.WS_MINIMIZE:
        win.ShowWindow(win32con.SW_RESTORE)
        win.BringWindowToTop()
        win.UpdateWindow()
    
    # Check to see if we are the foreground thread
    try:
        h = GetForegroundWindow()
        foregroundThreadID, processID = GetWindowThreadProcessId(h)
    except:
        foregroundThreadID = None
    ourThreadID = GetCurrentThreadId()

    # If not, attach our thread's 'input' to the foreground thread's
    if foregroundThreadID != ourThreadID:
        AttachThreadInput(foregroundThreadID, ourThreadID, True)

    win.ShowWindow(style)
    win.BringWindowToTop()
    # Force our window to redraw
    win.InvalidateRect()
    if foregroundThreadID != ourThreadID:
        AttachThreadInput(foregroundThreadID, ourThreadID, False)
        
        
class MyRectangle:
    def __str__(self):
        return "(%d, %d, %d, %d)" % (self.x, self.y, self.width, self.height)



def GetMonitorDimensions():
    retval = []
    def cb(hMonitor, hdcMonitor, lprcMonitor, dwData):
        r = lprcMonitor.contents
        rect = MyRectangle()
        rect.x = r.left
        rect.y = r.top
        rect.width = r.right - r.left
        rect.height = r.bottom - r.top
        retval.append(rect)
        return 1
    temp = EnumDisplayMonitors(0, 0, cb, 0)
    return retval



from win32con import (
    WM_GETICON, 
    ICON_SMALL, 
    ICON_BIG, 
    SMTO_ABORTIFHUNG,
    GCL_HICONSM, 
    GCL_HICON
)
from win32gui import (
    SendMessageTimeout,
    GetClassLong,
    IsWindowVisible, 
    EnumChildWindows, 
    EnumChildWindows, 
    GetParent
)

from wx import NullIcon


def _GetAllWindowChildren_EnumProc(hwnd, data):
    data.append(hwnd)
    return True


def GetAllWindowChildren(hwnd):
    """ Return a list of all children of the window 'hwnd' including subchilds
    """
    data = []
    try:
        EnumChildWindows(hwnd, _GetAllWindowChildren_EnumProc, data)
    except win32gui.error, exception:
        data = []
    return data

from win32gui import (UpdateWindow, GetWindowRect, GetWindowDC, SelectObject,
    ReleaseDC, GetDC, DeleteObject, GetStockObject, ScreenToClient)
from win32api import GetSystemMetrics
from win32con import R2_NOT, PS_INSIDEFRAME, SM_CXBORDER, NULL_BRUSH

_H_BORDERWIDTH = 3 * win32api.GetSystemMetrics(SM_CXBORDER)
_H_BORDERCOLOUR = win32api.RGB(255, 0, 0)
Rectangle = gdi32.Rectangle


def HighlightWindow(hwnd):
    """ 
    Draws an inverted rectange around a window to inform the user about
    the currently selected window.
    """
    
    UpdateWindow(hwnd)
    # Retrieve location of window on-screen.
    left, top, right, bottom = GetWindowRect(hwnd)

    # Get a device context that allows us to write anywhere within the window.
    hdc = GetWindowDC(hwnd)

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
    Rectangle(hdc, 0, 0, right - left, bottom - top)

    # Restore the original attributes and release the device context.
    RestoreDC(hdc, -1)
    ReleaseDC(hwnd, hdc)

    # We can destroy the pen only AFTER we have restored the DC because the DC
    # must have valid objects selected into it at all times.
    DeleteObject(hpen)


def BestWindowFromPoint(point):
    x, y = point
    found_window = WindowFromPoint(point)
    
    hwnds = GetAllWindowChildren(GetAncestor(found_window, GA_ROOT))
    if not hwnds:
        return found_window
    found_window_area = sys.maxint
    for hwnd in hwnds:
        left, top, right, bottom = GetWindowRect(hwnd)
        if x >= left and x <= right and y >= top and y <= bottom:
            hdc = GetDC(hwnd)
            x2, y2 = ScreenToClient(hwnd, point)
            if PtVisible(hdc, x2, y2):
                area = (right - left) * (bottom - top)
                if area < found_window_area:
                    found_window = hwnd
                    found_window_area = area
            ReleaseDC(hwnd, hdc)
    return found_window



def GetHwndIcon(hwnd):
    """ 
    Get a wx.Icon from a window through its hwnd window handle 
    """
    try:
        res, hicon = SendMessageTimeout(
            hwnd, WM_GETICON, ICON_SMALL, 0, SMTO_ABORTIFHUNG, 1000
        )
    except:
        hicon = 0
    if hicon < 10:
        hicon = GetClassLong(hwnd, GCL_HICONSM)
        if hicon == 0:
            try:
                res, hicon = SendMessageTimeout(
                    hwnd, WM_GETICON, ICON_BIG, 0, SMTO_ABORTIFHUNG, 1000
                )
            except:
                hicon = 0
            if hicon < 10:
                hicon = GetClassLong(hwnd, GCL_HICON)
    if hicon != 0:
        icon = NullIcon
        icon.SetHandle(hicon)
        icon.SetSize((16,16))
        return icon
    else:
        return None



def _HwndHasChildren_EnumProc1(hwnd, data):
    data[0] = True
    return False


def _HwndHasChildren_EnumProc2(hwnd, data):
    if IsWindowVisible(hwnd):
        data[0] = True
        return False
    else:
        return True


def HwndHasChildren(hwnd, invisible):
    """ 
    Return True if the window 'hwnd' has children.
    If 'invisible' is False, don't take invisible windows into account.
    """
    data = [False]
    try:
        if invisible:
            EnumChildWindows(hwnd, _HwndHasChildren_EnumProc1, data)
        else:
            EnumChildWindows(hwnd, _HwndHasChildren_EnumProc2, data)
    except win32gui.error, exception:
        pass
    return data[0]


def _GetHwndChildren_EnumProc1(hwnd, data):
    if GetParent(hwnd) == data[0]:
        data[1].append(hwnd)
    return True

def _GetHwndChildren_EnumProc2(hwnd, data):
    if not IsWindowVisible(hwnd):
        return True
    if GetParent(hwnd) == data[0]:
        data[1].append(hwnd)
    return True


def GetHwndChildren(hwnd, invisible):
    """ 
    Return a list of all direct children of the window 'hwnd'.
    """

    data = [hwnd, []]
    try:
        if invisible:
            EnumChildWindows(hwnd, _GetHwndChildren_EnumProc1, data)
        else:
            EnumChildWindows(hwnd, _GetHwndChildren_EnumProc2, data)
    except win32gui.error, exception:
        data[1] = []
    return data[1]

    
from win32api import OpenProcess, CloseHandle
from win32process import GetModuleFileNameEx, EnumProcesses

_GetNameOfPID_FLAGS = (
    win32con.PROCESS_QUERY_INFORMATION|win32con.PROCESS_VM_READ
)

def GetNameOfPID(pid):
    try:
        handle = OpenProcess(_GetNameOfPID_FLAGS, False, pid)
    except:
        return ""
    try:
        exe = GetModuleFileNameEx(handle, 0)
    except:
        exe = ""
    CloseHandle(handle)
    return exe
    
    
from os.path import basename

def GetModulesPID(exeName):
    result = []
    processes = EnumProcesses()
    for pid in processes:
        try:
            # 1040 = PROCESS_QUERY_INFORMATION|PROCESS_VM_READ
            handle = OpenProcess(1040, False, pid)
        except:
            continue
        try:
            exe = GetModuleFileNameEx(handle, 0)
        except:
            exe = ""
        CloseHandle(handle)
        if exeName == basename(exe):
            result.append(pid)
    return result



def GetHwndProcessName(hwnd):
    pid = GetWindowThreadProcessId(hwnd)[1]
    try:
        handle = OpenProcess(_GetNameOfPID_FLAGS, False, pid)
    except:
        return ""
    try:
        exe = GetModuleFileNameEx(handle, 0)
    except:
        exe = ""
    CloseHandle(handle)
    return basename(exe)
    

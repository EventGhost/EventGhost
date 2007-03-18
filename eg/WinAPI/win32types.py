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

from ctypes import *
from ctypes.wintypes import *
from GUID import GUID
import win32api

GWL_STYLE = -16
WS_MINIMIZE = 0x20000000
SW_MAXIMIZE = 3
SW_SHOW = 5
SW_SHOWNA = 8
SW_RESTORE = 9
HWND_TOPMOST = -1
SWP_NOMOVE = 2
SWP_NOSIZE = 1

GA_PARENT = 1
GA_ROOT = 2
GA_ROOTOWNER = 3

BOOL = c_int
UINT = c_uint
USHORT = c_ushort
##if defined(_WIN64)
# typedef unsigned __int64 ULONG_PTR;
##else
# typedef unsigned long ULONG_PTR;
##endif
ULONG_PTR = POINTER(c_ulong)

#typedef ULONG_PTR DWORD_PTR;
DWORD_PTR = ULONG_PTR

#typedef DWORD_PTR *PDWORD_PTR;
PDWORD_PTR = POINTER(DWORD_PTR)


class RECT(Structure):
    _fields_ = [
        ('left', c_long),
        ('top', c_long),
        ('right', c_long),
        ('bottom', c_long)
    ]



class MONITORINFO(Structure):
    _fields_ = [
        ('cbSize', c_ulong),
        ('rcMonitor', RECT),
        ('rcWork', RECT),
        ('dwFlags', c_ulong)
    ]
    
    
    
class DEV_BROADCAST_HDR(Structure):
    _fields_ = [
        ("dbch_size",       DWORD),
        ("dbch_devicetype", DWORD),
        ("dbch_reserved",   DWORD)
    ]



class DEV_BROADCAST_VOLUME(Structure):
    _fields_ = [
        ("dbcv_size",       DWORD),
        ("dbcv_devicetype", DWORD),
        ("dbcv_reserved",   DWORD),
        ("dbcv_unitmask",   DWORD),
        ("dbcv_flags",      WORD)
    ]



class DEV_BROADCAST_DEVICEINTERFACE(Structure):
    _fields_ = [
        ("dbcc_size",       DWORD),
        ("dbcc_devicetype", DWORD),
        ("dbcc_reserved",   DWORD),
        ("dbcc_classguid",  GUID),
        ("dbcc_name",       c_char * 128)
    ]

    def __init__(self, dbcc_devicetype=0, dbcc_classguid=None, dbcc_name=""):
        self.dbcc_devicetype = dbcc_devicetype
        self.dbcc_classguid = GUID(dbcc_classguid)
        self.dbcc_name = dbcc_name
        self.dbcc_size = sizeof(DEV_BROADCAST_DEVICEINTERFACE) + len(dbcc_name) + 1
        
# Device change events (WM_DEVICECHANGE wParam)

DBT_DEVICEARRIVAL = 0x8000
DBT_DEVICEQUERYREMOVE = 0x8001
DBT_DEVICEQUERYREMOVEFAILED = 0x8002
DBT_DEVICEMOVEPENDING = 0x8003
DBT_DEVICEREMOVECOMPLETE = 0x8004
DBT_DEVICETYPESSPECIFIC = 0x8005
DBT_CONFIGCHANGED = 0x0018


# type of device in DEV_BROADCAST_HDR

DBT_DEVTYP_OEM = 0x00000000
DBT_DEVTYP_DEVNODE = 0x00000001
DBT_DEVTYP_VOLUME = 0x00000002
DBT_DEVTYP_PORT = 0x00000003
DBT_DEVTYP_NET = 0x00000004
DBT_DEVTYP_DEVICEINTERFACE = 0x00000005

# media types in DBT_DEVTYP_VOLUME

DBTF_MEDIA = 0x0001
DBTF_NET = 0x0002



gdi32 = windll.Gdi32
user32 = windll.user32
kernel32 = windll.Kernel32

SaveDC = gdi32.SaveDC
SetROP2 = gdi32.SetROP2
CreatePen = gdi32.CreatePen
Rectangle = gdi32.Rectangle
RestoreDC = gdi32.RestoreDC
PtVisible = gdi32.PtVisible
GetViewportOrgEx = gdi32.GetViewportOrgEx

SendMessage = user32.SendMessageA
SendMessageTimeout = user32.SendMessageTimeoutA
SendNotifyMessage = user32.SendNotifyMessageA

PostMessage = user32.PostMessageA
GetMessage = user32.GetMessageA
AttachThreadInput = user32.AttachThreadInput

GetAncestor = user32.GetAncestor
GetParent = user32.GetParent
EnumChildWindows = user32.EnumChildWindows
InvalidateRect = user32.InvalidateRect
MapVirtualKey = user32.MapVirtualKeyA
VkKeyScan = user32.VkKeyScanW
GetKeyboardState = user32.GetKeyboardState
SetKeyboardState = user32.SetKeyboardState
SetWindowsHookEx = user32.SetWindowsHookExA
SetTimer = user32.SetTimer
RegisterDeviceNotification = user32.RegisterDeviceNotificationA
UnregisterDeviceNotification = user32.UnregisterDeviceNotification

MonitorEnumProc = WINFUNCTYPE(BOOL, c_ulong, c_ulong, POINTER(RECT), c_double)

def EnumDisplayMonitors(hdc, lprcClip, lpfnEnum, dwData):
    user32.EnumDisplayMonitors(
        hdc, 
        lprcClip, 
        MonitorEnumProc(lpfnEnum), 
        dwData
    )
    
SetThreadExecutionState = kernel32.SetThreadExecutionState

#typedef struct tagGUITHREADINFO {
#    DWORD cbSize;
#    DWORD flags;
#    HWND hwndActive;
#    HWND hwndFocus;
#    HWND hwndCapture;
#    HWND hwndMenuOwner;
#    HWND hwndMoveSize;
#    HWND hwndCaret;
#    RECT rcCaret;
#} GUITHREADINFO, *PGUITHREADINFO;

class GUITHREADINFO(Structure):
    _fields_ = [
        ("cbSize", DWORD),
        ("flags", DWORD),
        ("hwndActive", HWND),
        ("hwndFocus", HWND),
        ("hwndCapture", HWND),
        ("hwndMenuOwner", HWND),
        ("hwndMoveSize", HWND),
        ("hwndCaret", HWND),
        ("rcCaret", RECT),
    ]
       
    def __init__(self):
        self.cbSize = sizeof(GUITHREADINFO)
        
PGUITHREADINFO = POINTER(GUITHREADINFO)

GetGUIThreadInfo = user32.GetGUIThreadInfo

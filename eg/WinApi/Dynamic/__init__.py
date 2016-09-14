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

#pylint: disable-msg=C0103,C0301,C0302

# This file gets automatically extended by ctypeslib.dynamic_module, so don't
# edit it yourself.

from ctypes import *  #pylint: disable-msg=W0401,W0614
from ctypes.wintypes import *  #pylint: disable-msg=W0401,W0614
import sys

_user32 = WinDLL("user32")
_kernel32 = WinDLL("kernel32")
_ole32 = WinDLL("ole32")
_gdi32 = WinDLL("Gdi32")
#_winmm = WinDLL("Winmm")
_shell32 = WinDLL("shell32")
#_Psapi = WinDLL("Psapi")
_Advapi32 = WinDLL("Advapi32")
#_setupapi = WinDLL("setupapi")
_htmlhelp = WinDLL("hhctrl.ocx")
#_difxapi = WinDLL("DIFxAPI.dll")
if __name__ == "__main__":
    try:
        ctypeslib = __import__("ctypeslib.dynamic_module")
    except ImportError:
        print "ctypeslib is not installed!"
    else:
        try:
            ctypeslib.dynamic_module.include(
                "#define UNICODE\n"
                "#define _WIN32_WINNT 0x501\n"
                "#define WIN32_LEAN_AND_MEAN\n"
                "#define NO_STRICT\n"
                "#include <windows.h>\n"
                "#include <winuser.h>\n"
                "#include <Dbt.h>\n"
                "#include <objbase.h>\n"
                #"#include <Mmsystem.h>\n"
                "#include <shlobj.h>\n"
                #"#include <Psapi.h>\n"
                "#include <tlhelp32.h>\n"
                "#include <objidl.h>\n"
                #"#include <setupapi.h>\n"
                "#include <htmlhelp.h>\n"
                "#include <shellapi.h>\n"
                #"#include <difxapi.h>\n"
                "#include <AccCtrl.h>\n"
                "#include <Aclapi.h>\n"
            )
        except WindowsError:
            print "GCC_XML most likely not installed"
INVALID_HANDLE_VALUE = -1
HWND_TOPMOST = -1
HWND_NOTOPMOST = -2

PHANDLE = POINTER(HANDLE)
OpenThreadToken = _Advapi32.OpenThreadToken
OpenThreadToken.restype = BOOL
OpenThreadToken.argtypes = [HANDLE, DWORD, BOOL, PHANDLE]
OpenProcessToken = _Advapi32.OpenProcessToken
OpenProcessToken.restype = BOOL
OpenProcessToken.argtypes = [HANDLE, DWORD, PHANDLE]

#-----------------------------------------------------------------------------#
# everything after the following line is automatically created
#-----------------------------------------------------------------------------#
AttachThreadInput = _user32.AttachThreadInput
AttachThreadInput.restype = BOOL
AttachThreadInput.argtypes = [DWORD, DWORD, BOOL]
PtVisible = _gdi32.PtVisible
PtVisible.restype = BOOL
PtVisible.argtypes = [HDC, c_int, c_int]
SaveDC = _gdi32.SaveDC
SaveDC.restype = c_int
SaveDC.argtypes = [HDC]
RestoreDC = _gdi32.RestoreDC
RestoreDC.restype = BOOL
RestoreDC.argtypes = [HDC, c_int]
SetROP2 = _gdi32.SetROP2
SetROP2.restype = c_int
SetROP2.argtypes = [HDC, c_int]
GetAncestor = _user32.GetAncestor
GetAncestor.restype = HWND
GetAncestor.argtypes = [HWND, UINT]
Rectangle = _gdi32.Rectangle
Rectangle.restype = BOOL
Rectangle.argtypes = [HDC, c_int, c_int, c_int, c_int]
IsWindow = _user32.IsWindow
IsWindow.restype = BOOL
IsWindow.argtypes = [HWND]
IsIconic = _user32.IsIconic
IsIconic.restype = BOOL
IsIconic.argtypes = [HWND]
GetStockObject = _gdi32.GetStockObject
GetStockObject.restype = HGDIOBJ
GetStockObject.argtypes = [c_int]
SelectObject = _gdi32.SelectObject
SelectObject.restype = HGDIOBJ
SelectObject.argtypes = [HDC, HGDIOBJ]
ShowWindow = _user32.ShowWindow
ShowWindow.restype = BOOL
ShowWindow.argtypes = [HWND, c_int]
BringWindowToTop = _user32.BringWindowToTop
BringWindowToTop.restype = BOOL
BringWindowToTop.argtypes = [HWND]
UpdateWindow = _user32.UpdateWindow
UpdateWindow.restype = BOOL
UpdateWindow.argtypes = [HWND]
GetForegroundWindow = _user32.GetForegroundWindow
GetForegroundWindow.restype = HWND
GetForegroundWindow.argtypes = []
InvalidateRect = _user32.InvalidateRect
InvalidateRect.restype = BOOL
InvalidateRect.argtypes = [HWND, POINTER(RECT), BOOL]
GetCurrentThreadId = _kernel32.GetCurrentThreadId
GetCurrentThreadId.restype = DWORD
GetCurrentThreadId.argtypes = []
LPDWORD = POINTER(DWORD)
GetWindowThreadProcessId = _user32.GetWindowThreadProcessId
GetWindowThreadProcessId.restype = DWORD
GetWindowThreadProcessId.argtypes = [HWND, LPDWORD]
SendNotifyMessageW = _user32.SendNotifyMessageW
SendNotifyMessageW.restype = BOOL
SendNotifyMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendNotifyMessage = SendNotifyMessageW  # alias
LPRECT = POINTER(tagRECT)
GetWindowRect = _user32.GetWindowRect
GetWindowRect.restype = BOOL
GetWindowRect.argtypes = [HWND, LPRECT]
LPPOINT = POINTER(tagPOINT)
GetCursorPos = _user32.GetCursorPos
GetCursorPos.restype = BOOL
GetCursorPos.argtypes = [LPPOINT]
LPCRECT = POINTER(RECT)
MONITORENUMPROC = WINFUNCTYPE(BOOL, HMONITOR, HDC, LPRECT, LPARAM)
EnumDisplayMonitors = _user32.EnumDisplayMonitors
EnumDisplayMonitors.restype = BOOL
EnumDisplayMonitors.argtypes = [HDC, LPCRECT, MONITORENUMPROC, LPARAM]
FindWindowW = _user32.FindWindowW
FindWindowW.restype = HWND
FindWindowW.argtypes = [LPCWSTR, LPCWSTR]
FindWindow = FindWindowW  # alias
IsWindowVisible = _user32.IsWindowVisible
IsWindowVisible.restype = BOOL
IsWindowVisible.argtypes = [HWND]
GetParent = _user32.GetParent
GetParent.restype = HWND
GetParent.argtypes = [HWND]
GetWindowDC = _user32.GetWindowDC
GetWindowDC.restype = HDC
GetWindowDC.argtypes = [HWND]
GetClassLongW = _user32.GetClassLongW
GetClassLongW.restype = DWORD
GetClassLongW.argtypes = [HWND, c_int]
GetClassLong = GetClassLongW  # alias
FARPROC = WINFUNCTYPE(c_int)
WNDENUMPROC = FARPROC
EnumChildWindows = _user32.EnumChildWindows
EnumChildWindows.restype = BOOL
EnumChildWindows.argtypes = [HWND, WNDENUMPROC, LPARAM]
ReleaseDC = _user32.ReleaseDC
ReleaseDC.restype = c_int
ReleaseDC.argtypes = [HWND, HDC]
GetDC = _user32.GetDC
GetDC.restype = HDC
GetDC.argtypes = [HWND]
DeleteObject = _gdi32.DeleteObject
DeleteObject.restype = BOOL
DeleteObject.argtypes = [HGDIOBJ]
CreatePen = _gdi32.CreatePen
CreatePen.restype = HPEN
CreatePen.argtypes = [c_int, c_int, COLORREF]
GetSystemMetrics = _user32.GetSystemMetrics
GetSystemMetrics.restype = c_int
GetSystemMetrics.argtypes = [c_int]
LONG_PTR = c_long
LRESULT = LONG_PTR
ULONG_PTR = c_ulong
PDWORD_PTR = POINTER(ULONG_PTR)
SendMessageTimeoutW = _user32.SendMessageTimeoutW
SendMessageTimeoutW.restype = LRESULT
SendMessageTimeoutW.argtypes = [HWND, UINT, WPARAM, LPARAM, UINT, UINT, PDWORD_PTR]
SendMessageTimeout = SendMessageTimeoutW  # alias
ScreenToClient = _user32.ScreenToClient
ScreenToClient.restype = BOOL
ScreenToClient.argtypes = [HWND, LPPOINT]
WindowFromPoint = _user32.WindowFromPoint
WindowFromPoint.restype = HWND
WindowFromPoint.argtypes = [POINT]
WM_GETICON = 127  # Variable c_int '127'
ICON_SMALL = 0  # Variable c_int '0'
ICON_BIG = 1  # Variable c_int '1'
SMTO_ABORTIFHUNG = 2  # Variable c_int '2'
GCL_HICONSM = -34  # Variable c_int '-0x000000022'
GCL_HICON = -14  # Variable c_int '-0x00000000e'
R2_NOT = 6  # Variable c_int '6'
PS_INSIDEFRAME = 6  # Variable c_int '6'
SM_CXBORDER = 5  # Variable c_int '5'
NULL_BRUSH = 5  # Variable c_int '5'
GA_ROOT = 2  # Variable c_int '2'
SW_RESTORE = 9  # Variable c_int '9'
WM_SYSCOMMAND = 274  # Variable c_int '274'
SC_CLOSE = 61536  # Variable c_int '61536'
SW_SHOWNA = 8  # Variable c_int '8'
SMTO_BLOCK = 1  # Variable c_int '1'
WM_COMMAND = 273  # Variable c_int '273'
WM_USER = 1024  # Variable c_int '1024'
OpenClipboard = _user32.OpenClipboard
OpenClipboard.restype = BOOL
OpenClipboard.argtypes = [HWND]
EmptyClipboard = _user32.EmptyClipboard
EmptyClipboard.restype = BOOL
EmptyClipboard.argtypes = []
CloseClipboard = _user32.CloseClipboard
CloseClipboard.restype = BOOL
CloseClipboard.argtypes = []
GetClipboardData = _user32.GetClipboardData
GetClipboardData.restype = HANDLE
GetClipboardData.argtypes = [UINT]
SetClipboardData = _user32.SetClipboardData
SetClipboardData.restype = HANDLE
SetClipboardData.argtypes = [UINT, HANDLE]
GlobalLock = _kernel32.GlobalLock
GlobalLock.restype = LPVOID
GlobalLock.argtypes = [HGLOBAL]
GlobalUnlock = _kernel32.GlobalUnlock
GlobalUnlock.restype = BOOL
GlobalUnlock.argtypes = [HGLOBAL]
SIZE_T = ULONG_PTR
GlobalAlloc = _kernel32.GlobalAlloc
GlobalAlloc.restype = HGLOBAL
GlobalAlloc.argtypes = [UINT, SIZE_T]
CF_TEXT = 1  # Variable c_int '1'
CF_UNICODETEXT = 13  # Variable c_int '13'
GHND = 66  # Variable c_int '66'
GetCurrentProcessId = _kernel32.GetCurrentProcessId
GetCurrentProcessId.restype = DWORD
GetCurrentProcessId.argtypes = []
WM_SIZE = 5  # Variable c_int '5'
CW_USEDEFAULT = -2147483648  # Variable c_int '-0x080000000'
WS_OVERLAPPEDWINDOW = 13565952  # Variable c_long '13565952l'
GetModuleHandleW = _kernel32.GetModuleHandleW
GetModuleHandleW.restype = HMODULE
GetModuleHandleW.argtypes = [LPCWSTR]
GetModuleHandle = GetModuleHandleW  # alias
class tagWNDCLASSW(Structure):
    pass
WNDCLASSW = tagWNDCLASSW
WNDCLASS = WNDCLASSW
WNDPROC = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)
HCURSOR = HICON
tagWNDCLASSW._fields_ = [
    ('style', UINT),
    ('lpfnWndProc', WNDPROC),
    ('cbClsExtra', c_int),
    ('cbWndExtra', c_int),
    ('hInstance', HINSTANCE),
    ('hIcon', HICON),
    ('hCursor', HCURSOR),
    ('hbrBackground', HBRUSH),
    ('lpszMenuName', LPCWSTR),
    ('lpszClassName', LPCWSTR),
]
RegisterClassW = _user32.RegisterClassW
RegisterClassW.restype = ATOM
RegisterClassW.argtypes = [POINTER(WNDCLASSW)]
RegisterClass = RegisterClassW  # alias
CreateWindowExW = _user32.CreateWindowExW
CreateWindowExW.restype = HWND
CreateWindowExW.argtypes = [DWORD, LPCWSTR, LPCWSTR, DWORD, c_int, c_int, c_int, c_int, HWND, HMENU, HINSTANCE, LPVOID]
CreateWindowEx = CreateWindowExW  # alias
DefWindowProcW = _user32.DefWindowProcW
DefWindowProcW.restype = LRESULT
DefWindowProcW.argtypes = [HWND, UINT, WPARAM, LPARAM]
DefWindowProc = DefWindowProcW  # alias
SetClipboardViewer = _user32.SetClipboardViewer
SetClipboardViewer.restype = HWND
SetClipboardViewer.argtypes = [HWND]
ChangeClipboardChain = _user32.ChangeClipboardChain
ChangeClipboardChain.restype = BOOL
ChangeClipboardChain.argtypes = [HWND, HWND]
WM_CHANGECBCHAIN = 781  # Variable c_int '781'
WM_DRAWCLIPBOARD = 776  # Variable c_int '776'
SendMessageW = _user32.SendMessageW
SendMessageW.restype = LRESULT
SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendMessage = SendMessageW  # alias
class _SECURITY_ATTRIBUTES(Structure):
    pass
LPSECURITY_ATTRIBUTES = POINTER(_SECURITY_ATTRIBUTES)
CreateEventW = _kernel32.CreateEventW
CreateEventW.restype = HANDLE
CreateEventW.argtypes = [LPSECURITY_ATTRIBUTES, BOOL, BOOL, LPCWSTR]
CreateEvent = CreateEventW  # alias
_SECURITY_ATTRIBUTES._fields_ = [
    ('nLength', DWORD),
    ('lpSecurityDescriptor', LPVOID),
    ('bInheritHandle', BOOL),
]
SetEvent = _kernel32.SetEvent
SetEvent.restype = BOOL
SetEvent.argtypes = [HANDLE]
WAIT_OBJECT_0 = 0L  # Variable c_ulong '0ul'
WAIT_TIMEOUT = 258  # Variable c_long '258l'
QS_ALLINPUT = 1279  # Variable c_int '1279'
MsgWaitForMultipleObjects = _user32.MsgWaitForMultipleObjects
MsgWaitForMultipleObjects.restype = DWORD
MsgWaitForMultipleObjects.argtypes = [DWORD, POINTER(HANDLE), BOOL, DWORD, DWORD]
CoInitializeEx = _ole32.CoInitializeEx
CoInitializeEx.restype = HRESULT
CoInitializeEx.argtypes = [LPVOID, DWORD]
CoUninitialize = _ole32.CoUninitialize
CoUninitialize.restype = None
CoUninitialize.argtypes = []
LPMSG = POINTER(tagMSG)
PeekMessageW = _user32.PeekMessageW
PeekMessageW.restype = BOOL
PeekMessageW.argtypes = [LPMSG, HWND, UINT, UINT, UINT]
PeekMessage = PeekMessageW  # alias
DispatchMessageW = _user32.DispatchMessageW
DispatchMessageW.restype = LRESULT
DispatchMessageW.argtypes = [POINTER(MSG)]
DispatchMessage = DispatchMessageW  # alias
PM_REMOVE = 1  # Variable c_int '1'
WM_QUIT = 18  # Variable c_int '18'
SetProcessShutdownParameters = _kernel32.SetProcessShutdownParameters
SetProcessShutdownParameters.restype = BOOL
SetProcessShutdownParameters.argtypes = [DWORD, DWORD]
ExitProcess = _kernel32.ExitProcess
ExitProcess.restype = None
ExitProcess.argtypes = [UINT]
GetSysColor = _user32.GetSysColor
GetSysColor.restype = DWORD
GetSysColor.argtypes = [c_int]
COLOR_ACTIVECAPTION = 2  # Variable c_int '2'
COLOR_GRADIENTACTIVECAPTION = 27  # Variable c_int '27'
COLOR_CAPTIONTEXT = 9  # Variable c_int '9'
COLOR_INACTIVECAPTION = 3  # Variable c_int '3'
COLOR_GRADIENTINACTIVECAPTION = 28  # Variable c_int '28'
COLOR_INACTIVECAPTIONTEXT = 19  # Variable c_int '19'
OpenProcess = _kernel32.OpenProcess
OpenProcess.restype = HANDLE
OpenProcess.argtypes = [DWORD, BOOL, DWORD]
PROCESS_SET_QUOTA = 256  # Variable c_int '256'
SetProcessWorkingSetSize = _kernel32.SetProcessWorkingSetSize
SetProcessWorkingSetSize.restype = BOOL
SetProcessWorkingSetSize.argtypes = [HANDLE, SIZE_T, SIZE_T]
PostMessageW = _user32.PostMessageW
PostMessageW.restype = BOOL
PostMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
PostMessage = PostMessageW  # alias
class tagINPUT(Structure):
    pass
LPINPUT = POINTER(tagINPUT)
SendInput = _user32.SendInput
SendInput.restype = UINT
SendInput.argtypes = [UINT, LPINPUT, c_int]
class N8tagINPUT5DOLLAR_105E(Union):
    pass
class tagMOUSEINPUT(Structure):
    pass
tagMOUSEINPUT._fields_ = [
    ('dx', LONG),
    ('dy', LONG),
    ('mouseData', DWORD),
    ('dwFlags', DWORD),
    ('time', DWORD),
    ('dwExtraInfo', ULONG_PTR),
]
MOUSEINPUT = tagMOUSEINPUT
class tagKEYBDINPUT(Structure):
    pass
tagKEYBDINPUT._fields_ = [
    ('wVk', WORD),
    ('wScan', WORD),
    ('dwFlags', DWORD),
    ('time', DWORD),
    ('dwExtraInfo', ULONG_PTR),
]
KEYBDINPUT = tagKEYBDINPUT
class tagHARDWAREINPUT(Structure):
    pass
tagHARDWAREINPUT._fields_ = [
    ('uMsg', DWORD),
    ('wParamL', WORD),
    ('wParamH', WORD),
]
HARDWAREINPUT = tagHARDWAREINPUT
N8tagINPUT5DOLLAR_105E._fields_ = [
    ('mi', MOUSEINPUT),
    ('ki', KEYBDINPUT),
    ('hi', HARDWAREINPUT),
]
tagINPUT._anonymous_ = ['_0']
tagINPUT._fields_ = [
    ('type', DWORD),
    ('_0', N8tagINPUT5DOLLAR_105E),
]
CloseHandle = _kernel32.CloseHandle
CloseHandle.restype = BOOL
CloseHandle.argtypes = [HANDLE]
WaitForInputIdle = _user32.WaitForInputIdle
WaitForInputIdle.restype = DWORD
WaitForInputIdle.argtypes = [HANDLE, DWORD]
PBYTE = POINTER(BYTE)
GetKeyboardState = _user32.GetKeyboardState
GetKeyboardState.restype = BOOL
GetKeyboardState.argtypes = [PBYTE]
UINT_PTR = c_uint
TIMERPROC = FARPROC
SetTimer = _user32.SetTimer
SetTimer.restype = UINT_PTR
SetTimer.argtypes = [HWND, UINT_PTR, UINT, TIMERPROC]
LPBYTE = POINTER(BYTE)
SetKeyboardState = _user32.SetKeyboardState
SetKeyboardState.restype = BOOL
SetKeyboardState.argtypes = [LPBYTE]
INPUT = tagINPUT
INPUT_KEYBOARD = 1  # Variable c_int '1'
KEYEVENTF_KEYUP = 2  # Variable c_int '2'
class tagGUITHREADINFO(Structure):
    pass
PGUITHREADINFO = POINTER(tagGUITHREADINFO)
GetGUIThreadInfo = _user32.GetGUIThreadInfo
GetGUIThreadInfo.restype = BOOL
GetGUIThreadInfo.argtypes = [DWORD, PGUITHREADINFO]
tagGUITHREADINFO._fields_ = [
    ('cbSize', DWORD),
    ('flags', DWORD),
    ('hwndActive', HWND),
    ('hwndFocus', HWND),
    ('hwndCapture', HWND),
    ('hwndMenuOwner', HWND),
    ('hwndMoveSize', HWND),
    ('hwndCaret', HWND),
    ('rcCaret', RECT),
]
GUITHREADINFO = tagGUITHREADINFO
PROCESS_QUERY_INFORMATION = 1024  # Variable c_int '1024'
VK_SHIFT = 16  # Variable c_int '16'
VK_LSHIFT = 160  # Variable c_int '160'
VK_CONTROL = 17  # Variable c_int '17'
VK_LCONTROL = 162  # Variable c_int '162'
VK_MENU = 18  # Variable c_int '18'
WM_TIMER = 275  # Variable c_int '275'
WM_SYSKEYDOWN = 260  # Variable c_int '260'
WM_KEYDOWN = 256  # Variable c_int '256'
WM_SYSKEYUP = 261  # Variable c_int '261'
WM_KEYUP = 257  # Variable c_int '257'
VkKeyScanW = _user32.VkKeyScanW
VkKeyScanW.restype = SHORT
VkKeyScanW.argtypes = [WCHAR]
MapVirtualKeyW = _user32.MapVirtualKeyW
MapVirtualKeyW.restype = UINT
MapVirtualKeyW.argtypes = [UINT, UINT]
MapVirtualKey = MapVirtualKeyW  # alias
GetMessageW = _user32.GetMessageW
GetMessageW.restype = BOOL
GetMessageW.argtypes = [LPMSG, HWND, UINT, UINT]
GetMessage = GetMessageW  # alias
GetFocus = _user32.GetFocus
GetFocus.restype = HWND
GetFocus.argtypes = []
DWORD_PTR = ULONG_PTR
HtmlHelpW = _htmlhelp.HtmlHelpW
HtmlHelpW.restype = HWND
HtmlHelpW.argtypes = [HWND, LPCWSTR, UINT, DWORD_PTR]
HtmlHelp = HtmlHelpW  # alias
HH_DISPLAY_TOPIC = 0  # Variable c_int '0'
GetDesktopWindow = _user32.GetDesktopWindow
GetDesktopWindow.restype = HWND
GetDesktopWindow.argtypes = []
class tagMONITORINFO(Structure):
    pass
LPMONITORINFO = POINTER(tagMONITORINFO)
GetMonitorInfoW = _user32.GetMonitorInfoW
GetMonitorInfoW.restype = BOOL
GetMonitorInfoW.argtypes = [HMONITOR, LPMONITORINFO]
GetMonitorInfo = GetMonitorInfoW  # alias
tagMONITORINFO._fields_ = [
    ('cbSize', DWORD),
    ('rcMonitor', RECT),
    ('rcWork', RECT),
    ('dwFlags', DWORD),
]
MonitorFromWindow = _user32.MonitorFromWindow
MonitorFromWindow.restype = HMONITOR
MonitorFromWindow.argtypes = [HWND, DWORD]
MONITORINFO = tagMONITORINFO
MONITOR_DEFAULTTONEAREST = 2  # Variable c_int '2'
class _MEMORYSTATUSEX(Structure):
    pass
MEMORYSTATUSEX = _MEMORYSTATUSEX
ULONGLONG = c_ulonglong
DWORDLONG = ULONGLONG
_MEMORYSTATUSEX._fields_ = [
    ('dwLength', DWORD),
    ('dwMemoryLoad', DWORD),
    ('ullTotalPhys', DWORDLONG),
    ('ullAvailPhys', DWORDLONG),
    ('ullTotalPageFile', DWORDLONG),
    ('ullAvailPageFile', DWORDLONG),
    ('ullTotalVirtual', DWORDLONG),
    ('ullAvailVirtual', DWORDLONG),
    ('ullAvailExtendedVirtual', DWORDLONG),
]
LPMEMORYSTATUSEX = POINTER(_MEMORYSTATUSEX)
GlobalMemoryStatusEx = _kernel32.GlobalMemoryStatusEx
GlobalMemoryStatusEx.restype = BOOL
GlobalMemoryStatusEx.argtypes = [LPMEMORYSTATUSEX]
GetVolumeInformationW = _kernel32.GetVolumeInformationW
GetVolumeInformationW.restype = BOOL
GetVolumeInformationW.argtypes = [LPCWSTR, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD]
GetVolumeInformation = GetVolumeInformationW  # alias
WaitForSingleObject = _kernel32.WaitForSingleObject
WaitForSingleObject.restype = DWORD
WaitForSingleObject.argtypes = [HANDLE, DWORD]
INFINITE = 4294967295L  # Variable c_uint '-1u'
MAXDWORD = 4294967295L  # Variable c_uint '-1u'
GENERIC_READ = 2147483648L  # Variable c_ulong '-2147483648ul'
GENERIC_WRITE = 1073741824  # Variable c_long '1073741824l'
OPEN_EXISTING = 3  # Variable c_int '3'
FILE_ATTRIBUTE_NORMAL = 128  # Variable c_int '128'
FILE_FLAG_OVERLAPPED = 1073741824  # Variable c_int '1073741824'
ERROR_IO_PENDING = 997  # Variable c_long '997l'
NOPARITY = 0  # Variable c_int '0'
ODDPARITY = 1  # Variable c_int '1'
EVENPARITY = 2  # Variable c_int '2'
MARKPARITY = 3  # Variable c_int '3'
SPACEPARITY = 4  # Variable c_int '4'
ONESTOPBIT = 0  # Variable c_int '0'
ONE5STOPBITS = 1  # Variable c_int '1'
TWOSTOPBITS = 2  # Variable c_int '2'
SETDTR = 5  # Variable c_int '5'
CLRDTR = 6  # Variable c_int '6'
SETRTS = 3  # Variable c_int '3'
CLRRTS = 4  # Variable c_int '4'
DTR_CONTROL_DISABLE = 0  # Variable c_int '0'
EV_BREAK = 64  # Variable c_int '64'
EV_CTS = 8  # Variable c_int '8'
EV_DSR = 16  # Variable c_int '16'
EV_ERR = 128  # Variable c_int '128'
EV_RING = 256  # Variable c_int '256'
EV_RLSD = 32  # Variable c_int '32'
EV_RXCHAR = 1  # Variable c_int '1'
EV_RXFLAG = 2  # Variable c_int '2'
EV_TXEMPTY = 4  # Variable c_int '4'
class _OVERLAPPED(Structure):
    pass
OVERLAPPED = _OVERLAPPED
class N11_OVERLAPPED4DOLLAR_81E(Union):
    pass
class N11_OVERLAPPED4DOLLAR_814DOLLAR_82E(Structure):
    pass
N11_OVERLAPPED4DOLLAR_814DOLLAR_82E._fields_ = [
    ('Offset', DWORD),
    ('OffsetHigh', DWORD),
]
PVOID = c_void_p
N11_OVERLAPPED4DOLLAR_81E._anonymous_ = ['_0']
N11_OVERLAPPED4DOLLAR_81E._fields_ = [
    ('_0', N11_OVERLAPPED4DOLLAR_814DOLLAR_82E),
    ('Pointer', PVOID),
]
_OVERLAPPED._anonymous_ = ['_0']
_OVERLAPPED._fields_ = [
    ('Internal', ULONG_PTR),
    ('InternalHigh', ULONG_PTR),
    ('_0', N11_OVERLAPPED4DOLLAR_81E),
    ('hEvent', HANDLE),
]
class _DCB(Structure):
    pass
DCB = _DCB
_DCB._fields_ = [
    ('DCBlength', DWORD),
    ('BaudRate', DWORD),
    ('fBinary', DWORD, 1),
    ('fParity', DWORD, 1),
    ('fOutxCtsFlow', DWORD, 1),
    ('fOutxDsrFlow', DWORD, 1),
    ('fDtrControl', DWORD, 2),
    ('fDsrSensitivity', DWORD, 1),
    ('fTXContinueOnXoff', DWORD, 1),
    ('fOutX', DWORD, 1),
    ('fInX', DWORD, 1),
    ('fErrorChar', DWORD, 1),
    ('fNull', DWORD, 1),
    ('fRtsControl', DWORD, 2),
    ('fAbortOnError', DWORD, 1),
    ('fDummy2', DWORD, 17),
    ('wReserved', WORD),
    ('XonLim', WORD),
    ('XoffLim', WORD),
    ('ByteSize', BYTE),
    ('Parity', BYTE),
    ('StopBits', BYTE),
    ('XonChar', c_char),
    ('XoffChar', c_char),
    ('ErrorChar', c_char),
    ('EofChar', c_char),
    ('EvtChar', c_char),
    ('wReserved1', WORD),
]
class _COMMCONFIG(Structure):
    pass
COMMCONFIG = _COMMCONFIG
_COMMCONFIG._fields_ = [
    ('dwSize', DWORD),
    ('wVersion', WORD),
    ('wReserved', WORD),
    ('dcb', DCB),
    ('dwProviderSubType', DWORD),
    ('dwProviderOffset', DWORD),
    ('dwProviderSize', DWORD),
    ('wcProviderData', WCHAR * 1),
]
class _COMSTAT(Structure):
    pass
COMSTAT = _COMSTAT
_COMSTAT._fields_ = [
    ('fCtsHold', DWORD, 1),
    ('fDsrHold', DWORD, 1),
    ('fRlsdHold', DWORD, 1),
    ('fXoffHold', DWORD, 1),
    ('fXoffSent', DWORD, 1),
    ('fEof', DWORD, 1),
    ('fTxim', DWORD, 1),
    ('fReserved', DWORD, 25),
    ('cbInQue', DWORD),
    ('cbOutQue', DWORD),
]
class _COMMTIMEOUTS(Structure):
    pass
COMMTIMEOUTS = _COMMTIMEOUTS
_COMMTIMEOUTS._fields_ = [
    ('ReadIntervalTimeout', DWORD),
    ('ReadTotalTimeoutMultiplier', DWORD),
    ('ReadTotalTimeoutConstant', DWORD),
    ('WriteTotalTimeoutMultiplier', DWORD),
    ('WriteTotalTimeoutConstant', DWORD),
]
ResetEvent = _kernel32.ResetEvent
ResetEvent.restype = BOOL
ResetEvent.argtypes = [HANDLE]
CreateFileW = _kernel32.CreateFileW
CreateFileW.restype = HANDLE
CreateFileW.argtypes = [LPCWSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE]
CreateFile = CreateFileW  # alias
LPOVERLAPPED = POINTER(_OVERLAPPED)
ReadFile = _kernel32.ReadFile
ReadFile.restype = BOOL
ReadFile.argtypes = [HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED]
WriteFile = _kernel32.WriteFile
WriteFile.restype = BOOL
WriteFile.argtypes = [HANDLE, LPCVOID, DWORD, LPDWORD, LPOVERLAPPED]
GetOverlappedResult = _kernel32.GetOverlappedResult
GetOverlappedResult.restype = BOOL
GetOverlappedResult.argtypes = [HANDLE, LPOVERLAPPED, LPDWORD, BOOL]
LPDCB = POINTER(_DCB)
GetCommState = _kernel32.GetCommState
GetCommState.restype = BOOL
GetCommState.argtypes = [HANDLE, LPDCB]
SetCommState = _kernel32.SetCommState
SetCommState.restype = BOOL
SetCommState.argtypes = [HANDLE, LPDCB]
EscapeCommFunction = _kernel32.EscapeCommFunction
EscapeCommFunction.restype = BOOL
EscapeCommFunction.argtypes = [HANDLE, DWORD]
LPCOMSTAT = POINTER(_COMSTAT)
ClearCommError = _kernel32.ClearCommError
ClearCommError.restype = BOOL
ClearCommError.argtypes = [HANDLE, LPDWORD, LPCOMSTAT]
LPCOMMCONFIG = POINTER(_COMMCONFIG)
GetDefaultCommConfigW = _kernel32.GetDefaultCommConfigW
GetDefaultCommConfigW.restype = BOOL
GetDefaultCommConfigW.argtypes = [LPCWSTR, LPCOMMCONFIG, LPDWORD]
GetDefaultCommConfig = GetDefaultCommConfigW  # alias
LPCOMMTIMEOUTS = POINTER(_COMMTIMEOUTS)
GetCommTimeouts = _kernel32.GetCommTimeouts
GetCommTimeouts.restype = BOOL
GetCommTimeouts.argtypes = [HANDLE, LPCOMMTIMEOUTS]
SetCommTimeouts = _kernel32.SetCommTimeouts
SetCommTimeouts.restype = BOOL
SetCommTimeouts.argtypes = [HANDLE, LPCOMMTIMEOUTS]
WaitCommEvent = _kernel32.WaitCommEvent
WaitCommEvent.restype = BOOL
WaitCommEvent.argtypes = [HANDLE, LPDWORD, LPOVERLAPPED]
SetCommMask = _kernel32.SetCommMask
SetCommMask.restype = BOOL
SetCommMask.argtypes = [HANDLE, DWORD]
WS_CHILD = 1073741824  # Variable c_long '1073741824l'
WS_VISIBLE = 268435456  # Variable c_long '268435456l'
SBS_SIZEGRIP = 16  # Variable c_long '16l'
SBS_SIZEBOXTOPLEFTALIGN = 2  # Variable c_long '2l'
SM_CYHSCROLL = 3  # Variable c_int '3'
SM_CXVSCROLL = 2  # Variable c_int '2'
GA_PARENT = 1  # Variable c_int '1'
CreateNamedPipeW = _kernel32.CreateNamedPipeW
CreateNamedPipeW.restype = HANDLE
CreateNamedPipeW.argtypes = [LPCWSTR, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, LPSECURITY_ATTRIBUTES]
CreateNamedPipe = CreateNamedPipeW  # alias
FlushFileBuffers = _kernel32.FlushFileBuffers
FlushFileBuffers.restype = BOOL
FlushFileBuffers.argtypes = [HANDLE]
ConnectNamedPipe = _kernel32.ConnectNamedPipe
ConnectNamedPipe.restype = BOOL
ConnectNamedPipe.argtypes = [HANDLE, LPOVERLAPPED]
DisconnectNamedPipe = _kernel32.DisconnectNamedPipe
DisconnectNamedPipe.restype = BOOL
DisconnectNamedPipe.argtypes = [HANDLE]
WaitForMultipleObjects = _kernel32.WaitForMultipleObjects
WaitForMultipleObjects.restype = DWORD
WaitForMultipleObjects.argtypes = [DWORD, POINTER(HANDLE), BOOL, DWORD]
PIPE_ACCESS_DUPLEX = 3  # Variable c_int '3'
PIPE_TYPE_MESSAGE = 4  # Variable c_int '4'
PIPE_READMODE_MESSAGE = 2  # Variable c_int '2'
PIPE_WAIT = 0  # Variable c_int '0'
PIPE_UNLIMITED_INSTANCES = 255  # Variable c_int '255'
ERROR_NOT_CONNECTED = 2250  # Variable c_long '2250l'
class _SHELLEXECUTEINFOW(Structure):
    pass
SHELLEXECUTEINFOW = _SHELLEXECUTEINFOW
SHELLEXECUTEINFO = SHELLEXECUTEINFOW
class N18_SHELLEXECUTEINFOW5DOLLAR_249E(Union):
    pass
N18_SHELLEXECUTEINFOW5DOLLAR_249E._pack_ = 1
N18_SHELLEXECUTEINFOW5DOLLAR_249E._fields_ = [
    ('hIcon', HANDLE),
    ('hMonitor', HANDLE),
]
_SHELLEXECUTEINFOW._pack_ = 1
_SHELLEXECUTEINFOW._anonymous_ = ['_0']
_SHELLEXECUTEINFOW._fields_ = [
    ('cbSize', DWORD),
    ('fMask', DWORD),
    ('hwnd', HWND),
    ('lpVerb', LPCWSTR),
    ('lpFile', LPCWSTR),
    ('lpParameters', LPCWSTR),
    ('lpDirectory', LPCWSTR),
    ('nShow', c_int),
    ('hInstApp', HINSTANCE),
    ('lpIDList', LPVOID),
    ('lpClass', LPCWSTR),
    ('hkeyClass', HKEY),
    ('dwHotKey', DWORD),
    ('_0', N18_SHELLEXECUTEINFOW5DOLLAR_249E),
    ('hProcess', HANDLE),
]
SEE_MASK_NOASYNC = 256  # Variable c_int '256'
SEE_MASK_FLAG_DDEWAIT = SEE_MASK_NOASYNC  # alias
SEE_MASK_FLAG_NO_UI = 1024  # Variable c_int '1024'
SEE_MASK_NOCLOSEPROCESS = 64  # Variable c_int '64'
SW_SHOWNORMAL = 1  # Variable c_int '1'

# values for enumeration '_TOKEN_INFORMATION_CLASS'
TokenUser = 1
TokenGroups = 2
TokenPrivileges = 3
TokenOwner = 4
TokenPrimaryGroup = 5
TokenDefaultDacl = 6
TokenSource = 7
TokenType = 8
TokenImpersonationLevel = 9
TokenStatistics = 10
TokenRestrictedSids = 11
TokenSessionId = 12
TokenGroupsAndPrivileges = 13
TokenSessionReference = 14
TokenSandBoxInert = 15
TokenAuditPolicy = 16
TokenOrigin = 17
TokenElevationType = 18
TokenLinkedToken = 19
TokenElevation = 20
TokenHasRestrictions = 21
TokenAccessInformation = 22
TokenVirtualizationAllowed = 23
TokenVirtualizationEnabled = 24
TokenIntegrityLevel = 25
TokenUIAccess = 26
TokenMandatoryPolicy = 27
TokenLogonSid = 28
MaxTokenInfoClass = 29
_TOKEN_INFORMATION_CLASS = c_int  # enum
TOKEN_INFORMATION_CLASS = _TOKEN_INFORMATION_CLASS
PDWORD = POINTER(DWORD)
GetTokenInformation = _Advapi32.GetTokenInformation
GetTokenInformation.restype = BOOL
GetTokenInformation.argtypes = [HANDLE, TOKEN_INFORMATION_CLASS, LPVOID, DWORD, PDWORD]
GetCurrentThread = _kernel32.GetCurrentThread
GetCurrentThread.restype = HANDLE
GetCurrentThread.argtypes = []
GetCurrentProcess = _kernel32.GetCurrentProcess
GetCurrentProcess.restype = HANDLE
GetCurrentProcess.argtypes = []
TOKEN_QUERY = 8  # Variable c_int '8'
ERROR_NO_TOKEN = 1008  # Variable c_long '1008l'
ERROR_INSUFFICIENT_BUFFER = 122  # Variable c_long '122l'
class _TOKEN_GROUPS(Structure):
    pass
TOKEN_GROUPS = _TOKEN_GROUPS
class _SID_AND_ATTRIBUTES(Structure):
    pass
PSID = PVOID
_SID_AND_ATTRIBUTES._fields_ = [
    ('Sid', PSID),
    ('Attributes', DWORD),
]
SID_AND_ATTRIBUTES = _SID_AND_ATTRIBUTES
_TOKEN_GROUPS._fields_ = [
    ('GroupCount', DWORD),
    ('Groups', SID_AND_ATTRIBUTES * 1),
]
SECURITY_BUILTIN_DOMAIN_RID = 32  # Variable c_long '32l'
DOMAIN_ALIAS_RID_ADMINS = 544  # Variable c_long '544l'
class _SID_IDENTIFIER_AUTHORITY(Structure):
    pass
PSID_IDENTIFIER_AUTHORITY = POINTER(_SID_IDENTIFIER_AUTHORITY)
AllocateAndInitializeSid = _Advapi32.AllocateAndInitializeSid
AllocateAndInitializeSid.restype = BOOL
AllocateAndInitializeSid.argtypes = [PSID_IDENTIFIER_AUTHORITY, BYTE, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, POINTER(PSID)]
_SID_IDENTIFIER_AUTHORITY._fields_ = [
    ('Value', BYTE * 6),
]
SID_IDENTIFIER_AUTHORITY = _SID_IDENTIFIER_AUTHORITY
EqualSid = _Advapi32.EqualSid
EqualSid.restype = BOOL
EqualSid.argtypes = [PSID, PSID]
FreeSid = _Advapi32.FreeSid
FreeSid.restype = PVOID
FreeSid.argtypes = [PSID]
class _GUID(Structure):
    pass
GUID = _GUID
_GUID._fields_ = [
    ('Data1', c_ulong),
    ('Data2', c_ushort),
    ('Data3', c_ushort),
    ('Data4', c_ubyte * 8),
]
CLSID = GUID
LPCLSID = POINTER(CLSID)
CLSIDFromString = _ole32.CLSIDFromString
CLSIDFromString.restype = HRESULT
CLSIDFromString.argtypes = [LPOLESTR, LPCLSID]
ERROR_NO_MORE_ITEMS = 259  # Variable c_long '259l'
ENUM_CURRENT_SETTINGS = 4294967295L  # Variable c_ulong '-1u'
EDS_RAWMODE = 2  # Variable c_int '2'
class _DISPLAY_DEVICEW(Structure):
    pass
PDISPLAY_DEVICEW = POINTER(_DISPLAY_DEVICEW)
EnumDisplayDevicesW = _user32.EnumDisplayDevicesW
EnumDisplayDevicesW.restype = BOOL
EnumDisplayDevicesW.argtypes = [LPCWSTR, DWORD, PDISPLAY_DEVICEW, DWORD]
EnumDisplayDevices = EnumDisplayDevicesW  # alias
_DISPLAY_DEVICEW._fields_ = [
    ('cb', DWORD),
    ('DeviceName', WCHAR * 32),
    ('DeviceString', WCHAR * 128),
    ('StateFlags', DWORD),
    ('DeviceID', WCHAR * 128),
    ('DeviceKey', WCHAR * 128),
]
class _devicemodeW(Structure):
    pass
LPDEVMODEW = POINTER(_devicemodeW)
EnumDisplaySettingsExW = _user32.EnumDisplaySettingsExW
EnumDisplaySettingsExW.restype = BOOL
EnumDisplaySettingsExW.argtypes = [LPCWSTR, DWORD, LPDEVMODEW, DWORD]
EnumDisplaySettingsEx = EnumDisplaySettingsExW  # alias
class N12_devicemodeW4DOLLAR_96E(Union):
    pass
class N12_devicemodeW4DOLLAR_964DOLLAR_97E(Structure):
    pass
N12_devicemodeW4DOLLAR_964DOLLAR_97E._fields_ = [
    ('dmOrientation', c_short),
    ('dmPaperSize', c_short),
    ('dmPaperLength', c_short),
    ('dmPaperWidth', c_short),
    ('dmScale', c_short),
    ('dmCopies', c_short),
    ('dmDefaultSource', c_short),
    ('dmPrintQuality', c_short),
]
class N12_devicemodeW4DOLLAR_964DOLLAR_98E(Structure):
    pass
N12_devicemodeW4DOLLAR_964DOLLAR_98E._fields_ = [
    ('dmPosition', POINTL),
    ('dmDisplayOrientation', DWORD),
    ('dmDisplayFixedOutput', DWORD),
]
N12_devicemodeW4DOLLAR_96E._anonymous_ = ['_0', '_1']
N12_devicemodeW4DOLLAR_96E._fields_ = [
    ('_0', N12_devicemodeW4DOLLAR_964DOLLAR_97E),
    ('_1', N12_devicemodeW4DOLLAR_964DOLLAR_98E),
]
class N12_devicemodeW4DOLLAR_99E(Union):
    pass
N12_devicemodeW4DOLLAR_99E._fields_ = [
    ('dmDisplayFlags', DWORD),
    ('dmNup', DWORD),
]
_devicemodeW._anonymous_ = ['_0', '_1']
_devicemodeW._fields_ = [
    ('dmDeviceName', WCHAR * 32),
    ('dmSpecVersion', WORD),
    ('dmDriverVersion', WORD),
    ('dmSize', WORD),
    ('dmDriverExtra', WORD),
    ('dmFields', DWORD),
    ('_0', N12_devicemodeW4DOLLAR_96E),
    ('dmColor', c_short),
    ('dmDuplex', c_short),
    ('dmYResolution', c_short),
    ('dmTTOption', c_short),
    ('dmCollate', c_short),
    ('dmFormName', WCHAR * 32),
    ('dmLogPixels', WORD),
    ('dmBitsPerPel', DWORD),
    ('dmPelsWidth', DWORD),
    ('dmPelsHeight', DWORD),
    ('_1', N12_devicemodeW4DOLLAR_99E),
    ('dmDisplayFrequency', DWORD),
    ('dmICMMethod', DWORD),
    ('dmICMIntent', DWORD),
    ('dmMediaType', DWORD),
    ('dmDitherType', DWORD),
    ('dmReserved1', DWORD),
    ('dmReserved2', DWORD),
    ('dmPanningWidth', DWORD),
    ('dmPanningHeight', DWORD),
]
ChangeDisplaySettingsExW = _user32.ChangeDisplaySettingsExW
ChangeDisplaySettingsExW.restype = LONG
ChangeDisplaySettingsExW.argtypes = [LPCWSTR, LPDEVMODEW, HWND, DWORD, LPVOID]
ChangeDisplaySettingsEx = ChangeDisplaySettingsExW  # alias
DISPLAY_DEVICEW = _DISPLAY_DEVICEW
DISPLAY_DEVICE = DISPLAY_DEVICEW
DEVMODEW = _devicemodeW
DEVMODE = DEVMODEW
DISPLAY_DEVICE_MIRRORING_DRIVER = 8  # Variable c_int '8'
DISPLAY_DEVICE_PRIMARY_DEVICE = 4  # Variable c_int '4'
DISPLAY_DEVICE_ATTACHED_TO_DESKTOP = 1  # Variable c_int '1'
DM_POSITION = 32  # Variable c_long '32l'
DM_BITSPERPEL = 262144  # Variable c_long '262144l'
DM_PELSWIDTH = 524288  # Variable c_long '524288l'
DM_PELSHEIGHT = 1048576  # Variable c_long '1048576l'
DM_DISPLAYFLAGS = 2097152  # Variable c_long '2097152l'
DM_DISPLAYFREQUENCY = 4194304  # Variable c_long '4194304l'
CDS_UPDATEREGISTRY = 1  # Variable c_int '1'
CDS_NORESET = 268435456  # Variable c_int '268435456'
CDS_SET_PRIMARY = 16  # Variable c_int '16'
SetNamedPipeHandleState = _kernel32.SetNamedPipeHandleState
SetNamedPipeHandleState.restype = BOOL
SetNamedPipeHandleState.argtypes = [HANDLE, LPDWORD, LPDWORD, LPDWORD]
WaitNamedPipeW = _kernel32.WaitNamedPipeW
WaitNamedPipeW.restype = BOOL
WaitNamedPipeW.argtypes = [LPCWSTR, DWORD]
WaitNamedPipe = WaitNamedPipeW  # alias
FILE_SHARE_READ = 1  # Variable c_int '1'
FILE_SHARE_WRITE = 2  # Variable c_int '2'
ERROR_MORE_DATA = 234  # Variable c_long '234l'
class tagRAWINPUTDEVICELIST(Structure):
    pass
PRAWINPUTDEVICELIST = POINTER(tagRAWINPUTDEVICELIST)
PUINT = POINTER(c_uint)
GetRawInputDeviceList = _user32.GetRawInputDeviceList
GetRawInputDeviceList.restype = UINT
GetRawInputDeviceList.argtypes = [PRAWINPUTDEVICELIST, PUINT, UINT]
tagRAWINPUTDEVICELIST._fields_ = [
    ('hDevice', HANDLE),
    ('dwType', DWORD),
]
GetRawInputDeviceInfoW = _user32.GetRawInputDeviceInfoW
GetRawInputDeviceInfoW.restype = UINT
GetRawInputDeviceInfoW.argtypes = [HANDLE, UINT, LPVOID, PUINT]
GetRawInputDeviceInfo = GetRawInputDeviceInfoW  # alias
class tagRAWINPUTDEVICE(Structure):
    pass
RAWINPUTDEVICE = tagRAWINPUTDEVICE
PCRAWINPUTDEVICE = POINTER(RAWINPUTDEVICE)
RegisterRawInputDevices = _user32.RegisterRawInputDevices
RegisterRawInputDevices.restype = BOOL
RegisterRawInputDevices.argtypes = [PCRAWINPUTDEVICE, UINT, UINT]
tagRAWINPUTDEVICE._fields_ = [
    ('usUsagePage', USHORT),
    ('usUsage', USHORT),
    ('dwFlags', DWORD),
    ('hwndTarget', HWND),
]
HRAWINPUT = HANDLE
GetRawInputData = _user32.GetRawInputData
GetRawInputData.restype = UINT
GetRawInputData.argtypes = [HRAWINPUT, UINT, LPVOID, PUINT, UINT]
class tagRAWINPUTHEADER(Structure):
    pass
RAWINPUTHEADER = tagRAWINPUTHEADER
tagRAWINPUTHEADER._fields_ = [
    ('dwType', DWORD),
    ('dwSize', DWORD),
    ('hDevice', HANDLE),
    ('wParam', WPARAM),
]
class tagRAWINPUT(Structure):
    pass
RAWINPUT = tagRAWINPUT
class N11tagRAWINPUT5DOLLAR_110E(Union):
    pass
class tagRAWMOUSE(Structure):
    pass
class N11tagRAWMOUSE5DOLLAR_108E(Union):
    pass
class N11tagRAWMOUSE5DOLLAR_1085DOLLAR_109E(Structure):
    pass
N11tagRAWMOUSE5DOLLAR_1085DOLLAR_109E._fields_ = [
    ('usButtonFlags', USHORT),
    ('usButtonData', USHORT),
]
N11tagRAWMOUSE5DOLLAR_108E._anonymous_ = ['_0']
N11tagRAWMOUSE5DOLLAR_108E._fields_ = [
    ('ulButtons', ULONG),
    ('_0', N11tagRAWMOUSE5DOLLAR_1085DOLLAR_109E),
]
tagRAWMOUSE._anonymous_ = ['_0']
tagRAWMOUSE._fields_ = [
    ('usFlags', USHORT),
    ('_0', N11tagRAWMOUSE5DOLLAR_108E),
    ('ulRawButtons', ULONG),
    ('lLastX', LONG),
    ('lLastY', LONG),
    ('ulExtraInformation', ULONG),
]
RAWMOUSE = tagRAWMOUSE
class tagRAWKEYBOARD(Structure):
    pass
tagRAWKEYBOARD._fields_ = [
    ('MakeCode', USHORT),
    ('Flags', USHORT),
    ('Reserved', USHORT),
    ('VKey', USHORT),
    ('Message', UINT),
    ('ExtraInformation', ULONG),
]
RAWKEYBOARD = tagRAWKEYBOARD
class tagRAWHID(Structure):
    pass
tagRAWHID._fields_ = [
    ('dwSizeHid', DWORD),
    ('dwCount', DWORD),
    ('bRawData', BYTE * 1),
]
RAWHID = tagRAWHID
N11tagRAWINPUT5DOLLAR_110E._fields_ = [
    ('mouse', RAWMOUSE),
    ('keyboard', RAWKEYBOARD),
    ('hid', RAWHID),
]
tagRAWINPUT._fields_ = [
    ('header', RAWINPUTHEADER),
    ('data', N11tagRAWINPUT5DOLLAR_110E),
]
RAWINPUTDEVICELIST = tagRAWINPUTDEVICELIST
class tagRID_DEVICE_INFO(Structure):
    pass
RID_DEVICE_INFO = tagRID_DEVICE_INFO
class N18tagRID_DEVICE_INFO5DOLLAR_111E(Union):
    pass
class tagRID_DEVICE_INFO_MOUSE(Structure):
    pass
tagRID_DEVICE_INFO_MOUSE._fields_ = [
    ('dwId', DWORD),
    ('dwNumberOfButtons', DWORD),
    ('dwSampleRate', DWORD),
    ('fHasHorizontalWheel', BOOL),
]
RID_DEVICE_INFO_MOUSE = tagRID_DEVICE_INFO_MOUSE
class tagRID_DEVICE_INFO_KEYBOARD(Structure):
    pass
tagRID_DEVICE_INFO_KEYBOARD._fields_ = [
    ('dwType', DWORD),
    ('dwSubType', DWORD),
    ('dwKeyboardMode', DWORD),
    ('dwNumberOfFunctionKeys', DWORD),
    ('dwNumberOfIndicators', DWORD),
    ('dwNumberOfKeysTotal', DWORD),
]
RID_DEVICE_INFO_KEYBOARD = tagRID_DEVICE_INFO_KEYBOARD
class tagRID_DEVICE_INFO_HID(Structure):
    pass
tagRID_DEVICE_INFO_HID._fields_ = [
    ('dwVendorId', DWORD),
    ('dwProductId', DWORD),
    ('dwVersionNumber', DWORD),
    ('usUsagePage', USHORT),
    ('usUsage', USHORT),
]
RID_DEVICE_INFO_HID = tagRID_DEVICE_INFO_HID
N18tagRID_DEVICE_INFO5DOLLAR_111E._fields_ = [
    ('mouse', RID_DEVICE_INFO_MOUSE),
    ('keyboard', RID_DEVICE_INFO_KEYBOARD),
    ('hid', RID_DEVICE_INFO_HID),
]
tagRID_DEVICE_INFO._anonymous_ = ['_0']
tagRID_DEVICE_INFO._fields_ = [
    ('cbSize', DWORD),
    ('dwType', DWORD),
    ('_0', N18tagRID_DEVICE_INFO5DOLLAR_111E),
]
RID_INPUT = 268435459  # Variable c_int '268435459'
RIDI_PREPARSEDDATA = 536870917  # Variable c_int '536870917'
RIDI_DEVICENAME = 536870919  # Variable c_int '536870919'
RIDI_DEVICEINFO = 536870923  # Variable c_int '536870923'
RIM_TYPEHID = 2  # Variable c_int '2'
RIM_TYPEKEYBOARD = 1  # Variable c_int '1'
RIM_TYPEMOUSE = 0  # Variable c_int '0'
RIM_INPUT = 0  # Variable c_int '0'
RIDEV_NOLEGACY = 48  # Variable c_int '48'
RIDEV_INPUTSINK = 256  # Variable c_int '256'
WM_INPUT = 255  # Variable c_int '255'
def GET_RAWINPUT_CODE_WPARAM(wParam):
    return ((wParam) & 0xff)  # macro
TCHAR = WCHAR
OpenSCManagerW = _Advapi32.OpenSCManagerW
OpenSCManagerW.restype = SC_HANDLE
OpenSCManagerW.argtypes = [LPCWSTR, LPCWSTR, DWORD]
OpenSCManager = OpenSCManagerW  # alias
SC_MANAGER_ALL_ACCESS = 983103  # Variable c_long '983103l'
CreateServiceW = _Advapi32.CreateServiceW
CreateServiceW.restype = SC_HANDLE
CreateServiceW.argtypes = [SC_HANDLE, LPCWSTR, LPCWSTR, DWORD, DWORD, DWORD, DWORD, LPCWSTR, LPCWSTR, LPDWORD, LPCWSTR, LPCWSTR, LPCWSTR]
CreateService = CreateServiceW  # alias
SERVICE_ALL_ACCESS = 983551  # Variable c_long '983551l'
SERVICE_WIN32_OWN_PROCESS = 16  # Variable c_int '16'
SERVICE_DEMAND_START = 3  # Variable c_int '3'
SERVICE_AUTO_START = 2  # Variable c_int '2'
SERVICE_ERROR_NORMAL = 1  # Variable c_int '1'
CloseServiceHandle = _Advapi32.CloseServiceHandle
CloseServiceHandle.restype = BOOL
CloseServiceHandle.argtypes = [SC_HANDLE]
DELETE = 65536  # Variable c_long '65536l'
OpenServiceW = _Advapi32.OpenServiceW
OpenServiceW.restype = SC_HANDLE
OpenServiceW.argtypes = [SC_HANDLE, LPCWSTR, DWORD]
OpenService = OpenServiceW  # alias
DeleteService = _Advapi32.DeleteService
DeleteService.restype = BOOL
DeleteService.argtypes = [SC_HANDLE]

# values for enumeration '_SC_STATUS_TYPE'
SC_STATUS_PROCESS_INFO = 0
_SC_STATUS_TYPE = c_int  # enum
SC_STATUS_TYPE = _SC_STATUS_TYPE
QueryServiceStatusEx = _Advapi32.QueryServiceStatusEx
QueryServiceStatusEx.restype = BOOL
QueryServiceStatusEx.argtypes = [SC_HANDLE, SC_STATUS_TYPE, LPBYTE, DWORD, LPDWORD]
class _SERVICE_STATUS_PROCESS(Structure):
    pass
SERVICE_STATUS_PROCESS = _SERVICE_STATUS_PROCESS
_SERVICE_STATUS_PROCESS._fields_ = [
    ('dwServiceType', DWORD),
    ('dwCurrentState', DWORD),
    ('dwControlsAccepted', DWORD),
    ('dwWin32ExitCode', DWORD),
    ('dwServiceSpecificExitCode', DWORD),
    ('dwCheckPoint', DWORD),
    ('dwWaitHint', DWORD),
    ('dwProcessId', DWORD),
    ('dwServiceFlags', DWORD),
]
SERVICE_QUERY_STATUS = 4  # Variable c_int '4'
SERVICE_STOPPED = 1  # Variable c_int '1'
SERVICE_STOP_PENDING = 3  # Variable c_int '3'
SERVICE_START_PENDING = 2  # Variable c_int '2'
SERVICE_RUNNING = 4  # Variable c_int '4'
SERVICE_CONTROL_STOP = 1  # Variable c_int '1'
SERVICE_ACTIVE = 1  # Variable c_int '1'
GetTickCount = _kernel32.GetTickCount
GetTickCount.restype = DWORD
GetTickCount.argtypes = []
Sleep = _kernel32.Sleep
Sleep.restype = None
Sleep.argtypes = [DWORD]
StartServiceW = _Advapi32.StartServiceW
StartServiceW.restype = BOOL
StartServiceW.argtypes = [SC_HANDLE, DWORD, POINTER(LPCWSTR)]
StartService = StartServiceW  # alias
class _SERVICE_STATUS(Structure):
    pass
LPSERVICE_STATUS = POINTER(_SERVICE_STATUS)
ControlService = _Advapi32.ControlService
ControlService.restype = BOOL
ControlService.argtypes = [SC_HANDLE, DWORD, LPSERVICE_STATUS]
_SERVICE_STATUS._fields_ = [
    ('dwServiceType', DWORD),
    ('dwCurrentState', DWORD),
    ('dwControlsAccepted', DWORD),
    ('dwWin32ExitCode', DWORD),
    ('dwServiceSpecificExitCode', DWORD),
    ('dwCheckPoint', DWORD),
    ('dwWaitHint', DWORD),
]
class _ENUM_SERVICE_STATUSW(Structure):
    pass
LPENUM_SERVICE_STATUSW = POINTER(_ENUM_SERVICE_STATUSW)
EnumDependentServicesW = _Advapi32.EnumDependentServicesW
EnumDependentServicesW.restype = BOOL
EnumDependentServicesW.argtypes = [SC_HANDLE, DWORD, LPENUM_SERVICE_STATUSW, DWORD, LPDWORD, LPDWORD]
EnumDependentServices = EnumDependentServicesW  # alias
SERVICE_STATUS = _SERVICE_STATUS
_ENUM_SERVICE_STATUSW._fields_ = [
    ('lpServiceName', LPWSTR),
    ('lpDisplayName', LPWSTR),
    ('ServiceStatus', SERVICE_STATUS),
]
ChangeServiceConfig2W = _Advapi32.ChangeServiceConfig2W
ChangeServiceConfig2W.restype = BOOL
ChangeServiceConfig2W.argtypes = [SC_HANDLE, DWORD, LPVOID]
ChangeServiceConfig2 = ChangeServiceConfig2W  # alias
class _SERVICE_DESCRIPTIONW(Structure):
    pass
SERVICE_DESCRIPTIONW = _SERVICE_DESCRIPTIONW
SERVICE_DESCRIPTION = SERVICE_DESCRIPTIONW
_SERVICE_DESCRIPTIONW._fields_ = [
    ('lpDescription', LPWSTR),
]
SERVICE_CONFIG_DESCRIPTION = 1  # Variable c_int '1'
SERVICE_CHANGE_CONFIG = 2  # Variable c_int '2'
GetExitCodeProcess = _kernel32.GetExitCodeProcess
GetExitCodeProcess.restype = BOOL
GetExitCodeProcess.argtypes = [HANDLE, LPDWORD]
mouse_event = _user32.mouse_event
mouse_event.restype = None
mouse_event.argtypes = [DWORD, DWORD, DWORD, DWORD, ULONG_PTR]
PulseEvent = _kernel32.PulseEvent
PulseEvent.restype = BOOL
PulseEvent.argtypes = [HANDLE]
LPOVERLAPPED_COMPLETION_ROUTINE = WINFUNCTYPE(None, DWORD, DWORD, LPOVERLAPPED)
ReadDirectoryChangesW = _kernel32.ReadDirectoryChangesW
ReadDirectoryChangesW.restype = BOOL
ReadDirectoryChangesW.argtypes = [HANDLE, LPVOID, DWORD, BOOL, DWORD, LPDWORD, LPOVERLAPPED, LPOVERLAPPED_COMPLETION_ROUTINE]
class _FILE_NOTIFY_INFORMATION(Structure):
    pass
FILE_NOTIFY_INFORMATION = _FILE_NOTIFY_INFORMATION
_FILE_NOTIFY_INFORMATION._fields_ = [
    ('NextEntryOffset', DWORD),
    ('Action', DWORD),
    ('FileNameLength', DWORD),
    ('FileName', WCHAR * 1),
]
FILE_FLAG_BACKUP_SEMANTICS = 33554432  # Variable c_int '33554432'
FILE_NOTIFY_CHANGE_FILE_NAME = 1  # Variable c_int '1'
FILE_NOTIFY_CHANGE_DIR_NAME = 2  # Variable c_int '2'
FILE_NOTIFY_CHANGE_ATTRIBUTES = 4  # Variable c_int '4'
FILE_NOTIFY_CHANGE_SIZE = 8  # Variable c_int '8'
FILE_NOTIFY_CHANGE_LAST_WRITE = 16  # Variable c_int '16'
FILE_NOTIFY_CHANGE_SECURITY = 256  # Variable c_int '256'
FILE_LIST_DIRECTORY = 1  # Variable c_int '1'
FILE_ACTION_ADDED = 1  # Variable c_int '1'
FILE_ACTION_REMOVED = 2  # Variable c_int '2'
FILE_ACTION_MODIFIED = 3  # Variable c_int '3'
FILE_ACTION_RENAMED_OLD_NAME = 4  # Variable c_int '4'
FILE_ACTION_RENAMED_NEW_NAME = 5  # Variable c_int '5'
class _STARTUPINFOW(Structure):
    pass
LPSTARTUPINFOW = POINTER(_STARTUPINFOW)
class _PROCESS_INFORMATION(Structure):
    pass
LPPROCESS_INFORMATION = POINTER(_PROCESS_INFORMATION)
CreateProcessW = _kernel32.CreateProcessW
CreateProcessW.restype = BOOL
CreateProcessW.argtypes = [LPCWSTR, LPWSTR, LPSECURITY_ATTRIBUTES, LPSECURITY_ATTRIBUTES, BOOL, DWORD, LPVOID, LPCWSTR, LPSTARTUPINFOW, LPPROCESS_INFORMATION]
CreateProcess = CreateProcessW  # alias
_PROCESS_INFORMATION._fields_ = [
    ('hProcess', HANDLE),
    ('hThread', HANDLE),
    ('dwProcessId', DWORD),
    ('dwThreadId', DWORD),
]
_STARTUPINFOW._fields_ = [
    ('cb', DWORD),
    ('lpReserved', LPWSTR),
    ('lpDesktop', LPWSTR),
    ('lpTitle', LPWSTR),
    ('dwX', DWORD),
    ('dwY', DWORD),
    ('dwXSize', DWORD),
    ('dwYSize', DWORD),
    ('dwXCountChars', DWORD),
    ('dwYCountChars', DWORD),
    ('dwFillAttribute', DWORD),
    ('dwFlags', DWORD),
    ('wShowWindow', WORD),
    ('cbReserved2', WORD),
    ('lpReserved2', LPBYTE),
    ('hStdInput', HANDLE),
    ('hStdOutput', HANDLE),
    ('hStdError', HANDLE),
]
STARTUPINFOW = _STARTUPINFOW
STARTUPINFO = STARTUPINFOW
PROCESS_INFORMATION = _PROCESS_INFORMATION
CREATE_NEW_CONSOLE = 16  # Variable c_int '16'
STARTF_USESHOWWINDOW = 1  # Variable c_int '1'
SetWindowPos = _user32.SetWindowPos
SetWindowPos.restype = BOOL
SetWindowPos.argtypes = [HWND, HWND, c_int, c_int, c_int, c_int, UINT]
SWP_HIDEWINDOW = 128  # Variable c_int '128'
SWP_FRAMECHANGED = 32  # Variable c_int '32'
SWP_NOACTIVATE = 16  # Variable c_int '16'
SWP_NOOWNERZORDER = 512  # Variable c_int '512'
SWP_SHOWWINDOW = 64  # Variable c_int '64'
RegisterWindowMessageW = _user32.RegisterWindowMessageW
RegisterWindowMessageW.restype = UINT
RegisterWindowMessageW.argtypes = [LPCWSTR]
RegisterWindowMessage = RegisterWindowMessageW  # alias
class tagCOPYDATASTRUCT(Structure):
    pass
COPYDATASTRUCT = tagCOPYDATASTRUCT
tagCOPYDATASTRUCT._fields_ = [
    ('dwData', ULONG_PTR),
    ('cbData', DWORD),
    ('lpData', PVOID),
]
PCOPYDATASTRUCT = POINTER(tagCOPYDATASTRUCT)
WM_COPYDATA = 74  # Variable c_int '74'
def CreateWindowW(lpClassName, lpWindowName, dwStyle, x, y, nWidth, nHeight, hWndParent, hMenu, hInstance, lpParam):
    return CreateWindowExW(0L, lpClassName, lpWindowName, dwStyle, x, y, nWidth, nHeight, hWndParent, hMenu, hInstance, lpParam)  # macro
CreateWindow = CreateWindowW  # alias
DestroyWindow = _user32.DestroyWindow
DestroyWindow.restype = BOOL
DestroyWindow.argtypes = [HWND]
UnregisterClassW = _user32.UnregisterClassW
UnregisterClassW.restype = BOOL
UnregisterClassW.argtypes = [LPCWSTR, HINSTANCE]
UnregisterClass = UnregisterClassW  # alias
LoadCursorW = _user32.LoadCursorW
LoadCursorW.restype = HCURSOR
LoadCursorW.argtypes = [HINSTANCE, LPCWSTR]
LoadCursor = LoadCursorW  # alias
SetCursorPos = _user32.SetCursorPos
SetCursorPos.restype = BOOL
SetCursorPos.argtypes = [c_int, c_int]
GetDriveTypeW = _kernel32.GetDriveTypeW
GetDriveTypeW.restype = UINT
GetDriveTypeW.argtypes = [LPCWSTR]
GetDriveType = GetDriveTypeW  # alias
EXECUTION_STATE = DWORD
SetThreadExecutionState = _kernel32.SetThreadExecutionState
SetThreadExecutionState.restype = EXECUTION_STATE
SetThreadExecutionState.argtypes = [EXECUTION_STATE]
InitiateSystemShutdownW = _Advapi32.InitiateSystemShutdownW
InitiateSystemShutdownW.restype = BOOL
InitiateSystemShutdownW.argtypes = [LPWSTR, LPWSTR, DWORD, BOOL, BOOL]
InitiateSystemShutdown = InitiateSystemShutdownW  # alias
DeviceIoControl = _kernel32.DeviceIoControl
DeviceIoControl.restype = BOOL
DeviceIoControl.argtypes = [HANDLE, DWORD, LPVOID, DWORD, LPVOID, DWORD, LPDWORD, LPOVERLAPPED]
SystemParametersInfoW = _user32.SystemParametersInfoW
SystemParametersInfoW.restype = BOOL
SystemParametersInfoW.argtypes = [UINT, UINT, PVOID, UINT]
SystemParametersInfo = SystemParametersInfoW  # alias
ExitWindowsEx = _user32.ExitWindowsEx
ExitWindowsEx.restype = BOOL
ExitWindowsEx.argtypes = [UINT, DWORD]
class _LUID(Structure):
    pass
PLUID = POINTER(_LUID)
LookupPrivilegeValueW = _Advapi32.LookupPrivilegeValueW
LookupPrivilegeValueW.restype = BOOL
LookupPrivilegeValueW.argtypes = [LPCWSTR, LPCWSTR, PLUID]
LookupPrivilegeValue = LookupPrivilegeValueW  # alias
_LUID._fields_ = [
    ('LowPart', DWORD),
    ('HighPart', LONG),
]
class _TOKEN_PRIVILEGES(Structure):
    pass
PTOKEN_PRIVILEGES = POINTER(_TOKEN_PRIVILEGES)
AdjustTokenPrivileges = _Advapi32.AdjustTokenPrivileges
AdjustTokenPrivileges.restype = BOOL
AdjustTokenPrivileges.argtypes = [HANDLE, BOOL, PTOKEN_PRIVILEGES, DWORD, PTOKEN_PRIVILEGES, PDWORD]
class _LUID_AND_ATTRIBUTES(Structure):
    pass
LUID = _LUID
_LUID_AND_ATTRIBUTES._fields_ = [
    ('Luid', LUID),
    ('Attributes', DWORD),
]
LUID_AND_ATTRIBUTES = _LUID_AND_ATTRIBUTES
_TOKEN_PRIVILEGES._fields_ = [
    ('PrivilegeCount', DWORD),
    ('Privileges', LUID_AND_ATTRIBUTES * 1),
]
GetClipboardOwner = _user32.GetClipboardOwner
GetClipboardOwner.restype = HWND
GetClipboardOwner.argtypes = []
TOKEN_PRIVILEGES = _TOKEN_PRIVILEGES
SC_SCREENSAVE = 61760  # Variable c_int '61760'
SC_MONITORPOWER = 61808  # Variable c_int '61808'
TOKEN_ADJUST_PRIVILEGES = 32  # Variable c_int '32'
WSTRING = c_wchar_p
SE_SHUTDOWN_NAME = u'SeShutdownPrivilege'  # Variable WSTRING '(const wchar_t*)"S\\000e\\000S\\000h\\000u\\000t\\000d\\000o\\000w\\000n\\000P\\000r\\000i\\000v\\000i\\000l\\000e\\000g\\000e\\000\\000"'
SE_PRIVILEGE_ENABLED = 2  # Variable c_long '2l'
EWX_LOGOFF = 0  # Variable c_int '0'
SPI_SETDESKWALLPAPER = 20  # Variable c_int '20'
SPIF_SENDWININICHANGE = 2  # Variable c_int '2'
SPIF_SENDCHANGE = SPIF_SENDWININICHANGE  # alias
SPIF_UPDATEINIFILE = 1  # Variable c_int '1'
WM_DEVICECHANGE = 537  # Variable c_int '537'
class _DEV_BROADCAST_HDR(Structure):
    pass
DEV_BROADCAST_HDR = _DEV_BROADCAST_HDR
_DEV_BROADCAST_HDR._fields_ = [
    ('dbch_size', DWORD),
    ('dbch_devicetype', DWORD),
    ('dbch_reserved', DWORD),
]
class _DEV_BROADCAST_DEVICEINTERFACE_W(Structure):
    pass
DEV_BROADCAST_DEVICEINTERFACE_W = _DEV_BROADCAST_DEVICEINTERFACE_W
DEV_BROADCAST_DEVICEINTERFACE = DEV_BROADCAST_DEVICEINTERFACE_W
_DEV_BROADCAST_DEVICEINTERFACE_W._fields_ = [
    ('dbcc_size', DWORD),
    ('dbcc_devicetype', DWORD),
    ('dbcc_reserved', DWORD),
    ('dbcc_classguid', GUID),
    ('dbcc_name', c_wchar * 1),
]
class _DEV_BROADCAST_VOLUME(Structure):
    pass
DEV_BROADCAST_VOLUME = _DEV_BROADCAST_VOLUME
_DEV_BROADCAST_VOLUME._fields_ = [
    ('dbcv_size', DWORD),
    ('dbcv_devicetype', DWORD),
    ('dbcv_reserved', DWORD),
    ('dbcv_unitmask', DWORD),
    ('dbcv_flags', WORD),
]
DBT_DEVICEARRIVAL = 32768  # Variable c_int '32768'
DBT_DEVICEREMOVECOMPLETE = 32772  # Variable c_int '32772'
DBT_DEVTYP_VOLUME = 2  # Variable c_int '2'
DBT_DEVTYP_DEVICEINTERFACE = 5  # Variable c_int '5'
HDEVNOTIFY = PVOID
RegisterDeviceNotificationW = _user32.RegisterDeviceNotificationW
RegisterDeviceNotificationW.restype = HDEVNOTIFY
RegisterDeviceNotificationW.argtypes = [HANDLE, LPVOID, DWORD]
RegisterDeviceNotification = RegisterDeviceNotificationW  # alias
UnregisterDeviceNotification = _user32.UnregisterDeviceNotification
UnregisterDeviceNotification.restype = BOOL
UnregisterDeviceNotification.argtypes = [HDEVNOTIFY]
WM_POWERBROADCAST = 536  # Variable c_int '536'
PBT_APMSUSPEND = 4  # Variable c_int '4'
PBT_APMRESUMEAUTOMATIC = 18  # Variable c_int '18'
PBT_APMBATTERYLOW = 9  # Variable c_int '9'
PBT_APMOEMEVENT = 11  # Variable c_int '11'
PBT_APMPOWERSTATUSCHANGE = 10  # Variable c_int '10'
PBT_APMQUERYSUSPEND = 0  # Variable c_int '0'
PBT_APMQUERYSUSPENDFAILED = 2  # Variable c_int '2'
PBT_APMRESUMECRITICAL = 6  # Variable c_int '6'
PBT_APMRESUMESUSPEND = 7  # Variable c_int '7'
RegisterShellHookWindow = _user32.RegisterShellHookWindow
RegisterShellHookWindow.restype = BOOL
RegisterShellHookWindow.argtypes = [HWND]
DeregisterShellHookWindow = _user32.DeregisterShellHookWindow
DeregisterShellHookWindow.restype = BOOL
DeregisterShellHookWindow.argtypes = [HWND]
GetWindowLongW = _user32.GetWindowLongW
GetWindowLongW.restype = LONG
GetWindowLongW.argtypes = [HWND, c_int]
GetWindowLong = GetWindowLongW  # alias
EnumWindows = _user32.EnumWindows
EnumWindows.restype = BOOL
EnumWindows.argtypes = [WNDENUMPROC, LPARAM]
WM_APP = 32768  # Variable c_int '32768'
GWL_STYLE = -16  # Variable c_int '-0x000000010'
HSHELL_WINDOWCREATED = 1  # Variable c_int '1'
HSHELL_WINDOWDESTROYED = 2  # Variable c_int '2'
HSHELL_WINDOWACTIVATED = 4  # Variable c_int '4'
GWL_HWNDPARENT = -8  # Variable c_int '-0x000000008'
GetShellWindow = _user32.GetShellWindow
GetShellWindow.restype = HWND
GetShellWindow.argtypes = []
MoveWindow = _user32.MoveWindow
MoveWindow.restype = BOOL
MoveWindow.argtypes = [HWND, c_int, c_int, c_int, c_int, BOOL]
SW_MAXIMIZE = 3  # Variable c_int '3'
SW_MINIMIZE = 6  # Variable c_int '6'
GWL_EXSTYLE = -20  # Variable c_int '-0x000000014'
WS_EX_TOPMOST = 8  # Variable c_long '8l'
SWP_NOMOVE = 2  # Variable c_int '2'
SWP_NOSIZE = 1  # Variable c_int '1'
PM_QS_POSTMESSAGE = 9961472  # Variable c_int '9961472'

PM_NOYIELD = 2  # Variable c_int '2'
WH_KEYBOARD = 2  # Variable c_int '2'
TranslateMessage = _user32.TranslateMessage
TranslateMessage.restype = BOOL
TranslateMessage.argtypes = [POINTER(MSG)]
ReplyMessage = _user32.ReplyMessage
ReplyMessage.restype = BOOL
ReplyMessage.argtypes = [LRESULT]
InSendMessage = _user32.InSendMessage
InSendMessage.restype = BOOL
InSendMessage.argtypes = []
PM_NOREMOVE = 0  # Variable c_int '0'
GetAsyncKeyState = _user32.GetAsyncKeyState
GetAsyncKeyState.restype = SHORT
GetAsyncKeyState.argtypes = [c_int]

GetMessageTime = _user32.GetMessageTime
GetMessageTime.restype = LONG
GetMessageTime.argtypes = []

LPCTSTR = LPCWSTR
COINIT_MULTITHREADED = 0
COINIT_APARTMENTTHREADED = 2

FreeLibrary = _kernel32.FreeLibrary
FreeLibrary.restype = BOOL
FreeLibrary.argtypes = [HMODULE]

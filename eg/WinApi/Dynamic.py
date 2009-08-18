# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

#pylint: disable-msg=C0103,C0301,C0302

# This file gets automatically extended by ctypeslib.dynamic_module, so don't
# edit it yourself.

from ctypes import * #pylint: disable-msg=W0401,W0614
from ctypes.wintypes import * #pylint: disable-msg=W0401,W0614
_user32 = WinDLL("user32")
_kernel32 = WinDLL("kernel32")
_ole32 = WinDLL("ole32")
_gdi32 = WinDLL("Gdi32")
_winmm = WinDLL("Winmm")
_shell32 = WinDLL("shell32")
_Psapi = WinDLL("Psapi")
_Advapi32 = WinDLL("Advapi32")
_setupapi = WinDLL("setupapi")
_htmlhelp = WinDLL("hhctrl.ocx")
import sys
if not hasattr(sys, "frozen"): # detect py2exe
    try:
        ctypeslib = __import__("ctypeslib.dynamic_module")
    except ImportError :
        print "ctypeslib is not installed!"
    else:
        try:
            ctypeslib.dynamic_module.include(
                "#define UNICODE\n"
                "#define _WIN32_WINNT 0x500\n"
                "#define WIN32_LEAN_AND_MEAN\n"
                "#define NO_STRICT\n"
                "#include <windows.h>\n"
                "#include <Dbt.h>\n"
                "#include <objbase.h>\n"
                "#include <Mmsystem.h>\n"
                "#include <shlobj.h>\n"
                "#include <Psapi.h>\n"
                "#include <tlhelp32.h>\n"
                "#include <objidl.h>\n"
                "#include <setupapi.h>\n"
                "#include <htmlhelp.h>\n"
                "#include <shellapi.h>\n"
            )
        except WindowsError:
            print "GCC_XML most likely not installed"
INVALID_HANDLE_VALUE = -1
HWND_TOPMOST = -1
HWND_NOTOPMOST = -2
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
SendNotifyMessage = SendNotifyMessageW # alias
LPRECT = POINTER(tagRECT)
GetWindowRect = _user32.GetWindowRect
GetWindowRect.restype = BOOL
GetWindowRect.argtypes = [HWND, LPRECT]
LPPOINT = POINTER(tagPOINT)
GetCursorPos = _user32.GetCursorPos
GetCursorPos.restype = BOOL
GetCursorPos.argtypes = [LPPOINT]
EnumProcesses = _Psapi.EnumProcesses
EnumProcesses.restype = BOOL
EnumProcesses.argtypes = [POINTER(DWORD), DWORD, LPDWORD]
LPCRECT = POINTER(RECT)
MONITORENUMPROC = WINFUNCTYPE(BOOL, HMONITOR, HDC, LPRECT, LPARAM)
EnumDisplayMonitors = _user32.EnumDisplayMonitors
EnumDisplayMonitors.restype = BOOL
EnumDisplayMonitors.argtypes = [HDC, LPCRECT, MONITORENUMPROC, LPARAM]
FindWindowW = _user32.FindWindowW
FindWindowW.restype = HWND
FindWindowW.argtypes = [LPCWSTR, LPCWSTR]
FindWindow = FindWindowW # alias
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
GetClassLong = GetClassLongW # alias
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
SendMessageTimeout = SendMessageTimeoutW # alias
ScreenToClient = _user32.ScreenToClient
ScreenToClient.restype = BOOL
ScreenToClient.argtypes = [HWND, LPPOINT]
WindowFromPoint = _user32.WindowFromPoint
WindowFromPoint.restype = HWND
WindowFromPoint.argtypes = [POINT]
WM_GETICON = 127 # Variable c_int '127'
ICON_SMALL = 0 # Variable c_int '0'
ICON_BIG = 1 # Variable c_int '1'
SMTO_ABORTIFHUNG = 2 # Variable c_int '2'
GCL_HICONSM = -34 # Variable c_int '-0x000000022'
GCL_HICON = -14 # Variable c_int '-0x00000000e'
R2_NOT = 6 # Variable c_int '6'
PS_INSIDEFRAME = 6 # Variable c_int '6'
SM_CXBORDER = 5 # Variable c_int '5'
NULL_BRUSH = 5 # Variable c_int '5'
GA_ROOT = 2 # Variable c_int '2'
SW_RESTORE = 9 # Variable c_int '9'
WM_SYSCOMMAND = 274 # Variable c_int '274'
SC_CLOSE = 61536 # Variable c_int '61536'
SW_SHOWNA = 8 # Variable c_int '8'
SMTO_BLOCK = 1 # Variable c_int '1'
WM_COMMAND = 273 # Variable c_int '273'
WM_USER = 1024 # Variable c_int '1024'
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
LPVOID = c_void_p
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
CF_TEXT = 1 # Variable c_int '1'
CF_UNICODETEXT = 13 # Variable c_int '13'
GHND = 66 # Variable c_int '66'
GetCurrentProcessId = _kernel32.GetCurrentProcessId
GetCurrentProcessId.restype = DWORD
GetCurrentProcessId.argtypes = []
WM_SIZE = 5 # Variable c_int '5'
CW_USEDEFAULT = -2147483648 # Variable c_int '-0x080000000'
WS_OVERLAPPEDWINDOW = 13565952 # Variable c_long '13565952l'
GetModuleHandleW = _kernel32.GetModuleHandleW
GetModuleHandleW.restype = HMODULE
GetModuleHandleW.argtypes = [LPCWSTR]
GetModuleHandle = GetModuleHandleW # alias
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
RegisterClass = RegisterClassW # alias
CreateWindowExW = _user32.CreateWindowExW
CreateWindowExW.restype = HWND
CreateWindowExW.argtypes = [DWORD, LPCWSTR, LPCWSTR, DWORD, c_int, c_int, c_int, c_int, HWND, HMENU, HINSTANCE, LPVOID]
CreateWindowEx = CreateWindowExW # alias
DefWindowProcW = _user32.DefWindowProcW
DefWindowProcW.restype = LRESULT
DefWindowProcW.argtypes = [HWND, UINT, WPARAM, LPARAM]
DefWindowProc = DefWindowProcW # alias
SetClipboardViewer = _user32.SetClipboardViewer
SetClipboardViewer.restype = HWND
SetClipboardViewer.argtypes = [HWND]
ChangeClipboardChain = _user32.ChangeClipboardChain
ChangeClipboardChain.restype = BOOL
ChangeClipboardChain.argtypes = [HWND, HWND]
WM_CHANGECBCHAIN = 781 # Variable c_int '781'
WM_DRAWCLIPBOARD = 776 # Variable c_int '776'
SendMessageW = _user32.SendMessageW
SendMessageW.restype = LRESULT
SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendMessage = SendMessageW # alias
class _SECURITY_ATTRIBUTES(Structure):
    pass
LPSECURITY_ATTRIBUTES = POINTER(_SECURITY_ATTRIBUTES)
CreateEventW = _kernel32.CreateEventW
CreateEventW.restype = HANDLE
CreateEventW.argtypes = [LPSECURITY_ATTRIBUTES, BOOL, BOOL, LPCWSTR]
CreateEvent = CreateEventW # alias
_SECURITY_ATTRIBUTES._fields_ = [
    ('nLength', DWORD),
    ('lpSecurityDescriptor', LPVOID),
    ('bInheritHandle', BOOL),
]
SetEvent = _kernel32.SetEvent
SetEvent.restype = BOOL
SetEvent.argtypes = [HANDLE]
WAIT_OBJECT_0 = 0L # Variable c_ulong '0ul'
WAIT_TIMEOUT = 258 # Variable c_long '258l'
QS_ALLINPUT = 255 # Variable c_int '255'
MsgWaitForMultipleObjects = _user32.MsgWaitForMultipleObjects
MsgWaitForMultipleObjects.restype = DWORD
MsgWaitForMultipleObjects.argtypes = [DWORD, POINTER(HANDLE), BOOL, DWORD, DWORD]
CoInitialize = _ole32.CoInitialize
CoInitialize.restype = HRESULT
CoInitialize.argtypes = [LPVOID]
CoUninitialize = _ole32.CoUninitialize
CoUninitialize.restype = None
CoUninitialize.argtypes = []
LPMSG = POINTER(tagMSG)
PeekMessageW = _user32.PeekMessageW
PeekMessageW.restype = BOOL
PeekMessageW.argtypes = [LPMSG, HWND, UINT, UINT, UINT]
PeekMessage = PeekMessageW # alias
DispatchMessageW = _user32.DispatchMessageW
DispatchMessageW.restype = LRESULT
DispatchMessageW.argtypes = [POINTER(MSG)]
DispatchMessage = DispatchMessageW # alias
PM_REMOVE = 1 # Variable c_int '1'
WM_QUIT = 18 # Variable c_int '18'
WM_QUERYENDSESSION = 17 # Variable c_int '17'
WM_ENDSESSION = 22 # Variable c_int '22'
SetProcessShutdownParameters = _kernel32.SetProcessShutdownParameters
SetProcessShutdownParameters.restype = BOOL
SetProcessShutdownParameters.argtypes = [DWORD, DWORD]
ExitProcess = _kernel32.ExitProcess
ExitProcess.restype = None
ExitProcess.argtypes = [UINT]
GetSysColor = _user32.GetSysColor
GetSysColor.restype = DWORD
GetSysColor.argtypes = [c_int]
COLOR_ACTIVECAPTION = 2 # Variable c_int '2'
COLOR_GRADIENTACTIVECAPTION = 27 # Variable c_int '27'
COLOR_CAPTIONTEXT = 9 # Variable c_int '9'
COLOR_INACTIVECAPTION = 3 # Variable c_int '3'
COLOR_GRADIENTINACTIVECAPTION = 28 # Variable c_int '28'
COLOR_INACTIVECAPTIONTEXT = 19 # Variable c_int '19'
GetTickCount = _kernel32.GetTickCount
GetTickCount.restype = DWORD
GetTickCount.argtypes = []
OpenProcess = _kernel32.OpenProcess
OpenProcess.restype = HANDLE
OpenProcess.argtypes = [DWORD, BOOL, DWORD]
PROCESS_SET_QUOTA = 256 # Variable c_int '256'
SetProcessWorkingSetSize = _kernel32.SetProcessWorkingSetSize
SetProcessWorkingSetSize.restype = BOOL
SetProcessWorkingSetSize.argtypes = [HANDLE, SIZE_T, SIZE_T]
class tagINPUT(Structure):
    pass
LPINPUT = POINTER(tagINPUT)
SendInput = _user32.SendInput
SendInput.restype = UINT
SendInput.argtypes = [UINT, LPINPUT, c_int]
class N8tagINPUT5DOLLAR_102E(Union):
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
N8tagINPUT5DOLLAR_102E._fields_ = [
    ('mi', MOUSEINPUT),
    ('ki', KEYBDINPUT),
    ('hi', HARDWAREINPUT),
]
tagINPUT._anonymous_ = ['_0']
tagINPUT._fields_ = [
    ('type', DWORD),
    ('_0', N8tagINPUT5DOLLAR_102E),
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
INPUT_KEYBOARD = 1 # Variable c_int '1'
KEYEVENTF_KEYUP = 2 # Variable c_int '2'
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
PROCESS_QUERY_INFORMATION = 1024 # Variable c_int '1024'
VK_SHIFT = 16 # Variable c_int '16'
VK_LSHIFT = 160 # Variable c_int '160'
VK_CONTROL = 17 # Variable c_int '17'
VK_LCONTROL = 162 # Variable c_int '162'
VK_MENU = 18 # Variable c_int '18'
WM_TIMER = 275 # Variable c_int '275'
WM_SYSKEYDOWN = 260 # Variable c_int '260'
WM_KEYDOWN = 256 # Variable c_int '256'
WM_SYSKEYUP = 261 # Variable c_int '261'
WM_KEYUP = 257 # Variable c_int '257'
SHORT = c_short
VkKeyScanW = _user32.VkKeyScanW
VkKeyScanW.restype = SHORT
VkKeyScanW.argtypes = [WCHAR]
MapVirtualKeyW = _user32.MapVirtualKeyW
MapVirtualKeyW.restype = UINT
MapVirtualKeyW.argtypes = [UINT, UINT]
MapVirtualKey = MapVirtualKeyW # alias
GetMessageW = _user32.GetMessageW
GetMessageW.restype = BOOL
GetMessageW.argtypes = [LPMSG, HWND, UINT, UINT]
GetMessage = GetMessageW # alias
PostMessageW = _user32.PostMessageW
PostMessageW.restype = BOOL
PostMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
PostMessage = PostMessageW # alias
GetFocus = _user32.GetFocus
GetFocus.restype = HWND
GetFocus.argtypes = []
DWORD_PTR = ULONG_PTR
HtmlHelpW = _htmlhelp.HtmlHelpW
HtmlHelpW.restype = HWND
HtmlHelpW.argtypes = [HWND, LPCWSTR, UINT, DWORD_PTR]
HtmlHelp = HtmlHelpW # alias
HH_DISPLAY_TOPIC = 0 # Variable c_int '0'
GetDesktopWindow = _user32.GetDesktopWindow
GetDesktopWindow.restype = HWND
GetDesktopWindow.argtypes = []
GetDriveTypeW = _kernel32.GetDriveTypeW
GetDriveTypeW.restype = UINT
GetDriveTypeW.argtypes = [LPCWSTR]
GetDriveType = GetDriveTypeW # alias
EXECUTION_STATE = DWORD
SetThreadExecutionState = _kernel32.SetThreadExecutionState
SetThreadExecutionState.restype = EXECUTION_STATE
SetThreadExecutionState.argtypes = [EXECUTION_STATE]
GetCurrentProcess = _kernel32.GetCurrentProcess
GetCurrentProcess.restype = HANDLE
GetCurrentProcess.argtypes = []
InitiateSystemShutdownW = _Advapi32.InitiateSystemShutdownW
InitiateSystemShutdownW.restype = BOOL
InitiateSystemShutdownW.argtypes = [LPWSTR, LPWSTR, DWORD, BOOL, BOOL]
InitiateSystemShutdown = InitiateSystemShutdownW # alias
CreateFileW = _kernel32.CreateFileW
CreateFileW.restype = HANDLE
CreateFileW.argtypes = [LPCWSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE]
CreateFile = CreateFileW # alias
class _OVERLAPPED(Structure):
    pass
LPOVERLAPPED = POINTER(_OVERLAPPED)
DeviceIoControl = _kernel32.DeviceIoControl
DeviceIoControl.restype = BOOL
DeviceIoControl.argtypes = [HANDLE, DWORD, LPVOID, DWORD, LPVOID, DWORD, LPDWORD, LPOVERLAPPED]
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
SystemParametersInfoW = _user32.SystemParametersInfoW
SystemParametersInfoW.restype = BOOL
SystemParametersInfoW.argtypes = [UINT, UINT, PVOID, UINT]
SystemParametersInfo = SystemParametersInfoW # alias
ExitWindowsEx = _user32.ExitWindowsEx
ExitWindowsEx.restype = BOOL
ExitWindowsEx.argtypes = [UINT, DWORD]
PHANDLE = POINTER(HANDLE)
OpenProcessToken = _Advapi32.OpenProcessToken
OpenProcessToken.restype = BOOL
OpenProcessToken.argtypes = [HANDLE, DWORD, PHANDLE]
class _LUID(Structure):
    pass
PLUID = POINTER(_LUID)
LookupPrivilegeValueW = _Advapi32.LookupPrivilegeValueW
LookupPrivilegeValueW.restype = BOOL
LookupPrivilegeValueW.argtypes = [LPCWSTR, LPCWSTR, PLUID]
LookupPrivilegeValue = LookupPrivilegeValueW # alias
_LUID._fields_ = [
    ('LowPart', DWORD),
    ('HighPart', LONG),
]
class _TOKEN_PRIVILEGES(Structure):
    pass
PTOKEN_PRIVILEGES = POINTER(_TOKEN_PRIVILEGES)
PDWORD = POINTER(DWORD)
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
GENERIC_READ = 2147483648L # Variable c_ulong '-2147483648ul'
FILE_SHARE_READ = 1 # Variable c_int '1'
OPEN_EXISTING = 3 # Variable c_int '3'
SC_SCREENSAVE = 61760 # Variable c_int '61760'
SC_MONITORPOWER = 61808 # Variable c_int '61808'
TOKEN_ADJUST_PRIVILEGES = 32 # Variable c_int '32'
TOKEN_QUERY = 8 # Variable c_int '8'
WSTRING = c_wchar_p
SE_SHUTDOWN_NAME = u'SeShutdownPrivilege' # Variable WSTRING '(const wchar_t*)"S\\000e\\000S\\000h\\000u\\000t\\000d\\000o\\000w\\000n\\000P\\000r\\000i\\000v\\000i\\000l\\000e\\000g\\000e\\000\\000"'
SE_PRIVILEGE_ENABLED = 2 # Variable c_long '2l'
EWX_LOGOFF = 0 # Variable c_int '0'
SPI_SETDESKWALLPAPER = 20 # Variable c_int '20'
SPIF_SENDWININICHANGE = 2 # Variable c_int '2'
SPIF_SENDCHANGE = SPIF_SENDWININICHANGE # alias
SPIF_UPDATEINIFILE = 1 # Variable c_int '1'
HMIXER = HANDLE
class tagMIXERCAPSW(Structure):
    pass
MIXERCAPSW = tagMIXERCAPSW
MIXERCAPS = MIXERCAPSW
MMVERSION = UINT
tagMIXERCAPSW._pack_ = 1
tagMIXERCAPSW._fields_ = [
    ('wMid', WORD),
    ('wPid', WORD),
    ('vDriverVersion', MMVERSION),
    ('szPname', WCHAR * 32),
    ('fdwSupport', DWORD),
    ('cDestinations', DWORD),
]
class tagMIXERCONTROLW(Structure):
    pass
MIXERCONTROLW = tagMIXERCONTROLW
MIXERCONTROL = MIXERCONTROLW
class N16tagMIXERCONTROLW5DOLLAR_158E(Union):
    pass
class N16tagMIXERCONTROLW5DOLLAR_1585DOLLAR_159E(Structure):
    pass
N16tagMIXERCONTROLW5DOLLAR_1585DOLLAR_159E._pack_ = 1
N16tagMIXERCONTROLW5DOLLAR_1585DOLLAR_159E._fields_ = [
    ('lMinimum', LONG),
    ('lMaximum', LONG),
]
class N16tagMIXERCONTROLW5DOLLAR_1585DOLLAR_160E(Structure):
    pass
N16tagMIXERCONTROLW5DOLLAR_1585DOLLAR_160E._pack_ = 1
N16tagMIXERCONTROLW5DOLLAR_1585DOLLAR_160E._fields_ = [
    ('dwMinimum', DWORD),
    ('dwMaximum', DWORD),
]
N16tagMIXERCONTROLW5DOLLAR_158E._pack_ = 1
N16tagMIXERCONTROLW5DOLLAR_158E._anonymous_ = ['_0', '_1']
N16tagMIXERCONTROLW5DOLLAR_158E._fields_ = [
    ('_0', N16tagMIXERCONTROLW5DOLLAR_1585DOLLAR_159E),
    ('_1', N16tagMIXERCONTROLW5DOLLAR_1585DOLLAR_160E),
    ('dwReserved', DWORD * 6),
]
class N16tagMIXERCONTROLW5DOLLAR_161E(Union):
    pass
N16tagMIXERCONTROLW5DOLLAR_161E._pack_ = 1
N16tagMIXERCONTROLW5DOLLAR_161E._fields_ = [
    ('cSteps', DWORD),
    ('cbCustomData', DWORD),
    ('dwReserved', DWORD * 6),
]
tagMIXERCONTROLW._pack_ = 1
tagMIXERCONTROLW._fields_ = [
    ('cbStruct', DWORD),
    ('dwControlID', DWORD),
    ('dwControlType', DWORD),
    ('fdwControl', DWORD),
    ('cMultipleItems', DWORD),
    ('szShortName', WCHAR * 16),
    ('szName', WCHAR * 64),
    ('Bounds', N16tagMIXERCONTROLW5DOLLAR_158E),
    ('Metrics', N16tagMIXERCONTROLW5DOLLAR_161E),
]
class tagMIXERLINECONTROLSW(Structure):
    pass
MIXERLINECONTROLSW = tagMIXERLINECONTROLSW
MIXERLINECONTROLS = MIXERLINECONTROLSW
class N21tagMIXERLINECONTROLSW5DOLLAR_163E(Union):
    pass
N21tagMIXERLINECONTROLSW5DOLLAR_163E._pack_ = 1
N21tagMIXERLINECONTROLSW5DOLLAR_163E._fields_ = [
    ('dwControlID', DWORD),
    ('dwControlType', DWORD),
]
LPMIXERCONTROLW = POINTER(tagMIXERCONTROLW)
tagMIXERLINECONTROLSW._pack_ = 1
tagMIXERLINECONTROLSW._anonymous_ = ['_0']
tagMIXERLINECONTROLSW._fields_ = [
    ('cbStruct', DWORD),
    ('dwLineID', DWORD),
    ('_0', N21tagMIXERLINECONTROLSW5DOLLAR_163E),
    ('cControls', DWORD),
    ('cbmxctrl', DWORD),
    ('pamxctrl', LPMIXERCONTROLW),
]
class tagMIXERLINEW(Structure):
    pass
MIXERLINEW = tagMIXERLINEW
MIXERLINE = MIXERLINEW
class N13tagMIXERLINEW5DOLLAR_153E(Structure):
    pass
N13tagMIXERLINEW5DOLLAR_153E._pack_ = 1
N13tagMIXERLINEW5DOLLAR_153E._fields_ = [
    ('dwType', DWORD),
    ('dwDeviceID', DWORD),
    ('wMid', WORD),
    ('wPid', WORD),
    ('vDriverVersion', MMVERSION),
    ('szPname', WCHAR * 32),
]
tagMIXERLINEW._pack_ = 1
tagMIXERLINEW._fields_ = [
    ('cbStruct', DWORD),
    ('dwDestination', DWORD),
    ('dwSource', DWORD),
    ('dwLineID', DWORD),
    ('fdwLine', DWORD),
    ('dwUser', DWORD_PTR),
    ('dwComponentType', DWORD),
    ('cChannels', DWORD),
    ('cConnections', DWORD),
    ('cControls', DWORD),
    ('szShortName', WCHAR * 16),
    ('szName', WCHAR * 64),
    ('Target', N13tagMIXERLINEW5DOLLAR_153E),
]
class tMIXERCONTROLDETAILS(Structure):
    pass
MIXERCONTROLDETAILS = tMIXERCONTROLDETAILS
class N20tMIXERCONTROLDETAILS5DOLLAR_164E(Union):
    pass
N20tMIXERCONTROLDETAILS5DOLLAR_164E._pack_ = 1
N20tMIXERCONTROLDETAILS5DOLLAR_164E._fields_ = [
    ('hwndOwner', HWND),
    ('cMultipleItems', DWORD),
]
tMIXERCONTROLDETAILS._pack_ = 1
tMIXERCONTROLDETAILS._anonymous_ = ['_0']
tMIXERCONTROLDETAILS._fields_ = [
    ('cbStruct', DWORD),
    ('dwControlID', DWORD),
    ('cChannels', DWORD),
    ('_0', N20tMIXERCONTROLDETAILS5DOLLAR_164E),
    ('cbDetails', DWORD),
    ('paDetails', LPVOID),
]
class tMIXERCONTROLDETAILS_UNSIGNED(Structure):
    pass
MIXERCONTROLDETAILS_UNSIGNED = tMIXERCONTROLDETAILS_UNSIGNED
tMIXERCONTROLDETAILS_UNSIGNED._pack_ = 1
tMIXERCONTROLDETAILS_UNSIGNED._fields_ = [
    ('dwValue', DWORD),
]
MMRESULT = UINT
LPHMIXER = POINTER(HMIXER)
mixerOpen = _winmm.mixerOpen
mixerOpen.restype = MMRESULT
mixerOpen.argtypes = [LPHMIXER, UINT, DWORD_PTR, DWORD_PTR, DWORD]
mixerGetNumDevs = _winmm.mixerGetNumDevs
mixerGetNumDevs.restype = UINT
mixerGetNumDevs.argtypes = []
LPMIXERCAPSW = POINTER(tagMIXERCAPSW)
mixerGetDevCapsW = _winmm.mixerGetDevCapsW
mixerGetDevCapsW.restype = MMRESULT
mixerGetDevCapsW.argtypes = [UINT_PTR, LPMIXERCAPSW, UINT]
mixerGetDevCaps = mixerGetDevCapsW # alias
HMIXEROBJ = HANDLE
LPMIXERCONTROLDETAILS = POINTER(tMIXERCONTROLDETAILS)
mixerGetControlDetailsW = _winmm.mixerGetControlDetailsW
mixerGetControlDetailsW.restype = MMRESULT
mixerGetControlDetailsW.argtypes = [HMIXEROBJ, LPMIXERCONTROLDETAILS, DWORD]
mixerGetControlDetails = mixerGetControlDetailsW # alias
LPMIXERLINEW = POINTER(tagMIXERLINEW)
mixerGetLineInfoW = _winmm.mixerGetLineInfoW
mixerGetLineInfoW.restype = MMRESULT
mixerGetLineInfoW.argtypes = [HMIXEROBJ, LPMIXERLINEW, DWORD]
mixerGetLineInfo = mixerGetLineInfoW # alias
LPMIXERLINECONTROLSW = POINTER(tagMIXERLINECONTROLSW)
mixerGetLineControlsW = _winmm.mixerGetLineControlsW
mixerGetLineControlsW.restype = MMRESULT
mixerGetLineControlsW.argtypes = [HMIXEROBJ, LPMIXERLINECONTROLSW, DWORD]
mixerGetLineControls = mixerGetLineControlsW # alias
mixerSetControlDetails = _winmm.mixerSetControlDetails
mixerSetControlDetails.restype = MMRESULT
mixerSetControlDetails.argtypes = [HMIXEROBJ, LPMIXERCONTROLDETAILS, DWORD]
MIXERLINE_COMPONENTTYPE_DST_SPEAKERS = 4 # Variable c_long '4l'
MIXERCONTROL_CONTROLTYPE_MUTE = 536936450 # Variable c_long '536936450l'
MIXERCONTROL_CONTROLTYPE_VOLUME = 1342373889 # Variable c_long '1342373889l'
MIXER_GETLINEINFOF_COMPONENTTYPE = 3 # Variable c_long '3l'
MIXER_GETLINECONTROLSF_ONEBYTYPE = 2 # Variable c_long '2l'
MIXER_GETLINECONTROLSF_ALL = 0 # Variable c_long '0l'
MIXER_GETLINEINFOF_DESTINATION = 0 # Variable c_long '0l'
MIXER_GETLINEINFOF_SOURCE = 1 # Variable c_long '1l'
MMSYSERR_NOERROR = 0 # Variable c_int '0'
MIXERCONTROL_CT_CLASS_MASK = 4026531840L # Variable c_ulong '-268435456ul'
MIXERCONTROL_CT_CLASS_FADER = 1342177280 # Variable c_long '1342177280l'
MIXERCONTROL_CONTROLTYPE_BASS = 1342373890 # Variable c_long '1342373890l'
MIXERCONTROL_CONTROLTYPE_TREBLE = 1342373891 # Variable c_long '1342373891l'
MIXERCONTROL_CONTROLTYPE_EQUALIZER = 1342373892 # Variable c_long '1342373892l'
MIXERCONTROL_CONTROLTYPE_FADER = 1342373888 # Variable c_long '1342373888l'
MIXERCONTROL_CT_CLASS_LIST = 1879048192 # Variable c_long '1879048192l'
MIXERCONTROL_CONTROLTYPE_SINGLESELECT = 1879113728 # Variable c_long '1879113728l'
MIXERCONTROL_CONTROLTYPE_MULTIPLESELECT = 1895890944 # Variable c_long '1895890944l'
MIXERCONTROL_CONTROLTYPE_MUX = 1879113729 # Variable c_long '1879113729l'
MIXERCONTROL_CONTROLTYPE_MIXER = 1895890945 # Variable c_long '1895890945l'
MIXERCONTROL_CT_CLASS_METER = 268435456 # Variable c_long '268435456l'
MIXERCONTROL_CONTROLTYPE_BOOLEANMETER = 268500992 # Variable c_long '268500992l'
MIXERCONTROL_CONTROLTYPE_PEAKMETER = 268566529 # Variable c_long '268566529l'
MIXERCONTROL_CONTROLTYPE_SIGNEDMETER = 268566528 # Variable c_long '268566528l'
MIXERCONTROL_CONTROLTYPE_UNSIGNEDMETER = 268632064 # Variable c_long '268632064l'
MIXERCONTROL_CT_CLASS_NUMBER = 805306368 # Variable c_long '805306368l'
MIXERCONTROL_CONTROLTYPE_SIGNED = 805437440 # Variable c_long '805437440l'
MIXERCONTROL_CONTROLTYPE_UNSIGNED = 805502976 # Variable c_long '805502976l'
MIXERCONTROL_CONTROLTYPE_PERCENT = 805634048 # Variable c_long '805634048l'
MIXERCONTROL_CONTROLTYPE_DECIBELS = 805568512 # Variable c_long '805568512l'
MIXERCONTROL_CT_CLASS_SLIDER = 1073741824 # Variable c_long '1073741824l'
MIXERCONTROL_CONTROLTYPE_SLIDER = 1073872896 # Variable c_long '1073872896l'
MIXERCONTROL_CONTROLTYPE_PAN = 1073872897 # Variable c_long '1073872897l'
MIXERCONTROL_CONTROLTYPE_QSOUNDPAN = 1073872898 # Variable c_long '1073872898l'
MIXERCONTROL_CT_CLASS_SWITCH = 536870912 # Variable c_long '536870912l'
MIXERCONTROL_CONTROLTYPE_BOOLEAN = 536936448 # Variable c_long '536936448l'
MIXERCONTROL_CONTROLTYPE_BUTTON = 553713664 # Variable c_long '553713664l'
MIXERCONTROL_CONTROLTYPE_LOUDNESS = 536936452 # Variable c_long '536936452l'
MIXERCONTROL_CONTROLTYPE_MONO = 536936451 # Variable c_long '536936451l'
MIXERCONTROL_CONTROLTYPE_ONOFF = 536936449 # Variable c_long '536936449l'
MIXERCONTROL_CONTROLTYPE_STEREOENH = 536936453 # Variable c_long '536936453l'
MIXERCONTROL_CT_CLASS_TIME = 1610612736 # Variable c_long '1610612736l'
MIXERCONTROL_CONTROLTYPE_MICROTIME = 1610809344 # Variable c_long '1610809344l'
MIXERCONTROL_CONTROLTYPE_MILLITIME = 1627586560 # Variable c_long '1627586560l'
MIXERCONTROL_CT_CLASS_CUSTOM = 0 # Variable c_long '0l'
MIXERCONTROL_CONTROLF_DISABLED = 2147483648L # Variable c_ulong '-2147483648ul'
MIXERCONTROL_CONTROLF_MULTIPLE = 2 # Variable c_long '2l'
MIXERCONTROL_CONTROLF_UNIFORM = 1 # Variable c_long '1l'
ENUM_CURRENT_SETTINGS = 4294967295L # Variable c_ulong '-1u'
EDS_RAWMODE = 2 # Variable c_int '2'
class _DISPLAY_DEVICEW(Structure):
    pass
PDISPLAY_DEVICEW = POINTER(_DISPLAY_DEVICEW)
EnumDisplayDevicesW = _user32.EnumDisplayDevicesW
EnumDisplayDevicesW.restype = BOOL
EnumDisplayDevicesW.argtypes = [LPCWSTR, DWORD, PDISPLAY_DEVICEW, DWORD]
EnumDisplayDevices = EnumDisplayDevicesW # alias
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
EnumDisplaySettingsEx = EnumDisplaySettingsExW # alias
class N12_devicemodeW4DOLLAR_95E(Union):
    pass
class N12_devicemodeW4DOLLAR_954DOLLAR_96E(Structure):
    pass
N12_devicemodeW4DOLLAR_954DOLLAR_96E._fields_ = [
    ('dmOrientation', c_short),
    ('dmPaperSize', c_short),
    ('dmPaperLength', c_short),
    ('dmPaperWidth', c_short),
]
N12_devicemodeW4DOLLAR_95E._anonymous_ = ['_0']
N12_devicemodeW4DOLLAR_95E._fields_ = [
    ('_0', N12_devicemodeW4DOLLAR_954DOLLAR_96E),
    ('dmPosition', POINTL),
]
class N12_devicemodeW4DOLLAR_97E(Union):
    pass
N12_devicemodeW4DOLLAR_97E._fields_ = [
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
    ('_0', N12_devicemodeW4DOLLAR_95E),
    ('dmScale', c_short),
    ('dmCopies', c_short),
    ('dmDefaultSource', c_short),
    ('dmPrintQuality', c_short),
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
    ('_1', N12_devicemodeW4DOLLAR_97E),
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
ChangeDisplaySettingsEx = ChangeDisplaySettingsExW # alias
DISPLAY_DEVICEW = _DISPLAY_DEVICEW
DISPLAY_DEVICE = DISPLAY_DEVICEW
DEVMODEW = _devicemodeW
DEVMODE = DEVMODEW
DISPLAY_DEVICE_MIRRORING_DRIVER = 8 # Variable c_int '8'
DISPLAY_DEVICE_PRIMARY_DEVICE = 4 # Variable c_int '4'
DISPLAY_DEVICE_ATTACHED_TO_DESKTOP = 1 # Variable c_int '1'
DM_POSITION = 32 # Variable c_long '32l'
DM_BITSPERPEL = 262144 # Variable c_long '262144l'
DM_PELSWIDTH = 524288 # Variable c_long '524288l'
DM_PELSHEIGHT = 1048576 # Variable c_long '1048576l'
DM_DISPLAYFLAGS = 2097152 # Variable c_long '2097152l'
DM_DISPLAYFREQUENCY = 4194304 # Variable c_long '4194304l'
CDS_UPDATEREGISTRY = 1 # Variable c_int '1'
CDS_NORESET = 268435456 # Variable c_int '268435456'
CDS_SET_PRIMARY = 16 # Variable c_int '16'
class _STARTUPINFOW(Structure):
    pass
LPSTARTUPINFOW = POINTER(_STARTUPINFOW)
class _PROCESS_INFORMATION(Structure):
    pass
LPPROCESS_INFORMATION = POINTER(_PROCESS_INFORMATION)
CreateProcessW = _kernel32.CreateProcessW
CreateProcessW.restype = BOOL
CreateProcessW.argtypes = [LPCWSTR, LPWSTR, LPSECURITY_ATTRIBUTES, LPSECURITY_ATTRIBUTES, BOOL, DWORD, LPVOID, LPCWSTR, LPSTARTUPINFOW, LPPROCESS_INFORMATION]
CreateProcess = CreateProcessW # alias
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
WaitForSingleObject = _kernel32.WaitForSingleObject
WaitForSingleObject.restype = DWORD
WaitForSingleObject.argtypes = [HANDLE, DWORD]
STARTUPINFOW = _STARTUPINFOW
STARTUPINFO = STARTUPINFOW
PROCESS_INFORMATION = _PROCESS_INFORMATION
CREATE_NEW_CONSOLE = 16 # Variable c_int '16'
STARTF_USESHOWWINDOW = 1 # Variable c_int '1'
INFINITE = 4294967295L # Variable c_uint '-1u'
WM_DEVICECHANGE = 537 # Variable c_int '537'
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
class _GUID(Structure):
    pass
_GUID._fields_ = [
    ('Data1', c_ulong),
    ('Data2', c_ushort),
    ('Data3', c_ushort),
    ('Data4', c_ubyte * 8),
]
GUID = _GUID
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
DBT_DEVICEARRIVAL = 32768 # Variable c_int '32768'
DBT_DEVICEREMOVECOMPLETE = 32772 # Variable c_int '32772'
DBT_DEVTYP_VOLUME = 2 # Variable c_int '2'
DBT_DEVTYP_DEVICEINTERFACE = 5 # Variable c_int '5'
CLSID = GUID
LPCLSID = POINTER(CLSID)
CLSIDFromString = _ole32.CLSIDFromString
CLSIDFromString.restype = HRESULT
CLSIDFromString.argtypes = [LPOLESTR, LPCLSID]
HDEVNOTIFY = PVOID
RegisterDeviceNotificationW = _user32.RegisterDeviceNotificationW
RegisterDeviceNotificationW.restype = HDEVNOTIFY
RegisterDeviceNotificationW.argtypes = [HANDLE, LPVOID, DWORD]
RegisterDeviceNotification = RegisterDeviceNotificationW # alias
UnregisterDeviceNotification = _user32.UnregisterDeviceNotification
UnregisterDeviceNotification.restype = BOOL
UnregisterDeviceNotification.argtypes = [HDEVNOTIFY]
WM_POWERBROADCAST = 536 # Variable c_int '536'
PBT_APMSUSPEND = 4 # Variable c_int '4'
PBT_APMRESUMEAUTOMATIC = 18 # Variable c_int '18'
PBT_APMBATTERYLOW = 9 # Variable c_int '9'
PBT_APMOEMEVENT = 11 # Variable c_int '11'
PBT_APMPOWERSTATUSCHANGE = 10 # Variable c_int '10'
PBT_APMQUERYSUSPEND = 0 # Variable c_int '0'
PBT_APMQUERYSUSPENDFAILED = 2 # Variable c_int '2'
PBT_APMRESUMECRITICAL = 6 # Variable c_int '6'
PBT_APMRESUMESUSPEND = 7 # Variable c_int '7'
GetWindowLongW = _user32.GetWindowLongW
GetWindowLongW.restype = LONG
GetWindowLongW.argtypes = [HWND, c_int]
GetWindowLong = GetWindowLongW # alias
MoveWindow = _user32.MoveWindow
MoveWindow.restype = BOOL
MoveWindow.argtypes = [HWND, c_int, c_int, c_int, c_int, BOOL]
SetWindowPos = _user32.SetWindowPos
SetWindowPos.restype = BOOL
SetWindowPos.argtypes = [HWND, HWND, c_int, c_int, c_int, c_int, UINT]
SW_MAXIMIZE = 3 # Variable c_int '3'
SW_MINIMIZE = 6 # Variable c_int '6'
GWL_EXSTYLE = -20 # Variable c_int '-0x000000014'
WS_EX_TOPMOST = 8 # Variable c_long '8l'
SWP_NOMOVE = 2 # Variable c_int '2'
SWP_NOSIZE = 1 # Variable c_int '1'
mouse_event = _user32.mouse_event
mouse_event.restype = None
mouse_event.argtypes = [DWORD, DWORD, DWORD, DWORD, ULONG_PTR]
SetCursorPos = _user32.SetCursorPos
SetCursorPos.restype = BOOL
SetCursorPos.argtypes = [c_int, c_int]
RegisterWindowMessageW = _user32.RegisterWindowMessageW
RegisterWindowMessageW.restype = UINT
RegisterWindowMessageW.argtypes = [LPCWSTR]
RegisterWindowMessage = RegisterWindowMessageW # alias
RegisterShellHookWindow = _user32.RegisterShellHookWindow
RegisterShellHookWindow.restype = BOOL
RegisterShellHookWindow.argtypes = [HWND]
DeregisterShellHookWindow = _user32.DeregisterShellHookWindow
DeregisterShellHookWindow.restype = BOOL
DeregisterShellHookWindow.argtypes = [HWND]
EnumWindows = _user32.EnumWindows
EnumWindows.restype = BOOL
EnumWindows.argtypes = [WNDENUMPROC, LPARAM]
WM_APP = 32768 # Variable c_int '32768'
GWL_STYLE = -16 # Variable c_int '-0x000000010'
HSHELL_WINDOWCREATED = 1 # Variable c_int '1'
HSHELL_WINDOWDESTROYED = 2 # Variable c_int '2'
HSHELL_WINDOWACTIVATED = 4 # Variable c_int '4'
WS_VISIBLE = 268435456 # Variable c_long '268435456l'
GWL_HWNDPARENT = -8 # Variable c_int '-0x000000008'
GetShellWindow = _user32.GetShellWindow
GetShellWindow.restype = HWND
GetShellWindow.argtypes = []
DestroyWindow = _user32.DestroyWindow
DestroyWindow.restype = BOOL
DestroyWindow.argtypes = [HWND]
UnregisterClassW = _user32.UnregisterClassW
UnregisterClassW.restype = BOOL
UnregisterClassW.argtypes = [LPCWSTR, HINSTANCE]
UnregisterClass = UnregisterClassW # alias
LoadCursorW = _user32.LoadCursorW
LoadCursorW.restype = HCURSOR
LoadCursorW.argtypes = [HINSTANCE, LPCWSTR]
LoadCursor = LoadCursorW # alias
MAXDWORD = 4294967295L # Variable c_uint '-1u'
GENERIC_WRITE = 1073741824 # Variable c_long '1073741824l'
FILE_ATTRIBUTE_NORMAL = 128 # Variable c_int '128'
FILE_FLAG_OVERLAPPED = 1073741824 # Variable c_int '1073741824'
ERROR_IO_PENDING = 997 # Variable c_long '997l'
NOPARITY = 0 # Variable c_int '0'
ODDPARITY = 1 # Variable c_int '1'
EVENPARITY = 2 # Variable c_int '2'
MARKPARITY = 3 # Variable c_int '3'
SPACEPARITY = 4 # Variable c_int '4'
ONESTOPBIT = 0 # Variable c_int '0'
ONE5STOPBITS = 1 # Variable c_int '1'
TWOSTOPBITS = 2 # Variable c_int '2'
SETDTR = 5 # Variable c_int '5'
CLRDTR = 6 # Variable c_int '6'
SETRTS = 3 # Variable c_int '3'
CLRRTS = 4 # Variable c_int '4'
DTR_CONTROL_DISABLE = 0 # Variable c_int '0'
EV_BREAK = 64 # Variable c_int '64'
EV_CTS = 8 # Variable c_int '8'
EV_DSR = 16 # Variable c_int '16'
EV_ERR = 128 # Variable c_int '128'
EV_RING = 256 # Variable c_int '256'
EV_RLSD = 32 # Variable c_int '32'
EV_RXCHAR = 1 # Variable c_int '1'
EV_RXFLAG = 2 # Variable c_int '2'
EV_TXEMPTY = 4 # Variable c_int '4'
OVERLAPPED = _OVERLAPPED
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
ReadFile = _kernel32.ReadFile
ReadFile.restype = BOOL
ReadFile.argtypes = [HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED]
LPCVOID = c_void_p
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
GetDefaultCommConfig = GetDefaultCommConfigW # alias
LPCOMMTIMEOUTS = POINTER(_COMMTIMEOUTS)
GetCommTimeouts = _kernel32.GetCommTimeouts
GetCommTimeouts.restype = BOOL
GetCommTimeouts.argtypes = [HANDLE, LPCOMMTIMEOUTS]
SetCommTimeouts = _kernel32.SetCommTimeouts
SetCommTimeouts.restype = BOOL
SetCommTimeouts.argtypes = [HANDLE, LPCOMMTIMEOUTS]
WS_CHILD = 1073741824 # Variable c_long '1073741824l'
SBS_SIZEGRIP = 16 # Variable c_long '16l'
SBS_SIZEBOXTOPLEFTALIGN = 2 # Variable c_long '2l'
SM_CYHSCROLL = 3 # Variable c_int '3'
SM_CXVSCROLL = 2 # Variable c_int '2'
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
FILE_SHARE_WRITE = 2 # Variable c_int '2'
FILE_FLAG_BACKUP_SEMANTICS = 33554432 # Variable c_int '33554432'
FILE_NOTIFY_CHANGE_FILE_NAME = 1 # Variable c_int '1'
FILE_NOTIFY_CHANGE_DIR_NAME = 2 # Variable c_int '2'
FILE_NOTIFY_CHANGE_ATTRIBUTES = 4 # Variable c_int '4'
FILE_NOTIFY_CHANGE_SIZE = 8 # Variable c_int '8'
FILE_NOTIFY_CHANGE_LAST_WRITE = 16 # Variable c_int '16'
FILE_NOTIFY_CHANGE_SECURITY = 256 # Variable c_int '256'
FILE_LIST_DIRECTORY = 1 # Variable c_int '1'
FILE_ACTION_ADDED = 1 # Variable c_int '1'
FILE_ACTION_REMOVED = 2 # Variable c_int '2'
FILE_ACTION_MODIFIED = 3 # Variable c_int '3'
FILE_ACTION_RENAMED_OLD_NAME = 4 # Variable c_int '4'
FILE_ACTION_RENAMED_NEW_NAME = 5 # Variable c_int '5'
class tagCOPYDATASTRUCT(Structure):
    pass
COPYDATASTRUCT = tagCOPYDATASTRUCT
tagCOPYDATASTRUCT._fields_ = [
    ('dwData', ULONG_PTR),
    ('cbData', DWORD),
    ('lpData', PVOID),
]
PCOPYDATASTRUCT = POINTER(tagCOPYDATASTRUCT)
WM_COPYDATA = 74 # Variable c_int '74'
def CreateWindowW(lpClassName,lpWindowName,dwStyle,x,y,nWidth,nHeight,hWndParent,hMenu,hInstance,lpParam): return CreateWindowExW(0L, lpClassName, lpWindowName, dwStyle, x, y,nWidth, nHeight, hWndParent, hMenu, hInstance, lpParam) # macro
CreateWindow = CreateWindowW # alias
SWP_NOACTIVATE = 16 # Variable c_int '16'
SWP_NOOWNERZORDER = 512 # Variable c_int '512'
SWP_SHOWWINDOW = 64 # Variable c_int '64'
SWP_HIDEWINDOW = 128 # Variable c_int '128'
GA_PARENT = 1 # Variable c_int '1'
SetCommMask = _kernel32.SetCommMask
SetCommMask.restype = BOOL
SetCommMask.argtypes = [HANDLE, DWORD]
WaitCommEvent = _kernel32.WaitCommEvent
WaitCommEvent.restype = BOOL
WaitCommEvent.argtypes = [HANDLE, LPDWORD, LPOVERLAPPED]
class _MEMORYSTATUS(Structure):
    pass
MEMORYSTATUS = _MEMORYSTATUS
_MEMORYSTATUS._fields_ = [
    ('dwLength', DWORD),
    ('dwMemoryLoad', DWORD),
    ('dwTotalPhys', SIZE_T),
    ('dwAvailPhys', SIZE_T),
    ('dwTotalPageFile', SIZE_T),
    ('dwAvailPageFile', SIZE_T),
    ('dwTotalVirtual', SIZE_T),
    ('dwAvailVirtual', SIZE_T),
]
LPMEMORYSTATUS = POINTER(_MEMORYSTATUS)
GlobalMemoryStatus = _kernel32.GlobalMemoryStatus
GlobalMemoryStatus.restype = None
GlobalMemoryStatus.argtypes = [LPMEMORYSTATUS]
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
ERROR_OPERATION_ABORTED = 995 # Variable c_long '995l'
GetProcessHeap = _kernel32.GetProcessHeap
GetProcessHeap.restype = HANDLE
GetProcessHeap.argtypes = []
HeapFree = _kernel32.HeapFree
HeapFree.restype = BOOL
HeapFree.argtypes = [HANDLE, DWORD, LPVOID]
GetVolumeInformationW = _kernel32.GetVolumeInformationW
GetVolumeInformationW.restype = BOOL
GetVolumeInformationW.argtypes = [LPCWSTR, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD]
GetVolumeInformation = GetVolumeInformationW # alias
SWP_FRAMECHANGED = 32 # Variable c_int '32'

class tagMONITORINFO(Structure):
    pass
LPMONITORINFO = POINTER(tagMONITORINFO)
GetMonitorInfoW = _user32.GetMonitorInfoW
GetMonitorInfoW.restype = BOOL
GetMonitorInfoW.argtypes = [HMONITOR, LPMONITORINFO]
GetMonitorInfo = GetMonitorInfoW # alias
tagMONITORINFO._fields_ = [
    ('cbSize', DWORD),
    ('rcMonitor', RECT),
    ('rcWork', RECT),
    ('dwFlags', DWORD),
]
MONITORINFO = tagMONITORINFO
MonitorFromRect = _user32.MonitorFromRect
MonitorFromRect.restype = HMONITOR
MonitorFromRect.argtypes = [LPCRECT, DWORD]
MONITOR_DEFAULTTONULL = 0 # Variable c_int '0'
MONITOR_DEFAULTTONEAREST = 2 # Variable c_int '2'
MonitorFromWindow = _user32.MonitorFromWindow
MonitorFromWindow.restype = HMONITOR
MonitorFromWindow.argtypes = [HWND, DWORD]

OpenSCManagerW = _Advapi32.OpenSCManagerW
OpenSCManagerW.restype = SC_HANDLE
OpenSCManagerW.argtypes = [LPCWSTR, LPCWSTR, DWORD]
OpenSCManager = OpenSCManagerW # alias
SC_MANAGER_ALL_ACCESS = 983103 # Variable c_long '983103l'
CreateServiceW = _Advapi32.CreateServiceW
CreateServiceW.restype = SC_HANDLE
CreateServiceW.argtypes = [SC_HANDLE, LPCWSTR, LPCWSTR, DWORD, DWORD, DWORD, DWORD, LPCWSTR, LPCWSTR, LPDWORD, LPCWSTR, LPCWSTR, LPCWSTR]
CreateService = CreateServiceW # alias
SERVICE_ALL_ACCESS = 983551 # Variable c_long '983551l'
SERVICE_WIN32_OWN_PROCESS = 16 # Variable c_int '16'
SERVICE_DEMAND_START = 3 # Variable c_int '3'
SERVICE_ERROR_NORMAL = 1 # Variable c_int '1'
CloseServiceHandle = _Advapi32.CloseServiceHandle
CloseServiceHandle.restype = BOOL
CloseServiceHandle.argtypes = [SC_HANDLE]
DELETE = 65536 # Variable c_long '65536l'
OpenServiceW = _Advapi32.OpenServiceW
OpenServiceW.restype = SC_HANDLE
OpenServiceW.argtypes = [SC_HANDLE, LPCWSTR, DWORD]
OpenService = OpenServiceW # alias
DeleteService = _Advapi32.DeleteService
DeleteService.restype = BOOL
DeleteService.argtypes = [SC_HANDLE]
SERVICE_SYSTEM_START = 1 # Variable c_int '1'
SERVICE_AUTO_START = 2 # Variable c_int '2'

# values for enumeration '_SC_STATUS_TYPE'
SC_STATUS_PROCESS_INFO = 0
_SC_STATUS_TYPE = c_int # enum
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
SERVICE_QUERY_STATUS = 4 # Variable c_int '4'
SERVICE_STOPPED = 1 # Variable c_int '1'
SERVICE_STOP_PENDING = 3 # Variable c_int '3'
Sleep = _kernel32.Sleep
Sleep.restype = None
Sleep.argtypes = [DWORD]
StartServiceW = _Advapi32.StartServiceW
StartServiceW.restype = BOOL
StartServiceW.argtypes = [SC_HANDLE, DWORD, POINTER(LPCWSTR)]
StartService = StartServiceW # alias
SERVICE_START_PENDING = 2 # Variable c_int '2'
SERVICE_RUNNING = 4 # Variable c_int '4'
SERVICE_CONTROL_STOP = 1 # Variable c_int '1'
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
SERVICE_ACTIVE = 1 # Variable c_int '1'
class _ENUM_SERVICE_STATUSW(Structure):
    pass
LPENUM_SERVICE_STATUSW = POINTER(_ENUM_SERVICE_STATUSW)
EnumDependentServicesW = _Advapi32.EnumDependentServicesW
EnumDependentServicesW.restype = BOOL
EnumDependentServicesW.argtypes = [SC_HANDLE, DWORD, LPENUM_SERVICE_STATUSW, DWORD, LPDWORD, LPDWORD]
EnumDependentServices = EnumDependentServicesW # alias
SERVICE_STATUS = _SERVICE_STATUS
_ENUM_SERVICE_STATUSW._fields_ = [
    ('lpServiceName', LPWSTR),
    ('lpDisplayName', LPWSTR),
    ('ServiceStatus', SERVICE_STATUS),
]
ERROR_MORE_DATA = 234 # Variable c_long '234l'
class _SHELLEXECUTEINFOW(Structure):
    pass
SHELLEXECUTEINFOW = _SHELLEXECUTEINFOW
SHELLEXECUTEINFO = SHELLEXECUTEINFOW
class N18_SHELLEXECUTEINFOW5DOLLAR_254E(Union):
    pass
N18_SHELLEXECUTEINFOW5DOLLAR_254E._pack_ = 1
N18_SHELLEXECUTEINFOW5DOLLAR_254E._fields_ = [
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
    ('_0', N18_SHELLEXECUTEINFOW5DOLLAR_254E),
    ('hProcess', HANDLE),
]
SEE_MASK_NOASYNC = 256 # Variable c_int '256'
SEE_MASK_FLAG_DDEWAIT = SEE_MASK_NOASYNC # alias
SEE_MASK_FLAG_NO_UI = 1024 # Variable c_int '1024'
SW_SHOWNORMAL = 1 # Variable c_int '1'
SEE_MASK_NOCLOSEPROCESS = 64 # Variable c_int '64'
SEE_MASK_NOCLOSEPROCESS = 64 # Variable c_int '64'
ChangeServiceConfig2W = _Advapi32.ChangeServiceConfig2W
ChangeServiceConfig2W.restype = BOOL
ChangeServiceConfig2W.argtypes = [SC_HANDLE, DWORD, LPVOID]
ChangeServiceConfig2 = ChangeServiceConfig2W # alias
class _SERVICE_DESCRIPTIONW(Structure):
    pass
SERVICE_DESCRIPTIONW = _SERVICE_DESCRIPTIONW
SERVICE_DESCRIPTION = SERVICE_DESCRIPTIONW
_SERVICE_DESCRIPTIONW._fields_ = [
    ('lpDescription', LPWSTR),
]
SERVICE_CONFIG_DESCRIPTION = 1 # Variable c_int '1'
SERVICE_CHANGE_CONFIG = 2 # Variable c_int '2'

GetExitCodeProcess = _kernel32.GetExitCodeProcess
GetExitCodeProcess.restype = BOOL
GetExitCodeProcess.argtypes = [HANDLE, LPDWORD]
ERROR_SERVICE_DOES_NOT_EXIST = 1060 # Variable c_long '1060l'

PIPE_ACCESS_DUPLEX = 3 # Variable c_int '3'
PIPE_TYPE_MESSAGE = 4 # Variable c_int '4'
PIPE_READMODE_MESSAGE = 2 # Variable c_int '2'
PIPE_WAIT = 0 # Variable c_int '0'
PIPE_UNLIMITED_INSTANCES = 255 # Variable c_int '255'
ERROR_PIPE_CONNECTED = 535 # Variable c_long '535l'
CreateNamedPipeW = _kernel32.CreateNamedPipeW
CreateNamedPipeW.restype = HANDLE
CreateNamedPipeW.argtypes = [LPCWSTR, DWORD, DWORD, DWORD, DWORD, DWORD, DWORD, LPSECURITY_ATTRIBUTES]
CreateNamedPipe = CreateNamedPipeW # alias
FlushFileBuffers = _kernel32.FlushFileBuffers
FlushFileBuffers.restype = BOOL
FlushFileBuffers.argtypes = [HANDLE]
ConnectNamedPipe = _kernel32.ConnectNamedPipe
ConnectNamedPipe.restype = BOOL
ConnectNamedPipe.argtypes = [HANDLE, LPOVERLAPPED]
DisconnectNamedPipe = _kernel32.DisconnectNamedPipe
DisconnectNamedPipe.restype = BOOL
DisconnectNamedPipe.argtypes = [HANDLE]
PTHREAD_START_ROUTINE = WINFUNCTYPE(DWORD, LPVOID)
LPTHREAD_START_ROUTINE = PTHREAD_START_ROUTINE
CreateThread = _kernel32.CreateThread
CreateThread.restype = HANDLE
CreateThread.argtypes = [LPSECURITY_ATTRIBUTES, SIZE_T, LPTHREAD_START_ROUTINE, LPVOID, DWORD, LPDWORD]
NMPWAIT_USE_DEFAULT_WAIT = 0 # Variable c_int '0'
WaitNamedPipeW = _kernel32.WaitNamedPipeW
WaitNamedPipeW.restype = BOOL
WaitNamedPipeW.argtypes = [LPCWSTR, DWORD]
WaitNamedPipe = WaitNamedPipeW # alias
SetNamedPipeHandleState = _kernel32.SetNamedPipeHandleState
SetNamedPipeHandleState.restype = BOOL
SetNamedPipeHandleState.argtypes = [HANDLE, LPDWORD, LPDWORD, LPDWORD]
ERROR_PIPE_BUSY = 231 # Variable c_long '231l'
PeekNamedPipe = _kernel32.PeekNamedPipe
PeekNamedPipe.restype = BOOL
PeekNamedPipe.argtypes = [HANDLE, LPVOID, DWORD, LPDWORD, LPDWORD, LPDWORD]

WaitForMultipleObjects = _kernel32.WaitForMultipleObjects
WaitForMultipleObjects.restype = DWORD
WaitForMultipleObjects.argtypes = [DWORD, POINTER(HANDLE), BOOL, DWORD]

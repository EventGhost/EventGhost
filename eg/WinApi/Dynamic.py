# This file gets automatically extended by ctypeslib.dynamic_module, so don't
# edit it yourself.
#pylint: disable-msg=C0103,C0301
from ctypes import *
from ctypes.wintypes import *
_user32 = WinDLL("user32")
_kernel32 = WinDLL("kernel32")
_ole32 = WinDLL("ole32")
_gdi32 = WinDLL("Gdi32")
_winmm = WinDLL("Winmm")
_shell32 = WinDLL("shell32")
_Psapi = WinDLL("Psapi")
_Advapi32 = WinDLL("Advapi32")
_setupapi = WinDLL("setupapi")
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
            )       
        except WindowsError:
            print "GCC_XML most likely not installed"
# everything after the following line is automatically created
#-----------------------------------------------------------------------------#
WM_QUERYENDSESSION = 17 # Variable c_int
WM_ENDSESSION = 22 # Variable c_int
SetProcessShutdownParameters = _kernel32.SetProcessShutdownParameters
SetProcessShutdownParameters.restype = BOOL
SetProcessShutdownParameters.argtypes = [DWORD, DWORD]
WM_SIZE = 5 # Variable c_int
CW_USEDEFAULT = -2147483648 # Variable c_int
WS_OVERLAPPEDWINDOW = 13565952 # Variable c_long
GetModuleHandleW = _kernel32.GetModuleHandleW
GetModuleHandleW.restype = HMODULE
GetModuleHandleW.argtypes = [LPCWSTR]
GetModuleHandle = GetModuleHandleW # alias
class tagWNDCLASSW(Structure):
    pass
WNDCLASSW = tagWNDCLASSW
WNDCLASS = WNDCLASSW
LONG_PTR = c_long
LRESULT = LONG_PTR
WNDPROC = WINFUNCTYPE(LRESULT, c_void_p, c_uint, c_uint, c_long)
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
LPVOID = c_void_p
CreateWindowExW = _user32.CreateWindowExW
CreateWindowExW.restype = HWND
CreateWindowExW.argtypes = [DWORD, LPCWSTR, LPCWSTR, DWORD, c_int, c_int, c_int, c_int, HWND, HMENU, HINSTANCE, LPVOID]
CreateWindowEx = CreateWindowExW # alias
DefWindowProcW = _user32.DefWindowProcW
DefWindowProcW.restype = LRESULT
DefWindowProcW.argtypes = [HWND, UINT, WPARAM, LPARAM]
DefWindowProc = DefWindowProcW # alias
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
WAIT_OBJECT_0 = 0 # Variable c_ulong
WAIT_TIMEOUT = 258 # Variable c_long
QS_ALLINPUT = 255 # Variable c_int
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
TranslateMessage = _user32.TranslateMessage
TranslateMessage.restype = BOOL
TranslateMessage.argtypes = [POINTER(MSG)]
DispatchMessageW = _user32.DispatchMessageW
DispatchMessageW.restype = LRESULT
DispatchMessageW.argtypes = [POINTER(MSG)]
DispatchMessage = DispatchMessageW # alias
class tagINPUT(Structure):
    pass
LPINPUT = POINTER(tagINPUT)
SendInput = _user32.SendInput
SendInput.restype = UINT
SendInput.argtypes = [UINT, LPINPUT, c_int]
class N8tagINPUT4DOLLAR_70E(Union):
    pass
class tagMOUSEINPUT(Structure):
    pass
ULONG_PTR = c_ulong
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
N8tagINPUT4DOLLAR_70E._fields_ = [
    ('mi', MOUSEINPUT),
    ('ki', KEYBDINPUT),
    ('hi', HARDWAREINPUT),
]
tagINPUT._anonymous_ = ['_0']
tagINPUT._fields_ = [
    ('type', DWORD),
    ('_0', N8tagINPUT4DOLLAR_70E),
]
OpenProcess = _kernel32.OpenProcess
OpenProcess.restype = HANDLE
OpenProcess.argtypes = [DWORD, BOOL, DWORD]
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
FARPROC = WINFUNCTYPE(c_int)
TIMERPROC = FARPROC
SetTimer = _user32.SetTimer
SetTimer.restype = UINT_PTR
SetTimer.argtypes = [HWND, UINT_PTR, UINT, TIMERPROC]
GetCurrentThreadId = _kernel32.GetCurrentThreadId
GetCurrentThreadId.restype = DWORD
GetCurrentThreadId.argtypes = []
LPDWORD = POINTER(DWORD)
GetWindowThreadProcessId = _user32.GetWindowThreadProcessId
GetWindowThreadProcessId.restype = DWORD
GetWindowThreadProcessId.argtypes = [HWND, LPDWORD]
LPBYTE = POINTER(BYTE)
SetKeyboardState = _user32.SetKeyboardState
SetKeyboardState.restype = BOOL
SetKeyboardState.argtypes = [LPBYTE]
INPUT = tagINPUT
INPUT_KEYBOARD = 1 # Variable c_int
KEYEVENTF_KEYUP = 2 # Variable c_int
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
PROCESS_QUERY_INFORMATION = 1024 # Variable c_int
VK_SHIFT = 16 # Variable c_int
VK_LSHIFT = 160 # Variable c_int
VK_CONTROL = 17 # Variable c_int
VK_LCONTROL = 162 # Variable c_int
VK_MENU = 18 # Variable c_int
VK_LMENU = 164 # Variable c_int
VK_RMENU = 165 # Variable c_int
WM_TIMER = 275 # Variable c_int
WM_SYSKEYDOWN = 260 # Variable c_int
WM_KEYDOWN = 256 # Variable c_int
WM_SYSKEYUP = 261 # Variable c_int
WM_KEYUP = 257 # Variable c_int
AttachThreadInput = _user32.AttachThreadInput
AttachThreadInput.restype = BOOL
AttachThreadInput.argtypes = [DWORD, DWORD, BOOL]
SHORT = c_short
VkKeyScanW = _user32.VkKeyScanW
VkKeyScanW.restype = SHORT
VkKeyScanW.argtypes = [WCHAR]
TCHAR = WCHAR
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
GetForegroundWindow = _user32.GetForegroundWindow
GetForegroundWindow.restype = HWND
GetForegroundWindow.argtypes = []
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
InvalidateRect = _user32.InvalidateRect
InvalidateRect.restype = BOOL
InvalidateRect.argtypes = [HWND, POINTER(RECT), BOOL]
SendNotifyMessageW = _user32.SendNotifyMessageW
SendNotifyMessageW.restype = BOOL
SendNotifyMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendNotifyMessage = SendNotifyMessageW # alias
LPRECT = POINTER(tagRECT)
GetWindowRect = _user32.GetWindowRect
GetWindowRect.restype = BOOL
GetWindowRect.argtypes = [HWND, LPRECT]
LPCRECT = POINTER(RECT)
MONITORENUMPROC = WINFUNCTYPE(BOOL, c_void_p, c_void_p, POINTER(tagRECT), c_long)
EnumDisplayMonitors = _user32.EnumDisplayMonitors
EnumDisplayMonitors.restype = BOOL
EnumDisplayMonitors.argtypes = [HDC, LPCRECT, MONITORENUMPROC, LPARAM]
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
PDWORD_PTR = POINTER(ULONG_PTR)
SendMessageTimeoutW = _user32.SendMessageTimeoutW
SendMessageTimeoutW.restype = LRESULT
SendMessageTimeoutW.argtypes = [HWND, UINT, WPARAM, LPARAM, UINT, UINT, PDWORD_PTR]
SendMessageTimeout = SendMessageTimeoutW # alias
LPPOINT = POINTER(tagPOINT)
ScreenToClient = _user32.ScreenToClient
ScreenToClient.restype = BOOL
ScreenToClient.argtypes = [HWND, LPPOINT]
WindowFromPoint = _user32.WindowFromPoint
WindowFromPoint.restype = HWND
WindowFromPoint.argtypes = [POINT]
WM_GETICON = 127 # Variable c_int
ICON_SMALL = 0 # Variable c_int
ICON_BIG = 1 # Variable c_int
SMTO_ABORTIFHUNG = 2 # Variable c_int
GCL_HICONSM = -34 # Variable c_int
GCL_HICON = -14 # Variable c_int
R2_NOT = 6 # Variable c_int
PS_INSIDEFRAME = 6 # Variable c_int
SM_CXBORDER = 5 # Variable c_int
NULL_BRUSH = 5 # Variable c_int
GA_ROOT = 2 # Variable c_int
SW_RESTORE = 9 # Variable c_int
WM_SYSCOMMAND = 274 # Variable c_int
SC_CLOSE = 61536 # Variable c_int
SW_SHOWNA = 8 # Variable c_int
GetTickCount = _kernel32.GetTickCount
GetTickCount.restype = DWORD
GetTickCount.argtypes = []
SIZE_T = ULONG_PTR
SetProcessWorkingSetSize = _kernel32.SetProcessWorkingSetSize
SetProcessWorkingSetSize.restype = BOOL
SetProcessWorkingSetSize.argtypes = [HANDLE, SIZE_T, SIZE_T]
GetCurrentProcess = _kernel32.GetCurrentProcess
GetCurrentProcess.restype = HANDLE
GetCurrentProcess.argtypes = []
GetDriveTypeW = _kernel32.GetDriveTypeW
GetDriveTypeW.restype = UINT
GetDriveTypeW.argtypes = [LPCWSTR]
GetDriveType = GetDriveTypeW # alias
SendMessageW = _user32.SendMessageW
SendMessageW.restype = LRESULT
SendMessageW.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendMessage = SendMessageW # alias
EXECUTION_STATE = DWORD
SetThreadExecutionState = _kernel32.SetThreadExecutionState
SetThreadExecutionState.restype = EXECUTION_STATE
SetThreadExecutionState.argtypes = [EXECUTION_STATE]
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
class N11_OVERLAPPED4DOLLAR_48E(Union):
    pass
class N11_OVERLAPPED4DOLLAR_484DOLLAR_49E(Structure):
    pass
N11_OVERLAPPED4DOLLAR_484DOLLAR_49E._fields_ = [
    ('Offset', DWORD),
    ('OffsetHigh', DWORD),
]
PVOID = c_void_p
N11_OVERLAPPED4DOLLAR_48E._anonymous_ = ['_0']
N11_OVERLAPPED4DOLLAR_48E._fields_ = [
    ('_0', N11_OVERLAPPED4DOLLAR_484DOLLAR_49E),
    ('Pointer', PVOID),
]
_OVERLAPPED._anonymous_ = ['_0']
_OVERLAPPED._fields_ = [
    ('Internal', ULONG_PTR),
    ('InternalHigh', ULONG_PTR),
    ('_0', N11_OVERLAPPED4DOLLAR_48E),
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
TOKEN_PRIVILEGES = _TOKEN_PRIVILEGES
GENERIC_READ = 2147483648L # Variable c_ulong
FILE_SHARE_READ = 1 # Variable c_int
OPEN_EXISTING = 3 # Variable c_int
SC_SCREENSAVE = 61760 # Variable c_int
SC_MONITORPOWER = 61808 # Variable c_int
TOKEN_ADJUST_PRIVILEGES = 32 # Variable c_int
TOKEN_QUERY = 8 # Variable c_int
WSTRING = c_wchar_p
SE_SHUTDOWN_NAME = u'SeShutdownPrivilege' # Variable WSTRING
SE_PRIVILEGE_ENABLED = 2 # Variable c_long
EWX_LOGOFF = 0 # Variable c_int
SPI_SETDESKWALLPAPER = 20 # Variable c_int
SPIF_SENDWININICHANGE = 2 # Variable c_int
SPIF_SENDCHANGE = SPIF_SENDWININICHANGE # alias
SPIF_UPDATEINIFILE = 1 # Variable c_int
INVALID_HANDLE_VALUE = 4294967295L # Variable c_void_p
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
class N16tagMIXERCONTROLW5DOLLAR_132E(Union):
    pass
class N16tagMIXERCONTROLW5DOLLAR_1325DOLLAR_133E(Structure):
    pass
N16tagMIXERCONTROLW5DOLLAR_1325DOLLAR_133E._pack_ = 1
N16tagMIXERCONTROLW5DOLLAR_1325DOLLAR_133E._fields_ = [
    ('lMinimum', LONG),
    ('lMaximum', LONG),
]
class N16tagMIXERCONTROLW5DOLLAR_1325DOLLAR_134E(Structure):
    pass
N16tagMIXERCONTROLW5DOLLAR_1325DOLLAR_134E._pack_ = 1
N16tagMIXERCONTROLW5DOLLAR_1325DOLLAR_134E._fields_ = [
    ('dwMinimum', DWORD),
    ('dwMaximum', DWORD),
]
N16tagMIXERCONTROLW5DOLLAR_132E._pack_ = 1
N16tagMIXERCONTROLW5DOLLAR_132E._anonymous_ = ['_0', '_1']
N16tagMIXERCONTROLW5DOLLAR_132E._fields_ = [
    ('_0', N16tagMIXERCONTROLW5DOLLAR_1325DOLLAR_133E),
    ('_1', N16tagMIXERCONTROLW5DOLLAR_1325DOLLAR_134E),
    ('dwReserved', DWORD * 6),
]
class N16tagMIXERCONTROLW5DOLLAR_135E(Union):
    pass
N16tagMIXERCONTROLW5DOLLAR_135E._pack_ = 1
N16tagMIXERCONTROLW5DOLLAR_135E._fields_ = [
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
    ('Bounds', N16tagMIXERCONTROLW5DOLLAR_132E),
    ('Metrics', N16tagMIXERCONTROLW5DOLLAR_135E),
]
class tagMIXERLINECONTROLSW(Structure):
    pass
MIXERLINECONTROLSW = tagMIXERLINECONTROLSW
MIXERLINECONTROLS = MIXERLINECONTROLSW
class N21tagMIXERLINECONTROLSW5DOLLAR_137E(Union):
    pass
N21tagMIXERLINECONTROLSW5DOLLAR_137E._pack_ = 1
N21tagMIXERLINECONTROLSW5DOLLAR_137E._fields_ = [
    ('dwControlID', DWORD),
    ('dwControlType', DWORD),
]
LPMIXERCONTROLW = POINTER(tagMIXERCONTROLW)
tagMIXERLINECONTROLSW._pack_ = 1
tagMIXERLINECONTROLSW._anonymous_ = ['_0']
tagMIXERLINECONTROLSW._fields_ = [
    ('cbStruct', DWORD),
    ('dwLineID', DWORD),
    ('_0', N21tagMIXERLINECONTROLSW5DOLLAR_137E),
    ('cControls', DWORD),
    ('cbmxctrl', DWORD),
    ('pamxctrl', LPMIXERCONTROLW),
]
class tagMIXERLINEW(Structure):
    pass
MIXERLINEW = tagMIXERLINEW
MIXERLINE = MIXERLINEW
DWORD_PTR = ULONG_PTR
class N13tagMIXERLINEW5DOLLAR_127E(Structure):
    pass
N13tagMIXERLINEW5DOLLAR_127E._pack_ = 1
N13tagMIXERLINEW5DOLLAR_127E._fields_ = [
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
    ('Target', N13tagMIXERLINEW5DOLLAR_127E),
]
class tMIXERCONTROLDETAILS(Structure):
    pass
MIXERCONTROLDETAILS = tMIXERCONTROLDETAILS
class N20tMIXERCONTROLDETAILS5DOLLAR_138E(Union):
    pass
N20tMIXERCONTROLDETAILS5DOLLAR_138E._pack_ = 1
N20tMIXERCONTROLDETAILS5DOLLAR_138E._fields_ = [
    ('hwndOwner', HWND),
    ('cMultipleItems', DWORD),
]
tMIXERCONTROLDETAILS._pack_ = 1
tMIXERCONTROLDETAILS._anonymous_ = ['_0']
tMIXERCONTROLDETAILS._fields_ = [
    ('cbStruct', DWORD),
    ('dwControlID', DWORD),
    ('cChannels', DWORD),
    ('_0', N20tMIXERCONTROLDETAILS5DOLLAR_138E),
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
MIXERLINE_COMPONENTTYPE_DST_SPEAKERS = 4 # Variable c_long
MIXERCONTROL_CONTROLTYPE_MUTE = 536936450 # Variable c_long
MIXERCONTROL_CONTROLTYPE_VOLUME = 1342373889 # Variable c_long
MIXER_GETLINEINFOF_COMPONENTTYPE = 3 # Variable c_long
MIXER_GETLINECONTROLSF_ONEBYTYPE = 2 # Variable c_long
MIXER_GETLINECONTROLSF_ALL = 0 # Variable c_long
MIXER_GETLINEINFOF_DESTINATION = 0 # Variable c_long
MIXER_GETLINEINFOF_SOURCE = 1 # Variable c_long
MMSYSERR_NOERROR = 0 # Variable c_int
MIXERCONTROL_CT_CLASS_MASK = 4026531840L # Variable c_ulong
MIXERCONTROL_CT_CLASS_FADER = 1342177280 # Variable c_long
MIXERCONTROL_CONTROLTYPE_BASS = 1342373890 # Variable c_long
MIXERCONTROL_CONTROLTYPE_TREBLE = 1342373891 # Variable c_long
MIXERCONTROL_CONTROLTYPE_EQUALIZER = 1342373892 # Variable c_long
MIXERCONTROL_CONTROLTYPE_FADER = 1342373888 # Variable c_long
MIXERCONTROL_CT_CLASS_LIST = 1879048192 # Variable c_long
MIXERCONTROL_CONTROLTYPE_SINGLESELECT = 1879113728 # Variable c_long
MIXERCONTROL_CONTROLTYPE_MULTIPLESELECT = 1895890944 # Variable c_long
MIXERCONTROL_CONTROLTYPE_MUX = 1879113729 # Variable c_long
MIXERCONTROL_CONTROLTYPE_MIXER = 1895890945 # Variable c_long
MIXERCONTROL_CT_CLASS_METER = 268435456 # Variable c_long
MIXERCONTROL_CONTROLTYPE_BOOLEANMETER = 268500992 # Variable c_long
MIXERCONTROL_CONTROLTYPE_PEAKMETER = 268566529 # Variable c_long
MIXERCONTROL_CONTROLTYPE_SIGNEDMETER = 268566528 # Variable c_long
MIXERCONTROL_CONTROLTYPE_UNSIGNEDMETER = 268632064 # Variable c_long
MIXERCONTROL_CT_CLASS_NUMBER = 805306368 # Variable c_long
MIXERCONTROL_CONTROLTYPE_SIGNED = 805437440 # Variable c_long
MIXERCONTROL_CONTROLTYPE_UNSIGNED = 805502976 # Variable c_long
MIXERCONTROL_CONTROLTYPE_PERCENT = 805634048 # Variable c_long
MIXERCONTROL_CONTROLTYPE_DECIBELS = 805568512 # Variable c_long
MIXERCONTROL_CT_CLASS_SLIDER = 1073741824 # Variable c_long
MIXERCONTROL_CONTROLTYPE_SLIDER = 1073872896 # Variable c_long
MIXERCONTROL_CONTROLTYPE_PAN = 1073872897 # Variable c_long
MIXERCONTROL_CONTROLTYPE_QSOUNDPAN = 1073872898 # Variable c_long
MIXERCONTROL_CT_CLASS_SWITCH = 536870912 # Variable c_long
MIXERCONTROL_CONTROLTYPE_BOOLEAN = 536936448 # Variable c_long
MIXERCONTROL_CONTROLTYPE_BUTTON = 553713664 # Variable c_long
MIXERCONTROL_CONTROLTYPE_LOUDNESS = 536936452 # Variable c_long
MIXERCONTROL_CONTROLTYPE_MONO = 536936451 # Variable c_long
MIXERCONTROL_CONTROLTYPE_ONOFF = 536936449 # Variable c_long
MIXERCONTROL_CONTROLTYPE_STEREOENH = 536936453 # Variable c_long
MIXERCONTROL_CT_CLASS_TIME = 1610612736 # Variable c_long
MIXERCONTROL_CONTROLTYPE_MICROTIME = 1610809344 # Variable c_long
MIXERCONTROL_CONTROLTYPE_MILLITIME = 1627586560 # Variable c_long
MIXERCONTROL_CT_CLASS_CUSTOM = 0 # Variable c_long
MIXERCONTROL_CONTROLF_DISABLED = 2147483648L # Variable c_ulong
MIXERCONTROL_CONTROLF_MULTIPLE = 2 # Variable c_long
MIXERCONTROL_CONTROLF_UNIFORM = 1 # Variable c_long
ENUM_CURRENT_SETTINGS = 4294967295L # Variable c_ulong
EDS_RAWMODE = 2 # Variable c_int
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
class N12_devicemodeW4DOLLAR_62E(Union):
    pass
class N12_devicemodeW4DOLLAR_624DOLLAR_63E(Structure):
    pass
N12_devicemodeW4DOLLAR_624DOLLAR_63E._fields_ = [
    ('dmOrientation', c_short),
    ('dmPaperSize', c_short),
    ('dmPaperLength', c_short),
    ('dmPaperWidth', c_short),
    ('dmScale', c_short),
    ('dmCopies', c_short),
    ('dmDefaultSource', c_short),
    ('dmPrintQuality', c_short),
]
class N12_devicemodeW4DOLLAR_624DOLLAR_64E(Structure):
    pass
N12_devicemodeW4DOLLAR_624DOLLAR_64E._fields_ = [
    ('dmPosition', POINTL),
    ('dmDisplayOrientation', DWORD),
    ('dmDisplayFixedOutput', DWORD),
]
N12_devicemodeW4DOLLAR_62E._anonymous_ = ['_0', '_1']
N12_devicemodeW4DOLLAR_62E._fields_ = [
    ('_0', N12_devicemodeW4DOLLAR_624DOLLAR_63E),
    ('_1', N12_devicemodeW4DOLLAR_624DOLLAR_64E),
]
class N12_devicemodeW4DOLLAR_65E(Union):
    pass
N12_devicemodeW4DOLLAR_65E._fields_ = [
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
    ('_0', N12_devicemodeW4DOLLAR_62E),
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
    ('_1', N12_devicemodeW4DOLLAR_65E),
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
DISPLAY_DEVICE_MIRRORING_DRIVER = 8 # Variable c_int
DISPLAY_DEVICE_PRIMARY_DEVICE = 4 # Variable c_int
DISPLAY_DEVICE_ATTACHED_TO_DESKTOP = 1 # Variable c_int
DM_POSITION = 32 # Variable c_long
DM_BITSPERPEL = 262144 # Variable c_long
DM_PELSWIDTH = 524288 # Variable c_long
DM_PELSHEIGHT = 1048576 # Variable c_long
DM_DISPLAYFLAGS = 2097152 # Variable c_long
DM_DISPLAYFREQUENCY = 4194304 # Variable c_long
CDS_UPDATEREGISTRY = 1 # Variable c_int
CDS_NORESET = 268435456 # Variable c_int
CDS_SET_PRIMARY = 16 # Variable c_int
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
CREATE_NEW_CONSOLE = 16 # Variable c_int
STARTF_USESHOWWINDOW = 1 # Variable c_int
INFINITE = 4294967295L # Variable c_uint
WM_DEVICECHANGE = 537 # Variable c_int
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
DBT_DEVICEARRIVAL = 32768 # Variable c_int
DBT_DEVICEREMOVECOMPLETE = 32772 # Variable c_int
DBT_DEVTYP_VOLUME = 2 # Variable c_int
DBT_DEVTYP_DEVICEINTERFACE = 5 # Variable c_int
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
WM_POWERBROADCAST = 536 # Variable c_int
PBT_APMSUSPEND = 4 # Variable c_int
PBT_APMRESUMEAUTOMATIC = 18 # Variable c_int
PBT_APMBATTERYLOW = 9 # Variable c_int
PBT_APMOEMEVENT = 11 # Variable c_int
PBT_APMPOWERSTATUSCHANGE = 10 # Variable c_int
PBT_APMQUERYSUSPEND = 0 # Variable c_int
PBT_APMQUERYSUSPENDFAILED = 2 # Variable c_int
PBT_APMRESUMECRITICAL = 6 # Variable c_int
PBT_APMRESUMESUSPEND = 7 # Variable c_int
LPTSTR = LPWSTR
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
SW_MAXIMIZE = 3 # Variable c_int
SW_MINIMIZE = 6 # Variable c_int
WM_COMMAND = 273 # Variable c_int
GWL_EXSTYLE = -20 # Variable c_int
WS_EX_TOPMOST = 8 # Variable c_long
SWP_NOMOVE = 2 # Variable c_int
SWP_NOSIZE = 1 # Variable c_int
HWND_TOPMOST = 4294967295L # Variable c_void_p
HWND_NOTOPMOST = 4294967294L # Variable c_void_p
GA_PARENT = 1 # Variable c_int
mouse_event = _user32.mouse_event
mouse_event.restype = None
mouse_event.argtypes = [DWORD, DWORD, DWORD, DWORD, ULONG_PTR]
GetCursorPos = _user32.GetCursorPos
GetCursorPos.restype = BOOL
GetCursorPos.argtypes = [LPPOINT]
SetCursorPos = _user32.SetCursorPos
SetCursorPos.restype = BOOL
SetCursorPos.argtypes = [c_int, c_int]
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
OVERLAPPED = _OVERLAPPED
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
ReadFile = _kernel32.ReadFile
ReadFile.restype = BOOL
ReadFile.argtypes = [HANDLE, LPVOID, DWORD, LPDWORD, LPOVERLAPPED]
LPCVOID = c_void_p
WriteFile = _kernel32.WriteFile
WriteFile.restype = BOOL
WriteFile.argtypes = [HANDLE, LPCVOID, DWORD, LPDWORD, LPOVERLAPPED]
LPDCB = POINTER(_DCB)
GetCommState = _kernel32.GetCommState
GetCommState.restype = BOOL
GetCommState.argtypes = [HANDLE, LPDCB]
SetCommState = _kernel32.SetCommState
SetCommState.restype = BOOL
SetCommState.argtypes = [HANDLE, LPDCB]
LPCOMSTAT = POINTER(_COMSTAT)
ClearCommError = _kernel32.ClearCommError
ClearCommError.restype = BOOL
ClearCommError.argtypes = [HANDLE, LPDWORD, LPCOMSTAT]
LPCOMMCONFIG = POINTER(_COMMCONFIG)
GetDefaultCommConfigW = _kernel32.GetDefaultCommConfigW
GetDefaultCommConfigW.restype = BOOL
GetDefaultCommConfigW.argtypes = [LPCWSTR, LPCOMMCONFIG, LPDWORD]
GetDefaultCommConfig = GetDefaultCommConfigW # alias
EscapeCommFunction = _kernel32.EscapeCommFunction
EscapeCommFunction.restype = BOOL
EscapeCommFunction.argtypes = [HANDLE, DWORD]
GetOverlappedResult = _kernel32.GetOverlappedResult
GetOverlappedResult.restype = BOOL
GetOverlappedResult.argtypes = [HANDLE, LPOVERLAPPED, LPDWORD, BOOL]
ResetEvent = _kernel32.ResetEvent
ResetEvent.restype = BOOL
ResetEvent.argtypes = [HANDLE]
ERROR_IO_PENDING = 997 # Variable c_long
SETDTR = 5 # Variable c_int
CLRDTR = 6 # Variable c_int
SETRTS = 3 # Variable c_int
CLRRTS = 4 # Variable c_int
GENERIC_WRITE = 1073741824 # Variable c_long
FILE_ATTRIBUTE_NORMAL = 128 # Variable c_int
FILE_FLAG_OVERLAPPED = 1073741824 # Variable c_int
DTR_CONTROL_DISABLE = 0 # Variable c_int
NOPARITY = 0 # Variable c_int
ONESTOPBIT = 0 # Variable c_int
WS_CHILD = 1073741824 # Variable c_long
WS_VISIBLE = 268435456 # Variable c_long
SBS_SIZEGRIP = 16 # Variable c_long
SBS_SIZEBOXTOPLEFTALIGN = 2 # Variable c_long
SM_CYHSCROLL = 3 # Variable c_int
SM_CXVSCROLL = 2 # Variable c_int
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
WM_APP = 32768 # Variable c_int
GWL_STYLE = -16 # Variable c_int
HSHELL_WINDOWCREATED = 1 # Variable c_int
HSHELL_WINDOWDESTROYED = 2 # Variable c_int
HSHELL_WINDOWACTIVATED = 4 # Variable c_int
GetCurrentProcessId = _kernel32.GetCurrentProcessId
GetCurrentProcessId.restype = DWORD
GetCurrentProcessId.argtypes = []
GetWindowTextW = _user32.GetWindowTextW
GetWindowTextW.restype = c_int
GetWindowTextW.argtypes = [HWND, LPWSTR, c_int]
GetWindowText = GetWindowTextW # alias
GetClassNameW = _user32.GetClassNameW
GetClassNameW.restype = c_int
GetClassNameW.argtypes = [HWND, LPWSTR, c_int]
GetClassName = GetClassNameW # alias
EnumProcesses = _Psapi.EnumProcesses
EnumProcesses.restype = BOOL
EnumProcesses.argtypes = [POINTER(DWORD), DWORD, POINTER(DWORD)]
EnumProcesses = _Psapi.EnumProcesses
EnumProcesses.restype = BOOL
EnumProcesses.argtypes = [POINTER(DWORD), DWORD, POINTER(DWORD)]
# IID_IShellLink = IID_IShellLinkW # alias
FILE_SHARE_WRITE = 2 # Variable c_int
FILE_FLAG_BACKUP_SEMANTICS = 33554432 # Variable c_int
FILE_NOTIFY_CHANGE_FILE_NAME = 1 # Variable c_int
FILE_NOTIFY_CHANGE_DIR_NAME = 2 # Variable c_int
FILE_NOTIFY_CHANGE_ATTRIBUTES = 4 # Variable c_int
FILE_NOTIFY_CHANGE_SIZE = 8 # Variable c_int
FILE_NOTIFY_CHANGE_LAST_WRITE = 16 # Variable c_int
FILE_NOTIFY_CHANGE_SECURITY = 256 # Variable c_int
FILE_LIST_DIRECTORY = 1 # Variable c_int
PulseEvent = _kernel32.PulseEvent
PulseEvent.restype = BOOL
PulseEvent.argtypes = [HANDLE]
class _FILE_NOTIFY_INFORMATION(Structure):
    pass
FILE_NOTIFY_INFORMATION = _FILE_NOTIFY_INFORMATION
_FILE_NOTIFY_INFORMATION._fields_ = [
    ('NextEntryOffset', DWORD),
    ('Action', DWORD),
    ('FileNameLength', DWORD),
    ('FileName', WCHAR * 1),
]
LPOVERLAPPED_COMPLETION_ROUTINE = WINFUNCTYPE(None, c_ulong, c_ulong, POINTER(_OVERLAPPED))
ReadDirectoryChangesW = _kernel32.ReadDirectoryChangesW
ReadDirectoryChangesW.restype = BOOL
ReadDirectoryChangesW.argtypes = [HANDLE, LPVOID, DWORD, BOOL, DWORD, LPDWORD, LPOVERLAPPED, LPOVERLAPPED_COMPLETION_ROUTINE]
FILE_ACTION_ADDED = 1 # Variable c_int
FILE_ACTION_REMOVED = 2 # Variable c_int
FILE_ACTION_MODIFIED = 3 # Variable c_int
FILE_ACTION_RENAMED_OLD_NAME = 4 # Variable c_int
FILE_ACTION_RENAMED_NEW_NAME = 5 # Variable c_int
PM_REMOVE = 1 # Variable c_int
WM_QUIT = 18 # Variable c_int
SMTO_BLOCK = 1 # Variable c_int
WM_USER = 1024 # Variable c_int
FindWindowW = _user32.FindWindowW
FindWindowW.restype = HWND
FindWindowW.argtypes = [LPCWSTR, LPCWSTR]
FindWindow = FindWindowW # alias
SMTO_BLOCK = 1 # Variable c_int
class tagCOPYDATASTRUCT(Structure):
    pass
COPYDATASTRUCT = tagCOPYDATASTRUCT
tagCOPYDATASTRUCT._fields_ = [
    ('dwData', ULONG_PTR),
    ('cbData', DWORD),
    ('lpData', PVOID),
]
WM_COPYDATA = 74 # Variable c_int
PCOPYDATASTRUCT = POINTER(tagCOPYDATASTRUCT)
def CreateWindowW(lpClassName,lpWindowName,dwStyle,x,y,nWidth,nHeight,hWndParent,hMenu,hInstance,lpParam): return CreateWindowExW(0L, lpClassName, lpWindowName, dwStyle, x, y,nWidth, nHeight, hWndParent, hMenu, hInstance, lpParam) # macro
CreateWindow = CreateWindowW # alias
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
CS_VREDRAW = 1 # Variable c_int
CS_HREDRAW = 2 # Variable c_int
WSTRING = c_wchar_p
IDC_ARROW = 32512 # Variable WSTRING
COLOR_WINDOW = 5 # Variable c_int
WS_SYSMENU = 524288 # Variable c_long
WS_OVERLAPPED = 0 # Variable c_long
MIXERCONTROL_CONTROLTYPE_CUSTOM = 0 # Variable c_long
class tMIXERCONTROLDETAILS_SIGNED(Structure):
    pass
MIXERCONTROLDETAILS_SIGNED = tMIXERCONTROLDETAILS_SIGNED
tMIXERCONTROLDETAILS_SIGNED._pack_ = 1
tMIXERCONTROLDETAILS_SIGNED._fields_ = [
    ('lValue', LONG),
]
class tMIXERCONTROLDETAILS_BOOLEAN(Structure):
    pass
MIXERCONTROLDETAILS_BOOLEAN = tMIXERCONTROLDETAILS_BOOLEAN
tMIXERCONTROLDETAILS_BOOLEAN._pack_ = 1
tMIXERCONTROLDETAILS_BOOLEAN._fields_ = [
    ('fValue', LONG),
]
class tagMIXERCONTROLDETAILS_LISTTEXTW(Structure):
    pass
MIXERCONTROLDETAILS_LISTTEXTW = tagMIXERCONTROLDETAILS_LISTTEXTW
MIXERCONTROLDETAILS_LISTTEXT = MIXERCONTROLDETAILS_LISTTEXTW
tagMIXERCONTROLDETAILS_LISTTEXTW._pack_ = 1
tagMIXERCONTROLDETAILS_LISTTEXTW._fields_ = [
    ('dwParam1', DWORD),
    ('dwParam2', DWORD),
    ('szName', WCHAR * 64),
]
MIXER_GETLINECONTROLSF_ONEBYID = 1 # Variable c_long
MIXER_GETCONTROLDETAILSF_VALUE = 0 # Variable c_long
MIXER_GETCONTROLDETAILSF_LISTTEXT = 1 # Variable c_long
GetWindow = _user32.GetWindow
GetWindow.restype = HWND
GetWindow.argtypes = [HWND, UINT]
GW_HWNDFIRST = 0 # Variable c_int
GW_HWNDNEXT = 2 # Variable c_int
HWND_TOP = 0 # Variable c_void_p
WS_BORDER = 8388608 # Variable c_long
GetDesktopWindow = _user32.GetDesktopWindow
GetDesktopWindow.restype = HWND
GetDesktopWindow.argtypes = []
GetTopWindow = _user32.GetTopWindow
GetTopWindow.restype = HWND
GetTopWindow.argtypes = [HWND]
WS_DISABLED = 134217728 # Variable c_long
GW_OWNER = 4 # Variable c_int
WS_EX_APPWINDOW = 262144 # Variable c_long
WS_EX_NOACTIVATE = 134217728 # Variable c_long
WS_EX_TOOLWINDOW = 128 # Variable c_long
IsWindowEnabled = _user32.IsWindowEnabled
IsWindowEnabled.restype = BOOL
IsWindowEnabled.argtypes = [HWND]
OpenClipboard = _user32.OpenClipboard
OpenClipboard.restype = BOOL
OpenClipboard.argtypes = [HWND]
CloseClipboard = _user32.CloseClipboard
CloseClipboard.restype = BOOL
CloseClipboard.argtypes = []
GetClipboardData = _user32.GetClipboardData
GetClipboardData.restype = HANDLE
GetClipboardData.argtypes = [UINT]
GlobalLock = _kernel32.GlobalLock
GlobalLock.restype = LPVOID
GlobalLock.argtypes = [HGLOBAL]
GlobalUnlock = _kernel32.GlobalUnlock
GlobalUnlock.restype = BOOL
GlobalUnlock.argtypes = [HGLOBAL]
CF_TEXT = 1 # Variable c_int
CF_UNICODETEXT = 13 # Variable c_int
SetClipboardViewer = _user32.SetClipboardViewer
SetClipboardViewer.restype = HWND
SetClipboardViewer.argtypes = [HWND]
ChangeClipboardChain = _user32.ChangeClipboardChain
ChangeClipboardChain.restype = BOOL
ChangeClipboardChain.argtypes = [HWND, HWND]
WM_CHANGECBCHAIN = 781 # Variable c_int
WM_DRAWCLIPBOARD = 776 # Variable c_int
GetClipboardOwner = _user32.GetClipboardOwner
GetClipboardOwner.restype = HWND
GetClipboardOwner.argtypes = []
GHND = 66 # Variable c_int
GlobalAlloc = _kernel32.GlobalAlloc
GlobalAlloc.restype = HGLOBAL
GlobalAlloc.argtypes = [UINT, SIZE_T]
EmptyClipboard = _user32.EmptyClipboard
EmptyClipboard.restype = BOOL
EmptyClipboard.argtypes = []
SetClipboardData = _user32.SetClipboardData
SetClipboardData.restype = HANDLE
SetClipboardData.argtypes = [UINT, HANDLE]
GlobalAddAtomW = _kernel32.GlobalAddAtomW
GlobalAddAtomW.restype = ATOM
GlobalAddAtomW.argtypes = [LPCWSTR]
GlobalAddAtom = GlobalAddAtomW # alias
GlobalGetAtomNameW = _kernel32.GlobalGetAtomNameW
GlobalGetAtomNameW.restype = UINT
GlobalGetAtomNameW.argtypes = [ATOM, LPWSTR, c_int]
GlobalGetAtomName = GlobalGetAtomNameW # alias
GlobalDeleteAtom = _kernel32.GlobalDeleteAtom
GlobalDeleteAtom.restype = ATOM
GlobalDeleteAtom.argtypes = [ATOM]
ODDPARITY = 1 # Variable c_int
EVENPARITY = 2 # Variable c_int
MARKPARITY = 3 # Variable c_int
SPACEPARITY = 4 # Variable c_int
ONE5STOPBITS = 1 # Variable c_int
TWOSTOPBITS = 2 # Variable c_int
HDEVINFO = PVOID
class _SP_DEVINFO_DATA(Structure):
    pass
PSP_DEVINFO_DATA = POINTER(_SP_DEVINFO_DATA)
class _SP_DEVICE_INTERFACE_DATA(Structure):
    pass
PSP_DEVICE_INTERFACE_DATA = POINTER(_SP_DEVICE_INTERFACE_DATA)
SetupDiEnumDeviceInterfaces = _setupapi.SetupDiEnumDeviceInterfaces
SetupDiEnumDeviceInterfaces.restype = BOOL
SetupDiEnumDeviceInterfaces.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, POINTER(GUID), DWORD, PSP_DEVICE_INTERFACE_DATA]
_SP_DEVINFO_DATA._pack_ = 1
_SP_DEVINFO_DATA._fields_ = [
    ('cbSize', DWORD),
    ('ClassGuid', GUID),
    ('DevInst', DWORD),
    ('Reserved', ULONG_PTR),
]
_SP_DEVICE_INTERFACE_DATA._pack_ = 1
_SP_DEVICE_INTERFACE_DATA._fields_ = [
    ('cbSize', DWORD),
    ('InterfaceClassGuid', GUID),
    ('Flags', DWORD),
    ('Reserved', ULONG_PTR),
]
SP_DEVICE_INTERFACE_DATA = _SP_DEVICE_INTERFACE_DATA
SP_DEVINFO_DATA = _SP_DEVINFO_DATA
SetupDiDestroyDeviceInfoList = _setupapi.SetupDiDestroyDeviceInfoList
SetupDiDestroyDeviceInfoList.restype = BOOL
SetupDiDestroyDeviceInfoList.argtypes = [HDEVINFO]
WSTRING = c_wchar_p
PCWSTR = WSTRING
SetupDiGetClassDevsW = _setupapi.SetupDiGetClassDevsW
SetupDiGetClassDevsW.restype = HDEVINFO
SetupDiGetClassDevsW.argtypes = [POINTER(GUID), PCWSTR, HWND, DWORD]
SetupDiGetClassDevs = SetupDiGetClassDevsW # alias
class _SP_DEVICE_INTERFACE_DETAIL_DATA_W(Structure):
    pass
PSP_DEVICE_INTERFACE_DETAIL_DATA_W = POINTER(_SP_DEVICE_INTERFACE_DETAIL_DATA_W)
SetupDiGetDeviceInterfaceDetailW = _setupapi.SetupDiGetDeviceInterfaceDetailW
SetupDiGetDeviceInterfaceDetailW.restype = BOOL
SetupDiGetDeviceInterfaceDetailW.argtypes = [HDEVINFO, PSP_DEVICE_INTERFACE_DATA, PSP_DEVICE_INTERFACE_DETAIL_DATA_W, DWORD, PDWORD, PSP_DEVINFO_DATA]
SetupDiGetDeviceInterfaceDetail = SetupDiGetDeviceInterfaceDetailW # alias
_SP_DEVICE_INTERFACE_DETAIL_DATA_W._pack_ = 1
_SP_DEVICE_INTERFACE_DETAIL_DATA_W._fields_ = [
    ('cbSize', DWORD),
    ('DevicePath', WCHAR * 1),
]
SetupDiGetDeviceRegistryPropertyW = _setupapi.SetupDiGetDeviceRegistryPropertyW
SetupDiGetDeviceRegistryPropertyW.restype = BOOL
SetupDiGetDeviceRegistryPropertyW.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, DWORD, PDWORD, PBYTE, DWORD, PDWORD]
SetupDiGetDeviceRegistryProperty = SetupDiGetDeviceRegistryPropertyW # alias
SP_DEVICE_INTERFACE_DETAIL_DATA_W = _SP_DEVICE_INTERFACE_DETAIL_DATA_W
SP_DEVICE_INTERFACE_DETAIL_DATA = SP_DEVICE_INTERFACE_DETAIL_DATA_W
DIGCF_PRESENT = 2 # Variable c_int
PSP_DEVICE_INTERFACE_DETAIL_DATA = PSP_DEVICE_INTERFACE_DETAIL_DATA_W
GWL_HWNDPARENT = -8 # Variable c_int

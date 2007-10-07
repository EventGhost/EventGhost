# This file gets automatically extended by ctypeslib.dynamic_module, so don't
# edit it yourself.

from ctypes import *
from ctypes.wintypes import *
_user32 = WinDLL("user32")
_kernel32 = WinDLL("kernel32")
_ole32 = WinDLL("ole32")
_gdi32 = WinDLL("Gdi32")
_winmm = WinDLL("Winmm")
_shell32 = WinDLL("shell32")
import sys
if not hasattr(sys, "frozen"): # detect py2exe
    try:
        ctypeslib = __import__("ctypeslib.dynamic_module")
    except ImportError :
        print "ctypeslib is not installed!"
    else:
        ctypeslib.dynamic_module.include(
            "#define _WIN32_WINNT 0x500\n"
            "#define WIN32_LEAN_AND_MEAN\n"
            "#define NO_STRICT\n"
            "#include <windows.h>\n"
            "#include <Dbt.h>\n"
            "#include <objbase.h>\n"
            "#include <Mmsystem.h>\n"
            "#include <shlobj.h>\n"
        )        
# everything after the following line is automatically created
#-----------------------------------------------------------------------------#
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
class _OVERLAPPED(Structure):
    pass
OVERLAPPED = _OVERLAPPED
ULONG_PTR = c_ulong
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
LPVOID = c_void_p
LPDWORD = POINTER(DWORD)
LPOVERLAPPED = POINTER(_OVERLAPPED)
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
GetDefaultCommConfigA = _kernel32.GetDefaultCommConfigA
GetDefaultCommConfigA.restype = BOOL
GetDefaultCommConfigA.argtypes = [LPCSTR, LPCOMMCONFIG, LPDWORD]
GetDefaultCommConfig = GetDefaultCommConfigA # alias
EscapeCommFunction = _kernel32.EscapeCommFunction
EscapeCommFunction.restype = BOOL
EscapeCommFunction.argtypes = [HANDLE, DWORD]
MsgWaitForMultipleObjects = _user32.MsgWaitForMultipleObjects
MsgWaitForMultipleObjects.restype = DWORD
MsgWaitForMultipleObjects.argtypes = [DWORD, POINTER(HANDLE), BOOL, DWORD, DWORD]
WaitForSingleObject = _kernel32.WaitForSingleObject
WaitForSingleObject.restype = DWORD
WaitForSingleObject.argtypes = [HANDLE, DWORD]
GetOverlappedResult = _kernel32.GetOverlappedResult
GetOverlappedResult.restype = BOOL
GetOverlappedResult.argtypes = [HANDLE, LPOVERLAPPED, LPDWORD, BOOL]
class _SECURITY_ATTRIBUTES(Structure):
    pass
LPSECURITY_ATTRIBUTES = POINTER(_SECURITY_ATTRIBUTES)
CreateEventA = _kernel32.CreateEventA
CreateEventA.restype = HANDLE
CreateEventA.argtypes = [LPSECURITY_ATTRIBUTES, BOOL, BOOL, LPCSTR]
CreateEvent = CreateEventA # alias
_SECURITY_ATTRIBUTES._fields_ = [
    ('nLength', DWORD),
    ('lpSecurityDescriptor', LPVOID),
    ('bInheritHandle', BOOL),
]
SetEvent = _kernel32.SetEvent
SetEvent.restype = BOOL
SetEvent.argtypes = [HANDLE]
ResetEvent = _kernel32.ResetEvent
ResetEvent.restype = BOOL
ResetEvent.argtypes = [HANDLE]
ERROR_IO_PENDING = 997 # Variable c_long
WAIT_TIMEOUT = 258 # Variable c_long
WAIT_OBJECT_0 = 0 # Variable c_ulong
QS_ALLINPUT = 255 # Variable c_int
INFINITE = 4294967295L # Variable c_uint
SETDTR = 5 # Variable c_int
CLRDTR = 6 # Variable c_int
SETRTS = 3 # Variable c_int
CLRRTS = 4 # Variable c_int
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
TCHAR = c_char
MapVirtualKeyA = _user32.MapVirtualKeyA
MapVirtualKeyA.restype = UINT
MapVirtualKeyA.argtypes = [UINT, UINT]
MapVirtualKey = MapVirtualKeyA # alias
LPMSG = POINTER(tagMSG)
GetMessageA = _user32.GetMessageA
GetMessageA.restype = BOOL
GetMessageA.argtypes = [LPMSG, HWND, UINT, UINT]
GetMessage = GetMessageA # alias
PostMessageA = _user32.PostMessageA
PostMessageA.restype = BOOL
PostMessageA.argtypes = [HWND, UINT, WPARAM, LPARAM]
PostMessage = PostMessageA # alias
GA_ROOT = 2 # Variable c_int
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
LPCRECT = POINTER(RECT)
MONITORENUMPROC = WINFUNCTYPE(BOOL, c_void_p, c_void_p, POINTER(tagRECT), c_long)
EnumDisplayMonitors = _user32.EnumDisplayMonitors
EnumDisplayMonitors.restype = BOOL
EnumDisplayMonitors.argtypes = [HDC, LPCRECT, MONITORENUMPROC, LPARAM]
ENUM_CURRENT_SETTINGS = 4294967295L # Variable c_ulong
EDS_RAWMODE = 2 # Variable c_int
class _DISPLAY_DEVICEA(Structure):
    pass
PDISPLAY_DEVICEA = POINTER(_DISPLAY_DEVICEA)
EnumDisplayDevicesA = _user32.EnumDisplayDevicesA
EnumDisplayDevicesA.restype = BOOL
EnumDisplayDevicesA.argtypes = [LPCSTR, DWORD, PDISPLAY_DEVICEA, DWORD]
EnumDisplayDevices = EnumDisplayDevicesA # alias
CHAR = c_char
_DISPLAY_DEVICEA._fields_ = [
    ('cb', DWORD),
    ('DeviceName', CHAR * 32),
    ('DeviceString', CHAR * 128),
    ('StateFlags', DWORD),
    ('DeviceID', CHAR * 128),
    ('DeviceKey', CHAR * 128),
]
class _devicemodeA(Structure):
    pass
LPDEVMODEA = POINTER(_devicemodeA)
EnumDisplaySettingsExA = _user32.EnumDisplaySettingsExA
EnumDisplaySettingsExA.restype = BOOL
EnumDisplaySettingsExA.argtypes = [LPCSTR, DWORD, LPDEVMODEA, DWORD]
EnumDisplaySettingsEx = EnumDisplaySettingsExA # alias
class N12_devicemodeA4DOLLAR_58E(Union):
    pass
class N12_devicemodeA4DOLLAR_584DOLLAR_59E(Structure):
    pass
N12_devicemodeA4DOLLAR_584DOLLAR_59E._fields_ = [
    ('dmOrientation', c_short),
    ('dmPaperSize', c_short),
    ('dmPaperLength', c_short),
    ('dmPaperWidth', c_short),
    ('dmScale', c_short),
    ('dmCopies', c_short),
    ('dmDefaultSource', c_short),
    ('dmPrintQuality', c_short),
]
class N12_devicemodeA4DOLLAR_584DOLLAR_60E(Structure):
    pass
N12_devicemodeA4DOLLAR_584DOLLAR_60E._fields_ = [
    ('dmPosition', POINTL),
    ('dmDisplayOrientation', DWORD),
    ('dmDisplayFixedOutput', DWORD),
]
N12_devicemodeA4DOLLAR_58E._anonymous_ = ['_0', '_1']
N12_devicemodeA4DOLLAR_58E._fields_ = [
    ('_0', N12_devicemodeA4DOLLAR_584DOLLAR_59E),
    ('_1', N12_devicemodeA4DOLLAR_584DOLLAR_60E),
]
class N12_devicemodeA4DOLLAR_61E(Union):
    pass
N12_devicemodeA4DOLLAR_61E._fields_ = [
    ('dmDisplayFlags', DWORD),
    ('dmNup', DWORD),
]
_devicemodeA._anonymous_ = ['_0', '_1']
_devicemodeA._fields_ = [
    ('dmDeviceName', BYTE * 32),
    ('dmSpecVersion', WORD),
    ('dmDriverVersion', WORD),
    ('dmSize', WORD),
    ('dmDriverExtra', WORD),
    ('dmFields', DWORD),
    ('_0', N12_devicemodeA4DOLLAR_58E),
    ('dmColor', c_short),
    ('dmDuplex', c_short),
    ('dmYResolution', c_short),
    ('dmTTOption', c_short),
    ('dmCollate', c_short),
    ('dmFormName', BYTE * 32),
    ('dmLogPixels', WORD),
    ('dmBitsPerPel', DWORD),
    ('dmPelsWidth', DWORD),
    ('dmPelsHeight', DWORD),
    ('_1', N12_devicemodeA4DOLLAR_61E),
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
ChangeDisplaySettingsExA = _user32.ChangeDisplaySettingsExA
ChangeDisplaySettingsExA.restype = LONG
ChangeDisplaySettingsExA.argtypes = [LPCSTR, LPDEVMODEA, HWND, DWORD, LPVOID]
ChangeDisplaySettingsEx = ChangeDisplaySettingsExA # alias
DISPLAY_DEVICEA = _DISPLAY_DEVICEA
DISPLAY_DEVICE = DISPLAY_DEVICEA
DEVMODEA = _devicemodeA
DEVMODE = DEVMODEA
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
WM_DEVICECHANGE = 537 # Variable c_int
class _DEV_BROADCAST_HDR(Structure):
    pass
DEV_BROADCAST_HDR = _DEV_BROADCAST_HDR
_DEV_BROADCAST_HDR._fields_ = [
    ('dbch_size', DWORD),
    ('dbch_devicetype', DWORD),
    ('dbch_reserved', DWORD),
]
class _DEV_BROADCAST_DEVICEINTERFACE_A(Structure):
    pass
DEV_BROADCAST_DEVICEINTERFACE_A = _DEV_BROADCAST_DEVICEINTERFACE_A
DEV_BROADCAST_DEVICEINTERFACE = DEV_BROADCAST_DEVICEINTERFACE_A
class _GUID(Structure):
    pass
_GUID._fields_ = [
    ('Data1', c_ulong),
    ('Data2', c_ushort),
    ('Data3', c_ushort),
    ('Data4', c_ubyte * 8),
]
GUID = _GUID
_DEV_BROADCAST_DEVICEINTERFACE_A._fields_ = [
    ('dbcc_size', DWORD),
    ('dbcc_devicetype', DWORD),
    ('dbcc_reserved', DWORD),
    ('dbcc_classguid', GUID),
    ('dbcc_name', c_char * 1),
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
RegisterDeviceNotificationA = _user32.RegisterDeviceNotificationA
RegisterDeviceNotificationA.restype = HDEVNOTIFY
RegisterDeviceNotificationA.argtypes = [HANDLE, LPVOID, DWORD]
RegisterDeviceNotification = RegisterDeviceNotificationA # alias
UnregisterDeviceNotification = _user32.UnregisterDeviceNotification
UnregisterDeviceNotification.restype = BOOL
UnregisterDeviceNotification.argtypes = [HDEVNOTIFY]
EXECUTION_STATE = DWORD
SetThreadExecutionState = _kernel32.SetThreadExecutionState
SetThreadExecutionState.restype = EXECUTION_STATE
SetThreadExecutionState.argtypes = [EXECUTION_STATE]
SendNotifyMessageA = _user32.SendNotifyMessageA
SendNotifyMessageA.restype = BOOL
SendNotifyMessageA.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendNotifyMessage = SendNotifyMessageA # alias
LONG_PTR = c_long
LRESULT = LONG_PTR
SendMessageA = _user32.SendMessageA
SendMessageA.restype = LRESULT
SendMessageA.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendMessage = SendMessageA # alias
GA_PARENT = 1 # Variable c_int
class tagMIXERCONTROLA(Structure):
    pass
MIXERCONTROLA = tagMIXERCONTROLA
MIXERCONTROL = MIXERCONTROLA
class N16tagMIXERCONTROLA5DOLLAR_128E(Union):
    pass
class N16tagMIXERCONTROLA5DOLLAR_1285DOLLAR_129E(Structure):
    pass
N16tagMIXERCONTROLA5DOLLAR_1285DOLLAR_129E._pack_ = 1
N16tagMIXERCONTROLA5DOLLAR_1285DOLLAR_129E._fields_ = [
    ('lMinimum', LONG),
    ('lMaximum', LONG),
]
class N16tagMIXERCONTROLA5DOLLAR_1285DOLLAR_130E(Structure):
    pass
N16tagMIXERCONTROLA5DOLLAR_1285DOLLAR_130E._pack_ = 1
N16tagMIXERCONTROLA5DOLLAR_1285DOLLAR_130E._fields_ = [
    ('dwMinimum', DWORD),
    ('dwMaximum', DWORD),
]
N16tagMIXERCONTROLA5DOLLAR_128E._pack_ = 1
N16tagMIXERCONTROLA5DOLLAR_128E._anonymous_ = ['_0', '_1']
N16tagMIXERCONTROLA5DOLLAR_128E._fields_ = [
    ('_0', N16tagMIXERCONTROLA5DOLLAR_1285DOLLAR_129E),
    ('_1', N16tagMIXERCONTROLA5DOLLAR_1285DOLLAR_130E),
    ('dwReserved', DWORD * 6),
]
class N16tagMIXERCONTROLA5DOLLAR_131E(Union):
    pass
N16tagMIXERCONTROLA5DOLLAR_131E._pack_ = 1
N16tagMIXERCONTROLA5DOLLAR_131E._fields_ = [
    ('cSteps', DWORD),
    ('cbCustomData', DWORD),
    ('dwReserved', DWORD * 6),
]
tagMIXERCONTROLA._pack_ = 1
tagMIXERCONTROLA._fields_ = [
    ('cbStruct', DWORD),
    ('dwControlID', DWORD),
    ('dwControlType', DWORD),
    ('fdwControl', DWORD),
    ('cMultipleItems', DWORD),
    ('szShortName', CHAR * 16),
    ('szName', CHAR * 64),
    ('Bounds', N16tagMIXERCONTROLA5DOLLAR_128E),
    ('Metrics', N16tagMIXERCONTROLA5DOLLAR_131E),
]
class tagMIXERLINECONTROLSA(Structure):
    pass
MIXERLINECONTROLSA = tagMIXERLINECONTROLSA
MIXERLINECONTROLS = MIXERLINECONTROLSA
class N21tagMIXERLINECONTROLSA5DOLLAR_136E(Union):
    pass
N21tagMIXERLINECONTROLSA5DOLLAR_136E._pack_ = 1
N21tagMIXERLINECONTROLSA5DOLLAR_136E._fields_ = [
    ('dwControlID', DWORD),
    ('dwControlType', DWORD),
]
LPMIXERCONTROLA = POINTER(tagMIXERCONTROLA)
tagMIXERLINECONTROLSA._pack_ = 1
tagMIXERLINECONTROLSA._anonymous_ = ['_0']
tagMIXERLINECONTROLSA._fields_ = [
    ('cbStruct', DWORD),
    ('dwLineID', DWORD),
    ('_0', N21tagMIXERLINECONTROLSA5DOLLAR_136E),
    ('cControls', DWORD),
    ('cbmxctrl', DWORD),
    ('pamxctrl', LPMIXERCONTROLA),
]
class tagMIXERLINEA(Structure):
    pass
MIXERLINEA = tagMIXERLINEA
MIXERLINE = MIXERLINEA
DWORD_PTR = ULONG_PTR
class N13tagMIXERLINEA5DOLLAR_126E(Structure):
    pass
MMVERSION = UINT
N13tagMIXERLINEA5DOLLAR_126E._pack_ = 1
N13tagMIXERLINEA5DOLLAR_126E._fields_ = [
    ('dwType', DWORD),
    ('dwDeviceID', DWORD),
    ('wMid', WORD),
    ('wPid', WORD),
    ('vDriverVersion', MMVERSION),
    ('szPname', CHAR * 32),
]
tagMIXERLINEA._pack_ = 1
tagMIXERLINEA._fields_ = [
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
    ('szShortName', CHAR * 16),
    ('szName', CHAR * 64),
    ('Target', N13tagMIXERLINEA5DOLLAR_126E),
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
HMIXER = HANDLE
LPHMIXER = POINTER(HMIXER)
mixerOpen = _winmm.mixerOpen
mixerOpen.restype = MMRESULT
mixerOpen.argtypes = [LPHMIXER, UINT, DWORD_PTR, DWORD_PTR, DWORD]
HMIXEROBJ = HANDLE
LPMIXERCONTROLDETAILS = POINTER(tMIXERCONTROLDETAILS)
mixerGetControlDetailsA = _winmm.mixerGetControlDetailsA
mixerGetControlDetailsA.restype = MMRESULT
mixerGetControlDetailsA.argtypes = [HMIXEROBJ, LPMIXERCONTROLDETAILS, DWORD]
mixerGetControlDetails = mixerGetControlDetailsA # alias
MIXERLINE_COMPONENTTYPE_DST_SPEAKERS = 4 # Variable c_long
MIXERCONTROL_CONTROLTYPE_MUTE = 536936450 # Variable c_long
MIXER_GETLINEINFOF_COMPONENTTYPE = 3 # Variable c_long
MIXER_GETLINECONTROLSF_ONEBYTYPE = 2 # Variable c_long
MMSYSERR_NOERROR = 0 # Variable c_int
LPMIXERLINEA = POINTER(tagMIXERLINEA)
mixerGetLineInfoA = _winmm.mixerGetLineInfoA
mixerGetLineInfoA.restype = MMRESULT
mixerGetLineInfoA.argtypes = [HMIXEROBJ, LPMIXERLINEA, DWORD]
mixerGetLineInfo = mixerGetLineInfoA # alias
LPMIXERLINECONTROLSA = POINTER(tagMIXERLINECONTROLSA)
mixerGetLineControlsA = _winmm.mixerGetLineControlsA
mixerGetLineControlsA.restype = MMRESULT
mixerGetLineControlsA.argtypes = [HMIXEROBJ, LPMIXERLINECONTROLSA, DWORD]
mixerGetLineControls = mixerGetLineControlsA # alias
mixerSetControlDetails = _winmm.mixerSetControlDetails
mixerSetControlDetails.restype = MMRESULT
mixerSetControlDetails.argtypes = [HMIXEROBJ, LPMIXERCONTROLDETAILS, DWORD]
MIXERCONTROL_CONTROLTYPE_VOLUME = 1342373889 # Variable c_long
CreateFileA = _kernel32.CreateFileA
CreateFileA.restype = HANDLE
CreateFileA.argtypes = [LPCSTR, DWORD, DWORD, LPSECURITY_ATTRIBUTES, DWORD, DWORD, HANDLE]
CreateFile = CreateFileA # alias
GENERIC_READ = 2147483648L # Variable c_ulong
GENERIC_WRITE = 1073741824 # Variable c_long
OPEN_EXISTING = 3 # Variable c_int
FILE_ATTRIBUTE_NORMAL = 128 # Variable c_int
FILE_FLAG_OVERLAPPED = 1073741824 # Variable c_int
CloseHandle = _kernel32.CloseHandle
CloseHandle.restype = BOOL
CloseHandle.argtypes = [HANDLE]
SHGetFolderPathA = _shell32.SHGetFolderPathA
SHGetFolderPathA.restype = HRESULT
SHGetFolderPathA.argtypes = [HWND, c_int, HANDLE, DWORD, LPSTR]
SHGetFolderPath = SHGetFolderPathA # alias
CSIDL_PROGRAM_FILES = 38 # Variable c_int
SHGFP_TYPE_CURRENT = 0
CSIDL_STARTUP = 7 # Variable c_int
SHGetFolderPathW = _shell32.SHGetFolderPathW
SHGetFolderPathW.restype = HRESULT
SHGetFolderPathW.argtypes = [HWND, c_int, HANDLE, DWORD, LPWSTR]
CSIDL_APPDATA = 26 # Variable c_int

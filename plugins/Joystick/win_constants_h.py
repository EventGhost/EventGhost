import eg
import sys


def defined(macro):
    return macro is not None


windows_version = eg.WindowsVersion

_WIN32_WINNT_NT4 = 0x0400 # Windows NT 4.0
_WIN32_WINNT_WIN2K = 0x0500 # Windows 2000
_WIN32_WINNT_WINXP = 0x0501 # Windows XP
_WIN32_WINNT_WS03 = 0x0502 # Windows Server 2003
_WIN32_WINNT_WIN6 = 0x0600 # Windows Vista
_WIN32_WINNT_VISTA = 0x0600 # Windows Vista
_WIN32_WINNT_WS08 = 0x0600 # Windows Server 2008
_WIN32_WINNT_LONGHORN = 0x0600 # Windows Vista
_WIN32_WINNT_WIN7 = 0x0601 # Windows 7
_WIN32_WINNT_WIN8 = 0x0602 # Windows 8
_WIN32_WINNT_WINBLUE = 0x0603 # Windows 8.1
_WIN32_WINNT_WINTHRESHOLD = 0x0A00 # Windows 10
_WIN32_WINNT_WIN10 = 0x0A00 # Windows 10
_WIN32_WINNT_WIN10_RS2 = _WIN32_WINNT_WIN10
_WIN32_WINNT_WIN10_RS3 = _WIN32_WINNT_WIN10

if windows_version.IsXP():
    GDIPVER = 0x0100
    _WIN32_WINNT = _WIN32_WINNT_WINXP

elif windows_version.IsVista():
    GDIPVER = 0x0110
    _WIN32_WINNT = _WIN32_WINNT_VISTA

elif windows_version.Is7():
    GDIPVER = 0x0110
    _WIN32_WINNT = _WIN32_WINNT_WIN7

elif windows_version.Is8():
    GDIPVER = 0x0110
    _WIN32_WINNT = _WIN32_WINNT_WIN8

elif windows_version.Is10():
    GDIPVER = 0x0110
    _WIN32_WINNT = _WIN32_WINNT_WIN10

else:
    GDIPVER = 0x0110
    _WIN32_WINNT = None

WINVER = _WIN32_WINNT

if sys.maxsize > 2**32:
    __64BIT__ = 1
    _WIN64 = 1
    _AMD64_ = 1
    WIN64 = 1
    _X86_ = None
else:
    __64BIT__ = None
    _WIN64 = None
    WIN64 = None
    _AMD64_ = None
    _X86_ = 1

_MSC_VER = 1915
__cplusplus = None
_WIN32 = 1
UNICODE = 1
RC_INVOKED = None
_MAC = None


__all__ = (
    'UNICODE', '_WIN32', '__cplusplus', '_MSC_VER', '_WIN32_WINNT', 'WINVER',
    'defined', 'RC_INVOKED', '_MAC', '_WIN64'
)

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

from ctypes.wintypes import (
    BOOL, DWORD, LPCVOID, LPCWSTR, LPVOID, POINTER, byref, c_char, c_uint,
    cast, pointer, sizeof, Structure, windll, WinError,
)

PUINT = POINTER(c_uint)
LPDWORD = POINTER(DWORD)

GetFileVersionInfoSizeW = windll.version.GetFileVersionInfoSizeW
GetFileVersionInfoSizeW.restype = DWORD
GetFileVersionInfoSizeW.argtypes = [LPCWSTR, LPDWORD]
GetFileVersionInfoSize = GetFileVersionInfoSizeW  # alias

GetFileVersionInfoW = windll.version.GetFileVersionInfoW
GetFileVersionInfoW.restype = BOOL
GetFileVersionInfoW.argtypes = [LPCWSTR, DWORD, DWORD, LPVOID]
GetFileVersionInfo = GetFileVersionInfoW  # alias

VerQueryValueW = windll.version.VerQueryValueW
VerQueryValueW.restype = BOOL
VerQueryValueW.argtypes = [LPCVOID, LPCWSTR, POINTER(LPVOID), PUINT]
VerQueryValue = VerQueryValueW  # alias

class VS_FIXEDFILEINFO(Structure):
    _fields_ = [
        ("dwSignature", DWORD),  # will be 0xFEEF04BD
        ("dwStrucVersion", DWORD),
        ("dwFileVersionMS", DWORD),
        ("dwFileVersionLS", DWORD),
        ("dwProductVersionMS", DWORD),
        ("dwProductVersionLS", DWORD),
        ("dwFileFlagsMask", DWORD),
        ("dwFileFlags", DWORD),
        ("dwFileOS", DWORD),
        ("dwFileType", DWORD),
        ("dwFileSubtype", DWORD),
        ("dwFileDateMS", DWORD),
        ("dwFileDateLS", DWORD)
    ]


def GetFileVersion(filename):
    dwLen  = GetFileVersionInfoSize(filename, None)
    if not dwLen:
        raise WinError()
    lpData = (c_char * dwLen)()
    if not GetFileVersionInfo(filename, 0, sizeof(lpData), lpData):
        raise WinError()
    uLen = c_uint()
    lpffi = POINTER(VS_FIXEDFILEINFO)()
    lplpBuffer = cast(pointer(lpffi), POINTER(LPVOID))
    if not VerQueryValue(lpData, u"\\", lplpBuffer, byref(uLen)):
        raise WinError()
    ffi = lpffi.contents
    return (
        ffi.dwFileVersionMS >> 16,
        ffi.dwFileVersionMS & 0xFFFF,
        ffi.dwFileVersionLS >> 16,
        ffi.dwFileVersionLS & 0xFFFF,
    )

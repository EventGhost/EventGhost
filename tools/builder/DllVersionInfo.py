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

from ctypes.wintypes import (
    windll, sizeof, WinError, byref, POINTER, cast, c_char, Structure, c_uint,
    pointer, BOOL, DWORD, LPVOID, LPCVOID, LPCWSTR,
)

PUINT = POINTER(c_uint)
LPDWORD = POINTER(DWORD)

class VS_FIXEDFILEINFO(Structure):
    _fields_ = [
        ("dwSignature", DWORD), # will be 0xFEEF04BD
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

GetFileVersionInfoSizeW = windll.version.GetFileVersionInfoSizeW
GetFileVersionInfoSizeW.restype = DWORD
GetFileVersionInfoSizeW.argtypes = [LPCWSTR, LPDWORD]
GetFileVersionInfoSize = GetFileVersionInfoSizeW # alias

GetFileVersionInfoW = windll.version.GetFileVersionInfoW
GetFileVersionInfoW.restype = BOOL
GetFileVersionInfoW.argtypes = [LPCWSTR, DWORD, DWORD, LPVOID]
GetFileVersionInfo = GetFileVersionInfoW # alias

VerQueryValueW = windll.version.VerQueryValueW
VerQueryValueW.restype = BOOL
VerQueryValueW.argtypes = [LPCVOID, LPCWSTR, POINTER(LPVOID), PUINT]
VerQueryValue = VerQueryValueW # alias


def GetFileVersion(filename):
    dwLen  = GetFileVersionInfoSize(filename, None)
    if not dwLen :
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


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

import win32api
import _winreg

from eg.WinAPI.win32types import *
from eg.WinAPI.Display import dumps

GetRawInputDeviceList = user32.GetRawInputDeviceList 
GetRawInputDeviceInfo = user32.GetRawInputDeviceInfoA
RegisterRawInputDevices = user32.RegisterRawInputDevices
GetRawInputData = user32.GetRawInputData

RIM_TYPEHID = 2
RIM_TYPEKEYBOARD = 1
RIM_TYPEMOUSE = 0

RIDI_PREPARSEDDATA = 0x20000005
RIDI_DEVICENAME    = 0x20000007
RIDI_DEVICEINFO    = 0x2000000b


class RAWINPUTDEVICE(Structure):
    _fields_ = [
        ("usUsagePage", USHORT),
        ("usUsage", USHORT),
        ("dwFlags", DWORD),
        ("hwndTarget", HWND),
    ]
    
    
class RAWINPUTHEADER(Structure):
    _fields_ = [
        ("dwType", DWORD),
        ("dwSize", DWORD),
        ("hDevice", HANDLE),
        ("wParam", WPARAM),
    ]
    
    
class RAWMOUSE(Structure):
    class _U1(Union):
        class _S2(Structure):
            _fields_ = [
                ("usButtonFlags", USHORT),
                ("usButtonData", USHORT),
            ]
        _fields_ = [
            ("ulButtons", ULONG),
            ("_s2", _S2),
        ]
        
    _fields_ = [
        ("usFlags", USHORT),
        ("_u1", _U1),
        ("ulRawButtons", ULONG),
        ("lLastX", LONG),
        ("lLastY", LONG),
        ("ulExtraInformation", ULONG),
    ]
    _anonymous_ = ("_u1", )
    
    
class RAWKEYBOARD(Structure):
    _fields_ = [
        ("MakeCode", USHORT),
        ("Flags", USHORT),
        ("Reserved", USHORT),
        ("VKey", USHORT),
        ("Message", UINT),
        ("ExtraInformation", ULONG),
    ]
    
    
class RAWHID(Structure):
    _fields_ = [
        ("dwSizeHid", DWORD),
        ("dwCount", DWORD),
        ("bRawData", BYTE),
    ]
    
    
class RAWINPUT(Structure):
    class _U1(Union):
        _fields_ = [
            ("mouse", RAWMOUSE),
            ("keyboard", RAWKEYBOARD),
            ("hid", RAWHID),
        ]
        
    _fields_ = [
        ("header", RAWINPUTHEADER),
        ("_u1", _U1),
        ("hDevice", HANDLE),
        ("wParam", WPARAM),
    ]
    _anonymous_ = ("_u1", )
    
    
    
class RAWINPUTDEVICELIST(Structure):
    _fields_ = [
        ("hDevice", HANDLE),
        ("dwType", DWORD),
    ]
    

class RID_DEVICE_INFO_MOUSE(Structure):
    _fields_ = [
        ("dwId", DWORD),
        ("dwNumberOfButtons", DWORD),
        ("dwSampleRate", DWORD),
        ("fHasHorizontalWheel", BOOL),
    ]
    

class RID_DEVICE_INFO_KEYBOARD(Structure):
    _fields_ = [
        ("dwType", DWORD),
        ("dwSubType", DWORD),
        ("dwKeyboardMode", DWORD),
        ("dwNumberOfFunctionKeys", DWORD),
        ("dwNumberOfIndicators", DWORD),
        ("dwNumberOfKeysTotal", DWORD),
    ]
    
    
class RID_DEVICE_INFO_HID(Structure):
    _fields_ = [
        ("dwVendorId", DWORD),
        ("dwProductId", DWORD),
        ("dwVersionNumber", DWORD),
        ("usUsagePage", DWORD),
        ("usUsage", DWORD),
    ]
    

class RID_DEVICE_INFO(Structure):
    class _U1(Union):
        _fields_ = [
            ("mouse", RID_DEVICE_INFO_MOUSE),
            ("keyboard", RID_DEVICE_INFO_KEYBOARD),
            ("hid", RID_DEVICE_INFO_HID),
        ]
        
    _fields_ = [
        ("cbSize", DWORD),
        ("dwType", DWORD),
        ("_u1", _U1),
    ]
    _anonymous_ = ("_u1", )



def test():
    puiNumDevices = UINT()
    GetRawInputDeviceList(
        0, 
        byref(puiNumDevices), 
        sizeof(RAWINPUTDEVICELIST)
    )
    pRawInputDeviceList = (RAWINPUTDEVICELIST * puiNumDevices.value)()
    puiNumDevices.value = sizeof(pRawInputDeviceList)
    num = GetRawInputDeviceList(
        byref(pRawInputDeviceList), 
        byref(puiNumDevices), 
        sizeof(RAWINPUTDEVICELIST)
    )
    pData = RID_DEVICE_INFO()
    pData.cbSize = sizeof(RID_DEVICE_INFO)
    pcbSize = UINT()
    for i in range(num):
        hDevice = pRawInputDeviceList[i].hDevice
        dwType = pRawInputDeviceList[i].dwType
        print "Device: %d" % i
        GetRawInputDeviceInfo(
            hDevice, 
            RIDI_DEVICENAME, 
            0, 
            byref(pcbSize)
        )
        buf = create_string_buffer(pcbSize.value + 1)
        GetRawInputDeviceInfo(
            hDevice,
            RIDI_DEVICENAME,
            buf,
            byref(pcbSize)
        )
        print "  DeviceName: %r" % buf.value
        key = "System\\CurrentControlSet\\Enum\\" 
        key += buf.raw[4:].split("{", 1)[0].replace("#", "\\")
        hkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key)
        value, _ = _winreg.QueryValueEx(hkey, "DeviceDesc")
        mfg, _ = _winreg.QueryValueEx(hkey, "Mfg")
        _winreg.CloseKey(hkey)
        print "  DeviceDesc: %r" % value
        print "  Mfg: %r" % mfg
        pcbSize.value = sizeof(RID_DEVICE_INFO)
        GetRawInputDeviceInfo(
            hDevice,
            RIDI_DEVICEINFO,
            byref(pData),
            byref(pcbSize)
        )
        if dwType == RIM_TYPEMOUSE:
            print "  " + dumps(pData.mouse)
        elif dwType == RIM_TYPEKEYBOARD:
            print "  " + dumps(pData.keyboard)
        elif dwType == RIM_TYPEHID:
            print "  " + dumps(pData.hid)
        else:
            print "  unknown type", dwType
            
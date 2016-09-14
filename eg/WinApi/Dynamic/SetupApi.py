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

import sys

# Local imports
from eg.WinApi.Dynamic import *

_setupapi = WinDLL("setupapi")
if __name__ == "__main__":
    try:
        ctypeslib = __import__("ctypeslib.dynamic_module")
    except ImportError:
        print "ctypeslib is not installed!"
    else:
        try:
            ctypeslib.dynamic_module.include(
                "#define UNICODE\n"
                "#define _WIN32_WINNT 0x500\n"
                "#define WIN32_LEAN_AND_MEAN\n"
                "#define NO_STRICT\n"
                "#include <windows.h>\n"
                "#include <Setupapi.h>\n"
            )
        except WindowsError:
            print "GCC_XML most likely not installed"

#-----------------------------------------------------------------------------#
# everything after the following line is automatically created
#-----------------------------------------------------------------------------#
WSTRING = c_wchar_p
HDEVINFO = PVOID
PCWSTR = WSTRING
SetupDiGetClassDevsW = _setupapi.SetupDiGetClassDevsW
SetupDiGetClassDevsW.restype = HDEVINFO
SetupDiGetClassDevsW.argtypes = [POINTER(GUID), PCWSTR, HWND, DWORD]
SetupDiGetClassDevs = SetupDiGetClassDevsW  # alias
class _SP_DEVINFO_DATA(Structure):
    pass
PSP_DEVINFO_DATA = POINTER(_SP_DEVINFO_DATA)
PDWORD = POINTER(DWORD)
SetupDiGetDeviceRegistryPropertyW = _setupapi.SetupDiGetDeviceRegistryPropertyW
SetupDiGetDeviceRegistryPropertyW.restype = BOOL
SetupDiGetDeviceRegistryPropertyW.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, DWORD, PDWORD, PBYTE, DWORD, PDWORD]
SetupDiGetDeviceRegistryProperty = SetupDiGetDeviceRegistryPropertyW  # alias
class _GUID(Structure):
    pass
_GUID._fields_ = [
    ('Data1', c_ulong),
    ('Data2', c_ushort),
    ('Data3', c_ushort),
    ('Data4', c_ubyte * 8),
]
_SP_DEVINFO_DATA._pack_ = 1
_SP_DEVINFO_DATA._fields_ = [
    ('cbSize', DWORD),
    ('ClassGuid', GUID),
    ('DevInst', DWORD),
    ('Reserved', ULONG_PTR),
]
SetupDiEnumDeviceInfo = _setupapi.SetupDiEnumDeviceInfo
SetupDiEnumDeviceInfo.restype = BOOL
SetupDiEnumDeviceInfo.argtypes = [HDEVINFO, DWORD, PSP_DEVINFO_DATA]
class _SP_DRVINFO_DATA_V2_W(Structure):
    pass
PSP_DRVINFO_DATA_V2_W = POINTER(_SP_DRVINFO_DATA_V2_W)
PSP_DRVINFO_DATA_W = PSP_DRVINFO_DATA_V2_W
SetupDiGetSelectedDriverW = _setupapi.SetupDiGetSelectedDriverW
SetupDiGetSelectedDriverW.restype = BOOL
SetupDiGetSelectedDriverW.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, PSP_DRVINFO_DATA_W]
SetupDiGetSelectedDriver = SetupDiGetSelectedDriverW  # alias
class _FILETIME(Structure):
    pass
_FILETIME._fields_ = [
    ('dwLowDateTime', DWORD),
    ('dwHighDateTime', DWORD),
]
_SP_DRVINFO_DATA_V2_W._pack_ = 1
_SP_DRVINFO_DATA_V2_W._fields_ = [
    ('cbSize', DWORD),
    ('DriverType', DWORD),
    ('Reserved', ULONG_PTR),
    ('Description', WCHAR * 256),
    ('MfgName', WCHAR * 256),
    ('ProviderName', WCHAR * 256),
    ('DriverDate', FILETIME),
    ('DriverVersion', DWORDLONG),
]
class _SP_DEVINSTALL_PARAMS_W(Structure):
    pass
PSP_DEVINSTALL_PARAMS_W = POINTER(_SP_DEVINSTALL_PARAMS_W)
SetupDiSetDeviceInstallParamsW = _setupapi.SetupDiSetDeviceInstallParamsW
SetupDiSetDeviceInstallParamsW.restype = BOOL
SetupDiSetDeviceInstallParamsW.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, PSP_DEVINSTALL_PARAMS_W]
SetupDiSetDeviceInstallParams = SetupDiSetDeviceInstallParamsW  # alias
PSP_FILE_CALLBACK_W = WINFUNCTYPE(UINT, PVOID, UINT, UINT_PTR, UINT_PTR)
HSPFILEQ = PVOID
_SP_DEVINSTALL_PARAMS_W._pack_ = 1
_SP_DEVINSTALL_PARAMS_W._fields_ = [
    ('cbSize', DWORD),
    ('Flags', DWORD),
    ('FlagsEx', DWORD),
    ('hwndParent', HWND),
    ('InstallMsgHandler', PSP_FILE_CALLBACK_W),
    ('InstallMsgHandlerContext', PVOID),
    ('FileQueue', HSPFILEQ),
    ('ClassInstallReserved', ULONG_PTR),
    ('Reserved', DWORD),
    ('DriverPath', WCHAR * 260),
]
SetupDiGetDeviceInstallParamsW = _setupapi.SetupDiGetDeviceInstallParamsW
SetupDiGetDeviceInstallParamsW.restype = BOOL
SetupDiGetDeviceInstallParamsW.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, PSP_DEVINSTALL_PARAMS_W]
SetupDiGetDeviceInstallParams = SetupDiGetDeviceInstallParamsW  # alias
SetupDiOpenDeviceInfoW = _setupapi.SetupDiOpenDeviceInfoW
SetupDiOpenDeviceInfoW.restype = BOOL
SetupDiOpenDeviceInfoW.argtypes = [HDEVINFO, PCWSTR, HWND, DWORD, PSP_DEVINFO_DATA]
SetupDiOpenDeviceInfo = SetupDiOpenDeviceInfoW  # alias
SetupDiEnumDriverInfoW = _setupapi.SetupDiEnumDriverInfoW
SetupDiEnumDriverInfoW.restype = BOOL
SetupDiEnumDriverInfoW.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, DWORD, DWORD, PSP_DRVINFO_DATA_W]
SetupDiEnumDriverInfo = SetupDiEnumDriverInfoW  # alias
SetupDiBuildDriverInfoList = _setupapi.SetupDiBuildDriverInfoList
SetupDiBuildDriverInfoList.restype = BOOL
SetupDiBuildDriverInfoList.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, DWORD]
DIGCF_PRESENT = 2  # Variable c_int '2'
DIGCF_ALLCLASSES = 4  # Variable c_int '4'
DIGCF_DEVICEINTERFACE = 16  # Variable c_int '16'
SP_DEVINFO_DATA = _SP_DEVINFO_DATA
SP_DRVINFO_DATA_V2_W = _SP_DRVINFO_DATA_V2_W
SP_DRVINFO_DATA_V2 = SP_DRVINFO_DATA_V2_W
SP_DRVINFO_DATA = SP_DRVINFO_DATA_V2
SP_DEVINSTALL_PARAMS_W = _SP_DEVINSTALL_PARAMS_W
SP_DEVINSTALL_PARAMS = SP_DEVINSTALL_PARAMS_W
SPDRP_DEVICEDESC = 0  # Variable c_int '0'
SPDRP_HARDWAREID = 1  # Variable c_int '1'
SPDRP_DRIVER = 9  # Variable c_int '9'
SPDIT_CLASSDRIVER = 1  # Variable c_int '1'
SPDIT_COMPATDRIVER = 2  # Variable c_int '2'
ERROR_INSUFFICIENT_BUFFER = 122  # Variable c_long '122l'
ERROR_INVALID_DATA = 13  # Variable c_long '13l'
SetupDiDestroyDeviceInfoList = _setupapi.SetupDiDestroyDeviceInfoList
SetupDiDestroyDeviceInfoList.restype = BOOL
SetupDiDestroyDeviceInfoList.argtypes = [HDEVINFO]
class _SP_DEVICE_INTERFACE_DATA(Structure):
    pass
PSP_DEVICE_INTERFACE_DATA = POINTER(_SP_DEVICE_INTERFACE_DATA)
SetupDiEnumDeviceInterfaces = _setupapi.SetupDiEnumDeviceInterfaces
SetupDiEnumDeviceInterfaces.restype = BOOL
SetupDiEnumDeviceInterfaces.argtypes = [HDEVINFO, PSP_DEVINFO_DATA, POINTER(GUID), DWORD, PSP_DEVICE_INTERFACE_DATA]
_SP_DEVICE_INTERFACE_DATA._pack_ = 1
_SP_DEVICE_INTERFACE_DATA._fields_ = [
    ('cbSize', DWORD),
    ('InterfaceClassGuid', GUID),
    ('Flags', DWORD),
    ('Reserved', ULONG_PTR),
]
class _SP_DEVICE_INTERFACE_DETAIL_DATA_W(Structure):
    pass
PSP_DEVICE_INTERFACE_DETAIL_DATA_W = POINTER(_SP_DEVICE_INTERFACE_DETAIL_DATA_W)
SetupDiGetDeviceInterfaceDetailW = _setupapi.SetupDiGetDeviceInterfaceDetailW
SetupDiGetDeviceInterfaceDetailW.restype = BOOL
SetupDiGetDeviceInterfaceDetailW.argtypes = [HDEVINFO, PSP_DEVICE_INTERFACE_DATA, PSP_DEVICE_INTERFACE_DETAIL_DATA_W, DWORD, PDWORD, PSP_DEVINFO_DATA]
SetupDiGetDeviceInterfaceDetail = SetupDiGetDeviceInterfaceDetailW  # alias
_SP_DEVICE_INTERFACE_DETAIL_DATA_W._pack_ = 1
_SP_DEVICE_INTERFACE_DETAIL_DATA_W._fields_ = [
    ('cbSize', DWORD),
    ('DevicePath', WCHAR * 1),
]
SP_DEVICE_INTERFACE_DATA = _SP_DEVICE_INTERFACE_DATA
SP_DEVICE_INTERFACE_DETAIL_DATA_W = _SP_DEVICE_INTERFACE_DETAIL_DATA_W
SP_DEVICE_INTERFACE_DETAIL_DATA = SP_DEVICE_INTERFACE_DETAIL_DATA_W
PSP_DEVICE_INTERFACE_DETAIL_DATA = PSP_DEVICE_INTERFACE_DETAIL_DATA_W

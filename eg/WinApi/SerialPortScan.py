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

import re

# Local imports
from Dynamic import (
    byref,
    c_ubyte,
    cast,
    create_unicode_buffer,
    DWORD,
    GetLastError,
    PBYTE,
    sizeof,
    Structure,
    TCHAR,
    WinError,
)
from Dynamic.SetupApi import (
    DIGCF_PRESENT,
    GUID,
    PSP_DEVICE_INTERFACE_DETAIL_DATA,
    SetupDiDestroyDeviceInfoList,
    SetupDiEnumDeviceInterfaces,
    SetupDiGetClassDevs,
    SetupDiGetDeviceInterfaceDetail,
    SetupDiGetDeviceRegistryProperty,
    SP_DEVICE_INTERFACE_DATA,
    SP_DEVICE_INTERFACE_DETAIL_DATA,
    SP_DEVINFO_DATA,
)

GUID_CLASS_COMPORT = GUID(
    0x86e0d1e0L,
    0x8089,
    0x11d0,
    (c_ubyte * 8)(0x9c, 0xe4, 0x08, 0x00, 0x3e, 0x30, 0x1f, 0x73)
)

#DIGCF_PRESENT = 2
DIGCF_DEVICEINTERFACE = 16
INVALID_HANDLE_VALUE = 0
ERROR_INSUFFICIENT_BUFFER = 122
SPDRP_HARDWAREID = 1
SPDRP_FRIENDLYNAME = 12
ERROR_NO_MORE_ITEMS = 259

def GetComPorts(availableOnly=True):
    """
    Scans the registry for serial ports and return a list of (port, desc, hwid)
    tuples.
    If availableOnly is true only return currently existing ports.
    """
    result = []
    stringBuffer = create_unicode_buffer(256)
    flags = DIGCF_DEVICEINTERFACE
    if availableOnly:
        flags |= DIGCF_PRESENT
    hdi = SetupDiGetClassDevs(byref(GUID_CLASS_COMPORT), None, 0, flags)
    if hdi == INVALID_HANDLE_VALUE:
        raise WinError()
    dwRequiredSize = DWORD()
    dwIndex = 0
    while True:
        did = SP_DEVICE_INTERFACE_DATA()
        did.cbSize = sizeof(did)

        if not SetupDiEnumDeviceInterfaces(
            hdi,
            None,
            byref(GUID_CLASS_COMPORT),
            dwIndex,
            byref(did)
        ):
            err = GetLastError()
            if err != ERROR_NO_MORE_ITEMS:
                raise WinError(err)
            break

        # get the size
        if not SetupDiGetDeviceInterfaceDetail(
            hdi,
            byref(did),
            None,
            0,
            byref(dwRequiredSize),
            None
        ):
            # Ignore ERROR_INSUFFICIENT_BUFFER
            err = GetLastError()
            if err != ERROR_INSUFFICIENT_BUFFER:
                raise WinError(err)

        # allocate buffer
        class _SP_DEVICE_INTERFACE_DETAIL_DATA(Structure):
            _fields_ = [
                ('cbSize', DWORD),
                ('DevicePath', TCHAR * (dwRequiredSize.value - sizeof(DWORD))),
            ]
        idd = _SP_DEVICE_INTERFACE_DETAIL_DATA()
        idd.cbSize = sizeof(SP_DEVICE_INTERFACE_DETAIL_DATA)
        devinfo = SP_DEVINFO_DATA()
        devinfo.cbSize = sizeof(devinfo)
        if not SetupDiGetDeviceInterfaceDetail(
            hdi,
            byref(did),
            cast(byref(idd), PSP_DEVICE_INTERFACE_DETAIL_DATA),
            dwRequiredSize,
            None,
            byref(devinfo)
        ):
            raise WinError()
        # hardware ID
        if not SetupDiGetDeviceRegistryProperty(
            hdi,
            byref(devinfo),
            SPDRP_HARDWAREID,
            None,
            cast(stringBuffer, PBYTE),
            sizeof(stringBuffer) - 1,
            None
        ):
            # Ignore ERROR_INSUFFICIENT_BUFFER
            err = GetLastError()
            if err != ERROR_INSUFFICIENT_BUFFER:
                raise WinError(err)
        szHardwareID = stringBuffer.value
        # friendly name
        if not SetupDiGetDeviceRegistryProperty(
            hdi,
            byref(devinfo),
            SPDRP_FRIENDLYNAME,
            None,
            cast(stringBuffer, PBYTE),
            sizeof(stringBuffer) - 1,
            None
        ):
            # Ignore ERROR_INSUFFICIENT_BUFFER
            err = GetLastError()
            if err != ERROR_INSUFFICIENT_BUFFER:
                raise WinError(err)
        szFriendlyName = stringBuffer.value
        portName = re.search(r"\((.*)\)", szFriendlyName).group(1)
        result.append((portName, szFriendlyName, szHardwareID))
        dwIndex += 1

    SetupDiDestroyDeviceInfoList(hdi)
    return result

if __name__ == '__main__':
    for port, desc, hwid in GetComPorts():
        print "%s: %s" % (port, desc)

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

import ctypes
import re

def ValidHandle(value):
    if value == 0:
        raise ctypes.WinError()
    return value

NULL = 0

from Dynamic import (
    byref, sizeof, cast,
    SetupDiDestroyDeviceInfoList,
    SetupDiEnumDeviceInterfaces,
    SetupDiGetClassDevs,
    SetupDiGetDeviceInterfaceDetail,
    SetupDiGetDeviceRegistryProperty,
    DWORD,
    PBYTE,
    TCHAR,
    GUID,
    SP_DEVINFO_DATA,
    SP_DEVICE_INTERFACE_DATA,
    SP_DEVICE_INTERFACE_DETAIL_DATA,
    PSP_DEVICE_INTERFACE_DETAIL_DATA,
    DIGCF_PRESENT,
)

GUID_CLASS_COMPORT = GUID(0x86e0d1e0L, 0x8089, 0x11d0,
    (ctypes.c_ubyte*8)(0x9c, 0xe4, 0x08, 0x00, 0x3e, 0x30, 0x1f, 0x73))

DIGCF_PRESENT = 2
DIGCF_DEVICEINTERFACE = 16
INVALID_HANDLE_VALUE = 0
ERROR_INSUFFICIENT_BUFFER = 122
SPDRP_HARDWAREID = 1
SPDRP_FRIENDLYNAME = 12
ERROR_NO_MORE_ITEMS = 259

def GetComPorts(availableOnly=True):
    """
    This generator scans the device registry for com ports and yields port,
    desc, hwid.
    If availableOnly is true only return currently existing ports.
    """
    stringBuffer = ctypes.create_unicode_buffer(256)
    flags = DIGCF_DEVICEINTERFACE
    if availableOnly:
        flags |= DIGCF_PRESENT
    hdi = SetupDiGetClassDevs(byref(GUID_CLASS_COMPORT), None, NULL, flags)
    #~ for i in range(256):
    for dwIndex in range(256):
        did = SP_DEVICE_INTERFACE_DATA()
        did.cbSize = sizeof(did)

        if not SetupDiEnumDeviceInterfaces(
            hdi,
            None,
            byref(GUID_CLASS_COMPORT),
            dwIndex,
            byref(did)
        ):
            if ctypes.GetLastError() != ERROR_NO_MORE_ITEMS:
                raise ctypes.WinError()
            break

        dwNeeded = DWORD()
        # get the size
        if not SetupDiGetDeviceInterfaceDetail(
            hdi,
            byref(did),
            None,
            0,
            byref(dwNeeded),
            None
        ):
            # Ignore ERROR_INSUFFICIENT_BUFFER
            if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
                raise ctypes.WinError()
        # allocate buffer
        class _SP_DEVICE_INTERFACE_DETAIL_DATA(ctypes.Structure):
            _fields_ = [
                ('cbSize', DWORD),
                ('DevicePath', TCHAR*(dwNeeded.value - sizeof(DWORD))),
            ]
        idd = _SP_DEVICE_INTERFACE_DETAIL_DATA()
        idd.cbSize = sizeof(SP_DEVICE_INTERFACE_DETAIL_DATA)
        devinfo = SP_DEVINFO_DATA()
        devinfo.cbSize = sizeof(devinfo)
        if not SetupDiGetDeviceInterfaceDetail(
            hdi,
            byref(did),
            cast(byref(idd), PSP_DEVICE_INTERFACE_DETAIL_DATA),
            dwNeeded,
            None,
            byref(devinfo)
        ):
            raise ctypes.WinError()
        #print idd.DevicePath, sizeof(idd)
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
            if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
                raise ctypes.WinError()
        szHardwareID = stringBuffer.value
        # friendly name
        #szFriendlyName = ctypes.create_string_buffer('\0' * 250)
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
            if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
                raise ctypes.WinError()
        szFriendlyName = stringBuffer.value
        portName = re.search(r"\((.*)\)", szFriendlyName).group(1)
        yield portName, szFriendlyName, szHardwareID

    SetupDiDestroyDeviceInfoList(hdi)


if __name__ == '__main__':
    for i in range(10):
        import time
        start = time.clock()
        for port, desc, hwid in GetComPorts():
            print "%s: %s" % (port, desc)
        print time.clock() - start


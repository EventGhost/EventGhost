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

import sys
import string
import codecs
from os.path import join

import eg
from eg.WinApi.Dynamic import (
    cast,
    c_ubyte,
    POINTER,
    WinDLL,
    DWORD,
    BOOL,
    byref,
    FormatError,
    DriverPackageInstall,
    SetDifxLogCallback,
    DIFLOGCALLBACK,
)


PUBYTE = POINTER(c_ubyte)

HEADER = r"""\
; This file is automatically created by the BuildDriver.py script. Don't edit
; this file directly.

[Version]
Signature="$Windows NT$"
Class=HIDClass
ClassGuid={745a17a0-74d3-11d0-b6fe-00a0c90f57da}
Provider=%ProviderName%
DriverVer=07/01/2009,1.0.0.9
DriverPackageDisplayName=%DisplayName%

; ========== Manufacturer/Models sections ===========

[Manufacturer]
%ProviderName%=Remotes,NTx86,NTamd64

"""

DEVICE_SECTION = r"""
; ========== $DESCR ==========

[Install$NR]
Include=winusb.inf
Needs=WINUSB.NT

[Install$NR.Services]
Include=winusb.inf
AddService=WinUSB,0x00000002,WinUSB_ServiceInstall

[Install$NR.Wdf]
KmdfService=WINUSB, WinUsb_Install

[Install$NR.CoInstallers]
AddReg=CoInstallers_AddReg
CopyFiles=CoInstallers_CopyFiles

[Install$NR.HW]
AddReg=Dev_AddReg$NR

[Dev_AddReg$NR]
HKR,,DeviceInterfaceGUIDs,0x10000,"$GUID"
HKR,,"SystemWakeEnabled",0x00010001,1

"""

FOOTER = r"""
; ========== Global sections ===========

[WinUSB_Install]
KmdfLibraryVersion=1.7

[WinUSB_ServiceInstall]
DisplayName=%WinUSB_SvcDesc%
ServiceType=1
StartType=3
ErrorControl=1
ServiceBinary=%12%\WinUSB.sys

[CoInstallers_AddReg]
HKR,,CoInstallers32,0x00010000,"WdfCoInstaller01007.dll,WdfCoInstaller","WinUSBCoInstaller.dll","WUDFUpdate_01007.dll"

[CoInstallers_CopyFiles]
WinUSBCoInstaller.dll
WdfCoInstaller01007.dll

[DestinationDirs]
CoInstallers_CopyFiles=11

; ================= Source Media Section =====================

[SourceDisksNames]
1=%DISK_NAME%,,,\x86

[SourceDisksNames.amd64]
1=%DISK_NAME%,,,\amd64

[SourceDisksFiles]
WinUSBCoInstaller.dll=1
WdfCoInstaller01007.dll=1
WUDFUpdate_01007.dll=1

; =================== Strings ===================

[Strings]
ProviderName="EventGhost"
WinUSB_SvcDesc="WinUSB Driver"
DISK_NAME="My Install Disk"
DisplayName="USB Remote Driver"
"""

DRIVER_PACKAGE_FORCE = 4
DRIVER_PACKAGE_LEGACY_MODE = 0x10


class UsbDevice(object):
    dll = None

    def __init__(
        self,
        name,
        hardwareId,
        guid,
        callback,
        dataSize,
        suppressRepeat
    ):
        self.name = name
        self.hardwareId = hardwareId
        self.guid = unicode(guid)
        self.callback = callback
        self.dataSize = dataSize
        self.suppressRepeat = suppressRepeat
        self.threadId = None


    def Start(self):
        if self.dll is None:
            self.__class__.dll = WinDLL(
                join(
                     eg.sitePackagesDir,
                     "WinUsbWrapper.dll"
                ).encode(sys.getfilesystemencoding())
            )
        msgId = eg.messageReceiver.AddWmUserHandler(self.MsgHandler)
        self.threadId = self.dll.Start(
            eg.messageReceiver.hwnd,
            msgId,
            self.guid,
            self.dataSize,
            int(self.suppressRepeat)
        )
        if not self.threadId:
            raise Exception("Device did not start")


    def Stop(self):
        self.dll.End(self.threadId)
        self.threadId = None
        eg.messageReceiver.RemoveWmUserHandler(self.MsgHandler)


    def MsgHandler(self, dummyHwnd, dummyMsg, dummyWParam, lParam):
        dataArray = cast(lParam, PUBYTE)
        value = tuple(dataArray[i] for i in range(self.dataSize))
        self.callback(value)
        return 1



class WinUsb(object):

    def __init__(self):
        self.devices = []


    def AddDevice(
        self,
        name,
        hardwareId,
        guid,
        callback,
        dataSize=1,
        suppressRepeat=False
    ):
        device = UsbDevice(
            name,
            hardwareId,
            guid,
            callback,
            dataSize,
            suppressRepeat
        )
        self.devices.append(device)


    def Open(self):
        try:
            for device in self.devices:
                device.Start()
        except:
            self.EnsureDriver()
            for device in self.devices:
                device.Start()


    def Close(self):
        for device in self.devices:
            device.Close()


    def EnsureDriver(self):
        infPath = join(eg.configDir, self.devices[0].guid + ".inf")
        outfile = codecs.open(
            infPath,
            "wt",
            sys.getfilesystemencoding()
        )
        outfile.write(HEADER)
        outfile.write("[Remotes.NTx86]\n")
        for i, device in enumerate(self.devices):
            outfile.write(
                "%%Device%i.DeviceDesc%%=Install%i,%s\n"
                    % (i, i, device.hardwareId)
            )
        outfile.write("\n[Remotes.NTamd64]\n")
        for i, device in enumerate(self.devices):
            outfile.write(
                "%%Device%i.DeviceDesc%%=Install%i,%s\n"
                    % (i, i, device.hardwareId)
            )
        template = string.Template(DEVICE_SECTION)
        for i, device in enumerate(self.devices):
            outfile.write(
                template.substitute(NR=i, GUID=device.guid, DESCR=device.name)
            )
        outfile.write(FOOTER)
        for i, device in enumerate(self.devices):
            outfile.write('Device%i.DeviceDesc="%s"\n' % (i, device.name))

        outfile.close()
        from eg.WinApi.PipedProcess import ExecAsAdministrator
        print ExecAsAdministrator(
            __file__.decode(sys.getfilesystemencoding()),
            "InstallDriver",
            infPath
        )
#        flags.value = DRIVER_PACKAGE_FORCE
#        res = DriverPackageUninstall(
#            infPath,
#            flags,
#            None,
#            byref(needsReboot)
#        )
#        print res, FormatError(res)
#        print needsReboot.value


def InstallDriver(infPath):
    def Callback(eventType, error, description, context):
        print (eventType, error, description, context)
    difLogCallback = DIFLOGCALLBACK(Callback)
    SetDifxLogCallback(difLogCallback, None)
    flags = DWORD()
    flags.value = DRIVER_PACKAGE_FORCE | DRIVER_PACKAGE_LEGACY_MODE
    needsReboot = BOOL()
    res = DriverPackageInstall(
        infPath,
        flags,
        None,
        byref(needsReboot)
    )
    print res, FormatError(res)
    print needsReboot.value


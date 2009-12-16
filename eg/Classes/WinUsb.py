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

import os
import sys
import string
import codecs
import tempfile
import shutil
import threading
from os.path import join
from ctypes import (
    create_unicode_buffer,
    sizeof,
    WinDLL,
    c_ubyte,
    byref,
    POINTER,
    cast,
    GetLastError,
    WinError,
)
from ctypes.wintypes import DWORD

import wx
import eg
from eg.WinApi import IsWin64
from eg.WinApi.PipedProcess import ExecAs
from eg.WinApi.IsAdmin import IsAdmin
from eg.WinApi.Dynamic import (
    GUID,
    INVALID_HANDLE_VALUE,
    CLSIDFromString,
    PBYTE,
    ERROR_NO_MORE_ITEMS,
)
from eg.WinApi.Dynamic.SetupApi import (
    SetupDiGetClassDevs,
    SetupDiGetDeviceRegistryProperty,
    SetupDiEnumDeviceInfo,
    SetupDiSetDeviceInstallParams,
    SetupDiGetDeviceInstallParams,
    SetupDiEnumDriverInfo,
    SetupDiBuildDriverInfoList,
    DIGCF_PRESENT,
    SP_DEVINFO_DATA,
    SP_DRVINFO_DATA,
    SP_DEVINSTALL_PARAMS,
    SPDRP_HARDWAREID,
    SPDIT_COMPATDRIVER,
    ERROR_INSUFFICIENT_BUFFER,
    ERROR_INVALID_DATA,
)
DI_FLAGSEX_INSTALLEDDRIVER = 0x04000000


PUBYTE = POINTER(c_ubyte)

DRIVER_VERSION = "1.0.1.5"
DRIVER_PROVIDER = "EventGhost"

HEADER = r"""
; This file is automatically created by the BuildDriver.py script. Don't edit
; this file directly.

[Version]
Signature="$$Windows NT$$"
Class=HIDClass
ClassGuid={745a17a0-74d3-11d0-b6fe-00a0c90f57da}
Provider=%ProviderName%
DriverVer=08/24/2009,$DRIVER_VERSION
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
KmdfLibraryVersion=1.9

[WinUSB_ServiceInstall]
DisplayName=%WinUSB_SvcDesc%
ServiceType=1
StartType=3
ErrorControl=1
ServiceBinary=%12%\WinUSB.sys

[CoInstallers_AddReg]
HKR,,CoInstallers32,0x00010000,"WdfCoInstaller01009.dll,WdfCoInstaller","WinUSBCoInstaller2.dll","WUDFUpdate_01009.dll"

[CoInstallers_CopyFiles]
WinUSBCoInstaller2.dll
WdfCoInstaller01009.dll

[DestinationDirs]
CoInstallers_CopyFiles=11

; ================= Source Media Section =====================

[SourceDisksNames]
1=%DISK_NAME%,,,\dll

[SourceDisksNames.amd64]
1=%DISK_NAME%,,,\dll

[SourceDisksFiles]
WinUSBCoInstaller2.dll=1
WdfCoInstaller01009.dll=1
WUDFUpdate_01009.dll=1

; =================== Strings ===================

[Strings]
ProviderName="$DRIVER_PROVIDER"
WinUSB_SvcDesc="WinUSB Driver"
DISK_NAME="My Install Disk"
DisplayName="$DISPLAY_NAME"
"""


class Text(eg.TranslatableStrings):
    dialogCaption = "EventGhost Plugin: %s"
    downloadMsg = (
        "You need to install the EventGhost WinUSB add-on before this plugin"
        "can install the driver for the remote.\n"
        "After installation of the add-on, you need to restart EventGhost.\n\n"
        "Do you want to visit the download page now?\n"
    )
    installMsg = (
        "You need to install the proper driver for this %s device and restart "
        "EventGhost.\n\n"
        "Should EventGhost start the driver installation for you now?"
    )



def StripRevision(hardwareId):
    return "&".join(
        part for part in hardwareId.split("&") if not part.startswith("REV_")
    )


class UsbDevice(object):
    dll = None

    def __init__(
        self,
        name,
        hardwareId,
        guid,
        callback,
        dataSize,
        suppressRepeat,
        plugin
    ):
        self.name = name
        self.plugin = plugin
        self.hardwareId = hardwareId.upper()
        self.guid = unicode(guid)
        self.callback = callback
        self.dataSize = dataSize
        self.suppressRepeat = suppressRepeat
        self.threadId = None


    def Open(self):
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
            raise self.plugin.Exceptions.DriverNotOpen


    def Close(self):
        self.dll.End(self.threadId)
        self.threadId = None
        eg.messageReceiver.RemoveWmUserHandler(self.MsgHandler)


    def MsgHandler(self, dummyHwnd, dummyMsg, dummyWParam, lParam):
        dataArray = cast(lParam, PUBYTE)
        value = tuple(dataArray[i] for i in range(self.dataSize))
        try:
            self.callback(value)
        except:
            eg.PrintTraceback(source=self.plugin)
        return 1



class WinUsb(object):

    def __init__(self, plugin):
        self.plugin = plugin
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
            suppressRepeat,
            self.plugin,
        )
        self.devices.append(device)


    def Open(self):
        devices = ListDevices()
        for device in self.devices:
            hardwareId = StripRevision(device.hardwareId)
            if not hardwareId in devices:
                raise self.plugin.Exceptions.DeviceNotFound
            deviceInfo = devices[hardwareId]
            if (
                deviceInfo.version != DRIVER_VERSION
                or deviceInfo.provider != DRIVER_PROVIDER
                or deviceInfo.name != device.name
            ):
                threading.Thread(target=self.InstallDriver).start()
                raise self.plugin.Exceptions.DriverNotFound
        for device in self.devices:
            device.Open()


    def Close(self):
        for device in self.devices:
            device.Close()


    @eg.LogIt
    def InstallDriver(self):
        platformDir = "x64" if IsWin64() else "x86"
        testPath = join(
            eg.mainDir, "drivers", "winusb", platformDir, "dpinst.exe"
        )
        if not os.path.exists(testPath):
            wx.CallAfter(self.ShowDownloadMessage)
            return

        res = eg.CallWait(
            wx.MessageBox,
            Text.installMsg % self.plugin.name,
            caption=Text.dialogCaption % self.plugin.name,
            style=wx.YES_NO | wx.ICON_QUESTION
        )
        if res == wx.NO:
            return
        devices = [
            dict(
                name=device.name,
                guid=device.guid,
                hardwareId=device.hardwareId,
            ) for device in self.devices
        ]
        ExecAs(
            __file__.decode(sys.getfilesystemencoding()),
            sys.getwindowsversion()[0] > 5 or not IsAdmin(),
            "InstallDriver",
            devices
        )


    def ShowDownloadMessage(self):
        if wx.YES == wx.MessageBox(
            Text.downloadMsg,
            caption=Text.dialogCaption % self.plugin.name,
            style=wx.YES_NO | wx.ICON_QUESTION
        ):
            import webbrowser
            webbrowser.open(
                (
                    "http://www.eventghost.org/downloads/"
                    "EventGhost WinUSB Add-on.exe"
                ),
                False
            )



def CreateInf(targetDir, devices):
    infPath = join(targetDir, "driver.inf")
    outfile = codecs.open(
        infPath,
        "wt",
        sys.getfilesystemencoding()
    )
    template = string.Template(HEADER)
    outfile.write(template.substitute(DRIVER_VERSION=DRIVER_VERSION))
    outfile.write("[Remotes.NTx86]\n")
    for i, device in enumerate(devices):
        outfile.write(
            "%%Device%i.DeviceDesc%%=Install%i,%s\n"
                % (i, i, device["hardwareId"])
        )
    outfile.write("\n[Remotes.NTamd64]\n")
    for i, device in enumerate(devices):
        outfile.write(
            "%%Device%i.DeviceDesc%%=Install%i,%s\n"
                % (i, i, device["hardwareId"])
        )
    template = string.Template(DEVICE_SECTION)
    for i, device in enumerate(devices):
        outfile.write(
            template.substitute(
                NR=i,
                GUID=device["guid"],
                DESCR=device["name"]
            )
        )
    template = string.Template(FOOTER)
    outfile.write(
        template.substitute(
            DRIVER_PROVIDER=DRIVER_PROVIDER,
            DISPLAY_NAME=devices[0]["name"],
        )
    )
    for i, device in enumerate(devices):
        outfile.write('Device%i.DeviceDesc="%s"\n' % (i, device["name"]))

    outfile.close()
    return infPath


def InstallDriver(devices):
    from subprocess import call

    platformDir = "x64" if IsWin64() else "x86"
    tmpDir = tempfile.mkdtemp()
    shutil.copytree(
        join(eg.mainDir, "drivers", "winusb", platformDir),
        join(tmpDir, platformDir)
    )
    CreateInf(join(tmpDir, platformDir), devices)
    res = call('"' + join(tmpDir, platformDir, "dpinst.exe") + '" /f /lm')
    shutil.rmtree(tmpDir)
    return res


def ListDevices():
    devices = {}
    guid = GUID()
    CLSIDFromString("{745a17a0-74d3-11d0-b6fe-00a0c90f57da}", byref(guid))
    hDevInfo = SetupDiGetClassDevs(
        guid,
        None,#"USB", # Enumerator
        0,
        DIGCF_PRESENT #| DIGCF_ALLCLASSES
    )
    if hDevInfo == INVALID_HANDLE_VALUE:
        raise WinError()
    deviceInfoData = SP_DEVINFO_DATA()
    deviceInfoData.cbSize = sizeof(SP_DEVINFO_DATA)
    driverInfoData = SP_DRVINFO_DATA()
    driverInfoData.cbSize = sizeof(SP_DRVINFO_DATA)
    deviceInstallParams = SP_DEVINSTALL_PARAMS()
    deviceInstallParams.cbSize = sizeof(SP_DEVINSTALL_PARAMS)

    buffersize = DWORD()
    buffersize.value = 1000
    dataType = DWORD()
    hardwareId = create_unicode_buffer(1000)
    i = 0
    while True:
        if not SetupDiEnumDeviceInfo(hDevInfo, i, byref(deviceInfoData)):
            err = GetLastError()
            if err == ERROR_NO_MORE_ITEMS:
                break
            else:
                raise WinError(err)
        i += 1
        if SetupDiGetDeviceRegistryProperty(
            hDevInfo,
            byref(deviceInfoData),
            SPDRP_HARDWAREID, #SPDRP_DEVICEDESC,
            None,
            None,
            0,
            byref(buffersize)
        ):
            raise WinError()
        err = GetLastError()
        if err == ERROR_INSUFFICIENT_BUFFER:
            hardwareId = create_unicode_buffer(buffersize.value / 2)
        elif err == ERROR_INVALID_DATA:
            continue
        else:
            raise WinError(err)
        if not SetupDiGetDeviceRegistryProperty(
            hDevInfo,
            byref(deviceInfoData),
            SPDRP_HARDWAREID, #SPDRP_DEVICEDESC,
            byref(dataType),
            cast(hardwareId, PBYTE),
            buffersize.value,
            byref(buffersize)
        ):
            raise WinError()
        hardwareId = StripRevision(hardwareId.value.upper())
        driverInfoData.DriverVersion = 0
        SetupDiGetDeviceInstallParams(
            hDevInfo,
            byref(deviceInfoData),
            byref(deviceInstallParams)
        )
        deviceInstallParams.FlagsEx |= DI_FLAGSEX_INSTALLEDDRIVER
        SetupDiSetDeviceInstallParams(
            hDevInfo,
            byref(deviceInfoData),
            byref(deviceInstallParams)
        )
        SetupDiBuildDriverInfoList(
            hDevInfo,
            byref(deviceInfoData),
            SPDIT_COMPATDRIVER
        )
        if not SetupDiEnumDriverInfo(
            hDevInfo,
            byref(deviceInfoData),
            SPDIT_COMPATDRIVER,
            0,
            byref(driverInfoData)
        ):
            raise WinError()
        version = driverInfoData.DriverVersion
        versionStr =  "%d.%d.%d.%d" % (
            (version >> 48) & 0xFFFF,
            (version >> 32) & 0xFFFF,
            (version >> 16) & 0xFFFF,
            version & 0xFFFF
        )
        devices[hardwareId] = eg.Bunch(
            name = driverInfoData.Description,
            version = versionStr,
            hardwareId = hardwareId,
            provider = driverInfoData.ProviderName,
        )
    return devices


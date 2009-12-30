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
import threading
import codecs
import hashlib
import Queue
from os.path import join, dirname
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

PLATFORM = "x64" if IsWin64() else "x86"
DOWNLOAD_ROOT = "http://www.eventghost.org/winusb/%s/" % PLATFORM
INSTALLATION_ROOT = join(
    eg.folderPath.ProgramData, "eventghost", "drivers", "winusb", PLATFORM
)

if PLATFORM == "x64":
    NEEDED_FILES = [
        ("DPInst.exe", "aa0a91227631a09cd075d315646fb7a9"),
        ("WdfCoInstaller01009.dll", "4da5da193e0e4f86f6f8fd43ef25329a"),
        ("WinUSBCoInstaller2.dll", "246900ce6474718730ecd4f873234cf5"),
        ("WUDFUpdate_01009.dll", "ebf9ee8a7671f3b260ed9b08fcee0cc5"),
    ]
else:
    NEEDED_FILES = [
        ("DPInst.exe", "e6213cec602f332bf8e868b7b8bf2bb1"),
        ("WdfCoInstaller01009.dll", "a9970042be512c7981b36e689c5f3f9f"),
        ("WinUSBCoInstaller2.dll", "8e7b9f81e8823fee2d82f7de3a44300b"),
        ("WUDFUpdate_01009.dll", "e1bbe9e3568cf54598e9a8d23697b67e"),
    ]



HEADER = r"""
; This file is automatically created by the EventGhost.
; Don't edit this file directly.

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
1=%DISK_NAME%,,,

[SourceDisksNames.amd64]
1=%DISK_NAME%,,,

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
        "EventGhost needs to download additional files before it "
        "can install the driver for the %s plugin.\n\n"
        "Do you want to start the download now?\n"
    )
    installMsg = (
        "You need to install the proper driver for this %s device.\n\n"
        "Should EventGhost start the driver installation for you now?"
    )
    restartMsg = (
        "EventGhost needs to restart, before it can use the new driver.\n\n"
        "Do you want to restart EventGhost now?"
    )
    downloadFailedMsg = (
        "The download failed!\n\nPlease try again later."
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
            eg.PrintTraceback(source=self.plugin.info.treeItem)
        return 1


class WinUsb(object):
    installQueue = Queue.Queue()
    installThreadLock = threading.Lock()
    installThread = None

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

                with self.installThreadLock:
                    self.installQueue.put(self)
                    if self.installThread is None:
                        self.__class__.installThread = threading.Thread(
                            target=self.InstallDriver
                        )
                        self.installThread.start()
                raise self.plugin.Exceptions.DriverNotFound
        for device in self.devices:
            device.Open()


    def Close(self):
        for device in self.devices:
            device.Close()


    @classmethod
    def InstallDriver(cls):
        restartNeeded = False
        while True:
            with cls.installThreadLock:
                if cls.installQueue.empty():
                    cls.installThread = None
                    if restartNeeded:
                        wx.CallAfter(self.ShowRestartMessage)
                    return
            self = cls.installQueue.get()
            if wx.YES != eg.CallWait(
                wx.MessageBox,
                Text.installMsg % self.plugin.name,
                caption=Text.dialogCaption % self.plugin.name,
                style=wx.YES_NO | wx.ICON_QUESTION | wx.STAY_ON_TOP,
                parent=eg.document.frame
            ):
                continue
            if not self.CheckAddOnFiles():
                continue
            self.CreateInf()
            myDir = dirname(__file__.decode(sys.getfilesystemencoding()))
            result = -1
            try:
                result = ExecAs(
                    "subprocess",
                    sys.getwindowsversion()[0] > 5 or not IsAdmin(),
                    "call",
                    '"%s" /f /lm' % join(INSTALLATION_ROOT, "dpinst.exe"),
                )
            except WindowsError, exc:
                #only silence "User abort"
                if exc.winerror != 1223:
                    raise
            if result == 1:
                restartNeeded = True


    def ShowRestartMessage(self):
        res = wx.MessageBox(
            Text.restartMsg,
            caption=eg.APP_NAME,
            style=wx.YES_NO | wx.ICON_QUESTION | wx.STAY_ON_TOP,
            parent=eg.document.frame
        )
        if res == wx.YES:
            eg.app.Restart()


    def ShowDownloadMessage(self):
        return wx.YES == wx.MessageBox(
            Text.downloadMsg % self.plugin.name,
            caption=Text.dialogCaption % self.plugin.name,
            style=wx.YES_NO | wx.ICON_QUESTION | wx.STAY_ON_TOP,
            parent=eg.document.frame
        )


    def GetNeededFiles(self):
        neededFiles = []
        for name, md5hash in NEEDED_FILES:
            path = join(INSTALLATION_ROOT, name)
            if not os.path.exists(path):
                neededFiles.append((DOWNLOAD_ROOT + name, path))
                continue
            md5 = hashlib.md5()
            md5.update(open(path, "rb").read())
            #print name, md5.hexdigest()
            if md5.hexdigest() != md5hash:
                neededFiles.append((DOWNLOAD_ROOT + name, path))
        return neededFiles


    def CheckAddOnFiles(self):
        neededFiles = self.GetNeededFiles()
        if len(neededFiles) == 0:
            return True
        if not eg.CallWait(self.ShowDownloadMessage):
            return False
        stopEvent = threading.Event()
        wx.CallAfter(eg.TransferDialog, None, neededFiles, stopEvent)
        stopEvent.wait()
        neededFiles = self.GetNeededFiles()
        if neededFiles:
            eg.CallWait(
                wx.MessageBox,
                Text.downloadFailedMsg,
                caption=Text.dialogCaption % self.plugin.name,
                style=wx.OK | wx.ICON_EXCLAMATION | wx.STAY_ON_TOP,
                parent=eg.document.frame
            )
            return False
        return True


    def CreateInf(self):
        infPath = join(INSTALLATION_ROOT, "driver.inf")
        try:
            os.makedirs(dirname(infPath))
        except:
            pass
        outfile = codecs.open(infPath, "wt", sys.getfilesystemencoding())
        template = string.Template(HEADER)
        outfile.write(template.substitute(DRIVER_VERSION=DRIVER_VERSION))
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
                template.substitute(
                    NR=i,
                    GUID=device.guid,
                    DESCR=device.name
                )
            )
        template = string.Template(FOOTER)
        outfile.write(
            template.substitute(
                DRIVER_PROVIDER=DRIVER_PROVIDER,
                DISPLAY_NAME=self.plugin.name,
            )
        )
        for i, device in enumerate(self.devices):
            outfile.write('Device%i.DeviceDesc="%s"\n' % (i, device.name))

        outfile.close()
        return infPath



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
            err = GetLastError()
            if err == ERROR_NO_MORE_ITEMS:
                devices[hardwareId] = eg.Bunch(
                    name = "<unknown name>",
                    version = "",
                    hardwareId = hardwareId,
                    provider = "<unknown provider",
                )
                continue
            else:
                raise WinError(err)
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


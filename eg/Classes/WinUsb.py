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

import codecs
import hashlib
import os
import Queue
import string
import threading
import wx
from ctypes import (
    addressof,
    byref,
    c_ubyte,
    cast,
    create_string_buffer,
    create_unicode_buffer,
    GetLastError,
    POINTER,
    sizeof,
    WinDLL,
    WinError,
    wstring_at,
)
from ctypes.wintypes import DWORD
from os.path import join, dirname

# Local imports
import eg
from eg.WinApi import IsWin64
from eg.WinApi.Dynamic import (
    CLSIDFromString,
    ERROR_NO_MORE_ITEMS,
    GUID,
    INVALID_HANDLE_VALUE,
    PBYTE,
)
from eg.WinApi.Dynamic.SetupApi import (
    DIGCF_ALLCLASSES,
    DIGCF_DEVICEINTERFACE,
    DIGCF_PRESENT,
    ERROR_INSUFFICIENT_BUFFER,
    PSP_DEVICE_INTERFACE_DETAIL_DATA,
    SetupDiBuildDriverInfoList,
    SetupDiEnumDeviceInfo,
    SetupDiEnumDeviceInterfaces,
    SetupDiEnumDriverInfo,
    SetupDiGetClassDevs,
    SetupDiGetDeviceInstallParams,
    SetupDiGetDeviceInterfaceDetail,
    SetupDiGetDeviceRegistryProperty,
    SetupDiSetDeviceInstallParams,
    SP_DEVICE_INTERFACE_DATA,
    SP_DEVICE_INTERFACE_DETAIL_DATA,
    SP_DEVINFO_DATA,
    SP_DEVINSTALL_PARAMS,
    SP_DRVINFO_DATA,
    SPDIT_COMPATDRIVER,
    SPDRP_HARDWAREID,
)
from eg.WinApi.IsAdmin import IsAdmin
from eg.WinApi.PipedProcess import ExecAs

DI_FLAGSEX_INSTALLEDDRIVER = 0x04000000

PUBYTE = POINTER(c_ubyte)

DRIVER_VERSION = "1.0.2.0"
DRIVER_PROVIDER = "EventGhost"
DRIVER_CLASS_GUID = "{FE050E98-31CD-47EA-AC39-CB143EF208B2}"
PLATFORM = "x64" if IsWin64() else "x86"
DOWNLOAD_ROOT = "http://www.eventghost.org/downloads/winusb/%s/" % PLATFORM
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
DriverVer=01/25/2010,$DRIVER_VERSION
DriverPackageDisplayName=%DisplayName%

; ========== Manufacturer/Models sections ===========

[Manufacturer]
%ProviderName%=Remotes,NTx86,NTamd64

"""

FOOTER = r"""
; ========== Global sections ===========

[Install]
Include=winusb.inf
Needs=WINUSB.NT

[Install.Services]
Include=winusb.inf
AddService=WinUSB,0x00000002,WinUSB_ServiceInstall

[Install.Wdf]
KmdfService=WINUSB, WinUsb_Install

[Install.CoInstallers]
AddReg=CoInstallers_AddReg
CopyFiles=CoInstallers_CopyFiles

[Install.HW]
AddReg=Dev_AddReg

[Dev_AddReg]
HKR,,DeviceInterfaceGUIDs,0x10000,"{FE050E98-31CD-47EA-AC39-CB143EF208B2}"
HKR,,"SystemWakeEnabled",0x00010001,1

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
        device = self.Device(callback, dataSize, suppressRepeat)
        device.AddHardwareId(name, hardwareId)
        return device

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
        hardwareIds = []
        names = []
        for device in self.devices:
            for hardwareId, name in device.hardwareIds:
                hardwareIds.append(hardwareId)
                names.append(name)

        outfile = codecs.open(infPath, "w", 'mbcs')
        template = string.Template(HEADER)
        outfile.write(template.substitute(DRIVER_VERSION=DRIVER_VERSION))
        outfile.write("[Remotes.NTx86]\n")
        for i, hardwareId in enumerate(hardwareIds):
            outfile.write(
                "%%Device%i.DeviceDesc%%=Install,%s\n" % (i, hardwareId)
            )
        outfile.write("\n[Remotes.NTamd64]\n")
        for i, hardwareId in enumerate(hardwareIds):
            outfile.write(
                "%%Device%i.DeviceDesc%%=Install,%s\n" % (i, hardwareId)
            )
        template = string.Template(FOOTER)
        outfile.write(
            template.substitute(
                DRIVER_PROVIDER=DRIVER_PROVIDER,
                DISPLAY_NAME=self.plugin.name,
            )
        )
        for i, name in enumerate(names):
            outfile.write('Device%i.DeviceDesc="%s"\n' % (i, name))

        outfile.close()
        return infPath

    def Device(self, callback, dataSize=1, suppressRepeat=False):
        device = UsbDevice(self, callback, dataSize, suppressRepeat)
        self.devices.append(device)
        return device

    @staticmethod
    def GetDeviceHardwareId(hDevInfo, deviceInfoData):
        buffersize = DWORD(0)
        dataType = DWORD()
        if SetupDiGetDeviceRegistryProperty(
            hDevInfo,
            byref(deviceInfoData),
            SPDRP_HARDWAREID,
            None,
            None,
            0,
            byref(buffersize)
        ):
            raise WinError()
        err = GetLastError()
        if err == ERROR_INSUFFICIENT_BUFFER:
            hardwareId = create_unicode_buffer(buffersize.value / 2)
        else:
            raise WinError(err)
        if not SetupDiGetDeviceRegistryProperty(
            hDevInfo,
            byref(deviceInfoData),
            SPDRP_HARDWAREID,
            byref(dataType),
            cast(hardwareId, PBYTE),
            buffersize.value,
            byref(buffersize)
        ):
            raise WinError()
        return StripRevision(hardwareId.value.upper())

    @staticmethod
    def GetDevicePaths():
        classGuid = GUID()
        CLSIDFromString(DRIVER_CLASS_GUID, byref(classGuid))
        hDevInfo = SetupDiGetClassDevs(
            classGuid, None, None, DIGCF_PRESENT | DIGCF_DEVICEINTERFACE
        )
        if hDevInfo == INVALID_HANDLE_VALUE:
            raise WinError()

        deviceInterfaceData = SP_DEVICE_INTERFACE_DATA()
        deviceInterfaceData.cbSize = sizeof(SP_DEVICE_INTERFACE_DATA)
        deviceInfoData = SP_DEVINFO_DATA()
        deviceInfoData.cbSize = sizeof(SP_DEVINFO_DATA)
        memberIndex = 0
        result = {}
        while True:
            if not SetupDiEnumDeviceInterfaces(
                hDevInfo,
                None,
                classGuid,
                memberIndex,
                byref(deviceInterfaceData)
            ):
                err = GetLastError()
                if err == ERROR_NO_MORE_ITEMS:
                    break
                else:
                    raise WinError(err)
            requiredSize = DWORD()
            SetupDiGetDeviceInterfaceDetail(
                hDevInfo,
                byref(deviceInterfaceData),
                None,
                0,
                byref(requiredSize),
                byref(deviceInfoData)
            )
            buf = create_string_buffer(requiredSize.value)
            pDiDetailData = cast(buf, PSP_DEVICE_INTERFACE_DETAIL_DATA)
            pDiDetailData.contents.cbSize = sizeof(
                SP_DEVICE_INTERFACE_DETAIL_DATA
            )
            SetupDiGetDeviceInterfaceDetail(
                hDevInfo,
                byref(deviceInterfaceData),
                pDiDetailData,
                requiredSize.value,
                byref(requiredSize),
                None
            )

            devicePath = wstring_at(addressof(pDiDetailData.contents) + 4)
            hardwareId = WinUsb.GetDeviceHardwareId(hDevInfo, deviceInfoData)
            result[hardwareId] = devicePath
            memberIndex += 1
        return result

    def GetNeededFiles(self):
        neededFiles = []
        for name, md5hash in NEEDED_FILES:
            path = join(INSTALLATION_ROOT, name)
            if not os.path.exists(path):
                neededFiles.append((DOWNLOAD_ROOT + name, path))
                continue
            md5 = hashlib.md5()
            md5.update(open(path, "rb").read())
            if md5.hexdigest() != md5hash:
                neededFiles.append((DOWNLOAD_ROOT + name, path))
        return neededFiles

    @classmethod
    def InstallDriver(cls):
        while True:
            with cls.installThreadLock:
                if cls.installQueue.empty():
                    cls.installThread = None
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
            result = -1
            cmdLine = '"%s" /f /lm' % join(INSTALLATION_ROOT, "dpinst.exe")
            try:
                result = ExecAs(
                    "subprocess",
                    eg.WindowsVersion >= 'Vista' or not IsAdmin(),
                    "call",
                    cmdLine.encode('mbcs'),
                )
            except WindowsError, exc:
                #only silence "User abort"
                if exc.winerror != 1223:
                    raise
            if result == 1:
                eg.actionThread.Call(self.plugin.info.Start)

    @staticmethod
    def ListDevices():
        devices = {}
        guid = GUID()
        CLSIDFromString("{A5DCBF10-6530-11D2-901F-00C04FB951ED}", byref(guid))
        hDevInfo = SetupDiGetClassDevs(
            guid,
            "USB",  # Enumerator
            0,
            DIGCF_PRESENT | DIGCF_ALLCLASSES
        )
        if hDevInfo == INVALID_HANDLE_VALUE:
            raise WinError()
        deviceInfoData = SP_DEVINFO_DATA()
        deviceInfoData.cbSize = sizeof(SP_DEVINFO_DATA)
        driverInfoData = SP_DRVINFO_DATA()
        driverInfoData.cbSize = sizeof(SP_DRVINFO_DATA)
        deviceInstallParams = SP_DEVINSTALL_PARAMS()
        deviceInstallParams.cbSize = sizeof(SP_DEVINSTALL_PARAMS)

        i = 0
        while True:
            if not SetupDiEnumDeviceInfo(hDevInfo, i, byref(deviceInfoData)):
                err = GetLastError()
                if err == ERROR_NO_MORE_ITEMS:
                    break
                else:
                    raise WinError(err)
            i += 1
            hardwareId = WinUsb.GetDeviceHardwareId(hDevInfo, deviceInfoData)
            if hardwareId.startswith("USB\\ROOT_HUB"):
                continue
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
                    devices[hardwareId] = DeviceInfo(
                        name = "<unknown name>",
                        version = "",
                        hardwareId = hardwareId,
                        provider = "<unknown provider",
                    )
                    continue
                else:
                    raise WinError(err)
            version = driverInfoData.DriverVersion
            versionStr = "%d.%d.%d.%d" % (
                (version >> 48) & 0xFFFF,
                (version >> 32) & 0xFFFF,
                (version >> 16) & 0xFFFF,
                version & 0xFFFF
            )
            devices[hardwareId] = DeviceInfo(
                driverInfoData.Description,
                versionStr,
                hardwareId,
                driverInfoData.ProviderName,
            )
        return devices

    def ShowDownloadMessage(self):
        return wx.YES == wx.MessageBox(
            Text.downloadMsg % self.plugin.name,
            caption=Text.dialogCaption % self.plugin.name,
            style=wx.YES_NO | wx.ICON_QUESTION | wx.STAY_ON_TOP,
            parent=eg.document.frame
        )

    def ShowRestartMessage(self):
        res = wx.MessageBox(
            Text.restartMsg,
            caption=eg.APP_NAME,
            style=wx.YES_NO | wx.ICON_QUESTION | wx.STAY_ON_TOP,
            parent=eg.document.frame
        )
        if res == wx.YES:
            eg.app.Restart()

    def Start(self):
        installedHardware = self.ListDevices()
        for device in self.devices:
            for hardwareId, name in device.hardwareIds:
                if hardwareId in installedHardware:
                    break
            else:
                raise self.plugin.Exceptions.DeviceNotFound
            deviceInfo = installedHardware[hardwareId]
            if (
                deviceInfo.version != DRIVER_VERSION or
                deviceInfo.provider != DRIVER_PROVIDER or
                deviceInfo.name != name
            ):
                self.StartInstall()
                raise self.plugin.Exceptions.DriverNotFound
        for device in self.devices:
            device.Start()
    Open = Start

    def StartInstall(self):
        with self.installThreadLock:
            self.installQueue.put(self)
            if self.installThread is None:
                self.__class__.installThread = threading.Thread(
                    target=self.InstallDriver
                )
                self.installThread.start()

    def Stop(self):
        for device in self.devices:
            device.Stop()
    Close = Stop


class DeviceInfo(object):
    def __init__(self, name, version, hardwareId, provider):
        self.name = name
        self.version = version
        self.hardwareId = hardwareId
        self.provider = provider

    def __repr__(self):
        return "DeviceInfo(%r, %r, %r, %r)" % (
            self.name, self.version, self.hardwareId, self.provider
        )


class UsbDevice(object):
    dll = None

    def __init__(self, winUsb, callback, dataSize, suppressRepeat):
        self.winUsb = winUsb
        self.callback = callback
        self.dataSize = dataSize
        self.suppressRepeat = suppressRepeat
        self.threadId = None
        self.hardwareIds = []

    def AddHardwareId(self, name, *hardwareIds):
        for hardwareId in hardwareIds:
            hardwareId = StripRevision(hardwareId.upper())
            self.hardwareIds.append((hardwareId, name))
        return self

    def FindDevicePath(self):
        installedDevices = WinUsb.GetDevicePaths()
        for hardwareId, _ in self.hardwareIds:
            if hardwareId in installedDevices:
                return installedDevices[hardwareId]
        raise self.winUsb.plugin.Exceptions.DeviceNotFound

    def MsgHandler(self, dummyHwnd, dummyMsg, dummyWParam, lParam):
        dataArray = cast(lParam, PUBYTE)
        value = tuple(dataArray[i] for i in range(self.dataSize))
        try:
            self.callback(value)
        except:
            eg.PrintTraceback(source=self.winUsb.plugin.info.treeItem)
        return 1

    def Start(self):
        if self.dll is None:
            self.__class__.dll = WinDLL(
                join(eg.sitePackagesDir, "WinUsbWrapper.dll").encode('mbcs')
            )
        msgId = eg.messageReceiver.AddWmUserHandler(self.MsgHandler)
        devicePath = self.FindDevicePath()
        self.threadId = self.dll.Start(
            eg.messageReceiver.hwnd,
            msgId,
            devicePath,
            self.dataSize,
            int(self.suppressRepeat)
        )
        if not self.threadId:
            raise self.winUsb.plugin.Exceptions.DriverNotOpen

    def Stop(self):
        self.dll.Stop(self.threadId)
        self.threadId = None
        eg.messageReceiver.RemoveWmUserHandler(self.MsgHandler)


def StripRevision(hardwareId):
    return "&".join(
        part for part in hardwareId.split("&") if not part.startswith("REV_")
    )

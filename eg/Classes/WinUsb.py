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
from ctypes import (
    Structure,
    WINFUNCTYPE,
    WinDLL,
    c_ubyte,
    c_int,
    c_wchar_p,
    c_void_p,
    byref,
    POINTER,
    cast,
    FormatError,
    GetLastError,
)
from ctypes.wintypes import DWORD, BOOL

import eg
from eg.WinApi.PipedProcess import ExecAsAdministrator

PCWSTR = c_wchar_p
PWSTR = c_wchar_p
PVOID = c_void_p

# values for enumeration 'DIFXAPI_LOG'
DIFXAPI_SUCCESS = 0
DIFXAPI_INFO = 1
DIFXAPI_WARNING = 2
DIFXAPI_ERROR = 3
DIFXAPI_LOG = c_int # enum

DRIVER_PACKAGE_FORCE = 4
DRIVER_PACKAGE_LEGACY_MODE = 0x10

class INSTALLERINFO(Structure):
    _fields_ = [
        ('pApplicationId', PWSTR),
        ('pDisplayName', PWSTR),
        ('pProductName', PWSTR),
        ('pMfgName', PWSTR),
    ]
PCINSTALLERINFO = POINTER(INSTALLERINFO)

_difxapi = WinDLL("DIFxAPI.dll")

DIFLOGCALLBACK = WINFUNCTYPE(None, DIFXAPI_LOG, DWORD, PCWSTR, PVOID)
SetDifxLogCallback = _difxapi.SetDifxLogCallbackW
SetDifxLogCallback.restype = None
SetDifxLogCallback.argtypes = [DIFLOGCALLBACK, PVOID]

DriverPackageInstall = _difxapi.DriverPackageInstallW
DriverPackageInstall.restype = DWORD
DriverPackageInstall.argtypes = [PCWSTR, DWORD, PCINSTALLERINFO, POINTER(BOOL)]


PUBYTE = POINTER(c_ubyte)

DRIVER_VERSION = "1.0.1.2"
DRIVER_PROVIDER = "EventGhost"

HEADER = r"""\
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
ProviderName="$DRIVER_PROVIDER"
WinUSB_SvcDesc="WinUSB Driver"
DISK_NAME="My Install Disk"
DisplayName="USB Remote Driver"
"""

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
            suppressRepeat
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
                self.InstallDriver()
                break
        for device in self.devices:
            device.Start()


    def Close(self):
        for device in self.devices:
            device.Close()


    def InstallDriver(self):
        import wx
        res = eg.CallWait(
            wx.MessageBox,
            (
                "You need to install the proper driver for this %s device.\n\n"
                "Should EventGhost install the driver for you now?"
            ) % self.plugin.name,
            caption="EventGhost",
            style=wx.YES_NO | wx.ICON_QUESTION
        )
        if res == wx.NO:
            raise self.plugin.Exceptions.DriverNotFound
        infPath = join(eg.configDir, self.devices[0].guid + ".inf")
        outfile = codecs.open(
            infPath,
            "wt",
            sys.getfilesystemencoding()
        )
        template = string.Template(HEADER)
        outfile.write(
            template.substitute(DRIVER_VERSION=DRIVER_VERSION)
        )
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
        template = string.Template(FOOTER)
        outfile.write(
            template.substitute(DRIVER_PROVIDER=DRIVER_PROVIDER)
        )
        for i, device in enumerate(self.devices):
            outfile.write('Device%i.DeviceDesc="%s"\n' % (i, device.name))

        outfile.close()
        try:
            needsReboot = ExecAsAdministrator(
                __file__.decode(sys.getfilesystemencoding()),
                "InstallDriver",
                infPath
            )
        except WindowsError, exc:
            if exc.winerror == 1223:
                # user cancelled driver installation
                raise self.plugin.Exceptions.DriverNotFound

        if needsReboot:
            eg.CallWait(
                eg.MessageBox,
                "You need to restart the computer, before the driver will work."
            )



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
    return needsReboot.value


def FailedFunc(funcName):
    errCode = GetLastError()
    return WindowsError(
        errCode,
        "%s: %s" % (funcName, FormatError(errCode))
    )


from eg.WinApi.Dynamic import (
    sizeof,
    SetupDiGetClassDevs,
    DIGCF_PRESENT,
    DIGCF_ALLCLASSES,
    SP_DEVINFO_DATA,
    SetupDiGetDeviceRegistryProperty,
    SetupDiEnumDeviceInfo,
    SPDRP_DEVICEDESC,
    PBYTE,
    ERROR_INSUFFICIENT_BUFFER,
    create_unicode_buffer,
    SPDRP_HARDWAREID,
    ERROR_INVALID_DATA,
    INVALID_HANDLE_VALUE,
    CLSIDFromString,
    GUID,
    SPDRP_DRIVER,
    SetupDiGetSelectedDriver,
    SP_DRVINFO_DATA,
    SPDIT_CLASSDRIVER,
    SetupDiEnumDriverInfo,
    SPDIT_COMPATDRIVER,
    SetupDiBuildDriverInfoList,
    SP_DEVINSTALL_PARAMS,
    SetupDiSetDeviceInstallParams,
    SetupDiGetDeviceInstallParams,
    #DI_FLAGSEX_INSTALLEDDRIVER,
    SetupDiOpenDeviceInfo,
    DIGCF_DEVICEINTERFACE,
)
DI_FLAGSEX_INSTALLEDDRIVER = 0x04000000


def ListDevices():
    devices = {}
    guid = GUID()
    CLSIDFromString("{745a17a0-74d3-11d0-b6fe-00a0c90f57da}", byref(guid))
    hDevInfo = SetupDiGetClassDevs(
        guid,
        "USB", # Enumerator
        0,
        DIGCF_PRESENT #| DIGCF_ALLCLASSES
    )
    if hDevInfo == INVALID_HANDLE_VALUE:
        raise FailedFunc("SetupDiGetClassDevs")
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
    for i in range(0, 100000):
        if not SetupDiEnumDeviceInfo(hDevInfo, i, byref(deviceInfoData)):
            break
        if SetupDiGetDeviceRegistryProperty(
            hDevInfo,
            byref(deviceInfoData),
            SPDRP_HARDWAREID, #SPDRP_DEVICEDESC,
            None,
            None,
            0,
            byref(buffersize)
        ):
            raise FailedFunc("SetupDiGetDeviceRegistryProperty")
        err = GetLastError()
        if err == ERROR_INSUFFICIENT_BUFFER:
            hardwareId = create_unicode_buffer(buffersize.value / 2)
        elif err == ERROR_INVALID_DATA:
            continue
        else:
            raise WindowsError(err, FormatError(err))
        if not SetupDiGetDeviceRegistryProperty(
            hDevInfo,
            byref(deviceInfoData),
            SPDRP_HARDWAREID, #SPDRP_DEVICEDESC,
            byref(dataType),
            cast(hardwareId, PBYTE),
            buffersize.value,
            byref(buffersize)
        ):
            raise FailedFunc("SetupDiGetDeviceRegistryProperty")
        hardwareId = StripRevision(hardwareId.value)
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
            print err, FormatError(err)
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


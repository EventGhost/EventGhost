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

# ____Changes By K                            2/21/2017 21:07 -7
# Added support for more device types         2/21/2017 21:07 -7
# Added support for device metrics in payload 2/21/2017 21:07 -7
# Added support for device names in the event 2/21/2017 21:07 -7

import win32com.client
import fnmatch
import wx
import sys
import os
import threading
import platform
from wx.lib import iewin_old

# Local imports
import eg
from eg.WinApi.Dynamic import (
    CLSIDFromString,
    DBT_DEVICEARRIVAL,
    DBT_DEVICEREMOVECOMPLETE,
    DBT_DEVTYP_DEVICEINTERFACE,
    DBT_DEVTYP_VOLUME,
    DEV_BROADCAST_DEVICEINTERFACE,
    DEV_BROADCAST_HDR,
    DEV_BROADCAST_VOLUME,
    pointer,
    RegisterDeviceNotification,
    sizeof,
    UnregisterDeviceNotification,
    WM_DEVICECHANGE,
    wstring_at,
    byref,
    oledll,
    c_wchar_p,
    windll
)

if platform.version() in ('5.2', '5.1'):
    WIN_XP = True
else:
    WIN_XP = False

del platform

DEVICE_NOTIFY_ALL_INTERFACE_CLASSES = 0x00000004

# XP and later
BUS1394_CLASS_GUID = '{6BDD1FC1-810F-11D0-BEC7-08002BE2092F}'
KSCATEGORY_AUDIO = '{6994AD04-93EF-11D0-A3CC-00A0C9223196}'
KSCATEGORY_BDA_NETWORK_EPG = '{71985F49-1CA1-11D3-9CC8-00C04F7971E0}'
KSCATEGORY_BDA_NETWORK_TUNER = '{71985F48-1CA1-11D3-9CC8-00C04F7971E0}'
KSCATEGORY_TVTUNER = '{A799A800-A46D-11D0-A18C-00A02401DCD4}'
GUID_61883_CLASS = '{7EBEFBC0-3200-11D2-B4C2-00A0C9697D07}'
GUID_DEVICE_BATTERY = '{72631E54-78A4-11D0-BCF7-00AA00B7B32A}'
GUID_BTHPORT_DEVICE_INTERFACE = '{0850302A-B344-4FDA-9BE9-90576B8D46F0}'
GUID_DEVINTERFACE_WPD = '{6AC27878-A6FA-4155-BA85-F98F491D4F33}'
GUID_DEVINTERFACE_USB_HUB = '{F18A0E88-C30C-11D0-8815-00A0C906BED8}'
GUID_DEVINTERFACE_USB_DEVICE = '{A5DCBF10-6530-11D2-901F-00C04FB951ED}'
GUID_DEVINTERFACE_PARCLASS = '{811FC6A5-F728-11D0-A537-0000F8753ED1}'
GUID_DEVINTERFACE_PARALLEL = '{97F76EF0-F883-11D0-AF1F-0000F800845C}'
GUID_DEVINTERFACE_COMPORT = '{86E0D1E0-8089-11D0-9CE4-08003E301F73}'
GUID_DEVINTERFACE_MODEM = '{2C7089AA-2E0E-11D1-B114-00C04FC2AAE4}'
GUID_DEVINTERFACE_MOUSE = '{378DE44C-56EF-11D1-BC8C-00A0C91405DD}'
GUID_DEVINTERFACE_KEYBOARD = '{884B96C3-56EF-11D1-BC8C-00A0C91405DD}'
GUID_DEVINTERFACE_HID = '{4D1E55B2-F16F-11CF-88CB-001111000030}'
GUID_DEVINTERFACE_MONITOR = '{E6F07B5F-EE97-4A90-B076-33F57BF4EAA7}'
GUID_DEVINTERFACE_IMAGE = '{6BDD1FC6-810F-11D0-BEC7-08002BE2092F}'
GUID_DEVINTERFACE_DISPLAY_ADAPTER = '{5B45201D-F2F2-4F3B-85BB-30FF1F953599}'
GUID_DEVINTERFACE_CDROM = '{53F56308-B6BF-11D0-94F2-00A0C91EFB8B}'
GUID_DEVINTERFACE_DISK = '{53F56307-B6BF-11D0-94F2-00A0C91EFB8B}'
GUID_DEVINTERFACE_FLOPPY = '{53F56311-B6BF-11D0-94F2-00A0C91EFB8B}'
GUID_DEVINTERFACE_STORAGEPORT = '{2ACCFE60-C130-11D2-B082-00A0C91EFB8B}'
GUID_DEVINTERFACE_TAPE = '{53F5630B-B6BF-11D0-94F2-00A0C91EFB8B}'
GUID_DEVCLASS_IRDA = '{6BDD1fC5-810F-11D0-BEC7-08002BE2092F}'
GUID_DEVCLASS_SYSTEM = ' {4D36E97D-E325-11CE-BFC1-08002BE10318}'
GUID_DEVCLASS_PRINTERS = '{4D36E979-E325-11CE-BFC1-08002BE10318}'
GUID_DEVCLASS_PCMCIA = '{4D36E977-E325-11CE-BFC1-08002BE10318}'

KSCATEGORY_CAPTURE = '{65E8773D-8F56-11D0-A3B9-00A0C9223196}'
KSCATEGORY_VIDEO = '{6994AD05-93EF-11D0-A3CC-00A0C9223196}'
KSCATEGORY_STILL = '{FB6C428A-0353-11D1-905F-0000C0CC16BA}'
GUID_DEVINTERFACE_WRITEONCEDISK = ( # Blank CD/DVD insertion
    '{53F5630C-B6BF-11D0-94F2-00A0C91EFB8B}'
)
GUID_DEVINTERFACE_USB_HOST_CONTROLLER = (
    '{3ABF6F2D-71C4-462A-8A92-1E6861E6AF27}'
)
GUID_DEVINTERFACE_SERENUM_BUS_ENUMERATOR = ( # S Dev
    '{4D36E978-E325-11CE-BFC1-08002BE10318}'
)

MOUNTDEV_MOUNTED_DEVICE_GUID = '{53F5630D-B6BF-11D0-94F2-00A0C91EFB8B}'
# Vista and later
GUID_DEVINTERFACE_NET = '{CAC88484-7515-4C03-82E6-71A87ABAC361}'
GUID_DEVINTERFACE_I2C = '{2564AA4F-DDDB-4495-B497-6AD4A84163D7}'
GUID_DEVINTERFACE_PHYSICALMEDIA = '{F33FDC04-D1AC-4E8E-9A30-19BBD4B108AE}'

DEVICES = {
    GUID_DEVINTERFACE_KEYBOARD: (
        dict(
            cls_name='Keyboard',
            attr_names=(),
            url_id=394166,
            action_search='Description',
            display_name='Keyboard'
        ),
    ),
    GUID_DEVICE_BATTERY: (
        dict(
            cls_name='Battery',
            attr_names=(
                'BatteryRechargeTime',
                'EstimatedChargeRemaining',
                'ExpectedBatteryLife',
                'FullChargeCapacity',
                'MaxRechargeTime'
            ),
            url_id=394074,
            action_search='Caption',
            display_name='Battery'
        ),
        dict(
            cls_name='PortableBattery',
            attr_names=(
                'DesignVoltage',
                'DesignCapacity',
                'ExpectedBatteryLife',
                'EstimatedRunTime',
                'ExpectedLife',
                'Manufacturer',
                'ManufactureDate',
                'TimeOnBattery',
                'MaxRechargeTime'
            ),
            url_id=394357,
            action_search='Caption',
            display_name='Portable Battery'
        ),
    ),
    GUID_DEVINTERFACE_CDROM: (
        dict(
            cls_name='CDROMDrive',
            attr_names=(
                'CompressionMethod',
                'Drive',
                'Manufacturer',
                'MaxMediaSize',
                'MediaLoaded',
                'MediaType'
            ),
            url_id=394081,
            action_search='Caption',
            display_name='CD-ROM Drive'
        ),
    ),
    GUID_DEVINTERFACE_MONITOR: (
        dict(
            cls_name='DesktopMonitor',
            attr_names=(
                'DisplayType',
                'MonitorManufacturer',
                'MonitorType',
                'ScreenWidth',
                'ScreenHeight'
            ),
            url_id=394122,
            action_search='Caption',
            display_name='Desktop Monitor'
        ),
    ),
    GUID_DEVINTERFACE_DISK: (
        dict(
            cls_name='DiskDrive',
            attr_names=(
                'Model',
                'Manufacturer',
                'InterfaceType',
                'Partitions',
                'MediaLoaded',
                'MediaType',
                'Size'
            ),
            url_id=394132,
            action_search='Caption',
            display_name='Disk Drive'
        ),
        dict(
            cls_name='IDEController',
            attr_names=(),
            url_id=394155,
            action_search='Caption',
            display_name='IDE Controller'
        ),
        dict(
            cls_name='SCSIController',
            attr_names=('Manufacturer',),
            url_id=394400,
            action_search='Caption',
            display_name='SCSI Controller'
        ),
    ),
    GUID_DEVINTERFACE_FLOPPY: (
        dict(
            cls_name='FloppyDrive',
            attr_names=(
                'Manufacturer',
            ),
            url_id=394149,
            action_search='Caption',
            display_name='Floppy Drive'
        ),
        dict(
            cls_name='FloppyController',
            attr_names=(),
            url_id=394148,
            action_search='Caption',
            display_name='Floppy Controller'
        )
    ),
    GUID_DEVINTERFACE_USB_HOST_CONTROLLER: (
        dict(
            cls_name='USBController',
            attr_names=('Manufacturer',),
            url_id=394504,
            action_search='Caption',
            display_name='USB Controller'
        ),
    ),
    GUID_DEVINTERFACE_USB_HUB: (
        dict(
            cls_name='USBHub',
            attr_names=('USBVersion',),
            url_id=394506,
            action_search='Caption',
            display_name='USB Hub'
        ),
    ),
    GUID_DEVINTERFACE_DISPLAY_ADAPTER: (
        dict(
            cls_name='VideoController',
            attr_names=(
                'VideoProcessor',
                'AdapterRAM',
                'CurrentHorizontalResolution',
                'CurrentVerticalResolution'
            ),
            url_id=394512,
            action_search='Caption',
            display_name='Video Controller'
        ),
    ),
    GUID_DEVINTERFACE_TAPE: (
        dict(
            cls_name='TapeDrive',
            attr_names=(
                'Manufacturer',
                'MediaType',
                'MaxMediaSize'
            ),
            url_id=394491,
            action_search='Caption',
            display_name='Tape Drive'
        ),
    ),
    KSCATEGORY_AUDIO: (
        dict(
            cls_name='SoundDevice',
            attr_names=('Manufacturer', 'ProductName'),
            url_id=394463,
            action_search='Caption',
            display_name='Sound Device'
        ),
    ),
    GUID_DEVINTERFACE_COMPORT: (
        dict(
            cls_name='SerialPort',
            attr_names=(),
            url_id=394413,
            action_search='Caption',
            display_name='Serial Port'
        ),
    ),
    GUID_DEVINTERFACE_MOUSE: (
        dict(
            cls_name='PointingDevice',
            attr_names=(
                'Manufacturer',
                'NumberOfButtons',
                'Resolution',
                'SampleRate',
                'HardwareType'
            ),
            url_id=394356,
            action_search='Caption',
            display_name='Pointing Device'
        ),
    ),
    GUID_DEVINTERFACE_MODEM: (
        dict(
            cls_name='POTSModem',
            attr_names=(),
            url_id=394360,
            action_search='Caption',
            display_name='POTS Modem'
        ),
    ),
    GUID_DEVINTERFACE_PARALLEL: (
        dict(
            cls_name='ParallelPort',
            attr_names=(),
            url_id=394247,
            action_search='Caption',
            display_name='Parallel Port'
        ),
    ),
    BUS1394_CLASS_GUID: (
        dict(
            cls_name='1394Controller',
            attr_names=(),
            url_id=394059,
            action_search='Caption',
            display_name='1394 Controller'
        ),
    ),
    GUID_61883_CLASS: (
        dict(
            cls_name='1394ControllerDevice',
            attr_names=(),
            url_id=394060,
            action_search='Caption',
            display_name='1394 Controller Device'
        ),
    ),
    GUID_DEVCLASS_IRDA: (
        dict(
            cls_name='InfraredDevice',
            attr_names=(),
            url_id=394158,
            action_search='Caption',
            display_name='Infrared Device'
        ),
    ),
    GUID_DEVCLASS_SYSTEM: (
        dict(
            cls_name='MotherboardDevice',
            attr_names=(),
            url_id=394204,
            action_search='Name',
            display_name='Motherboard Device'
        ),
        dict(
            cls_name='CacheMemory',
            attr_names=(),
            url_id=394080,
            action_search='DeviceID',
            display_name='Cache Memory'
        ),
        dict(
            cls_name='Fan',
            attr_names=(),
            url_id=394146,
            action_search='Caption',
            display_name='Fan'
        ),
        dict(
            cls_name='HeatPipe',
            attr_names=(),
            url_id=394154,
            action_search='Caption',
            display_name='Heat Pipe'
        ),
        dict(
            cls_name='OnBoardDevice',
            attr_names=(),
            url_id=394238,
            action_search='Caption',
            display_name='OnBoard Device'
        ),
        dict(
            cls_name='PhysicalMemory',
            attr_names=(),
            url_id=394347,
            action_search='Tag',
            display_name='Physical Memory'
        ),
        dict(
            cls_name='Refrigeration',
            attr_names=(),
            url_id=394393,
            action_search='Caption',
            display_name='Refrigeration'
        ),
        dict(
            cls_name='SystemSlot',
            attr_names=(),
            url_id=394486,
            action_search='SlotDesignation',
            display_name='System Slot'
        ),
        dict(
            cls_name='TemperatureProbe',
            attr_names=(),
            url_id=394493,
            action_search='Caption',
            display_name='Temperature Probe'
        ),
        dict(
            cls_name='VoltageProbe',
            attr_names=(),
            url_id=394514,
            action_search='Caption',
            display_name='Voltage Probe'
        ),
        dict(
            cls_name='Processor',
            attr_names=(),
            url_id=394373,
            action_search='Name',
            display_name='Processor'
        )
    ),
    GUID_DEVCLASS_PCMCIA: (
        dict(
            cls_name='PCMCIAController',
            attr_names=(),
            url_id=394251,
            action_search='Caption',
            display_name='PCMCIA Controller'
        ),
    ),
    GUID_DEVCLASS_PRINTERS: (
        dict(
            cls_name='Printer',
            attr_names=(),
            url_id=394363,
            action_search='Caption',
            display_name='Printer'
        ),
        dict(
            cls_name='TCPIPPrinterPort',
            attr_names=(),
            url_id=394492,
            action_search='Caption',
            display_name='TCPIP PrinterPort'
        ),
        dict(
            cls_name='PrinterController',
            attr_names=(),
            url_id=394365,
            action_search='Caption',
            display_name='Printer Controller'
        )
    ),
    KSCATEGORY_BDA_NETWORK_EPG: (
        dict(
            cls_name='PNPEntity',
            attr_names=(),
            url_id=394353,
            action_search='Caption',
            display_name='EPG'
        ),
    ),
    KSCATEGORY_BDA_NETWORK_TUNER: (
        dict(
            cls_name='PNPEntity',
            attr_names=(),
            url_id=394353,
            action_search='Caption',
            display_name='Network Tuner'
        ),
    ),
    KSCATEGORY_TVTUNER: (
        dict(
            cls_name='PNPEntity',
            attr_names=(),
            url_id=394353,
            action_search='Caption',
            display_name='TV Tuner'
        ),
    ),
    GUID_BTHPORT_DEVICE_INTERFACE: (
        dict(
            cls_name='PNPEntity',
            attr_names=(),
            url_id=394353,
            action_search='Caption',
            display_name='BlueTeeth'
        ),
    ),
    GUID_DEVINTERFACE_WPD: (
        dict(
            cls_name='PNPEntity',
            attr_names=(),
            url_id=394353,
            action_search='Caption',
            display_name='Portable'
        ),
    ),

    GUID_DEVINTERFACE_USB_DEVICE: (
        dict(
            cls_name='PNPEntity',
            attr_names=(),
            url_id=394353,
            action_search='Caption',
            display_name='USB'
        ),
    ),
    GUID_DEVINTERFACE_HID: (
        dict(
            cls_name='PNPEntity',
            attr_names=(),
            url_id=394353,
            action_search='Caption',
            display_name='HID'
        ),
    ),
    GUID_DEVINTERFACE_IMAGE: (
        dict(
            cls_name='PNPEntity',
            attr_names=(),
            url_id=394353,
            action_search='Caption',
            display_name='Image Capture'
        ),
    ),
    KSCATEGORY_CAPTURE: (
        dict(
            cls_name='PNPEntity',
            attr_names=(),
            url_id=394353,
            action_search='Caption',
            display_name='Video Capture'
        ),
    ),
    KSCATEGORY_VIDEO: (
        dict(
            cls_name='PNPEntity',
            attr_names=(),
            url_id=394353,
            action_search='Caption',
            display_name='Video'
        ),
    ),
    KSCATEGORY_STILL: (
        dict(
            cls_name='PNPEntity',
            attr_names=(),
            url_id=394353,
            action_search='Caption',
            display_name='Still Capture'
        ),
    ),
}

if not WIN_XP:
    DEVICES[GUID_DEVINTERFACE_DISK][0]['attr_names'] += (
        'FirmwareRevision',
    )
    DEVICES[GUID_DEVINTERFACE_I2C] = (
        dict(
            cls_name='PNPEntity',
            attr_names=(),
            url_id=394353,
            action_search='Caption',
            display_name='I2C'
        ),
    )
    DEVICES[GUID_DEVINTERFACE_NET] = (
        dict(
            cls_name='NetworkAdapter',
            attr_names=(
                'AdapterType',
                'MACAddress',
                'Manufacturer',
                'MaxSpeed',
                'NetworkAddresses'
            ),
            url_id=394216,
            action_search='Description',
            display_name='Network Adapter'
        ),
    )

SEARCH = [
    GUID_DEVINTERFACE_KEYBOARD,
    GUID_DEVICE_BATTERY,
    GUID_DEVINTERFACE_CDROM,
    GUID_DEVINTERFACE_MONITOR,
    GUID_DEVINTERFACE_DISK,
    GUID_DEVINTERFACE_FLOPPY,
    GUID_DEVINTERFACE_USB_HOST_CONTROLLER,
    GUID_DEVINTERFACE_USB_HUB,
    GUID_DEVINTERFACE_DISPLAY_ADAPTER,
    GUID_DEVINTERFACE_TAPE,
    KSCATEGORY_AUDIO,
    GUID_DEVINTERFACE_COMPORT,
    GUID_DEVINTERFACE_MOUSE,
    GUID_DEVINTERFACE_MODEM,
    GUID_DEVINTERFACE_PARALLEL,
    BUS1394_CLASS_GUID,
    GUID_61883_CLASS,
    GUID_DEVCLASS_IRDA,
    GUID_DEVCLASS_SYSTEM,
    GUID_DEVCLASS_PCMCIA,
    GUID_DEVCLASS_PRINTERS,
    GUID_DEVINTERFACE_USB_DEVICE,
]


class DEV_BROADCAST_DEVICEINTERFACE(DEV_BROADCAST_DEVICEINTERFACE):
    def __init__(self):
        self.dbcc_devicetype = DBT_DEVTYP_DEVICEINTERFACE
        self.dbcc_size = sizeof(DEV_BROADCAST_DEVICEINTERFACE)

DBD_NAME_OFFSET = DEV_BROADCAST_DEVICEINTERFACE.dbcc_name.offset

ASSOCIATORS = (
    'ASSOCIATORS OF {Win32_%s.DeviceID="%s"}'
    ' WHERE AssocClass=Win32_%s'
)


class WMI(threading.Thread):

    def __init__(self, plugin):
        threading.Thread.__init__(self, name='WMI Thread')
        self.plugin = plugin
        self.wmi = None
        self.queueEvent = threading.Event()
        self.stopEvent = threading.Event()
        self.queue = []
        self.driveQueue = []
        self.currentDevices = {}
        self.networkDrives = {}
        self.localDrives = {}
        self.cdromDrives = {}
        self.wmiDevices = []
        self.wmi = None

    def GetDrives(self):
        logicalDisks = self.wmi.ExecQuery(
            "Select * from Win32_LogicalDisk"
        )

        for disk in logicalDisks:
            if disk.DriveType == 2: # Removable
                suffix = []
                storedDrives = {}
                drives = {}

            elif disk.DriveType == 3: # Local
                suffix = ['Drive']
                storedDrives = self.localDrives
                diskDrives = self.wmi.ExecQuery(
                    "Select * from Win32_DiskDrive"
                )
                drives = {drive.DeviceID: drive for drive in diskDrives}

            elif disk.DriveType == 4: # Network
                suffix = ['NetworkDrive']
                storedDrives = self.networkDrives
                mappedDrives = self.wmi.ExecQuery(
                    "Select * from  Win32_MappedLogicalDisk"
                )
                drives = {drive.DeviceID: drive for drive in mappedDrives}

            elif disk.DriveType == 5: # Compact
                suffix = ['CD-Rom']
                storedDrives = self.cdromDrives
                cdromDrives = self.wmi.ExecQuery(
                    "Select * from Win32_CDROMDrive"
                )
                drives = {drive.DeviceID: drive for drive in cdromDrives}

            elif disk.DriveType == 6: # Ram
                suffix = []
                storedDrives = {}
                drives = {}

            else:
                suffix = []
                storedDrives = {}
                drives = {}

            yield suffix, storedDrives, drives

    def UnmountDrive(self, letter):
        for suffix, storedDrives, drives in self.GetDrives():
            if 'Drive' in suffix:
                suffix.append('Unmounted')
            elif 'NetworkDrive' in suffix:
                suffix.append('Detached')
            else:
                suffix.append('Ejected')

            for deviceId in storedDrives.keys():
                drive, payload = storedDrives[deviceId]
                if deviceId in drives:
                    continue

                suffix.extend([
                    payload['name'],
                    payload['drive_letter'][:-1]
                ])

                if suffix[-1] == letter:
                    self.plugin.TriggerEvent(
                        '.'.join(suffix),
                        payload
                    )
                    del (storedDrives[deviceId])

    def MountDrive(self, letter=None):

        for suffix, storedDrives, drives in self.GetDrives():
            for deviceId in drives.keys():
                if deviceId in storedDrives:
                    continue

                if 'CD-Rom' in suffix:
                    cdrom = drives[deviceId]
                    if cdrom.MediaLoaded:
                        suffix.append('Inserted')
                        payload = dict(
                            drive_letter=cdrom.Drive,
                            max_size=cdrom.MaxMediaSize,
                            media_type=cdrom.MediaType,
                            manufacturer=cdrom.Manufacturer,
                            size=cdrom.Size,
                            status=cdrom.Status,
                            name=cdrom.Caption,
                        )
                        suffix.extend([
                            cdrom.Caption,
                            letter
                        ])
                        if cdrom.Drive[:-1] == letter or letter is None:
                            storedDrives[deviceId] = (
                                cdrom,
                                payload
                            )
                            if letter is not None:
                                self.plugin.TriggerEvent(
                                    '.'.join(suffix),
                                    payload
                                )

                elif 'NetworkDrive' in suffix:
                    nDrive = drives[deviceId]
                    suffix.append('Attached')

                    payload = dict(
                        network_path=nDrive.ProviderName,
                        name=nDrive.ProviderName.replace('\\', '\\\\'),
                        volume_name=nDrive.VolumeName,
                        size=nDrive.Size,
                        drive_letter=nDrive.Name,
                        free_space=nDrive.FreeSpace
                    )
                    suffix.extend([
                        nDrive.ProviderName.replace('\\', '\\\\'),
                        letter
                    ])

                    if nDrive.Name[:-1] == letter or letter is None:
                        storedDrives[deviceId] = (
                            nDrive,
                            payload
                        )
                        if letter is not None:
                            self.plugin.TriggerEvent(
                                '.'.join(suffix),
                                payload
                            )

                else:
                    drive = drives[deviceId]

                    partitionQuery = ASSOCIATORS % (
                        'DiskDrive',
                        deviceId.replace('\\', '\\\\'),
                        'DiskDriveToDiskPartition'
                    )
                    for partition in self.wmi.ExecQuery(partitionQuery):
                        diskQuery = ASSOCIATORS % (
                            'DiskPartition',
                            partition.DeviceID,
                            'LogicalDiskToPartition'
                        )
                        for disk in self.wmi.ExecQuery(diskQuery):
                            suffix.append('Mounted')
                            payload = dict(
                                drive_letter=disk.DeviceID,
                                free_space=disk.FreeSpace,
                                size=disk.Size,
                                volume_name=disk.VolumeName,
                                name=drive.Caption
                            )
                            suffix.extend([
                                drive.Caption,
                                letter
                            ])
                            if disk.DeviceID[:-1] == letter or letter is None:
                                storedDrives[deviceId] = (
                                    disk,
                                    payload
                                )
                                if letter is not None:
                                    self.plugin.TriggerEvent(
                                        '.'.join(suffix),
                                        payload
                                    )

    def Lookup(self, suffix, guid, data):
        if data:
            vendorId = data.replace('\\\\?\\', '').split('#')
            vendorId = vendorId[:-1]
            if len(vendorId) >= 3:
                vendorId = '\\'.join(vendorId[:3]).upper()
            else:
                vendorId = '\\'.join(vendorId[:2]).upper()

            if guid in (
                MOUNTDEV_MOUNTED_DEVICE_GUID,
                GUID_DEVINTERFACE_PHYSICALMEDIA
            ):
                return

            if guid not in self.currentDevices:
                self.currentDevices[guid] = {}

            cDevices = self.currentDevices[guid]

            if suffix == 'Removed':
                try:
                    displayName = (
                        DEVICES[guid][0]['display_name'].replace(' ', '')
                    )
                except:
                    self.plugin.TriggerEvent('Device' + suffix, [data])
                    return

                if cDevices:
                    for devId in cDevices.keys():
                        if devId.find(vendorId) == -1:
                            continue

                        payload = cDevices[devId]

                        sfx = [
                            'Device' + suffix,
                            displayName, payload['name']
                        ]

                        self.plugin.TriggerEvent('.'.join(sfx), payload)
                        del (cDevices[devId])
                        self.wmiDevices.remove(payload['device'])
                        return
            else:
                def FindDevices(wmiName, displayName, attrs):
                    displayName = displayName.replace(' ', '')
                    devices = self.wmi.ExecQuery(
                        "Select * from Win32_" + wmiName
                    )

                    for device in devices:
                        if device in self.wmiDevices:
                            continue

                        def TriggerEvent(devId):
                            payload = {
                                attrName: getattr(device, attrName)
                                for attrName in attrs
                            }
                            payload.update(dict(
                                name=device.Name,
                                description=device.Description,
                                status=device.Status,
                                device_id=devId,
                                device=device
                            ))

                            cDevices[devId.upper()] = payload

                            sufx = [
                                'Device' + suffix,
                                displayName,
                                payload['name']
                            ]

                            self.plugin.TriggerEvent('.'.join(sufx), payload)
                            self.wmiDevices.append(device)
                            return True

                        if hasattr(device, 'DeviceId'):
                            if device.DeviceId.upper().find(vendorId) > -1:
                                return TriggerEvent(device.DeviceId)
                        elif hasattr(device, 'DeviceID'):
                            if device.DeviceID.upper().find(vendorId) > -1:
                                return TriggerEvent(device.DeviceID)
                        elif hasattr(device, 'HardwareId'):
                            if device.HardwareId.upper().find(vendorId) > -1:
                                return TriggerEvent(device.HardwareId)

                if guid in DEVICES:
                    dev = DEVICES[guid][0]
                    if FindDevices(
                        dev['cls_name'],
                        dev['display_name'],
                        dev['attr_names']
                    ):
                        return
                for guid in SEARCH:
                    devs = DEVICES[guid]
                    for dev in devs:
                        if FindDevices(
                            dev['cls_name'],
                            dev['display_name'],
                            dev['attr_names']
                        ):
                            return

                self.plugin.TriggerEvent('Device' + suffix, [data])

    def DriveEvent(self, eventType, letter):
        self.driveQueue.append((getattr(self, eventType), letter))
        self.queueEvent.set()

    def DeviceEvent(self, suffix, guid, data):
        self.queue.append((suffix, guid, data))
        self.queueEvent.set()

    def run(self):
        win32com.client.pythoncom.CoInitialize()
        self.wmi = wmi = win32com.client.GetObject("winmgmts:\\root\\cimv2")

        self.MountDrive()

        for guid in DEVICES.keys():
            devs = DEVICES[guid]
            guid = guid.upper()

            if guid not in self.currentDevices:
                self.currentDevices[guid] = {}
            for dev in devs:
                devices = wmi.ExecQuery(
                    "Select * from Win32_" + dev['cls_name']
                )

                for device in devices:
                    if hasattr(device, 'DeviceId'):
                        devId = device.DeviceId
                    elif hasattr(device, 'DeviceID'):
                        devId = device.DeviceID
                    elif hasattr(device, 'HardwareId'):
                        devId = device.HardwareId
                    else:
                        continue

                    payload = {
                        attrName: getattr(device, attrName)
                        for attrName in dev['attr_names']
                    }
                    payload.update(dict(
                        name=device.Name,
                        description=device.Description,
                        status=device.Status,
                        device_id=devId,
                        device=device
                    ))
                    self.currentDevices[guid][devId.upper()] = (
                        payload
                    )
                    self.wmiDevices.append(device)

        while not self.stopEvent.isSet():
            self.queueEvent.wait()
            if not self.stopEvent.isSet():
                while self.queue:
                    self.Lookup(*self.queue.pop(0))
                while self.driveQueue:
                    func, letter = self.driveQueue.pop(0)
                    func(letter)
                self.queueEvent.clear()

        del self.wmi
        self.wmi = None
        win32com.client.pythoncom.CoUninitialize()

    def stop(self):
        self.stopEvent.set()
        self.queueEvent.set()
        self.join(1.0)


class DeviceChangeNotifier:
    def __init__(self, plugin):
        self.plugin = plugin
        self.notifier = None
        self.WMI = WMI(plugin)
        eg.messageReceiver.AddHandler(WM_DEVICECHANGE, self.OnDeviceChange)

        self.WMI.start()
        wx.CallAfter(self.Register)

    def Register(self):
        self.notifier = RegisterDeviceNotification(
            eg.messageReceiver.hwnd,
            pointer(DEV_BROADCAST_DEVICEINTERFACE()),
            DEVICE_NOTIFY_ALL_INTERFACE_CLASSES
        )

    def Close(self):
        self.WMI.stop()
        UnregisterDeviceNotification(self.notifier)
        eg.messageReceiver.RemoveHandler(WM_DEVICECHANGE, self.OnDeviceChange)

    def OnDeviceChange(self, hwnd, msg, wparam, lparam):

        def DriveLettersFromMask(mask):
            return [
                chr(65 + driveNum) for driveNum in range(0, 26)
                if (mask & (2 ** driveNum))
            ]

        def IsDeviceInterface():
            dbch = DEV_BROADCAST_HDR.from_address(lparam)
            return dbch.dbch_devicetype == DBT_DEVTYP_DEVICEINTERFACE

        def IsVolume():
            dbch = DEV_BROADCAST_HDR.from_address(lparam)
            return dbch.dbch_devicetype == DBT_DEVTYP_VOLUME

        def DeviceEvent(suffix):
            dbcc = DEV_BROADCAST_DEVICEINTERFACE.from_address(lparam)
            p = c_wchar_p()
            oledll.ole32.StringFromCLSID(byref(dbcc.dbcc_classguid), byref(p))
            guid = p.value
            windll.ole32.CoTaskMemFree(p)
            self.WMI.DeviceEvent(
                suffix,
                guid,
                wstring_at(lparam + DBD_NAME_OFFSET)
            )

        def VolumeEvent(mountType):
            dbcv = DEV_BROADCAST_VOLUME.from_address(lparam)
            for driveLetter in DriveLettersFromMask(dbcv.dbcv_unitmask):
                self.WMI.DriveEvent(mountType, driveLetter)

        if wparam == DBT_DEVICEARRIVAL:
            if IsDeviceInterface():
                DeviceEvent('Attached')
            elif IsVolume():
                VolumeEvent("MountDrive")

        elif wparam == DBT_DEVICEREMOVECOMPLETE:
                if IsDeviceInterface():
                    DeviceEvent('Removed')
                elif IsVolume():
                    VolumeEvent("UnmountDrive")

        return 1


class GetDevices(eg.ActionBase):
    name = 'Get System Devices'
    description = (
        'Returns a device object that represents a physical device\n'
        'on your computer.'
    )

    def __call__(self, pattern=None, **kwargs):
        if pattern is None and not kwargs:
            return

        if isinstance(pattern, dict):
            clsName = pattern.keys()[0]
            pattern = pattern.values()[0]

        elif pattern is None:
            if len(kwargs.keys()) > 1:
                eg.PrintNotice(
                    'You can only specify one device to search for.\n'
                    'If you want to broaden your search use ? or * as'
                    ' wildcards'
                )
                return
            clsName = kwargs.keys()[0]
            pattern = kwargs.values()[0]
        else:
            clsName = None

        searchableItems = []
        foundDevices = ()

        win32com.client.pythoncom.CoInitialize()
        wmi = win32com.client.GetObject("winmgmts:\\root\\cimv2")
        for devs in DEVICES.values():
            for dev in devs:
                if clsName == dev['cls_name']:
                    searchableItems.append(dev)
                    break
                if clsName is None:
                    if dev['display_name'].replace(' ', '') == dev['cls_name']:
                        searchableItems.append(dev)
            if clsName is not None and searchableItems:
                break

        for searchCls in searchableItems:
            primarySearch = searchCls['action_search']
            clsName = searchCls['cls_name']
            for device in wmi.ExecQuery("Select * from Win32_" + clsName):
                primarySearch = [getattr(device, primarySearch)]
                if hasattr(device, 'Name') and device.Name is not None:
                    primarySearch.append(device.Name)

                if hasattr(device, 'DeviceId') and device.DeviceId is not None:
                    primarySearch.append(device.DeviceId)
                if (
                    hasattr(device, 'Description') and
                    device.Description is not None
                ):
                    primarySearch.append(device.Description)
                if (
                    hasattr(device, 'HardwareId') and
                    device.HardwareId is not None
                ):
                    primarySearch.append(device.HardwareId)

                if '*' not in pattern and '?' not in pattern:
                    if pattern in primarySearch:
                        foundDevices += (device,)
                else:
                    for search in primarySearch:
                        if fnmatch.fnmatch(search, pattern):
                            foundDevices += (device,)
                            break
        del wmi
        win32com.client.pythoncom.CoUninitialize()
        eg.Print(str(len(foundDevices)) + ' Devices Found')
        return foundDevices

    def Configure(self, pattern=None):
        filePath = os.path.join(os.path.split(__file__)[0], 'Help.zip')

        sys.path.insert(0, filePath)
        import Help

        win32com.client.pythoncom.CoInitialize()
        wmi = win32com.client.GetObject("winmgmts:\\root\\cimv2")

        panel = eg.ConfigPanel()
        panel.EnableButtons(False)

        self.result = pattern
        splitterWindow = wx.SplitterWindow(
            panel,
            -1,
            style=(
                wx.SP_LIVE_UPDATE |
                wx.CLIP_CHILDREN |
                wx.NO_FULL_REPAINT_ON_RESIZE
            )
        )

        htmlHelp = iewin_old.IEHtmlWindow(splitterWindow)

        tree = wx.TreeCtrl(
            splitterWindow,
            -1,
            style=(
                wx.TR_HAS_BUTTONS |
                wx.TR_ROW_LINES |
                wx.CLIP_CHILDREN
            )
        )

        root = tree.AddRoot('Devices')

        def SetHelp(cName):
            cName = cName.upper()
            if cName[0].isdigit():
                helpName = cName[4:] + cName[:4]
            else:
                helpName = cName
            htmlHelp.LoadString(getattr(Help, helpName))

        deviceDict = {}
        for guid in DEVICES.keys():
            devices = DEVICES[guid]
            for device in devices:
                if device['cls_name'] == device['display_name'].replace(' ', ''):
                    deviceDict[device['cls_name']] = device

        for clsName in sorted(deviceDict.keys()):
            dvc = deviceDict[clsName]
            deviceTree = tree.AppendItem(root, dvc['display_name'])
            tree.SetPyData(deviceTree, clsName)

            for device in wmi.ExecQuery("Select * from Win32_" + clsName):
                deviceLabel = getattr(device, dvc['action_search'])
                deviceItem = tree.AppendItem(deviceTree, deviceLabel)
                tree.SetPyData(deviceItem, dvc)
                if self.result == {clsName: deviceLabel}:
                    tree.SelectItem(deviceItem)

        def OnActivated(evt):
            item = evt.GetItem()
            if item.IsOk():
                pyData = tree.GetPyData(item)
                if isinstance(pyData, dict):
                    deviceName = tree.GetItemText(item)
                    clsName = pyData['cls_name']
                    self.result = {clsName: deviceName}
                    panel.EnableButtons(True)
                else:
                    if tree.ItemHasChildren(item):
                        if tree.IsExpanded(item):
                            tree.Collapse(item)
                        else:
                            tree.Expand(item)
                    clsName = pyData
                    panel.EnableButtons(False)
                    self.result = None
                SetHelp(clsName)
            evt.Skip()

        def OnSelectionChanged(evt):
            item = evt.GetItem()
            if item.IsOk():
                pyData = tree.GetPyData(item)
                if isinstance(pyData, dict):
                    deviceName = tree.GetItemText(item)
                    clsName = pyData['cls_name']
                    self.result = {clsName: deviceName}
                    panel.EnableButtons(True)
                else:
                    panel.EnableButtons(False)
                    self.result = None
                    clsName = pyData
                SetHelp(clsName)
            evt.Skip()

        def OnClose(evt):
            self.event.set()
            evt.Skip()
        panel.Bind(wx.EVT_CLOSE, OnClose)

        tree.Expand(root)
        tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, OnActivated)
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, OnSelectionChanged)

        splitterWindow.SplitVertically(tree, htmlHelp)
        splitterWindow.SetMinimumPaneSize(120)
        splitterWindow.UpdateSize()

        panel.sizer.Add(splitterWindow, 1, wx.EXPAND | wx.ALL, 10)
        SetHelp('START')

        while panel.Affirmed():
            panel.SetResult(self.result)

        sys.path.pop(0)
        del wmi
        win32com.client.pythoncom.CoUninitialize()

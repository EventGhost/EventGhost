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

try:
    WIN_XP = eg.WindowsVersion.IsXP()
except AttributeError:
    import platform

    if platform.version().split('.')[:2] in (['5', '2'], ['5', '1']):
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

NOEVENT = (
    MOUNTDEV_MOUNTED_DEVICE_GUID,
    GUID_DEVINTERFACE_PHYSICALMEDIA
)


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
    """
    Subclass of threading.Thread that handles the WMI lookup of devices as well
     as generating events.
    """

    def __init__(self, plugin):
        """
        Threading object that runs the WMI device lookup.

        :param plugin: Instance of System plugin.
        """

        threading.Thread.__init__(self, name='WMI Thread')
        self.plugin = plugin
        self.wmi = None
        self.queueEvent = threading.Event()
        self.stopEvent = threading.Event()
        self.queue = []
        self.currentDevices = {}
        self.networkDrives = {}
        self.localDrives = {}
        self.cdromDrives = {}
        self.wmiDevices = []
        self.wmi = None

    def GetDrives(self):
        """
        Generator that retrieves WMI instances that represent drives.

        :return: WMI instances of Win32_DiskDrive, Win32_MappedLogicalDisk and
        Win32_CDROMDrive.
        """

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
        """
        Called by the internal queue mechanism for generating a drive unmounted
         event.

        :param letter: str() Drive letter.
        :return: None
        """

        driveTypes = [
            [self.localDrives, ['Drive.Unmounted']],
            [self.networkDrives, ['NetworkDrive.Detached']],
            [self.cdromDrives, ['CD-Rom.Ejected']]
        ]

        while driveTypes:
            storedDrives, suffix = driveTypes.pop(0)
            if letter + ':' in storedDrives:
                drive, payload = storedDrives[letter + ':']
                suffix += [payload['name'], letter]
                self.plugin.TriggerEvent('.'.join(suffix), payload)
                del storedDrives[letter + ':']
                return

        for suffix, storedDrives, drives in self.GetDrives():
            if 'Drive' in suffix:
                suffix.append('Unmounted')
            elif 'NetworkDrive' in suffix:
                suffix.append('Detached')
            else:
                suffix.append('Ejected')

            for deviceId in storedDrives.keys():
                drive, payload = storedDrives[deviceId]

                if payload['drive_letter'][:-1] != letter:
                    continue

                if deviceId in drives:
                    continue

                suffix += [payload['name'], letter]
                self.plugin.TriggerEvent('.'.join(suffix), payload)
                del storedDrives[deviceId]

    def MountDrive(self, letter=None):
        """
        Called by the internal queue mechanism for generating a drive mounted
        event.

        :param letter: str() Drive letter.
        :return: None
        """
        TriggerEvent = self.plugin.TriggerEvent

        for suffix, storedDrives, drives in self.GetDrives():
            for deviceId in drives.keys():
                if deviceId in storedDrives:
                    continue

                if 'CD-Rom' in suffix:
                    cdrom = drives[deviceId]

                    if letter and cdrom.Drive[:-1] != letter:
                        continue
                    if not cdrom.MediaLoaded:
                        continue

                    payload = dict(
                        drive_letter=cdrom.Drive,
                        max_size=cdrom.MaxMediaSize,
                        media_type=cdrom.MediaType,
                        manufacturer=cdrom.Manufacturer,
                        size=cdrom.Size,
                        status=cdrom.Status,
                        name=cdrom.Caption,
                    )
                    storedDrives[deviceId] = (cdrom, payload)

                    if letter:
                        suffix += ['Inserted', cdrom.Caption, letter]
                        TriggerEvent('.'.join(suffix), payload)

                elif 'NetworkDrive' in suffix:
                    nDrive = drives[deviceId]

                    if letter and nDrive.Name[:-1] != letter:
                        continue

                    payload = dict(
                        network_path=nDrive.ProviderName,
                        name=nDrive.ProviderName.replace('\\', '\\\\'),
                        volume_name=nDrive.VolumeName,
                        size=nDrive.Size,
                        drive_letter=nDrive.Name,
                        free_space=nDrive.FreeSpace
                    )
                    storedDrives[deviceId] = (nDrive, payload)

                    if letter:
                        suffix += [
                            'Attached',
                            nDrive.ProviderName.replace('\\', '\\\\'),
                            letter
                        ]
                        TriggerEvent('.'.join(suffix), payload)

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
                            if letter and disk.DeviceID[:-1] != letter:
                                continue

                            payload = dict(
                                drive_letter=disk.DeviceID,
                                free_space=disk.FreeSpace,
                                size=disk.Size,
                                volume_name=disk.VolumeName,
                                name=drive.Caption
                            )
                            storedDrives[deviceId] = (disk, payload)

                            if letter:
                                suffix += ['Mounted', drive.Caption, letter]
                                TriggerEvent('.'.join(suffix), payload)

    def ParseVendorId(self, vendorId):
        """
        Parses the vendor id that is received from a Windows notification.

        :param vendorId: str() Notification vendor id
        :return: str() Modified vendor id.
        """

        vendorId = vendorId.replace('\\\\?\\', '').split('#')
        vendorId = vendorId[:-1]

        if len(vendorId) >= 3:
            vendorId = '\\'.join(vendorId[:3]).upper()
        else:
            vendorId = '\\'.join(vendorId[:2]).upper()

        return vendorId

    def Removed(self, guid, data):
        """
        Called by the internal queue mechanism for generating a device removed
         event.

        :param guid: str() guid of the calling Windows notification.
        :param data: str() Vendor Id of the device that has changed.
        :return: None
        """

        if guid in NOEVENT:
            return

        suffix = ['Device.Removed']
        TriggerEvent = self.plugin.TriggerEvent

        try:
            display_name = DEVICES[guid][0]['display_name']
        except KeyError:
            TriggerEvent(suffix[0], [data])
            return

        if guid not in self.currentDevices:
            self.currentDevices[guid] = {}

        cDevices = self.currentDevices[guid]

        if not cDevices:
            return

        vendorId = self.ParseVendorId(data)

        for devId in cDevices.keys():
            if devId.find(vendorId) == -1:
                continue
            payload = cDevices[devId]
            suffix += [display_name.replace(' ', ''), payload['name']]

            del cDevices[devId]
            self.wmiDevices.remove(payload['device'])

            TriggerEvent('.'.join(suffix), payload)
            return

    def Attached(self, guid, data):
        """
        Called by the internal queue mechanism for generating a device attached
         event.

        :param guid: str() guid of the calling Windows notification.
        :param data: str() Vendor Id of the device that has changed.
        :return: None
        """

        if guid in NOEVENT:
            return

        if guid not in self.currentDevices:
            self.currentDevices[guid] = {}

        cDevices = self.currentDevices[guid]
        vendorId = self.ParseVendorId(data)
        suffix = ['Device.Attached']
        TriggerEvent = self.plugin.TriggerEvent

        def FindDevices(cls_name, display_name, attr_names, **kwargs):
            display_name = display_name.replace(' ', '')
            devices = self.wmi.ExecQuery(
                "Select * from Win32_" + cls_name
            )

            for device in devices:
                if device in self.wmiDevices:
                    continue

                deviceId = ''
                for attrName in ('DeviceId', 'DeviceID', 'HardwareId'):
                    deviceId = getattr(device, attrName, None)

                    if not isinstance(deviceId, tuple):
                        deviceId = (deviceId,)
                    for deviceId in list(deviceId)[:]:
                        if deviceId and deviceId.upper().find(vendorId) > -1:
                            break
                        deviceId = None

                    if deviceId is not None:
                        break

                if deviceId is None:
                    continue

                attr_names += ('Name', 'Description', 'Status')
                payload = {
                    attrName.lower(): getattr(device, attrName)
                    for attrName in attr_names
                }
                payload['device_id'] = deviceId
                payload['device'] = device
                suffix.extend([display_name, device.Name])

                cDevices[deviceId.upper()] = payload
                self.wmiDevices.append(device)

                TriggerEvent('.'.join(suffix), payload)
                return True

        if guid in DEVICES:
            dev = DEVICES[guid][0]
            if FindDevices(**dev):
                return

        for guid in SEARCH:
            devs = DEVICES[guid]
            for dev in devs:
                if FindDevices(**dev):
                    return

        TriggerEvent(suffix[0], [data])

    def DriveEvent(self, eventType, letter):
        """
        Puts the Windows notification data into the queue.

        :param eventType: str() Attribute name for the event.
        :param letter: str() Drive Letter
        :return: None
        """

        self.queue.append((getattr(self, eventType), (letter,)))
        self.queueEvent.set()

    def DeviceEvent(self, eventType, guid, data):
        """
        Puts the Windows notification data into the queue.

        :param eventType: str() Attribute name for the event.
        :param guid: str() Notification GUID
        :param data: str() Vendor id
        :return: None
        """

        self.queue.append((getattr(self, eventType), (guid, data)))
        self.queueEvent.set()

    def run(self):
        """
        Handles the population of devices when the thread starts. This also
        loops and pulls data from the queue and sends it where it needs to go
         for proper event generation.

        :return: None
        """
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

                    attrs = dev['attr_names']
                    attrs += ('Name', 'Description', 'Status')
                    payload = {
                        attrName.lower(): getattr(device, attrName)
                        for attrName in attrs
                    }
                    payload['device_id'] = devId
                    payload['device'] = device

                    self.currentDevices[guid][devId.upper()] = payload
                    self.wmiDevices.append(device)

        while not self.stopEvent.isSet():
            self.queueEvent.wait()
            if not self.stopEvent.isSet():
                while self.queue:
                    func, data = self.queue.pop(0)
                    func(*data)
                self.queueEvent.clear()

        del self.wmi
        self.wmi = None
        win32com.client.pythoncom.CoUninitialize()

    def stop(self):
        """
        Stops the thread.

        :return: None
        """
        self.stopEvent.set()
        self.queueEvent.set()
        self.join(1.0)


class DeviceChangeNotifier:
    """
    This class receives the Windows notifications and grams any necessary data
    from the message and then passes it to the WMI thread so an event can be
     generated.
    """
    def __init__(self, plugin):
        """
        Registers for Windows notifications for Devices/Drives being attached
        or removed.

        :param plugin: System plugin instance
        """
        self.plugin = plugin
        self.notifier = None
        self.WMI = WMI(plugin)

        eg.messageReceiver.AddHandler(
            WM_DEVICECHANGE,
            self.OnDeviceChange
        )

        self.WMI.start()
        wx.CallAfter(self.Register)

    def Register(self):
        """
        Registers for the notifications. This gets called via the use of
        wx.CallAfter. This is done because the actual registration seems to be
        much happier when done from the main thread.

        :return: None
        """
        self.notifier = RegisterDeviceNotification(
            eg.messageReceiver.hwnd,
            pointer(DEV_BROADCAST_DEVICEINTERFACE()),
            DEVICE_NOTIFY_ALL_INTERFACE_CLASSES
        )

    def Close(self):
        """
        Performs the shutdown of the WMI thread. Als unregisters for the
        Windows notifications.

        :return:None
        """
        self.WMI.stop()
        UnregisterDeviceNotification(self.notifier)

        eg.messageReceiver.RemoveHandler(
            WM_DEVICECHANGE,
            self.OnDeviceChange
        )

    def OnDeviceChange(self, hwnd, msg, wparam, lparam):
        """
        Callback method the Windows notification calls when a message needs to
        be delivered.

        :param hwnd: Some window handle.
        :param msg: Some window message.
        :param wparam: long() Notification type.
        :param lparam: long() Memory address for notification class.
        :return: None
        """

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
            oledll.ole32.StringFromCLSID(
                byref(dbcc.dbcc_classguid),
                byref(p)
            )
            guid = p.value
            windll.ole32.CoTaskMemFree(p)

            self.WMI.DeviceEvent(
                suffix,
                guid,
                wstring_at(lparam + DBD_NAME_OFFSET)
            )

        def VolumeEvent(mountType):
            dbcv = DEV_BROADCAST_VOLUME.from_address(lparam)
            letters = DriveLettersFromMask(dbcv.dbcv_unitmask)
            for letter in letters:
                self.WMI.DriveEvent(mountType, letter)

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
    """
    System.GetDevice action.

    Searches for a device that the user specifies the name/vendorId.
    Returns a WMI device instance for the device(s).

    Help is located in the configuration dialog for this action.
    """

    name = 'Get System Devices'
    description = (
        'Returns a device object that represents a physical device\n'
        'on your computer.'
    )

    def __init__(self):
        self.result = None

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
                    displayName = dev['display_name'].replace(' ', '')
                    if displayName == dev['cls_name']:
                        searchableItems.append(dev)

            if clsName is not None and searchableItems:
                break

        for searchCls in searchableItems:
            primarySearch = searchCls['action_search']
            clsName = searchCls['cls_name']
            for device in wmi.ExecQuery("Select * from Win32_" + clsName):
                priSearch = [getattr(device, primarySearch)]

                for attr in ('Name', 'DeviceId', 'Description'):
                    priSearch.append(getattr(device, attr, None))

                hardId = getattr(device, 'HardwareId', None)
                if hardId and isinstance(hardId, tuple):
                    priSearch.extend(list(hardId))
                elif hardId:
                    priSearch.append(hardId)

                if '*' not in pattern and '?' not in pattern:
                    if pattern in priSearch:
                        foundDevices += (device,)
                else:
                    for search in priSearch:
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

        Help = __import__('Help')

        win32com.client.pythoncom.CoInitialize()
        wmi = win32com.client.GetObject("winmgmts:\\root\\cimv2")

        panel = eg.ConfigPanel()
        panel.EnableButtons(False)

        self.result = pattern
        splitterWindow = wx.SplitterWindow(
            panel,
            -1,
            size=(850, 400),
            style=(
                wx.SP_LIVE_UPDATE |
                wx.CLIP_CHILDREN |
                wx.NO_FULL_REPAINT_ON_RESIZE
            )
        )

        htmlHelp = eg.HtmlWindow(splitterWindow)

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
        tree.SetPyData(root, 'START')

        def SetHelp(cName):
            if cName.startswith('1394'):
                cName = cName[4:] + '1394'
            htmlHelp.SetPage(getattr(Help, cName.upper()).encode('ascii'))

        deviceDict = {}
        for guid in DEVICES.keys():
            devices = DEVICES[guid]
            for device in devices:
                clsName = device['display_name'].replace(' ', '')
                if device['cls_name'] == clsName:
                    deviceDict[clsName] = device

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
        splitterWindow.SetSashPosition(200)

        while panel.Affirmed():
            panel.SetResult(self.result)

        del wmi
        win32com.client.pythoncom.CoUninitialize()
        sys.path.remove(filePath)

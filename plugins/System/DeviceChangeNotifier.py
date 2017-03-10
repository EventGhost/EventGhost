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
    DEV_BROADCAST_DEVICEINTERFACE as _DEV_BROADCAST_DEVICEINTERFACE,
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
            action_search='Caption',
            display_name='Disk Drive'
        ),
        dict(
            cls_name='IDEController',
            attr_names=(),
            action_search='Caption',
            display_name='IDE Controller'
        ),
        dict(
            cls_name='SCSIController',
            attr_names=('Manufacturer',),
            action_search='Caption',
            display_name='SCSI Controller'
        ),
    ),
    GUID_DEVINTERFACE_USB_HOST_CONTROLLER: (
        dict(
            cls_name='USBController',
            attr_names=('Manufacturer',),
            action_search='Caption',
            display_name='USB Controller'
        ),
    ),
    GUID_DEVINTERFACE_USB_HUB: (
        dict(
            cls_name='USBHub',
            attr_names=('USBVersion',),
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
            action_search='Caption',
            display_name='Tape Drive'
        ),
    ),
    KSCATEGORY_AUDIO: (
        dict(
            cls_name='SoundDevice',
            attr_names=('Manufacturer', 'ProductName'),
            action_search='Caption',
            display_name='Sound Device'
        ),
    ),
    GUID_DEVINTERFACE_COMPORT: (
        dict(
            cls_name='SerialPort',
            attr_names=(),
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
            action_search='Caption',
            display_name='Pointing Device'
        ),
    ),
    GUID_DEVINTERFACE_MODEM: (
        dict(
            cls_name='POTSModem',
            attr_names=(),
            action_search='Caption',
            display_name='POTS Modem'
        ),
    ),
    GUID_DEVINTERFACE_PARALLEL: (
        dict(
            cls_name='ParallelPort',
            attr_names=(),
            action_search='Caption',
            display_name='Parallel Port'
        ),
    ),
    BUS1394_CLASS_GUID: (
        dict(
            cls_name='1394Controller',
            attr_names=(),
            action_search='Caption',
            display_name='1394 Controller'
        ),
    ),
    GUID_61883_CLASS: (
        dict(
            cls_name='1394ControllerDevice',
            attr_names=(),
            action_search='Caption',
            display_name='1394 Controller Device'
        ),
    ),
    GUID_DEVCLASS_IRDA: (
        dict(
            cls_name='InfraredDevice',
            attr_names=(),
            action_search='Caption',
            display_name='Infrared Device'
        ),
    ),
    GUID_DEVCLASS_SYSTEM: (
        dict(
            cls_name='MotherboardDevice',
            attr_names=(),
            action_search='Name',
            display_name='Motherboard Device'
        ),
        dict(
            cls_name='CacheMemory',
            attr_names=(),
            action_search='DeviceID',
            display_name='Cache Memory'
        ),
        dict(
            cls_name='Fan',
            attr_names=(),
            action_search='Caption',
            display_name='Fan'
        ),
        dict(
            cls_name='HeatPipe',
            attr_names=(),
            action_search='Caption',
            display_name='Heat Pipe'
        ),
        dict(
            cls_name='OnBoardDevice',
            attr_names=(),
            action_search='Caption',
            display_name='OnBoard Device'
        ),
        dict(
            cls_name='PhysicalMemory',
            attr_names=(),
            action_search='Tag',
            display_name='Physical Memory'
        ),
        dict(
            cls_name='Refrigeration',
            attr_names=(),
            action_search='Caption',
            display_name='Refrigeration'
        ),
        dict(
            cls_name='SystemSlot',
            attr_names=(),
            action_search='SlotDesignation',
            display_name='System Slot'
        ),
        dict(
            cls_name='TemperatureProbe',
            attr_names=(),
            action_search='Caption',
            display_name='Temperature Probe'
        ),
        dict(
            cls_name='VoltageProbe',
            attr_names=(),
            action_search='Caption',
            display_name='Voltage Probe'
        ),
        dict(
            cls_name='Processor',
            attr_names=(),
            action_search='Name',
            display_name='Processor'
        )
    ),
    GUID_DEVCLASS_PCMCIA: (
        dict(
            cls_name='PCMCIAController',
            attr_names=(),
            action_search='Caption',
            display_name='PCMCIA Controller'
        ),
    ),
    GUID_DEVCLASS_PRINTERS: (
        dict(
            cls_name='Printer',
            attr_names=(),
            action_search='Caption',
            display_name='Printer'
        ),
        dict(
            cls_name='TCPIPPrinterPort',
            attr_names=(),
            action_search='Caption',
            display_name='TCPIP PrinterPort'
        ),
        dict(
            cls_name='PrinterController',
            attr_names=(),
            action_search='Caption',
            display_name='Printer Controller'
        )
    ),
    KSCATEGORY_BDA_NETWORK_EPG: (
        dict(
            cls_name='PNPEntity',
            attr_names=('Caption', 'Description', 'Manufacturer'),
            action_search='Description',
            display_name='EPG'
        ),
    ),
    KSCATEGORY_BDA_NETWORK_TUNER: (
        dict(
            cls_name='PNPEntity',
            attr_names=('Caption', 'Description', 'Manufacturer'),
            action_search='Description',
            display_name='Network Tuner'
        ),
    ),
    KSCATEGORY_TVTUNER: (
        dict(
            cls_name='PNPEntity',
            attr_names=('Caption', 'Description', 'Manufacturer'),
            action_search='Description',
            display_name='TV Tuner'
        ),
    ),
    GUID_BTHPORT_DEVICE_INTERFACE: (
        dict(
            cls_name='PNPEntity',
            attr_names=('Caption', 'Description', 'Manufacturer'),
            action_search='Description',
            display_name='BlueTeeth Device'
        ),
    ),
    GUID_DEVINTERFACE_WPD: (
        dict(
            cls_name='PNPEntity',
            attr_names=('Caption', 'Description', 'Manufacturer'),
            action_search='Description',
            display_name='Portable'
        ),
    ),
    GUID_DEVINTERFACE_USB_DEVICE: (
        dict(
            cls_name='PNPEntity',
            attr_names=('Caption', 'Description', 'Manufacturer'),
            action_search='Description',
            display_name='USB Device'
        ),
    ),
    GUID_DEVINTERFACE_HID: (
        dict(
            cls_name='PNPEntity',
            attr_names=('Caption', 'Description', 'Manufacturer'),
            action_search='Description',
            display_name='HID Device'
        ),
    ),
    GUID_DEVINTERFACE_IMAGE: (
        dict(
            cls_name='PNPEntity',
            attr_names=('Caption', 'Description', 'Manufacturer'),
            action_search='Description',
            display_name='Imaging Device'
        ),
    ),
    KSCATEGORY_CAPTURE: (
        dict(
            cls_name='PNPEntity',
            attr_names=('Caption', 'Description', 'Manufacturer'),
            action_search='Description',
            display_name='Video Capture'
        ),
    ),
    KSCATEGORY_VIDEO: (
        dict(
            cls_name='PNPEntity',
            attr_names=('Caption', 'Description', 'Manufacturer'),
            action_search='Description',
            display_name='Video Device'
        ),
    ),
    KSCATEGORY_STILL: (
        dict(
            cls_name='PNPEntity',
            attr_names=('Caption', 'Description', 'Manufacturer'),
            action_search='Description',
            display_name='Still Capture'
        ),
    ),
}

NOEVENT = (
    MOUNTDEV_MOUNTED_DEVICE_GUID,
    GUID_DEVINTERFACE_PHYSICALMEDIA
)

SETUP_CLASS_GUIDS = {
    '{72631E54-78A4-11D0-BCF7-00AA00B7B32A}': 'Battery',
    '{53D29EF7-377C-4D14-864B-EB3A85769359}': 'BiometricDevice',
    '{E0CBF06C-CD8B-4647-BB8A-263B43F0F974}': 'BluetoothDevice',
    '{4D36E965-E325-11CE-BFC1-08002BE10318}': 'CDROMDrive',
    '{4D36E967-E325-11CE-BFC1-08002BE10318}': 'DiskDrive',
    '{4D36E968-E325-11CE-BFC1-08002BE10318}': 'DisplayAdapter',
    '{4D36E969-E325-11CE-BFC1-08002BE10318}': 'FloppyDiskController',
    '{4D36E980-E325-11CE-BFC1-08002BE10318}': 'FloppyDiskDrive',
    '{6BDD1FC3-810F-11D0-BEC7-08002BE2092F}': 'GlobalPositioningDevice',
    '{4D36E96A-E325-11CE-BFC1-08002BE10318}': 'HardDriveController',
    '{745A17A0-74D3-11D0-B6FE-00A0C90F57DA}': 'HIDDevice',
    '{48721B56-6795-11D2-B1A8-0080C72E74A2}': '1284.4Device',
    '{49CE6AC8-6F86-11D2-B1E5-0080C72E74A2}': '1284.4PrintFunction',
    '{7EBEFBC0-3200-11D2-B4C2-00A0C9697D07}': '1394-61883Device',
    '{C06FF265-AE09-48F0-812C-16753D7CBA83}': '1394-AVCDevice',
    '{D48179BE-EC20-11D1-B6B8-00C04FA372A7}': '1394-SBP2Device',
    '{6BDD1FC1-810F-11D0-BEC7-08002BE2092F}': '1394Controller',
    '{6BDD1FC6-810F-11D0-BEC7-08002BE2092F}': 'ImagingDevice',
    '{6BDD1FC5-810F-11D0-BEC7-08002BE2092F}': 'IrDADevice',
    '{4D36E96B-E325-11CE-BFC1-08002BE10318}': 'Keyboard',
    '{CE5939AE-EBDE-11D0-B181-0000F8753EC4}': 'MediaChanger',
    '{4D36E970-E325-11CE-BFC1-08002BE10318}': 'MemoryTechnology',
    '{4D36E96D-E325-11CE-BFC1-08002BE10318}': 'Modem',
    '{4D36E96E-E325-11CE-BFC1-08002BE10318}': 'Monitor',
    '{4D36E96F-E325-11CE-BFC1-08002BE10318}': 'Mouse',
    '{4D36E971-E325-11CE-BFC1-08002BE10318}': 'Multifunction',
    '{4D36E96C-E325-11CE-BFC1-08002BE10318}': 'Multimedia',
    '{50906CB8-BA12-11D1-BF5D-0000F805F530}': 'MultiportSerialAdapter',
    '{4D36E972-E325-11CE-BFC1-08002BE10318}': 'NetworkAdapter',
    '{4D36E973-E325-11CE-BFC1-08002BE10318}': 'NetworkClient',
    '{4D36E974-E325-11CE-BFC1-08002BE10318}': 'NetworkService',
    '{4D36E975-E325-11CE-BFC1-08002BE10318}': 'NetworkTransport',
    '{268C95A1-EDFE-11D3-95C3-0010DC4050A5}': 'SSLSecurityAccelerator',
    '{4D36E977-E325-11CE-BFC1-08002BE10318}': 'PCMCIA',
    '{4D36E978-E325-11CE-BFC1-08002BE10318}': 'Ports',
    '{4D36E979-E325-11CE-BFC1-08002BE10318}': 'Printer',
    '{4658EE7E-F050-11D1-B6BD-00C04FA372A7}': 'PNPPrinters',
    '{50127DC3-0F36-415E-A6CC-4CB3BE910B65}': 'Processor',
    '{4D36E97B-E325-11CE-BFC1-08002BE10318}': 'SCSIAdapter',
    '{5175D334-C371-4806-B3BA-71FD53C9258D}': 'Sensor',
    '{50DD5230-BA8A-11D1-BF5D-0000F805F530}': 'SmartCardReader',
    '{71A27CDD-812A-11D0-BEC7-08002BE2092F}': 'StorageVolume',
    '{4D36E97D-E325-11CE-BFC1-08002BE10318}': 'SystemDevice',
    '{6D807884-7D21-11CF-801C-08002BE10318}': 'TapeDrive',
    '{88BAE032-5A81-49F0-BC3D-A4FF138216D6}': 'USBDevice',
    '{25DBCE51-6C8F-4A72-8A6D-B54C2B4FC835}': 'CEUSBActiveSync',
    '{EEC5AD98-8080-425F-922A-DABF3DE3F69A}': 'Portable',
    '{997B5D8D-C442-4F2E-BAF3-9C8E671E9E21}': 'SideShow'
}

SEARCH = [
    GUID_DEVINTERFACE_KEYBOARD,
    GUID_DEVICE_BATTERY,
    GUID_DEVINTERFACE_CDROM,
    GUID_DEVINTERFACE_MONITOR,
    GUID_DEVINTERFACE_DISK,
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


if eg.WindowsVersion.IsXP():
    DEVICES[GUID_DEVINTERFACE_DISK][0]['attr_names'] += (
        'FirmwareRevision',
    )
    DEVICES[GUID_DEVINTERFACE_I2C] = (
        dict(
            cls_name='PNPEntity',
            attr_names=(),
            action_search='Caption',
            display_name='I2C Device'
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
            action_search='Description',
            display_name='Network Adapter'
        ),
    )
    SEARCH.insert(0, GUID_DEVINTERFACE_NET)

if not eg.WindowsVersion.Is10():
    DEVICES[GUID_DEVINTERFACE_FLOPPY] = (
        dict(
            cls_name='FloppyDrive',
            attr_names=(
                'Manufacturer',
            ),
            action_search='Caption',
            display_name='Floppy Drive'
        ),
        dict(
            cls_name='FloppyController',
            attr_names=(),
            action_search='Caption',
            display_name='Floppy Controller'
        )
    )

    SEARCH.insert(0, GUID_DEVINTERFACE_FLOPPY)


class DEV_BROADCAST_DEVICEINTERFACE(_DEV_BROADCAST_DEVICEINTERFACE):
    def __init__(self):
        self.dbcc_devicetype = DBT_DEVTYP_DEVICEINTERFACE
        self.dbcc_size = sizeof(DEV_BROADCAST_DEVICEINTERFACE)

DBD_NAME_OFFSET = DEV_BROADCAST_DEVICEINTERFACE.dbcc_name.offset

ASSOCIATORS = (
    'ASSOCIATORS OF {Win32_%s.DeviceID="%s"}'
    ' WHERE AssocClass=Win32_%s'
)


def _parse_vendor_id(vendor_id):
    """
    Parses the vendor id that is received from a Windows notification.

    :param vendor_id: str() Notification vendor id
    :return: str() Modified vendor id.
    """

    vendor_id = vendor_id.replace('\\\\?\\', '').split('#')
    vendor_id = vendor_id[:-1]

    if len(vendor_id) >= 3:
        vendor_id = '\\'.join(vendor_id[:3]).upper()
    else:
        vendor_id = '\\'.join(vendor_id[:2]).upper()

    return vendor_id


def _get_ids(device):
    res = ()
    for attr_name in ('DeviceId', 'DeviceID', 'HardwareId'):
        if hasattr(device, attr_name):
            device_id = getattr(device, attr_name)
            if device_id is None:
                continue
            if not isinstance(device_id, tuple):
                device_id = (device_id,)
            res += device_id
    return res


def _create_key(device_ids):
    return tuple(device_id.upper() for device_id in device_ids)


def _create_event(device_ids, attr_names, display_name, device):
    attr_names += ('Name', 'Description', 'Status')
    payload = {
        attrName.lower(): getattr(device, attrName)
        for attrName in attr_names
    }
    payload['device_id'] = device_ids
    payload['device'] = device

    name = device.Name

    for device_id in device_ids:
        if device_id.startswith('WPDBUSENUMROOT'):
            name = device.Description + '.' + device.Name[0]
            payload['drive_letter'] = device.Name[:2]

    if hasattr(device, 'ClassGuid') and device.ClassGuid in SETUP_CLASS_GUIDS:
        suffix = [SETUP_CLASS_GUIDS[device.ClassGuid], name]
    else:
        suffix = [display_name.replace(' ', ''), name]

    return suffix, payload


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
        self.wmi = None

    @eg.LogItWithReturn
    def GetDrives(self):
        """
        Retrieves WMI instances that represent drives.

        :return: WMI instances of Win32_DiskDrive, Win32_MappedLogicalDisk and
        Win32_CDROMDrive.
        """
        res = ()
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

            if not suffix:
                continue
            res += ((suffix, storedDrives, drives),)
        return res

    @eg.LogIt
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

    @eg.LogIt
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

    @eg.LogIt
    def Removed(self, guid, data):
        """
        Called by the internal queue mechanism for generating a device removed
         event.

        :param guid: str() guid of the calling Windows notification.
        :param data: str() Vendor Id of the device that has changed.
        :return: None
        """

        TriggerEvent = self.plugin.TriggerEvent

        if guid in NOEVENT:
            return

        cDevices = self._current_devices(guid)
        if not cDevices or guid not in DEVICES:
            TriggerEvent('Device.Removed', [data])
            return

        vendor_id = _parse_vendor_id(data)

        for device_ids in cDevices.keys():
            for device_id in device_ids:
                if device_id.find(vendor_id) == -1:
                    continue

                suffix, payload = cDevices[device_ids]
                TriggerEvent('.'.join(['Device.Removed'] + suffix), payload)

                del cDevices[device_ids]
                return

    @eg.LogIt
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

        vendor_id = _parse_vendor_id(data)
        current_devices = self._current_devices(guid)
        TriggerEvent = self.plugin.TriggerEvent

        def FindId(device):
            device_ids = _get_ids(device)
            for device_id in device_ids:
                if device_id.upper().find(vendor_id) > -1:
                    return device_ids
            return ()

        def FindDevices(cls_name, display_name, attr_names, **kwargs):
            devices = self.wmi.ExecQuery(
                "Select * from Win32_" + cls_name
            )

            for device in devices:
                device_ids = FindId(device)

                key = _create_key(device_ids)
                if not key or key in current_devices:
                    continue

                suffix, payload = _create_event(
                    device_ids,
                    attr_names,
                    display_name,
                    device
                )

                current_devices[key] = (suffix, payload)
                TriggerEvent('.'.join(['Device.Attached'] + suffix), payload)
                return True

        if guid in DEVICES:
            if FindDevices(**DEVICES[guid][0]):
                return

        for guid in SEARCH:
            for dev in DEVICES[guid]:
                if FindDevices(**dev):
                    return

        TriggerEvent('Device.Attached', [data])

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

    def _current_devices(self, guid):
        guid = guid.upper()
        if guid not in self.currentDevices:
            self.currentDevices[guid] = {}
        return self.currentDevices[guid]

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
            current_devices = self._current_devices(guid)
            for dev in DEVICES[guid]:
                devices = wmi.ExecQuery(
                    "Select * from Win32_" + dev['cls_name']
                )

                for device in devices:
                    device_ids = _get_ids(device)
                    if not device_ids:
                        continue

                    current_devices[_create_key(device_ids)] = _create_event(
                        device_ids,
                        dev['attr_names'],
                        dev['display_name'],
                        device
                    )

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

    __docsort__ = ('__call__',)

    name = 'Get System Devices'
    description = (
        'Returns a device object that represents a physical device\n'
        'on your computer.'
    )

    def __init__(self):
        self.result = None

    def __call__(self, pattern=None, **kwargs):
        """
        Searches Windows WMI for devices matching a user supplied string.

        Calls Windows WMI for device instances and then searches the instances
         Caption, Name, HardwareId, DeviceId, DeviceID attributes to see if
         they match the string that has been supplied.

        Wildcards can be used :
            ? Matches a single character
            * Matches a  series of characters

        When using this action it is advisable to pass the search text via a
        keyword. the keyword you would use is the device type. it is very
        expensive to iterate through all of the devices on a computer. If you
        also use wildcards it could take a while to return the devices. The
        device types can be gotten from the configuration dialog for this
        action. They are container labels for the devices, all you need do is
        remove any spaces.

        The returned value is a tuple of device instances.. Each device comes
        from a device type and each device type may have different attributes.
        So you will need to read the Help for the different device types you
        want to access. These help files contain all of the attribute names
        and a description of them. The help is located in this actions
        configuration panel, you just need to click on the device type you
        want to know about and the help will load.

        :param pattern: str() text to search for.

        GetDevices('SOME HDD NAME')

        :param kwargs: Keyword must be a valid device type. Value is the string
         to search for.

        GetDevices(DiskDrive='SOME HDD NAME')

        :return: tuple() WMI instances that represent a device.
        """

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

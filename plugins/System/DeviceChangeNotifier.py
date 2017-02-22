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
)

DEVICE_ATTRIBUTES = (
    ('Keyboard', ()),
    ('PointingDevice', (
        'Manufacturer',
        'NumberOfButtons',
        'Resolution',
        'SampleRate',
        'HardwareType'
    )),
    ('CDROMDrive', (
        'CompressionMethod',
        'Drive',
        'Manufacturer',
        'MaxMediaSize',
        'MediaLoaded',
        'MediaType'
    )),
    ('SCSIController', ('Manufacturer',)),
    ('SerialPort', ()),
    ('SoundDevice', ('Manufacturer', 'ProductName')),
    ('USBController', ('Manufacturer',)),
    ('USBHub', ('USBVersion',)),
    ('NetworkAdapter', (
        'AdapterType',
        'MACAddress',
        'Manufacturer',
        'MaxSpeed',
        'NetworkAddresses'
    )),
    ('Battery', (
        'BatteryRechargeTime',
        'EstimatedChargeRemaining',
        'ExpectedBatteryLife',
        'FullChargeCapacity',
        'MaxRechargeTime'
    )),
    ('PortableBattery', (
        'DesignVoltage',
        'DesignCapacity',
        'ExpectedBatteryLife',
        'EstimatedRunTime',
        'ExpectedLife',
        'Manufacturer',
        'ManufactureDate',
        'TimeOnBattery',
        'MaxRechargeTime'
    )),
    ('DesktopMonitor', (
        'DisplayType',
        'MonitorManufacturer',
        'MonitorType',
        ('ScreenWidth', 'ScreenHeight')
    )),
    ('VideoController', (
        'VideoProcessor',
        'AdapterRAM',
        ('CurrentHorizontalResolution', 'CurrentVerticalResolution')
    )),
    ('DiskDrive', (
        'FirmwareRevision',
        'Model',
        'Manufacturer',
        'InterfaceType',
        'Partitions',
        'MediaLoaded',
        'MediaType',
        'Size'
    )),
    ('PNPEntity', ()),
)


class DeviceChangeNotifier:
    def __init__(self, plugin):
        self.currentDevices = {}
        self.WMI = None
        self.plugin = plugin
        eg.messageReceiver.AddHandler(WM_DEVICECHANGE, self.OnDeviceChange)

        def Register(guid):
            return RegisterDeviceNotification(
                eg.messageReceiver.hwnd,
                pointer(
                    DEV_BROADCAST_DEVICEINTERFACE(
                        dbcc_devicetype=DBT_DEVTYP_DEVICEINTERFACE,
                        dbcc_classguid=guid
                    )
                ),
                0
            )

        # Disk device class
        self.handle1 = Register("{53F5630D-B6BF-11D0-94F2-00A0C91EFB8B}")
        # HID device class
        self.handle2 = Register("{4d1e55b2-f16f-11cf-88cb-001111000030}")
        # USB device class
        self.handle3 = Register("{A5DCBF10-6530-11D2-901F-00C04FB951ED}")
        # Monitor device class
        self.handle4 = Register("{E6F07B5F-EE97-4a90-B076-33F57BF4EAA7}")
        # Serial Port
        self.handle5 = Register("{86E0D1E0-8089-11D0-9CE4-08003E301F73}")
        # Windows Portable Devices
        self.handle6 = Register("{6AC27878-A6FA-4155-BA85-F98F491D4F33}")
        # Network Adapters
        self.handle7 = Register("{CAC88484-7515-4C03-82E6-71A87ABAC361}")
        # Modems
        self.handle8 = Register("{2C7089AA-2E0E-11D1-B114-00C04FC2AAE4}")
        # Keyboard
        self.handle9 = Register("{884b96c3-56ef-11d1-bc8c-00a0c91405dd}")
        # Mouse
        self.handle10 = Register("{378DE44C-56EF-11D1-BC8C-00A0C91405DD}")
        # Display Adapter
        self.handle11 = Register("{5B45201D-F2F2-4F3B-85BB-30FF1F953599}")
        # Blue Teeth
        self.handle12 = Register("{0850302A-B344-4fda-9BE9-90576B8D46F0}")

        wx.CallAfter(self.StartWMI)

    def Close(self):
        UnregisterDeviceNotification(self.handle1)
        UnregisterDeviceNotification(self.handle2)
        UnregisterDeviceNotification(self.handle3)
        UnregisterDeviceNotification(self.handle4)
        UnregisterDeviceNotification(self.handle5)
        UnregisterDeviceNotification(self.handle6)
        UnregisterDeviceNotification(self.handle7)
        UnregisterDeviceNotification(self.handle8)
        UnregisterDeviceNotification(self.handle9)
        UnregisterDeviceNotification(self.handle10)
        UnregisterDeviceNotification(self.handle11)
        UnregisterDeviceNotification(self.handle12)
        eg.messageReceiver.RemoveHandler(WM_DEVICECHANGE, self.OnDeviceChange)

    def StartWMI(self):
        self.WMI = WMI = win32com.client.GetObject("winmgmts:")
        for deviceType, attrNames in DEVICE_ATTRIBUTES:
            devices = WMI.InstancesOf('Win32_' + deviceType)
            for device in devices:
                self.currentDevices[device.DeviceId] = device.Name

    def TriggerEvent(self, suffix, vendorId, driveLetters=None):
        vendorId = '\\'.join(vendorId.replace('\\\\?\\', '').split('#')[:2])

        if suffix.endswith('Removed.'):
            for deviceId in self.currentDevices.keys():
                if deviceId.find(vendorId) > -1:
                    payload = dict(
                        name=self.currentDevices[deviceId],
                        device_id=deviceId
                    )
                    suffix += payload['name']
                    if driveLetters is None:
                        self.plugin.TriggerEvent(suffix, payload)
                    else:
                        for letter in driveLetters:
                            self.plugin.TriggerEvent(
                                suffix + '.' + letter,
                                payload
                            )
                    del(self.currentDevices[deviceId])
                    return

        for deviceType, attrNames in DEVICE_ATTRIBUTES:
            for device in self.WMI.InstancesOf('Win32_' + deviceType):
                if device.DeviceId.find(vendorId) > -1:
                    payload = {
                        attrName: getattr(device, attrName)
                        for attrName in attrNames
                    }
                    payload.update(dict(
                        name=device.Name,
                        description=device.Description,
                        status=device.Status,
                        device_id=device.DeviceId
                    ))
                    suffix += device.Name

                    if driveLetters is None:
                        self.plugin.TriggerEvent(suffix, payload)
                    else:
                        for letter in driveLetters:
                            self.plugin.TriggerEvent(
                                suffix + '.' + letter,
                                payload
                            )
                    self.currentDevices[device.DeviceId] = device.Name
                    return

    def OnDeviceChange(self, hwnd, msg, wparam, lparam):
        #
        # WM_DEVICECHANGE:
        #  wParam - type of change: arrival, removal etc.
        #  lParam - what's changed?
        #    if it's a volume then...
        #  lParam - what's changed more exactly
        #

        if wparam == DBT_DEVICEARRIVAL:
            dbch = DEV_BROADCAST_HDR.from_address(lparam)
            if dbch.dbch_devicetype == DBT_DEVTYP_VOLUME:
                dbcv = DEV_BROADCAST_VOLUME.from_address(lparam)
                wx.CallAfter(
                    self.TriggerEvent,
                    "DriveMounted.",
                    wstring_at(lparam + DBD_NAME_OFFSET),
                    DriveLettersFromMask(dbcv.dbcv_unitmask)
                )

            elif dbch.dbch_devicetype == DBT_DEVTYP_DEVICEINTERFACE:
                wx.CallAfter(
                    self.TriggerEvent,
                    "DeviceAttached.",
                    wstring_at(lparam + DBD_NAME_OFFSET)
                )

        elif wparam == DBT_DEVICEREMOVECOMPLETE:
            dbch = DEV_BROADCAST_HDR.from_address(lparam)
            if dbch.dbch_devicetype == DBT_DEVTYP_VOLUME:
                dbcv = DEV_BROADCAST_VOLUME.from_address(lparam)
                wx.CallAfter(
                    self.TriggerEvent,
                    "DriveRemoved.",
                    wstring_at(lparam + DBD_NAME_OFFSET),
                    DriveLettersFromMask(dbcv.dbcv_unitmask)
                )
            elif dbch.dbch_devicetype == DBT_DEVTYP_DEVICEINTERFACE:
                wx.CallAfter(
                    self.TriggerEvent,
                    "DeviceRemoved.",
                    wstring_at(lparam + DBD_NAME_OFFSET)
                )
        return 1


class DEV_BROADCAST_DEVICEINTERFACE(DEV_BROADCAST_DEVICEINTERFACE):
    def __init__(self, dbcc_devicetype=0, dbcc_classguid=None):
        self.dbcc_devicetype = dbcc_devicetype
        CLSIDFromString(dbcc_classguid, self.dbcc_classguid)
        self.dbcc_size = sizeof(DEV_BROADCAST_DEVICEINTERFACE)

DBD_NAME_OFFSET = DEV_BROADCAST_DEVICEINTERFACE.dbcc_name.offset


def DriveLettersFromMask(mask):
    return [
        chr(65 + driveNum) for driveNum in range(0, 26)
        if (mask & (2 ** driveNum))
    ]


class GetDevices(eg.ActionBase):
    name = 'Get System Devices'
    description = (
        'Returns a device object that represents a physical device\n'
        'on your computer.'
    )

    WMI_CLASSES = dict(
        Battery=dict(url_id=394074, search='Caption'),
        CDROMDrive=dict(url_id=394081, search='Caption'),
        CacheMemory=dict(url_id=394080, search='DeviceID'),
        DesktopMonitor=dict(url_id=394122, search='Caption'),
        DiskDrive=dict(url_id=394132, search='Caption'),
        Fan=dict(url_id=394146, search='Caption'),
        FloppyController=dict(url_id=394148, search='Caption'),
        FloppyDrive=dict(url_id=394149, search='Caption'),
        HeatPipe=dict(url_id=394154, search='Caption'),
        IDEController=dict(url_id=394155, search='Caption'),
        InfraredDevice=dict(url_id=394158, search='Caption'),
        Keyboard=dict(url_id=394166, search='Description'),
        MotherboardDevice=dict(url_id=394204, search='Name'),
        NetworkAdapter=dict(url_id=394216, search='Description'),
        OnBoardDevice=dict(url_id=394238, search='Caption'),
        PCMCIAController=dict(url_id=394251, search='Caption'),
        POTSModem=dict(url_id=394360, search='Caption'),
        ParallelPort=dict(url_id=394247, search='Caption'),
        PhysicalMedia=dict(url_id=394346, search='Tag'),
        PhysicalMemory=dict(url_id=394347, search='Tag'),
        PointingDevice=dict(url_id=394356, search='Caption'),
        PortableBattery=dict(url_id=394357, search='Caption'),
        Printer=dict(url_id=394363, search='Caption'),
        PrinterController=dict(url_id=394365, search='Caption'),
        Processor=dict(url_id=394373, search='Name'),
        Refrigeration=dict(url_id=394393, search='Caption'),
        SCSIController=dict(url_id=394400, search='Caption'),
        SerialPort=dict(url_id=394413, search='Caption'),
        SoundDevice=dict(url_id=394463, search='Caption'),
        SystemSlot=dict(url_id=394486, search='SlotDesignation'),
        TCPIPPrinterPort=dict(url_id=394492, search='Caption'),
        TapeDrive=dict(url_id=394491, search='Caption'),
        TemperatureProbe=dict(url_id=394493, search='Caption'),
        USBController=dict(url_id=394504, search='Caption'),
        USBHub=dict(url_id=394506, search='Caption'),
        VideoController=dict(url_id=394512, search='Caption'),
        VoltageProbe=dict(url_id=394514, search='Caption'),
    )

    WMI_CLASSES['1394Controller'] = dict(url_id=394059, search='Caption')
    WMI_CLASSES['1394ControllerDevice'] = dict(url_id=394060, search='Caption')
    HELP_URL = 'https://msdn.microsoft.com/en-us/library/aa%d(v=vs.85).aspx'

    def __call__(self, pattern=None, **kwargs):
        if pattern is None and not kwargs:
            return

        if isinstance(pattern, dict):
            searchCls = pattern.keys()
            pattern = pattern[searchCls[0]]
        elif pattern is not None:
            searchCls = self.WMI_CLASSES.keys()
        else:
            if len(kwargs.keys()) > 1:
                eg.PrintNotice(
                    'You can only specify one device to search for.\n'
                    'If you want to broaden your search use ? or * as'
                    ' wildcards'
                )
                return
            searchCls = kwargs.keys()
            pattern = kwargs[searchCls[0]]

        searchableItems = {}

        WMI = win32com.client.GetObject("winmgmts:")
        for clsName in searchCls:
            primarySearch = self.WMI_CLASSES[clsName]['search']
            for device in WMI.InstancesOf('Win32_' + clsName):
                searchItem = getattr(device, primarySearch)
                searchableItems[searchItem] = device
                if device.Name is not None:
                    if device.Name not in searchableItems:
                        searchableItems[device.Name] = device
                if device.Description is not None:
                    if device.Description not in searchableItems:
                        searchableItems[device.Description] = device
                if hasattr(device, 'DeviceId') and device.DeviceId is not None:
                    if device.DeviceId not in searchableItems:
                        searchableItems[device.DeviceId] = device
                if hasattr(device, 'HardwareId') and device.HardwareId is not None:
                    if device.HardwareId not in searchableItems:
                        searchableItems[device.HardwareId] = device

        if '*' not in pattern and '?' not in pattern:
            if pattern in searchableItems:
                eg.Print('Device Found')
                return (searchableItems[pattern],)
            return None

        devices = ()
        for key in searchableItems.keys():
            if fnmatch.fnmatch(key, pattern):
                if searchableItems[key] not in devices:
                    devices += (searchableItems[key],)

        eg.Print(str(len(devices)) + ' Devices Found')
        return devices

    def Configure(self, pattern=''):
        WMI = win32com.client.GetObject("winmgmts:")
        panel = eg.ConfigPanel()
        panel.EnableButtons(False)

        self.result = pattern

        tree = wx.TreeCtrl(
            panel,
            -1,
            style=(
                wx.TR_HAS_BUTTONS |
                wx.TR_ROW_LINES |
                wx.CLIP_CHILDREN
            )
        )

        root = tree.AddRoot('Devices')

        for clsName in sorted(self.WMI_CLASSES.keys()):
            label = ''
            for char in clsName:
                if not char.isdigit():
                    match = char.lower() == char
                    if match and label[-1].lower() != label[-1]:
                        label = label[:len(label) - 1] + ' ' + label[-1]
                    elif not match and label and label[-1].isdigit():
                        label += ' '
                label += char
            deviceTree = tree.AppendItem(root, label)

            attrName = self.WMI_CLASSES[clsName]['search']
            for device in WMI.InstancesOf('Win32_' + clsName):
                deviceLabel = getattr(device, attrName)
                deviceItem = tree.AppendItem(deviceTree, deviceLabel)
                tree.SetPyData(deviceItem, {clsName: deviceLabel})
                if self.result == {clsName: deviceLabel}:
                    tree.SelectItem(deviceItem)

        def OnActivated(evt):
            item = evt.GetItem()
            if item.IsOk():
                if tree.ItemHasChildren(item):
                    if tree.IsExpanded(item):
                        tree.Collapse(item)
                    else:
                        tree.Expand(item)
                    panel.EnableButtons(False)
                else:
                    self.result = tree.GetPyData(item)
                    panel.EnableButtons(True)
            evt.Skip()

        def OnSelectionChanged(evt):
            item = evt.GetItem()
            if item.IsOk():
                if tree.ItemHasChildren(item):
                    panel.EnableButtons(False)
                    self.result = None
                else:
                    self.result = tree.GetPyData(item)
                    panel.EnableButtons(True)
            evt.Skip()

        tree.Expand(root)
        tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, OnActivated)
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, OnSelectionChanged)

        panel.sizer.Add(tree, 1, wx.EXPAND | wx.ALL, 10)

        while panel.Affirmed():
            panel.SetResult(self.result)

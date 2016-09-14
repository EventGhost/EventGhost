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

class DeviceChangeNotifier:
    def __init__(self, plugin):
        self.TriggerEvent = plugin.TriggerEvent
        eg.messageReceiver.AddHandler(WM_DEVICECHANGE, self.OnDeviceChange)

        # Disk device class
        self.handle1 = RegisterDeviceNotification(
            eg.messageReceiver.hwnd,
            pointer(
                DEV_BROADCAST_DEVICEINTERFACE(
                    dbcc_devicetype = DBT_DEVTYP_DEVICEINTERFACE,
                    dbcc_classguid = "{53f56307-b6bf-11d0-94f2-00a0c91efb8b}"
                )
            ),
            0
        )
        # HID device class
        self.handle2 = RegisterDeviceNotification(
            eg.messageReceiver.hwnd,
            pointer(
                DEV_BROADCAST_DEVICEINTERFACE(
                    dbcc_devicetype = DBT_DEVTYP_DEVICEINTERFACE,
                    dbcc_classguid = "{4d1e55b2-f16f-11cf-88cb-001111000030}"
                )
            ),
            0
        )
        # USB device class
        self.handle3 = RegisterDeviceNotification(
            eg.messageReceiver.hwnd,
            pointer(
                DEV_BROADCAST_DEVICEINTERFACE(
                    dbcc_devicetype = DBT_DEVTYP_DEVICEINTERFACE,
                    dbcc_classguid = "{a5dcbf10-6530-11d2-901f-00c04fb951ed}"
                )
            ),
            0
        )
        # Monitor device class
        self.handle4 = RegisterDeviceNotification(
            eg.messageReceiver.hwnd,
            pointer(
                DEV_BROADCAST_DEVICEINTERFACE(
                    dbcc_devicetype = DBT_DEVTYP_DEVICEINTERFACE,
                    dbcc_classguid = "{E6F07B5F-EE97-4a90-B076-33F57BF4EAA7}"
                )
            ),
            0
        )

    def Close(self):
        UnregisterDeviceNotification(self.handle1)
        UnregisterDeviceNotification(self.handle2)
        UnregisterDeviceNotification(self.handle3)
        UnregisterDeviceNotification(self.handle4)
        eg.messageReceiver.RemoveHandler(WM_DEVICECHANGE, self.OnDeviceChange)

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
                for driveLetter in DriveLettersFromMask(dbcv.dbcv_unitmask):
                    self.TriggerEvent("DriveMounted." + driveLetter)
            elif dbch.dbch_devicetype == DBT_DEVTYP_DEVICEINTERFACE:
                deviceName = wstring_at(lparam + DBD_NAME_OFFSET)
                self.TriggerEvent("DeviceAttached", [deviceName])
        elif wparam == DBT_DEVICEREMOVECOMPLETE:
            dbch = DEV_BROADCAST_HDR.from_address(lparam)
            if dbch.dbch_devicetype == DBT_DEVTYP_VOLUME:
                dbcv = DEV_BROADCAST_VOLUME.from_address(lparam)
                for driveLetter in DriveLettersFromMask(dbcv.dbcv_unitmask):
                    self.TriggerEvent("DriveRemoved." + driveLetter)
            elif dbch.dbch_devicetype == DBT_DEVTYP_DEVICEINTERFACE:
                deviceName = wstring_at(lparam + DBD_NAME_OFFSET)
                self.TriggerEvent("DeviceRemoved", [deviceName])
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

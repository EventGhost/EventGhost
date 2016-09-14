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
from Dynamic import (
    CDS_NORESET, CDS_SET_PRIMARY, CDS_UPDATEREGISTRY, ChangeDisplaySettingsEx,
    DEVMODE, DISPLAY_DEVICE, DISPLAY_DEVICE_ATTACHED_TO_DESKTOP,
    DISPLAY_DEVICE_MIRRORING_DRIVER, DISPLAY_DEVICE_PRIMARY_DEVICE,
    DM_BITSPERPEL, DM_DISPLAYFLAGS, DM_DISPLAYFREQUENCY, DM_PELSHEIGHT,
    DM_PELSWIDTH, DM_POSITION, EDS_RAWMODE, ENUM_CURRENT_SETTINGS,
    EnumDisplayDevices, EnumDisplaySettingsEx, pointer, sizeof,
)

class Display(object):
    def __init__(self, iDevNum, displayDevice):
        self.iDevNum = iDevNum
        self.deviceName = displayDevice.DeviceName
        self.deviceString = displayDevice.DeviceString
        self.isPrimary = bool(
            displayDevice.StateFlags & DISPLAY_DEVICE_PRIMARY_DEVICE
        )
        self.devMode = DEVMODE()
        self.devMode.dmSize = sizeof(DEVMODE)
        self.dmp = pointer(self.devMode)

    def GetCurrentMode(self):
        self.Refresh()
        return ((self.width, self.height), self.frequency, self.bitsPerPixel)

    def GetDisplayModes(self, allModes=False):
        devMode = DEVMODE()
        devMode.dmSize = sizeof(DEVMODE)
        lpDevMode = pointer(devMode)
        modes = {}
        if allModes:
            flag = EDS_RAWMODE
        else:
            flag = 0
        iModeNum = 0
        while 0 != EnumDisplaySettingsEx(
            self.deviceName, iModeNum, lpDevMode, flag
        ):
            iModeNum += 1
            resolution = (devMode.dmPelsWidth, devMode.dmPelsHeight)
            deepthDict = modes.setdefault(resolution, {})
            frequencyList = deepthDict.setdefault(devMode.dmBitsPerPel, [])
            frequencyList.append(devMode.dmDisplayFrequency)
        return modes

    def GetRectangle(self):
        """
        Returns the displays position and size as a tuple.

        The fields are: (left, top, width, height)
        """
        self.Refresh()
        return (self.x, self.y, self.width, self.height)

    def Refresh(self):
        name = self.deviceName
        dmp = self.dmp
        EnumDisplaySettingsEx(name, 0, dmp, 0)
        EnumDisplaySettingsEx(name, ENUM_CURRENT_SETTINGS, dmp, 0)
        devMode = self.devMode
        self.x = devMode.dmPosition.x
        self.y = devMode.dmPosition.y
        self.width = devMode.dmPelsWidth
        self.height = devMode.dmPelsHeight
        self.frequency = devMode.dmDisplayFrequency
        self.bitsPerPixel = devMode.dmBitsPerPel

    def SetDisplayMode(self, size, frequency, bitdepth, flags=0):
        devMode = DEVMODE()
        devMode.dmSize = sizeof(DEVMODE)
        devMode.dmPelsWidth = size[0]
        devMode.dmPelsHeight = size[1]
        devMode.dmBitsPerPel = bitdepth
        devMode.dmDisplayFrequency = frequency
        devMode.dmFields = (
            DM_BITSPERPEL |
            DM_PELSWIDTH |
            DM_PELSHEIGHT |
            DM_DISPLAYFREQUENCY
        )
        ChangeDisplaySettingsEx(self.deviceName, pointer(devMode), 0, flags, 0)


def GetDisplay(displayNum):
    displayDevice = DISPLAY_DEVICE()
    displayDevice.cb = sizeof(DISPLAY_DEVICE)
    if EnumDisplayDevices(None, displayNum, pointer(displayDevice), 0) == 0:
        return None
    return Display(displayNum, displayDevice)

def GetDisplays():
    res = []
    displayDevice = DISPLAY_DEVICE()
    displayDevice.cb = sizeof(DISPLAY_DEVICE)
    iDevNum = 0
    while True:
        if EnumDisplayDevices(None, iDevNum, pointer(displayDevice), 0) == 0:
            break
        #DISPLAY_DEVICE_ATTACHED_TO_DESKTOP = 1
        if not (displayDevice.StateFlags & DISPLAY_DEVICE_MIRRORING_DRIVER):
            disp = Display(iDevNum, displayDevice)
            res.append(disp)
            displayDevice = DISPLAY_DEVICE()
            displayDevice.cb = sizeof(DISPLAY_DEVICE)
        iDevNum += 1
    return res

def GetDisplayModes():
    res = []
    displayDevice = DISPLAY_DEVICE()
    displayDevice.cb = sizeof(DISPLAY_DEVICE)
    devMode = DEVMODE()
    devMode.dmSize = sizeof(DEVMODE)
    iDevNum = 0
    while True:
        if EnumDisplayDevices(None, iDevNum, pointer(displayDevice), 0) == 0:
            break
        iDevNum += 1
        if displayDevice.StateFlags & DISPLAY_DEVICE_MIRRORING_DRIVER:
            continue
        EnumDisplaySettingsEx(
            displayDevice.DeviceName,
            ENUM_CURRENT_SETTINGS,
            pointer(devMode),
            0
        )
        displayMode = (
            displayDevice.DeviceName,
            devMode.dmPosition.x,
            devMode.dmPosition.y,
            devMode.dmPelsWidth,
            devMode.dmPelsHeight,
            devMode.dmDisplayFrequency,
            devMode.dmBitsPerPel,
            bool(
                displayDevice.StateFlags & DISPLAY_DEVICE_ATTACHED_TO_DESKTOP
            ),
            bool(displayDevice.StateFlags & DISPLAY_DEVICE_PRIMARY_DEVICE),
            devMode.dmDisplayFlags,
        )
        res.append(displayMode)
    return tuple(res)

def SetDisplayModes(*args):
    for (
        deviceName,
        x,
        y,
        width,
        height,
        freq,
        bitdepth,
        isAttached,
        isPrimary,
        displayFlags
    ) in args:
        devMode = DEVMODE()
        devMode.dmSize = sizeof(DEVMODE)
        if isAttached:
            devMode.dmPosition.x = x
            devMode.dmPosition.y = y
            devMode.dmPelsWidth = width
            devMode.dmPelsHeight = height
            devMode.dmBitsPerPel = bitdepth
            devMode.dmDisplayFrequency = freq
            devMode.dmDisplayFlags = displayFlags
        devMode.dmFields = (
            DM_POSITION |
            DM_BITSPERPEL |
            DM_PELSWIDTH |
            DM_PELSHEIGHT |
            DM_DISPLAYFLAGS |
            DM_DISPLAYFREQUENCY
        )
        flags = (CDS_UPDATEREGISTRY | CDS_NORESET)
        if isPrimary:
            flags |= CDS_SET_PRIMARY
        ChangeDisplaySettingsEx(deviceName, pointer(devMode), 0, flags, 0)
    ChangeDisplaySettingsEx(None, None, 0, 0, 0)

if __name__ == "__main__":
    print GetDisplayModes()

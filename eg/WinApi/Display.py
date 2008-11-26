# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

from eg.WinApi.Dynamic import (
    sizeof, pointer,
    ENUM_CURRENT_SETTINGS, EDS_RAWMODE, EnumDisplayDevices,
    EnumDisplaySettingsEx, ChangeDisplaySettingsEx, DISPLAY_DEVICE, DEVMODE, 
    DISPLAY_DEVICE_MIRRORING_DRIVER, DISPLAY_DEVICE_PRIMARY_DEVICE,
    DISPLAY_DEVICE_ATTACHED_TO_DESKTOP, DM_POSITION, DM_BITSPERPEL,
    DM_PELSWIDTH, DM_PELSHEIGHT, DM_DISPLAYFLAGS, DM_DISPLAYFREQUENCY,
    CDS_UPDATEREGISTRY, CDS_NORESET, CDS_SET_PRIMARY,
)


class Display(object):
    
    def __init__(self, iDevNum, displayDevice):
        self.iDevNum = iDevNum
        self.DeviceName = displayDevice.DeviceName
        self.DeviceString = displayDevice.DeviceString
        self.isPrimary = bool(displayDevice.StateFlags & DISPLAY_DEVICE_PRIMARY_DEVICE)
        self.dm = DEVMODE()
        self.dm.dmSize = sizeof(DEVMODE)
        self.dmp = pointer(self.dm)
    
    
    def Refresh(self):
        name = self.DeviceName
        dmp = self.dmp
        EnumDisplaySettingsEx(name, 0, dmp, 0)
        EnumDisplaySettingsEx(name, ENUM_CURRENT_SETTINGS, dmp, 0)
        dm = self.dm
        self.x = dm.dmPosition.x
        self.y = dm.dmPosition.y
        self.width = dm.dmPelsWidth
        self.height = dm.dmPelsHeight
        self.frequency = dm.dmDisplayFrequency
        self.bitsPerPixel = dm.dmBitsPerPel        
    
    
    def GetDisplayModes(self, all=False):
        dm = DEVMODE()
        dm.dmSize = sizeof(DEVMODE)
        modes = {}
        if all:
            flag = EDS_RAWMODE
        else:
            flag = 0
        iModeNum = 0
        while 0 != EnumDisplaySettingsEx(self.DeviceName, iModeNum, pointer(dm), flag):
            iModeNum += 1
            resolution = (dm.dmPelsWidth, dm.dmPelsHeight)
            deepth_dict = modes.setdefault(resolution, {})
            frequency_list = deepth_dict.setdefault(dm.dmBitsPerPel, [])
            frequency_list.append(dm.dmDisplayFrequency)
        return modes


    def SetDisplayMode(self, size, frequency, bitdepth, flags=0):
        dm = DEVMODE()
        dm.dmSize = sizeof(DEVMODE)
        dm.dmPelsWidth = size[0]
        dm.dmPelsHeight = size[1]
        dm.dmBitsPerPel = bitdepth
        dm.dmDisplayFrequency = frequency
        dm.dmFields = (
            DM_BITSPERPEL
            |DM_PELSWIDTH
            |DM_PELSHEIGHT
            |DM_DISPLAYFREQUENCY
        )
        ChangeDisplaySettingsEx(self.DeviceName, pointer(dm), 0, flags, 0)


    def GetCurrentMode(self):
        self.Refresh()
        return ((self.width, self.height), self.frequency, self.bitsPerPixel)
        
        
    def GetRectangle(self):
        """
        Returns the displays position and size as a tuple.
        
        The fields are: (left, top, width, height)
        """
        self.Refresh()
        return (self.x, self.y, self.width, self.height)
        
        
        
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
            bool(displayDevice.StateFlags & DISPLAY_DEVICE_ATTACHED_TO_DESKTOP),
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
            DM_POSITION
            |DM_BITSPERPEL
            |DM_PELSWIDTH
            |DM_PELSHEIGHT
            |DM_DISPLAYFLAGS
            |DM_DISPLAYFREQUENCY
        )
        flags = (CDS_UPDATEREGISTRY | CDS_NORESET)
        if isPrimary:
            flags |= CDS_SET_PRIMARY
        ChangeDisplaySettingsEx(deviceName, pointer(devMode), 0, flags, 0)
    ChangeDisplaySettingsEx(None, None, 0, 0, 0)          
    
    
if __name__ == "__main__":
    print GetDisplayModes()

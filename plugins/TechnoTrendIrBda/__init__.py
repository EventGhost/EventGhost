# -*- coding: utf-8 -*-
#
# plugins/TechnoTrendIrBda/__init__.py
#
# Copyright (C) 2009 Mika Fischer <mika.fischer@zoopnet.de>
#
# This file is a plugin for EventGhost.
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

eg.RegisterPlugin(
    name            = "TechnoTrend IR Devices (BDA)",
    author          = "Mika Fischer",
    version         = "1.0.1",
    kind            = "remote",
    guid            = "{A0AC16CE-BC3C-4F66-A95B-D4A1A06EC9EE}",
    description     = (
                        'Hardware plugin for TechnoTrend IR receivers '
                        'delivered with TechnoTrend TV cards.'
                      ),
    url             = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=2275",
)

import os
from threading import Timer

from eg.WinApi.Dynamic import (
    cdll, POINTER, c_int, c_uint, CFUNCTYPE
)

KEYMAP = {
    0x41:    "Power",
    0x58:    "Mute",
    0x43:    "Num1",
    0x44:    "Num2",
    0x45:    "Num3",
    0x46:    "Num4",
    0x47:    "Num5",
    0x48:    "Num6",
    0x49:    "Num7",
    0x4A:    "Num8",
    0x4B:    "Num9",
    0x4C:    "Num0",
    0x42:    "Refresh",
    0x5A:    "TV_Radio",
    0x65:    "VolumeUp",
    0x66:    "VolumeDown",
    0x59:    "Text",
    0x4D:    "Up",
    0x4E:    "Left",
    0x4F:    "Ok",
    0x50:    "Right",
    0x51:    "Down",
    0x63:    "ChannelUp",
    0x64:    "ChannelDown",
    0x53:    "Exit",
    0x54:    "Red",
    0x55:    "Green",
    0x56:    "Yellow",
    0x57:    "Blue",
    0x7A:    "Record",
    0x7B:    "Play",
    0x7C:    "Stop",
    0x52:    "Info",
    0x7D:    "Rewind",
    0x7E:    "Pause",
    0x7F:    "Forward",
    0x62:    "Guide",
}

DEVICE_TYPES = [
    "Unknown",
    "Budget 2",
    "Budget 3",
    "USB 2",
    "USB 2 Pinnacle",
    "USB 2 DSS"
]

IRCALLBACKFUNC = CFUNCTYPE(None, c_int, POINTER(c_uint))

class TTIRBDA(eg.PluginBase):

    def __init__(self):
        pass

    def __close__(self):
        pass

    def __start__(self):
        self.dll = None
        self.handles = []
        self.contexts = []

        # Try opening DLL
        paths = [
            os.path.join(os.path.abspath(os.environ["ProgramFiles"]), "TT-Viewer"),
            os.path.abspath(os.path.dirname(__file__)),
        ]
        dll = None
        for path in paths:
            try:
                dll = cdll.LoadLibrary(os.path.join(path, "ttBdaDrvApi_Dll.dll"))
                dll.bdaapiEnumerate.restype = c_uint
                dll.bdaapiOpen.restype = POINTER(c_int)
                dll.bdaapiClose.restype = None
                break
            except WindowsError:
                dll = None

        if dll is None:
            self.PrintError(
                "Couldn't find ttBdaDrvApi_Dll.dll!\n"
                "Install the TT-Viewer application in %s\n"
                "or place the dll in %s." % (paths[0], paths[1])
            )
            raise self.Exceptions.DeviceNotFound


        self.dll = dll
        self.cCallback = IRCALLBACKFUNC(self.IrCallback)
        context = 0
        for type in range(len(DEVICE_TYPES)):
            for index in range(self.dll.bdaapiEnumerate(type)):
                handle = dll.bdaapiOpen(type, index)
                if handle.contents != 0 and handle.contents != -1:
                    error = dll.bdaapiOpenIR(handle, self.cCallback, context)
                    context += 1
                    if (error == 0):
                        #print "Listening to device %s(%d)" % (DEVICE_TYPES[type], index)
                        self.handles.append(handle)
                else:
                    self.dll.bdaapiClose(handle)
        if len(self.handles) == 0:
            raise self.Exceptions.DeviceNotFound
        self.timer = eg.ResettableTimer(self.OnTimeout)
        self.event = None
        self.lastKey = None

    def __stop__(self):
        if self.dll is not None:
            for handle in self.handles:
                self.dll.bdaapiCloseIR(handle)
                self.dll.bdaapiClose(handle)
        self.timer.Stop()

    def OnComputerSuspend(self, dummySuspendType):
        __stop__(self)

    def OnComputerResume(self, dummySuspendType):
        __start__(self)

    def IrCallback(self, context, buffer):
        keystr = None
        try:
            keystr = KEYMAP[buffer.contents.value & 0xFF]
        except KeyError:
            keystr = hex(buffer.contents.value & 0xFF)
        if keystr != self.lastKey:
            if self.event is not None:
                self.event.SetShouldEnd()
            self.event = self.TriggerEnduringEvent(keystr)
            self.lastKey = keystr
        self.timer.Reset(125)

    def OnTimeout(self):
        if self.event is not None:
            self.event.SetShouldEnd()
        self.event = None
        self.lastKey = None


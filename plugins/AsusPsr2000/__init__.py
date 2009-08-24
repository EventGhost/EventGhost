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

ur"""<rst>
A plugin for the ASUS PSR-2000 remote.

**Notice:** You need a special driver to use the remote with this plugin.
Please `download it here`__ and install it while the device is connected.

__ http://www.eventghost.org/downloads/USB-Remote-Driver.exe
"""

import eg

eg.RegisterPlugin(
    name = "ASUS PSR-2000",
    author = "Bitmonster",
    version = "1.0.0",
    kind = "remote",
    guid = "{4365E03A-CA73-4C30-88B8-BA00D6B7E2F5}",
    description = __doc__,
)

from math import atan2, pi
from os.path import dirname, join
import sys
from eg.WinApi.Dynamic import mouse_event, WinDLL, DWORD, BOOL, byref, FormatError

BUTTONS = {
    1: "VCR",
    2: "DVD",
    4: "Radio",
    5: "Red",
    6: "Green",
    7: "Yellow",
    8: "Blue",
    9: "Rewind",
    10: "Play",
    11: "Forward",
    12: "Record",
    13: "Stop",
    15: "VolumeUp",
    16: "VolumeDown",
    17: "Mute",
    18: "ChannelUp",
    19: "ChannelDown",
    23: "Num1",
    24: "Num2",
    25: "Num3",
    26: "Num4",
    27: "Num5",
    28: "Num6",
    29: "Num7",
    30: "Num8",
    31: "Num9",
    33: "Num0",
    35: "Teletext",
    
}

DRIVER_PACKAGE_FORCE = 4
DRIVER_PACKAGE_LEGACY_MODE = 0x10


class AsusPsr2000(eg.PluginBase):

    def __start__(self):
        self.usb = eg.WinUsb(self)
        self.usb.AddDevice(
            "ASUS PSR-2000",
            "USB\\VID_147A&PID_E006",
            "{4365E03A-CA73-4C30-88B8-BA00D6B7E2F5}", 
            self.Callback, 
            4,
            #True
        )
        self.usb.Open()
        self.lastCode = None
        self.lastDirection = None
        self.timer = eg.ResettableTimer(self.OnTimeOut)
        self.leftDown = 0
        self.rightDown = 0
        self.tick = 0
        self.receiveQueue = eg.plugins.Mouse.plugin.thread.receiveQueue


    def __stop__(self):
        self.timer.Stop()
        self.usb.Close()


    def Callback(self, code):
        if code[0] & 0x88:
            x, y = code[1:3]
            leftDown = code[0] & 0x01
            if leftDown != self.leftDown:
                self.leftDown = leftDown
                if leftDown:
                    mouse_event(0x0002, 0, 0, 0, 0)
                else:
                    mouse_event(0x0004, 0, 0, 0, 0)
            rightDown = code[0] & 0x02
            if rightDown != self.rightDown:
                self.rightDown = rightDown
                if rightDown:
                    mouse_event(0x0008, 0, 0, 0, 0)
                else:
                    mouse_event(0x0010, 0, 0, 0, 0)
            if x == 0 and y == 0:
                degree = -2
            else:
                if x > 127:
                    x = x - 256
                if y > 127:
                    y = y - 256
                degree = round((atan2(x, y) / pi) * 180)
                if degree < 0:
                    degree += 360
            if degree != self.lastDirection:
                self.receiveQueue.put(degree)
                self.lastDirection = degree
            self.timer.Reset(75)
            return
        if code != self.lastCode:
            self.lastCode = code
            if code[0] == 64 and code[3] == 15:
                if code[1] == 0:
                    self.TriggerEnduringEvent(
                        BUTTONS.get(code[2], "%s" % code[2])
                    )
                    return
        self.EndLastEvent()


    def OnTimeOut(self):
        self.receiveQueue.put(-2)
        self.lastDirection = None
        if self.leftDown:
            self.leftDown = None
            mouse_event(0x0004, 0, 0, 0, 0)
        if self.rightDown:
            self.rightDown = None
            mouse_event(0x0010, 0, 0, 0, 0)


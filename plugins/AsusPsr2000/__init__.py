# -*- coding: utf-8 -*-
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

ur"""<rst>
A plugin for the ASUS PSR-2000 remote.
"""

import eg

eg.RegisterPlugin(
    name = "ASUS PSR-2000",
    author = "Bitmonster",
    version = "1.0.0",
    kind = "remote",
    guid = "{4365E03A-CA73-4C30-88B8-BA00D6B7E2F5}",
    description = __doc__,
    hardwareId = "USB\\VID_147A&PID_E006",
)

from math import atan2, pi
from os.path import dirname, join
import sys
from eg.WinApi.Dynamic import (
    mouse_event, WinDLL, DWORD, BOOL, byref, FormatError
)

BUTTONS = {
    (64, 0, 1, 15): "VCR",
    (64, 0, 2, 15): "DVD",
    (64, 0, 4, 15): "Radio",
    (64, 0, 5, 15): "Red",
    (64, 0, 6, 15): "Green",
    (64, 0, 7, 15): "Yellow",
    (64, 0, 8, 15): "Blue",
    (64, 0, 9, 15): "Rewind",
    (64, 0, 10, 15): "Play",
    (64, 0, 11, 15): "Forward",
    (64, 0, 12, 15): "Record",
    (64, 0, 13, 15): "Stop",
    (64, 0, 14, 15): "Eject",
    (64, 0, 15, 15): "VolumeUp",
    (64, 0, 16, 15): "VolumeDown",
    (64, 0, 17, 15): "Mute",
    (64, 0, 18, 15): "ChannelUp",
    (64, 0, 19, 15): "ChannelDown",
    (64, 0, 20, 15): "Menu",
    (64, 0, 21, 15): "Bookmark",
    (64, 0, 22, 15): "NumLock",
    (64, 0, 23, 15): "Num1",
    (64, 0, 24, 15): "Num2",
    (64, 0, 25, 15): "Num3",
    (64, 0, 26, 15): "Num4",
    (64, 0, 27, 15): "Num5",
    (64, 0, 28, 15): "Num6",
    (64, 0, 29, 15): "Num7",
    (64, 0, 30, 15): "Num8",
    (64, 0, 31, 15): "Num9",
    (64, 0, 32, 15): "GoUp",
    (64, 0, 33, 15): "Num0",
    (64, 0, 35, 15): "Teletext",
    (64, 0, 36, 15): "GoTo",
}


class AsusPsr2000(eg.PluginBase):

    def __start__(self):
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.Callback, 4).AddHardwareId(
            "ASUS PSR-2000", "USB\\VID_147A&PID_E006"
        )
        self.winUsb.Start()
        self.lastCode = None
        self.lastDirection = None
        self.timer = eg.ResettableTimer(self.OnTimeOut)
        self.leftDown = 0
        self.rightDown = 0
        self.tick = 0
        self.receiveQueue = eg.plugins.Mouse.plugin.thread.receiveQueue


    def __stop__(self):
        self.timer.Stop()
        self.winUsb.Stop()


    def Callback(self, code):
        if code[0] & 0x88:
            buttonType, x, y, dummy = code
            leftDown = buttonType & 0x01
            if leftDown != self.leftDown:
                self.leftDown = leftDown
                if leftDown:
                    mouse_event(0x0002, 0, 0, 0, 0)
                else:
                    mouse_event(0x0004, 0, 0, 0, 0)

            rightDown = buttonType & 0x02
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
                    x -= 256
                if y > 127:
                    y -= 256
                degree = (round((atan2(x, y) / pi) * 180) + 360) % 360
            if degree != self.lastDirection:
                self.receiveQueue.put(degree)
                self.lastDirection = degree
            self.timer.Reset(75)
        elif code != self.lastCode:
            self.lastCode = code
            if code in BUTTONS:
                self.TriggerEnduringEvent(BUTTONS[code])
            else:
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


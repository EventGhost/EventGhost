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

r"""<rst>
Plugin for the PHX01RN USB Remote
"""

import eg

eg.RegisterPlugin(
    name="PHX01RN",
    description=__doc__,
    author="Bitmonster",
    version="1.0.0",
    kind="remote",
    guid="{0B5511F9-6E8D-447D-9BD7-340E2C3548DD}",
    usbIds = ["USB\\VID_0755&PID_2626"],
)

REMOTE_BUTTONS = {
    (1, 4, 0, 61, 0, 0, 0, 0): ("Close", 0),
    (1, 1, 0, 8, 0, 0, 0, 0): ("Video", 0),
    (1, 1, 0, 23, 0, 0, 0, 0): ("TV", 0),
    (1, 1, 0, 4, 0, 0, 0, 0): ("Radio", 0),
    (1, 1, 0, 12, 0, 0, 0, 0): ("Pictures", 0),
    (1, 1, 0, 16, 0, 0, 0, 0): ("Music", 0),
    (1, 3, 0, 16, 0, 0, 0, 0): ("DvdMenu", 0),
    (1, 0, 0, 30, 0, 0, 0, 0): ("Num1", 0),
    (1, 0, 0, 31, 0, 0, 0, 0): ("Num2", 0),
    (1, 0, 0, 32, 0, 0, 0, 0): ("Num3", 0),
    (1, 0, 0, 33, 0, 0, 0, 0): ("Num4", 0),
    (1, 0, 0, 34, 0, 0, 0, 0): ("Num5", 0),
    (1, 0, 0, 35, 0, 0, 0, 0): ("Num6", 0),
    (1, 0, 0, 36, 0, 0, 0, 0): ("Num7", 0),
    (1, 0, 0, 37, 0, 0, 0, 0): ("Num8", 0),
    (1, 0, 0, 38, 0, 0, 0, 0): ("Num9", 0),
    (1, 0, 0, 39, 0, 0, 0, 0): ("Num0", 0),
    (1, 2, 0, 37, 0, 0, 0, 0): ("Star", 0),
    (1, 2, 0, 32, 0, 0, 0, 0): ("Dash", 0),
    (1, 0, 0, 41, 0, 0, 0, 0): ("Clear", 0),
    (1, 4, 0, 40, 0, 0, 0, 0): ("Fullscreen", 0),
    (1, 1, 0, 21, 0, 0, 0, 0): ("Record", 0),
    (1, 12, 0, 40, 0, 0, 0, 0): ("Menu", 0),
    (1, 8, 0, 7, 0, 0, 0, 0): ("Desktop", 0),
    (1, 0, 0, 75, 0, 0, 0, 0): ("ChannelUp", 0),
    (1, 0, 0, 78, 0, 0, 0, 0): ("ChannelDown", 0),
    (1, 0, 0, 40, 0, 0, 0, 0): ("Ok", 0),
    (1, 0, 0, 79, 0, 0, 0, 0): ("Right", 1),
    (1, 0, 0, 80, 0, 0, 0, 0): ("Left", 1),
    (1, 0, 0, 81, 0, 0, 0, 0): ("Down", 1),
    (1, 0, 0, 82, 0, 0, 0, 0): ("Up", 1),
    (1, 0, 0, 42, 0, 0, 0, 0): ("Back", 0),
    (1, 0, 0, 101, 0, 0, 0, 0): ("More", 0),
    (2, 129, 0, 0, 0, 0, 0, 0): ("Power", 0),
    (3, 1, 0, 0, 0, 0, 0, 0): ("MouseLeftButton", 0),
    (3, 2, 0, 0, 0, 0, 0, 0): ("MouseRightButton", 0),
    (4, 35, 2, 0, 0, 0, 0, 0): ("WWW", 0),
    (4, 36, 2, 0, 0, 0, 0, 0): ("Previous", 0),
    (4, 37, 2, 0, 0, 0, 0, 0): ("Next", 0),
    (4, 138, 1, 0, 0, 0, 0, 0): ("E-Mail", 0),
    (4, 179, 0, 0, 0, 0, 0, 0): ("Forward", 0),
    (4, 180, 0, 0, 0, 0, 0, 0): ("Rewind", 0),
    (4, 181, 0, 0, 0, 0, 0, 0): ("NextTrack", 0),
    (4, 182, 0, 0, 0, 0, 0, 0): ("PreviousTrack", 0),
    (4, 183, 0, 0, 0, 0, 0, 0): ("Stop", 0),
    (4, 205, 0, 0, 0, 0, 0, 0): ("Play", 0),
    (4, 226, 0, 0, 0, 0, 0, 0): ("Mute", 0),
    (4, 233, 0, 0, 0, 0, 0, 0): ("VolumeUp", 1),
    (4, 234, 0, 0, 0, 0, 0, 0): ("VolumeDown", 1),
}

STOP_CODES = set([
    (1, 0, 0, 0, 0, 0, 0, 0),
    (2, 0, 0, 0, 0, 0, 0, 0),
    (3, 0, 0, 0, 0, 0, 0, 0),
    (4, 0, 0, 0, 0, 0, 0, 0),
])


class PHX01RN(eg.PluginBase):

    def __start__(self):
        self.usb = eg.WinUsb(self)
        self.usb.AddDevice(
            "PHX01RN USB Receiver",
            "USB\\VID_0755&PID_2626",
            "{7D0541A9-9CF3-439E-BA91-CD4C2A1EBAAA}",
            self.Callback,
            8
        )
        self.usb.Open()
        self.lastButton = None
        self.lastMouseValue = (0, 0)
        self.timer = eg.ResettableTimer(self.OnTimeOut)
        

    def __stop__(self):
        self.timer.Stop()
        self.usb.Close()


    def OnTimeOut(self):
        self.lastButton = None
        self.lastMouseValue = (0, 0)
        self.EndLastEvent()


    def Callback(self, data):
        if data in REMOTE_BUTTONS:
            suffix, bType = REMOTE_BUTTONS[data]
            if bType:
                self.timer.Reset(175)
                if suffix != self.lastButton:
                    self.TriggerEnduringEvent(suffix)
            else:
                self.timer.Reset(None)
                self.TriggerEvent(suffix)
            self.lastButton = suffix
            self.lastMouseValue = (0, 0)
        elif data in STOP_CODES:
            self.timer.Reset(175)
        elif data[0] == 3:
            isFirst = False
            lastX, lastY = self.lastMouseValue
            x, y = data[2:4]
            if x > 127:
                x -= 256
            if y > 127:
                y -= 256
            if x > 0:
                suffix = "MouseRight"
                if x < lastX or lastX == 0:
                    isFirst = True
            elif x < 0:
                suffix = "MouseLeft"
                if x > lastX or lastX == 0:
                    isFirst = True
            elif y < 0:
                suffix = "MouseUp"
                if y > lastY or lastY == 0:
                    isFirst = True
            elif y > 0:
                suffix = "MouseDown"
                if y < lastY or lastY == 0:
                    isFirst = True
            if isFirst:
                self.TriggerEnduringEvent(suffix)
                self.timer.Reset(200)
            else:
                self.timer.Reset(100)
            self.lastButton = suffix
            self.lastMouseValue = (x, y)
        else:
            self.timer.Reset(None)
            self.EndLastEvent()
            self.lastButton = None
            self.lastMouseValue = (0, 0)
            print data

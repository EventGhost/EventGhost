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
Plugin for some small no-name USB-PC-Remote from China.
"""

import eg

eg.RegisterPlugin(
    name = "Small PC-Remote",
    author = "Bitmonster",
    version = "1.0.0",
    kind = "remote",
    guid = "{B7440E71-AE2F-4928-9270-5728E81FED5B}",
    description = __doc__,
    hardwareId = "USB\\VID_073A&PID_2230",
)

from math import atan2, pi

# the first byte of every code chain identifies the length of the chain
LENGTHES = {
    1: 3,
    2: 4,
    3: 3,
    4: 3,
    5: 4,
    6: 3,
}

CODES = {
    (6, 129, 0): (0, 'Power', 3),
    (3, 138, 1): (3, 'eMail', 3),
    (3, 35, 2): (3, 'WWW', 3),
    (1, 4, 61): (3, 'Close', 3),
    (1, 5, 4): (17, 'A', 10),
    (1, 5, 5): (17, 'B', 10),
    (1, 5, 6): (17, 'C', 10),
    (1, 5, 7): (17, 'D', 10),
    (3, 182, 0): (3, 'PreviousTrack', 3),
    (3, 181, 0): (3, 'NextTrack', 3),
    (3, 203, 0): (10, 'FastRewind', 13),
    (3, 202, 0): (10, 'FastForward', 13),
    (3, 205, 0): (3, 'Play', 3),
    (3, 183, 0): (3, 'Stop', 3),
    (3, 48, 2): (15, 'Fullscreen', 9),
    (3, 226, 0): (3, 'Mute', 3),
    (3, 234, 0): (0, 'VolumeDown', 3),
    (3, 233, 0): (0, 'VolumeUp', 3),
    (1, 0, 42): (0, 'Backspace', 3),
    (1, 0, 75): (0, 'PageUp', 3),
    (1, 0, 78): (0, 'PageDown', 3),
    (1, 8, 8): (3, 'MyPc', 3),
    (1, 8, 7): (3, 'Desktop', 3),
    (1, 0, 43): (0, 'Tab', 3),
    (5, 0, 42, 30): (4, 'Tab', 4),
    (5, 0, 42, 54): (4, 'Tab', 4),
    (5, 0, 42, 55): (4, 'Tab', 4),
    (5, 2, 42, 56): (4, 'Tab', 4),
    (5, 0, 0, 54): (4, 'Tab', 4),
    (1, 0, 82): (0, 'Up', 3),
    (5, 0, 0, 4): (4, 'Up', 4),
    (5, 0, 42, 5): (4, 'Up', 4),
    (5, 0, 42, 6): (4, 'Up', 4),
    (5, 0, 42, 31): (4, 'Up', 4),
    (5, 0, 42, 4): (4, 'Up', 4),
    (5, 2, 42, 4): (4, 'Up', 4),
    (5, 2, 42, 5): (4, 'Up', 4),
    (5, 2, 42, 6): (4, 'Up', 4),
    (5, 2, 0, 4): (4, 'Up', 4),
    (1, 8, 0): (3, 'Start', 3),
    (5, 0, 0, 7): (4, 'Start', 4),
    (5, 0, 42, 8): (4, 'Start', 4),
    (5, 0, 42, 9): (4, 'Start', 4),
    (5, 0, 42, 32): (4, 'Start', 4),
    (5, 0, 42, 7): (4, 'Start', 4),
    (5, 2, 0, 7): (4, 'Start', 4),
    (5, 2, 42, 7): (4, 'Start', 4),
    (5, 2, 42, 8): (4, 'Start', 4),
    (5, 2, 42, 9): (4, 'Start', 4),
    (1, 0, 80): (0, 'Left', 3),
    (5, 0, 0, 10): (4, 'Left', 4),
    (5, 0, 42, 10): (4, 'Left', 4),
    (5, 0, 42, 11): (4, 'Left', 4),
    (5, 0, 42, 12): (4, 'Left', 4),
    (5, 0, 42, 33): (4, 'Left', 4),
    (5, 2, 0, 10): (4, 'Left', 4),
    (5, 2, 42, 10): (4, 'Left', 4),
    (5, 2, 42, 11): (4, 'Left', 4),
    (5, 2, 42, 12): (4, 'Left', 4),
    (1, 0, 40): (0, 'Ok', 3),
    (5, 0, 0, 13): (4, 'Ok', 4),
    (5, 0, 42, 14): (4, 'Ok', 4),
    (5, 0, 42, 15): (4, 'Ok', 4),
    (5, 0, 42, 34): (4, 'Ok', 4),
    (5, 0, 42, 13): (4, 'Ok', 4),
    (5, 2, 0, 13): (4, 'Ok', 4),
    (5, 2, 42, 13): (4, 'Ok', 4),
    (5, 2, 42, 14): (4, 'Ok', 4),
    (5, 2, 42, 15): (4, 'Ok', 4),
    (1, 0, 79): (0, 'Right', 3),
    (5, 0, 0, 16): (4, 'Right', 4),
    (5, 0, 42, 16): (4, 'Right', 4),
    (5, 0, 42, 17): (4, 'Right', 4),
    (5, 0, 42, 18): (4, 'Right', 4),
    (5, 0, 42, 35): (4, 'Right', 4),
    (5, 2, 0, 16): (4, 'Right', 4),
    (5, 2, 42, 16): (4, 'Right', 4),
    (5, 2, 42, 17): (4, 'Right', 4),
    (5, 2, 42, 18): (4, 'Right', 4),
    (1, 1, 18): (0, 'Open', 3),
    (5, 0, 0, 19): (4, 'Open', 4),
    (5, 0, 42, 19): (4, 'Open', 4),
    (5, 0, 42, 20): (4, 'Open', 4),
    (5, 0, 42, 21): (4, 'Open', 4),
    (5, 0, 42, 22): (4, 'Open', 4),
    (5, 0, 42, 36): (4, 'Open', 4),
    (5, 2, 0, 19): (4, 'Open', 4),
    (5, 2, 42, 19): (4, 'Open', 4),
    (5, 2, 42, 20): (4, 'Open', 4),
    (5, 2, 42, 21): (4, 'Open', 4),
    (5, 2, 42, 22): (4, 'Open', 4),
    (1, 0, 81): (0, 'Down', 3),
    (5, 0, 0, 23): (4, 'Down', 4),
    (5, 0, 42, 23): (4, 'Down', 4),
    (5, 0, 42, 24): (4, 'Down', 4),
    (5, 0, 42, 25): (4, 'Down', 4),
    (5, 0, 42, 37): (4, 'Down', 4),
    (5, 2, 0, 23): (4, 'Down', 4),
    (5, 2, 42, 23): (4, 'Down', 4),
    (5, 2, 42, 24): (4, 'Down', 4),
    (5, 2, 42, 25): (4, 'Down', 4),
    (1, 0, 41): (0, 'Esc', 3),
    (5, 0, 0, 26): (4, 'Esc', 4),
    (5, 0, 42, 26): (4, 'Esc', 4),
    (5, 0, 42, 27): (4, 'Esc', 4),
    (5, 0, 42, 28): (4, 'Esc', 4),
    (5, 0, 42, 29): (4, 'Esc', 4),
    (5, 0, 42, 38): (4, 'Esc', 4),
    (5, 2, 0, 26): (4, 'Esc', 4),
    (5, 2, 42, 26): (4, 'Esc', 4),
    (5, 2, 42, 27): (4, 'Esc', 4),
    (5, 2, 42, 28): (4, 'Esc', 4),
    (5, 2, 42, 29): (4, 'Esc', 4),
    (1, 4, 43): (3, 'SwitchWindows', 3),
    (5, 0, 0, 44): (4, 'SwitchWindows', 4),
    (5, 2, 42, 31): (4, 'SwitchWindows', 4),
    (5, 2, 42, 37): (4, 'SwitchWindows', 4),
    (5, 2, 42, 32): (4, 'SwitchWindows', 4),
    (5, 0, 42, 39): (4, 'SwitchWindows', 4),
    (5, 0, 42, 44): (4, 'SwitchWindows', 4),
}


class SmallPcRemote(eg.PluginBase):

    def __start__(self):
        self.buf = []
        self.lastDirection = None
        self.lastMouseState = 0
        self.stopCodeLength = 0
        self.bytesToIgnore = 0
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.Callback, 1).AddHardwareId(
            "PC Remote Controller", "USB\\VID_073A&PID_2230"
        )
        self.winUsb.Start()
        self.timer = eg.ResettableTimer(self.OnTimeOut)


    def __stop__(self):
        self.timer.Stop()
        self.winUsb.Stop()


    def Callback(self, data):
        buf = self.buf
        buf.append(data[0])
        first = buf[0]
        if first not in LENGTHES:
            del buf[:]
            return
        if len(buf) < LENGTHES[first]:
            return
        try:
            if first == 2:
                mButton, x, y = buf[1:4]
                if mButton != self.lastMouseState:
                    self.lastMouseState = mButton
                    if mButton == 32:
                        self.TriggerEnduringEvent("LeftMouseButton")
                    elif mButton == 64:
                        self.TriggerEnduringEvent("RightMouseButton")
                    else:
                        self.EndLastEvent()
                if x != 0 or y != 0:
                    if x > 127:
                        x -= 256
                    if y > 127:
                        y -= 256
                    degree = (round((atan2(x, -y) / pi) * 180)) % 360
                    if self.lastDirection != degree:
                        self.TriggerEnduringEvent(
                            "MouseDirection.%03d" % degree
                        )
                        self.lastDirection = degree
                    self.timer.Reset(75)
                return

            if self.bytesToIgnore:
                self.bytesToIgnore -= len(buf)
                if self.bytesToIgnore < 0:
                    self.bytesToIgnore = 0
                return

            if self.stopCodeLength:
                self.stopCodeLength -= len(buf)
                if self.stopCodeLength <= 0:
                    self.EndLastEvent()
                    self.stopCodeLength = 0
                return

            if buf == [1, 0, 0]:
                self.TriggerEvent("NumLock")
                return

            if buf == [1, 3, 0]:
                return

            data = CODES.get(tuple(buf), None)
            if data:
                self.bytesToIgnore, eventname, self.stopCodeLength = data
                self.TriggerEnduringEvent(eventname)
            else:
                self.EndLastEvent()
                self.bytesToIgnore = 0
                self.stopCodeLength = 0
                self.lastDirection = None
                self.PrintError("Unknown code %r received." % buf)
        finally:
            del buf[:]


    def OnTimeOut(self):
        self.EndLastEvent()
        self.lastDirection = None


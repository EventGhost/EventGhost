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
Plugin for the CyberLink Universal Remote Control
"""

import eg

eg.RegisterPlugin(
    name = "CyberLink Universal Remote Control",
    author = "Bitmonster",
    version = "1.0.0",
    kind = "remote",
    guid = "{097D33BE-FD65-43D2-852B-5DA8A3FBC489}",
    description = __doc__,
)

KEY_CODES = {
    (0, 0, 30, 0, 0, 0, 0, 0): "Num1",
    (0, 0, 31, 0, 0, 0, 0, 0): "Num2",
    (0, 0, 32, 0, 0, 0, 0, 0): "Num3",
    (0, 0, 33, 0, 0, 0, 0, 0): "Num4",
    (0, 0, 34, 0, 0, 0, 0, 0): "Num5",
    (0, 0, 35, 0, 0, 0, 0, 0): "Num6",
    (0, 0, 36, 0, 0, 0, 0, 0): "Num7",
    (0, 0, 37, 0, 0, 0, 0, 0): "Num8",
    (0, 0, 38, 0, 0, 0, 0, 0): "Num9",
    (0, 0, 39, 0, 0, 0, 0, 0): "Num0",
    (0, 0, 76, 0, 0, 0, 0, 0): "Clear",
    (0, 0, 40, 0, 0, 0, 0, 0): "Ok",
    (0, 0, 79, 0, 0, 0, 0, 0): "Right",
    (0, 0, 80, 0, 0, 0, 0, 0): "Left",
    (0, 0, 81, 0, 0, 0, 0, 0): "Down",
    (0, 0, 82, 0, 0, 0, 0, 0): "Up",
    (2, 2, 0, 0): "Power",
    (4, 1, 0, 0): "Home",
    (4, 128, 0, 0): "Red",
    (4, 8, 0, 0): "Green",
    (4, 16, 0, 0): "Yellow",
    (4, 32, 0, 0): "Blue",
    (4, 2, 0, 0): "TV",
    (3, 128, 0, 0): "Record",
    (3, 4, 0, 0): "Radio",
    (4, 0, 16, 0): "SAP",
    (4, 0, 32, 0): "Teletext",
    (4, 0, 64, 0): "LastChannel",
    (4, 0, 8, 0): "Subtitle",
    (4, 0, 2, 0): "Language",
    (4, 0, 1, 0): "Angel",
    (3, 0, 4, 0): "Back",
    (3, 0, 0, 2): "Info",
    (4, 0, 4, 2): "DvdMenu",
    (3, 0, 1, 0): "ChannelUp",
    (3, 0, 2, 0): "ChannelDown",
    (3, 16, 0, 0): "Mute",
    (3, 32, 0, 0): "VolumeUp",
    (3, 64, 0, 0): "VolumeDown",
    (3, 0, 0, 64): "Play",
    (3, 0, 0, 4): "Rewind",
    (3, 0, 0, 128): "Pause",
    (3, 0, 0, 8): "Forward",
    (3, 2, 0, 0): "PreviousTrack",
    (3, 0, 16, 0): "Stop",
    (3, 1, 0, 0): "NextTrack",
}


class CyberlinkUniversalRemote(eg.PluginBase):

    def __start__(self):
        self.buffer = []
        self.expectedLength = 0
        self.usb = eg.WinUsb(self)
        self.usb.AddDevice(
            "CyberLink Universal Remote Control (Keypad)",
            "USB\\VID_0766&PID_0204&MI_00",
            "{EADE53A2-CFB5-4A5D-89B2-316FDBE428A2}",
            self.Callback,
            8
        )
        self.usb.AddDevice(
            "CyberLink Universal Remote Control (Buttons)",
            "USB\\VID_0766&PID_0204&MI_01",
            "{5D4C1DAB-E80F-4076-852D-BAB7C175A035}",
            self.Callback,
            4
        )
        self.usb.Open()


    def __stop__(self):
        self.usb.Close()


    def Callback(self, data):
        if data in KEY_CODES:
            self.TriggerEnduringEvent(KEY_CODES[data])
        else:
            self.EndLastEvent()


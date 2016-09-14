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
Plugin for the Logitech UltraX Media Remote.

.. image:: picture.gif
   :align: center
"""


import eg

eg.RegisterPlugin(
    name = "Logitech UltraX Media Remote",
    author = "Bitmonster",
    version = "1.0.0",
    kind = "remote",
    guid = "{5416ED98-E9CF-4658-9135-AB67EF4335DC}",
    description = __doc__,
    hardwareId = "USB\\VID_046D&PID_C101",
)


KEYPAD_CODE = {
    0x1E: "Num1",
    0x1F: "Num2",
    0x20: "Num3",
    0x21: "Num4",
    0x22: "Num5",
    0x23: "Num6",
    0x24: "Num7",
    0x25: "Num8",
    0x26: "Num9",
    0x27: "Num0",
    0x28: "Ok",
    0x4C: "Clear",
    0x4F: "Right",
    0x50: "Left",
    0x51: "Down",
    0x52: "Up",
    0x58: "Enter",
}

BUTTON_CODES3 = {
    0: "NextTrack",
    1: "PreviousTrack",
    2: "Radio",
    3: "Play",
    4: "Mute",
    5: "VolumeUp",
    6: "VolumeDown",
    7: "Record",
    8: "ChannelUp",
    9: "ChannelDown",
    10: "Back",
    11: "Subtitle",
    12: "Stop",
    13: "Teletext",
    14: "LastChannel",
    15: "Repeat",
    16: "Start",
    17: "Info",
    18: "Rewind",
    19: "Forward",
}

BUTTON_CODES4 = {
    0: "Home",
    1: "TV",
    2: "Shuffle",
    3: "Music",
    4: "Pictures",
    5: "Videos",
    6: "VolumeDown",
    7: "DVD",
    8: "Angle",
    9: "Language",
    10: "DVDMenu",
    11: "Subtitle",
    12: "SAP",
    13: "Teletext",
    14: "LastChannel",
    15: "Repeat",
    16: "Start",
    17: "Close",
    18: "Rewind",
    19: "Forward",
}


class UltraX(eg.PluginBase):

    def __start__(self):
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.KeypadCallback, 8, True).AddHardwareId(
            "Logitech UltraX Media Remote (Keypad)",
            "USB\\VID_046D&PID_C101&MI_00",
        )
        self.winUsb.Device(self.ButtonsCallback, 4).AddHardwareId(
            "Logitech UltraX Media Remote (Buttons)",
            "USB\\VID_046D&PID_C101&MI_01",
        )
        self.winUsb.Start()


    def __stop__(self):
        self.winUsb.Stop()


    def KeypadCallback(self, data):
        #print "key", data
        keys = []
        for value in data:
            if value in KEYPAD_CODE:
                keys.append(KEYPAD_CODE[value])
        if keys:
            self.TriggerEnduringEvent("+".join(keys))
        else:
            self.EndLastEvent()


    def ButtonsCallback(self, data):
        #print "button", data
        if data[0] == 3:
            table = BUTTON_CODES3
        else:
            table = BUTTON_CODES4
        value = (data[3] << 16) + (data[2] << 8) + data[1]
        mask = 1
        buttons = []
        for i in range(24):
            if value & mask:
                buttons.append(table[i])
            mask <<= 1
        if buttons:
            self.TriggerEnduringEvent("+".join(buttons))
        else:
            self.EndLastEvent()


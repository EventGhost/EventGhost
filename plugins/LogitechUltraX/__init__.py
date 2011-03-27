# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
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

ur"""<rst>
Plugin for the Logitech UltraX Media Remote.

.. image:: picture.gif
   :align: center

**Notice:** You need a special driver to use the remote with this plugin. 
Please `download it here`__ and install it while the device is connected.

__ http://www.eventghost.net/downloads/USB-Remote-Driver.exe
"""


import eg

eg.RegisterPlugin(
    name = "Logitech UltraX Media Remote",
    author = "Bitmonster",
    version = "1.0.0",
    kind = "remote",
    description = __doc__,
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
        self.usb1 = eg.WinUsbRemote(
            "{F73227F9-6CBD-45F9-83C4-A48B3F9F56A4}",
            self.KeypadCallback,
            8,
            True
        )
        self.usb2 = eg.WinUsbRemote(
            "{4C6BCF9C-8F5B-4CEB-8CEA-4713E31B125F}",
            self.ButtonsCallback,
            4
        )
        if not self.usb1.IsOk() or not self.usb2.IsOk():
            raise self.Exceptions.DeviceNotFound


    def __stop__(self):
        self.usb1.Close()
        self.usb2.Close()
        

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


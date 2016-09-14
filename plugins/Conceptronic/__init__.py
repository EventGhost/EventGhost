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
Plugin for the `Conceptronic Remote Control for Windows\u00ae Media Center`__.

|

.. image:: picture.jpg
   :align: center

__ http://www.conceptronic.net/site/desktopdefault.aspx
   ?tabindex=1&tabid=242&cid=40&gid=4050&pid=CLLRCMCE
"""

import eg

eg.RegisterPlugin(
    name = "Conceptronic CLLRCMCE",
    author = "Bitmonster",
    version = "1.0.0",
    kind = "remote",
    guid = "{F809DB61-4F57-483B-A867-C5081571755F}",
    description = __doc__,
    hardwareId = "USB\\VID_1784&PID_0004",
)


BUTTON_CODES = {
    (2,): 'Power',
    (0, 13): 'Start',
    (0, 36): 'DVDMenu',
    (0, 37): 'TV',
    (0, 39): 'AspectRatio',
    (0, 71): 'Music',
    (0, 72): 'RecordedTV',
    (0, 73): 'Photo',
    (0, 74): 'Video',
    (0, 80): 'Radio',
    (0, 90): 'Teletext',
    (0, 91): 'Red',
    (0, 92): 'Green',
    (0, 93): 'Yellow',
    (0, 94): 'Blue',
    (0, 0, 0, 1): 'Info',
    (0, 0, 0, 2): 'TVGuide',
    (0, 0, 0, 4): 'Play',
    (0, 0, 0, 8): 'Pause',
    (0, 0, 4, 0): 'Rewind',
    (0, 0, 8, 0): 'Forward',
    (0, 0, 16, 0): 'Record',
    (0, 0, 32, 0): 'ChannelUp',
    (0, 0, 64, 0): 'ChannelDown',
    (0, 4, 0, 0): 'Back',
    (1, 0, 0, 0): 'NextTrack',
    (2, 0, 0, 0): 'PreviousTrack',
    (4, 0, 0, 0): 'Stop',
    (16, 0, 0, 0): 'Mute',
    (32, 0, 0, 0): 'VolumeUp',
    (64, 0, 0, 0): 'VolumeDown',
}

KEYPAD_CODES = {
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
    (0, 0, 40, 0, 0, 0, 0, 0): "Ok",
    (0, 0, 41, 0, 0, 0, 0, 0): "Clear",
    (0, 0, 79, 0, 0, 0, 0, 0): "Right",
    (0, 0, 80, 0, 0, 0, 0, 0): "Left",
    (0, 0, 81, 0, 0, 0, 0, 0): "Down",
    (0, 0, 82, 0, 0, 0, 0, 0): "Up",
    (2, 0, 37, 0, 0, 0, 0, 0): "Star",
    (2, 0, 32, 0, 0, 0, 0, 0): "Dash",
}


class Conceptronic(eg.PluginBase):

    def __start__(self):
        self.buffer = []
        self.expectedLength = 0
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.KeypadCallback, 8, True).AddHardwareId(
            "Conceptronic CLLRCMCE (Keypad)", "USB\\VID_1784&PID_0004&MI_00"
        )
        self.winUsb.Device(self.ButtonsCallback, 1).AddHardwareId(
            "Conceptronic CLLRCMCE (Buttons)", "USB\\VID_1784&PID_0004&MI_01"
        )
        self.winUsb.Start()


    def __stop__(self):
        self.winUsb.Stop()


    def KeypadCallback(self, data):
        if data == (0, 0, 0, 0, 0, 0, 0, 0):
            self.EndLastEvent()
        else:
            self.TriggerEnduringEvent(KEYPAD_CODES[data])


    def ButtonsCallback(self, data):
        value = data[0]
        numReceived = len(self.buffer)
        if self.expectedLength == 0:
            if value not in (2, 3, 4):
                return
            self.expectedLength = {2: 1, 3: 4, 4: 2}[value]
        elif numReceived < self.expectedLength - 1:
            self.buffer.append(value)
        elif numReceived == self.expectedLength - 1:
            self.buffer.append(value)
            value = tuple(self.buffer)
            if value in BUTTON_CODES:
                self.TriggerEnduringEvent(BUTTON_CODES[value])
            else:
                self.EndLastEvent()
            self.buffer = []
            self.expectedLength = 0
        else:
            self.PrintError("Unknown data received")
            self.buffer = []
            self.expectedLength = 0
            self.EndLastEvent()


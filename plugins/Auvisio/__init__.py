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
Plugin for the Auvisio PC-Remote.
"""

import eg

eg.RegisterPlugin(
    name = "auvisio VRC-1100 Ro",
    author = "Bitmonster",
    version = "1.0.0",
    kind = "remote",
    guid = "{96F3D335-C941-4F4E-A196-AAD190E3E255}",
    description = __doc__,
    hardwareId = "USB\VID_05A4&PID_9881",
)

from math import atan2, pi

BUTTONS1 = {
    (0, 0, 75, 0, 0, 0, 0, 0): "ChannelUp",
    (0, 0, 78, 0, 0, 0, 0, 0): "ChannelDown",
    (0, 0, 79, 0, 0, 0, 0, 0): "Right",
    (0, 0, 80, 0, 0, 0, 0, 0): "Left",
    (0, 0, 81, 0, 0, 0, 0, 0): "Down",
    (0, 0, 82, 0, 0, 0, 0, 0): "Up",
    (0, 0, 89, 0, 0, 0, 0, 0): "Num1",
    (0, 0, 90, 0, 0, 0, 0, 0): "Num2",
    (0, 0, 91, 0, 0, 0, 0, 0): "Num3",
    (0, 0, 92, 0, 0, 0, 0, 0): "Num4",
    (0, 0, 93, 0, 0, 0, 0, 0): "Num5",
    (0, 0, 94, 0, 0, 0, 0, 0): "Num6",
    (0, 0, 95, 0, 0, 0, 0, 0): "Num7",
    (0, 0, 96, 0, 0, 0, 0, 0): "Num8",
    (0, 0, 97, 0, 0, 0, 0, 0): "Num9",
    (0, 0, 98, 0, 0, 0, 0, 0): "Num0",
    (0, 0, 85, 0, 0, 0, 0, 0): "Star",
    (4, 0, 93, 0, 0, 0, 0, 0): "Dash",
    (4, 0, 61, 0, 0, 0, 0, 0): "Close",
    (0, 0, 41, 0, 0, 0, 0, 0): "Clear",
    (0, 0, 40, 0, 0, 0, 0, 0): "Ok",
    (0, 0, 42, 0, 0, 0, 0, 0): "Back",
    (1, 0, 10, 0, 0, 0, 0, 0): "TvGuide",
    (1, 0, 18, 0, 0, 0, 0, 0): "TvRecordings",
    (1, 0, 21, 0, 0, 0, 0, 0): "Record",
    (1, 0, 23, 0, 0, 0, 0, 0): "LiveTv",
    (3, 0, 5, 0, 0, 0, 0, 0): "FastRewind",
    (3, 0, 9, 0, 0, 0, 0, 0): "FastForward",
    (3, 0, 16, 0, 0, 0, 0, 0): "Dvd",
    (12, 0, 40, 0, 0, 0, 0, 0): "Start",
    (3, 0, 23, 0, 0, 0, 0, 0): "Yellow",
    (1, 0, 16, 0, 0, 0, 0, 0): "Blue",
    (1, 0, 12, 0, 0, 0, 0, 0): "Green",
    (1, 0, 8, 0, 0, 0, 0, 0): "Red",
}

BUTTONS2 = {
    (2, 0, 16, 0, 85): "VolumeDown",
    (2, 16, 0, 0, 85): "VolumeUp",
    (2, 0, 1, 0, 85): "Mute",
    (2, 0, 0, 2, 85): "Play",
    (2, 0, 2, 0, 85): "NextTrack",
    (2, 128, 0, 0, 85): "PreviousTrack",
    (2, 0, 0, 1, 85): "Stop",
    (3, 2, 85, 85, 85): "Power",
    (2, 2, 0, 0, 85): "Internet",
    (1, 2, 0, 0, 0): "RightClickInfo",
    (1, 1, 0, 0, 0): "LeftClick",
    (1, 0, 0, 0, 0): "MouseButtonUp",
}


class Auvisio(eg.PluginBase):

    def __start__(self):
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.Callback1, 8).AddHardwareId(
            "Auvisio PC-Remote (Buttons)", "USB\VID_05A4&PID_9881&MI_00"
        )
        self.winUsb.Device(self.Callback2, 5).AddHardwareId(
            "Auvisio PC-Remote (Mousepad)", "USB\VID_05A4&PID_9881&MI_01"
        )
        self.winUsb.Start()


    def __stop__(self):
        self.winUsb.Stop()


    def Callback1(self, data):
        if data in BUTTONS1:
            self.TriggerEnduringEvent(BUTTONS1[data])
        else:
            self.EndLastEvent()


    def Callback2(self, data):
        if data[0] == 1:
            # mouse codes always start with 1
            mouseState, x, y = data[1:4]
            if x != 0 or y != 0:
                if x > 127:
                    x -= 256
                if y > 127:
                    y -= 256
                degree = (round((atan2(x, -y) / pi) * 180)) % 360
                self.TriggerEnduringEvent('MouseDir', degree)
        if data in BUTTONS2:
            if data[0] == 1 and data[1] == 0:
                self.TriggerEvent(BUTTONS2[data])
            else:
                self.TriggerEnduringEvent(BUTTONS2[data])
        else:
            self.EndLastEvent()

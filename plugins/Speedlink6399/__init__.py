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
Plugin for the Speed-Link Media Remote Control (SL-6399)

"""

import eg

eg.RegisterPlugin(
    name = "Speed-Link SL-6399 Media Remote",
    author = "Bitmonster",
    version = "1.0.0",
    kind = "remote",
    guid = "{ED814A18-5379-46B5-9A3B-65449C21871E}",
    description = __doc__,
    hardwareId = "USB\\VID_1241&PID_E000",
)

CODES1 = {
    (0, 0, 40): "Ok",
    (0, 0, 75): "ChannelUp",
    (0, 0, 78): "ChannelDown",
    (0, 0, 79): "Right",
    (0, 0, 80): "Left",
    (0, 0, 81): "Down",
    (0, 0, 82): "Up",
    (0, 0, 85): "Star",
    (0, 0, 30): "Num1",
    (0, 0, 31): "Num2",
    (0, 0, 32): "Num3",
    (0, 0, 33): "Num4",
    (0, 0, 34): "Num5",
    (0, 0, 35): "Num6",
    (0, 0, 36): "Num7",
    (0, 0, 37): "Num8",
    (0, 0, 38): "Num9",
    (0, 0, 39): "Num0",
    (0, 0, 42): "Back",
    (0, 0, 58): "Help",
    (1, 0, 4): "Radio",
    (1, 0, 17): "Msn",
    (1, 0, 24): "Title",
    (2, 0, 32): "Dash",
    (3, 0, 4): "Audio",
    (3, 0, 16): "DVD",
    (3, 0, 29): "Aspect",
    (4, 0, 40): "Desktop",
    (4, 0, 61): "PC",
}

CODES2 =  {
    (4, 2, 0): "TV",
    (3, 180, 0): "Rewind",
    (3, 176, 0): "Play",
    (3, 179, 0): "Forward",
    (3, 183, 0): "Stop",
    (3, 182, 0): "Replay",
    (3, 177, 0): "Pause",
    (3, 181, 0): "Skip",
    (3, 178, 0): "Record",
    (3, 9, 2): "More",
    (4, 16, 0): "Videos",
    (4, 4, 0): "Music",
    (4, 8, 0): "Pictures",
    (4, 32, 0): "MyTV",
    (3, 233, 0): "VolumeUp",
    (3, 234, 0): "VolumeDown",
    (4, 1, 0): "Start",
    (3, 226, 0): "Mute",
    (3, 141, 0): "Guide",
    (4, 64, 0): "RTV",
}


class Speedlink(eg.PluginBase):

    def __start__(self):
        self.info.eventPrefix = "SpeedLink"
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.Callback1, 8).AddHardwareId(
            "SPEEDLINK SL-6399 Media Remote", "USB\\VID_1241&PID_E000&MI_00"
        )
        self.winUsb.Device(self.Callback2, 4).AddHardwareId(
            "SPEEDLINK SL-6399 Media Remote", "USB\\VID_1241&PID_E000&MI_01"
        )
        self.winUsb.Start()


    def __stop__(self):
        self.winUsb.Stop()


    def Callback1(self, data):
        code = data[:3]
        if code == (0, 0, 0):
            self.EndLastEvent()
        elif code in CODES1:
            self.TriggerEnduringEvent(CODES1[code])
        else:
            print "#1", data


    def Callback2(self, data):
        if data[1:] == (0, 0, 0):
            self.EndLastEvent()
            return
        code = data[:3]
        if code in CODES2:
            self.TriggerEnduringEvent(CODES2[code])
        else:
            print "#2", data


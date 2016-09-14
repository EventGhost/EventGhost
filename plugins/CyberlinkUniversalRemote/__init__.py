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
Plugin for the CyberLink Universal Remote Control
"""

import eg

eg.RegisterPlugin(
    name = "CyberLink Universal Remote Control",
    author = "Bitmonster",
    version = "1.0.1",
    kind = "remote",
    guid = "{097D33BE-FD65-43D2-852B-5DA8A3FBC489}",
    description = __doc__,
    hardwareId = "USB\\VID_0766&PID_0204",
)

KEY_CODES_1 = {
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
}

KEY_CODES_2 = {
    (3, 0, 0, 2):   "Info",
    (3, 0, 0, 4):   "Rewind",
    (3, 0, 0, 8):   "Forward",
    (3, 0, 0, 64):  "Play",
    (3, 0, 0, 128): "Pause",
}

KEY_CODES_3 = {
    (3, 0, 1):   "ChannelUp",
    (3, 0, 2):   "ChannelDown",
    (3, 0, 4):   "Back",
    (3, 0, 16):  "Stop",
    (3, 1, 0):   "NextTrack",
    (3, 2, 0):   "PreviousTrack",
    (3, 4, 0):   "Radio",
    (3, 16, 0):  "Mute",
    (3, 32, 0):  "VolumeUp",
    (3, 64, 0):  "VolumeDown",
    (3, 128, 0): "Record",
    (4, 0, 1):   "Angel",
    (4, 0, 2):   "Language",
    (4, 0, 4):   "DvdMenu",
    (4, 0, 8):   "Subtitle",
    (4, 0, 16):  "SAP",
    (4, 0, 32):  "Teletext",
    (4, 0, 64):  "LastChannel",
    (4, 1, 0):   "Home",
    (4, 2, 0):   "TV",
    (4, 8, 0):   "Green",
    (4, 16, 0):  "Yellow",
    (4, 32, 0):  "Blue",
    (4, 128, 0): "Red",
}

KEY_CODES_4 = {
    (2, 2):   "Power",
}

class CyberlinkUniversalRemote(eg.PluginBase):

    def __start__(self):
        self.buffer = []
        self.expectedLength = 0
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.Callback, 8).AddHardwareId(
            "CyberLink Universal Remote Control (Keypad)",
            "USB\\VID_0766&PID_0204&MI_00"
        )
        self.winUsb.Device(self.Callback, 4).AddHardwareId(
            "CyberLink Universal Remote Control (Buttons)",
            "USB\\VID_0766&PID_0204&MI_01"
        )
        self.winUsb.Start()
        self.last_data = []


    def __stop__(self):
        self.winUsb.Stop()


    def Callback(self, data):
        if self.last_data != data:
#            print data
            if data in KEY_CODES_1:
                self.TriggerEnduringEvent(KEY_CODES_1[data])
                self.last_data = data
            elif data in KEY_CODES_2:
                self.TriggerEnduringEvent(KEY_CODES_2[data])
                self.last_data = data
            elif data[:3] in KEY_CODES_3:
                self.TriggerEnduringEvent(KEY_CODES_3[data[:3]])
                self.last_data = data
            elif data[:2] in KEY_CODES_4:
                self.TriggerEnduringEvent(KEY_CODES_4[data[:2]])
                self.last_data = data
            elif len(data) == len(self.last_data):
                self.EndLastEvent()
                self.last_data = []
#                print "EndLastEvent"


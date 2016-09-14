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

r"""<rst>
Plugin for the `ATI Remote Wonder II`__ remote.

|

.. image:: picture.jpg
   :align: center

__ http://ati.amd.com/products/remotewonder2/index.html
"""


import eg

eg.RegisterPlugin(
    name="ATI Remote Wonder II (WinUSB)",
    description=__doc__,
    url="http://www.eventghost.org/forum/viewtopic.php?t=915",
    author="Bitmonster",
    version="1.0.2",
    kind="remote",
    hardwareId = "USB\\VID_0471&PID_0602",
    guid="{74DBFE39-FEF6-41E5-A047-96454512B58D}",
)

from math import atan2, pi
from eg.WinApi.Dynamic import mouse_event


CODES = {
    0: "Num0",
    1: "Num1",
    2: "Num2",
    3: "Num3",
    4: "Num4",
    5: "Num5",
    6: "Num6",
    7: "Num7",
    8: "Num8",
    9: "Num9",
    12: "Power",
    13: "Mute",
    16: "VolumeUp",
    17: "VolumeDown",
    32: "ChannelUp",
    33: "ChannelDown",
    40: "FastForward",
    41: "FastRewind",
    44: "Play",
    48: "Pause",
    49: "Stop",
    55: "Record",
    56: "DVD",
    57: "TV",
    84: "Setup",
    88: "Up",
    89: "Down",
    90: "Left",
    91: "Right",
    92: "Ok",
    120: "A",
    121: "B",
    122: "C",
    123: "D",
    124: "E",
    125: "F",
    130: "Checkmark",
    142: "ATI",
    150: "Stopwatch",
    190: "Help",
    208: "Hand",
    213: "Resize",
    249: "Info",
}

DEVICES = {
    0: "AUX1",
    1: "AUX2",
    2: "AUX3",
    3: "AUX4",
    4: "PC",
}


class AtiRemoteWonder2(eg.PluginBase):

    def __start__(self):
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.Callback1, 3).AddHardwareId(
            "ATI Remote Wonder II (Mouse)", "USB\\VID_0471&PID_0602&MI_00"
        )
        self.winUsb.Device(self.Callback2, 3).AddHardwareId(
            "ATI Remote Wonder II (Buttons)", "USB\\VID_0471&PID_0602&MI_01"
        )
        self.winUsb.Start()
        self.lastDirection = None
        self.currentDevice = None
        self.timer = eg.ResettableTimer(self.OnTimeOut)
        self.receiveQueue = eg.plugins.Mouse.plugin.thread.receiveQueue


    def __stop__(self):
        self.winUsb.Stop()
        self.timer.Stop()


    def Callback1(self, (device, x, y)):
        if x > 127:
            x -= 256
        if y > 127:
            y -= 256
        degree = (round((atan2(x, -y) / pi) * 180)) % 360
        if degree != self.lastDirection:
            self.receiveQueue.put(degree)
            self.lastDirection = degree
        self.timer.Reset(100)


    def Callback2(self, (device, event, code)):
        if device != self.currentDevice:
            self.currentDevice = device
            self.TriggerEvent(DEVICES[device])
        if event == 1:
            if code == 169:
                mouse_event(0x0002, 0, 0, 0, 0)
            elif code == 170:
                mouse_event(0x0008, 0, 0, 0, 0)
            elif code != 63:
                self.TriggerEnduringEvent(CODES.get(code, "%i" % code))
        elif event == 0:
            if code == 169:
                mouse_event(0x0004, 0, 0, 0, 0)
            elif code == 170:
                mouse_event(0x0010, 0, 0, 0, 0)
            else:
                self.EndLastEvent()


    @eg.LogIt
    def OnTimeOut(self):
        self.receiveQueue.put(-2)
        self.lastDirection = None

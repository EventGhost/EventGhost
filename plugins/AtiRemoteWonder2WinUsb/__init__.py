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
Plugin for the `ATI Remote Wonder II`__ remote.

.. image:: picture.jpg
   :align: center

**Notice:** The ATI Remote Wonder software must also run to receive events
from this remote and the special "EventGhost.dll" must be imported and enabled
inside the ATI Remote Wonder Software.

| You will find this DLL inside:
| {ProgramFiles}\\EventGhost\\Plugins\\AtiRemoteWonder2\\

__ http://ati.amd.com/products/remotewonder2/index.html
"""


import eg

eg.RegisterPlugin(
    name="ATI Remote Wonder II (WinUSB)",
    description=__doc__,
    url="http://www.eventghost.org/forum/viewtopic.php?t=915",
    author="Bitmonster",
    version="1.0.0",
    kind="remote",
    guid="{74DBFE39-FEF6-41E5-A047-96454512B58D}",
)


KEY_MAP = (
    "Hand",
    "LButtonDown", "RButtonDown", "LButtonDoubleClick", "RButtonDoubleClick",
    "Mouse090", "Mouse000", "Mouse270", "Mouse180",
    "Mouse045", "Mouse135", "Mouse315", "Mouse225",
    "Menu", "Setup",
    "FastForward", "Rewind", 
    "StopWatch",
    "Resize", "WebLaunch", "Help", "Info", "Power", "Book",
    "Ati", "TV", "TV2", "FM", "DVD", "Guide",
)

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
    44: "Play",
    48: "Pause",
    49: "Stop",
    55: "Record",
    56: "DVD",
    57: "TV",
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
    142: "Ati",
    150: "StopWatch",
}


class AtiRemoteWonder2(eg.PluginBase):

    def __start__(self):
        self.usb = eg.WinUsb(self)
        self.usb.AddDevice(
            "ATI Remote Wonder II (Mouse)",
            "USB\VID_0471&PID_0602&MI_00",
            "{626E95E1-40B8-4BCD-A9C2-C28D52BB1283}",
            self.Callback1,
            3
        )
        self.usb.AddDevice(
            "ATI Remote Wonder II (Buttons)",
            "USB\VID_0471&PID_0602&MI_01",
            "{8D725CF7-AA01-420F-B797-4CD77EC63644}",
            self.Callback2,
            3
        )
        self.usb.Open()


    def __stop__(self):
        self.usb.Close()


    def Callback1(self, data):
        print "#1", data


    def Callback2(self, (device, event, code)):
        print "#2", (device, event, code)
        if event == 1:
            if code == 63:
                if device == 4:
                    self.TriggerEnduringEvent("PC")
                else:
                    self.TriggerEnduringEvent("AUX%i" % (device + 1))
            else:
                self.TriggerEnduringEvent(CODES.get(code, "%i" % code))
        elif event == 0:
            self.EndLastEvent()


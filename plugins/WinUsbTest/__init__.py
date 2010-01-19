# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2010 Lars-Peter Voss <bitmonster@eventghost.org>
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
Plugin for the Auvisio PC-Remote.
"""

import eg

eg.RegisterPlugin(
    name = "WinUSB Test",
    author = "Bitmonster",
    version = "1.0.0",
    kind = "remote",
    guid = "{68EA5E13-712D-47C7-AB95-D4B8707D8D33}",
    description = __doc__,
)

from math import atan2, pi

class WinUsbTest(eg.PluginBase):

    def __start__(self):
        self.usb = eg.WinUsb(self)
        self.usb.AddDevice(
            "WinUSB Test Device",
            "USB\\VID_0609&PID_031D",
            "{F7068BA0-977A-45D6-B488-AF725A604CDC}",
            self.Callback1,
            1
        )
        self.usb.Open()


    def __stop__(self):
        self.usb.Close()


    def Callback1(self, data):
        print data


    def Callback2(self, data):
        print data


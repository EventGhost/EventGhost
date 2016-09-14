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
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.Callback1, 1).AddHardwareId(
            "WinUsb Test Device", "USB\\VID_073A&PID_2230"
        )
        self.winUsb.Start()


    def __stop__(self):
        self.winUsb.Stop()


    def Callback1(self, data):
        print data


    def Callback2(self, data):
        print data


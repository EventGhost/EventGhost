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
Plugin for the Terratec USB Remote
"""


import eg

eg.RegisterPlugin(
    name="Terratec USB",
    description=__doc__,
    author="Bitmonster",
    version="1.0.0",
    kind="remote",
    guid="{230378AB-00FC-43E4-A0E5-B60A2AE15493}",
    usbIds = ["USB\\VID_0419&PID_0001"],
)



class TerratecUsb(eg.PluginBase):

    def __start__(self):
        self.usb = eg.WinUsb(self)
        self.usb.AddDevice(
            "Terratec USB Receiver",
            "USB\\VID_0419&PID_0001",
            "{AB561634-B296-4022-8C5A-107CF2BC2A2E}",
            self.Callback1,
            1
        )
        self.usb.Open()


    def __stop__(self):
        self.usb.Close()


    def Callback1(self, data):
        print "#1", data



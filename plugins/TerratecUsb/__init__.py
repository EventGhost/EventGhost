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
Plugin for the Terratec USB Remote
"""

import eg

eg.RegisterPlugin(
    name="Terratec USB Receiver",
    description=__doc__,
    author="Bitmonster",
    version="1.0.0",
    kind="remote",
    guid="{230378AB-00FC-43E4-A0E5-B60A2AE15493}",
    hardwareId = "USB\\VID_0419&PID_0001",
)

REMOTE_BUTTONS = {
    (4, 1, 0, 0, 0, 0, 0, 0): "Home",
    (3, 130, 0, 0, 0, 0, 0, 0): "Power",
    (4, 2, 0, 0, 0, 0, 0, 0): "DvdMenu",
    (4, 32, 0, 0, 0, 0, 0, 0): "Subtitles",
    (4, 0, 2, 0, 0, 0, 0, 0): "Teletext",
    (4, 0, 32, 0, 0, 0, 0, 0): "Delete",
    (4, 4, 0, 0, 0, 0, 0, 0): "Num1",
    (4, 8, 0, 0, 0, 0, 0, 0): "Num2",
    (4, 16, 0, 0, 0, 0, 0, 0): "Num3",
    (4, 64, 0, 0, 0, 0, 0, 0): "Num4",
    (4, 128, 0, 0, 0, 0, 0, 0): "Num5",
    (4, 0, 1, 0, 0, 0, 0, 0): "Num6",
    (4, 0, 4, 0, 0, 0, 0, 0): "Num7",
    (4, 0, 8, 0, 0, 0, 0, 0): "Num8",
    (4, 0, 16, 0, 0, 0, 0, 0): "Num9",
    (4, 0, 128, 0, 0, 0, 0, 0): "Num0",
    (4, 0, 64, 0, 0, 0, 0, 0): "AV",
    (4, 0, 0, 1, 0, 0, 0, 0): "LastChannel",
    (4, 0, 0, 2, 0, 0, 0, 0): "TV",
    (4, 0, 0, 4, 0, 0, 0, 0): "DVD",
    (4, 0, 0, 8, 0, 0, 0, 0): "Video",
    (4, 0, 0, 16, 0, 0, 0, 0): "Music",
    (4, 0, 0, 32, 0, 0, 0, 0): "Picture",
    (4, 0, 0, 0, 1, 0, 0, 0): "Ok",
    (4, 0, 0, 64, 0, 0, 0, 0): "Up",
    (4, 0, 0, 0, 4, 0, 0, 0): "Down",
    (4, 0, 0, 128, 0, 0, 0, 0): "Left",
    (4, 0, 0, 0, 2, 0, 0, 0): "Right",
    (4, 0, 0, 0, 8, 0, 0, 0): "EPG",
    (4, 0, 0, 0, 16, 0, 0, 0): "Info",
    (4, 0, 0, 0, 32, 0, 0, 0): "Back",
    (4, 0, 0, 0, 64, 0, 0, 0): "VolumeUp",
    (4, 0, 0, 0, 0, 2, 0, 0): "VolumeDown",
    (4, 0, 0, 0, 0, 4, 0, 0): "Mute",
    (4, 0, 0, 0, 128, 0, 0, 0): "Play",
    (4, 0, 0, 0, 0, 1, 0, 0): "ChannelUp",
    (4, 0, 0, 0, 0, 8, 0, 0): "ChannelDown",
    (4, 0, 0, 0, 0, 16, 0, 0): "Red",
    (4, 0, 0, 0, 0, 32, 0, 0): "Green",
    (4, 0, 0, 0, 0, 64, 0, 0): "Yellow",
    (4, 0, 0, 0, 0, 128, 0, 0): "Blue",
    (4, 0, 0, 0, 0, 0, 1, 0): "Record",
    (4, 0, 0, 0, 0, 0, 2, 0): "Stop",
    (4, 0, 0, 0, 0, 0, 4, 0): "Pause",
    (4, 0, 0, 0, 0, 0, 8, 0): "PreviousTrack",
    (4, 0, 0, 0, 0, 0, 16, 0): "Rewind",
    (4, 0, 0, 0, 0, 0, 32, 0): "FastForward",
    (4, 0, 0, 0, 0, 0, 64, 0): "NextTrack",
}


class TerratecUsb(eg.PluginBase):

    def __start__(self):
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.Callback, 8).AddHardwareId(
            "Terratec USB Receiver", "USB\\VID_0419&PID_0001"
        )
        self.winUsb.Start()


    def __stop__(self):
        self.winUsb.Stop()


    def Callback(self, data):
        #print "#", data
        button = REMOTE_BUTTONS.get(data, None)
        if button:
            self.TriggerEnduringEvent(button)
        else:
            self.EndLastEvent()


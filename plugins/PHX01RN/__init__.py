# -*- coding: utf-8 -*-
#
# PHX01RN plugin v3.0
#
# Marius van der Spek
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

import eg

eg.RegisterPlugin(
    name="PHX01RN",
    description= '''<div align="center"><img src="PHX01RN.png"/></div>''',
    author="WharfRat",
    version="3.0.1",
    kind="remote",
    url="http://www.eventghost.org/forum/viewtopic.php?f=9&t=5927",
    guid="{0B5511F9-6E8D-447D-9BD7-340E2C3548DD}",
    hardwareId = "USB\\VID_0755&PID_2626",
)

# 8 byte button press codes
BUTTON_PRESS_1 = {
    (4, 0, 61, 0, 0, 0, 0, 0): "Close",
    (1, 0, 8, 0, 0, 0, 0, 0): "MyVideo",
    (3, 0, 23, 0, 0, 0, 0, 0): "MyTV",
    (1, 0, 4, 0, 0, 0, 0, 0): "FmRadio",
    (1, 0, 12, 0, 0, 0, 0, 0): "MyPicture",
    (1, 0, 16, 0, 0, 0, 0, 0): "MyMusic",
    (3, 0, 16, 0, 0, 0, 0, 0): "DvdMenu",
    (3, 0, 5, 0, 0, 0, 0, 0): "Rew",
    (8, 0, 7, 0, 0, 0, 0, 0): "Desktop",
    (0, 0, 75, 0, 0, 0, 0, 0): "ChUp",
    (12, 0, 40, 0, 0, 0, 0, 0): "MediaCenter",
    (0, 0, 78, 0, 0, 0, 0, 0): "ChDown",
    (0, 0, 82, 0, 0, 0, 0, 0): "Up",
    (0, 0, 80, 0, 0, 0, 0, 0): "Left",
    (0, 0, 40, 0, 0, 0, 0, 0): "Enter",
    (0, 0, 79, 0, 0, 0, 0, 0): "Right",
    (0, 0, 42, 0, 0, 0, 0, 0): "Back",
    (0, 0, 81, 0, 0, 0, 0, 0): "Down",
    (0, 0, 101, 0, 0, 0, 0, 0): "More",
    (1, 0, 21, 0, 0, 0, 0, 0): "Rec",
    (0, 0, 30, 0, 0, 0, 0, 0): "1",
    (0, 0, 31, 0, 0, 0, 0, 0): "2",
    (0, 0, 32, 0, 0, 0, 0, 0): "3",
    (0, 0, 33, 0, 0, 0, 0, 0): "4",
    (0, 0, 34, 0, 0, 0, 0, 0): "5",
    (0, 0, 35, 0, 0, 0, 0, 0): "6",
    (0, 0, 36, 0, 0, 0, 0, 0): "7",
    (0, 0, 37, 0, 0, 0, 0, 0): "8",
    (0, 0, 38, 0, 0, 0, 0, 0): "9",
    (4, 0, 40, 0, 0, 0, 0, 0): "FullScreen",
    (2, 0, 37, 0, 0, 0, 0, 0): "Star",
    (0, 0, 39, 0, 0, 0, 0, 0): "0",
    (2, 0, 32, 0, 0, 0, 0, 0): "Hash",
    (0, 0, 41, 0, 0, 0, 0, 0): "Clear",
}

# 8 byte button release codes (ignored)
BUTTON_RELEASE_1 = {
    (0, 0, 0, 0, 0, 0, 0, 0): "button released",
}

# 6 byte button press codes
BUTTON_PRESS_2 = {
    (3, 129, 0, 0, 0, 0): "Power",
    (2, 183, 0, 0, 0, 0): "Stop",
    (2, 179, 0, 0, 0, 0): "Fwd",
    (2, 182, 0, 0, 0, 0): "Replay",
    (2, 205, 0, 0, 0, 0): "PlayPause",
    (2, 181, 0, 0, 0, 0): "Skip",
    (2, 233, 0, 0, 0, 0): "VolPlus",
    (2, 226, 0, 0, 0, 0): "Mute",
    (2, 234, 0, 0, 0, 0): "VolMinus",
    (2, 35, 2, 0, 0, 0): "WWW",
    (2, 138, 1, 0, 0, 0): "E-mail",
    (2, 36, 2, 0, 0, 0): "Previous",
    (2, 37, 2, 0, 0, 0): "Next",
}

# 6 byte button press codes
BUTTON_PRESS_2A = {
    (1, 1, 0, 0, 0, 0): "Back",   # mouse left click
    (1, 2, 0, 0, 0, 0): "More",   # mouse right click
    (1, 0, 0, 254, 0, 0): "Up",   # mouse up
    (1, 0, 254, 0, 0, 0): "Left", # mouse left
    (1, 0, 2, 0, 0, 0): "Right",  # mouse right
    (1, 0, 0, 2, 0, 0): "Down",   # mouse down
}

# 6 byte button press codes (ignored)
BUTTON_PRESS_2B = {
    (3, 0, 0, 0, 0, 0): "Power",  # sometimes follows (3, 129, 0, 0, 0, 0)
}

# 6 byte button release codes
BUTTON_RELEASE_2 = {
    (1, 0, 0, 0, 0, 0): "button released",
    (2, 0, 0, 0, 0, 0): "button released",
}

class PHX01RN(eg.PluginBase):

    def __start__(self):
        self.winUsb = eg.WinUsb(self)
        # create the 8 byte button handler
        self.winUsb.Device(self.Callback1, 8).AddHardwareId(
            "PHX01RN W-01RN MI_00", "USB\\VID_0755&PID_2626&MI_00"
        )
        # create the 6 byte button handler
        self.winUsb.Device(self.Callback2, 6).AddHardwareId(
            "PHX01RN W-01RN MI_01", "USB\\VID_0755&PID_2626&MI_01"
        )
        self.winUsb.Start()
        self.inCursorMode = 1
        self.buttonNotPressed = 1


    def __stop__(self):
        self.winUsb.Stop()


    def Callback1(self, data):
        # 8 byte buttons
        value = data[:8]
        if value in BUTTON_PRESS_1:
            self.TriggerEnduringEvent("".join(BUTTON_PRESS_1[value]))
            self.buttonNotPressed = 0
        # else: ignore (0, 0, 0, 0, 0, 0, 0, 0) button release


    def Callback2(self, data):
        # 6 byte buttons
        value = data[:6]
        if value in BUTTON_RELEASE_2:
            if self.buttonNotPressed:
                self.TriggerEvent("".join("Toggle"))
            #self.TriggerEvent("".join("button released"))
            self.EndLastEvent()
            self.inCursorMode = 1
            self.buttonNotPressed = 1
        elif value in BUTTON_PRESS_2A:
            if self.inCursorMode:
                self.TriggerEnduringEvent("".join(BUTTON_PRESS_2A[value]))
                self.inCursorMode = 0
            self.buttonNotPressed = 0
        elif value in BUTTON_PRESS_2:
            self.TriggerEnduringEvent("".join(BUTTON_PRESS_2[value]))
            self.inCursorMode = 0
            self.buttonNotPressed = 0
        # else: ignore (3, 0, 0, 0, 0, 0) occassional extra power press

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
Plugin for the PC Remote Controller.

|

.. image:: remote.jpg
   :align: center
"""

import eg

eg.RegisterPlugin(
    name = "PC Remote Controller",
    description = __doc__,
    author = "Bitmonster",
    version = "1.0.0",
    kind = "remote",
    guid = "{401F1F43-58D9-4F99-936A-A9114CE73D7E}",
    hardwareId = "USB\\VID_06B4&PID_1C70",
)

from math import atan2, pi

BUTTONS = {
    # first_code: (number_of_codes_to_ignore, name_of_the_event)
    (1, 0, 30, 0):  (0, 'Num1'),
    (1, 0, 31, 0):  (0, 'Num2'),
    (1, 0, 32, 0):  (0, 'Num3'),
    (1, 0, 33, 0):  (0, 'Num4'),
    (1, 0, 34, 0):  (0, 'Num5'),
    (1, 0, 35, 0):  (0, 'Num6'),
    (1, 0, 36, 0):  (0, 'Num7'),
    (1, 0, 37, 0):  (0, 'Num8'),
    (1, 0, 38, 0):  (0, 'Num9'),
    (1, 0, 39, 0):  (0, 'Num0'),
    (1, 0, 40, 0):  (0, 'Enter'),
    (1, 0, 41, 0):  (0, 'Escape'),
    (1, 0, 42, 0):  (0, 'Backspace'),
    (1, 0, 43, 0):  (0, 'Tabulator'),
    (1, 0, 75, 0):  (0, 'PageUp'),
    (1, 0, 78, 0):  (0, 'PageDown'),
    (1, 0, 79, 0):  (0, 'Right'),
    (1, 0, 80, 0):  (0, 'Left'),
    (1, 0, 81, 0):  (0, 'Down'),
    (1, 0, 82, 0):  (0, 'Up'),
    (1, 1, 18, 0):  (0, 'Open'),
    (1, 4, 43, 0):  (1, 'SwitchWindows'),
    (1, 4, 61, 0):  (1, 'Close'),
    (1, 5, 4, 0):   (5, 'Music'),
    (1, 5, 5, 0):   (5, 'MyMovies'),
    (1, 5, 6, 0):   (5, 'MyPhotos'),
    (1, 5, 7, 0):   (5, 'MyTV'),
    (1, 8, 0, 0):   (1, 'Start'),
    (1, 8, 7, 0):   (1, 'Desktop'),
    (1, 8, 8, 0):   (1, 'MyPC'),
    (3, 35, 2, 0):  (1, 'WWW'),
    (3, 48, 2, 0):  (5, 'FullScreen'),
    (3, 138, 1, 0): (1, 'E-mail'),
    (3, 181, 0, 0): (1, 'NextTrack'),
    (3, 182, 0, 0): (1, 'PreviousTrack'),
    (3, 183, 0, 0): (1, 'Stop'),
    (3, 202, 0, 0): (3, 'Forward'),
    (3, 203, 0, 0): (3, 'Rewind'),
    (3, 205, 0, 0): (1, 'Play'),
    (3, 226, 0, 0): (1, 'Mute'),
    (3, 233, 0, 0): (0, 'VolumeUp'),
    (3, 234, 0, 0): (0, 'VolumeDown'),
    (6, 129, 0, 0): (0, 'Power'),
}


class PcRemoteController(eg.PluginBase):

    def __start__(self):
        self.winUsb = eg.WinUsb(self)
        self.winUsb.Device(self.Callback, 4).AddHardwareId(
            "PC Remote Controller", "USB\\VID_06B4&PID_1C70",
        )
        self.winUsb.Start()
        self.lastDirection = None
        self.timer = eg.ResettableTimer(self.OnTimeOut)
        self.numIgnoreCodes = 0
        self.mouseState = 0


    def __stop__(self):
        self.timer.Stop()
        self.winUsb.Stop()


    def Callback(self, code):
        #print code
        if code[0] == 2:
            # mouse codes always start with 2
            mouseState, x, y = code[1:4]
            if mouseState != self.mouseState:
                if mouseState == 32:
                    self.TriggerEvent("Mouse.Button.Left.Pressed")
                elif mouseState == 64:
                    self.TriggerEnduringEvent("Mouse.Button.Right")
                else:
                    if self.mouseState == 32:
                        self.TriggerEvent("Mouse.Button.Left.Released")
                    else:
                        self.EndLastEvent()
                self.mouseState = mouseState
                self.lastDirection = None
            if x != 0 or y != 0:
                if x > 127:
                    x -= 256
                if y > 127:
                    y -= 256
                degree = (round((atan2(x, y) / pi) * 180) + 360) % 360
                if degree != self.lastDirection:
                    self.TriggerEnduringEvent("Mouse.Direction.%03d" % degree)
                    self.lastDirection = degree
                self.timer.Reset(75)
        else:
            if self.numIgnoreCodes == 0:
                if code in BUTTONS:
                    self.numIgnoreCodes, eventname = BUTTONS[code]
                    self.TriggerEnduringEvent(eventname)
                else:
                    self.EndLastEvent()
            else:
                self.numIgnoreCodes -= 1


    @eg.LogIt
    def OnTimeOut(self):
        self.lastDirection = None
        self.EndLastEvent()

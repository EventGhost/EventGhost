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

import eg

ICON = """iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QArABNAAA01td7
AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QQHDwonssmjmQAAAIx0RVh0Q29tbWVudABNZW
51LXNpemVkIGljb24KPT09PT09PT09PQoKKGMpIDIwMDMgSmFrdWIgJ2ppbW1hYycgU3RlaW5lciwg
Cmh0dHA6Ly9qaW1tYWMubXVzaWNoYWxsLmN6CgpjcmVhdGVkIHdpdGggdGhlIEdJTVAsCmh0dHA6Ly
93d3cuZ2ltcC5vcmdnisdHAAACIUlEQVQ4y5WSy2tTQRTGf5Pc5CbW0qSxNvXRh6C4SbAU/4KCexGK
iIKoIFgIwYWtD7TdiC5ECgqCSBZd1boTRNCFuyJUsxNEFCoVNTW3afTmdW/muLhpmkKy6IEDw/DNN7
/55ig61MezhP+q3TNhKV8CfOsqsmBQvzo+Xyi16lSnw3V83/oO7Y0b4RCiNY5dZu37urWhegZPzOft
Ta2vnYFGpWNDsbivK4zr92MVa9iuj4Ej/b3A/Vatr8MLUoFdYfymiREMEAwa/F61iA7GicjGmVahkU
pPzgB3WjfLVganVMHK2XRHuyjm/+HWHNyqQ0WZ0VT6sjSksyqVnpS5h4+2Xf/r5T2qy3NYuSL5tRKi
YN/wHqKxLuqHL3Dw1G1s2+bGrSkMAK01hUJhC+v4OXJvHtM/1MfIaA+GGaD48w+5VYcD5y9iWRZBM7
iVgWjxWrxWgRAD15dY1Kf5uvSFz+8+8ao0zv6b71GBECICjUd4BKLRIiDifawAhokb6mXkwSorKyvk
376GgInWGsAzaRKIYL24xo/pYdYXpxpEGrfutiQjSF0jutENA6OZ/PICUitRWl6g++RdAI4lR3n67E
lzXRfdRG/mtRliaGyCyofnhMYm0FqjREgkkiQSSUQUSomH3zDYRmCaJkevZIBM26mybW9yy+UyAJVK
ZTtBNpvFdV12UkqpLYNIJNJEAqhWqwDUarWOBo7jeEbtRnkHNfsfqMAAn2HmrMwAAAAASUVORK5CYI
I="""

eg.RegisterPlugin(
    name = "Joystick",
    author = "Bitmonster",
    version = "1.0.1175",
    kind = "remote",
    guid = "{615F3B89-FB7E-4FD9-B7D5-9F07FEF0BED9}",
    description = (
        "Use joysticks and gamepads as input devices for EventGhost."
    ),
    icon = ICON,
)


EVT_DIRECTION = 0
EVT_BTN_RELEASED = 1
EVT_BTN_PUSHED = 2
EVT_X_AXIS = 3
EVT_Y_AXIS = 4
EVT_Z_AXIS = 5



class Joystick(eg.PluginBase):

    def __init__(self):
        self.AddEvents()


    def __start__(self):
        self.x = 0
        self.y = 0
        import _dxJoystick
        self._dxJoystick = _dxJoystick
        self._dxJoystick.RegisterEventFunc(self.EventFunc)


    def __stop__(self):
        self._dxJoystick.RegisterEventFunc(None)


    def EventFunc(self, joynum, eventtype, value):
        if eventtype == EVT_BTN_PUSHED:
            self.TriggerEnduringEvent("Button" + str(value + 1))
        elif eventtype == EVT_BTN_RELEASED:
            self.EndLastEvent()
        elif eventtype == EVT_X_AXIS:
            self.x = value
            if value == 0:
                if self.y == 0:
                    self.EndLastEvent()
                elif self.y == 1:
                    self.TriggerEnduringEvent("Down")
                else:
                    self.TriggerEnduringEvent("Up")
            elif value == 1:
                self.TriggerEnduringEvent("Right")
            elif value == -1:
                self.TriggerEnduringEvent("Left")
        elif eventtype == EVT_Y_AXIS:
            self.y = value
            if value == 0:
                if self.x == 0:
                    self.EndLastEvent()
                elif self.x == 1:
                    self.TriggerEnduringEvent("Right")
                else:
                    self.TriggerEnduringEvent("Left")
            elif value == 1:
                self.TriggerEnduringEvent("Down")
            elif value == -1:
                self.TriggerEnduringEvent("Up")


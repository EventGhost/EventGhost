# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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

import colorsys
import wx

# Local imports
from eg.WinApi.Dynamic import (
    COLOR_ACTIVECAPTION,
    COLOR_CAPTIONTEXT,
    COLOR_GRADIENTACTIVECAPTION,
    COLOR_GRADIENTINACTIVECAPTION,
    COLOR_INACTIVECAPTION,
    COLOR_INACTIVECAPTIONTEXT,
    GetSysColor,
)

def GetWinSysColour(nIndex):
    val = GetSysColor(nIndex)
    return val & 0xFF, (val >> 8) & 0xFF, (val >> 16) & 0xFF

class Colour:
    """
    Holds all colours needed by the program.

    These might get configurable in the future.
    """
    windowText = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOWTEXT).Get()
    windowBackground = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW).Get()
    treeItem = windowText
    pluginError = (255, 0, 0)
    activeCaption = GetWinSysColour(COLOR_ACTIVECAPTION)
    activeCaptionGradient = GetWinSysColour(COLOR_GRADIENTACTIVECAPTION)
    activeCaptionTextColour = GetWinSysColour(COLOR_CAPTIONTEXT)
    inactiveCaption = GetWinSysColour(COLOR_INACTIVECAPTION)
    inactiveCaptionGradient = GetWinSysColour(COLOR_GRADIENTINACTIVECAPTION)
    inactiveCaptionTextColour = GetWinSysColour(COLOR_INACTIVECAPTIONTEXT)

    def GetOddLogColour(self):
        """
        Returns the colour for odd lines in the log.
        """
        hue, saturation, value = self.RgbToHsv(self.windowBackground)
        if value > 0.5:
            value -= 0.05
        else:
            value += 0.2
        return self.HsvToRgb(hue, saturation, value)

    def GetRenamedColor(self):
        """
        Returns the colour for renamed elements in the configuration tree.
        """
        hue, saturation, value = self.RgbToHsv(self.windowText)
        if value > 0.5:
            value -= 0.25
        else:
            value += 0.25
        return self.HsvToRgb(hue, saturation, value)

    @staticmethod
    def HsvToRgb(hue, saturation, value):
        """
        Returns RGB colour tuple from HSV (Hue, Saturation, Value).
        """
        red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
        return (
            int(round(red * 255.0)),
            int(round(green * 255.0)),
            int(round(blue * 255.0))
        )

    @staticmethod
    def RgbToHsv(colour):
        """
        Returns HSV (Hue, Saturation, Value) from a RGB colour tuple.
        """
        red, green, blue = colour
        return colorsys.rgb_to_hsv(red / 255.0, green / 255.0, blue / 255.0)

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

import wx

# Local imports
import eg

class ColourSelectButton(wx.BitmapButton):
    def __init__(
        self,
        parent,
        value=(255, 255, 255),
        pos=wx.DefaultPosition,
        size=(40, wx.Button.GetDefaultSize()[1]),
        style=wx.BU_AUTODRAW,
        validator=wx.DefaultValidator,
        name="ColourSelectButton",
        title = "Colour Picker"
    ):
        self.value = value
        self.title = title
        wx.BitmapButton.__init__(
            self, parent, -1, wx.NullBitmap, pos, size, style, validator, name
        )
        self.SetValue(value)
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def GetValue(self):
        return self.value

    def OnButton(self, event):
        colourData = wx.ColourData()
        colourData.SetChooseFull(True)
        colourData.SetColour(self.value)
        for i, colour in enumerate(eg.config.colourPickerCustomColours):
            colourData.SetCustomColour(i, colour)
        dialog = wx.ColourDialog(self.GetParent(), colourData)
        dialog.SetTitle(self.title)
        if dialog.ShowModal() == wx.ID_OK:
            colourData = dialog.GetColourData()
            self.SetValue(colourData.GetColour().Get())
            event.Skip()
        eg.config.colourPickerCustomColours = [
            colourData.GetCustomColour(i).Get() for i in range(16)
        ]
        dialog.Destroy()
        evt = eg.ValueChangedEvent(self.GetId(), value = self.value)
        wx.PostEvent(self, evt)

    def SetValue(self, value):
        self.value = value
        width, height = self.GetSize()
        image = wx.EmptyImage(width - 10, height - 10)
        image.SetRGBRect((1, 1, width - 12, height - 12), *value)
        self.SetBitmapLabel(image.ConvertToBitmap())

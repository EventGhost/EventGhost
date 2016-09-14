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
from eg.Icons import GetInternalBitmap

class FontSelectButton(wx.BitmapButton):
    """
    A button to select a font.
    """
    def __init__(
        self,
        parent,
        id=-1,
        pos=wx.DefaultPosition,
        size=(40, wx.Button.GetDefaultSize()[1]),
        style=wx.BU_AUTODRAW,
        validator=wx.DefaultValidator,
        name="FontSelectButton",
        value=None
    ):
        self.value = value
        wx.BitmapButton.__init__(
            self,
            parent,
            id,
            GetInternalBitmap("font"),
            pos,
            size,
            style,
            validator,
            name
        )
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def GetValue(self):
        return self.value

    def OnButton(self, event):
        fontData = wx.FontData()
        fontData.EnableEffects(False)
        if self.value is not None:
            font = wx.FontFromNativeInfoString(self.value)
            fontData.SetInitialFont(font)
        else:
            fontData.SetInitialFont(
                wx.SystemSettings_GetFont(wx.SYS_ANSI_VAR_FONT)
            )
        dialog = wx.FontDialog(self.GetParent(), fontData)
        if dialog.ShowModal() == wx.ID_OK:
            fontData = dialog.GetFontData()
            font = fontData.GetChosenFont()
            self.value = font.GetNativeFontInfo().ToString()
            event.Skip()
        dialog.Destroy()
        evt = eg.ValueChangedEvent(self.GetId(), value = self.value)
        wx.PostEvent(self, evt)

    def SetValue(self, value):
        self.value = value

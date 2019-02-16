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


class StaticWrapText(wx.Control):

    def __init__(self, parent, wxid=wx.ID_ANY, label='', pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.NO_BORDER,
                 validator=wx.DefaultValidator, name='StaticWrapText'):
        wx.Control.__init__(self, parent, wxid, pos, size, style, validator, name)
        self.statictext = wx.StaticText(self, wx.ID_ANY, label, style=style)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.wraplabel = label
        wx.CallAfter(self.wrap)

    def __getattribute__(self, item):
        try:
            return wx.Control.__getattribute__(self, item)
        except AttributeError:
            print item
            return getattr(self.statictext, item)

    def on_size(self, evt):
        evt.Skip()
        wx.CallAfter(self.wrap)

    def wrap(self):
        self.Freeze()
        self.statictext.SetLabel(self.wraplabel)
        self.statictext.Wrap(self.GetSize().GetWidth())
        self.Thaw()

    def DoGetBestSize(self):
        self.wrap()
        return self.GetSize()

    def SetLabel(self, label):
        self.wraplabel = label
        self.statictext.SetLabel(label)
        wx.CallAfter(self.wrap)

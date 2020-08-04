# -*- coding: utf-8 -*-
#
# plugins/MceRemote_Vista/__init__.py
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.net/>
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


def v_sizer(label, *ctrls):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)
    for ctrl in ctrls:
        sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)

    return sizer


def h_sizer(label, *ctrls):
    sizer = wx.BoxSizer(wx.HORIZONTAL)
    sizer.Add(label, 0, wx.EXPAND | wx.ALL, 5)

    for ctrl in ctrls:
        sizer.Add(ctrl, 1, wx.EXPAND | wx.ALL, 5)

    return sizer

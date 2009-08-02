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

import wx
from eg.WinApi.Dynamic import (
    GetSystemMetrics, GetModuleHandle, CreateWindowEx,
    WS_CHILD, WS_VISIBLE, SBS_SIZEGRIP, SBS_SIZEBOXTOPLEFTALIGN,
    SM_CYHSCROLL, SM_CXVSCROLL,
)
FLAGS = WS_CHILD|WS_VISIBLE|SBS_SIZEGRIP|SBS_SIZEBOXTOPLEFTALIGN


class SizeGrip(wx.PyWindow):

    def __init__(self, parent):
        wx.PyWindow.__init__(self, parent)
        size = GetSystemMetrics(SM_CYHSCROLL), GetSystemMetrics(SM_CXVSCROLL)
        self.SetMinSize(size)
        self.SetMaxSize(size)

        self.sizeGripHandle = CreateWindowEx(
            0,
            "Scrollbar",
            None,
            FLAGS,
            0, 0, 0, 0,
            self.GetHandle(),
            0,
            GetModuleHandle(None),
            None
        )


    def AcceptsFocus(self):
        return False


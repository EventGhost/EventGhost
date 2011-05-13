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
import eg


class PasswordCtrl(wx.TextCtrl):

    def __init__(
        self,
        parent,
        id=-1,
        value="",
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
    ):
        if isinstance(value, eg.Password):
            self.password = value
        else:
            self.password = eg.Password(content=value)
        wx.TextCtrl.__init__(
            self,
            parent,
            id,
            self.password.Get(),
            pos,
            size,
            style=wx.TE_PASSWORD,
        )


    def GetValue(self):
        value = wx.TextCtrl.GetValue(self)
        if value == self.password.Get():
            return self.password
        return eg.Password(content=value)


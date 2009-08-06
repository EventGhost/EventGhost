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

import eg
import wx
from eg.Classes.ControlProviderMixin import ControlProviderMixin


class Dialog(wx.Dialog, ControlProviderMixin):

    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, **kwargs)
        eg.Notify("DialogCreate", self)


    @eg.LogIt
    def Destroy(self):
        eg.Notify("DialogDestroy", self)
        wx.Dialog.Destroy(self)


    def Show(self, show=True):
        if show:
            eg.EnsureVisible(self)
        wx.Dialog.Show(self, show)


    def ShowModal(self):
        eg.EnsureVisible(self)
        return wx.Dialog.ShowModal(self)


# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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


# monkey patch to correct the setting of the value
# following possible errors:
#
# masked.NumCtrl(value=5, min=5)
#   ValueError: value 0 is below minimum value of control
# masked.NumCtrl(value=-15, max=-25)
#   ValueError: value 0 exceeds value of control

import sys
import __builtin__
import wx.lib.masked
import wx.lib.masked.numctrl

_num_ctrl = wx.lib.masked.numctrl.NumCtrl


class _NumCtrl(_num_ctrl):

    def __init__(self, parent, id=-1, value=None, *args, **kwargs):
        self._hold_value = value
        self.SetParameters = self._set_parameters
        _num_ctrl.__init__(self, parent, id, value, *args, **kwargs)

    def _set_parameters(self, **kwargs):
        self.SetValue(self._hold_value)
        _num_ctrl.SetParameters(self, **kwargs)
        self.SetParameters = _num_ctrl.SetParameters

wx.lib.masked.numctrl.NumCtrl = _NumCtrl

sys.modules['wx.lib.masked.numctrl'].NumCtrl = wx.lib.masked.numctrl.NumCtrl
sys.modules['wx.lib.masked'].numctrl.NumCtrl = wx.lib.masked.numctrl.NumCtrl
sys.modules['wx.lib'].masked.numctrl.NumCtrl = wx.lib.masked.numctrl.NumCtrl
sys.modules['wx'].lib.masked.numctrl.NumCtrl = wx.lib.masked.numctrl.NumCtrl

__builtin__.wx = sys.modules['wx']

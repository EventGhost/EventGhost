# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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


import sys
from wx.lib.masked import NumCtrl

_num_ctrl = NumCtrl


class _NumCtrl(_num_ctrl):

    def __init__(self, parent, id=-1, value=None, *args, **kwargs):
        self._hold_value = value
        self.SetParameters = self._set_parameters
        super(_NumCtrl, self).__init__(parent, id, value, *args, **kwargs)
        del self._hold_value

    def _set_parameters(self, **kwargs):
        try:
            self.SetValue(self._hold_value)
            _num_ctrl.SetParameters(self, **kwargs)
        except:
            _num_ctrl.SetParameters(self, **kwargs)
            self.SetValue(self._hold_value)

        self.SetParameters = _num_ctrl.SetParameters


sys.modules['wx.lib.masked.numctrl'].NumCtrl = _NumCtrl
sys.modules['wx.lib.masked'].NumCtrl = _NumCtrl

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
import wx.lib.masked

class TimeCtrl(wx.lib.masked.TimeCtrl):
    """
    Work-around of wx.lib.masked.TimeCtrl bug.
    See http://trac.wxwidgets.org/ticket/11171
    """
    def _TimeCtrl__IncrementValue(self, key, pos):
        text = self.GetValue()
        field = self._FindField(pos)
        start, end = field._extent
        slice = text[start:end]
        if slice == 'A':
            newslice = 'P'
        elif slice == 'P':
            newslice = 'A'
        else:
            top = 24 if field._index == 0 else 60
            increment = 1 if key == wx.WXK_UP else -1
            newslice = "%02d" % ((int(slice) + increment) % top)
        newvalue = text[:start] + newslice + text[end:]
        try:
            self._SetValue(newvalue)
        except ValueError:  # must not be in bounds:
            if not wx.Validator_IsSilent():
                wx.Bell()

    def _TimeCtrl__validateValue(self, value):
        if not value:
            raise ValueError('%s not a valid time value' % repr(value))
        try:
            #value = self.GetWxDateTime(value) - THIS CAUSES THE PROBLEM !!!!!!!
            args = [int(slice) for slice in value.split(":")]
            value = wx.DateTimeFromHMS(*args)
        except:
            raise
        if self.IsLimited() and not self.IsInBounds(value):
            raise ValueError(
                'value %s is not within the bounds of the control' % str(value)
            )
        return value

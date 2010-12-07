# This file is part of EventGhost.
# Copyright (C) 2010 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate: 2010-12-07 14:06:00 +0100 (Tu, 07 Dec 2010) $
# $LastChangedRevision: r1481 $
# $LastChangedBy: Pako $

import wx
import wx.lib.masked

class TimeCtrl(wx.lib.masked.TimeCtrl):

    '''Workaround of wx.lib.masked.TimeCtrl bug.
       See http://trac.wxwidgets.org/ticket/11171'''

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


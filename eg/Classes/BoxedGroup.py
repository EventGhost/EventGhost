# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import wx
import types


class BoxedGroup(wx.StaticBoxSizer):

    def __init__(self, parent, label="", *items):
        staticBox = wx.StaticBox(parent, -1, label)
        wx.StaticBoxSizer.__init__(self, staticBox, wx.VERTICAL)
        self.items = []
        for item in items:
            lineSizer = wx.BoxSizer(wx.HORIZONTAL)
            if isinstance(item, types.StringTypes):
                labelCtrl = wx.StaticText(parent, -1, item)
                lineSizer.Add(
                    labelCtrl,
                    0,
                    wx.LEFT|wx.ALIGN_CENTER_VERTICAL,
                    5
                )
                self.items.append([labelCtrl])
            elif isinstance(item, (types.ListType, types.TupleType)):
                lineItems = []
                for subitem in item:
                    if isinstance(subitem, types.StringTypes):
                        subitem = wx.StaticText(parent, -1, subitem)
                        lineSizer.Add(
                            subitem,
                            0,
                            wx.LEFT|wx.ALIGN_CENTER_VERTICAL,
                            5
                        )
                    else:
                        lineSizer.Add(
                            subitem,
                            0,
                            wx.ALL|wx.ALIGN_CENTER_VERTICAL,
                            5
                        )
                    lineItems.append(subitem)
                self.items.append(lineItems)
            else:
                lineSizer.Add(item, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
                self.items.append([item])
            self.Add(lineSizer, 0, wx.EXPAND)


    def GetColumnItems(self, colNum):
        return [row[colNum] for row in self.items if len(row) > colNum]


    def AppendItem(self):
        pass


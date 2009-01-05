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
           
import eg
import wx


class DisplayChoice(eg.Choice):
    """
    A eg.Choice control, that shows all available displays.
    """
    def __init__(self, parent, value, *args, **kwargs):
        numDisplays = wx.Display().GetCount()
        display = min(value, numDisplays)
        choices = ["Monitor %d" % (i+1) for i in range(numDisplays)]
        eg.Choice.__init__(self, parent, value, choices=choices, *args, **kwargs)

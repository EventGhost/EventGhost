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


from eg.WinApi.Dynamic import (
    GetSystemMetrics, GetModuleHandle, CreateWindowEx,
    WS_CHILD, WS_VISIBLE, SBS_SIZEGRIP, SBS_SIZEBOXTOPLEFTALIGN,
    SM_CYHSCROLL, SM_CXVSCROLL, 
)
FLAGS = WS_CHILD|WS_VISIBLE|SBS_SIZEGRIP|SBS_SIZEBOXTOPLEFTALIGN


class SizeGrip(wx.PyWindow):
    
    def __init__(self, parent, id=-1):
        wx.PyWindow.__init__(self, parent, id)
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
    

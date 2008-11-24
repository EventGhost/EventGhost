# This file is part of EventGhost.
# Copyright (C) 2007 Lars-Peter Voss <bitmonster@eventghost.org>
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
import sys
import wx.lib.mixins.listctrl as listmix
from eg.WinApi import GetWindowText, GetClassName
from eg.WinApi.Utils import GetHwndIcon, GetWindowProcessName


class WindowList(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    
    def __init__(self, parent, hwnds):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        imageList = wx.ImageList(16, 16)
        imageList.Add(wx.Bitmap("images/cwindow.png"))
        self.AssignImageList(imageList, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, "Program")
        self.InsertColumn(1, "Name")
        self.InsertColumn(2, "Class")
        self.InsertColumn(3, "Handle", wx.LIST_FORMAT_RIGHT)
        for hwnd in hwnds:
            imageIdx = 0
            icon = GetHwndIcon(hwnd)
            if icon:
                imageIdx = imageList.AddIcon(icon)
            idx = self.InsertImageStringItem(sys.maxint, GetWindowProcessName(hwnd), imageIdx)
            self.SetStringItem(idx, 1, GetWindowText(hwnd))
            self.SetStringItem(idx, 2, GetClassName(hwnd))
            self.SetStringItem(idx, 3, str(hwnd))
        for i in range(4):
            self.SetColumnWidth(i, -2)
            headerSize = self.GetColumnWidth(i)
            self.SetColumnWidth(i, -1)
            labelSize = self.GetColumnWidth(i)
            if headerSize > labelSize:
                self.SetColumnWidth(i, headerSize)
        
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


class Config(eg.PersistentData):
    position = None
    size = (400, 300)



class HtmlDialog(eg.Dialog):

    def __init__(self, parent, title, htmldata, icon=None, basePath=None):
        style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
        eg.Dialog.__init__(self, parent, -1, title, style=style)
        if icon:
            self.SetIcon(icon)
        htmlCtrl = eg.HtmlWindow(self, -1, style=wx.SUNKEN_BORDER)
        htmlCtrl.SetBorders(2)
        htmlCtrl.SetBasePath(basePath)
        htmlCtrl.SetPage(htmldata)
        okButton = wx.Button(self, wx.ID_OK, eg.text.General.ok)
        okButton.SetDefault()
        self.okButton = okButton

        btnSizer = eg.HBoxSizer(
            ((5, 5), 1, wx.EXPAND),
            (okButton, 0, wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5),
            ((5, 5), 1, wx.EXPAND),
            (eg.SizeGrip(self), 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT),
        )
        mainSizer = eg.VBoxSizer(
            (htmlCtrl, 1, wx.EXPAND|wx.ALL, 5),
            (btnSizer, 0, wx.EXPAND),
        )
        self.SetSizerAndFit(mainSizer)
        if Config.position is not None:
            self.SetPosition(Config.position)
        self.SetSize(Config.size)


    def Destroy(self):
        Config.size = self.GetSizeTuple()
        Config.position = self.GetPositionTuple()
        eg.Dialog.Destroy(self)


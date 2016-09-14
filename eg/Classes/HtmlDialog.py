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

# Local imports
import eg

class Config(eg.PersistentData):
    position = None
    size = (400, 300)


class HtmlDialog(eg.Dialog):
    def __init__(
        self,
        parent=None,
        title=eg.APP_NAME,
        source="",
        icon=None,
        basePath=None,
        style=wx.OK
    ):
        eg.Dialog.__init__(
            self,
            parent,
            -1,
            title,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        if icon:
            self.SetIcon(icon)
        htmlCtrl = eg.HtmlWindow(self, -1, style=wx.SUNKEN_BORDER)
        htmlCtrl.SetBorders(2)
        htmlCtrl.SetBasePath(basePath)
        htmlCtrl.SetPage(source)
        buttonIds = []
        if style & wx.OK:
            buttonIds.append(wx.ID_OK)
        if style & wx.CANCEL:
            buttonIds.append(wx.ID_CANCEL)
        self.buttonRow = eg.ButtonRow(self, buttonIds, True, True)
        mainSizer = eg.VBoxSizer(
            (htmlCtrl, 1, wx.EXPAND | wx.ALL, 5),
            (self.buttonRow.sizer, 0, wx.EXPAND),
        )
        self.SetSizerAndFit(mainSizer)
        if Config.position is not None:
            self.SetPosition(Config.position)
        self.SetSize(Config.size)

    def Destroy(self):
        Config.size = self.GetSizeTuple()
        Config.position = self.GetPositionTuple()
        eg.Dialog.Destroy(self)

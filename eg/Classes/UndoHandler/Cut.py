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
from eg.Classes.UndoHandler import UndoHandlerBase

class Cut(UndoHandlerBase):
    name = eg.text.MainFrame.Menu.Cut.replace("&", "")

    @eg.AssertInMainThread
    def Do(self, selection):
        if not selection.CanDelete() or not selection.AskDelete():
            return

        def ProcessInActionThread():
            self.data = selection.GetFullXml()
            self.treePosition = eg.TreePosition(selection)
            data = selection.GetXmlString()
            selection.Delete()
            return data.decode("utf-8")

        data = eg.actionThread.Func(ProcessInActionThread)()
        self.document.AppendUndoHandler(self)
        if data and wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(data))
            wx.TheClipboard.Close()

    @eg.AssertInActionThread
    def Redo(self):
        self.treePosition.GetItem().Delete()

    @eg.AssertInActionThread
    def Undo(self):
        item = self.document.RestoreItem(self.treePosition, self.data)
        item.Select()

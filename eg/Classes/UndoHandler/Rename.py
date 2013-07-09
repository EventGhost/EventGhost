# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg


class Rename:
    name = eg.text.MainFrame.Menu.Rename.replace("&", "")

    @eg.AssertInMainThread
    def __init__(self, document, item, newName):
        self.newName = newName
        self.oldName = item.name
        self.positionData = eg.TreePosition(item)
        eg.actionThread.Func(item.RenameTo)(newName)
        document.AppendUndoHandler(self)


    @eg.AssertInActionThread
    def Undo(self, document):
        item = self.positionData.GetItem()
        item.RenameTo(self.oldName)
        item.Select()


    @eg.AssertInActionThread
    def Redo(self, document):
        item = self.positionData.GetItem()
        item.RenameTo(self.newName)
        item.Select()


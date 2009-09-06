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
from eg.Classes.UndoHandler import UndoHandlerBase


class NewItem(UndoHandlerBase):
    """
    Abstract class for the creation of new tree items.
    """

    def Do(self, selection):
        raise NotImplementedError


    def StoreItem(self, item):
        self.treePosition = eg.TreePosition(item)
        item.document.AppendUndoHandler(self)


    @eg.AssertInActionThread
    @eg.LogIt
    def Undo(self):
        item = self.treePosition.GetItem()
        self.data = item.GetFullXml()
        item.Delete()


    @eg.AssertInActionThread
    @eg.LogIt
    def Redo(self):
        item = self.document.RestoreItem(self.treePosition, self.data)
        item.Select()


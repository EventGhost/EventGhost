# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2019 EventGhost Project <http://www.eventghost.org/>
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

# Local imports
import eg
from eg.Classes.UndoHandler import UndoHandlerBase

class NewItem(UndoHandlerBase):
    """
    Abstract class for the creation of new tree items.
    """
    def Do(self, selection):
        raise NotImplementedError

    @eg.AssertInActionThread
    @eg.LogIt
    def Redo(self):
        item = self.document.RestoreItem(self.treePosition, self.data)
        item.Select()

    def StoreItem(self, item):
        self.treePosition = eg.TreePosition(item)
        item.document.AppendUndoHandler(self)

    @eg.AssertInActionThread
    @eg.LogIt
    def Undo(self):
        item = self.treePosition.GetItem()
        self.data = item.GetFullXml()
        item.Delete()

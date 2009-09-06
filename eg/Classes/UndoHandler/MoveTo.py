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


class MoveTo(UndoHandlerBase):
    name = "Move Item"

    @eg.AssertInMainThread
    @eg.LogIt
    def Do(self, item, parent, pos):
        oldParent = item.parent
        self.oldPos = item.parent.childs.index(item)
        eg.actionThread.Func(item.MoveItemTo)(parent, pos)
        self.oldParentPath = oldParent.GetPath()
        self.newPositionData = eg.TreePosition(item)
        item.Select()
        self.document.AppendUndoHandler(self)


    @eg.AssertInActionThread
    @eg.LogIt
    def Undo(self):
        parent1, pos1 = self.newPositionData.GetParentAndPosition()
        item = parent1.childs[pos1]
        parent = item.root
        for parentPos in self.oldParentPath:
            parent = parent.childs[parentPos]
        oldParent = item.parent
        oldPos = self.oldPos
        self.oldPos = item.parent.childs.index(item)
        if parent1 == parent:
            if pos1 < oldPos:
                oldPos += 1
        item.MoveItemTo(parent, oldPos)
        self.oldParentPath = oldParent.GetPath()
        self.newPositionData = eg.TreePosition(item)
        item.Select()

    Redo = Undo


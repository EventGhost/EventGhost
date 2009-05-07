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
# $LastChangedDate: 2007-12-23 14:49:00 +0100 (So, 23 Dez 2007) $
# $LastChangedRevision: 344 $
# $LastChangedBy: bitmonster $

import eg


class MoveTo:
    name = "Move Item"

    @eg.LogIt
    def __init__(self, document, item, parent, pos):
        tree = document.tree
        tmp = tree.GetFirstVisibleItem()
        oldParent = item.parent
        self.oldPos = item.parent.childs.index(item)
        item.MoveItemTo(parent, pos)
        tree.EnsureVisible(tmp)
        self.oldParentPath = oldParent.GetPath()
        self.newPositionData = eg.TreePosition(item)
        item.Select()
        document.AppendUndoHandler(self)


    @eg.LogIt
    def Undo(self, document):
        parent1, pos1 = self.newPositionData.GetPosition()
        item = parent1.childs[pos1]
        parent = item.tree.root
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


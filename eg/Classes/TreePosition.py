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

class TreePosition:
    """
    Object to find the position of an item inside the tree.

    This class is mainly used by the Undo/Redo handlers to find the
    right position of an item. Because previous Undo/Redo handlers
    might have deleted/restored an item or any of its parents, they can't
    use any direct item reference, but must use an "index path" to find
    the right object.
    """
    def __init__(self, item):
        self.root = item.root
        self.path = item.GetPath()

    def GetItem(self):
        """
        Returns the item this TreePosition is pointing to.
        """
        item = self.root
        for pos in self.path:
            item = item.childs[pos]
        return item

    def GetParentAndPosition(self):
        """
        Return the parent item and the index inside the parents childs.
        """
        parent = self.root
        for pos in self.path[:-1]:
            parent = parent.childs[pos]
        return parent, self.path[-1]

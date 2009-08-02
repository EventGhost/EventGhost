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
        parent = item.parent
        if parent is None:
            self.GetItem = self.GetRootItem
            return
        self.path = parent.GetPath()
        pos = parent.childs.index(item)
        if pos + 1 >= len(parent.childs):
            pos = -1
        self.pos = pos


    def GetRootItem(self):
        return self.root


    def GetItem(self):
        """
        Returns the item this TreePosition is pointing to.
        """
        searchParent = self.root
        for parentPos in self.path:
            searchParent = searchParent.childs[parentPos]
        return searchParent.childs[self.pos]


    def GetPosition(self):
        """
        Return the parent item and the index inside the parents childs.

        If the item is the last in the parents childs it will return -1 as
        index.
        """
        searchParent = self.root
        for parentPos in self.path:
            searchParent = searchParent.childs[parentPos]
        return searchParent, self.pos


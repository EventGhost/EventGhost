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


class NewFolder(eg.UndoHandler.NewItem):
    """
    Create a new FolderItem if the user has choosen to do so from the menu
    or toolbar.
    """

    @eg.LogIt
    def Do(self, document):
        self.name = eg.text.MainFrame.Menu.AddFolder.replace("&", "")
        obj = document.selection
        if isinstance(obj, (document.MacroItem, document.AutostartItem)):
            parentObj = obj.parent
            pos = parentObj.childs.index(obj) + 1
            if pos >= len(parentObj.childs):
                pos = -1
        elif isinstance(
            obj,
            (document.ActionItem, document.EventItem, document.PluginItem)
        ):
            obj = obj.parent
            parentObj = obj.parent
            pos = parentObj.childs.index(obj) + 1
            if pos >= len(parentObj.childs):
                pos = -1
        else:
            parentObj = obj
            pos = -1
        item = document.FolderItem.Create(
            parentObj,
            pos,
            name=eg.text.General.unnamedFolder
        )
        self.StoreItem(item)
        item.tree.SetFocus()
        item.Select()
        item.tree.EditLabel(item.id)
        return item


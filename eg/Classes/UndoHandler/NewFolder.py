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
from NewItem import NewItem


class NewFolder(NewItem):
    """
    Create a new FolderItem if the user has choosen to do so from the menu
    or toolbar.
    """
    name = eg.text.MainFrame.Menu.AddFolder.replace("&", "")

    @eg.LogIt
    def Do(self, document, selection):
        if isinstance(selection, (document.MacroItem, document.AutostartItem)):
            parentObj = selection.parent
            pos = parentObj.childs.index(selection) + 1
            if pos >= len(parentObj.childs):
                pos = -1
        elif isinstance(
            selection,
            (document.ActionItem, document.EventItem, document.PluginItem)
        ):
            selection = selection.parent
            parentObj = selection.parent
            pos = parentObj.childs.index(selection) + 1
            if pos >= len(parentObj.childs):
                pos = -1
        else:
            parentObj = selection
            pos = -1
        item = document.FolderItem.Create(
            parentObj,
            pos,
            name=eg.text.General.unnamedFolder
        )
        self.StoreItem(item)
        item.Select()
        return item


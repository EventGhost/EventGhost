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

# Local imports
import eg
from NewItem import NewItem

class NewFolder(NewItem):
    """
    Create a new FolderItem if the user has choosen to do so from the menu
    or toolbar.
    """
    name = eg.text.MainFrame.Menu.AddFolder.replace("&", "")

    @eg.AssertInMainThread
    @eg.LogIt
    def Do(self, selection):
        document = self.document

        def ProcessInActionThread():
            if isinstance(
                selection,
                (document.MacroItem, document.AutostartItem)
            ):
                parent = selection.parent
                pos = parent.childs.index(selection) + 1
                if pos >= len(parent.childs):
                    pos = -1
            elif isinstance(
                selection,
                (document.ActionItem, document.EventItem, document.PluginItem)
            ):
                parent = selection.parent.parent
                pos = parent.childs.index(selection.parent) + 1
                if pos >= len(parent.childs):
                    pos = -1
            else:
                parent = selection
                pos = -1
            return document.FolderItem.Create(
                parent,
                pos,
                name=eg.text.General.unnamedFolder
            )
        item = eg.actionThread.Func(ProcessInActionThread)()
        self.StoreItem(item)
        item.Select()
        return item

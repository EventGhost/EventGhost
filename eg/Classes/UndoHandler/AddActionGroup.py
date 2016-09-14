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

class AddActionGroup(eg.UndoHandler.NewItem):
    name = "Add all actions of plugin"

    @eg.AssertInMainThread
    def Do(self, pluginItem):
        document = self.document
        result = eg.AddActionGroupDialog.GetResult((document.frame))
        if result is None:
            return
        parentItem = result[0]

        def Traverse(parentItem, actionGroup):
            folderItem = document.FolderItem.Create(
                parentItem,
                name=actionGroup.name
            )
            for item in actionGroup.items:
                if isinstance(item, eg.ActionGroup):
                    Traverse(folderItem, item)
                else:
                    macroItem = document.MacroItem.Create(
                        folderItem,
                        name=item.name
                    )
                    document.ActionItem.Create(
                        macroItem,
                        text = "%s.%s()" % (
                            item.plugin.info.evalName,
                            item.__name__
                        ),
                    )
            return folderItem

        folderItem = eg.actionThread.Func(Traverse)(
            parentItem,
            pluginItem.executable.info.actionGroup
        )
        self.StoreItem(folderItem)
        folderItem.Select()
        folderItem.Expand()

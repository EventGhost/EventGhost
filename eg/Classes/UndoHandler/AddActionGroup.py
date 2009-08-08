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


class AddActionGroup(eg.UndoHandler.NewItem):
    name = "Add all actions of plugin"

    def Do(self, document, pluginItem):
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
                    actionItem = document.ActionItem.Create(
                        macroItem,
                        text = "%s.%s()" % (
                            item.plugin.info.evalName,
                            item.__name__
                        ),
                    )
            return folderItem
        folderItem = Traverse(
            parentItem,
            pluginItem.executable.info.actionGroup
        )
        self.StoreItem(folderItem)
        folderItem.Select()
        folderItem.Expand()


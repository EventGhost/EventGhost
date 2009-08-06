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


class NewMacro(NewItem):
    """
    Create a new MacroItem if the user has choosen to do so from the menu
    or toolbar.
    """
    name = eg.text.MainFrame.Menu.AddMacro.replace("&", "")

    def Do(self, document, selection):
        obj = selection
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
        item = document.MacroItem.Create(
            parentObj,
            pos,
            name=eg.text.General.unnamedMacro
        )
        item.Select()
        self.StoreItem(item)
        # let the user choose an action
        result = eg.AddActionDialog.GetModalResult(document.frame)

        # if user canceled the dialog, take a quick exit
        if result is None:
            return item
        action = result[0]

        actionObj = eg.UndoHandler.NewAction().Do(document, item, action)
        if actionObj:
            label = actionObj.GetLabel()
            item.RenameTo(label)
            item.Select()
        return item


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

class NewAction(NewItem):
    """
    Create a new ActionItem if the user has choosen to do so from the menu
    or toolbar.
    """
    name = eg.text.MainFrame.Menu.AddAction.replace("&", "")

    @eg.AssertInMainThread
    def Do(self, selection, action):
        document = self.document
        # find the right insert position
        if isinstance(selection, (document.MacroItem, document.AutostartItem)):
            # if a macro is selected, append it as last element of the macro
            parent = selection
            pos = -1
        else:
            parent = selection.parent
            childs = parent.childs
            for pos in range(childs.index(selection) + 1, len(childs)):
                if not isinstance(childs[pos], document.EventItem):
                    break
            else:
                pos = -1

        # create the ActionItem instance and setup all data
        item = eg.actionThread.Func(document.ActionItem.Create)(
            parent,
            pos,
            text = "%s.%s()" % (action.plugin.info.evalName, action.__name__)
        )
        item.Select()

        if item.NeedsStartupConfiguration():
            if not document.CmdConfigure(item, True):
                eg.actionThread.Call(item.Delete)
                return None
        self.StoreItem(item)
        return item

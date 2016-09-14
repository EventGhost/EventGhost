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

class NewEvent(NewItem):
    name = eg.text.MainFrame.Menu.AddEvent.replace("&", "").replace("...", "")

    @eg.AssertInMainThread
    def Do(self, selection, pos=-1, label=None):
        document = self.document

        def ProcessInActionThread():
            parent = selection
            if not isinstance(selection, document.MacroItem):
                parent = selection.parent
            pos = 0
            for child in parent.childs:
                if isinstance(child, document.ActionItem):
                    break
                pos += 1
            else:
                pos = 0
            if not isinstance(parent, eg.MacroItem):
                return
            if isinstance(parent, eg.AutostartItem):
                return
            needsConfigure = False
            name = label
            if label is None:
                name = eg.event.string
                needsConfigure = True
            eventItem = document.EventItem.Create(parent, pos, name=name)
            eventItem.Select()
            return eventItem, needsConfigure

        result = eg.actionThread.Func(ProcessInActionThread)()
        if result is None:
            return
        item, needsConfigure = result

        if (
            needsConfigure and
            not eg.UndoHandler.Configure(document).Do(item, True)
        ):
            eg.actionThread.Call(item.Delete)
            return None
        self.StoreItem(item)
        return item

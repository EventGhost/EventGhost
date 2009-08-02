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


class NewEvent(NewItem):
    name = eg.text.MainFrame.Menu.AddEvent.replace("&", "").replace("...", "")

    def Do(self, document, selection, pos=-1, label=None):
        if not isinstance(selection, document.MacroItem):
            selection = selection.parent
        pos = 0
        for child in selection.childs:
            if isinstance(child, document.ActionItem):
                break
            pos += 1
        else:
            pos = 0
        if not isinstance(selection, eg.MacroItem):
            return
        if isinstance(selection, eg.AutostartItem):
            return
        needsConfigure = False
        if label is None:
            label = eg.event.string
            needsConfigure = True
        item = document.EventItem.Create(selection, pos, name=label)
        item.Select()

        if needsConfigure and not eg.UndoHandler.Configure().Do(item, True):
            item.Delete()
            return None
        self.StoreItem(item)
        return item


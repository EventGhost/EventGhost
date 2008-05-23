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


class NewEvent(eg.UndoHandler.NewItem):
    
    def Do(self, document, label=None, parent=None, pos=-1):
        self.name = eg.text.MainFrame.Menu.AddEvent.replace("&", "")
        if parent is None:
            obj = document.selection
            if isinstance(obj, document.MacroItem):
                parent = obj
            else:
                parent = obj.parent
            for pos, obj in enumerate(parent.childs):
                if isinstance(obj, document.ActionItem):
                    break
            else:
                pos = 0
        if not isinstance(parent, eg.MacroItem):
            return
        if isinstance(parent, eg.AutostartItem):
            return    
        if label is not None:
            item = document.EventItem.Create(parent, pos, name=label)
            item.Select()
        else:
            label = eg.text.General.unnamedEvent
            item = document.EventItem.Create(parent, pos, name=label)
            item.Select()
            item.tree.EditLabel(item.id)
            
        self.StoreItem(item)
        return item
    



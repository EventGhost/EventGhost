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


class AddActionGroup(eg.UndoHandler.NewItem):
    name="Add all actions of plugin"
    
    def Do(self, document, pluginItem):
        parentItem = eg.AddActionGroupDialog.GetModalResult((document.frame))
        if parentItem is None:
            return
        parentItem = parentItem[0][0]
        
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
        folderItem = Traverse(parentItem, pluginItem.executable.info.actionGroup)
        self.StoreItem(folderItem)
        folderItem.Select()
        folderItem.tree.Expand(folderItem.id)
            
    
    

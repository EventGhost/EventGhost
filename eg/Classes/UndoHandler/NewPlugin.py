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
# $LastChangedDate: 2007-12-23 14:49:00 +0100 (So, 23 Dez 2007) $
# $LastChangedRevision: 344 $
# $LastChangedBy: bitmonster $


class NewPlugin(eg.UndoHandler.NewItem):
    """
    Create a new PluginItem if the user has choosen to do so from the menu
    or toolbar.
    """
    
    def Do(self, document, pluginInfo):
        """ Handle the menu command 'Add Plugin...'. """
        self.name = eg.text.MainFrame.Menu.AddPlugin.replace("&", "")

        pluginItem = document.PluginItem.Create(
            document.autostartMacro,
            -1,
            file=pluginInfo.pluginName
        )
        pluginItem.Select()
        if pluginItem.executable:
            if pluginItem.NeedsStartupConfiguration():
                if not eg.UndoHandler.Configure().Do(pluginItem):
                    pluginItem.Delete()
                    return None
            eg.actionThread.CallWait(pluginItem.Execute)
        self.StoreItem(pluginItem)
        if pluginInfo.createMacrosOnAdd:
            eg.UndoHandler.AddActionGroup().Do(document, pluginItem)
        return pluginItem
       
            
            

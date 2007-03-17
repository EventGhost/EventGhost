# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <lpv@eventghost.org>
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
from MacroItem import MacroItem

class AutostartItem(MacroItem):
    xmlTag = "Autostart"
    iconIndex = eg.SetupIcons("Execute")
    isDeactivatable = False
    isRenameable = False
    
    
    def __init__(self, parent, node):
        MacroItem.__init__(self, parent, node)
        self.name = eg.text.General.autostartItem
        self.document.autostartMacro = self
        
        
    def CanCut(self):
        return False
    
    
    def CanCopy(self):
        return False
    
    
    def CanDelete(self):
        return False
    
    
    def Enable(self, flag):
        pass
    
    
    @eg.LogIt
    def UnloadPlugins(self):
        for child in self.childs:
            if child.__class__ == self.document.PluginItem:
                if child.executable:
                    child.StopPlugin()
                    eg.ClosePlugin(child.executable)
    
    
    def DropTest(self, cls):
        if cls == FolderItem:
            return 3 # 3 = item would move after
        if cls == MacroItem:
            return 3 # 3 = item would move after
        if cls == ActionItem:
            return 1 # 1 = item would be dropped inside
        #if cls == PluginItem:
        #    return 1 # 1 = item would be dropped inside
        return None # None = item cannot be dropped on it


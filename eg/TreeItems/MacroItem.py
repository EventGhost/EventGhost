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

import wx
import eg
from ContainerItem import ContainerItem


class MacroItem(ContainerItem):
    xmlTag = "Macro"
    iconIndex = eg.SetupIcons("macro")
    canExecute = True    
    

    def GetNextChild(self, index):
        index += 1
        if len(self.childs) > index:
            return self.childs[index], index
        else:
            return None
        
        
    def Execute(self):
        if self.isEnabled:
            del eg.lastFoundWindows[:]
            if self.shouldSelectOnExecute:
                wx.CallAfter(self.Select)
                
            if self.childs:
                eg.SetProgramCounter((self.childs[0], 0))
            else:
                eg.SetProgramCounter(None)


    def DropTest(self, cls):
        if cls == EventItem:
            return 1 # 1 = item would be dropped inside
        if cls == MacroItem:
            return 4 # 4 = item can be inserted before or after
        if cls == FolderItem:
            return 4 # 4 = item can be inserted before or after
        if cls == ActionItem:
            return 1 # 1 = item would be dropped inside
        return None  # None = item cannot be dropped on it

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
from TreeItem import TreeItem


        
class EventItem(TreeItem):
    xmlTag = "Event"
    icon = eg.Icons.EVENT_ICON
    
    def __init__(self, parent, node):
        TreeItem.__init__(self, parent, node)
        eg.RegisterEvent(self.name, self)
        
        
    def _Delete(self):
        eg.UnRegisterEvent(self.name, self)
        TreeItem._Delete(self)
        
        
    def RenameTo(self, newName):
        eg.UnRegisterEvent(self.name, self)
        TreeItem.RenameTo(self, newName)
        eg.RegisterEvent(newName, self)
        
        
    def DropTest(self, cls):
        if cls == EventItem:
            return 4 # 4 = item can be inserted before or after
        if cls == eg.ActionItem:
            return 3 # 3 = item would move after
        return None # None = item cannot be dropped on it



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
from TreeItem import HINT_NO_DROP, HINT_MOVE_BEFORE_OR_AFTER, HINT_MOVE_AFTER

        
class EventItem(TreeItem):
    xmlTag = "Event"
    icon = eg.Icons.EVENT_ICON
    
    def __init__(self, parent, node):
        TreeItem.__init__(self, parent, node)
        self.RegisterEvent(self.name)        
        
        
    def _Delete(self):
        self.UnRegisterEvent(self.name)
        TreeItem._Delete(self)
        
        
    def RenameTo(self, newName):
        self.UnRegisterEvent(self.name)
        TreeItem.RenameTo(self, newName)
        self.RegisterEvent(newName)
        
        
    def RegisterEvent(self, eventString):
        eventTable = eg.eventTable
        if eventString not in eventTable:
            eventTable[eventString] = []
        eventTable[eventString].append(self)
    
                
    def UnRegisterEvent(self, eventString):
        eventTable = eg.eventTable
        if eventString not in eventTable:
            return
        try:
            eventTable[eventString].remove(self)
        except:
            pass
        if len(eventTable[eventString]) == 0:
            del eventTable[eventString]

    
    def DropTest(self, cls):
        if cls == EventItem:
            return HINT_MOVE_BEFORE_OR_AFTER
        if cls == eg.ActionItem:
            return HINT_MOVE_AFTER
        return HINT_NO_DROP


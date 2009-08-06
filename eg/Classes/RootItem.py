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
import time
from ContainerItem import ContainerItem
from TreeItem import HINT_NO_DROP, HINT_MOVE_INSIDE


class RootItem(ContainerItem):
    xmlTag = "EventGhost"
    icon = eg.Icons.ROOT_ICON
    time = None
    guid = None
    isDeactivatable = False
    isRenameable = False

    def GetData(self):
        from comtypes import GUID
        attr, text = ContainerItem.GetData(self)
        self.guid = str(GUID.create_new())
        self.time = str(time.time())
        attr.append(('Version', str(eg.revision)))
        attr.append(('Guid', self.guid))
        attr.append(('Time', self.time))
        return attr, text


    def __init__(self, parent, node):
        parent = None
        ContainerItem.__init__(self, parent, node)
        self.guid = node.attrib.get("guid", "0")
        self.time = node.attrib.get("time", "0")
        self.name = eg.text.General.configTree


    def Delete(self):
        childs = self.childs[:]
        for child in childs:
            child.Delete()


    def CanCut(self):
        return False


    def CanCopy(self):
        return False


    def CanDelete(self):
        return False


    def Enable(self, flag=True):
        pass


    def DropTest(self, cls):
        if cls == eg.MacroItem:
            return HINT_MOVE_INSIDE
        if cls == eg.FolderItem:
            return HINT_MOVE_INSIDE
        return HINT_NO_DROP


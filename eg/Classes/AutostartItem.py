# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.net/>
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
from MacroItem import MacroItem
from TreeItem import HINT_MOVE_INSIDE, HINT_MOVE_AFTER
from datetime import datetime


class Time(object):
    _datetime = None

    def __init__(self):
        self._datetime = datetime.now()

    def __getattr__(self, item):
        return getattr(self._datetime, item)

    def __str__(self):
        t_fmt = '%A, %B %d{}, %Y @ %H:%M:%S %p'
        if 4 <= self.day <= 20 or 24 <= self.day <= 30:
            t_fmt = t_fmt.format('th')
        else:
            t_fmt = t_fmt.format(
                ["st", "nd", "rd"][self.day % 10 - 1]
            )
        return self.strftime(t_fmt)

    def __repr__(self):
        return self.__str__()

class AutostartItem(MacroItem):
    xmlTag = "Autostart"
    icon = eg.Icons.AUTOSTART_ICON
    isDeactivatable = False
    isRenameable = False
    isMoveable = False
    dropBehaviour = {
        "Folder": HINT_MOVE_AFTER,
        "Macro": HINT_MOVE_AFTER,
        "Plugin": HINT_MOVE_INSIDE,
        "Action": HINT_MOVE_INSIDE,
    }

    @eg.AssertInActionThread
    def __init__(self, parent, node):
        eg.TreeItem.__init__(self, parent, node)
        tagDict = self.document.XMLTag2ClassDict
        self.childs = []
        for childNode in node:
            childTag = childNode.tag.lower()
            if childTag == "plugin":
                child = self.document.PluginItem(self, childNode)
            else:
                child = None
            self.childs.append(child)
        for i, childNode in enumerate(node):
            childTag = childNode.tag.lower()
            if childTag == "plugin":
                continue
            self.childs[i] = tagDict[childTag](self, childNode)
        if node.attrib.get("expanded", "").lower() == "true":
            self.document.expandedNodes.add(self)
        self.name = eg.text.General.autostartItem
        self.document.autostartMacro = self

    def CanCut(self):
        return False

    def CanCopy(self):
        return False

    def CanDelete(self):
        return False

    def Enable(self, flag=True):
        # never disable the Autostart item
        pass

    def Execute(self):
        event = eg.EventGhostEvent(
            prefix='EventGhost',
            suffix='Startup',
            payload=Time()
        )
        event.Execute()
        MacroItem.Execute(self)

    @eg.LogIt
    @eg.AssertInActionThread
    def UnloadPlugins(self):
        for child in self.childs:
            if child.__class__ == self.document.PluginItem:
                child.info.Close()
                child.info.RemovePluginInstance()

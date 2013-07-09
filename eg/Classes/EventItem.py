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
from TreeItem import TreeItem, HINT_MOVE_BEFORE_OR_AFTER, HINT_MOVE_AFTER

class Text(eg.TranslatableStrings):
    eventItem = "Event Item"
    eventName = "Event Name:"
    notice = (
        "Note: You can also drag and drop events from the logger to a "
        "macro."
    )



class EventItem(TreeItem):
    xmlTag = "Event"
    icon = eg.Icons.EVENT_ICON
    isConfigurable = True
    openConfigDialog = None
    isRenameable = False
    dropBehaviour = {
        "Event": HINT_MOVE_BEFORE_OR_AFTER,
        "Action": HINT_MOVE_AFTER,
    }

    def __init__(self, parent, node):
        TreeItem.__init__(self, parent, node)
        self.RegisterEvent(self.name)


    def GetTypeName(self):
        return Text.eventItem


    def GetDescription(self):
        return ""


    def GetArgumentString(self):
        return self.name


    def SetArgumentString(self, argString):
        self.RenameTo(argString)


    def GetArguments(self):
        return (self.name, )


    def SetArguments(self, args):
        newName = args[0]
        self.RenameTo(newName)


    def GetBasePath(self):
        """
        Returns the filesystem path, where additional files (like pictures)
        should be found.
        """
        # currently an event item doesn't have any plugin assigned to it,
        # so we also have no base path
        return ""


    def Configure(self, name):
        panel = eg.ConfigPanel()
        staticText = panel.StaticText(Text.eventName)
        textCtrl = panel.TextCtrl(name, size=(250, -1))
        staticText2 = panel.StaticText(Text.notice)
        panel.sizer.Add(staticText)
        panel.sizer.Add(textCtrl)
        panel.sizer.Add((5, 5))
        panel.sizer.Add(staticText2)
        while panel.Affirmed():
            panel.SetResult(textCtrl.GetValue())


    def Delete(self):
        self.UnRegisterEvent(self.name)
        TreeItem.Delete(self)


    @eg.AssertInActionThread
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


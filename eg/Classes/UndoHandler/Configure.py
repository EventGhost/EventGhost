# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

import wx

# Local imports
import eg
from eg.Classes.UndoHandler import UndoHandlerBase

class Configure(UndoHandlerBase):
    name = eg.text.MainFrame.Menu.Configure.replace("&", "")

    @eg.AssertInMainThread
    @eg.LogItWithReturn
    def Do(self, item, isFirstConfigure = False):
        if item.openConfigDialog:
            item.openConfigDialog.Raise()
            return False
        item.isFirstConfigure = isFirstConfigure
        ActionThreadFunc = eg.actionThread.Func
        self.oldArgumentString = ActionThreadFunc(item.GetArgumentString)()
        #oldArgs = newArgs = ActionThreadFunc(item.GetArguments)()
        newArgs = ActionThreadFunc(item.GetArguments)()  # bugfix: http://www.eventghost.org/forum/viewtopic.php?f=4&t=3676
        oldArgs = DeepCopy(newArgs)                      # bugfix
        revertOnCancel = False
        dialog = eg.ConfigDialog.Create(item, *oldArgs)

        for event, newArgs in dialog:
            if event == wx.ID_OK:
                break
            elif event == wx.ID_APPLY:
                revertOnCancel = True
                ActionThreadFunc(item.SetArguments)(newArgs)
                item.Refresh()
            elif event == eg.ID_TEST:
                revertOnCancel = True
                eg.actionThread.Call(DoExecute, item, newArgs)
        else:
            if revertOnCancel:
                ActionThreadFunc(item.SetArguments)(oldArgs)
                item.Refresh()
            return False
        ActionThreadFunc(item.SetArguments)(newArgs)
        newArgumentString = ActionThreadFunc(item.GetArgumentString)()

        if self.oldArgumentString != newArgumentString:
            if not isFirstConfigure:
                self.treePosition = eg.TreePosition(item)
                item.document.AppendUndoHandler(self)
            item.Refresh()
        return True

    @eg.AssertInActionThread
    def Undo(self):
        item = self.treePosition.GetItem()
        argumentString = item.GetArgumentString()
        eg.TreeLink.StartUndo()
        item.SetArgumentString(self.oldArgumentString)
        eg.TreeLink.StopUndo()
        self.oldArgumentString = argumentString
        item.Refresh()
        item.Select()

    Redo = Undo


def DeepCopy(lst):
    res = []
    for item in lst:
        if type(item) in (list, tuple):
            res.append(DeepCopy(item))
        else:
            res.append(item)
    if type(lst) is tuple:
        res = tuple(res)
    return res

def DoExecute(item, newArgs):
    oldArgs = item.GetArguments()
    item.SetArguments(newArgs)
    item.Execute()
    item.SetArguments(oldArgs)

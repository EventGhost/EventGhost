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
import wx
from eg.Classes.UndoHandler import UndoHandlerBase

def DoExecute(item, newArgs):
    oldArgs = item.GetArguments()
    item.SetArguments(newArgs)
    item.Execute()
    item.SetArguments(oldArgs)


class Configure(UndoHandlerBase):
    name = eg.text.MainFrame.Menu.Configure.replace("&", "")

    @eg.AssertInMainThread
    @eg.LogItWithReturn
    def Do(self, item, isFirstConfigure=False):
        if item.openConfigDialog:
            item.openConfigDialog.Raise()
            return False
        ActionThreadFunc = eg.actionThread.Func
        self.oldArgumentString = ActionThreadFunc(item.GetArgumentString)()
        oldArgs = newArgs = ActionThreadFunc(item.GetArguments)()
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


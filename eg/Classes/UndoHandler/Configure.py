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
import wx


def DoExecute(item, newArgs):
    oldArgs = item.GetArgs()
    item.SetArgs(newArgs)
    item.Execute()
    item.SetArgs(oldArgs)


class Configure:
    name = eg.text.MainFrame.Menu.Configure.replace("&", "")

    @eg.LogItWithReturn
    def Try(self, document):
        item = document.selection
        if isinstance(item, (eg.ActionItem, eg.EventItem)):
            eg.Tasklet(self.Do)(item).run()


    @eg.LogItWithReturn
    def Do(self, item, isFirstConfigure=False):
        # TODO: doing the thread ping-pong right

        if item.openConfigDialog:
            item.openConfigDialog.Raise()
            return False

        self.oldArgumentString = item.GetArgumentString()
        oldArgs = newArgs = item.GetArgs()
        revertOnCancel = False
        eg.currentConfigureItem = item
        dialog = eg.ConfigDialog.Create(item, *oldArgs)
        for event, newArgs in dialog:
            if event == wx.ID_OK:
                break
            elif event == wx.ID_APPLY:
                revertOnCancel = True
                item.SetArgs(newArgs)
                item.Refresh()
            elif event == eg.ID_TEST:
                revertOnCancel = True
                eg.actionThread.Call(DoExecute, item, newArgs)
        else:
            if revertOnCancel:
                item.SetArgs(oldArgs)
                item.Refresh()
            return False

        item.SetArgs(newArgs)
        newArgumentString = item.GetArgumentString()
        if self.oldArgumentString != newArgumentString:
            if not isFirstConfigure:
                self.positionData = eg.TreePosition(item)
                item.document.AppendUndoHandler(self)
            item.Refresh()
        return True


    def Undo(self, document):
        item = self.positionData.GetItem()
        argumentString = item.GetArgumentString()
        eg.TreeLink.StartUndo()
        item.SetArgumentString(self.oldArgumentString)
        eg.TreeLink.StopUndo()
        self.oldArgumentString = argumentString
        item.Refresh()
        item.Select()

    Redo = Undo


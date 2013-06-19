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
# $LastChangedDate: 2007-12-23 14:49:00 +0100 (So, 23 Dez 2007) $
# $LastChangedRevision: 344 $
# $LastChangedBy: bitmonster $


class Configure:
    
    def Try(self, document):
        item = document.selection
        if isinstance(item, eg.ActionItem):
            eg.Greenlet(self.Do).switch(item)
        
    
    def Do(self, item, isFirstConfigure=False):
        # TODO: doing the thread ping-pong right
        executable = item.executable
        if executable is None:
            return False
        if item.openConfigDialog:
            item.openConfigDialog.Raise()
            return False
        
        self.oldArgumentString = item.GetArgumentString()
        oldArgs = item.args
        self.name = eg.text.MainFrame.Menu.Edit.replace("&", "")
        
        wasApplied = False
        lastArgs = oldArgs
        gr = None
        while True:
            eg.currentConfigureItem = item
            try:
                if gr is None or gr.dead:
                    gr = eg.Greenlet(executable.Configure)
                    newArgs = gr.switch(*item.GetArgs())
                else:
                    newArgs = gr.switch()
            except:
                eg.PrintError("Error while configuring: %s", item.GetLabel())
                raise
            if item.openConfigDialog is not None:
                userAction = item.openConfigDialog.result
                if userAction == wx.ID_CANCEL:
                    if not gr.dead:
                        gr.switch()
                    item.openConfigDialog.Destroy()
                    del item.openConfigDialog
                    if wasApplied:
                        item.SetArgs(oldArgs)
                        item.Refresh()
                    return False
                elif userAction == wx.ID_OK:
                    if not gr.dead:
                        gr.switch(wx.ID_CANCEL)
                    item.openConfigDialog.Destroy()
                    del item.openConfigDialog
                    break
                elif userAction == wx.ID_APPLY:
                    lastArgs = newArgs
                    item.SetArgs(newArgs)
                    item.Refresh()
                    wasApplied = True
                    continue
                elif userAction == eg.ID_TEST:
                    def Do():
                        item.SetArgs(newArgs)
                        item.Execute()
                        item.SetArgs(lastArgs)
                    eg.actionThread.Call(Do)
                    continue
            elif newArgs is None:
                return False
            elif newArgs is -1:
                # This is most likely a PythonScript action
                return True
        item.SetArgs(newArgs)
        newArgumentString = item.GetArgumentString()
        if self.oldArgumentString != newArgumentString:
            if not isFirstConfigure:
                self.positionData = item.GetPositionData()
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

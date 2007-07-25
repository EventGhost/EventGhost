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

import sys
import os
import imp
import traceback
import inspect
import weakref

import wx
import eg


    
class Text:
    title = "Python-Editor - %s"
    class SaveChanges:
        title = "Apply changes?"
        mesg = "The file was altered.\n\nDo you want to apply the changes?\n"

Text = eg.GetTranslation(Text)



class ScriptEditor(wx.Frame):
    
    def __init__(self, parent, id, actionItem, action):
        self.actionItem = actionItem
        if len(actionItem.args) < 1:
            actionItem.args = ['']
        text = actionItem.args[0]
        config = self.config = action.config
        wx.Frame.__init__(
            self, 
            parent, 
            id,
            eg.APP_NAME + " " + (Text.title % actionItem.GetLabel()),
            pos=config.position,
            size=config.size,
            style=wx.DEFAULT_FRAME_STYLE
        )
        self.SetIcon(action.info.GetWxIcon())
        
        self.editCtrl = editCtrl = eg.PythonEditorCtrl(self)
        editCtrl.SetText(text)
        editCtrl.EmptyUndoBuffer()
        editCtrl.Colourise(0, -1)

        self.CreateStatusBar()

        # menu creation
        self.MenuBar = eg.MenuBar(self, eg.text.MainFrame.Menu)

        # file menu
        fileMenu = self.MenuBar.AddMenu("File")
        AddItem = fileMenu.AddItem
        AddItem("Apply", hotkey="F4")
        AddItem("Execute", hotkey="F5")
        AddItem()
#        if eg.debugLevel:
#            AddItem("EditLinks")
#            AddItem()
        AddItem("Close", hotkey="Ctrl+W")

        # edit menu        
        editMenu = self.MenuBar.AddMenu("Edit")
        AddItem = editMenu.AddItem
        AddItem("Undo", hotkey="Ctrl+Z")
        AddItem("Redo", hotkey="Ctrl+Y")
        AddItem()
        AddItem("Cut", hotkey="Ctrl+X")
        AddItem("Copy", hotkey="Ctrl+C")
        AddItem("Paste", hotkey="Ctrl+V")
        AddItem("Delete", hotkey="Del")
        AddItem()
        AddItem("SelectAll", hotkey="Ctrl+A")

        self.MenuBar.Realize()
        
        # popup menu
        popupMenu = self.popupMenu = eg.Menu(self, "", eg.text.MainFrame.Menu)
        AddItem = popupMenu.AddItem
        AddItem("Undo")
        AddItem("Redo")
        AddItem()
        AddItem("Cut")
        AddItem("Copy")
        AddItem("Paste")
        AddItem("Delete")
        AddItem()
        AddItem("SelectAll")

        self.Show(True)
        self.Bind(wx.EVT_CLOSE, self.OnCmdClose)
        self.Bind(wx.EVT_MENU_OPEN, self.OnShowMenu)
        editCtrl.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)


    def CheckFileNeedsSave(self):
        if self.editCtrl.GetModify():
            dlg = wx.MessageDialog(
                self,
                Text.SaveChanges.mesg, 
                Text.SaveChanges.title, 
                wx.YES_DEFAULT 
                    |wx.YES_NO
                    |wx.CANCEL
                    |wx.STAY_ON_TOP
                    |wx.ICON_EXCLAMATION
            )
            res = dlg.ShowModal()
            dlg.Destroy()
            if res == wx.ID_CANCEL:
                return wx.ID_CANCEL
            if res == wx.ID_YES:
                self._FileSave()
        return wx.ID_OK


    def OnShowMenu(self, event):
        self.ValidateEditMenu(self.MenuBar.Edit)
        self.MenuBar.File.Apply.Enable(self.editCtrl.GetModify())
        
        
    def OnRightClick(self, event):
        self.ValidateEditMenu(self.popupMenu)
        self.editCtrl.PopupMenu(self.popupMenu)


    def ValidateEditMenu(self, menu):
        editCtrl = self.editCtrl
        menu.Undo.Enable(editCtrl.CanUndo())
        menu.Redo.Enable(editCtrl.CanRedo())
        first, last = editCtrl.GetSelection()
        menu.Cut.Enable(first != last)
        menu.Copy.Enable(first != last)
        menu.Paste.Enable(editCtrl.CanPaste())
        menu.Delete.Enable(True)


    def OnCmdApply(self, event):
        self._FileSave()
        
        
    def OnCmdExecute(self, event):
        pass
        
        
    def OnCmdClose(self, event):
        if self.CheckFileNeedsSave() == wx.ID_CANCEL:
            return wx.ID_CANCEL
                
        self.Bind(wx.EVT_CLOSE, None)
        self.config.size = self.GetSizeTuple()
        self.config.position = self.GetPositionTuple()
        self.Close()
        return None
        
        
    def OnCmdUndo(self, event):
        self.editCtrl.Undo()
        
        
    def OnCmdRedo(self, event):
        self.editCtrl.Redo()
        
        
    def OnCmdCut(self, event):
        self.editCtrl.Cut()
        
        
    def OnCmdCopy(self, event):
        self.editCtrl.Copy()
        
        
    def OnCmdPaste(self, event):
        self.editCtrl.Paste()
        
        
    def OnCmdDelete(self, event):
        self.editCtrl.Delete()
        
        
    def OnCmdSelectAll(self, event):
        self.editCtrl.SelectAll()
        
        
    def _FileSave(self):
        self.UndoHandler(self.actionItem, self.editCtrl.GetText())
        self.editCtrl.SetSavePoint()
        
        
    def OnCmdEditLinks(self, event):
        dialog = EditLinksDialog(self)
        dialog.ShowModal()
        dialog.Destroy()
        
    
    def OnCmdExecute(self, event):
        self.actionItem.Execute()
        
        
    class UndoHandler:
        def __init__(self, item, text):
            self.name = "Edit PythonScript"
            self.positionData = item.GetPositionData()
            self.oldText = item.args[0]
            item.SetParams(text)
            item.document.AppendUndoHandler(self)


        def Undo(self, document):
            item = self.positionData.GetItem()
            if item in item.executable.openEditFrames:
                id = item.executable.openEditFrames[item]
                win = wx.FindWindowById(id, None)
                if win is not None:
                    win.editCtrl.SetText(self.oldText)
                    win.editCtrl.SetSavePoint()
            tmp = item.args[0]
            item.SetParams(self.oldText)
            self.oldText = tmp


        Redo = Undo
        

#------------------------------------------------------------------------
# Action: PythonScript
#------------------------------------------------------------------------
class PythonScript(eg.ActionClass):
    name = "Python Script"
    description = "Full featured Python script." 
    iconFile = "icons/PythonScript"

    def __init__(self):
        class Defaults:
            size = (400, 300)
            position = (10, 10)
        self.config = eg.GetConfig("plugins.EventGhost.PythonScript", Defaults)
        self.openEditFrames = {}

        
    def GetLabel(self, pythonstring=None):
        return self.name


    def Configure(self, *args):
#        actionItem = eg.currentConfigureItem
#        win = ScriptEditor(actionItem.document.frame, -1, actionItem, self)
#        actionItem.openConfigDialog = win
#        win.Raise()
#        gr1 = eg.Greenlet.getcurrent()
#        self.result = gr1.parent.switch()
        wx.CallAfter(self.OnOpen, eg.currentConfigureItem)
        return None


    def OnOpen(self, actionItem):
        if actionItem not in self.openEditFrames:
            id = wx.NewId()
            self.openEditFrames[actionItem] = id
        else:
            id = self.openEditFrames[actionItem]
        win = wx.FindWindowById(id, None)
        if win is None:
            id = wx.NewId()
            self.openEditFrames[actionItem] = id
            win = ScriptEditor(eg.document.frame, id, actionItem, self)
        else:
            win.Show()
        win.Raise()
        
        
    class Compile:
        idCounter = 0
        scriptDict = weakref.WeakValueDictionary()

        def __init__(self, text=""):
            id = self.__class__.idCounter
            self.__class__.idCounter += 1
            mod = imp.new_module(str(id))
            self.mod = mod
            mod.eg = eg
            self.text = text
            try:
                self.code = compile(text + "\n", str(id), "exec")
            except:
                eg.PrintError("Error compiling script.")
                self.PrintTraceback()
            self.scriptDict[id] = self
            
            
        def __call__(self):
            mod = self.mod
            old_result = eg.result
            mod.result = old_result
            try:
                exec(self.code, mod.__dict__)
            except SystemExit:
                pass
            except:
                self.PrintTraceback()
            if eg.result is not old_result:
                return eg.result
            else:
                return mod.result


        def PrintTraceback(self):
            eg.PrintError("Traceback (most recent call last):")
            lines = self.text.splitlines()
            tb_type, tb_value, tb_traceback = sys.exc_info() 
            for entry in traceback.extract_tb(tb_traceback)[1:]:
                file, linenum, func, source = entry
                try:
                    filenum = int(file)
                except:
                    filenum = None
                if source is None and filenum is not None:
                    eg.PrintError(
                        '  Python script "%s", line %d, in %s' % (
                            file, linenum, func
                        )
                    )
                    lines = self.scriptDict[int(file)].text.splitlines()
                    eg.PrintError('    ' + lines[linenum-1].lstrip())
                else:
                    eg.PrintError(
                        '  File "%s", line %d, in %s' % (
                            file, linenum, func
                        )
                    )
                    if source is not None:
                        eg.PrintError('    ' + source.lstrip())
            name = tb_type if type(tb_type) == type("") else tb_type.__name__
            eg.PrintError(str(name) + ': ' + str(tb_value))
                
            
        @eg.LogIt
        def __del__(self):
            pass
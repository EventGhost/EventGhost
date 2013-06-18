import sys
import os
import imp
import traceback
import inspect

import wx

import eg
from eg.IconTools import GetWxIconFromFile
from eg.Controls.PythonEditorCtrl import PythonEditorCtrl
       
class Text:
    title = "Python-Editor - %s"
    class SaveChanges:
        title = "Apply changes?"
        mesg = "The file was altered.\n\nDo you want to apply the changes?\n"

Text = eg.GetTranslation(Text)


class PythonEditorFrame(wx.Frame):
    
    def __init__(
        self, 
        parent=None, 
        id=-1, 
        text=None, 
        filename=None, 
        fileTitle=None, 
        config=None
    ):
        self.config = config
        if filename is None:
            self.editFile = ""
        else:
            self.editFile = filename
        if fileTitle is None:
            fileTitle == self.editFile
        wx.Frame.__init__(
            self, 
            parent, 
            id,
            eg.APP_NAME + " " + (Text.title % fileTitle),
            pos=config.position,
            size=config.size,
            style=wx.DEFAULT_FRAME_STYLE
        )
        self.SetIcon(
            GetWxIconFromFile(
                os.path.join(
                    os.path.abspath(os.path.split(__file__)[0]),
                    "PythonScript.png"
                )
            )
        )
        self.editCtrl = editCtrl = PythonEditorCtrl(self)
        if filename is not None:
            self.editFile = eg.config.ConfigFilePath
            text = open(self.editFile).read()
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


    def _FileSave(self):
        fd = file(self.editFile, "w+")
        fd.write(self.editCtrl.GetText())
        fd.close()
        self.editCtrl.SetSavePoint()


    def CheckFileNeedsSave(self):
        if (self.editFile is None) or (self.editCtrl.GetModify()):
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
        
    
        
class ScriptEditor(PythonEditorFrame):
    
    def __init__(self, parent, id, actionItem, action):
        if len(actionItem.args) < 1:
            actionItem.args = ['']
        PythonEditorFrame.__init__(
            self, 
            parent, 
            id,
            actionItem.args[0],
            fileTitle=actionItem.GetLabel(),
            config = action.config
        )
        self.actionItem = actionItem


    def _FileSave(self):
        self.UndoHandler(self.actionItem, self.editCtrl.GetText())
        self.editCtrl.SetSavePoint()
        
        
    def OnCmdExecute(self, event):
        self.actionItem.Execute()
        
        
    class UndoHandler:
        def __init__(self, item, text):
            self.name = "Edit PythonScript"
            self.positioner = item.GetPositioner()
            self.oldText = item.args[0]
            item.SetParams(text)
            item.document.AppendUndoHandler(self)


        def Undo(self, document):
            parent, pos = self.positioner()
            item = parent.childs[pos]
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
        

gScriptIdCounter = 0

def GetNewId():
    global gScriptIdCounter
    gScriptIdCounter += 1
    return gScriptIdCounter

import weakref
gScriptDict = weakref.WeakValueDictionary()

#------------------------------------------------------------------------
# Action: PythonScript
#------------------------------------------------------------------------
class PythonScript(eg.ActionClass):
    name = "Python Script"
    description = "Full featured Python script." 
    iconFile = "PythonScript"

    def __init__(self):
        class Default:
            size = (400, 300)
            position = (10, 10)
        self.config = eg.GetConfig("plugins.EventGhost.PythonScript", Default)
        self.openEditFrames = {}

        
    def GetLabel(self, pythonstring=None):
        return self.name


    def Configure(self, *args):
        wx.CallAfter(self.OnOpen, eg.currentConfigureItem)
        return args


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
            win = ScriptEditor(eg.mainFrame, id, actionItem, self)
        else:
            win.Show()
        win.Raise()
        
        
    class Compile:
        
        def __init__(self, text):
            id = GetNewId()
            mod = imp.new_module(str(id))
            self.mod = mod
            mod.eg = eg
            self.text = text
            try:
                self.code = compile(text + "\n", str(id), "exec")
            except:
                eg.PrintError("Error compiling script.")
                self.PrintTraceback()
            gScriptDict[id] = self
            
            
        def __call__(self):
            mod = self.mod
            old_result = eg.result
            mod.result = old_result
            try:
                exec self.code in mod.__dict__
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
                    lines = gScriptDict[int(file)].text.splitlines()
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
                
            
        def __del__(self):
            eg.whoami()
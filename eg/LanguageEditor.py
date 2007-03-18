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

import wx
import types
import os
import sys

def Start():
    print "lang"
    import Init
    global eg
    eg = Init.EventGhost()
    eg.Init(0)
    
    global OpenPlugin
    from PluginTools import OpenPlugin
    
    global languageNames
    from LanguageTools import languageNames

    LanguageEditor(None)
    eg.app.MainLoop()



class UnassignedValue:
    pass



def ExpandKeyname(key):
    last = key[0].upper()
    tmp = ""
    lastWasUpper = key[0].isupper()
    for c in key[1:]:
        cIsUpper = c.isupper()
        if lastWasUpper:
            if cIsUpper:
                tmp += last
            else:
                tmp += " " + last
        else:
            if cIsUpper:
                tmp += last + " "
            else:
                tmp += last
        last = c
        lastWasUpper = cIsUpper
    return (tmp + last).lstrip()


def ExpandKeyname(key):
    return key


class Text:
    class Menu:
        FileMenu = "&File"
        New = "&New"
        Open = "&Open..."
        Save = "&Save"
        Exit = "E&xit"
        
        EditMenu = "&Edit"
        Undo = "&Undo"
        Redo = "&Redo"
        Cut = "Cu&t"
        Copy = "&Copy"
        Paste = "&Paste"
        Delete = "&Delete"
        SelectAll = "Select &All"
        FindNext = "Find &Next Untranslated"
        
        About = "About Language Editor..."
        
        
        
class LanguageEditor(wx.Frame):
    
    def __init__(self, parent):
        global eg
        class DefaultConfig:
            position = (50, 50)
            size = (700, 433)
            splitPosition = 244
            language = None

        config = eg.GetConfig("languageEditor", DefaultConfig)
        if config.language is None:
            config.language = eg.config.language

        wx.Frame.__init__(
            self, 
            parent, 
            -1, 
            "Language Editor", 
            pos = config.position, 
            size = config.size
        )

        # menu creation
        menuBar = eg.MenuBar(self, Text.Menu)

        # file menu
        fileMenu = menuBar.AddMenu("File")
        AddItem = fileMenu.AddItem
        AddItem("Open", hotkey="Ctrl+O")
        AddItem("Save", hotkey="Ctrl+S")
        AddItem()
        AddItem("Exit", hotkey="Alt+F4")

        # edit menu        
        editMenu = menuBar.AddMenu("Edit")
        AddItem = editMenu.AddItem
        AddItem("Undo", False, hotkey="Ctrl+Z")
        AddItem("Redo", False, hotkey="Ctrl+Y")
        AddItem()
        AddItem("Cut", hotkey="Ctrl+X")
        AddItem("Copy", hotkey="Ctrl+C")
        AddItem("Paste", hotkey="Ctrl+V")
        AddItem("Delete")        
        AddItem()
        AddItem("FindNext", hotkey="F3")  

        # help menu
        helpMenu = menuBar.AddMenu("Help")
        AddItem = helpMenu.AddItem
        AddItem("About")  
        
        menuBar.Realize()
        
        statusBar = wx.StatusBar(self)
        self.SetStatusBar(statusBar)
        
        splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE)
        
        imageList = wx.ImageList(16, 16)
        for pathName in (
            "plugins//EventGhost//DisableItem.png", 
            "plugins//EventGhost//EnableItem.png", 
            "images//folder.png", 
            "images//root.png", 
            "images//new.png", 
        ):
            imageList.Add(
                wx.BitmapFromImage(wx.Image(pathName, wx.BITMAP_TYPE_PNG))
            )

        tree = wx.TreeCtrl(splitter, -1, style=wx.TR_HAS_BUTTONS)
        tree.AssignImageList(imageList)
        rootId = tree.AddRoot("Language Strings", 3)
        tree.SetPyData(rootId, ["", None, None])
        
        import CheckUpdate
        import eg.Dialogs.AboutDialog
        import eg.Dialogs.AddActionDialog
        import eg.Dialogs.AddPluginDialog
        import eg.Dialogs.OptionsDialog
        import eg.Dialogs.FindDialog
        #import MainFrame
        from ActionThread import CORE_PLUGINS
        
#        for pluginIdent in CORE_PLUGINS:
#            plugin = eg.OpenPlugin(pluginIdent, pluginIdent, ())
#            plugin.info.isStarted = True
        for plugin in os.listdir("Plugins"):
            if not plugin.startswith("."):
                OpenPlugin(plugin, plugin, ())
        
        rightPanel = wx.Panel(splitter)
        disabledColour = rightPanel.GetBackgroundColour()
        sizer = wx.BoxSizer(wx.VERTICAL)
                
        langKeys = sorted(languageNames, key=languageNames.get)
        langNames = [languageNames[k] for k in langKeys]
            
        languageList = ["en_EN"]
        for item in os.listdir("Languages"):
            name, ext = os.path.splitext(item)
            if ext == ".py" and languageNames.has_key(name):
                x = langKeys.index(name)
#                languageChoiceCtrl.SetString(
#                    x,
#                    "[" + langNames[x] + "]"
#                )
        try:
            x = langKeys.index(self.config.language)
        except:
            x = 0

        staticBoxSizer = wx.StaticBoxSizer(
            wx.StaticBox(rightPanel, label="Original Text"),
            wx.VERTICAL
        )
        currentValueCtrl = wx.TextCtrl(
            rightPanel, 
            style = wx.TE_MULTILINE|wx.TE_READONLY
        )
        enabledColour = currentValueCtrl.GetBackgroundColour()
        currentValueCtrl.SetBackgroundColour(disabledColour)
        currentValueCtrl.SetEditable(False)
        staticBoxSizer.Add(currentValueCtrl, 1, wx.EXPAND)
        sizer.Add(staticBoxSizer, 1, wx.EXPAND|wx.ALL, 5)

        sizer.Add((5,5))
        staticBoxSizer = wx.StaticBoxSizer(
            wx.StaticBox(rightPanel, label="Translated Text"),
            wx.VERTICAL
        )
        newValueCtrl = wx.TextCtrl(rightPanel, style=wx.TE_MULTILINE)
        staticBoxSizer.Add(newValueCtrl, 1, wx.EXPAND)
        sizer.Add(staticBoxSizer, 1, wx.EXPAND|wx.ALL, 5)
        
        rightPanel.SetSizer(sizer)        
        
        splitter.SplitVertically(tree, rightPanel)
        splitter.SetMinimumPaneSize(120)
        splitter.SetSashGravity(0.0)
        splitter.SetSashPosition(config.splitPosition) #width + 20)
        
        self.isDirty = False
        self.config = config
        self.langKeys = langKeys
        self.langNames = langNames
        self.tree = tree
        self.menuBar = menuBar
        self.rootId = rootId
        self.newValueCtrl = newValueCtrl
        self.currentValueCtrl = currentValueCtrl
        self.disabledColour = disabledColour
        self.enabledColour = enabledColour
        
        newValueCtrl.Bind(wx.EVT_TEXT, self.OnTextChange)
        tree.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnSelectionChanging)
        tree.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnItemCollapsing)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_MENU_OPEN, self.OnValidateMenus)
        
        self.LoadLanguage(self.config.language)
        self.Show()
        
        
    def OnCmdOpen(self, event):
        if self.CheckNeedsSave():
            return
        dialog = wx.SingleChoiceDialog(
            self, 'Choose a language to edit', 'Choose a language',
            self.langNames, 
            wx.CHOICEDLG_STYLE
        )
        try:
            x = self.langKeys.index(self.language)
        except:
            x = 0
        dialog.SetSelection(x)
        if dialog.ShowModal() == wx.ID_OK:
            self.LoadLanguage(self.langKeys[dialog.GetSelection()])
        dialog.Destroy()

        
    def OnCmdAbout(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "EventGhost Language Editor"
        info.Version = "1.0.0"
        info.Copyright = "(C) 2006 EventGhost Project"
        info.Developers = ["Bitmonster",]
        info.WebSite = ("http://www.eventghost.org", "EventGhost home page")
        wx.AboutBox(info)
        
        
    def LoadLanguage(self, language):
        self.config.language = language
        self.isDirty = False
        self.SetTitle(
            "EventGhost Language Editor - %s [%s]" % 
                (languageNames[language], language)
        )
        tree = self.tree
        tree.Unbind(wx.EVT_TREE_SEL_CHANGING)
        tree.DeleteChildren(self.rootId)
        translation = eg.Bunch()
        languagePath = "Languages\\%s.py" % language
        if os.path.exists(languagePath):
            execfile(languagePath, {}, translation.__dict__)
        self.translation = translation
        self.translationDict = translation.__dict__.copy()
        self.translationDict["__builtins__"] = {}
        
        for name in (
            "General",
            "MainFrame",
            "Error",
            "CheckUpdate",
            "AddActionDialog",
            "AddPluginDialog",
            "OptionsDialog",
            "FindDialog",
            "AboutDialog",
        ):
            newId = tree.AppendItem(self.rootId, name, 2)
            value = getattr(eg.text, name)
            tree.SetPyData(newId, [name, value, None])
            self.FillTree(newId, value, name)
            #tree.Expand(newId)
        
        plugins = [
            "EventGhost",
            "System",
            "Window",
            "Mouse",
        ]
        for name in dir(eg.text.Plugin):
            if name.startswith("__"):
                continue
            if name not in plugins:
                plugins.append(name)
            
        pluginId = tree.AppendItem(self.rootId, "Plugins", 2)
        tree.SetPyData(pluginId, ["Plugin", eg.text.Plugin, None])
        for name in plugins:
            newId = tree.AppendItem(pluginId, name, 2)
            value = getattr(eg.text.Plugin, name)
            evalPath = "Plugin." + name
            tree.SetPyData(newId, [evalPath, value, None])
            self.FillTree(newId, value, evalPath)
        
        tree.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnSelectionChanging)
        tree.Expand(self.rootId)
        tree.Expand(pluginId)      
        tree.ScrollTo(self.rootId)
        self.OnCmdFindNext(currentId=self.rootId)
        
        
    def OnCmdFindNext(self, event=None, currentId=None):
        tree = self.tree
        if currentId is None:
            currentId = tree.GetSelection()
        id = currentId
        found = False
        while not found:
            if not tree.ItemHasChildren(id):
                newId = tree.GetNextSibling(id)
                if newId.IsOk():
                    id = newId
                else:
                    while 1:
                        id = tree.GetItemParent(id)
                        if not id.IsOk():
                            print "unknown"
                            found = True
                            id = self.rootId
                            break
                        newId = tree.GetNextSibling(id)
                        if newId.IsOk():
                            id = newId
                            break
            while tree.ItemHasChildren(id):
                id, cookie = tree.GetFirstChild(id)
            if tree.GetItemImage(id) == 0:
                found = True
        tree.SelectItem(id)
        
    
    def OnTextChange(self, event):
        self.isDirty = True
    
        
    def CheckNeedsSave(self):
        if self.isDirty:
            dlg = wx.MessageDialog(
                self, 
                "Save Changes?", 
                "Save Changes?", 
                wx.YES_NO|wx.CANCEL|wx.ICON_QUESTION 
            )
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_CANCEL:
                return True
            if result == wx.ID_YES:
                self.OnCmdSave()
        return False
        
        
    def OnClose(self, event):
        if self.CheckNeedsSave():
            event.Veto()
            return
        self.config.position = self.GetPositionTuple()
        self.config.size = self.GetSizeTuple()
        self.config.splitPosition = self.tree.GetSizeTuple()[0]
        eg.SaveConfig()
        wx.GetApp().ExitMainLoop()
            
        
    def OnCmdSave(self, event=None):
        self.StoreEditField()
        tree = self.tree
        INDENT = "    "
        def Traverse(id, indent=0, isSequence=False):
            res = []
            Add = res.append
            item, cookie = tree.GetFirstChild(id)
            while item.IsOk():
                evalPath, value, transValue = tree.GetPyData(item)
                key = evalPath.split(".")[-1]
                if type(value) in (types.ClassType, types.InstanceType):
                    tmp = Traverse(item, indent+1)
                    if tmp != "":
                        Add(INDENT * indent + "class %s:\n" % key)
                        Add(tmp)
                elif type(value) == types.ListType:
                    tmp = Traverse(item, indent+1, True)
                    if tmp != "":
                        Add(INDENT * indent + key + " = [\n")
                        Add(tmp)
                        Add(INDENT * indent + "]\n")
                elif type(value) == types.TupleType:
                    tmp = Traverse(item, indent+1, True)
                    if tmp != "":
                        Add(INDENT * indent + key + " = (\n")
                        Add(tmp)
                        Add(INDENT * indent + ")\n")
                elif isSequence:
                    if transValue is UnassignedValue:
                        return ""
                    if type(transValue) == type(""):
                        transValue = transValue.decode("latin-1")
                    Add(INDENT * indent + repr(unicode(transValue)) + ",\n")
                elif transValue is not UnassignedValue and transValue != "":
                    #if type(transValue) == type(u""):
                    #    transValue = transValue.decode("latin-1")
                    Add(INDENT * indent + key + " = " + repr(unicode(transValue)) + "\n")
                item, cookie = tree.GetNextChild(id, cookie)
            return "".join(res)
        
        fd = open("Languages\\%s.py" % self.config.language, "w")
        fd.write("# -*- coding: UTF-8 -*-\n")
        fd.write(Traverse(tree.GetRootItem()))
        fd.close()
        self.isDirty = False
        
        
    def OnItemCollapsing(self, event):
        if event.GetItem() == self.rootId:
            event.Veto()


    def FillTree(self, id, node, evalPath=""):
        tree = self.tree
        firstItems = []
        valueItems = []
        groupItems = []
        for key in dir(node):
            if key.startswith("__"):
                continue
            if key == "name":
                value = node.__class__.__dict__[key]
                firstItems.append((key, value))
            elif key == "description":
                try:
                    value = node.__class__.__dict__[key]
                except:
                    print node.__dict__
                    print "class has no:", key
                    raise
                firstItems.append((key, value))
            elif type(getattr(node, key)) in (types.ClassType, types.InstanceType):
                value = getattr(node, key)
                groupItems.append((key, value))
            else:
                try:
                    value = node.__class__.__dict__[key]
                except (KeyError, AttributeError):
                    print "no class item:", node, key
                    continue
                valueItems.append((key, value))
            
        firstItems.sort()
        firstItems.reverse()
        valueItems.sort()
        groupItems.sort()
        for key, value in firstItems + valueItems + groupItems:
            if evalPath == "":
                newEvalPath = key
            else:
                newEvalPath = evalPath + "." + key
            if type(value) in (types.ClassType, types.InstanceType):
                newId = tree.AppendItem(id, ExpandKeyname(key), 2)
                value = getattr(node, key)
                tree.SetPyData(newId, [newEvalPath, value, None])
                self.FillTree(newId, value, newEvalPath)
                #tree.Expand(newId)
            elif type(value) in (types.TupleType, types.ListType):
                newId = tree.AppendItem(id, ExpandKeyname(key), 4)
                for i, item in enumerate(value):
                    tmp = newEvalPath + "[%i]" % i
                    try:
                        transValue = eval(tmp, self.translationDict)
                        icon = 1
                    except (AttributeError, NameError):
                        transValue = UnassignedValue
                        icon = 0
                    tmpId = tree.AppendItem(newId, "[%i]" % i, icon)
                    tree.SetPyData(tmpId, [tmp, item, transValue])
                tree.SetPyData(newId, [newEvalPath, value, None])
                #tree.Expand(newId)
            else:
                try:
                    transValue = eval(newEvalPath, self.translationDict)
                    icon = 1
                except (AttributeError, NameError):
                    transValue = UnassignedValue
                    icon = 0
                newId = tree.AppendItem(id, ExpandKeyname(key), icon)
                tree.SetPyData(newId, [newEvalPath, value, transValue])
                

    def StoreEditField(self):
        tree = self.tree
        newValueCtrl = self.newValueCtrl
        if newValueCtrl.IsModified():
            self.isDirty = True
            item = tree.GetSelection()
            text = newValueCtrl.GetValue()
            if text == "":
                tree.GetPyData(item)[2] = UnassignedValue
                tree.SetItemImage(item, 0)
            else:
                tree.GetPyData(item)[2] = newValueCtrl.GetValue()
                tree.SetItemImage(item, 1)
            newValueCtrl.SetModified(False)


    def OnSelectionChanging(self, event):
        self.StoreEditField()
                
        id = event.GetItem()
        if not id.IsOk():
            return
        tree = self.tree
        newValueCtrl = self.newValueCtrl
        evalPath, value, transValue = tree.GetPyData(id)
        self.SetStatusText(evalPath)

        if type(value) not in types.StringTypes:
            self.currentValueCtrl.SetValue("")
            newValueCtrl.ChangeValue("")
            newValueCtrl.Enable(False)
            newValueCtrl.SetBackgroundColour(self.disabledColour)
            return

        newValueCtrl.Enable(True)
        newValueCtrl.SetBackgroundColour(self.enabledColour)

        self.currentValueCtrl.SetValue(value)
        
        newValueCtrl.ChangeValue(
            transValue if transValue is not UnassignedValue else ""
        )
        
        
    def OnCmdExit(self, event):
        self.OnClose(None)
    
    
    def OnCmdUndo(self, event):
        self.newValueCtrl.Undo()
    
    
    def OnCmdRedo(self, event):
        self.newValueCtrl.Redo()
    
    
    def OnCmdCut(self, event):
        self.newValueCtrl.Cut()
    
    
    def OnCmdCopy(self, event):
        self.newValueCtrl.Copy()
    
    
    def OnCmdPaste(self, event):
        self.newValueCtrl.Paste()
    
    
    def OnCmdDelete(self, event):
        self.newValueCtrl.Clear()
    
    
    def OnValidateMenus(self, event):    
        self.menuBar.File.Save.Enable(self.isDirty)
        newValueCtrl = self.newValueCtrl
        editMenu = self.menuBar.Edit
        if self.FindFocus() == newValueCtrl:
            editMenu.Undo.Enable(newValueCtrl.CanUndo())
            editMenu.Redo.Enable(newValueCtrl.CanRedo())
            editMenu.Cut.Enable(newValueCtrl.CanCut())
            editMenu.Copy.Enable(newValueCtrl.CanCopy())
            editMenu.Paste.Enable(newValueCtrl.CanPaste())
            editMenu.Delete.Enable(True)
        else:
            editMenu.Undo.Enable(False)
            editMenu.Redo.Enable(False)
            editMenu.Cut.Enable(False)
            editMenu.Copy.Enable(False)
            editMenu.Paste.Enable(False)
            editMenu.Delete.Enable(False)
            
            
            
            

# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2018 EventGhost Project <http://www.eventghost.net/>
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

import os
import types
import wx
from os.path import join
from wx.combo import BitmapComboBox
from PIL import Image
# Local imports
import eg
from . import Translation


class Config(eg.PersistentData):
    position = (50, 50)
    size = (700, 433)
    splitPosition = 244
    language = None


class LanguageEditor(wx.Frame):
    def __init__(self, parent=None):
        self.translationDict = None

        countries = Translation.countries
        for cntry in countries:
            for lng in cntry.wx_languages:
                if lng.iso_code == Config.language:
                    Config.language = lng
                    break
            else:
                continue

            break
        else:
            for cntry in countries:
                for lng in cntry.wx_languages:
                    if lng.iso_code == 'en_US':
                        Config.language = lng
                        break
                else:
                    continue
                break

        if Config.language is None:
            Config.language = eg.config.language

        wx.Frame.__init__(
            self,
            parent,
            -1,
            "Language Editor",
            pos = Config.position,
            size = Config.size
        )

        self.plugins = []
        self.loaded_plugins = []

        eg.Init.ImportAll()
        eg.actionThread.Start()

        def LoadPlugins():

            if eg.localPluginDir != eg.corePluginDir:
                plugin_folders = (
                    os.listdir(eg.corePluginDir) +
                    os.listdir(eg.localPluginDir)
                )
            else:
                plugin_folders = os.listdir(eg.corePluginDir)

            for plugin_folder in plugin_folders:
                if not plugin_folder.startswith("."):
                    try:
                        plugin = eg.pluginManager.OpenPlugin(
                            plugin_folder,
                            plugin_folder,
                            ()
                        )

                        if plugin.pluginCls.__name__ in [
                            "EventGhost",
                            "System",
                            "Window",
                            "Mouse"
                        ]:
                            plugin.load_language_file(Config.language)
                            self.loaded_plugins += [plugin]

                        self.plugins += [plugin]

                    except eg.Exceptions.PluginLoadError:
                        import traceback
                        traceback.print_exc()

        eg.actionThread.CallWait(LoadPlugins)

        self.menuBar = self.CreateMenuBar()
        self.CreateStatusBar()

        splitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE)

        imageList = wx.ImageList(16, 16)
        for pathName in (
            join(eg.corePluginDir, "EventGhost", "icons", "DisableItem.png"),
            join(eg.corePluginDir, "EventGhost", "icons", "EnableItem.png"),
            join(eg.imagesDir, "folder.png"),
            join(eg.imagesDir, "root.png"),
            join(eg.imagesDir, "new.png"),
        ):
            imageList.Add(
                wx.BitmapFromImage(wx.Image(pathName, wx.BITMAP_TYPE_PNG))
            )

        self.tree = tree = wx.TreeCtrl(splitter, -1, style=wx.TR_HAS_BUTTONS)
        tree.AssignImageList(imageList)
        self.rootId = tree.AddRoot("Language Strings", 3)
        tree.SetPyData(self.rootId, ["", None, None])

        rightPanel = wx.Panel(splitter)
        self.disabledColour = rightPanel.GetBackgroundColour()

        self.languages = []

        for country in countries:
            self.languages.extend(country.wx_languages)

        self.currentValueCtrl = wx.TextCtrl(
            rightPanel,
            style = wx.TE_MULTILINE | wx.TE_READONLY
        )
        self.enabledColour = self.currentValueCtrl.GetBackgroundColour()
        self.currentValueCtrl.SetBackgroundColour(self.disabledColour)
        self.currentValueCtrl.SetEditable(False)

        self.newValueCtrl = wx.TextCtrl(rightPanel, style=wx.TE_MULTILINE)

        staticBoxSizer1 = wx.StaticBoxSizer(
            wx.StaticBox(rightPanel, label="Original Text"),
            wx.VERTICAL
        )
        staticBoxSizer1.Add(self.currentValueCtrl, 1, wx.EXPAND)
        staticBoxSizer2 = wx.StaticBoxSizer(
            wx.StaticBox(rightPanel, label="Translated Text"),
            wx.VERTICAL
        )
        staticBoxSizer2.Add(self.newValueCtrl, 1, wx.EXPAND)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(staticBoxSizer1, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add((5, 5))
        sizer.Add(staticBoxSizer2, 1, wx.EXPAND | wx.ALL, 5)
        rightPanel.SetSizer(sizer)

        splitter.SplitVertically(tree, rightPanel)
        splitter.SetMinimumPaneSize(120)
        splitter.SetSashGravity(0.0)
        splitter.SetSashPosition(Config.splitPosition)  #width + 20)

        self.isDirty = False

        self.newValueCtrl.Bind(wx.EVT_TEXT, self.OnTextChange)
        tree.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnSelectionChanging)
        tree.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnItemCollapsing)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_MENU_OPEN, self.OnValidateMenus)

        self.LoadLanguage(Config.language)
        self.Show()

    def CheckNeedsSave(self):
        if self.isDirty:
            dlg = wx.MessageDialog(
                self,
                "Save Changes?",
                "Save Changes?",
                wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION
            )
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_CANCEL:
                return True
            if result == wx.ID_YES:
                self.OnCmdSave()
        return False

    def CreateMenuBar(self):
        # menu creation
        menuBar = wx.MenuBar()

        def AddMenuItem(name, func, itemId):
            menu.Append(itemId, name)
            self.Bind(wx.EVT_MENU, func, id=itemId)

        # file menu

        self.open_plugin_id = wx.NewId()

        menu = wx.Menu()
        menuBar.Append(menu, "&File")
        AddMenuItem("&Open...\tCtrl+O", self.OnCmdOpen, wx.ID_OPEN)
        AddMenuItem("Open Plugin...", self.OnCmdOpenPlugin, self.open_plugin_id)
        AddMenuItem("&Save\tCtrl+S", self.OnCmdSave, wx.ID_SAVE)
        menu.AppendSeparator()
        AddMenuItem("E&xit\tAlt+F4", self.OnCmdExit, wx.ID_EXIT)

        # edit menu
        menu = wx.Menu()
        menuBar.Append(menu, "&Edit")
        AddMenuItem("&Undo\tCtrl+Z", self.OnCmdUndo, wx.ID_UNDO)
        AddMenuItem("&Redo\tCtrl+Y", self.OnCmdRedo, wx.ID_REDO)
        menu.AppendSeparator()
        AddMenuItem("Cu&t\tCtrl+X", self.OnCmdCut, wx.ID_CUT)
        AddMenuItem("&Copy\tCtrl+C", self.OnCmdCopy, wx.ID_COPY)
        AddMenuItem("&Paste\tCtrl+V", self.OnCmdPaste, wx.ID_PASTE)
        AddMenuItem("&Delete", self.OnCmdDelete, wx.ID_DELETE)
        menu.AppendSeparator()
        AddMenuItem(
            "Find &Next Untranslated\tF3", self.OnCmdFindNext, wx.ID_FIND
        )

        # help menu
        menu = wx.Menu()
        menuBar.Append(menu, "&Help")
        AddMenuItem("About Language Editor...", self.OnCmdAbout, wx.ID_ABOUT)

        self.SetMenuBar(menuBar)
        return menuBar

    def FillTree(self, treeId, node, evalPath=""):
        tree = self.tree
        for key, value in self.SortItems(node):
            if evalPath == "":
                newEvalPath = key
            else:
                newEvalPath = evalPath + "." + key

            if type(value) in (types.ClassType, types.InstanceType):
                newId = tree.AppendItem(treeId, ExpandKeyname(key), 2)
                value = getattr(node, key)
                tree.SetPyData(newId, [newEvalPath, value, None])
                self.FillTree(newId, value, newEvalPath)
                #tree.Expand(newId)

            elif type(value) in (types.TupleType, types.ListType):
                newId = tree.AppendItem(treeId, ExpandKeyname(key), 4)
                for i, item in enumerate(value):
                    tmp = newEvalPath + "[%i]" % i
                    try:
                        transValue = eval(tmp, self.translationDict)
                        icon = 1
                    except (AttributeError, NameError, IndexError):
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
                newId = tree.AppendItem(treeId, ExpandKeyname(key), icon)
                tree.SetPyData(newId, [newEvalPath, value, transValue])

    def LoadLanguage(self, language):
        Config.language = language
        self.isDirty = False
        self.SetTitle(
            "EventGhost Language Editor - %s [%s]" %
            (language.label, language.iso_code)
        )
        tree = self.tree
        tree.Unbind(wx.EVT_TREE_SEL_CHANGING)
        tree.DeleteChildren(self.rootId)

        translation = language.load()

        self.translationDict = translation.__dict__
        self.translationDict["__builtins__"] = {}

        for name in (
            "General",
            "MainFrame",
            "Error",
            "Exceptions",
            "CheckUpdate",
            "AddActionDialog",
            "AddPluginDialog",
            "AddActionGroupDialog",
            "EventItem",
            "OptionsDialog",
            "FindDialog",
            "AboutDialog",
            "WinUsb",
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

    def OnClose(self, event):
        if self.CheckNeedsSave():
            event.Veto()
            return

        for plugin in self.plugins:
            plugin.Close()

        Config.position = self.GetPositionTuple()
        Config.size = self.GetSizeTuple()
        Config.splitPosition = self.tree.GetSizeTuple()[0]

        language = Config.language
        Config.language = language.iso_code
        eg.config.Save()
        eg.actionThread.Stop()
        wx.GetApp().ExitMainLoop()

    @staticmethod
    def OnCmdAbout(dummyEvent):
        info = wx.AboutDialogInfo()
        info.Name = "EventGhost Language Editor"
        info.Version = "1.0.2"
        info.Copyright = "© 2005-2016 EventGhost Project"
        info.Developers = ["Bitmonster", ]
        info.WebSite = ("http://www.eventghost.net", "EventGhost home page")
        wx.AboutBox(info)

    def OnCmdCopy(self, dummyEvent):
        self.newValueCtrl.Copy()

    def OnCmdCut(self, dummyEvent):
        self.newValueCtrl.Cut()

    def OnCmdDelete(self, dummyEvent):
        self.newValueCtrl.Clear()

    def OnCmdExit(self, dummyEvent):
        self.OnClose(None)

    def OnCmdFindNext(self, dummyEvent=None, currentId=None):
        tree = self.tree
        if currentId is None:
            currentId = tree.GetSelection()
        treeId = currentId
        found = False
        while not found:
            if not tree.ItemHasChildren(treeId):
                newId = tree.GetNextSibling(treeId)
                if newId.IsOk():
                    treeId = newId
                else:
                    while 1:
                        treeId = tree.GetItemParent(treeId)
                        if not treeId.IsOk():
                            print "unknown"
                            found = True
                            treeId = self.rootId
                            break
                        newId = tree.GetNextSibling(treeId)
                        if newId.IsOk():
                            treeId = newId
                            break
            while tree.ItemHasChildren(treeId):
                treeId = tree.GetFirstChild(treeId)[0]
            if tree.GetItemImage(treeId) == 0:
                found = True
        tree.SelectItem(treeId)
        self.newValueCtrl.SetFocus()

    def OnCmdOpen(self, dummyEvent):
        if self.CheckNeedsSave():
            return

        dialog = wx.Dialog(self, -1, title='Choose Language')

        sizer = wx.BoxSizer(wx.VERTICAL)
        language_choice = BitmapComboBox(dialog, style=wx.CB_READONLY)

        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.Add(language_choice, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(h_sizer, 0, wx.EXPAND)
        sizer.AddStretchSpacer(1)

        button_sizer = dialog.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.AddStretchSpacer(1)
        h_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(h_sizer, 0, wx.EXPAND)
        dialog.SetSizer(sizer)

        for language in self.languages:
            language_choice.Append(language.label, language.flag)

        for i, language in enumerate(self.languages):
            if language.iso_code == Config.language.iso_code:
                language_choice.SetSelection(i)
                break
        else:
            language_choice.SetSelection(0)

        if dialog.ShowModal() == wx.ID_OK:
            self.LoadLanguage(self.languages[language_choice.GetSelection()])

        dialog.Destroy()

    def OnCmdOpenPlugin(self, dummyEvent):
        if self.CheckNeedsSave():
            return

        dialog = wx.Dialog(self, -1, title='Choose Plugin')

        sizer = wx.BoxSizer(wx.VERTICAL)
        plugin_choice = BitmapComboBox(dialog, style=wx.CB_READONLY)

        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.Add(plugin_choice, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(h_sizer, 0, wx.EXPAND)
        sizer.AddStretchSpacer(1)

        button_sizer = dialog.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.AddStretchSpacer(1)
        h_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(h_sizer, 0, wx.EXPAND)
        dialog.SetSizer(sizer)

        for plugin in self.plugins:
            if plugin in self.loaded_plugins:
                continue

            img = plugin.icon.pil.resize((24, 24), Image.ANTIALIAS)
            bmp = eg.Icons.PilToBitmap(img)

            plugin_choice.Append(
                    plugin.pluginName,
                    bmp
                )

        plugin_choice.SetSelection(0)

        if dialog.ShowModal() == wx.ID_OK:
            plugin_name = plugin_choice.GetStringSelection()

            for plugin in self.plugins:
                if plugin.pluginName == plugin_name:
                    self.loaded_plugins += [plugin]
                    plugin.load_language_file(Config.language)
                    self.LoadLanguage(Config.language)
                    break

        dialog.Destroy()

    def OnCmdPaste(self, dummyEvent):
        self.newValueCtrl.Paste()

    def OnCmdRedo(self, dummyEvent):
        self.newValueCtrl.Redo()

    def OnCmdSave(self, dummyEvent=None):
        self.StoreEditField()
        tree = self.tree

        def Traverse(treeId):
            cls = tree.GetPyData(treeId)[1]
            item, cookie = tree.GetFirstChild(treeId)

            while item.IsOk():
                evalPath, value, transValue = tree.GetPyData(item)

                key = evalPath.split(".")[-1]

                if type(value) in (types.ClassType, types.InstanceType):
                    Traverse(item)

                elif transValue != UnassignedValue and transValue:
                    cls.__dict__[key] = value
                else:
                    cls.__dict__[key] = value

                item, cookie = tree.GetNextChild(treeId, cookie)

        Traverse(self.rootId)
        Config.language.save()
        self.isDirty = False

    def OnCmdUndo(self, dummyEvent):
        self.newValueCtrl.Undo()

    def OnItemCollapsing(self, event):
        if event.GetItem() == self.rootId:
            event.Veto()

    def OnSelectionChanging(self, event):
        self.StoreEditField()

        treeId = event.GetItem()
        if not treeId.IsOk():
            return
        tree = self.tree
        newValueCtrl = self.newValueCtrl
        evalPath, value, transValue = tree.GetPyData(treeId)
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

    def OnTextChange(self, dummyEvent):
        self.isDirty = True

    def OnValidateMenus(self, dummyEvent):
        menuBar = self.menuBar
        menuBar.Enable(wx.ID_SAVE, self.isDirty)
        newValueCtrl = self.newValueCtrl
        if self.FindFocus() == newValueCtrl:
            menuBar.Enable(wx.ID_UNDO, newValueCtrl.CanUndo())
            menuBar.Enable(wx.ID_REDO, newValueCtrl.CanRedo())
            menuBar.Enable(wx.ID_CUT, newValueCtrl.CanCut())
            menuBar.Enable(wx.ID_COPY, newValueCtrl.CanCopy())
            menuBar.Enable(wx.ID_PASTE, newValueCtrl.CanPaste())
            menuBar.Enable(wx.ID_DELETE, True)
        else:
            menuBar.Enable(wx.ID_UNDO, False)
            menuBar.Enable(wx.ID_REDO, False)
            menuBar.Enable(wx.ID_CUT, False)
            menuBar.Enable(wx.ID_COPY, False)
            menuBar.Enable(wx.ID_PASTE, False)
            menuBar.Enable(wx.ID_DELETE, False)

    @staticmethod
    def SortItems(node):
        firstItems = []
        valueItems = []
        groupItems = []
        for key in dir(node):
            if key.startswith("__"):
                continue
            if key == "name":
                try:
                    value = node.__dict__[key]
                except KeyError:
                    print node.__dict__
                    print "class has no:", key
                    continue
                firstItems.append((key, value))
            elif key == "description":
                try:
                    value = node.__dict__[key]
                except KeyError:
                    print node.__dict__
                    print "class has no:", key
                    continue
                firstItems.append((key, value))
            elif type(getattr(node, key)) in (
                types.ClassType,
                types.InstanceType
            ):
                value = getattr(node, key)
                groupItems.append((key, value))
            else:
                try:
                    value = node.__dict__[key]
                except (KeyError, AttributeError):
                    print "no class item:", node, key
                    continue
                valueItems.append((key, value))

        firstItems.sort()
        firstItems.reverse()
        valueItems.sort()
        groupItems.sort()
        return firstItems + valueItems + groupItems

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


class UnassignedValue:
    pass


def ExpandKeyname(key):
    return key

def MyRepr(value):
    value = value.replace("\n", "\\n")
    if value.count("'") < value.count('"'):
        value = value.replace("'", "\\'")
        return "u'%s'" % value
    else:
        value = value.replace('"', '\\"')
        return 'u"%s"' % value

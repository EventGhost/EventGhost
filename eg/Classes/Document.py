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

import os
import wx
from tempfile import mkstemp
from threading import Lock
from types import ClassType
from xml.etree import cElementTree as ElementTree

# Local imports
import eg

class Document(object):
    def __init__(self):
        class ItemMixin:
            document = self
            root = None
        self.ItemMixin = ItemMixin
        itemNamespace = {}
        self.XMLTag2ClassDict = {}

        def MakeCls(name):
            baseCls = getattr(eg, name)
            cls = ClassType(name, (ItemMixin, baseCls), itemNamespace)
            self.XMLTag2ClassDict[cls.xmlTag.lower()] = cls
            return cls

        self.TreeLink = eg.TreeLink
#        self.TreeItem = MakeCls("TreeItem")
#        self.ContainerItem = MakeCls("ContainerItem")
        self.EventItem = MakeCls("EventItem")
        self.ActionItem = MakeCls("ActionItem")
        self.PluginItem = MakeCls("PluginItem")
        self.FolderItem = MakeCls("FolderItem")
        self.MacroItem = MakeCls("MacroItem")
        self.RootItem = MakeCls("RootItem")
        self.AutostartItem = MakeCls("AutostartItem")

        self.selection = None
        self.stockUndo = []
        self.stockRedo = []
        self.undoId = 0
        self.undoIdOnSave = 0
        self.undoState = (False, False, "", "")
        self.isDirty = False
        self.filePath = None
        self.root = None
        self.firstVisibleItem = None
        self.frame = None
        self.reentrantLock = Lock()
        self.expandedNodes = set()
        self.visibleLogItem = 0

    def AfterLoad(self):
        if (
            TreeStateData.guid == self.root.guid and
            TreeStateData.time == self.root.time
        ):
            self.SetExpandState(TreeStateData.expanded)
            self.selection = self.FindItemWithPath(TreeStateData.selection)
            self.firstVisibleItem = self.FindItemWithPath(
                TreeStateData.firstVisibleItem
            )
        else:
            self.selection = self.root
            self.firstVisibleItem = self.root

    @eg.LogIt
    def AppendUndoHandler(self, handler):
        stockUndo = self.stockUndo
        if len(stockUndo) >= 20:
            del stockUndo[0]
        stockUndo.append(handler)
        self.undoId += 1
        del self.stockRedo[:]
        self.SetIsDirty()
        self.SetUndoState((True, False, ": " + handler.name, ""))

    def AskFile(self, style):
        fileDialog = wx.FileDialog(
            self.frame,
            message="",
            wildcard="EventGhost Tree (*.egtree; *.xml)|*.egtree;*.xml",
            style=style
        )
        try:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return None
            return fileDialog.GetPath()
        finally:
            fileDialog.Destroy()

    @eg.LogItWithReturn
    def CheckFileNeedsSave(self):
        """
        Checks if the file was changed and if necessary asks the user if he
        wants to save it. If the user affirms, calls Save/SaveAs also.

        returns: wx.ID_OK     if no save was needed
                 wx.ID_YES    if file was saved
                 wx.ID_NO     if file was not saved
                 wx.ID_CANCEL if user canceled possible save
        """
        if not self.isDirty:
            return wx.ID_OK
        dialog = SaveChangesDialog(self.frame)
        result = dialog.ShowModal()
        dialog.Destroy()
        if result == wx.ID_CANCEL:
            return wx.ID_CANCEL
        elif result == wx.ID_YES:
            return self.Save()
        else:
            return wx.ID_NO

    def IsDirty(self):
        return self.isDirty

    @eg.LogItWithReturn
    def Close(self):
        try:
            eg.config.hideOnStartup = self.frame is None
            eg.config.autoloadFilePath = self.filePath
            if self.frame is not None:
                frame = self.frame
                self.frame = None
                frame.Destroy()
            TreeStateData.guid = self.root.guid
            TreeStateData.time = self.root.time
            TreeStateData.expanded = self.GetExpandState()
            TreeStateData.selection = self.selection.GetPath()
            TreeStateData.firstVisibleItem = self.firstVisibleItem.GetPath()
        except:
            eg.PrintTraceback()

    @eg.AssertInMainThread
    def CmdAddAction(self, selection=None, action=None):
        if selection is None:
            selection = self.selection
        if not selection.DropTest(eg.ActionItem):
            self.DisplayError("cantAddAction")
            return
        if action is None:
            # let the user choose an action
            result = eg.AddActionDialog.GetModalResult(self.frame)
            # if user canceled the dialog, take a quick exit
            if result is None:
                return
            action = result[0]
        return eg.UndoHandler.NewAction(self).Do(selection, action)

    @eg.AssertInMainThread
    def CmdAddEvent(self):
        if not self.selection.DropTest(eg.EventItem):
            self.DisplayError("cantAddEvent")
            return
        result = eg.AddEventDialog.GetResult(self.frame)
        if result is None:
           return
        return eg.UndoHandler.NewEvent(self).Do(
            self.selection,
            label=result[0]
        )

    @eg.AssertInMainThread
    def CmdAddFolder(self):
        folderNode = eg.UndoHandler.NewFolder(self).Do(self.selection)
        wx.CallAfter(self.frame.treeCtrl.EditNodeLabel, folderNode)

    @eg.AssertInMainThread
    def CmdAddMacro(self):
        return eg.UndoHandler.NewMacro(self).Do(self.selection)

    @eg.AssertInMainThread
    def CmdAddPlugin(self):
        result = eg.AddPluginDialog.GetModalResult(self.frame)
        if result:
            try:
                eg.UndoHandler.NewPlugin(self).Do(result[0])
            except eg.Exceptions.PluginLoadError:
                pass

    @eg.AssertInMainThread
    def CmdConfigure(self, item=None, isFirstConfigure=False):
        if item is None:
            item = self.selection
        if not item.isConfigurable:
            self.DisplayError("cantConfigure")
        else:
            return eg.UndoHandler.Configure(self).Do(item, isFirstConfigure)

    @eg.AssertInMainThread
    def CmdCopy(self):
        self.selection.OnCmdCopy()

    @eg.AssertInMainThread
    def CmdCut(self):
        eg.UndoHandler.Cut(self).Do(self.selection)

    @eg.AssertInMainThread
    def CmdDelete(self):
        eg.UndoHandler.Clear(self).Do(self.selection)

    @eg.AssertInMainThread
    def CmdExecute(self):
        if not self.selection.isExecutable:
            self.DisplayError("cantExecute")
        else:
            self.ExecuteNode(self.selection).SetShouldEnd()

    @eg.AssertInMainThread
    def CmdPaste(self):
        eg.UndoHandler.Paste(self).Do(self.selection)

    @eg.AssertInMainThread
    def CmdPython(self):
        self.selection.OnCmdPython()

    @eg.AssertInMainThread
    def CmdRename(self):
        if not self.selection.isRenameable:
            self.DisplayError("cantRename")
        else:
            self.frame.treeCtrl.EditNodeLabel(self.selection)

    @eg.AssertInMainThread
    def CmdToggleEnable(self):
        if not self.selection.isDeactivatable:
            self.DisplayError("cantDisable")
        else:
            eg.UndoHandler.ToggleEnable(self).Do(self.selection)

    @eg.AssertInMainThread
    def DisplayError(self, ident):
        self.frame.DisplayError(getattr(eg.text.MainFrame.Messages, ident))

    def ExecuteNode(self, node):
        event = eg.EventGhostEvent("OnCmdExecute")
        eg.actionThread.Call(eg.actionThread.ExecuteTreeItem, node, event)
        return event

    def FindItemWithPath(self, path):
        item = self.root
        if path is None:
            return item
        try:
            for pos in path:
                item = item.childs[pos]
        except IndexError:
            item = self.root
        return item

    @eg.LogIt
    def GetExpandState(self):
        expanded = set()
        add = expanded.add
        ContainerItem = eg.ContainerItem

        def Traverse(item, i):
            if isinstance(item, ContainerItem):
                i += 1
                if item in self.expandedNodes:
                    add(i)
                for child in item.childs:
                    i = Traverse(child, i)
            return i
        Traverse(self.root, -1)

        return expanded

    def GetTitle(self):
        if self.filePath is None:
            filename = eg.text.General.unnamedFile
        elif not self.filePath:
            filename = "Example"
        else:
            filename = os.path.splitext(os.path.basename(self.filePath))[0]
        return "EventGhost %s - %s" % (eg.Version.string, filename)

    @eg.LogItWithReturn
    def HideFrame(self):
        # NOTICE:
        # If the program is started through a shortcut with "minimize" option
        # set, we get an iconize event while ShowFrame() is executing.
        # Therefore we have to use this CallLater workaround.
        # TODO: Find a better way. Preferable detect the minimize option
        #       before we create the MainFrame.
        if self.reentrantLock.acquire(False):
            if self.frame is not None:
                if len(self.frame.openDialogs) == 0:
                    logCtrl = self.frame.logCtrl
                    if logCtrl.IsAutoscroll():
                        self.visibleLogItem = 0
                    else:
                        self.visibleLogItem = (
                            logCtrl.GetTopItem() + logCtrl.GetCountPerPage()
                        )

                        if self.visibleLogItem:
                            self.visibleLogItem -= 1

                    self.frame.Destroy()
                    self.frame = eg.mainFrame = None
            self.reentrantLock.release()
        else:
            wx.CallLater(100, self.HideFrame)

    @eg.LogIt
    def Load(self, filePath):
        if filePath is None:
            return self.LoadEmpty()
        self.ResetUndoState()
#        if self.root:
#            self.root.Delete()
        if not filePath:
            filePath = os.path.join(eg.mainDir, "Example.egtree")
            self.SetFilePath(False)
        else:
            self.SetFilePath(filePath)
        eg.TreeLink.StartLoad()
        xmlTree = ElementTree.parse(filePath)
        node = xmlTree.getroot()
        root = self.RootItem(self, node)
        self.ItemMixin.root = root
        self.root = root
        self.selection = root
        eg.TreeLink.StopLoad()
        self.SetIsDirty(False)
        self.AfterLoad()
        wx.CallAfter(eg.Notify, "DocumentNewRoot", root)
        return root

    @eg.LogIt
    def LoadEmpty(self):
        self.ResetUndoState()
#        if self.root:
#            self.root.Delete()
        self.SetFilePath(None)
        eg.TreeLink.StartLoad()
        node = ElementTree.Element("EventGhost")
        root = self.RootItem(self, node)
        self.root = root
        self.selection = root
        self.ItemMixin.root = root
        node = ElementTree.Element("Autostart")
        self.autostartMacro = self.AutostartItem(root, node)
        root.childs.append(self.autostartMacro)
        eg.TreeLink.StopLoad()
        self.SetIsDirty(False)
        wx.CallAfter(eg.Notify, "DocumentNewRoot", root)
        return root

    def New(self):
        if self.CheckFileNeedsSave() == wx.ID_CANCEL:
            return
        self.StartSession(None)

    def OnCmdConfigure(self, node):
        eg.AsTasklet(eg.UndoHandler.Configure(self).Do)(node)

    def Open(self, filePath=None):
        self.ShowFrame()
        if filePath is not None:
            res = wx.MessageBox(
                "Do you really want to load the tree file:\n%s" % filePath,
                eg.APP_NAME,
                wx.YES_NO | wx.CENTRE | wx.ICON_QUESTION,
                parent = self.frame,
            )
            if res == wx.ID_NO:
                return wx.ID_CANCEL
        if self.CheckFileNeedsSave() == wx.ID_CANCEL:
            return wx.ID_CANCEL
        if filePath is None:
            filePath = self.AskFile(wx.OPEN)
        if filePath is None:
            return wx.ID_CANCEL
        self.StartSession(filePath)

    @eg.AssertInMainThread
    @eg.LogIt
    def Redo(self):
        if len(self.stockRedo) == 0:
            return
        handler = self.stockRedo.pop()
        eg.actionThread.Func(handler.Redo)()
        self.undoId += 1
        self.SetIsDirty(self.undoId != self.undoIdOnSave)
        self.stockUndo.append(handler)
        if len(self.stockRedo):
            redoName = ": " + self.stockRedo[-1].name
            hasRedo = True
        else:
            redoName = ""
            hasRedo = False
        self.SetUndoState((True, hasRedo, ": " + handler.name, redoName))

    def ResetUndoState(self):
        del self.stockUndo[:]
        del self.stockRedo[:]
        self.undoId = 0
        self.undoIdOnSave = 0
        self.SetUndoState((False, False, "", ""))

    @eg.AssertInActionThread
    def RestoreItem(self, treePosition, xmlData):
        eg.TreeLink.StartUndo()
        parent, pos = treePosition.GetParentAndPosition()
        node = ElementTree.fromstring(xmlData)
        cls = self.XMLTag2ClassDict[node.tag.lower()]
        item = cls(parent, node)
        parent.AddChild(item, pos)
        eg.TreeLink.StopUndo()
        item.RestoreState()
        return item

    @eg.LogItWithReturn
    def Save(self):
        if not self.filePath:
            return self.SaveAs()
        self.WriteFile(self.filePath)
        return wx.ID_YES

    def SaveAs(self):
        filePath = self.AskFile(style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if filePath is None:
            return wx.ID_CANCEL
        self.WriteFile(filePath)
        self.SetFilePath(filePath)
        return wx.ID_YES

    @eg.LogIt
    def SetExpandState(self, expanded):
        if expanded is None:
            return
        self.expandedNodes.clear()
        ContainerItem = eg.ContainerItem

        def Traverse(item, i):
            if isinstance(item, ContainerItem):
                i += 1
                if i in expanded:
                    self.expandedNodes.add(item)
                for child in item.childs:
                    i = Traverse(child, i)
            return i
        Traverse(self.root, -1)

    def SetFilePath(self, filePath):
        self.filePath = filePath
        eg.Notify("DocumentFileChange", filePath)

    def SetIsDirty(self, flag=True):
        self.isDirty = flag
        eg.Notify("DocumentChange", flag)

    def SetUndoState(self, undoState):
        self.undoState = undoState
        eg.Notify("UndoChange", undoState)

    @eg.LogItWithReturn
    def ShowFrame(self):
        if self.reentrantLock.acquire(False):
            if self.frame is None:
                self.frame = eg.mainFrame = eg.MainFrame(self)
                self.frame.Show()
            else:
                self.frame.Iconize(False)
            self.reentrantLock.release()

    def StartSession(self, filePath):
        eg.eventThread.Func(eg.eventThread.StopSession)()
        eg.eventThread.Call(eg.eventThread.StartSession, filePath)

    @eg.AssertInMainThread
    def Undo(self):
        if len(self.stockUndo) == 0:
            return
        handler = self.stockUndo.pop()
        eg.actionThread.Func(handler.Undo)()
        self.undoId -= 1
        self.SetIsDirty(self.undoId != self.undoIdOnSave)
        self.stockRedo.append(handler)
        if len(self.stockUndo):
            undoName = ": " + self.stockUndo[-1].name
            hasUndo = True
        else:
            undoName = ""
            hasUndo = False
        self.SetUndoState((hasUndo, True, undoName, ": " + handler.name))

    def WriteFile(self, filePath):
        success = False
        tmpFile, tmpPath = mkstemp(".xml", "$", os.path.dirname(filePath))
        os.close(tmpFile)
        try:
            tmpFile = file(tmpPath, "wb+")
            tmpFile.write('<?xml version="1.0" encoding="UTF-8" ?>\r\n')
            self.root.WriteXmlString(tmpFile.write)
            tmpFile.close()
            try:
                os.remove(filePath)
            except:
                pass
            os.rename(tmpPath, filePath)
            self.SetIsDirty(False)
            self.undoIdOnSave = self.undoId
            success = True
        except:
            eg.PrintTraceback("Error while saving file")
        return success


class SaveChangesDialog(wx.Dialog):
    def __init__(self, parent=None):
        text = eg.text.MainFrame.SaveChanges
        wx.Dialog.__init__(self, parent, title=eg.APP_NAME)
        bmp = wx.ArtProvider.GetBitmap(
            wx.ART_WARNING, wx.ART_CMN_DIALOG, (32, 32)
        )
        staticBitmap = wx.StaticBitmap(self, -1, bmp)

        messageCtrl = wx.StaticText(
            self, -1, eg.text.MainFrame.SaveChanges.mesg
        )
        messageCtrl.Wrap(400)
        saveButton = wx.Button(self, wx.ID_YES, text.saveButton)
        saveButton.Bind(wx.EVT_BUTTON, self.OnButton)
        saveButton.SetDefault()
        saveButton.SetFocus()
        dontSaveButton = wx.Button(self, wx.ID_NO, text.dontSaveButton)
        dontSaveButton.Bind(wx.EVT_BUTTON, self.OnButton)
        cancelButton = wx.Button(self, wx.ID_CANCEL, eg.text.General.cancel)
        cancelButton.Bind(wx.EVT_BUTTON, self.OnButton)
        self.SetDefaultItem(saveButton)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(staticBitmap, 0, wx.ALL, 12)
        sizer.Add(messageCtrl, 0, wx.ALIGN_CENTER | wx.LEFT | wx.TOP | wx.RIGHT, 6)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add(saveButton, 0, wx.LEFT | wx.RIGHT, 3)
        buttonSizer.Add(dontSaveButton, 0, wx.LEFT | wx.RIGHT, 3)
        buttonSizer.Add(cancelButton, 0, wx.LEFT | wx.RIGHT, 3)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer)
        mainSizer.Add(buttonSizer, 0, wx.ALIGN_RIGHT | wx.ALL, 12)
        self.SetSizerAndFit(mainSizer)
        if parent:
            self.CenterOnParent()
        else:
            self.Center()

    def OnButton(self, event):
        buttonId = event.GetId()
        self.EndModal(buttonId)
        event.Skip()


class TreeStateData(eg.PersistentData):
    guid = None
    time = None
    expanded = None

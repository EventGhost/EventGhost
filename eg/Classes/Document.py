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
from types import ClassType
import os
from xml.etree import cElementTree as ElementTree
from tempfile import mkstemp
from threading import Lock


class TreeStateData(eg.PersistentData):
    guid = None
    time = None
    expandState = None # deprecated
    expanded = None



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

        self.stockUndo = []
        self.stockRedo = []
        self.lastUndoId = 0
        self.undoIdOnSave = 0
        eg.Notify("UndoChange", (False, False, "", ""))
        eg.Notify("DocumentChange", False)
        self.filePath = None
        self.root = None
        self.firstVisibleItem = None
        self.frame = None
        self.reentrantLock = Lock()
        self.expandedNodes = set()


    def SetFilePath(self, filePath):
        self.filePath = filePath
        eg.Notify("DocumentFileChange", filePath)


    def GetTitle(self):
        if self.filePath is None:
            filename = eg.text.General.unnamedFile
        elif not self.filePath:
            filename = "Example.xml"
        else:
            filename = os.path.splitext(os.path.basename(self.filePath))[0]
        return "EventGhost %s - %s" % (eg.Version.string, filename)


    def ResetUndoState(self):
        del self.stockUndo[:]
        del self.stockRedo[:]
        self.undoState = 0
        self.undoStateOnSave = 0
        eg.Notify("UndoChange", (False, False, "", ""))


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
        eg.Notify("DocumentChange", False)
        wx.CallAfter(eg.Notify, "DocumentNewRoot", root)
        return root


    @eg.LogIt
    def Load(self, filePath):
        if filePath is None:
            return self.LoadEmpty()
        self.ResetUndoState()
#        if self.root:
#            self.root.Delete()
        if not filePath:
            filePath = os.path.join(eg.mainDir, "Example.xml")
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
        eg.Notify("DocumentChange", False)
        self.AfterLoad()
        wx.CallAfter(eg.Notify, "DocumentNewRoot", root)
        return root


    def StartSession(self, filePath):
        eg.eventThread.CallWait(eg.eventThread.StopSession)
        eg.eventThread.Call(eg.eventThread.StartSession, filePath)


    def AfterLoad(self):
        if (
            TreeStateData.guid == self.root.guid
            and TreeStateData.time == self.root.time
        ):
            self.SetExpandState(TreeStateData.expanded)
            self.selection = self.FindItemWithPath(TreeStateData.selection)
            self.firstVisibleItem = self.FindItemWithPath(
                TreeStateData.firstVisibleItem
            )
        else:
            self.selection = self.root
            self.firstVisibleItem = self.root


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
            eg.Notify("DocumentChange", False)
            self.undoStateOnSave = self.undoState
            success = True
        except:
            eg.PrintTraceback("Error while saving file")
        return success


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


    @eg.LogIt
    def AppendUndoHandler(self, handler):
        stockUndo = self.stockUndo
        if len(stockUndo) >= 20:
            del stockUndo[0]
        stockUndo.append(handler)
        self.undoState += 1
        del self.stockRedo[:]
        eg.Notify("DocumentChange", True)
        eg.Notify("UndoChange", (True, False, ": " + handler.name, ""))


    def Undo(self):
        if len(self.stockUndo) == 0:
            return
        handler = self.stockUndo.pop()
        handler.Undo(self)
        self.undoState -= 1
        eg.Notify("DocumentChange", self.undoState != self.undoStateOnSave)
        self.stockRedo.append(handler)
        if len(self.stockUndo):
            undoName = ": " + self.stockUndo[-1].name
            hasUndo = True
        else:
            undoName = ""
            hasUndo = False
        eg.Notify("UndoChange", (hasUndo, True, undoName, ": " + handler.name))


    @eg.LogIt
    def Redo(self):
        if len(self.stockRedo) == 0:
            return
        handler = self.stockRedo.pop()
        handler.Redo(self)
        self.undoState += 1
        eg.Notify("DocumentChange", self.undoState != self.undoStateOnSave)
        self.stockUndo.append(handler)
        if len(self.stockRedo):
            redoName = ": " + self.stockRedo[-1].name
            hasRedo = True
        else:
            redoName = ""
            hasRedo = False
        eg.Notify("UndoChange", (True, hasRedo, ": " + handler.name, redoName))


    def RestoreItem(self, positionData, xmlData):
        eg.TreeLink.StartUndo()
        parent, pos = positionData.GetPosition()
        node = ElementTree.fromstring(xmlData)
        cls = self.XMLTag2ClassDict[node.tag.lower()]
        item = cls(parent, node)
        parent.AddChild(item, pos)
        eg.TreeLink.StopUndo()
        item.RestoreState()
        return item


    @eg.LogItWithReturn
    def ShowFrame(self):
        if self.reentrantLock.acquire(False):
            if self.frame is None:
                self.frame = eg.MainFrame(self)
                self.frame.Show()
            self.frame.Raise()
            self.reentrantLock.release()


    @eg.LogItWithReturn
    def HideFrame(self):
        # NOTICE:
        # If the program is started through a shortcut with "minimise" option
        # set, we get an iconize event while ShowFrame() is executing.
        # Therefore we have to use this CallLater workaround.
        # TODO: Find a better way. Preferable detect the minimise option
        #       before we create the MainFrame.
        if self.reentrantLock.acquire(False):
            if self.frame is not None:
                if len(self.frame.openDialogs) == 0:
                    self.frame.Destroy()
                    self.frame = None
            self.reentrantLock.release()
        else:
            wx.CallLater(100, self.HideFrame)


    def IsDirty(self):
        return eg.notificationHandlers["DocumentChange"].value
    
    
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
        if not self.IsDirty():
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


    def New(self):
        if self.CheckFileNeedsSave() == wx.ID_CANCEL:
            return
        self.StartSession(None)


    def Open(self, filePath=None):
        self.ShowFrame()
        if filePath is not None:
            res = wx.MessageBox(
                "Do you really want to load the tree file:\n%s" % filePath,
                eg.APP_NAME,
                wx.YES_NO|wx.CENTRE|wx.ICON_QUESTION,
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


    @eg.LogItWithReturn
    def Save(self):
        if not self.filePath:
            return self.SaveAs()
        self.WriteFile(self.filePath)
        return wx.ID_YES


    def SaveAs(self):
        filePath = self.AskFile(style=wx.SAVE|wx.OVERWRITE_PROMPT)
        if filePath is None:
            return wx.ID_CANCEL
        self.WriteFile(filePath)
        self.SetFilePath(filePath)
        return wx.ID_YES


    def AskFile(self, style):
        fileDialog = wx.FileDialog(
            self.frame,
            message="",
            wildcard="EventGhost Tree|*.xml;*.egtree",
            style=style
        )
        try:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return None
            return fileDialog.GetPath()
        finally:
            fileDialog.Destroy()


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


    #@eg.LogIt
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


    def OnCmdConfigure(self, node):
        eg.UndoHandler.Configure().Try(self, node)


    def OnCmdToggleEnable(self, node):
        eg.UndoHandler.ToggleEnable(self, node)



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
        sizer.Add(messageCtrl, 0, wx.ALIGN_CENTER|wx.LEFT|wx.TOP|wx.RIGHT, 6)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add(saveButton, 0, wx.LEFT|wx.RIGHT, 3)
        buttonSizer.Add(dontSaveButton, 0, wx.LEFT|wx.RIGHT, 3)
        buttonSizer.Add(cancelButton, 0, wx.LEFT|wx.RIGHT, 3)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(sizer)
        mainSizer.Add(buttonSizer, 0, wx.ALIGN_RIGHT|wx.ALL, 12)
        self.SetSizerAndFit(mainSizer)
        if parent:
            self.CenterOnParent()
        else:
            self.Center()


    def OnButton(self, event):
        buttonId = event.GetId()
        self.EndModal(buttonId)
        event.Skip()


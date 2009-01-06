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
from types import ClassType
import os
from xml.etree import cElementTree as ElementTree
from tempfile import mkstemp
from threading import Lock


class TreeStateData:
    guid = None
    time = None
    expandState = None # deprecated
    expanded = None
    
eg.GetConfig("treeStateData", TreeStateData)


class Document(object):
    
    def __init__(self):
        class ItemMixin:
            document = self
            tree = None
            root = None
        self.ItemMixin = ItemMixin
        itemNamespace = {}
        self.XMLTag2ClassDict = {}
        
        def MakeCls(name):
            baseCls = getattr(eg, name)
            cls = ClassType(name, (ItemMixin, baseCls), itemNamespace)
            self.XMLTag2ClassDict[cls.xmlTag] = cls
            return cls
        
        self.TreeLink = eg.TreeLink
        self.TreeItem = MakeCls("TreeItem")
        self.ContainerItem = MakeCls("ContainerItem")
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
        self.listeners = {}
        self.undoEvent = eg.NotificationHandler((False, False, "", ""))
        self.selectionEvent = eg.NotificationHandler()
        self.isDirty = eg.NotificationHandler(False)
        self.filePath = None
        self.root = None
        self.firstVisibleItem = None
        self.frame = None
        self.tree = None
        self._selection = None
        self.reentrantLock = Lock()
        
        
    def GetSelection(self):
        return self._selection
    
    
    def SetSelection(self, selection):
        self._selection = selection
        self.selectionEvent.Fire(selection)
        
    selection = property(fget=GetSelection, fset=SetSelection)
        
        
    def SetFilePath(self, filePath):
        self.filePath = filePath
        if self.frame is not None:
            self.frame.SetTitle(self.GetTitle())
    
    
    def GetTitle(self):
        if self.filePath is None:
            filename = eg.text.General.unnamedFile
        elif self.filePath is False:
            filename = "Example.xml"
        else:
            filename = os.path.basename(self.filePath)
        return "EventGhost %s - %s" % (eg.Version.string, filename)
        
        
    @eg.LogIt
    def SetTree(self, tree):
        self.tree = tree
        self.ItemMixin.tree = tree
        if tree and self.root:
            tree.SetData()


    def ResetUndoState(self):
        del self.stockUndo[:]
        del self.stockRedo[:]
        self.undoState = 0
        self.undoStateOnSave = 0
        self.undoEvent.Fire((False, False, "", ""))


    @eg.LogIt
    def LoadEmpty(self):
        self.ResetUndoState()
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
        self.isDirty.Fire(False)
        if self.tree:
            wx.CallAfter(self.tree.SetData)
        return root
        
    
    @eg.LogIt
    def Load(self, filePath):
        if self.tree:
            self.tree.DeleteAllItems()
        if filePath is None:
            return self.LoadEmpty()
        self.ResetUndoState()
        
        if filePath is False:
            filePath = "Example.xml"
            self.SetFilePath(filePath)
            self.filePath = False
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
        self.isDirty.Fire(False)
        self.AfterLoad()
        if self.tree:
            wx.CallAfter(self.tree.SetData)
        return root
        
        
    def StartSession(self, filePath):
        eg.eventThread.CallWait(eg.eventThread.StopSession)
        eg.eventThread.Call(eg.eventThread.StartSession, filePath)
        
        
    def AfterLoad(self):
        tsData = eg.config.treeStateData
        if tsData.guid == self.root.guid and tsData.time == self.root.time:
            self.SetExpandState(tsData.expanded)
            self.selection = self.FindItemWithPath(tsData.selection)
            self.firstVisibleItem = self.FindItemWithPath(
                tsData.firstVisibleItem
            )
        
    
    def WriteFile(self, filePath=None):
        if filePath is not None:
            self.SetFilePath(filePath)
        else:
            filePath = self.filePath
        success = False
        tmpFile, tmpPath = mkstemp(".xml", "$", os.path.dirname(filePath))
        os.close(tmpFile)
        try:
            tmpFile = file(tmpPath, "wb+")
            tmpFile.write('<?xml version="1.0" encoding="UTF-8" ?>\r\n')
            self.root.GetXmlString(tmpFile.write)
            tmpFile.close()
            try:
                os.remove(filePath)
            except:
                pass
            os.rename(tmpPath, filePath)
            self.isDirty.Fire(False)
            self.undoStateOnSave = self.undoState
            success = True
        except:
            eg.PrintTraceback("Error while saving file")
        return success    
 

    @eg.LogItWithReturn
    def Close(self):
        eg.config.hideOnStartup = self.frame is None
        if self.frame is not None:
            self.frame.Destroy()
        eg.config.autoloadFilePath = self.filePath
        stateData = eg.config.treeStateData
        stateData.guid = self.root.guid
        stateData.time = self.root.time
        stateData.expanded = self.GetExpandState()
        stateData.selection = self.selection.GetPath()
        stateData.firstVisibleItem = self.firstVisibleItem.GetPath()
    
    
    @eg.LogIt
    def AppendUndoHandler(self, handler):
        stockUndo = self.stockUndo
        if len(stockUndo) >= 20:
            del stockUndo[0]
        stockUndo.append(handler)
        self.undoState += 1
        del self.stockRedo[:]
        
        self.isDirty.Fire(True)
        self.undoEvent.Fire((True, False, ": " + handler.name, ""))
        
        
    def Undo(self):
        if len(self.stockUndo) == 0:
            return
        handler = self.stockUndo.pop()
        handler.Undo(self)
        self.undoState -= 1
        self.isDirty.Fire(self.undoState != self.undoStateOnSave)
        self.stockRedo.append(handler)
        if len(self.stockUndo):
            undoName = ": " + self.stockUndo[-1].name
            hasUndo = True
        else:
            undoName = ""
            hasUndo = False
        self.undoEvent.Fire((hasUndo, True, undoName, ": " + handler.name))
        
        
    @eg.LogIt
    def Redo(self):
        if len(self.stockRedo) == 0:
            return
        handler = self.stockRedo.pop()
        handler.Redo(self)
        self.undoState += 1
        self.isDirty.Fire(self.undoState != self.undoStateOnSave)
        self.stockUndo.append(handler)
        if len(self.stockRedo):
            redoName = ": " + self.stockRedo[-1].name
            hasRedo = True
        else:
            redoName = ""
            hasRedo = False
        self.undoEvent.Fire((True, hasRedo, ": " + handler.name, redoName))
        
        
    def RestoreItem(self, positionData, xmlData):
        eg.TreeLink.StartUndo()
        parent, pos = positionData.GetPosition()
        node = ElementTree.fromstring(xmlData)
        cls = self.XMLTag2ClassDict[node.tag]
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
        # If the program is started through a shortcut with "minimize" option
        # set, we get an iconize event while ShowFrame() is executing.
        # Therefore we have to use this CallLater workaround.
        # TODO:
        # Find a better way. Preferable detect the minimize option before
        # we create the MainFrame.
        if self.reentrantLock.acquire(False):
            if self.frame is not None:
                if len(self.frame.openDialogs) == 0:
                    self.frame.Destroy()
                    self.frame = None
            self.reentrantLock.release()
        else:
            wx.CallLater(100, self.HideFrame)
        
    
    def CheckFileNeedsSave(self):
        """
        Checks if the file was changed and if necessary asks the user if he 
        wants to save it. If the user affirms, calls Save/SaveAs also.
        
        returns: wx.ID_OK     if no save was needed
                 wx.ID_YES    if file was saved
                 wx.ID_NO     if file was not saved
                 wx.ID_CANCEL if user canceled possible save
        """
        if not self.isDirty.GetValue():
            return wx.ID_OK
        dialog = eg.MessageDialog(
            None, 
            eg.text.MainFrame.SaveChanges.mesg, 
            eg.APP_NAME + ": " + eg.text.MainFrame.SaveChanges.title, 
            style = wx.YES_DEFAULT
                |wx.YES_NO
                |wx.CANCEL
                |wx.STAY_ON_TOP
                |wx.ICON_EXCLAMATION
        )
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
        
    
    def Open(self):
        if self.CheckFileNeedsSave() == wx.ID_CANCEL:
            return wx.ID_CANCEL
        filePath = self.AskFile(wx.OPEN)
        if filePath is None:
            return wx.ID_CANCEL
        self.StartSession(filePath)
        
    
    def Save(self):
        if not self.filePath:
            return self.SaveAs()
        self.WriteFile()
        return wx.ID_YES


    def SaveAs(self):
        filePath = self.AskFile(style=wx.SAVE|wx.OVERWRITE_PROMPT)
        if filePath is None:
            return wx.ID_CANCEL
        self.WriteFile(filePath)
        return wx.ID_YES            


    def AskFile(self, style):
        fileDialog = wx.FileDialog(
            self.frame, 
            message="", 
            wildcard="*.xml", 
            style=style
        )
        result = fileDialog.ShowModal()
        if result == wx.ID_CANCEL:
            return None
        filePath = fileDialog.GetPath()
        fileDialog.Destroy()
        return filePath
        
    
    def ExecuteSelected(self):
        item = self.selection
        event = eg.EventGhostEvent("OnCmdExecute")
        eg.actionThread.Call(eg.actionThread.ExecuteTreeItem, item, event)
        return event

    
    def FindItemWithPath(self, path):
        item = self.root
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
                if item.isExpanded:
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
        ContainerItem = eg.ContainerItem
        def Traverse(item, i):
            if isinstance(item, ContainerItem):
                i += 1
                item.isExpanded = (i in expanded)
                for child in item.childs:
                    i = Traverse(child, i)
            return i
        
        Traverse(self.root, -1)


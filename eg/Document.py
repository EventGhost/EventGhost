# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import eg
import wx
from new import classobj
import os
import xml.etree.cElementTree as ElementTree
from tempfile import mkstemp


class Observable:
    
    def __init__(self, initialValue=None):
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

    def set(self, data):
        self.data = data
        for func in self.callbacks:
            #eg.notice(func, data)
            func(data)

    def get(self):
        return self.data

    def unset(self):
        self.data = None

gTreeItemTypes = ["TreeItem", "ContainerItem", "EventItem", "ActionItem",
    "PluginItem", "FolderItem", "MacroItem", "RootItem", "AutostartItem"]    

class Document:
    
    def __init__(self):
        class ItemMixin:
            document = self
            tree = None
            root = None
        self.ItemMixin = ItemMixin
        itemNamespace = {}
        self.XMLTag2ClassDict = {}
        for itemType in gTreeItemTypes:
            baseCls = getattr(eg, itemType)
            itemCls = classobj(itemType, (baseCls, ItemMixin), itemNamespace)
            setattr(self, itemType, itemCls)
            self.XMLTag2ClassDict[itemCls.xmlTag] = itemCls

        self.stockUndo = []
        self.stockRedo = []
        self.lastUndoId = 0
        self.undoIdOnSave = 0
        self.listeners = {}
        self.undoEvent = eg.EventHook()
        self.selection = None
        self.selectionEvent = eg.EventHook()
        self.isDirty = Observable(False)
        self.filePath = Observable(None)
        self.TreeLink = eg.TreeLink
        self.root = None
        
        
    def SetTree(self, tree):
        eg.whoami()
        self.tree = tree
        self.ItemMixin.tree = tree
        if tree and self.root:
            tree.SetData()


    def ResetUndoState(self):
        del self.stockUndo[:]
        del self.stockRedo[:]
        self.undoState = 0
        self.undoStateOnSave = 0
        self.undoEvent.Fire(False, False, "", "")


    def New(self):
        eg.whoami()
        self.ResetUndoState()
        self.filePath.set(None)
        eg.TreeLink.StartLoad()
        node = ElementTree.Element("EventGhost")
        root = self.RootItem(self, node)
        self.root = root
        self.ItemMixin.root = root
        node = ElementTree.Element("Autostart")
        self.autostartMacro = self.AutostartItem(root, node)
        self.root.AddChild(self.autostartMacro)
        self.isInLabelEdit = False
        eg.TreeLink.StopLoad()
        self.isDirty.set(False)
        return root
        
    
    def Load(self, filePath):
        eg.whoami()
        if self.tree:
            self.tree.DeleteAllItems()
        if not filePath:
            return self.New()
        self.ResetUndoState()
        
        self.filePath.set(filePath)
        eg.TreeLink.StartLoad()
        xmlTree = ElementTree.parse(filePath)
        node = xmlTree.getroot()
        root = self.RootItem(self, node)
        self.ItemMixin.root = root
        self.root = root
        eg.TreeLink.StopLoad()
        self.isDirty.set(False)
        if self.tree:
            self.tree.SetData()
        
        return root
        
        
    def Save(self, filePath=None):
        if filePath is not None:
            self.filePath.set(filePath)
        else:
            filePath = self.filePath.get()
        success = False
        fd, tmp_path = mkstemp(".xml", "$", os.path.dirname(filePath))
        os.close(fd)
        try:
            fd = file(tmp_path, "w+")
            fd.write('<?xml version="1.0" encoding="UTF-8" ?>')
            self.root.GetXmlString(fd.write, "", False)
            fd.close()
            try:
                os.remove(filePath)
            except:
                pass
            os.rename(tmp_path, filePath)
            self.isDirty.set(False)
            self.undoStateOnSave = self.undoState
            success = True
        except:
            eg.PrintTraceback("Error while saving file")
        return success    
 

    def AppendUndoHandler(self, handler):
        eg.whoami()
        stockUndo = self.stockUndo
        if len(stockUndo) >= 20:
            del stockUndo[0]
        stockUndo.append(handler)
        self.undoState += 1
        del self.stockRedo[:]
        
        self.isDirty.set(True)
        self.undoEvent.Fire(True, False, ": " + handler.name, "")
        
        
    def Undo(self):
        if len(self.stockUndo) == 0:
            return
        handler = self.stockUndo.pop()
        handler.Undo(self)
        self.undoState -= 1
        self.isDirty.set(self.undoState != self.undoStateOnSave)
        self.stockRedo.append(handler)
        if len(self.stockUndo):
            undoName = ": " + self.stockUndo[-1].name
            hasUndo = True
        else:
            undoName = ""
            hasUndo = False
        self.undoEvent.Fire(hasUndo, True, undoName, ": " + handler.name)
        
        
    def Redo(self):
        eg.whoami()
        if len(self.stockRedo) == 0:
            return
        handler = self.stockRedo.pop()
        handler.Redo(self)
        self.undoState += 1
        self.isDirty.set(self.undoState != self.undoStateOnSave)
        self.stockUndo.append(handler)
        if len(self.stockRedo):
            redoName = ": " + self.stockRedo[-1].name
            hasRedo = True
        else:
            redoName = ""
            hasRedo = False
        self.undoEvent.Fire(True, hasRedo, ": " + handler.name, redoName)
        
        
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
    
    
    def CheckFileNeedsSave(self):
        """
        Checks if the file was changed and if necessary asks the user if he 
        wants to save it. If the user affirms, calls Save/SaveAs also.
        
        returns: wx.ID_OK     if no save was needed
                 wx.ID_YES    if file was saved
                 wx.ID_NO     if file was not saved
                 wx.ID_CANCEL if user canceled posssible save
        """
        if not self.isDirty.get():
            return wx.ID_OK
        dialog = wx.MessageDialog(
            None, 
            eg.text.MainFrame.SaveChanges.mesg, 
            eg.APP_NAME + ": " + eg.text.MainFrame.SaveChanges.title, 
            style = wx.YES_DEFAULT
                |wx.YES_NO
                |wx.CANCEL
                |wx.STAY_ON_TOP
                |wx.ICON_EXCLAMATION
        )
        res = dialog.ShowModal()
        dialog.Destroy()
        if res == wx.ID_CANCEL:
            return wx.ID_CANCEL
        if res == wx.ID_YES:
            return self.OnCmdSave()
        return wx.ID_NO
            

    def OnCmdSave(self, event=None):
        """ Handle the menu command 'Save'. """
        if self.filePath.get() is None:
            return self.OnCmdSaveAs()
        self.Save()
        return wx.ID_YES


    def ExecuteSelected(self):
        item = self.selection
        event = eg.EventGhostEvent("OnCmdExecute")
        eg.actionThread.Call(eg.actionThread.ExecuteTreeItem, item, event)
        return event

    
                     
        

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
eg.PrintDebugNotice("Loading UndoableTasks")
import wx
import xml.etree.cElementTree as ElementTree

class Text:
    rename = "Rename item"
    
    
    
class NewItem:
    """
    Abstract class for the creation of new tree items.
    """
    
    def StoreItem(self, item):
        self.positionData = item.GetPositionData()
        self.cls = item.__class__
        item.document.AppendUndoHandler(self)
    
    
    @eg.LogIt
    def Undo(self, document):
        item = self.positionData.GetItem()
        self.data = item.GetFullXml()
        item.Delete()
        
        
    @eg.LogIt
    def Redo(self, document):
        item = document.RestoreItem(self.positionData, self.data)
        item.Select()
    
    
    
class NewPlugin(NewItem):
    """
    Create a new PluginItem if the user has choosen to do so from the menu
    or toolbar.
    """
    
    def Do(self, document, pluginInfo):
        """ Handle the menu command 'Add Plugin...'. """
        self.name = eg.text.MainFrame.Menu.AddPlugin.replace("&", "")

        pluginItem = document.PluginItem.Create(
            document.autostartMacro,
            -1,
            file=pluginInfo.pluginName
        )
        pluginItem.Select()
        if pluginItem.executable:
            if pluginItem.NeedsStartupConfiguration():
                if not CmdConfigure().Do(pluginItem):
                    pluginItem.Delete()
                    return None
#                args = pluginItem.ProcessConfigureDialog()
#                if args is None:
#                    pluginItem.Delete()
#                    return None
#                else:
#                    pluginItem.SetParams(*args)
#                    pluginItem.Refresh()
            eg.actionThread.CallWait(pluginItem.Execute)
        self.StoreItem(pluginItem)
        if pluginInfo.createMacrosOnAdd:
            AddActionGroup().Do(document, pluginItem)
        return pluginItem
       
            
            
class AddActionGroup(NewItem):
    name="Add all actions of plugin"
    
    def Do(self, document, pluginItem):
        parentItem = eg.AddActionGroupDialog(document.frame).DoModal()
        if parentItem is None:
            return
        
        def Traverse(parentItem, info):
            folderItem = document.FolderItem.Create(
                parentItem, 
                name=info.name
            )
            for action in info.actionList:
                if isinstance(action, eg.ActionGroup):
                    Traverse(folderItem, action)
                else:
                    macroItem = document.MacroItem.Create(
                        folderItem, 
                        name=action.name
                    )
                    actionItem = document.ActionItem.Create(
                        macroItem,
                        text = "%s.%s()" % (
                            action.plugin.info.evalName, 
                            action.__class__.__name__
                        ),
                    )
            return folderItem
        folderItem = Traverse(parentItem, pluginItem.executable.info)
        self.StoreItem(folderItem)
        folderItem.Select()
        folderItem.tree.Expand(folderItem.id)
            
    
    
class NewFolder(NewItem):
    """
    Create a new FolderItem if the user has choosen to do so from the menu
    or toolbar.
    """
    
    @eg.LogIt
    def Do(self, document):
        self.name = eg.text.MainFrame.Menu.NewFolder.replace("&", "")
        obj = document.selection
        if isinstance(obj, (document.MacroItem, document.AutostartItem)):
            parentObj = obj.parent
            pos = parentObj.childs.index(obj) + 1
            if pos >= len(parentObj.childs):
                pos = -1
        elif isinstance(
            obj, 
            (document.ActionItem, document.EventItem, document.PluginItem)
        ):
            obj = obj.parent
            parentObj = obj.parent
            pos = parentObj.childs.index(obj) + 1
            if pos >= len(parentObj.childs):
                pos = -1
        else:
            parentObj = obj
            pos = -1
        item = document.FolderItem.Create(
            parentObj, 
            pos, 
            name=eg.text.General.unnamedFolder
        )
        self.StoreItem(item)
        item.tree.SetFocus()
        item.Select()
        item.tree.EditLabel(item.id)
        return item
    
    
    
class NewMacro(NewItem):
    """
    Create a new MacroItem if the user has choosen to do so from the menu
    or toolbar.
    """
    
    def Do(self, document):
        self.name = eg.text.MainFrame.Menu.NewMacro.replace("&", "")
        obj = document.selection
        if isinstance(obj, (document.MacroItem, document.AutostartItem)):
            parentObj = obj.parent
            pos = parentObj.childs.index(obj) + 1
            if pos >= len(parentObj.childs):
                pos = -1
        elif isinstance(
            obj, 
            (document.ActionItem, document.EventItem, document.PluginItem)
        ):
            obj = obj.parent
            parentObj = obj.parent
            pos = parentObj.childs.index(obj) + 1
            if pos >= len(parentObj.childs):
                pos = -1
        else:
            parentObj = obj
            pos = -1
        item = document.MacroItem.Create(
            parentObj, 
            pos, 
            name=eg.text.General.unnamedMacro
        )
        item.Select()
        self.StoreItem(item)
        # let the user choose an action
        action = eg.AddActionDialog(document.frame).DoModal()
        
        # if user canceled the dialog, take a quick exit
        if action is None:
            return item
        
        actionObj = NewAction().Do(document, action)
        if actionObj:
            label = actionObj.GetLabel()
            item.RenameTo(label)
            item.Select()
        return item



class NewAction(NewItem):
    """
    Create a new ActionItem if the user has choosen to do so from the menu
    or toolbar.
    """
    
    @eg.LogIt
    def Do(self, document, action):
        self.name = eg.text.MainFrame.Menu.NewAction.replace("&", "")
        # find the right insert position
        selection = document.selection
        if isinstance(selection, (document.MacroItem, document.AutostartItem)):
            # if a macro is selected, append it as last element of the macro
            parent = selection
            pos = -1
        else:
            parent = selection.parent
            childs = parent.childs
            for pos in range(childs.index(selection) + 1, len(childs)):
                if not isinstance(childs[pos], document.EventItem):
                    break
            else:
                pos = -1
        
        # create the ActionItem instance and setup all data
        item = document.ActionItem.Create(
            parent, 
            pos, 
            text = "%s.%s()" % (
                action.plugin.info.evalName, 
                action.__class__.__name__
            )
        )
        item.Select()
        
        if item.NeedsStartupConfiguration():
            if not CmdConfigure().Do(item, True):
                item.Delete()
                return None
        self.StoreItem(item)
        return item
    
    

class NewEvent(NewItem):
    
    def Do(self, document, label=None, parent=None, pos=-1):
        self.name = eg.text.MainFrame.Menu.NewEvent.replace("&", "")
        if parent is None:
            obj = document.selection
            if isinstance(obj, document.MacroItem):
                parent = obj
            else:
                parent = obj.parent
            for pos, obj in enumerate(parent.childs):
                if isinstance(obj, document.ActionItem):
                    break
            else:
                pos = 0
            
        if label is not None:
            item = document.EventItem.Create(parent, pos, name=label)
            item.Select()
        else:
            label = eg.text.General.unnamedEvent
            item = document.EventItem.Create(parent, pos, name=label)
            item.Select()
            item.tree.EditLabel(item.id)
            
        self.StoreItem(item)
        return item
    


class CmdClear:
    name = eg.text.MainFrame.Menu.Delete.replace("&", "")
    
    def __init__(self, document, item):
        if not item.CanDelete() or not item.AskDelete():
            return

        self.data = item.GetFullXml()
        self.positionData = item.GetPositionData()
        document.AppendUndoHandler(self)
        item.Delete()


    def Undo(self, document):
        item = document.RestoreItem(self.positionData, self.data)
        item.Select()
        
        
    def Redo(self, document):
        self.positionData.GetItem().Delete()


        
class CmdCut(CmdClear):
    name = eg.text.MainFrame.Menu.Cut.replace("&", "")
    
    def __init__(self, document, item):
        if not item.CanDelete() or not item.AskDelete():
            return

        self.data = item.GetFullXml()
        self.positionData = item.GetPositionData()
        document.AppendUndoHandler(self)
        document.tree.Copy()
        item.Delete()
        
        
        
class CmdPaste:
    name = eg.text.MainFrame.Menu.Paste.replace("&", "")
    
    def __init__(self, document):
        tree = document.tree
        self.items = []
        is_internal_paste = False
        selectionObj = tree.GetPyData(tree.GetSelection())
        if not wx.TheClipboard.Open():
            return
        try:
            dataObj = wx.CustomDataObject("DragEventItem")
            if wx.TheClipboard.GetData(dataObj):
                selectedObj = tree.GetPyData(tree.GetSelection())
                if selectedObj.DropTest(eg.EventItem):
                    label = dataObj.GetData()
                    parent = selectionObj.parent
                    pos = parent.childs.index(selectionObj)
                    NewEvent().Do(tree.document, label)
                    #tree.OnNewEvent(label)
                return
            dataObj = wx.TextDataObject()
            if not wx.TheClipboard.GetData(dataObj):
                return
            clipboardData = dataObj.GetText()
            is_internal_paste = (clipboardData == tree.clipboardData)
            xmlTree = ElementTree.fromstring(clipboardData.encode("utf-8"))
            for childXmlNode in xmlTree:
                targetObj = selectionObj
                childCls = document.XMLTag2ClassDict[childXmlNode.tag]
                before = None
                childClsBase = childCls.__bases__[0]
                insertionHint = targetObj.DropTest(childClsBase)
                if insertionHint in (1, 5): 
                    # item will move inside
                    for i in xrange(len(targetObj.childs)-1, -1, -1):
                        next = targetObj.childs[i]
                        insertionHint = next.DropTest(childClsBase)
                        if insertionHint in (3, 4, 5):
                            break
                        before = next
                elif insertionHint in (2, 4): 
                    # item will move before selection
                    before = targetObj
                    parent = targetObj.parent
                    pos = parent.GetChildIndex(targetObj)
                    for i in xrange(pos-1, -1, -1):
                        next = parent.childs[i]
                        insertionHint = next.DropTest(childClsBase)
                        if insertionHint != 2:
                            break
                        before = next
                    targetObj = targetObj.parent
                elif insertionHint == 3: #in (3, 4):
                    # item will move after selection
                    parent = targetObj.parent
                    pos = parent.GetChildIndex(targetObj)
                    for i in xrange(pos+1, len(parent.childs)):
                        next = parent.childs[i]
                        insertionHint = next.DropTest(childClsBase)
                        if insertionHint != 3:
                            before = next
                            break
                    targetObj = targetObj.parent
                else:
                    eg.PrintError("Unexpected item in paste.")
                    return
                if before is None:
                    pos = -1;
                else:
                    pos = before.parent.childs.index(before)
                    if pos + 1 == len(before.parent.childs):
                        pos = -1
                obj = eg.actionThread.CallWait(childCls, targetObj, childXmlNode)
                obj.RestoreState()
                targetObj.AddChild(obj, pos)
                self.items.append(obj.GetPositionData())
            if len(self.items):
                obj.Select()
                document.TreeLink.StopLoad()
                document.AppendUndoHandler(self)
        finally:
            wx.TheClipboard.Close()                        

            
    def Undo(self, document):
        data = []
        for positionData in self.items:
            item = positionData.GetItem()
            data.append((positionData, item.GetFullXml()))
            item.Delete()
        self.items = data
        
        
    def Redo(self, document):
        data = []
        for positionData, xmlString in self.items:
            item = document.RestoreItem(positionData, xmlString)
            data.append(positionData)
        item.Select()
        self.items = data
        
        
        
class CmdRename:
    name = eg.text.MainFrame.Menu.Rename.replace("&", "")
    
    def __init__(self, document, item, text):
        self.oldText = item.name
        self.positionData = item.GetPositionData()
        self.text = text
        item.RenameTo(text)
        document.AppendUndoHandler(self)
        
        
    def Undo(self, document):
        item = self.positionData.GetItem()
        item.RenameTo(self.oldText)
        item.Select()
        
        
    def Redo(self, document):
        item = self.positionData.GetItem()
        item.RenameTo(self.text)
        item.Select()



class CmdToggleEnable:
    name = eg.text.MainFrame.Menu.Disabled.replace("&", "")
    
    def __init__(self, document):
        item = document.selection
        self.positionData = item.GetPositionData()
        self.state = not item.isEnabled
        item.Enable(self.state)
        document.AppendUndoHandler(self)
        
        
    def Undo(self, document):
        item = self.positionData.GetItem()
        item.Enable(not self.state)
        item.Select()

        
    def Redo(self, document):
        item = self.positionData.GetItem()
        item.Enable(self.state)
        item.Select()



class CmdMoveTo:
    name = "Move Item"
    
    @eg.LogIt
    def __init__(self, document, item, parent, pos):
        tree = document.tree
        tmp = tree.GetFirstVisibleItem()
        oldParent = item.parent
        self.oldPos = item.parent.childs.index(item)
        item.MoveItemTo(parent, pos)
        tree.EnsureVisible(tmp)
        self.oldParentPath = oldParent.GetPath()
        self.newPositionData = item.GetPositionData()
        item.Select()
        document.AppendUndoHandler(self)
    
    
    @eg.LogIt
    def Undo(self, document):
        parent1, pos1 = self.newPositionData.GetPosition()
        item = parent1.childs[pos1]
        parent = item.tree.root
        for parentPos in self.oldParentPath:
            parent = parent.childs[parentPos]
        oldParent = item.parent
        oldPos = self.oldPos
        self.oldPos = item.parent.childs.index(item)
        if parent1 == parent:
            if pos1 < oldPos:
                oldPos += 1
        item.MoveItemTo(parent, oldPos)
        self.oldParentPath = oldParent.GetPath()
        self.newPositionData = item.GetPositionData()
        item.Select()
        
    Redo = Undo
        


class CmdConfigure:
    
    def Try(self, document):
        item = document.selection
        if isinstance(item, eg.ActionItem):
            eg.Greenlet(self.Do).switch(item)
        
    
    def Do(self, item, isFirstConfigure=False):
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
        gr = None
        while True:
            eg.currentConfigureItem = item
            try:
                if gr is None or gr.dead:
                    gr = eg.Greenlet(executable.Configure)
                    newArgs = gr.switch(*item.args)
                else:
                    newArgs = gr.switch()
                #newArgs = executable.Configure(*item.args)
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
                        item.SetParams(*oldArgs)
                        item.Refresh()
                    return False
                elif userAction == wx.ID_OK:
                    if not gr.dead:
                        gr.switch(wx.ID_CANCEL)
                    item.openConfigDialog.Destroy()
                    del item.openConfigDialog
                    break
                elif userAction == wx.ID_APPLY:
                    item.SetParams(*newArgs)
                    item.Refresh()
                    wasApplied = True
                    continue
            elif newArgs is None:
                return False
            elif newArgs is -1:
                # This is most likely a PythonScript action
                return True
        item.SetParams(*newArgs)
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
        
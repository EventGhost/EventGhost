import eg
import wx
import xml.etree.cElementTree as ElementTree

class Text:
    rename = "Rename item"
    
    
    
class CmdNewItem:
    """
    Abstract class for the creation of new tree items.
    """
    
    def Do(self, item):
        self.positioner = item.GetPositioner()
        self.cls = item.__class__
        item.document.AppendUndoHandler(self)
    
    
    def Undo(self, document):
        eg.whoami()
        parent, pos = self.positioner()
        item = parent.childs[pos]
        self.data = item.GetFullXml()
        item.Delete()
        
        
    def Redo(self, document):
        eg.whoami()
        item = document.RestoreItem(self.positioner, self.data)
        item.Select()
    
    
    
class CmdNewPlugin(CmdNewItem):
    """
    Create a new PluginItem if the user has choosen to do so from the menu
    or toolbar.
    """
    
    def Do(self, document):
        """ Handle the menu command 'Add Plugin...'. """
        def ShowDialog():
            from eg.Dialogs.AddPluginDialog import AddPluginDialog
            return AddPluginDialog().DoModal()
        pluginInfo = eg.CallWait(ShowDialog)
        
        if pluginInfo is None:
            return

        self.name = eg.text.MainFrame.Menu.AddPlugin.replace("&", "")
        tree = document.tree
        pluginItem = document.PluginItem.Create(
            document.autostartMacro,
            -1,
            file=pluginInfo.pluginName
        )
        self.positioner = pluginItem.GetPositioner()
        pluginItem.Select()
        if pluginItem.executable:
            if pluginItem.NeedsConfiguration():
                result = eg.CallWait(pluginItem.DoConfigure)
                if result is False:
                    pluginItem.Delete()
                    return
            eg.actionThread.Call(pluginItem.Execute)
        CmdNewItem.Do(self, pluginItem)
       
            

class CmdNewFolder(CmdNewItem):
    """
    Create a new FolderItem if the user has choosen to do so from the menu
    or toolbar.
    """
    
    def Do(self, document):
        eg.whoami()
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
        CmdNewItem.Do(self, item)
        item.Select()
        item.tree.EditLabel(item.id)
        return item
    
    
    
class CmdNewMacro(CmdNewItem):
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
        CmdNewItem.Do(self, item)
        actionObj = CmdNewAction().Do(document)
        if actionObj:
            label = actionObj.GetLabel()
            item.RenameTo(label)
            item.Select()
        return item



class CmdNewAction(CmdNewItem):
    """
    Create a new ActionItem if the user has choosen to do so from the menu
    or toolbar.
    """
    
    def Do(self, document):
        eg.whoami()
        self.name = eg.text.MainFrame.Menu.NewAction.replace("&", "")
        # let the user choose an action
        def ShowDialog():
            from eg.Dialogs.AddActionDialog import AddActionDialog
            return AddActionDialog().DoModal()
        action = eg.CallWait(ShowDialog)
        
        # if user canceled the dialog, take a quick exit
        if action is None:
            return None
        
        # find the right insert position
        selectedItem = document.selection
        if isinstance(selectedItem, (document.MacroItem, document.AutostartItem)):
            # if a macro is selected, append it as last element of the macro
            parent = selectedItem
            pos = -1
        else:
            parent = selectedItem.parent
            childs = parent.childs
            for pos in range(childs.index(selectedItem) + 1, len(childs)):
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
        
        if item.NeedsConfiguration():
            result = eg.CallWait(item.DoConfigure)
            if result is False:
                item.Delete()
                return None
        CmdNewItem.Do(self, item)
        return item
    
    

class CmdNewEvent(CmdNewItem):
    
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
            
        CmdNewItem.Do(self, item)
        return item
    


class CmdClear:
    name = eg.text.MainFrame.Menu.Delete.replace("&", "")
    
    def __init__(self, document, item):
        if not item.CanDelete() or not item.AskDelete():
            return

        self.data = item.GetFullXml()
        self.positioner = item.GetPositioner()
        document.AppendUndoHandler(self)
        item.Delete()


    def Undo(self, document):
        item = document.RestoreItem(self.positioner, self.data)
        item.Select()
        
        
    def Redo(self, document):
        parent, pos = self.positioner()
        item = parent.childs[pos]
        childs = item.childs[:]
        item.Delete()


        
class CmdCut(CmdClear):
    name = eg.text.MainFrame.Menu.Cut.replace("&", "")
    
    def __init__(self, document, item):
        if not item.CanDelete() or not item.AskDelete():
            return

        self.data = item.GetFullXml()
        self.positioner = item.GetPositioner()
        document.AppendUndoHandler(self)
        document.tree.Copy()
        item.Delete()
        
        
        
class CmdPaste:
    name = eg.text.MainFrame.Menu.Paste.replace("&", "")
    
    def __init__(self, document):
        tree = document.tree
        self.items = []
        is_internal_paste = False
        if not wx.TheClipboard.Open():
            return
        try:
            dataObj = wx.CustomDataObject("DragEventItem")
            if wx.TheClipboard.GetData(dataObj):
                selectedObj = tree.GetPyData(tree.GetSelection())
                if selectedObj.DropTest(EventItem):
                    label = dataObj.GetData()
                    tree.OnNewEvent(label)
                return
            dataObj = wx.TextDataObject()
            if not wx.TheClipboard.GetData(dataObj):
                return
            selectionObj = tree.GetPyData(tree.GetSelection())
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
                obj = childCls(targetObj, childXmlNode)
                obj.RestoreState()
                targetObj.AddChild(obj, pos)
                self.items.append(obj.GetPositioner())
            if len(self.items):
                obj.Select()
                document.TreeLink.StopLoad()
                document.AppendUndoHandler(self)
        finally:
            wx.TheClipboard.Close()                        

            
    def Undo(self, document):
        data = []
        for positioner in self.items:
            parent, pos = positioner()
            item = parent.childs[pos]
            data.append((positioner, item.GetFullXml()))
            item.Delete()
        self.items = data
        
        
    def Redo(self, document):
        data = []
        for positioner, xmlString in self.items:
            item = document.RestoreItem(positioner, xmlString)
            data.append(positioner)
        item.Select()
        self.items = data
        
        
        
class CmdRename:
    name = eg.text.MainFrame.Menu.Rename.replace("&", "")
    
    def __init__(self, document, item, text):
        self.oldText = item.name
        self.positioner = item.GetPositioner()
        self.text = text
        item.RenameTo(text)
        document.AppendUndoHandler(self)
        
        
    def Undo(self, document):
        parent, pos = self.positioner()
        item = parent.childs[pos]
        item.RenameTo(self.oldText)
        item.Select()
        
        
    def Redo(self, document):
        parent, pos = self.positioner()
        item = parent.childs[pos]
        item.RenameTo(self.text)
        item.Select()



class CmdToggleEnable:
    name = eg.text.MainFrame.Menu.Disabled.replace("&", "")
    
    def __init__(self, document, item):
        self.positioner = item.GetPositioner()
        self.state = not item.isEnabled
        item.Enable(self.state)
        document.AppendUndoHandler(self)
        
        
    def Undo(self, document):
        parent, pos = self.positioner()
        item = parent.childs[pos]
        item.Enable(not self.state)
        item.Select()

        
    def Redo(self, document):
        parent, pos = self.positioner()
        item = parent.childs[pos]
        item.Enable(self.state)
        item.Select()



class CmdMoveTo:
    name = "Move Item"
    
    def __init__(self, document, item, parent, pos):
        tree = document.tree
        tmp = tree.GetFirstVisibleItem()
        oldParent = item.parent
        self.oldPos = item.parent.childs.index(item)
        item.MoveItemTo(parent, pos)
        tree.EnsureVisible(tmp)
        self.oldParentPath = oldParent.GetPath()
        self.newPositioner = item.GetPositioner()
        item.Select()
        document.AppendUndoHandler(self)
    
    
    def Undo(self, document):
        eg.whoami()
        parent1, pos1 = self.newPositioner()
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
        self.newPositioner = item.GetPositioner()
        item.Select()
        
    Redo = Undo
        


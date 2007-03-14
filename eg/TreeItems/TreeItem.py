
from xml.sax.saxutils import quoteattr, escape
import weakref
from cStringIO import StringIO
import xml.etree.cElementTree as ElementTree

import wx
import eg
from TreeLink import TreeLink
from TreePosition import TreePosition


class TreeItem(object):
    # name
    # id
    # parent
    # isEnabled
    # iconIndex
    # xmlId
    # __ weakref__
    
    xmlTag = "Item"
    dependants = None
    childs = ()
    canExecute = False
            
        
    def GetFullXml(self):
        TreeLink.StartUndo()
        data = self.GetXml()
        TreeLink.StopUndo()
        return data
    
        
    @classmethod
    def Create(cls, parent, pos, text="", **kwargs):
        node = ElementTree.Element(cls.xmlTag)
        node.text = text
        for k, v in kwargs.items():
            node.attrib[k] = v
        self = cls(parent, node)
        parent.AddChild(self, pos)
        return self
        
        
    def __init__(self, parent, node):
        self.parent = parent
        self.id = None
        attrib = node.attrib
        for key, value in node.items():
            del attrib[key] 
            attrib[key.lower()] = value
        get = attrib.get
        self.name = get("name", "")
        self.isEnabled = not get('enabled') == "False"
        self.xmlId = TreeLink.NewXmlId(int(get('id', -1)), self)

        
    def RestoreState(self):
        pass
    
    
    def WriteToXML(self):
        attr = []
        if self.name:
            attr.append(('Name', self.name))
        if self.dependants or TreeLink.inUndo:
            attr.append(('id', self.xmlId))
        if not self.isEnabled:
            attr.append(('Enabled', 'False'))
        if self.childs:
            childs = self.childs
        else:
            childs = None
        return attr, None, childs


    def GetXmlString(self, write, indent_str="", pretty=True):
        attr, text, childs = self.WriteToXML()
        write(indent_str)
        write("<")
        write(self.xmlTag)
        for key, value in attr:
            write(' %s=%s' % (key, quoteattr(unicode(value)).encode("UTF-8")))
        write(">")
        if pretty:
            new_indent_str = indent_str + "    "
        else:
            new_indent_str = indent_str
        if text is not None:
            write(new_indent_str)
            write(escape(text).encode("UTF-8"))
        if childs:
            for child in childs:
                child.GetXmlString(write, new_indent_str, pretty)
        write(indent_str)
        write("</%s>" % self.xmlTag)
                
                
    def GetXml(self, indent_str="", pretty=False):
        output = StringIO()
        self.GetXmlString(output.write, "", False)
        data = output.getvalue()
        output.close()
        return data
        
        
    def CreateTreeItem(self, tree, parentId):
        #eg.whoami()
        id = tree.AppendItem(
            parentId,
            self.GetLabel(), 
            self.iconIndex + (not self.isEnabled), 
            -1, 
            wx.TreeItemData(self)
        )
        self.id = id
        self.SetAttributes(tree, id)
        return id
        
    
    def CreateTreeItemAt(self, tree, parentId, pos):
        eg.whoami()
        if pos == -1 or pos >= len(self.parent.childs):
            return TreeItem.CreateTreeItem(self, tree, parentId)
        else:
            id = tree.InsertItemBefore(
                parentId,
                pos, 
                self.GetLabel(), 
                self.iconIndex + (not self.isEnabled), 
                -1, 
                wx.TreeItemData(self)
            )
            self.SetAttributes(tree, id)
            self.id = id
            return id
    
    
    def DeleteTreeItem(self, tree):
        eg.AssertThread()
        if self.id is not None:
            tree.Delete(self.id)
            self.id = None
        
        
    def Select(self):
        eg.AssertThread()
        tree = self.tree
        if tree is None:
            return
        if self.id is None:
            root = self.root
            stack = []
            item = self.parent
            while item is not root:
                stack.append(item)
                item = item.parent
            for item in reversed(stack):
                if not tree.IsExpanded(item.id):
                    tree.Expand(item.id)
        tree.SelectItem(self.id)
        
        
    def GetPositionData(self):
        """ 
        Returns a TreePosition object to the item.
        """    
        return TreePosition(self)
    
    
    def Delete(self):
        eg.AssertThread()
        self._Delete()
        if self.id:
            self.tree.Delete(self.id)


    def _Delete(self):
        if self.dependants is not None:
            TreeLink.RemoveDependants(self)
        if self.xmlId in TreeLink.sessionId2target:
            del TreeLink.sessionId2target[self.xmlId]
        if self.xmlId in TreeLink.id2target:
            del TreeLink.id2target[self.xmlId]
        self.parent.RemoveChild(self)
        self.parent = None
        
        
    def ShowInfo(self):
        s = "%r " % self
        s += self.GetLabel() + "\n"
        s += "Dependant Links:\n"
        if self.dependants:
            for i, link in enumerate(self.dependants):
                s += "%d.\n" % i
                if link.target is None:
                    s += "Target: %r\n" % link.target
                else:
                    s += "  Target: %r %s\n" % (link.target, link.target.GetLabel())
                if link.owner is None:
                    s += "  Owner: %r\n" % (link.owner)
                else:
                    s += "  Owner: %r %s\n" % (link.owner, link.owner.GetLabel())
        import  wx.lib.dialogs
        wx.lib.dialogs.ScrolledMessageDialog(None, s, "Info").Show()
        
    
    
    def GetAllItems(self):
        """
        Return a list of all nodes including self, by recusively traversing
        the child nodes.
        """
        result = []
        append = result.append
        def _RecurseChilds(item):
            append(item)
            for child in item.childs:
                _RecurseChilds(child)
        _RecurseChilds(self)
        return result
    
    
    def GetDependantsOutside(self, allItems):
        result = []
        append = result.append
        def _RecurseChilds(item):
            if item.dependants is not None:
                for link in item.dependants:
                    if link.owner and link.owner not in allItems:
                        append(link)
            for child in item.childs:
                _RecurseChilds(child)
        _RecurseChilds(self)
        return result
            
                
    def AskDelete(self):
        if not eg.config.confirmDelete:
            return True
        allItems = self.GetAllItems()
        count = len(allItems) - 1
        if count > 0:
            mesg = eg.text.General.deleteManyQuestion % str(count)
        else:
            mesg = eg.text.General.deleteQuestion
        answer = wx.MessageBox(
            mesg, 
            eg.APP_NAME,
            wx.NO_DEFAULT|wx.YES_NO|wx.ICON_EXCLAMATION
        )
        if answer == wx.NO:
            return False
        dependants = self.GetDependantsOutside(allItems)
        if len(dependants) > 0:
            answer = wx.MessageBox(
                eg.text.General.deleteLinkedItems,
                eg.APP_NAME,
                wx.NO_DEFAULT|wx.YES_NO|wx.ICON_EXCLAMATION
            )
            return answer == wx.YES
        return True
    
    
    def CanCut(self):
        return True
    
    
    def CanCopy(self):
        return True
    
    
    def CanPaste(self):
        if not wx.TheClipboard.Open():
            return False
        try:
            dataObj = wx.CustomDataObject("DragEventItem")
            if wx.TheClipboard.GetData(dataObj):
                if self.DropTest(EventItem):
                    return True
                
            dataObj = wx.TextDataObject()
            if not wx.TheClipboard.GetData(dataObj):
                return False
            try:
                data = dataObj.GetText().encode("utf-8")
                xml_tree = ElementTree.fromstring(data)
                for childXmlNode in xml_tree:
                    childCls = self.document.XMLTag2ClassDict[childXmlNode.tag].__bases__[0]
                    if self.DropTest(childCls) in (1, 5):
                        continue
                    if self.parent is None:
                        return False
                    else:
                        if self.parent.DropTest(childCls) not in (1, 5):
                            return False
            except:
                return False
        finally:            
            wx.TheClipboard.Close()
        return True    
    
    
    def CanDelete(self):
        return True
    
    
    def CanDisable(self):
        return True
    
    
    def GetLabel(self):
        return self.name
    
    
    def RenameTo(self, newName):
        eg.AssertThread()
        eg.whoami()
        self.name = newName
        self.tree.SetItemText(self.id, newName)
        wx.CallAfter(self.Refresh)
        if self.dependants:
            for link in self.dependants:
                wx.CallAfter(link.owner.Refresh)
                
                
    def Refresh(self):
        pass
            
            
    def SetAttributes(self, tree, id):
        pass
    
    
    def MoveItemTo(self, newParentItem, pos):
        eg.whoami()
        tree = self.tree
        tree.Freeze()
        try:
            oldPos = self.parent.RemoveChild(self)
            if newParentItem == self.parent:
                if pos > oldPos:
                    pos -= 1
            #if pos >= len(newParentItem.childs):
            #    pos = -1
            self.parent = newParentItem
            newParentItem.AddChild(self, pos)
        finally:
            tree.Thaw()
        return id
            
    
    def Enable(self, enable=True):
        self.isEnabled = enable
        if self.id is not None:
            self.tree.SetItemImage(
                self.id,
                self.iconIndex + (not enable), 
                wx.TreeItemIcon_Normal
            )
            if self.document.selection == self:
                self.document.selectionEvent.Fire(self)
                

    def IsEditable(self):
        return True
    
    
    def IsConfigurable(self):
        return False
    
    
    def Execute(self):
        return None, None
    
    
    def DoDoubleClick(self, event):
        return False
    
    
    def GetChildIndex(self, child):
        try:
            return self.childs.index(child)
        except ValueError:
            return None
    
    
    def GetCount(self, count=0):
        return count + 1
    
    
    def GetPath(self):
        item = self
        root = self.root
        path = []
        while item is not root:
            parent = item.parent
            path.append(parent.childs.index(item))
            item = parent
        path.reverse()
        return path
    
        
    def Traverse(self, func):
        result = func(self)
        if result is not None:
            return result
        for child in self.childs:
            result = child.Traverse(func)
            if result is not None:
                return result
        return None
    
    
    def TraverseDeepthFirst(self, func):
        for child in self.childs:
            result = child.TraverseDeepthFirst(func)
            if result is not None:
                return result
        result = func(self)
        if result is not None:
            return result
        return None
        
        
        
    def DoPrint(self, text):
        wRef = weakref.ref(self)
        eg.log.DoPrint(text, self.iconIndex, wRef)
        
    
    def DropTest(self, cls):
        # returns:
        #   None = item cannot be dropped on it
        #   1 = item would be dropped inside
        #   2 = item would move before
        #   3 = item would move after
        #   4 = item can be inserted before or after
        #   5 = item can be inserted before or after or dropped inside
        return None # None = item cannot be dropped on it
    

    def GetNextItem(self):
        """ 
        Returns the next item in the tree.
        
        This would be the next visible item of the tree if all items were 
        expanded. So this can be used to forward traverse through the tree
        from any starting position.
        """
        
        if len(self.childs):
            return self.childs[0]
        while True:
            childs = self.parent.childs
            pos = childs.index(self) + 1
            if pos < len(childs):
                return childs[pos]
            self = self.parent
            if self.parent is None:
                return self


    def GetPreviousItem(self):
        """ 
        Returns the previous item in the tree.
        
        This would be the previous visible item of the tree if all items were 
        expanded. So this can be used to reverse traverse through the tree
        from any starting position.
        """
        parent = self.parent
        if parent is not None:
            childs = parent.childs
            pos = childs.index(self)
            if pos > 0:
                self = childs[pos - 1]
            else:
                return parent
        while len(self.childs):
            self = self.childs[-1]
        return self
    
    
    def __del__(self):
        eg.whoami()

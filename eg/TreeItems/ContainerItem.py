import wx
import eg
from TreeItems import TreeItem



class ContainerItem(TreeItem):
        
    def WriteToXML(self):
        attr, text, childs = TreeItem.WriteToXML(self)
        if self.isExpanded:
            attr.append(("Expanded", "True"))
        return attr, text, childs
    
    
    def __init__(self, parent, node):
        TreeItem.__init__(self, parent, node)
        self.childs = []
        for childNode in node:
            cls = self.document.XMLTag2ClassDict[childNode.tag]
            child = cls(self, childNode)
            self.childs.append(child)
        self.isExpanded = node.attrib.get("expanded") == "True"
        
            
    def CreateTreeItem(self, tree, parentId):
        id = TreeItem.CreateTreeItem(self, tree, parentId)
        if len(self.childs):
            tree.SetItemHasChildren(id, True)
            if self.isExpanded:
                tree.Expand(self.id)
        return id
            
        
    def CreateTreeItemAt(self, tree, parentId, pos):
        id = TreeItem.CreateTreeItemAt(self, tree, parentId, pos)
        if len(self.childs):
            tree.SetItemHasChildren(id, True)
            if self.isExpanded:
                tree.Expand(self.id)
        return id

    
    def DeleteTreeItem(self, tree):
        if self.id is not None:
            for child in self.childs:
                child.DeleteTreeItem(tree)
            tree.Delete(self.id)
            self.id = None
        
        
    def _Delete(self):
        for child in self.childs[:]:
            child._Delete()
        TreeItem._Delete(self)
        
        
#    def AskDelete(self):
#        """ Ask all children, if they are ready to be deleted """
#        if TreeItem.AskDelete(self) is False:
#            return False
#        for child in self.childs:
#            res = child.AskDelete()
#            if not res:
#                return False
#        return True
#
        
    def GetCount(self, count=0):
        for child in self.childs:
            count = child.GetCount(count)
        return count + 1


    def AddChild(self, child, pos=-1):
        childs = self.childs
        tree = self.tree
        id = self.id
        if len(childs) == 0 and id is not None:
            tree.SetItemHasChildren(id)
        if pos == -1 or pos >= len(childs):
            childs.append(child)
            pos = -1
        else:
            childs.insert(pos, child)
        if id is not None and (id == self.root.id or tree.IsExpanded(id)):
            child.CreateTreeItemAt(tree, id, pos)
            
            
    def RemoveChild(self, child):
        pos = self.childs.index(child)
        del self.childs[pos]
        tree = self.tree
        if child.id is not None:
            child.DeleteTreeItem(tree)
        if len(self.childs) == 0 and self.id is not None:
            tree.SetItemHasChildren(self.id, False)
        return pos
            
        
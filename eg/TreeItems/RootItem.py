import wx
import eg
from ContainerItem import ContainerItem
import pythoncom
import time


class RootItem(ContainerItem):
    xmlTag = "EventGhost"    
    iconIndex = eg.SetupIcons("root")
    time = None
    guid = None
    
    def WriteToXML(self):
        attr, text, childs = ContainerItem.WriteToXML(self)
        autostartMacro = self.document.autostartMacro
        childs = [autostartMacro]
        for child in self.childs:
            if child is not autostartMacro:
                childs.append(child)
        attr.append(('Version', str(eg.buildNum)))
        self.guid = str(pythoncom.CreateGuid())
        attr.append(('Guid', self.guid))
        self.time = str(time.time())
        attr.append(('Time', self.time))
        return attr, text, childs


    def __init__(self, parent, node):
        parent = None
        ContainerItem.__init__(self, parent, node)
        self.guid = node.attrib.get("guid")
        self.time = node.attrib.get("time")
        self.name = eg.text.General.configTree
         
        
    def CreateTreeItem(self, tree, parentId):
        self.id = tree.AddRoot(
            self.name,
            self.iconIndex, 
            -1, 
            wx.TreeItemData(self)
        )
        item = tree.AppendItem(self.id, '')
        font1 = tree.GetItemFont(self.id)
        tree.normalfont = font1
        tree.Delete(item)
        item = tree.AppendItem(self.id, '')
        tree.SetItemHasChildren(self.id, True)
        # evil workaround to get another font
        font2 = tree.GetItemFont(item)
        tree.Delete(item)
        font2.SetStyle(wx.FONTSTYLE_ITALIC)
        tree.italicfont = font2
        #for child in self.childs:
        #    child.CreateTreeItem(tree, self.id)
        return id


    def _Delete(self):
        childs = self.childs[:]
        for child in childs:
            child._Delete()


    def IsEditable(self):
        return False
    
    
    def CanCut(self):
        return False
    
    
    def CanCopy(self):
        return False
    
    
    def CanDelete(self):
        return False
    
    
    def CanDisable(self):
        return False
    
    
    def Enable(self, flag):
        pass
    
    
    def DropTest(self, cls):
        if cls == MacroItem:
            return 1 # 1 = item would be dropped inside
        if cls == FolderItem:
            return 1 # 1 = item would be dropped inside
        return None  # None = item cannot be dropped on it
    

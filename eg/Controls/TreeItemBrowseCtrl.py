import wx
import eg


class TreeItemBrowseCtrl(wx.TreeCtrl):
    
    def __init__(
        self, 
        parent, 
        filterFunc=None, 
        searchFunc=None, 
        selectItem=None,
        multiSelect=False
    ):
        if searchFunc is None:
            searchFunc = lambda obj, id: None

        self.filterFunc = filterFunc
        self.searchFunc = searchFunc
        style = (
            wx.TR_HAS_BUTTONS
            |wx.CLIP_CHILDREN
            |wx.NO_FULL_REPAINT_ON_RESIZE
        )
        if multiSelect:
            style |= wx.TR_MULTIPLE 
        wx.TreeCtrl.__init__(self, parent, style=style)
        self.SetMinSize((10, 10))
        self.SetImageList(eg.imageList)
        self.srcTree = srcTree = eg.mainFrame.treeCtrl

        srcRoot = srcTree.GetRootItem()
        text = srcTree.GetItemText(srcRoot)
        image = srcTree.GetItemImage(srcRoot)
        obj = srcTree.GetPyData(srcRoot)
        self.root = root = self.AddRoot(text, image)
        self.SetPyData(root, obj)
        
        self.normalfont = self.GetItemFont(self.root)
        # evil workaround to get another font
        id = self.AppendItem(self.root, '')
        self.italicfont = self.GetItemFont(id)
        self.Delete(id)
        self.italicfont.SetStyle(wx.FONTSTYLE_ITALIC)

        self.__collapsing = False
        self.Bind(wx.EVT_TREE_ITEM_EXPANDING, self.OnExpanding)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSING, self.OnCollapsing)
        self.SetItemHasChildren(root)
        self.Expand(root)
        self.ScrollTo(root)
        self.UnselectAll()
        if not selectItem:
            return
        item = selectItem
        path = []
        while item is not selectItem.tree.root:
            path.append(item)
            item = item.parent
        id = root
        for item in reversed(path):
            if not self.IsExpanded(id):
                self.Expand(id)
            tmp, cookie = self.GetFirstChild(id)
            while self.GetPyData(tmp) is not item:
                tmp, cookie = self.GetNextChild(tmp, cookie)
            id = tmp
        self.EnsureVisible(root)
        self.SelectItem(id)


    def OnCollapsing(self, event):
        # Be prepared, self.CollapseAndReset below may cause
        # another wx.EVT_TREE_ITEM_COLLAPSING event being triggered.
        id = event.GetItem()
        if self.__collapsing or id is self.root:
            event.Veto()
        else:
            self.__collapsing = True
            self.CollapseAndReset(id)
            self.SetItemHasChildren(id)
            self.__collapsing = False


    def OnExpanding(self, event):
        eg.whoami()
        id = event.GetItem()
        obj = self.GetPyData(id)
        for child in obj.childs:
            if not self.filterFunc(child):
                continue
            tmp = self.AppendItem(
                id,
                child.GetLabel(),
                child.iconIndex + (not child.isEnabled),
                -1,
                wx.TreeItemData(child)
            )
            for subChild in child.childs:
                if self.filterFunc(subChild):
                    self.SetItemHasChildren(tmp, True)
            child.SetAttributes(self, tmp)
            self.searchFunc(child, tmp)
            


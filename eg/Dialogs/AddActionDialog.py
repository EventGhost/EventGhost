import wx
import eg

gLastSelected = None


class DefaultConfig:
    position = None
    size = (550, 400)
    splitPosition = 210

config = eg.GetConfig("AddActionDialog", DefaultConfig)


class Text:
    title = "Select an action to add..."
    descriptionLabel = "Description"

Text = eg.GetTranslation(Text)


class AddActionDialog(eg.Dialog):
    
    def __init__(self, searchItem=None):
        self.resultData = None
        eg.Dialog.__init__(
            self, 
            None, 
            -1,
            Text.title, 
            style=wx.DEFAULT_DIALOG_STYLE
                |wx.RESIZE_BORDER
                |wx.THICK_FRAME
        )
        splitter = wx.SplitterWindow(
            self, 
            -1,
            style=wx.SP_LIVE_UPDATE
                |wx.CLIP_CHILDREN
                |wx.NO_FULL_REPAINT_ON_RESIZE
        )
        self.splitter = splitter

        style = wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT|wx.TR_FULL_ROW_HIGHLIGHT
        tree = wx.TreeCtrl(splitter, -1, style=style)
        tree.SetMinSize((100,100))
        tree.SetImageList(eg.imageList)
        self.tree = tree
        
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        tree.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnCollapsed)
        tree.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnExpanded)
       
        self.htmlTemplate = (
            '<html><body bgcolor="#%02X%02X%02X">%%s</body></html>' 
                % self.GetBackgroundColour().Get()
        )

        rightPanel = self.rightPanel = wx.Panel(splitter)
        rightSizer = self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightPanel.SetSizer(rightSizer)
        rightPanel.SetAutoLayout(True)
        
        self.nameText = nameText = wx.StaticText(rightPanel)
        nameText.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD))
        rightSizer.Add(nameText, 0, wx.EXPAND|wx.LEFT|wx.BOTTOM, 5)
        
        staticBoxSizer = wx.StaticBoxSizer(
            wx.StaticBox(rightPanel, label=Text.descriptionLabel),
            wx.VERTICAL
        )
        self.docText = eg.HtmlWindow(rightPanel)
        self.docText.SetBorders(2)
        
        staticBoxSizer.Add(self.docText, 1, wx.EXPAND)
        rightSizer.Add(staticBoxSizer, 1, wx.EXPAND, 5)
        
        splitter.SplitVertically(self.tree, rightPanel)
        splitter.SetMinimumPaneSize(60)
        splitter.UpdateSize()

        self.buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL))
        
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(splitter, 1, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(self.buttonRow.sizer, 0, wx.EXPAND)
        
        self.SetSizerAndFit(mainSizer)
        minSize = mainSizer.GetMinSize()
        self.SetMinSize(minSize)
        self.SetSize(config.size)
        self.splitter.SetSashPosition(config.splitPosition)
        if config.position is not None:
            self.SetPosition(config.position)
        self.ReloadTree()


    def FillTree(self, item, data):
        tree = self.tree
        for i in data:
            if isinstance(i, eg.ActionClass):
                iconIndex = i.info.iconIndex
                actionList = None
                name = i.name
            elif isinstance(i, eg.PluginClass):
                iconIndex = i.info.iconIndex + 2
                actionList = i.info.actionList
                i = i.info
                name = i.label
            elif isinstance(i, eg.ActionGroup):
                iconIndex = i.iconIndex
                actionList = i.actionList
                name = i.name
            else:
                raise "unknown type in FillTree", i
            tmp = tree.AppendItem(item, name)
            tree.SetPyData(tmp, i)
            tree.SetItemImage(tmp, iconIndex)
            if actionList:
                self.FillTree(tmp, actionList)
                if i.expanded:
                    tree.Expand(tmp)
            if i == gLastSelected:
                self.lastSelectedTreeItem = tmp
    
    
    def ReloadTree(self):
        tree = self.tree
        tree.DeleteAllItems()
        self.root = tree.AddRoot("Functions")
        self.lastSelectedTreeItem = None
        self.FillTree(self.root, eg.actionList)
        
        if self.lastSelectedTreeItem:
            item = self.lastSelectedTreeItem
            while True:
                item = tree.GetItemParent(item)
                if item == self.root:
                    break
                tree.EnsureVisible(item)
            tree.SelectItem(self.lastSelectedTreeItem)
        
        
    def OnSelectionChanged(self, event):
        item = event.GetItem()
        if not item.IsOk():
            return
        data = self.tree.GetPyData(item)
        if isinstance(data, eg.ActionClass):
            self.resultData = data
            self.buttonRow.okButton.Enable(True)
            info = data.plugin.info
        else:
            self.resultData = None
            self.buttonRow.okButton.Enable(False)
            if isinstance(data, eg.ActionGroup):
                info = data.plugin.info
            else:
                info = data
        self.nameText.SetLabel(data.name)
        self.docText.SetBasePath(info.path)
        self.docText.SetPage(self.htmlTemplate % data.description)
        
        
    def OnCollapsed(self, event):
        self.tree.GetPyData(event.GetItem()).expanded = False
        
        
    def OnExpanded(self, event):
        self.tree.GetPyData(event.GetItem()).expanded = True
        
        
    def OnActivated(self, event):
        item = self.tree.GetSelection()
        data = self.tree.GetPyData(item)
        if isinstance(data, eg.ActionClass):
            self.EndModal(wx.ID_OK)
        else:
            event.Skip()


    def Destroy(self):
        global gLastSelected
        item = self.tree.GetSelection()
        gLastSelected = self.tree.GetPyData(item)        
        config.size = self.GetSizeTuple()
        config.position = self.GetPositionTuple()
        config.splitPosition = self.splitter.GetSashPosition()
        eg.Dialog.Destroy(self)
        
        


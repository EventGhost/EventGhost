import wx
import eg
from eg.Controls.TreeItemBrowseCtrl import TreeItemBrowseCtrl
from eg.Controls.SizeGrip import SizeGrip


class TreeItemBrowseDialog(eg.Dialog):
    
    def __init__(self, title, text, searchItem, resultClasses):
        self.resultData = searchItem
        self.resultClasses = resultClasses
        self.foundId = None
        style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
        wx.Dialog.__init__(self, None, -1, title=title, style=style)
        staticText = wx.StaticText(self, -1, text)
        
        filterClasses = (eg.FolderItem, eg.MacroItem)
        def filterFunc(obj):
            return isinstance(obj, filterClasses)
        
        tree = TreeItemBrowseCtrl(self, filterFunc, selectItem=searchItem)
        tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        self.treeCtrl = tree
        
        okButton = wx.Button(self, wx.ID_OK, eg.text.General.ok)
        self.okButton = okButton
        
        cancelButton = wx.Button(self, wx.ID_CANCEL, eg.text.General.cancel)

        stdbtnsizer = wx.StdDialogButtonSizer()
        stdbtnsizer.AddButton(okButton)
        stdbtnsizer.AddButton(cancelButton)
        okButton.SetDefault()
        stdbtnsizer.Realize()
        
        btnrowSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnrowSizer.Add((5,5), 1)
        btnrowSizer.Add(stdbtnsizer, 0, wx.TOP|wx.BOTTOM, 6)
        btnrowSizer.Add((2,2), 0)
        btnrowSizer.Add(SizeGrip(self), 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(staticText, 0, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(tree, 1, wx.EXPAND)
        mainSizer.Add(btnrowSizer, 0, wx.EXPAND)

        self.SetSizerAndFit(mainSizer)
        #self.SetMinSize(self.GetSize())
        self.SetSize((450,400))
        if not searchItem:
            okButton.Enable(False)
        self.Centre()


    def OnSelectionChanged(self, event):
        item = event.GetItem()
        if item.IsOk():
            obj = self.treeCtrl.GetPyData(item)
            if isinstance(obj, self.resultClasses):
                self.resultData = obj
                self.okButton.Enable(True)
            else:
                self.okButton.Enable(False)
        event.Skip()


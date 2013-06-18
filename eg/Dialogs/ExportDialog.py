import eg
import wx
from eg.Controls.TreeItemBrowseCtrl import TreeItemBrowseCtrl
from eg.Controls.SizeGrip import SizeGrip


class ExportDialog(eg.Dialog):
    
    def __init__(self):
        self.foundId = None
        style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
        wx.Dialog.__init__(self, None, -1, title="Export", style=style)
        staticText = wx.StaticText(self, -1, "Please select the items you want to export")
        
        filterClasses = (eg.FolderItem, eg.MacroItem)
        def filterFunc(obj):
            return isinstance(obj, filterClasses)
        
        tree = TreeItemBrowseCtrl(self, filterFunc, multiSelect=True)
        #tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectionChanged)
        tree.UnselectAll()
        self.treeCtrl = tree
        
        okButton = wx.Button(self, wx.ID_OK, eg.text.General.ok)
        self.okButton = okButton
        okButton.Bind(wx.EVT_BUTTON, self.OnOk)
        
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

        self.SetSizer(mainSizer)
        self.SetAutoLayout(True)
        mainSizer.Fit(self)
        #self.SetMinSize(self.GetSize())
        self.SetSize((450, 400))
        self.Centre()
        
        
    def OnOk(self, event):
        eg.whoami()
        items = self.treeCtrl.GetSelections()
        GetPyData = self.treeCtrl.GetPyData
        self.resultData = [GetPyData(item) for item in items]
        event.Skip()
    
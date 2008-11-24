import eg
import wx
import wx.gizmos

class NamespaceTree(wx.gizmos.TreeListCtrl):
    
    def __init__(self, parent, namespace):
        self.namespace = namespace
        wx.gizmos.TreeListCtrl.__init__(
            self,
            parent, 
            style = wx.TR_FULL_ROW_HIGHLIGHT 
                |wx.TR_DEFAULT_STYLE
                |wx.VSCROLL
                |wx.ALWAYS_SHOW_SB 
                #|wx.CLIP_CHILDREN
        )
        self.AddColumn("Name")
        self.AddColumn("Type")
        self.AddColumn("Value")
        
        
    def FillTree(self):
        root = self.AddRoot("Root")
        for name, value in self.namespace.__dict__.items():
            item = self.AppendItem(root, name)
            typeStr = str(type(value))
            if typeStr.startswith("<class "):
                typeStr = "class"
            else:
                typeStr = typeStr[7:-2]
            self.SetItemText(item, typeStr, 1)
            valueStr = repr(value)
            self.SetItemText(item, valueStr, 2)
            self.SetPyData(item, value)
        self.Expand(root)
            
            
    @classmethod
    def Test(cls):
        dialog = eg.Dialog(None, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        tree = cls(dialog, eg)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(tree, 1, wx.EXPAND)
        tree.FillTree()
        dialog.SetSizerAndFit(sizer)
        dialog.ShowModal()
        dialog.Destroy()
        
        
        
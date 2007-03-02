import eg
import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin


class LinkList(wx.ListCtrl, ListCtrlAutoWidthMixin):
    
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_REPORT|wx.LC_VIRTUAL)
        ListCtrlAutoWidthMixin.__init__(self)
        self.SetImageList(eg.imageList, wx.IMAGE_LIST_SMALL)
        self.InsertColumn(0, "ID")
        self.InsertColumn(1, "Item Label")
        self.SetItemCount(1)
    
    
    def OnGetItemColumnImage(self, item, column):
        return 5
        if column == 0:
            return 5
        else:
            return -1
    
    
    def OnGetItemText(self, item, column):
        return "huhu"
    
    
    
class LinkListDialog(eg.Dialog):
    
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE
        if eg.debugLevel:
            style |= wx.RESIZE_BORDER
        eg.Dialog.__init__(self, parent, title="Edit Item Links", style=style)
        
        listCtrl = LinkList(self)
        
        addButton = wx.Button(self, -1, "Add")
        deleteButton = wx.Button(self, -1, "Delete")
        buttonRow = eg.ButtonRow(self, (wx.ID_OK, wx.ID_CANCEL))
        
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add((10, 10), 1)
        btnSizer.Add(addButton)
        btnSizer.Add((10, 10))
        btnSizer.Add(deleteButton)
        btnSizer.Add((10, 10), 1)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(listCtrl, 1, wx.EXPAND)
        sizer.Add(btnSizer, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 5)
        sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALIGN_CENTER)
        sizer.Add(buttonRow.sizer, 0, wx.EXPAND)
        
        self.SetSizerAndFit(sizer)



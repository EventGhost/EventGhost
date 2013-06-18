import wx
import eg
from eg.Dialogs.TreeItemBrowseDialog import TreeItemBrowseDialog


class BrowseMacroButton(wx.Window):
    
    def __init__(self, parent, label, title, mesg, macro=None):
        if macro is None:
            macro_name = ""
        else:
            macro_name = macro.name
        self.title = title
        self.mesg = mesg
        self.macro = macro
        wx.Window.__init__(self, parent, -1)
        self.textBox = eg.StaticTextBox(self, -1, macro_name, size=(200,-1))
        self.button = wx.Button(self, -1, label)
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.textBox, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(self.button, 0, wx.LEFT, 5)
        self.SetSizer(sizer)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.Layout()


    def OnSetFocus(self, event):
        self.button.SetFocus()
        
        
    def OnSize(self, event):
        if self.GetAutoLayout():
            self.Layout()

        
    def OnButton(self, event):
        macro = TreeItemBrowseDialog(
            self.title,
            self.mesg, 
            self.macro, 
            (eg.MacroItem,)
        ).DoModal()
        if macro:
            self.textBox.SetLabel(macro.name)
            self.macro = macro
            
            
    def GetValue(self):
        return self.macro

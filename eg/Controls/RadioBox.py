import wx

class RadioBox(wx.Panel):
    
    def __init__(
        self,
        parent = None,
        id = -1,
        label = "",
        pos = (-1, -1),
        size = (-1, -1),
        choices = (),
        majorDimension = 0,
        style = wx.RA_SPECIFY_COLS,
        validator = wx.DefaultValidator,
        name = "radioBox"
    ):
        self.value = 0
        wx.Panel.__init__(self, parent, id, pos, size, name=name)
        sizer = self.sizer = wx.GridSizer(len(choices), 1, 6, 6)
        style = wx.RB_GROUP
        for i, choice in enumerate(choices):
            radioButton = wx.RadioButton(self, i, choice, style=style)
            style = 0
            self.sizer.Add(radioButton, 0, wx.EXPAND)
            radioButton.Bind(wx.EVT_RADIOBUTTON, self.OnSelect)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.Layout()
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_SIZE, self.OnSize)


    def OnSize(self, event):
        if self.GetAutoLayout():
            self.Layout()

    
    def OnSelect(self, event):
        self.value = event.GetId()
        newEvent = wx.CommandEvent(wx.EVT_RADIOBOX.evtType[0], self.GetId())
        newEvent.SetInt(self.value)
        self.ProcessEvent(newEvent)
        
        
    def SetSelection(self, selection):
        self.FindWindowById(selection).SetValue(True)
        self.value = selection
    
    
    def GetSelection(self):
        return self.value
    
    
        
        
        
        
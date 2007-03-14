import wx
            
            
class DisplayChoice(wx.Choice):
    
    def __init__(self, parent, id=-1, display=0):
        numDisplays = wx.Display().GetCount()
        choices = ["Monitor %d" % (i+1) for i in range(numDisplays)]
        wx.Choice.__init__(self, parent, id, choices=choices)
        self.SetSelection(display)                        

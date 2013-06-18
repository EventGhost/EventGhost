import wx
            
            
class DisplayChoice(wx.Choice):
    
    def __init__(self, parent, id=-1, display=0):
        choices = []
        num_displays = wx.Display().GetCount()
        for i in xrange(0, num_displays):
            choices.append("Monitor %d" % (i+1))
        wx.Choice.__init__(self, parent, id, choices=choices)
        self.SetSelection(display)                        

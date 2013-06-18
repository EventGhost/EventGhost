import wx


class Dialog(wx.Dialog):
    
    def DoModal(self):
        result = None
        if self.ShowModal() == wx.ID_OK and hasattr(self, "resultData"):
            result = self.resultData
        self.Destroy()
        return result

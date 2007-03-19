import wx
from RadioButtonGrid import RadioButtonGrid


class CheckBoxGrid(RadioButtonGrid):
    CtrlType = wx.CheckBox
    
    def GetValue(self):
        result = []
        for column in self.ctrlTable:
            value = 0
            for i, ctrl in enumerate(column):
                if ctrl.GetValue():
                    value |= (1 << i)
            result.append(value)
        return result
            
            
    def SetValue(self, value):
        for x, val in enumerate(value):
            column = self.ctrlTable[x]
            for i, ctrl in enumerate(column):
                ctrl.SetValue(val & (1 << i))
            
            

import math
import locale
import wx
from wx.lib import masked


localedict = locale.localeconv()

class SpinNumCtrl(wx.Window):
    _default_args = {
        "integerWidth": 3,
        "fractionWidth": 2,
        "allowNegative": False,
        "min": 0,
        "limited": True,
        "groupChar": localedict['thousands_sep'],
        "decimalChar": localedict['decimal_point'],
    }
    
    def __init__(
        self, 
        parent, 
        id=-1,
        value = 0.0,
        pos = wx.DefaultPosition,
        size = wx.DefaultSize,
        style = wx.TE_RIGHT,
        validator = wx.DefaultValidator,
        name = "eg.SpinNumCtrl", 
        **kwargs
    ):
        if kwargs.has_key("increment"):
            self.increment = kwargs["increment"]
            del kwargs["increment"]
        else:
            self.increment = 1

        new_args = self._default_args.copy()
        if kwargs.has_key("min"):
            if kwargs["min"] < 0:
                new_args["allowNegative"] = True
                
        new_args.update(kwargs)
        wx.Window.__init__(self, parent, id, pos, size, style)
        numCtrl = masked.NumCtrl(
            self, 
            -1, 
            value, 
            pos, 
            size, 
            style,
            validator, 
            name, 
            **new_args
        )
        numCtrl.SetLimited(True)
        w, h = numCtrl.GetSize()
        spinbutton = wx.SpinButton(
            self, 
            -1, 
            style=wx.SP_VERTICAL,
            size=(h*2/3, h)
        )
        spinbutton.MoveBeforeInTabOrder(numCtrl)
        self.spinbutton = spinbutton
        numCtrl.Bind(wx.EVT_CHAR, self.OnChar)
        spinbutton.Bind(wx.EVT_SPIN_UP, self.OnSpinUp)
        spinbutton.Bind(wx.EVT_SPIN_DOWN, self.OnSpinDown)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(numCtrl, 1, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(spinbutton, 0, wx.ALIGN_CENTER)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.Layout()
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.numCtrl = numCtrl


    def OnSize(self, event):
        if self.GetAutoLayout():
            self.Layout()


    def OnSetFocus(self, event):
        self.numCtrl.SetFocus()
        
        
    def OnSpinUp(self, event):
        value = self.numCtrl.GetValue() + self.increment
        minValue, maxValue = self.numCtrl.GetBounds()
        if maxValue is not None and value > maxValue:
            value = maxValue
        if minValue is not None and value < minValue:
            value = minValue
        self.numCtrl.SetValue(value)
        
        
    def OnSpinDown(self, event):
        value = self.numCtrl.GetValue() - self.increment
        minValue, maxValue = self.numCtrl.GetBounds()
        if maxValue is not None and value > maxValue:
            value = maxValue
        if minValue is not None and value < minValue:
            value = minValue
        self.numCtrl.SetValue(value)
    
    
    def OnChar(self, event):
        key = event.GetKeyCode()
        if key == wx.WXK_UP:
            self.OnSpinUp(event)
            return
        if key == wx.WXK_DOWN:
            self.OnSpinDown(event)
            return
        event.Skip()
        
        
    def GetValue(self):
        return self.numCtrl.GetValue()


    def SetValue(self, value):
        minValue, maxValue = self.numCtrl.GetBounds()
        if maxValue is not None and value > maxValue:
            value = maxValue
        if minValue is not None and value < minValue:
            value = minValue
        return self.numCtrl.SetValue(value)



class SpinIntCtrl(SpinNumCtrl):
    
    def __init__(
        self, 
        parent, 
        id=-1, 
        value=0, 
        min=0, 
        max=None, 
        size=(-1,-1), 
        style=0
    ):
        allowNegative = bool(min < 0)
        if max is None:
            integerWidth = 5
        else:
            integerWidth = int(math.ceil(math.log10(max + 1)))
        SpinNumCtrl.__init__(
            self, 
            parent, 
            id, 
            value, 
            min=min, 
            max=max,
            size=size, 
            allowNegative=allowNegative, 
            groupDigits = False,
            fractionWidth=0,
            integerWidth=integerWidth
        )

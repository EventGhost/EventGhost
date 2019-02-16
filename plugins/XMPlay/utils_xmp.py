# -*- coding: utf-8 -*-
#


import eg



class IntSetter(eg.ActionBase):
    """Indexing here begins from zero."""
    
    def Configure(self, value=0, from_eg_result=False):
        panel = eg.ConfigPanel()
        valueControl = panel.SpinIntCtrl(value)
        valueControl.Enable(not from_eg_result)
        fromControl = panel.CheckBox(from_eg_result, self.plugin.text.from_eg_result)
        def egresultOn(evt):
            if evt.IsChecked():
                valueControl.Enable(False)
                valueControl.SetValue(0)
            else:
                valueControl.Enable()
        fromControl.Bind(wx.EVT_CHECKBOX, egresultOn)
        panel.AddCtrl(valueControl)
        panel.AddCtrl(fromControl)
        while panel.Affirmed():
            panel.SetResult(valueControl.GetValue(), fromControl.GetValue())

            
            
class TextSetter(eg.ActionBase):

    def Configure(self, value="", from_eg_result=False):
        panel = eg.ConfigPanel()
        valueControl = panel.TextCtrl(value)
        valueControl.Enable(not from_eg_result)
        fromControl = panel.CheckBox(from_eg_result, self.plugin.text.from_eg_result)
        def fromOn(evt):
            if evt.IsChecked():
                valueControl.Enable(False)
                valueControl.SetValue("")
            else:
                valueControl.Enable()
        fromControl.Bind(wx.EVT_CHECKBOX, fromOn)
        #panel.AddCtrl(valueControl)
        panel.sizer.Add(valueControl, 0, wx.EXPAND | wx.BOTTOM, 10)
        panel.AddCtrl(fromControl)
        while panel.Affirmed():
            panel.SetResult(valueControl.GetValue().strip(), fromControl.GetValue())
            
            
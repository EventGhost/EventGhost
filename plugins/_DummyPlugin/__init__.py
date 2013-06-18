import eg
import wx

class DummyPlugin(eg.PluginClass):

    def __init__(self):
        eg.whoami()
        self.AddAction(DummyAction)
        
        
    def __start__(self, *args):
        eg.whoami()
        
        
    def __stop__(self):
        eg.whoami()
        
        
    def __close__(self):
        eg.whoami()
        
        
    def Configure(self, *args):
        eg.whoami()
        dialog = eg.ConfigurationDialog(self, resizeable=True)
        choices = ["option1", "option2", "option3"]
        ctrls = []
        for choice in choices:
            ctrl = wx.CheckBox(dialog, -1, choice)
            dialog.sizer.Add(ctrl)
            dialog.sizer.Add((5,5))
            ctrls.append(ctrl)
        args = ({"huhu": 1},)
        if dialog.AffirmedShowModal():
            for ctrl in ctrls:
                ctrl.GetValue()
            return args
    
    


class DummyAction(eg.ActionClass):
    
    def __call__(self, *args):
        pass
        
    
    

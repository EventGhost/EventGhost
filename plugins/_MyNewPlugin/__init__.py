import eg
import wx

print "MyNewPlugin module code gets loaded."


class MyNewPlugin(eg.PluginClass):

    def Configure(self, myString=""):
        dialog = eg.ConfigurationDialog(self)
        textControl = wx.TextCtrl(dialog, -1, myString)
        dialog.sizer.Add(textControl, 1, wx.EXPAND)
        if dialog.AffirmedShowModal():
            return (textControl.GetValue(), )
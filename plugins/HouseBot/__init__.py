import eg

eg.RegisterPlugin(
    name = "HouseBot",
    author = "Allan Stevens",
    version = "0.0.2",
    kind = "program",
    description = (
        "Adds actions to control <a href='http://www.housebot.com' target='_blank'>HouseBot</a> home automation software.<br><br>"
        "<b>Notice:</b> This device requires the External Control Device installed in HouseBot and the HBControlMod.dll to be registered on the EventGhost PC."   
    ),
	guid = "{a2492ac6-3e8c-49d3-9ff5-d47003b63cd2}",
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=3868",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz"
        "AAAK8AAACvABQqw0mAAAACB0RVh0U29mdHdhcmUATWFjcm9tZWRpYSBGaXJld29ya3MgTVi7kSok"
        "AAACoklEQVR4nI2TS2iUZxSGn++/zGSshliSqsXGXMxksrDShi6solBwV3DVRTcutLqKCxFLIboo"
        "lG5KScGdzaJSKLqqrYhVjKHebw2iKFhNAtFJdHRmkjiTycz3/9/bRS5YMKUHzuY973l4OXCMJJaq"
        "C8b0A4VPpC+XNEl6Y1+EL3LpdDXb0lI6D58v5Xuj+Kfn9RQznXq+8QOVPt6iXFurBmDv/wJc8v2e"
        "ya5OTXSkde/36+7xH7fd9IfdetnWqkHY95+AS77fM9WV0Xh7h3vw6+W4LLlZSSMDQ8p3f6R8e6su"
        "et6B13fMwhGvhGHPho71R2aiWKW+Y26i+X3v+UjWuBjezayhuZQltW8X4ctn3B970rvZ2m8Xj3gt"
        "mdwz1ZXRs86Mu3/yamQld/rsY93NWt16YHXqzLCqkh7dHtX45m2abGvRnYaG3p8h5V0wZn/Huuaj"
        "NghU7Dvm3tuxyQ/ASIahwVHuXh3FGDBAY3cL5R9PUG5u5+1U8pt3YA/nIHVrWf3Bk18fj2YklSWV"
        "JBUkjeSl4YL0QlJxXnsl6cwvf6k/1bZTEsF2qQJ8d+/434dDWFEBXBxRGvqBumQNOVEZa+KtjXsR"
        "c0kqTY0c/nTw8m7AAzDmszpmZ20ECKiVZghffcWqhl5WrzxEnO0nisAx19gaG8YGEiwA4EoUxy5y"
        "8wBnPMLkMjwLVAxeop7FGeAEthpHrwEmojhWLZ43yIBqBiKYydURVee0hQQS2GpkFwGSCBNe1Qd8"
        "wAsNQWzBwvL6CqlUjOfPzXzA+IbKdC0GCBaeqpivRA8fFQgSPrXZKsHTNJPTBbCQs40wPI0xMYGg"
        "mCvTtHaF+xdgfGzqt5/6bmwLQl8Y3w+87xOy1YQxhARBaG/eCJALhRKB7+W37kiXAf4BVjbT9bje"
        "pcQAAAAASUVORK5CYII="
    ),
)

import win32com.client

class HouseBotPlugin(eg.PluginBase):

    def __init__(self):
        self.AddAction(SetPropertyValue)
        self.AddAction(SetModeState)
        self.AddAction(ExecuteTask)
        self.AddAction(BlankRemoteScreen)
        self.AddAction(OpenRemotePanel)
        self.AddAction(CloseRemotePanel)
        self.AddAction(ExecuteRemoteApp)
        self.AddAction(MinimizeRemote)
        self.AddAction(RestoreRemote)

    def __start__(self, server="127.0.0.1", port = "1234", password = "password"):
        self.server = server
        self.port = port
        self.password = password
        
    def Configure(self, server="127.0.0.1", port = "1234", password = "password"):
        panel = eg.ConfigPanel()
        serverControl = wx.TextCtrl(panel, -1, server)
        portControl = wx.TextCtrl(panel, -1, port)
        passwordControl = wx.TextCtrl(panel, -1, password)
        serverText = panel.StaticText("HouseBot Server")
        portText = panel.StaticText("Port")
        passwordText  = panel.StaticText("Password")
        panel.sizer.Add(serverText, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(serverControl, 0, wx.EXPAND)
        panel.sizer.Add((-1, 10))
        panel.sizer.Add(portText, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(portControl, 0, wx.EXPAND)
        panel.sizer.Add((-1, 10))
        panel.sizer.Add(passwordText, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(passwordControl, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(serverControl.GetValue(), portControl.GetValue(), passwordControl.GetValue())
            
            
class SetPropertyValue(eg.ActionBase):
    name = "Set Property Value"
    description = "Sets the property value of a device"

    def __call__(self, par1="", par2="", par3=""):
        obj = win32com.client.Dispatch("HBControlMod.HBControl")
        hbResponse = obj.Connect(self.plugin.port, self.plugin.server, self.plugin.password)
        if hbResponse == "OK":
            par1 = eg.ParseString(par1)
            par2 = eg.ParseString(par2)
            par3 = eg.ParseString(par3)
            obj.SetPropertyValue(par1, par2, par3)
            print "SetPropertyValue sent"
        else:
            print "Error: " + hbResponse
        obj = None
        
    def Configure(self, par1="", par2="", par3=""):
        panel = eg.ConfigPanel()
        par1Control = wx.TextCtrl(panel, -1, par1)
        par2Control = wx.TextCtrl(panel, -1, par2)
        par3Control = wx.TextCtrl(panel, -1, par3)
        par1Text = panel.StaticText("Specifies the Device Name for the Value to set")
        par2Text = panel.StaticText("Specifies the Property Description for the Value to set")
        par3Text  = panel.StaticText("Specifies the new Property Value")
        footerText = panel.StaticText("\nExpressions are allowed for example {eg.event.payload[0]} returns the first payload.")
        panel.sizer.Add(par1Text, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par1Control, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par2Text, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par2Control, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par3Text, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par3Control, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(footerText, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(par1Control.GetValue(),par2Control.GetValue(),par3Control.GetValue())


class SetModeState(eg.ActionBase):
    name = "Set Mode State"
    description = "Sets the mode to Active to Inactive"

    def __call__(self, par1="", par2=""):
        obj = win32com.client.Dispatch("HBControlMod.HBControl")
        hbResponse = obj.Connect(self.plugin.port, self.plugin.server, self.plugin.password)
        if hbResponse == "OK":
            par1 = eg.ParseString(par1)
            par2 = eg.ParseString(par2)
            obj.SetModeState(par1, par2)
            print "SetModeState sent"
        else:
            print "Error: " + hbResponse
        obj = None
        
    def Configure(self, par1="", par2=""):
        panel = eg.ConfigPanel()
        par1Control = wx.TextCtrl(panel, -1, par1)
        par2Control = wx.TextCtrl(panel, -1, par2)
        par1Text = panel.StaticText("Specifies the name of the Mode to change state")
        par2Text = panel.StaticText("Specifies the new mode state.  Valid values are Active or Inactive")
        footerText = panel.StaticText("\nExpressions are allowed for example {eg.event.payload[0]} returns the first payload.")
        panel.sizer.Add(par1Text, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par1Control, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par2Text, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par2Control, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(footerText, 0, wx.EXPAND)
        
        while panel.Affirmed():
            panel.SetResult(par1Control.GetValue(),par2Control.GetValue())


class BlankRemoteScreen(eg.ActionBase):
    name = "Blank Remote Screen"
    description = "Switches off Software Remote screen"

    def __call__(self):
        obj = win32com.client.Dispatch("HBControlMod.HBControl")
        hbResponse = obj.Connect(self.plugin.port, self.plugin.server, self.plugin.password)
        if hbResponse == "OK":
            obj.BlankRemoteScreen()
            print "BlankRemoteScreen sent"
        else:
            print "Error: " + hbResponse
        obj = None


class CloseRemotePanel(eg.ActionBase):
    name = "Close Remote Panel"
    description = "Closes the Software Remote Panel"

    def __call__(self, par1=""):
        obj = win32com.client.Dispatch("HBControlMod.HBControl")
        hbResponse = obj.Connect(self.plugin.port, self.plugin.server, self.plugin.password)
        if hbResponse == "OK":
            par1 = eg.ParseString(par1)
            obj.CloseRemotePanel(par1)
            print "CloseRemotePanel sent"
        else:
            print "Error: " + hbResponse
        obj = None
        
    def Configure(self, par1=""):
        panel = eg.ConfigPanel()
        par1Control = wx.TextCtrl(panel, -1, par1)
        par1Text = panel.StaticText("Specifies the name of the Panel to close")
        footerText = panel.StaticText("\nExpressions are allowed for example {eg.event.payload[0]} returns the first payload.")
        panel.sizer.Add(par1Text, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par1Control, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(footerText, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(par1Control.GetValue())


class OpenRemotePanel(eg.ActionBase):
    name = "Open Remote Panel"
    description = "Opens the Software Remote Panel"

    def __call__(self, par1=""):
        obj = win32com.client.Dispatch("HBControlMod.HBControl")
        hbResponse = obj.Connect(self.plugin.port, self.plugin.server, self.plugin.password)
        if hbResponse == "OK":
            par1 = eg.ParseString(par1)
            obj.OpenRemotePanel(par1)
            print "OpenRemotePanel sent"
        else:
            print "Error: " + hbResponse
        obj = None
        
    def Configure(self, par1=""):
        panel = eg.ConfigPanel()
        par1Control = wx.TextCtrl(panel, -1, par1)
        par1Text = panel.StaticText("Specifies the name of the Panel to open")
        footerText = panel.StaticText("\nExpressions are allowed for example {eg.event.payload[0]} returns the first payload.")
        panel.sizer.Add(par1Text, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par1Control, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(footerText, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(par1Control.GetValue())


class ExecuteRemoteApp(eg.ActionBase):
    name = "Execute Remote Application"
    description = "Executes an Application on the Software Remotes"

    def __call__(self, par1="", par2=""):
        obj = win32com.client.Dispatch("HBControlMod.HBControl")
        hbResponse = obj.Connect(self.plugin.port, self.plugin.server, self.plugin.password)
        if hbResponse == "OK":
            par1 = eg.ParseString(par1)
            par2 = eg.ParseString(par2)
            obj.ExecuteRemoteApp(par1, par2)
            print "ExecuteRemoteApp sent"
        else:
            print "Error: " + hbResponse
        obj = None
        
    def Configure(self, par1="", par2=""):
        panel = eg.ConfigPanel()
        par1Control = wx.TextCtrl(panel, -1, par1)
        par2Control = wx.TextCtrl(panel, -1, par2)
        par1Text = panel.StaticText("Specifies the application path")
        par2Text = panel.StaticText("Specifies the application arguments")
        footerText = panel.StaticText("\nExpressions are allowed for example {eg.event.payload[0]} returns the first payload.")
        panel.sizer.Add(par1Text, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par1Control, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par2Text, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par2Control, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(footerText, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(par1Control.GetValue(),par2Control.GetValue())


class ExecuteTask(eg.ActionBase):
    name = "Execute Task"
    description = "Executes a task"

    def __call__(self, par1=""):
        obj = win32com.client.Dispatch("HBControlMod.HBControl")
        hbResponse = obj.Connect(self.plugin.port, self.plugin.server, self.plugin.password)
        if hbResponse == "OK":
            par1 = eg.ParseString(par1)
            obj.ExecuteTask(par1)
            print "ExecuteTask sent"
        else:
            print "Error: " + hbResponse
        obj = None
        
    def Configure(self, par1=""):
        panel = eg.ConfigPanel()
        par1Control = wx.TextCtrl(panel, -1, par1)
        par1Text = panel.StaticText("Specifies the name of the Task to execute.")
        footerText = panel.StaticText("\nExpressions are allowed for example {eg.event.payload[0]} returns the first payload.")
        panel.sizer.Add(par1Text, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(par1Control, 0, wx.EXPAND)
        panel.sizer.Add((-1, 2))
        panel.sizer.Add(footerText, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(par1Control.GetValue())


class MinimizeRemote(eg.ActionBase):
    name = "Minimize Remote"
    description = "Minimizes the Software Remotes"

    def __call__(self):
        obj = win32com.client.Dispatch("HBControlMod.HBControl")
        hbResponse = obj.Connect(self.plugin.port, self.plugin.server, self.plugin.password)
        if hbResponse == "OK":
            obj.MinimizeRemote()
            print "MinimizeRemote sent"
        else:
            print "Error: " + hbResponse
        obj = None


class RestoreRemote(eg.ActionBase):
    name = "Restore Remote"
    description = "Restores the Software Remotes"

    def __call__(self):
        obj = win32com.client.Dispatch("HBControlMod.HBControl")
        hbResponse = obj.Connect(self.plugin.port, self.plugin.server, self.plugin.password)
        if hbResponse == "OK":
            obj.RestoreRemote()
            print "RestoreRemote sent"
        else:
            print "Error: " + hbResponse
        obj = None

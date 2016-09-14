#
# plugins/TellStick/__init__.py
#
# Copyright (C) 2008 Telldus Technologies
#


eg.RegisterPlugin(
    name = "TellStick",
    author = "Micke Prag",
    version = "1.2.2",
    kind = "external",
    guid = "{9ECBA250-AF41-4372-B64B-E42F2C2F2975}",
    url = "http://www.eventghost.org/forum/viewtopic.php?t=455",
    description = 'Plugin to control TellStick devices.',
    help = """
        <a href="http://www.telldus.se">Telldus Hompage</a>

        <center><img src="tellstick.png" /></center>
    """,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAAZi"
        "S0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9gDGxAtBidu"
        "wgYAAAGjSURBVDjL7ZIxaxphAIbfqxIvcuoVDpJcliDoYikdJNBDCTWQIXQqJXTJlKF7"
        "/4FLnTs4OARcpBJMliQki2QQpA6KioeQHNpioVG+Xr8e33lX8L7rFtIh0B+QZ3+f4eEF"
        "HvkvJEkKFIvFrXa7/Wk0Go2Hw+GoUqnsAoDw0CgSiTwpFApZTdP2ZFl+Y1nWqiRJmEwm"
        "yGQyYIz5zWbzwz+CWCwm5PN5LZvN7imK8lZVVbXVaqHX60EURSQSCaRSKYiiCEIIdF13"
        "7wTRaDTWaDS68Xh8IxQKoV6vw/M8hMNhpNNpBAIBUEoxnU4xm81AKQWllAcBQHu5Kb0/"
        "2H/3+9fPDddVIQgCcrkcFosFTNOEYRgghIBSCs45OOdwHKdvmuahcHpcOVpZUV4/leXl"
        "dXUNnf4NlNV1MMZACIFlWeCcw/d9zOfzsW3b1U6nUy2Xy30ACH77+iP54vmz5RtjjD+O"
        "B8di6N5277q4rnvLGDsaDAafa7VaixDi3+8WPLu43AktLV0mE0mq69fVk/PzL6+2tz9y"
        "zr8bhlErlUpXtm17j2d+mL+2ksVgUYb12AAAAABJRU5ErkJggg=="
    ),
)

TELLSTICK_TURNON       = 1
TELLSTICK_TURNOFF      = 2
TELLSTICK_BELL         = 4
TELLSTICK_TOGGLE       = 8
TELLSTICK_DIM          = 16

from ctypes import windll, c_char_p

class TellStick(eg.PluginClass):

    def __init__(self):
        self.AddAction(TurnOn)
        self.AddAction(Dim)
        self.AddAction(TurnOff)
        self.AddAction(Bell)

    def __start__(self):
        self.dll = None
        try:
            self.dll = windll.LoadLibrary("TellUsbD101.dll")
        except:
            raise eg.Exception("TellUsbD101.dll not found.")



class DeviceBase(object):

    def GetLabel(self, device):
        return self.name + " " + (c_char_p(self.plugin.dll.devGetName(device))).value

    def Configure(self, device=0):
        deviceList = []
        indexToIdMap = {}
        try:
            numDevices = self.plugin.dll.devGetNumberOfDevices()
        except:
            numDevices = 0
        selected = 0
        for i in range(numDevices):
            id = self.plugin.dll.devGetDeviceId(i)
            methods = self.plugin.dll.devMethods(id)
            if (methods & self.method):
                index = len(deviceList)
                name = (c_char_p(self.plugin.dll.devGetName(id))).value
                if (id == device):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name)
        if (len(deviceList) == 0):
            print "There is no devices supporting '" + self.name + "'"
            return
        panel = eg.ConfigPanel(self)
        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)
        panel.sizer.Add(
            wx.StaticText(panel, -1, "Device:"),
            0,
            wx.ALIGN_CENTER_VERTICAL
        )
        panel.sizer.Add(deviceCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        while panel.Affirmed():
            if self.plugin.dll is not None:
                device = indexToIdMap[deviceCtrl.GetSelection()]
            else:
                device = 0
            panel.SetResult(device)


class TurnOn(DeviceBase, eg.ActionClass):
    name = "Turn on"
    description = "Turns on a TellStick device."
    iconFile = "lamp-on"
    method = TELLSTICK_TURNON

    def __call__(self, device):
        ret = self.plugin.dll.devTurnOn(device)
        if (ret <> True):
            raise eg.Exception("An error occurred while trying to transmit")


class TurnOff(DeviceBase, eg.ActionClass):
    name = "Turn off"
    description = "Turns off a TellStick device."
    iconFile = "lamp-off"
    method = TELLSTICK_TURNOFF

    def __call__(self, device):
        ret = self.plugin.dll.devTurnOff(device)
        if (ret <> True):
            raise eg.Exception("An error occurred while trying to transmit")


class Bell(DeviceBase, eg.ActionClass):
    name = "Bell"
    description = "Sends bell to a TellStick device."
    iconFile = "bell"
    method = TELLSTICK_BELL

    def __call__(self, device):
        ret = self.plugin.dll.devBell(device)
        if (ret <> True):
            raise eg.Exception("An error occurred while trying to transmit")


class Dim(eg.ActionClass):
    name = "Dim"
    description = "Dims a TellStick device."
    iconFile = "lamp-dim"
    method = TELLSTICK_DIM

    def __call__(self, device, level):
        ret = self.plugin.dll.devDim(device, level)
        if (ret <> True):
            raise eg.Exception("An error occurred while trying to transmit")


    def GetLabel(self, device, level):
        percent = int((level*100)/256)
        return "Dim " + (c_char_p(self.plugin.dll.devGetName(device))).value + " to " + str(percent) + "%"


    def Configure(self, device=0, level=128):
        deviceList = []
        indexToIdMap = {}
        try:
            numDevices = self.plugin.dll.devGetNumberOfDevices()
        except:
            numDevices = 0
        selected = 0
        for i in range(numDevices):
            id = self.plugin.dll.devGetDeviceId(i)
            methods = self.plugin.dll.devMethods(id)
            if (methods & self.method):
                index = len(deviceList)
                name = (c_char_p(self.plugin.dll.devGetName(id))).value
                if (id == device):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name)
        if (len(deviceList) == 0):
            print "There is no devices supporting '" + self.name + "'"
            return
        panel = eg.ConfigPanel(self)
        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)
        levelCtrl = wx.Slider(panel, -1, level, 1, 254)
        panel.sizer.Add(
            wx.StaticText(panel, -1, "Device:"),
            0,
            wx.ALIGN_CENTER_VERTICAL
        )
        panel.sizer.Add(deviceCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        panel.sizer.Add(
            wx.StaticText(panel, -1, "Level:"),
            0,
            wx.ALIGN_CENTER_VERTICAL
        )
        panel.sizer.Add(levelCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        while panel.Affirmed():
            if self.plugin.dll is not None:
                device = indexToIdMap[deviceCtrl.GetSelection()]
                level = levelCtrl.GetValue()
            else:
                device = 0
            panel.SetResult(device, level)

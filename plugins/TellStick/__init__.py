#
# plugins/TellStick/__init__.py
#
# Copyright (C) 2007 Telldus Technologies
#


eg.RegisterPlugin(
    name = "TellStick",
    author = "Micke Prag",
    version = "0.1.1",
    kind = "external",
    url = "http://www.eventghost.org/forum/viewtopic.php?t=455",
    description = (
        '<p>Plugin to control TellStick devices.</p>'
        '\n\n<p><a href="http://www.telldus.se">Telldus Hompage</a></p>'
        '<center><img src="tellstick.png" /></center>'
    ),
)

from ctypes import windll, c_char_p

class TellStick(eg.PluginClass):

    def __init__(self):
        self.AddAction(TurnOn)
        self.AddAction(TurnOff)

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
        panel = eg.ConfigPanel(self)
        deviceList = []
        try:
            numDevices = self.plugin.dll.devGetNumberOfDevices()
        except:
            numDevices = 0
        selected = 0
        for i in range(numDevices):
            id = self.plugin.dll.devGetDeviceId(i)
            name = (c_char_p(self.plugin.dll.devGetName(id))).value
            if (id == device):
                selected = i
            deviceList.append(name)
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
                device = self.plugin.dll.devGetDeviceId(deviceCtrl.GetSelection())
            else:
                device = 0
            panel.SetResult(device)
            
            

class TurnOn(DeviceBase, eg.ActionClass):
    name = "Turn on"
    description = "Turns on a TellStick device."
    iconFile = "lamp-on"

    def __call__(self, device):
        ret = self.plugin.dll.devTurnOn(device)
        if (ret <> True):
            raise eg.Exception("An error occurred while trying to transmit")


class TurnOff(DeviceBase, eg.ActionClass):
    name = "Turn off"
    description = "Turns off a TellStick device."
    iconFile = "lamp-off"

    def __call__(self, device):
        ret = self.plugin.dll.devTurnOff(device)
        if (ret <> True):
            raise eg.Exception("An error occurred while trying to transmit")

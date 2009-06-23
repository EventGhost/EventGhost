import eg

eg.RegisterPlugin(
    name = "TechniSat USB IR Receiver",
    author = "Bitmonster",
    version = "1.0.0",
    kind = "remote",
    description = 'Plugin for the TechniSat USB IR Receiver.',
)

CODES = {
    (1, 0, 8, 0): "Epg",
    (1, 0, 9, 0): "Exit",
    (1, 0, 12, 0): "Help",
    (1, 0, 16, 0): "Mute",
    (1, 0, 19, 0): "Stop",
    (1, 0, 22, 0): "Swap",
    (1, 0, 23, 0): "Text",
    (1, 0, 25, 0): "Ext",
    (1, 0, 30, 0): "Num1",
    (1, 0, 31, 0): "Num2",
    (1, 0, 32, 0): "Num3",
    (1, 0, 33, 0): "Num4",
    (1, 0, 34, 0): "Num5",
    (1, 0, 35, 0): "Num6",
    (1, 0, 36, 0): "Num7",
    (1, 0, 37, 0): "Num8",
    (1, 0, 38, 0): "Num9",
    (1, 0, 39, 0): "Num0",
    (1, 0, 40, 0): "Ok",
    (1, 0, 59, 0): "Menu",
    (1, 0, 62, 0): "Red",
    (1, 0, 63, 0): "Green",
    (1, 0, 64, 0): "Yellow",
    (1, 0, 65, 0): "Blue",
    (1, 0, 66, 0): "Tv",
    (1, 0, 79, 0): "Right",
    (1, 0, 80, 0): "Left",
    (1, 0, 81, 0): "Down",
    (1, 0, 82, 0): "Up",
    (2, 5, 0, 0): "Power",
}


class TechniSatUsb(eg.PluginBase):
                
    @eg.LogIt
    def __start__(self):
        self.usb = eg.WinUsbRemote(
            "{108E11FA-7EA0-4F13-AA64-1926E14A9C31}",
            self.Callback,
            6,
         )
        if not self.usb.IsOk():
            raise self.Exceptions.DeviceNotFound

         
    def __stop__(self):
        self.usb.Close()


    def Callback(self, data):
        #print tuple(data[:4]), data
        value = tuple(data[:4])
        if value in CODES:
            self.TriggerEvent(CODES[value])
        else:
            self.TriggerEvent("".join("%02X" % x for x in data))


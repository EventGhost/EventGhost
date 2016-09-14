eg.RegisterPlugin(
    name = "Sidewinder Game Voice",
    author = "Bartman",
    version = "0.1.614",
    guid = "{B66C27F5-26C0-47DE-B74A-50A3A483D71E}",
    kind = "remote",
    canMultiLoad = False,
    description = (
        'Allows the communication with the Microsoft Sidewinder Game Voice.<br/>'
        'This plug in also demonstrates how to use EventGhost\'s HID API.'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=571",
)

from eg.WinApi.HID import HIDThread
from eg.WinApi.HID import GetDevicePath
from eg.WinApi.HID import IsDeviceName

class Text:
    errorFind = "Error finding Game Voice"

VENDOR_ID = 1118
PRODUCT_ID = 59

ButtonMapping = {
    0 : "All",
    1 : "Team",
    2 : "1",
    3 : "2",
    4 : "3",
    5 : "4",
    6 : "Command",
    7 : "Mute" }

class GameVoice(eg.PluginClass):
    def __init__(self):
        self.thread = None

    def ButtonCallback(self, data):
        btnPressed = []
        for num in data:
            btnPressed.append(ButtonMapping[num])

        buttonsCount = len(btnPressed)
        if buttonsCount == 0:
            self.TriggerEvent("None")
        elif buttonsCount == 1:
            self.TriggerEvent(btnPressed[0])
        else:
            self.TriggerEvent("+".join(btnPressed))

    def StopCallback(self):
        self.TriggerEvent("Stopped")
        self.thread = None

    def GetMyDevicePath(self):
        path = GetDevicePath(
            None,
            VENDOR_ID,
            PRODUCT_ID,
            None,
            0,
            True,
            0)
        return path;

    def SetupHidThread(self, newDevicePath):
        #create thread
        self.thread = HIDThread(self.name, newDevicePath, self.name)
        self.thread.start()
        self.thread.SetStopCallback(self.StopCallback)
        self.thread.SetButtonCallback(self.ButtonCallback)

    def SetFeature(self, buffer):
        if self.thread:
            self.thread.SetFeature(buffer)

    def ReconnectDevice(self, event):
        """method to reconnect a disconnect device"""
        if self.thread == None:
            if not IsDeviceName(event.payload, VENDOR_ID, PRODUCT_ID):
                return

            #check if the right device was connected
            #getting devicePath
            newDevicePath = self.GetMyDevicePath()
            if not newDevicePath:
                #wrong device
                return

            self.SetupHidThread(newDevicePath)

    def __start__(self):
        #Bind plug in to RegisterDeviceNotification message
        eg.Bind("System.DeviceAttached", self.ReconnectDevice)

        newDevicePath = self.GetMyDevicePath()
        if not newDevicePath:
            #device not found
            self.PrintError(Text.errorFind)
        else:
            self.SetupHidThread(newDevicePath)

    def __stop__(self):
        if self.thread:
            self.thread.AbortThread()

        #unbind from RegisterDeviceNotification message
        eg.Unbind("System.DeviceAttached", self.ReconnectDevice)

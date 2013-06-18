import eg

class PluginInfo(eg.PluginInfo):
    name = "d-box2 Remote Emulator"
    author = "Bitmonster"
    version = "1.0.0"
    kind = "external"
    description = (
        "Control your d-box2 set-top box over Ethernet.\n"
        "\n"
        "<p><i>(Linux/Neutrino must be installed on the box)</i>"
    )
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACmklEQVR42o2TS0hVYRDH"
        "/3O+c859dX1mvhOzSw+kByZW1ibICIQIxSBqYUUQLdpkoW0Meu3b3AiCFrWqMFoItTGL"
        "wo2UCUrY1V6o3Hx1Pffc1/d9jfQgUcEDM/Od+WZ+35z55hBWfIw8Vh2A3sj2Dks3r5dE"
        "0QrJLPo8qxt/YobYXGbbA6hVA9pNgWat9ZRUVMiONxx+btWAHZWq/UQjTmoL8/e74BuM"
        "EFeBYwzWqwCQqA3pzo5WHPDbmGkPY65/BOvZf5rl4/9VLAOgBV8TQftrq/Daa8N5NYSA"
        "BnWxf5j3F3oT/QtZDrCZ1bWFHjAqslAwBwXYd4aIjrANC8IzofR8YinAEJx4iWWWk8Ms"
        "llKQQZvjNGoNjeKMMiaIdFxpPRhXyCwChEqpiDefjE+j00ngOZ/uYUkyYJ0J7NMZiqVh"
        "zEihpTDUsJOE+w8wGEZNSuGsJ4Cj97oxcPsRrnNyn9QoXSMQMAkbVMqYTQJzOWu5LsLA"
        "eBSSkJ2XBTKDb69GT22p0ldMC6mxSVi3HuDp45e4mEqj2SCQT2DSVBRt2Iv81kZ90G/i"
        "5v42MULIK26CYde1HZqpaal3qnOCyg54tf2iD98uhM2eWZeKBemSXZXyS321jm7fZG4d"
        "jvrV5wnj7sMeo5dQUNYC8u72eUSsIidpVea6gVB+vOjDV1P0fgpOScN0SWuqK5+uLt9m"
        "lvYng2Ojo0iriBtEwmFAVmEZ7OBxCI9lJGMZ7q6CFRAQhhfEcwhtQqZ8kE6IdtoJUYEJ"
        "FUn61btULqQcIvizAX/BYR6+BuiUBTIkrzMw+H8g/nqtJDJuDJmEy8D3sOR3TkwjlZ6H"
        "IOf3LRSESnjE9/BJaU6KQ0mHR4LnhOLQ0uWIBFfE7/onfnxeNDm/ADdeEckvKwEjAAAA"
        "AElFTkSuQmCC"
    )

import wx
from httplib import HTTPConnection
    

CMDS = (
    ("Left", "Left", "KEY_LEFT"),
    ("Right", "Right", "KEY_RIGHT"),
    ("Up", "Up", "KEY_UP"),             
    ("Down", "Down", "KEY_DOWN"),
    ("Ok", "Ok", "KEY_OK"),            
    ("Mute", "Mute", "KEY_MUTE"),
    ("Power", "Power", "KEY_POWER"),           
    ("Red", "Red", "KEY_RED"),
    ("Green", "Green", "KEY_GREEN"),
    ("Yellow", "Yellow", "KEY_YELLOW"),         
    ("Blue", "Blue", "KEY_BLUE"),           
    ("VolumeUp", "Volume Up", "KEY_VOLUMEUP"),
    ("VolumeDown", "Volume Down", "KEY_VOLUMEDOWN"),     
    ("Help", "Help", "KEY_HELP"),
    ("Setup", "Setup", "KEY_SETUP"),           
    ("TopLeft", "Top Left", "KEY_TOPLEFT"),
    ("TopRight", "Top Right", "KEY_TOPRIGHT"),       
    ("BottomLeft", "Bottom Left", "KEY_BOTTOMLEFT"),
    ("BottomRight", "Bottom Right", "KEY_BOTTOMRIGHT"),     
    ("Home", "Home", "KEY_HOME"),
    ("PageDown", "Page Down", "KEY_PAGEDOWN"),       
    ("PageUp", "Page Up", "KEY_PAGEUP"),
    ("Num0", "Number 0", "KEY_0"),               
    ("Num1", "Number 1", "KEY_1"),
    ("Num2", "Number 2", "KEY_2"),               
    ("Num3", "Number 3", "KEY_3"),
    ("Num4", "Number 4", "KEY_4"),               
    ("Num5", "Number 5", "KEY_5"),
    ("Num6", "Number 6", "KEY_6"),               
    ("Num7", "Number 7", "KEY_7"),
    ("Num8", "Number 8", "KEY_8"),               
    ("Num9", "Number 9", "KEY_9"),
)


class DBox2(eg.PluginClass):
    canMultiLoad = True
    
    def __init__(self):
        self.host = "127.0.0.1"
        SendCommand = self.SendCommand
        
        for tmpName, tmpDescription, tmpKey in CMDS:
            class tmpAction(eg.ActionClass):
                name = tmpDescription
                key = tmpKey
                def __call__(self2):
                    SendCommand(self2.key)
            tmpAction.__name__ = tmpName
            self.AddAction(tmpAction)
        
        
    def __start__(self, host, useRcem=False):
        self.host = host
        self.useRcem = useRcem
        
        
    def Configure(self, host="127.0.0.1", useRcem=False):
        dialog = eg.ConfigurationDialog(self)
        text1 = wx.StaticText(dialog, -1, "d-box2 Host:")
        hostCtrl = wx.TextCtrl(dialog, -1, host)
        mySizer = wx.FlexGridSizer(cols=2)
        mySizer.Add(text1, 0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        mySizer.Add(hostCtrl, 0, wx.EXPAND)
        dialog.sizer.Add(mySizer, 1, wx.EXPAND)
        useRcemCtrl = wx.CheckBox(dialog, -1, 'Use "rcem" instead of "rcsim"')
        useRcemCtrl.SetValue(useRcem)
        dialog.sizer.Add(useRcemCtrl, 0, wx.EXPAND|wx.ALL, 5)
        
        if dialog.AffirmedShowModal():
            return (hostCtrl.GetValue(), useRcemCtrl.GetValue())
    
    
    def SendCommand(self, key):
        conn = HTTPConnection(self.host)
        if self.useRcem:
            conn.request("GET", "/control/rcem?" + key)
        else:
            conn.request("GET", "/control/exec?Y_Tools&rcsim&" + key)
        conn.getresponse()
        conn.close()
        

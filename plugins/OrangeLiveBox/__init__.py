# -*- coding: utf-8 -*-

import eg

eg.RegisterPlugin(
    name="Orange LiveBox Play",
    guid='{62F731F7-2623-46D1-8E47-261154DB8B7B}',
    author="Flop",
    version="1.0",
    kind="external",
    createMacrosOnAdd=True,
    canMultiLoad=False,
    description="Control Orange LiveBox over TCP/IP",
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=7986",
    help="""<center><img src="images/livebox.png" /></center>""",
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACx"
        "jwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAAGYktHRAD/AP8A/6C9p5MAAAEJSURBVDhP7ZIx"
        "S0JRGIafYwRhLRaJQTYF1dLQrLTUGBStgUNkzW2NBdFUTf0DNx0boghaG7SlsNkIwiBBpLppXd/v"
        "3usfsNUXHu4557483O9wnZ/H5x+JRc++MxAMBJb+BPbvdsSfCWzzFfEjPPEdYetPYeVep/d+PguJ"
        "KZy/JUXuDJpv8PoIqTloq9URXgsWVqG4D+vH8PECtYrOVuDmNOjESE7Cb1u2NCzvwfU5jE1AZhuW"
        "NuHuAnaLcF+A6UXYOAnlzkGrKUH9HeLj+tQGlEswpGtJzMDzbYinGS6PIJuH5KzWhzCqfqOurjz+"
        "jkaw2SQMrnQ4mtFie5WCrB3A0xVUH8KzEeGgC67jULYkBxpTAAAAAElFTkSuQmCC"
    )
)


import urllib2


class OrangeLiveBox(eg.PluginBase):

    def __init__(self):
        groupVolumeControl = self.AddGroup(
            "Volume Control",
            "Action to control volume"
        )
        groupVolumeControl.AddAction(ActionGetCode, value="VOLUME-UP", clsName="Volume up")
        groupVolumeControl.AddAction(ActionGetCode, value="VOLUME-DOWN", clsName="Volume down")
        groupVolumeControl.AddAction(ActionGetCode, value="VOLUME-MUTE", clsName="Volume mute")

        groupMainControl = self.AddGroup(
            "Main Control",
            "Action to main control"
        )
        groupMainControl.AddAction(ActionGetCode, value="CONTROL-POWER", clsName="Control power on/off")
        groupMainControl.AddAction(ActionGetCode, value="CONTROL-UP", clsName="Control up")
        groupMainControl.AddAction(ActionGetCode, value="CONTROL-DOWN", clsName="Control down")
        groupMainControl.AddAction(ActionGetCode, value="CONTROL-LEFT", clsName="Control left")
        groupMainControl.AddAction(ActionGetCode, value="CONTROL-RIGHT", clsName="Control right")
        groupMainControl.AddAction(ActionGetCode, value="CONTROL-ARROW", clsName="Control right arrow")
        groupMainControl.AddAction(ActionGetCode, value="CONTROL-OK", clsName="Control ok")
        groupMainControl.AddAction(ActionGetCode, value="CONTROL-RETURN", clsName="Control return")
        groupMainControl.AddAction(ActionGetCode, value="CONTROL-MENU", clsName="Control menu")

        groupKeypadControl = self.AddGroup(
            "Keypad Control",
            "Action to control Keypad"
        )
        groupKeypadControl.AddAction(ActionGetCode, value="KEYPAD-0", clsName="Keypad 0")
        groupKeypadControl.AddAction(ActionGetCode, value="KEYPAD-1", clsName="Keypad 1")
        groupKeypadControl.AddAction(ActionGetCode, value="KEYPAD-2", clsName="Keypad 2")
        groupKeypadControl.AddAction(ActionGetCode, value="KEYPAD-3", clsName="Keypad 3")
        groupKeypadControl.AddAction(ActionGetCode, value="KEYPAD-4", clsName="Keypad 4")
        groupKeypadControl.AddAction(ActionGetCode, value="KEYPAD-5", clsName="Keypad 5")
        groupKeypadControl.AddAction(ActionGetCode, value="KEYPAD-6", clsName="Keypad 6")
        groupKeypadControl.AddAction(ActionGetCode, value="KEYPAD-7", clsName="Keypad 7")
        groupKeypadControl.AddAction(ActionGetCode, value="KEYPAD-8", clsName="Keypad 8")
        groupKeypadControl.AddAction(ActionGetCode, value="KEYPAD-9", clsName="Keypad 9")

        groupMediaControl = self.AddGroup(
            "Media Control",
            "Action to control Media"
        )
        groupMediaControl.AddAction(ActionGetCode, value="MEDIA-CHANNEL-UP", clsName="Channel up")
        groupMediaControl.AddAction(ActionGetCode, value="MEDIA-CHANNEL-DOWN", clsName="Channel down")
        groupMediaControl.AddAction(ActionGetCode, value="MEDIA-PLAY-PAUSE", clsName="Play/Pause")
        groupMediaControl.AddAction(ActionGetCode, value="MEDIA-FBWD", clsName="Channel up")
        groupMediaControl.AddAction(ActionGetCode, value="MEDIA-FFWD", clsName="Channel up")
        groupMediaControl.AddAction(ActionGetCode, value="MEDIA-RECORD", clsName="Record")
        groupMediaControl.AddAction(ActionGetCode, value="MEDIA-VOD", clsName="Vod")

    def __start__(self, ip_address="", port=""):
        eg.globals.LiveBoxCallUri = "http://%s:%s/remoteControl/cmd?operation=01&" % (ip_address, port)

    def Configure(self, ip_address="192.168.1.17", port="8080"):
        x_start = 10
        x_padding = 70
        y_start = 10
        y_padding = 22
        label_padding = 3
        i = 0

        panel = eg.ConfigPanel()
        labelIpAddress = wx.StaticText(panel, label="Device IP",
                                       pos=(x_start, y_start + label_padding + (i * y_padding)))
        textControlIpAddress = wx.TextCtrl(panel, -1, ip_address,
                                           (x_start + (x_padding * 2), y_start + (i * y_padding)), (150, -1))

        i += 1
        labelPort = wx.StaticText(panel, label="TCP Port (Default: 8080)",
                                  pos=(x_start, y_start + label_padding + (i * y_padding)))
        spinPort = wx.SpinCtrl(panel, -1, "", (x_start + (x_padding * 2), y_start + (i * y_padding)), (80, -1))
        spinPort.SetRange(1, 65535)
        spinPort.SetValue(int(port))

        while panel.Affirmed():
            panel.SetResult(textControlIpAddress.GetValue(), spinPort.GetValue())


class ActionBase(eg.ActionClass):

    def runLiveBoxApi(self, key, mode='0'):
        uri = eg.globals.LiveBoxCallUri + "key=%s&mode=%s" % (key, mode)
        resp = urllib2.urlopen(uri)
        return resp


class ActionGetCode(ActionBase):

    def __call__(self):

        code = REMOTE_COMMANDS[self.value]

        if code is not None:
            return self.runLiveBoxApi(key=code)
        else:
            eg.PrintError("Something went wrong when try to find LiveBox remote code..")


REMOTE_COMMANDS = {

    'KEYPAD-0': '512',
    'KEYPAD-1': '513',
    'KEYPAD-2': '514',
    'KEYPAD-3': '515',
    'KEYPAD-4': '516',
    'KEYPAD-5': '517',
    'KEYPAD-6': '518',
    'KEYPAD-7': '519',
    'KEYPAD-8': '520',
    'KEYPAD-9': '521',

    'VOLUME-UP': '115',
    'VOLUME-DOWN': '114',
    'VOLUME-MUTE': '113',

    'CONTROL-POWER': '116',
    'CONTROL-UP': '103',
    'CONTROL-DOWN': '108',
    'CONTROL-LEFT': '105',
    'CONTROL-RIGHT': '116',
    'CONTROL-ARROW': '106',
    'CONTROL-OK': '352',
    'CONTROL-RETURN': '158',
    'CONTROL-MENU': '139',

    'MEDIA-CHANNEL-UP': '402',
    'MEDIA-CHANNEL-DOWN': '403',
    'MEDIA-PLAY-PAUSE': '164',
    'MEDIA-FBWD': '168',
    'MEDIA-FFWD': '159',
    'MEDIA-RECORD': '167',
    'MEDIA-VOD': '393'
}

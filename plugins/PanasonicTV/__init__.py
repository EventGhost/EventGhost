# -*- coding: utf-8 -*-

import eg

# expose some information about the plugin through an eg.PluginInfo subclass
eg.RegisterPlugin(
    name="Panasonic VIERA TV",
    guid='{2EBAC2D6-D7AD-469C-8910-C127CFC5AC5C}',
    author="EssKaa & Jingo",
    version="1.3",
    kind="external",
    # We don't auto load macros because they are not configured yet.
    createMacrosOnAdd=False,
    canMultiLoad=False,
    description="Control Panasonic VIERA TV over TCP/IP"
)

import urllib2
from xml.dom import minidom

REMOTE_COMMANDS = {
    'Channel down': 'CH_DOWN',
    'Channel up': 'CH_UP',
    'Volume up': 'VOLUP',
    'Volume down': 'VOLDOWN',
    'Mute': 'MUTE',
    'TV': 'TV',
    'AV': 'CHG_INPUT',
    'HDMI1': 'HDMI1',
    'HDMI2': 'HDMI2',
    'HDMI3': 'HDMI3',
    'HDMI4': 'HDMI4',
    'AV1': 'AV1',
    'AV2': 'AV2',
    'Component': 'VIDEO1',
    'Red': 'RED',
    'Green': 'GREEN',
    'Yellow': 'YELLOW',
    'Blue': 'BLUE',
    'VIERA Tools': 'VTOOLS',
    'Exit': 'CANCEL',
    'Option': 'SUBMENU',
    'Return': 'RETURN',
    'OK': 'ENTER',
    'Control RIGHT': 'RIGHT',
    'Control LEFT': 'LEFT',
    'Control UP': 'UP',
    'Control DOWN': 'DOWN',
    '3D button': '3D',
    'SD-Card': 'SD_CARD',
    'Display Mode / Aspect Ratio': 'DISP_MODE',
    'Menu': 'MENU',
    'VIERA connect': 'INTERNET',
    'VIERA link': 'VIERA_LINK',
    'Guide / EPG': 'EPG',
    'Text / TTV': 'TEXT',
    'STTL / Subtitles': 'STTL',
    'Info': 'INFO',
    'TTV index': 'INDEX',
    'TTV hold / image freeze': 'HOLD',
    'Last view': 'R_TUNE',
    'Power': 'POWER',
    'Rewind': 'REW',
    'Play': 'PLAY',
    'Fast forward': 'FF',
    'Skip previous': 'SKIP_PREV',
    'Pause': 'PAUSE',
    'Skip next': 'SKIP_NEXT',
    'Stop': 'STOP',
    'Record': 'REC',
    'Digit 1': 'D1',
    'Digit 2': 'D2',
    'Digit 3': 'D3',
    'Digit 4': 'D4',
    'Digit 5': 'D5',
    'Digit 6': 'D6',
    'Digit 7': 'D7',
    'Digit 8': 'D8',
    'Digit 9': 'D9',
    'Digit 0': 'D0',
    'P-NR (Noise reduction)': 'P_NR'
}


class PansonicTV(eg.PluginBase):
    def __init__(self):
        # self.grp1 = self.AddGroup('!!! Developement !!!', 'Send Custom Commands, expect errors if you don\'t know what you are doing! Use at your own risk!')
        # self.grp1.AddAction(RendCtrl, clsName="Render Control", description="Sets or gets informations in absolute values.")
        # self.grp1.AddAction(NetCtrl, clsName="Net Control", description="Emulates remote keys and sends them to the TV.")
        self.AddAction(SendKey, clsName="Send Remote Key", description="Sends a remote key over the network.")
        self.AddAction(GetVolume, clsName="Get Volume", description="Gets current volume")
        self.AddAction(GetMute, clsName="Get Mute", description="Gets mute status")
        self.AddAction(SetVolume, clsName="Set Volume", description="Sets volume to x")
        self.AddAction(SetMuteOn, clsName="Mute On", description="Mute TV")
        self.AddAction(SetMuteOff, clsName="Mute Off", description="Unmute TV")
        self.AddAction(SmartMuteOff, clsName="SmartMute Off", description="Sets previous volume")
        self.AddAction(SmartMuteOn, clsName="SmartMute On", description="Sets volume to 0 (no mute symbol displayed)")
        self.AddAction(SmartMuteToggle, clsName="SmartMute Toggle", description="Toggles SmartMute")

    def __start__(self, ip_address="", port=""):
        eg.globals.VieraRendCtrlUrl = "http://%s:%s/dmr/control_0" % (ip_address, port)
        eg.globals.VieraNetCtrlUrl = "http://%s:%s/nrc/control_0" % (ip_address, port)
        eg.globals.VieraSmartMuted = False
        eg.globals.VieraSmartMuteLastVolume = 20

    def Configure(self, ip_address="192.168.11.20", port="55000"):
        x_start = 10
        x_padding = 70
        y_start = 10
        y_padding = 22
        label_padding = 3
        i = 0

        panel = eg.ConfigPanel()
        labelIpAddress = wx.StaticText(panel, label="Device IP or FQDN",
                                       pos=(x_start, y_start + label_padding + (i * y_padding)))
        textControlIpAddress = wx.TextCtrl(panel, -1, ip_address,
                                           (x_start + (x_padding * 2), y_start + (i * y_padding)), (150, -1))

        i += 1
        labelPort = wx.StaticText(panel, label="TCP Port (Default: 55000)",
                                  pos=(x_start, y_start + label_padding + (i * y_padding)))
        spinPort = wx.SpinCtrl(
            parent=panel,
            value=port,
            pos=(x_start + (x_padding * 2), y_start + (i * y_padding)),
            size=(80, -1),
            min=1,
            max=65535,
        )

        while panel.Affirmed():
            panel.SetResult(textControlIpAddress.GetValue(), spinPort.GetValue())


class ActionBase(eg.ActionClass):

    def runCmdRend(self, method='Get', command='Volume', value=None):
        xmlstr = '<?xml version="1.0" encoding="utf-8"?>'
        xmlstr += '<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">'
        xmlstr += '<s:Body>'
        xmlstr += '<u:%s%s xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1">' % (method, command)
        xmlstr += '<InstanceID>0</InstanceID>'
        xmlstr += '<Channel>Master</Channel>'
        if value:
            value = eg.ParseString(value)
            xmlstr += '<Desired%s>%s</Desired%s>' % (command, value, command)
        xmlstr += '</u:%s%s>' % (method, command)
        xmlstr += '</s:Body>'
        xmlstr += '</s:Envelope>'

        req = urllib2.Request(url=eg.globals.VieraRendCtrlUrl,
                              data=xmlstr,
                              headers={'Content-Type': 'text/xml; charset="utf-8"',
                                       'Content-Length': len(xmlstr),
                                       'SOAPACTION': '"urn:schemas-upnp-org:service:RenderingControl:1#%s%s"' % (
                                       method, command), })

        resp = urllib2.urlopen(req)
        xml = minidom.parseString(resp.read())
        eg.myvar1 = xml
        if method == "Get" and command == "Volume":
            nodes = xml.getElementsByTagName('CurrentVolume')
            eg.result = nodes[0].firstChild.data
        elif method == "Get" and command == "Mute":
            nodes = xml.getElementsByTagName('CurrentMute')
            if int(nodes[0].firstChild.data) == 0:
                eg.result = False
            else:
                eg.result = True
        else:
            eg.result = value
        return eg.result

    def runCmdNet(self, command="MUTE"):
        command = 'NRC_%s-ONOFF' % command.upper()
        xmlstr = '<?xml version="1.0" encoding="utf-8"?>'
        xmlstr += '<s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">'
        xmlstr += '<s:Body>'
        xmlstr += '<u:X_SendKey xmlns:u="urn:panasonic-com:service:p00NetworkControl:1">'
        xmlstr += '<X_KeyEvent>%s</X_KeyEvent>' % command
        xmlstr += '</u:X_SendKey>'
        xmlstr += '</s:Body>'
        xmlstr += '</s:Envelope>'
        req = urllib2.Request(url=eg.globals.VieraNetCtrlUrl,
                              data=xmlstr,
                              headers={'Content-Type': 'text/xml; charset="utf-8"',
                                       'Content-Length': len(xmlstr),
                                       'SOAPACTION': '"urn:panasonic-com:service:p00NetworkControl:1#X_SendKey"',
                                       })
        resp = urllib2.urlopen(req)


class RendCtrl(ActionBase):

    def __call__(self, method="Get", rendCmd="Volume", value=None):
        return self.runCmdRend(method=method, command=rendCmd, value=value)

    def Configure(self, method="", rendCmd="", value=""):
        panel = eg.ConfigPanel()
        labelMethod = wx.StaticText(panel, label="Method (Get or Set)")
        textControlMethod = wx.TextCtrl(panel, -1, method, (100, 10))
        labelRendCmd = wx.StaticText(panel, label="Command to execute")
        textControlRendCmd = wx.TextCtrl(panel, -1, rendCmd, (100, 10))
        labelValue = wx.StaticText(panel, label='Value to set, only needed if Method is "Set"')
        textControlValue = wx.TextCtrl(panel, -1, value, (100, 10))
        panel.sizer.Add(labelMethod, 1, wx.EXPAND)
        panel.sizer.Add(textControlMethod, 1, wx.EXPAND)
        panel.sizer.Add(labelRendCmd, 1, wx.EXPAND)
        panel.sizer.Add(textControlRendCmd, 1, wx.EXPAND)
        panel.sizer.Add(labelValue, 1, wx.EXPAND)
        panel.sizer.Add(textControlValue, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControlMethod.GetValue(), textControlRendCmd.GetValue(), textControlValue.GetValue())


class NetCtrl(ActionBase):

    def __call__(self, irCmd=None):
        if not irCmd:
            raise Exception('Please insert CMD')
        return self.runCmdNet(command=irCmd)

    def Configure(self, irCmd=""):
        panel = eg.ConfigPanel()
        textControl = wx.TextCtrl(panel, -1, irCmd)
        panel.sizer.Add(textControl, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())


class GetVolume(ActionBase):
    def __call__(self):
        return self.runCmdRend(method="Get", command="Volume", value="")


class GetMute(ActionBase):
    def __call__(self):
        return self.runCmdRend(method="Get", command="Mute", value="")


class SetVolume(ActionBase):
    def __call__(self, volLevel):
        return self.runCmdRend(method="Set", command="Volume", value=volLevel)

    def Configure(self, volLevel=""):
        panel = eg.ConfigPanel()
        labelValue = wx.StaticText(panel, label='Value to set. Valid Values: 0 - 100 or {eg.myvar}')
        textControlValue = wx.TextCtrl(panel, -1, volLevel, (100, 10))
        panel.sizer.Add(labelValue, 0, wx.EXPAND)
        panel.sizer.Add(textControlValue, 0, wx.EXPAND)
        while panel.Affirmed():
            volLevel = textControlValue.GetValue()
            panel.SetResult(volLevel)


class SetMuteOn(ActionBase):
    def __call__(self):
        return self.runCmdRend(method="Set", command="Mute", value="1")


class SetMuteOff(ActionBase):
    def __call__(self, value):
        return self.runCmdRend(method="Set", command="Mute", value="0")


class SmartMuteOff(ActionBase):
    def __call__(self):
        if self.runCmdRend(method="Get", command="Volume") == "0":
            if eg.globals.VieraSmartMuteLastVolume:
                self.runCmdRend(method="Set", command="Volume", value=eg.globals.VieraSmartMuteLastVolume)
        return


class SmartMuteOn(ActionBase):
    def __call__(self):
        currentVolume = self.runCmdRend(method="Get", command="Volume")
        if currentVolume != "0":
            eg.globals.VieraSmartMuteLastVolume = currentVolume
            self.runCmdRend(method="Set", command="Volume", value="0")
            if self.runCmdRend(method="Get", command="Volume") != "0":
                # Fix needed
                self.runCmdRend(method="Set", command="Volume", value="1")
                self.runCmdRend(method="Set", command="Volume", value="0")
        return


class SmartMuteToggle(ActionBase):
    def __call__(self):
        currentVolume = self.runCmdRend(method="Get", command="Volume")
        if currentVolume == "0":
            try:
                self.runCmdRend(method="Set", command="Volume", value=eg.globals.VieraSmartMuteLastVolume)
            except:
                self.runCmdRend(method="Set", command="Volume", value="15")
        else:
            eg.globals.VieraSmartMuteLastVolume = currentVolume
            self.runCmdRend(method="Set", command="Volume", value="0")
            if self.runCmdRend(method="Get", command="Volume") != "0":
                # Fix needed
                self.runCmdRend(method="Set", command="Volume", value="1")
                self.runCmdRend(method="Set", command="Volume", value="0")
        return


class SendKey(ActionBase):
    def __call__(self, irCmd=None):

        code = None
        code = REMOTE_COMMANDS[irCmd]

        if code is not None:
            return self.runCmdNet(command=code)
        else:
            eg.PrintError("Something went wrong...")

    def Configure(self, irCmd="OK"):
        panel = eg.ConfigPanel()

        irCommands = sorted(REMOTE_COMMANDS.keys())

        # self.irCmdLabel = wx.StaticText(panel, label="Command to send: ", pos=(100,10))
        # self.combo = wx.ComboBox(panel, -1, pos=(100,20), size=(100, -1), choices=irCommands)
        wx.StaticText(panel, label="Action: ", pos=(10, 60))
        combo = wx.Choice(panel, -1, (10, 80), choices=irCommands)
        if irCmd in irCommands:
            combo.SetStringSelection(irCmd)

        while panel.Affirmed():
            panel.SetResult(irCommands[combo.GetCurrentSelection()])

#
# plugins/SamsungLAN/__init__.py
# 
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Samsung-LAN-Control


README = """\
This Plugin Control your Samsung TV with LAN Interface.<br>
Without Change any Setting on your Device. You don't need to Hack your TV.
Simply enter the IP-Address of your TV.<br>

You can Control:<br>
	-Volume<br>
	-Mute<br>
	-Brightness<br>
	-Contrast<br>
	-Sharpness<br>
	-ColorTemperature<br>
via a UPNP/SOAP Request.<br>

The Info's are taken from this Forum:
<a href="http://forum.samygo.tv/viewtopic.php?f=5&t=190&start=170#p21299">http://forum.samygo.tv</a><br>

I tested an developed this with a Samsung LE46B650<br>

This Plugin is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License version 2 as published by the
Free Software Foundation
"""

import eg

eg.RegisterPlugin(
    name="SamsungTV-LAN-Control",
    guid='{481C4084-5B10-4DF1-BCE8-B22254B41F32}',
    author="MrGangster",
    version="0.1.0",
    kind="external",
    url="http://nix.d",
    description="Control some Settings from your Samsung TV via UPNP/SOAP",
    canMultiLoad=True,
    help=README,
)

import httplib
from xml.dom.minidom import parseString
import eg

#	Name 					Action '0'				Argument '1'				Full '2'						Return '3'
ACTIONS = (
    ('GetVolume', 'GetVolume', 'CurrentVolume', '<Channel>Master</Channel>', 'GetVolumeResponse'),
    ('GetMute', 'GetMute', 'CurrentMute', '<Channel>Master</Channel>', 'GetMuteResponse'),
    ('GetBrightness', 'GetBrightness', 'CurrentBrightness', '', 'GetBrightnessResponse'),
    ('GetContrast', 'GetContrast', 'CurrentContrast', '', 'GetContrastResponse'),
    ('GetSharpness', 'GetSharpness', 'CurrentSharpness', '', 'GetSharpnessResponse'),
    ('GetColorTemperature', 'GetColorTemperature', 'CurrentColorTemperature', '', 'GetColorTemperatureResponse'),
    ('SetMute', 'SetMute', 'DesiredMute', '<Channel>Master</Channel>', None),
    ('SetVolume', 'SetVolume', 'DesiredVolume', '<Channel>Master</Channel>', None),
    ('SetBrightness', 'SetBrightness', 'DesiredBrightness', '', None),
    ('SetContrast', 'SetContrast', 'DesiredContrast', '', None),
    ('SetSharpness', 'SetSharpness', 'DesiredSharpness', '', None),
    ('SetColorTemperature', 'SetColorTemperature', 'DesiredColorTemperature', '', None),
)

eg.RegisterPlugin()


def GetActions(TYPE):
    for ACTION_Name, ACTION_Command, ACTION_Argument, ACTION_Full, ACTION_Return in ACTIONS:
        if ACTION_Name == TYPE:
            COMMANDS = (ACTION_Command, ACTION_Argument, ACTION_Full, ACTION_Return)
    # print "GetActions Return:", (COMMANDS)
    return COMMANDS


def MakeHeader(ACTION):
    HEADERS = {"Content-Type": "text/xml",
               "SoapAction": "",
               "Accept": "*/*", }
    HEADERS["SoapAction"] = "urn:schemas-upnp-org:service:RenderingControl:1#" + ACTION
    return HEADERS


def Get(ACTION):
    MyACTION = GetActions(ACTION)
    BODY = "<?xml version='1.0' encoding='utf-8'?>\n\
	<s:Envelope s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/' xmlns:s='http://schemas.xmlsoap.org/soap/envelope/'>\n\
		<s:Body>\n\
			<ns0:" + MyACTION[0] + " xmlns:ns0='urn:schemas-upnp-org:service:RenderingControl:1'>\n\
				<" + MyACTION[1] + "></" + MyACTION[1] + ">\n\
				<InstanceID>0</InstanceID>\n\
				" + MyACTION[2] + "\n\
			</ns0:" + MyACTION[0] + ">\n\
		</s:Body>\n\
	</s:Envelope>"
    conn = httplib.HTTPConnection(HOST, PORT)
    conn.request("POST", "/upnp/control/RenderingControl1", BODY, MakeHeader(MyACTION[0]))
    r1 = conn.getresponse()
    if (r1.status != 200):
        return r1.status, r1.reason
    data3 = parseString(r1.read())
    NodeName = "u:" + MyACTION[3]
    for B1 in data3.firstChild.childNodes:
        if B1.nodeName == "s:Body":
            for B2 in B1.childNodes:
                # print B2.nodeName
                if B2.nodeName == NodeName:
                    # print "DEBUG B2.nodeName: ", B2.nodeName
                    for B3 in B2.childNodes:
                        # print "DEBUG B3.nodeName: ", B3.nodeName
                        if B3.nodeName == MyACTION[1]:
                            # print B3.nodeName, B3.firstChild.data.strip()
                            RET = B3.firstChild.data.strip()
    conn.close()
    return RET


def Set(ACTION, VALUE):
    MyACTION = GetActions(ACTION)
    BODY = "<?xml version='1.0' encoding='utf-8'?>\n\
	<s:Envelope s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/' xmlns:s='http://schemas.xmlsoap.org/soap/envelope/'>\n\
		<s:Body>\n\
			<ns0:" + MyACTION[0] + " xmlns:ns0='urn:schemas-upnp-org:service:RenderingControl:1'>\n\
				<InstanceID>0</InstanceID>\n\
				<" + MyACTION[1] + ">" + str(VALUE) + "</" + MyACTION[1] + ">\n\
				" + MyACTION[2] + "\n\
			</ns0:" + MyACTION[0] + ">\n\
		</s:Body>\n\
	</s:Envelope>"
    conn = httplib.HTTPConnection(HOST, PORT)
    conn.request("POST", "/upnp/control/RenderingControl1", BODY, MakeHeader(MyACTION[0]))
    r1 = conn.getresponse()
    if (r1.status != 200):
        return r1.status, r1.reason
    # print r1.status, r1.reason
    data2 = r1.read()
    conn.close()
    return BODY


class SamsungUPNP(eg.PluginBase):

    def __init__(self):
        Volume = self.AddGroup(
            "Sound",
            "All about Sound"
        )
        Volume.AddAction(GetVolume)
        Volume.AddAction(SetVolume)
        Volume.AddAction(Mute)
        Volume.AddAction(UnMute)
        Volume.AddAction(Volume_Up)
        Volume.AddAction(Volume_Down)
        Volume.AddAction(Togle_Mute)

        Brightness = self.AddGroup(
            "Brightness",
            "Brightness Settings"
        )
        Brightness.AddAction(GetBrightness)
        Brightness.AddAction(SetBrightness)
        Brightness.AddAction(Brightness_Up)
        Brightness.AddAction(Brightness_Down)

        Contrast = self.AddGroup(
            "Contrast",
            "Contrast Settings"
        )
        Contrast.AddAction(GetContrast)
        Contrast.AddAction(SetContrast)
        Contrast.AddAction(Contrast_Up)
        Contrast.AddAction(Contrast_Down)

        Sharpness = self.AddGroup(
            "Sharpness",
            "Sharpness Settings"
        )
        Sharpness.AddAction(GetSharpness)
        Sharpness.AddAction(SetSharpness)
        Sharpness.AddAction(Sharpness_Up)
        Sharpness.AddAction(Sharpness_Down)

        ColorTemperature = self.AddGroup(
            "ColorTemperature",
            "ColorTemperature Settings"
        )
        ColorTemperature.AddAction(GetColorTemperature)
        ColorTemperature.AddAction(SetColorTemperature)
        ColorTemperature.AddAction(Togle_ColorTemperature)

    def __start__(self, SamsungIP):
        global HOST
        global PORT
        HOST = SamsungIP
        PORT = 52235

    def Configure(self, SamsungIP=""):
        panel = eg.ConfigPanel()
        IP = panel.TextCtrl(SamsungIP)
        panel.AddLine("IP-Adress or Hostname of Samung TV:", IP)
        while panel.Affirmed():
            panel.SetResult(IP.GetValue())


class GetVolume(eg.ActionBase):

    def __call__(self):
        print "Samsung-LAN-Control GetVol:", Get("GetVolume")


class SetVolume(eg.ActionBase):

    def __call__(self, Volume):
        Set("SetVolume", Volume)

    def Configure(self, Volume="10"):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(Volume, min=0, max=100)
        panel.AddLine("Set Volume to:", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())


class Mute(eg.ActionBase):

    def __call__(self):
        Set("SetMute", 1)


class UnMute(eg.ActionBase):

    def __call__(self):
        Set("SetMute", 0)


class Volume_Up(eg.ActionBase):

    def __call__(self):
        NewVol = int(Get("GetVolume")) + 1
        Set("SetVolume", NewVol)


class Volume_Down(eg.ActionBase):

    def __call__(self):
        NewVol = int(Get("GetVolume")) - 1
        Set("SetVolume", NewVol)


class Togle_Mute(eg.ActionBase):

    def __call__(self):
        print "UnMute"
        CurMute = Get("GetMute")
        if CurMute == "0":
            Set("SetMute", 1)
        else:
            Set("SetMute", 0)


class GetBrightness(eg.ActionBase):

    def __call__(self):
        print "Samsung-LAN-Control GetBrightness:", Get("GetBrightness")


class SetBrightness(eg.ActionBase):

    def __call__(self, Brightness):
        Set("SetBrightness", Brightness)

    def Configure(self, Brightness="50"):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(Brightness, min=0, max=100)
        panel.AddLine("Set Brightness to:", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())


class Brightness_Up(eg.ActionBase):

    def __call__(self):
        NewBright = int(Get("GetBrightness")) + 1
        Set("SetBrightness", NewBright)


class Brightness_Down(eg.ActionBase):

    def __call__(self):
        NewBright = int(Get("GetBrightness")) - 1
        Set("SetBrightness", NewBright)


class GetContrast(eg.ActionBase):

    def __call__(self):
        print "Samsung-LAN-Control GetContrast:", Get("GetContrast")


class SetContrast(eg.ActionBase):

    def __call__(self, Contrast):
        Set("SetContrast", Contrast)

    def Configure(self, Contrast="80"):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(Contrast, min=0, max=100)
        panel.AddLine("Set Contrast to:", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())


class Contrast_Up(eg.ActionBase):

    def __call__(self):
        NewContr = int(Get("GetContrast")) + 1
        Set("SetContrast", NewContr)


class Contrast_Down(eg.ActionBase):

    def __call__(self):
        NewContr = int(Get("GetContrast")) - 1
        Set("SetContrast", NewContr)


class GetSharpness(eg.ActionBase):

    def __call__(self):
        print "Samsung-LAN-Control GetSharpness:", Get("GetSharpness")


class SetSharpness(eg.ActionBase):

    def __call__(self, Sharpness):
        Set("SetSharpness", Sharpness)

    def Configure(self, Sharpness="20"):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(Sharpness, min=0, max=100)
        panel.AddLine("Set Sharpness to:", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())


class Sharpness_Up(eg.ActionBase):

    def __call__(self):
        NewSharp = int(Get("GetSharpness")) + 1
        Set("SetSharpness", NewSharp)


class Sharpness_Down(eg.ActionBase):

    def __call__(self):
        NewSharp = int(Get("GetSharpness")) - 1
        Set("SetSharpness", NewSharp)


class GetColorTemperature(eg.ActionBase):

    def __call__(self):
        TEMP = Get("GetColorTemperature")
        TEMP = int(TEMP)
        if TEMP == 2:
            ColTemp = "Cool"
        elif TEMP == 3:
            ColTemp = "Normal"
        elif TEMP == 4:
            ColTemp = "Warm1"
        elif TEMP == 5:
            ColTemp = "Warm2"
        elif TEMP == 6:
            ColTemp = "Warm3"
        print "Samsung-LAN-Control ColorTemperature:", ColTemp


class SetColorTemperature(eg.ActionBase):

    def __call__(self, CurTemp):
        if CurTemp == "0":
            NewTemp = "2"
        elif CurTemp == "1":
            NewTemp = "3"
        elif CurTemp == "2":
            NewTemp = "4"
        elif CurTemp == "3":
            NewTemp = "5"
        elif CurTemp == "4":
            NewTemp = "6"
        Set("SetColorTemperature", NewTemp)

    def Configure(self, bytesize=2):
        panel = eg.ConfigPanel()
        valueChoice = panel.Choice(bytesize, ['Cold', 'Normal', 'Warm1', 'Warm2', 'Warm3'])
        panel.AddLine("Set ColorTemperature to:", valueChoice)
        while panel.Affirmed():
            panel.SetResult(valueChoice.GetValue())


class Togle_ColorTemperature(eg.ActionBase):

    def __call__(self):
        CurTemp = Get("GetColorTemperature")
        if CurTemp == "2":
            NewTemp = "3"
        elif CurTemp == "3":
            NewTemp = "4"
        elif CurTemp == "4":
            NewTemp = "5"
        elif CurTemp == "5":
            NewTemp = "6"
        # Maybe it's a Bug in my Firmware but i can't set Warm3 over UPNP
        elif CurTemp == "6":
            NewTemp = "2"
        Set("SetColorTemperature", NewTemp)
        print Get("GetColorTemperature")
        if CurTemp == NewTemp:
            print "Firmware Bug found!! Set ColorTemperature to ""Cool"""
            Set("SetColorTemperature", "2")
            print Get("GetColorTemperature")

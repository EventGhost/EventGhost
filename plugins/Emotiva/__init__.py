# This file is a plugin for EventGhost.
#
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import eg

eg.RegisterPlugin(
    name="Emotiva Network Control",
    guid='{924C36E9-4166-4BDF-B0C6-AB7AA37D4C8A}',
    version="0.1",
    author="Nuts",
    description=(
        "Sends commands to Emotiva XMC-1 through UDP."
    ),
    kind="external",
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QAAAAAAAD5Q7t/"
        "AAAACXBIWXMAAAsSAAALEgHS3X78AAAAB3RJTUUH1gIQFgQOuRVmrAAAAVRJREFUOMud"
        "kjFLw2AQhp+kMQ7+jJpCF+ni1lFEwUXq5g+wgiCCgoNUrG5Oltb2DygGYwUXwbmbg+Li"
        "IhSHhobaora2MZTGoQb5aBLFd/u4u/fuufskApQ92DWAFOEqKSHB1OzMHJoW8w1aloVR"
        "1tNhBmhajPnlQ9/Yzdk2AKEGkiQBkExOAS4wfFcqDwwGg6FBGGv++IiF5DiOZPHcnKDb"
        "+6T9YQs5iscajSd8p2jUqhhlnZfXYfeIMgaA67o/CNF4gsW1C1RVJHKcPlfFJQCaZt23"
        "geKxqqpCYnpSYL2/feIbleuTrZErjCwxEpGpNzp0ew7tjshaKOb8BsgIBnePdXAlz05g"
        "XV1ZEyplWaZQzGUVL8lx+qhv7yM78NRqtYJ30KhVucynAq8AoJ+fBhqUjLKe/uXPZzI7"
        "e/tBBumN9U1s2/at9FiBQANM0+S/UsL4/qIvHUp+5VOP+PAAAAAASUVORK5CYII="
    ),
    createMacrosOnAdd=True,
)

import socket
from time import sleep

ACTIONS = (

    (eg.ActionGroup, 'GroupMainControls', 'Emotiva Commands', None, (

        ('volume +', 'Volume up', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><volume value="1" ack="yes" /></emotivaControl>'),
        ('volume -', 'Volume down', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><volume value="-1" ack="yes" /></emotivaControl>'),
        ('mute', 'Mute Toggle', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><mute value="0" ack="yes" /></emotivaControl>'),

        ('power_on', 'Power On', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><power_on value="0" ack="yes" /></emotivaControl>'),
        ('power_off', 'Power Off', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><power_off value="0" ack="yes" /></emotivaControl>'),
        ('input +', 'Input up', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><input value="1" ack="yes" /></emotivaControl>'),
        ('input -', 'Input down', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><input value="-1" ack="yes" /></emotivaControl>'),
        ('info', 'Show Info screen', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><info value="0" ack="yes" /></emotivaControl>'),

        ('mode +', 'Mode up', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><mode value="1" ack="yes" /></emotivaControl>'),
        ('mode -', 'Mode down', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><mode value="-1" ack="yes" /></emotivaControl>'),
        ('reference_stereo', 'Set Mode to Reference Stereo', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><reference_stereo value="0" ack="yes" /></emotivaControl>'),
        ('music', 'Select Music preset', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><music value="0" ack="yes" /></emotivaControl>'),
        ('movie', 'Select Movie preset', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><movie value="0" ack="yes" /></emotivaControl>'),
        ('speaker_preset', 'Cycle through Speaker Presets', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><speaker_preset value="0" ack="yes" /></emotivaControl>'),
        ('loudness', 'Toggle Loudness on/off', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><loudness value="0" ack="yes" /></emotivaControl>'),

        ('source_tuner', 'Set source_tuner', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><source_tuner value="0" ack="yes" /></emotivaControl>'),
        ('source_1', 'Set source_1', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><source_1 value="0" ack="yes" /></emotivaControl>'),
        ('source_2', 'Set source_2', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><source_2 value="0" ack="yes" /></emotivaControl>'),
        ('source_3', 'Set source_3', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><source_3 value="0" ack="yes" /></emotivaControl>'),
        ('source_4', 'Set source_4', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><source_4 value="0" ack="yes" /></emotivaControl>'),
        ('source_5', 'Set source_5', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><source_5 value="0" ack="yes" /></emotivaControl>'),
        ('source_6', 'Set source_6', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><source_6 value="0" ack="yes" /></emotivaControl>'),
        ('source_7', 'Set source_7', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><source_7 value="0" ack="yes" /></emotivaControl>'),
        ('source_8', 'Set source_8', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><source_8 value="0" ack="yes" /></emotivaControl>'),

        ('menu', 'Enter/Exit menu', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><menu value="0" ack="yes" /></emotivaControl>'),
        ('up', 'Menu up', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><up value="0" ack="yes" /></emotivaControl>'),
        ('down', 'Menu down', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><down value="0" ack="yes" /></emotivaControl>'),
        ('right', 'Menu right', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><right value="0" ack="yes" /></emotivaControl>'),
        ('left', 'Menu left', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><lft value="0" ack="yes" /></emotivaControl>'),
        ('enter', 'Menu enter', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><enter value="0" ack="yes" /></emotivaControl>'),
        ('dim', 'Cycle through FP dimness settings', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><dim value="0" ack="yes" /></emotivaControl>'),

        ('center +', 'Center Volume up', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><center value="1" ack="yes" /></emotivaControl>'),
        ('center -', 'Center Volume down', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><center value="-1" ack="yes" /></emotivaControl>'),
        ('subwoofer +', 'Subwoofer Volume up', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><subwoofer value="1" ack="yes" /></emotivaControl>'),
        ('subwoofer -', 'Subwoofer Volume down', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><subwoofer value="-1" ack="yes" /></emotivaControl>'),
        ('surround +', 'Surrounds Volume up', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><surround value="1" ack="yes" /></emotivaControl>'),
        ('surround -', 'Surrounds Volume down', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><surround value="-1" ack="yes" /></emotivaControl>'),
        ('back +', 'Backs Volume up', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><back value="1" ack="yes" /></emotivaControl>'),
        ('back -', 'Backs Volume down', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><back value="-1" ack="yes" /></emotivaControl>'),

        ('zone2_power', 'Toggle Zone 2 Power On/Off', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><zone2_power value="0" ack="yes" /></emotivaControl>'),
        ('zone2_volume +', 'Zone 2 Volume up', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><zone2_volume value="1" ack="yes" /></emotivaControl>'),
        ('zone2_volume -', 'Zone 2 Volume down', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><zone2_volume value="-1" ack="yes" /></emotivaControl>'),
        ('zone2_input +', 'Change Zone 2 Input up', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><zone2_input value="1" ack="yes" /></emotivaControl>'),
        ('zone2_input -', 'Change Zone 2 Input down', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><zone2_input value="-1" ack="yes" /></emotivaControl>'),

        ('zone1_band', 'Toggle Tuner Band AM/FM', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><zone1_band value="0" ack="yes" /></emotivaControl>'),
        ('frequency +', 'Tuner Frequency up', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><frequency value="1" ack="yes" /></emotivaControl>'),
        ('frequency -', 'Tuner Frequency down', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><frequency value="-1" ack="yes" /></emotivaControl>'),
        ('seek +', 'Tuner Seek up', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><seek value="1" ack="yes" /></emotivaControl>'),
        ('seek -', 'Tuner Seek down', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><seek value="-1" ack="yes" /></emotivaControl>'),
        ('channel +', 'Tuner Preset Station up', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><channel value="1" ack="yes" /></emotivaControl>'),
        ('channel -', 'Tuner Preset Station down', None,
         '<?xml version="1.0" encoding="utf-8"?><emotivaControl><channel value="-1" ack="yes" /></emotivaControl>'),

    )),

)


class UDPNetworkSender(eg.PluginBase):

    def __init__(self):
        self.AddActionsFromList(ACTIONS, SendCommand)
        self.AddAction(SendCommandEx)
        self.AddAction(CloseSocket)
        self.AddAction(OpenSocket)

    def __start__(self, ip, port):
        self.ip = ip
        self.port = port
        self.Connect()

    def __stop__(self):
        self.socket.close()

    def Configure(self, ip="192.168.1.105", port=7002):
        panel = eg.ConfigPanel()
        ipCtrl = panel.TextCtrl(ip)
        portCtrl = panel.SpinIntCtrl(port, max=65535)

        st1 = panel.StaticText("IP")
        st2 = panel.StaticText("Port")
        eg.EqualizeWidths((st1, st2))
        tcpBox = panel.BoxedGroup(
            "UDP Settings",
            (st1, ipCtrl),
            (st2, portCtrl),
        )

        panel.sizer.Add(tcpBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                ipCtrl.GetValue(),
                portCtrl.GetValue(),
            )

    def Connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(1.0)
        self.socket = s

        ip = self.ip
        port = self.port


class SendCommand(eg.ActionBase):
    def __call__(self):
        line = str(self.value) + '\r'

        try:
            self.plugin.socket.sendto(line, (self.plugin.ip, self.plugin.port))
            sleep(0.1)
        except socket.error, msg:
            print "Error sending command, retrying", msg
            # print "IP=" + self.plugin.ip + " port=" + self.plugin.port
            self.plugin.Connect()
            try:
                self.plugin.socket.sendto(line, (self.plugin.ip, self.plugin.port))
            except socket.error, msg:
                print "Error sending command", msg
                # print "IP=" + self.plugin.ip + " port=" + self.plugin.port


class SendCommandEx(eg.ActionBase):

    def __call__(self, myAction="", myValue="1"):

        line = '<?xml version="1.0" encoding="utf-8"?><emotivaControl><' + str(myAction) + ' value="' + str(
            myValue) + '" ack="yes" /></emotivaControl>'
        # eg.Print(line) #debug

        try:
            self.plugin.socket.sendto(line, (self.plugin.ip, self.plugin.port))
            sleep(0.1)
        except socket.error, msg:
            print "Error sending command, retrying", msg
            # print "IP=" + self.plugin.ip + " port=" + self.plugin.port
            self.plugin.Connect()
            try:
                self.plugin.socket.sendto(line, (self.plugin.ip, self.plugin.port))
            except socket.error, msg:
                print "Error sending command", msg
                # print "IP=" + self.plugin.ip + " port=" + self.plugin.port

    def Configure(self, myAction="volume", myValue="1"):
        panel = eg.ConfigPanel()
        actionCtrl = panel.TextCtrl(myAction)
        numberCtrl = panel.TextCtrl(myValue)
        panel.AddLine("Action: ", actionCtrl)
        panel.AddLine("+/- n: ", numberCtrl)

        while panel.Affirmed():
            panel.SetResult(actionCtrl.GetValue(), numberCtrl.GetValue())


class OpenSocket(eg.ActionBase):

    def __call__(self):
        self.plugin.Connect()


class CloseSocket(eg.ActionBase):

    def __call__(self):
        self.plugin.socket.close()

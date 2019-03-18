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
    name = "Denon & Marantz Network Control",
    guid='{11C2C41D-5D50-4882-811B-403812624D97}',
    version = "0.1",
    author = "Nuts",
    description = (
        "Sends events to a Denon & Marantz Receiver through TCP/IP."
    ),
    kind = "external",
    icon = (
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
    createMacrosOnAdd = True,
)


import socket
import select
import re
from time import sleep
from threading import Event, Thread

ACTIONS = (

(eg.ActionGroup, 'GroupMainControls', 'Denon & Marantz Actions', None, (

    ('PowerOn', 'Power On', None, 'PWON'),
    ('PowerOff', 'Power Standby', None, 'PWSTANDBY'),

    ('MasterUp', 'Master Volume Up', None, 'MVUP'),
    ('MasterDown', 'Master Volume Down', None, 'MVDOWN'),

    ('MuteOn', 'Mute On', None, 'MUON'),
    ('MuteOff', 'Mute Off', None, 'MUOFF'),

    ('MainZoneOn', 'Main Zone On', None, 'ZMON'),
    ('MainZoneOff', 'Main Zone Off', None, 'ZMOFF'),

    ('Z2On', 'Zone 2 On', None, 'Z2ON'),
    ('Z2Off', 'Zone 2 Off', None, 'Z2OFF'),
    ('Z2Source', 'Zone 2 Source', None, 'Z2SOURCE'),
    ('Z2VolUp', 'Zone 2 Volume Up', None, 'Z2UP'),
    ('Z2VolDown', 'Zone 2 Volume Down', None, 'Z2DOWN'),
    ('Z2MuteOn', 'Zone 2 Mute On', None, 'Z2MUON'),
    ('Z2MuteOff', 'Zone 2 Mute Off', None, 'Z2MUOFF'),

    ('DelayUp', 'Audio Delay Increasse', None, 'PSDELAY UP'),
    ('DelayDown', 'Audio Delay Decrease', None, 'PSDELAY DOWN'),

    ('SMDirect','Surround Mode DIRECT', None, 'MSDIRECT'),
    ('SMPureDirect','Surround Mode PURE DIRECT', None, 'MSPURE DIRECT'),
    ('SMStereo','Surround Mode STEREO', None, 'MSSTEREO'),

    ('SMAUTO', 'Surround Mode Auto (Marantz)', None, 'MSAUTO'),
    ('SMSTANDARD', 'Surround Mode STANDARD (Marantz)', None, 'MSSTANDARD'),
    ('SMNEURAL', 'Surround Mode NEURAL (Marantz)', None, 'MSNEURAL'),
    ('SMDOLBY', 'Surround Mode Dolby (Marantz)', None, 'MSDOLBY DIGITAL'),
    ('SMDTS', 'Surround Mode DTS (Marantz)', None, 'MSDTS SURROUND'),
    ('SMMCSTEREO', 'Surround Mode MCH STEREO (Marantz)', None, 'MSMCH STEREO'),

    ('ModeMusic', 'Programm Mode Music', None, 'PSMODE:MUSIC'),
    ('ModeCinema', 'Programm Mode Cinema', None, 'PSMODE:CINEMA'),
    ('ModeGame', 'Programm Mode Game', None, 'PSMODE:GAME'),
)),

)




class NetworkSender(eg.PluginBase):

    def __init__(self):

        self.AddActionsFromList(ACTIONS, Send_Action)
        self.AddAction(Send_Custom_Action)
        self.AddAction(Close_Socket)
        self.AddAction(Open_Socket)


    def __start__(self, ip, port):
        self.ip = ip
        self.port = port
        self.Connect()

    def __stop__(self):
    	self.socket.close()


    def Configure(self, ip="127.0.0.1", port=23):

        panel = eg.ConfigPanel()
        ipCtrl = panel.TextCtrl(ip)
        portCtrl = panel.SpinIntCtrl(port, max=65535)

        st1 = panel.StaticText("IP")
        st2 = panel.StaticText("Port")
        eg.EqualizeWidths((st1, st2))
        tcpBox = panel.BoxedGroup(
            "TCP/IP Settings",
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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(1.0)
        self.socket = s

        ip = self.ip
        port = self.port
        try:
            s.connect((ip, port))
        except Exception as e:
            print "Failed to connect to " + ip + ":" + str(port), e
        else:
            print "Connected to " + ip + ":" + str(port)

class Send_Action(eg.ActionBase):
    def __call__(self):
        line = str(self.value)+'\r'

        try:
            self.plugin.socket.sendall(line)
            sleep(0.1)
        except socket.error, msg:
            print "Error sending command, retrying", msg
            self.plugin.Connect()
            try:
                self.plugin.socket.sendall(line)
            except socket.error, msg:
                print "Error sending command", msg

class Send_Custom_Action(eg.ActionBase):

    def __call__(self, myAction=""):

        line = str(myAction)+'\r'
        #eg.Print(line)
        try:
            self.plugin.socket.sendall(line)
            sleep(0.1)
        except socket.error, msg:
            print "Error sending command, retrying", msg
            self.plugin.Connect()
            try:
                self.plugin.socket.sendall(line)
            except socket.error, msg:
                print "Error sending command", msg


    def Configure( self, myAction ="" ):
        panel = eg.ConfigPanel()
        actionCtrl = panel.TextCtrl(myAction)
        panel.AddLine("Action: ", actionCtrl)

        while panel.Affirmed():
            panel.SetResult(actionCtrl.GetValue())

class Open_Socket(eg.ActionBase):

    def __call__(self):
        self.plugin.Connect()

class Close_Socket(eg.ActionBase):

    def __call__(self):
        self.plugin.socket.close()


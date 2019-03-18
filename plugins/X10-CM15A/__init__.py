# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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
#
#

import eg

import wx

import string

import comtypes.client as comcli


x10_cm15a = None
cm15a = None


#####################################################
eg.RegisterPlugin(
    name = "X10_CM15A",
    guid='{EF6F634B-04B2-4243-B0C4-2BEDA4E05D01}',
    author = "Dean Owens",
    version = "0.1",
    kind = "remote",
    description = (
        'Hardware plugin for the <a href="http://www.x10.com/activehomepro/sneakpreview.html">'
        'CM15A</a> transceiver.'
        '\n\n<p>'
        '<a href="http://www.x10.com/activehomepro/sneakpreview.html"><p>'
        '<center><img src="picture.jpg" alt="CM15A" /></a></center>'
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAYklEQVR42mNkoBAwwhgq"
        "uf//k6LxzmRGRrgBpGpGNoSRXM1wL1DFgNuTGBhU8xCCyHx0Ngggq4W7AKYQlwZchqJ4"
        "Ad0l+AymvgHYFBJtAFUCkaJopMgAEEFRUoZxKMpMlAAAoBBdp8TBL7gAAAAASUVORK5C"
        "YII="
    ),
)


#####################################################
class Text:
    class TransmitX10:
        name = "Transmit X10"
        description = "Transmits an X10 command via the CM15A hardware."
        irCode = "X10 Command:"
        x10CmdType = "Command:"
        x10CmdTypeChoices = ( "PLC", "RF" )
        x10HouseCode = "House Code:"
        x10HouseCodeChoices = ( "A", "B", "C", "D", "E", "F", "G", "H",
            "I", "J", "K", "L", "M", "N", "O", "P")
        x10UnitCode = "Unit Code:"
        x10UnitCodeChoices = ( "1", "2", "3", "4", "5", "6", "7", "8",
            "9", "10", "11", "12", "13", "14", "15", "16" )
        x10State = "State:"
        x10StateChoices = ("Off", "On", "Bright", "Dim", "AllLightsOff", "AllLightsOn" )
        x10Percent = "Percent:"
        x10PercentChoices = ("0", "5", "10", "15", "20", "25", "30", "35", "40", "45", "50",
            "55", "60", "65", "70", "75", "80", "85", "90", "95", "100")


#####################################################
class X10_CM15A(eg.RawReceiverPlugin):
    conn = None
    eventHandler = None
    enabled = False

    text = Text

    def __init__(self):
        global x10_cm15a
        x10_cm15a = self
        eg.RawReceiverPlugin.__init__(self)
        self.enabled = False
        self.AddAction(TransmitX10)

    def __start__(self):
        try:
            global cm15a
            cm15a = comcli.CreateObject("X10.ActiveHome")
        except:
            cm15a = None
            eg.PrintError("X10_CM15A start error")

        eventHandler = self.EventHandler()
        try:
            self.conn = comcli.GetEvents(cm15a, eventHandler)
            self.enabled = True
            eg.PrintNotice("X10_CM15A started...")
        except AttributeError:
            self.conn = None
            self.enabled = False
            eg.PrintNotice("X10_CM15A could not connect!")

    def __stop__(self):
        global cm15a
        if self.enabled == True:
            self.enabled = False
            if self.conn:
                del self.conn
                self.conn = None
            if cm15a:
                del cm15a
                cm15a = None
            print "X10_CM15A stopped..."


    class EventHandler():
        """Event handler for CM15A COM events."""

        def __getattr__(self, name):
            "Create event handler methods on demand"
            if name.startswith("__") and name.endswith("__"):
                raise AttributeError(name)

            def handler(*args):
                if args[1] == "recvplc":
                    cmdType = "PLC"
                elif args[1] == "recvrf":
                    cmdType = "RF"
                else:
                    cmdType = "Unknown"
                if x10_cm15a.enabled:
                    x10_cm15a.TriggerEvent(" Recv, %s, %s, %s, %s" % (cmdType,
                        string.upper(args[2]), args[3], args[4]))
                return comcli.S_OK

            return handler


    def Configure(self):
        panel = eg.ConfigPanel(self)
        while panel.Affirmed():
            panel.SetResult()


#####################################################
class TransmitX10(eg.ActionClass):
    x10CmdType = 0
    x10HouseCode = 0
    x10UnitCode = 0
    x10State = 0
    x10Percent = 0


    def __call__(self, x10CmdType_, x10HouseCode_, x10UnitCode_, x10State_, x10Percent_):
        text = self.text
        
        if text.x10CmdTypeChoices[x10CmdType_] == "PLC":
            x10CmdType = "sendplc"
        elif text.x10CmdTypeChoices[x10CmdType_] == "RF":
            x10CmdType = "sendrf"
        else:
            x10CmdType = None

        if text.x10StateChoices[x10State_] == "Bright" or text.x10StateChoices[x10State_] == "Dim":
            x10State = text.x10StateChoices[x10State_] + " " + text.x10PercentChoices[x10Percent_]
        else:
            x10State = text.x10StateChoices[x10State_]

        cm15a.SendAction(x10CmdType,
            text.x10HouseCodeChoices[x10HouseCode_] + text.x10UnitCodeChoices[x10UnitCode_] + " " + \
            x10State,
            None, None
        )


    def GetLabel(self, x10CmdType, x10HouseCode, x10UnitCode, x10State, x10Percent):
        text = self.text
        retStr = "Send, " + \
            text.x10CmdTypeChoices[x10CmdType] + ", " + \
            text.x10HouseCodeChoices[x10HouseCode] + \
            text.x10UnitCodeChoices[x10UnitCode] + ", " + \
            text.x10StateChoices[x10State]
        if text.x10StateChoices[x10State] == "Bright" or text.x10StateChoices[x10State] == "Dim":
            retStr += ", " + text.x10PercentChoices[x10Percent]
        return retStr

    def Configure(self, x10CmdType = None, x10HouseCode = None, x10UnitCode = None, 
        x10State = None, x10Percent = None):
        text = self.text

        panel = eg.ConfigPanel(self)

        if x10CmdType is None:
            x10CmdType = self.x10CmdType

        if x10HouseCode is None:
            x10HouseCode = self.x10HouseCode

        if x10UnitCode is None:
            x10UnitCode = self.x10UnitCode

        if x10State is None:
            x10State = self.x10State

        if x10Percent is None:
            x10Percent = self.x10Percent

        x10CmdTypeCtrl = wx.Choice(panel, -1, choices=text.x10CmdTypeChoices)
        x10CmdTypeCtrl.Select(x10CmdType)

        x10HouseCodeCtrl = wx.Choice(panel, -1, choices=text.x10HouseCodeChoices)
        x10HouseCodeCtrl.Select(x10HouseCode)

        x10UnitCodeCtrl = wx.Choice(panel, -1, choices=text.x10UnitCodeChoices)
        x10UnitCodeCtrl.Select(x10UnitCode)

        x10StateCtrl = wx.Choice(panel, -1, choices=text.x10StateChoices)
        x10StateCtrl.Select(x10State)

        x10PercentCtrl = wx.Choice(panel, -1, choices=text.x10PercentChoices)
        x10PercentCtrl.Select(x10Percent)

        stFlags = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT

        gridSizer = wx.GridBagSizer(5,5)
        gridSizer.Add(panel.StaticText(text.x10CmdType), (1,0), flag=stFlags)
        gridSizer.Add(x10CmdTypeCtrl, (1,1), flag=stFlags | wx.EXPAND)
        gridSizer.Add(panel.StaticText(text.x10HouseCode), (2,0), flag=stFlags)
        gridSizer.Add(x10HouseCodeCtrl, (2,1), flag=stFlags | wx.EXPAND)
        gridSizer.Add(panel.StaticText(text.x10UnitCode), (3,0), flag=stFlags)
        gridSizer.Add(x10UnitCodeCtrl, (3,1), flag=stFlags | wx.EXPAND)
        gridSizer.Add(panel.StaticText(text.x10State), (4,0), flag=stFlags)
        gridSizer.Add(x10StateCtrl, (4,1), flag=stFlags | wx.EXPAND)
        gridSizer.Add(panel.StaticText(text.x10Percent), (5,0), flag=stFlags)
        gridSizer.Add(x10PercentCtrl, (5,1), flag=stFlags | wx.EXPAND)

        panel.sizer.Add(gridSizer, 0)

        def GetResult():
            x10CmdType = x10CmdTypeCtrl.GetSelection()
            x10HouseCode = x10HouseCodeCtrl.GetSelection()
            x10UnitCode = x10UnitCodeCtrl.GetSelection()
            x10State = x10StateCtrl.GetSelection()
            x10Percent = x10PercentCtrl.GetSelection()
            return (
                x10CmdType,
                x10HouseCode,
                x10UnitCode,
                x10State,
                x10Percent,
            )

        while panel.Affirmed():
            panel.SetResult(*GetResult())


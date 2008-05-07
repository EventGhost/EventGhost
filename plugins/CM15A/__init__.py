# This file is part of EventGhost.
# Copyright (C) 2007 Dean Owens
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
# Version 0.2 changes by Bitmonster:
# - removed Configure() from plugin, because there are currently no options 
#   to set.
# - removed print statements
# - moved eg.RegisterPlugin to be the first code statement
# - transferred code to use win32com instead of comtypes
# - re-arranged the layout of the configuration dialog for TransmitX10 action
# - percent control will only get enabled, if command supports it 
# - removed a lot of "x10" prefixes from variables
# - added a separate thread to handle X10 notifications
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$


eg.RegisterPlugin(
    name = "X10 CM15A",
    author = "Dean Owens",
    version = "0.2." + "$LastChangedRevision$".split()[1],
    kind = "remote",
    description = (
        'Hardware plugin for the <a href="http://www.x10.com/activehomepro/sneakpreview.html">'
        'CM15A</a> transceiver.'
        '\n\n<p>'
        '<a href="http://www.x10.com/activehomepro/sneakpreview.html"><p>'
        '<center><img src="picture.jpg" alt="CM15A" /></a></center>'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=667",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAYklEQVR42mNkoBAwwhgq"
        "uf//k6LxzmRGRrgBpGpGNoSRXM1wL1DFgNuTGBhU8xCCyHx0Ngggq4W7AKYQlwZchqJ4"
        "Ad0l+AymvgHYFBJtAFUCkaJopMgAEEFRUoZxKMpMlAAAoBBdp8TBL7gAAAAASUVORK5C"
        "YII="
    ),
)

from win32com.client import DispatchWithEvents


class Text:
    class TransmitX10:
        name = "Transmit X10"
        description = "Transmits an X10 command via the CM15A hardware."
        cmdType = "Command:"
        cmdTypeChoices = ("Powerline", "Radio Frequency")
        houseCode = "House Code:"
        unitCode = "Unit Code:"
        state = "State:"
        stateChoices = ("Off", "On", "Bright", "Dim", "All Lights Off", "All Lights On")
        percent = "Percent:"
        sendLabel = "Send"


CMD_TYPE_PLC = 0
CMD_TYPE_RF = 1

STATE_OFF = 0
STATE_ON = 1
STATE_BRIGHT = 2
STATE_DIM = 3
STATE_ALL_LIGHTS_OFF = 4
STATE_ALL_LIGHTS_ON = 5

STATE_CODES = ("Off", "On", "Bright", "Dim", "AllLightsOff", "AllLightsOn")
HOUSE_CODES = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", 
    "M", "N", "O", "P")
UNIT_CODES = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", 
    "12", "13", "14", "15", "16")
PERCENT_CODES = ("0", "5", "10", "15", "20", "25", "30", "35", "40", "45", 
    "50", "55", "60", "65", "70", "75", "80", "85", "90", "95", "100")
PERCENT_STATES = (STATE_BRIGHT, STATE_DIM)


class EventHandler():
    """Event handler for CM15A COM events."""

    def OnRecvAction(self, actionType, address, command, data, *args):
        if actionType == "recvplc":
            cmdType = "PLC"
        elif actionType == "recvrf":
            if data == 0:
                self.plugin.TriggerEnduringEvent(
                    "%s.%s.%s" % ("RF", address.upper(), command)
                )
            elif data == -1:
                self.plugin.EndLastEvent()
            return
        else:
            cmdType = "Unknown"
        self.plugin.TriggerEvent(
            "%s.%s.%s.%s" % (cmdType, address.upper(), command, data)
        )


# we need a separate thread to receive events, because otherwise it would not
# be possible to receive notifications while some action is executing

class CM15AWorkerThread(eg.ThreadWorker):
    comInstance = None
    
    def Setup(self, plugin):
        self.plugin = plugin
        class TmpHandler(EventHandler):
            plugin = self.plugin
        self.comInstance = DispatchWithEvents('X10.ActiveHome', TmpHandler)
        plugin.SendAction = self.comInstance.SendAction

        
    def Finish(self):
        if self.comInstance:
            self.comInstance.close()
            self.plugin.SendAction = None
            del self.comInstance
        
        


class X10_CM15A(eg.PluginClass):
    text = Text

    def __init__(self):
        self.AddAction(TransmitX10)


    def __start__(self):
        self.workerThread = CM15AWorkerThread(self)
        try:
            self.workerThread.Start()
        except:
            raise self.Exceptions.DeviceNotFound


    def __stop__(self):
        self.workerThread.Stop()



class TransmitX10(eg.ActionClass):
    cmdType = 0
    houseCode = 0
    unitCode = 0
    state = 0
    percentIndex = 0

    def __call__(self, cmdType, houseCode, unitCode, state, percentIndex):
        if cmdType == CMD_TYPE_PLC:
            cmdType = "sendplc"
        elif cmdType == CMD_TYPE_RF:
            cmdType = "sendrf"
        else:
            cmdType = None

        cmd = HOUSE_CODES[houseCode] + UNIT_CODES[unitCode]
        cmd += " " + STATE_CODES[state]
        if state in PERCENT_STATES:
            cmd += " " + PERCENT_CODES[percentIndex]

        self.plugin.SendAction(cmdType, cmd, None, None)


    def GetLabel(self, cmdType, houseCode, unitCode, state, percentIndex):
        text = self.text
        parts = [
            text.sendLabel,
            text.cmdTypeChoices[cmdType],
            HOUSE_CODES[houseCode] + UNIT_CODES[unitCode],
            text.stateChoices[state],
        ]
        if state in PERCENT_STATES:
            parts.append(PERCENT_CODES[percentIndex] + "%")
        return ", ".join(parts)


    def Configure(
        self, 
        cmdType = None, 
        houseCode = None, 
        unitCode = None, 
        state = None, 
        percentIndex = None
    ):
        text = self.text

        panel = eg.ConfigPanel(self)

        stFlags = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT
        gridSizer = wx.GridBagSizer(5,5)

        if cmdType is None:
            cmdType = self.cmdType

        if houseCode is None:
            houseCode = self.houseCode

        if unitCode is None:
            unitCode = self.unitCode

        if state is None:
            state = self.state

        if percentIndex is None:
            percentIndex = self.percentIndex

        cmdTypeCtrl = panel.Choice(cmdType, text.cmdTypeChoices)
        houseCodeCtrl = panel.Choice(houseCode, HOUSE_CODES)
        unitCodeCtrl = panel.Choice(unitCode, UNIT_CODES)
        stateCtrl = panel.Choice(state, text.stateChoices)
        percentCtrl = panel.Choice(percentIndex, PERCENT_CODES)
        
        # disable the percent choice if command doesn't supports it
        def OnStateChoice(event):
            percentCtrl.Enable(stateCtrl.GetValue() in PERCENT_STATES)
            event.Skip()
        stateCtrl.Bind(wx.EVT_CHOICE, OnStateChoice)
        OnStateChoice(wx.CommandEvent())
        
        stFlags = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT
        gridSizer = wx.GridBagSizer(10,5)

        gridSizer.Add(panel.StaticText(text.cmdType), (0,0), flag=stFlags)
        gridSizer.Add(cmdTypeCtrl, (0,1), flag=wx.EXPAND)

        gridSizer.Add(panel.StaticText(text.houseCode), (1,0), flag=stFlags)
        gridSizer.Add(houseCodeCtrl, (1,1), flag=wx.EXPAND)

        gridSizer.Add(panel.StaticText(text.unitCode), (2,0), flag=stFlags)
        gridSizer.Add(unitCodeCtrl, (2,1), flag=wx.EXPAND)

        gridSizer.Add(panel.StaticText(text.state), (3,0), flag=stFlags)
        gridSizer.Add(stateCtrl, (3,1), flag=wx.EXPAND)

        gridSizer.Add(panel.StaticText(text.percent), (4,0), flag=stFlags)
        gridSizer.Add(percentCtrl, (4,1), flag=wx.EXPAND)

        panel.sizer.Add(gridSizer, 0, wx.EXPAND)

        def GetResult():
            # assign the values to self, so next configure will use current
            # values as defaults
            self.cmdType = cmdTypeCtrl.GetSelection()
            self.houseCode = houseCodeCtrl.GetSelection()
            self.unitCode = unitCodeCtrl.GetSelection()
            self.state = stateCtrl.GetSelection()
            self.percentIndex = percentCtrl.GetSelection()
            return (
                self.cmdType,
                self.houseCode,
                self.unitCode,
                self.state,
                self.percentIndex,
            )

        while panel.Affirmed():
            panel.SetResult(*GetResult())


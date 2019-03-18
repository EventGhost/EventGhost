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
# $LastChangedDate: 2009-05-15 12:00:002 +0800 $
# $LastChangedRevision: 500 $
# $LastChangedBy: kingtd $

import eg

eg.RegisterPlugin(
    name="VMC Controller",
    guid='{1F36E902-541E-44E7-B45F-CC34F967AD9C}',
    description="Receives events from a Vista Media Center with the controller installed from http://www.codeplex.com/VmcController",
    kind="external",
    version="0.5." + "$LastChangedRevision: 348 $".split()[1],
    author="kingtd (based off original code from Bitmonster)",
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QAAAAAAAD5Q7t/"
        "AAAACXBIWXMAAAsSAAALEgHS3X78AAAAB3RJTUUH1gIQFgQb1MiCRwAAAVVJREFUOMud"
        "kjFLw2AQhp8vif0fUlPoIgVx6+AgopNI3fwBViiIoOAgFaugIDhUtP4BxWDs4CI4d3MR"
        "cSyIQ1tDbcHWtjFI4tAWG5pE8ca7997vnrtP4BOZvW0dSBAcZ0pAMTEzPUs4GvMsVkvP"
        "6HktGWRAOBpjIXVNKOSWWdYXN7lFAAINhBCEQgqxyTHAAQQAD/dFbLurUYJYT7P7TI2C"
        "VavwIiZodyyaH6ZLo/RZVTXiOYVhGOh5jcpbq5eRAXAc5wdBVSPMLR16GtxdbgJgN95d"
        "OxicACG6bPH4uIu1UHjE7sFqR/NDVxhaoixLvFYbtDufNFtu1tzxgdeAaZfBU7ECTvd1"
        "WRlxsa4sp1ydkiRxkstmlEFRrWT4nrRer3vmlf6mb883fK8AoF1d+Bqc6Xkt+cufT6e3"
        "dnb9DJJrq+uYpunZ2WcFfA0ol8v8N5Qgvr/EN8Lzfbs+L0goAAAAAElFTkSuQmCC"
    ),
)

import asynchat
import socket
import time


class Text:
    host = "Hostname/IP Address:"
    port = "Listen Port:"
    controlport = "Command Port:"
    eventPrefix = "Event Prefix:"
    rconfail = "Attempt reconnect on send"
    rconset = "Reconnect"
    tcpBox = "TCP/IP Settings"
    securityBox = "Security"
    eventGenerationBox = "Event generation"

    class Send:
        name = "Send"


class VMCstatus(asynchat.async_chat):
    """Telnet engine class. Implements command line user interface."""

    def __init__(self, host, port, plugin):

        asynchat.async_chat.__init__(self)

        self.set_terminator("\n")

        self.data = ""
        self.host = host
        self.port = port
        self.plugin = plugin

        # connect to VMC Status Engine
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        eg.RestartAsyncore()
        self.connect((host, port))

    def handle_connect(self):
        # connection succeeded
        self.plugin.TriggerEvent("Status Session Connected", str(self.host) + ":" + str(self.port))
        pass

    def handle_close(self):
        self.plugin.TriggerEvent("Status Session Closed", str(self.host) + ":" + str(self.port))
        self.close()

    def handle_expt(self):
        # connection failed
        self.plugin.TriggerEvent("Status Session Could Not Connect", str(self.host) + ":" + str(self.port))
        self.close()

    def collect_incoming_data(self, data):
        # received a chunk of incoming data
        self.data = self.data + data

    def found_terminator(self):
        # got a response line
        data = self.data
        if data.endswith("\r"):
            data = data[:-1]
        self.data = ""
        if (data.find("=") > -1):
            dcmd = data[:data.find("=")]
            dpay = data[data.find("=") + 1:]
            self.plugin.TriggerEvent(dcmd, dpay)
        elif (data.find("204 Connected") > -1):
            dcmd = "204 Connected"
            dpay = data[data.find("204 Connected") + 14:]
            self.plugin.TriggerEvent(dcmd, dpay)
        else:
            self.plugin.TriggerEvent(data)


class VMCcommander(asynchat.async_chat):
    """Telnet engine class. Implements command line user interface."""

    def __init__(self, host, controlport, plugin):

        asynchat.async_chat.__init__(self)

        self.set_terminator("\n")

        self.data = ""
        self.host = host
        self.controlport = controlport
        self.plugin = plugin

        # connect to VMC Command Engine
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        eg.RestartAsyncore()
        self.connect((host, controlport))

    def handle_connect(self):
        # connection succeeded
        pass

    def handle_close(self):
        self.plugin.TriggerEvent("Control Session Closed", str(self.host) + ":" + str(self.controlport))
        self.close()
        self.plugin.commander = None

    def handle_expt(self):
        # connection failed
        self.plugin.TriggerEvent("Control Session Could Not Connect", str(self.host) + ":" + str(self.controlport))
        self.close()
        self.plugin.commander = None

    def collect_incoming_data(self, data):
        # received a chunk of incoming data
        self.data = self.data + data

    def found_terminator(self):
        # got a response line
        data = self.data
        if data.endswith("\r"):
            data = data[:-1]
        self.data = ""
        if (data.find("204 Connected") > -1):
            dcmd = "204 Connected"
            dpay = data[data.find("204 Connected") + 14:]
            self.plugin.TriggerEvent(dcmd, dpay)
        else:
            self.plugin.TriggerEvent(data)

    def vmcsend(self, data):
        self.push(str(data) + "\r\n")


class VMCControl(eg.PluginClass):
    canMultiLoad = True
    text = Text

    def __init__(self):
        self.AddAction(self.Send)
        self.AddAction(self.Connect)

    def __start__(self, host, port, controlport, prefix, rcon):
        self.host = host
        self.port = port
        self.rcon = rcon
        self.controlport = controlport
        self.info.eventPrefix = prefix

        try:
            self.status = VMCstatus(self.host, self.port, self)
        except socket.error, exc:
            raise self.Exception(exc[1])

        try:
            self.commander = VMCcommander(self.host, self.controlport, self)
        except socket.error, exc:
            raise self.Exception(exc[1])

    def __stop__(self):
        if self.status:
            self.status.close()
        self.status = None

    def Configure(self, host="127.0.0.1", port=40400, controlport=40500, prefix="VMC", rcon=True):
        text = self.text
        panel = eg.ConfigPanel(self)

        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        controlportCtrl = panel.SpinIntCtrl(controlport, max=65535)
        eventPrefixCtrl = panel.TextCtrl(prefix)
        rconCtrl = wx.CheckBox(panel, -1, text.rconfail)
        rconCtrl.SetValue(rcon)

        st1 = panel.StaticText(text.host)
        st2 = panel.StaticText(text.port)
        st3 = panel.StaticText(text.controlport)
        st4 = panel.StaticText(text.eventPrefix)
        eg.EqualizeWidths((st1, st2, st3, st4))

        box1 = panel.BoxedGroup(text.tcpBox, (st1, hostCtrl), (st2, portCtrl), (st3, controlportCtrl))
        box2 = panel.BoxedGroup(text.eventGenerationBox, (st4, eventPrefixCtrl))
        box3 = panel.BoxedGroup(text.rconset, (st4, rconCtrl))
        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND | wx.TOP, 10),
            (box3, 0, wx.EXPAND),

        ])

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                controlportCtrl.GetValue(),
                eventPrefixCtrl.GetValue(),
                rconCtrl.GetValue(),
            )

    class Send(eg.ActionWithStringParameter):
        description = ("Sends a command to VMC Controller.")

        class Text:
            action = "VMC Command:"

        def __call__(self, action):
            self.SendCommand(action)
            return True

        def SendCommand(self, action):
            print("Reconnect on Failure:" + str(self.plugin.rcon))
            if self.plugin.commander:
                self.plugin.commander.vmcsend(action)
            else:
                print("Control Connection Not Available")
                if self.plugin.rcon:
                    self.plugin.TriggerEvent("Command Failed No Connection (Retrying)", action)
                    try:
                        self.plugin.commander = VMCcommander(self.plugin.host, self.plugin.controlport, self.plugin)
                    except socket.error, exc:
                        raise self.Exception(exc[1])

                    time.sleep(2)
                    if self.plugin.commander:
                        self.plugin.commander.vmcsend(action)
                    else:
                        self.plugin.TriggerEvent("Command Failed No Connection", action)
                else:
                    self.plugin.TriggerEvent("Command Failed No Connection", action)

        def Configure(self, action=""):
            text = self.text
            panel = eg.ConfigPanel(self)

            actionCtrl = panel.TextCtrl(action)
            st1 = panel.StaticText("Command:")
            box1 = panel.BoxedGroup("Command", (st1, actionCtrl))
            panel.sizer.AddMany([
                (box1, 0, wx.EXPAND)
            ])

            while panel.Affirmed():
                panel.SetResult(
                    actionCtrl.GetValue(),
                )

    class Connect(eg.ActionWithStringParameter):
        description = ("Attempts Reconnect to VMC.")

        class Text:
            action = "Action:"
            cmdhelp = "- The Command Port should be reconnected whenever Media Center is restarted.\r\n- The Status Port should be reconnected whenever the MSAS service restarts."

        def __call__(self, action):
            self.VMCConnect(action)
            return True

        def VMCConnect(self, action):
            if action == "Command Port" or action == "Status and Command Port":
                if self.plugin.commander:
                    self.plugin.commander.close()
                    self.plugin.commander = None
                try:
                    self.plugin.commander = VMCcommander(self.plugin.host, self.plugin.controlport, self.plugin)
                except socket.error, exc:
                    raise self.Exception(exc[1])
            if action == "Status Port" or action == "Status and Command Port":
                if self.plugin.status:
                    self.plugin.status.close()
                    self.plugin.status = None
                try:
                    self.plugin.status = VMCstatus(self.plugin.host, self.plugin.port, self.plugin)
                except socket.error, exc:
                    raise self.Exception(exc[1])

        def Configure(self, action=""):
            text = self.Text
            panel = eg.ConfigPanel(self)
            cmdlist = ["Command Port", "Status Port", "Status and Command Port"]
            cmdCtrl = wx.Choice(panel, -1, choices=cmdlist)

            if action == "Status and Command Port":
                cmdCtrl.SetSelection(2)
            elif action == "Status Port":
                cmdCtrl.SetSelection(1)
            else:
                cmdCtrl.SetSelection(0)

            cmdhelpText = wx.StaticText(panel, -1, text.cmdhelp)

            st1 = panel.StaticText("Command:")
            box1 = panel.BoxedGroup("Information:", (cmdhelpText))
            box2 = panel.BoxedGroup("Reconnect", (cmdCtrl))
            panel.sizer.AddMany([
                (box1, 0, wx.EXPAND),
                (box2, 0, wx.EXPAND)
            ])

            while panel.Affirmed():
                panel.SetResult(
                    cmdlist[cmdCtrl.GetSelection()],
                )

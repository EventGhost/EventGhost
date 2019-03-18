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
# $LastChangedDate: 2008-06-26 12:06:42 +0100 (Di, 04 Mrz 2008) $
# $LastChangedRevision: 348 $
# $LastChangedBy: kingtd $

import eg

eg.RegisterPlugin(
    name="ISY Event Receiver 0.2",
    guid='{D572187E-076D-4B38-B339-43EBA5D28C06}',
    description="Receives events from an ISY-26 Insteon ethernet bridge (www.universal-devices.com)",
    kind="external",
    version="0.2." + "$LastChangedRevision: 348 $".split()[1],
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


class Text:
    host = "Hostname/IP Address:"
    port = "TCP/IP Port:"
    username = "Username:"
    password = "Password:"
    eventPrefix = "Event Prefix:"
    showhb = "Trigger on Heartbeat:"
    tcpBox = "TCP/IP Settings"
    securityBox = "Security"
    eventGenerationBox = "Event generation"

    class Send:
        name = "Send"


class ISYeventer(asynchat.async_chat):
    """Telnet engine class. Implements command line user interface."""

    def __init__(self, host, port, plugin):

        asynchat.async_chat.__init__(self)

        self.set_terminator("\n")

        self.data = ""
        self.host = host
        self.port = port
        self.plugin = plugin

        # connect to ftp server
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        eg.RestartAsyncore()
        self.connect(("lights", 80))

    def handle_connect(self):
        # connection succeeded
        subscribestr = "<s:Envelope><s:Body><u:Subscribe xmlns:u=\"urn:udi-com:service:X_Insteon_Lighting_Service:1\"></u:Subscribe></s:Body></s:Envelope>"

        self.push("SUBSCRIBE /eventing HTTP/1.1\r\n")
        self.push("Host: " + str(self.host) + ":" + str(self.port) + "\r\n")
        self.push("Content-Length: " + str(len(subscribestr)) + "\r\n")
        self.push("Content-Type: text/xml; charset=\"utf-8\"\r\n")
        self.push("CALLBACK:<REUSE_SOCKET>\r\n")
        self.push("NT:upnp:event\r\n")
        self.push("TIMEOUT:Second-infinite\r\n")
        self.push("SOAPACTION:\"urn:udi-com:service:X_Insteon_Lighting_Service:1#Subscribe\"\r\n\r\n")

        self.push(subscribestr + "\r\n")

    def handle_close(self):
        self.plugin.TriggerEvent("Subscription-Closed", str(self.host) + ":" + str(self.port))
        self.close()

    def handle_expt(self):
        # connection failed
        self.plugin.TriggerEvent("Subscription-Error", str(self.host) + ":" + str(self.port))
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

        if (data.find("HTTP/1.1 200 OK") > -1):
            self.plugin.TriggerEvent("Subscribed", str(self.host) + ":" + str(self.port))

        if (data.find("<e:propertyset xmlns:e=\"urn:schemas-upnp-org:event-1-0\">") > -1):
            eprops = data[data.find("<e:propertyset") + 56:data.find("</e:propertyset")]
            # print "E:",eprops
            status = "None"
            node = "None"
            Heartbeat = "None"
            while (eprops.find("<e:property>") > -1):
                dpoint = eprops[eprops.find("<e:property>") + 12:eprops.find("</e:property>")]
                eprops = eprops[eprops.find("</e:property>") + 13:]
                tpoint = dpoint[dpoint.find("<") + 1:dpoint.find(">")]
                dpoint = dpoint[dpoint.find(">") + 1:dpoint.find("</")]
                # print "Type: ",tpoint, "Data: ",dpoint
                if (tpoint == "node"):
                    node = dpoint
                if (tpoint == "ST"):
                    status = dpoint
                # if (tpoint=="RR"):
                #	status=dpoint
                if (tpoint == "_0"):
                    Heartbeat = "Heartbeat"
            if (node != "None" and status != "None"):
                self.plugin.TriggerEvent(str(node) + ":" + str(status))
    # if (Heartbeat == "Heartbeat"):
#	self.plugin.TriggerEvent("Heartbeat")


class ISYEvent(eg.PluginClass):
    canMultiLoad = True
    text = Text

    def __init__(self):
        self.eventer = None
        self.AddAction(self.Send)

    def __start__(self, host, port, username, password, prefix):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.info.eventPrefix = prefix
        try:
            authenticated = self.Authenticate()
        except:
            eg.PrintTraceback()

        if authenticated:
            try:
                self.eventer = ISYeventer(self.host, self.port, self)
            except socket.error, exc:
                raise self.Exception(exc[1])

    def __stop__(self):
        if self.eventer:
            self.eventer.close()
        self.eventer = None

    def Authenticate(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket = sock
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(12.0)

        self.host = "lights"
        self.port = 80
        self.username = "admin"
        self.password = "admin"

        connected = False
        try:
            sock.connect((self.host, self.port))
            connected = True
            sock.settimeout(10.0)
            # First wake up the server, for security reasons it does not
            # respond by it self it needs this string, why this odd word ?
            # well if someone is scanning ports "connect" would be very 
            # obvious this one you'd never guess :-) 

            authstr = "<s:Envelope><s:Body><u:Authenticate xmlns:u=\"urn:udi-com:service:X_Insteon_Lighting_Service:1\"><name>" + self.username + "</name><id>" + self.password + "</id></u:Authenticate></s:Body></s:Envelope>"

            sock.send("POST /services HTTP/1.1\r\n")
            sock.send("Host: " + str(self.host) + ":" + str(self.port) + "\r\n")
            sock.send("Content-Length: " + str(len(authstr)) + "\r\n")
            sock.send("Content-Type: text/xml; charset=\"utf-8\"\r\n")
            sock.send("SOAPACTION:\"urn:udi-com:service:X_Insteon_Lighting_Service:1#Authenticate\"\r\n\r\n")

            sock.send(authstr + "\r\n")

            # Get the answer
            answer = sock.recv(1024)

            # If the password was correct and you are allowed to connect
            # to the server, you'll get "accept"
            if (answer.find("HTTP/1.1 200 OK") == -1):
                self.PrintError("Could not authenticate to Insteon ISY")
                self.PrintError(answer.strip())
                sock.close()
                return False
            self.TriggerEvent("Authenticated", str(self.host) + ":" + str(self.port))
            sock.close()
            return True

        except:
            # if eg.debugLevel:
            eg.PrintTraceback()
            sock.close()
            return None

    def Configure(self, host="insteon", port=80, username="admin", password="admin", prefix="Insteon"):
        text = self.text
        panel = eg.ConfigPanel(self)

        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        usernameCtrl = panel.TextCtrl(username)
        passwordCtrl = panel.TextCtrl(password, style=wx.TE_PASSWORD)
        eventPrefixCtrl = panel.TextCtrl(prefix)
        st1 = panel.StaticText(text.host)
        st2 = panel.StaticText(text.port)
        st3 = panel.StaticText(text.username)
        st4 = panel.StaticText(text.password)
        st5 = panel.StaticText(text.eventPrefix)
        eg.EqualizeWidths((st1, st2, st3, st4, st5))
        box1 = panel.BoxedGroup(text.tcpBox, (st1, hostCtrl), (st2, portCtrl))
        box2 = panel.BoxedGroup(text.securityBox, (st3, usernameCtrl), (st4, passwordCtrl))
        box3 = panel.BoxedGroup(text.eventGenerationBox, (st5, eventPrefixCtrl))
        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND | wx.TOP, 10),
            (box3, 0, wx.EXPAND | wx.TOP, 10),
        ])

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                usernameCtrl.GetValue(),
                passwordCtrl.GetValue(),
                eventPrefixCtrl.GetValue()
            )

    class Send(eg.ActionWithStringParameter):
        description = ("Sends a command through the ISY-26.")

        class Text:
            control = "Control:"
            action = "Action:"
            flag = "Flag:"
            node = "Node:"

        def __call__(self, control, action, flag, node):
            self.SendCommand(control, action, flag, node)
            return True

        def SendCommand(self, control, action, flag, node):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.socket = sock
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(12.0)

            connected = False
            try:
                sock.connect((self.plugin.host, self.plugin.port))
                connected = True
                sock.settimeout(10.0)
                cmdstr = "<s:Envelope><s:Body><u:UDIService xmlns:u='urn:udi-com:service:X_Insteon_Lighting_Service:1'><control>" + control + "</control><action>" + action + "</action><flag>" + flag + "</flag><node>" + node + "</node></u:UDIService></s:Body></s:Envelope>"

                sock.send("POST /services HTTP/1.1\r\n")
                sock.send("Host: " + str(self.plugin.host) + ":" + str(self.plugin.port) + "\r\n")
                sock.send("Content-Length: " + str(len(cmdstr)) + "\r\n")
                sock.send("Content-Type: text/xml; charset=\"utf-8\"\r\n")
                sock.send("SOAPACTION:\"urn:udi-com:device:X_Insteon_Lighting_Service:1#UDIService\"\r\n\r\n")

                sock.send(cmdstr + "\r\n")

                # Get the answer
                answer = sock.recv(1024)

                # If the password was correct and you are allowed to connect
                # to the server, you'll get "accept"
                if (answer.find("HTTP/1.1 200 OK") == -1):
                    self.PrintError("Command Failed")
                    self.PrintError(answer.strip())
                    sock.close()
                    return False
                # self.plugin.TriggerEvent("Command Successful", str(self.plugin.host)+":"+str(self.plugin.port))
                sock.close()
                return True

            except:
                # if eg.debugLevel:
                eg.PrintTraceback()
                sock.close()
                return None

        def Configure(self, control="", action="", flag="", node=""):
            text = self.text
            panel = eg.ConfigPanel(self)

            controlCtrl = panel.TextCtrl(control)
            actionCtrl = panel.TextCtrl(action)
            flagCtrl = panel.TextCtrl(flag)
            nodeCtrl = panel.TextCtrl(node)
            st1 = panel.StaticText("Control:")
            st2 = panel.StaticText("Action:")
            st3 = panel.StaticText("Flag:")
            st4 = panel.StaticText("Node:")
            eg.EqualizeWidths((st1, st2, st3, st4))
            box1 = panel.BoxedGroup("Attributes", (st1, controlCtrl), (st2, actionCtrl), (st3, flagCtrl),
                                    (st4, nodeCtrl))
            panel.sizer.AddMany([
                (box1, 0, wx.EXPAND)
            ])

            while panel.Affirmed():
                panel.SetResult(
                    controlCtrl.GetValue(),
                    actionCtrl.GetValue(),
                    flagCtrl.GetValue(),
                    nodeCtrl.GetValue()
                )

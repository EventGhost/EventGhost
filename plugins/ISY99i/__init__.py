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
# $LastChangedDate: 20011-10-26 12:06:42 +0100 (Di, 04 Mrz 2008) $
# $LastChangedRevision: 348 $
# $LastChangedBy: kingtd $

import eg

eg.RegisterPlugin(
    name="ISY99i",
    guid='{0C7F0A59-672E-463B-959D-6376CCF0975D}',
    description="Receives events from an ISY-99 Insteon ethernet bridge (www.universal-devices.com)",
    kind="external",
    version="0.6." + "$LastChangedRevision: 348 $".split()[1],
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
import base64
import socket
import wx
from operator import itemgetter


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
        name = "Send Manual Command"

    class SetLogLevel:
        name = "Set Log Level"

    class GetDeviceStatus:
        name = "Get Device Status"

    class SetGroup:
        name = "Set Group"

    class SetDevice:
        name = "Set Device"


class ISYeventer(asynchat.async_chat):
    """Telnet engine class. Implements command line user interface."""

    def __init__(self, host, port, username, password, plugin):

        asynchat.async_chat.__init__(self)

        self.set_terminator("\n")

        self.data = ""
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.plugin = plugin

        # connect to ftp server
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        eg.RestartAsyncore()
        self.connect((self.host, self.port))

    def handle_connect(self):
        # connection succeeded
        subscribestr = "<s:Envelope><s:Body><u:Subscribe xmlns:u=\"urn:udi-com:service:X_Insteon_Lighting_Service:1\"><reportURL>REUSE_SOCKET</reportURL><duration>infinite</duration></u:Subscribe></s:Body></s:Envelope>"

        self.push("POST /services HTTP/1.1\r\n")
        self.push("Host: " + str(self.host) + ":" + str(self.port) + "\r\n")
        self.push("Content-Length: " + str(len(subscribestr)) + "\r\n")
        self.push("Content-Type: text/xml; charset=\"utf-8\"\r\n")
        self.push("Authorization: Basic " + base64.encodestring('%s:%s' % (self.username, self.password)))
        self.push("\r\n\r\n")
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

        if (data.find("<Event seqnum") > -1):
            epx = data.find("<Event seqnum")
            eprops = data[epx:data.find("</Event")]
            eprops = eprops[eprops.find(">") + 1:]
            # print "E:",eprops
            status = "None"
            node = "None"
            Heartbeat = "None"
            RunProg = "None"
            Program = "None"
            icmd = "None"
            econtrol = "None"
            eaction = "None"
            enode = "None"

            if (eprops.find("<control>") > -1):
                econtrol = eprops[eprops.find("<control>") + 9:eprops.find("</control>")]

            if (eprops.find("<action>") > -1):
                eaction = eprops[eprops.find("<action>") + 8:eprops.find("</action>")]

            if (eprops.find("<node>") > -1):
                enode = eprops[eprops.find("<node>") + 6:eprops.find("</node>")]

            if (eprops.find("<eventInfo>") > -1):
                eeventinfo = eprops[eprops.find("<eventInfo>") + 6:eprops.find("</eventInfo>")]
                if (eeventinfo.find("[") > -1):
                    enode = eeventinfo[eeventinfo.find("[") + 1:eeventinfo.find("]")].strip()
                    icmd = eeventinfo[eeventinfo.find("]") + 1:].strip()
                if (eeventinfo.find("<id>") > -1):
                    Program = eeventinfo[eeventinfo.find("<id>") + 4:eeventinfo.find("</id>")]

            if econtrol == "_0":
                self.plugin.TriggerEvent("Heartbeat")
            elif econtrol == "ST" or econtrol == "RR" or econtrol == "OL":
                self.plugin.TriggerEvent("Status", str(enode) + ":" + str(eaction))
                self.plugin.xlightmap[str(enode)] = str(eaction)
                for index, sublist in enumerate(self.plugin.devices):
                    if sublist[0] == str(enode):
                        sublist[2] = str(eaction)
                        color = str(hex(int(eaction)))[2:]
                        sublist[3] = color + color + color
            elif econtrol == "_1":
                if Program == "None":
                    self.plugin.TriggerEvent("Command." + str(enode) + ":" + str(icmd))
                else:
                    self.plugin.TriggerEvent("Program." + str(Program))

        # This processes pre-2.6 beta commands
        if (data.find("<e:propertyset xmlns:e=\"urn:schemas-upnp-org:event-1-0\">") > -1):
            eprops = data[data.find("<e:propertyset") + 56:data.find("</e:propertyset")]
            # print "E:",eprops
            status = "None"
            node = "None"
            Heartbeat = "None"
            RunProg = "None"
            Program = "None"
            icmd = "None"
            while (eprops.find("<e:property>") > -1):
                dpoint = eprops[eprops.find("<e:property>") + 12:eprops.find("</e:property>")]
                eprops = eprops[eprops.find("</e:property>") + 13:]
                tpoint = dpoint[dpoint.find("<") + 1:dpoint.find(">")]
                dpoint = dpoint[dpoint.find(">") + 1:dpoint.find("</" + tpoint + ">")]
                # print "Type: ",tpoint, "Data: ",dpoint
                if (tpoint == "node"):
                    node = dpoint
                elif (tpoint == "ST"):
                    status = dpoint
                # if (tpoint=="RR"):
                #	status=dpoint
                elif (tpoint == "_0"):
                    Heartbeat = "Heartbeat"
                elif (tpoint == "_1"):
                    RunProg = dpoint
                elif (tpoint == "eventInfo"):
                    if (dpoint.find("[") > -1):
                        node = dpoint[dpoint.find("[") + 1:dpoint.find("]")].strip()
                        icmd = dpoint[dpoint.find("]") + 1:].strip()
                    if (dpoint.find("<id>") > -1):
                        Program = dpoint[dpoint.find("<id>") + 4:dpoint.find("</id>")]
                else:
                    status = tpoint + ":" + dpoint
            if (node != "None" and status != "None"):
                self.plugin.TriggerEvent("Status", str(node), str(status))
                self.plugin.xlightmap[node] = status
                if not (str(node) in eg.globals.excludedinsteondevices):
                    for index, sublist in enumerate(self.plugin.devices):
                        if sublist[0] == str(node):
                            sublist[2] = str(status)
            if (Heartbeat == "Heartbeat"):
                self.plugin.TriggerEvent("Heartbeat")
            if (RunProg != "None" and Program != "None"):
                self.plugin.TriggerEvent("Program." + str(Program))
            if (icmd != "None" and icmd != "None"):
                self.plugin.TriggerEvent("Command." + str(node) + ":" + str(icmd))


class ISYEvent(eg.PluginClass):
    canMultiLoad = True
    text = Text
    devices = []
    xlightmap = {}
    xgrpmap = {}

    def __init__(self):
        self.AddAction(self.Send)
        self.AddAction(self.SetLogLevel)
        self.AddAction(self.GetDeviceStatus)
        self.AddAction(self.SetGroup)
        self.AddAction(self.SetDevice)

    def __start__(self, host="insteon", port=80, username="admin", password="admin", prefix="Insteon"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.info.eventPrefix = prefix
        try:
            authenticated = self.Authenticate(self.host, self.port, self.username, self.password, self)
        except:
            eg.PrintTraceback()

        try:
            logleveled = self.Setloglevel(self.host, self.port, self.username, self.password, self)
        except:
            eg.PrintTraceback()

        try:
            x = self.GetNodesConfig(self.host, self.port, self.username, self.password, self)
        except:
            eg.PrintTraceback()

        if authenticated:
            try:
                self.eventer = ISYeventer(self.host, self.port, self.username, self.password, self)
            except socket.error, exc:
                raise self.Exception(exc[1])

    def __stop__(self):
        if hasattr(self, 'eventer') and self.eventer:
            self.eventer.close()
        self.eventer = None

    def Authenticate(self, host, port, username, password, plugin):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket = sock
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(12.0)

        self.host = host
        self.port = port
        self.username = username
        self.password = password

        connected = False
        try:
            sock.connect((self.host, self.port))
            connected = True
            sock.settimeout(10.0)

            authstr = "<s:Envelope><s:Body><u:Authenticate xmlns:u=\"urn:udi-com:service:X_Insteon_Lighting_Service:1\"><name>" + self.username + "</name><id>" + self.password + "</id></u:Authenticate></s:Body></s:Envelope>"

            sock.send("POST /services HTTP/1.1\r\n")
            sock.send("Host: " + str(self.host) + ":" + str(self.port) + "\r\n")
            sock.send("Content-Length: " + str(len(authstr)) + "\r\n")
            sock.send("Content-Type: text/xml; charset=\"utf-8\"\r\n")
            sock.send("Authorization: Basic " + base64.encodestring('%s:%s' % (self.username, self.password)))
            sock.send("SOAPACTION:\"urn:udi-com:service:X_Insteon_Lighting_Service:1#Authenticate\"\r\n\r\n")

            sock.send(authstr + "\r\n")
            # Get the answer
            answer = sock.recv(1024)

            # If the password was correct and you are allowed to connect
            # to the server, you'll get "accept"
            # print "Authenticate response: "+answer
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

    def Setloglevel(self, host, port, username, password, plugin):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket = sock
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(12.0)

        self.host = host
        self.port = port
        self.username = username
        self.password = password

        connected = False
        try:
            sock.connect((self.host, self.port))
            connected = True
            sock.settimeout(10.0)

            authstr = "<s:Envelope><s:Body><u:SetDebugLevel xmlns:u=\"urn:udi-com:service:X_Insteon_Lighting_service:1\"><option>1</option></u:SetDebugLevel></s:Body></s:Envelope>"

            sock.send("POST /services HTTP/1.1\r\n")
            sock.send("Host: " + str(self.host) + ":" + str(self.port) + "\r\n")
            sock.send("Content-Length: " + str(len(authstr)) + "\r\n")
            sock.send("Content-Type: text/xml; charset=\"utf-8\"\r\n")
            sock.send("Authorization: Basic " + base64.encodestring('%s:%s' % (self.username, self.password)))
            sock.send("SOAPACTION:\"urn:udi-com:service:X_Insteon_Lighting_Service:1#SetDebugLevel\"\r\n\r\n")

            sock.send(authstr + "\r\n")

            # Get the answer
            answer = sock.recv(1024)
            # print "Set Log Level response: "+answer
            if (answer.find("HTTP/1.1 200 OK") == -1):
                self.PrintError("Could not set log level")
                self.PrintError(answer.strip())
                sock.close()
                return False
            self.TriggerEvent("Set Log Level to 1", str(self.host) + ":" + str(self.port))
            sock.close()
            return True

        except:
            # if eg.debugLevel:
            eg.PrintTraceback()
            sock.close()
            return None

    def GetNodesConfig(self, host, port, username, password, plugin):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket = sock
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(12.0)

        connected = False
        try:
            self.xdevmap = {}
            sock.connect((self.host, self.port))
            connected = True
            sock.settimeout(10.0)
            authstr = "<s:Envelope><s:Body><u:GetNodesConfig xmlns:u=\"urn:udi-com:service:X_Insteon_Lighting_service:1\"><option/></u:GetNodesConfig></s:Body></s:Envelope>"

            sock.send("POST /services HTTP/1.1\r\n")
            sock.send("Host: " + str(self.host) + ":" + str(self.port) + "\r\n")
            sock.send("Content-Length: " + str(len(authstr)) + "\r\n")
            sock.send("Content-Type: text/xml; charset=\"utf-8\"\r\n")
            sock.send("Authorization: Basic " + base64.encodestring('%s:%s' % (self.username, self.password)))
            sock.send("SOAPACTION:\"urn:udi-com:service:X_Insteon_Lighting_Service:1#GetNodesConfig\"\r\n\r\n")

            sock.send(authstr + "\r\n")

            # Get the answer
            answer = sock.recv(1024)

            # If the password was correct and you are allowed to connect
            # to the server, you'll get "accept"
            if (answer.find("HTTP/1.1 200 OK") == -1):
                self.PrintError("Could not GetNodesConfig")
                self.PrintError(answer.strip())
                sock.close()
                return False
            xcl = answer[answer.find("Content-Length: "):answer.find("Content-Length: ") + 30]
            xcl = xcl[xcl.find("Content-Length: ") + 16:xcl.find("\r")]
            # eg.TriggerEvent("GetNodesConfig", str(self.host)+":"+str(self.port))
            answer = ""
            while len(answer) < int(xcl):
                answer += sock.recv(8192)
            answer = answer[answer.find("<nodes>") + 7:]

            while (answer.find("</node>") > -1):
                x = answer.find("<node")
                y = answer.find("</node>")
                xnode = answer[x:y]
                if (xnode.find("128") > -1):
                    xnode = xnode[xnode.find(">") + 1:]
                    xadd = xnode[xnode.find("<address>") + 9:xnode.find("</address>")]
                    xname = xnode[xnode.find("<name>") + 6:xnode.find("</name>")]
                    # eg.globals.insteondevices[xadd]=xname
                    self.xdevmap[xadd] = xname
                # if (xadd not in eg.globals.excludedinsteondevices):
                # self.devices.append([xadd,xname,"Unknown","777777"])
                answer = answer[y + 7:]
            self.devices = sorted(self.devices, key=itemgetter(1))

            while (answer.find("</group>") > -1):
                x = answer.find("<group")
                y = answer.find("</group>")
                xnode = answer[x:y]
                xnode = xnode[xnode.find(">") + 1:]
                xadd = xnode[xnode.find("<address>") + 9:xnode.find("</address>")]
                xname = xnode[xnode.find("<name>") + 6:xnode.find("</name>")]
                # eg.globals.insteondevices[xadd]=xname
                eg.plugins.ISYEvent.plugin.xgrpmap[xadd] = xname
                answer = answer[y + 8:]
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

    class SetDevice(eg.ActionWithStringParameter):
        description = ("Sets the status of an Insteon Device.")

        class Text:
            control = "Control:"
            action = "Action:"
            node = "Node:"

        def __call__(self, control, action, flag, node):
            self.SetDevice(control, action, flag, node)
            return True

        def SetDevice(self, control, action, flag, node):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.socket = sock
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(12.0)

            connected = False
            try:
                sock.connect((self.plugin.host, self.plugin.port))
                connected = True
                sock.settimeout(10.0)
                node = eg.ParseString(node)
                cmdstr = "<s:Envelope><s:Body><u:UDIService xmlns:u='urn:udi-com:service:X_Insteon_Lighting_Service:1'><control>" + control + "</control><action>" + action + "</action><flag>" + flag + "</flag><node>" + node + "</node></u:UDIService></s:Body></s:Envelope>"
                sock.send("POST /services HTTP/1.1\r\n")
                sock.send("Authorization: Basic " + base64.encodestring(
                    '%s:%s' % (self.plugin.username, self.plugin.password)))
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
                self.plugin.TriggerEvent("Command Successful", str(self.plugin.host) + ":" + str(self.plugin.port))
                sock.close()
                return True

            except:
                # if eg.debugLevel:
                eg.PrintTraceback()
                sock.close()
                return None

        def Configure(self, control="", action=0, flag="", node=""):
            text = self.text
            panel = eg.ConfigPanel(self)
            controlCtrl = wx.Choice(panel, -1, choices=["DON", "DOF", "DIM"])
            controlCtrl.SetStringSelection(control)
            actionCtrl = wx.Slider(panel, -1, int(action), 0, 255, (10, 10),
                                   size=(150, -1),
                                   style=wx.SL_HORIZONTAL)
            nodeCtrl = wx.Choice(panel, -1, choices=eg.plugins.ISYEvent.plugin.xdevmap.values())
            try:
                nodeCtrl.SetStringSelection(eg.plugins.ISYEvent.plugin.xdevmap[node])
            except:
                pass
            st1 = panel.StaticText("Control:")
            st2 = panel.StaticText("Action:")
            st4 = panel.StaticText("Node:")
            eg.EqualizeWidths((st1, st2, st4))
            box1 = panel.BoxedGroup("Attributes", (st1, controlCtrl), (st2, actionCtrl), (st4, nodeCtrl))
            panel.sizer.AddMany([
                (box1, 0, wx.EXPAND)
            ])

            while panel.Affirmed():
                xnode = nodeCtrl.GetSelection()
                try:
                    node = eg.plugins.ISYEvent.plugin.xdevmap.keys()[xnode]
                except IndexError:
                    node = ''
                panel.SetResult(
                    controlCtrl.GetStringSelection(),
                    str(actionCtrl.GetValue()),
                    "65531",
                    node
                )

    class SetGroup(eg.ActionWithStringParameter):
        description = ("Sets the status for a group of devices")

        class Text:
            control = "Control:"
            action = "Action:"
            flag = "Flag:"
            node = "Node:"

        def __call__(self, control, action, flag, node):
            self.SetGroup(control, action, flag, node)
            return True

        def SetGroup(self, control, action, flag, node):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.socket = sock
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(12.0)

            connected = False
            try:
                sock.connect((self.plugin.host, self.plugin.port))
                connected = True
                sock.settimeout(10.0)
                node = eg.ParseString(node)
                cmdstr = "<s:Envelope><s:Body><u:UDIService xmlns:u='urn:udi-com:service:X_Insteon_Lighting_Service:1'><control>" + control + "</control><action>" + action + "</action><flag>" + flag + "</flag><node>" + node + "</node></u:UDIService></s:Body></s:Envelope>"
                sock.send("POST /services HTTP/1.1\r\n")
                sock.send("Authorization: Basic " + base64.encodestring(
                    '%s:%s' % (self.plugin.username, self.plugin.password)))
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
                self.plugin.TriggerEvent("Command Successful", str(self.plugin.host) + ":" + str(self.plugin.port))
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
            controlCtrl = wx.Choice(panel, -1, choices=["DON", "DOF", "DFON", "DFOF", "DIM"])
            controlCtrl.SetStringSelection(control)
            actionCtrl = panel.TextCtrl(action)
            nodeCtrl = wx.Choice(panel, -1, choices=eg.plugins.ISYEvent.plugin.xgrpmap.values())
            try:
                nodeCtrl.SetStringSelection(eg.plugins.ISYEvent.plugin.xgrpmap[node])
            except:
                pass
            st1 = panel.StaticText("Control:")
            st4 = panel.StaticText("Group:")
            eg.EqualizeWidths((st1, st4))
            box1 = panel.BoxedGroup("Attributes", (st1, controlCtrl), (st4, nodeCtrl))
            panel.sizer.AddMany([
                (box1, 0, wx.EXPAND)
            ])

            while panel.Affirmed():
                xnode = nodeCtrl.GetSelection()
                try:
                    node = eg.plugins.ISYEvent.plugin.xgrpmap.keys()[xnode]
                except IndexError:
                    node = ''
                panel.SetResult(
                    controlCtrl.GetStringSelection(),
                    "",
                    "4",
                    node
                )

    class Send(eg.ActionWithStringParameter):
        description = ("Sends a manual command through the ISY-99.")

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
                node = eg.ParseString(node)
                print node
                cmdstr = "<s:Envelope><s:Body><u:UDIService xmlns:u='urn:udi-com:service:X_Insteon_Lighting_Service:1'><control>" + control + "</control><action>" + action + "</action><flag>" + flag + "</flag><node>" + node + "</node></u:UDIService></s:Body></s:Envelope>"
                print cmdstr
                sock.send("POST /services HTTP/1.1\r\n")
                sock.send("Authorization: Basic " + base64.encodestring(
                    '%s:%s' % (self.plugin.username, self.plugin.password)))
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
                self.plugin.TriggerEvent("Command Successful", str(self.plugin.host) + ":" + str(self.plugin.port))
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

    class SetLogLevel(eg.ActionWithStringParameter):
        description = ("Sets the log level of the ISY-26.")

        class Text:
            level = "Level: "

        def __call__(self, level):
            self.SetLogLevelCommand(level)
            return True

        def SetLogLevelCommand(self, level):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.socket = sock
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(12.0)

            connected = False
            try:
                sock.connect((self.plugin.host, self.plugin.port))
                connected = True
                sock.settimeout(10.0)

                authstr = "<s:Envelope><s:Body><u:SetDebugLevel xmlns:u=\"urn:udi-com:service:X_Insteon_Lighting_service:1\"><option>" + str(
                    level) + "</option></u:SetDebugLevel></s:Body></s:Envelope>"

                sock.send("POST /services HTTP/1.1\r\n")
                sock.send("Host: " + str(self.plugin.host) + ":" + str(self.plugin.port) + "\r\n")
                sock.send("Content-Length: " + str(len(authstr)) + "\r\n")
                sock.send("Content-Type: text/xml; charset=\"utf-8\"\r\n")
                sock.send("Authorization: Basic " + base64.encodestring(
                    '%s:%s' % (self.plugin.username, self.plugin.password)))
                sock.send("SOAPACTION:\"urn:udi-com:service:X_Insteon_Lighting_Service:1#SetDebugLevel\"\r\n\r\n")

                sock.send(authstr + "\r\n")

                # Get the answer
                answer = sock.recv(1024)
                # print "Set Log Level response: "+answer
                if (answer.find("HTTP/1.1 200 OK") == -1):
                    self.PrintError("Could not set log level")
                    self.PrintError(answer.strip())
                    sock.close()
                    return False
                self.plugin.TriggerEvent("Set Log Level to " + level,
                                         str(self.plugin.host) + ":" + str(self.plugin.port))
                sock.close()
                return True

            except:
                # if eg.debugLevel:
                eg.PrintTraceback()
                sock.close()
                return None

        def Configure(self, level="0"):
            text = self.text
            panel = eg.ConfigPanel(self)

            LevelCtrl = panel.TextCtrl(level)
            st1 = panel.StaticText("Level:")
            box1 = panel.BoxedGroup("Attributes", (st1, LevelCtrl))
            panel.sizer.AddMany([
                (box1, 0, wx.EXPAND)
            ])

            while panel.Affirmed():
                panel.SetResult(
                    LevelCtrl.GetValue()
                )

    class GetDeviceStatus(eg.ActionWithStringParameter):
        description = ("Asks all modules to report status.")

        class Text:
            modulerange = "Range: "

        def __call__(self, modulerange):
            self.GetNodesConfig(modulerange)
            return True

        def GetNodesConfig(self, modulerange):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # self.socket = sock
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(12.0)

            connected = False
            try:
                eg.plugins.ISYEvent.plugin.xdevmap = {}
                sock.connect((self.plugin.host, self.plugin.port))
                connected = True
                sock.settimeout(10.0)
                authstr = "<s:Envelope><s:Body><u:GetNodesConfig xmlns:u=\"urn:udi-com:service:X_Insteon_Lighting_service:1\"><option/></u:GetNodesConfig></s:Body></s:Envelope>"

                sock.send("POST /services HTTP/1.1\r\n")
                sock.send("Host: " + str(self.plugin.host) + ":" + str(self.plugin.port) + "\r\n")
                sock.send("Content-Length: " + str(len(authstr)) + "\r\n")
                sock.send("Content-Type: text/xml; charset=\"utf-8\"\r\n")
                sock.send("Authorization: Basic " + base64.encodestring(
                    '%s:%s' % (self.plugin.username, self.plugin.password)))
                sock.send("SOAPACTION:\"urn:udi-com:service:X_Insteon_Lighting_Service:1#GetNodesConfig\"\r\n\r\n")

                sock.send(authstr + "\r\n")

                # Get the answer
                answer = sock.recv(1024)

                if (answer.find("HTTP/1.1 200 OK") == -1):
                    self.PrintError("Could not GetNodesConfig")
                    self.PrintError(answer.strip())
                    sock.close()
                    return False
                xcl = answer[answer.find("Content-Length: "):answer.find("Content-Length: ") + 30]
                xcl = xcl[xcl.find("Content-Length: ") + 16:xcl.find("\r")]
                # eg.TriggerEvent("GetNodesConfig", str(self.plugin.host)+":"+str(self.plugin.port))
                answer = ""
                while len(answer) < int(xcl):
                    answer += sock.recv(8192)
                answer = answer[answer.find("<nodes>") + 7:]
                while (answer.find("</node>") > -1):
                    x = answer.find("<node")
                    y = answer.find("</node>")
                    xnode = answer[x:y]
                    xnode = xnode[xnode.find(">") + 1:]
                    xadd = xnode[xnode.find("<address>") + 9:xnode.find("</address>")]
                    xname = xnode[xnode.find("<name>") + 6:xnode.find("</name>")]
                    # eg.globals.insteondevices[xadd]=xname
                    eg.plugins.ISYEvent.plugin.xdevmap[xadd] = xname
                    answer = answer[y + 7:]
                print answer
                while (answer.find("</group>") > -1):
                    x = answer.find("<group>")
                    y = answer.find("</group>")
                    xnode = answer[x:y]
                    xnode = xnode[xnode.find(">") + 1:]
                    xadd = xnode[xnode.find("<address>") + 9:xnode.find("</address>")]
                    xname = xnode[xnode.find("<name>") + 6:xnode.find("</name>")]
                    # eg.globals.insteondevices[xadd]=xname
                    eg.plugins.ISYEvent.plugin.xgrpmap[xadd] = xname
                    answer = answer[y + 7:]
                sock.close()
                print eg.plugins.ISYEvent.plugin.xdevmap
                return True

            except:
                # if eg.debugLevel:
                eg.PrintTraceback()
                sock.close()
                return None

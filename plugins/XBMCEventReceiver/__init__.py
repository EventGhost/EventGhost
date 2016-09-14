# -*- coding: utf-8 -*-
#
# plugins/XBMCEventReceiver/__init__.py
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.
#
# This plugin is based on the Broadcaster plugin that was originally provided
# by the good work from Kingtd.  I have used it as a basis for true 2-way control
# too and from XBMC.  The following improvements have been made to v2.0:
#
#	- Enabled additional fields for configuration of HTTP.API destination in setup
#	- Enabled the invoking of XBMC Host Broadcast function with in the script
#	  (so it is not necessary to do it manually)
#	- Cleaned up some of the code.
#	- Fixed error when trying to reconfigure plugin
#
# Future enhancements to make for future ver. as time permits such as:
#
#  - Extending response functionality as it applies to XBMC (once it is implemented @ the XBMC Host).
#  - Additional parsing of input from XBMC host
#
#  If you have any additional comments or suggestions feel free to contact me at vortexrotor@vortexbb.com

import eg

eg.RegisterPlugin(
    name = "XBMC Event Receiver",
    author = "vortexrotor",
    version = "2.0.5",
    kind = "program",
    guid = "{9872BD49-2022-4F1B-B362-85F1ED203B7E}",
    description = (
        "Receives events from XBMC Host UDP Broadcasts."
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?f=10&t=2140",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsRAAALEQF/ZF+RAAAA"
        "BGdBTUEAALGeYUxB9wAAACBjSFJNAAB6fAAAfosAAPoBAACHPAAAbUoAAPFDAAA2IAAAHlNX4WK7"
        "AAACYElEQVR42tTTPW8ScQDH8d/9n44HESgFKQjFWku1rUYdTEAT0sGHSU10cHZz0piYjqYxbia6"
        "+hB3Y0w3kzq0scaojdZqYiMp1dQWAlLg4A7ugbvzRXTy8wK+21dyXRe7QbBLuw6wG3ceJnJnLuTL"
        "279DrutySBIhEnUopSbjtMsYVzkXLSFEU5Y9dY/XW5Nlr207DpRWE+zzp6VHxWLpstpWKaEA5RT9"
        "XgCcC/jDDihjOpWI6vF4WkLweigULgdD4R/p4ZH30X1Dr6XhbK4i/OH43qSKVikJLhhGz26AEo61"
        "+Qz0roWR8RDWixtIJKP4/mUVA5EgkvvjOHEy/1FKj+XnwpHMxdipIhJH29C2o0hMVmH1KJQyxWTw"
        "FuKhKYCbaDUVOI4LwzKxOD8PAvkrMazOW1uSUH43ilCqgUYphvJyBitzKUyfLiCVBe7PPkVzp4l7"
        "dx9g+lwB5T9bePPqJTIjB4v0uqmVi4cHbx67UkFteRjRAx30mgEcym9iZz2NpRcyfAM6Om0Nruui"
        "sr2F8SNZuIQjEhl6Lj0LAY8Hcwtq6nwhStuQJB8sWOh3fTClBgIDOhj1wDAtcEFRq/5FW+shPRRF"
        "diyTYJNe4Kr1bfaJHiv0qAtBKTgX4D6CAJXAbQIhaYhyG16iIxvpwEfW0BITM75YrsJm3Ah6SnfB"
        "kCtzWmLikmabYLYAIRxO34Zp6nAs9VdX6xSVRn2lb7QWe2b3w9RxplwLy2AL8AOMIa5s3vb6gzUm"
        "+5mh1XXL0Lq2pVRVQ2z66J6fpLdaMqu6KjwUXo8XnFH0+w6k/3+mfwMAzwT87LI0qNEAAAAASUVO"
        "RK5CYII="
    ),
)

import wx
import os
import asyncore
import socket
import urllib

class Text:
    eventPrefix = "Event prefix:"
    xbmcip = "XBMC Host IP:"
    xbmchttpport = "XBMC HTTP Port:"
    zone = "XBMC Broadcast IP:"
    port = "UDP port:"
    selfXbmceventbroadcast = "Respond to Self Broadcast"
    delim = "Payload Delimiter"

class Xbmceventbroadcast:
    name="Xbmceventbroadcast"

class Server(asyncore.dispatcher):

    def __init__(self, port, selfXbmceventbroadcast,payDelim, plugin):
        self.selfXbmceventbroadcast=selfXbmceventbroadcast
        self.plugin=plugin
        self.port=port
        self.payDelim=payDelim
        asyncore.dispatcher.__init__(self)
        self.ipadd = socket.gethostbyname(socket.gethostname())
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        eg.RestartAsyncore()
        self.bind(('', port))


    def handle_connect(self):
        print "XBMC Event Broadcast listener ENABLED on Local Host @ " + self.ipadd + ":" + str(self.port) + ". Response to XBMC is " + str(self.selfXbmceventbroadcast) + "."
        pass

    def handle_read(self):
        data, addr = self.recvfrom(1024)

        if (self.ipadd != addr[0]) or self.selfXbmceventbroadcast:
            data = unicode(data, 'UTF8')
            #print data
            bits = data.split(str(self.payDelim))
            commandSize=len(bits)
            if commandSize==1:
                self.plugin.TriggerEvent(bits[0])
            if commandSize==2:
                self.plugin.TriggerEvent(bits[0],bits[1])
            if commandSize>2:
                self.plugin.TriggerEvent(bits[0],bits[1:])
    def writable(self):
        return False  # we don't have anything to send !

class XbmceventbroadcastListener(eg.PluginClass):
    canMultiLoad = True
    text = Text

    def __init__(self):
        self.AddAction(self.Xbmceventbroadcast)

    def __start__(self, prefix=None, xbmcip="None", xbmchttpport=8080, zone="255.255.255.255", port=8279, selfXbmceventbroadcast=False, payDelim="&&"):
        self.info.eventPrefix = prefix
        self.xbmcip = xbmcip
        self.xbmchttpport = xbmchttpport
        self.port = port
        self.payDelim=payDelim
        self.zone = zone
        self.selfXbmceventbroadcast=selfXbmceventbroadcast

        try:
            self.server = Server(self.port, self.selfXbmceventbroadcast, self.payDelim, self)
        except socket.error, exc:
            raise self.Exception(exc[1])


    def __stop__(self):
        if self.server:
            self.server.close()
        self.server = None

    def Configure(self, prefix="XBMC-Event", xbmcip="192.168.1.1", xbmchttpport=8080, zone="224.0.0.2", port=8278, selfXbmceventbroadcast=False, payDelim="<b></b>"):
        panel = eg.ConfigPanel(self)

        editCtrl = panel.TextCtrl(prefix)
        xbmcipCtrl = panel.TextCtrl(xbmcip)
        xbmchttpportCtrl = panel.SpinIntCtrl(xbmchttpport, min=1, max=65535)
        zoneCtrl = panel.TextCtrl(zone)
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        selfXbmceventbroadcastCtrl=panel.CheckBox(selfXbmceventbroadcast)
        payDelimCtrl = panel.TextCtrl(payDelim)

        panel.AddLine(self.text.eventPrefix, editCtrl)
        panel.AddLine(self.text.xbmcip, xbmcipCtrl)
        panel.AddLine(self.text.xbmchttpport, xbmchttpportCtrl)
        panel.AddLine(self.text.zone, zoneCtrl)
        panel.AddLine(self.text.port, portCtrl)

        panel.AddLine(self.text.selfXbmceventbroadcast,selfXbmceventbroadcastCtrl)
        panel.AddLine("Payload Delimiter", payDelimCtrl)

        while panel.Affirmed():
            panel.SetResult(editCtrl.GetValue(),xbmcipCtrl.GetValue(),int(xbmchttpportCtrl.GetValue()),zoneCtrl.GetValue(),int(portCtrl.GetValue()),selfXbmceventbroadcastCtrl.GetValue(), payDelimCtrl.GetValue() )
            v_header = urllib.quote("This is the Header")

            v_message = urllib.quote("This is the Message")

        host_xbmc = xbmcipCtrl.GetValue()
        port_xbmc = int(xbmchttpportCtrl.GetValue())
        udp_xbmc = int(portCtrl.GetValue())
        url_xbmc = "http://" + str(host_xbmc) + ":" + str(port_xbmc) + "/xbmcCmds/xbmcHttp?command=SetBroadcast&parameter=2;" + str(udp_xbmc) + "(Notification(" + v_header + "," + v_message + "))"
        print "str(url_xbmc)"
        try:
            urllib.urlopen(url_xbmc)
        except IOError:
            print 'Connection error'



    class Xbmceventbroadcast(eg.ActionWithStringParameter):

        def __call__(self, mesg, payload=""):
            res = self.bcastSend(mesg, payload)
            return res

        def bcastSend(self, eventString, payload=""):
            addr = (self.plugin.zone, self.plugin.port)
            UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create socket
            UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            if (payload==None):
                UDPSock.sendto(eg.ParseString(eventString),addr)
            else:
                UDPSock.sendto(eg.ParseString(eventString)+self.plugin.payDelim+eg.ParseString(payload),addr)
            UDPSock.close()

    def Configure(self, command="", payload=""):
        text = self.text
        panel = eg.ConfigPanel(self)

        commandCtrl = panel.TextCtrl(command)
        payloadCtrl = panel.TextCtrl(payload)

        commandlabel = panel.StaticText("Command:")
        payloadlabel = panel.StaticText("Payload:")
        panel.sizer.Add(commandlabel,0,wx.EXPAND)
        panel.sizer.Add(commandCtrl,0,wx.EXPAND)
        panel.sizer.Add((20, 20))
        panel.sizer.Add(payloadlabel,0,wx.EXPAND)
        panel.sizer.Add(payloadCtrl,0,wx.EXPAND)


        while panel.Affirmed():
            panel.SetResult(
                commandCtrl.GetValue(),
                payloadCtrl.GetValue()
            )

# -*- coding: utf-8 -*-
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

import eg

eg.RegisterPlugin(
    name = "Network Event Receiver",
    description = "Receives events from Network Event Sender plugins.",
    version = "1.0",
    author = "Bitmonster",
    guid = "{8F35AE6D-AF12-4A94-AA91-4B63F0CBBE1C}",
    canMultiLoad = True,
    icon = (
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
    url = "http://www.eventghost.org/forum/viewtopic.php?f=4&t=959",
)

import wx
import asynchat
import asyncore
from hashlib import md5
import random
import socket


class Text:
    port = "TCP/IP Port:"
    password = "Password:"
    eventPrefix = "Event Prefix:"
    tcpBox = "TCP/IP Settings"
    securityBox = "Security"
    eventGenerationBox = "Event generation"


DEBUG = False
if DEBUG:
    log = eg.Print
else:
    def log(dummyMesg):
        pass


class ServerHandler(asynchat.async_chat):
    """Telnet engine class. Implements command line user interface."""

    def __init__(self, sock, addr, password, plugin, server):
        log("Server Handler inited")
        self.plugin = plugin

        # Call constructor of the parent class
        asynchat.async_chat.__init__(self, sock)

        # Set up input line terminator
        self.set_terminator('\n')

        # Initialize input data buffer
        self.data = ''
        self.state = self.state1
        self.ip = addr[0]
        self.payload = [self.ip]
        #self.cookie = hex(random.randrange(65536))
        #self.cookie = self.cookie[len(self.cookie) - 4:]
        self.cookie = format(random.randrange(65536), '04x')
        self.hex_md5 = md5(self.cookie + ":" + password).hexdigest().upper()


    def handle_close(self):
        self.plugin.EndLastEvent()
        asynchat.async_chat.handle_close(self)


    def collect_incoming_data(self, data):
        """Put data read from socket to a buffer
        """
        # Collect data in input buffer
        log("<<" + repr(data))
        self.data = self.data + data


    if DEBUG:
        def push(self, data):
            log(">>", repr(data))
            asynchat.async_chat.push(self, data)


    def found_terminator(self):
        """
        This method is called by asynchronous engine when it finds
        command terminator in the input stream
        """
        # Take the complete line
        line = self.data

        # Reset input buffer
        self.data = ''

        #call state handler
        self.state(line)


    def initiate_close(self):
        if self.writable():
            self.push("close\n")
        #asynchat.async_chat.handle_close(self)
        self.plugin.EndLastEvent()
        self.state = self.state1


    def state1(self, line):
        """
        get keyword "quintessence\n" and send cookie
        """
        if line == "quintessence":
            self.state = self.state2
            self.push(self.cookie + "\n")
        else:
            self.initiate_close()


    def state2(self, line):
        """get md5 digest
        """
        line = line.strip()[-32:]
        if line == "":
            pass
        elif line.upper() == self.hex_md5:
            self.push("accept\n")
            self.state = self.state3
        else:
            eg.PrintError("NetworkReceiver md5 error")
            self.initiate_close()


    def state3(self, line):
        line = line.decode(eg.systemEncoding)
        if line == "close":
            self.initiate_close()
        elif line[:8] == "payload ":
            self.payload.append(line[8:])
        else:
            if line == "ButtonReleased":
                self.plugin.EndLastEvent()
            else:
                if self.payload[-1] == "withoutRelease":
                    self.plugin.TriggerEnduringEvent(line, self.payload)
                else:
                    self.plugin.TriggerEvent(line, self.payload)
            self.payload = [self.ip]



class Server(asyncore.dispatcher):

    def __init__ (self, port, password, handler):
        self.handler = handler
        self.password = password

        # Call parent class constructor explicitly
        asyncore.dispatcher.__init__(self)

        # Create socket of requested type
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        # restart the asyncore loop, so it notices the new socket
        eg.RestartAsyncore()

        # Set it to re-use address
        #self.set_reuse_addr()

        # Bind to all interfaces of this host at specified port
        self.bind(('', port))

        # Start listening for incoming requests
        #self.listen (1024)
        self.listen(5)


    def handle_accept (self):
        """Called by asyncore engine when new connection arrives"""
        # Accept new connection
        log("handle_accept")
        (sock, addr) = self.accept()
        ServerHandler(
            sock,
            addr,
            self.password,
            self.handler,
            self
        )



class NetworkReceiver(eg.PluginBase):
    text = Text

    def __init__(self):
        self.AddEvents()

    def __start__(self, port, password, prefix):
        self.port = port
        self.password = password
        self.info.eventPrefix = prefix
        try:
            self.server = Server(self.port, self.password, self)
        except socket.error, exc:
            raise self.Exception(exc[1])


    def __stop__(self):
        if self.server:
            self.server.close()
        self.server = None


    def Configure(self, port=1024, password="", prefix="TCP"):
        text = self.text
        panel = eg.ConfigPanel()
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        passwordCtrl = panel.TextCtrl(password, style=wx.TE_PASSWORD)
        eventPrefixCtrl = panel.TextCtrl(prefix)
        st1 = panel.StaticText(text.port)
        st2 = panel.StaticText(text.password)
        st3 = panel.StaticText(text.eventPrefix)
        eg.EqualizeWidths((st1, st2, st3))
        box1 = panel.BoxedGroup(text.tcpBox, (st1, portCtrl))
        box2 = panel.BoxedGroup(text.securityBox, (st2, passwordCtrl))
        box3 = panel.BoxedGroup(
            text.eventGenerationBox, (st3, eventPrefixCtrl)
        )
        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND|wx.TOP, 10),
            (box3, 0, wx.EXPAND|wx.TOP, 10),
        ])
        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
                passwordCtrl.GetValue(),
                eventPrefixCtrl.GetValue()
            )


# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright (C) 2014 Rasmus Vergo <Rasmus_vergo@hotmail.com>
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
# This plugin is a tcp server that can send and receive data.
# 
# This plugin is based on the network event receiver and sender plugins by bitmonster
#
# I made this pluck in so i was abel to communicate with an RTI XP-6 Controller
#
# There is no password or any ting.
# Strings send til get "\n" added to them.
# String recived will not generate an event befor "\n" is recived.
#
# Know Bugs : Plugin will contieue to generate commands even thure you disabel the plugin. (dont know how to stop the Asyn Calling)

import eg

eg.RegisterPlugin(
    name = "RTI Simpel TCP server",
    guid='{D2C978CE-D0F0-4FB8-A84A-4E0D4A449B5C}',
    author = "Rasmus Vergo",
    version = "0.2",
    kind = "other",
    description = "This plugin will open a simpel TCP server for comunicating with RTI two way string driver.",
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
)

import wx
import asynchat
import asyncore
import socket
import sys

class Text:
    port = "TCP/IP Port:"
    eventPrefix = "Event Prefix:"
    eventGenerationBox = "Event generation"
    tcpBox = "TCP/IP Settings"
    class Map:
        parameterDescription = "Event name to send:"
        
    
    
    
class ServerHandler(asynchat.async_chat):
#    Telnet engine class. Implements command line user interface.

    def __init__(self, sock, addr, plugin, server):
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


    def handle_close(self):
        print "cose 1"
        self.plugin.EndLastEvent()
        asynchat.async_chat.handle_close(self)

    def push(self, data):
            print ">>", repr(data)
            asynchat.async_chat.push(self, data)
    
    

    def collect_incoming_data(self, data):
        #Put data read from socket to a buffer
        # Collect data in input buffer
         self.data = self.data + data

    def found_terminator(self):
#        This method is called by asynchronous engine when it finds
#        command terminator in the input stream
        # Take the complete line
        line = self.data

        # Reset input buffer
        self.data = ''

        #call state handler
        self.state(line)


    def initiate_close(self):
        print "colse 2"
        if self.writable():
            self.push("close\n")
        asynchat.async_chat.handle_close(self)
        self.plugin.EndLastEvent()
        self.state = self.state1

    def state1(self, line):
                    self.plugin.TriggerEnduringEvent(line, self.ip)

class Server(asyncore.dispatcher):

    def __init__ (self, port, handler):
        self.handler = handler
        # Call parent class constructor explicitly
        asyncore.dispatcher.__init__(self)

        # Create socket of requested type
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        # restart the asyncore loop, so it notices the new socket
        eg.RestartAsyncore()

        # Bind to all interfaces of this host at specified port
        self.bind(('', port))
        
        # Start listening for incoming requests
        #self.listen (1024)
        self.listen(5)


    def handle_accept (self):
        #Called by asyncore engine when new connection arrives
        # Accept new connection
        (sock, addr) = self.accept()
        self.sock = sock
        self.addr = addr
        print "RTI Simpel TCP server is connected with: " + addr[0] + ":" + str(addr[1])
        ServerHandler(
            self.sock,
            self.addr,
            self.handler,
            self
        ) 
    
class RTISimpelTCPServer(eg.PluginBase):
    text = Text

    def __init__(self):
        print "RTI Simpel TCP server is inited."
        self.AddEvents()
        self.AddAction(SendString)
    
    def __start__(self, port, prefix):
        print "RTI Simpel TCP server is started"
        self.port = port              
        self.info.eventPrefix = prefix
        try:
            self.server = Server(self.port, self)
        except socket.error, exc:
            raise self.Exception(exc[1])


     
    def __stop__(self):
        print "RTI Simpel TCP server is stopped."
        if self.server:
            self.server.close()
        self.server = None
        
    def __close__(self):
        print "RTI Simpel TCP server is closed."
        if self.server:
            self.server.close()
        self.server = None
        
    def Configure(self, port=1024, prefix="RTI"):
        text = self.text
        panel = eg.ConfigPanel()
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        eventPrefixCtrl = panel.TextCtrl(prefix)
        st1 = panel.StaticText(text.port)
        st2 = panel.StaticText(text.eventPrefix)
        eg.EqualizeWidths((st1, st2))
        box1 = panel.BoxedGroup(text.tcpBox, (st1, portCtrl))
        box2 = panel.BoxedGroup(
            text.eventGenerationBox, (st2, eventPrefixCtrl)
        )
        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND|wx.TOP, 10),
        ])
        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
                eventPrefixCtrl.GetValue()
            )

    def Send(self, eventString, payload=None):
        #See if there has been a connection
        try:
            sock = self.server.sock
            try:
                # now just pipe those commands to the server
                sock.sendall(eventString.encode(eg.systemEncoding) + "\n")
                return sock

            except:
                self.PrintError("RTI Simpel TCP server: Send failed")
                return None
        except:
                self.PrintError("RTI Simpel TCP server: Send failed")
                return None

class SendString(eg.ActionWithStringParameter):

    def __call__(self, mesg):
        self.plugin.Send(eg.ParseString(mesg))

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
# $LastChangedDate: 2009-09-03 05:49:00 +0200 (Th, 03 Sept 2009) $
# $LastChangedRevision: 1084 $
# $LastChangedBy: Tim Hoeck $

import eg

eg.RegisterPlugin(
    name="Android",
    guid='{ea4ea2cc-98db-49d1-86d4-a8e36ce08a83}',
    description="This plugin acts as a Network Event Sender/Network Event Receiver all in one. The plugin is created to work with Android devices, using the app 'EventGhost for Android!' available in the Android Market.",
    version="1.0." + "$LastChangedRevision: 1084 $".split()[1],
    author="Network Sender/Receiver code by Bitmonster, mod by Tim Hoeck",
    createMacrosOnAdd=True,
    canMultiLoad=True,
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

import wx
import asynchat
import asyncore
from hashlib import md5
import random
import socket


class Text:
    host = "Android Host/IP:"
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

    def __init__(self, sock, addr, hex_md5, cookie, plugin, server):
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
        self.hex_md5 = hex_md5
        self.cookie = cookie

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

        # call state handler
        self.state(line)

    def initiate_close(self):
        if self.writable():
            self.push("close\n")
        # asynchat.async_chat.handle_close(self)
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
            eg.PrintError("Android: Invalid Password")
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

    def __init__(self, port, password, handler):
        self.handler = handler
        self.cookie = hex(random.randrange(65536))
        self.cookie = self.cookie[len(self.cookie) - 4:]
        self.hex_md5 = md5(self.cookie + ":" + password).hexdigest().upper()

        # Call parent class constructor explicitly
        asyncore.dispatcher.__init__(self)

        # Create socket of requested type
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        # restart the asyncore loop, so it notices the new socket
        eg.RestartAsyncore()

        # Set it to re-use address
        # self.set_reuse_addr()

        # Bind to all interfaces of this host at specified port
        self.bind(('', port))

        # Start listening for incoming requests
        # self.listen (1024)
        self.listen(5)

    def handle_accept(self):
        """Called by asyncore engine when new connection arrives"""
        # Accept new connection
        log("handle_accept")
        (sock, addr) = self.accept()
        ServerHandler(
            sock,
            addr,
            self.hex_md5,
            self.cookie,
            self.handler,
            self
        )


class Android(eg.PluginClass):
    text = Text

    def __init__(self):
        self.AddEvents()
        self.AddAction(Map)
        self.AddAction(SendEvents)

    def __start__(self, host, port, password, prefix):
        self.host = host
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

    def Configure(self, host="", port=1024, password="EG4Android!", prefix="Android"):
        text = self.text
        panel = eg.ConfigPanel()
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        passwordCtrl = panel.TextCtrl(password, style=wx.TE_PASSWORD)
        eventPrefixCtrl = panel.TextCtrl(prefix)
        st1 = panel.StaticText(text.host)
        st2 = panel.StaticText(text.port)
        st3 = panel.StaticText(text.password)
        st4 = panel.StaticText(text.eventPrefix)
        eg.EqualizeWidths((st1, st2, st3, st4))
        box1 = panel.BoxedGroup(
            text.tcpBox,
            (st1, hostCtrl),
            (st2, portCtrl),
        )
        box2 = panel.BoxedGroup(text.securityBox, (st3, passwordCtrl))
        box3 = panel.BoxedGroup(
            text.eventGenerationBox, (st4, eventPrefixCtrl)
        )
        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND | wx.TOP, 10),
            (box3, 0, wx.EXPAND | wx.TOP, 10),
        ])

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                passwordCtrl.GetValue(),
                eventPrefixCtrl.GetValue()
            )

    def Send(self, eventString, payload=None):
        sockout = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket = sock
        sockout.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sockout.settimeout(2.0)
        try:
            sockout.connect((self.host, self.port))
            sockout.settimeout(5.0)
            # First wake up the server, for security reasons it does not
            # respond by it self it needs this string, why this odd word ?
            # well if someone is scanning ports "connect" would be very 
            # obvious this one you'd never guess :-) 

            sockout.sendall("quintessence\n\r")

            # The server now returns a cookie, the protocol works like the
            # APOP protocol. The server gives you a cookie you add :<password>
            # calculate the md5 digest out of this and send it back
            # if the digests match you are in.
            # We do this so that no one can listen in on our password exchange
            # much safer then plain text.

            cookie = sockout.recv(128)

            # Trim all enters and whitespaces off
            cookie = cookie.strip()

            # Combine the token <cookie>:<password>
            token = cookie + ":" + self.password

            # Calculate the digest
            digest = md5(token).hexdigest()

            # add the enters
            digest = digest + "\n"

            # Send it to the server		
            sockout.sendall(digest)

            # Get the answer
            answer = sockout.recv(512)

            # If the password was correct and you are allowed to connect
            # to the server, you'll get "accept"
            if (answer.strip() != "accept"):
                sockout.close()
                return False

            # now just pipe those commands to the server
            if (payload is not None) and (len(payload) > 0):
                for pld in payload:
                    sockout.sendall(
                        "payload %s\n" % pld.encode(eg.systemEncoding)
                    )

            sockout.sendall("payload withoutRelease\n")
            sockout.sendall(eventString.encode(eg.systemEncoding) + "\n")

            return sockout

        except:
            if eg.debugLevel:
                eg.PrintTraceback()
            sockout.close()
            self.PrintError("NetworkSender failed")
            return None

    def MapUp(self, sockout):
        # tell the server that we are done nicely.
        sockout.sendall("close\n")
        sockout.close()


class Map(eg.ActionWithStringParameter):
    name = "Map"
    description = "Events associated with this action will cause the event name give to be sent to the Android client"

    def __call__(self, mesg="Map"):
        res = self.plugin.Send(eg.ParseString(mesg))
        if res:
            eg.event.AddUpFunc(self.plugin.MapUp, res)
        return res


class SendEvents(eg.ActionBase):
    name = "Send Event"
    description = "Events associated with this action will be sent to the Android client"

    def __call__(self):
        print "Sent Event: " + eg.ParseString(eg.event.string)
        res = self.plugin.Send(eg.ParseString(eg.event.string))
        if res:
            eg.event.AddUpFunc(self.plugin.MapUp, res)
        return res

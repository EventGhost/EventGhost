# EventGhost receiver for iPhone/iPod Touch native application client
# Copyright (C) 2008 Melloware <info@melloware.com>
# http://www.melloware.com/products/eventphone
#
# Description:  EventGhost iPhone client for controlling your home
#                        automation from the comfort of your iPhone or
#                        iPod Touch using EventPhone native app.
#
# Instructions: 1. Simply purchase EventPhone native app from the Apple
#                            Appstore to install it.
#                        2. Install iPhone plugin for EventGhost found on Melloware
#                             Website http://www.melloware.com
#                        3. In EventGhost configure the Port and Password in the plugin.
#                        4.  On the iPhone configure the Settings to have the same port
#                             and password, and enter the IP address of the PC running
#                             EventGhost.
#                         5. Start EventPhone on the iPhone and it will connect to your
#                              PC and you can map events to whatever you want!
#
# Based on the Network Receiver plugin but had to be modifed to work for the
# iPhone.  Thanks to BitMonster for the excellent Network Receiver Plugin.
# EventGhost
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>

import eg

eg.RegisterPlugin(
    name = "EventPhone Remote",
    description=(
        u'Plugin for the EventPhone iPhone/Ipod Touch\u2122 native application.'
        u'\n\n<p>'
        u'<center><img src="picture.jpg" /></a></center>'
    ),
    version = "1.0.1",
    kind = "remote",
    guid = "{BAD86ECC-5B21-4F47-9ADE-9CC8FFF8D191}",
    canMultiLoad = True,
    author = "Melloware Inc",
    url="http://www.melloware.com/products/eventphone",
    help = """
        <b>Instructions:</b> <p>1. Simply purchase <a href="http://www.melloware.com/products/eventphone">EventPhone Native Application</a> from the Apple Appstore to install it.
        <p>2. Install EventPhone plugin for EventGhost found on <a href="http://www.melloware.com">Melloware Website</a>
        <p>3. In EventGhost configure the Port and Password in the plugin.
        <p>4. On the iPhone configure the Settings to have the same port and password, and enter the IP address of the PC running EventGhost.
        <p>5. Start EventPhone on the iPhone and it will connect to your PC and you can map events to whatever you want!
    """,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAAA0AAAAPCAMAAAAI/bVFAAAAB3RJTUUH2AgaDAIK5pS6"
        "IAAAAAlwSFlzAAAOwgAADsIBFShKgAAAAARnQU1BAACxjwv8YQUAAAGPUExURf///7LE"
        "8XWW58PR87bH8neX6N7l+Gmc8gBA3wNL3wBH3ABB3ABA2wBG3gBK4AA73Lzb/+7F0ZAP"
        "UKImWKAkVZ8jU6EjU6MiUqEiUp8iU58hUpgRSrshVbwfTrghTbUfSrYfSbYeSrgeSbce"
        "SbgcSbYOPteIn/vPz/wODP0hG/4fGv4dGf0dGf0dGP0cF/wbFvwbFfwbE/oCAPmlpPyH"
        "iv4TFv0eHf4cHP0bGv4aGv0ZGv4ZGf0YF/4EAfu6ufyBZ/5DHf1EH/1DHf1DHP5DHP1C"
        "G/1DGf1DGv0/FvpJH/uKaP1MHvxQIPxOHvtMHfxMHPtMG/xNG/xLFvttP/3ujf/PH//Q"
        "J//PJf/OI//SH//VH//VHf/XEv/+76mjBLusIbyoH7yqH7yqHbqqG76rHb6uHb6vGr2v"
        "D7bCV6XXsAB+AAKDBgSECACBACeWKwyJDgSIBgaJCQGGARGOCPT58vz9+6TSn57Pl/j8"
        "9rbZr6HOmczmx47IhrTbrZ/QlwCCAGe0XCiVGd3t2nu/cbndsqC5CdoAAAABdFJOUwBA"
        "5thmAAAAtElEQVR42mNggILmFgYEaKxvQnDq6hugrNKy8orKquqaWhAnMys7Jzcvv6Cw"
        "qLiEITYuPiExKTklNS09g4EhJDQsPCIiIjIqOgao0Mvbx9fP3z8gMCgYyLN3cHRydnF1"
        "c/fwBPJMTM3MLSytLK1tbO0YGNQ1NLW0dXT19A0MjYwZGGRk5eQVFJWUlVRU1RgYBIWE"
        "RUTFxCUkpaRB1rNzcHJx8/Dy8QuAncbIxMzAwMLKxsAAAAExJCRS1N69AAAAAElFTkSu"
        "QmCC"
    ),
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
        get keyword "iphone\n" and send cookie
        """
        line = line.strip()
        if line == "iphone":
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
            self.push("version:" +eg.Version.string+ "\n")
            self.state = self.state3
        else:
            eg.PrintError("EventPhone Remote md5 error")
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
            self.hex_md5,
            self.cookie,
            self.handler,
            self
        )



class EventPhone(eg.PluginBase):
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


    def Configure(self, port=1025, password="", prefix="Apple"):
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


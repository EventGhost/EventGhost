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
    name = "Broadcaster",
    author = (
        "Kingtd",
        "Bitmonster",
    ),
    version = "2.2.501",
    description = (
        "Listens for and Transmits UDP Broadcasts"
    ),
    guid = "{5E8DA56B-24AC-4092-9521-169343C5171C}",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeT"
        "AAAACXBIWXMAAA3XAAAN1wFCKJt4AAAAB3RJTUUH1gEECzsZ7j1DbAAAAu1JREFUOMul"
        "kztsW3UUxn////Xb1684NXbzsOskA6UiklWCCOmCCiKwsCDBjBShThVCDICYgCIxMHgC"
        "BhYYkbJAhaIoIBCKKvUBhArHGLexaar4/bj2ffjey0CboagTZ/l0jo5+Ovp0PvifJR4c"
        "5F64NOMX7kcoyrppOwmBwOcRHTGZXBk7YuPW5bfrDwWcWv/gdSFlcWEp55mZyxCJhBGA"
        "ruvcqd+lXKpOsMxLpW/ffe8/gNz6h6/FYuFP184VlNO5E8yfTJEKu2QSQbojk51rt7nx"
        "Z4Pr124Sks7HP3918S0ACfDJlz+ueBRZfPaZJ5R3Xinw3HKKx7MRCgtTzCaDRAMKwjJo"
        "N1qcWX6Uu93xm/nn358/Bmzt7r+RX8wG4kGFdm+MGo3h93lojaCnO5RrbZpjQXYmSSrq"
        "Y2EpJ7zC/QLAA1Ctt5568lxeDHULTYaYQtLUwCOh3dX47Osr9EcG0qOgjUzyi1lq1drK"
        "MWBs2ul4LMLiXJxkSHLQNvB5PWiWzfZuid5wjGnZGMMxXr+faFTFmNihY4DANXyK9L28"
        "NkejM6J5NET4VSa2jaqGkIrEtWxsx0EfaAC47r/my3vN3mg4sAcjk0wyTLvR4vL31zls"
        "9FG8Pp5eXWZm9hEmtoMQgn5/iILbPr4AIbaq1b+Xd/ZmQ/WDO5QPWmSmIzQ6A8aWjTY2"
        "SSdVMoVTBFSVq7/XXOHY3wEoAPGl8+VWq3fBDai+W0ea2K8c0hxa5OdPoOAQUCRnl6bZ"
        "eKnASLf49ZdSM51OvvrH7mZXAeiWtweR3FrvqNF7Mb8wh5QSfzjEYVujdtRnYtuczk4x"
        "HQ3gdQwrEZxs39j6fKdSqbSU+5/Y++uHsieateuHg9VYPCpTqSSp6QSJmIqhm+z9VnJu"
        "V6o9Jv2beq++WywWf3IcZ/hgmNKh9JnVk4+d31CCyRXDljEAx9T6zrC+dzYrribCcn9z"
        "c/ObTqdzALjiIQmNArF76gcMYAB0gT7g3l/+ByWIP9hU8ktfAAAAAElFTkSuQmCC"
    ),
)

import wx
import os
import asyncore
import socket


class Server(asyncore.dispatcher):

    def __init__(self, port, listenAddr, selfBroadcast, payDelim, plugin):
        self.selfBroadcast=selfBroadcast
        self.plugin=plugin
        self.addresses = socket.gethostbyname_ex(socket.gethostname())[2]
        self.addresses.sort(key=lambda a: [int(b) for b in a.split('.', 4)])
        self.port=port
        self.payDelim=payDelim

        if listenAddr in self.addresses:
            self.listenAddr = listenAddr
        else:
            addrs = socket.gethostbyname_ex(socket.gethostname())[2]
            self.listenAddr = addrs[0]

        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        eg.RestartAsyncore()
        self.set_reuse_addr()
        self.bind((self.listenAddr, self.port))

    def handle_connect(self):
        print "%s %s:%s. %s %s."  % (self.plugin.text.message_1, self.listenAddr, str(self.port), self.plugin.text.message_2, str(self.selfBroadcast))
        pass

    def handle_read(self):
        data, addr = self.socket.recvfrom(1024)

        # Check if the sending address is any of our interfaces
        my_addr = addr[0] in self.addresses

        if (not my_addr) or self.selfBroadcast:
            data = data.decode(eg.systemEncoding)

            bits = data.split(self.payDelim);

            commandSize=len(bits)
            if commandSize==1:
                self.plugin.TriggerEvent(bits[0])
            if commandSize==2:
                self.plugin.TriggerEvent(bits[0],bits[1])
            if commandSize>2:
                self.plugin.TriggerEvent(bits[0],bits[1:])

    def writable(self):
        return False  # we don't have anything to send !


class BroadcastListener(eg.PluginBase):

    class Text:
        eventPrefix = "Event prefix:"
        zone = "Broadcast zone:"
        port = "UDP port:"
        listenAddr = "Listening address:"
        selfBroadcast = "Respond to self broadcast"
        delim = "Payload delimiter"
        message_1 = "Broadcast listener on"
        message_2 = "Self broadcast is"

    text = Text
    canMultiLoad = True

    def __init__(self):
        self.AddAction(Broadcast)

    def __start__(self, prefix=None, zone="255.255.255.255", port=33333, selfBroadcast=False, payDelim="&&", listenAddr=""):
        self.info.eventPrefix = prefix
        self.port = port
        self.payDelim=payDelim
        self.zone = zone
        self.listenAddr = listenAddr
        self.selfBroadcast=selfBroadcast

        try:
            self.server = Server(self.port, self.listenAddr, self.selfBroadcast, self.payDelim, self)
        except socket.error, exc:
            raise self.Exception(exc[1].decode(eg.systemEncoding))

    def __stop__(self):
        if self.server:
            self.server.close()
        self.server = None

    def Configure(self, prefix="Broadcast", zone="255.255.255.255", port=33333, selfBroadcast=False, payDelim="&&", listenAddr=""):
        text = self.text
        panel = eg.ConfigPanel(self)

        addrs = socket.gethostbyname_ex(socket.gethostname())[2]
        addrs.sort(key=lambda a: [int(b) for b in a.split('.', 4)])

        try:
            addr = addrs.index(listenAddr)
        except ValueError:
            addr = 0

        editCtrl = panel.TextCtrl(prefix)
        zoneCtrl = panel.TextCtrl(zone)
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        listenAddrCtrl = panel.Choice(addr, addrs)
        selfBroadcastCtrl=panel.CheckBox(selfBroadcast)
        payDelimCtrl = panel.TextCtrl(payDelim)

        panel.AddLine(text.eventPrefix, editCtrl)
        panel.AddLine(text.zone, zoneCtrl)
        panel.AddLine(text.port, portCtrl)

        panel.AddLine(text.listenAddr, listenAddrCtrl)
        panel.AddLine(text.selfBroadcast,selfBroadcastCtrl)
        panel.AddLine(text.delim, payDelimCtrl)

        while panel.Affirmed():
            panel.SetResult(
                editCtrl.GetValue(),
                zoneCtrl.GetValue(),
                int(portCtrl.GetValue()),
                selfBroadcastCtrl.GetValue(),
                payDelimCtrl.GetValue(),
                addrs[listenAddrCtrl.GetValue()]
            )


class Broadcast(eg.ActionWithStringParameter):

    class Text:
        sendport = "UDP port: (0 = default)"
        command = "Command:"
        payload="Payload:"

    text = Text

    def __call__(self, mesg, payload="",port=0):
        res = self.bcastSend(mesg, payload,port)
        return res

    def bcastSend(self, eventString, payload="", port=0):
        if (port==None):
            sendToPort=self.plugin.port
        else:
            sendToPort=int(port)

        addr = (self.plugin.zone, sendToPort)
        UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create socket
        UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        if (payload==None):
            UDPSock.sendto(eg.ParseString(eventString).encode(eg.systemEncoding),addr)
        else:
            bits = payload.split(self.plugin.payDelim);
            bits = [eg.ParseString(bit) for bit in bits];

            payload = self.plugin.payDelim.join(bits).encode(eg.systemEncoding);

            UDPSock.sendto(eg.ParseString(eventString).encode(eg.systemEncoding) + self.plugin.payDelim.encode(eg.systemEncoding) + payload,addr)
        UDPSock.close()


    def Configure(self, command="", payload="", port=""):
        text = self.text
        panel = eg.ConfigPanel(self)

        commandCtrl = panel.TextCtrl(command)
        payloadCtrl = panel.TextCtrl(payload)
        portCtrl = panel.SpinIntCtrl(port, min=0, max=65535)
        commandlabel = panel.StaticText(text.command)
        payloadlabel = panel.StaticText(text.payload)
        portlabel =panel.StaticText(text.sendport)
        panel.sizer.Add(commandlabel,0,wx.EXPAND)
        panel.sizer.Add(commandCtrl,0,wx.EXPAND)
        panel.sizer.Add((20, 20))
        panel.sizer.Add(payloadlabel,0,wx.EXPAND)
        panel.sizer.Add(payloadCtrl,0,wx.EXPAND)
        panel.sizer.Add((20, 20))
        panel.sizer.Add(portlabel,0)
        panel.sizer.Add(portCtrl,0)
        panel.sizer.Add((20, 20))


        while panel.Affirmed():
            panel.SetResult(commandCtrl.GetValue(), payloadCtrl.GetValue(), portCtrl.GetValue())

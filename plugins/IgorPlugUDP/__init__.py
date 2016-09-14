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

u"""<rst>
Plugin for `Igor \u010Ce\u0161ko's UDP IR`__ receiver.

This device is connected directly to twisted pair 10/100 BASE TX network.
It receives signal from standard infrared remote control
(used for TV, DVD players, ... ) and send it to group of computers
on the network (UDP broadcast).
Therefore signal can be collected by more computers also.

__ http://www.cesko.host.sk/IgorPlugUDP/IgorPlug-UDP%20%28AVR%29_eng.htm
"""

import eg
from threading import Thread, Event
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from socket import error as socket_error
import asyncore
from locale import getdefaultlocale as localeEncoding

eg.RegisterPlugin(
    name = "IgorPlug-UDP",
    author = (
        "Pako",
        "Bitmonster",
    ),
    version = "0.1.1",
    kind = "remote",
    guid = "{F31FCA60-D7D2-4767-801D-D1B8566D57EA}",
    description = __doc__,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAADAFBMVEUAAACAAAAAgACA"
        "gAAAAICAAIAAgICAgIDAwMD/AAAA/wD//wAAAP//AP8A//////8AAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABYBAnEAAAA"
        "0klEQVR4nJWQ2xKDIAxEwwMDIw75/78tuZKU2mlXRckeNhkBftB1yUPLRSou9dkwoJRN"
        "1HBe7pKAegBk7hZ1DOsgEBnZH3FEA6xDrTUDwHWfYbkKmEoS5yfgzef8CFC1Lfl5Bk5f"
        "iId8BzT/eUCbf875BHD+nJs4ATm/IzQybHiXgZkA8TcQAjQ/BQDknfidlEs6unx/9RGR"
        "fcScr52DjyFh/5jgI2RC/d4NaHDK/QW0Bjes+77pRQvnu5oDvkCP+hfgFn2Ea/k54QCo"
        "4vN9ANb+BYRyE8/VBob3AAAAAElFTkSuQmCC"
    ),
)


class Text:
    eventPrefix = "Event prefix:"
    remIP = "IgorPlug-UDP IP address:"
    locPort = "Local UDP port:"

class udpReceiver(asyncore.dispatcher):

    def __init__(self, address, port, plugin):
        self.irCommand = []
        self.remAddress=address
        self.plugin=plugin
        asyncore.dispatcher.__init__(self)
        self.create_socket(AF_INET, SOCK_DGRAM)
        eg.RestartAsyncore()
        self.bind(('', port))

    def writable(self):
        return False  # we don't have anything to send !

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_expt(self):
        self.close()

    def handle_read(self):
        payload, address = self.socket.recvfrom(128)
        if self.remAddress == address[0]:
            if len(payload)==44:
                weight = 1
                byte = 0
                flag = True
                for i in range(4,44,5):
                    if payload[i] == '\x80':
                        byte += weight
                    elif payload[i:i+5] == 5*'\x00':
                        pass
                    else:
                        flag = False
                        break
                    weight *= 2
                if flag:
                    self.irCommand.append(chr(byte))
                    if byte == 0xFF:
                        datagram = ''.join(self.irCommand)
                        if len(datagram) > 4:
                            if datagram[:4]==4*"\x00":
                                datagram = datagram[4:]
                            if len(datagram) > 4 and ord(datagram[0]) == len(datagram)-4:
                                self.plugin.irDecoder.Decode(datagram[3:],len(datagram)-3)
                        self.irCommand = []
                else:
                    self.plugin.TriggerEvent('DataError')
                    self.irCommand = []


class IgorPlugUDP(eg.IrDecoderPlugin):
    canMultiLoad = True
    text = Text

    def __init__(self):
        eg.IrDecoderPlugin.__init__(self, 51.2)

    def __start__(self, prefix="IgorUDP", locPort=6668, remAddress="192.168.1.7"):
        self.info.eventPrefix = prefix
        try:
            self.receiver = udpReceiver(remAddress, locPort, self)
        except socket_error, exc:
            raise self.Exception(exc[1].decode(localeEncoding()[1]))

    def __stop__(self):
        if self.receiver:
            self.receiver.close()
        self.receiver = None

    def __close__(self):
        self.irDecoder.Close()

    def Configure(self, prefix="IgorUDP", locPort=6668, remAddress="192.168.1.7"):
        panel = eg.ConfigPanel(self)
        prefixCtrl = panel.TextCtrl(prefix)
        ipAddressCtrl = panel.TextCtrl(remAddress)
        locPortCtrl = panel.SpinIntCtrl(locPort, min=1, max=65535)
        panel.AddLine(self.text.eventPrefix, prefixCtrl)
        panel.AddLine(self.text.remIP, ipAddressCtrl)
        panel.AddLine(self.text.locPort, locPortCtrl)

        while panel.Affirmed():
            panel.SetResult(
                prefixCtrl.GetValue(),
                int(locPortCtrl.GetValue()),
                ipAddressCtrl.GetValue(),
            )




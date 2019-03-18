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

# ChangeLog
# 0.3    29-11-2017, 14:37 -7.00 UTC
# Modified reading of data from ipconfig so it wasn't looking for specific
# english words.


import eg

eg.RegisterPlugin(
    name="Wake On Lan(WOL)",
    author="K",
    version="0.3.1",
    description="Plugin For receiving WOL Packets",
    guid="{429172A5-54C9-4D07-B51E-90CDE0F3F2E4}",
)

DEBUG = bool(eg.debugLevel)

import wx # NOQA
import os # NOQA
import asyncore # NOQA
import socket # NOQA
import re # NOQA
import threading # NOQA
from subprocess import Popen, PIPE # NOQA


class Timer(threading._Timer):

    def __init__(self, *args, **kwargs):
        threading._Timer.__init__(self, *args, **kwargs)
        self.ip_address = None
        self.finished.set()

    def restart(self, ip_address):
        self.__dict__.update(Timer(self.interval, self.function).__dict__)
        self.ip_address = ip_address
        self.finished.clear()
        self.start()

    def is_running(self, ip_address):
        return ip_address == self.ip_address and not self.finished.isSet()


def dummy_func():
    pass

_lock = threading.Lock()
_timer = Timer(1.0, dummy_func)


def get_mac_addresses(ip_addresses):
    proc = Popen("ipconfig -all", stdout=PIPE)
    data = proc.communicate()[0]
    data = data.split('\n')
    results = []

    for ip_address in ip_addresses[:]:
        mac_address = None
        for line in data:
            line = line.strip()
            if not line:
                continue
            line = line.split(': ')
            if len(line) != 2:
                continue
            if len(line[1].split('-')) == 6:
                mac_address = line[1]
                continue
            if ip_address in line[1] and mac_address is not None:
                results += [[ip_address, mac_address.replace('-', ':')]]
                break

    return results


class Server(asyncore.dispatcher):

    def __init__(self, plugin, port, ip_address, mac_address):
        self.plugin = plugin
        self.addresses = socket.gethostbyname_ex(socket.gethostname())[2]
        self.addresses.sort(key=lambda a: [int(b) for b in a.split('.', 4)])
        self.port = port

        self.wol_packet = (
            [255, 255, 255, 255, 255, 255] +
            (list(int(m, 16) for m in mac_address.split(':')) * 16)
        )

        if ip_address in self.addresses:
            self.ip_address = ip_address
            asyncore.dispatcher.__init__(self)
            self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
            eg.RestartAsyncore()
            self.set_reuse_addr()
            self.bind((self.ip_address, self.port))
        else:
            raise socket.error

    def handle_connect(self):
        pass

    def handle_read(self):
        data, address = self.socket.recvfrom(102)

        _lock.acquire()

        try:
            if _timer.is_running(address[0]):
                return

            data = list(int(hex(ord(char)), 16) for char in data)

            if data == self.wol_packet:
                _timer.restart(address[0])
                eg.TriggerEvent(
                    prefix=self.plugin.info.eventPrefix,
                    suffix='PacketReceived.Port' + str(self.port),
                    payload=address[0]
                )

            elif DEBUG:
                print 'data:', data
                print 'wol_packet:', self.wol_packet

        finally:
            _lock.release()

    def writable(self):
        return False  # we don't have anything to send !


class WOL(eg.PluginBase):

    class Text:
        event_lbl = "Event prefix:"
        listen_lbl = "Listening address:"

    text = Text

    def __init__(self):
        self.server_0 = None
        self.server_7 = None
        self.server_9 = None

    def __start__(self, prefix=None, lan_address=""):
        self.info.eventPrefix = prefix

        def start_server(port):
            try:
                return Server(self, port, *lan_address.split(' - '))
            except socket.error:
                eg.PrintNotice('Wake On Lan: Unable to bind to port %d' % port)
                return None

        self.server_0 = start_server(0)
        self.server_7 = start_server(7)
        self.server_9 = start_server(9)

    def __stop__(self):
        _timer.cancel()

        if self.server_0 is not None:
            self.server_0.close()
        if self.server_7 is not None:
            self.server_7.close()
        if self.server_9 is not None:
            self.server_9.close()

        self.server_0 = None
        self.server_7 = None
        self.server_9 = None

    def debugging_on(self):
        global DEBUG

        DEBUG = True

    def debugging_off(self):
        global DEBUG

        DEBUG = False

    def Configure(self, prefix="WOL",  lan_address=""):
        text = self.text
        panel = eg.ConfigPanel(self)

        addresses = socket.gethostbyname_ex(socket.gethostname())[2]
        addresses.sort(key=lambda a: [int(b) for b in a.split('.', 4)])

        addresses = get_mac_addresses(addresses)
        addresses = list(' - '.join(address) for address in addresses)

        for selected, address in enumerate(addresses):
            if lan_address == address:
                break
        else:
            selected = 0

        edit_ctrl = panel.TextCtrl(prefix)
        listen_ctrl = panel.Choice(selected, addresses)

        panel.AddLine(text.event_lbl, edit_ctrl)
        panel.AddLine(text.listen_lbl, listen_ctrl)

        while panel.Affirmed():
            panel.SetResult(
                edit_ctrl.GetValue(),
                listen_ctrl.GetStringSelection(),
            )

# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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
import threading
import socket
import traceback


class TelnetClient(threading.Thread):

    def __init__(self, plugin, host, port, timeout, debug):
        self.plugin = plugin
        self.sock = None
        self.host = host
        self.port = port
        self.timeout = timeout
        self.errorCount = 0
        self.event = threading.Event()
        self.debug = debug
        threading.Thread.__init__(self, name='Marantz AVR Connection')

    def run(self):

        def Connect():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(self.timeout)
                s.connect((self.host, self.port))
                return s
            except socket.error:
                tb = traceback.format_exc().split('\n')
                tb = '    ' + '\n    '.join(tb)
                self.debug('AVR connection error:' + tb)
                if self.errorCount == 5:
                    eg.PrintError('Marantz AVR connection error')
                    traceback.print_exc()
                    self.event.set()
                self.errorCount += 1

        self.sock = sock = Connect()

        while not self.event.isSet() and sock is None:
            self.event.wait(5)
            self.sock = sock = Connect()

        if sock:
            eg.PrintNotice('Marantz AVR connected')

        data = ''
        while not self.event.isSet():
            try:
                data += sock.recv(1024)
                while '\r' in data:
                    rIndex = data.find('\r') + 1
                    if not self.event.isSet():
                        self.plugin.ProcessData(data[:rIndex])
                    data = data[rIndex:]

            except socket.error as e:
                if str(e) != 'timed out':
                    if not self.event.isSet():
                        traceback.print_exc()
                    self.event.set()
        if self.sock is not None:
            eg.PrintNotice('Marantz AVR disconnected')
            self.sock = None

        self.plugin.client = None

    def Send(self, message):
        try:
            self.sock.send(message)
        except socket.error:
            pass

    def Start(self):
        self.start()

    def Stop(self):
        self.event.set()
        try:
            self.sock.close()
            self.Send('MV?\r')
        except AttributeError:
            pass
        self.join(self.timeout + 1)

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


class ClientThread(threading.Thread):
    def __init__(self, handler, plugin, timeout, ip, sock, debug):
        self.handler = handler
        self.plugin = plugin
        self.timeout = timeout
        self.ip = ip
        self.sock = sock
        self.event = threading.Event()
        self.debug = debug
        threading.Thread.__init__(
            self,
            name='Marantz Telnet Server Client %s' % ip
        )

    def run(self):
        self.plugin.TriggerEvent('Connection.Established.%s' % self.ip)
        self.sock.settimeout(self.timeout)
        data = ''

        while not self.event.isSet():
            try:
                data += self.sock.recv(1024)
                while '\r' in data:
                    rIndex = data.find('\r') + 1
                    if not self.event.isSet():
                        self.debug(
                            'ECHO CLIENT %s: <--- %r' %
                            (self.ip, data[:rIndex])
                        )
                        self.plugin.EchoCommand(data[:rIndex])
                    data = data[rIndex:]

            except socket.error as e:
                if str(e) != 'timed out':
                    if not self.event.isSet():
                        tb = traceback.format_exc().split('\n')
                        tb = '    ' + '\n    '.join(tb)
                        self.debug(
                            'ECHO CLIENT %s: connection error\n%s' %
                            (self.ip, tb)
                        )
                        traceback.print_exc()
                    self.event.set()

        self.plugin.TriggerEvent('Connection.Closed.%s' % self.ip)
        self.sock = None
        self.handler.RemoveThread(self)

    def Send(self, message):
        self.debug(
            'ECHO CLIENT %s: ---> %r' %
            (self.ip, message)
        )
        self.sock.send(message)

    def Start(self):
        self.start()

    def Stop(self):
        self.event.set()


class TelnetServer(threading.Thread):

    def __init__(self, plugin, timeout, debug):
        self.plugin = plugin
        self.timeout = timeout
        self.sock = None
        self.threads = []
        self.event = threading.Event()
        self.debug = debug
        threading.Thread.__init__(self, name='Marantz Telnet Server')

    def run(self):
        try:
            self.sock = sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(self.timeout)
            sock.bind(('', 23))
        except socket.error:
            eg.PrintError('Marantz Echo Server Error')
            traceback.print_exc()
        else:
            eg.PrintNotice('Marantz Echo Server Started')

            while not self.event.isSet():
                sock.listen(4)
                try:
                    conn, addr = sock.accept()

                    self.debug('ECHO SERVER: new client %s' % addr[0])

                    t = ClientThread(
                        self,
                        self.plugin,
                        self.timeout,
                        addr[0],
                        conn,
                        self.debug
                    )
                    t.start()
                    self.threads.append(t)
                except socket.error as e:
                    if str(e) != 'timed out':
                        if not self.event.isSet():
                            tb = traceback.format_exc().split('\n')
                            tb = '    ' + '\n    '.join(tb)
                            self.debug(
                                'ECHO SERVER: connection error\n%s' % tb
                            )
                            traceback.print_exc()
                        self.event.set()
            self.sock = None
            eg.PrintNotice('Marantz Echo Server Stopped')

        self.plugin.server = None

    def RemoveThread(self, t):
        try:
            self.threads.remove(t)
        except:
            pass

    def Send(self, message):
        self.threads = list(t for t in self.threads if t)
        for t in self.threads:
            t.Send(message)

    def Start(self):
        self.start()

    def Stop(self):
        self.threads = list(t for t in self.threads if t)

        for t in self.threads[:]:
            t.Stop()
        self.event.set()
        try:
            self.sock.close()
        except AttributeError:
            pass
        self.join(self.timeout + 1)

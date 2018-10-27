# -*- coding: utf-8 -*-
# cython: language_level=2

# This file is part of EventGhost.
# Copyright © 2005-2018 EventGhost Project <http://eventghost.net/>
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


import threading
import socket
import traceback
import sys
import atexit
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


eg = None

class WriteProtect(type):

    def __setattr__(cls, key, value):
        raise RuntimeError('Permission Denied')


class AESCipher(object):
    __metaclass__ = WriteProtect

    @classmethod
    def encrypt(cls, raw):
        raw = cls._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(
            hashlib.sha256(
                'GENERATED KEY'.encode()
            ).digest(),
            AES.MODE_CBC,
            iv
        )
        return base64.b64encode(iv + cipher.encrypt(raw))

    @classmethod
    def decrypt(cls, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(
            hashlib.sha256(
                'GENERATED KEY'.encode()
            ).digest(),
            AES.MODE_CBC,
            iv
        )

        return cls._unpad(
            cipher.decrypt(enc[AES.block_size:])
        ).decode('utf-8')

    @staticmethod
    def _pad(s):
        return s + (32 - len(s) % 32) * chr(32 - len(s) % 32)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s) - 1:])]


class SocketException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class SocketDataError(SocketException):
    pass


class SocketCommandError(SocketException):
    pass


class SocketConnectionError(SocketException):

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        return self.msg[item]


def process_data(command):
    try:
        command, data = command.split(',', 1)
    except ValueError:
        data = '()'

    eg.PrintDebugNotice('Command: {0}, Parameters: {1}'.format(command, data))
    command = command.strip()
    data = data.strip()

    try:
        if '=' in command:
            raise SocketCommandError('Command not allowed: ' + command)

        if not data.startswith('dict') and '=' in data:
            raise SocketDataError('Data not allowed: ' + data)

        if (
            data[0] not in ('(', '[', '{') and
            not data.startswith('dict')
        ):
            raise SocketDataError('Data not allowed: ' + data)

        try:
            command = eval(command.split('(', 1)[0])
        except SyntaxError:
            raise SocketDataError('Command malformed: ' + command)
        else:
            if isinstance(command, (str, unicode)):
                raise SocketCommandError('Command does not exist: ' + command)
        try:
            data = eval(data)
        except SyntaxError:
            raise SocketDataError('Data malformed: ' + str(data))

        if not isinstance(data, (dict, list, tuple)):
            raise SocketDataError('Data malformed: ' + str(data))

    except SocketException:
        eg.PrintDebugNotice(traceback.format_exc())

    else:
        try:
            if isinstance(data, dict):
                return command(**data)
            elif isinstance(data, (tuple, list)):
                return command(*data)
        except:
            eg.PrintDebugNotice(traceback.format_exc())
            return None


def send_message(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(2.0)
    sys.stderr._displayMessage = False
    sys.stderr.write('New Instance: send message ' + repr(message) + '\n')
    try:
        sock.connect(('127.0.0.1', 38765))

        data = ''
        while '\r' not in data:
            data += sock.recv(4096)

        data = data[:data.find('\r')]
        if data == '?':
            aes_string = AESCipher.encrypt(str(message))
            sock.sendall(aes_string + '\r')
        else:
            return None

        data = ''

        while '\r' not in data:
            data += sock.recv(4096)

        aes_string = data[:data.find('\r')]
        response = AESCipher.decrypt(aes_string)
        sys.stderr.write('New Instance: response ' + repr(response) + '\n')

        aes_string = AESCipher.encrypt('closecon')
        sock.sendall(aes_string + '\r')

        return response
    except socket.timeout:
        return None
    except socket.error:
        return None
    finally:
        try:
            sock.close()
        except socket.error:
            pass


def _close_sock(sock):
    try:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except (AttributeError, socket.error):
        pass


def is_eg_running():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(2.0)
    try:
        sock.connect(('127.0.0.1', 38765))
        data = ''
        try:
            while '\r' not in data:
                data += sock.recv(4096)
            data = data[:data.find('\r')]
            if data == '?':
                aes_string = AESCipher.encrypt('testcon')
                sock.sendall(aes_string + '\r')
                _close_sock(sock)
                return True
            else:
                _close_sock(sock)
                return None

        except socket.error:
            _close_sock(sock)
            return None

    except socket.timeout:
        _close_sock(sock)
        return None

    except socket.error:
        _close_sock(sock)
        return False


class Client(threading.Thread):
    __metaclass__ = WriteProtect

    def __init__(self, handler, ip, sock, id):
        self.id = id
        self.rsa_key = None
        self.handler = handler
        self.ip = ip
        self.sock = sock
        self.event = threading.Event()
        threading.Thread.__init__(
            self,
            name='EventGhost Socket Client: {0}:{1}'.format(ip, id)
        )

    def run(self):
        eg.PrintDebugNotice('New Client')
        try:
            self.sock.settimeout(600)
            data = ''
            self.sock.sendall('?\r')
        except socket.error:
            pass

        else:

            while not self.event.isSet():
                try:
                    while '\r' not in data:

                        data += self.sock.recv(4096)
                    index = data.find('\r')
                    aes_string = data[:index]
                    data = data[index + 1:]

                    if not self.event.isSet():
                        try:
                            command = AESCipher.decrypt(aes_string)
                            eg.PrintDebugNotice(' ---> EG - ' + command)
                        except:
                            eg.PrintError('Unauthorized access')
                            self.handler.unauth_count += 1
                            self.event.set()
                        else:

                            if command in ('testcon', 'closecon'):
                                self.event.set()
                            else:
                                self.Send(process_data(command))
                except socket.timeout():
                    self.Send('closecon')
                    self.event.set()

                except socket.error:
                    self.event.set()

            eg.PrintDebugNotice('Connection Closed')

        _close_sock(self.sock)
        self.sock = None

    def Send(self, message):
        eg.PrintDebugNotice('<---- EG - ' + repr(message))

        aes_string = AESCipher.encrypt(str(message))
        self.sock.sendall(aes_string + '\r')

    def Start(self):
        self.start()

    def Stop(self):
        if not self.event.isSet():
            self.event.set()
            self.sock.close()
            self.join(2.0)


class Server(threading.Thread):

    __metaclass__ = WriteProtect

    def __init__(self):
        self.unauth_count = 0
        self.sock = None
        self.threads = []
        self.error_count = 0
        self.conn_count = 0
        self.event = threading.Event()
        threading.Thread.__init__(self, name='EventGhost SocketServer')

    def run(self):
        atexit.register(self.Stop)

        def start_sock():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('127.0.0.1', 38765))
                # SOMAXCONN = 2147483647
                s.listen(socket.SOMAXCONN)
                eg.PrintDebugNotice('Socket Server: startup success.')
                return s
            except socket.error:
                eg.PrintError('Socket Server: startup failed.')
                traceback.print_exc()
                return None
        self.sock = sock = start_sock()

        if sock is not None:
            while not self.event.isSet():
                if self.unauth_count > 3:
                    eg.PrintError(
                        'Socket Server: to many unauthorized '
                        'access attempts shutting down.'
                    )
                    self.event.set()
                    break
                try:
                    conn, addr = sock.accept()
                    self.conn_count += 1
                    t = Client(self, addr[0], conn, self.conn_count)
                    t.start()
                    self.threads.append(t)
                    self.threads = list(t for t in self.threads if t.isAlive())
                    self.error_count = 0

                except socket.error:
                    tb = traceback.format_exc().split('\n')
                    tb = '    ' + '\n    '.join(tb)
                    eg.PrintDebugNotice('Connection Error:')
                    eg.PrintDebugNotice(tb)

                    if not self.event.isSet():

                        def restart_sock():
                            self.error_count += 1

                            if self.error_count > 2:
                                self.end_threads()
                                _close_sock(self.sock)

                                self.event.wait(self.error_count)

                                return start_sock()
                            return self.sock

                        self.sock = sock = restart_sock()
                        while not self.event.isSet() and self.sock is None:
                            self.sock = sock = restart_sock()

            self.end_threads()
            _close_sock(self.sock)

            self.sock = None
            eg.PrintDebugNotice('Socket Server: server stopped.')

    def Send(self, message):
        self.threads = list(t for t in self.threads if t.isAlive())
        for t in self.threads:
            t.Send(message)

    def Start(self):
        global eg
        eg = __import__('eg')
        self.start()
        return self

    def end_threads(self):
        self.threads = list(t for t in self.threads if t.isAlive())
        for t in self.threads[:]:
            t.Stop()

    def Stop(self):
        if not self.event.isSet():
            self.event.set()
            is_eg_running()
            try:
                self.join(2.0)
            except:
                pass


def Start():
    server = Server()
    return server.Start()

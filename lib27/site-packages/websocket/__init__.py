import re
import struct
from hashlib import md5

version_info = (0, 2, 1)
__version__ = '0.2.1'

# This class implements the Websocket protocol draft version as of May 23, 2010
# The version as of August 6, 2010 will be implementend once Firefox or
# Webkit-trunk support this version.


class WebSocket(object):

    @classmethod
    def is_socket(self, environ):
        if 'upgrade' not in environ.get("HTTP_CONNECTION").lower():
            return False
        if environ.get("HTTP_UPGRADE") != "WebSocket":
            return False
        if not environ.get("HTTP_ORIGIN"):
            return False
        return True

    def __init__(self, environ, socket, rfile):
        # QQQ should reply Bad Request when IOError is raised above
        #     should only log the error message, traceback is not necessary
        self.origin = environ['HTTP_ORIGIN']
        self.protocol = environ.get('HTTP_SEC_WEBSOCKET_PROTOCOL', 'unknown')
        self.path_info = environ['PATH_INFO']
        self.host = environ['HTTP_HOST']
        self.key1 = environ.get('HTTP_SEC_WEBSOCKET_KEY1')
        self.key2 = environ.get('HTTP_SEC_WEBSOCKET_KEY2')
        self.socket = socket
        self.rfile = rfile
        self.handshaked = False

    def __repr__(self):
        try:
            info = ' ' + self.socket._formatinfo()
        except Exception:
            info = ''
        return '<%s at %s%s>' % (type(self).__name__, hex(id(self)), info)

    def do_handshake(self):
        """This method is called automatically in the first send() or receive()"""
        assert not self.handshaked, 'Already did handshake'
        if self.key1 is not None:
            # version 76
            if not self.key1:
                message = "Missing HTTP_SEC_WEBSOCKET_KEY1 header in the request"
                self._reply_400(message)
                raise IOError(message)
            if not self.key2:
                message = "Missing HTTP_SEC_WEBSOCKET_KEY2 header in the request"
                self._reply_400(message)
                raise IOError(message)
            headers = [
                ("Upgrade", "WebSocket"),
                ("Connection", "Upgrade"),
                ("Sec-WebSocket-Origin", self.origin),
                ("Sec-WebSocket-Protocol", self.protocol),
                ("Sec-WebSocket-Location", "ws://" + self.host + self.path_info),
            ]
            self._send_reply("101 Web Socket Protocol Handshake", headers)
            challenge = self._get_challenge()
            self.socket.sendall(challenge)
        else:
            # version 75
            headers = [
                ("Upgrade", "WebSocket"),
                ("Connection", "Upgrade"),
                ("WebSocket-Origin", self.websocket.origin),
                ("WebSocket-Protocol", self.websocket.protocol),
                ("WebSocket-Location", "ws://" + self.host + self.path_info),
            ]
            self._send_reply("101 Web Socket Protocol Handshake", headers)
        self.handshaked = True

    def _send_reply(self, status, headers, message=None):
        self.status = status
        self.headers_sent = True
        towrite = ['HTTP/1.1 %s\r\n' % self.status]
        for header in headers:
            towrite.append("%s: %s\r\n" % header)
        towrite.append("\r\n")
        if message:
            towrite.append(message)
        self.socket.sendall(''.join(towrite))

    def _reply_400(self, message):
        self._send_reply('400 Bad Request',
                         [('Content-Length', str(len(message))),
                          ('Content-Type', 'text/plain')],
                         message)
        self.socket = None
        self.rfile = None

    def _get_key_value(self, key_value):
        key_number = int(re.sub("\\D", "", key_value))
        spaces = re.subn(" ", "", key_value)[1]

        if key_number % spaces != 0:
            self._reply_400('Invalid key')
            raise IOError("key_number %r is not an intergral multiple of spaces %r" % (key_number, spaces))

        return key_number / spaces

    def _get_challenge(self):
        part1 = self._get_key_value(self.key1)
        part2 = self._get_key_value(self.key2)

        # This request should have 8 bytes of data in the body
        key3 = self.rfile.read(8)

        challenge = ""
        challenge += struct.pack("!I", part1)
        challenge += struct.pack("!I", part2)
        challenge += key3
        return md5(challenge).digest()

    def send(self, message):
        if not self.handshaked:
            self.do_handshake()
        if isinstance(message, str):
            pass
        elif isinstance(message, unicode):
            message = message.encode('utf-8')
        else:
            raise TypeError("Expected string or unicode: %r" % (message, ))
        self.socket.sendall("\x00" + message + "\xFF")

    def close(self):
        # XXX implement graceful close with 0xFF frame
        if self.socket is not None:
            try:
                self.socket.close()
            except Exception:
                pass
            self.socket = None
            self.rfile = None

    def _message_length(self):
        # TODO: buildin security agains lengths greater than 2**31 or 2**32
        length = 0

        while True:
            byte_str = self.rfile.read(1)

            if not byte_str:
                return 0
            else:
                byte = ord(byte_str)

            if byte != 0x00:
                length = length * 128 + (byte & 0x7f)
                if (byte & 0x80) != 0x80:
                    break

        return length

    def _read_until(self):
        bytes = []

        while True:
            byte = self.rfile.read(1)
            if ord(byte) != 0xff:
                bytes.append(byte)
            else:
                break

        return ''.join(bytes)

    def receive(self):
        if not self.handshaked:
            self.do_handshake()
        while self.socket is not None:
            frame_str = self.rfile.read(1)
            if not frame_str:
                self.close()
                break
            else:
                frame_type = ord(frame_str)

            if (frame_type & 0x80) == 0x00:  # most significant byte is not set
                if frame_type == 0x00:
                    bytes = self._read_until()
                    return bytes.decode("utf-8")
                else:
                    self.close()
            elif (frame_type & 0x80) == 0x80:  # most significant byte is set
                # Read binary data (forward-compatibility)
                if frame_type != 0xff:
                    self.close()
                    break
                else:
                    length = self._message_length()
                    if length == 0:
                        self.close()
                        break
                    else:
                        self.rfile.read(length)  # discard the bytes
            else:
                raise IOError("Received invalid message")

    def getsockname(self):
        return self.socket.getsockname()

    def getpeername(self):
        return self.socket.getpeername()

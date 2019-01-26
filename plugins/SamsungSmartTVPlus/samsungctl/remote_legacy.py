import base64
import socket
import struct
import threading
import sys
from . import exceptions

import logging

logger = logging.getLogger('samsungctl')

PY3 = sys.version_info[0] >= 3


class RemoteLegacy(object):
    """Object for remote control connection."""

    def __init__(self, config):
        """Make a new connection."""

        self.send = self.control
        self._connect_event = threading.Event()
        self._receive_event = threading.Event()
        self._send_lock = threading.Lock()
        self.connection = None
        self.config = config

    def open(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.config.host, self.config.port))

        if PY3:
            payload = b'\x64\x00'
            packet = b'\x00\x00\x00'

        else:
            payload = '\x64\x00'
            packet = '\x00\x00\x00'

        payload += (
            self._serialize_string(self.config.description) +
            self._serialize_string(self.config.id) +
            self._serialize_string(self.config.name)
        )

        packet += self._serialize_string(payload, True)
        logger.info("Sending handshake.")

        self.connection.send(packet)
        self._read_response(True)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        """Close the connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.debug("Connection closed.")

    def control(self, key):
        """Send a control command."""
        if not self.connection:
            raise exceptions.ConnectionClosed()

        with self._send_lock:
            self._receive_event.clear()

            if PY3:
                payload = b'\x00\x00\x00'
                packet = b'\x00\x00\x00'
            else:
                payload = '\x00\x00\x00'
                packet = '\x00\x00\x00'

            payload += self._serialize_string(key)
            packet += self._serialize_string(payload, True)

            logging.info("Sending control command: %s", key)
            self.connection.send(packet)
            self._read_response()
            self._receive_event.wait(self._key_interval)

    _key_interval = 0.2

    def _read_response(self, first_time=False):
        header = self.connection.recv(3)

        tv_name_len = struct.unpack("<H", header[1:3])[0]

        tv_name = self.connection.recv(tv_name_len)
        if first_time:
            logger.debug("Connected to '%s'.", tv_name.decode())

        response_len = struct.unpack("<H", self.connection.recv(2))[0]

        response = self.connection.recv(response_len)

        if len(response) == 0:
            self.close()
            raise exceptions.ConnectionClosed()

        if PY3:
            response1 = b'\x64\x00\x01\x00'
            response2 = b'\x64\x00\x00\x00'
            response3 = b'\x0A'
            response4 = b'\x65'
            response5 = b'\x00\x00\x00\x00'

        else:
            response1 = '\x64\x00\x01\x00'
            response2 = '\x64\x00\x00\x00'
            response3 = '\x0A'
            response4 = '\x65'
            response5 = '\x00\x00\x00\x00'

        if response == response1:
            logger.debug("Access granted.")
            return
        elif response == response2:
            raise exceptions.AccessDenied()
        elif response[0:1] == response3:
            if first_time:
                logger.warning("Waiting for authorization...")
            return self._read_response()
        elif response[0:1] == response4:
            logger.warning("Authorization cancelled.")
            raise exceptions.AccessDenied()
        elif response == response5:
            logger.debug("Control accepted.")
            self._receive_event.set()
            return

        raise exceptions.UnhandledResponse(response)

    @staticmethod
    def _serialize_string(string, raw=False):
        if PY3:
            if isinstance(string, str):
                string = string.encode('utf-8')
            if not raw:
                string = base64.b64encode(string)

            return bytes([len(string)]) + b"\x00" + string
        else:
            if isinstance(string, str):
                string = string.decode('utf-8')
            if not raw:
                string = base64.b64encode(string)

            return chr(len(string)) + "\x00" + string

# -*- coding: utf-8 -*-

from __future__ import print_function
import re
import requests
import time
import json
import threading
import logging
from . import exceptions
from websocket import WebSocketApp
from .pySmartCrypto.command_encryption import AESCipher
from .pySmartCrypto import crypto

logger = logging.getLogger('samsungctl')

WEBSOCKET_URL = 'ws://{ip}:{port}/socket.io/1/websocket/{path}'
URL = 'http://{ip}:{http_port}'
PAIRING_URL_FINAL = 'http://{ip}:{http_port}/socket.io/1/?t={millis}'
PIN_URL_OPEN = 'http://{ip}:{http_port}/ws/apps/CloudPINPage'
PIN_URL_CLOSE = 'http://{ip}:{http_port}/ws/apps/CloudPINPage/run'
PAIRING_URL = (
    'http://{ip}:{http_port}/ws/pairing?'
    'step={step}&'
    'app_id=com.samsung.companion&'
    'device_id={device_id}'
)


class RemoteWebsocketEncrypted(WebSocketApp):
    """Object for remote control connection."""

    def on_open(self, ws):
        self._socket = ws
        self._connect_event.set()

    def on_close(self, _):
        self._socket = None
        self._connect_event.clear()

    def on_error(self, _, err):
        logger.error('Websocket Error: %s', err)

    def on_message(self, _, message):
        logger.debug('Incoming message: %s', message)
        self._receive_event.set()

    def __init__(self, config):
        self.config = config

        self.last_request_id = 0
        self.pairing_step = 0

        self.session_id = None
        self.ctx = None
        self._aes_lib = None

        self.send = self.control
        self._connect_event = threading.Event()
        self._receive_event = threading.Event()
        self._authorization_event = threading.Event()
        self._send_lock = threading.Lock()
        self._socket = None
        self._run_thread = None

    @property
    def aes_lib(self):
        if self._aes_lib is None:
            self._aes_lib = AESCipher(self.ctx, self.session_id)
        return self._aes_lib

    @property
    def pairing_url(self):
        if self.pairing_step == 3:
            millis = int(round(time.time() * 1000))
            url = PAIRING_URL_FINAL.format(self.config.host, millis=millis)
        else:
            url = PAIRING_URL.format(
                ip=self.config.ip,
                http_port=self.config.http_port,
                step=self.pairing_step,
                device_id=self.config.device_id
            )

            if self.pairing_step == 0:
                url += "&type=1"

            self.pairing_step += 1

        return url

    @property
    def pin(self):
        return self.config.token

    @pin.setter
    def pin(self, pin):
        self.config.token = pin
        self.run_forever()

    @property
    def is_pin_page_open(self):
        url = PIN_URL_OPEN.format(
            ip=self.config.host,
            http_port=self.config.http_port,
        )
        response = requests.get(url)
        response = re.search(
            'state>([^<>]*)</state>',
            response.content,
            flags=re.IGNORECASE
        )

        if response is not None:
            state = response.group(1)
            if state == "stopped":
                return False
            return True
        return False

    def open(self):
        if self.pin is None:
            if not self.is_pin_page_open:
                url = PIN_URL_OPEN.format(
                    ip=self.config.host,
                    http_port=self.config.http_port,
                )

                requests.post(url, "pin4")
        else:
            self.pin = self.config.token

    def run_forever(self):
        def do():
            WebSocketApp.run_forever(self)
            self._run_thread = None

        if self._run_thread is None:
            requests.get(self.pairing_url)

            server_hello, data_hash, aes_key = crypto.generate_server_hello(
                self.config.id,
                self.pin
            )

            content = dict(
                auth_Data=dict(
                    auth_type="SPC",
                    GeneratorServerHello=hex(int(server_hello)).upper()
                )
            )

            content = json.dumps(content)
            response = requests.post(self.pairing_url, content)

            response = re.search(
                'request_id.*?(\d).*?GeneratorClientHello.*?:.*?(\d[0-9a-zA-Z]*)',
                response.content,
                flags=re.IGNORECASE
            )

            if response is not None:
                request_id = response.group(1)
                client_hello = response.group(2)
                self.last_request_id = int(request_id)
                ctx, sk_prime = crypto.parse_client_hello(
                    client_hello,
                    data_hash,
                    aes_key,
                    self.config.id
                )

                ack_message = crypto.generate_server_acknowledge(sk_prime)
                content = dict(
                    auth_Data=dict(
                        auth_type="SPC",
                        request_id=self.last_request_id,
                        ServerAckMsg=ack_message
                    )
                )
                content = json.dumps(content)

                response = requests.post(self.pairing_url, content)
                response = response.content

                if "secure-mode" in response:
                    raise RuntimeError(
                        'TODO: Implement handling of encryption flag!!!!'
                    )

                response = re.search(
                    'ClientAckMsg.*?:.*?(\d[0-9a-zA-Z]*).*?session_id.*?(\d)',
                    response,
                    flags=re.IGNORECASE
                )

                if response is None:
                    raise RuntimeError(
                        "Unable to get session_id and/or ClientAckMsg!!!"
                    )

                client_ack = response.group(1)
                if not crypto.parse_client_acknowledge(client_ack, sk_prime):
                    raise RuntimeError(
                        "Parse client ac message failed."
                    )

                self.session_id = response.group(2)
                self.ctx = ctx.upper()

                response = requests.get(self.pairing_url)
                url = WEBSOCKET_URL.format(
                    ip=self.config.host,
                    port=self.config.port,
                    path=response.content.split(':')[0]
                )

                time.sleep(0.35)
                # need sleeps cuz if you send commands to quick it fails

                if self.is_pin_page_open:
                    url = PIN_URL_CLOSE.format(
                        ip=self.config.host,
                        http_port=self.config.http_port
                    )
                    requests.delete(url)
                self._connect_event.clear()
                self._receive_event.clear()

                super(RemoteWebsocketEncrypted, self).__init__(url)

                self._run_thread = threading.Thread(target=do)
                self._run_thread.start()
                self._connect_event.wait(5)
                self._receive_event.wait(30)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def close(self):
        """Close the connection."""
        logger.debug("Closing Websocket Connection.")
        WebSocketApp.close(self)

    def control(self, key):
        """Send a control command."""
        if self._socket is None:
            raise exceptions.ConnectionClosed

        with self._send_lock:
            payload = self.aes_lib.generate_command(key)

            logger.info("Sending control command: %s", key)
            logger.debug("Command data: %s", payload)

            self._receive_event.clear()
            WebSocketApp.send(self, '1::/com.samsung.companion')
            self._receive_event.wait(self._key_interval)
            self._receive_event.clear()
            WebSocketApp.send(self, payload)
            self._receive_event.wait(self._key_interval)

    _key_interval = 0.35

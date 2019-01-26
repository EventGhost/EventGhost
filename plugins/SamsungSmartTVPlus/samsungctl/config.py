# -*- coding: utf-8 -*-

import os
import socket
import json
import logging
from . import exceptions


logger = logging.getLogger('samsungctl')


DEFAULT_CONFIG = dict(
    name=None,
    description=None,
    host=None,
    port=None,
    id=None,
    method=None,
    timeout=None
)


class Config(object):
    LOG_OFF = logging.NOTSET
    LOG_CRITICAL = logging.CRITICAL
    LOG_ERROR = logging.ERROR
    LOG_WARNING = logging.WARNING
    LOG_INFO = logging.INFO
    LOG_DEBUG = logging.DEBUG

    def __init__(
        self,
        name=None,
        description=None,
        host=None,
        port=None,
        id=None,
        method=None,
        timeout=0,
        token=None,
        path=None,
        device_id=None,
        http_port=None
    ):

        if description is None:
            description = socket.gethostname()

        self.name = name
        self.description = description
        self.host = host
        self.port = port
        self.id = id
        self.method = method
        self.timeout = timeout
        self.token = token
        self.path = path
        self.device_id = device_id
        self.http_port = http_port
        self.serialized_name = None
        self.protocol = None

    @property
    def log_level(self):
        return logger.getEffectiveLevel()

    @log_level.setter
    def log_level(self, log_level):
        if log_level is None:
            log_level = logging.NOTSET

        if log_level in (
            logging.NOTSET,
            logging.CRITICAL,
            logging.ERROR,
            logging.WARNING,
            logging.INFO,
            logging.DEBUG
        ):
            logger.setLevel(log_level)

    def __eq__(self, other):
        if isinstance(other, Config):
            return (
                self.name == other.name and
                self.description == other.description and
                self.port == other.port and
                self.token == other.token and
                self.device_id == other.device_id
            )

        return False

    @classmethod
    def load(cls, path):
        if os.path.exists(path):
            config = dict(
                list(item for item in DEFAULT_CONFIG.items())
            )
            with open(path, 'r') as f:
                loaded_config = f.read()

                try:
                    loaded_config = json.loads(loaded_config)
                    config.update(loaded_config)

                except ValueError:
                    for line in loaded_config.split('\n'):
                        if not line.strip():
                            continue

                        try:
                            key, value = line.split('=')
                        except ValueError:
                            raise exceptions.ConfigParseError

                        key = key.lower().strip()
                        value = value.strip()

                        if key != 'token' and key not in config:
                            raise exceptions.ConfigParameterError(key)

                        try:
                            value = int(value)
                        except ValueError:
                            continue

                        config[key] = value

        else:
            raise exceptions.ConfigLoadError

        config['path'] = path

        return cls.__new__(**config)

    def save(self, path=None):
        if path is None:
            if self.path is None:
                raise exceptions.ConfigSavePathNotSpecified

            path = self.path

        elif self.path is None:
            self.path = path

        if not os.path.exists(path):
            path, file_name = os.path.split(path)

            if not os.path.exists(path) or not os.path.isdir(path):
                raise exceptions.ConfigSavePathError(path)

            path = os.path.join(path, file_name)

        if os.path.isdir(path):
            path = os.path.join(path, self.name + '.config')

        try:
            with open(path, 'w') as f:
                f.write(str(self))
        except (IOError, OSError):
            import traceback
            traceback.print_exc()
            raise exceptions.ConfigSaveError

    def __iter__(self):
        yield 'name', self.name
        yield 'description', self.description
        yield 'host', self.host
        yield 'port', self.port
        yield 'id', self.id
        yield 'method', self.method
        yield 'timeout', self.timeout
        yield 'token', self.token
        yield 'device_id', self.device_id
        yield 'http_port', self.http_port

    def __str__(self):
        return TEMPLATE.format(
            name=self.name,
            description=self.description,
            host=self.host,
            port=self.port,
            id=self.id,
            method=self.method,
            timeout=self.timeout,
            token=self.token,
            device_id=self.device_id,
            http_port=self.http_port
        )


TEMPLATE = '''name = {name}
description = {description}
host = {host}
port = {port}
id = {id}
method = {method}
timeout = {timeout}
token = {token}
device_id = {device_id}
http_port = {http_port}
'''

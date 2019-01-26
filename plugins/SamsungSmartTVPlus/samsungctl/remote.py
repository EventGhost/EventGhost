
import logging
import six

from .remote_legacy import RemoteLegacy
from .remote_websocket import RemoteWebsocket
from .remote_encrypted import RemoteWebsocketEncrypted
from .config import Config
from . import exceptions

logger = logging.getLogger('samsungctl')


class RemoteInstanceSingleton(type):
    _objects = {}

    def __call__(cls, config, *args):

        if isinstance(config, dict):
            config = Config(**config)

        key = str(config)

        if key not in RemoteInstanceSingleton._objects:
            instance = (
                super(RemoteInstanceSingleton, cls).__call__(config, *args)
            )

            RemoteInstanceSingleton._objects[key] = instance

        return RemoteInstanceSingleton._objects[key]


@six.add_metaclass(RemoteInstanceSingleton)
class Remote(object):

    def __init__(self, config, log_level=logging.NOTSET, upnp_tv=None):
        self.config = config
        logger.setLevel(log_level)

        if config.id is None:
            from uuid import uuid4
            config.id = str(uuid4())[1:-1]

        if config.device_id is None:
            from uuid import uuid4
            config.id = str(uuid4())[1:-1]
        elif upnp_tv is None:
            from .discover import discover
            tvs = list(discover(config, log_level))
            if tvs:
                upnp_tv = tvs[0]

        if upnp_tv is None:
            logger.warning('UPNP disabled')

            if config.port not in (55000, 8000, 8001, 8002):
                if config.token is not None:
                    if config.token.isdigit():
                        config.method = 'websocket_encrypted'
                    elif config.token:
                        config.method = 'websocket_ssl'
                    else:
                        config.method = 'websocket'
                else:
                    config.method = 'legacy'

        else:
            if upnp_tv.new_gen:
                if upnp_tv.token_auth_support is True:
                    config.method = 'websocket_ssl'
                else:
                    config.method = 'websocket'

            elif upnp_tv.year in (2014, 2015):
                config.method = 'websocket_encrypted'
            else:
                config.method = 'legacy'

        if config.method == 'websocket':
            config.port = 8001
            config.http = 8001
            self._remote = RemoteWebsocket(config)
        elif config.method == 'websocket_ssl':
            config.port = 8002
            config.http_port = 8001
            self._remote = RemoteWebsocket(config)
        elif config.method == 'websocket_encrypted':
            config.port = 8000
            config.http_port = 8080
            self._remote = RemoteWebsocketEncrypted(config)
        elif config.method == 'legacy':
            config.port = 55000
            config.http_port = None
            self._remote = RemoteLegacy(config)
        else:
            if upnp_tv is None:
                raise exceptions.NoTVFound

            elif config.host:
                raise exceptions.ConfigUnknownMethod

            else:
                raise RuntimeError('Unknown Error')

        self.upnp_tv = upnp_tv

    def __enter__(self):
        return self._remote.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._remote.__exit__(exc_type, exc_val, exc_tb)

    def open(self):
        self._remote.open()

    def close(self):
        return self._remote.close()

    def send(self, cmd):
        self._remote.send(cmd)

    def control(self, key):
        return self._remote.control(key)

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        if self.upnp_tv is not None:
            return getattr(self.upnp_tv, item)

    def __setattr__(self, key, value):
        if key in ('_remote', 'upnp_tv', 'config'):
            self.__dict__[key] = value
        else:
            if self.upnp_tv is not None:
                setattr(self.upnp_tv, key, value)



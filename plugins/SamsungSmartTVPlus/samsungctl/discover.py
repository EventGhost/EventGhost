# -*- coding: utf-8 -*-
import logging
import threading
import socket

from .config import Config
from .remote import Remote


def discover(config=None, log_level=logging.NOTSET):
    import requests
    from lxml import etree
    from .upnp.UPNP_Device.discover import discover as _discover
    from .upnp.UPNP_Device.discover import get_upnp_classes
    from .upnp.UPNP_Device.xmlns import strip_xmlns
    from.upnp import UPNPTV

    found_event = threading.Event()
    found = []
    threads = []

    def do(addr):
        locations = get_upnp_classes(addr, 8, log_level)
        if locations:
            location = locations[0]
            response = requests.get(location)
            root = etree.fromstring(response.content)

            root = strip_xmlns(root)

            device = root.find('device')
            friendly_name = device.find('friendlyName').text
            mfgr = device.find('manufacturer').text
            if (
                mfgr == 'Samsung Electronics' and
                friendly_name.startswith('[TV]')
            ):
                found.append(UPNPTV(addr, locations))
                found_event.set()

        if threading.current_thread() in threads:
            threads.remove(threading.current_thread())

    if config is None:
        for address in _discover(8, log_level):
            t = threading.Thread(target=do, args=(address,))
            t.daemon = True
            threads += [t]
            t.start()

        while threads:
            found_event.wait()
            found_event.clear()
            while found:
                tv = found.pop(0)
                host_name = socket.gethostname()
                host = tv.ip_address
                device_id = tv.device_id
                name = tv.__name__ + ':' + device_id
                id = host_name + ':' + device_id
                config = Config(
                    host=host,
                    name=name,
                    device_id=device_id,
                    id=id,
                )

                yield Remote(config, log_level, tv)

    if isinstance(config, Config):
        if config.device_id is not None:
            for address in _discover(8, log_level):
                t = threading.Thread(target=do, args=(address,))
                t.daemon = True
                threads += [t]
                t.start()

            while threads:
                found_event.wait()
                found_event.clear()
                while found:
                    tv = found.pop(0)
                    if tv.device_id == config.device_id:
                        config.host = tv.ip_address
                        yield Remote(config, log_level, tv)
                        raise StopIteration

        elif config.host is not None:
            do(config.host)
            if found:
                tv = found[0]
                config.device_id = tv.device_id
                yield Remote(config, log_level, tv)

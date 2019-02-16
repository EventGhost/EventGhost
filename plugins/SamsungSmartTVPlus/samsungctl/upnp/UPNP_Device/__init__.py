# -*- coding: utf-8 -*-
"""UPNP device mapping tool"""


import logging
import threading
from logging import NullHandler

logger = logging.getLogger('UPNP_Devices')
logger.addHandler(NullHandler())
logging.basicConfig(format="%(message)s", level=None)

logger.setLevel(logging.NOTSET)


def discover(ip=None, log_level=logging.NOTSET):
    from .discover import discover as _discover
    from .discover import get_upnp_classes
    from .xmlns import strip_xmlns
    from .upnp_class import UPNPObject  # NOQA

    found_event = threading.Event()
    found = []
    threads = []

    def do(addr):
        locations = get_upnp_classes(addr, 8, log_level)
        found.append(UPNPObject(addr, locations))
        found_event.set()

        if threading.current_thread() in threads:
            threads.remove(threading.current_thread())

    if ip is None:
        for address in _discover(8, log_level):
            t = threading.Thread(target=do, args=(address,))
            t.daemon = True
            threads += [t]
            t.start()

        while threads:
            found_event.wait()
            found_event.clear()
            while found:
                yield found.pop(0)

    else:
        do(ip)
        if found:
            yield found[0]


__title__ = "UPNP_Device"
__version__ = "0.1.0b"
__url__ = "https://github.com/kdschlosser/UPNP_Device"
__author__ = "Kevin Schlosser"
__author_email__ = "kevin.g.schlosser@gmail.com"
__all__ = (
    '__title__', '__version__', '__url__', '__author__', '__author_email__',
    'discover'
)


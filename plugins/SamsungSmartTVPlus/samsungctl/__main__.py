import argparse
import socket

import sys
import os

from . import __doc__ as doc
from . import __title__ as title
from . import __version__ as version
from . import exceptions
from . import Remote

import logging
from logging import NullHandler

logger = logging.getLogger('samsungctl')
logger.addHandler(NullHandler())
logging.basicConfig(format="%(message)s", level=logging.NOTSET)


def main():
    epilog = "E.g. %(prog)s --host 192.168.0.10 --name myremote KEY_VOLDOWN"
    parser = argparse.ArgumentParser(prog=title, description=doc,
                                     epilog=epilog)
    parser.add_argument("--version", action="version",
                        version="%(prog)s {0}".format(version))
    parser.add_argument("-v", "--verbose", action="count",
                        help="increase output verbosity")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="suppress non-fatal output")
    parser.add_argument("-i", "--interactive", action="store_true",
                        help="interactive control")
    parser.add_argument("--host", help="TV hostname or IP address")
    parser.add_argument("--port", type=int, help="TV port number (TCP)")
    parser.add_argument("--method",
                        help="Connection method (legacy or websocket)")
    parser.add_argument("--name", help="remote control name")
    parser.add_argument("--description", metavar="DESC",
                        help="remote control description")
    parser.add_argument("--id", help="remote control id")
    parser.add_argument("--timeout", type=float,
                        help="socket timeout in seconds (0 = no timeout)")
    parser.add_argument("key", nargs="*",
                        help="keys to be sent (e.g. KEY_VOLDOWN)")

    args = parser.parse_args()

    if args.quiet:
        log_level = logging.ERROR
    elif not args.verbose:
        log_level = logging.WARNING
    elif args.verbose == 1:
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    config = {}
    config.update({k: v for k, v in vars(args).items() if v is not None})

    try:
        with Remote(log_level=log_level, **config) as remote:
            for key in args.key:
                remote.control(key)

            if args.interactive:
                logging.getLogger().setLevel(logging.ERROR)
                from . import interactive
                interactive.run(remote)
            elif len(args.key) == 0:
                logging.warning("Warning: No keys specified.")
    except exceptions.ConnectionClosed:
        logging.error("Error: Connection closed!")
    except exceptions.AccessDenied:
        logging.error("Error: Access denied!")
    except exceptions.UnknownMethod:
        logging.error("Error: Unknown method '{}'".format(config["method"]))
    except socket.timeout:
        logging.error("Error: Timed out!")
    except OSError as e:
        logging.error("Error: %s", e.strerror)


if __name__ == "__main__":
    main()

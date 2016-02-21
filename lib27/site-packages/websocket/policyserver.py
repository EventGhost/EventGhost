from gevent.server import StreamServer

__all__ = ['FlashPolicyServer']


class FlashPolicyServer(StreamServer):
    policy = """<?xml version="1.0"?><!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
<cross-domain-policy><allow-access-from domain="*" to-ports="*"/></cross-domain-policy>"""

    noisy = False

    def __init__(self, listener=None, backlog=None, noisy=None):
        if listener is None:
            listener = ('0.0.0.0', 843)
        if noisy is not None:
            self.noisy = noisy
        StreamServer.__init__(self, listener=listener, backlog=backlog)

    def handle(self, socket, address):
        if self.noisy:
            print 'Accepted connection from %s:%s' % address
        socket.sendall(self.policy)

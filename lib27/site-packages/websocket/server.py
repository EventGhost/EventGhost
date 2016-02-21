import sys
import traceback
from os.path import abspath, dirname, join, basename
from socket import error
from hashlib import md5
from datetime import datetime
from gevent.pywsgi import WSGIHandler, WSGIServer

from websocket.policyserver import FlashPolicyServer
from websocket import WebSocket

import gevent
assert gevent.version_info >= (0, 13, 2), 'Newer version of gevent is required to run websocket.server'

__all__ = ['WebsocketHandler', 'WebsocketServer']


class WebsocketHandler(WSGIHandler):

    def run_application(self):
        path = self.environ.get('PATH_INFO')
        content_type = self.server.data_handlers.get(path)
        if content_type is not None:
            self.serve_file(basename(path), content_type)
            return

        websocket_mode = False

        if WebSocket.is_socket(self.environ):
            self.status = 'websocket'
            self.log_request()
            self.environ['websocket'] = WebSocket(self.environ, self.socket, self.rfile)
            websocket_mode = True
        try:
            self.result = self.application(self.environ, self.start_response)
            if self.result is not None:
                self.process_result()
        except:
            websocket = self.environ.get('websocket')
            if websocket is not None:
                websocket.close()
            raise
        finally:
            if websocket_mode:
                # we own the socket now, make sure pywsgi does not try to read from it:
                self.socket = None

    def serve_file(self, filename, content_type):
        from websocket import data
        path = join(dirname(abspath(data.__file__)), filename)
        if self.server.etags.get(path) == (self.environ.get('HTTP_IF_NONE_MATCH') or 'x'):
            self.start_response('304 Not Modifed', [])
            self.write('')
            return
        try:
            body = open(path).read()
        except IOError, ex:
            sys.stderr.write('Cannot open %s: %s\n' % (path, ex))
            self.start_response('404 Not Found', [])
            self.write('')
            return
        etag = md5(body).hexdigest()
        self.server.etags[path] = etag
        self.start_response('200 OK', [('Content-Type', content_type),
                                       ('Content-Length', str(len(body))),
                                       ('Etag', etag)])
        self.write(body)


class WebsocketServer(WSGIServer):

    handler_class = WebsocketHandler
    data_handlers = {
        '/websocket/WebSocketMain.swf': 'application/x-shockwave-flash',
        '/websocket/flashsocket.js': 'text/javascript'
    }
    etags = {}

    def __init__(self, listener, application=None, policy_server=True, backlog=None,
                 spawn='default', log='default', handler_class=None, environ=None, **ssl_args):
        if policy_server is True:
            self.policy_server = FlashPolicyServer()
        elif isinstance(policy_server, tuple):
            self.policy_server = FlashPolicyServer(policy_server)
        elif policy_server:
            raise TypeError('Expected tuple or boolean: %r' % (policy_server, ))
        else:
            self.policy_server = None
        super(WebsocketServer, self).__init__(listener, application, backlog=backlog, spawn=spawn, log=log,
                                              handler_class=handler_class, environ=environ, **ssl_args)

    def start_accepting(self):
        self._start_policy_server()
        super(WebsocketServer, self).start_accepting()
        self.log_message('%s accepting connections on %s', self.__class__.__name__, _format_address(self))

    def _start_policy_server(self):
        server = self.policy_server
        if server is not None:
            try:
                server.start()
                self.log_message('%s accepting connections on %s', server.__class__.__name__, _format_address(server))
            except error, ex:
                sys.stderr.write('FAILED to start %s on %s: %s\n' % (server.__class__.__name__, _format_address(server), ex))
            except Exception:
                traceback.print_exc()
                sys.stderr.write('FAILED to start %s on %s\n' % (server.__class__.__name__, _format_address(server)))

    def kill(self):
        if self.policy_server is not None:
            self.policy_server.kill()
        super(WebsocketServer, self).kill()

    def log_message(self, message, *args):
        log = self.log
        if log is not None:
            try:
                message = message % args
            except Exception:
                traceback.print_exc()
                try:
                    message = '%r %r' % (message, args)
                except Exception:
                    traceback.print_exc()
            log.write('%s %s\n' % (datetime.now().replace(microsecond=0), message))


def _format_address(server):
    try:
        if server.server_host == '0.0.0.0':
            return ':%s' % server.server_port
        return '%s:%s' % (server.server_host, server.server_port)
    except Exception:
        traceback.print_exc()

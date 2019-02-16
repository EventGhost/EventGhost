
import threading
import socket
import traceback
import sys
import atexit

eg = None


class SocketException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class SocketDataError(SocketException):
    pass


class SocketCommandError(SocketException):
    pass


class SocketConnectionError(SocketException):

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        return self.msg[item]


def shutdown():
    import wx
    wx.CallAfter(eg.app.Exit)

    return True


def process_data(command):
    try:
        command, data = command.split(',', 1)
    except ValueError:
        data = '()'

    eg.PrintDebugNotice('Command: {0}, Parameters: {1}'.format(command, data))
    command = command.strip()
    data = data.strip()

    try:
        if '=' in command:
            raise SocketCommandError('Command not allowed: ' + command)

        if (
            (not data.startswith('dict') and '=' in data) or
            (data[0] not in ('(', '[', '{') and not data.startswith('dict'))
        ):
            raise SocketDataError('Data not allowed: ' + data)

        try:
            command = eval(command.split('(', 1)[0])
            if isinstance(command, (str, unicode)):
                raise SocketCommandError('Command does not exist: ' + command)
        except (SyntaxError, NameError):
            raise SocketDataError('Command malformed: ' + command)
        try:
            data = eval(data)
        except SyntaxError:
            raise SocketDataError('Data malformed: ' + str(data))

        if not isinstance(data, (dict, list, tuple)):
            raise SocketDataError('Data malformed: ' + str(data))

    except SocketException:
        eg.PrintDebugNotice(traceback.format_exc())

    else:
        try:
            if isinstance(data, dict):
                return command(**data)
            elif isinstance(data, (tuple, list)):
                return command(*data)
        except:
            eg.PrintDebugNotice(traceback.format_exc())
            return None


def send_message(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(2.0)
    try:
        sys.stderr._displayMessage = False
    except AttributeError:
        pass
    sys.stderr.write('New Instance: send message ' + repr(message) + '\n')
    res = None

    try:
        sock.connect(('127.0.0.1', 38765))
        data = ''
        while '\r' not in data:
            data += sock.recv(4096)

        data = data[:data.find('\r')]
        if data == '?':
            sock.sendall(str(message) + '\r')
            data = ''

            while '\r' not in data:
                data += sock.recv(4096)

            response = data[:data.find('\r')]
            sys.stderr.write('New Instance: response ' + repr(response) + '\n')
            sock.sendall('closecon\r')

            try:
                res = eval(response)
            except:
                res = response

    except socket.timeout:
        pass
    except socket.error:
        pass

    _close_sock(sock)
    return res


def _close_sock(sock):
    try:
        sock.shutdown(socket.SHUT_RDWR)
    except AttributeError:
        return
    except socket.error:
        pass

    try:
        sock.close()
    except socket.error:
        pass


def is_eg_running():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(2.0)
    try:
        sock.connect(('127.0.0.1', 38765))
        data = ''
        while '\r' not in data:
            data += sock.recv(4096)
        data = data[:data.find('\r')]
        if data == '?':
            sock.sendall('testcon\r')
            res = True
        else:
            res = None

    except socket.timeout:
        res = None
    except socket.error:
        res = False

    _close_sock(sock)
    return res


class Client(threading.Thread):

    def __init__(self, handler, ip, sock, id):
        self.timeout_clicks = 0
        self.id = id
        self.rsa_key = None
        self.handler = handler
        self.ip = ip
        self.sock = sock
        self.event = threading.Event()
        threading.Thread.__init__(
            self,
            name='Socket Client: {0}:{1}'.format(ip, id)
        )
        eg.PrintDebugNotice('new client')

    def run(self):
        try:
            self.sock.settimeout(1)
            data = ''
            self.sock.sendall('?\r')
        except socket.error:
            pass

        else:
            while not self.event.isSet():
                try:
                    while '\r' not in data:
                        data += self.sock.recv(4096)

                    index = data.find('\r')

                    command = data[:index]
                    data = data[index + 1:]

                    if not self.event.isSet():
                        eg.PrintDebugNotice(' ---> EG - ' + repr(command))

                        if command in ('testcon', 'closecon'):
                            self.event.set()
                        else:
                            self.Send(process_data(command))
                except socket.timeout():
                    self.timeout_clicks += 1
                    if self.timeout_clicks == 600 or self.event.isSet():
                        self.Send('closecon')
                        self.event.set()

                except socket.error:
                    self.event.set()

            eg.PrintDebugNotice('connection closed')

        _close_sock(self.sock)
        self.sock = None

    def Send(self, message):
        eg.PrintDebugNotice('<---- EG - ' + repr(message))
        self.sock.sendall(str(message) + '\r')

    def Start(self):
        self.start()

    def Stop(self):
        self.event.set()


class Server(threading.Thread):

    def __init__(self):
        self.unauth_count = 0
        self.sock = None
        self.threads = []
        self.error_count = 0
        self.conn_count = 0
        self.event = threading.Event()
        threading.Thread.__init__(self, name='Socket Server')

    def run(self):
        atexit.register(self.Stop)

        def start_sock():
            try:
                eg.PrintDebugNotice('starting...')
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(('127.0.0.1', 38765))
                # SOMAXCONN = 2147483647
                s.listen(socket.SOMAXCONN)
                s.settimeout(1)
                eg.PrintDebugNotice('started.')
                return s
            except socket.error:
                eg.PrintDebugNotice('startup failed.')
                eg.PrintDebugNotice(traceback.format_exc())
                return None

        def restart_sock():
            self.error_count += 1

            if self.error_count > 2:
                self.end_threads()
                _close_sock(self.sock)

                self.event.wait(self.error_count)

                return start_sock()
            return self.sock

        self.sock = sock = start_sock()

        if sock is not None:
            while not self.event.isSet():
                try:
                    conn, addr = sock.accept()
                    if self.event.isSet():
                        _close_sock(conn)
                    else:
                        self.conn_count += 1
                        t = Client(self, addr[0], conn, self.conn_count)
                        t.start()
                        self.threads.append(t)
                        self.threads = list(t for t in self.threads if t.isAlive())
                        self.error_count = 0
                except socket.timeout:
                    pass

                except socket.error:
                    tb = traceback.format_exc().split('\n')
                    tb = '    ' + '\n    '.join(tb)
                    eg.PrintDebugNotice('connection error')
                    eg.PrintDebugNotice(tb)

                    if not self.event.isSet():
                        self.sock = sock = restart_sock()
                        while not self.event.isSet() and self.sock is None:
                            self.sock = sock = restart_sock()

            eg.PrintDebugNotice('stopping...')
            self.end_threads()
            _close_sock(self.sock)
            eg.PrintDebugNotice('stopped.')

    def Send(self, message):
        self.threads = list(t for t in self.threads if t.isAlive())
        for t in self.threads:
            t.Send(message)

    def Start(self):
        global eg
        eg = __import__('eg')
        self.start()
        return self

    def end_threads(self):
        while self.threads:
            t = self.threads.pop(0)
            if t.isAlive():
                t.Stop()
                self.threads += [t]

    def Stop(self):
        if not self.event.isSet():
            self.event.set()
            self.join(2.0)


def Start():
    server = Server()
    return server.Start()

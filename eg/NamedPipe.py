# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

# changelog
# 18-12-2017: 23:07 -7:00   K
# Adds multiple pipe connection support.


import win32security
import win32pipe
import win32file
import threading
import wx
import traceback
import random


PIPE_ACCESS_OUTBOUND = 0x00000002
PIPE_ACCESS_DUPLEX = 0x00000003
PIPE_ACCESS_INBOUND = 0x00000001

PIPE_WAIT = 0x00000000
PIPE_NOWAIT = 0x00000001

PIPE_READMODE_BYTE = 0x00000000
PIPE_READMODE_MESSAGE = 0x00000002
PIPE_TYPE_BYTE = 0x00000000
PIPE_TYPE_MESSAGE = 0x00000004

PIPE_CLIENT_END = 0x00000000
PIPE_SERVER_END = 0x00000001

FILE_FLAG_OVERLAPPED = 0x40000000
FILE_ATTRIBUTE_NORMAL = 0x00000080
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002

PIPE_UNLIMITED_INSTANCES = 0xFF

NMPWAIT_WAIT_FOREVER = 0xFFFFFFFF
NMPWAIT_NOWAIT = 0x00000001
NMPWAIT_USE_DEFAULT_WAIT = 0x00000000

GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
GENERIC_EXECUTE = 0x20000000
GENERIC_ALL = 0x10000000

FILE_FLAG_FIRST_PIPE_INSTANCE = 0x00080000

ERROR_PIPE_CONNECTED = 0x217
ERROR_PIPE_LISTENING = 0x218
ERROR_BROKEN_PIPE = 0x6D
ERROR_PIPE_LOCAL = 0xE5
ERROR_BAD_PIPE = 0xE6
ERROR_PIPE_BUSY = 0xE7
ERROR_NO_DATA = 0xE8
ERROR_PIPE_NOT_CONNECTED = 0xE9
ERROR_FILE_NOT_FOUND = 0x2


class NamedPipeException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class NamedPipeDataError(NamedPipeException):
    pass


class NamedPipeCommandError(NamedPipeException):
    pass


class NamedPipeConnectionError(NamedPipeException):

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]

        return self.msg[item]


def process_data(in_data):
    """
    Strips 0x0 bytes from incoming data.

    :param in_data: data received from the named pipe
    :type in_data: str
    :return: Corrected data from the named pipe
    :rtype: str
    """
    out_data = ''
    for char in in_data:
        if ord(char) != 0:
            out_data += char
    return out_data


def _is_eg_running():
    try:
        win32pipe.WaitNamedPipe(
            r'\\.\pipe\eventghost',
            NMPWAIT_USE_DEFAULT_WAIT
        )
        return True

    except win32pipe.error as err:
        if err[0] == ERROR_FILE_NOT_FOUND:
            return False
        raise NamedPipeConnectionError(err)


is_eg_running = _is_eg_running()


class Pipe(object):
    """
    Thread class for handling additional pipe connections.
    """

    def __init__(self, parent, pipe_id, security_attributes):
        """

        :param parent: Server class
        :type parent: instance
        :param pipe_id: ID assigned to this pipe instance.
        :type pipe_id: int
        :param security_attributes: Windows SACL and DACL data for creating the
            pipe.
        :type security_attributes: win32security.SECURITY_ATTRIBUTES instance
        """
        self._parent = parent
        self._pipe_id = pipe_id
        self.is_waiting = True
        self._thread = threading.Thread(
            name='EventGhost.Pipe.{0}.Thread'.format(pipe_id),
            target=self.run,
            args=(security_attributes,)
        )
        self._thread.daemon = True
        self._thread.start()

    def run(self, security_attributes):
        """
        Handles the creation of the pipe.


        Windows SACL and DACL data for creating the
            pipe.
        :type security_attributes: win32security.SECURITY_ATTRIBUTES instance
        :return: None
        :rtype: None
        """
        import eg

        eg.PrintDebugNotice(
            'Named Pipe: Creating pipe {0}'.format(self._pipe_id)
        )

        pipe = win32pipe.CreateNamedPipe(
            r'\\.\pipe\eventghost',
            PIPE_ACCESS_DUPLEX,
            PIPE_TYPE_MESSAGE | PIPE_WAIT | PIPE_READMODE_MESSAGE,
            PIPE_UNLIMITED_INSTANCES,
            4096,
            4096,
            5,
            security_attributes
        )

        win32pipe.ConnectNamedPipe(pipe, None)
        data = win32file.ReadFile(pipe, 4096)
        self.is_waiting = False

        if not self._parent.running_pipes[-1].is_waiting == self:
            self._parent.running_pipes += [
                Pipe(
                    self._parent,
                    self._parent.get_pipe_id(),
                    security_attributes
                )
            ]

        eg.PrintDebugNotice('Pipe {0}: Data received'.format(self._pipe_id))

        if data[0] == 0:
            event = threading.Event()
            res = ['']

            self._parent.process_command.add(
                self._pipe_id,
                data[1],
                res,
                event
            )

            while not event.isSet():
                pass

            win32file.WriteFile(pipe, str(repr(res[0])))
            win32pipe.DisconnectNamedPipe(pipe)
            win32file.CloseHandle(pipe)
        else:
            try:
                raise NamedPipeDataError(
                    'Pipe {0}: Unknown Error: {1}'.format(
                        self._pipe_id,
                        str(data)
                    )
                )
            except NamedPipeDataError:
                traceback.print_exc()
        self._parent.running_pipes.remove(self)


class ProcessCommand(object):
    """
    Incoming pipe command processor.
    """

    def __init__(self):
        self._thread = threading.Thread(target=self.run)
        self._thread.daemon = True
        self._queue = []
        self._running_id = 0
        self._thread.start()
        self._queue_event = threading.Event()

    def add(self, pipe_id, data, res, event):
        """
        Adds new data to the queue to be processed.

        :param pipe_id: ID of the pipe instance sending in the data to be
            processed.
        :type pipe_id: int
        :param data: Data to be processed.
        :type data: str
        :param res: Container to hold any return data.
        :type res: list
        :param event: vent that gets set when processing has finished. This
            lets the pipe instance know when to send return data back.
        :type event: threading.Event instance
        :return: None
        :rtype: None
        """
        self._queue += [(pipe_id, data, res, event)]
        self._queue_event.set()

    def run(self):
        """
        Processes the queued data.

        :return: None
        :rtype: None
        """
        import eg

        while True:
            self._queue_event.wait()
            self._queue_event.clear()
            while self._queue:
                pipe_id, data, res, event = self._queue.pop(0)
                if pipe_id != self._running_id:
                    self._queue += [(pipe_id, data, res, event)]
                    continue

                command = process_data(data)
                try:
                    command, data = command.split(',', 1)
                except ValueError:
                    data = '()'

                eg.PrintDebugNotice(
                    'Pipe {0}: Command: {1}, Parameters: {2}'.format(
                        pipe_id,
                        command,
                        data
                    )
                )

                command = command.strip()
                data = data.strip()

                try:
                    if '=' in command:
                        raise NamedPipeCommandError(
                            'Pipe {0}: Command not allowed: {1}'.format(
                                pipe_id,
                                command
                            )
                        )

                    if not data.startswith('dict') and '=' in data:
                        raise NamedPipeDataError(
                            'Pipe {0}: Data not allowed: {1}'.format(
                                pipe_id,
                                data
                            )
                        )

                    if (
                        data[0] not in ('(', '[', '{') and
                        not data.startswith('dict')
                    ):
                        raise NamedPipeDataError(
                            'Pipe {0}: Data not allowed: {1}'.format(
                                pipe_id,
                                data
                            )
                        )

                    try:
                        command = eval(command.split('(', 1)[0])
                    except SyntaxError:
                        raise NamedPipeDataError(
                            'Pipe {0}: Command malformed: {1}'.format(
                                pipe_id,
                                command
                            )
                        )
                    else:
                        if isinstance(command, (str, unicode)):
                            raise NamedPipeCommandError(
                                'Pipe {0}: Command does not exist: {1}'.format(
                                    pipe_id,
                                    command
                                )
                            )
                    try:
                        data = eval(data)
                    except SyntaxError:
                        raise NamedPipeDataError(
                            'Pipe {0}: Data malformed: {1}'.format(
                                pipe_id,
                                data
                            )
                        )

                    if not isinstance(data, (dict, list, tuple)):
                        raise NamedPipeDataError(
                            'Pipe {0}: Data malformed: {1}'.format(
                                pipe_id,
                                str(data)
                            )
                        )

                except NamedPipeException:
                    traceback.print_exc()
                    event.set()
                else:
                    def run():
                        if isinstance(data, dict):
                            res[0] = command(**data)
                        elif isinstance(data, (tuple, list)):
                            res[0] = command(*data)

                        eg.PrintDebugNotice(
                            'Pipe {0}: Return data: {1}'.format(
                                pipe_id,
                                str(res[0])
                            )
                        )

                        event.set()

                    wx.CallAfter(run)
                    event.wait()
                self._running_id = pipe_id + 1


class Server:
    """
    Receiving thread class for the "\\.\pipe\eventghost" named pipe.

    When EventGhost gets run a named pipe gets created by the name of
    "\\.\pipe\eventghost". The pipe is created so that everyone has full
    control. This allows for an instance of EventGhost to be running as
    Administrator and be able to send commands into EventGhost as a user.

    EventGhost command line arguments have been changed to use
    this pipe and has opened up the ability to be able to do things like hide
    the current running instance from the command line. It has also
    significantly increased the speed in which the operations are carried out.

    This has been added in a way that will allow for another application that
    is running on the same computer as EventGhost to be able to make
    EventGhost perform various tasks. The API is as follows.

    all data written to the pipe has be done as a string. this is a message
    only pipe and you are not able to send any byte data through it. It is also
    one way communications. the running instance of EventGhost will never
    write anything to the pipe. the structure of the message is

    function/class/method name, *args or **kwargs

    you are only able to make a call to an existing function/class/method you
    are not able to set a attributes value directly. you will have to create a
    function and then you can have data passed to that function via the named
    pipe and have the function then set the attributes value.

    the args either have to be a list or a tuple empty if there are no
    parameters to be sent.

    kwargs can either be formatted as
    dict(keyword1=None, keyword2=None)
    or
    {'keyword1': None, 'keyword2': None}

    any public class/method/function can be accessed by use of this pipe.

    when a command is received it passes the command to the main thread to be
    evaluated for correctness and to be run. The reason this is done is 2 fold
    It is so that the named pipe can be created once again as fast as possible
    without having to wait for the command to finish executing. But also if a
    command is used that deals with the GUI aspects of EG a lot of the wx
    components need to be ran from the main thread.

    """

    def __init__(self):
        self._thread = None
        self.running_pipes = []
        self._id_lock = threading.Lock()
        self._pipe_id = -1
        self.is_waiting = True
        self.process_command = None

    def start(self):
        if self._thread is None:
            self.process_command = ProcessCommand()

            self._thread = threading.Thread(
                name='EventGhost.Pipe.0.Thread',
                target=self.run
            )
            self._thread.daemon = True
            self._thread.start()

    def ping(self):
        return 'pong'

    def get_pipe_id(self):
        self._id_lock.acquire()
        self._pipe_id += 1
        try:
            return self._pipe_id
        finally:
            self._id_lock.release()

    def run(self):

        import eg

        # This is where the permissions get created for the pipe
        eg.PrintDebugNotice('Pipe: Creating security descriptor')
        security_attributes = win32security.SECURITY_ATTRIBUTES()
        security_descriptor = win32security.SECURITY_DESCRIPTOR()
        security_descriptor.SetSecurityDescriptorDacl(1, None, 0)
        security_attributes.SECURITY_DESCRIPTOR = security_descriptor
        eg.PrintDebugNotice('Pipe 0: Creating Pipe')

        pipe = win32pipe.CreateNamedPipe(
            r'\\.\pipe\eventghost',
            PIPE_ACCESS_DUPLEX | FILE_FLAG_FIRST_PIPE_INSTANCE,
            PIPE_TYPE_MESSAGE | PIPE_WAIT | PIPE_READMODE_MESSAGE,
            PIPE_UNLIMITED_INSTANCES,
            4096,
            4096,
            5,
            security_attributes
        )

        while True:
            self.is_waiting = True
            pipe_id = self.get_pipe_id()

            # creation of the pipe. once the pipe has been made it will sit
            # and wait for data to be written to the pipe. once data has been
            # written it will then read the data and close the pipe. then it
            # will parse the data sent and execute the command. It will loop
            # like this the entire time EG is running. The thread that handles
            # the pipe is a daemon thread and the thread will be terminated
            # when EG closes.

            win32pipe.ConnectNamedPipe(pipe, None)

            self.running_pipes += [self]

            if len(self.running_pipes) > 1:
                if not self.running_pipes[-1].is_waiting:
                    self.running_pipes += [
                        Pipe(self, self.get_pipe_id(), security_attributes)
                    ]
            else:
                self.running_pipes += [
                    Pipe(self, self.get_pipe_id(), security_attributes)
                ]

            data = win32file.ReadFile(pipe, 4096)
            self.is_waiting = False

            eg.PrintDebugNotice('Pipe {0}: Data received'.format(pipe_id))

            if data[0] == 0:
                event = threading.Event()
                res = ['']

                self.process_command.add(
                    pipe_id,
                    data[1],
                    res,
                    event
                )

                while not event.isSet():
                    pass

                win32file.WriteFile(pipe, str(repr(res[0])))
                win32pipe.DisconnectNamedPipe(pipe)

            else:
                try:
                    raise NamedPipeDataError(
                        'Pipe {0}: Unknown Error: {1}'.format(
                            pipe_id,
                            str(data)
                        )
                    )
                except NamedPipeDataError:
                    traceback.print_exc()
            self.running_pipes.remove(self)


def send_message(msg):
    try:
        pipe = win32file.CreateFile(
            r'\\.\pipe\eventghost',
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )
        win32file.WriteFile(pipe, msg)
        # while not win32pipe.PeekNamedPipe(pipe, 4096):
        #     pass
        data = win32file.ReadFile(pipe, 4096)
        if data[0] == 0:
            data = process_data(data[1])
            if data != '':
                try:
                    return eval(data)
                except SyntaxError:
                    return data
            else:
                return data
        else:
            raise NamedPipeDataError('Error in data received: ' + str(data))

    except win32pipe.error as err:
        if err[0] in (ERROR_PIPE_BUSY, ERROR_PIPE_CONNECTED):
            event = threading.Event()
            event.wait(float(random.randrange(1, 100)) / 2000.0)
            return send_message(msg)

        raise NamedPipeConnectionError(err)

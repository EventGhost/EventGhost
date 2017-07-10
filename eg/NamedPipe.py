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

import win32security
import win32pipe
import win32file
import threading
import wx


def process_data(in_data):
    out_data = ''
    for char in in_data:
        if ord(char) != 0:
            out_data += char
    return out_data


class Server:
    """
    Receiving thread class for the eventghost named pipe.

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

    def start(self):
        if self._thread is None:
            self._thread = threading.Thread(
                name='EventGhost.Pipe.Thread',
                target=self.run
            )
            self._thread.daemon = True
            self._thread.start()

    def ping(self):
        return 'pong'

    def run(self):
        import eg
        # This is where the permissions get created for the pipe
        eg.PrintDebugNotice('Named Pipe: Creating security descriptor')
        security_attributes = win32security.SECURITY_ATTRIBUTES()
        security_descriptor = win32security.SECURITY_DESCRIPTOR()
        security_descriptor.SetSecurityDescriptorDacl(1, None, 0)
        security_attributes.SECURITY_DESCRIPTOR = security_descriptor

        while True:

            # creation of the pipe. once the pipe has been made it will sit
            # and wait for data to be written to the pipe. once data has been
            # written it will then read the data and close the pipe. then it
            # will parse the data sent and execute the command. It will loop
            # like this the entire time EG is running. The thread that handles
            # the pipe is a daemon thread and the thread will be terminated
            # when EG closes.
            eg.PrintDebugNotice('Named Pipe: Creating pipe')
            pipe = win32pipe.CreateNamedPipe(
                r'\\.\pipe\eventghost',
                (
                    win32pipe.PIPE_ACCESS_DUPLEX |
                    win32file.GENERIC_READ |
                    win32file.GENERIC_WRITE
                ),
                (
                    win32pipe.PIPE_TYPE_MESSAGE |
                    win32pipe.PIPE_WAIT |
                    win32pipe.PIPE_READMODE_MESSAGE
                ),
                255,
                4096,
                4096,
                50,
                security_attributes
            )
            win32pipe.ConnectNamedPipe(pipe, None)
            data = win32file.ReadFile(pipe, 4096)
            eg.PrintDebugNotice('Named Pipe: Data received')

            if data[0] == 0:
                event = threading.Event()
                res = ['']

                def run_command(d):

                    command = process_data(d)
                    try:
                        command, d = command.split(',', 1)
                    except ValueError:
                        d = '()'

                    eg.PrintDebugNotice(
                        'Named Pipe: Command: %s, Parameters: %s' %
                        (command, d)
                    )

                    command = command.strip()
                    d = d.strip()

                    if '=' in command:
                        eg.PrintError(
                            'Named Pipe Error: '
                            'Command not allowed: ' + command
                        )
                        command = None

                    if not d.startswith('dict') and '=' in d:
                        eg.PrintError(
                            'Named Pipe Error: '
                            'Data not allowed: ' + d
                        )
                        command = None

                    if (
                                d[0] not in ('(', '[', '{') and
                            not d.startswith('dict')
                    ):
                        eg.PrintError(
                            'Named Pipe Error: '
                            'Data not allowed: ' + d
                        )
                        command = None

                    try:
                        command = eval(command.split('(', 1)[0])
                    except SyntaxError:
                        eg.PrintTraceback(
                            'Named Pipe Error: '
                            'Command malformed: ' + command
                        )
                        command = None
                    else:
                        if isinstance(command, (str, unicode)):
                            eg.PrintError(
                                'Named Pipe Error: '
                                'Command does not exist: ' + command
                            )
                            command = None
                    try:
                        d = eval(d.strip())
                    except SyntaxError:
                        eg.PrintError(
                            'Named Pipe Error: '
                            'Data malformed: ' + d
                        )
                        command = None

                    if command is not None:
                        if isinstance(d, dict):
                            res[0] = command(**d)
                        elif isinstance(d, (tuple, list)):
                            res[0] = command(*d)
                        else:
                            eg.PrintError(
                                'Named Pipe Error: '
                                'Data malformed: ' + str(d)
                            )
                    event.set()

                wx.CallAfter(run_command, data[1])

                while not event.isSet():
                    pass

                eg.PrintDebugNotice(
                    'Named Pipe: return data: ' + str(res[0])
                )

                win32file.WriteFile(pipe, str(repr(res[0])))
                win32pipe.DisconnectNamedPipe(pipe)

            else:
                eg.PrintError(
                    'Named Pipe Data Error: '
                    'Unknown Error: ' + str(data)
                )


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
        if err[0] == 231:
            return send_message(msg)

        raise NamedPipeConnectionError(err)


class NamedPipeException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return str(self.msg)


class NamedPipeDataError(NamedPipeException):
    pass


class NamedPipeConnectionError(NamedPipeException):

    def __getitem__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        
        return self.msg[item]

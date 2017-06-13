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

import win32pipe
import win32file
import threading
import ast
import wx


class Server:
    def __init__(self):
        self._event = threading.Event()
        self._thread = None

    def start(self):
        while self._event.isSet():
            pass

        if self._thread is None:
            self._thread = threading.Thread(
                name='EventGhost.Pipe.Thread',
                target=self.run
            )
            self._thread.start()

    def stop(self):
        if self._thread is not None:
            self._event.set()
            self._thread.join(1)

    def run(self):
        import eg

        while not self._event.isSet():

            try:
                pipe = win32file.CreateFile(
                    r'\\.\pipe\eventghost_pipe',
                    win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                    0,
                    None,
                    win32file.OPEN_EXISTING,
                    0,
                    None
                )
            except win32file.error:
                self._event.wait(0.5)
            else:
                data = win32file.ReadFile(pipe, 4096)
                if data[0] == 0:
                    command = ''
                    for char in data[1]:
                        if ord(char) != 0:
                            command += char
                    try:
                        command, data = command.split(',', 1)
                    except ValueError:
                        data = '()'

                    command = command.strip()
                    data = data.strip()

                    if '=' in command:
                        eg.PrintError(
                            'Named Pipe Error: '
                            'Command not allowed: ' + command
                        )

                    if not data.startswith('dict') and '=' in data:
                        eg.PrintError(
                            'Named Pipe Error: ' 
                            'Data not allowed: ' + data
                        )
                        continue

                    if (
                        data[0] not in ('(', '[', '{') and
                        not data.startswith('dict')
                    ):
                        eg.PrintError(
                            'Named Pipe Error: '
                            'Data not allowed: ' + data
                        )
                        continue

                    try:
                        command = eval(command.split('(', 1)[0])
                    except SyntaxError:
                        eg.PrintTraceback(
                            'Named Pipe Error: '
                            'Command malformed: ' + command
                        )
                        continue
                    else:
                        if isinstance(command, (str, unicode)):
                            eg.PrintError(
                                'Named Pipe Error: '
                                'Command does not exist: ' + command
                            )
                            continue
                    try:
                        data = eval(data.strip())
                    except SyntaxError:
                        eg.PrintError(
                            'Named Pipe Error: '
                            'Data malformed: ' + data
                        )
                        continue

                    if command is not None:
                        if isinstance(data, dict):
                            wx.CallAfter(command, **data)
                        elif isinstance(data, (tuple, list)):
                            wx.CallAfter(command, *data)
                        else:
                            eg.PrintError(
                                'Named Pipe Error: '
                                'Data malformed: ' + str(data)
                            )
                            continue

                else:
                    eg.PrintError(
                        'Named Pipe Error: '
                        'Unknown Error: ' + str(data)
                    )

        self._event.clear()
        self._thread = None


def send_message(msg):
    p = win32pipe.CreateNamedPipe(
        r'\\.\pipe\eventghost_pipe',
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT,
        1,
        65536,
        65536,
        300,
        None
    )

    win32pipe.ConnectNamedPipe(p, None)
    win32file.WriteFile(p, msg)


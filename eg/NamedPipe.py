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
import wx


class Server:
    def __init__(self):
        self.eg = __import__('eg')
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
                        if ord(char) > 31:
                            command += char

                    command, data = command.split(':', 1)

                    hide_frame = False

                    if command == 'plugin_install':
                        wx.CallAfter(self.eg.PluginInstall.Import, data)

                    elif command == 'trigger_event':
                        event, payload = data.split('^')
                        payload = eval(payload)
                        wx.CallAfter(self.eg.TriggerEvent, event, payload)

                    elif command == 'open_file':
                        wx.CallAfter(self.eg.document.Open, data)

                    elif command == 'hide_frame':
                        hide_frame = True
                    else:
                        print command, data

                    if hide_frame and self.eg.mainFrame is not None:
                        wx.CallAfter(self.eg.mainFrame.Iconize, True)

                    else:
                        if self.eg.mainFrame is not None:
                            wx.CallAfter(self.eg.mainFrame.Iconize, False)
                        else:
                            wx.CallAfter(self.eg.document.ShowFrame)
                else:
                    print 'ERROR', data

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

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


import eg
import threading
import traceback
import win32event
import win32file


class Serial(threading.Thread):

    def __init__(self, plugin, port, timeout):
        self.plugin = plugin
        self.port = port
        self.timeout = timeout
        self.event = threading.Event()
        self.stopEvent = None
        self.serial = None
        threading.Thread.__init__(self, name='Marantz Serial Thread')

    def Start(self):
        self.start()

    def Stop(self):
        self.event.set()
        win32event.SetEvent(self.stopEvent)
        self.serial.close()
        self.join(1.0)

    def Send(self, message):
        self.serial.write(message)

    def run(self):

        try:
            self.serial = serial = eg.SerialPort(
                self.port,
                timeout=self.timeout,
                baudrate=9600,
                bytesize=8,
                stopbits=1,
                parity='N',
                xonxoff=1,
                rtscts=0,
            )
        except:
            eg.PrintError('Marantz: Failed to initialize serial port.')
            traceback.print_exc()
        else:
            eg.PrintNotice(
                'Marantz: Serial Connected on COM' + str(self.port + 1)
            )

            self.stopEvent = stopEvent = win32event.CreateEvent(
                None,
                1,
                0,
                None
            )
            overlapped = getattr(serial, '_overlappedRead')
            hComPort = serial.hComPort
            hEvent = overlapped.hEvent
            n = 1
            waitingOnRead = False
            buf = win32file.AllocateReadBuffer(n)
            mBuf = ''

            while not self.event.isSet():
                if not waitingOnRead:
                    win32event.ResetEvent(hEvent)
                    hr, _ = win32file.ReadFile(hComPort, buf, overlapped)
                    if hr == 997:
                        waitingOnRead = True
                    elif hr != 0:
                        raise
                rc = win32event.MsgWaitForMultipleObjects(
                    (hEvent, stopEvent),
                    0,
                    1000,
                    win32event.QS_ALLINPUT
                )
                if rc == win32event.WAIT_OBJECT_0:
                    n = win32file.GetOverlappedResult(hComPort, overlapped, 1)
                    if n:
                        if str(buf[0]) == '\r':
                            mBuf += str(buf[0])
                            self.plugin.ProcessData(mBuf)
                            mBuf = ''
                        elif 31 < ord(buf[0]) < 128:
                            mBuf += str(buf[0])
                    waitingOnRead = False
                elif rc == win32event.WAIT_OBJECT_0 + 1:
                    self.event.set()
                elif rc != win32event.WAIT_TIMEOUT:
                    eg.PrintError("unknown message")
                    eg.PrintNotice(str(rc))
            self.serial = None
            eg.PrintNotice('Marantz: Serial disconnected from COM' + str(self.port))
        self.plugin.client = None

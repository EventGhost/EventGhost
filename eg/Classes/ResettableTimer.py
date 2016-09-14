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

from threading import Thread, Lock

# Local imports
from eg.WinApi.Dynamic import (
    CreateEvent,
    INFINITE,
    SetEvent,
    WAIT_OBJECT_0,
    WAIT_TIMEOUT,
    WaitForSingleObject,
)

class ResettableTimer(Thread):
    def __init__(self, callback):
        Thread.__init__(self, target=self.ThreadLoop)
        self.timeout = INFINITE
        self.lock = Lock()
        self.callback = callback
        self.event = CreateEvent(None, 0, 0, None)
        self.start()

    def Reset(self, milliseconds):
        self.lock.acquire()
        if milliseconds is None:
            milliseconds = INFINITE
        self.timeout = milliseconds
        SetEvent(self.event)
        self.lock.release()

    def Stop(self):
        self.Reset(StopMessage)

    def ThreadLoop(self):
        timeout = INFINITE
        while True:
            res = WaitForSingleObject(self.event, timeout)
            if res == WAIT_TIMEOUT:
                self.callback()
                timeout = INFINITE
            elif res == WAIT_OBJECT_0:
                self.lock.acquire()
                timeout = self.timeout
                self.lock.release()
                if timeout is StopMessage:
                    break
        self.callback = None


class StopMessage(object):
    pass

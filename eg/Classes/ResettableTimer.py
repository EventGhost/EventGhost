# This file is part of EventGhost.
# Copyright (C) 2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

from threading import Thread, Lock
from eg.WinApi.Dynamic import (
    CreateEvent,
    SetEvent,
    WaitForSingleObject,
    INFINITE,
    WAIT_TIMEOUT,
    WAIT_OBJECT_0
)


class StopMessage(object):
    pass


class ResettableTimer(Thread):

    def __init__(self, callback):
        Thread.__init__(self, target=self.ThreadLoop)
        self.timeout = INFINITE
        self.lock = Lock()
        self.callback = callback
        self.event = CreateEvent(None, 0, 0, None)
        self.start()


    def Stop(self):
        self.Reset(StopMessage)


    def Reset(self, milliseconds):
        self.lock.acquire()
        self.timeout = milliseconds
        SetEvent(self.event)
        self.lock.release()


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


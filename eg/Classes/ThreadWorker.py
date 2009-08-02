# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
# 
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import eg
from sys import exc_info, _getframe
from threading import Event, Thread, currentThread
from traceback import extract_stack, format_list
from functools import partial
from collections import deque
from time import clock
from eg.WinApi.Dynamic import (
    CreateEvent, SetEvent, WAIT_OBJECT_0, WAIT_TIMEOUT, QS_ALLINPUT,
    MsgWaitForMultipleObjects, byref, HANDLE, CoInitialize, CoUninitialize,
    MSG, PeekMessage, DispatchMessage, PM_REMOVE, WM_QUIT
)

def PumpWaitingMessages():
    msg = MSG()
    # PM_REMOVE = 0x0001
    while PeekMessage(byref(msg), 0, 0, 0, PM_REMOVE):
        if msg.message == WM_QUIT:
            return 1
        DispatchMessage(byref(msg))


class ThreadWorkerAction(object):
    """
    Represents an item that will be put on the ThreadWorker queue to be
    executed there.
    """
    __slots__ = [
        "time",
        "func",
        "returnValue",
        "processed",
        "exceptionInfo",
        "raiseException",
        "callersFrame",
    ]

    def __init__(self, func, raiseException=True):
        self.time = clock()
        self.func = func
        self.returnValue = None
        self.processed = Event()
        self.raiseException = raiseException
        self.exceptionInfo = None
        self.callersFrame = _getframe().f_back.f_back


    def __call__(self):
        try:
            self.returnValue = self.func()
        except Exception, exc:
            if self.raiseException:
                raise
            else:
                self.exceptionInfo = exc_info()
        finally:
            self.processed.set()


    def PrintUnhandledException(self):
        lines = [
            "Unhandled exception in WorkerThread <%s>:\n" % currentThread().name,
            "Callers stack:\n"
        ]
        lines += format_list(extract_stack(self.callersFrame))
        eg.PrintError("".join(lines).rstrip())
        eg.PrintTraceback()



class ThreadWorker(object):
    """
    General purpose message pumping thread, that is used in many places.
    """
    def __init__(self, *args, **kwargs):
        self.__startupExceptionInfo = None
        self.__alive = True
        self.__queue = deque()
        self.__setupFunc = partial(self.Setup, *args, **kwargs)
        self.__wakeEvent = CreateEvent(None, 0, 0, None)
        self.__dummyEvent = CreateEvent(None, 0, 0, None)
        self.__events = (HANDLE * 1)(self.__wakeEvent)
        self.__thread = Thread(
            group=None,
            target=self.__MainLoop,
            name=self.__class__.__name__,
        )


    def Setup(self, *args, **kwargs):
        """
        This will be called inside the thread at the beginning.

        Any exception raised in this method will be propagated to the
        self.Start() method and re-raised there.
        """
        pass


    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        pass


    def Start(self, timeout=None):
        """
        Start the thread execution.

        The thread will first call the self.Setup method with the parameters
        assigned by the ThreadWorker constructor and waits till self.Setup has
        finished its execution.
        If an exception is raised in self.Setup, this exception will be
        propagated to the self.Start method, so it will look like self.Start
        has directly called self.Setup. But self.Setup is actually executed in
        the new thread.
        """
        if timeout is None:
            timeout = eg.config.defaultThreadStartTimeout
        if timeout > 0.0:
            self.__thread.start()
            try:
                self.CallWait(self.__setupFunc, timeout)
            except:
                self.Stop()
                raise
        else:
            self.__thread.start()
            self.Call(self.__setupFunc)
            return True


    def Stop(self, timeout=0.0):
        """
        Call this if the thread should stop.
        """
        def StopCall():
            self.__alive = False

        self.Call(StopCall)
        if timeout > 0.0:
            self.__thread.join(timeout)
            return self.__thread.isAlive()


    @eg.LogItWithReturn
    def __MainLoop(self):
        """
        Mainloop of the new thread.
        """
        CoInitialize(None)
        PumpWaitingMessages()
        try:
            while self.__alive:
                self.__DoOneEvent()
        finally:
            CoUninitialize() # why I haven't put this as last statement?
                             # Must have a reason.
            self.Finish()


    def __DoOneEvent(self):
        try:
            resultCode = MsgWaitForMultipleObjects(
                1,
                self.__events,
                0,
                10000,
                QS_ALLINPUT
            )
            if resultCode == WAIT_OBJECT_0:
                while 1:
                    try:
                        action = self.__queue.popleft()
                    except IndexError:
                        break
                    try:
                        self.HandleAction(action)
                    except:
                        action.PrintUnhandledException()
                    finally:
                        # if the frame reference would not be removed, the 
                        # action would never be garbage collected.
                        action.callersFrame = None
            elif resultCode == WAIT_OBJECT_0+1:
                if PumpWaitingMessages():
                    eg.PrintDebugNotice("Got WM_QUIT")
                    self.__alive = False
                    return
            elif resultCode == WAIT_TIMEOUT:
                # Our timeout has elapsed.
                self.Poll()
            else:
                raise RuntimeError("unexpected win32wait return value")
        except:
            eg.PrintDebugNotice("Exception in __DoOneEvent")
            eg.PrintTraceback()


    def HandleAction(self, action):
        action()


    def Wait(self, timeout):
        endTime = clock() + timeout
        events = (HANDLE * 1)(self.__dummyEvent)
        while True:
            resultCode = MsgWaitForMultipleObjects(
                1,
                events,
                0,
                int(timeout * 1000),
                QS_ALLINPUT
            )
            if resultCode == WAIT_OBJECT_0:
                # event signalled - should never happen!
                raise Exception("Got unknown event in ThreadWorker.Wait()")
            elif resultCode == WAIT_TIMEOUT:
                # Timeout expired.
                return
            # must be a message.
            PumpWaitingMessages()
            timeout = endTime - clock()
            if timeout < 0:
                return


    def WaitOnEvent(self, event, timeout=10):
        endTime = clock() + timeout
        events = (HANDLE * 1)(event)
        while True:
            resultCode = MsgWaitForMultipleObjects(
                1,
                events,
                0,
                int(timeout * 1000),
                QS_ALLINPUT
            )
            if resultCode == WAIT_OBJECT_0:
                return
            elif resultCode == WAIT_TIMEOUT:
                # Timeout expired.
                return
            # must be a message.
            PumpWaitingMessages()
            timeout = endTime - clock()
            if timeout < 0:
                return


    def Poll(self):
        pass


    def AppendAction(self, action):
        self.__queue.append(action)
        SetEvent(self.__wakeEvent)


    def ClearPendingEvents(self):
        self.__queue.clear()


    def Call(self, func, *args, **kwargs):
        """
        Queue a function and its arguments for execution in the ThreadWorker 
        thread. Doesn't wait for the completion of the function.
        """
        action = ThreadWorkerAction(partial(func, *args, **kwargs), True)
        self.__queue.append(action)
        SetEvent(self.__wakeEvent)
        return action


    def CallWait(self, func, timeout=10.0):
        """
        Queue a function and its arguments for execution in the ThreadWorker 
        thread. Waits for completion of the function and returns its result.
        """
        action = ThreadWorkerAction(func, False)
        self.__queue.append(action)
        SetEvent(self.__wakeEvent)
        action.processed.wait(timeout)
        if not action.processed.isSet():
            eg.PrintStack()
            raise Exception(
                "Timeout in %s.CallWait()" % self.__class__.__name__
            )
        elif action.exceptionInfo is not None:
            excType, excValue, excTraceback = action.exceptionInfo
            raise excType, excValue, excTraceback
        return action.returnValue


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

from collections import deque
from functools import partial
from sys import exc_info, _getframe
from threading import currentThread, Event, Thread
from time import clock
from traceback import extract_stack, format_list

# Local imports
import eg
from eg.WinApi.Dynamic import (
    byref, COINIT_APARTMENTTHREADED, CoInitializeEx, CoUninitialize,
    CreateEvent, DispatchMessage, HANDLE, MSG, MsgWaitForMultipleObjects,
    PeekMessage, PM_REMOVE, QS_ALLINPUT, SetEvent, WAIT_OBJECT_0, WAIT_TIMEOUT,
    WM_QUIT
)

class ThreadWorker(object):
    """
    General purpose message pumping thread, that is used in many places.
    """
    # used for automatic documentation creation
    __docsort__ = (
        "Start, Stop, Setup, Finish, Call, Func, CallWait"
    )

    def __init__(self, *args, **kwargs):
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

    def AppendAction(self, action):
        self.__queue.append(action)
        SetEvent(self.__wakeEvent)

    def Call(self, func, *args, **kwargs):
        """
        Queue a function and its arguments for execution in the
        :class:`eg.ThreadWorker` thread. Doesn't wait for the completion of the
        function.
        """
        action = ThreadWorkerAction(func, args, kwargs, True)
        self.__queue.append(action)
        SetEvent(self.__wakeEvent)
        return action

    def CallWait(self, func, timeout=10.0):
        """
        Queue a function for execution in the :class:`eg.ThreadWorker` thread.
        Waits for completion of the function and returns its result.

        The function must have no arguments, so if some are needed one should
        create a argumentless function with functools.partial.

        .. note::

            This function is deprecated. Use the :meth:`Func` wrapper instead.
        """
        return self.Func(func, timeout)()

    def ClearPendingEvents(self):
        self.__queue.clear()

    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        pass

    def Func(self, func, timeout=None):
        """
        Wraps a function for synchronized execution in the
        :class:`eg.ThreadWorker` thread.

        The returned object can be called like the unwrapped function but will
        execute in the :class:`eg.ThreadWorker` thread regardless were it is
        called from. The call will deliver the return value of the function.
        If the function raises an exception, it will be propagated to the
        calling thread.

        The optional *timeout* value specifies the maximal time to wait for the
        completion of the function in floating point seconds. If the timeout
        expires, the call will raise an exception. If timeout is not specified
        or None (the default), it will wait forever.

        Example usage::

            threadWorker = eg.ThreadWorker()
            threadWorker.Start()

            def MyFunction(param):
                print param
                return "Hello Caller!"

            wrappedFunc = threadWorker.Func(MyFunction, 5.0)
            result = wrappedFunc("Hello World!")
            print result
        """
        def Wrapper(*args, **kwargs):
            action = ThreadWorkerAction(func, args, kwargs, False)
            self.__queue.append(action)
            SetEvent(self.__wakeEvent)
            action.processed.wait(timeout)
            if timeout is not None and not action.processed.isSet():
                eg.PrintStack()
                raise Exception("Timeout while calling %s" % func.__name__)
            if action.exceptionInfo is not None:
                excType, excValue, excTraceback = action.exceptionInfo
                raise excType, excValue, excTraceback
            return action.returnValue
        return Wrapper

    def HandleAction(self, action):
        action()

    def Poll(self):
        pass

    def Setup(self, *args, **kwargs):
        """
        This will be called inside the thread at the beginning.

        Any exception raised in this method will be propagated to the
        :meth:`Start` method and re-raised there.
        """
        pass

    def Start(self, timeout=None):
        """
        Start the thread execution.

        The thread will first call the self.Setup method with the parameters
        assigned by the :class:`eg.ThreadWorker` constructor and waits till
        :meth:`Setup` has finished its execution.
        If an exception is raised in self.Setup, this exception will be
        propagated to the self.Start method, so it will look like self.Start
        has directly called :meth:`Setup`. But :meth:`Setup` is actually
        executed in the new thread.
        """
        if timeout is None:
            timeout = eg.config.defaultThreadStartTimeout
        if timeout > 0.0:
            self.__thread.start()
            try:
                self.Func(self.__setupFunc, timeout)()
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
                # event signaled - should never happen!
                raise Exception("Got unknown event in ThreadWorker.Wait()")
            elif resultCode == WAIT_TIMEOUT:
                # Timeout expired.
                return
            # must be a message.
            self.__PumpWaitingMessages()
            timeout = endTime - clock()
            if timeout < 0:
                return

    def WaitOnEvent(self, event, timeout=10):
        endTime = clock() + timeout
        events = (HANDLE * 1)(event)
        while self.__alive:
            resultCode = MsgWaitForMultipleObjects(
                1,
                events,
                0,
                int(timeout * 1000),
                QS_ALLINPUT
            )
            if resultCode == WAIT_OBJECT_0:
                return True
            elif resultCode == WAIT_TIMEOUT:
                # Timeout expired.
                return
            # must be a message.
            self.__PumpWaitingMessages()
            timeout = endTime - clock()
            if timeout < 0:
                return True

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
            elif resultCode == WAIT_OBJECT_0 + 1:
                self.__PumpWaitingMessages()
            elif resultCode == WAIT_TIMEOUT:
                # Our timeout has elapsed.
                self.Poll()
            else:
                raise RuntimeError("unexpected win32wait return value")
        except:
            eg.PrintDebugNotice("Exception in __DoOneEvent")
            eg.PrintTraceback()

    @eg.LogItWithReturn
    def __MainLoop(self):
        """
        Mainloop of the new thread.
        """
        CoInitializeEx(None, COINIT_APARTMENTTHREADED)
        self.__PumpWaitingMessages()
        try:
            while self.__alive:
                self.__DoOneEvent()
        finally:
            self.Finish()
            CoUninitialize()

    def __PumpWaitingMessages(self):
        msg = MSG()
        while PeekMessage(byref(msg), 0, 0, 0, PM_REMOVE):
            if msg.message == WM_QUIT:
                self.__alive = False
                return
            DispatchMessage(byref(msg))


class ThreadWorkerAction(object):
    """
    Represents an item that will be put on the ThreadWorker queue to be
    executed there.
    """
    __slots__ = [
        "time",
        "func",
        "args",
        "kwargs",
        "returnValue",
        "processed",
        "exceptionInfo",
        "raiseException",
        "callersFrame",
    ]

    def __init__(self, func, args, kwargs, raiseException=True):
        self.time = clock()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.returnValue = None
        self.processed = Event()
        self.raiseException = raiseException
        self.exceptionInfo = None
        self.callersFrame = _getframe().f_back.f_back

    def __call__(self):
        try:
            self.returnValue = self.func(*self.args, **self.kwargs)
        except Exception:
            if self.raiseException:
                raise
            else:
                self.exceptionInfo = exc_info()
        finally:
            self.processed.set()

    def PrintUnhandledException(self):
        name = currentThread().name
        lines = [
            "Unhandled exception in WorkerThread <%s>:\n" % name,
            "Callers stack:\n"
        ]
        lines += format_list(extract_stack(self.callersFrame))
        eg.PrintError("".join(lines).rstrip())
        eg.PrintTraceback()

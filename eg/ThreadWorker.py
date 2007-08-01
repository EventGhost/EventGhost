# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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

from threading import Event, Thread, Lock
from collections import deque
from time import clock
from pythoncom import CoInitialize, CoUninitialize, PumpWaitingMessages
from win32event import (
    CreateEvent,
    SetEvent,
    MsgWaitForMultipleObjects,
    WAIT_OBJECT_0, 
    WAIT_TIMEOUT, 
    QS_ALLINPUT
)
import eg

class ThreadWorkerAction:
    """ 
    Represents an item that will be put on the ThreadWorker queue to be
    executed there.
    """
    def __init__(self, func, args, kwargs):
        self.time = clock()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.returnValue = None
        self.event = Event()
        
        
    def __call__(self):
        self.returnValue = self.func(*self.args, **self.kwargs)
        self.event.set()        



class ThreadWorker:
    """General purpose message pumping thread, that is used in many places.
    """
    def __init__(self):
        self.__thread = Thread(
            None, 
            self.__MainLoop, 
            self.__class__.__name__
        )
        self.__alive = True
        self.__timeout = 120.0
        self.__queue = deque()
        self.__queue_lock = Lock()
        self.__wakeEvent = CreateEvent(None, 0, 0, None)
        self.__dummyEvent = CreateEvent(None, 0, 0, None)
        
        
    def Setup(self):
        """
        This will be called inside the thread at the beginning.
        """
        pass
    
    
    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        pass
    
    
    def Start(self, timeout=None):
        if timeout is None:
            timeout = eg.config.defaultThreadStartTimeout
        if timeout > 0.0:
            startupEvent = Event()
            self.Call(startupEvent.set)
            self.__thread.start()
            startupEvent.wait(timeout)
            return startupEvent.isSet()
        else:
            self.__thread.start()
            return True
        
        
    def Stop(self, timeout=0.0):
        """
        Call this if the thread should stop.
        """
        def _stop():
            self.__alive = False
            
        self.Call(_stop)
        if timeout > 0.0:
            self.__thread.join(blocking)
            return self.__thread.isAlive()
        
        
    @eg.LogItWithReturn
    def __MainLoop(self):
        """
        Mainloop of the new thread.
        """
        CoInitialize()
        PumpWaitingMessages()
        self.Setup()
        try:
            while self.__alive:
                self.__DoOneEvent()
        finally:
            CoUninitialize()
            self.Finish()
            
            
    def __DoOneEvent(self):
        rc = MsgWaitForMultipleObjects(
            (self.__wakeEvent,), 
            0, 
            1000, 
            QS_ALLINPUT
        )
        if rc == WAIT_OBJECT_0:
            while 1:
                self.__queue_lock.acquire()
                if len(self.__queue) == 0:
                    self.__queue_lock.release()
                    break
                action = self.__queue.popleft()
                self.__queue_lock.release()
                self.HandleAction(action)
        elif rc == WAIT_OBJECT_0+1:
            #eg.DebugNote("WAIT_OBJECT_0+1")
            if PumpWaitingMessages():
                eg.DebugNote("Got WM_QUIT")
                self.__alive = False
                return
            #eg.DebugNote("WAIT_OBJECT_0+1 done")
        elif rc == WAIT_TIMEOUT:
            # Our timeout has elapsed.
            self.Poll()
        else:
            raise RuntimeError("unexpected win32wait return value")
        
            
    def HandleAction(self, action):
        try:
            action()
        except:
            eg.PrintTraceback()
        
    
    def Wait(self, timeout):
        otimeout = timeout
        start = clock()
        endTime = clock() + timeout
        while True:
            rc = MsgWaitForMultipleObjects(
                (self.__dummyEvent,),
                0,
                int(timeout * 1000),
                QS_ALLINPUT
            )
            if rc == WAIT_OBJECT_0:
                # event signalled - should never happen!
                raise Exception("Got unknown event in ThreadWorker.Wait()")
            elif rc == WAIT_TIMEOUT:
                # Timeout expired.
                return
            # must be a message.
            PumpWaitingMessages()
            timeout = endTime - clock()
            if timeout < 0:
                return

    
    def WaitOnEvent(self, event, timeout=10):
        otimeout = timeout
        start = clock()
        endTime = clock() + timeout
        while True:
            rc = MsgWaitForMultipleObjects(
                (event,),
                0,
                int(timeout * 1000),
                QS_ALLINPUT
            )
            if rc == WAIT_OBJECT_0:
                return
            elif rc == WAIT_TIMEOUT:
                # Timeout expired.
                return
            # must be a message.
            PumpWaitingMessages()
            timeout = endTime - clock()
            if timeout < 0:
                return
    
    
    def Poll(self):
        pass
    
    
    def AppendEvent(self, event):
        self.__queue_lock.acquire()
        self.__queue.append(event)
        self.__queue_lock.release()
        SetEvent(self.__wakeEvent)
        
        
    def FlushAllEvents(self):
        self.__queue_lock.acquire()
        self.__queue.clear()
        self.__queue_lock.release()


    def Call(self, func, *args, **kwargs):
        """ 
        Transmit a function and arguments to the thread and let it execute 
        there. Doesn't wait for the completion.
        """
        action = ThreadWorkerAction(func, args, kwargs)
        self.__queue_lock.acquire()
        self.__queue.append(action)
        self.__queue_lock.release()
        SetEvent(self.__wakeEvent)
        return action
        
        
    def CallWait(self, func, *args, **kwargs):
        """ 
        Transmit a function and arguments to the thread and let it execute 
        there. Waits for completion and returns the result of the function.
        """
        action = self.Call(func, *args, **kwargs)
        action.event.wait(self.__timeout)
        if not action.event.isSet():
            raise Exception("Timout in CallWait")
        return action.returnValue
    
    
    
        
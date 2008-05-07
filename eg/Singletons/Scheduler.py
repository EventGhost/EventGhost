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

from time import clock, time
from heapq import heappush, heapify, heappop
import threading



class Scheduler(threading.Thread):
    """Sometimes you want to execute some code at a specified time or after a 
    specified time period. EventGhost includes a small scheduler, that helps 
    you to accomplish this.
    
    :undocumented: Stop, MainLoop, __init__
    """

    def __init__(self):
        self.keepRunning = True
        self.event = threading.Event()
        self.lock = threading.Lock()
        self.heap = [(time() + 100000000, None, None, None)]
        threading.Thread.__init__(
            self, 
            target=self.MainLoop, 
            name="SchedulerThread"
        )
        
        
    def AddTask(self, waitTime, func, *args, **kwargs):
        """
        This function will call the callable `func` after `waitTime`
        seconds (expressed as a floating point number) with optional 
        parameters, by adding it to the scheduler's queue. A little example:

        .. python::
            def MyTestFunc(myArgument):
                print "MyTestFunc was called with:", repr(myArgument)
            
            eg.scheduler.AddTask(10.0, MyTestFunc, "just some test data")
            
        Ten seconds after invocation of the code it will print the following 
        message to the log::
        
            MyTestFunc was called with: 'just some test data'
        
        The function will also return an object, that you can use as the 
        `task` identifier for `CancelTask()`.

        :Parameters:
          waitTime
            The time to wait in floating point seconds.
          func
            The callable to invoke after the time has elapsed.
          args
            Optional positional arguments for the callable.
          kwargs
            Optional keyword arguments for the callable.
            
        :Returns:
          An object to identify the task.
        
        """
        return self.AddTaskAbsolute(time() + waitTime, func, *args, **kwargs)
        
        
    def AddTaskAbsolute(self, startTime, func, *args, **kwargs):
        """
        This does the same as `AddTask`, but the `startTime` parameter specifies
        an absolute time expressed in floating point seconds since the epoch. 
        Take a look at the documentation of `Python's time module`_, 
        for more information about this time format. Again a little example:
        
        .. python::
            import time
            startTime = time.mktime((2007, 8, 15, 16, 53, 0, 0, 0, -1))
            eg.scheduler.AddTaskAbsolute(startTime, eg.TriggerEvent, "MyEvent")
            
        This will trigger the event "Main.MyEvent" at 16:53:00 on 15 August 
        2007. If you run this code after this point of time, the 
        `eg.TriggerEvent` will be called immediately. 
        
        .. _Python's time module: http://docs.python.org/lib/module-time.html
        """
        try:
            self.lock.acquire()
            task = (startTime, func, args, kwargs)
            heappush(self.heap, task)
            self.event.set()
        finally:
            self.lock.release()
        return task
        
        
    def CancelTask(self, task):
        """
        This will cancel a task formerly added by `AddTask` or 
        `AddTaskAbsolute`, if the task hasn't been started yet. 
        
        If the task has already been called or simply wasn't added before, the 
        function will raise an IndexError.
        """
        try:
            self.lock.acquire()
            self.heap.remove(task)
            heapify(self.heap)
            self.event.set()
        finally:
            self.lock.release()
        
    
    def MainLoop(self):
        timeout = 0
        while self.keepRunning:
            self.event.wait(timeout)
            self.lock.acquire()
            self.event.clear()
            startTime, func, args, kwargs = self.heap[0]
            if startTime <= time():
                heappop(self.heap)
                self.lock.release()
                try:
                    func(*args, **kwargs)
                except:
                    eg.PrintTraceback()
                startTime = self.heap[0][0]
            else:
                self.lock.release()
            timeout = startTime - time()
            
            
    def Stop(self):
        def func():
            self.keepRunning = False
        self.AddTask(-1, func)
        
        
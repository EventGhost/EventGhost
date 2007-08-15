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
# $LastChangedDate: 2007-07-27 18:08:37 +0200 (Fri, 27 Jul 2007) $
# $LastChangedRevision: 192 $
# $LastChangedBy: bitmonster $

import eg
from time import clock
from heapq import heappush, heapify, heappop
import threading



class Scheduler(threading.Thread):

    def __init__(self):
        self.keepRunning = True
        self.event = threading.Event()
        self.lock = threading.Lock()
        self.heap = [(clock() + 100000000, None, None, None)]
        threading.Thread.__init__(self, target=self.MainLoop)
        
        
    def AddTaskAbsolute(self, startTime, callback, *args, **kwargs):
        try:
            self.lock.acquire()
            task = (startTime, callback, args, kwargs)
            heappush(self.heap, task)
            self.event.set()
        finally:
            self.lock.release()
        return task
        
        
    def AddTaskRelative(self, waitTime, callback, *args, **kwargs):
        startTime = clock() + waitTime
        return self.AddTaskAbsolute(startTime, callback, *args, **kwargs)
        
        
    def RemoveTask(self, task):
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
            startTime, callback, args, kwargs = self.heap[0]
            if startTime <= clock():
                heappop(self.heap)
                self.lock.release()
                try:
                    callback(*args, **kwargs)
                except:
                    eg.PrintTraceback()
            else:
                self.lock.release()
                startTime = self.heap[0][0]
            timeout = startTime - clock()
            
            
    def Stop(self):
        def callback():
            self.keepRunning = False
        self.AddTaskRelative(-1, callback)
        
            
            
if __name__ == "__main__":
    import random
    import time
    
    s = Scheduler()
    s.start()
    
    counter = 0
    def make_test_func(i, timeout):
        def test_func():
            global counter
            print "test", i, counter, timeout, clock() - timeout
            counter += 1
            time.sleep(0.01)
        return test_func
        
    times = [random.random() * 10.0 for i in range(100)]
    times.sort()
    for i, timeout in enumerate(times):
        time.sleep(0.01)
        s.AddTaskRelative(timeout, make_test_func(i, clock() + timeout))
    print "done"
    
                
                
        
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

import traceback
import time
from functools import partial
from eg.WinApi.Dynamic import (
    GetTickCount, 
    SetProcessWorkingSetSize, 
    GetCurrentProcess
)

EventGhostEvent = eg.EventGhostEvent



class EventThread(eg.ThreadWorker):
    
    def __init__(self):
        eg.ThreadWorker.__init__(self)
        eg.event = EventGhostEvent("")
        self.startupEvent = None
        self.currentProcess = GetCurrentProcess()


    def Poll(self):
        if eg.config.limitMemory and eg.document.frame is None:
            try:
                SetProcessWorkingSetSize(
                    self.currentProcess,
                    3670016,
                    eg.config.limitMemorySize * 1048576
                )
            except:
                self.Poll = self.Poll2
                
                
    def Poll2(self):
        pass
    
        
    def HandleAction(self, action):
        try:
            action()
        except:
            eg.PrintTraceback()
            
            
    def TriggerEvent(self, suffix, payload=None, prefix="Main", source=eg):
        '''Trigger an event'''
        event = EventGhostEvent(suffix, payload, prefix, source)
        self.AppendEvent(event.Trigger)
        return event
    
    
    def TriggerEnduringEvent(
        self, 
        suffix, 
        payload=None, 
        prefix="Main", 
        source=eg
    ):
        event = EventGhostEvent(suffix, payload, prefix, source)
        self.AppendEvent(event.TriggerEnduring)
        return event
        

    def TriggerEventWait(
        self, 
        suffix, 
        payload=None, 
        prefix="Main", 
        source=eg
    ):
        event = self.TriggerEvent(suffix, payload, prefix, source)
        event.startProcessed.wait(5.0)
        if not event.startProcessed.isSet():
            if eg.debugLevel:
                eg.PrintDebugNotice("timeout TriggerEventWait")
                traceback.print_stack()
        return event
    
    
    @eg.LogIt
    def StartSession(self, filename):
        self.shouldRun = True

        eg.actionThread.CallWait(
            partial(eg.actionThread.StartSession, filename),
            120
        )
        
        self.TriggerEvent("OnInit")
        boottime = time.time() - GetTickCount() / 1000.0
        if boottime > int(eg.config.storedBootTime) + 10:
            eg.config.storedBootTime = boottime
            eg.config.Save()
            self.TriggerEvent("OnInitAfterBoot")
            
        if self.startupEvent is not None:
            self.TriggerEvent(self.startupEvent[0], self.startupEvent[1])
            self.startupEvent = None
                

    @eg.LogIt
    def StopSession(self):
        eg.actionThread.CallWait(eg.actionThread.StopSession, 120)
        eg.PrintDebugNotice("StopSession done")


    

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

import eg
import traceback
import time
from functools import partial
from threading import Event
from eg.WinApi.Dynamic import (
    GetTickCount,
    OpenProcess,
    PROCESS_SET_QUOTA,
    SetProcessWorkingSetSize,
    FormatError,
)
from ThreadWorker import ThreadWorker
# some shortcuts
EventGhostEvent = eg.EventGhostEvent
actionThread = eg.actionThread
ActionThreadCall = actionThread.Call
ActionThreadCallWait = actionThread.CallWait


class EventThread(ThreadWorker):

    def __init__(self):
        ThreadWorker.__init__(self)
        eg.event = EventGhostEvent("")
        self.startupEvent = None
        self.hHandle = OpenProcess(PROCESS_SET_QUOTA, 0, eg.processId)
        self.filters = {}


    def Poll(self):
        if eg.config.limitMemory and eg.document.frame is None:
            try:
                if 0 == SetProcessWorkingSetSize(
                    self.hHandle,
                    3670016,
                    eg.config.limitMemorySize * 1048576
                ):
                    #TODO: what to do here?
                    eg.PrintDebugNotice(FormatError())
                    self.__class__.Poll = self.Poll2
            except:
                self.__class__.Poll = self.Poll2


    def Poll2(self):
        pass


    def AddFilter(self, source, filterFunc):
        if source in self.filters:
            self.filters[source].append(filterFunc)
        else:
            self.filters[source] = [filterFunc]
            
    
    def RemoveFilter(self, source, filterFunc):
        self.filters[source].remove(filterFunc)
        if len(self.filters[source]) == 0:
            del self.filters[source]


    def TriggerEvent(self, suffix, payload=None, prefix="Main", source=eg):
        '''Trigger an event'''
        event = EventGhostEvent(suffix, payload, prefix, source)
        if event.source in self.filters:
            for filterFunc in self.filters[event.source]:
                if filterFunc(event) == True:
                    return event
        def Transfer():
            ActionThreadCall(event.Execute)
            event.SetShouldEnd()
        self.AppendAction(Transfer)
        return event


    def TriggerEnduringEvent(
        self,
        suffix,
        payload=None,
        prefix="Main",
        source=eg
    ):
        event = EventGhostEvent(suffix, payload, prefix, source)
        if event.source in self.filters:
            for filterFunc in self.filters[event.source]:
                if filterFunc(event) == True:
                    return event
        def Transfer():
            ActionThreadCall(event.Execute)
        self.AppendAction(Transfer)
        return event


    def TriggerEventWait(
        self,
        suffix,
        payload=None,
        prefix="Main",
        source=eg
    ):
        event = EventGhostEvent(suffix, payload, prefix, source)
        if event.source in self.filters:
            for filterFunc in self.filters[event.source]:
                if filterFunc(event) == True:
                    return event
        executed = Event()
        def Execute():
            try:
                event.Execute()
            finally:
                executed.set()
            
        def Transfer():
            ActionThreadCall(Execute)
            event.SetShouldEnd()

        self.AppendAction(Transfer)
        executed.wait(5.0)
        if not executed.isSet():
            if eg.debugLevel:
                eg.PrintDebugNotice("timeout TriggerEventWait")
                traceback.print_stack()
        return event


    @eg.LogIt
    def StartSession(self, filename):
        ActionThreadCallWait(
            partial(actionThread.StartSession, filename),
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
        ActionThreadCallWait(actionThread.StopSession, 120)
        eg.PrintDebugNotice("StopSession done")


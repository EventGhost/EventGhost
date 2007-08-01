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
from time import clock
from threading import Event


def Init():
    global LogEvent 
    LogEvent = eg.log.LogEvent
    global actionThread
    actionThread = eg.actionThread
    global RunProgram
    RunProgram = eg.RunProgram
    global GetItemPath
    GetItemPath = eg.EventItem.GetPath


    
class EventGhostEvent(object):
    
    data = None

    def __init__(self, suffix="", payload=None, prefix="Main", source=eg):
        self.string = prefix + "." + suffix
        self.prefix = prefix
        self.suffix = suffix
        self.payload = payload
        self.source = source
        self.time = clock()
        
        self.startProcessed = Event()
        self.isEnded = False
        
        self.shouldEnd = Event()
        
        self.upFuncList = []
        self.onlyShowIfAssigned = False
        
        
    def AddUpFunc(self, func, *args, **kwargs):
        if self.isEnded:
            func(*args, **kwargs)
        else:
            self.upFuncList.append((func, args, kwargs))
        
        
    def SetStarted(self):
        self.startProcessed.set()
        if self.shouldEnd.isSet():
            self.DoUpFuncs()
            
        
    def DoUpFuncs(self):
        for func, args, kwargs in self.upFuncList:
            func(*args, **kwargs)
        del self.upFuncList[:]
        self.isEnded = True
        
        
    def Trigger(self):
        """
        Transfer this event from the EventThread to the ActionThread
        """
        actionThread.Call(self.Execute)
        self.SetShouldEnd()
        
        
    def TriggerEnduring(self):
        """
        Transfer this event from the EventThread to the ActionThread
        """
        actionThread.Call(self.Execute)
        
        
    def SetShouldEnd(self, dummy=None):
        if not self.shouldEnd.isSet():
            self.shouldEnd.set()
            eg.SetProcessingState(0, self)
            actionThread.Call(self.DoUpFuncs)
        
        
    def Execute(self):
        #start = clock()
        eventString = self.string
        eventHandlerList = eg.eventTable2.get(eventString, [])
        for eventFunc in eventHandlerList:
            if eventFunc(self) == True:
                return
            
        eg.event = self
        eg.eventString = eventString
        eg.EventString = eventString # eg.EventString is deprecated
        
        get = eg.eventTable.get
        eventHandlerList = []
        eventHandlerList += get(eventString, [])
        if self.prefix != "Keyboard":
            eventHandlerList += get(self.suffix, [])
            key2 = self.suffix.rsplit(".", 1)[-1]
            if self.suffix != key2:
                eventHandlerList += get(key2, [])
            eventHandlerList += get('*', [])
            key1 = eventString.rsplit(".", 1)[0] + '.*'
            eventHandlerList += get(key1, [])
            key2 = eventString.split(".", 1)[0] + '.*'
            if key1 != key2:
                eventHandlerList += get(key2, [])
        
        activeHandlers = set()
        for eventHandler in eventHandlerList:
            obj = eventHandler
            while obj:
                if not obj.isEnabled:
                    break
                obj = obj.parent
            else:
                activeHandlers.add(eventHandler)
        # show the event in the logger
        if eg.onlyLogAssigned and len(activeHandlers) == 0:
            return
        else:
            LogEvent(self)
        
        activeHandlers = sorted(activeHandlers, key=GetItemPath)
        #print clock()-start, len(eventHandlerList)
        
        eg.SetProcessingState(2, self)
        self.skipEvent = False
        for eventHandler in activeHandlers:
            try:
                eg.programCounter = (eventHandler.parent, None)
                RunProgram()
            except:
                eg.PrintTraceback()
            if self.skipEvent:
                break
        self.SetStarted()
        eg.SetProcessingState(1, self)
        

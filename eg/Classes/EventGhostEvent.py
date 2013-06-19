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

# some shortcuts to speed things up
#pylint: disable-msg=C0103
actionThread = eg.actionThread
LogEvent = eg.log.LogEvent
RunProgram = eg.RunProgram
GetItemPath = eg.EventItem.GetPath
config = eg.config
#pylint: enable-msg=C0103


class EventGhostEvent(object):
    """
    .. attribute:: string
    
        This is the full qualified event string as you see it inside the 
        logger, with the exception that if the payload field 
        (that is explained below) is not None the logger will also show it 
        behind the event string, but this is not a part of the event string 
        we are talking about here. 
        
    .. attribute:: payload
        
        A plugin might publish additional data related to this event. 
        Through payload you can access this data. For example the 'Network 
        Event Receiver' plugin returns also the IP of the client that has 
        generated the event. If there is no data, this field is ``None``. 
        
    .. attribute:: prefix
    
        This is the first part of the event string till the first dot. This 
        normally identifies the source of the event as a short string. 
        
    .. attribute:: suffix
    
        This is the part of the event string behind the first dot. So you 
        could say: 
        
        event.string = event.prefix + '.' + event.suffix 
    
    .. attribute:: time
    
        The time the event was generated as a floating point number in 
        seconds (as returned by the clock() function of Python's time module). 
        Since most events are processed very quickly, this is most likely 
        nearly the current time. But in some situations it might be more 
        clever to use this time, instead of the current time, since even 
        small differences might matter (for example if you want to determine 
        a double-press). 
    
    .. attribute:: isEnded
    
        This boolean value indicates if the event is an enduring event and is 
        still active. Some plugins (e.g. most of the remote receiver plugins) 
        indicate if a button is pressed longer. As long as the button is 
        pressed, this flag is ``False`` and in the moment the user releases the 
        button the flag turns to ``True``. So you can poll this flag to see, if 
        the button is still pressed. 

    """
    
    skipEvent = False
    
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
        if eventString in eg.notificationHandlers:
            for listener in eg.notificationHandlers[eventString].listeners:
                if listener(self) == True:
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
                
        if config.onlyLogAssigned and len(activeHandlers) == 0:
            self.SetStarted()
            return

        # show the event in the logger
        LogEvent(self)
        
        activeHandlers = sorted(activeHandlers, key=GetItemPath)
        
        eg.SetProcessingState(2, self)
        for eventHandler in activeHandlers:
            try:
                eg.programCounter = (eventHandler.parent, None)
                eg.indent = 1
                RunProgram()
            except:
                eg.PrintTraceback()
            if self.skipEvent:
                break
        self.SetStarted()
        eg.SetProcessingState(1, self)


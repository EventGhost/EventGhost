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

from fnmatch import fnmatchcase
from threading import Event
from time import clock

# Local imports
import eg

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
        self.isEnded = False
        self.shouldEnd = Event()
        self.upFuncList = []

    def AddUpFunc(self, func, *args, **kwargs):
        if self.isEnded:
            func(*args, **kwargs)
        else:
            self.upFuncList.append((func, args, kwargs))

    def DoUpFuncs(self):
        for func, args, kwargs in self.upFuncList:
            func(*args, **kwargs)
        del self.upFuncList[:]
        self.isEnded = True

    def Execute(self):
        #start = clock()
        eventString = self.string
        if eventString in eg.notificationHandlers:
            for listener in eg.notificationHandlers[eventString].listeners:
                if listener(self) is True:
                    return

        eg.event = self
        eg.eventString = eventString

        eventHandlerList = []
        for key, val in eg.eventTable.iteritems():
            if (
                eventString == key or
                (("*" in key or "?" in key) and fnmatchcase(eventString, key))
            ):
                eventHandlerList += val

        activeHandlers = set()
        for eventHandler in eventHandlerList:
            obj = eventHandler
            while obj:
                if not obj.isEnabled:
                    break
                obj = obj.parent
            else:
                activeHandlers.add(eventHandler)

        for listener in eg.log.eventListeners:
            listener.LogEvent(self)

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

    def SetShouldEnd(self):
        if not self.shouldEnd.isSet():
            self.shouldEnd.set()
            eg.SetProcessingState(0, self)
            actionThread.Call(self.DoUpFuncs)

    def SetStarted(self):
        if self.shouldEnd.isSet():
            self.DoUpFuncs()

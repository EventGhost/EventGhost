# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

import eg
from threading import Timer


class RawReceiverPlugin(eg.PluginBase):

    def __init__(self):
        eg.PluginBase.__init__(self)
        self.mapTable = {}
        self.timer = Timer(0, self.OnTimeOut)
        self.lastEventString = ""
        self.timeout = 0.2
        self.lastTimeout = self.timeout
        self.disableUnmapped = False
        self.repeatCode = None


    def TriggerEvent(self, suffix, payload=None):
        if suffix == self.repeatCode:
            suffix = self.lastEventString
            timeout = self.lastTimeout
        elif suffix in self.mapTable:
            newEventString, timeout, self.repeatCode = self.mapTable[suffix]
        else:
            if self.disableUnmapped:
                return
            newEventString = suffix
            timeout = self.timeout
            self.repeatCode = None
        self.timer.cancel()
        if self.lastEventString != suffix:
            self.TriggerEnduringEvent(newEventString, payload)
            self.lastEventString = suffix
        self.timer = Timer(timeout, self.OnTimeOut)
        self.timer.start()
        self.lastTimeout = timeout
        return self.info.lastEvent


    def OnTimeOut(self):
        self.EndLastEvent()
        self.lastEventString = ""


    def Map(self, what, to, timeout=None, repeatCode=None):
        self.mapTable[what] = (to, timeout or self.timeout, repeatCode)


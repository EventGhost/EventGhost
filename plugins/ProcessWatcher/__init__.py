# -*- coding: utf-8 -*-
#
# plugins/ProcessWatcher/__init__.py
#
# This file is a plugin for EventGhost.
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

import eg

eg.RegisterPlugin(
    name="Process Watcher",
    author=(
        "Bitmonster",
        "DranDane",
    ),
    version="1.1.",
    guid="{82BADF9F-D809-4EBC-A540-CCBF7563F8DF}",
    description=(
        "Generates events if a process is created or destoyed"
    ),
    url="http://www.eventghost.org/forum/viewtopic.php?f=10&t=1207",
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABuklEQVR42o1Sv0tCYRQ9"
        "L1FccpCEB73wVy1NjTrUPxD1lgZp0dWKaAhXxWhoyWgoIUjHBEH65RSE0CAUgWIPLAqR"
        "gkAQIQXR8nW/Z0ai6btweJfDd847934fhz8VCARkqCjTmBGra+sc67kOGQqFZIfDMVCo"
        "1WphMpng9/vxkMvi9u6e4zp/ZmStVkOpVOor1mg00Ol0CIfDKBQK/Q1isRhcLhedJpIn"
        "vHXkI+D5SUSj+0in0wMM4mSw6WqL9whLhHeCYAA/tobo9twQgxsyEMjglUj6IE7YIJxQ"
        "gk9K8DwsgTLCMjGGdvJxJibMUgJ+hUaYGWyQSCQQDO7+ZO8uo1EHn8/2v4Hb7UYmkxl4"
        "jY1GA9lsFrlcDl+fDZxfJNsGHo9H1QNiVa/XlQSiuIAp2wS466ukHNjaUauHXq+H0+n8"
        "HYPrzF+pVHriSpLUxbGHJAgCIpFIr0EqlYI0KmH6Y1o5XC6XaaFBpW+1WqhWq7BYLLRI"
        "X9ciFQNRFJHP53FoO4T3xdsTu9lsolgswm63Kz1b9tPTI6xmAVzk+Eg+PbtUvQNWstxS"
        "xHv7B+1bEBfnVd8CK6vFrIhZ/w1wBAQrC42uqQAAAABJRU5ErkJggg=="
    ),
)

from eg.cFunctions import GetProcessDict # NOQA
from threading import Thread # NOQA
from os.path import splitext # NOQA
import threading # NOQA


class Process(eg.PluginClass):

    def __init__(self):
        self.thread = None
        self.startException = None
        self.event = threading.Event()

    def __start__(self):
        self.thread = threading.Thread(
            target=self.ThreadLoop,
            name="ProcessWatcherThread"
        )

        self.thread.start()
        self.event.wait(3)
        if self.startException is not None:
            raise self.Exception(self.startException)

    def __stop__(self):
        self.event.set()
        if self.thread is not None:
            self.thread.join(5.0)
        self.thread = None
        self.startException = None

    def ThreadLoop(self):
        while self.event.isSet():
            pass

        oldProcesses = GetProcessDict()
        oldPids = set(oldProcesses.iterkeys())

        while not self.event.isSet():
            newProcesses = GetProcessDict()
            newPids = set(newProcesses.iterkeys())
            for pid in newPids.difference(oldPids):
                name = splitext(newProcesses[pid])[0]
                eg.TriggerEvent("Created." + name, prefix="Process")
            for pid in oldPids.difference(newPids):
                name = splitext(oldProcesses[pid])[0]
                eg.TriggerEvent("Destroyed." + name, prefix="Process")
            oldProcesses = newProcesses
            oldPids = newPids
            self.event.wait(0.1)
        self.event.clear()

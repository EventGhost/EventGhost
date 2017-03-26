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

# ChangeLog

# 30-1-2017 8:46 GMT -7:00      K
#   Added: Polling speed adjustment by the user
#   Added: Dynamic polling speed change via an action
#   Added: Select which processes to trigger events for
#   Changed: How the thread terminates
#   Changed: Replaced time.sleep with threading.Event


import eg


eg.RegisterPlugin(
    name = "Process Watcher",
    author = (
        "Bitmonster",
        "DranDane",
        "Sem;colon",
        "K"
    ),
    version = "1.2.0",
    guid = "{82BADF9F-D809-4EBC-A540-CCBF7563F8DF}",
    description = (
        "Generates events if a process is created or destoyed"
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?f=10&t=1207",
    icon = (
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

import wx

from eg.cFunctions import GetProcessDict
from os.path import splitext
import threading
from fnmatch import fnmatch
from eg.WinApi.Dynamic import (
# functions:
    CreateEvent,
    PulseEvent,
)


class Config(eg.PersistentData):
    processes = []

class Text(eg.TranslatableStrings):

    pollLbl = 'Default Poll Interval:'
    processNamesLbl = 'Allowed Processes (no checks = all processes)'
    resetMessage = 'ProcessWatcher: Setting poll interval %.2f back to %.2f'
    changeMessage = (
        'ProcessWatcher: Setting poll interval %.2f for %.2f seconds'
    )
    startMessage = 'ProcessWatcher: Watching..'
    stopMessage = 'ProcessWatcher: Not Watching..'

    class PollInterval:
        name = 'Change Poll Interval'
        description = (
            'Sets the duration of time between checking the process\n'
            'list for changes.'
        )
        pollLbl = 'New Poll Interval:'
        durationLbl = 'Interval Duration:'
        descLbl = (
            '\nHow long to keep the new polling interval set for.\n'
            'Set to 0 to keep indefinitely\n'
        )

    class GetProcessesByName:
        name = 'Get processes by name'
        description = (
            'Returns an array of dicts with processes (pid and name)\n'
            'that match a process name.'
        )
        processNameLbl = 'Process name:'


    class GetProcessByPid:
        name = 'Get process by PID'
        description = 'Returns True if the PID exists and False if not.'
        pidLbl = 'PID:'


class Process(eg.PluginClass):

    text = Text

    def __init__(self):
        self.AddAction(PollInterval)
        self.AddAction(GetProcessByPid)
        self.AddAction(GetProcessesByName)

        self._processNameList = Config.processes
        self._allowedEvents = ()
        self._threadEvent = threading.Event()
        self._pollInterval = 0.1
        self._resetIntervalTimer = None
        self._defaultInterval = 0.1
        self._processes = GetProcessDict()
        self._thread = None
        self.info.eventPrefix = "Process"

    def __start__(self, pollInterval=0.1, processNameList=()):
        self._allowedEvents = processNameList

        while self._threadEvent.isSet():
            pass

        self._pollInterval = pollInterval
        self._defaultInterval = pollInterval

        self._thread = threading.Thread(
            target=self.ThreadLoop,
            name="ProcessWatcherThread",
        )

        self._thread.start()

    def __stop__(self):
        Config.processes = self._processNameList
        self.StopIntervalTimer()

        if self._thread is not None:
            self._threadEvent.set()
            self._thread.join(5.0)

    def ResetInterval(self):
        eg.Print(
            self.text.resetMessage %
            (self._pollInterval, self._defaultInterval)
        )
        self._pollInterval = self._defaultInterval
        self._resetIntervalTimer = None

    def StopIntervalTimer(self):
        try:
            self._resetIntervalTimer.stop()
        except AttributeError:
            pass
        self._resetIntervalTimer = None

    def SetInterval(self, pollInterval, duration):
        eg.Print(
            self.text.changeMessage %
            (pollInterval, duration)
        )
        self._pollInterval = pollInterval
        self.StopIntervalTimer()
        if duration:
            self._resetIntervalTimer = threading.Timer(
                duration,
                self.ResetInterval
            )
            self._resetIntervalTimer.start()

    def TriggerEvents(self, suffix, set1, set2, processes):
        for pid in set1.difference(set2):
            name = splitext(processes[pid])[0]

            if name not in self._processNameList:
                self._processNameList.append(name)

            if not self._allowedEvents or name in self._allowedEvents:
                self.TriggerEvent(suffix=suffix + name, payload=dict(pid=pid))

    def ThreadLoop(self):
        eg.Print(self.text.startMessage)
        oldPids = set(key for key in self._processes.keys())

        while not self._threadEvent.isSet():
            newProcesses = GetProcessDict()
            newPids = set(key for key in newProcesses.keys())

            self.TriggerEvents("Created.", newPids, oldPids, newProcesses)
            self.TriggerEvents("Destroyed.", oldPids, newPids, self._processes)
            self._processes = newProcesses
            oldPids = newPids
            self._threadEvent.wait(self._pollInterval)

        self._threadEvent.clear()
        eg.Print(self.text.stopMessage)

    def Configure(self, pollInterval=0.1, processNamesList=()):
        text = self.text
        panel = eg.ConfigPanel()

        processNamesList = list(processNamesList)

        pollST = panel.StaticText(text.pollLbl)
        pollCtrl = panel.SpinNumCtrl(
            pollInterval,
            min=0.05,
            max=1.0,
            increment=0.05
        )

        processNamesST = panel.StaticText(text.processNamesLbl)
        processNamesCtrl = wx.CheckListBox(
            panel,
            choices=self._processNameList
        )
        if processNamesCtrl.GetCount():
            processNamesCtrl.SetCheckedStrings(processNamesList)
            if processNamesList:
                processNamesCtrl.SetFirstItem(len(processNamesList) - 1)
            else:
                processNamesCtrl.SetFirstItem(0)

        pollSizer = wx.BoxSizer(wx.HORIZONTAL)

        pollSizer.Add(pollST, 0, wx.EXPAND | wx.ALL, 10)
        pollSizer.Add(pollCtrl, 0, wx.EXPAND | wx.ALL, 10)
        panel.sizer.Add(pollSizer, 0, wx.EXPAND)
        panel.sizer.Add(
            processNamesST,
            0,
            wx.EXPAND | wx.ALIGN_CENTER | wx.ALL,
            10
        )
        panel.sizer.Add(
            processNamesCtrl,
            1,
            wx.EXPAND | wx.RIGHT | wx.LEFT | wx.BOTTOM,
            10
        )

        while panel.Affirmed():
            panel.SetResult(
                pollCtrl.GetValue(),
                processNamesCtrl.GetCheckedStrings()
            )


class PollInterval(eg.ActionBase):
    def __call__(self, pollInterval, duration):
        self.plugin.SetInterval(pollInterval, duration)

    def GetLabel(self, pollInterval, duration):
        return Text.changeMessage % (pollInterval, duration)

    def Configure(self, pollInterval=None, duration=0.0):

        if pollInterval is None:
            pollInterval = self.plugin._defaultInterval

        text = self.text
        panel = eg.ConfigPanel()

        pollST = panel.StaticText(text.pollLbl)
        pollCtrl = panel.SpinNumCtrl(
            pollInterval,
            min=0.05,
            max=1.0,
            increment=0.05
        )
        durationDesc = panel.StaticText(text.descLbl)
        durationST = panel.StaticText(text.durationLbl)
        durationCtrl = panel.SpinNumCtrl(
            duration,
            min=0.0,
            increment=0.05
        )

        pollSizer = wx.BoxSizer(wx.HORIZONTAL)
        durationSizer = wx.BoxSizer(wx.HORIZONTAL)

        pollSizer.Add(pollST, 0, wx.EXPAND | wx.ALL, 10)
        pollSizer.Add(pollCtrl, 0, wx.EXPAND | wx.ALL, 10)

        durationSizer.Add(durationST, 0, wx.EXPAND | wx.ALL, 10)
        durationSizer.Add(durationCtrl, 0, wx.EXPAND | wx.ALL, 10)

        panel.sizer.Add(pollSizer, 0, wx.EXPAND)
        panel.sizer.Add(durationDesc, 0, wx.EXPAND | wx.ALL, 10)
        panel.sizer.Add(durationSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                pollCtrl.GetValue(),
                durationCtrl.GetValue()
            )


class GetProcessByPid(eg.ActionBase):
    def __call__(self, pid):
        return pid in GetProcessDict()

    def Configure(self, pid=0):
        text = self.text
        panel = eg.ConfigPanel()

        wx_pid = panel.SpinIntCtrl(pid, min=0)
        st_pid = panel.StaticText(text.pidLbl)

        panel.AddLine(st_pid, wx_pid)

        while panel.Affirmed():
            panel.SetResult(wx_pid.GetValue())


class GetProcessesByName(eg.ActionBase):
    def __call__(self, processName):
        processes = GetProcessDict()
        pids = set(key for key in processes.keys())
        result = []
        for pid in pids:
            name = splitext(processes[pid])[0]
            if fnmatch(name, processName):
                result.append({"pid": pid, "name": name})
        return result

    def Configure(self, processName=""):
        text = self.text
        panel = eg.ConfigPanel()

        wx_processName = panel.TextCtrl(processName)
        st_processName = panel.StaticText(text.processNameLbl)

        panel.AddLine(st_processName, wx_processName)

        while panel.Affirmed():
            panel.SetResult(wx_processName.GetValue())


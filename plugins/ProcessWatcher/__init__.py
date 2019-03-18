# -*- coding: utf-8 -*-
#
# plugins/ProcessWatcher/__init__.py
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2018 EventGhost Project <http://www.eventghost.net/>
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
        "Sem;colon",
        "K",
    ),
    version="2.0.0",
    guid="{82BADF9F-D809-4EBC-A540-CCBF7563F8DF}",
    description=(
        "Generates events if a process is created or destoyed"
    ),
    url="http://www.eventghost.net/forum/viewtopic.php?f=10&t=1207",
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

import threading
from fnmatch import fnmatch
from os.path import splitext

import wx
from eg.cFunctions import GetProcessDict
from eg.WinApi.Dynamic import CreateEvent, PulseEvent


class Text(eg.TranslatableStrings):
    pollLbl = 'Default Poll Interval:'
    resetMessage = 'ProcessWatcher: Setting poll interval %.2f back to %.2f'
    changeMessage = (
        'ProcessWatcher: Setting poll interval %.2f for %.2f seconds'
    )
    startMessage = 'ProcessWatcher: Watching..'
    stopMessage = 'ProcessWatcher: Not Watching..'

    class PollInterval:
        name = 'Change Poll Interval'
        description = (
            'Sets the duration of time between checking the process list for '
            'changes'
        )
        pollLbl = 'New Poll Interval:'
        durationLbl = 'Interval Duration:'
        descLbl = (
            '\n\nHow long to keep the new polling interval set for.\n'
            'Set to 0 to keep indefinitely\n\n'
        )

    class IsPidExisting:
        name = "Is PID existing"
        description = """Returns True if the PID exists and False if not."""
        pid = "PID:"

    class GetProcessesByName:
        name = "Get processes by name"
        description = """Returns an array of dicts with processes (pid and name) that match a process name."""
        processName = "Process name:"


class PollInterval(eg.ActionBase):

    def __call__(self, pollInterval, duration):

        self.plugin.SetInterval(pollInterval, duration)

    def GetLabel(self, pollInterval, duration):
        return Text.changeMessage % (pollInterval, duration)

    def Configure(self, poll_interval=None, duration=0.0):

        if poll_interval is None:
            poll_interval = self.plugin._default_interval

        text = self.text
        panel = eg.ConfigPanel()

        poll_st = panel.StaticText(text.pollLbl)
        poll_ctrl = panel.SpinNumCtrl(
            poll_interval,
            min=0.05,
            max=1.0,
            increment=0.05
        )
        duration_desc = panel.StaticText(text.descLbl)
        duration_st = panel.StaticText(text.durationLbl)
        duration_ctrl = panel.SpinNumCtrl(
            duration,
            min=0.0,
            increment=0.05
        )

        poll_sizer = wx.BoxSizer(wx.HORIZONTAL)
        duration_sizer = wx.BoxSizer(wx.HORIZONTAL)

        poll_sizer.Add(poll_st, 0, wx.EXPAND | wx.ALL, 10)
        poll_sizer.Add(poll_ctrl, 0, wx.EXPAND | wx.ALL, 10)

        duration_sizer.Add(duration_st, 0, wx.EXPAND | wx.ALL, 10)
        duration_sizer.Add(duration_ctrl, 0, wx.EXPAND | wx.ALL, 10)

        panel.sizer.Add(poll_sizer, 0, wx.EXPAND)
        panel.sizer.Add(duration_desc, 0, wx.EXPAND | wx.ALL, 10)
        panel.sizer.Add(duration_sizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                poll_ctrl.GetValue(),
                duration_ctrl.GetValue()
            )


class IsPidExisting(eg.ActionBase):

    def __call__(self, pid):
        processes = GetProcessDict()
        return pid in processes

    def Configure(self, pid=0):
        panel = eg.ConfigPanel()
        text = self.text
        wx_pid = panel.SpinIntCtrl(pid, min=0)
        st_pid = panel.StaticText(text.pid)

        panel.AddLine(st_pid, wx_pid)

        while panel.Affirmed():
            panel.SetResult(wx_pid.GetValue(), )


class GetProcessesByName(eg.ActionBase):

    def __call__(self, processName):
        processes = GetProcessDict()
        pids = set(processes.iterkeys())
        result = []
        for pid in pids:
            name = splitext(processes[pid])[0]
            if fnmatch(name, processName):
                result.append({"pid": pid, "name": name})
        return result

    def Configure(self, processName=""):
        panel = eg.ConfigPanel()
        text = self.text
        wx_process_name = panel.TextCtrl(processName)
        st_process_name = panel.StaticText(text.processName)

        panel.AddLine(st_process_name, wx_process_name)

        while panel.Affirmed():
            panel.SetResult(wx_process_name.GetValue(), )


class Process(eg.PluginClass):
    text = Text

    def __init__(self):
        super(Process, self).__init__()
        self.AddAction(IsPidExisting)
        self.AddAction(GetProcessesByName)
        self.AddAction(PollInterval)
        self._threadEvent = threading.Event()
        self._pollInterval = 0.1
        self._resetIntervalTimer = None
        self._default_interval = 0.1

    def __start__(self, pollInterval=0.1):

        while self._threadEvent.isSet():
            pass

        self._pollInterval = pollInterval
        self._default_interval = pollInterval

        self.stopEvent = CreateEvent(None, 1, 0, None)
        self.startException = None

        startup_event = threading.Event()

        self.thread = threading.Thread(
            target=self.ThreadLoop,
            name="ProcessWatcherThread",
            args=(startup_event,)
        )

        self.thread.start()
        startup_event.wait(3)
        if self.startException is not None:
            raise self.Exception(self.startException)

    def __stop__(self):
        self.StopIntervalTimer()

        if self.thread is not None:
            self._threadEvent.set()
            PulseEvent(self.stopEvent)
            self.thread.join(5.0)

    def ResetInterval(self):
        eg.Print(
            self.text.resetMessage %
            (self._pollInterval, self._default_interval)
        )
        self._pollInterval = self._default_interval
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

    def Configure(self, pollInterval=0.1):
        text = self.text
        panel = eg.ConfigPanel()

        pollST = panel.StaticText(text.pollLbl)
        pollCtrl = panel.SpinNumCtrl(
            pollInterval,
            min=0.05,
            max=1.0,
            increment=0.05
        )

        pollSizer = wx.BoxSizer(wx.HORIZONTAL)

        pollSizer.Add(pollST, 0, wx.EXPAND | wx.ALL, 10)
        pollSizer.Add(pollCtrl, 0, wx.EXPAND | wx.ALL, 10)
        panel.sizer.Add(pollSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                pollCtrl.GetValue()
            )

    def ThreadLoop(self, stopThreadEvent):
        oldProcesses = GetProcessDict()
        oldPids = set(oldProcesses.iterkeys())

        eg.Print(self.text.startMessage)

        while not self._threadEvent.isSet():
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
            self._threadEvent.wait(self._pollInterval)
        self._threadEvent.clear()
        eg.Print(self.text.stopMessage)



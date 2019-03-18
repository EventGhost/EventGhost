# -*- coding: utf-8 -*-

PLUGIN_NAME     = "Standby Control"
PLUGIN_VERSION  = "1.14"

#
# plugins/Standby/__init__.py
#
# Copyright (C) 2008-2012 Stefan Gollmer & Daniel Brugger
#
# version history (newest on top)
# 1.13 Impr: ShowOSDCountDown: Supports now i18n (internationalization) for the text to be displayed.
#        Syntax: ${expression} will be replaced by the evaluated result of the Python 'expression'.
#      Impr: Stop threads on app exit
#      Fix: avoid exception during app exit
#      Fix: avoid PyDeadObject exception
# 1.12 Fix: EnableStandbyByApplication: triggerModePending == TM_PENDING_0_DONT_TRIGGER:
#        recovers previously set trigger time instead of using default pending time
# 1.11 Fix: Deadlock in ForceReleaseThread fixed.
#        (broken probably in 1.08, reproducible by calling InhibitStandby action with force release time set many times in a short interval)
#      Impr: Show number of monitored processes running in Config dialog
# 1.10 Refactoring and fixes for Monitored Process functionality:
#        Refactored monitorProcessList (ex. monitorProcessMap)
#        Fix: Count the number of running process instances in allProcessesMap (instead of True / False)
#        Impr: Display number of running process instances in Configure dialog
#        Impr: Only trigger 'Created' event for the first and 'Terminated' event for the last process (in case of multiple instances)
#        Fix: Re-initialize allProcessesMap in ProcessMonitorThread.Start() (otherwise it might be wrong after resume)
#        Impr: 'IsMonitoredProcessRunning' compares now monitorProcessList names case-insensitive (eg. 'setup.exe' is equal to 'SETUP.exe')
#        Fix: Event triggering for monitored processes after Configure.OK() fixed
#        Impr: Filter duplicate process names case-insensitive in Configure dialog
#        Fix: Sort monitorProcessList already on load case-insensitive
#      Fix for 'OnComputerSuspend' (broken in 1.09)
# 1.09 New events "KeepAlivePeriodStarted", "KeepAlivePeriodEnded", "AllKeepAlivePeriodsEnded" implemented.
#      New event "AllMonitoredProcessesTerminated" implemented.
#      Fix: Config dialog > processNameCtrl combo box was empty after adding StandbyControl Plugin to a new EG configuration.
#      Doc: Help page updated.
#      Doc: Event list implemented and documented.
# 1.08 Feature 'Keep Alive' completed and released.
#      On screen documentation added. HTML help file added.
#      Fix: Calling CheckAndEnable() from StartThreads(), otherwise Inhibits get lost when Config dialog is closed with OK.
#      Naming conventions for method names introduced. Class order tidied up. Lot of smaller refactorings and renamings.
#      Found and fixed again thread sync bugs. Thread locking consequently applied.
#      Config panel > Clear buttons fixed (broken in 1.07)
#      Sort procs in proc table case insensitive
# 1.07 Partially re-implemented CountDownOSD due to further multi-threading issues
#          EG action ShowOSD must not be called from another thread.
#      Reviewed and refactored thread synchronization for the timer and monitor threads
#      New feature 'Keepalive Schedule' implemented (but still hidden, feature still work in progress)
#      plugin.Configure() dialog refactored
# 1.06 _stop_ / _start_ after Configure() fixed -> deep copy necessary
#      Fixed multi-threading issues, causing EG to crash when calling CancelOSDCountdown
#          -> implemented thread synchronisation
# 1.05 IsMonitoredProcessRunning() action fixed. Application counter was wrong after system resume.
# 1.14 AddGrowableCol() updated to support EG 0.5
#
# This file is part of EventGhost.
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

import eg


from os.path import join, dirname, abspath
import codecs

HELPFILE = abspath(join(dirname(__file__.decode('mbcs')), "StandbyControl-Help.html"))

def GetHelp():
    try:
        f = codecs.open(HELPFILE, mode="r", encoding="latin_1", buffering=-1)
        hlp = f.read()
        f.close()
        hlp = hlp % (PLUGIN_VERSION)
        return hlp
    except Exception, exc:
        msg = "Error reading help file " + HELPFILE + ", error=" + unicode(exc)
        eg.PrintTraceback(msg)
        return msg

HELP = GetHelp()

eg.RegisterPlugin(
    name=PLUGIN_NAME,
    author="Stefan Gollmer, Daniel Brugger",
    version=PLUGIN_VERSION,
    kind="other",
    createMacrosOnAdd = True,
    guid="{427420BD-DCE6-458B-9A2A-858093DF1C55}",
    description=(
        "This plugin offers a better control of the system's standby / hibernate function "
        "by providing tools and convenient functions "
        "in order to build a sophisticated standby control environment."
    ),
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=3722",
    help=HELP,
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeT"
        "AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1QIRDwU5NWx/1gAAAl5JREFUeNqd"
        "k0tPU0EYhp9zzpy2NlDaCgqBBIo1Gi6NidE10cSNiXFr4sYfoO505+UHuHCJMbo10cS9"
        "QVR0YTR4CSCQQg2kgrSl9GI5PbcZFy1SxJWzmUzeeZ9vvjfzaXM3YgCK/1uaANTx62fQ"
        "f50GjL1y8HBjtzf+8vnItg8s3J9UAkAvjEKwfx/e77mA63lUvz6hKx7Zo+kFC5hENCrU"
        "QBUaSmQAKquARDNMTF2QW1uhK9wDZju41cY9p9YAAWBtQT0PsaOQOM+XTL5x3ommvglW"
        "EXnsEj9UArZzDc8fQHEadIXsHSMz8xatsgB+sflYBXYJttcpLb2jZ/Qc2aIL9VaAtQSB"
        "IJpu8m3iHqlBHfwidmWNciGLocpgF4hlHiF9j3J4CGpZgGYGwsCNDlPLLTMYeI+23Q1m"
        "HP/jNZaXK6R6BXhFNE/ibKaJdPZhzU4D7U2AoeNpAaT0iMYksAH2T9o8xaluBXUFtg+2"
        "g+FWMAyDUk21tCB0dGue6KEkVS0KIRNCAoI6mIDhg+GBKTC7T5DPTNMRagVoGsHqCwAC"
        "w7egLQhBEwICTAOEDkJHnbyLZoZZ//ycsKAFoAPOIluZcRKpy2zEb0NHbNdsHkCl7sDQ"
        "VWYnxkm6U6BUS4jNHA6Kx3xPhxhIXsF1L+KUZhFIRHQEIxBh7vVDNl/eZKxPB1+2AHxA"
        "SvBsEh0PWJl5Rc05S7xzBBAUFp+S/fSMI+4UY0kfrN0/JgBUroIWMMDxoVijX+XBekN1"
        "1aFcdhkQkpEuCbYCW4JUOx0gAG0+HVakbcD+58xW0JtBiX3j/Bvd+fjUkZbpxAAAAABJ"
        "RU5ErkJggg=="
    )
)

import wx
from time import time, mktime, strptime, strftime, localtime
from datetime import datetime as dt, timedelta as td
from threading import Thread, Event, Lock
from pythoncom import CoInitialize, CoUninitialize
from win32com.client import GetObject
from copy import deepcopy as cpy
from CountDownOSD import CountDownOSD, CancelOSDCountDown

# Blocking Counter Modes
CNT_MODE_0_SET   = 0
CNT_MODE_1_INCR  = 1
CNT_MODE_2_DECR  = 2
CNT_MODE_3_RESET = 3

# triggerModePending
TM_PENDING_0_DONT_TRIGGER    = 0  # doNotTrigger
TM_PENDING_1_PENDING_DEFAULT = 1  # triggerPendingDefault
TM_PENDING_2_STANDBY_DEFAULT = 2  # triggerStandbyDefault
TM_PENDING_3_SPECIAL_VALUE   = 3  # triggerSpecialValue

# triggerModeStandby
TM_STBY_0_DONT_TRIGGER       = 0  # doNotTrigger
TM_STBY_1_STANDBY_DEFAULT    = 1  # triggerStandbyDefault
TM_STBY_2_SPECIAL_VALUE      = 2  # triggerSpecialValue


class Text:
    standbyTime = "Standby default time [s]"
    standbyTimeAfterWakeUp = "Standby time after system resume [s]"
    standbyTimePending = "Standby default time, if standby was pending [s]"

    pendingCheckBox = "Pending status: "
    nextStandby = "Next trigger / force release in "

    timersTitle = "Standby trigger times"
    applicationsTitle = "Standby blocking counters"
    applications = "Currently known blocking counters:"
    applicationName = "Blocking counter name"
    applicationCounter = "Counter value"
    applicationReleaseTime = "Release time"
    resetAfterStandby = "Reset after resume"

    clearButton = "Clear"
    clearAllButton = "ClearAll"
    refreshButton = "Refresh"

    monitoredProcesses = "Monitored processes"
    processNameTxt = "Process name: "
    activeProcessCount = "Current count of active processes: "

    addProcess = "Add"
    removeProcess = "Remove"

    processName = "Process name"
    processStatus = "Process status"
    processCount = "Count"

    refreshProcesses = "Refresh"

    notStarted = "Plugin is not started, event was ignored"

    ok = "OK"
    cancel = "Cancel"

    kaSchedule = "Keep Alive Schedule"
    kaStartTime = "Start time"
    kaEndTime = "End time"
    kaDuration = "Duration HH:MM"
    kaWeekday = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
    kaStatus = "Status"
    kaNextStart = "Next start"
    kaAdd = "Add"
    kaModify = "Modify"
    kaRemove = "Remove"
    kaRefresh = "Refresh"
    kaFrameTitle = "Add / modify keep alive schedule entry"
    kaHelpAddModifyEntry = "Define a \'keep alive\' schedule entry. \nEnter the time period and the weekdays on which system suspend \nshall be blocked."
    kaHelpTable = "Define time periods when system suspend shall be blocked."

    class InhibitStandbyByApplication:
        applicationName = "Blocking counter name:"
        releaseCheckBox = "Set force release time [min]:"
        countUpCheckBox = "Increment counter (otherwise just set to 'True')"
        reserAfterStandby = "Reset counter after system resume"
        standbyTime = "Trigger standby timer"
        doNotTrigger = "Don't trigger"
        defaultCheckBox = "With default standby time"
        triggerSpecial = "With following value [s]:"

    class EnableStandbyByApplication:
        applicationName = "Blocking counter name:"
        resetCheckBox = "Reset the counter (otherwise decrement)"
        standbyTime = "Trigger standby timer"
        pendingText = "If counter is equal to zero"
        doNotPending = "Don't trigger"
        pendingCheckBox = "With default pending time"
        pendingSpecial = "With following value [s]:"
        standbyText = "If counter is unequal to zero"
        doNotTrigger = "Don't trigger"
        defaultCheckBox = "With default standby time"
        triggerSpecial = "With following value [s]:"
        applicationError = "Application name '%s' not found."

    class TriggerStandbyTimer:
        forceCheckBox = "Force standby time"
        defaultCheckBox = "Use standard standby time"
        standbyTime = "Standby time [s]:"

    class CountDownOSD:
        label = "Show OSD: %s"
        eventText = "OSD count down \nfinished event:"
        useExternal = "Use external OSD"
        externalOSD = "External OSD \nPython command:"
        headText = "Placeholder of the count down value: %c%"
        editText = "Text to display:"
        osdFont = "Text Font:"
        osdColour = "Text Colour:"
        outlineFont = "Outline OSD"
        alignment = "Alignment:"
        alignmentChoices = [
            "Top Left",
            "Top Right",
            "Bottom Left",
            "Bottom Right",
            "Screen Center",
            "Bottom Center",
            "Top Center",
            "Left Center",
            "Right Center",
        ]
        display = "Show on display:"
        xOffset = "Horizontal offset X:"
        yOffset = "Vertical offset Y:"
        wait = "Time interval [s]"
        start = "Start value:"
        end = "End value:"
        interval = "Interval:"
        skin = "Use skin"


class StandbyControl(eg.PluginClass):
    text = Text

    @eg.LogIt
    def __init__(self):
        self.countDownOSD = None
        self.AddEvents(*EVENT_LIST)
        self.AddActionsFromList(ACTIONS)

        #self.AddAction(Resume)                        # only for debugging the resume function of the plugin
        #self.AddAction(Suspend)                       # only for debugging the suspend function of the plugin

        self.applicationNames = []                     # List containing the application names
        self.applicationCounters = {}                  # Dictionary containing the application counters

        self.allProcessesMap = {}                      # Map containing all known processes and their instance count
        self.monitorProcessList = []                   # List containing the monitored processes (in lower case)
        self.keepAliveSchedule = []                    # List containing the keep alive schedule entries
        self.keepAliveTasks = {}                       # Map containing current tasks from eg.scheduler

        self.osdLock = Lock()           # global synchronization object for the DisplayOsdThread thread
        self.timerLock = Lock()         # global synchronization object for the StandbyTimerThread
        self.forceThreadLock = Lock()   # global synchronization object for the ForceReleaseThread
        self.processLock = Lock()       # global synchronization object for the ProcessMonitorThread
        self.appCtrLock = Lock()        # global synchronization object for the applicationCounters object
        self.kaScheduleLock = Lock()    # global synchronization object for the keepAliveSchedule object

        self.standbyTimeDefault = 0.0
        self.standbyTimePendingDefault = 0.0
        self.standbyTimeAfterWakeUp = 0.0

        self.lastApplicationName = ""

        self.threadStandby = None
        self.threadForce = None

        self.triggered = False
        self.started = False

    @eg.LogIt
    def __start__(
        self,
        standbyTime=300.0,
        standbyTimePending=60.0,
        standbyTimeAfterWakeUp=300.0,
        monitorProcessListMc=None,
        keepAliveSchedule=None
    ):
        if keepAliveSchedule is None:
            keepAliveSchedule = []
        if monitorProcessListMc is None:
            monitorProcessListMc = []
        eg.PrintDebugNotice(PLUGIN_NAME, PLUGIN_VERSION, 'plugin started on', strftime( "%d %b %Y %H:%M:%S", localtime() ))
        #print "__start__"
        self.standbyTimeDefault = standbyTime
        self.standbyTimePendingDefault = standbyTimePending
        self.standbyTimeAfterWakeUp = standbyTimeAfterWakeUp

        self.countDownOSD = None # current OSD count down action
        self.osdThread = None # global osd thread instance

        try:
            self.processLock.acquire()
            self.monitorProcessList = []
            for name in monitorProcessListMc:
                self.monitorProcessList.append(name.lower())
        finally:
            self.processLock.release()

        self.StartThreads()
        self.InitKeepAliveSchedule(keepAliveSchedule)

        self.started = True
        return True

    @eg.LogIt
    def StartThreads(self):
        self.threadStandby = StandbyTimerThread(self, self.standbyTimeDefault, self.standbyTimePendingDefault)
        self.threadStandby.start()

        self.threadForce = ForceReleaseThread(self)
        self.threadForce.start()

        try:
            self.appCtrLock.acquire()
            # If one closes the Config dialog with OK, __stop__ / __start__ gets called,
            # which restarts the threads, so we must make sure that currently running Inhibits don't get lost
            self.CheckAndEnable()
        finally:
            self.appCtrLock.release()

        self.processMonitor = ProcessMonitorThread(self, 5.0)
        self.processMonitor.start()

        eg.app.onExitFuncs.append(self.FinishThreads)

        return True

    @eg.LogIt
    def FinishThreads(self):
        if self.started:
            if self.threadStandby:
                self.threadStandby.Finish()
                self.threadStandby.join()
                del self.threadStandby
                self.threadStandby = None
            if self.threadForce:
                self.threadForce.Finish()
                self.threadForce.join()
                del self.threadForce
                self.threadForce = None
            if self.countDownOSD:
                self.countDownOSD.OSDCancel()
                self.countDownOSD = None
            if self.processMonitor:
                self.processMonitor.Terminate()
                self.processMonitor.join()
                del self.processMonitor
                self.processMonitor = None

        try:
            eg.app.onExitFuncs.remove(self.FinishThreads)
        except:
            pass

        return self.started

    @eg.LogItWithReturn
    def __stop__(self):
        #print "__stop__"
        self.started = False
        self.FinishThreads()
        self.StopKeepAliveSchedule()

    @eg.LogIt
    def __close__(self):
        pass
        #self.__stop__()

    @eg.LogItWithReturn
    def Configure(self,
                  standbyTime=600.0,
                  standbyTimePending=60.0,
                  standbyTimeAfterWakeUp=600.0,
                  monProcList=None,
                  kaSchedule=None):

        if kaSchedule is None:
            kaSchedule = []
        if monProcList is None:
            monProcList = []

        class TimerPanel:

            def BuildPanel(self):
                #Input of the timer values
                self.standbyTimeCtrl = panel.SpinNumCtrl(standbyTime, min=0, max=99999, fractionWidth=0, integerWidth=5)
                self.standbyTimePendingCtrl = panel.SpinNumCtrl(standbyTimePending, min=5, max=9999, fractionWidth=0, integerWidth=5)
                self.standbyTimeAfterWakeUpCtrl = panel.SpinNumCtrl(standbyTimeAfterWakeUp, min=0, max=99999, fractionWidth=0, integerWidth=5)
                self.standbyTextCtrl = wx.TextCtrl(panel, -1, "None / None", style = wx.TE_RIGHT)
                standbyTextCtrl = self.standbyTextCtrl
                standbyTextCtrl.Enable(False)

                gridSizer = wx.GridBagSizer(5, 5)
                rowCount = 0
                gridSizer.Add(wx.StaticText(panel, -1, text.standbyTime), (rowCount, 0), flag=wx.ALIGN_CENTER_VERTICAL)
                gridSizer.Add(self.standbyTimeCtrl, (rowCount, 1), flag=wx.ALIGN_RIGHT)

                gridSizer.Add(wx.StaticText(panel, -1, text.standbyTimePending), (rowCount, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=5)
                gridSizer.Add(self.standbyTimePendingCtrl, (rowCount, 3), flag=wx.EXPAND)

                rowCount += 1
                gridSizer.Add(wx.StaticText(panel, -1, text.nextStandby), (rowCount, 0), flag=wx.ALIGN_CENTER_VERTICAL)
                gridSizer.Add(standbyTextCtrl, (rowCount, 1), flag=wx.EXPAND)

                gridSizer.Add(wx.StaticText(panel, -1, text.standbyTimeAfterWakeUp), (rowCount, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=5)
                gridSizer.Add(self.standbyTimeAfterWakeUpCtrl, (rowCount, 3), flag=wx.EXPAND)

                appSBox = wx.StaticBox(panel, -1, text.timersTitle)
                appSBoxSizer = wx.StaticBoxSizer(appSBox, wx.VERTICAL)
                appSBoxSizer.Add(gridSizer, 1, flag=wx.EXPAND)

                return appSBoxSizer


        class ApplPanel:

            def BuildPanel(self):
                #Application table
                appTblSizer = wx.GridBagSizer(5,5)
                appTblSizer.AddGrowableCol(0)
                rowCount = 0

                txtCtrl = wx.StaticText(panel, -1, text.applications)
                appTblSizer.Add(txtCtrl, (rowCount, 0), span=(1,3), flag=wx.ALIGN_CENTER_VERTICAL)
                rowCount += 1

                self.applicationListCtrl = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)
                applicationListCtrl = self.applicationListCtrl
                applicationListCtrl.InsertColumn(0, text.applicationName)
                applicationListCtrl.InsertColumn(1, text.applicationCounter)
                applicationListCtrl.InsertColumn(2, text.resetAfterStandby)
                applicationListCtrl.InsertColumn(3, text.applicationReleaseTime)

                columnDelta = (150, 0, 0, 20)

                size = 0
                for c in range(len(columnDelta)):
                    applicationListCtrl.SetColumnWidth(c, wx.LIST_AUTOSIZE_USEHEADER)
                    csize = applicationListCtrl.GetColumnWidth(c) + columnDelta[c]
                    applicationListCtrl.SetColumnWidth(c, csize)
                    size += csize

                applicationListCtrl.SetMinSize((size, -1))

                tableRows = 6
                appTblSizer.Add(applicationListCtrl, (rowCount, 0), (tableRows, 3), flag=wx.EXPAND)
                appTblSizer.AddGrowableRow(rowCount)
                rowCount += tableRows

                #buttons
                self.clearButton = wx.Button(panel, -1, text.clearButton)
                appTblSizer.Add(self.clearButton, (rowCount,0), flag=wx.LEFT)
                self.clearButton.Enable(False)

                clearAllButton = wx.Button(panel, -1, text.clearAllButton)
                appTblSizer.Add(clearAllButton, (rowCount,1), flag=wx.ALIGN_CENTER_HORIZONTAL)

                refreshAButton = wx.Button(panel, -1, text.refreshButton)
                appTblSizer.Add(refreshAButton, (rowCount,2), flag=wx.ALIGN_RIGHT)

                self.clearButton.Bind(wx.EVT_BUTTON, self.onClearButton)
                clearAllButton.Bind(wx.EVT_BUTTON, self.onClearAllButton)
                refreshAButton.Bind(wx.EVT_BUTTON, self.onRefreshApplButton)

                applicationListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.applListSelection)
                applicationListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.applListSelection)

                appSBox = wx.StaticBox(panel, -1, text.applicationsTitle)
                appSBoxSizer = wx.StaticBoxSizer(appSBox, wx.VERTICAL)
                appSBoxSizer.Add(appTblSizer, 1, flag=wx.EXPAND)

                return appSBoxSizer

            def FillApplTable (self, event):
                self.applicationListCtrl.DeleteAllItems()
                row = 0
                for name, entry in plugin.applicationCounters.iteritems():
                    counter = entry.counter
                    self.applicationListCtrl.InsertItem(row, name)
                    self.applicationListCtrl.SetItem(row, 1, str(counter))
                    if entry.resetAfterStandby:
                        string = "Yes"
                    else:
                        string = "No"
                    self.applicationListCtrl.SetItem(row, 2, string)
                    releaseTime = entry.releaseTime
                    if (releaseTime > 0.0):
                        string = strftime("%d.%m %H:%M:%S", localtime(releaseTime))
                    else:
                        string = "Not set"
                    self.applicationListCtrl.SetItem(row, 3, string)
                    row += 1
                event.Skip()

            def applListSelection(self, event):
                enable = self.applicationListCtrl.GetFirstSelected() != -1
                self.clearButton.Enable(enable)
                event.Skip()

            def onClearButton(self, event):
                try:
                    plugin.appCtrLock.acquire()
                    item = self.applicationListCtrl.GetFirstSelected()
                    while item != -1:
                        name = self.applicationListCtrl.GetItemText(item)
                        plugin.applicationCounters[name] = plugin.AppEntry()
                        item = self.applicationListCtrl.GetNextSelected(item)
                    self.onRefreshApplButton(wx.CommandEvent(), alreadyLocked=True)
                    plugin.CheckAndEnable()
                    plugin.UpdateReleaseTime()
                finally:
                    plugin.appCtrLock.release()
                event.Skip()

            def onClearAllButton(self, event):
                try:
                    plugin.appCtrLock.acquire()
                    for name, counter in plugin.applicationCounters.iteritems():
                        plugin.applicationCounters[name] = plugin.AppEntry()
                    self.onRefreshApplButton(wx.CommandEvent(), alreadyLocked=True)
                    plugin.CheckAndEnable()
                    plugin.UpdateReleaseTime()
                finally:
                    plugin.appCtrLock.release()
                event.Skip()

            def onRefreshApplButton(self, event, alreadyLocked=False):
                self.FillApplTable(event)
                if plugin.started and plugin.threadStandby and plugin.threadForce:
                    try:
                        if not alreadyLocked:
                            plugin.appCtrLock.acquire()
                        nextStandby = plugin.threadStandby.GetNextTriggerTime()
                        if plugin.threadStandby.GetPendingStatus():
                            status = "Pending"
                        elif nextStandby >= 0.0:
                            status = str(nextStandby) + " s"
                        else:
                            status = "None"
                        status += " / "
                        nextRelease = plugin.threadForce.GetNextReleaseTime()
                        if nextRelease:
                            status += str(nextRelease) + " s"
                        else:
                            status += "None"
                        plugin.timerPanel.standbyTextCtrl.SetValue(status)
                    finally:
                        if not alreadyLocked:
                            plugin.appCtrLock.release()


        class ProcessPanel:
            def __init__(self):
                if len(plugin.allProcessesMap) == 0 and not plugin.started:
                    ProcessMonitorThread.InitProcessesMap(plugin)

            def BuildPanel(self):
                # Monitored Process List
                procTblSizer = wx.GridBagSizer(5,5)
                procTblSizer.AddGrowableCol(0)
                rowCount = 0

                # process name drop down and button
                self.processNameCtrl = wx.ComboBox(panel, -1, value='', choices = [], size=(200,-1) )
                procTblSizer.Add(
                    wx.StaticText(panel, -1, text.processNameTxt), (rowCount, 0),
                    flag=wx.ALIGN_CENTER_VERTICAL
                )
                procTblSizer.Add(self.processNameCtrl, (rowCount, 1), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
                self.addProcButton = wx.Button(panel, -1, text.addProcess)
                self.addProcButton.Enable(False)
                procTblSizer.Add(self.addProcButton, (rowCount, 2), flag=wx.ALIGN_LEFT)
                procTblSizer.Add(wx.Size(20, 0), (rowCount, 3), flag=wx.EXPAND)

                # active process count label
                procTblSizer.Add(
                    wx.StaticText(panel, -1, text.activeProcessCount), (rowCount, 4),
                    flag=wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL
                )
                self.activeProcCntTextCtrl = wx.TextCtrl(panel, -1, "0", size=(40, -1), style = wx.TE_RIGHT)
                self.activeProcCntTextCtrl.Enable(False)
                procTblSizer.Add(self.activeProcCntTextCtrl, (rowCount, 5), flag=wx.ALIGN_RIGHT)

                # table
                self.processListCtrl = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)
                processListCtrl = self.processListCtrl
                processListCtrl.InsertColumn(0, text.processName)
                processListCtrl.InsertColumn(1, text.processStatus)
                processListCtrl.InsertColumn(2, text.processCount)

                columnDelta = (200, 0, 0)

                size = 0
                for c in range(len(columnDelta)):
                    processListCtrl.SetColumnWidth(c, wx.LIST_AUTOSIZE_USEHEADER)
                    csize = processListCtrl.GetColumnWidth(c) + columnDelta[c]
                    processListCtrl.SetColumnWidth(c, csize)
                    size += csize

                processListCtrl.SetMinSize((size, -1))

                tableRows = 6
                rowCount += 1
                procTblSizer.Add(processListCtrl, (rowCount, 0), span=(tableRows, 6), flag=wx.EXPAND)
                procTblSizer.AddGrowableRow(rowCount)
                rowCount += tableRows

                #buttons
                self.removeProcButton = wx.Button(panel, -1, text.removeProcess)
                procTblSizer.Add(self.removeProcButton, (rowCount, 0), flag=wx.ALIGN_LEFT)
                self.removeProcButton.Enable(False)

                self.refreshProcButton = wx.Button(panel, -1, text.refreshProcesses)
                procTblSizer.Add(self.refreshProcButton, (rowCount, 5), flag=wx.ALIGN_RIGHT)
                rowCount += 1

                self.processNameCtrl.Bind(wx.EVT_TEXT, self.onProcComboChange)
                self.addProcButton.Bind(wx.EVT_BUTTON, self.onAddProcButton)
                processListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onProcSelection)
                processListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onProcSelection)
                processListCtrl.Bind(wx.EVT_LIST_COL_CLICK, self.onColumnSort)
                self.refreshProcButton.Bind(wx.EVT_BUTTON, self.onRefreshProcButton)
                self.removeProcButton.Bind(wx.EVT_BUTTON, self.onRemoveProcButton)

                procSbox = wx.StaticBox(panel, -1, text.monitoredProcesses)
                procSboxSizer = wx.StaticBoxSizer(procSbox, wx.VERTICAL)
                procSboxSizer.Add(procTblSizer, 1, flag=wx.EXPAND)

                return procSboxSizer

            def onProcSelection(self, event):
                enable = self.processListCtrl.GetFirstSelected() != -1
                self.removeProcButton.Enable(enable)
                event.Skip()

            def onColumnSort(self, event):
                # not implemented yet
                obj = event.GetEventObject()
                event.Skip()

            def onProcComboChange(self, event):
                name = self.processNameCtrl.GetValue()
                self.addProcButton.Enable(name != '')

            def onAddProcButton(self, event):
                name = self.processNameCtrl.GetValue()
                if name != '' and name not in monitorProcessListMc:
                    monitorProcessListMc.append(name)
                    monitorProcessListMc.sort(cmp=lambda x, y: cmp(x.lower(), y.lower()))
                    self.onRefreshProcButton(event)
                event.Skip()

            def onRemoveProcButton(self, event):
                item = self.processListCtrl.GetFirstSelected()
                while item != -1:
                    name = self.processListCtrl.GetItemText(item)
                    monitorProcessListMc.remove(name)
                    item = self.processListCtrl.GetNextSelected(item)
                self.onRefreshProcButton(event)
                self.removeProcButton.Enable(False)
                event.Skip()

            def onRefreshProcButton(self, event):
                # sort and remove duplicates
                monitorProcessListMc.sort(cmp=lambda x, y: cmp(x.lower(), y.lower()))
                lastname = ''
                for name in monitorProcessListMc:
                    if name.lower() == lastname.lower():
                        if name in plugin.allProcessesMap:
                            monitorProcessListMc.remove(lastname)
                        else:
                            monitorProcessListMc.remove(name)
                    lastname = name

                # fill table
                self.processListCtrl.DeleteAllItems()
                activeProcCnt = 0
                row = 0
                for name1 in monitorProcessListMc:
                    status = 'terminated'
                    count = 0
                    lname1 = name1.lower()
                    # find active process case-insensitive (i.e. regardless how they are written in monitorProcessList)
                    for name2 in plugin.allProcessesMap:
                        lname2 = name2.lower()
                        if lname1 == lname2 and plugin.allProcessesMap[name2] > 0:
                            status = 'active'
                            count = plugin.allProcessesMap[name2]
                            activeProcCnt += count
                    self.processListCtrl.InsertItem(row, name1)
                    self.processListCtrl.SetItem(row, 1, status)
                    self.processListCtrl.SetItem(row, 2, str(count))
                    row += 1
                self.processNameCtrl.Clear()
                self.processNameCtrl.AppendItems(self.getProcessList())
                self.activeProcCntTextCtrl.SetValue(str(activeProcCnt))
                event.Skip()

            def getProcessList(self):
                processList = []
                for name in plugin.allProcessesMap:
                    if name not in monitorProcessListMc:
                        processList.append(name)
                processList.sort(cmp=lambda x, y: cmp(x.lower(), y.lower()))
                return processList


        class KeepAlivePanel:

            def BuildPanel(self):
                kaTblSizer = wx.GridBagSizer(5,5)
                kaTblSizer.AddGrowableCol(0)
                rowcount = 0

                helpLbl = wx.StaticText(panel, -1, text.kaHelpTable)
                kaTblSizer.Add(helpLbl, (rowcount,0), span=(1,3), flag=wx.EXPAND)
                rowcount += 1

                self.keepaliveTbl = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL | wx.LC_SINGLE_SEL)
                self.keepaliveTbl.InsertColumn(0, text.kaStartTime)
                self.keepaliveTbl.InsertColumn(1, text.kaEndTime)
                self.keepaliveTbl.InsertColumn(2, text.kaDuration)
                for c in range(len(text.kaWeekday)):
                    self.keepaliveTbl.InsertColumn(c+3, text.kaWeekday[c])
                self.keepaliveTbl.InsertColumn(10, text.kaStatus)
                self.keepaliveTbl.InsertColumn(11, text.kaNextStart)

                kaColWidths = (70, 70, 90, 35, 35, 35, 35, 35, 35, 35, 60, 130)
                size = 0
                for c in range(len(kaColWidths)):
                    self.keepaliveTbl.SetColumnWidth(c, kaColWidths[c])
                    size += kaColWidths[c]
                self.keepaliveTbl.SetMinSize((size, -1))

                tableRows = 6
                kaTblSizer.Add(self.keepaliveTbl, (rowcount,0), span=(tableRows,3), flag=wx.EXPAND)
                kaTblSizer.AddGrowableRow(rowcount)
                rowcount += tableRows

                #buttons
                kaBtnSizer = wx.GridBagSizer(5,50)

                self.kaAddBtn = wx.Button(panel, -1, text.kaAdd)
                kaBtnSizer.Add(self.kaAddBtn, (0,0), flag=wx.ALIGN_LEFT)

                self.kaModifyBtn = wx.Button(panel, -1, text.kaModify)
                kaBtnSizer.Add(self.kaModifyBtn, (0,1), flag=wx.ALIGN_CENTER)
                self.kaModifyBtn.Enable(False)

                self.kaRemoveBtn = wx.Button(panel, -1, text.kaRemove)
                kaBtnSizer.Add(self.kaRemoveBtn, (0,2), flag=wx.ALIGN_RIGHT)
                self.kaRemoveBtn.Enable(False)

                kaTblSizer.Add(kaBtnSizer, (rowcount,0), span=(1,2), flag=wx.ALIGN_LEFT)

                self.kaRefreshBtn = wx.Button(panel, -1, text.kaRefresh)
                kaTblSizer.Add(self.kaRefreshBtn, (rowcount,2), flag=wx.ALIGN_RIGHT)
                rowcount += 1

                self.kaAddBtn.Bind(wx.EVT_BUTTON, self.onKaAddButton)
                self.kaModifyBtn.Bind(wx.EVT_BUTTON, self.onKaModifyButton)
                self.kaRemoveBtn.Bind(wx.EVT_BUTTON, self.onKaRemoveButton)
                self.kaRefreshBtn.Bind(wx.EVT_BUTTON, self.onKaRefreshButton)

                self.keepaliveTbl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onKaEntrySelection)
                self.keepaliveTbl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onKaEntrySelection)
                self.keepaliveTbl.Bind(wx.EVT_LEFT_DCLICK, self.onKaModifyButton)

                kaSBox = wx.StaticBox(panel, -1, text.kaSchedule)
                kaSBoxSizer = wx.StaticBoxSizer(kaSBox, wx.VERTICAL)
                kaSBoxSizer.Add(kaTblSizer, 1, flag=wx.EXPAND)

                return kaSBoxSizer

            def onKaRefreshButton(self, event, selRow=-1):
                keepaliveTbl = self.keepaliveTbl
                currSel = keepaliveTbl.GetFirstSelected()
                keepaliveTbl.DeleteAllItems()
                for row, kaEntry in enumerate(keepaliveSchedule):
                    keepaliveTbl.InsertItem(row, kaEntry.startTime)
                    keepaliveTbl.SetItem(row, 1, kaEntry.endTime)
                    keepaliveTbl.SetItem(row, 2, kaEntry.Get_HHMM_DurationStr())
                    for i, wd in enumerate(kaEntry.weekday):
                        keepaliveTbl.SetItem(row, i+3, wd and "yes" or "no")
                    isActive, nextStart = kaEntry.GetExecutionStatus()[0:4:3]
                    keepaliveTbl.SetItem(row, 10, isActive and "active" or "waiting")
                    keepaliveTbl.SetItem(row, 11, str(nextStart))
                self.kaModifyBtn.Enable(False)
                self.kaRemoveBtn.Enable(False)
                if selRow >= 0:
                    currSel = selRow
                if currSel >= len(keepaliveSchedule):
                    currSel = len(keepaliveSchedule) -1
                if currSel >= 0:
                    self.keepaliveTbl.Select(currSel, 1)
                event.Skip()

            def AddModifyKaEntry(self, mode, kaEntry):
                if mode == "add":
                    keepaliveSchedule.append(kaEntry)
                    self.onKaRefreshButton(wx.CommandEvent(), selRow=len(keepaliveSchedule)-1)
                elif mode == "modify":
                    self.onKaRefreshButton(wx.CommandEvent())

            def onKaAddButton(self, evt):
                dlg = self.AddModKeepaliveDlg(parent=panel, kaEntry=KeepAliveEntry(), mode="add")
                dlg.Centre()
                wx.CallAfter(dlg.ShowAddModKeepaliveDlg)
                evt.Skip()

            def onKaModifyButton(self, evt):
                entry = self.keepaliveTbl.GetFirstSelected()
                if entry != -1:
                    dlg = self.AddModKeepaliveDlg(parent=panel, kaEntry=keepaliveSchedule[entry], mode="modify")
                    dlg.Centre()
                    wx.CallAfter(dlg.ShowAddModKeepaliveDlg)
                    evt.Skip()

            def onKaRemoveButton(self, evt):
                entry = self.keepaliveTbl.GetFirstSelected()
                if entry != -1:
                    del keepaliveSchedule[entry]
                    self.onKaRefreshButton(wx.CommandEvent())
                    evt.Skip()

            def onKaEntrySelection(self, event):
                enable = self.keepaliveTbl.GetFirstSelected() != -1
                self.kaRemoveBtn.Enable(enable)
                self.kaModifyBtn.Enable(enable)
                event.Skip()

            class AddModKeepaliveDlg(wx.Dialog):
                def __init__(self, parent, kaEntry, mode):
                    self.kaEntry = kaEntry
                    self.mode = mode
                    wx.Dialog.__init__(self, parent, -1,
                        style = wx.RESIZE_BORDER | wx.DEFAULT_DIALOG_STYLE | wx.CLOSE_BOX | wx.TAB_TRAVERSAL,
                        name = plugin.text.kaFrameTitle
                    )
                    self.SetIcon(plugin.info.icon.GetWxIcon())
                    self.panel = parent

                def MakeModal(self, modal=True):
                    if modal and not hasattr(self, '_disabler'):
                        self._disabler = wx.WindowDisabler(self)
                    if not modal and hasattr(self, '_disabler'):
                        del self._disabler

                def ShowAddModKeepaliveDlg(self):
                    text = plugin.text
                    self.SetTitle(text.kaFrameTitle)
                    mainSizer = wx.BoxSizer(wx.VERTICAL)

                    helpLbl = wx.StaticText(self, -1, text.kaHelpAddModifyEntry)
                    startLbl=wx.StaticText(self, -1, text.kaStartTime + ":")
                    endLbl=wx.StaticText(self, -1, text.kaEndTime + ":")
                    spinBtn1 = wx.SpinButton(self, -1, wx.DefaultPosition, (-1, 22), wx.SP_VERTICAL)
                    spinBtn2 = wx.SpinButton(self, -1, wx.DefaultPosition, (-1, 22), wx.SP_VERTICAL)
                    startTimeCtrl = eg.TimeCtrl(self, -1, format="24HHMM", name="startTime", spinButton=spinBtn1)
                    endTimeCtrl = eg.TimeCtrl(self, -1, value=self.kaEntry.endTime, format="24HHMM", name="endTime", spinButton=spinBtn2)

                    timeSizer = wx.BoxSizer(wx.HORIZONTAL)
                    timeSizer.Add(startLbl, 0, wx.ALIGN_CENTRE | wx.ALL)
                    timeSizer.Add(startTimeCtrl, 0, wx.ALIGN_CENTRE | wx.ALL)
                    timeSizer.Add(spinBtn1, 0, wx.ALIGN_CENTRE | wx.ALL)
                    timeSizer.Add((50, 1))
                    timeSizer.Add(endLbl, 0, wx.ALIGN_CENTRE | wx.ALL)
                    timeSizer.Add(endTimeCtrl, 0, wx.ALIGN_CENTRE | wx.ALL)
                    timeSizer.Add(spinBtn2, 0, wx.ALIGN_CENTRE | wx.ALL)

                    wdSizer = wx.GridSizer(rows=1, cols=7, vgap=10, hgap=10)
                    weekdayCheckbox = []
                    for i, weekday in enumerate(text.kaWeekday):
                        weekdayCheckbox.append(wx.CheckBox(self, -1, label=weekday, name=weekday))
                        wdSizer.Add(weekdayCheckbox[i])

                    okBtn = wx.Button(self, wx.ID_OK)
                    okBtn.SetLabel(text.ok)
                    okBtn.SetDefault()
                    cancelBtn = wx.Button(self, wx.ID_CANCEL)
                    cancelBtn.SetLabel(text.cancel)
                    btnsizer = wx.StdDialogButtonSizer()
                    btnsizer.AddButton(okBtn)
                    btnsizer.AddButton(cancelBtn)
                    btnsizer.Realize()

                    mainSizer.Add((1,20))
                    mainSizer.Add(helpLbl,1,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
                    mainSizer.Add((1,20))
                    mainSizer.Add(timeSizer,1,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
                    mainSizer.Add((1,20))
                    mainSizer.Add(wdSizer,1,wx.LEFT|wx.RIGHT|wx.EXPAND,10)
                    mainSizer.Add((1,5))
                    line = wx.StaticLine(self, -1, size=(20,-1),pos = (200,0), style=wx.LI_HORIZONTAL)
                    mainSizer.Add(line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM,5)
                    mainSizer.Add(btnsizer, 0, wx.EXPAND|wx.RIGHT, 10)
                    mainSizer.Add((1,5))
                    self.SetSizer(mainSizer)
                    mainSizer.Fit(self)
                    self.CenterOnParent()
                    self.SetMinSize(self.GetSize())

                    # data
                    startTimeCtrl.SetValue(self.kaEntry.startTime)
                    endTimeCtrl.SetValue(self.kaEntry.endTime)
                    for i, cb in enumerate(weekdayCheckbox):
                        cb.SetValue(self.kaEntry.weekday[i])

                    # finalize
                    mainSizer.Layout()
                    self.MakeModal(True)
                    self.SetFocus()
                    self.Show()

                    # evt handling
                    def onClose(evt):
                        self.MakeModal(False)
                        self.GetParent().GetParent().Raise()
                        self.Destroy()
                    self.Bind(wx.EVT_CLOSE, onClose)

                    def onCancel(evt):
                        self.Close()
                    cancelBtn.Bind(wx.EVT_BUTTON, onCancel)

                    def onOK(evt):
                        self.kaEntry.startTime = startTimeCtrl.GetValue()
                        self.kaEntry.endTime = endTimeCtrl.GetValue()
                        for i, cb in enumerate(weekdayCheckbox):
                            self.kaEntry.weekday[i] = cb.GetValue()
                        self.panel.kaAddModCallback(self.mode, self.kaEntry)
                        self.Close()
                    okBtn.Bind(wx.EVT_BUTTON, onOK)


        monitorProcessListMc = cpy(monProcList) # deep copy! otherwise changes are not detected by EG framework (until EG 4.1, fixed in later releases)!
        keepaliveSchedule = cpy(kaSchedule)

        plugin = self
        text = self.text
        panel = eg.ConfigPanel(self, resizable=True)

        timerPanel = TimerPanel()
        self.timerPanel = timerPanel
        applPanel = ApplPanel()
        processPanel = ProcessPanel()
        keepAlivePanel = KeepAlivePanel()

        tableSizer = wx.GridBagSizer(5, 5)
        rowCount = 0
        tableSizer.Add(timerPanel.BuildPanel(), (rowCount,0), flag=wx.EXPAND)
        rowCount += 1
        tableSizer.Add(applPanel.BuildPanel(), (rowCount,0), flag=wx.EXPAND)
        tableSizer.AddGrowableRow(rowCount)
        rowCount += 1
        tableSizer.Add(processPanel.BuildPanel(), (rowCount,0), flag=wx.EXPAND)
        tableSizer.AddGrowableRow(rowCount)
        rowCount += 1
        tableSizer.Add(keepAlivePanel.BuildPanel(), (rowCount,0), flag=wx.EXPAND)
        tableSizer.AddGrowableRow(rowCount)
        rowCount += 1

        panel.sizer.Add(tableSizer, 1, flag=wx.EXPAND)

        applPanel.onRefreshApplButton(wx.CommandEvent())
        processPanel.onRefreshProcButton(wx.CommandEvent())
        keepAlivePanel.onKaRefreshButton(wx.CommandEvent())
        panel.kaAddModCallback = keepAlivePanel.AddModifyKaEntry

        while panel.Affirmed():
            standbyTime = timerPanel.standbyTimeCtrl.GetValue()
            standbyTimePending = timerPanel.standbyTimePendingCtrl.GetValue()
            standbyTimeAfterWakeUp = timerPanel.standbyTimeAfterWakeUpCtrl.GetValue()
            panel.SetResult(
                standbyTime,
                standbyTimePending,
                standbyTimeAfterWakeUp,
                monitorProcessListMc,
                keepaliveSchedule
            )

    @eg.LogIt
    def OnComputerSuspend(self, suspendType):
        self.FinishThreads()

    @eg.LogIt
    def OnComputerResume(self, suspendType):
        self.triggered = False
        if self.started:
            self.StartThreads()
            self.threadStandby.TriggerTimer(self.standbyTimeAfterWakeUp)
            return True
        else:
            return False

    @eg.LogIt
    def TriggerTimer(self, time):
        if self.threadStandby:
            self.threadStandby.TriggerTimer(time)

    @eg.LogIt
    def TriggerTimerAndForceTime(self, time):
        if self.threadStandby:
            self.threadStandby.TriggerTimerAndForceTime(time)

    @eg.LogIt
    def DisableStandby(self):
        if self.threadStandby:
            self.threadStandby.DisableStandby()

    @eg.LogIt
    def OSDCancel(self):
        if self.countDownOSD:
            self.countDownOSD.OSDCancel()
            return True
        else:
            return False


    class AppEntry:
        """Defines an entry of the applicationCounters list"""

        def __init__(self):
            self.counter = 0
            self.releaseTime = -1.0
            self.resetAfterStandby = True

    class CounterStatus:
        """Return object for the SetCounter method"""

        def __init__(self, changed = False, enabled=True):
            self.changed = changed
            self.enabled = enabled

        def setChanged(self, changed=True):
            self.changed = changed

        def setEnabled(self, enabled=True):
            self.enabled = enabled

        def getChanged(self):
            return self.changed

        def getEnabled(self):
            return self.enabled

    @eg.LogItWithReturn
    def SetCounter(
        self,
        applicationName,
        mode,
        maxTime=-1.0,
        resetAfterStandby=True
    ):
        """
        Adds or updates an entry in the applicationCounters list
        Returns a CounterStatus object indicating the action taken.
        # mode:= 0     Set counter to 1
        # mode:= 1     Increment counter
        # mode:= 2     Decrement counter
        # mode:= 3     Reset counter
        """
        status = self.CounterStatus()

        if (not applicationName or applicationName != ""):
            exists = self.applicationCounters.has_key(applicationName)
            if exists:
                entry = self.applicationCounters[applicationName]
            else:
                entry = self.AppEntry()

            entry.resetAfterStandby = resetAfterStandby

            if mode == CNT_MODE_0_SET:
                if entry.counter == 0:
                    status.setChanged()
                status.setEnabled(False)
                entry.counter = 1
            elif mode == CNT_MODE_1_INCR:
                if entry.counter == 0:
                    status.setChanged()
                status.setEnabled(False)
                entry.counter += 1
            elif mode == CNT_MODE_2_DECR and entry.counter > 0:
                entry.counter -= 1
                if entry.counter != 0:
                    status.setEnabled(False)
                else:
                    status.setChanged()
            elif mode == CNT_MODE_3_RESET:
                if entry.counter > 0:
                    status.setChanged()
                entry.counter = 0

            setReleaseTime = False

            if (mode == CNT_MODE_0_SET or mode == CNT_MODE_1_INCR):
                if maxTime >= 0.0:
                    releaseTime = time() + maxTime
                    if (releaseTime > entry.releaseTime):
                        entry.releaseTime = releaseTime
                        setReleaseTime = True
                elif mode == CNT_MODE_0_SET:
                    entry.releaseTime = -1.0
                    setReleaseTime = True

            elif status.getChanged():
                setReleaseTime = True
                entry.releaseTime = -1.0    # -1 = ready to trigger

            if (exists or entry.counter > 0):
                self.applicationCounters[applicationName] = entry

            if setReleaseTime:
                self.UpdateReleaseTime()

        return status

    @eg.LogItWithReturn
    def UpdateReleaseTime(self, lock=True):
        """calculates the time of the next block release and reprograms the threadForce accordingly"""

        if not self.started or not self.threadForce:
            return

        threadForce = self.threadForce

        if lock:
            threadForce.Hold()

        now = time()
        nextTime = -1.0

        for name, entry in self.applicationCounters.iteritems():
            releaseTime = entry.releaseTime
            if releaseTime >= 0.0 and entry.counter > 0:
                if releaseTime - now <= 0:
                    entry.counter = 0
                    entry.releaseTime = -1.0
                    self.CheckAndEnable()
                    self.TriggerEvent(EVT_RELEASE + "." + name)
                else:
                    delta = releaseTime - now
                    if nextTime < 0.0 or delta < nextTime:
                        nextTime = delta
        if nextTime > 0.0:
            threadForce.SetTime(nextTime, lock)

    def GetApplicationNames(self):
        self.applicationNames.sort(lambda a,b: cmp(a.lower(), b.lower()))
        return self.applicationNames

    def GetNextTriggerTime(self):
        if self.threadStandby:
            return self.threadStandby.GetNextTriggerTime()
        else:
            return 0.0

    def AddApplicationName(self, applicationName):
        if not applicationName in self.applicationNames:
            self.applicationNames.append(applicationName)

    @eg.LogItWithReturn
    def CheckAndEnable(self, time = 0.0, afterStandby = False):
        """
        Determines if standby trigger is enabled or not.
        The trigger will be enabled if all applicationCounter entries have counter == 0. 
        """
        if not self.threadStandby:
            return False
        enable = True
        for entry in self.applicationCounters.itervalues():
            if afterStandby and entry.resetAfterStandby:
                entry.counter = 0
                entry.releaseTime = -1.0
            if entry.counter != 0:
                enable = False
                break
        if enable and self.started:
            self.threadStandby.EnableStandby(time)
        return enable

    @eg.LogIt
    def InitKeepAliveSchedule(self, keepAliveSchedule):
        self.keepAliveSchedule = keepAliveSchedule
        try:
            self.kaScheduleLock.acquire()
            for kaEntry in keepAliveSchedule:
                isActive, currStart, currEnd, nextStart, nextEnd = kaEntry.GetExecutionStatus()
                if isActive:
                    self.AddScheduledTask(currStart, kaEntry)
                else:
                    self.AddScheduledTask(nextStart, kaEntry)
        finally:
            self.kaScheduleLock.release()

    @eg.LogIt
    def KeepAlivePeriodChange(self, kaEntry, cancel=False):
        """callback called from eg.scheduler"""
        #eg.PrintDebugNotice("KeepAlivePeriodChange kaEntry=" + str(kaEntry))
        try:
            self.kaScheduleLock.acquire()
            isActive, currStart, currEnd, nextStart, nextEnd = kaEntry.GetExecutionStatus()
            if cancel:
                if isActive:
                    self.TriggerEvent(EVT_KEEPALIVE_ENDED, kaEntry)
            else:
                if isActive:
                    self.TriggerEvent(EVT_KEEPALIVE_STARTED, kaEntry)
                    self.AddScheduledTask(currEnd, kaEntry)
                else:
                    self.TriggerEvent(EVT_KEEPALIVE_ENDED, kaEntry)
                    self.AddScheduledTask(nextStart, kaEntry)

            keepAlive = False
            for entry in self.keepAliveSchedule:
                isActive = entry.GetExecutionStatus()[0]
                if isActive:
                    keepAlive = True
                    break
            if not keepAlive:
                self.TriggerEvent(EVT_ALL_KEEPALIVE_ENDED)

            # housekeeping
            try:
                self.keepAliveTasks.pop(kaEntry) # remove from dict
            except Exception, exc:
                print "keepAliveTasks.pop(kaEntry) failed", exc
        finally:
            self.kaScheduleLock.release()


    @eg.LogIt
    def AddScheduledTask(self, datetime, kaEntry):
        """Adds a scheduled task to the eg.scheduler"""
        #eg.PrintDebugNotice("AddScheduledTask for StandbyControl.KeepAliveEntry. Wakeup=" + str(datetime) + ", kaEntry=" + str(kaEntry))
        entry = cpy(kaEntry)
        task = eg.scheduler.AddTaskAbsolute(mktime(datetime.timetuple()), self.KeepAlivePeriodChange, entry)
        self.keepAliveTasks[entry] = task


    def StopKeepAliveSchedule(self):
        if self.started:
            activeTasks = False
            for kaEntry, task in self.keepAliveTasks.items():
                try:
                    eg.scheduler.CancelTask(task)
                except Exception, exc:
                    print "CancelTask failed", exc
                isActive = kaEntry.GetExecutionStatus()[0]
                if isActive:
                    activeTasks = True
                # make sure we send the same amount of 'Stop' events than 'Start' events
                self.KeepAlivePeriodChange(kaEntry, cancel=True)
            if activeTasks:
                self.TriggerEvent(EVT_ALL_KEEPALIVE_ENDED)

            self.keepAliveTasks = {}


class TriggerStandbyTimer(eg.ActionClass):

    @eg.LogItWithReturn
    def __call__(
        self,
        force,
        useDefault,
        standbyTime
    ):

        plugin = self.plugin

        if not plugin.started:
            self.PrintError(plugin.text.notStarted)
            return False

        if useDefault:
            standbyTime = plugin.standbyTimeDefault

        plugin.appCtrLock.acquire()
        try:
            if force:
                plugin.TriggerTimerAndForceTime(standbyTime)
            else:
                plugin.TriggerTimer(standbyTime)
        finally:
            plugin.appCtrLock.release()

        return True



    def Configure(self, force=False, useDefault=True, standbyTime=600.0):

        def onCheckBox(event):
            enable = not useDefaultCtrl.GetValue()
            standbyTimeCtrl.Enable(enable)

            event.Skip()

        text = self.text
        panel = eg.ConfigPanel(self)

        #showRemaingLoopsText

        forceCtrl = wx.CheckBox(panel, -1, text.forceCheckBox)
        forceCtrl.SetValue(force)

        useDefaultCtrl = wx.CheckBox(panel, -1, text.defaultCheckBox)
        useDefaultCtrl.SetValue(useDefault)
        useDefaultCtrl.Bind(wx.EVT_CHECKBOX, onCheckBox)

        standbyTimeCtrl = panel.SpinNumCtrl(standbyTime, min=0, max=99999, fractionWidth=0, integerWidth=5)

        onCheckBox(wx.CommandEvent())

        panel.AddLine(forceCtrl)
        panel.AddLine(useDefaultCtrl)
        panel.AddLine(text.standbyTime, standbyTimeCtrl)

        while panel.Affirmed():
            force = forceCtrl.GetValue()
            useDefault = useDefaultCtrl.GetValue()
            standbyTime = standbyTimeCtrl.GetValue()
            panel.SetResult(force, useDefault, standbyTime)


class InhibitStandbyByApplication(eg.ActionClass):

    @eg.LogItWithReturn
    def __call__(
        self ,
        applicationName = None ,
        countUp = True ,
        triggerMode = TM_STBY_0_DONT_TRIGGER ,
        standbyTime = 600.0 ,
        enableRelease = False ,
        maxTime = -1.0 ,
        resetAfterStandby = True ,
    ):
        # triggerMode == 0:    doNotTrigger
        # triggerMode == 1:    triggerDefault
        # triggerMode == 2:    triggerSpecialValue

        plugin = self.plugin

        if not plugin.started:
            eg.PrintError(plugin.text.notStarted)
            return False

        try:
            plugin.appCtrLock.acquire()
            plugin.DisableStandby() # -> threadStandby.DisableStandby()

            if countUp:
                counterMode = CNT_MODE_1_INCR
            else:
                counterMode = CNT_MODE_0_SET

            if not enableRelease:
                maxTime = -1.0

            plugin.SetCounter(applicationName, counterMode, maxTime * 60, resetAfterStandby)

            if triggerMode != TM_STBY_0_DONT_TRIGGER:
                if triggerMode == TM_STBY_1_STANDBY_DEFAULT:
                    standbyTime = plugin.standbyTimeDefault
                plugin.TriggerTimer(standbyTime)
        finally:
            plugin.appCtrLock.release()

        return True


    def Configure(
        self,
        applicationName = None ,
        countUp = False ,
        triggerMode = 0 ,
        standbyTime = 600.0 ,
        enableRelease = False ,
        maxTime = 0.0 ,
        resetAfterStandby = True
    ):

        def onRadioButton(event):
            enable = triggerSpecialCtrl.GetValue()
            standbyTimeCtrl.Enable(enable)

            event.Skip()


        def onCheckBox(event):
            enable = releaseCheckBoxCtrl.GetValue()
            releaseTimeCtrl.Enable(enable)

            event.Skip()


        text = self.text
        plugin = self.plugin

        if applicationName:
            plugin.AddApplicationName(applicationName)

        panel = eg.ConfigPanel(self)

        if not applicationName:
            applicationName = plugin.lastApplicationName


        #define controls

        applicationNameCtrl = wx.ComboBox(
            panel,
            -1,
            value=applicationName,
            choices=plugin.GetApplicationNames(),
            size=(200,-1)
        )

        releaseCheckBoxCtrl = wx.CheckBox(panel, -1, text.releaseCheckBox)
        releaseCheckBoxCtrl.SetValue(enableRelease)
        releaseCheckBoxCtrl.Bind(wx.EVT_CHECKBOX, onCheckBox)

        maxTime = maxTime
        releaseTimeCtrl = panel.SpinNumCtrl(maxTime, min=0, max=99999, fractionWidth=0, integerWidth=5)

        countUpCheckBoxCtrl = wx.CheckBox(panel, -1, text.countUpCheckBox)
        countUpCheckBoxCtrl.SetValue(countUp)

        resetCheckBoxCtrl = wx.CheckBox(panel, -1, text.reserAfterStandby)
        resetCheckBoxCtrl.SetValue(resetAfterStandby)

        doNotTriggerCtrl = wx.RadioButton(panel, -1, text.doNotTrigger, style = wx.RB_GROUP)
        doNotTriggerCtrl.SetValue(triggerMode == 0)
        doNotTriggerCtrl.Bind(wx.EVT_RADIOBUTTON, onRadioButton)

        useDefaultCtrl = wx.RadioButton(panel, -1, text.defaultCheckBox)
        useDefaultCtrl.SetValue(triggerMode == 1)
        useDefaultCtrl.Bind(wx.EVT_RADIOBUTTON, onRadioButton)

        triggerSpecialCtrl = wx.RadioButton(panel, -1, text.triggerSpecial)
        triggerSpecialCtrl.SetValue(triggerMode == 2)
        triggerSpecialCtrl.Bind(wx.EVT_RADIOBUTTON, onRadioButton)

        standbyTimeCtrl = panel.SpinNumCtrl(standbyTime, min=0, max=99999, fractionWidth=0, integerWidth=5)

        #paint
        gridSizer = wx.GridBagSizer(10, 5)

        rowCount = 0
        gridSizer.Add(
            wx.StaticText(panel, -1, text.applicationName),
            (rowCount, 0),
            flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL
        )
        gridSizer.Add(applicationNameCtrl, (rowCount, 1), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)

        rowCount += 1
        gridSizer.Add(releaseCheckBoxCtrl, (rowCount, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(releaseTimeCtrl,     (rowCount, 1), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)

        panel.sizer.Add(gridSizer)

        panel.sizer.Add(wx.Size(0,13))
        panel.sizer.Add(countUpCheckBoxCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
        panel.sizer.Add(wx.Size(0,18))

        panel.sizer.Add(resetCheckBoxCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
        panel.sizer.Add(wx.Size(0,15))

        sb = wx.StaticBox(panel, -1, text.standbyTime)
        boxSizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        gridSizer = wx.GridBagSizer(5, 5)
        rowCount = 0
        gridSizer.Add(doNotTriggerCtrl, (rowCount, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        rowCount += 1
        gridSizer.Add(useDefaultCtrl, (rowCount, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        rowCount += 1
        gridSizer.Add(triggerSpecialCtrl, (rowCount, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(standbyTimeCtrl, (rowCount, 1), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        boxSizer.Add(gridSizer, flag=wx.TOP, border=5)
        panel.sizer.Add(boxSizer)

        onRadioButton(wx.CommandEvent())
        onCheckBox(wx.CommandEvent())

        while panel.Affirmed():
            applicationName = applicationNameCtrl.GetValue()
            enableRelease = releaseCheckBoxCtrl.GetValue()
            maxTime = releaseTimeCtrl.GetValue()
            countUp = countUpCheckBoxCtrl.GetValue()
            triggerMode = useDefaultCtrl.GetValue() + triggerSpecialCtrl.GetValue() * 2
            standbyTime = standbyTimeCtrl.GetValue()
            resetAfterStandby = resetCheckBoxCtrl.GetValue()
            panel.SetResult(
                applicationName,
                countUp,
                triggerMode,
                standbyTime,
                enableRelease,
                maxTime,
                resetAfterStandby
            )

        plugin.lastApplicationName = applicationName
        plugin.AddApplicationName(applicationName)


class EnableStandbyByApplication(eg.ActionClass):

    @eg.LogItWithReturn
    def __call__(
        self,
        applicationName = None ,
        resetCounter = True ,
        triggerModePending = TM_PENDING_1_PENDING_DEFAULT ,
        standbyTimePending = 60.0 ,
        triggerModeStandby = TM_STBY_0_DONT_TRIGGER,
        standbyTime = 600.0
    ):

        plugin = self.plugin

        if not plugin.started:
            eg.PrintError(plugin.text.notStarted)
            return False

        if resetCounter:
            counterMode = CNT_MODE_3_RESET
        else:
            counterMode = CNT_MODE_2_DECR

        try:
            plugin.appCtrLock.acquire()
            status = plugin.SetCounter(applicationName, counterMode)

            time = 0.0
            if status.getEnabled():
                if triggerModePending == TM_PENDING_0_DONT_TRIGGER:
                    time = plugin.GetNextTriggerTime()
                elif triggerModePending == TM_PENDING_1_PENDING_DEFAULT:
                    time = plugin.standbyTimePendingDefault
                elif triggerModePending == TM_PENDING_2_STANDBY_DEFAULT:
                    time = plugin.standbyTimeDefault
                elif triggerModePending == TM_PENDING_3_SPECIAL_VALUE:
                    time = standbyTimePending
            else:
                if triggerModeStandby != TM_STBY_0_DONT_TRIGGER:
                    if triggerModeStandby == TM_STBY_1_STANDBY_DEFAULT:
                        time = plugin.standbyTimeDefault
                    elif triggerModeStandby == TM_STBY_2_SPECIAL_VALUE:
                        time = standbyTime

            plugin.CheckAndEnable(time)
            plugin.TriggerTimer(time)
        finally:
            plugin.appCtrLock.release()

        return True


    def Configure(
        self,
        applicationName = None ,
        resetCounter = True ,
        modePending = TM_PENDING_0_DONT_TRIGGER ,
        standbyTimePending = 60.0 ,
        modeStandby = TM_STBY_0_DONT_TRIGGER,
        standbyTime = 600.0
    ):


        def onRadioButtonGroup1(event):
            enable = triggerSpecialPendingCtrl.GetValue()
            standbyTimePendingCtrl.Enable(enable)
            event.Skip()


        def onRadioButtonGroup2(event):
            enable = triggerSpecialCtrl.GetValue()
            standbyTimeCtrl.Enable(enable)
            event.Skip()


        text = self.text
        plugin = self.plugin

        if applicationName:
            plugin.AddApplicationName(applicationName)

        panel = eg.ConfigPanel(self)

        if not applicationName:
            applicationName = plugin.lastApplicationName

        applicationNameCtrl = wx.ComboBox(
            panel,
            -1,
            value=applicationName,
            choices=plugin.GetApplicationNames(),
            size=(200,-1)
        )

        #define controls

        resetCheckBoxCtrl = wx.CheckBox(panel, -1, text.resetCheckBox)
        resetCheckBoxCtrl.SetValue(resetCounter)

        doNotPendingCtrl = wx.RadioButton(panel, -1, text.doNotPending, style = wx.RB_GROUP)
        doNotPendingCtrl.SetValue(modePending == 0)
        doNotPendingCtrl.Bind(wx.EVT_RADIOBUTTON, onRadioButtonGroup1)

        usePendingCtrl = wx.RadioButton(panel, -1, text.pendingCheckBox)
        usePendingCtrl.SetValue(modePending == 1)
        usePendingCtrl.Bind(wx.EVT_RADIOBUTTON, onRadioButtonGroup1)

        useStandbyCtrl = wx.RadioButton(panel, -1, text.defaultCheckBox)
        useStandbyCtrl.SetValue(modePending == 2)
        useStandbyCtrl.Bind(wx.EVT_RADIOBUTTON, onRadioButtonGroup1)

        triggerSpecialPendingCtrl = wx.RadioButton(panel, -1, text.pendingSpecial)
        triggerSpecialPendingCtrl.SetValue(modePending == 3)
        triggerSpecialPendingCtrl.Bind(wx.EVT_RADIOBUTTON, onRadioButtonGroup1)

        standbyTimePendingCtrl = panel.SpinNumCtrl(standbyTimePending, min=5, max=99999, fractionWidth=0, integerWidth=5)


        doNotTriggerCtrl = wx.RadioButton(panel, -1, text.doNotTrigger, style = wx.RB_GROUP)
        doNotTriggerCtrl.SetValue(modeStandby == 0)
        doNotTriggerCtrl.Bind(wx.EVT_RADIOBUTTON, onRadioButtonGroup2)

        useDefaultCtrl = wx.RadioButton(panel, -1, text.defaultCheckBox)
        useDefaultCtrl.SetValue(modeStandby == 1)
        useDefaultCtrl.Bind(wx.EVT_RADIOBUTTON, onRadioButtonGroup2)

        triggerSpecialCtrl = wx.RadioButton(panel, -1, text.triggerSpecial)
        triggerSpecialCtrl.SetValue(modeStandby == 2)
        triggerSpecialCtrl.Bind(wx.EVT_RADIOBUTTON, onRadioButtonGroup2)

        standbyTimeCtrl = panel.SpinNumCtrl(standbyTime, min=0, max=99999, fractionWidth=0, integerWidth=5)


        #paint
        boxSizer = wx.BoxSizer(wx.HORIZONTAL)

        boxSizer.Add(wx.StaticText(panel, -1, text.applicationName), flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL, border=10)
        boxSizer.Add(applicationNameCtrl, flag=wx.ALIGN_CENTER_VERTICAL)

        panel.sizer.Add(boxSizer)

        panel.sizer.Add(wx.Size(0, 15))
        panel.sizer.Add(resetCheckBoxCtrl, flag=wx.ALIGN_CENTER_VERTICAL)
        panel.sizer.Add(wx.Size(0, 15))

        sbO = wx.StaticBox(panel, -1, text.standbyTime)
        boxSizerO = wx.StaticBoxSizer(sbO, wx.HORIZONTAL)

        sb = wx.StaticBox(panel, -1, text.pendingText)
        boxSizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        gridSizer = wx.GridBagSizer(5, 5)
        rowCount = 0
        gridSizer.Add(doNotPendingCtrl, (rowCount, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        rowCount += 1
        gridSizer.Add(usePendingCtrl, (rowCount, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        rowCount += 1
        gridSizer.Add(useStandbyCtrl, (rowCount, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        rowCount += 1
        gridSizer.Add(triggerSpecialPendingCtrl, (rowCount, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(standbyTimePendingCtrl, (rowCount, 1), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        boxSizer.Add(gridSizer, flag=wx.TOP, border=5)

        boxSizerO.Add(boxSizer, flag=wx.TOP, border=3)


        sb = wx.StaticBox(panel, -1, text.standbyText)
        boxSizer = wx.StaticBoxSizer(sb, wx.VERTICAL)

        gridSizer = wx.GridBagSizer(5, 5)
        rowCount = 0
        gridSizer.Add(doNotTriggerCtrl, (rowCount, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        rowCount += 1
        gridSizer.Add(useDefaultCtrl, (rowCount, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        rowCount += 1
        gridSizer.Add(triggerSpecialCtrl, (rowCount, 0), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(standbyTimeCtrl, (rowCount, 1), flag=wx.LEFT | wx.ALIGN_CENTER_VERTICAL)
        boxSizer.Add(gridSizer, flag=wx.TOP, border=5)

        boxSizerO.Add(boxSizer, flag=wx.TOP, border=3)
        panel.sizer.Add(boxSizerO)

        onRadioButtonGroup1(wx.CommandEvent())
        onRadioButtonGroup2(wx.CommandEvent())


        while panel.Affirmed():
            applicationName = applicationNameCtrl.GetValue()
            resetCounter = resetCheckBoxCtrl.GetValue()
            modePending = (usePendingCtrl.GetValue()
                + useStandbyCtrl.GetValue() * 2
                + triggerSpecialPendingCtrl.GetValue() * 3
            )
            standbyTimePending = standbyTimePendingCtrl.GetValue()
            modeStandby = useDefaultCtrl.GetValue() + triggerSpecialCtrl.GetValue() * 2
            standbyTime = standbyTimeCtrl.GetValue()
            panel.SetResult(applicationName, resetCounter, modePending, standbyTimePending, modeStandby, standbyTime)

        plugin.lastApplicationName = applicationName
        plugin.AddApplicationName(applicationName)


class WasTriggered(eg.ActionClass):

    @eg.LogItWithReturn
    def __call__(self):
        if not self.plugin.started:
            self.PrintError(self.plugin.text.notStarted)
            return False

        result = self.plugin.triggered
        self.plugin.triggered = False
        return result


class IsMonitoredProcessRunning(eg.ActionClass):

    @eg.LogItWithReturn
    def __call__(self):
        if not self.plugin.started:
            self.PrintError(self.plugin.text.notStarted)
            return False

        numberOfActiveProcesses = ProcessMonitorThread.GetActiveProcessCount(self.plugin, lock=True, logprint=True)
        return numberOfActiveProcesses != 0


class IsKeepAlive(eg.ActionClass):

    @eg.LogItWithReturn
    def __call__(self):
        if not self.plugin.started:
            self.PrintError(self.plugin.text.notStarted)
            return False

        keepAlive = False
        try:
            self.plugin.kaScheduleLock.acquire()
            for kaEntry in self.plugin.keepAliveSchedule:
                isActive = kaEntry.GetExecutionStatus()[0]
                if isActive:
                    keepAlive = True
                    break
        finally:
            self.plugin.kaScheduleLock.release()
        return keepAlive


class StandbyTimerThread(Thread):
    """
    This thread waits until it is enabled and then starts generating 'StandbyControl.Trigger' events.
    The time, when to trigger the next event, is controlled from external functions, like the actions 'Enable / Inhibit Standby'. 
    """
    def __init__(
        self,
        plugin,
        standbyTime,
        standbyTimePending
    ):
        Thread.__init__(self, name="StandbyTimerThread")
        self.plugin = plugin

        self.stbTimeDefault = standbyTime
        self.stbTime = standbyTime
        self.stbTimePendingDefault = standbyTimePending
        self.stbTimePending = standbyTimePending

        self.waitTime = standbyTime
        self.nextStandby = 0.0

        self.started = False
        self.enabled = True
        self.pending = False
        self.triggered = True
        self.getNewStatus = False
        self.abort = False

        self.lock = plugin.timerLock
        self.event = Event()

    @eg.LogItWithReturn
    def run(self):
        self.started = True
        self.event.clear()

        lock = self.lock
        try:
            lock.acquire()
            while not self.abort:
                if self.triggered:
                    if self.nextStandby == 0.0:
                        self.waitTime = self.stbTime
                    else:
                        delta = self.nextStandby - time()
                        if delta < self.stbTime:
                            self.waitTime = self.stbTime
                        else:
                            self.waitTime = delta
                    self.stbTime = self.stbTimeDefault
                    self.pending = False
                elif self.pending:
                    self.waitTime = self.stbTimePending
                    self.stbTimePending = self.stbTimePendingDefault
                    self.pending = False
                else:
                    self.waitTime = self.stbTimeDefault

                if not self.enabled and not self.triggered:
                    # 'pending' means that the thread is waiting for an 'EnableStandby' event.
                    self.pending = True

                self.triggered = False

                if self.pending:
                    lock.release()
                    self.event.wait()   # wait until external notification
                    lock.acquire()
                else:
                    self.nextStandby = time() + self.waitTime
                    lock.release()
                    self.event.wait(self.waitTime)
                    lock.acquire()
                    if not self.getNewStatus and self.enabled:
                        self._triggerStandby()
                        self.nextStandby = 0.0
                self.event.clear()
                self.getNewStatus = False

            self.started = False
        finally:
            lock.release()

        return True

    @eg.LogIt
    def _triggerStandby(self):
        self.plugin.TriggerEvent(EVT_TRIGGER)
        self.plugin.triggered = True  # Obacht. This is not the same as 'self.triggered' (...intended? or just to confuse the Chinese?)

    def _getLockAndNotify(self):
        if self.started:
            try:
                self.lock.acquire()
                self.getNewStatus = True
                self.event.set()
            except:
                self.lock.release()
                return False
            return True
        else:
            return False

    @eg.LogIt
    def Finish(self):
        if self._getLockAndNotify():
            try:
                self.abort = True
            finally:
                self.lock.release()
            return True
        else:
            return False

    @eg.LogIt
    def TriggerTimer(self, time):
        if time == 0.0:
            return False
        if self._getLockAndNotify():
            try:
                self.triggered = True
                self.stbTime = time
            finally:
                self.lock.release()
            return True
        else:
            return False

    @eg.LogIt
    def TriggerTimerAndForceTime(self, time):
        if self._getLockAndNotify():
            try:
                self.nextStandby = 0.0
                self.triggered = True
                self.stbTime = time
                if time == 0:
                    if self.enabled:
                        self._triggerStandby()
                    self.stbTime = self.stbTimeDefault
            finally:
                self.lock.release()
            return True
        else:
            return False

    @eg.LogIt
    def EnableStandby(self, setTime):
        if self._getLockAndNotify():
            try:
                if self.started:
                    self.enabled = True
                    if self.pending:
                        if setTime != 0.0:
                            self.stbTimePending = setTime
                        else:
                            self.stbTimePending = self.stbTimePendingDefault
            finally:
                self.lock.release()
            return True
        else:
            return False

    @eg.LogIt
    def DisableStandby(self):
        if self._getLockAndNotify():
            try:
                self.enabled = False
            finally:
                self.lock.release()
        else:
            return False

    def GetPendingStatus(self):
        return self.pending

    def GetNextTriggerTime(self):
        standby = 0.0
        if self._getLockAndNotify():
            try:
                standby = self.nextStandby - time()
                if standby < 0.0:
                    standby = 0.0
                else:
                    standby = int(standby * 10) / 10.0       # 0.1 s accuracy
            finally:
                self.lock.release()
        return standby


class ForceReleaseThread(Thread):
    """
    This thread is schedules Standby.Trigger events of standby blockers with 'force release' time set.
    """
    def __init__(self, plugin):
        Thread.__init__(self, name="ForceReleaseThread")
        self.plugin = plugin
        self.timeDelta = -1.0
        self.nextReleaseTime = -1.0
        self.started = False
        self.abort = False
        self.event = Event()
        self.lock = plugin.forceThreadLock

    @eg.LogItWithReturn
    def run(self):
        self.started = True
        lock = self.lock
        try:
            lock.acquire()
            while not self.abort:
                waitTime = self.timeDelta
                self.nextReleaseTime = time() + waitTime
                if waitTime <= 0.0:
                    lock.release()
                    self.event.wait()
                    lock.acquire()
                    self.event.clear()
                else:
                    lock.release()
                    self.event.wait(waitTime)
                    try:
                        self.plugin.appCtrLock.acquire() # acquire appCtrLock not before releasing own lock (otherwise: deadlock)
                        self.plugin.UpdateReleaseTime(lock=True)
                    finally:
                        self.plugin.appCtrLock.release()
                    lock.acquire()
                    self.event.clear()
            self.started = False
        finally:
            lock.release()
        return True

    def _getLockAndNotify(self):
        if self.started:
            try:
                self.lock.acquire()
                self.event.set()
            except:
                self.lock.release()
                return False
            return True
        else:
            return False

    @eg.LogIt
    def Finish(self):
        if self._getLockAndNotify():
            try:
                self.abort = True
            finally:
                self.lock.release()
            return True
        else:
            return False

    @eg.LogIt
    def Hold(self):
        """tells the thread to wait forever"""
        if self._getLockAndNotify():
            try:
                self.timeDelta = -1.0
            finally:
                self.lock.release()
            return True
        else:
            return False

    @eg.LogIt
    def SetTime(self, time, lock=True):
        """sets the next release time"""
        if not lock:
            self.timeDelta = time
            return True
        elif self._getLockAndNotify():
            try:
                self.timeDelta = time
            finally:
                self.lock.release()
            return True
        else:
            return False

    def GetNextReleaseTime(self):
        delta = self.nextReleaseTime - time()
        if delta < 0.0:
            delta = 0
        else:
            delta = int(delta)       # 1 s accuracy
        return(delta)


class ProcessMonitorThread(Thread):
    """
    This thread monitors creation and termination of OS processes and fires events for monitored processes.
    """

    @classmethod
    def InitProcessesMap(cls, plugin, lock=True):
        """Builds the list of all running processes"""
        try:
            if lock:
                CoInitialize()
                plugin.processLock.acquire()

            plugin.allProcessesMap = {}
            WMI = GetObject('winmgmts:{impersonationLevel=impersonate}')
            objectSet = WMI.ExecQuery('select * from Win32_Process')

            for obj in objectSet:
                name = obj.Caption
                if name == 'System Idle Process':
                    continue
                elif name == 'System':
                    continue
                elif name in plugin.allProcessesMap:
                    plugin.allProcessesMap[name] += 1
                else:
                    plugin.allProcessesMap[name] = 1

            return WMI
        finally:
            if lock:
                CoUninitialize()
                plugin.processLock.release()

    @classmethod
    def GetActiveProcessCount(cls, plugin, lock=True, logprint=False):
        try:
            if lock:
                plugin.processLock.acquire()

            numberOfActiveProcesses = 0
            for name in plugin.allProcessesMap:
                if name.lower() in plugin.monitorProcessList:
                    count = plugin.allProcessesMap[name]
                    if count > 0:
                        numberOfActiveProcesses += count
                        if logprint:
                            if count == 1:
                                print name, " is running"
                            else:
                                print name, " is running ", count, " times"
            if logprint:
                print "numberOfActiveProcesses = ", numberOfActiveProcesses
        finally:
            if lock:
                plugin.processLock.release()

        return numberOfActiveProcesses


    def __init__(self, plugin, waitTime=5.0):
        Thread.__init__(self, name="ProcessMonitorThread")
        self.abort = False
        self.plugin = plugin
        self.waitTime = waitTime
        self.event = Event()
        self.lock = plugin.processLock

    def _trigger(self, name, created, forceTrigger=False):
        plugin = self.plugin
        lname = name.lower()
        if lname in plugin.monitorProcessList:
            count = plugin.allProcessesMap[name]
            if count == 0 or (count == 1 and created) or forceTrigger:
                pos = lname.rfind('.')
                suffix = lname[pos + 1:]
                if suffix == 'exe':
                    name = name[:pos]
                name = name.replace('.', '_')
                if count == 0:
                    event = EVT_TERMINATED
                else:
                    event = EVT_CREATED
                plugin.TriggerEvent(event + "." + name)
                plugin.TriggerEvent(EVT_MON_PROC_CHANGED) # un-indent this line if all changes shall be notified

            if count == 0:
                numberOfActiveProcesses = ProcessMonitorThread.GetActiveProcessCount(plugin, lock=False, logprint=False)
                if numberOfActiveProcesses == 0:
                    plugin.TriggerEvent(EVT_ALL_MON_PROC_TERMINATED)

    @eg.LogItWithReturn
    def run(self):

        lock = self.lock
        plugin = self.plugin
        try:
            CoInitialize()
            lock.acquire()

            WMI = self.InitProcessesMap(plugin, lock=False)
            for name in plugin.allProcessesMap:
                self._trigger(name, created=True, forceTrigger=True)

            query = ("SELECT * FROM __InstanceOperationEvent WITHIN " +
                      str(self.waitTime) +
                      " WHERE TargetInstance ISA 'Win32_Process'")

            eventSource = WMI.ExecNotificationQuery(query)

            while not self.abort:
                lock.release()
                lock.acquire()
                try:
                    event = eventSource.NextEvent(500)
                except:
                    continue

                typ = event.Path_.Class
                name = event.TargetInstance.Name
                incr = 0
                if   typ == '__InstanceCreationEvent':
                    #print "__InstanceCreationEvent name = ", name
                    incr = 1
                    created = True
                elif typ == '__InstanceDeletionEvent':
                    #print "__InstanceDeletionEvent name = ", name
                    incr = -1
                    created = False
                else:
                    continue

                if name in plugin.allProcessesMap:
                    plugin.allProcessesMap[name] += incr
                elif incr > 0:
                    plugin.allProcessesMap[name] = incr
                else:
                    plugin.allProcessesMap[name] = 0

                self._trigger(name, created)

        finally:
            lock.release()
            CoUninitialize()

    @eg.LogIt
    def Terminate(self):
        try:
            self.lock.acquire()
            self.abort = True
            self.event.set()

            plugin = self.plugin
            for name, count in plugin.allProcessesMap.items():
                if count > 0:
                    plugin.allProcessesMap[name] = 0
                    self._trigger(name, created=False)
        finally:
            self.lock.release()


class Suspend(eg.ActionClass):

    @eg.LogItWithReturn
    def __call__(self):
        plugin = self.plugin
        plugin.OnComputerSuspend(None)


class Resume(eg.ActionClass):

    @eg.LogItWithReturn
    def __call__(self):
        plugin = self.plugin
        plugin.OnComputerResume(None)


class KeepAliveEntry:
    """
    Defines one entry in the keep alive schedule.
    An entry consists of a startTime, an endTime and a list of seven weekdays, when the entry shall be active
    """

    def __init__(self,
        startTime = None,
        endTime = None,
        weekday = [True] * 7
    ):
        if startTime is None:
            self.startTime = str(dt.now())[11:16] # cannot be done as constructor arg, it's not realtime then
        else:
            self.startTime = startTime

        if endTime is None:
            self.endTime = str(dt.now())[11:16]
        else:
            self.endTime = endTime

        self.weekday = weekday

    def GetDurationInSecs(self):
        t1 = dt.strptime(self.startTime, "%H:%M") # datetime
        t2 = dt.strptime(self.endTime, "%H:%M")
        secs = (t2 - t1).seconds # datetime.timedelta().seconds
        if secs <= 0:
            secs += 24 * 60 * 60
        return secs

    def Get_HHMM_DurationStr(self):
        secs = self.GetDurationInSecs()
        hh = secs / 3600
        mm = (secs - 3600 * hh) / 60
        return '%02d:%02d' % (hh, mm)

    @eg.LogItWithReturn
    def GetExecutionStatus(self):
        """Returns a tuple of (isActive, currStart, currEnd, nextStart, nextEnd)"""
        # some lines borrowed from SchedulGhost - nice algorithm!
        now = dt.now()
        nowDay = now.weekday()
        startTime = dt.strptime(self.startTime, "%H:%M").time()
        durationSecs = self.GetDurationInSecs()
        weekdaysLower = []
        weekdaysLarger = []
        for wd in range(7):
            if self.weekday[wd]:
                if wd < nowDay or (wd == nowDay and now.time() >= startTime):
                    weekdaysLower.append(wd)
                else:
                    weekdaysLarger.append(wd)

        # calculate nextStart, nextEnd
        delta = -1
        nextStart = nextEnd = None
        if len(weekdaysLarger) > 0:
            delta = weekdaysLarger[0] - nowDay
        elif len(weekdaysLower) > 0:
            delta = 7 + weekdaysLower[0] - nowDay
        if delta >= 0:
            nextStart = dt.combine(now.date() + td(days=delta), startTime)
            nextEnd = nextStart + td(seconds=durationSecs)

        # calculate isActive, currStart, currEnd
        isActive = False
        currStart = currEnd = None
        if nowDay in weekdaysLower:
            currStart = dt.combine(now.date(), startTime)
        elif (nowDay-1) % 7 in weekdaysLower:
            currStart = dt.combine(now.date() - td(days=1), startTime)
        if currStart is not None:
            currEnd = currStart + td(seconds=durationSecs)
            if currStart <= now and now < currEnd:
                isActive = True
            else:
                currStart = currEnd = None

        #eg.PrintDebugNotice("GetExecutionStatus: isActive=" + str(isActive) + ", currStart=" + str(currStart) + ", currEnd=" + str(currEnd) + ", nextStart=" + str(nextStart) + ", nextEnd=" + str(nextEnd))
        return (isActive, currStart, currEnd, nextStart, nextEnd)

    def __str__(self):
        return "(" + str(self.startTime) + ", " + str(self.endTime) + ", " + str(self.weekday) + ")"

    def __repr__(self):
        return str(self)



seeRef = "See help page on plugin configuration for more information."

ACTIONS = (
    (InhibitStandbyByApplication, "InhibitStandbyByApplication", "Inhibit Standby",
        "Increments the counter for a standby blocking application. "
        "Optionally, the number of inhibits can be counted. "+seeRef, None),
    (EnableStandbyByApplication, "EnableStandbyByApplication", "Enable Standby",
        "Decrements or resets the counter for a standby blocking application. "+seeRef, None),
    (TriggerStandbyTimer, "TriggerStandbyTimer", "Trigger Standby Timer",
        "A StandbyControl.Trigger event is fired after the specified amount of time and in case that standby "
        "is not inhibited by a standby blocker. "+seeRef, None),
    (WasTriggered, "WasTriggered", "Was Triggered",
        "Returns True if TriggerStandby event was fired before. "+seeRef, None),

    (CountDownOSD, "CountDownOSD", "OSD Count Down",
        "On Screen Display of a message with the option of a count down. "+seeRef, None),
    (CancelOSDCountDown, "CancelOSDCountDown", "Cancel OSD Count Down",
        "Cancels the current OSD Count Down. "+seeRef, None),

    (IsMonitoredProcessRunning, "IsMonitoredProcessRunning", "Is Monitored Process Running",
        "Returns True if a process, defined in the monitor process list (plugin configuration), "
        "is currently active. "+seeRef, None),
    (IsKeepAlive, "IsKeepAlive", "Is Keep Alive",
        "Returns True if a Keep Alive entry, defined in the Keep Alive Schedule (plugin configuration), "
        "is currently active. "+seeRef, None)
)

EVT_TRIGGER                 = "Trigger"
EVT_RELEASE                 = "Release"
EVT_MON_PROC_CHANGED        = "MonitoredProcessesChanged"
EVT_CREATED                 = "Created"
EVT_TERMINATED              = "Terminated"
EVT_ALL_MON_PROC_TERMINATED = "AllMonitoredProcessesTerminated"
EVT_KEEPALIVE_STARTED       = "KeepAlivePeriodStarted"
EVT_KEEPALIVE_ENDED         = "KeepAlivePeriodEnded"
EVT_ALL_KEEPALIVE_ENDED     = "AllKeepAlivePeriodsEnded"

EVENT_LIST = (
    (EVT_TRIGGER,                   "Gets fired when the standby timer ends."),
    (EVT_RELEASE,                   "Gets fired when a Standby Blocking Counter has expired."),
    (EVT_MON_PROC_CHANGED,          "Gets fired when the status of a monitored process has changed."),
    (EVT_CREATED,                   "Gets fired when a monitored process has started."),
    (EVT_TERMINATED,                "Gets fired when a monitored process has ended."),
    (EVT_ALL_MON_PROC_TERMINATED,   "Gets fired when all monitored processes have ended."),
    (EVT_KEEPALIVE_STARTED,         "Gets fired when a KeepAlive period has began."),
    (EVT_KEEPALIVE_ENDED,           "Gets fired when a KeepAlive period has ended."),
    (EVT_ALL_KEEPALIVE_ENDED,       "Gets fired when all KeepAlive periods have ended."),
)



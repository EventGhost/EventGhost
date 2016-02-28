
eg.RegisterPlugin(
    name = "Timer",
    author = "Bartman",
    version = "2.0",
    guid = "{6149CA99-1FCD-4450-9160-7543BC20CFD3}",
    description = (
        "Triggers an event after an adjustable time and optionally repeats it "
        "after an interval."
    ),
    url = "http://www.eventghost.net/forum/viewtopic.php?t=572",
)

import time

class Text:
    stopped = "Plugin stopped"
    timerFinished = "Timer finished"
    listhl = "Currently active Timers:"
    colLabels = ("Timer Name",
        "Start time",
        "Next event",
        "Event Name",
        "Loop Counter",
        "Loops",
        "Interval")

    class TimerAction:
        name = "Start new or control running timer"
        description = "Allows starting, stopping or resetting timers, which can trigger an event after a given time"
        timerName = "Timer name:"
        start = "Start new timer (currently running timer with the same name will be aborted)"

        startTime = "Start:"
        startTimeTypes = (
            "immediately",
            "after interval time",
            "at given time (HH:MM:SS)",
            "after given duration (HH:MM:SS)",
            "next full minute",
            "next full five minutes",
            "next full 15 minutes",
            "next full 30 minutes",
            "next hour"
        )
        actions = (
            "Restart timer with existing settings",
            "Restart timer (when running only)",
            "Reset the loop counter",
            "Abort")

        loop1 = "Loops: "
        loop2 = "(0 = unlimited)"
        showRemaingLoopsText = "loop counter shows remaining loops"
        interval1 = "Interval:"
        interval2 = "seconds"
        eventName = "Event name:"
        addCounterToName = "add loop counter to event name" #(otherwise payload only)"

        labelStartUnlimited = 'Start timer "%s" (unlimited loops, %.2f seconds interval)'
        labelStartOneTime = 'Start timer "%s"'
        labelStart = 'Start timer "%s" (%s loops, %.2f seconds interval)'
        labels = (
            'Restart timer "%s"',
            'Restart timer "%s" if it is still running' ,
            'Reset counter of timer "%s"',
            'Abort timer "%s"'
        )

class TimerObject():
    def __init__(self,
        plugin,
        name,
        loops,
        interval,
        eventName,
        addCounterToName,
        showRemainingLoops,
        startTimeType,
        startTime
    ):
        #copy settings to instance variables
        self.plugin = plugin
        self.name = name
        self.interval = interval
        if self.interval <= 0:
            self.loops = 1 #prevent constant eventTriggering
        else:
            self.loops = loops

        self.eventName = eventName
        self.addCounterToName = addCounterToName
        self.showRemainingLoops = showRemainingLoops
        self.startTimeType = startTimeType
        self.startTime = startTime
        self.ScheduleFirst()

    def ScheduleFirst(self):
        self.loopCounter = 0
        self.active = True
        self.startedAt = time.time()

        #immediately
        if self.startTimeType == 0:
            self.nextEventAt = self.startedAt
            self.TriggerScheduledEvent(self.nextEventAt)
            return

        #after interval time
        if self.startTimeType == 1:
            self.nextEventAt = self.startedAt + self.interval
        #at given time (HH:MM:SS)
        elif self.startTimeType == 2:
            hoursStr, minutesStr, secondsStr = self.startTime.split(":")
            hours = int(hoursStr)
            minutes = int(minutesStr)
            seconds = int(secondsStr)
            #check if we have to schedule today or tomorrow
            now = time.localtime(self.startedAt)
            self.nextEventAt = time.mktime((now[0], now[1], now[2], hours, minutes, seconds, now[6], now[7], -1))
            if (self.nextEventAt <= self.startedAt):
                #have to start tomorrow
                self.nextEventAt = time.mktime((now[0], now[1], now[2] + 1, hours, minutes, seconds, now[6], now[7], -1))
        #after given duration (HH:MM:SS)
        elif self.startTimeType == 3:
            hoursStr, minutesStr, secondsStr = self.startTime.split(":")
            self.nextEventAt = self.startedAt + int(hoursStr) * 3600 + int(minutesStr) * 60 + int(secondsStr)
        #next full x minute
        elif self.startTimeType > 3 and self.startTimeType < 9:
            now = time.localtime(self.startedAt)
            times = (1, 5, 15, 30, 60)
            fullMinutes = times[self.startTimeType - 4]
            minutes = ((now[4] / fullMinutes) + 1) * fullMinutes
            self.nextEventAt = time.mktime((now[0], now[1], now[2], now[3], minutes, 0, now[6], now[7], now[8]))
        else:
            raise ValueError("unknown startTimeType")

        eg.scheduler.AddShortTaskAbsolute(self.nextEventAt, self.TriggerScheduledEvent, self.nextEventAt)

    def TriggerScheduledEvent(self, scheduledTime):
        if not self.plugin.started or not self.active or self.nextEventAt != scheduledTime:
            #timer has changed in some way
            return

        if self.showRemainingLoops and self.loops != 0:
            loopDisplay = self.loops - self.loopCounter - 1
        else:
            loopDisplay = self.loopCounter

        eventNameTmp = self.eventName
        if self.addCounterToName:
            eventNameTmp += str(loopDisplay)

        self.plugin.TriggerEvent(eventNameTmp, (loopDisplay, time.strftime("%c")))

        self.loopCounter += 1
        self.ScheduleNext()

    def ScheduleNext(self):
        if not self.IsActive():
            #no more event to schedule
            return
        self.nextEventAt += self.interval
        eg.scheduler.AddShortTaskAbsolute(self.nextEventAt, self.TriggerScheduledEvent, self.nextEventAt)

    def Restart(self):
        #just reschedule
        self.ScheduleFirst()

    def Abort(self):
        self.active = False

    def ResetCounter(self):
        self.loopCounter = 0

    def IsActive(self):
        return self.plugin.started and self.active and not self.HasFinished()

    def HasFinished(self):
        return self.loops != 0 and self.loopCounter >= self.loops

class Timer(eg.PluginClass):
    text = Text
    started = False

    def __init__(self):
        self.AddAction(TimerAction)

        #timer names are kept for usability reasons
        self.timerNames = []
        self.lastTimerName = ""
        self.timerObjects = {}

    def __start__(self):
        self.started = True

    def __stop__(self):
        self.started = False
        #end all running timers
        self.AbortAllTimers()

    def __close__(self):
        self.AbortAllTimers()

    def OnComputerSuspend(self, suspendType):
        self.AbortAllTimers()

    #methods to Control timers
    def StartTimer(self,
        timerName,
        loops,
        interval,
        eventName,
        addCounterToName,
        showRemainingLoops,
        startTimeType,
        startTime
    ):

        timer = self.timerObjects.get(timerName)
        if timer:
            timer.Abort()
        timer = TimerObject(self,
            timerName,
            loops,
            interval,
            eventName,
            addCounterToName,
            showRemainingLoops,
            startTimeType,
            startTime)
        self.timerObjects[timerName] = timer


    def ResetTimerCounter(self, timerName):
        timer = self.timerObjects.get(timerName)
        if timer:
            if timer.IsActive():
                timer.ResetCounter()
            else:
                eg.PrintError(Text.timerFinished + timerName)
                return False

    def AbortTimer(self, timerName):
        timer = self.timerObjects.get(timerName)
        if timer:
            del self.timerObjects[timerName]
            timer.Abort()

    def AbortAllTimers(self):
        for timer in self.timerObjects.itervalues():
            timer.Abort()
        self.timerObjects = {}

    def RestartTimer(self, timerName, startNewIfNotAlive = False):
        timer = self.timerObjects.get(timerName)
        if timer:
            if timer.IsActive() or startNewIfNotAlive:
                timer.Restart()

    def RestartAllTimers(self, startNewIfNotAlive = False):
        for timer in self.timerObjects.itervalues():
            if timer.IsActive() or startNewIfNotAlive:
                timer.Restart()


    def Configure(self, *args):
        panel = eg.ConfigPanel(self, resizable=True)

        panel.sizer.Add(
            wx.StaticText(panel, -1, Text.listhl),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        mySizer = wx.GridBagSizer(5, 5)
        mySizer.AddGrowableRow(0)
        mySizer.AddGrowableCol(1)
        mySizer.AddGrowableCol(2)
        mySizer.AddGrowableCol(3)

        timerListCtrl = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)

        for i, colLabel in enumerate(Text.colLabels):
            timerListCtrl.InsertColumn(i, colLabel)

        #setting column width to fit label
        #insert date to get size
        timerListCtrl.InsertStringItem(0, "Test EventName")
        timerListCtrl.SetStringItem(0, 1, time.strftime("%c"))

        size = 0
        for i in range(7):
            timerListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER) #wx.LIST_AUTOSIZE
            size += timerListCtrl.GetColumnWidth(i)

        timerListCtrl.SetMinSize((size, -1))

        mySizer.Add(timerListCtrl, (0,0), (1, 5), flag = wx.EXPAND)

        #buttons
        abortButton = wx.Button(panel, -1, "Abort")
        mySizer.Add(abortButton, (1,0))

        abortAllButton = wx.Button(panel, -1, "Abort all")
        mySizer.Add(abortAllButton, (1,1), flag = wx.ALIGN_CENTER_HORIZONTAL)

        restartButton = wx.Button(panel, -1, "Restart")
        mySizer.Add(restartButton, (1,2), flag = wx.ALIGN_CENTER_HORIZONTAL)

        restartAllButton = wx.Button(panel, -1, "Restart All")
        mySizer.Add(restartAllButton, (1,3), flag = wx.ALIGN_CENTER_HORIZONTAL)

        refreshButton = wx.Button(panel, -1, "Refresh")
        mySizer.Add(refreshButton, (1,4), flag = wx.ALIGN_RIGHT)

        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)

        def PopulateList (event):
            timerListCtrl.DeleteAllItems()
            row = 0
            for timer in self.timerObjects.itervalues():
                if timer.IsActive():
                    timerListCtrl.InsertStringItem(row, timer.name)
                    #print "Timer", t.name, t.eventName, t.loopCounter
                    timerListCtrl.SetStringItem(row,
                        1, time.strftime("%c",  time.localtime(timer.startedAt)))
                    timerListCtrl.SetStringItem(row,
                        2, time.strftime("%X",  time.localtime(timer.nextEventAt)))
                    timerListCtrl.SetStringItem(row,
                        3, timer.eventName)
                    timerListCtrl.SetStringItem(row,
                        4, str(timer.loopCounter))
                    timerListCtrl.SetStringItem(row,
                        5, str(timer.loops))
                    timerListCtrl.SetStringItem(row,
                    6, str(timer.interval) + " sec")
                    row += 1
            ListSelection(wx.CommandEvent())

        def OnAbortButton(event):
            item = timerListCtrl.GetFirstSelected()
            while item != -1:
                name = timerListCtrl.GetItemText(item)
                self.AbortTimer(name)
                item = timerListCtrl.GetNextSelected(item)
            PopulateList(wx.CommandEvent())
            event.Skip()

        def OnAbortAllButton(event):
            self.AbortAllTimers()
            PopulateList(wx.CommandEvent())
            event.Skip()

        def OnRestartButton(event):
            item = timerListCtrl.GetFirstSelected()
            while item != -1:
                name = timerListCtrl.GetItemText(item)
                self.RestartTimer(name)
                item = timerListCtrl.GetNextSelected(item)
            PopulateList(wx.CommandEvent())
            event.Skip()

        def OnRestartAllButton(event):
            self.RestartAllTimers()
            PopulateList(wx.CommandEvent())
            event.Skip()

        def ListSelection(event):
            flag = timerListCtrl.GetFirstSelected() != -1
            abortButton.Enable(flag)
            restartButton.Enable(flag)
            event.Skip()

        def OnSize(event):
            timerListCtrl.SetColumnWidth(6, wx.LIST_AUTOSIZE_USEHEADER) #wx.LIST_AUTOSIZE
            event.Skip()

        PopulateList(wx.CommandEvent())
        #timerListCtrl.SetMinSize(timerListCtrl.GetBestFittingSize())


        abortButton.Bind(wx.EVT_BUTTON, OnAbortButton)
        abortAllButton.Bind(wx.EVT_BUTTON, OnAbortAllButton)
        restartButton.Bind(wx.EVT_BUTTON, OnRestartButton)
        restartAllButton.Bind(wx.EVT_BUTTON, OnRestartAllButton)
        refreshButton.Bind(wx.EVT_BUTTON, PopulateList)
        timerListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelection)
        timerListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelection)
        panel.Bind(wx.EVT_SIZE, OnSize)

        while panel.Affirmed():
            panel.SetResult(*args)

    #function to fill the timer name ComboBox
    def GetTimerNames(self):
        self.timerNames.sort(lambda a,b: cmp(a.lower(), b.lower()) )
        return self.timerNames

    #function to collect timer names for ComboBox
    def AddTimerName(self, timerName):
        #self.lastTimerName = timerName
        if not timerName in self.timerNames:
            self.timerNames.append(timerName)

class TimerAction(eg.ActionClass):
    def __call__(self,
        timerName,
        action,
        loops,
        interval,
        eventName,
        addCounterToName,
        showRemainingLoops,
        startTimeType,
        startTime
    ):
        if not self.plugin.started:
            self.PrintError(Text.stopped)
            return False

        if action == 0:#start
            self.plugin.StartTimer(timerName,
                loops,
                interval,
                eventName,
                addCounterToName,
                showRemainingLoops,
                startTimeType,
                startTime)
        elif action == 1:#restart
            self.plugin.RestartTimer(timerName, True)
        elif action == 2:#restart, when running only
            self.plugin.RestartTimer(timerName, False)
        elif action == 3:#reset counter
            self.plugin.ResetTimerCounter(timerName)
        elif action == 4:#abort
            self.plugin.AbortTimer(timerName)
        else:
            raise ValueError("unknown action index")

    def GetLabel(self,
        timerName,
        action,
        loops,
        interval,
        eventName,
        addCounterToName,
        showRemainingLoops,
        startTimeType,
        startTime
    ):
        self.plugin.AddTimerName(timerName)
        if action == 0:
            if loops == 0:
                return Text.labelStartUnlimited % (timerName, interval)
            if loops == 1:
                return Text.labelStartOneTime % timerName
            return Text.labelStart % (timerName, loops, interval)
        return Text.labels[action-1] % timerName

    def Configure(self,
        timerName = None,
        action = 0,
        loops = 1,
        interval = 1,
        eventName = "",
        addCounterToName = False,
        showRemainingLoops = True,
        startTimeType = 1,
        startTime = "00:00:00"
    ):
        plugin = self.plugin

        panel = eg.ConfigPanel(self)

        #name
        nameSizer = wx.BoxSizer(wx.HORIZONTAL)

        nameSizer.Add(
            wx.StaticText(panel, -1, Text.TimerAction.timerName),
            flag = wx.ALIGN_CENTER_VERTICAL
        )
        if not timerName:
            timerName = plugin.lastTimerName
        timerNameCtrl = wx.ComboBox(panel, -1,
            timerName,
            choices = plugin.GetTimerNames(),
            size=(200,-1))
        nameSizer.Add(timerNameCtrl, flag = wx.EXPAND)

        panel.sizer.Add(nameSizer)
        panel.sizer.Add(wx.Size(5,5))

        #action and settings
        #sizer = wx.GridBagSizer(5, 5)
        #sizer.SetEmptyCellSize((0,0))


        choices = len(Text.TimerAction.actions)
        rb = range(0, choices + 1)

        rb[0] = wx.RadioButton(panel, -1, Text.TimerAction.start, style = wx.RB_GROUP)
        rb[0].SetValue(action == 0)

        panel.sizer.Add(wx.Size(5,5))
        panel.sizer.Add(rb[0], flag = wx.ALIGN_CENTER_VERTICAL)

        #space to indent the settings
        startSettingsSizer = wx.GridBagSizer(5, 5)

        rowCount = 0 #used to find the correct row of the gridbagsizer
        startSettingsSizer.Add(wx.Size(rowCount,1), (1, 0))

        #loop
        startSettingsSizer.Add(
            wx.StaticText(panel, -1, Text.TimerAction.loop1),
            (rowCount, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        loopCtrl = eg.SpinIntCtrl(panel, -1, loops, 0, size=(200,-1))
        startSettingsSizer.Add(loopCtrl, (rowCount, 1), flag = wx.EXPAND)
        startSettingsSizer.Add(
            wx.StaticText(panel, -1, Text.TimerAction.loop2),
            (rowCount, 2), (1, 2),
            flag = wx.ALIGN_CENTER_VERTICAL)

        #showRemaingLoopsText
        rowCount += 1
        showRemaingLoopsCtrl = wx.CheckBox(panel, -1, Text.TimerAction.showRemaingLoopsText)
        showRemaingLoopsCtrl.SetValue(showRemainingLoops)
        startSettingsSizer.Add(showRemaingLoopsCtrl, (rowCount, 1), (1, 3))

        #intervall
        rowCount += 1
        startSettingsSizer.Add(
            wx.StaticText(panel, -1, Text.TimerAction.interval1),
            (rowCount, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        intervalCtrl = eg.SpinNumCtrl(
            panel, -1, interval, size=(200,-1), integerWidth=7
        )
        startSettingsSizer.Add(intervalCtrl, (rowCount, 1), flag = wx.EXPAND)

        startSettingsSizer.Add(
            wx.StaticText(panel, -1, Text.TimerAction.interval2),
            (rowCount, 2), (1, 2),
            flag = wx.ALIGN_CENTER_VERTICAL)

        #startTime
        rowCount += 1
        startSettingsSizer.Add(
            wx.StaticText(panel, -1, Text.TimerAction.startTime),
            (rowCount, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        startTimeTypeCtrl = wx.Choice(panel, -1, choices = Text.TimerAction.startTimeTypes)
        startTimeTypeCtrl.SetSelection(startTimeType)
        startSettingsSizer.Add(startTimeTypeCtrl, (rowCount, 1), (1, 2), flag = wx.EXPAND)

        startTimeCtrl = wx.lib.masked.timectrl.TimeCtrl(
            panel,
            format = "24HHMMSS"
        )
        startTimeCtrl.SetValue(startTime)
        startSettingsSizer.Add(startTimeCtrl, (rowCount, 3), flag = wx.EXPAND)

        #eventName
        rowCount += 1
        startSettingsSizer.Add(
            wx.StaticText(panel, -1, Text.TimerAction.eventName),
            (rowCount, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        eventNameCtrl = wx.TextCtrl(panel, -1, eventName, size=(200,-1))
        startSettingsSizer.Add(eventNameCtrl, (rowCount, 1), (1, 3), flag = wx.EXPAND)

        #addCounterToName
        rowCount += 1
        addCounterToNameCtrl = wx.CheckBox(panel, -1, Text.TimerAction.addCounterToName)
        addCounterToNameCtrl.SetValue(addCounterToName)
        startSettingsSizer.Add(addCounterToNameCtrl, (rowCount, 1), (1, 3))

        settingsSizer = wx.BoxSizer(wx.HORIZONTAL)
        settingsSizer.Add(wx.Size(20,20))
        settingsSizer.Add(startSettingsSizer)

        panel.sizer.Add(wx.Size(5,5))

        panel.sizer.Add(settingsSizer)
        #remaining radio buttons

        for i in range(1, len(rb)):
            rowCount += 1
            rb[i] = wx.RadioButton(panel, -1, Text.TimerAction.actions[i - 1])
            rb[i].SetValue(action == i)
            panel.sizer.Add(wx.Size(5,5))
            panel.sizer.Add(rb[i], flag = wx.ALIGN_CENTER_VERTICAL)

        def onRadioButton(event):
            flag = rb[0].GetValue()
            loopCtrl.Enable(flag)
            showRemaingLoopsCtrl.Enable(flag)
            intervalCtrl.Enable(flag)
            eventNameCtrl.Enable(flag)
            addCounterToNameCtrl.Enable(flag)
            startTimeTypeCtrl.Enable(flag)
            tmp = startTimeTypeCtrl.GetSelection()
            startTimeCtrl.Enable(flag and (tmp == 2 or tmp == 3))
            event.Skip()

        def onChoiceChange(event):
            tmp = startTimeTypeCtrl.GetSelection()
            startTimeCtrl.Enable(tmp == 2 or tmp == 3)
            event.Skip()

        onRadioButton(wx.CommandEvent())

        for i in range(len(rb)):
            rb[i].Bind(wx.EVT_RADIOBUTTON, onRadioButton)

        startTimeTypeCtrl.Bind(wx.EVT_CHOICE, onChoiceChange)

        #panel.sizer.Add(sizer)

        while panel.Affirmed():
            timerName = timerNameCtrl.GetValue()
            plugin.lastTimerName = timerName
            plugin.AddTimerName(timerName)
            for i in range(len(rb)):
                if rb[i].GetValue():
                    action = i
                    break
            loops = loopCtrl.GetValue()
            showRemainingLoops = showRemaingLoopsCtrl.GetValue()
            eventName = eventNameCtrl.GetValue()
            interval = intervalCtrl.GetValue()
            startTimeType = startTimeTypeCtrl.GetSelection()
            addCounterToName = addCounterToNameCtrl.GetValue()
            startTime = startTimeCtrl.GetValue()

            panel.SetResult(
                timerName,
                action,
                loops,
                interval,
                eventName,
                addCounterToName,
                showRemainingLoops,
                startTimeType,
                startTime
            )

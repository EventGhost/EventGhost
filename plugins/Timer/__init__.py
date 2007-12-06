
eg.RegisterPlugin(
    name = "Timer",
    author = "Bartman",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    description = (
        "Triggers an event after an adjustable time and optionally repeats it "
        "after an interval."
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=572",
)

from threading import Thread, Event
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

        labelStartUnlimited = 'Start timer "%s" (unlimited loops, %.2f seconds intervall)'
        labelStartOneTime = 'Start timer "%s"'
        labelStart = 'Start timer "%s" (%s loops, %.2f seconds intervall)'
        labels = (
            'Restart timer "%s"',
            'Restart timer "%s" if it is still running' ,
            'Reset counter of timer "%s"',
            'Abort timer "%s"'
        )



class TimerThread(Thread):
    def __init__(self,
        name,
        loops,
        interval,
        eventName,
        addCounterToName,
        showRemainingLoops,
        startTimeType,
        startTime
    ):

        # Thread.__init__(self, name = name)
        # threading Thread doesn't like unicode strings as name. This seems
        # to be a bug of the library. We don't need the name anyhow, so we
        # init it anonymous.
        Thread.__init__(self, name="TimerThread")
        if not eventName:
            eventName = name
        self.name = name
        self.interval = interval
        if self.interval == 0:
            self.loops = 1 #prevent constant eventTriggering
        else:
            self.loops = loops
        self.eventName = eventName
        self.finished = Event()
        self.abort = False
        self.restart = False
        self.loopCounter = 0
        self.timeStarted = 0
        self.timeNextEvent = 0
        self.addCounterToName = addCounterToName
        self.showRemainingLoops = showRemainingLoops
        self.startTimeType = startTimeType
        self.startTime = startTime

        #print "Starting", time.strftime("%c", time.localtime(self.startTime))
   
    def run(self):
        self.timeStarted = time.time()
        self.resetLoopCounter = False
        self.loopCounter = 0
        while (self.loops == 0 or self.loopCounter < self.loops):
            #print "Loop", self.loopCounter
            self.restart = True
            while self.restart:#loops one time unless restart is called
                self.restart = False
                if self.loopCounter == 0:
                    #calculate time2wait depending on startTypeChoice
                    if self.startTimeType == 0:#immediately
                        time2wait = 0
                    elif self.startTimeType == 1:#after interval time
                        time2wait = self.interval
                    elif self.startTimeType == 2:#at given time (HH:MM:SS)
                        hours, minutes, seconds = self.startTime.split(":")
                        time2wait = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
                        currentTime = time.time()
                        tmp = time.localtime(currentTime)
                        secondsToday = tmp[3] * 3600 + tmp[4] * 60 + tmp[5]
                        if time2wait >= secondsToday:
                            time2wait = time2wait - (secondsToday + (currentTime %1))
                        else:
                            time2wait = (24 * 60 * 60) - (secondsToday + (currentTime %1)) + time2wait
                    elif self.startTimeType == 3:#after given duration (HH:MM:SS)
                        hours, minutes, seconds = self.startTime.split(":")
                        time2wait = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
                    else:#next full x minute
                        currentTime = time.time()
                        times = (1, 5, 15, 30, 60)
                        fullMinutes = times[self.startTimeType - 4]
                        time2wait = 60 - (currentTime % 60)
                        currentTime = round (currentTime + time2wait) #time with next full minute
                        currentTime = (currentTime % 3600) / 60 #now minutes of hour
                        currentTime = currentTime % fullMinutes
                        if currentTime != 0:
                            time2wait += ((fullMinutes - currentTime) *60)
                   
                else:#not first loop
                    time2wait = self.interval
               
                self.timeNextEvent = time.time() + time2wait
                #print time2wait, "Seconds until event", time.strftime("%c",  time.localtime(self.timeNextEvent))
               
                self.finished.wait(time2wait)
                self.finished.clear()
            if self.abort:
                break
           
            if self.resetLoopCounter:
                self.loopCounter = 0
                self.resetLoopCounter = False

            if self.showRemainingLoops and self.loops != 0:
                loopDisplay = self.loops - self.loopCounter - 1
            else:
                loopDisplay = self.loopCounter

            eventNameTmp = self.eventName
            if self.addCounterToName:
                eventNameTmp += str(loopDisplay)
           
            eg.TriggerEvent(eventNameTmp, (loopDisplay, time.strftime("%c")), prefix = "Timer")
            self.loopCounter += 1
           
        
    def AbortTimer(self):
        self.abort = True
        self.finished.set()
       
    
    def ResetCounter(self):
        self.resetLoopCounter = True
   

    def RestartTimer(self):
        self.timeStarted = time.time()
        self.loopCounter = 0
        self.restart = True
        self.finished.set()



class Timer(eg.PluginClass):
    text = Text
    started = False
    
    def __init__(self):
        self.AddAction(TimerAction)
       
        #timernames are kept for usebility reasons
        self.timerNames = []
        self.lastTimerName = ""
        self.timerThreads = {}


    def __start__(self):
        self.started = True


    def __stop__(self):
        self.started = False
        #end all running threads
        self.AbortAllTimers()


    def __close__(self):
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

        if self.timerThreads.has_key(timerName):
            t = self.timerThreads[timerName]
            if t.isAlive():
                t.AbortTimer()
            del self.timerThreads[timerName]
        t = TimerThread(timerName,
            loops,
            interval,
            eventName,
            addCounterToName,
            showRemainingLoops,
            startTimeType,
            startTime)
        t.start()
        self.timerThreads[timerName] = t


    def ResetTimerCounter(self, timer):
        if self.timerThreads.has_key(timer):
            t = self.timerThreads[timer]
            if t.isAlive():
                t.ResetCounter()
            else:
                eg.PrintError(self.text.timerFinished + timerName)
                del threads[timerName]
                return False


    def AbortTimer(self, timer):
        if self.timerThreads.has_key(timer):
            t = self.timerThreads[timer]
            t.AbortTimer()
            del self.timerThreads[timer]


    def AbortAllTimers(self):
        for i, item in enumerate(self.timerThreads):
            t = self.timerThreads[item]
            t.AbortTimer()
            del t
        self.timerThreads = {}


    def RestartTimer(self, timer, startNewIfNotAlive = False):
        if self.timerThreads.has_key(timer):
            t = self.timerThreads[timer]
            if t.isAlive():
                t.RestartTimer()
            elif startNewIfNotAlive:
                self.StartTimer(t.name,
                    t.loops,
                    t.interval,
                    t.eventName,
                    t.addCounterToName,
                    t.showRemainingLoops,
                    t.startTimeType,
                    t.startTime)


    def RestartAllTimers(self, startNewIfNotAlive = False):
        for i, item in enumerate(self.timerThreads):
            t = self.timerThreads[item]
            if t.isAlive():
                t.RestartTimer()
            elif startNewIfNotAlive:
                self.StartTimer(
                    t.timerName,
                    t.loops,
                    t.interval,
                    t.eventName,
                    t.addCounterToName,
                    t.showRemainingLoops,
                    t.startTimeType,
                    t.startTime
                )


    def Configure(self, *args):
        panel = eg.ConfigPanel(self, resizeable=True)

        panel.sizer.Add(
            wx.StaticText(panel, -1, self.text.listhl),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        mySizer = wx.GridBagSizer(5, 5)
        mySizer.AddGrowableRow(0)
        mySizer.AddGrowableCol(1)
        mySizer.AddGrowableCol(2)
        mySizer.AddGrowableCol(3)
       
        timerListCtrl = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)
       
        for i, colLabel in enumerate(self.text.colLabels):
            timerListCtrl.InsertColumn(i, colLabel)

        #setting col width to fit label
        #insert date to get Size
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
            for i, item in enumerate(self.timerThreads):
                t = self.timerThreads[item]
                if t.isAlive():
                    timerListCtrl.InsertStringItem(row, t.name)
                    #print "Timer", t.name, t.eventName, t.loopCounter
                    timerListCtrl.SetStringItem(row,
                        1, time.strftime("%c",  time.localtime(t.timeStarted)))
                    timerListCtrl.SetStringItem(row,
                        2, time.strftime("%H:%M:%S",  time.localtime(t.timeNextEvent)))
                    timerListCtrl.SetStringItem(row,
                        3, t.eventName)
                    timerListCtrl.SetStringItem(row,
                        4, str(t.loopCounter))
                    timerListCtrl.SetStringItem(row,
                        5, str(t.loops))
                    timerListCtrl.SetStringItem(row,
                    6, str(t.interval) + " sec")
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

    #function to fill the timer name Combobox
    def GetTimerNames(self):
        self.timerNames.sort(lambda a,b: cmp(a.lower(), b.lower()) )
        return self.timerNames

    #function to collect timer names for Combobox
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
            self.PrintError(self.plugin.text.stopped)
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
                return self.text.labelStartUnlimited % (timerName, interval)
            if loops == 1:
                return self.text.labelStartOneTime % timerName
            return self.text.labelStart % (timerName, loops, interval)
        return self.text.labels[action-1] % timerName


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
        text = self.text
        plugin = self.plugin

        panel = eg.ConfigPanel(self)

        #name
        nameSizer = wx.BoxSizer(wx.HORIZONTAL)


        nameSizer.Add(
            wx.StaticText(panel, -1, self.text.timerName),
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

       
        choices = len(text.actions)
        rb = range(0, choices + 1)
       
        rb[0] = wx.RadioButton(panel, -1, text.start, style = wx.RB_GROUP)
        rb[0].SetValue(action == 0)

        panel.sizer.Add(wx.Size(5,5))
        panel.sizer.Add(rb[0], flag = wx.ALIGN_CENTER_VERTICAL)
       
        #space to indent the settings
        startSettingsSizer = wx.GridBagSizer(5, 5)
       
        rowCount = 0 #used to find the correct row of the gridbagsizer
        startSettingsSizer.Add(wx.Size(rowCount,1), (1, 0))

        #loop
        startSettingsSizer.Add(
            wx.StaticText(panel, -1, self.text.loop1),
            (rowCount, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        loopCtrl = eg.SpinIntCtrl(panel, -1, loops, 0, size=(200,-1))
        startSettingsSizer.Add(loopCtrl, (rowCount, 1), flag = wx.EXPAND)
        startSettingsSizer.Add(
            wx.StaticText(panel, -1, self.text.loop2),
            (rowCount, 2), (1, 2),
            flag = wx.ALIGN_CENTER_VERTICAL)

        #showRemaingLoopsText
        rowCount += 1
        showRemaingLoopsCtrl = wx.CheckBox(panel, -1, text.showRemaingLoopsText)
        showRemaingLoopsCtrl.SetValue(showRemainingLoops)
        startSettingsSizer.Add(showRemaingLoopsCtrl, (rowCount, 1), (1, 3))
       
        #intervall
        rowCount += 1
        startSettingsSizer.Add(
            wx.StaticText(panel, -1, self.text.interval1),
            (rowCount, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        intervalCtrl = eg.SpinNumCtrl(
            panel, -1, interval, size=(200,-1), integerWidth=7
        )
        startSettingsSizer.Add(intervalCtrl, (rowCount, 1), flag = wx.EXPAND)
       
        startSettingsSizer.Add(
            wx.StaticText(panel, -1, self.text.interval2),
            (rowCount, 2), (1, 2),
            flag = wx.ALIGN_CENTER_VERTICAL)

        #startTime
        rowCount += 1
        startSettingsSizer.Add(
            wx.StaticText(panel, -1, self.text.startTime),
            (rowCount, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        startTimeTypeCtrl = wx.Choice(panel, -1, choices = text.startTimeTypes)
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
            wx.StaticText(panel, -1, self.text.eventName),
            (rowCount, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        eventNameCtrl = wx.TextCtrl(panel, -1, eventName, size=(200,-1))
        startSettingsSizer.Add(eventNameCtrl, (rowCount, 1), (1, 3), flag = wx.EXPAND)
       
        #addCounterToName
        rowCount += 1
        addCounterToNameCtrl = wx.CheckBox(panel, -1, text.addCounterToName)
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
            rb[i] = wx.RadioButton(panel, -1, text.actions[i - 1])
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
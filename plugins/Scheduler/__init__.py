# -*- coding: utf-8 -*-
#
# plugins/Scheduler/__init__.py
#
# This file is a plugin for EventGhost.
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

eg.RegisterPlugin(
    name = "Scheduler",
    guid = '{5C822DE2-97E7-4DB8-8281-CD77ED216A63}',
    author = "Walter Kraembring",
    version = "1.2.2",
    description = (
        "Triggers an event at configurable dates & times"
    ),
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=818",
)

##############################################################################
# Revision history:
#
# 2014-08-11  Added default params to ensure correct startup
#             Added plugin setting for customizing the event prefix
#             Added event to allow controlling restart of threads when
#             changing 'empty house' and 'vacation' modes
# 2014-05-12  Plugin settings updated for 'empty house' and 'vacation' modes
#             when changed via actions from externals
# 2014-05-10  Plugin termination problem improved/solved
# 2014-02-24  Added new day type, 'empty house', and new empty house mode
# 2013-12-27  Synchronization is now deactived during vacation mode
# 2012-10-19  Vacation mode set from external is now persistent
# 2012-10-07  Vacation mode can now be set from external
# 2012-09-02  Commented out a number of print statements (info can be found
#             in the log files)
# 2010-02-19  Added routine to restore device states at restart
# 2009-12-19  0.4.0 compatible GUID added
# 2009-12-03  Introduced a small random delay between thread executions
# 2009-07-17  Using python calendar module to check the weekday
# 2009-04-16  Fix for logging in Vista (/ProgramData/EventGhost/Log)
# 2009-03-19  Fix for SpinNumCtrl, many thanks to jinxdone
# 2009-01-26  Re-designed, moved some action variables to common plugin
#             variables with configuration settings in the plugin dialog
#             Changed the behaviour of buttons in action and plugin dialogs
# 2008-09-23  Individual settings for bursts (ON/OFF) added
# 2008-09-17  Bugfix in string conversion
#             Added individual log files for each thread
# 2008-04-26  Improved input control of time interval
#             Added synchronization option
# 2008-04-19  Added a daytype for "Vacation" to be used when the house is
#             empty
# 2008-04-18  First version published
##############################################################################

from threading import Thread, Event
import time
import os
import sys
import calendar
import random



class Text:
    started = "Plugin started"
    closing = "Please wait, terminating threads..."
    schedulerFinished = "Scheduler finished"
    listhl = "Currently active Schedulers:"
    colLabels = (
        "Scheduler Name",
        "Event Name ON",
        "Event Name OFF"
    )
    #Buttons
    b_abort = "Abort"
    b_abortAll = "Abort all"
    b_restartAll = "Restart All"
    b_refresh = "Refresh"

    #Thread
    n_SchedulerThread = "SchedulerThread"
    nd_mo = "Monday"
    nd_tu = "Tuesday"
    nd_we = "Wednesday"
    nd_th = "Thursday"
    nd_fr = "Friday"
    nd_sa = "Saturday"
    nd_su = "Sunday"
    nd_vc = "Vacation"
    nd_eh = "Empty House"
    nxt_1 = "Next execution of "
    nxt_2 = " will start in "
    nxt_3 = " seconds"
    lg_today = "Today is "
    lg_dayOfWeek = "Normal scheduling would have followed settings for "
    lg_holiday_1 = "Due to holidays, scheduling of "
    lg_holiday_2 = "will instead follow "
    lg_holiday_3 = "your settings for "
    lg_vacation_1 = "Due to vacation, scheduling of "
    lg_vacation_2 = "will instead follow "
    lg_vacation_3 = "your settings for "
    lg_emptyHouse_1 = "Due to Empty House, scheduling of "
    lg_emptyHouse_2 = "will instead follow "
    lg_emptyHouse_3 = "your settings for "
    thr_abort = "Thread is terminating: "
    txtFixedHolidays = "Fixed Public Holidays:"
    txtVariableHolidays = "Variable Public Holidays:"
    txtVacation_m = "Vacation mode"
    txtEmptyHouse_m = "Empty House mode"
    txtRestoreState_1 = "Earlier Today Set to ON at: "
    txtRestoreState_2 = "Earlier Today Set to OFF at: "
    txtRestoreState_3 = "Yesterday or Earlier Set to ON at: "
    txtRestoreState_4 = "Yesterday or Earlier Set to OFF at: "
    eventPrefix = "Event prefix (default is 'Main'):"

    class SchedulerAction:
        name = "Start new or control running scheduler"
        description = (
            "Allows starting, stopping or resetting schedulers, which "+
            "triggers an event at a given date & time"
        )
        #schedulerName = "Scheduler name:"
        eventNameOn = "Event name ON:"
        eventNameOff = "Event name OFF:"
        labelStart = ' "%s"'
        moON = "Monday ON"
        tuON = "Tuesday ON"
        weON = "Wednesday ON"
        thON = "Thursday ON"
        frON = "Friday ON"
        saON = "Saturday ON"
        suON = "Sunday ON"
        vcON = "Vacation ON"
        ehON = "Empty House ON"
        txtON = "ON"
        txtOFF = "OFF"
        txtNbrBursts = "Number of events per control (1-10 bursts)"
        txtCmdDelay = "Delay between the events (0.5-5.0 s)"
        doLogLoopsText = "Print normal loop info (Y/N)"
        bDoSynchText = "Synchronization activated (Y/N)"
        txtSynchInterval = "Synchronization interval (6-600 min)"

    class SetVacationON:
        txtMG_ON = "Vacation function ON"
        txtInit = "Please wait, Scheduler is just initialising..."

    class SetVacationOFF:
        txtMG_OFF = "Vacation function OFF"
        txtInit = "Please wait, Scheduler is just initialising..."

    class SetEmptyHouseON:
        txtMG_ON = "EmptyHouse function ON"
        txtInit = "Please wait, Scheduler is just initialising..."

    class SetEmptyHouseOFF:
        txtMG_OFF = "EmptyHouse function OFF"
        txtInit = "Please wait, Scheduler is just initialising..."



class SchedulerThread(Thread):
    text = Text

    def __init__(
        self,
        dayTimeSettings,
        name,
        eventNameOn,
        eventNameOff,
        fixedHolidays,
        variableHolidays,
        iNbrOfBurstsON,
        iNbrOfBurstsOFF,
        cmdDelay,
        doLogLoops,
        vacation_m,
        bDoSynch,
        iSynchInterval,
        emptyHouse_m
    ):
        Thread.__init__(self, name=self.text.n_SchedulerThread)
        if not eventNameOn:
            eventNameOn = name
        if not eventNameOff:
            eventNameOff = name
        self.name = name
        self.dayTimeSettings =  dayTimeSettings[:]
        self.eventNameOn = eventNameOn
        self.eventNameOff = eventNameOff
        self.finished = Event()
        self.abort = False
        self.fixedHolidays = fixedHolidays
        self.variableHolidays = variableHolidays
        self.iNbrOfBurstsON = iNbrOfBurstsON
        self.iNbrOfBurstsOFF = iNbrOfBurstsOFF
        self.cmdDelay = cmdDelay
        self.doLogLoops = doLogLoops
        self.vacation_m = vacation_m
        self.bDoSynch = bDoSynch
        self.iSynchInterval = iSynchInterval
        self.emptyHouse_m = emptyHouse_m


    def run(self):
        try:
            dummy
        except NameError:
            dummy = 0
            init = 1
            iSynch = 1
            prevDate = 0
        random.jumpahead(213)
        self.lst_3 = []


        def Check_for_holidays():
            currDate = time.strftime("%m/%d/%Y", time.localtime())
            date = time.strftime("%m%d", time.localtime())
            dateTmw = time.strftime(
                "%m%d",
                time.localtime(time.time() + 60*60*24)
            )
            dw = GetDayOfWeek(currDate)
            if dw < 6:
                dwt = dw + 1
            else:
                dwt = 0
            nDw = dw

            if (
                self.fixedHolidays.find(date) != -1
                or self.variableHolidays.find(date) != -1
            ):
                nDw = 5
                if dwt < 5:
                    nDw = 6
                if (
                    self.fixedHolidays.find(dateTmw) != -1
                    or self.variableHolidays.find(dateTmw) != -1
                ):
                    nDw = 5
            if (
                self.fixedHolidays.find(dateTmw) != -1
                or self.variableHolidays.find(dateTmw) != -1
            ):
                if nDw > 4:
                    nDw = 5
                else:
                    nDw = 4
            if self.emptyHouse_m:
                nDw = 8
                return(nDw)
            if self.vacation_m:
                nDw = 7
            return(nDw)


        def GetDayOfWeek(dateString):
            # day of week (monday = 0) of a given month/day/year
            ds = dateString.split('/')
            dayOfWeek = int(calendar.weekday(int(ds[2]),int(ds[0]),int(ds[1])))
            return(dayOfWeek)


        def GetNameOfDay(dt):
            nd = ""
            if dt == "0":
                nd = self.text.nd_mo
            if dt == "1":
                nd = self.text.nd_tu
            if dt == "2":
                nd = self.text.nd_we
            if dt == "3":
                nd = self.text.nd_th
            if dt == "4":
                nd = self.text.nd_fr
            if dt == "5":
                nd = self.text.nd_sa
            if dt == "6":
                nd = self.text.nd_su
            if dt == "7":
                nd = self.text.nd_vc
            if dt == "8":
                nd = self.text.nd_eh
            return(nd)


        def CheckIfLog(lightOld, light, iSynch, label):
            if (
                light != lightOld
                or iSynch == 1
            ):
                LogToFile(label)


        def LogToFile(s):
            timeStamp = str(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            logStr = timeStamp+"\t"+s+"<br\n>"
            fileHandle = None

            progData = eg.configDir + '\plugins\Scheduler'
            if not os.path.exists(progData) and not os.path.isdir(progData):
                    os.makedirs(progData)
            fileHandle = open(progData+'/'+'Scheduler.html', 'a')
            fileHandle.write(logStr)
            fileHandle.close()


        def StrCheck(s):
            if s == "----":
                s = "0000"
            return(s)


        def SendEvent(j):
            for i in range(j-3, j+3):
                #print self.dayTimeSettings[i]
                if i % 2 == 0: #Try ON settings
                    if trigTime == self.dayTimeSettings[i]:
                        for i in range(self.iNbrOfBurstsON):
                            eg.TriggerEvent(
                                self.eventNameOn,
                                None,
                                eg.plugins.Scheduler.plugin.eventPrefix
                            )
                            self.finished.wait(self.cmdDelay)
                        LogToFile(self.eventNameOn)

                if i % 2 == 1: #Try OFF settings
                    if trigTime == self.dayTimeSettings[i]:
                        for i in range(self.iNbrOfBurstsOFF):
                            eg.TriggerEvent(
                                self.eventNameOff,
                                None,
                                eg.plugins.Scheduler.plugin.eventPrefix
                            )
                            self.finished.wait(self.cmdDelay)
                        LogToFile(self.eventNameOff)

            #Restore device states at startup and during synch
            if (
                init == 1
                or iSynch == self.iSynchInterval
            ):
                for index, item in enumerate(self.lst_3):
                    if item != "----":
                        #print index, item

                        if index < 6: #Today
                            if item <= trigTime:
                                if index % 2 == 1:
                                    if init == 1:
                                        LogToFile(self.eventNameOn)
                                    for i in range(self.iNbrOfBurstsON):
                                        eg.TriggerEvent(
                                            self.eventNameOn,
                                            None,
                                            eg.plugins.Scheduler.plugin.eventPrefix
                                        )
                                        self.finished.wait(self.cmdDelay)
                                    break
                                if index % 2 == 0:
                                    if init == 1:
                                        LogToFile(self.eventNameOff)
                                    for i in range(self.iNbrOfBurstsOFF):
                                        eg.TriggerEvent(
                                            self.eventNameOff,
                                            None,
                                            eg.plugins.Scheduler.plugin.eventPrefix
                                        )
                                        self.finished.wait(self.cmdDelay)
                                    break

                        if index >= 6: #Yesterday & Previous days
                            if index % 2 == 1:
                                if init == 1:
                                    LogToFile(self.eventNameOn)
                                for i in range(self.iNbrOfBurstsON):
                                    eg.TriggerEvent(
                                        self.eventNameOn,
                                        None,
                                        eg.plugins.Scheduler.plugin.eventPrefix
                                    )
                                    self.finished.wait(self.cmdDelay)
                                break
                            if index % 2 == 0:
                                if init == 1:
                                    LogToFile(self.eventNameOff)
                                for i in range(self.iNbrOfBurstsOFF):
                                    eg.TriggerEvent(
                                        self.eventNameOff,
                                        None,
                                        eg.plugins.Scheduler.plugin.eventPrefix
                                    )
                                    self.finished.wait(self.cmdDelay)
                                break

        while (self.abort == False):
            # Check if vacation is enabled and if so, disable synchronizing
            self.vacation_m = eg.plugins.Scheduler.plugin.vacation_m
            if self.vacation_m:
                self.bDoSynch = False

            # Check if empty house is enabled
            self.emptyHouse_m = eg.plugins.Scheduler.plugin.emptyHouse_m

            # Count the number of runs to activate synchronization
            if self.bDoSynch:
                if iSynch >= self.iSynchInterval:
                    iSynch = 1
                else:
                    iSynch += 1

            tr = random.random()
            remain = 61.0 - int(time.strftime("%S", time.localtime())) + tr
            self.finished.wait(remain)
            if self.abort:
                break

            # Get the current date & time now, check if it has changed
            trigTime = str(time.strftime("%H%M", time.localtime()))
            currDate = str(time.strftime("%m/%d/%Y", time.localtime()))
            if currDate != prevDate:
                prevDate = 0

            # Get day of week and check for holidays
            odayType = str(GetDayOfWeek(currDate))
            dayType = str(Check_for_holidays())

            if prevDate == 0:
                # Initial logging when a new day begins
                prevDate = currDate
                od = GetNameOfDay(odayType)
                nd = GetNameOfDay(dayType)
                lg = self.text.lg_today+od
                LogToFile(lg)
                if nd != od:
                    lg = self.text.lg_dayOfWeek+od
                    LogToFile(lg)
                    if dayType == "8":
                        lg = (
                            self.text.lg_emptyHouse_1+
                            self.name+
                            " "+
                            self.text.lg_emptyHouse_2+
                            self.text.lg_emptyHouse_3+
                            nd
                        )
                        LogToFile(lg)
                    if dayType == "7":
                        lg = (
                            self.text.lg_vacation_1+
                            self.name+
                            " "+
                            self.text.lg_vacation_2+
                            self.text.lg_vacation_3+
                            nd
                        )
                        LogToFile(lg)
                    else:
                        lg = (
                            self.text.lg_holiday_1+
                            self.name+
                            " "+
                            self.text.lg_holiday_2+
                            self.text.lg_holiday_3+
                            nd
                        )
                        LogToFile(lg)

                # Create daily data for device state synchronisation
                lst_1 = self.dayTimeSettings[0:3+int(dayType)*6+3]
                lst_1.reverse()
                lst_2 = self.dayTimeSettings[3+int(dayType)*6+3:]
                lst_2.reverse()
                self.lst_3 = lst_1 + lst_2

            j = 3
            for i in range(0,9):
                #print dayType, str(i)
                if dayType == str(i):
                    SendEvent(j+i*6)

            if self.doLogLoops and init == 0:
                print (
                    self.text.nxt_1+
                    self.name+
                    self.text.nxt_2+
                    str(remain)+
                    self.text.nxt_3
                )

            init = 0


    def AbortScheduler(self):
        self.abort = True
        #print self.text.thr_abort, self.name
        self.finished.set()



class Scheduler(eg.PluginClass):
    text = Text

    def __init__(self):
        self.AddAction(SchedulerAction)
        self.AddAction(SetVacationON)
        self.AddAction(SetVacationOFF)
        self.AddAction(SetEmptyHouseON)
        self.AddAction(SetEmptyHouseOFF)
        self.AllschedulerNames = []
        self.AlldayTimeSettings = []
        self.AlleventNameOn = []
        self.AlleventNameOff = []
        self.AlliNbrOfBurstsON = []
        self.AlliNbrOfBurstsOFF = []
        self.AllcmdDelay = []
        self.AlldoLogLoops = []
        self.AllbDoSynch = []
        self.AlliSynchInterval = []
        self.lastSchedulerName = ""
        self.schedulerThreads = {}
        self.OkButtonClicked = False
        self.started = False
        self.restarted = False


    def __start__(
        self,
        fixedHolidays = "0101,0501,0606,1224,1225,1226,1231",
        variableHolidays = "0106,0321,0324,0620",
        vacation_m = False,
        emptyHouse_m = False,
        eventPrefix = "Main"
    ):
        print self.text.started
        self.vacation_m = vacation_m
        self.emptyHouse_m = emptyHouse_m
        self.fixedHolidays = fixedHolidays
        self.variableHolidays = variableHolidays
        self.eventPrefix = eventPrefix
        if self.OkButtonClicked:
            self.RestartAllSchedulers()
        if self.restarted:
            self.restarted = False
            self.RestartAllSchedulers()
        progData = eg.configDir + '\plugins\Scheduler'
        if not os.path.exists(progData) and not os.path.isdir(progData):
                os.makedirs(progData)

        self.started = True


    def __stop__(self):
        print self.text.closing
        self.AbortAllSchedulers()
        self.started = False


    def __close__(self):
        self.AbortAllSchedulers()
        self.started = False


    def SetVarMain(self, trItem, args):
        eg.actionThread.Func(trItem.SetArguments)(args) # __stop__ / __start__
        eg.document.SetIsDirty()
        eg.document.Save()
        eg.TriggerEvent(
            'Restart threads',
            None,
            self.eventPrefix
        )


    def SetVar(self, prm):
        from threading import currentThread
        trItem = self.info.treeItem
        args = list(trItem.GetArguments())
        if(
            self.emptyHouse_m <> prm['3'] or
            self.vacation_m <> prm['2']
        ):
            self.restarted = True
            for i in prm:
                arg = prm[i]
                args[int(i)] = arg
            ct = currentThread()
            if ct == eg.actionThread._ThreadWorker__thread:
                trItem.SetArguments(args) # __stop__ / __start__
                eg.document.SetIsDirty()
                eg.document.Save()
                eg.TriggerEvent(
                    'Restart threads',
                    None,
                    self.eventPrefix
                )
            else:
                eg.scheduler.AddTask(0.5, self.SetVarMain, trItem, args)
            print 'Vacation/Empty House modes changed for Scheduler: ', prm


    #methods to Control schedulers
    def StartScheduler(
        self,
        dayTimeSettings,
        name,
        eventNameOn,
        eventNameOff,
        fixedHolidays,
        variableHolidays,
        iNbrOfBurstsON,
        iNbrOfBurstsOFF,
        cmdDelay,
        doLogLoops,
        vacation_m,
        bDoSynch,
        iSynchInterval,
        emptyHouse_m
    ):

        if self.schedulerThreads.has_key(name):
            t = self.schedulerThreads[name]
            if t.isAlive():
                t.AbortScheduler()
            del self.schedulerThreads[name]
        t = SchedulerThread(
            dayTimeSettings,
            name,
            eventNameOn,
            eventNameOff,
            self.fixedHolidays,
            self.variableHolidays,
            iNbrOfBurstsON,
            iNbrOfBurstsOFF,
            cmdDelay,
            doLogLoops,
            self.vacation_m,
            bDoSynch,
            iSynchInterval,
            emptyHouse_m
        )
        self.schedulerThreads[name] = t
        t.start()


    def AbortScheduler(self, scheduler):
        if self.schedulerThreads.has_key(scheduler):
            t = self.schedulerThreads[scheduler]
            t.AbortScheduler()
            del self.schedulerThreads[scheduler]


    def AbortAllSchedulers(self):
        for i, item in enumerate(self.schedulerThreads):
            t = self.schedulerThreads[item]
            t.AbortScheduler()
            del t
            time.sleep(0.1)
        self.schedulerThreads = {}


    def RestartAllSchedulers(self, startNewIfNotAlive = True):
        self.AbortAllSchedulers()
        for i, item in enumerate(self.AllschedulerNames):
            if startNewIfNotAlive:
                time.sleep(0.1)
                self.StartScheduler(
                    self.GetAlldayTimeSettings()[i],
                    self.GetAllschedulerNames()[i],
                    self.GetAlleventNameOn()[i],
                    self.GetAlleventNameOff()[i],
                    self.fixedHolidays,
                    self.variableHolidays,
                    self.GetAlliNbrOfBurstsON()[i],
                    self.GetAlliNbrOfBurstsOFF()[i],
                    self.GetAllcmdDelay()[i],
                    self.GetAlldoLogLoops()[i],
                    self.vacation_m,
                    self.GetAllbDoSynch()[i],
                    self.GetAlliSynchInterval()[i],
                    self.emptyHouse_m
                )


    def Configure(
        self,
        fixedHolidays = "0101,0501,0606,1224,1225,1226,1231",
        variableHolidays = "0106,0321,0324,0620",
        vacation_m = False,
        emptyHouse_m = False,
        eventPrefix = "Main",
        *args
    ):

        panel = eg.ConfigPanel(self, resizable=True)

        panel.sizer.Add(
            wx.StaticText(panel, -1, self.text.listhl),
            flag = wx.ALIGN_CENTER_VERTICAL
        )

        mySizer = wx.GridBagSizer(5, 5)
        mySizer.AddGrowableRow(0)
        mySizer.AddGrowableCol(1)
        mySizer.AddGrowableCol(2)
        mySizer.AddGrowableCol(3)

        schedulerListCtrl = wx.ListCtrl(
            panel,
            -1,
            style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL
        )

        for i, colLabel in enumerate(self.text.colLabels):
            schedulerListCtrl.InsertColumn(i, colLabel)

        #setting col width to fit label
        schedulerListCtrl.InsertStringItem(0, "Test Scheduler Name")
        schedulerListCtrl.SetStringItem(0, 1, "Test EventName On")

        size = 0
        for i in range(2):
            schedulerListCtrl.SetColumnWidth(
                i,
                wx.LIST_AUTOSIZE_USEHEADER
            )
            size += schedulerListCtrl.GetColumnWidth(i)

        schedulerListCtrl.SetMinSize((size, -1))

        mySizer.Add(schedulerListCtrl, (0,0), (1, 5), flag = wx.EXPAND)

        #buttons
        abortButton = wx.Button(panel, -1, self.text.b_abort)
        mySizer.Add(abortButton, (1,0))

        abortAllButton = wx.Button(panel, -1, self.text.b_abortAll)
        mySizer.Add(abortAllButton, (1,1), flag = wx.ALIGN_RIGHT)

        restartAllButton = wx.Button(panel, -1, self.text.b_restartAll)
        mySizer.Add(restartAllButton, (1,2), flag = wx.ALIGN_RIGHT)

        refreshButton = wx.Button(panel, -1, self.text.b_refresh)
        mySizer.Add(refreshButton, (1,4), flag = wx.ALIGN_RIGHT)

        fixedHolidaysCtrl = wx.TextCtrl(panel, -1, fixedHolidays)
        fixedHolidaysCtrl.SetInitialSize((250,-1))
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtFixedHolidays
            ),
            (2,0)
        )
        mySizer.Add(fixedHolidaysCtrl,(2,1))

        variableHolidaysCtrl = wx.TextCtrl(panel, -1, variableHolidays)
        variableHolidaysCtrl.SetInitialSize((250,-1))
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtVariableHolidays
            ),
            (3,0)
        )
        mySizer.Add(variableHolidaysCtrl,(3,1))

        eventPrefixCtrl = wx.TextCtrl(panel, -1, eventPrefix)
        eventPrefixCtrl.SetInitialSize((100,-1))
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.eventPrefix
            ),
           (4,0)
        )
        mySizer.Add(eventPrefixCtrl,(4,1))

        vacation_mCtrl = wx.CheckBox(panel, -1, self.text.txtVacation_m)
        vacation_mCtrl.SetValue(vacation_m)
        mySizer.Add(vacation_mCtrl,(5,0))

        emptyHouse_mCtrl = wx.CheckBox(panel, -1, self.text.txtEmptyHouse_m)
        emptyHouse_mCtrl.SetValue(emptyHouse_m)
        mySizer.Add(emptyHouse_mCtrl,(5,1))

        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)

        def PopulateList (event):
            schedulerListCtrl.DeleteAllItems()
            row = 0
            for i, item in enumerate(self.schedulerThreads):
                t = self.schedulerThreads[item]
                if t.isAlive():
                    schedulerListCtrl.InsertStringItem(row, t.name)
                    schedulerListCtrl.SetStringItem(row,
                        1, t.eventNameOn)
                    schedulerListCtrl.SetStringItem(row,
                        2, t.eventNameOff)
                    row += 1
            ListSelection(wx.CommandEvent())


        def OnAbortButton(event):
            item = schedulerListCtrl.GetFirstSelected()
            while item != -1:
                name = schedulerListCtrl.GetItemText(item)
                self.AbortScheduler(name)
                item = schedulerListCtrl.GetNextSelected(item)
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnAbortAllButton(event):
            self.AbortAllSchedulers()
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnRestartAllButton(event):
            self.RestartAllSchedulers()
            PopulateList(wx.CommandEvent())
            event.Skip()


        def ListSelection(event):
            flag = schedulerListCtrl.GetFirstSelected() != -1
            abortButton.Enable(flag)
            event.Skip()


        def OnSize(event):
            schedulerListCtrl.SetColumnWidth(
                6,
                wx.LIST_AUTOSIZE_USEHEADER
            )
            event.Skip()


        def OnApplyButton(event):
            event.Skip()
            self.RestartAllSchedulers()
            PopulateList(wx.CommandEvent())


        def OnOkButton(event):
            event.Skip()
            self.OkButtonClicked = True


        PopulateList(wx.CommandEvent())

        abortButton.Bind(wx.EVT_BUTTON, OnAbortButton)
        abortAllButton.Bind(wx.EVT_BUTTON, OnAbortAllButton)
        restartAllButton.Bind(wx.EVT_BUTTON, OnRestartAllButton)
        refreshButton.Bind(wx.EVT_BUTTON, PopulateList)
        schedulerListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelection)
        schedulerListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelection)
        panel.Bind(wx.EVT_SIZE, OnSize)
        panel.dialog.buttonRow.applyButton.Bind(wx.EVT_BUTTON, OnApplyButton)
        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnOkButton)

        while panel.Affirmed():
            fixedHolidays = fixedHolidaysCtrl.GetValue()
            variableHolidays = variableHolidaysCtrl.GetValue()
            vacation_m = vacation_mCtrl.GetValue()
            emptyHouse_m = emptyHouse_mCtrl.GetValue()
            eventPrefix = eventPrefixCtrl.GetValue()
            panel.SetResult(
                        fixedHolidays,
                        variableHolidays,
                        vacation_m,
                        emptyHouse_m,
                        eventPrefix,
                        *args
            )


    def GetAllschedulerNames(self):
        return self.AllschedulerNames


    def GetAlldayTimeSettings(self):
        return self.AlldayTimeSettings


    def GetAlleventNameOn(self):
        return self.AlleventNameOn


    def GetAlleventNameOff(self):
        return self.AlleventNameOff


    def GetAlliNbrOfBurstsON(self):
        return self.AlliNbrOfBurstsON


    def GetAlliNbrOfBurstsOFF(self):
        return self.AlliNbrOfBurstsOFF


    def GetAllcmdDelay(self):
        return self.AllcmdDelay


    def GetAlldoLogLoops(self):
        return self.AlldoLogLoops


    def GetAllbDoSynch(self):
        return self.AllbDoSynch


    def GetAlliSynchInterval(self):
        return self.AlliSynchInterval


    def AddSchedulerName(self, schedulerName):
        if not schedulerName in self.AllschedulerNames:
            self.AllschedulerNames.append(schedulerName)
        return self.AllschedulerNames.index(schedulerName)


    def AddDayTimeSettings(self, dayTimeSettings, indx):
        try:
            del self.AlldayTimeSettings[indx]
        except IndexError:
            i = -1 # no match
        self.AlldayTimeSettings.insert(indx, dayTimeSettings)


    def AddEventNameOn(self, eventNameOn, indx):
        try:
            del self.AlleventNameOn[indx]
        except IndexError:
            i = -1 # no match
        self.AlleventNameOn.insert(indx, eventNameOn)


    def AddEventNameOff(self, eventNameOff, indx):
        try:
            del self.AlleventNameOff[indx]
        except IndexError:
            i = -1 # no match
        self.AlleventNameOff.insert(indx, eventNameOff)


    def AddInbrOfBurstsON(self, iNbrOfBurstsON, indx):
        try:
            del self.AlliNbrOfBurstsON[indx]
        except IndexError:
            i = -1 # no match
        self.AlliNbrOfBurstsON.insert(indx, iNbrOfBurstsON)


    def AddInbrOfBurstsOFF(self, iNbrOfBurstsOFF, indx):
        try:
            del self.AlliNbrOfBurstsOFF[indx]
        except IndexError:
            i = -1 # no match
        self.AlliNbrOfBurstsOFF.insert(indx, iNbrOfBurstsOFF)


    def AddCmdDelay(self, cmdDelay, indx):
        try:
            del self.AllcmdDelay[indx]
        except IndexError:
            i = -1 # no match
        self.AllcmdDelay.insert(indx, cmdDelay)


    def AddDoLogLoops(self, doLogLoops, indx):
        try:
            del self.AlldoLogLoops[indx]
        except IndexError:
            i = -1 # no match
        self.AlldoLogLoops.insert(indx, doLogLoops)


    def AddBdoSynch(self, bDoSynch, indx):
        try:
            del self.AllbDoSynch[indx]
        except IndexError:
            i = -1 # no match
        self.AllbDoSynch.insert(indx, bDoSynch)


    def AddIsynchInterval(self, iSynchInterval, indx):
        try:
            del self.AlliSynchInterval[indx]
        except IndexError:
            i = -1 # no match
        self.AlliSynchInterval.insert(indx, iSynchInterval)



class SchedulerAction(eg.ActionClass):

    def __call__(
        self,
        dayTimeSettings,
        name,
        eventNameOn,
        eventNameOff,
        mondayON_1,
        mondayON_2,
        mondayON_3,
        mondayOFF_1,
        mondayOFF_2,
        mondayOFF_3,
        tuesdayON_1,
        tuesdayON_2,
        tuesdayON_3,
        tuesdayOFF_1,
        tuesdayOFF_2,
        tuesdayOFF_3,
        wednesdayON_1,
        wednesdayON_2,
        wednesdayON_3,
        wednesdayOFF_1,
        wednesdayOFF_2,
        wednesdayOFF_3,
        thursdayON_1,
        thursdayON_2,
        thursdayON_3,
        thursdayOFF_1,
        thursdayOFF_2,
        thursdayOFF_3,
        fridayON_1,
        fridayON_2,
        fridayON_3,
        fridayOFF_1,
        fridayOFF_2,
        fridayOFF_3,
        saturdayON_1,
        saturdayON_2,
        saturdayON_3,
        saturdayOFF_1,
        saturdayOFF_2,
        saturdayOFF_3,
        sundayON_1,
        sundayON_2,
        sundayON_3,
        sundayOFF_1,
        sundayOFF_2,
        sundayOFF_3,
        vacationON_1,
        vacationON_2,
        vacationON_3,
        vacationOFF_1,
        vacationOFF_2,
        vacationOFF_3,
        fixedHolidays,
        variableHolidays,
        iNbrOfBurstsON,
        iNbrOfBurstsOFF,
        cmdDelay,
        doLogLoops,
        vacation_m,
        bDoSynch,
        iSynchInterval,
        emptyHouseON_1,
        emptyHouseON_2,
        emptyHouseON_3,
        emptyHouseOFF_1,
        emptyHouseOFF_2,
        emptyHouseOFF_3,
        emptyHouse_m
   ):
        self.plugin.StartScheduler(
            dayTimeSettings,
            name,
            eventNameOn,
            eventNameOff,
            self.plugin.fixedHolidays,
            self.plugin.variableHolidays,
            iNbrOfBurstsON,
            iNbrOfBurstsOFF,
            cmdDelay,
            doLogLoops,
            self.plugin.vacation_m,
            bDoSynch,
            iSynchInterval,
            self.plugin.emptyHouse_m
        )


    def GetLabel(
        self,
        dayTimeSettings,
        name,
        eventNameOn,
        eventNameOff,
        mondayON_1,
        mondayON_2,
        mondayON_3,
        mondayOFF_1,
        mondayOFF_2,
        mondayOFF_3,
        tuesdayON_1,
        tuesdayON_2,
        tuesdayON_3,
        tuesdayOFF_1,
        tuesdayOFF_2,
        tuesdayOFF_3,
        wednesdayON_1,
        wednesdayON_2,
        wednesdayON_3,
        wednesdayOFF_1,
        wednesdayOFF_2,
        wednesdayOFF_3,
        thursdayON_1,
        thursdayON_2,
        thursdayON_3,
        thursdayOFF_1,
        thursdayOFF_2,
        thursdayOFF_3,
        fridayON_1,
        fridayON_2,
        fridayON_3,
        fridayOFF_1,
        fridayOFF_2,
        fridayOFF_3,
        saturdayON_1,
        saturdayON_2,
        saturdayON_3,
        saturdayOFF_1,
        saturdayOFF_2,
        saturdayOFF_3,
        sundayON_1,
        sundayON_2,
        sundayON_3,
        sundayOFF_1,
        sundayOFF_2,
        sundayOFF_3,
        vacationON_1,
        vacationON_2,
        vacationON_3,
        vacationOFF_1,
        vacationOFF_2,
        vacationOFF_3,
        fixedHolidays,
        variableHolidays,
        iNbrOfBurstsON,
        iNbrOfBurstsOFF,
        cmdDelay,
        doLogLoops,
        vacation_m,
        bDoSynch,
        iSynchInterval,
        emptyHouseON_1,
        emptyHouseON_2,
        emptyHouseON_3,
        emptyHouseOFF_1,
        emptyHouseOFF_2,
        emptyHouseOFF_3,
        emptyHouse_m
    ):

        indx = self.plugin.AddSchedulerName(name)
        self.plugin.AddDayTimeSettings(dayTimeSettings, indx)
        self.plugin.AddEventNameOn(eventNameOn, indx)
        self.plugin.AddEventNameOff(eventNameOff, indx)
        self.plugin.AddInbrOfBurstsON(iNbrOfBurstsON, indx)
        self.plugin.AddInbrOfBurstsOFF(iNbrOfBurstsOFF, indx)
        self.plugin.AddCmdDelay(cmdDelay, indx)
        self.plugin.AddDoLogLoops(doLogLoops, indx)
        self.plugin.AddBdoSynch(bDoSynch, indx)
        self.plugin.AddIsynchInterval(iSynchInterval, indx)

        return self.text.labelStart % (name)


    def timeFormat(self, theString):
        if theString == "----":
            return theString
        if (
            theString == "0000"
            or theString == "000"
            or theString == "00"
            or theString == "0"
            or theString == ""
        ):
            return "----"
        if len(theString) != 4:
            return "----"
        dat1 = theString[:2]
        dat2 = theString[2:]
        if int(dat1)>23:
            dat1 = "23"
        if int(dat2)>59:
            dat2 = "59"

        return(dat1+dat2)


    def timeCheck(self, timeIntervals):
        t_list = [0]*6

        for i in range(0,3):
            theTime_1 = timeIntervals[i]
            theTime_2 = timeIntervals[i+3]

            if theTime_1 == "----":
                t_1 = 0
            else:
                t_1 = int(theTime_1)

            if theTime_2 == "----":
                t_2 = 0
            else:
                t_2 = int(theTime_2)

            if t_1 == 0:
                t_list[i] = ("----")
            else:
                tS = ""
                tL = len(str(t_1))
                if tL == 1:
                    tS = "000"+str(t_1)
                if tL == 2:
                    tS = "00"+str(t_1)
                if tL == 3:
                    tS = "0"+str(t_1)
                if tL == 4:
                    tS = str(t_1)
                t_list[i] = tS

            if t_2 <= t_1 and t_1 > 0 and t_2 != 0:
                t_2 = t_1+1
                if t_2 > 2359:
                    t_2 = 2359

            if t_2 == 0:
                t_list[i+3] = ("----")
            else:
                tS = ""
                tL = len(str(t_2))
                if tL == 1:
                    tS = "000"+str(t_2)
                if tL == 2:
                    tS = "00"+str(t_2)
                if tL == 3:
                    tS = "0"+str(t_2)
                if tL == 4:
                    tS = str(t_2)
                t_list[i+3] = tS
        return(t_list)


    def Configure(
        self,
        dayTimeSettings = [],
        name = "Give schedule a name",
        eventNameOn = "nn ON",
        eventNameOff = "nn OFF",
        mondayON_1 = "----",
        mondayON_2 = "----",
        mondayON_3 = "----",
        mondayOFF_1 = "----",
        mondayOFF_2 = "----",
        mondayOFF_3 = "----",
        tuesdayON_1 = "----",
        tuesdayON_2 = "----",
        tuesdayON_3 = "----",
        tuesdayOFF_1 = "----",
        tuesdayOFF_2 = "----",
        tuesdayOFF_3 = "----",
        wednesdayON_1 = "----",
        wednesdayON_2 = "----",
        wednesdayON_3 = "----",
        wednesdayOFF_1 = "----",
        wednesdayOFF_2 = "----",
        wednesdayOFF_3 = "----",
        thursdayON_1 = "----",
        thursdayON_2 = "----",
        thursdayON_3 = "----",
        thursdayOFF_1 = "----",
        thursdayOFF_2 = "----",
        thursdayOFF_3 = "----",
        fridayON_1 = "----",
        fridayON_2 = "----",
        fridayON_3 = "----",
        fridayOFF_1 = "----",
        fridayOFF_2 = "----",
        fridayOFF_3 = "----",
        saturdayON_1 = "----",
        saturdayON_2 = "----",
        saturdayON_3 = "----",
        saturdayOFF_1 = "----",
        saturdayOFF_2 = "----",
        saturdayOFF_3 = "----",
        sundayON_1 = "----",
        sundayON_2 = "----",
        sundayON_3 = "----",
        sundayOFF_1 = "----",
        sundayOFF_2 = "----",
        sundayOFF_3 = "----",
        vacationON_1 = "----",
        vacationON_2 = "----",
        vacationON_3 = "----",
        vacationOFF_1 = "----",
        vacationOFF_2 = "----",
        vacationOFF_3 = "----",
        fixedHolidays = "0101,0501,0606,1224,1225,1226,1231",
        variableHolidays = "0106,0321,0324,0620",
        iNbrOfBurstsON = 1,
        iNbrOfBurstsOFF = 1,
        cmdDelay = 1.5,
        doLogLoops = False,
        vacation_m = False,
        bDoSynch = True,
        iSynchInterval = 30,
        emptyHouseON_1 = "----",
        emptyHouseON_2 = "----",
        emptyHouseON_3 = "----",
        emptyHouseOFF_1 = "----",
        emptyHouseOFF_2 = "----",
        emptyHouseOFF_3 = "----",
        emptyHouse_m = False
    ):

        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(5, 5)
        mySizer_3 = wx.GridBagSizer(10, 10)

        #name
        schedulerNameCtrl = wx.TextCtrl(panel, -1, name)
        schedulerNameCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.name), (0,0))
        mySizer_1.Add(schedulerNameCtrl, (0,1))

        #eventName ON
        eventNameOnCtrl = wx.TextCtrl(panel, -1, eventNameOn)
        eventNameOnCtrl.SetInitialSize((150,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.eventNameOn), (1,0))
        mySizer_1.Add(eventNameOnCtrl, (1,1))

        #eventName OFF
        eventNameOffCtrl = wx.TextCtrl(panel, -1, eventNameOff)
        eventNameOffCtrl.SetInitialSize((150,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.eventNameOff), (2,0))
        mySizer_1.Add(eventNameOffCtrl, (2,1))

        mondayON_1Ctrl = wx.TextCtrl(panel, -1, mondayON_1)
        mondayON_1Ctrl.SetInitialSize((35,-1))
        mondayOFF_1Ctrl = wx.TextCtrl(panel, -1, mondayOFF_1)
        mondayOFF_1Ctrl.SetInitialSize((35,-1))
        mondayON_2Ctrl = wx.TextCtrl(panel, -1, mondayON_2)
        mondayON_2Ctrl.SetInitialSize((35,-1))
        mondayOFF_2Ctrl = wx.TextCtrl(panel, -1, mondayOFF_2)
        mondayOFF_2Ctrl.SetInitialSize((35,-1))
        mondayON_3Ctrl = wx.TextCtrl(panel, -1, mondayON_3)
        mondayON_3Ctrl.SetInitialSize((35,-1))
        mondayOFF_3Ctrl = wx.TextCtrl(panel, -1, mondayOFF_3)
        mondayOFF_3Ctrl.SetInitialSize((35,-1))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.moON), (1,0))
        mySizer_2.Add(mondayON_1Ctrl, (1,1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (1,2))
        mySizer_2.Add(mondayOFF_1Ctrl, (1,3))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (1,4))
        mySizer_2.Add(mondayON_2Ctrl, (1,5))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (1,6))
        mySizer_2.Add(mondayOFF_2Ctrl, (1,7))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (1,8))
        mySizer_2.Add(mondayON_3Ctrl, (1,9))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (1,10))
        mySizer_2.Add(mondayOFF_3Ctrl, (1,11))

        tuesdayON_1Ctrl = wx.TextCtrl(panel, -1, tuesdayON_1)
        tuesdayON_1Ctrl.SetInitialSize((35,-1))
        tuesdayOFF_1Ctrl = wx.TextCtrl(panel, -1, tuesdayOFF_1)
        tuesdayOFF_1Ctrl.SetInitialSize((35,-1))
        tuesdayON_2Ctrl = wx.TextCtrl(panel, -1, tuesdayON_2)
        tuesdayON_2Ctrl.SetInitialSize((35,-1))
        tuesdayOFF_2Ctrl = wx.TextCtrl(panel, -1, tuesdayOFF_2)
        tuesdayOFF_2Ctrl.SetInitialSize((35,-1))
        tuesdayON_3Ctrl = wx.TextCtrl(panel, -1, tuesdayON_3)
        tuesdayON_3Ctrl.SetInitialSize((35,-1))
        tuesdayOFF_3Ctrl = wx.TextCtrl(panel, -1, tuesdayOFF_3)
        tuesdayOFF_3Ctrl.SetInitialSize((35,-1))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.tuON), (2,0))
        mySizer_2.Add(tuesdayON_1Ctrl, (2,1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (2,2))
        mySizer_2.Add(tuesdayOFF_1Ctrl, (2,3))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (2,4))
        mySizer_2.Add(tuesdayON_2Ctrl, (2,5))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (2,6))
        mySizer_2.Add(tuesdayOFF_2Ctrl, (2,7))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (2,8))
        mySizer_2.Add(tuesdayON_3Ctrl, (2,9))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (2,10))
        mySizer_2.Add(tuesdayOFF_3Ctrl, (2,11))

        wednesdayON_1Ctrl = wx.TextCtrl(panel, -1, wednesdayON_1)
        wednesdayON_1Ctrl.SetInitialSize((35,-1))
        wednesdayOFF_1Ctrl = wx.TextCtrl(panel, -1, wednesdayOFF_1)
        wednesdayOFF_1Ctrl.SetInitialSize((35,-1))
        wednesdayON_2Ctrl = wx.TextCtrl(panel, -1, wednesdayON_2)
        wednesdayON_2Ctrl.SetInitialSize((35,-1))
        wednesdayOFF_2Ctrl = wx.TextCtrl(panel, -1, wednesdayOFF_2)
        wednesdayOFF_2Ctrl.SetInitialSize((35,-1))
        wednesdayON_3Ctrl = wx.TextCtrl(panel, -1, wednesdayON_3)
        wednesdayON_3Ctrl.SetInitialSize((35,-1))
        wednesdayOFF_3Ctrl = wx.TextCtrl(panel, -1, wednesdayOFF_3)
        wednesdayOFF_3Ctrl.SetInitialSize((35,-1))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.weON), (3,0))
        mySizer_2.Add(wednesdayON_1Ctrl, (3,1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (3,2))
        mySizer_2.Add(wednesdayOFF_1Ctrl, (3,3))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (3,4))
        mySizer_2.Add(wednesdayON_2Ctrl, (3,5))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (3,6))
        mySizer_2.Add(wednesdayOFF_2Ctrl, (3,7))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (3,8))
        mySizer_2.Add(wednesdayON_3Ctrl, (3,9))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (3,10))
        mySizer_2.Add(wednesdayOFF_3Ctrl, (3,11))

        thursdayON_1Ctrl = wx.TextCtrl(panel, -1, thursdayON_1)
        thursdayON_1Ctrl.SetInitialSize((35,-1))
        thursdayOFF_1Ctrl = wx.TextCtrl(panel, -1, thursdayOFF_1)
        thursdayOFF_1Ctrl.SetInitialSize((35,-1))
        thursdayON_2Ctrl = wx.TextCtrl(panel, -1, thursdayON_2)
        thursdayON_2Ctrl.SetInitialSize((35,-1))
        thursdayOFF_2Ctrl = wx.TextCtrl(panel, -1, thursdayOFF_2)
        thursdayOFF_2Ctrl.SetInitialSize((35,-1))
        thursdayON_3Ctrl = wx.TextCtrl(panel, -1, thursdayON_3)
        thursdayON_3Ctrl.SetInitialSize((35,-1))
        thursdayOFF_3Ctrl = wx.TextCtrl(panel, -1, thursdayOFF_3)
        thursdayOFF_3Ctrl.SetInitialSize((35,-1))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.thON), (4,0))
        mySizer_2.Add(thursdayON_1Ctrl, (4,1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (4,2))
        mySizer_2.Add(thursdayOFF_1Ctrl, (4,3))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (4,4))
        mySizer_2.Add(thursdayON_2Ctrl, (4,5))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (4,6))
        mySizer_2.Add(thursdayOFF_2Ctrl, (4,7))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (4,8))
        mySizer_2.Add(thursdayON_3Ctrl, (4,9))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (4,10))
        mySizer_2.Add(thursdayOFF_3Ctrl, (4,11))

        fridayON_1Ctrl = wx.TextCtrl(panel, -1, fridayON_1)
        fridayON_1Ctrl.SetInitialSize((35,-1))
        fridayOFF_1Ctrl = wx.TextCtrl(panel, -1, fridayOFF_1)
        fridayOFF_1Ctrl.SetInitialSize((35,-1))
        fridayON_2Ctrl = wx.TextCtrl(panel, -1, fridayON_2)
        fridayON_2Ctrl.SetInitialSize((35,-1))
        fridayOFF_2Ctrl = wx.TextCtrl(panel, -1, fridayOFF_2)
        fridayOFF_2Ctrl.SetInitialSize((35,-1))
        fridayON_3Ctrl = wx.TextCtrl(panel, -1, fridayON_3)
        fridayON_3Ctrl.SetInitialSize((35,-1))
        fridayOFF_3Ctrl = wx.TextCtrl(panel, -1, fridayOFF_3)
        fridayOFF_3Ctrl.SetInitialSize((35,-1))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.frON), (5,0))
        mySizer_2.Add(fridayON_1Ctrl, (5,1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (5,2))
        mySizer_2.Add(fridayOFF_1Ctrl, (5,3))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (5,4))
        mySizer_2.Add(fridayON_2Ctrl, (5,5))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (5,6))
        mySizer_2.Add(fridayOFF_2Ctrl, (5,7))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (5,8))
        mySizer_2.Add(fridayON_3Ctrl, (5,9))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (5,10))
        mySizer_2.Add(fridayOFF_3Ctrl, (5,11))

        saturdayON_1Ctrl = wx.TextCtrl(panel, -1, saturdayON_1)
        saturdayON_1Ctrl.SetInitialSize((35,-1))
        saturdayOFF_1Ctrl = wx.TextCtrl(panel, -1, saturdayOFF_1)
        saturdayOFF_1Ctrl.SetInitialSize((35,-1))
        saturdayON_2Ctrl = wx.TextCtrl(panel, -1, saturdayON_2)
        saturdayON_2Ctrl.SetInitialSize((35,-1))
        saturdayOFF_2Ctrl = wx.TextCtrl(panel, -1, saturdayOFF_2)
        saturdayOFF_2Ctrl.SetInitialSize((35,-1))
        saturdayON_3Ctrl = wx.TextCtrl(panel, -1, saturdayON_3)
        saturdayON_3Ctrl.SetInitialSize((35,-1))
        saturdayOFF_3Ctrl = wx.TextCtrl(panel, -1, saturdayOFF_3)
        saturdayOFF_3Ctrl.SetInitialSize((35,-1))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.saON), (6,0))
        mySizer_2.Add(saturdayON_1Ctrl, (6,1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (6,2))
        mySizer_2.Add(saturdayOFF_1Ctrl, (6,3))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (6,4))
        mySizer_2.Add(saturdayON_2Ctrl, (6,5))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (6,6))
        mySizer_2.Add(saturdayOFF_2Ctrl, (6,7))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (6,8))
        mySizer_2.Add(saturdayON_3Ctrl, (6,9))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (6,10))
        mySizer_2.Add(saturdayOFF_3Ctrl, (6,11))

        sundayON_1Ctrl = wx.TextCtrl(panel, -1, sundayON_1)
        sundayON_1Ctrl.SetInitialSize((35,-1))
        sundayOFF_1Ctrl = wx.TextCtrl(panel, -1, sundayOFF_1)
        sundayOFF_1Ctrl.SetInitialSize((35,-1))
        sundayON_2Ctrl = wx.TextCtrl(panel, -1, sundayON_2)
        sundayON_2Ctrl.SetInitialSize((35,-1))
        sundayOFF_2Ctrl = wx.TextCtrl(panel, -1, sundayOFF_2)
        sundayOFF_2Ctrl.SetInitialSize((35,-1))
        sundayON_3Ctrl = wx.TextCtrl(panel, -1, sundayON_3)
        sundayON_3Ctrl.SetInitialSize((35,-1))
        sundayOFF_3Ctrl = wx.TextCtrl(panel, -1, sundayOFF_3)
        sundayOFF_3Ctrl.SetInitialSize((35,-1))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.suON), (7,0))
        mySizer_2.Add(sundayON_1Ctrl, (7,1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (7,2))
        mySizer_2.Add(sundayOFF_1Ctrl, (7,3))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (7,4))
        mySizer_2.Add(sundayON_2Ctrl, (7,5))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (7,6))
        mySizer_2.Add(sundayOFF_2Ctrl, (7,7))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (7,8))
        mySizer_2.Add(sundayON_3Ctrl, (7,9))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (7,10))
        mySizer_2.Add(sundayOFF_3Ctrl, (7,11))

        vacationON_1Ctrl = wx.TextCtrl(panel, -1, vacationON_1)
        vacationON_1Ctrl.SetInitialSize((35,-1))
        vacationOFF_1Ctrl = wx.TextCtrl(panel, -1, vacationOFF_1)
        vacationOFF_1Ctrl.SetInitialSize((35,-1))
        vacationON_2Ctrl = wx.TextCtrl(panel, -1, vacationON_2)
        vacationON_2Ctrl.SetInitialSize((35,-1))
        vacationOFF_2Ctrl = wx.TextCtrl(panel, -1, vacationOFF_2)
        vacationOFF_2Ctrl.SetInitialSize((35,-1))
        vacationON_3Ctrl = wx.TextCtrl(panel, -1, vacationON_3)
        vacationON_3Ctrl.SetInitialSize((35,-1))
        vacationOFF_3Ctrl = wx.TextCtrl(panel, -1, vacationOFF_3)
        vacationOFF_3Ctrl.SetInitialSize((35,-1))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.vcON), (8,0))
        mySizer_2.Add(vacationON_1Ctrl, (8,1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (8,2))
        mySizer_2.Add(vacationOFF_1Ctrl, (8,3))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (8,4))
        mySizer_2.Add(vacationON_2Ctrl, (8,5))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (8,6))
        mySizer_2.Add(vacationOFF_2Ctrl, (8,7))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (8,8))
        mySizer_2.Add(vacationON_3Ctrl, (8,9))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (8,10))
        mySizer_2.Add(vacationOFF_3Ctrl, (8,11))

        emptyHouseON_1Ctrl = wx.TextCtrl(panel, -1, emptyHouseON_1)
        emptyHouseON_1Ctrl.SetInitialSize((35,-1))
        emptyHouseOFF_1Ctrl = wx.TextCtrl(panel, -1, emptyHouseOFF_1)
        emptyHouseOFF_1Ctrl.SetInitialSize((35,-1))
        emptyHouseON_2Ctrl = wx.TextCtrl(panel, -1, emptyHouseON_2)
        emptyHouseON_2Ctrl.SetInitialSize((35,-1))
        emptyHouseOFF_2Ctrl = wx.TextCtrl(panel, -1, emptyHouseOFF_2)
        emptyHouseOFF_2Ctrl.SetInitialSize((35,-1))
        emptyHouseON_3Ctrl = wx.TextCtrl(panel, -1, emptyHouseON_3)
        emptyHouseON_3Ctrl.SetInitialSize((35,-1))
        emptyHouseOFF_3Ctrl = wx.TextCtrl(panel, -1, emptyHouseOFF_3)
        emptyHouseOFF_3Ctrl.SetInitialSize((35,-1))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.ehON), (9,0))
        mySizer_2.Add(emptyHouseON_1Ctrl, (9,1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (9,2))
        mySizer_2.Add(emptyHouseOFF_1Ctrl, (9,3))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (9,4))
        mySizer_2.Add(emptyHouseON_2Ctrl, (9,5))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (9,6))
        mySizer_2.Add(emptyHouseOFF_2Ctrl, (9,7))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtON), (9,8))
        mySizer_2.Add(emptyHouseON_3Ctrl, (9,9))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtOFF), (9,10))
        mySizer_2.Add(emptyHouseOFF_3Ctrl, (9,11))

        iNbrOfBurstsCtrlON = panel.SpinIntCtrl(iNbrOfBurstsON, 1, 10)
        iNbrOfBurstsCtrlON.SetInitialSize((45,-1))

        mySizer_3.Add(wx.StaticText(panel, -1, self.text.txtNbrBursts), (1,0))
        mySizer_3.Add(wx.StaticText(panel, -1, self.text.txtON), (1,1))
        mySizer_3.Add(iNbrOfBurstsCtrlON, (1,2))

        iNbrOfBurstsCtrlOFF = panel.SpinIntCtrl(iNbrOfBurstsOFF, 1, 10)
        iNbrOfBurstsCtrlOFF.SetInitialSize((45,-1))

        mySizer_3.Add(wx.StaticText(panel, -1, self.text.txtNbrBursts), (2,0))
        mySizer_3.Add(wx.StaticText(panel, -1, self.text.txtOFF), (2,1))
        mySizer_3.Add(iNbrOfBurstsCtrlOFF, (2,2))

        cmdDelayCtrl = panel.SpinNumCtrl(
            cmdDelay,
            decimalChar = '.', # by default, use '.' for decimal point
            groupChar = ',',   # by default, use ',' for grouping
            integerWidth = 2,
            fractionWidth = 1,
            min = 0.5,
            max = 5.0,
            increment = 0.5
        )
        cmdDelayCtrl.SetInitialSize((45,-1))

        mySizer_3.Add(wx.StaticText(panel, -1, self.text.txtCmdDelay), (3,0))
        mySizer_3.Add(cmdDelayCtrl, (3,1))

        doLogLoopsCtrl = wx.CheckBox(panel, -1, "")
        doLogLoopsCtrl.SetValue(doLogLoops)

        mySizer_3.Add(wx.StaticText(panel, -1, self.text.doLogLoopsText), (4,0))
        mySizer_3.Add(doLogLoopsCtrl, (4,1))

        bDoSynchCtrl = wx.CheckBox(panel, -1, "")
        bDoSynchCtrl.SetValue(bDoSynch)

        mySizer_3.Add(wx.StaticText(panel, -1, self.text.bDoSynchText), (5,0))
        mySizer_3.Add(bDoSynchCtrl, (5,1))

        iSynchIntervalCtrl = panel.SpinIntCtrl(iSynchInterval, 6, 600)
        iSynchIntervalCtrl.SetInitialSize((50,-1))

        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtSynchInterval
            ),
            (6,0)
        )
        mySizer_3.Add(iSynchIntervalCtrl, (6,1))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_3, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            dayTimeSettings = []
            name = schedulerNameCtrl.GetValue()
            plugin.lastSchedulerName = name
            indx = plugin.AddSchedulerName(name)
            eventNameOn = eventNameOnCtrl.GetValue()
            plugin.AddEventNameOn(eventNameOn, indx)
            eventNameOff = eventNameOffCtrl.GetValue()
            plugin.AddEventNameOff(eventNameOff, indx)
            fixedHolidays = self.plugin.fixedHolidays
            variableHolidays = self.plugin.variableHolidays
            iNbrOfBurstsON = iNbrOfBurstsCtrlON.GetValue()
            plugin.AddInbrOfBurstsON(iNbrOfBurstsON, indx)
            iNbrOfBurstsOFF = iNbrOfBurstsCtrlOFF.GetValue()
            plugin.AddInbrOfBurstsOFF(iNbrOfBurstsOFF, indx)
            cmdDelay = cmdDelayCtrl.GetValue()
            plugin.AddCmdDelay(cmdDelay, indx)
            doLogLoops = doLogLoopsCtrl.GetValue()
            plugin.AddDoLogLoops(doLogLoops, indx)
            vacation_m = self.plugin.vacation_m
            emptyHouse_m = self.plugin.emptyHouse_m
            bDoSynch = bDoSynchCtrl.GetValue()
            plugin.AddBdoSynch(bDoSynch, indx)
            iSynchInterval = iSynchIntervalCtrl.GetValue()
            plugin.AddIsynchInterval(iSynchInterval, indx)

            mondayON_1 = self.timeFormat(mondayON_1Ctrl.GetValue())
            mondayOFF_1 = self.timeFormat(mondayOFF_1Ctrl.GetValue())
            mondayON_2 = self.timeFormat(mondayON_2Ctrl.GetValue())
            mondayOFF_2 = self.timeFormat(mondayOFF_2Ctrl.GetValue())
            mondayON_3 = self.timeFormat(mondayON_3Ctrl.GetValue())
            mondayOFF_3 = self.timeFormat(mondayOFF_3Ctrl.GetValue())

            moList = []
            moList.append(mondayON_1)
            moList.append(mondayOFF_1)
            moList.append(mondayON_2)
            moList.append(mondayOFF_2)
            moList.append(mondayON_3)
            moList.append(mondayOFF_3)
            moList = self.timeCheck(moList)
            mondayON_1 = moList[0]
            mondayON_2 = moList[2]
            mondayON_3 = moList[4]
            mondayOFF_1 = moList[1]
            mondayOFF_2 = moList[3]
            mondayOFF_3 = moList[5]
            dayTimeSettings += moList

            tuesdayON_1 = self.timeFormat(tuesdayON_1Ctrl.GetValue())
            tuesdayOFF_1 = self.timeFormat(tuesdayOFF_1Ctrl.GetValue())
            tuesdayON_2 = self.timeFormat(tuesdayON_2Ctrl.GetValue())
            tuesdayOFF_2 = self.timeFormat(tuesdayOFF_2Ctrl.GetValue())
            tuesdayON_3 = self.timeFormat(tuesdayON_3Ctrl.GetValue())
            tuesdayOFF_3 = self.timeFormat(tuesdayOFF_3Ctrl.GetValue())

            tuList = []
            tuList.append(tuesdayON_1)
            tuList.append(tuesdayOFF_1)
            tuList.append(tuesdayON_2)
            tuList.append(tuesdayOFF_2)
            tuList.append(tuesdayON_3)
            tuList.append(tuesdayOFF_3)
            tuList = self.timeCheck(tuList)
            tuesdayON_1 = tuList[0]
            tuesdayON_2 = tuList[2]
            tuesdayON_3 = tuList[4]
            tuesdayOFF_1 = tuList[1]
            tuesdayOFF_2 = tuList[3]
            tuesdayOFF_3 = tuList[5]
            dayTimeSettings += tuList

            wednesdayON_1 = self.timeFormat(wednesdayON_1Ctrl.GetValue())
            wednesdayOFF_1 = self.timeFormat(wednesdayOFF_1Ctrl.GetValue())
            wednesdayON_2 = self.timeFormat(wednesdayON_2Ctrl.GetValue())
            wednesdayOFF_2 = self.timeFormat(wednesdayOFF_2Ctrl.GetValue())
            wednesdayON_3 = self.timeFormat(wednesdayON_3Ctrl.GetValue())
            wednesdayOFF_3 = self.timeFormat(wednesdayOFF_3Ctrl.GetValue())

            weList = []
            weList.append(wednesdayON_1)
            weList.append(wednesdayOFF_1)
            weList.append(wednesdayON_2)
            weList.append(wednesdayOFF_2)
            weList.append(wednesdayON_3)
            weList.append(wednesdayOFF_3)
            weList = self.timeCheck(weList)
            wednesdayON_1 = weList[0]
            wednesdayON_2 = weList[2]
            wednesdayON_3 = weList[4]
            wednesdayOFF_1 = weList[1]
            wednesdayOFF_2 = weList[3]
            wednesdayOFF_3 = weList[5]
            dayTimeSettings += weList

            thursdayON_1 = self.timeFormat(thursdayON_1Ctrl.GetValue())
            thursdayOFF_1 = self.timeFormat(thursdayOFF_1Ctrl.GetValue())
            thursdayON_2 = self.timeFormat(thursdayON_2Ctrl.GetValue())
            thursdayOFF_2 = self.timeFormat(thursdayOFF_2Ctrl.GetValue())
            thursdayON_3 = self.timeFormat(thursdayON_3Ctrl.GetValue())
            thursdayOFF_3 = self.timeFormat(thursdayOFF_3Ctrl.GetValue())

            thList = []
            thList.append(thursdayON_1)
            thList.append(thursdayOFF_1)
            thList.append(thursdayON_2)
            thList.append(thursdayOFF_2)
            thList.append(thursdayON_3)
            thList.append(thursdayOFF_3)
            thList = self.timeCheck(thList)
            thursdayON_1 = thList[0]
            thursdayON_2 = thList[2]
            thursdayON_3 = thList[4]
            thursdayOFF_1 = thList[1]
            thursdayOFF_2 = thList[3]
            thursdayOFF_3 = thList[5]
            dayTimeSettings += thList

            fridayON_1 = self.timeFormat(fridayON_1Ctrl.GetValue())
            fridayOFF_1 = self.timeFormat(fridayOFF_1Ctrl.GetValue())
            fridayON_2 = self.timeFormat(fridayON_2Ctrl.GetValue())
            fridayOFF_2 = self.timeFormat(fridayOFF_2Ctrl.GetValue())
            fridayON_3 = self.timeFormat(fridayON_3Ctrl.GetValue())
            fridayOFF_3 = self.timeFormat(fridayOFF_3Ctrl.GetValue())

            frList = []
            frList.append(fridayON_1)
            frList.append(fridayOFF_1)
            frList.append(fridayON_2)
            frList.append(fridayOFF_2)
            frList.append(fridayON_3)
            frList.append(fridayOFF_3)
            frList = self.timeCheck(frList)
            fridayON_1 = frList[0]
            fridayON_2 = frList[2]
            fridayON_3 = frList[4]
            fridayOFF_1 = frList[1]
            fridayOFF_2 = frList[3]
            fridayOFF_3 = frList[5]
            dayTimeSettings += frList

            saturdayON_1 = self.timeFormat(saturdayON_1Ctrl.GetValue())
            saturdayOFF_1 = self.timeFormat(saturdayOFF_1Ctrl.GetValue())
            saturdayON_2 = self.timeFormat(saturdayON_2Ctrl.GetValue())
            saturdayOFF_2 = self.timeFormat(saturdayOFF_2Ctrl.GetValue())
            saturdayON_3 = self.timeFormat(saturdayON_3Ctrl.GetValue())
            saturdayOFF_3 = self.timeFormat(saturdayOFF_3Ctrl.GetValue())

            saList = []
            saList.append(saturdayON_1)
            saList.append(saturdayOFF_1)
            saList.append(saturdayON_2)
            saList.append(saturdayOFF_2)
            saList.append(saturdayON_3)
            saList.append(saturdayOFF_3)
            saList = self.timeCheck(saList)
            saturdayON_1 = saList[0]
            saturdayON_2 = saList[2]
            saturdayON_3 = saList[4]
            saturdayOFF_1 = saList[1]
            saturdayOFF_2 = saList[3]
            saturdayOFF_3 = saList[5]
            dayTimeSettings += saList

            sundayON_1 = self.timeFormat(sundayON_1Ctrl.GetValue())
            sundayOFF_1 = self.timeFormat(sundayOFF_1Ctrl.GetValue())
            sundayON_2 = self.timeFormat(sundayON_2Ctrl.GetValue())
            sundayOFF_2 = self.timeFormat(sundayOFF_2Ctrl.GetValue())
            sundayON_3 = self.timeFormat(sundayON_3Ctrl.GetValue())
            sundayOFF_3 = self.timeFormat(sundayOFF_3Ctrl.GetValue())

            suList = []
            suList.append(sundayON_1)
            suList.append(sundayOFF_1)
            suList.append(sundayON_2)
            suList.append(sundayOFF_2)
            suList.append(sundayON_3)
            suList.append(sundayOFF_3)
            suList = self.timeCheck(suList)
            sundayON_1 = suList[0]
            sundayON_2 = suList[2]
            sundayON_3 = suList[4]
            sundayOFF_1 = suList[1]
            sundayOFF_2 = suList[3]
            sundayOFF_3 = suList[5]
            dayTimeSettings += suList

            vacationON_1 = self.timeFormat(vacationON_1Ctrl.GetValue())
            vacationOFF_1 = self.timeFormat(vacationOFF_1Ctrl.GetValue())
            vacationON_2 = self.timeFormat(vacationON_2Ctrl.GetValue())
            vacationOFF_2 = self.timeFormat(vacationOFF_2Ctrl.GetValue())
            vacationON_3 = self.timeFormat(vacationON_3Ctrl.GetValue())
            vacationOFF_3 = self.timeFormat(vacationOFF_3Ctrl.GetValue())

            vaList = []
            vaList.append(vacationON_1)
            vaList.append(vacationOFF_1)
            vaList.append(vacationON_2)
            vaList.append(vacationOFF_2)
            vaList.append(vacationON_3)
            vaList.append(vacationOFF_3)
            vaList = self.timeCheck(vaList)
            vacationON_1 = vaList[0]
            vacationON_2 = vaList[2]
            vacationON_3 = vaList[4]
            vacationOFF_1 = vaList[1]
            vacationOFF_2 = vaList[3]
            vacationOFF_3 = vaList[5]
            dayTimeSettings += vaList

            emptyHouseON_1 = self.timeFormat(emptyHouseON_1Ctrl.GetValue())
            emptyHouseOFF_1 = self.timeFormat(emptyHouseOFF_1Ctrl.GetValue())
            emptyHouseON_2 = self.timeFormat(emptyHouseON_2Ctrl.GetValue())
            emptyHouseOFF_2 = self.timeFormat(emptyHouseOFF_2Ctrl.GetValue())
            emptyHouseON_3 = self.timeFormat(emptyHouseON_3Ctrl.GetValue())
            emptyHouseOFF_3 = self.timeFormat(emptyHouseOFF_3Ctrl.GetValue())

            ehList = []
            ehList.append(emptyHouseON_1)
            ehList.append(emptyHouseOFF_1)
            ehList.append(emptyHouseON_2)
            ehList.append(emptyHouseOFF_2)
            ehList.append(emptyHouseON_3)
            ehList.append(emptyHouseOFF_3)
            ehList = self.timeCheck(ehList)
            emptyHouseON_1 = ehList[0]
            emptyHouseON_2 = ehList[2]
            emptyHouseON_3 = ehList[4]
            emptyHouseOFF_1 = ehList[1]
            emptyHouseOFF_2 = ehList[3]
            emptyHouseOFF_3 = ehList[5]
            dayTimeSettings += ehList

            plugin.AddDayTimeSettings(dayTimeSettings, indx)

            panel.SetResult(
                dayTimeSettings,
                name,
                eventNameOn,
                eventNameOff,
                mondayON_1,
                mondayON_2,
                mondayON_3,
                mondayOFF_1,
                mondayOFF_2,
                mondayOFF_3,
                tuesdayON_1,
                tuesdayON_2,
                tuesdayON_3,
                tuesdayOFF_1,
                tuesdayOFF_2,
                tuesdayOFF_3,
                wednesdayON_1,
                wednesdayON_2,
                wednesdayON_3,
                wednesdayOFF_1,
                wednesdayOFF_2,
                wednesdayOFF_3,
                thursdayON_1,
                thursdayON_2,
                thursdayON_3,
                thursdayOFF_1,
                thursdayOFF_2,
                thursdayOFF_3,
                fridayON_1,
                fridayON_2,
                fridayON_3,
                fridayOFF_1,
                fridayOFF_2,
                fridayOFF_3,
                saturdayON_1,
                saturdayON_2,
                saturdayON_3,
                saturdayOFF_1,
                saturdayOFF_2,
                saturdayOFF_3,
                sundayON_1,
                sundayON_2,
                sundayON_3,
                sundayOFF_1,
                sundayOFF_2,
                sundayOFF_3,
                vacationON_1,
                vacationON_2,
                vacationON_3,
                vacationOFF_1,
                vacationOFF_2,
                vacationOFF_3,
                fixedHolidays,
                variableHolidays,
                iNbrOfBurstsON,
                iNbrOfBurstsOFF,
                cmdDelay,
                doLogLoops,
                vacation_m,
                bDoSynch,
                iSynchInterval,
                emptyHouseON_1,
                emptyHouseON_2,
                emptyHouseON_3,
                emptyHouseOFF_1,
                emptyHouseOFF_2,
                emptyHouseOFF_3,
                emptyHouse_m
            )

            self.plugin.StartScheduler(
                dayTimeSettings,
                name,
                eventNameOn,
                eventNameOff,
                self.plugin.fixedHolidays,
                self.plugin.variableHolidays,
                iNbrOfBurstsON,
                iNbrOfBurstsOFF,
                cmdDelay,
                doLogLoops,
                self.plugin.vacation_m,
                bDoSynch,
                iSynchInterval,
                self.plugin.emptyHouse_m
            )



class SetVacationON(eg.ActionClass):
    name = "Vacation ON"
    description = "Action to set the Vacation flag TRUE"

    def __call__(self):
        if self.plugin.started:
            prm = {'3':self.plugin.emptyHouse_m, '2':True}
            self.plugin.SetVar(prm)
        else:
            print self.text.txtInit



class SetVacationOFF(eg.ActionClass):
    name = "Vacation OFF"
    description = "Action to set the Vacation flag FALSE"

    def __call__(self):
        if self.plugin.started:
            prm = {'3':self.plugin.emptyHouse_m, '2':False}
            self.plugin.SetVar(prm)
        else:
            print self.text.txtInit



class SetEmptyHouseON(eg.ActionClass):
    name = "EmptyHouse ON"
    description = "Action to set the EmptyHouse flag TRUE"

    def __call__(self):
        if self.plugin.started:
            prm = {'3':True, '2':self.plugin.vacation_m}
            self.plugin.SetVar(prm)
        else:
            print self.text.txtInit



class SetEmptyHouseOFF(eg.ActionClass):
    name = "EmptyHouse OFF"
    description = "Action to set the EmptyHouse flag FALSE"

    def __call__(self):
        if self.plugin.started:
            prm = {'3':False, '2':self.plugin.vacation_m}
            self.plugin.SetVar(prm)
        else:
            print self.text.txtInit


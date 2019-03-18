# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright (C) 2014 Walter Kraembring <krambriw>.
#
###############################################################################
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
#
# Acknowledgements: 
#
##############################################################################
# Revision history:
#
# 2014-07-02  Modifications & corrections of the control logic
# 2014-06-07  First public version 
##############################################################################

import eg

eg.RegisterPlugin(
    name="AwningManager",
    guid='{7388955C-1112-49FB-9F1F-C7A4D9D9EE50}',
    author="Walter Kraembring",
    version="1.0.1",
    kind="other",
    canMultiLoad=True,
    description=(
        "Used to manage power supply and maneuvers to awnings, blinds or "
        " shutters during summer season at configurable times considering "
        " weather conditions and readings from an external light sensor. "
        " For the sunstate and weather conditions, this plugin requires "
        " the SunTracker plugin to be installed. "
        " To capture sensor readings and to send maneuvers, suitable plugins "
        " are required. "
    ),
    url="http://www.eventghost.org/forum",
)

import os
import random
import time
import wx
from threading import Event, Thread

import weather_conditions_abs


class Text:
    started = "Plugin started"
    pHeading = "Common Plug-In Settings"
    controlerFinished = "Awning Controler finished"
    listhl = "Currently active Controlers:"
    colLabels = (
        "Controler Name",
        "START event name ",
        "END event name"
    )
    # Buttons
    b_abort = "Abort"
    b_abortAll = "Abort all"
    b_restartAll = "Restart All"
    b_refresh = "Refresh"

    # Thread
    n_ControlerThread = "ControlerThread"
    nxt_1 = "Next execution of "
    nxt_2 = " will start in "
    nxt_3 = " seconds"
    thr_abort = "Thread is terminating: "
    txtRestoreState_1 = "Earlier Today Set to START at: "
    txtRestoreState_2 = "Earlier Today Set to END at: "
    txtRestoreState_3 = "Yesterday or Earlier Set to START at: "
    txtRestoreState_4 = "Yesterday or Earlier Set to END at: "
    txtSummerSeasonBegins = "Summer Season Begins with (month): "
    txtSummerSeasonEnds = "Summer Season Ends with (month): "
    bConsiderSeasonText = "Consider seasonal settings: "
    txt_ok_level = "Set sensor average threshold level: "
    nbr_of_samples_end = "Sensor data samples for END calculation: "
    nbr_of_samples_start = "Sensor data samples for START calculation: "
    weather_check = "Ended due to bad weather"
    light_check = "Ended due to low light condition"
    lost_sensor = "Sensor data to old..."

    class ControlerAction:
        name = "Start new or manage running controlers"
        description = (
            "Allows starting, stopping or resetting controlers, which " +
            "triggers a START and END event at a given date & time " +
            "also considering weather conditions and light sensor data"
        )
        controlerName = "Controler name: "
        eventNameStart = "START Event name: "
        eventNameEnd = "END event name: "
        labelStart = ' "%s"'
        daySTART = "Day START"
        txtSTART = "START"
        txtEND = "END"
        doLogLoopsText = "Print loop and debug info: "
        doLogText = "Log activities to file: "
        bDoSynchText = "Synchronization activated: "
        txtSynchInterval = "Synchronization interval (6-600 min): "
        bConsiderWeatherText = "Consider weather conditions: "
        bUseForManouverText = "Use for maneuvering: "
        txtSunRiseOffset = "Select the offset after sunrise: "
        txtSunSetOffset = "Select the offset before sunset: "

    class RFXtrx_SensorCapture:
        txt_name = "Give the sensor a name: "
        description = (
            "Allows capturing of sensor data from devices using a RFXtrx"
        )
        txt_task_killed = "Succesfully stopped scheduled task"
        txt_valuePos = "Select the payload position of the value: "
        txt_deviceId = "Enter the device ID of the sensor: "
        txtOffset = "Select the hysteresis between START and END commands: "
        txt_timeout_lost = (
            "Select or enter the number of seconds for sensor lost event: "
        )
        txt_signal_back = "Recovered contact with sensor"
        txt_taskObj = "Lost contact with sensor"
        txt_value_error = (
            "Something is wrong in your setting for the value position"
        )

    class SensorCapture:
        txt_name = "Give the sensor a name: "
        description = (
            "Allows capturing of sensor data from events"
        )
        txt_task_killed = "Succesfully stopped scheduled task"
        txt_idLabel = "Enter the key for the device ID: "
        txt_deviceId = "Enter the device ID of the sensor: "
        txt_valLabel = "Enter the key for the value: "
        txtOffset = "Select the hysteresis between START and END commands: "
        txtBaseLevel = "Select the base value the reading shall be added to: "
        txtMultiplier = "Select the multiplier for the read value: "
        txt_timeout_lost = (
            "Select or enter the number of seconds for sensor lost event: "
        )
        txt_signal_back = "Recovered contact with sensor"
        txt_taskObj = "Lost contact with sensor"


class ControlerThread(Thread):
    text = Text

    def __init__(
        self,
        dayTimeSettings,
        name,
        eventNameStart,
        eventNameEnd,
        doLogLoops,
        bDoSynch,
        iSynchInterval,
        summerSeasonBegins,
        summerSeasonEnds,
        bConsiderSeason,
        bConsiderWeather,
        bUseForManouver,
        iSunRiseOffset,
        iSunSetOffset,
        doLog,
        plugin
    ):
        Thread.__init__(self, name=self.text.n_ControlerThread)
        if not eventNameStart:
            eventNameStart = name
        if not eventNameEnd:
            eventNameEnd = name
        self.name = name
        self.dayTimeSettings = dayTimeSettings[:]
        self.eventNameStart = eventNameStart
        self.eventNameEnd = eventNameEnd
        self.finished = Event()
        self.abort = False
        self.doLogLoops = doLogLoops
        self.bDoSynch = bDoSynch
        self.iSynchInterval = iSynchInterval
        self.summerSeasonBegins = summerSeasonBegins
        self.summerSeasonEnds = summerSeasonEnds
        self.bConsiderSeason = bConsiderSeason
        self.bConsiderWeather = bConsiderWeather
        self.bUseForManouver = bUseForManouver
        self.iSunRiseOffset = iSunRiseOffset
        self.iSunSetOffset = iSunSetOffset
        self.bWeatherFlag = True
        self.CurrentState = 'Ended'
        self.blockCommands = False
        self.tBlock = None
        self.doLog = doLog
        self.plugin = plugin

    def run(self):
        try:
            dummy
        except NameError:
            dummy = 0
            init = 1
            iSynch = 1
            iWeatherCheck = 1
            prevDate = 0
            # Create a unique entry for the current state
            sName = 'my_' + str(self.name).replace(' ', '_')
            # print sName
            vars()[sName] = 'Ended'
            self.plugin.currentStates[sName] = eval(sName)
        random.jumpahead(213)
        self.lst_3 = []

        def CheckIfLog(lightOld, light, iSynch, label):
            if (
                light != lightOld
                or iSynch == 1
            ):
                LogToFile(label)

        def LogToFile(s):
            if self.doLog:
                timeStamp = str(
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                )
                logStr = timeStamp + "\t" + s + "<br\n>"
                fileHandle = None
                progData = eg.configDir + '\plugins\AwningManager'

                if (
                    not os.path.exists(progData)
                    and not os.path.isdir(progData)
                ):
                    os.makedirs(progData)

                fileHandle = open(
                    progData + '/' + 'AwningManager_' +
                    self.name + '.html', 'a'
                )
                fileHandle.write(logStr)
                fileHandle.close()

        def BlockCommands(nbr):
            self.blockCommands = True
            # print "Blocking commands"
            try:
                eg.scheduler.CancelTask(self.tBlock)
            except ValueError:
                pass
            self.tBlock = eg.scheduler.AddTask(
                nbr * 60.0,
                UnBlockCommands,
                ''
            )

        def UnBlockCommands(myArgument):
            self.blockCommands = False
            # print "Unblocking commands"

        def CalcNbrOfMinutes(s):
            iHour = int(s[0:2])
            iMin = int(s[2:4])
            iTotMin = iHour * 60 + iMin
            return (iTotMin)

        def CalcTime(iO):
            iHour = int(iO / 60)
            iMin = int(iO - iHour * 60)
            sh = str(iHour)
            if len(sh) < 2:
                sh = "0" + sh
            sm = str(iMin)
            if len(sm) < 2:
                sm = "0" + sm
            return (sh + sm)

        def CalcTrigTime():
            sunstate = ''
            c_time = '2500'
            try:
                sunstate = eg.plugins.Suntracker.GetTimeFor_SunSet_SunRise()

                sr = sunstate[0].split('|')[1]
                c_min = CalcNbrOfMinutes(sunstate[1]) + self.iSunRiseOffset
                c_time = CalcTime(c_min)

                c_min = CalcNbrOfMinutes(sunstate[1]) + self.iSunSetOffset
                if c_min >= 24 * 60:
                    c_min = 24 * 60 - 1
                c_time = CalcTime(c_min)
            except:
                pass
            return c_time

        def CalcTrigTime():
            sunstate = ''
            s_rise_time = '2500'
            s_set_time = '2500'
            try:
                sunstate = eg.plugins.Suntracker.GetTimeFor_SunSet_SunRise()
                sr = sunstate[0].split('|')[1]
                ss = sunstate[1].split('|')[1]

                c_min = CalcNbrOfMinutes(sr) + self.iSunRiseOffset
                s_rise_time = CalcTime(c_min)

                c_min = CalcNbrOfMinutes(ss) - self.iSunSetOffset
                if c_min >= 24 * 60:
                    c_min = 24 * 60 - 1
                s_set_time = CalcTime(c_min)
            except:
                pass
            return s_rise_time, s_set_time

        def GetBasicData(j, sName, CurrentState):
            # Calculate the trig times with the sunrise/sunset offsets
            s_rise_time, s_set_time = CalcTrigTime()
            c_month = time.localtime()[1]

            # Get current state
            CurrentState = self.plugin.currentStates[sName]

            # Event Trigger times
            sT = []
            eT = []
            for i in range(j - 3, j + 3):
                tt = self.dayTimeSettings[i]
                if tt == '----':
                    pass
                else:
                    if i % 2 == 0:  # START settings
                        sT.append(tt)
                    if i % 2 == 1:  # END settings
                        eT.append(tt)
            if len(sT) == 0:
                sT.append('0000')
            if len(eT) == 0:
                eT.append('2400')
            sT.sort()
            eT.sort()
            return s_rise_time, s_set_time, c_month, CurrentState, sT, eT

        def SendEventManouver(j):
            # Get/calculate basic data
            basicData = GetBasicData(j, sName, self.CurrentState)
            s_rise_time = basicData[0]
            s_set_time = basicData[1]
            c_month = basicData[2]
            self.CurrentState = basicData[3]
            sT = basicData[4]
            eT = basicData[5]

            # Event Trigger memory tag
            e_done = False

            # With normal time setting usage
            for i in range(j - 3, j + 3):
                if i % 2 == 0:  # Try START settings
                    if (
                        self.iSunRiseOffset == 0
                        and
                        self.CurrentState == 'Ended'
                        and
                        self.bWeatherFlag
                        and
                        self.plugin.ExtSensor_level
                        and
                        self.plugin.ExtSensor_state
                        and
                        c_month >= int(self.summerSeasonBegins)
                        and
                        c_month <= int(self.summerSeasonEnds)
                        and
                        trigTime >= self.dayTimeSettings[i]
                        and
                        trigTime < self.dayTimeSettings[i + 1]
                        # and
                        # not self.blockCommands
                    ):
                        eg.TriggerEvent(self.eventNameStart)
                        LogToFile(self.eventNameStart)
                        self.CurrentState = 'Started'
                        # BlockCommands(self.plugin.nbr_of_samples_end)

                if i % 2 == 1:  # Try END settings
                    if (
                        self.iSunSetOffset == 0
                        and
                        self.CurrentState == 'Started'
                        and
                        c_month >= int(self.summerSeasonBegins)
                        and
                        c_month <= int(self.summerSeasonEnds)
                        and
                        trigTime == self.dayTimeSettings[i]
                        # and
                        # not self.blockCommands
                    ):
                        eg.TriggerEvent(self.eventNameEnd)
                        LogToFile(self.eventNameEnd)
                        self.CurrentState = 'Ended'
                        # BlockCommands(self.plugin.nbr_of_samples_start)

            # With offset relative to sunrise/sunset usage
            if (
                self.iSunRiseOffset <> 0
                and
                self.CurrentState == 'Ended'
                and
                self.bWeatherFlag
                and
                self.plugin.ExtSensor_level
                and
                self.plugin.ExtSensor_state
                and
                c_month >= int(self.summerSeasonBegins)
                and
                c_month <= int(self.summerSeasonEnds)
                and
                trigTime >= s_rise_time
                and
                trigTime < '2400'
                and
                trigTime < eT[0]
                and
                not self.blockCommands
            ):
                eg.TriggerEvent(self.eventNameStart)
                LogToFile(self.eventNameStart)
                self.CurrentState = 'Started'
                BlockCommands(self.plugin.nbr_of_samples_end)

            if (
                self.iSunSetOffset <> 0
                and
                self.CurrentState == 'Started'
                and
                c_month >= int(self.summerSeasonBegins)
                and
                c_month <= int(self.summerSeasonEnds)
                and
                trigTime >= s_set_time
                and
                trigTime > sT[-1]
                and
                not self.blockCommands
            ):
                eg.TriggerEvent(self.eventNameEnd)
                LogToFile(self.eventNameEnd)
                self.CurrentState = 'Ended'
                BlockCommands(self.plugin.nbr_of_samples_start)

            # Restore device states at startup
            if init == 1:

                # With normal time setting usage
                for index, item in enumerate(self.lst_3):
                    if item != "----":
                        # print index, item, trigTime
                        if item <= trigTime:

                            if (
                                index % 2 == 1
                                and
                                self.iSunRiseOffset == 0
                                and
                                self.bWeatherFlag
                                and
                                c_month >= int(self.summerSeasonBegins)
                                and
                                c_month <= int(self.summerSeasonEnds)
                                and
                                not e_done
                            ):
                                LogToFile(self.eventNameStart)
                                print self.text.txtRestoreState_1, item
                                eg.TriggerEvent(self.eventNameStart)
                                self.CurrentState = 'Started'
                                e_done = True
                                break

                            if (
                                index % 2 == 0
                                and
                                self.iSunSetOffset == 0
                                and
                                c_month >= int(self.summerSeasonBegins)
                                and
                                c_month <= int(self.summerSeasonEnds)
                                and
                                not e_done
                            ):
                                LogToFile(self.eventNameEnd)
                                print self.text.txtRestoreState_2, item
                                eg.TriggerEvent(self.eventNameEnd)
                                self.CurrentState = 'Ended'
                                e_done = True
                                break

                # With offset relative to sunrise/sunset usage
                if (
                    self.iSunRiseOffset <> 0
                    and
                    self.bWeatherFlag
                    and
                    self.plugin.ExtSensor_level
                    and
                    self.plugin.ExtSensor_state
                    and
                    c_month >= int(self.summerSeasonBegins)
                    and
                    c_month <= int(self.summerSeasonEnds)
                    and
                    trigTime >= s_rise_time
                    and
                    trigTime < '2400'
                    and
                    trigTime < eT[0]
                    and
                    not e_done
                ):
                    LogToFile(self.eventNameStart)
                    print self.text.txtRestoreState_1, s_rise_time
                    eg.TriggerEvent(self.eventNameStart)
                    self.CurrentState = 'Started'
                    e_done = True

                if (
                    self.iSunSetOffset <> 0
                    and
                    c_month >= int(self.summerSeasonBegins)
                    and
                    c_month <= int(self.summerSeasonEnds)
                    and
                    trigTime >= s_set_time
                    and
                    trigTime > sT[-1]
                    and
                    not e_done
                ):
                    LogToFile(self.eventNameEnd)
                    print self.text.txtRestoreState_2, s_set_time
                    eg.TriggerEvent(self.eventNameEnd)
                    self.CurrentState = 'Ended'
                    e_done = True

            # Device states synch
            if (
                iSynch == self.iSynchInterval
                and
                c_month >= int(self.summerSeasonBegins)
                and
                c_month <= int(self.summerSeasonEnds)
            ):
                if self.CurrentState == 'Started':
                    eg.TriggerEvent(self.eventNameStart)
                if self.CurrentState == 'Ended':
                    eg.TriggerEvent(self.eventNameEnd)

            # Weather & light condition monitoring safety check
            if (
                self.CurrentState == 'Started'
                and
                not self.blockCommands
                and
                init == 0
            ):
                if (
                    not self.bWeatherFlag
                    or
                    not self.plugin.ExtSensor_state
                    or
                    not self.plugin.ExtSensor_level
                ):
                    log_info = ''
                    if not self.bWeatherFlag:
                        log_info = (
                            self.text.weather_check +
                            ' Weather condition: ' +
                            str(self.bWeatherFlag)
                        )
                        print log_info
                        LogToFile(log_info)
                    if not self.plugin.ExtSensor_state:
                        log_info = (
                            self.text.lost_sensor
                        )
                        print log_info
                        LogToFile(log_info)
                    if not self.plugin.ExtSensor_level:
                        log_info = (
                            self.text.light_check +
                            ' Light condition: ' +
                            str(self.plugin.ExtSensor_level)
                        )
                        print log_info
                        LogToFile(log_info)
                    eg.TriggerEvent(self.eventNameEnd)
                    self.CurrentState = 'Ended'
                    BlockCommands(self.plugin.nbr_of_samples_start)

            # Remember current state
            self.plugin.currentStates[sName] = self.CurrentState

        def SendEventControlWeather(j):
            # Get/calculate basic data
            basicData = GetBasicData(j, sName, self.CurrentState)
            s_rise_time = basicData[0]
            s_set_time = basicData[1]
            c_month = basicData[2]
            self.CurrentState = basicData[3]
            sT = basicData[4]
            eT = basicData[5]

            # Event Trigger memory tag
            e_done = False

            # With normal time setting usage
            for i in range(j - 3, j + 3):
                if i % 2 == 0:  # Try START settings
                    if (
                        trigTime == self.dayTimeSettings[i]
                        and
                        self.iSunRiseOffset == 0
                        and
                        self.CurrentState == 'Ended'
                        and
                        self.bWeatherFlag
                        and
                        c_month >= int(self.summerSeasonBegins)
                        and
                        c_month <= int(self.summerSeasonEnds)
                        and
                        not e_done
                    ):
                        eg.TriggerEvent(self.eventNameStart)
                        LogToFile(self.eventNameStart)
                        self.CurrentState = 'Started'
                        e_done = True

                if i % 2 == 1:  # Try END settings
                    if (
                        trigTime == self.dayTimeSettings[i]
                        and
                        self.iSunSetOffset == 0
                        and
                        self.CurrentState == 'Started'
                        and
                        c_month >= int(self.summerSeasonBegins)
                        and
                        c_month <= int(self.summerSeasonEnds)
                        and
                        not e_done
                    ):
                        eg.TriggerEvent(self.eventNameEnd)
                        LogToFile(self.eventNameEnd)
                        self.CurrentState = 'Ended'
                        e_done = True

            # With offset relative to sunrise/sunset usage
            if (
                self.iSunRiseOffset <> 0
                and
                self.CurrentState == 'Ended'
                and
                trigTime >= s_rise_time
                and
                trigTime < s_set_time
                and
                trigTime < eT[0]
                and
                self.bWeatherFlag
                and
                c_month >= int(self.summerSeasonBegins)
                and
                c_month <= int(self.summerSeasonEnds)
                and
                not e_done
            ):
                eg.TriggerEvent(self.eventNameStart)
                LogToFile(self.eventNameStart)
                self.CurrentState = 'Started'
                e_done = True

            if (
                self.iSunSetOffset <> 0
                and
                self.CurrentState == 'Started'
                and
                trigTime >= s_set_time
                and
                trigTime > sT[-1]
                and
                c_month >= int(self.summerSeasonBegins)
                and
                c_month <= int(self.summerSeasonEnds)
                and
                not e_done
            ):
                eg.TriggerEvent(self.eventNameEnd)
                LogToFile(self.eventNameEnd)
                self.CurrentState = 'Ended'
                e_done = True

            # Restore device states at startup
            if init == 1:

                # With normal time setting usage
                for index, item in enumerate(self.lst_3):
                    if item != "----":
                        # print index, item, trigTime
                        if item <= trigTime:
                            if (
                                index % 2 == 1
                                and
                                self.iSunRiseOffset == 0
                                and
                                self.bWeatherFlag
                                and
                                c_month >= int(self.summerSeasonBegins)
                                and
                                c_month <= int(self.summerSeasonEnds)
                                and
                                not e_done
                            ):
                                LogToFile(self.eventNameStart)
                                print self.text.txtRestoreState_1, item
                                eg.TriggerEvent(self.eventNameStart)
                                self.CurrentState = 'Started'
                                e_done = True
                                break

                            if (
                                index % 2 == 0
                                and
                                self.iSunSetOffset == 0
                                and
                                c_month >= int(self.summerSeasonBegins)
                                and
                                c_month <= int(self.summerSeasonEnds)
                                and
                                not e_done
                            ):
                                LogToFile(self.eventNameEnd)
                                print self.text.txtRestoreState_2, item
                                eg.TriggerEvent(self.eventNameEnd)
                                self.CurrentState = 'Ended'
                                e_done = True
                                break

                # With offset relative to sunrise/sunset usage
                if (
                    self.iSunRiseOffset <> 0
                    and
                    self.bWeatherFlag
                    and
                    trigTime >= s_rise_time
                    and
                    trigTime < s_set_time
                    and
                    trigTime < eT[0]
                    and
                    c_month >= int(self.summerSeasonBegins)
                    and
                    c_month <= int(self.summerSeasonEnds)
                    and
                    not e_done
                ):
                    LogToFile(self.eventNameStart)
                    print self.text.txtRestoreState_1, s_rise_time
                    eg.TriggerEvent(self.eventNameStart)
                    self.CurrentState = 'Started'
                    e_done = True

                if (
                    self.iSunSetOffset <> 0
                    and
                    trigTime >= s_set_time
                    and
                    trigTime > sT[-1]
                    and
                    c_month >= int(self.summerSeasonBegins)
                    and
                    c_month <= int(self.summerSeasonEnds)
                    and
                    not e_done
                ):
                    LogToFile(self.eventNameEnd)
                    print self.text.txtRestoreState_2, s_set_time
                    eg.TriggerEvent(self.eventNameEnd)
                    self.CurrentState = 'Ended'
                    e_done = True

            # Device states synch
            if (
                iSynch == self.iSynchInterval
                and
                c_month >= int(self.summerSeasonBegins)
                and
                c_month <= int(self.summerSeasonEnds)
            ):
                if self.CurrentState == 'Started':
                    eg.TriggerEvent(self.eventNameStart)
                if self.CurrentState == 'Ended':
                    eg.TriggerEvent(self.eventNameEnd)

            # Weather monitoring safety check
            if (
                iWeatherCheck == 10
                and
                self.CurrentState == 'Started'
                and
                init == 0
            ):
                if not self.bWeatherFlag:
                    eg.TriggerEvent(self.eventNameEnd)
                    self.CurrentState = 'Ended'
                    e_done = True

            # Remember current state
            self.plugin.currentStates[sName] = self.CurrentState

        def SendEventControl(j):
            # Get/calculate basic data
            basicData = GetBasicData(j, sName, self.CurrentState)
            s_rise_time = basicData[0]
            s_set_time = basicData[1]
            c_month = basicData[2]
            self.CurrentState = basicData[3]
            sT = basicData[4]
            eT = basicData[5]

            # Event Trigger memory tag
            e_done = False

            # With normal time setting usage
            for i in range(j - 3, j + 3):
                if i % 2 == 0:  # Try START settings
                    if (
                        trigTime == self.dayTimeSettings[i]
                        and
                        self.iSunRiseOffset == 0
                        and
                        self.CurrentState == 'Ended'
                        and
                        c_month >= int(self.summerSeasonBegins)
                        and
                        c_month <= int(self.summerSeasonEnds)
                        and
                        not e_done
                    ):
                        eg.TriggerEvent(self.eventNameStart)
                        LogToFile(self.eventNameStart)
                        self.CurrentState = 'Started'
                        e_done = True

                if i % 2 == 1:  # Try END settings
                    if (
                        trigTime == self.dayTimeSettings[i]
                        and
                        self.iSunSetOffset == 0
                        and
                        self.CurrentState == 'Started'
                        and
                        c_month >= int(self.summerSeasonBegins)
                        and
                        c_month <= int(self.summerSeasonEnds)
                        and
                        not e_done
                    ):
                        eg.TriggerEvent(self.eventNameEnd)
                        LogToFile(self.eventNameEnd)
                        self.CurrentState = 'Ended'
                        e_done = True

            # With offset relative to sunrise/sunset usage
            if (
                self.iSunRiseOffset <> 0
                and
                self.CurrentState == 'Ended'
                and
                trigTime >= s_rise_time
                and
                trigTime < s_set_time
                and
                trigTime < eT[0]
                and
                c_month >= int(self.summerSeasonBegins)
                and
                c_month <= int(self.summerSeasonEnds)
                and
                not e_done
            ):
                eg.TriggerEvent(self.eventNameStart)
                LogToFile(self.eventNameStart)
                self.CurrentState = 'Started'
                e_done = True

            if (
                self.iSunSetOffset <> 0
                and
                self.CurrentState == 'Started'
                and
                trigTime >= s_set_time
                and
                trigTime > sT[-1]
                and
                c_month >= int(self.summerSeasonBegins)
                and
                c_month <= int(self.summerSeasonEnds)
                and
                not e_done
            ):
                eg.TriggerEvent(self.eventNameEnd)
                LogToFile(self.eventNameEnd)
                self.CurrentState = 'Ended'
                e_done = True

            # Restore device states at startup
            if init == 1:

                # With normal time setting usage
                for index, item in enumerate(self.lst_3):
                    if item != "----":
                        # print index, item, trigTime
                        if item <= trigTime:
                            if (
                                index % 2 == 1
                                and
                                self.iSunRiseOffset == 0
                                and
                                c_month >= int(self.summerSeasonBegins)
                                and
                                c_month <= int(self.summerSeasonEnds)
                                and
                                not e_done
                            ):
                                LogToFile(self.eventNameStart)
                                print self.text.txtRestoreState_1, item
                                eg.TriggerEvent(self.eventNameStart)
                                self.CurrentState = 'Started'
                                e_done = True
                                break

                            if (
                                index % 2 == 0
                                and
                                self.iSunSetOffset == 0
                                and
                                c_month >= int(self.summerSeasonBegins)
                                and
                                c_month <= int(self.summerSeasonEnds)
                                and
                                not e_done
                            ):
                                LogToFile(self.eventNameEnd)
                                print self.text.txtRestoreState_2, item
                                eg.TriggerEvent(self.eventNameEnd)
                                self.CurrentState = 'Ended'
                                e_done = True
                                break

                # With offset relative to sunrise/sunset usage
                if (
                    self.iSunRiseOffset <> 0
                    and
                    trigTime >= s_rise_time
                    and
                    trigTime < s_set_time
                    and
                    trigTime < eT[0]
                    and
                    c_month >= int(self.summerSeasonBegins)
                    and
                    c_month <= int(self.summerSeasonEnds)
                    and
                    not e_done
                ):
                    LogToFile(self.eventNameStart)
                    print self.text.txtRestoreState_1, s_rise_time
                    eg.TriggerEvent(self.eventNameStart)
                    self.CurrentState = 'Started'
                    e_done = True

                if (
                    self.iSunSetOffset <> 0
                    and
                    trigTime >= s_set_time
                    and
                    trigTime > sT[-1]
                    and
                    c_month >= int(self.summerSeasonBegins)
                    and
                    c_month <= int(self.summerSeasonEnds)
                    and
                    not e_done
                ):
                    LogToFile(self.eventNameEnd)
                    print self.text.txtRestoreState_2, s_set_time
                    eg.TriggerEvent(self.eventNameEnd)
                    self.CurrentState = 'Ended'
                    e_done = True

            # Device states synch
            if (
                iSynch == self.iSynchInterval
                and
                c_month >= int(self.summerSeasonBegins)
                and
                c_month <= int(self.summerSeasonEnds)
            ):
                if self.CurrentState == 'Started':
                    eg.TriggerEvent(self.eventNameStart)
                if self.CurrentState == 'Ended':
                    eg.TriggerEvent(self.eventNameEnd)

            # Remember current state
            self.plugin.currentStates[sName] = self.CurrentState

        while (self.abort == False):
            if self.bDoSynch:
                if iSynch >= self.iSynchInterval:
                    iSynch = 1
                else:
                    iSynch += 1
            if iWeatherCheck >= 10:
                iWeatherCheck = 1
            else:
                iWeatherCheck += 1
            tr = random.random()
            remain = 61.0 - int(time.strftime("%S", time.localtime())) + tr
            #            remain = 10
            self.finished.wait(remain)
            if self.abort:
                break

            # Get the current date & time now, check if it has changed
            trigTime = str(time.strftime("%H%M", time.localtime()))
            currDate = str(time.strftime("%m/%d/%Y", time.localtime()))
            if currDate != prevDate:
                prevDate = 0

            if prevDate == 0:
                # Create daily data for device state synchronisation
                lst_1 = self.dayTimeSettings[0:3 * 6 + 3]
                lst_1.reverse()
                lst_2 = self.dayTimeSettings[3 * 6 + 3:]
                lst_2.reverse()
                self.lst_3 = lst_1 + lst_2
                # print "self.lst_3: ", self.lst_3

            # Update the weather flag
            if self.bConsiderWeather:
                self.bWeatherFlag = self.plugin.weatherRuleCondition

            # Start checking if sending of the actual event shall occure
            if self.bUseForManouver:
                SendEventManouver(3)

            if not self.bUseForManouver and self.bConsiderWeather:
                SendEventControlWeather(3)

            if not self.bUseForManouver and not self.bConsiderWeather:
                SendEventControl(3)

            self.finished.wait(0.1)

            if self.doLogLoops and init == 0:
                print(
                    self.text.nxt_1 +
                    self.name +
                    self.text.nxt_2 +
                    str(remain) +
                    self.text.nxt_3
                )

                average_end = 'In progress..'
                average_start = 'In progress..'

                if len(self.plugin.Ext_average_end) > 0:
                    average_end = (
                        float(sum(self.plugin.Ext_average_end)) /
                        len(self.plugin.Ext_average_end)
                    )

                    average_start = (
                        float(sum(self.plugin.Ext_average_start)) /
                        len(self.plugin.Ext_average_start)
                    )

                print(
                    "Weather:",
                    self.plugin.currCondition,
                    "Weather condition:",
                    self.bWeatherFlag,
                    "AwningManager state:",
                    self.CurrentState,
                    "ExtSensor_level:",
                    self.plugin.ExtSensor_level,
                    "ExtSensor_state:",
                    self.plugin.ExtSensor_state,
                    "BlockCommands:",
                    self.blockCommands,
                    "iSynch:",
                    iSynch
                )

                print(
                    "Average_start:",
                    average_start,
                    "Average_end:",
                    average_end
                )
            init = 0

    def AbortControler(self):
        self.abort = True
        print self.text.thr_abort, self.name
        self.finished.set()


class ABS_Controler(eg.PluginClass):
    text = Text

    def __init__(self):
        self.AddAction(ControlerAction)
        self.AddAction(RFXtrx_SensorCapture)
        self.AddAction(SensorCapture)
        self.AllcontrolerNames = []
        self.AlldayTimeSettings = []
        self.AlleventNameStart = []
        self.AlleventNameEnd = []
        self.AlldoLogLoops = []
        self.AllDoLog = []
        self.AllbDoSynch = []
        self.AlliSynchInterval = []
        self.AllbConsiderWeather = []
        self.AllbUseForManouver = []
        self.AlliSunRiseOffset = []
        self.AlliSunSetOffset = []
        self.lastControlerName = ""
        self.controlerThreads = {}
        self.currentStates = {}
        self.ExtSensor_state = True
        self.ExtSensor_level = False
        self.Ext_average_end = []
        self.Ext_average_start = []
        self.objectTasks = {}
        self.level_states = {}
        self.OkButtonClicked = False
        self.started = False
        self.prev_msg = ''

    def __start__(
        self,
        summerSeasonBegins,
        summerSeasonEnds,
        bConsiderSeason,
        ok_level,
        nbr_of_samples_end,
        nbr_of_samples_start
    ):
        print self.text.started
        self.summerSeasonBegins = summerSeasonBegins
        self.summerSeasonEnds = summerSeasonEnds
        self.bConsiderSeason = bConsiderSeason
        if self.bConsiderSeason:
            if self.summerSeasonBegins == '--':
                self.summerSeasonBegins = "01"
            if self.summerSeasonEnds == '--':
                self.summerSeasonBegins = "12"
        if not self.bConsiderSeason:
            self.summerSeasonBegins = "01"
            self.summerSeasonEnds = "12"
        self.ok_level = ok_level
        self.nbr_of_samples_end = nbr_of_samples_end
        self.nbr_of_samples_start = nbr_of_samples_start
        self.started = True
        self.weatherRuleCondition = False
        self.currCondition = "Unavailable"
        self.prevcurrCondition = "Undefined"
        self.ctrCondition = 0

        if self.OkButtonClicked:
            self.OkButtonClicked = False
            self.RestartAllControlers()
        progData = eg.configDir + '\plugins\AwningManager'
        if not os.path.exists(progData) and not os.path.isdir(progData):
            os.makedirs(progData)

        # Get the various possible weather conditions
        self.not_allowed = (
            weather_conditions_abs.weather_conditions_not_allowed()
        )
        self.allowed = weather_conditions_abs.weather_conditions_allowed()
        self.excpt = weather_conditions_abs.weather_conditions_except()

        # start the main thread
        self.mainThreadEvent = Event()
        mainThread = Thread(target=self.main, args=(self.mainThreadEvent,))
        mainThread.start()

    def __stop__(self):
        self.mainThreadEvent.set()
        self.AbortAllControlers()
        self.started = False

    def __close__(self):
        self.AbortAllControlers()
        self.started = False
        for task in self.objectTasks:
            try:
                eg.scheduler.CancelTask(self.objectTasks[task])
            except:
                pass

    def CalcWeatherCompensation(
        self,
        currCondition
    ):
        # Check weather and season condition
        weatherRuleCondition = False
        cFound = False
        currMonth = time.strftime("%m", time.localtime())

        if currCondition in self.not_allowed:
            weatherRuleCondition = False
            cFound = True

        if currCondition in self.allowed:
            weatherRuleCondition = True
            cFound = True

        if currCondition in self.excpt:
            weatherRuleCondition = False
            cFound = True

        if not cFound:
            eg.PrintError("Condition not defined in list: " + currCondition)
            weatherRuleCondition = False
            return weatherRuleCondition

        if self.bConsiderSeason:
            if (
                (
                    int(self.summerSeasonBegins) <
                    int(self.summerSeasonEnds)
                )
                and
                (
                    int(currMonth) < int(self.summerSeasonBegins)
                    or int(currMonth) > int(self.summerSeasonEnds)
                )
            ):
                weatherRuleCondition = False

            if (
                (
                    int(self.summerSeasonBegins) >
                    int(self.summerSeasonEnds)
                )
                and
                (
                    int(currMonth) < int(self.summerSeasonBegins)
                    and int(currMonth) > int(self.summerSeasonEnds)
                )
            ):
                weatherRuleCondition = False

        return weatherRuleCondition

    def main(self, mainThreadEvent):
        # print "mainthread started"
        while not mainThreadEvent.isSet():
            try:
                self.currCondition = (
                    eg.plugins.Suntracker.plugin.currCondition
                )
                self.weatherRuleCondition = (
                    self.CalcWeatherCompensation(self.currCondition)
                )
            except:
                eg.PrintError("Weather condition cannot be retrieved")
            remain = 60.0 - int(time.strftime("%S", time.localtime()))
            mainThreadEvent.wait(remain)
        # print "mainthread ended"

    # methods to Control controlers
    def StartControler(
        self,
        dayTimeSettings,
        controlerName,
        eventNameStart,
        eventNameEnd,
        doLogLoops,
        bDoSynch,
        iSynchInterval,
        summerSeasonBegins,
        summerSeasonEnds,
        bConsiderSeason,
        bConsiderWeather,
        bUseForManouver,
        iSunRiseOffset,
        iSunSetOffset,
        doLog
    ):
        if self.controlerThreads.has_key(controlerName):
            t = self.controlerThreads[controlerName]
            if t.isAlive():
                t.AbortControler()
            del self.controlerThreads[controlerName]
        t = ControlerThread(
            dayTimeSettings,
            controlerName,
            eventNameStart,
            eventNameEnd,
            doLogLoops,
            bDoSynch,
            iSynchInterval,
            summerSeasonBegins,
            summerSeasonEnds,
            bConsiderSeason,
            bConsiderWeather,
            bUseForManouver,
            iSunRiseOffset,
            iSunSetOffset,
            doLog,
            self
        )
        self.controlerThreads[controlerName] = t
        t.start()

    def AbortControler(self, controler):
        if self.controlerThreads.has_key(controler):
            t = self.controlerThreads[controler]
            t.AbortControler()
            del self.controlerThreads[controler]

    def AbortAllControlers(self):
        for i, item in enumerate(self.controlerThreads):
            t = self.controlerThreads[item]
            t.AbortControler()
            del t
        self.controlerThreads = {}

    def RestartAllControlers(self, startNewIfNotAlive=True):
        for i, item in enumerate(self.GetAllcontrolerNames()):
            if startNewIfNotAlive:
                self.StartControler(
                    self.GetAlldayTimeSettings()[i],
                    self.GetAllcontrolerNames()[i],
                    self.GetAlleventNameStart()[i],
                    self.GetAlleventNameEnd()[i],
                    self.GetAlldoLogLoops()[i],
                    self.GetAllbDoSynch()[i],
                    self.GetAlliSynchInterval()[i],
                    self.summerSeasonBegins,
                    self.summerSeasonEnds,
                    self.bConsiderSeason,
                    self.GetAllbConsiderWeather()[i],
                    self.GetAllbUseForManouver()[i],
                    self.GetAlliSunRiseOffset()[i],
                    self.GetAlliSunSetOffset()[i],
                    self.GetAllDoLog()[i]
                )

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        summerSeasonBegins="--",
        summerSeasonEnds="--",
        bConsiderSeason=True,
        ok_level=92.5,
        nbr_of_samples_end=63,
        nbr_of_samples_start=7,
        *args
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        panel.sizer.Add(
            wx.StaticText(panel, -1, self.text.listhl),
            flag=wx.ALIGN_CENTER_VERTICAL
        )

        mySizer = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)

        controlerListCtrl = wx.ListCtrl(
            panel,
            -1,
            style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL
        )

        for i, colLabel in enumerate(self.text.colLabels):
            controlerListCtrl.InsertColumn(i, colLabel)

        # setting col width to fit label
        controlerListCtrl.InsertItem(0, "Test Controler Name")
        controlerListCtrl.SetItem(0, 1, "Test Start EventName")
        controlerListCtrl.SetItem(0, 2, "Test End   EventName")

        size = 0
        for i in range(3):
            controlerListCtrl.SetColumnWidth(
                i,
                wx.LIST_AUTOSIZE_USEHEADER
            )  # wx.LIST_AUTOSIZE
            size += controlerListCtrl.GetColumnWidth(i)

        controlerListCtrl.SetMinSize((size, -1))
        mySizer.Add(controlerListCtrl, (0, 0), (1, 5), flag=wx.EXPAND)

        # buttons
        abortButton = wx.Button(panel, -1, self.text.b_abort)
        mySizer.Add(abortButton, (1, 0))

        abortAllButton = wx.Button(panel, -1, self.text.b_abortAll)
        mySizer.Add(abortAllButton, (1, 1), flag=wx.ALIGN_RIGHT)

        restartAllButton = wx.Button(panel, -1, self.text.b_restartAll)
        mySizer.Add(restartAllButton, (1, 2), flag=wx.ALIGN_RIGHT)

        refreshButton = wx.Button(panel, -1, self.text.b_refresh)
        mySizer.Add(refreshButton, (1, 4), flag=wx.ALIGN_RIGHT)

        summerBeginsCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '--',
            '01',
            '02',
            '03',
            '04',
            '05',
            '06',
            '07',
            '08',
            '09',
            '10',
            '11',
            '12'
        ]
        summerBeginsCtrl.AppendItems(items=list)
        if list.count(summerSeasonBegins) == 0:
            summerBeginsCtrl.Select(n=0)
        else:
            summerBeginsCtrl.SetSelection(int(list.index(summerSeasonBegins)))
        summerBeginsCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        sBtxt = wx.StaticText(panel, -1, self.text.txtSummerSeasonBegins)
        mySizer_2.Add(sBtxt, (1, 0))
        mySizer_2.Add(summerBeginsCtrl, (1, 1))

        summerEndsCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '--',
            '01',
            '02',
            '03',
            '04',
            '05',
            '06',
            '07',
            '08',
            '09',
            '10',
            '11',
            '12'
        ]
        summerEndsCtrl.AppendItems(items=list)
        if list.count(summerSeasonEnds) == 0:
            summerEndsCtrl.Select(n=0)
        else:
            summerEndsCtrl.SetSelection(int(list.index(summerSeasonEnds)))
        summerEndsCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        sEtxt = wx.StaticText(panel, -1, self.text.txtSummerSeasonEnds)
        mySizer_2.Add(sEtxt, (2, 0))
        mySizer_2.Add(summerEndsCtrl, (2, 1))

        bConsiderSeasonCtrl = wx.CheckBox(panel, -1, "")
        bConsiderSeasonCtrl.SetValue(bConsiderSeason)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.text.bConsiderSeasonText), (3, 0)
        )
        mySizer_2.Add(bConsiderSeasonCtrl, (3, 1))

        ok_levelCtrl = panel.SpinNumCtrl(
            ok_level,
            decimalChar='.',  # by default, use '.' for decimal point
            groupChar=',',  # by default, use ',' for grouping
            fractionWidth=1,
            integerWidth=4,
            min=0.0,
            max=100.0,
            increment=0.1
        )
        ok_levelCtrl.SetInitialSize((60, -1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_ok_level
            ),
            (5, 0)
        )
        mySizer_2.Add(ok_levelCtrl, (5, 1))

        nbr_of_samples_endCtrl = (
            panel.SpinIntCtrl(int(nbr_of_samples_end), 1, 99)
        )
        nbr_of_samples_endCtrl.SetInitialSize((50, -1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.text.nbr_of_samples_end),
            (6, 0)
        )
        mySizer_2.Add(nbr_of_samples_endCtrl, (6, 1))

        nbr_of_samples_startCtrl = (
            panel.SpinIntCtrl(int(nbr_of_samples_start), 1, 99)
        )
        nbr_of_samples_startCtrl.SetInitialSize((50, -1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.text.nbr_of_samples_start),
            (7, 0)
        )
        mySizer_2.Add(nbr_of_samples_startCtrl, (7, 1))

        font = panel.GetFont()
        p = font.GetPointSize()
        font.SetPointSize(9)
        # font.SetWeight(wx.BOLD)
        panel.SetFont(font)
        box = wx.StaticBox(panel, -1, self.text.pHeading)
        font.SetPointSize(p)
        font.SetWeight(wx.NORMAL)
        panel.SetFont(font)
        Sizer_2 = wx.StaticBoxSizer(box, wx.VERTICAL)
        Sizer_2.Add(mySizer_2)

        mySizer.AddGrowableRow(0)
        mySizer.AddGrowableCol(1)
        mySizer.AddGrowableCol(2)
        mySizer.AddGrowableCol(3)
        panel.sizer.Add(mySizer, 0, flag=wx.EXPAND)
        panel.sizer.Add(Sizer_2, 0, flag=wx.EXPAND)

        def PopulateList(event):
            controlerListCtrl.DeleteAllItems()
            row = 0
            for i, item in enumerate(self.controlerThreads):
                t = self.controlerThreads[item]
                if t.isAlive():
                    controlerListCtrl.InsertItem(row, t.name)
                    controlerListCtrl.SetItem(row,
                                                    1, t.eventNameStart)
                    controlerListCtrl.SetItem(row,
                                                    2, t.eventNameEnd)
                    row += 1
            ListSelection(wx.CommandEvent())

        def OnAbortButton(event):
            item = controlerListCtrl.GetFirstSelected()
            while item != -1:
                name = controlerListCtrl.GetItemText(item)
                self.AbortControler(name)
                item = controlerListCtrl.GetNextSelected(item)
            PopulateList(wx.CommandEvent())
            event.Skip()

        def OnAbortAllButton(event):
            self.AbortAllControlers()
            PopulateList(wx.CommandEvent())
            event.Skip()

        def OnRestartAllButton(event):
            self.RestartAllControlers()
            PopulateList(wx.CommandEvent())
            event.Skip()

        def ListSelection(event):
            flag = controlerListCtrl.GetFirstSelected() != -1
            abortButton.Enable(flag)
            event.Skip()

        def OnSize(event):
            controlerListCtrl.SetColumnWidth(
                6,
                wx.LIST_AUTOSIZE_USEHEADER
            )
            event.Skip()

        def OnApplyButton(event):
            event.Skip()
            self.RestartAllControlers()
            PopulateList(wx.CommandEvent())

        def OnOkButton(event):
            event.Skip()
            self.OkButtonClicked = True
            if not self.started:
                self.RestartAllControlers()
            PopulateList(wx.CommandEvent())

        PopulateList(wx.CommandEvent())

        abortButton.Bind(wx.EVT_BUTTON, OnAbortButton)
        abortAllButton.Bind(wx.EVT_BUTTON, OnAbortAllButton)
        restartAllButton.Bind(wx.EVT_BUTTON, OnRestartAllButton)
        refreshButton.Bind(wx.EVT_BUTTON, PopulateList)
        controlerListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelection)
        controlerListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelection)
        panel.Bind(wx.EVT_SIZE, OnSize)
        panel.dialog.buttonRow.applyButton.Bind(wx.EVT_BUTTON, OnApplyButton)
        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnOkButton)

        while panel.Affirmed():
            summerSeasonBegins = summerBeginsCtrl.GetStringSelection()
            summerSeasonEnds = summerEndsCtrl.GetStringSelection()
            bConsiderSeason = bConsiderSeasonCtrl.GetValue()
            ok_level = ok_levelCtrl.GetValue()
            nbr_of_samples_end = nbr_of_samples_endCtrl.GetValue()
            nbr_of_samples_start = nbr_of_samples_startCtrl.GetValue()

            panel.SetResult(
                summerSeasonBegins,
                summerSeasonEnds,
                bConsiderSeason,
                ok_level,
                nbr_of_samples_end,
                nbr_of_samples_start,
                *args
            )

    def GetAllcontrolerNames(self):
        return self.AllcontrolerNames

    def GetAlldayTimeSettings(self):
        return self.AlldayTimeSettings

    def GetAlleventNameStart(self):
        return self.AlleventNameStart

    def GetAlleventNameEnd(self):
        return self.AlleventNameEnd

    def GetAlldoLogLoops(self):
        return self.AlldoLogLoops

    def GetAllbDoSynch(self):
        return self.AllbDoSynch

    def GetAlliSynchInterval(self):
        return self.AlliSynchInterval

    def GetAllbConsiderWeather(self):
        return self.AllbConsiderWeather

    def GetAllbUseForManouver(self):
        return self.AllbUseForManouver

    def GetAlliSunRiseOffset(self):
        return self.AlliSunRiseOffset

    def GetAlliSunSetOffset(self):
        return self.AlliSunSetOffset

    def GetAllDoLog(self):
        return self.AllDoLog

    def AddControlerName(self, controlerName):
        if not controlerName in self.AllcontrolerNames:
            self.AllcontrolerNames.append(controlerName)
        return self.AllcontrolerNames.index(controlerName)

    def AddDayTimeSettings(self, dayTimeSettings, indx):
        try:
            del self.AlldayTimeSettings[indx]
        except IndexError:
            i = -1  # no match
        self.AlldayTimeSettings.insert(indx, dayTimeSettings)

    def AddeventNameStart(self, eventNameStart, indx):
        try:
            del self.AlleventNameStart[indx]
        except IndexError:
            i = -1  # no match
        self.AlleventNameStart.insert(indx, eventNameStart)

    def AddeventNameEnd(self, eventNameEnd, indx):
        try:
            del self.AlleventNameEnd[indx]
        except IndexError:
            i = -1  # no match
        self.AlleventNameEnd.insert(indx, eventNameEnd)

    def AddDoLogLoops(self, doLogLoops, indx):
        try:
            del self.AlldoLogLoops[indx]
        except IndexError:
            i = -1  # no match
        self.AlldoLogLoops.insert(indx, doLogLoops)

    def AddBdoSynch(self, bDoSynch, indx):
        try:
            del self.AllbDoSynch[indx]
        except IndexError:
            i = -1  # no match
        self.AllbDoSynch.insert(indx, bDoSynch)

    def AddIsynchInterval(self, iSynchInterval, indx):
        try:
            del self.AlliSynchInterval[indx]
        except IndexError:
            i = -1  # no match
        self.AlliSynchInterval.insert(indx, iSynchInterval)

    def AddBConsiderWeather(self, bConsiderWeather, indx):
        try:
            del self.AllbConsiderWeather[indx]
        except IndexError:
            i = -1  # no match
        self.AllbConsiderWeather.insert(indx, bConsiderWeather)

    def AddBUseForManouver(self, bUseForManouver, indx):
        try:
            del self.AllbUseForManouver[indx]
        except IndexError:
            i = -1  # no match
        self.AllbUseForManouver.insert(indx, bUseForManouver)

    def AddIsunRiseOffset(self, iSunRiseOffset, indx):
        try:
            del self.AlliSunRiseOffset[indx]
        except IndexError:
            i = -1  # no match
        self.AlliSunRiseOffset.insert(indx, iSunRiseOffset)

    def AddIsunSetOffset(self, iSunSetOffset, indx):
        try:
            del self.AlliSunSetOffset[indx]
        except IndexError:
            i = -1  # no match
        self.AlliSunSetOffset.insert(indx, iSunSetOffset)

    def AddDoLog(self, doLog, indx):
        try:
            del self.AllDoLog[indx]
        except IndexError:
            i = -1  # no match
        self.AllDoLog.insert(indx, doLog)


class ControlerAction(eg.ActionClass):

    def __call__(
        self,
        dayTimeSettings,
        controlerName,
        eventNameStart,
        eventNameEnd,
        aDaySTART_1,
        aDaySTART_2,
        aDaySTART_3,
        aDayEND_1,
        aDayEND_2,
        aDayEND_3,
        doLogLoops,
        bDoSynch,
        iSynchInterval,
        summerSeasonBegins,
        summerSeasonEnds,
        bConsiderSeason,
        bConsiderWeather,
        bUseForManouver,
        iSunRiseOffset,
        iSunSetOffset,
        doLog
    ):
        self.plugin.StartControler(
            dayTimeSettings,
            controlerName,
            eventNameStart,
            eventNameEnd,
            doLogLoops,
            bDoSynch,
            iSynchInterval,
            self.plugin.summerSeasonBegins,
            self.plugin.summerSeasonEnds,
            self.plugin.bConsiderSeason,
            bConsiderWeather,
            bUseForManouver,
            iSunRiseOffset,
            iSunSetOffset,
            doLog
        )

    def GetLabel(
        self,
        dayTimeSettings,
        controlerName,
        eventNameStart,
        eventNameEnd,
        aDaySTART_1,
        aDaySTART_2,
        aDaySTART_3,
        aDayEND_1,
        aDayEND_2,
        aDayEND_3,
        doLogLoops,
        bDoSynch,
        iSynchInterval,
        summerSeasonBegins,
        summerSeasonEnds,
        bConsiderSeason,
        bConsiderWeather,
        bUseForManouver,
        iSunRiseOffset,
        iSunSetOffset,
        doLog
    ):
        indx = self.plugin.AddControlerName(controlerName)
        self.plugin.AddDayTimeSettings(dayTimeSettings, indx)
        self.plugin.AddeventNameStart(eventNameStart, indx)
        self.plugin.AddeventNameEnd(eventNameEnd, indx)
        self.plugin.AddDoLogLoops(doLogLoops, indx)
        self.plugin.AddBdoSynch(bDoSynch, indx)
        self.plugin.AddIsynchInterval(iSynchInterval, indx)
        self.plugin.AddBConsiderWeather(bConsiderWeather, indx)
        self.plugin.AddBUseForManouver(bUseForManouver, indx)
        self.plugin.AddIsunRiseOffset(iSunRiseOffset, indx)
        self.plugin.AddIsunSetOffset(iSunSetOffset, indx)
        self.plugin.AddDoLog(doLog, indx)

        return self.text.labelStart % (controlerName)

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
        if int(dat1) > 23:
            dat1 = "23"
        if int(dat2) > 59:
            dat2 = "59"

        return (dat1 + dat2)

    def timeCheck(self, timeIntervals):
        t_list = [0] * 6

        for i in range(0, 3):
            theTime_1 = timeIntervals[i]
            theTime_2 = timeIntervals[i + 3]

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
                    tS = "000" + str(t_1)
                if tL == 2:
                    tS = "00" + str(t_1)
                if tL == 3:
                    tS = "0" + str(t_1)
                if tL == 4:
                    tS = str(t_1)
                t_list[i] = tS

            if t_2 <= t_1 and t_1 > 0 and t_2 != 0:
                t_2 = t_1 + 1
                if t_2 > 2359:
                    t_2 = 2359

            if t_2 == 0:
                t_list[i + 3] = ("----")
            else:
                tS = ""
                tL = len(str(t_2))
                if tL == 1:
                    tS = "000" + str(t_2)
                if tL == 2:
                    tS = "00" + str(t_2)
                if tL == 3:
                    tS = "0" + str(t_2)
                if tL == 4:
                    tS = str(t_2)
                t_list[i + 3] = tS
        return (t_list)

    def Configure(
        self,
        dayTimeSettings=[],
        controlerName="Give controler a name",
        eventNameStart="nn START",
        eventNameEnd="nn END",
        aDaySTART_1="----",
        aDaySTART_2="----",
        aDaySTART_3="----",
        aDayEND_1="----",
        aDayEND_2="----",
        aDayEND_3="----",
        doLogLoops=False,
        bDoSynch=False,
        iSynchInterval=30,
        summerSeasonBegins="",
        summerSeasonEnds="",
        bConsiderSeason=True,
        bConsiderWeather=True,
        bUseForManouver=True,
        iSunRiseOffset=0,
        iSunSetOffset=0,
        doLog=False
    ):
        plugin = self.plugin

        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(5, 5)
        mySizer_3 = wx.GridBagSizer(10, 10)

        # name
        controlerNameCtrl = wx.TextCtrl(panel, -1, controlerName)
        controlerNameCtrl.SetInitialSize((250, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.controlerName), (0, 0))
        mySizer_1.Add(controlerNameCtrl, (0, 1))

        # eventName START
        eventNameStartCtrl = wx.TextCtrl(panel, -1, eventNameStart)
        eventNameStartCtrl.SetInitialSize((150, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.eventNameStart), (1, 0))
        mySizer_1.Add(eventNameStartCtrl, (1, 1))

        # eventName END
        eventNameEndCtrl = wx.TextCtrl(panel, -1, eventNameEnd)
        eventNameEndCtrl.SetInitialSize((150, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.eventNameEnd), (2, 0))
        mySizer_1.Add(eventNameEndCtrl, (2, 1))

        aDaySTART_1Ctrl = wx.TextCtrl(panel, -1, aDaySTART_1)
        aDaySTART_1Ctrl.SetInitialSize((35, -1))
        aDayEND_1Ctrl = wx.TextCtrl(panel, -1, aDayEND_1)
        aDayEND_1Ctrl.SetInitialSize((35, -1))
        aDaySTART_2Ctrl = wx.TextCtrl(panel, -1, aDaySTART_2)
        aDaySTART_2Ctrl.SetInitialSize((35, -1))
        aDayEND_2Ctrl = wx.TextCtrl(panel, -1, aDayEND_2)
        aDayEND_2Ctrl.SetInitialSize((35, -1))
        aDaySTART_3Ctrl = wx.TextCtrl(panel, -1, aDaySTART_3)
        aDaySTART_3Ctrl.SetInitialSize((35, -1))
        aDayEND_3Ctrl = wx.TextCtrl(panel, -1, aDayEND_3)
        aDayEND_3Ctrl.SetInitialSize((35, -1))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.daySTART), (1, 0))
        mySizer_2.Add(aDaySTART_1Ctrl, (1, 1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtEND), (1, 2))
        mySizer_2.Add(aDayEND_1Ctrl, (1, 3))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtSTART), (1, 4))
        mySizer_2.Add(aDaySTART_2Ctrl, (1, 5))

        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtEND), (1, 6))
        mySizer_2.Add(aDayEND_2Ctrl, (1, 7))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtSTART), (1, 8))
        mySizer_2.Add(aDaySTART_3Ctrl, (1, 9))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.txtEND), (1, 10))
        mySizer_2.Add(aDayEND_3Ctrl, (1, 11))

        doLogLoopsCtrl = wx.CheckBox(panel, -1, "")
        doLogLoopsCtrl.SetValue(doLogLoops)

        mySizer_3.Add(
            wx.StaticText(panel, -1, self.text.doLogLoopsText), (1, 0)
        )
        mySizer_3.Add(doLogLoopsCtrl, (1, 1))

        doLogCtrl = wx.CheckBox(panel, -1, "")
        doLogCtrl.SetValue(doLog)

        mySizer_3.Add(
            wx.StaticText(panel, -1, self.text.doLogText), (2, 0)
        )
        mySizer_3.Add(doLogCtrl, (2, 1))

        bDoSynchCtrl = wx.CheckBox(panel, -1, "")
        bDoSynchCtrl.SetValue(bDoSynch)

        mySizer_3.Add(wx.StaticText(panel, -1, self.text.bDoSynchText), (3, 0))
        mySizer_3.Add(bDoSynchCtrl, (3, 1))

        iSynchIntervalCtrl = panel.SpinIntCtrl(iSynchInterval, 6, 600)
        iSynchIntervalCtrl.SetInitialSize((50, -1))

        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtSynchInterval
            ),
            (4, 0)
        )
        mySizer_3.Add(iSynchIntervalCtrl, (4, 1))

        bConsiderWeatherCtrl = wx.CheckBox(panel, -1, "")
        bConsiderWeatherCtrl.SetValue(bConsiderWeather)
        mySizer_3.Add(
            wx.StaticText(panel, -1, self.text.bConsiderWeatherText), (5, 0)
        )
        mySizer_3.Add(bConsiderWeatherCtrl, (5, 1))

        bUseForManouverCtrl = wx.CheckBox(panel, -1, "")
        bUseForManouverCtrl.SetValue(bUseForManouver)
        mySizer_3.Add(
            wx.StaticText(panel, -1, self.text.bUseForManouverText), (6, 0)
        )
        mySizer_3.Add(bUseForManouverCtrl, (6, 1))

        iSunRiseOffsetCtrl = panel.SpinIntCtrl(iSunRiseOffset, 0, 600)
        iSunRiseOffsetCtrl.SetInitialSize((50, -1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtSunRiseOffset
            ),
            (7, 0)
        )
        mySizer_3.Add(iSunRiseOffsetCtrl, (7, 1))

        iSunSetOffsetCtrl = panel.SpinIntCtrl(iSunSetOffset, 0, 600)
        iSunSetOffsetCtrl.SetInitialSize((50, -1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtSunSetOffset
            ),
            (8, 0)
        )
        mySizer_3.Add(iSunSetOffsetCtrl, (8, 1))

        panel.sizer.Add(mySizer_1, 0, flag=wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag=wx.EXPAND)
        panel.sizer.Add(mySizer_3, 0, flag=wx.EXPAND)

        def OnButton(event):
            # re-assign the OK button

            event.Skip()

            dayTimeSettings = []
            controlerName = controlerNameCtrl.GetValue()
            plugin.lastControlerName = controlerName
            indx = plugin.AddControlerName(controlerName)
            eventNameStart = eventNameStartCtrl.GetValue()
            plugin.AddeventNameStart(eventNameStart, indx)
            eventNameEnd = eventNameEndCtrl.GetValue()
            plugin.AddeventNameEnd(eventNameEnd, indx)
            doLogLoops = doLogLoopsCtrl.GetValue()
            plugin.AddDoLogLoops(doLogLoops, indx)
            doLog = doLogCtrl.GetValue()
            plugin.AddDoLog(doLog, indx)
            bDoSynch = bDoSynchCtrl.GetValue()
            plugin.AddBdoSynch(bDoSynch, indx)
            iSynchInterval = iSynchIntervalCtrl.GetValue()
            plugin.AddIsynchInterval(iSynchInterval, indx)
            bConsiderWeather = bConsiderWeatherCtrl.GetValue()
            plugin.AddBConsiderWeather(bConsiderWeather, indx)
            bUseForManouver = bUseForManouverCtrl.GetValue()
            plugin.AddBUseForManouver(bUseForManouver, indx)
            iSunRiseOffset = iSunRiseOffsetCtrl.GetValue()
            plugin.AddIsunRiseOffset(iSunRiseOffset, indx)
            iSunSetOffset = iSunSetOffsetCtrl.GetValue()
            plugin.AddIsunSetOffset(iSunSetOffset, indx)

            aDaySTART_1 = self.timeFormat(aDaySTART_1Ctrl.GetValue())
            aDayEND_1 = self.timeFormat(aDayEND_1Ctrl.GetValue())
            aDaySTART_2 = self.timeFormat(aDaySTART_2Ctrl.GetValue())
            aDayEND_2 = self.timeFormat(aDayEND_2Ctrl.GetValue())
            aDaySTART_3 = self.timeFormat(aDaySTART_3Ctrl.GetValue())
            aDayEND_3 = self.timeFormat(aDayEND_3Ctrl.GetValue())

            aDayList = []
            aDayList.append(aDaySTART_1)
            aDayList.append(aDayEND_1)
            aDayList.append(aDaySTART_2)
            aDayList.append(aDayEND_2)
            aDayList.append(aDaySTART_3)
            aDayList.append(aDayEND_3)
            aDayList = self.timeCheck(aDayList)
            aDaySTART_1 = aDayList[0]
            aDaySTART_2 = aDayList[2]
            aDaySTART_3 = aDayList[4]
            aDayEND_1 = aDayList[1]
            aDayEND_2 = aDayList[3]
            aDayEND_3 = aDayList[5]
            dayTimeSettings += aDayList

            plugin.AddDayTimeSettings(dayTimeSettings, indx)

            plugin.StartControler(
                dayTimeSettings,
                controlerName,
                eventNameStart,
                eventNameEnd,
                doLogLoops,
                bDoSynch,
                iSynchInterval,
                plugin.summerSeasonBegins,
                plugin.summerSeasonEnds,
                plugin.bConsiderSeason,
                bConsiderWeather,
                bUseForManouver,
                iSunRiseOffset,
                iSunSetOffset,
                doLog
            )

        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            dayTimeSettings = []
            controlerName = controlerNameCtrl.GetValue()
            plugin.lastControlerName = controlerName
            indx = plugin.AddControlerName(controlerName)
            eventNameStart = eventNameStartCtrl.GetValue()
            plugin.AddeventNameStart(eventNameStart, indx)
            eventNameEnd = eventNameEndCtrl.GetValue()
            plugin.AddeventNameEnd(eventNameEnd, indx)
            doLogLoops = doLogLoopsCtrl.GetValue()
            plugin.AddDoLogLoops(doLogLoops, indx)
            doLog = doLogCtrl.GetValue()
            plugin.AddDoLog(doLog, indx)
            bDoSynch = bDoSynchCtrl.GetValue()
            plugin.AddBdoSynch(bDoSynch, indx)
            iSynchInterval = iSynchIntervalCtrl.GetValue()
            plugin.AddIsynchInterval(iSynchInterval, indx)
            bConsiderWeather = bConsiderWeatherCtrl.GetValue()
            plugin.AddBConsiderWeather(bConsiderWeather, indx)
            bUseForManouver = bUseForManouverCtrl.GetValue()
            plugin.AddBUseForManouver(bUseForManouver, indx)
            iSunRiseOffset = iSunRiseOffsetCtrl.GetValue()
            plugin.AddIsunRiseOffset(iSunRiseOffset, indx)
            iSunSetOffset = iSunSetOffsetCtrl.GetValue()
            plugin.AddIsunSetOffset(iSunSetOffset, indx)

            aDaySTART_1 = self.timeFormat(aDaySTART_1Ctrl.GetValue())
            aDayEND_1 = self.timeFormat(aDayEND_1Ctrl.GetValue())
            aDaySTART_2 = self.timeFormat(aDaySTART_2Ctrl.GetValue())
            aDayEND_2 = self.timeFormat(aDayEND_2Ctrl.GetValue())
            aDaySTART_3 = self.timeFormat(aDaySTART_3Ctrl.GetValue())
            aDayEND_3 = self.timeFormat(aDayEND_3Ctrl.GetValue())

            aDayList = []
            aDayList.append(aDaySTART_1)
            aDayList.append(aDayEND_1)
            aDayList.append(aDaySTART_2)
            aDayList.append(aDayEND_2)
            aDayList.append(aDaySTART_3)
            aDayList.append(aDayEND_3)
            aDayList = self.timeCheck(aDayList)
            aDaySTART_1 = aDayList[0]
            aDaySTART_2 = aDayList[2]
            aDaySTART_3 = aDayList[4]
            aDayEND_1 = aDayList[1]
            aDayEND_2 = aDayList[3]
            aDayEND_3 = aDayList[5]
            dayTimeSettings += aDayList

            plugin.AddDayTimeSettings(dayTimeSettings, indx)

            panel.SetResult(
                dayTimeSettings,
                controlerName,
                eventNameStart,
                eventNameEnd,
                aDaySTART_1,
                aDaySTART_2,
                aDaySTART_3,
                aDayEND_1,
                aDayEND_2,
                aDayEND_3,
                doLogLoops,
                bDoSynch,
                iSynchInterval,
                plugin.summerSeasonBegins,
                plugin.summerSeasonEnds,
                plugin.bConsiderSeason,
                bConsiderWeather,
                bUseForManouver,
                iSunRiseOffset,
                iSunSetOffset,
                doLog
            )


class RFXtrx_SensorCapture(eg.ActionClass):

    def setExtSensors(self, myArgument):
        self.plugin.ExtSensor_state = False
        self.plugin.ExtSensor_level = False
        eg.TriggerEvent(repr(myArgument))

    def __call__(
        self,
        name,
        deviceId,
        valuePos,
        offset,
        timeout_lost
    ):
        average_end = 0.0
        average_start = 0.0

        if (
            eg.event.suffix.find("id:") != -1
            and
            eg.event.suffix.split('id: ')[1] == str(deviceId)
        ):
            try:
                value = float(eg.event.payload.split(' ')[valuePos])

                if (
                    len(self.plugin.Ext_average_end) <
                    self.plugin.nbr_of_samples_end
                ):
                    self.plugin.Ext_average_end.append(value)
                else:
                    self.plugin.Ext_average_end.insert(0, value)
                    del self.plugin.Ext_average_end[-1]

                average_end = (
                    float(sum(self.plugin.Ext_average_end)) /
                    len(self.plugin.Ext_average_end)
                )

                if (
                    len(self.plugin.Ext_average_start) <
                    self.plugin.nbr_of_samples_start
                ):
                    self.plugin.Ext_average_start.append(value)
                else:
                    self.plugin.Ext_average_start.insert(0, value)
                    del self.plugin.Ext_average_start[-1]

                average_start = (
                    float(sum(self.plugin.Ext_average_start)) /
                    len(self.plugin.Ext_average_start)
                )

                if not self.plugin.ExtSensor_level:
                    if average_start >= self.plugin.ok_level:
                        self.plugin.level_states[name] = True
                        self.plugin.ExtSensor_level = True

                elif self.plugin.ExtSensor_level:
                    if average_end < self.plugin.ok_level + offset:
                        self.plugin.level_states[name] = False
                        self.plugin.ExtSensor_level = False

                try:
                    eg.scheduler.CancelTask(self.plugin.objectTasks[name])
                except:
                    self.plugin.objectTasks[name] = None
                    print(
                        self.text.txt_signal_back + ': ' + name
                    )

                self.plugin.ExtSensor_state = True

                self.plugin.objectTasks[name] = eg.scheduler.AddTask(
                    float(timeout_lost),
                    self.setExtSensors,
                    self.text.txt_taskObj + ': ' + name
                )
            except:
                eg.PrintError(self.text.txt_value_error)
                pass

    def Configure(
        self,
        name='RFXtrx External Sensor',
        deviceId=58116,
        valuePos=6,
        offset=-1.5,
        timeout_lost=900
    ):
        try:
            eg.scheduler.CancelTask(self.plugin.objectTasks[name])
            print self.text.txt_task_killed
        except:
            pass
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_3 = wx.GridBagSizer(10, 10)

        nameCtrl = wx.TextCtrl(panel, -1, name)
        nameCtrl.SetInitialSize((250, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.txt_name), (0, 0))
        mySizer_1.Add(nameCtrl, (0, 1))

        deviceIdCtrl = panel.SpinIntCtrl(int(deviceId), 1, 99999)
        deviceIdCtrl.SetInitialSize((70, -1))
        mySizer_3.Add(
            wx.StaticText(panel, -1, self.text.txt_deviceId),
            (1, 0)
        )
        mySizer_3.Add(deviceIdCtrl, (1, 1))

        valuePosCtrl = panel.SpinIntCtrl(int(valuePos), 0, 9999)
        valuePosCtrl.SetInitialSize((50, -1))
        mySizer_3.Add(
            wx.StaticText(panel, -1, self.text.txt_valuePos),
            (2, 0)
        )
        mySizer_3.Add(valuePosCtrl, (2, 1))

        offsetCtrl = panel.SpinNumCtrl(
            offset,
            decimalChar='.',  # by default, use '.' for decimal point
            groupChar=',',  # by default, use ',' for grouping
            integerWidth=2,
            fractionWidth=1,
            allowNegative=True,
            min=-20.0,
            max=20.0,
            increment=0.1
        )
        offsetCtrl.SetInitialSize((60, -1))
        mySizer_3.Add(wx.StaticText(panel, -1, self.text.txtOffset), (3, 0))
        mySizer_3.Add(offsetCtrl, (3, 1))

        timeout_lostCtrl = panel.SpinIntCtrl(int(timeout_lost), 1, 9999)
        timeout_lostCtrl.SetInitialSize((50, -1))
        mySizer_3.Add(
            wx.StaticText(panel, -1, self.text.txt_timeout_lost),
            (4, 0)
        )
        mySizer_3.Add(timeout_lostCtrl, (4, 1))

        panel.sizer.Add(mySizer_1, 0, flag=wx.EXPAND)
        panel.sizer.Add(mySizer_3, 0, flag=wx.EXPAND)

        while panel.Affirmed():
            name = nameCtrl.GetValue()
            deviceId = deviceIdCtrl.GetValue()
            self.plugin.objectTasks[name] = None
            valuePos = valuePosCtrl.GetValue()
            offset = offsetCtrl.GetValue()
            timeout_lost = timeout_lostCtrl.GetValue()

            panel.SetResult(
                name,
                deviceId,
                valuePos,
                offset,
                timeout_lost
            )


class SensorCapture(eg.ActionClass):

    def setExtSensors(self, myArgument):
        self.plugin.ExtSensor_state = False
        self.plugin.ExtSensor_level = False
        eg.TriggerEvent(repr(myArgument))

    def __call__(
        self,
        name,
        idLabel,
        deviceId,
        valLabel,
        offset,
        base_level,
        multiplier,
        timeout_lost
    ):
        if eg.event.payload.find('undecoded') < 0:
            newEvent = eg.event.suffix
            average_end = 0.0
            average_start = 0.0
            sensorData = eval(eg.event.payload)

            if idLabel in sensorData:
                if sensorData[idLabel] == str(deviceId):
                    value = (
                        float(sensorData[valLabel]) * multiplier + base_level
                    )

                    if (
                        len(self.plugin.Ext_average_end) <
                        self.plugin.nbr_of_samples_end
                    ):
                        self.plugin.Ext_average_end.append(value)
                    else:
                        self.plugin.Ext_average_end.insert(0, value)
                        del self.plugin.Ext_average_end[-1]

                    average_end = (
                        float(sum(self.plugin.Ext_average_end)) /
                        len(self.plugin.Ext_average_end)
                    )

                    if (
                        len(self.plugin.Ext_average_start) <
                        self.plugin.nbr_of_samples_start
                    ):
                        self.plugin.Ext_average_start.append(value)
                    else:
                        self.plugin.Ext_average_start.insert(0, value)
                        del self.plugin.Ext_average_start[-1]

                    average_start = (
                        float(sum(self.plugin.Ext_average_start)) /
                        len(self.plugin.Ext_average_start)
                    )

                    if not self.plugin.ExtSensor_level:
                        if average_start >= self.plugin.ok_level:
                            self.plugin.level_states[name] = True
                            self.plugin.ExtSensor_level = True

                    elif self.plugin.ExtSensor_level:
                        if average_end < self.plugin.ok_level + offset:
                            self.plugin.level_states[name] = False
                            self.plugin.ExtSensor_level = False

                    try:
                        eg.scheduler.CancelTask(self.plugin.objectTasks[name])
                    except:
                        self.plugin.objectTasks[name] = None
                        print(
                            self.text.txt_signal_back + ': ' + name
                        )

                    self.plugin.ExtSensor_state = True

                    self.plugin.objectTasks[name] = eg.scheduler.AddTask(
                        float(timeout_lost),
                        self.setExtSensors,
                        self.text.txt_taskObj + ': ' + name
                    )

    def Configure(
        self,
        name='External Sensor name',
        idLabel='Oregon.Id',
        deviceId='62',
        valLabel='Oregon.Moisture',
        offset=-1.5,
        base_level=0.0,
        multiplier=1.0,
        timeout_lost=900
    ):
        try:
            eg.scheduler.CancelTask(self.plugin.objectTasks[name])
            print self.text.txt_task_killed

        except:
            pass
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)

        nameCtrl = wx.TextCtrl(panel, -1, name)
        nameCtrl.SetInitialSize((250, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.txt_name), (0, 0))
        mySizer_1.Add(nameCtrl, (0, 1))

        idLabelCtrl = wx.TextCtrl(panel, -1, idLabel)
        idLabelCtrl.SetInitialSize((150, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.txt_idLabel), (1, 0))
        mySizer_1.Add(idLabelCtrl, (1, 1))

        deviceIdCtrl = wx.TextCtrl(panel, -1, deviceId)
        deviceIdCtrl.SetInitialSize((150, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.txt_deviceId), (2, 0))
        mySizer_1.Add(deviceIdCtrl, (2, 1))

        valLabelCtrl = wx.TextCtrl(panel, -1, valLabel)
        valLabelCtrl.SetInitialSize((150, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.txt_valLabel), (3, 0))
        mySizer_1.Add(valLabelCtrl, (3, 1))

        base_levelCtrl = panel.SpinNumCtrl(
            base_level,
            decimalChar='.',  # by default, use '.' for decimal point
            groupChar=',',  # by default, use ',' for grouping
            integerWidth=3,
            fractionWidth=1,
            min=0.0,
            max=100.0,
            increment=0.1
        )
        base_levelCtrl.SetInitialSize((60, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.txtBaseLevel), (4, 0))
        mySizer_1.Add(base_levelCtrl, (4, 1))

        offsetCtrl = panel.SpinNumCtrl(
            offset,
            decimalChar='.',  # by default, use '.' for decimal point
            groupChar=',',  # by default, use ',' for grouping
            integerWidth=2,
            fractionWidth=1,
            allowNegative=True,
            min=-20.0,
            max=20.0,
            increment=0.1
        )
        offsetCtrl.SetInitialSize((60, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.txtOffset), (5, 0))
        mySizer_1.Add(offsetCtrl, (5, 1))

        multiplierCtrl = panel.SpinNumCtrl(
            multiplier,
            decimalChar='.',  # by default, use '.' for decimal point
            groupChar=',',  # by default, use ',' for grouping
            integerWidth=2,
            fractionWidth=1,
            min=1.0,
            max=10.0,
            increment=0.1
        )
        multiplierCtrl.SetInitialSize((60, -1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.txtMultiplier), (6, 0))
        mySizer_1.Add(multiplierCtrl, (6, 1))

        timeout_lostCtrl = panel.SpinIntCtrl(int(timeout_lost), 1, 9999)
        timeout_lostCtrl.SetInitialSize((60, -1))
        mySizer_1.Add(
            wx.StaticText(panel, -1, self.text.txt_timeout_lost),
            (7, 0)
        )
        mySizer_1.Add(timeout_lostCtrl, (7, 1))

        panel.sizer.Add(mySizer_1, 0, flag=wx.EXPAND)

        while panel.Affirmed():
            name = nameCtrl.GetValue()
            idLabel = idLabelCtrl.GetValue()
            deviceId = deviceIdCtrl.GetValue()
            self.plugin.objectTasks[name] = None
            valLabel = valLabelCtrl.GetValue()
            offset = offsetCtrl.GetValue()
            base_level = base_levelCtrl.GetValue()
            multiplier = multiplierCtrl.GetValue()
            timeout_lost = timeout_lostCtrl.GetValue()

            panel.SetResult(
                name,
                idLabel,
                deviceId,
                valLabel,
                offset,
                base_level,
                multiplier,
                timeout_lost
            )

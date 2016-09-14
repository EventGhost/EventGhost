# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# plugins/SunTracker/__init__.py
#
# Copyright (C) 2008
# Walter Kraembring
#
##############################################################################
# Revision history:
#
# 2014-08-11  Added event to allow controlling restart of threads when
#             changing 'empty house' and 'vacation' modes
# 2014-08-04  Added default params to ensure correct startup
#             Bugfix in MovingGhost feature: OFF is forced at sunrise if
#             a running ghost is still ON
# 2014-05-13  Added actions to set plugin configurations for
#             - your location specific data including latitude, longitude, time zone
#             and others
#             - vacation and empty house modes on/off
# 2014-05-07  Plugin termination problem improved/solved
# 2014-04-16  Added plugin setting for customizing the event prefix
#             Weather condition event now synchronized with the update rate
#             Added plugin setting to select if weather condition event will be
#             triggered on weather changes only
# 2014-02-24  Added new day type, 'empty house', and new empty house mode
# 2013-12-27  Fixed a bug in function for setting vacation mode. Vacation mode
#             set from external signal is now also saved persistent.
#             Synchronization is now deactived during vacation mode
# 2013-02-15  Added also a setting for fixed offset to getter action 'Check if
#             time now is inside calculated virtual range with  weather
#             compensated offset'
# 2013-01-10  Modified calculation rules of offsets for "InsideRange" actions
# 2013-01-06  Added a getter action 'Check if time now is inside calculated virtual
#             range with  weather compensated offset' to check dawn/dusk calculations
#             for various twilight options and +/- X minutes offset setting with
#             weather condition compensation.
#             Added a getter action 'GetTimeFor_SunSet_SunRise' to retrieve
#             current time stamps for todays Sunset and Sunrise".
#             Changed settings to allow 120 minutes instead of 60 for weather
#             compensation settings.
#             Bugfix in action 'GetSunStatusWeatherCompensated'
# 2012-10-20  Added actions to retrieve weather forecasts, wind and atmosphere
#             data
# 2012-09-10  Fixed a bug in main event creation for Sunrise/Sunset
# 2012-09-02  Commented out a number of print statements (info can be found
#             in the log files)
# 2012-08-30  Fixed a bug in CalcWeatherCompensation function
# 2012-08-29  Monitoring and reporting missing weather conditions.
#             Weather conditions defined in a separate file
# 2012-08-27  Google weather replaced by Yahoo! Weather
# 2012-08-16  Improved the handling for getting weather data from Google.
#             Also blocking getter actions during initialisation to improve
#             stability
# 2012-08-04  Re-worked the dawn/dusk calculation action with start and stop
#             times and some additional options. Renamed to "InsideRange"
# 2012-07-31  Added function to the dawn/dusk calcutations to stop or continue
#             the current macro execution depending on the condition
# 2012-07-30  Added a getter action to check dawn/dusk calculations for
#             various twilight options and +/- X minutes offset setting
# 2012-07-22  A controller action can now run as "Moving Ghost" exclusive
# 2012-07-21  Improved the functions for "Global Moving Ghost with external
#             triggering"
# 2012-07-17  Bug fixed in Moving Ghost functionality (it did create events
#             even if the sun was up)
# 2012-04-02  Added a getter action to get the sunstate with timestamp for last
#             sunrise and/or sunset
# 2011-12-09  Bugfix in timezone and current time calculation routine
# 2011-11-29  Timezone is now selectable to allow you to setup an environment
#             that is different from your (computers) actual location
# 2011-10-06  Added a (selectable) function that generates an event every
#             minute bringing information about the current weather condition
# 2011-10-01  Added a getter action to retrieve the weather condition
# 2011-09-18  New location for logfiles: eg.configDir/plugins/SunTracker
# 2011-09-15  Adjusted setting for longitude to allow max/min 180/-180
# 2011-07-31  Added a getter action to check if sun will be down within X
#             minutes considering weather compensation with Y minutes
# 2011-07-06  Reviewed the possible weather conditions retrieved from Google
# 2010-12-16  Fixed to work with -translate switch
# 2010-11-01  Fixed a bug in logging function daylight savings True/False
# 2010-08-30  Fixed a bug in the weather data compensation
# 2010-08-19  Added a getter action to retrieve the Sun status with weather
#             data compensation
#             Improved the code to avoid flickering lights ON/OFF
#             General cleanup of the code
# 2010-07-09  Created myself and fixed a bug in the weather data compensation
# 2010-07-04  General events for sunset/sunrise can now be triggered.
#             Added a MovingGhost variable and related actions that allows
#             you to set a global MovingGhost function ON/OFF.
#             As example you could have a key switch that turns the function
#             ON/OFF or any other input device generating ON/OFF events
# 2010-03-15  Improved control & handling of on/off commands
#             Improved handling of weather data to avoid on/off "flickering"
#             Added settings to improve light control in the blue hour
#             during the summer season
#             Cleaned up and re-organized the GUI
# 2010-02-09  Changed how to retrieve weather data from Google(city/country)
# 2009-12-31  Introduced getter action to retrieve sun status from scripts
#             Improved error handling when retrieving Weather Info from Google
# 2009-12-19  0.4.0 compatible GUID added
# 2009-12-02  Introducing light control compensation for weather conditions
#             All credits to Eugene Kaznacheev for providing the pywapi.py
# 2009-07-17  Using python calendar module to check the weekday
# 2009-05-22  Introduced eg.global variable to indicate if sun is up or down
# 2009-04-16  Fix for logging in Vista(/ProgramData/EventGhost/Log)
# 2009-03-19  Fix for SpinNumCtrl, many thanks to jinxdone
# 2009-02-22  Moving Ghost settings moved back to the action settings ;)
# 2009-01-26  Re-designed, moved some action variables to common plugin
#             variables with configuration settings in the plugin dialog
#             Changed the behaviour of buttons in action and plugin dialogs
# 2008-12-12  Bug fix for functions "EveningLightOFF" and "NightLightON" when
#             using negative offset settings
# 2008-09-24  Individual settings for bursts(ON/OFF) added
# 2008-09-17  Bugfix in string conversion
#             Bugfix in synchronization routine
# 2008-09-03  Added function for random control(Moving Ghost)
# 2008-05-13  Added individual log files for each thread
# 2008-04-28  Still stumbling, had to add better string control(StrCheck)
# 2008-04-25  A "little" Bug fix
# 2008-04-22  First version published
##############################################################################

eg.RegisterPlugin(
    name = "SunTracker",
    guid = '{6AE8C0C3-93B4-4446-BC77-FDFA2528E531}',
    author = "Walter Kraembring",
    version = "1.5.6",
    description =(
        'Triggers an event at sunset/sunrise and configurable dates & times'
        '<br\n><br\n>'
        '<center><img src="suntracker_plugin.png" /></center>'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=982",
)

import eg
import time
import datetime
import math
import string
import sys
import os
import random
import calendar
import Sun
import pywapi
import weather_conditions
from threading import Thread, Event



class Text:
    started = "Plugin started"
    closing = "Please wait, terminating threads..."
    pHeading = "Common Plug-In Settings"
    suntrackerFinished = "SunTracker finished"
    listhl = "Currently Active SunTrackers"
    colLabels =(
        "SunTracker Name",
        "Event Name ON",
        "Event Name OFF"
    )
    #Buttons
    b_abort = "Abort"
    b_abortAll = "Abort all"
    b_refresh = "Refresh"
    b_restartAll = "Restart All"

    #Thread
    n_SuntrackerThread = "SunTrackerThread"
    nd_mo = "Monday"
    nd_tu = "Tuesday"
    nd_we = "Wednesday"
    nd_th = "Thursday"
    nd_fr = "Friday"
    nd_sa = "Saturday"
    nd_su = "Sunday"
    nd_vc = "Vacation"
    nd_eh = "Empty house"
    nxt_1 = "Next execution of "
    nxt_2 = " will start in "
    nxt_3 = " seconds"
    txt_dls_true = "Daylight saving is TRUE"
    txt_dls_false = "Daylight saving is FALSE"
    txt_tz = " - Timezone"
    lg_today = "Today is "
    lg_sunrise_sunset_1 = ". Sunrise will be at "
    lg_sunrise_sunset_2 = " and Sunset at "
    lg_dayOfWeek = "Normal scheduling would have followed settings for "
    lg_holiday_1 = "Due to holidays, scheduling of "
    lg_holiday_2 = "will instead follow "
    lg_holiday_3 = "your settings for "
    lg_vacation_1 = "Due to vacation mode, scheduling of "
    lg_vacation_2 = "will instead follow "
    lg_vacation_3 = "your settings for "
    lg_emptyhouse_1 = "Due to empty house, scheduling of "
    lg_emptyhouse_2 = "will instead follow "
    lg_emptyhouse_3 = "your settings for "
    lg_movingG_1 = "Moving Ghost with random control is enabled for "
    lg_movingG_2 = "Global Moving Ghost status is: "
    lg_movingG_disabled = "Moving Ghost...disabled for "
    lg_movingG_enabled = "Moving Ghost...enabled for "
    thr_abort = "Thread is terminating: "
    txtFixedHolidays = "Fixed Public Holidays:"
    txtVariableHolidays = "Variable Public Holidays:"
    txtVacation_m = "Vacation mode"
    txtEmptyHouse_m = "Empty House mode"
    txtMyLongitude = "My Longitude"
    txtMyLatitude = "My Latitude"
    LocationLabel = "Location:"
    txtUnit = "Select your units:"
    weatherUpdateRate = "Update weather data every x minutes:"
    txtWeatherCondition = "Weather Condition: "
    txtNoCondition = "Yahoo!Weather condition not in list: "
    txtTimeCompensation = "Total time compensation(negative is ON earlier and OFF later): "
    txtSummerSeasonBegins = "Summer Season Begins with (month): "
    txtSummerSeasonEnds = "Summer Season Ends with (month): "
    sunStatus = "Create events at sunset and sunrise"
    sunIsUp = "Sunrise"
    sunIsDown = "Sunset"
    weatherStatus = "Create weather condition events"
    txtWeatherChange = "Create only on weather change"
    txtTimeZone = "Select or accept proposed timezone (UTC): "
    eventPrefix = "Event prefix (default is 'Main'):"

    class SuntrackerAction:
        general = "General Action Settings"
        daytime = "Day and Time Settings"
        eventrules = "Event Creation Rules and Settings"
        mghost = "Moving Ghost Settings"
        suntrackerName = "SunTracker name:"
        eventNameOn = "Event name ON:"
        eventNameOff = "Event name OFF:"
        labelStart = ' "%s"'
        txt_moNightOFF = "Monday Night OFF"
        txt_moMorningON = "Monday Morning ON"
        txt_moEveningOFF = "Monday Evening OFF"
        txt_tuNightOFF = "Tuesday Night OFF"
        txt_tuMorningON = "Tuesday Morning ON"
        txt_tuEveningOFF = "Tuesday Evening OFF"
        txt_weNightOFF = "Wednesday Night OFF"
        txt_weMorningON = "Wednesday Morning ON"
        txt_weEveningOFF = "Wednesday Evening OFF"
        txt_thNightOFF = "Thursday Night OFF"
        txt_thMorningON = "Thursday Morning ON"
        txt_thEveningOFF = "Thursday Evening OFF"
        txt_frNightOFF = "Friday Night OFF"
        txt_frMorningON = "Friday Morning ON"
        txt_frEveningOFF = "Friday Evening OFF"
        txt_saNightOFF = "Saturday Night OFF"
        txt_saMorningON = "Saturday Morning ON"
        txt_saEveningOFF = "Saturday Evening OFF"
        txt_suNightOFF = "Sunday Night OFF"
        txt_suMorningON = "Sunday Morning ON"
        txt_suEveningOFF = "Sunday Evening OFF"
        txt_vaNightOFF = "Vacation Night OFF"
        txt_vaMorningON = "Vacation Morning ON"
        txt_vaEveningOFF = "Vacation Evening OFF"
        txt_ehNightOFF = "Empty House Night OFF"
        txt_ehMorningON = "Empty House Morning ON"
        txt_ehEveningOFF = "Empty House Evening OFF"
        txtNbrBursts = "Number of events per control (1-10 bursts)"
        txtON = " ON"
        txtOFF = " OFF"
        txtCmdDelay = "Delay between the events (0.5-5.0 s)"
        doLogLoopsText = "Print normal loop info(Y/N)"
        txtMoving_Ghost = "Enable Local Moving Ghost"
        txtMoving_Ghost_G = "Enable Global Moving Ghost with external triggering"
        txtMoving_Ghost_excl = "Exclusive usage"
        txtMoving_Ghost_r_1 = "Moving Ghost: Random intervals BEFORE midnight"
        txtMoving_Ghost_r_2 = "Moving Ghost: Random intervals AFTER midnight"
        txtMoving_Ghost_ON_min = "ON min"
        txtMoving_Ghost_ON_max = "ON max"
        txtMoving_Ghost_OFF_min = "OFF min"
        txtMoving_Ghost_OFF_max = "OFF max"
        txtMinOnPeriod = "Minimum ON period required (0-60 min)"
        txtDoSynch = "Synchronization activated(Y/N)"
        txtSynchInterval = "Synch interval (6-600 min)"
        txtOffset = "Set offset for this control (-120...120 min)"
        txtWeather = "Weather compensation factor (0...120 min)"

    class SetMovingGhostON:
        txtMG_ON = "Moving Ghost function ON"
        txtInit = "Please wait, SunTracker is just initialising..."

    class SetMovingGhostOFF:
        txtMG_OFF = "Moving Ghost function OFF"
        txtInit = "Please wait, SunTracker is just initialising..."

    class SetVacationON:
        txtInit = "Please wait, SunTracker is just initialising..."

    class SetVacationOFF:
        txtInit = "Please wait, SunTracker is just initialising..."

    class SetEmptyHouseON:
        txtInit = "Please wait, SunTracker is just initialising..."

    class SetEmptyHouseOFF:
        txtInit = "Please wait, SunTracker is just initialising..."

    class SetLocation:
        txtInit = "Please wait, SunTracker is just initialising..."
        label = "Give the action a proper name"

    class GetSunStatusWeatherCompensated:
        txtWeather = "Weather compensation factor (1...120 min)"
        txtInit = "Please wait, SunTracker is just initialising..."

    class GetSunState:
        txtInit = "Please wait, SunTracker is just initialising..."

    class GetSunStateWithTimeStamp:
        txtInit = "Please wait, SunTracker is just initialising..."

    class GetWeatherCondition:
        txtInit = "Please wait, SunTracker is just initialising..."

    class IsSunDown:
        txtOffset = "Set offset for this control (-120...120 min)"
        txtWeather = "Weather compensation factor (0...120 min)"
        txtInit = "Please wait, SunTracker is just initialising..."

    class InsideRange:
        rangeName = "Name of the calculated virtual range"
        txtOffset = "Set offset for this control (-120...120 min)"
        tlStartType = "Select the twilight type for the start time calculation"
        tlEndType = "Select the twilight type for the end time calculation"
        stopMacroOnTrue = "Check to stop the running macro if condition is True"
        stopMacroOnFalse = "Check to stop the running macro if condition is False"
        txtInit = "Please wait, SunTracker is just initialising..."

    class InsideRangeWeatherCompensated:
        rangeName = "Name of the calculated virtual range"
        txtOffset = "Set offset for this control (-120...120 min)"
        txtWeather = "Weather compensation factor (0...120 min)"
        tlStartType = "Select the twilight type for the start time calculation"
        tlEndType = "Select the twilight type for the end time calculation"
        stopMacroOnTrue = "Check to stop the running macro if condition is True"
        stopMacroOnFalse = "Check to stop the running macro if condition is False"
        txtInit = "Please wait, SunTracker is just initialising..."


#All credits to Henrik Haerkoenen for Sun.py
class SunState(Sun.Sun):

    def getSunState(self, year, month, day, lon, lat):
        sunRise, sunSet = self.sunRiseSet(year, month, day, lon, lat)
        return sunRise, sunSet


    def getCivilTwilight(self, year, month, day, lon, lat):
        cDawn, cDusk = self.civilTwilight(year, month, day, lon, lat)
        return cDawn, cDusk


    def getNauticalTwilight(self, year, month, day, lon, lat):
        nDawn, nDusk = self.nauticalTwilight(year, month, day, lon, lat)
        return nDawn, nDusk


    def getAstronomicalTwilight(self, year, month, day, lon, lat):
        aDawn, aDusk = self.astronomicalTwilight(year, month, day, lon, lat)
        return aDawn, aDusk


    def getCivilDayTwilightLength(self, year, month, day, lon, lat):
        print self.dayCivilTwilightLength(year, month, day, lon, lat)


    def getNauticalDayTwilightLength(self, year, month, day, lon, lat):
        print self.dayNauticalTwilightLength(year, month, day, lon, lat)


    def getAstronomicalDayTwilightLength(self, year, month, day, lon, lat):
        print self.dayAstronomicalTwilightLength(year, month, day, lon, lat)



class ConfigData(eg.PersistentData):
    movingGhost = False



class SuntrackerThread(Thread):
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
        moving_Ghost,
        moving_Ghost_G,
        moving_Ghost_r1,
        moving_Ghost_r2,
        moving_Ghost_r3,
        moving_Ghost_r4,
        moving_Ghost_r5,
        moving_Ghost_r6,
        moving_Ghost_r7,
        moving_Ghost_r8,
        bDoSynch,
        iOffset,
        iWeather,
        iMinOnPeriod,
        myLongitude,
        myLatitude,
        location_id,
        iSynchInterval,
        summerSeasonBegins,
        summerSeasonEnds,
        moving_Ghost_excl,
        unit,
        weatherUpdateRate,
        emptyHouse_m,
        eventPrefix,
        weatherChange,
        plugin
    ):
        Thread.__init__(self, name=self.text.n_SuntrackerThread)
        if not eventNameOn:
            eventNameOn = name
        if not eventNameOff:
            eventNameOff = name
        self.name = name
        self.dayTimeSettings =  dayTimeSettings[:]
        self.eventNameOn = eventNameOn
        self.eventNameOff = eventNameOff
        self.eventPrefix = eventPrefix
        self.finished = Event()
        self.abort = False
        self.fixedHolidays = fixedHolidays
        self.variableHolidays = variableHolidays
        self.iNbrOfBurstsON = iNbrOfBurstsON
        self.iNbrOfBurstsOFF = iNbrOfBurstsOFF
        self.cmdDelay = cmdDelay
        self.doLogLoops = doLogLoops
        self.vacation_m = vacation_m
        self.emptyHouse_m = emptyHouse_m
        self.moving_Ghost = moving_Ghost
        self.moving_Ghost_G = moving_Ghost_G
        self.moving_Ghost_r1 = moving_Ghost_r1
        self.moving_Ghost_r2 = moving_Ghost_r2
        self.moving_Ghost_r3 = moving_Ghost_r3
        self.moving_Ghost_r4 = moving_Ghost_r4
        self.moving_Ghost_r5 = moving_Ghost_r5
        self.moving_Ghost_r6 = moving_Ghost_r6
        self.moving_Ghost_r7 = moving_Ghost_r7
        self.moving_Ghost_r8 = moving_Ghost_r8
        self.GMG_state = False
        self.bDoSynch = bDoSynch
        self.bDoSynchRestore = None
        self.iOffset = iOffset
        self.iWeather = iWeather
        self.weatherChange = weatherChange
        self.iMinOnPeriod = iMinOnPeriod
        self.myLongitude = myLongitude
        self.myLatitude = myLatitude
        self.location_id = location_id
        self.iSynchInterval = iSynchInterval
        self.currCondition = "Undefined"
        self.timeCompensation = 0
        self.plugin = plugin
        self.lastAction = ['', '']
        self.iGetWeather = 0
        self.summerSeasonBegins = summerSeasonBegins
        self.summerSeasonEnds = summerSeasonEnds
        self.moving_Ghost_excl = moving_Ghost_excl


    def run(self):
        try:
            dummy
        except NameError:
            dummy = 0
            prevDate = 0
            initsynch = 1
            iSynchLight = 1
            prevDate = 0
            lightON = False
            iRndm = 0
            bToggle = False
        random.jumpahead(137)


        def Check_for_holidays():
            currDate = time.strftime("%m/%d/%Y", time.localtime())
            date = time.strftime("%m%d", time.localtime())
            dateTmw = time.strftime(
                "%m%d",
                time.localtime(time.time() + (60 * 60 * 24))
            )
            dw = GetDayOfWeek(currDate)
            if dw < 6:
                dwt = dw + 1
            else:
                dwt = 0
            nDw = dw

            if(
                self.fixedHolidays.find(date) != -1
                or self.variableHolidays.find(date) != -1
            ):
                nDw = 5
                if dwt < 5:
                    nDw = 6
                if(
                    self.fixedHolidays.find(dateTmw) != -1
                    or self.variableHolidays.find(dateTmw) != -1
                ):
                    nDw = 5
            if(
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
            # day of week(monday = 0) of a given month/day/year
            ds = dateString.split('/')
            dayOfWeek = int(
                calendar.weekday(
                    int(ds[2]),
                    int(ds[0]),
                    int(ds[1])
                )
            )
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
            if(
                light != lightOld
                or iSynch == 1
            ):
                self.plugin.LogToFile(
                    label
                    + ", "
                    + self.text.txtWeatherCondition
                    + self.currCondition
                    + ", "
                    + self.text.txtTimeCompensation
                    + str(self.timeCompensation),
                    'Suntracker_'+self.name+'.html'
                )


        def CalcNbrOfMinutes(s):
            iHour = int(s[0:2])
            iMin = int(s[2:4])
            iTotMin = iHour*60 + iMin
            return(iTotMin)


        def StrCheck(s):
            if s == "----":
                s = "0000"
            return(s)


        def NightLightON(
            night_OFF,
            trigTimeSR,
            trigTime,
            csSR,
            light,
            lightON
        ):
            if(
                night_OFF != "----"
                and(
                    not lightON
                    or iSynchLight == self.iSynchInterval
                    or initsynch == 1
                )
            ):
                if(
                  (int(trigTime) < int(StrCheck(night_OFF))
                    and int(csSR) >= int(StrCheck(night_OFF))
                    and int(trigTime) < 0600
                    and(
                            int(trigTimeSR) < int(csSR)
                            or int(trigTime) < int(csSR)
                    )
                  )
                    or self.lastAction[1] == "ON"
                ):
                    light = 1;
                    if self.iMinOnPeriod > 0:
                        if(
                            CalcNbrOfMinutes(csSR) -
                            CalcNbrOfMinutes(trigTimeSR) < self.iMinOnPeriod
                        ):
                            light = 10;
                        if(
                            CalcNbrOfMinutes(StrCheck(night_OFF)) -
                            CalcNbrOfMinutes(trigTime) < self.iMinOnPeriod
                        ):
                            light = 10;
            return(light)


        def NightLightOFF(
            night_OFF,
            evening_OFF,
            morning_ON,
            trigTime,
            light,
            lightON
        ):
            if(
                night_OFF != "----"
                and(
                    lightON
                    or iSynchLight == self.iSynchInterval
                    or initsynch == 1
                )
            ):
                if(
                   (int(trigTime) >= int(StrCheck(night_OFF))
                    and int(StrCheck(night_OFF)) < 0600
                    and int(trigTime) < int(StrCheck(morning_ON)))
                    or self.lastAction[1] == "OFF"
                ):
                    light = 0
                if(
                    int(trigTime) >= int(StrCheck(night_OFF))
                    and int(StrCheck(night_OFF)) < 0600
                    and morning_ON == "----"
                    and int(trigTime) < 0600
                ):
                    light = 0
            if(
                night_OFF == "----"
                and evening_OFF != "----"
                and(
                    lightON
                    or iSynchLight == self.iSynchInterval
                    or initsynch == 1
                )
            ):
                if(
                   (int(trigTime) > 0000
                    and int(trigTime) < 0600
                    and(
                        int(trigTime) < int(StrCheck(morning_ON))
                        or morning_ON == "----"
                    )
                   )
                    or self.lastAction[1] == "OFF"
                ):
                    light = 0
            return(light)


        def MorningLightON(
            morning_ON,
            trigTimeSR,
            trigTime,
            csSR,
            light,
            lightON
        ):
            if(
                morning_ON != "----"
                and(
                    not lightON
                    or iSynchLight == self.iSynchInterval
                    or initsynch == 1
                )
            ):
                if(
                   (int(trigTime) >= int(StrCheck(morning_ON))
                    and int(csSR) >= int(StrCheck(morning_ON))
                    and int(trigTime) < 1200
                    and int(trigTimeSR) < int(csSR))
                    or self.lastAction[1] == "ON"
                ):
                    light = 1
                    if self.iMinOnPeriod > 0:
                        if(
                            CalcNbrOfMinutes(csSR) -
                            CalcNbrOfMinutes(trigTimeSR) < self.iMinOnPeriod
                        ):
                            light = 10
            return(light)


        def MorningLightOFF(
            morning_ON,
            trigTimeSR,
            trigTimeSS,
            trigTime,
            csSR,
            csSS,
            light,
            lightON
        ):
            if(
                morning_ON != "----"
                and(
                    lightON
                    or iSynchLight == self.iSynchInterval
                    or initsynch == 1
                )
            ):
                if(
                   (int(trigTimeSR) >= int(trigTime)
                    and int(trigTimeSR) >= int(csSR)
                    and int(trigTime) < 1800)
                    or self.lastAction[1] == "OFF"
                ):
                    if int(trigTimeSR) < int(csSS):
                        light = 0
                if(
                   (int(trigTimeSR) < int(trigTime)
                    and int(trigTimeSR) >= int(csSR)
                    and int(trigTime) < 1800)
                    or self.lastAction[1] == "OFF"
                ):
                    if int(trigTimeSS) < int(csSS):
                        light = 0

            if(
                morning_ON == "----"
                and(
                    lightON
                    or iSynchLight == self.iSynchInterval
                    or initsynch == 1
                )
            ):
                if(
                   (int(trigTimeSR) >= int(trigTime)
                    and int(trigTimeSR) >= int(csSR)
                    and int(trigTime) < 1800)
                    or self.lastAction[1] == "OFF"
                ):
                    if int(trigTimeSR) < int(csSS):
                        light = 0
                if(
                   (int(trigTimeSR) < int(trigTime)
                    and int(trigTimeSR) >= int(csSR)
                    and int(trigTime) < 1800)
                    or self.lastAction[1] == "OFF"
                ):
                    if int(trigTimeSS) < int(csSS):
                        light = 0
            return(light)


        def EveningLightON(
            morning_ON,
            evening_OFF,
            night_OFF,
            trigTimeSS,
            trigTime,
            csSS,
            light,
            lightON
        ):
            if(
                evening_OFF != "----"
                and(
                    not lightON
                    or iSynchLight == self.iSynchInterval
                    or initsynch == 1
                )
            ):
                if(
                    int(trigTimeSS) >= int(csSS)
                    and int(csSS) > 1200
                ):
                    if(
                       (int(csSS) <= int(StrCheck(evening_OFF))
                        and int(trigTimeSS) > 1200
                        and int(trigTime) > 1200
                        and int(trigTime) < int(StrCheck(evening_OFF)))
                        or self.lastAction[1] == "ON"
                    ):
                        light = 1
                        if self.iMinOnPeriod > 0:
                            if(
                                CalcNbrOfMinutes(StrCheck(evening_OFF)) -
                                CalcNbrOfMinutes(trigTimeSS) <
                                self.iMinOnPeriod
                            ):
                                light = 10
            if(
                evening_OFF == "----"
                and night_OFF != "----"
                and(
                    not lightON
                    or iSynchLight == self.iSynchInterval
                    or initsynch == 1
                )
            ):
                if(
                    int(trigTimeSS) >= int(csSS)
                    and int(csSS) > 1200
                ):
                    if(
                       (int(csSS) <= 2359
                        and int(trigTimeSS) > 1200
                        and int(trigTime) > 1200
                        and int(trigTime) <= 2359)
                        or self.lastAction[1] == "ON"
                    ):
                        light = 1
                        if self.iMinOnPeriod > 0:
                            # 23 hours 59 minutes == 1439 minutes
                            if(
                               (1439 - CalcNbrOfMinutes(trigTimeSS) +
                                CalcNbrOfMinutes(StrCheck(night_OFF))) <
                                self.iMinOnPeriod
                            ):
                                light = 10
            if(
                evening_OFF == "----"
                and night_OFF == "----"
                and morning_ON != "----"
                and(
                    not lightON
                    or iSynchLight == self.iSynchInterval
                    or initsynch == 1
                )
            ):
                if(
                    int(trigTimeSS) >= int(csSS)
                    and int(csSS) > 1200
                ):
                    if(
                       (int(csSS) <= 2359
                        and int(trigTimeSS) > 1200
                        and int(trigTime) > 1200
                        and int(trigTime) <= 2359)
                        or self.lastAction[1] == "ON"
                    ):
                        light = 1
                        if self.iMinOnPeriod > 0:
                            # 23 hours 59 minutes == 1439 minutes
                            if(
                               (1439 - CalcNbrOfMinutes(trigTimeSS) +
                                CalcNbrOfMinutes(StrCheck(night_OFF))) <
                                self.iMinOnPeriod
                            ):
                                light = 10
            return(light)


        def EveningLightOFF(
            morning_ON,
            evening_OFF,
            trigTimeSS,
            trigTime,
            csSS,
            light,
            lightON
        ):
            if(
                evening_OFF != "----"
                and(
                    lightON
                    or iSynchLight == self.iSynchInterval
                    or initsynch == 1
                )
            ):
                if(
                   (int(trigTime) > 1800
                    and int(StrCheck(evening_OFF)) > 1800
                    and int(trigTime) >= int(StrCheck(evening_OFF)))
                    or self.lastAction[1] == "OFF"
                ):
                    light = 0
            if(
                morning_ON != "----"
                and(
                    lightON
                    or iSynchLight == self.iSynchInterval
                    or initsynch == 1
                )
            ):
                if(
                   (int(trigTime) > 1800
                    and int(trigTimeSS) > 1800
                    and int(trigTimeSS) < int(csSS))
                    or self.lastAction[1] == "OFF"
                ):
                    light = 0
            return(light)


        def CheckNightLightOn(
            dayType,
            trigTimeSR,
            trigTime,
            csSR,
            light,
            lightON
        ):
            for i in range(0,9):
                if dayType == str(i):
                    light = NightLightON(
                        self.dayTimeSettings[i*3],
                        trigTimeSR,
                        trigTime,
                        csSR,
                        light,
                        lightON
                    )
            return(int(light))


        def CheckNightLightOff(
            dayType,
            trigTime,
            light,
            lightON
        ):
            for i in range(0,9):
                if dayType == str(i):
                    j = i * 3 - 1
                    if j == -1:
                        j = 20
                    elif j == 20:
                        j = 23
                    elif j == 23:
                        j = 26
                    light = NightLightOFF(
                        self.dayTimeSettings[i*3],
                        self.dayTimeSettings[j],
                        self.dayTimeSettings[i*3+1],
                        trigTime,
                        light,
                        lightON
                    )
            return(int(light))


        def CheckMorningLightOn(
            dayType,
            trigTimeSR,
            trigTime,
            csSR,
            light,
            lightON
        ):
            for i in range(0,9):
                if dayType == str(i):
                    light = MorningLightON(
                        self.dayTimeSettings[i*3+1],
                        trigTimeSR,
                        trigTime,
                        csSR,
                        light,
                        lightON
                    )
            return(int(light))


        def CheckMorningLightOff(
            dayType,
            trigTimeSR,
            trigTimeSS,
            trigTime,
            csSR,
            csSS,
            light,
            lightON
        ):
            for i in range(0,9):
                if dayType == str(i):
                    light = MorningLightOFF(
                        self.dayTimeSettings[i*3+1],
                        trigTimeSR,
                        trigTimeSS,
                        trigTime,
                        csSR,
                        csSS,
                        light,
                        lightON
                    )
            return(int(light))


        def CheckEveningLightOn(
            dayType,
            trigTimeSS,
            trigTime,
            csSS,
            light,
            lightON
        ):

            for i in range(0,9):
                if dayType == str(i):
                    j = i * 3 + 3
                    if j == 21:
                        j = 0
                    elif j == 24:
                        j = 21
                    elif j == 27:
                        j = 24
                    light = EveningLightON(
                        self.dayTimeSettings[i*3+1],
                        self.dayTimeSettings[i*3+2],
                        self.dayTimeSettings[j],
                        trigTimeSS,
                        trigTime,
                        csSS,
                        light,
                        lightON
                    )
            return(int(light))


        def CheckEveningLightOff(
            dayType,
            trigTimeSS,
            trigTime,
            csSS,
            light,
            lightON
        ):
            for i in range(0,9):
                if dayType == str(i):
                    light = EveningLightOFF(
                        self.dayTimeSettings[i*3+1],
                        self.dayTimeSettings[i*3+2],
                        trigTimeSS,
                        trigTime,
                        csSS,
                        light,
                        lightON
                    )
            return(int(light))


        def CreateEvent_ON(
            light,
            bDoSynch,
            lightON,
            iSynchLight
        ):
            cmdTime = str(time.strftime("%H%M", time.localtime()))
            if light == 1 and bDoSynch:
                lightOld = lightON
                lightON = True
                CheckIfLog(
                    lightOld,
                    lightON,
                    initsynch,
                    self.eventNameOn
                )
                self.lastAction = [cmdTime, "ON"]
                if iSynchLight != self.iSynchInterval:
                    self.plugin.iGetWeatherCntr = self.iWeather * 2
                for i in range(self.iNbrOfBurstsON):
                    eg.TriggerEvent(
                        self.eventNameOn,
                        None,
                        self.plugin.eventPrefix
                    )
                    self.finished.wait(self.cmdDelay)
            if light == 1 and not bDoSynch:
                if(
                    not lightON
                    or initsynch == 1
                ):
                    lightON = True
                    self.plugin.LogToFile(
                        self.eventNameOn
                        + ", "
                        + self.text.txtWeatherCondition
                        + self.currCondition
                        + ", "
                        + self.text.txtTimeCompensation
                        + str(self.timeCompensation),
                        'Suntracker_'+self.name+'.html'
                    )
                    self.lastAction = [cmdTime, "ON"]
                    if iSynchLight != self.iSynchInterval:
                        self.plugin.iGetWeatherCntr = self.iWeather * 2
                    for i in range(self.iNbrOfBurstsON):
                        eg.TriggerEvent(
                            self.eventNameOn,
                            None,
                            self.plugin.eventPrefix
                        )
                        self.finished.wait(self.cmdDelay)
            return(lightON)


        def CreateEvent_OFF(
            light,
            bDoSynch,
            lightON,
            iSynchLight
        ):
            cmdTime = str(time.strftime("%H%M", time.localtime()))
            if light == 0 and bDoSynch:
                lightOld = lightON
                lightON = False
                CheckIfLog(
                    lightOld,
                    lightON,
                    initsynch,
                    self.eventNameOff
                )
                self.lastAction = [cmdTime, "OFF"]
                if iSynchLight != self.iSynchInterval:
                    self.plugin.iGetWeatherCntr = self.iWeather * 2
                for i in range(self.iNbrOfBurstsOFF):
                    eg.TriggerEvent(
                        self.eventNameOff,
                        None,
                        self.plugin.eventPrefix
                    )
                    self.finished.wait(self.cmdDelay)
            if light == 0 and not bDoSynch:
                if(
                    lightON
                    or initsynch == 1
                ):
                    lightON = False
                    self.plugin.LogToFile(
                        self.eventNameOff
                        + ", "
                        + self.text.txtWeatherCondition
                        + self.currCondition
                        + ", "
                        + self.text.txtTimeCompensation
                        + str(self.timeCompensation),
                        'Suntracker_'+self.name+'.html'
                    )
                    self.lastAction = [cmdTime, "OFF"]
                    if iSynchLight != self.iSynchInterval:
                        self.plugin.iGetWeatherCntr = self.iWeather * 2
                    for i in range(self.iNbrOfBurstsOFF):
                        eg.TriggerEvent(
                            self.eventNameOff,
                            None,
                            self.plugin.eventPrefix
                        )
                        self.finished.wait(self.cmdDelay)
            return(lightON)


        while(not self.abort):
            if self.plugin.iGetWeather <  self.iWeather * 2:
                self.plugin.iGetWeather =  self.iWeather * 2
            tr = random.random()
            remain = 61.0 - int(time.strftime("%S", time.localtime())) + tr
            self.finished.wait(remain)
            self.finished.clear()
            if self.abort:
                break

            # Check if vacation is enabled and if so, disable synchronizing
            self.vacation_m = self.plugin.vacation_m
            if self.vacation_m:
                self.bDoSynch = False

            # Check if empty house is enabled
            self.emptyHouse_m = self.plugin.emptyHouse_m

            # Count the number of runs to activate synchronization
            if self.bDoSynch:
                if iSynchLight >= int(self.iSynchInterval):
                    iSynchLight = 1
                else:
                    iSynchLight += 1

            # Get the current date & time now, check if it has changed
            trigTime = str(time.strftime("%H%M", time.localtime()))
            currDate = str(time.strftime("%m/%d/%Y", time.localtime()))
            if currDate != prevDate:
                prevDate = 0

            # Adjust the sunrise/sunset trig times with defined offset
            trigTimeSR = self.plugin.GetOffsetTimeSR(self.iOffset)
            trigTimeSS = self.plugin.GetOffsetTimeSS(self.iOffset)

            # Get day of week and check for holidays
            odayType = str(GetDayOfWeek(currDate))
            dayType = str(Check_for_holidays())

            # Check status of Moving Ghost function
            bMghost = False
            if self.moving_Ghost:
                bMghost = True
            elif self.moving_Ghost_G and ConfigData.movingGhost:
                bMghost = True

            # Set the conditions depending on the weather
            if self.iWeather <> 0:
                self.currCondition = self.plugin.currCondition

                # Adjust the sunrise/sunset trig times to weather condition
                self.timeCompensation = 0

                self.currCondition, self.timeCompensation, trigTimeSS, trigTimeSR = (
                        self.plugin.CalcWeatherCompensation(
                                self.currCondition,
                                self.timeCompensation,
                                self.iWeather,
                                self.iOffset
                        )
                )

            # Fetch the times for sunrise/sunset
            csSR = self.plugin.csSR
            csSS = self.plugin.csSS

            # Initial logging when a new day begins
            if prevDate == 0:
                prevDate = currDate
                od = GetNameOfDay(odayType)
                nd = GetNameOfDay(dayType)
                lg =(self.text.lg_today
                    + od
                    + self.text.lg_sunrise_sunset_1
                    + csSR
                    + self.text.lg_sunrise_sunset_2
                    + csSS
                )
                self.plugin.LogToFile(
                            lg,
                            'Suntracker_'+self.name+'.html'
                )
                if nd != od and not bMghost:
                    lg = self.text.lg_dayOfWeek+od
                    self.plugin.LogToFile(
                                lg,
                                'Suntracker_'+self.name+'.html'
                    )
                    if dayType == "8":
                        lg =(
                            self.text.lg_emptyhouse_1
                            + self.name
                            + " "
                            + self.text.lg_emptyhouse_2
                            + self.text.lg_emptyhouse_3
                            + nd
                        )
                        self.plugin.LogToFile(
                                    lg,
                                    'Suntracker_'+self.name+'.html'
                        )
                    if dayType == "7":
                        lg =(
                            self.text.lg_vacation_1
                            + self.name
                            + " "
                            + self.text.lg_vacation_2
                            + self.text.lg_vacation_3
                            + nd
                        )
                        self.plugin.LogToFile(
                                    lg,
                                    'Suntracker_'+self.name+'.html'
                        )
                    else:
                        lg =(
                            self.text.lg_holiday_1
                            + self.name
                            + " "
                            + self.text.lg_holiday_2
                            + self.text.lg_holiday_3
                            + nd
                        )
                        self.plugin.LogToFile(
                                    lg,
                                    'Suntracker_'+self.name+'.html'
                        )

            # Initial logging when Moving Ghost is activated
            if bMghost and initsynch == 1:
                self.plugin.LogToFile(
                            self.text.lg_movingG_1 + self.name,
                            'Suntracker_'+self.name+'.html'
                )

            # Restoring to initial value
            light = 10

            if not self.moving_Ghost_excl:
                # Night Light On
                light = CheckNightLightOn(
                    dayType,
                    trigTimeSR,
                    trigTime,
                    csSR,
                    light,
                    lightON
                )

                # Night Light Off
                light = CheckNightLightOff(
                    dayType,
                    trigTime,
                    light,
                    lightON
                )

                # Morning Light On
                light = CheckMorningLightOn(
                    dayType,
                    trigTimeSR,
                    trigTime,
                    csSR,
                    light,
                    lightON
                )

                # Morning Light Off
                light = CheckMorningLightOff(
                    dayType,
                    trigTimeSR,
                    trigTimeSS,
                    trigTime,
                    csSR,
                    csSS,
                    light,
                    lightON
                )

                # Evening Light On
                light = CheckEveningLightOn(
                    dayType,
                    trigTimeSS,
                    trigTime,
                    csSS,
                    light,
                    lightON
                )

                # Evening Light Off
                light = CheckEveningLightOff(
                    dayType,
                    trigTimeSS,
                    trigTime,
                    csSS,
                    light,
                    lightON
                )

            # Moving Ghost...
            if initsynch == 1:
                initsynch = 0
                random.seed(self.name)
                random.jumpahead(int(len(self.name)))
                if(
                    self.moving_Ghost
                    or(
                        self.moving_Ghost_G
                        and ConfigData.movingGhost
                    )
                ):
                    self.bDoSynchRestore = self.bDoSynch
                    self.GMG_state = ConfigData.movingGhost
                    self.bDoSynch = False
                    if(trigTime > csSS or trigTime < csSR):
                        light = 1
            else:
                if(
                    self.moving_Ghost
                    or(
                        self.moving_Ghost_G
                        and ConfigData.movingGhost
                    )
                ):
                    self.GMG_state = ConfigData.movingGhost
                    if(trigTime > csSS or trigTime < csSR):
                        light = 10
                        if iRndm == 0:
                            # Get random number
                            if not lightON:
                                if trigTime > csSS:
                                    iRndm = random.randint(
                                        self.moving_Ghost_r3,
                                        self.moving_Ghost_r4
                                    )
                                else:
                                    iRndm = random.randint(
                                        self.moving_Ghost_r6,
                                        self.moving_Ghost_r8
                                    )

                            if lightON:
                                if trigTime > csSS:
                                    iRndm = random.randint(
                                        self.moving_Ghost_r1,
                                        self.moving_Ghost_r2
                                    )
                                else:
                                    iRndm = random.randint(
                                        self.moving_Ghost_r5,
                                        self.moving_Ghost_r6
                                    )

                        if iRndm == 1:
                            iRndm -= 1
                            if not lightON:
                                light = 1
                            if lightON:
                                light = 0

                        if iRndm > 1:
                            iRndm -= 1

                    if(trigTime <= csSS and trigTime >= csSR):
                        if lightON:
                            light = 0

            if(
                self.moving_Ghost_G
                and not ConfigData.movingGhost
                and self.GMG_state
            ):
                if initsynch != 1:
                    initsynch = 1
                    if not self.moving_Ghost_excl:
                        self.bDoSynch = self.bDoSynchRestore
                    self.GMG_state = ConfigData.movingGhost

            #Print basic loop info
            if self.doLogLoops and initsynch == 0:
                print(
                    self.text.nxt_1
                    + self.name
                    + self.text.nxt_2
                    + str(remain)
                    + self.text.nxt_3
                    + ' '
                    + str(iRndm)
                )

            lightON = CreateEvent_ON(
                    light,
                    self.bDoSynch,
                    lightON,
                    iSynchLight
                )

            lightON = CreateEvent_OFF(
                    light,
                    self.bDoSynch,
                    lightON,
                    iSynchLight
                )


    def AbortSuntracker(self):
        self.abort = True
        #print self.text.thr_abort, self.name
        self.finished.set()



class Suntracker(eg.PluginClass):
    iconFile = "suntracker_plugin"
    text = Text

    def __init__(self):
        self.AddAction(SuntrackerAction)
        self.AddAction(SetLocation)
        self.AddAction(SetVacationON)
        self.AddAction(SetVacationOFF)
        self.AddAction(SetEmptyHouseON)
        self.AddAction(SetEmptyHouseOFF)
        self.AddAction(IsSunDown)
        self.AddAction(InsideRange)
        self.AddAction(InsideRangeWeatherCompensated)
        self.AddAction(GetWeatherCondition)
        self.AddAction(GetSunStatusWeatherCompensated)
        self.AddAction(GetTimeFor_SunSet_SunRise)
        self.AddAction(GetSunState)
        self.AddAction(GetSunStateWithTimeStamp)
        self.AddAction(SetMovingGhostON)
        self.AddAction(SetMovingGhostOFF)
        self.AddAction(GetCurrentCondition)
        self.AddAction(GetWindData)
        self.AddAction(GetForecasts)
        self.AddAction(GetAtmosphereData)
        self.AllsuntrackerNames = []
        self.AlldayTimeSettings = []
        self.AlleventNameOn = []
        self.AlleventNameOff = []
        self.AlliNbrOfBurstsON = []
        self.AlliNbrOfBurstsOFF = []
        self.AllcmdDelay = []
        self.AlldoLogLoops = []
        self.AllbDoSynch = []
        self.AlliSynchInterval = []
        self.AlliOffset = []
        self.AlliWeather = []
        self.AlliMinOnPeriod = []
        self.Allmoving_Ghost = []
        self.Allmoving_Ghost_G = []
        self.Allmoving_Ghost_excl = []
        self.AllMoving_Ghost_r1 = []
        self.AllMoving_Ghost_r2 = []
        self.AllMoving_Ghost_r3 = []
        self.AllMoving_Ghost_r4 = []
        self.AllMoving_Ghost_r5 = []
        self.AllMoving_Ghost_r6 = []
        self.AllMoving_Ghost_r7 = []
        self.AllMoving_Ghost_r8 = []
        self.lastSuntrackerName = ""
        self.suntrackerThreads = {}
        self.k = SunState()
        self.OkButtonClicked = False
        self.started = False
        self.restarted = False


    def __start__(
        self,
        myLongitude = "18.0000",
        myLatitude = "59.2500",
        location_id = "905335",
        fixedHolidays = "0101,0501,0606,1224,1225,1226",
        variableHolidays = "0106,0402,0405,0512,0522,0523,0625",
        summerSeasonBegins = "--",
        summerSeasonEnds = "--",
        vacation_m = False,
        sunStatus = True,
        weatherStatus = True,
        iTimeZone = '+01.00',
        unit = "metric",
        weatherUpdateRate = 5,
        emptyHouse_m = False,
        eventPrefix = "Main",
        weatherChange = False
    ):
        print self.text.started
        self.myLongitude = myLongitude
        self.myLatitude = myLatitude
        self.location_id = location_id
        self.fixedHolidays = fixedHolidays
        self.variableHolidays = variableHolidays
        self.summerSeasonBegins = summerSeasonBegins
        self.summerSeasonEnds = summerSeasonEnds
        self.vacation_m = vacation_m
        self.emptyHouse_m = emptyHouse_m
        self.sunStatus = sunStatus
        self.iTimeZone = iTimeZone
        self.unit = unit
        self.weatherUpdateRate = weatherUpdateRate
        self.weatherStatus = weatherStatus
        self.weather_data = None
        self.sunIsUp = True
        self.initsynch = True
        self.csSR = ''
        self.csSS = ''
        self.cDawn = ''
        self.cDusk = ''
        self.nDawn = ''
        self.nDusk = ''
        self.aDawn = ''
        self.aDusk = ''
        self.currCondition = "Undefined"
        self.prevcurrCondition = "Undefined"
        self.ctrCondition = 0
        self.iGetWeather = 1
        self.eventPrefix = eventPrefix
        self.weatherChange = weatherChange
        if self.OkButtonClicked:
            self.RestartAllSuntrackers()
        if self.restarted:
            self.restarted = False
            self.RestartAllSuntrackers()
        self.pData = eg.configDir + '\plugins\SunTracker'
        if not os.path.exists(self.pData) and not os.path.isdir(self.pData):
                os.makedirs(self.pData)
        if ConfigData.movingGhost:
            print self.text.lg_movingG_2 + "ON"

        #Get the various possible weather conditions
        self.dark = weather_conditions.weather_conditions_dark()
        self.half_bright = weather_conditions.weather_conditions_half_bright()
        self.bright = weather_conditions.weather_conditions_bright()
        self.excpt = weather_conditions.weather_conditions_except()

        # start the main thread
        self.mainThreadEvent = Event()
        mainThread = Thread(target=self.main, args=(self.mainThreadEvent,))
        mainThread.start()
        self.started = True


    def __stop__(self):
        self.mainThreadEvent.set()
        print self.text.closing
        self.AbortAllSuntrackers()
        self.started = False


    def __close__(self):
        self.AbortAllSuntrackers()
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
        print 'Vacation/Empty House modes changed for SunTracker: ', prm


    def LogToFile(self, s, fName):
        bLogToFile = True
        try:
            bLogToFile = weather_conditions.doLogToFile()
        except:
            pass
        if bLogToFile:
            timeStamp = str(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            logStr = timeStamp+"\t"+s+"<br\n>"
            fileHandle = None

            progData = eg.configDir + '\plugins\SunTracker'
            if not os.path.exists(progData) and not os.path.isdir(progData):
                    os.makedirs(progData)
            fileHandle = open(progData+'/'+fName, 'a')
            fileHandle.write(logStr)
            fileHandle.close()


    def Check_for_daylight_saving(self):
        iDLS = 0
        iDLS = time.localtime()[-1]
        if iDLS == 1:
            if self.initsynch:
                msg = "SunTracker: "+self.text.txt_dls_true
                self.LogToFile(msg, 'Suntracker.html')
                msg = time.strftime(
                   ("%Z"+self.text.txt_tz),
                    time.localtime()
                )
                self.LogToFile(msg, 'Suntracker.html')
        else:
            iDLS = 0
            if self.initsynch:
                msg = "SunTracker: "+self.text.txt_dls_false
                self.LogToFile(msg, 'Suntracker.html')
                msg = time.strftime(
                   ("%Z"+self.text.txt_tz),
                    time.localtime()
                )
                self.LogToFile(msg, 'Suntracker.html')
        return(iDLS)


    def CheckWeatherCondition(self):
        self.weather_data = None
        currCondition = "Undefined"
        try:
            self.weather_data = pywapi.get_weather_from_yahoo(
                int(self.location_id),
                units = self.unit
            )
            wd = self.weather_data['html_description'].split(':')[2].split('>')[2]
            currCondition = wd[1:wd.find(',')]
            self.prevcurrCondition = currCondition
        except:
             currCondition = self.prevcurrCondition
        return currCondition


    def GetOffsetTimeSR(self, iO):
        if iO > 120:
            iO = 120
        if iO < -120:
            iO = -120
        now = datetime.datetime.now()
        diff = datetime.timedelta(minutes=abs(iO))
        if iO<0:
            corr = now - diff
        else:
            corr = now + diff
        s = corr.strftime("%H%M")
        return(s)


    def GetOffsetTimeSS(self, iO):
        if iO > 120:
            iO = 120
        if iO < -120:
            iO = -120
        now = datetime.datetime.now()
        diff = datetime.timedelta(minutes=abs(iO))
        if iO<0:
            corr = now + diff
        else:
            corr = now - diff
        s = corr.strftime("%H%M")
        return(s)


    def CalcWeatherCompensation(
        self,
        currCondition,
        timeCompensation,
        iWeather,
        iOffset
    ):
        cFound = False

        # Adjust the sunrise/sunset trig times to weather condition
        currMonth = time.strftime("%m", time.localtime())

        # Set the default
        trigTimeSR = self.GetOffsetTimeSR(iOffset)
        trigTimeSS = self.GetOffsetTimeSS(iOffset)

        if  currCondition in self.dark:
            cFound = True
            trigTimeSR = self.GetOffsetTimeSR(
                                - iWeather
                                + iOffset
                         )
            trigTimeSS = self.GetOffsetTimeSS(
                                - iWeather
                                + iOffset
                         )
            timeCompensation = - iWeather + iOffset

        if  currCondition in self.half_bright:
            cFound = True
            trigTimeSR = self.GetOffsetTimeSR(
                                - iWeather/2
                                + iOffset
                         )
            trigTimeSS = self.GetOffsetTimeSS(
                                - iWeather/2
                                + iOffset
                         )
            timeCompensation = - iWeather/2 + iOffset

        if  currCondition in self.bright:
            cFound = True
            if(
                not self.summerSeasonBegins == "--"
                and not self.summerSeasonEnds == "--"
            ):
                if(
                    (
                        int(self.summerSeasonBegins) <=
                        int(self.summerSeasonEnds)
                    )
                    and
                    (
                        int(currMonth) >= int(self.summerSeasonBegins)
                        and int(currMonth) <= int(self.summerSeasonEnds)
                    )
                ):
                    trigTimeSR = self.GetOffsetTimeSR(
                                        iWeather
                                        + iOffset
                                 )
                    trigTimeSS = self.GetOffsetTimeSS(
                                        iWeather
                                        + iOffset
                                 )
                    timeCompensation =(
                                        iWeather
                                        + iOffset
                                        )
                if(
                    (
                        int(self.summerSeasonBegins) >
                        int(self.summerSeasonEnds)
                    )
                    and
                    (
                        int(currMonth) >= int(self.summerSeasonBegins)
                        or int(currMonth) <= int(self.summerSeasonEnds)
                    )
                ):
                    trigTimeSR = self.GetOffsetTimeSR(
                                        iWeather
                                        + iOffset
                                 )
                    trigTimeSS = self.GetOffsetTimeSS(
                                        iWeather
                                        + iOffset
                                 )
                    timeCompensation = iWeather + iOffset
            else:
                timeCompensation = iWeather/2 + iOffset

        if currCondition in self.excpt:
            cFound = True
            timeCompensation = iOffset

        if not cFound:
            eg.PrintError(self.text.txtNoCondition + currCondition)

        return (currCondition, timeCompensation, trigTimeSS, trigTimeSR)


    def GetTimeStrings(self, st, iDLS, strTz):
        st = st.replace("(", "")
        st = st.replace(")", "")
        st = st.replace(",", "")

        # Split and extract the data
        data = st.split()
        t1 = float(data[0])
        if t1 < 0:
            t1 = 24.0 + t1
        t2 = float(data[1])
        if t2 < 0:
            t2 = 24.0 + t2

        dat1 = str(t1).split(".")
        dat2 = str(t2).split(".")

        if int(strTz[0]) < 0 and strTz[1] <> '00':
            strTz[1] = '-' + strTz[1]

        if int(dat1[0]) < 0 and int(dat1[1]) > 0:
            h1 = int(int(dat1[0]) -1 + iDLS + int(strTz[0]))
            m1 = int(60-float('.' + dat1[1]) * 60 + float(strTz[1]))
        else:
            h1 = int(int(dat1[0]) + iDLS + int(strTz[0]))
            m1 = int(float('.' + dat1[1]) * 60 + float(strTz[1]))

        if m1 < 0:
            h1 -= 1
            m1 = 60 + m1
        if m1 > 60:
            h1 += 1
            m1 = m1 - 60
        if h1 > 23:
            h1 = abs(24 - h1)
        if h1 < 0:
            h1 = 24 + h1

        sh1 = str(h1)
        if len(sh1) < 2:
            sh1 = "0" + sh1
        sm1 = str(m1)
        if len(sm1) < 2:
            sm1 = "0" + sm1

        if int(dat2[0]) < 0 and int(dat2[1]) > 0:
            h2 = int(int(dat2[0]) - 1 + iDLS + int(strTz[0]))
            m2 = int(60 - float('.' + dat2[1]) * 60 + float(strTz[1]))
        else:
            h2 = int(int(dat2[0]) + iDLS + int(strTz[0]))
            m2 = int(float('.' + dat2[1]) * 60 + float(strTz[1]))

        if m2 < 0:
            h2 -= 1
            m2 = 60 + m2
        if m2 > 60:
            h2 += 1
            m2 = m2 - 60
        if h2 > 23:
            h2 = abs(24 - h2)
        if h2 < 0:
            h2 = 24 + h2

        sh2 = str(h2)
        if len(sh2) < 2:
            sh2 = "0" + sh2
        sm2 = str(m2)
        if len(sm2) < 2:
            sm2 = "0" + sm2

        return sh1 + sm1, sh2 + sm2


    def main(self,mainThreadEvent):
        self.iGetWeatherCntr = 0
        i = 0
        while not mainThreadEvent.isSet():
            if self.initsynch:
                mainThreadEvent.wait(1.0)
                self.currCondition = self.CheckWeatherCondition()
                if self.weatherStatus:
                    eg.TriggerEvent(
                        "Weather Condition:",
                        str(self.currCondition),
                        self.eventPrefix
                    )

            year = int(time.strftime("%Y", time.localtime()))
            month = int(time.strftime("%m", time.localtime()))
            day = int(time.strftime("%d", time.localtime()))

            # Check if we are in daylight savings
            iDLS = self.Check_for_daylight_saving()

            # Adjust the times according to your timezone and daylight savings
            strTz = self.iTimeZone.split('.')

            # Get the Sunrise/Sunset times in UT and fix the format
            st = str(self.k.getSunState(
                year,
                month,
                day,
                float(self.myLongitude),
                float(self.myLatitude))
            )
            self.csSR, self.csSS = self.GetTimeStrings(st, iDLS, strTz)

            # Get the various Dawn/Dusk times in UT and fix the format
            st = str(self.k.getCivilTwilight(
                year,
                month,
                day,
                float(self.myLongitude),
                float(self.myLatitude))
            )
            self.cDawn, self.cDusk = self.GetTimeStrings(st, iDLS, strTz)

            st = str(self.k.getNauticalTwilight(
                year,
                month,
                day,
                float(self.myLongitude),
                float(self.myLatitude))
            )
            self.nDawn, self.nDusk = self.GetTimeStrings(st, iDLS, strTz)

            st = str(self.k.getAstronomicalTwilight(
                year,
                month,
                day,
                float(self.myLongitude),
                float(self.myLatitude))
            )
            self.aDawn, self.aDusk = self.GetTimeStrings(st, iDLS, strTz)

            # Get the current date & time now and adjust to timezone
            now = datetime.datetime.now()
            hr = str(now.hour)
            mn = str(now.minute)

            if len(hr) < 2:
                hr = '0' + hr
            if len(mn)< 2 :
                mn = '0' + mn
            trigTime = hr + mn

            # Set the flag for sun status
            if trigTime >= self.csSS or trigTime < self.csSR:
                self.sunIsUp = False
            else:
                self.sunIsUp = True

            if trigTime == self.csSR:
                if self.sunStatus:
                    eg.TriggerEvent(
                        self.text.sunIsUp,
                        None,
                        self.eventPrefix
                    )
            if trigTime == self.csSS:
                if self.sunStatus:
                    eg.TriggerEvent(
                        self.text.sunIsDown,
                        None,
                        self.eventPrefix
                    )

            if i >= self.weatherUpdateRate:
                self.currCondition = self.CheckWeatherCondition()
                i = 0
                # Generate an event with current weather condition
                if self.weatherStatus:
                    if(
                        (self.weatherChange and
                             self.currCondition <> self.prevcurrCondition)
                        or not self.weatherChange
                    ):
                        eg.TriggerEvent(
                            "Weather Condition:",
                            str(self.currCondition),
                            self.eventPrefix
                        )

            self.initsynch = False
            i += 1
            remain = 60.0 - int(time.strftime("%S", time.localtime()))
            mainThreadEvent.wait(remain)

    #methods to Control suntrackers
    def StartSuntracker(
        self,
        dayTimeSettings,
        suntrackerName,
        eventNameOn,
        eventNameOff,
        fixedHolidays,
        variableHolidays,
        iNbrOfBurstsON,
        iNbrOfBurstsOFF,
        cmdDelay,
        doLogLoops,
        vacation_m,
        moving_Ghost,
        moving_Ghost_G,
        moving_Ghost_r1,
        moving_Ghost_r2,
        moving_Ghost_r3,
        moving_Ghost_r4,
        moving_Ghost_r5,
        moving_Ghost_r6,
        moving_Ghost_r7,
        moving_Ghost_r8,
        bDoSynch,
        iOffset,
        iWeather,
        iMinOnPeriod,
        myLongitude,
        myLatitude,
        location_id,
        iSynchInterval,
        summerSeasonBegins,
        summerSeasonEnds,
        moving_Ghost_excl,
        unit,
        weatherUpdateRate,
        emptyHouse_m,
        eventPrefix,
        weatherChange
    ):
        if self.suntrackerThreads.has_key(suntrackerName):
            t = self.suntrackerThreads[suntrackerName]
            if t.isAlive():
                t.AbortSuntracker()
            del self.suntrackerThreads[suntrackerName]
        t = SuntrackerThread(
            dayTimeSettings,
            suntrackerName,
            eventNameOn,
            eventNameOff,
            fixedHolidays,
            variableHolidays,
            iNbrOfBurstsON,
            iNbrOfBurstsOFF,
            cmdDelay,
            doLogLoops,
            vacation_m,
            moving_Ghost,
            moving_Ghost_G,
            moving_Ghost_r1,
            moving_Ghost_r2,
            moving_Ghost_r3,
            moving_Ghost_r4,
            moving_Ghost_r5,
            moving_Ghost_r6,
            moving_Ghost_r7,
            moving_Ghost_r8,
            bDoSynch,
            iOffset,
            iWeather,
            iMinOnPeriod,
            myLongitude,
            myLatitude,
            location_id,
            iSynchInterval,
            summerSeasonBegins,
            summerSeasonEnds,
            moving_Ghost_excl,
            unit,
            weatherUpdateRate,
            emptyHouse_m,
            eventPrefix,
            weatherChange,
            self
        )
        t.start()
        self.suntrackerThreads[suntrackerName] = t


    def AbortSuntracker(self, suntracker):
        if self.suntrackerThreads.has_key(suntracker):
            t = self.suntrackerThreads[suntracker]
            t.AbortSuntracker()
            del self.suntrackerThreads[suntracker]


    def AbortAllSuntrackers(self):
        for i, item in enumerate(self.suntrackerThreads):
            t = self.suntrackerThreads[item]
            t.AbortSuntracker()
            del t
            time.sleep(0.1)
        self.suntrackerThreads = {}


    def RestartAllSuntrackers(self, startNewIfNotAlive = True):
        self.AbortAllSuntrackers()
        params = self.AllsuntrackerNames
        for i, item in enumerate(params):
            if startNewIfNotAlive:
                time.sleep(0.1)
                self.StartSuntracker(
                    self.GetAlldayTimeSettings()[i],
                    self.GetAllsuntrackerNames()[i],
                    self.GetAlleventNameOn()[i],
                    self.GetAlleventNameOff()[i],
                    self.fixedHolidays,
                    self.variableHolidays,
                    self.GetAlliNbrOfBurstsON()[i],
                    self.GetAlliNbrOfBurstsOFF()[i],
                    self.GetAllcmdDelay()[i],
                    self.GetAlldoLogLoops()[i],
                    self.vacation_m,
                    self.GetAllmoving_Ghost()[i],
                    self.GetAllmoving_Ghost_G()[i],
                    self.GetAllMoving_Ghost_r1()[i],
                    self.GetAllMoving_Ghost_r2()[i],
                    self.GetAllMoving_Ghost_r3()[i],
                    self.GetAllMoving_Ghost_r4()[i],
                    self.GetAllMoving_Ghost_r5()[i],
                    self.GetAllMoving_Ghost_r6()[i],
                    self.GetAllMoving_Ghost_r7()[i],
                    self.GetAllMoving_Ghost_r8()[i],
                    self.GetAllbDoSynch()[i],
                    self.GetAlliOffset()[i],
                    self.GetAlliWeather()[i],
                    self.GetAlliMinOnPeriod()[i],
                    self.myLongitude,
                    self.myLatitude,
                    self.location_id,
                    self.GetAlliSynchInterval()[i],
                    self.summerSeasonBegins,
                    self.summerSeasonEnds,
                    self.GetAllmoving_Ghost_excl()[i],
                    self.unit,
                    self.weatherUpdateRate,
                    self.emptyHouse_m,
                    self.eventPrefix,
                    self.weatherChange
                )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        myLongitude = "18.0000",
        myLatitude = "59.2500",
        location_id = "905335",
        fixedHolidays = "0101,0501,0606,1224,1225,1226",
        variableHolidays = "0106,0402,0405,0512,0522,0523,0625",
        summerSeasonBegins = "--",
        summerSeasonEnds = "--",
        vacation_m = False,
        sunStatus = True,
        weatherStatus = True,
        iTimeZone = '+01.00',
        unit = "metric",
        weatherUpdateRate = 5,
        emptyHouse_m = False,
        eventPrefix = "Main",
        weatherChange = False,
        *args
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)

        suntrackerListCtrl = wx.ListCtrl(
            panel,
            -1,
            style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL
        )

        for i, colLabel in enumerate(self.text.colLabels):
            suntrackerListCtrl.InsertColumn(i, colLabel)

        #setting col width to fit label
        suntrackerListCtrl.InsertStringItem(0, "Test Suntracker Name")
        suntrackerListCtrl.SetStringItem(0, 1, "Test EventName On")

        size = 0
        for i in range(2):
            suntrackerListCtrl.SetColumnWidth(
                i,
                wx.LIST_AUTOSIZE_USEHEADER
            ) #wx.LIST_AUTOSIZE
            size += suntrackerListCtrl.GetColumnWidth(i)

        suntrackerListCtrl.SetMinSize((size, -1))

        mySizer_1.Add(suntrackerListCtrl,(0,0),(1, 5), flag = wx.EXPAND)

        #buttons
        abortButton = wx.Button(panel, -1, self.text.b_abort)
        mySizer_1.Add(abortButton,(1,0))

        abortAllButton = wx.Button(panel, -1, self.text.b_abortAll)
        mySizer_1.Add(abortAllButton,(1,1), flag = wx.ALIGN_RIGHT)

        restartAllButton = wx.Button(panel, -1, self.text.b_restartAll)
        mySizer_1.Add(restartAllButton,(1,2), flag = wx.ALIGN_RIGHT)

        refreshButton = wx.Button(panel, -1, self.text.b_refresh)
        mySizer_1.Add(refreshButton,(1,4), flag = wx.ALIGN_RIGHT)

        mySizer_1.AddGrowableRow(0)
        mySizer_1.AddGrowableCol(1)
        mySizer_1.AddGrowableCol(2)
        mySizer_1.AddGrowableCol(3)

        f_myLatitude = float(myLatitude)
        myLatitudeCtrl = panel.SpinNumCtrl(
            f_myLatitude,
            decimalChar = '.',                 # by default, use '.' for decimal point
            groupChar = ',',                   # by default, use ',' for grouping
            fractionWidth = 4,
            integerWidth = 3,
            min = -90.0000,
            max = 90.0000,
            increment = 0.0050
        )
        myLatitudeCtrl.SetInitialSize((90,-1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMyLatitude
            ),
           (0,0)
        )
        mySizer_2.Add(myLatitudeCtrl,(0,1))

        f_myLongitude = float(myLongitude)
        myLongitudeCtrl = panel.SpinNumCtrl(
            f_myLongitude,
            decimalChar = '.',                 # by default, use '.' for decimal point
            groupChar = ',',                   # by default, use ',' for grouping
            fractionWidth = 4,
            integerWidth = 4,
            min = -180.0000,
            max = 180.0000,
            increment = 0.0050
        )
        myLongitudeCtrl.SetInitialSize((90,-1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMyLongitude
            ),
           (1,0)
        )
        mySizer_2.Add(myLongitudeCtrl,(1,1))

        # Select or accept proposed timezone
        iTimeZoneCtrl = wx.Choice(parent=panel, pos=(10,10))
        list = [
            '-12.00',
            '-11.00',
            '-10.00',
            '-09.30',
            '-09.00',
            '-08.00',
            '-07.00',
            '-06.00',
            '-05.00',
            '-04.30',
            '-04.00',
            '-03.00',
            '-02.00',
            '-01.00',
            '00.00',
            '+01.00',
            '+02.00',
            '+03.00',
            '+03.30',
            '+04.00',
            '+04.30',
            '+05.00',
            '+05.30',
            '+05.45',
            '+06.00',
            '+06.30',
            '+07.00',
            '+08.00',
            '+09.00',
            '+09.30',
            '+10.00',
            '+10.30',
            '+11.00',
            '+11.30',
            '+12.00',
            '+12.45',
            '+13.00',
            '+14.00'
        ]
        iTimeZoneCtrl.SetInitialSize((60,-1))
        iTimeZoneCtrl.AppendItems(strings=list)
        if list.count(iTimeZone)==0:
            iTimeZoneCtrl.Select(n=0)
        else:
            iTimeZoneCtrl.SetSelection(int(list.index(iTimeZone)))
        iTimeZoneCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtTimeZone
            ),
           (1,2)
        )
        mySizer_2.Add(iTimeZoneCtrl,(1,3))

        desc1 = wx.StaticText(panel, -1, self.text.LocationLabel)
        mySizer_2.Add(desc1,(2,0))
        Location = wx.TextCtrl(panel, -1,location_id)
        Location.SetInitialSize((200,-1))
        mySizer_2.Add(Location,(2,1))

        unitCtrl = wx.Choice(parent=panel, pos=(10,10))
        list = ['metric', 'non-metric']
        unitCtrl.AppendItems(strings=list)
        if list.count(unit)==0:
            unitCtrl.Select(n=0)
        else:
            unitCtrl.SetSelection(int(list.index(unit)))
        unitCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        sBtxt = wx.StaticText(panel, -1, self.text.txtUnit)
        mySizer_2.Add(sBtxt,(3,0))
        mySizer_2.Add(unitCtrl,(3,1))

        weatherUpdateRateCtrl = panel.SpinIntCtrl(weatherUpdateRate, 1, 60)
        weatherUpdateRateCtrl.SetInitialSize((50,-1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.weatherUpdateRate
            ),
           (4,0)
        )
        mySizer_2.Add(weatherUpdateRateCtrl,(4,1))

        fixedHolidaysCtrl = wx.TextCtrl(panel, -1, fixedHolidays)
        fixedHolidaysCtrl.SetInitialSize((300,-1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtFixedHolidays
            ),
           (5,0)
        )
        mySizer_2.Add(fixedHolidaysCtrl,(5,1))

        variableHolidaysCtrl = wx.TextCtrl(panel, -1, variableHolidays)
        variableHolidaysCtrl.SetInitialSize((300,-1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtVariableHolidays
            ),
           (6,0)
        )
        mySizer_2.Add(variableHolidaysCtrl,(6,1))

        summerBeginsCtrl = wx.Choice(parent=panel, pos=(10,10))
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
        summerBeginsCtrl.AppendItems(strings=list)
        if list.count(summerSeasonBegins)==0:
            summerBeginsCtrl.Select(n=0)
        else:
            summerBeginsCtrl.SetSelection(int(list.index(summerSeasonBegins)))
        summerBeginsCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        sBtxt = wx.StaticText(panel, -1, self.text.txtSummerSeasonBegins)
        mySizer_2.Add(sBtxt,(7,0))
        mySizer_2.Add(summerBeginsCtrl,(7,1))

        summerEndsCtrl = wx.Choice(parent=panel, pos=(10,10))
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
        summerEndsCtrl.AppendItems(strings=list)
        if list.count(summerSeasonEnds)==0:
            summerEndsCtrl.Select(n=0)
        else:
            summerEndsCtrl.SetSelection(int(list.index(summerSeasonEnds)))
        summerEndsCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        sEtxt = wx.StaticText(panel, -1, self.text.txtSummerSeasonEnds)
        mySizer_2.Add(sEtxt,(8,0))
        mySizer_2.Add(summerEndsCtrl,(8,1))

        eventPrefixCtrl = wx.TextCtrl(panel, -1, eventPrefix)
        eventPrefixCtrl.SetInitialSize((100,-1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.eventPrefix
            ),
           (9,0)
        )
        mySizer_2.Add(eventPrefixCtrl,(9,1))

        vacation_mCtrl = wx.CheckBox(panel, -1, self.text.txtVacation_m)
        vacation_mCtrl.SetValue(vacation_m)
        mySizer_2.Add(vacation_mCtrl,(11,0))

        emptyHouse_mCtrl = wx.CheckBox(panel, -1, self.text.txtEmptyHouse_m)
        emptyHouse_mCtrl.SetValue(emptyHouse_m)
        mySizer_2.Add(emptyHouse_mCtrl,(11,1))

        sunStatusCtrl = wx.CheckBox(panel, -1, self.text.sunStatus)
        sunStatusCtrl.SetValue(sunStatus)
        mySizer_2.Add(sunStatusCtrl,(12,0))

        weatherStatusCtrl = wx.CheckBox(panel, -1, self.text.weatherStatus)
        weatherStatusCtrl.SetValue(weatherStatus)
        mySizer_2.Add(weatherStatusCtrl,(13,0))

        weatherChangeCtrl = wx.CheckBox(panel, -1, self.text.txtWeatherChange)
        weatherChangeCtrl.SetValue(weatherChange)
        mySizer_2.Add(weatherChangeCtrl,(13,1))

        font = panel.GetFont()
        p = font.GetPointSize()

        font.SetPointSize(9)
        font.SetWeight(wx.BOLD)
        panel.SetFont(font)
        box = wx.StaticBox(panel,-1, self.text.listhl)
        font.SetPointSize(p)
        font.SetWeight(wx.NORMAL)
        panel.SetFont(font)
        Sizer_1 = wx.StaticBoxSizer(box,wx.VERTICAL)
        Sizer_1.Add(mySizer_1)
        panel.sizer.Add(Sizer_1, 0, flag = wx.EXPAND)

        font.SetPointSize(9)
        font.SetWeight(wx.BOLD)
        panel.SetFont(font)
        box = wx.StaticBox(panel,-1, self.text.pHeading)
        font.SetPointSize(p)
        font.SetWeight(wx.NORMAL)
        panel.SetFont(font)
        Sizer_2 = wx.StaticBoxSizer(box,wx.VERTICAL)
        Sizer_2.Add(mySizer_2)
        panel.sizer.Add(Sizer_2, 0, flag = wx.EXPAND)


        def PopulateList(event):
            suntrackerListCtrl.DeleteAllItems()
            row = 0
            for i, item in enumerate(self.suntrackerThreads):
                t = self.suntrackerThreads[item]
                if t.isAlive():
                    suntrackerListCtrl.InsertStringItem(row, t.name)
                    suntrackerListCtrl.SetStringItem(row,
                        1, t.eventNameOn)
                    suntrackerListCtrl.SetStringItem(row,
                        2, t.eventNameOff)
                    row += 1
            ListSelection(wx.CommandEvent())


        def OnAbortButton(event):
            item = suntrackerListCtrl.GetFirstSelected()
            while item != -1:
                name = suntrackerListCtrl.GetItemText(item)
                self.AbortSuntracker(name)
                item = suntrackerListCtrl.GetNextSelected(item)
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnAbortAllButton(event):
            self.AbortAllSuntrackers()
            PopulateList(wx.CommandEvent())
            event.Skip()


        def OnRestartAllButton(event):
            self.RestartAllSuntrackers()
            PopulateList(wx.CommandEvent())
            event.Skip()


        def ListSelection(event):
            flag = suntrackerListCtrl.GetFirstSelected() != -1
            abortButton.Enable(flag)
            event.Skip()


        def OnSize(event):
            suntrackerListCtrl.SetColumnWidth(
                6,
                wx.LIST_AUTOSIZE_USEHEADER
            )
            event.Skip()


        def OnApplyButton(event):
            event.Skip()
            self.RestartAllSuntrackers()
            PopulateList(wx.CommandEvent())


        def OnOkButton(event):
            event.Skip()
            self.OkButtonClicked = True


        PopulateList(wx.CommandEvent())
        abortButton.Bind(wx.EVT_BUTTON, OnAbortButton)
        abortAllButton.Bind(wx.EVT_BUTTON, OnAbortAllButton)
        restartAllButton.Bind(wx.EVT_BUTTON, OnRestartAllButton)
        refreshButton.Bind(wx.EVT_BUTTON, PopulateList)
        suntrackerListCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, ListSelection)
        suntrackerListCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, ListSelection)
        panel.Bind(wx.EVT_SIZE, OnSize)
        panel.dialog.buttonRow.applyButton.Bind(wx.EVT_BUTTON, OnApplyButton)
        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnOkButton)

        while panel.Affirmed():
            myLongitude = str(myLongitudeCtrl.GetValue())
            myLatitude = str(myLatitudeCtrl.GetValue())
            location_id = Location.GetValue()
            fixedHolidays = fixedHolidaysCtrl.GetValue()
            variableHolidays = variableHolidaysCtrl.GetValue()
            summerSeasonBegins = summerBeginsCtrl.GetStringSelection()
            summerSeasonEnds = summerEndsCtrl.GetStringSelection()
            eventPrefix = eventPrefixCtrl.GetValue()
            if eventPrefix == '':
                eventPrefix = 'SunTracker'
            vacation_m = vacation_mCtrl.GetValue()
            emptyHouse_m = emptyHouse_mCtrl.GetValue()
            sunStatus = sunStatusCtrl.GetValue()
            weatherStatus = weatherStatusCtrl.GetValue()
            iTimeZone = iTimeZoneCtrl.GetStringSelection()
            unit = unitCtrl.GetStringSelection()
            weatherUpdateRate = weatherUpdateRateCtrl.GetValue()
            weatherChange = weatherChangeCtrl.GetValue()
            panel.SetResult(
                        myLongitude,
                        myLatitude,
                        location_id,
                        fixedHolidays,
                        variableHolidays,
                        summerSeasonBegins,
                        summerSeasonEnds,
                        vacation_m,
                        sunStatus,
                        weatherStatus,
                        iTimeZone,
                        unit,
                        weatherUpdateRate,
                        emptyHouse_m,
                        eventPrefix,
                        weatherChange,
                        *args
            )


    def GetAllsuntrackerNames(self):
        return self.AllsuntrackerNames


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


    def GetAlliOffset(self):
        return self.AlliOffset


    def GetAlliWeather(self):
        return self.AlliWeather


    def GetAlliMinOnPeriod(self):
        return self.AlliMinOnPeriod


    def GetAllmoving_Ghost(self):
        return self.Allmoving_Ghost


    def GetAllmoving_Ghost_G(self):
        return self.Allmoving_Ghost_G


    def GetAllmoving_Ghost_excl(self):
        return self.Allmoving_Ghost_excl


    def GetAllMoving_Ghost_r1(self):
        return self.AllMoving_Ghost_r1


    def GetAllMoving_Ghost_r2(self):
        return self.AllMoving_Ghost_r2


    def GetAllMoving_Ghost_r3(self):
        return self.AllMoving_Ghost_r3


    def GetAllMoving_Ghost_r4(self):
        return self.AllMoving_Ghost_r4


    def GetAllMoving_Ghost_r5(self):
        return self.AllMoving_Ghost_r5


    def GetAllMoving_Ghost_r6(self):
        return self.AllMoving_Ghost_r6


    def GetAllMoving_Ghost_r7(self):
        return self.AllMoving_Ghost_r7


    def GetAllMoving_Ghost_r8(self):
        return self.AllMoving_Ghost_r8


    def AddSuntrackerName(self, suntrackerName):
        if not suntrackerName in self.AllsuntrackerNames:
            self.AllsuntrackerNames.append(suntrackerName)
        return self.AllsuntrackerNames.index(suntrackerName)


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


    def AddiOffset(self, iOffset, indx):
        try:
            del self.AlliOffset[indx]
        except IndexError:
            i = -1 # no match
        self.AlliOffset.insert(indx, iOffset)


    def AddiWeather(self, iWeather, indx):
        try:
            del self.AlliWeather[indx]
        except IndexError:
            i = -1 # no match
        self.AlliWeather.insert(indx, iWeather)


    def AddiMinOnPeriod(self, iMinOnPeriod, indx):
        try:
            del self.AlliMinOnPeriod[indx]
        except IndexError:
            i = -1 # no match
        self.AlliMinOnPeriod.insert(indx, iMinOnPeriod)


    def AddMoving_Ghost(self, moving_Ghost, indx):
        try:
            del self.Allmoving_Ghost[indx]
        except IndexError:
            i = -1 # no match
        self.Allmoving_Ghost.insert(indx, moving_Ghost)


    def AddMoving_Ghost_G(self, moving_Ghost_G, indx):
        try:
            del self.Allmoving_Ghost_G[indx]
        except IndexError:
            i = -1 # no match
        self.Allmoving_Ghost_G.insert(indx, moving_Ghost_G)


    def AddMoving_Ghost_excl(self, moving_Ghost_excl, indx):
        try:
            del self.Allmoving_Ghost_excl[indx]
        except IndexError:
            i = -1 # no match
        self.Allmoving_Ghost_excl.insert(indx, moving_Ghost_excl)


    def AddMoving_Ghost_r1(self, moving_Ghost_r1, indx):
        try:
            del self.AllMoving_Ghost_r1[indx]
        except IndexError:
            i = -1 # no match
        self.AllMoving_Ghost_r1.insert(indx, moving_Ghost_r1)


    def AddMoving_Ghost_r2(self, moving_Ghost_r2, indx):
        try:
            del self.AllMoving_Ghost_r2[indx]
        except IndexError:
            i = -1 # no match
        self.AllMoving_Ghost_r2.insert(indx, moving_Ghost_r2)


    def AddMoving_Ghost_r3(self, moving_Ghost_r3, indx):
        try:
            del self.AllMoving_Ghost_r3[indx]
        except IndexError:
            i = -1 # no match
        self.AllMoving_Ghost_r3.insert(indx, moving_Ghost_r3)


    def AddMoving_Ghost_r4(self, moving_Ghost_r4, indx):
        try:
            del self.AllMoving_Ghost_r4[indx]
        except IndexError:
            i = -1 # no match
        self.AllMoving_Ghost_r4.insert(indx, moving_Ghost_r4)


    def AddMoving_Ghost_r5(self, moving_Ghost_r5, indx):
        try:
            del self.AllMoving_Ghost_r5[indx]
        except IndexError:
            i = -1 # no match
        self.AllMoving_Ghost_r5.insert(indx, moving_Ghost_r5)


    def AddMoving_Ghost_r6(self, moving_Ghost_r6, indx):
        try:
            del self.AllMoving_Ghost_r6[indx]
        except IndexError:
            i = -1 # no match
        self.AllMoving_Ghost_r6.insert(indx, moving_Ghost_r6)


    def AddMoving_Ghost_r7(self, moving_Ghost_r7, indx):
        try:
            del self.AllMoving_Ghost_r7[indx]
        except IndexError:
            i = -1 # no match
        self.AllMoving_Ghost_r7.insert(indx, moving_Ghost_r7)


    def AddMoving_Ghost_r8(self, moving_Ghost_r8, indx):
        try:
            del self.AllMoving_Ghost_r8[indx]
        except IndexError:
            i = -1 # no match
        self.AllMoving_Ghost_r8.insert(indx, moving_Ghost_r8)



class SuntrackerAction(eg.ActionClass):
    name = "Start new or control running SunTracker"
    description =(
        "Allows starting, stopping or resetting SunTrackers, which "+
        "triggers an event at sunset/sunrise and a given date & time"
    )
    iconFile = "suntracker"

    def __call__(
        self,
        dayTimeSettings,
        suntrackerName,
        eventNameOn,
        eventNameOff,
        moNight_OFF,
        moMorning_ON,
        moEvening_OFF,
        tuNight_OFF,
        tuMorning_ON,
        tuEvening_OFF,
        weNight_OFF,
        weMorning_ON,
        weEvening_OFF,
        thNight_OFF,
        thMorning_ON,
        thEvening_OFF,
        frNight_OFF,
        frMorning_ON,
        frEvening_OFF,
        saNight_OFF,
        saMorning_ON,
        saEvening_OFF,
        suNight_OFF,
        suMorning_ON,
        suEvening_OFF,
        vaNight_OFF,
        vaMorning_ON,
        vaEvening_OFF,
        fixedHolidays,
        variableHolidays,
        iNbrOfBurstsON,
        iNbrOfBurstsOFF,
        cmdDelay,
        doLogLoops,
        vacation_m,
        moving_Ghost,
        moving_Ghost_G,
        moving_Ghost_r1,
        moving_Ghost_r2,
        moving_Ghost_r3,
        moving_Ghost_r4,
        moving_Ghost_r5,
        moving_Ghost_r6,
        moving_Ghost_r7,
        moving_Ghost_r8,
        bDoSynch,
        iOffset,
        iWeather,
        iMinOnPeriod,
        myLongitude,
        myLatitude,
        location_id,
        iSynchInterval,
        summerSeasonBegins,
        summerSeasonEnds,
        moving_Ghost_excl,
        unit,
        weatherUpdateRate,
        ehNight_OFF,
        ehMorning_ON,
        ehEvening_OFF,
        emptyHouse_m,
        eventPrefix,
        weatherChange
    ):
        self.plugin.StartSuntracker(
            dayTimeSettings,
            suntrackerName,
            eventNameOn,
            eventNameOff,
            self.plugin.fixedHolidays,
            self.plugin.variableHolidays,
            iNbrOfBurstsON,
            iNbrOfBurstsOFF,
            cmdDelay,
            doLogLoops,
            self.plugin.vacation_m,
            moving_Ghost,
            moving_Ghost_G,
            moving_Ghost_r1,
            moving_Ghost_r2,
            moving_Ghost_r3,
            moving_Ghost_r4,
            moving_Ghost_r5,
            moving_Ghost_r6,
            moving_Ghost_r7,
            moving_Ghost_r8,
            bDoSynch,
            iOffset,
            iWeather,
            iMinOnPeriod,
            self.plugin.myLongitude,
            self.plugin.myLatitude,
            self.plugin.location_id,
            iSynchInterval,
            self.plugin.summerSeasonBegins,
            self.plugin.summerSeasonEnds,
            moving_Ghost_excl,
            self.plugin.unit,
            self.plugin.weatherUpdateRate,
            self.plugin.emptyHouse_m,
            self.plugin.eventPrefix,
            self.plugin.weatherChange
        )


    def GetLabel(
        self,
        dayTimeSettings,
        suntrackerName,
        eventNameOn,
        eventNameOff,
        moNight_OFF,
        moMorning_ON,
        moEvening_OFF,
        tuNight_OFF,
        tuMorning_ON,
        tuEvening_OFF,
        weNight_OFF,
        weMorning_ON,
        weEvening_OFF,
        thNight_OFF,
        thMorning_ON,
        thEvening_OFF,
        frNight_OFF,
        frMorning_ON,
        frEvening_OFF,
        saNight_OFF,
        saMorning_ON,
        saEvening_OFF,
        suNight_OFF,
        suMorning_ON,
        suEvening_OFF,
        vaNight_OFF,
        vaMorning_ON,
        vaEvening_OFF,
        fixedHolidays,
        variableHolidays,
        iNbrOfBurstsON,
        iNbrOfBurstsOFF,
        cmdDelay,
        doLogLoops,
        vacation_m,
        moving_Ghost,
        moving_Ghost_G,
        moving_Ghost_r1,
        moving_Ghost_r2,
        moving_Ghost_r3,
        moving_Ghost_r4,
        moving_Ghost_r5,
        moving_Ghost_r6,
        moving_Ghost_r7,
        moving_Ghost_r8,
        bDoSynch,
        iOffset,
        iWeather,
        iMinOnPeriod,
        myLongitude,
        myLatitude,
        location_id,
        iSynchInterval,
        summerSeasonBegins,
        summerSeasonEnds,
        moving_Ghost_excl,
        unit,
        weatherUpdateRate,
        ehNight_OFF,
        ehMorning_ON,
        ehEvening_OFF,
        emptyHouse_m,
        eventPrefix,
        weatherChange
    ):


        indx = self.plugin.AddSuntrackerName(suntrackerName)
        self.plugin.AddDayTimeSettings(dayTimeSettings, indx)
        self.plugin.AddEventNameOn(eventNameOn, indx)
        self.plugin.AddEventNameOff(eventNameOff, indx)
        self.plugin.AddInbrOfBurstsON(iNbrOfBurstsON, indx)
        self.plugin.AddInbrOfBurstsOFF(iNbrOfBurstsOFF, indx)
        self.plugin.AddCmdDelay(cmdDelay, indx)
        self.plugin.AddDoLogLoops(doLogLoops, indx)
        self.plugin.AddBdoSynch(bDoSynch, indx)
        self.plugin.AddIsynchInterval(iSynchInterval, indx)
        self.plugin.AddiOffset(iOffset, indx)
        self.plugin.AddiWeather(iWeather, indx)
        self.plugin.AddiMinOnPeriod(iMinOnPeriod, indx)
        self.plugin.AddMoving_Ghost(moving_Ghost, indx)
        self.plugin.AddMoving_Ghost_G(moving_Ghost_G, indx)
        self.plugin.AddMoving_Ghost_excl(moving_Ghost_excl, indx)
        self.plugin.AddMoving_Ghost_r1(moving_Ghost_r1, indx)
        self.plugin.AddMoving_Ghost_r2(moving_Ghost_r2, indx)
        self.plugin.AddMoving_Ghost_r3(moving_Ghost_r3, indx)
        self.plugin.AddMoving_Ghost_r4(moving_Ghost_r4, indx)
        self.plugin.AddMoving_Ghost_r5(moving_Ghost_r5, indx)
        self.plugin.AddMoving_Ghost_r6(moving_Ghost_r6, indx)
        self.plugin.AddMoving_Ghost_r7(moving_Ghost_r7, indx)
        self.plugin.AddMoving_Ghost_r8(moving_Ghost_r8, indx)

        return self.text.labelStart %(suntrackerName)


    def timeFormat(self, theString):
        if theString == "----":
            return theString
        if(
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


    def nightOffFormat(self, theString):
        if theString == "----":
            return theString
        elif int(theString) < int("0001"):
            return "0001"
        elif int(theString) > int("0559"):
            return "0559"
        return theString


    def morningOnFormat(self, theString):
        if theString == "----":
            return theString
        elif int(theString) < int("0001"):
            return "0001"
        elif int(theString) > int("1159"):
            return "1159"
        return theString


    def eveningOffFormat(self, theString):
        if theString == "----":
            return theString
        elif int(theString) <= int("1800"):
            return "1801"
        elif int(theString) > int("2359"):
            return "2359"
        return theString


    def Configure(
        self,
        dayTimeSettings = [],
        suntrackerName = "Give suntracker a name",
        eventNameOn = "nn ON",
        eventNameOff = "nn OFF",
        moNight_OFF = "----",
        moMorning_ON = "----",
        moEvening_OFF = "----",
        tuNight_OFF = "----",
        tuMorning_ON = "----",
        tuEvening_OFF = "----",
        weNight_OFF = "----",
        weMorning_ON = "----",
        weEvening_OFF = "----",
        thNight_OFF = "----",
        thMorning_ON = "----",
        thEvening_OFF = "----",
        frNight_OFF = "----",
        frMorning_ON = "----",
        frEvening_OFF = "----",
        saNight_OFF = "----",
        saMorning_ON = "----",
        saEvening_OFF = "----",
        suNight_OFF = "----",
        suMorning_ON = "----",
        suEvening_OFF = "----",
        vaNight_OFF = "----",
        vaMorning_ON = "----",
        vaEvening_OFF = "----",
        fixedHolidays = "0101,0501,0606,1224,1225,1226,1231",
        variableHolidays = "0106,0321,0324,0620",
        iNbrOfBurstsON = 1,
        iNbrOfBurstsOFF = 1,
        cmdDelay = 1.5,
        doLogLoops = False,
        vacation_m = False,
        moving_Ghost = False,
        moving_Ghost_G = False,
        moving_Ghost_r1 = 10,
        moving_Ghost_r2 = 40,
        moving_Ghost_r3 = 10,
        moving_Ghost_r4 = 40,
        moving_Ghost_r5 = 3,
        moving_Ghost_r6 = 10,
        moving_Ghost_r7 = 40,
        moving_Ghost_r8 = 80,
        bDoSynch = True,
        iOffset = 0,
        iWeather = 0,
        iMinOnPeriod = 10,
        myLongitude = "18.0000",
        myLatitude = "59.2500",
        location_id = "905335",
        iSynchInterval = 30,
        summerSeasonBegins = "--",
        summerSeasonEnds = "--",
        moving_Ghost_excl = False,
        unit = 'metric',
        weatherUpdateRate = 5,
        ehNight_OFF = "----",
        ehMorning_ON = "----",
        ehEvening_OFF = "----",
        emptyHouse_m = False,
        eventPrefix = 'Main',
        weatherChange = False
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(5, 5)
        mySizer_2 = wx.GridBagSizer(5, 5)
        mySizer_3 = wx.GridBagSizer(5, 5)
        mySizer_4 = wx.GridBagSizer(5, 5)

        #name
        suntrackerNameCtrl = wx.TextCtrl(panel, -1, suntrackerName)
        suntrackerNameCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.suntrackerName
            ),
           (0,0)
        )
        mySizer_1.Add(suntrackerNameCtrl,(0,1))

        doLogLoopsCtrl = wx.CheckBox(panel, -1, "")
        doLogLoopsCtrl.SetValue(doLogLoops)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.doLogLoopsText
            ),
           (0,5)
        )
        mySizer_1.Add(doLogLoopsCtrl,(0,6))

        #eventName ON
        eventNameOnCtrl = wx.TextCtrl(panel, -1, eventNameOn)
        eventNameOnCtrl.SetInitialSize((150,-1))
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.eventNameOn
            ),
           (1,0)
        )
        mySizer_1.Add(eventNameOnCtrl,(1,1))

        #eventName OFF
        eventNameOffCtrl = wx.TextCtrl(panel, -1, eventNameOff)
        eventNameOffCtrl.SetInitialSize((150,-1))
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.eventNameOff
            ),
           (2,0)
        )
        mySizer_1.Add(eventNameOffCtrl,(2,1))

        moNight_OFFCtrl = wx.TextCtrl(panel, -1, moNight_OFF)
        moNight_OFFCtrl.SetInitialSize((35,-1))
        moMorning_ONCtrl = wx.TextCtrl(panel, -1, moMorning_ON)
        moMorning_ONCtrl.SetInitialSize((35,-1))
        moEvening_OFFCtrl = wx.TextCtrl(panel, -1, moEvening_OFF)
        moEvening_OFFCtrl.SetInitialSize((35,-1))

        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_moNightOFF
            ),
           (0,0)
        )
        mySizer_2.Add(moNight_OFFCtrl,(0,1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_moMorningON
            ),
           (0,2)
        )
        mySizer_2.Add(moMorning_ONCtrl,(0,3))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_moEveningOFF
            ),
           (0,4)
        )
        mySizer_2.Add(moEvening_OFFCtrl,(0,5))

        tuNight_OFFCtrl = wx.TextCtrl(panel, -1, tuNight_OFF)
        tuNight_OFFCtrl.SetInitialSize((35,-1))
        tuMorning_ONCtrl = wx.TextCtrl(panel, -1, tuMorning_ON)
        tuMorning_ONCtrl.SetInitialSize((35,-1))
        tuEvening_OFFCtrl = wx.TextCtrl(panel, -1, tuEvening_OFF)
        tuEvening_OFFCtrl.SetInitialSize((35,-1))

        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_tuNightOFF
            ),
           (1,0)
        )
        mySizer_2.Add(tuNight_OFFCtrl,(1,1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_tuMorningON
            ),
           (1,2)
        )
        mySizer_2.Add(tuMorning_ONCtrl,(1,3))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_tuEveningOFF
            ),
           (1,4)
        )
        mySizer_2.Add(tuEvening_OFFCtrl,(1,5))

        weNight_OFFCtrl = wx.TextCtrl(panel, -1, weNight_OFF)
        weNight_OFFCtrl.SetInitialSize((35,-1))
        weMorning_ONCtrl = wx.TextCtrl(panel, -1, weMorning_ON)
        weMorning_ONCtrl.SetInitialSize((35,-1))
        weEvening_OFFCtrl = wx.TextCtrl(panel, -1, weEvening_OFF)
        weEvening_OFFCtrl.SetInitialSize((35,-1))

        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_weNightOFF
            ),
           (2,0)
        )
        mySizer_2.Add(weNight_OFFCtrl,(2,1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_weMorningON
            ),
           (2,2)
        )
        mySizer_2.Add(weMorning_ONCtrl,(2,3))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_weEveningOFF
            ),
           (2,4)
        )
        mySizer_2.Add(weEvening_OFFCtrl,(2,5))

        thNight_OFFCtrl = wx.TextCtrl(panel, -1, thNight_OFF)
        thNight_OFFCtrl.SetInitialSize((35,-1))
        thMorning_ONCtrl = wx.TextCtrl(panel, -1, thMorning_ON)
        thMorning_ONCtrl.SetInitialSize((35,-1))
        thEvening_OFFCtrl = wx.TextCtrl(panel, -1, thEvening_OFF)
        thEvening_OFFCtrl.SetInitialSize((35,-1))

        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_thNightOFF
            ),
           (3,0)
        )
        mySizer_2.Add(thNight_OFFCtrl,(3,1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_thMorningON
            ),
           (3,2)
        )
        mySizer_2.Add(thMorning_ONCtrl,(3,3))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_thEveningOFF
            ),
           (3,4)
        )
        mySizer_2.Add(thEvening_OFFCtrl,(3,5))

        frNight_OFFCtrl = wx.TextCtrl(panel, -1, frNight_OFF)
        frNight_OFFCtrl.SetInitialSize((35,-1))
        frMorning_ONCtrl = wx.TextCtrl(panel, -1, frMorning_ON)
        frMorning_ONCtrl.SetInitialSize((35,-1))
        frEvening_OFFCtrl = wx.TextCtrl(panel, -1, frEvening_OFF)
        frEvening_OFFCtrl.SetInitialSize((35,-1))

        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_frNightOFF
            ),
           (4,0)
        )
        mySizer_2.Add(frNight_OFFCtrl,(4,1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_frMorningON
            ),
           (4,2)
        )
        mySizer_2.Add(frMorning_ONCtrl,(4,3))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_frEveningOFF
            ),
           (4,4)
        )
        mySizer_2.Add(frEvening_OFFCtrl,(4,5))

        saNight_OFFCtrl = wx.TextCtrl(panel, -1, saNight_OFF)
        saNight_OFFCtrl.SetInitialSize((35,-1))
        saMorning_ONCtrl = wx.TextCtrl(panel, -1, saMorning_ON)
        saMorning_ONCtrl.SetInitialSize((35,-1))
        saEvening_OFFCtrl = wx.TextCtrl(panel, -1, saEvening_OFF)
        saEvening_OFFCtrl.SetInitialSize((35,-1))

        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_saNightOFF
            ),
           (5,0)
        )
        mySizer_2.Add(saNight_OFFCtrl,(5,1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_saMorningON
            ),
           (5,2)
        )
        mySizer_2.Add(saMorning_ONCtrl,(5,3))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_saEveningOFF
            ),
           (5,4)
        )
        mySizer_2.Add(saEvening_OFFCtrl,(5,5))

        suNight_OFFCtrl = wx.TextCtrl(panel, -1, suNight_OFF)
        suNight_OFFCtrl.SetInitialSize((35,-1))
        suMorning_ONCtrl = wx.TextCtrl(panel, -1, suMorning_ON)
        suMorning_ONCtrl.SetInitialSize((35,-1))
        suEvening_OFFCtrl = wx.TextCtrl(panel, -1, suEvening_OFF)
        suEvening_OFFCtrl.SetInitialSize((35,-1))

        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_suNightOFF
            ),
           (6,0)
        )
        mySizer_2.Add(suNight_OFFCtrl,(6,1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_suMorningON
            ),
           (6,2)
        )
        mySizer_2.Add(suMorning_ONCtrl,(6,3))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_suEveningOFF
            ),
           (6,4)
        )
        mySizer_2.Add(suEvening_OFFCtrl,(6,5))

        vaNight_OFFCtrl = wx.TextCtrl(panel, -1, vaNight_OFF)
        vaNight_OFFCtrl.SetInitialSize((35,-1))
        vaMorning_ONCtrl = wx.TextCtrl(panel, -1, vaMorning_ON)
        vaMorning_ONCtrl.SetInitialSize((35,-1))
        vaEvening_OFFCtrl = wx.TextCtrl(panel, -1, vaEvening_OFF)
        vaEvening_OFFCtrl.SetInitialSize((35,-1))

        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_vaNightOFF
            ),
           (7,0)
        )
        mySizer_2.Add(vaNight_OFFCtrl,(7,1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_vaMorningON
            ),
           (7,2)
        )
        mySizer_2.Add(vaMorning_ONCtrl,(7,3))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_vaEveningOFF
            ),
           (7,4)
        )
        mySizer_2.Add(vaEvening_OFFCtrl,(7,5))

        ehNight_OFFCtrl = wx.TextCtrl(panel, -1, ehNight_OFF)
        ehNight_OFFCtrl.SetInitialSize((35,-1))
        ehMorning_ONCtrl = wx.TextCtrl(panel, -1, ehMorning_ON)
        ehMorning_ONCtrl.SetInitialSize((35,-1))
        ehEvening_OFFCtrl = wx.TextCtrl(panel, -1, ehEvening_OFF)
        ehEvening_OFFCtrl.SetInitialSize((35,-1))

        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_ehNightOFF
            ),
           (8,0)
        )
        mySizer_2.Add(ehNight_OFFCtrl,(8,1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_ehMorningON
            ),
           (8,2)
        )
        mySizer_2.Add(ehMorning_ONCtrl,(8,3))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txt_ehEveningOFF
            ),
           (8,4)
        )
        mySizer_2.Add(ehEvening_OFFCtrl,(8,5))

        iNbrOfBurstsCtrlON = panel.SpinIntCtrl(iNbrOfBurstsON, 1, 10)
        iNbrOfBurstsCtrlON.SetInitialSize((45,-1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtNbrBursts
            ),
           (0,0)
        )
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtON
            ),
           (0,1)
        )
        mySizer_3.Add(iNbrOfBurstsCtrlON,(0,2))

        iNbrOfBurstsCtrlOFF = panel.SpinIntCtrl(iNbrOfBurstsOFF, 1, 10)
        iNbrOfBurstsCtrlOFF.SetInitialSize((45,-1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtNbrBursts
            ),
           (0,3)
        )
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtOFF
            ),
           (0,4)
        )
        mySizer_3.Add(iNbrOfBurstsCtrlOFF,(0,5))

        cmdDelayCtrl = panel.SpinNumCtrl(
            cmdDelay,
            decimalChar = '.',  # by default, use '.' for decimal point
            groupChar = ',',    # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 2,
            min = 0.5,
            max = 5.0,
            increment = 0.5
        )
        cmdDelayCtrl.SetInitialSize((45,-1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtCmdDelay
            ),
           (1,0)
        )
        mySizer_3.Add(cmdDelayCtrl,(1,1))

        iMinOnPeriodCtrl = panel.SpinIntCtrl(iMinOnPeriod, 0, 60)
        iMinOnPeriodCtrl.SetInitialSize((40,-1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMinOnPeriod
            ),
           (1,2)
        )
        mySizer_3.Add(iMinOnPeriodCtrl,(1,3))

        bDoSynchCtrl = wx.CheckBox(panel, -1, "")
        bDoSynchCtrl.SetValue(bDoSynch)
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtDoSynch
            ),
           (2,0)
        )
        mySizer_3.Add(bDoSynchCtrl,(2,1))

        iSynchIntervalCtrl = panel.SpinIntCtrl(iSynchInterval, 6, 600)
        iSynchIntervalCtrl.SetInitialSize((50,-1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtSynchInterval
            ),
           (2,2)
        )
        mySizer_3.Add(iSynchIntervalCtrl,(2,3))

        iOffsetCtrl = panel.SpinIntCtrl(iOffset, -120, 120)
        iOffsetCtrl.SetInitialSize((50,-1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtOffset
            ),
           (3,0)
        )
        mySizer_3.Add(iOffsetCtrl,(3,1))

        iWeatherCtrl = panel.SpinIntCtrl(iWeather, 0, 120)
        iWeatherCtrl.SetInitialSize((50,-1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtWeather
            ),
           (3,2)
        )
        mySizer_3.Add(iWeatherCtrl,(3,3))

        moving_GhostCtrl = wx.CheckBox(panel, -1, "")
        moving_GhostCtrl.SetValue(moving_Ghost)
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost
            ),
           (0,0)
        )
        mySizer_4.Add(moving_GhostCtrl,(0,1))

        moving_Ghost_G_Ctrl = wx.CheckBox(panel, -1, "")
        moving_Ghost_G_Ctrl.SetValue(moving_Ghost_G)
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_G
            ),
           (0,2)
        )
        mySizer_4.Add(moving_Ghost_G_Ctrl,(0,3))

        moving_Ghost_excl_Ctrl = wx.CheckBox(panel, -1, "")
        moving_Ghost_excl_Ctrl.SetValue(moving_Ghost_excl)
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_excl
            ),
           (0,4)
        )
        mySizer_4.Add(moving_Ghost_excl_Ctrl,(0,5))

        moving_Ghost_r1Ctrl = panel.SpinIntCtrl(moving_Ghost_r1, 1, 99)
        moving_Ghost_r1Ctrl.SetInitialSize((45,-1))
        moving_Ghost_r2Ctrl = panel.SpinIntCtrl(moving_Ghost_r2, 1, 99)
        moving_Ghost_r2Ctrl.SetInitialSize((45,-1))
        moving_Ghost_r3Ctrl = panel.SpinIntCtrl(moving_Ghost_r3, 1, 99)
        moving_Ghost_r3Ctrl.SetInitialSize((45,-1))
        moving_Ghost_r4Ctrl = panel.SpinIntCtrl(moving_Ghost_r4, 1, 99)
        moving_Ghost_r4Ctrl.SetInitialSize((45,-1))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_r_1
            ),
           (2,0)
        )
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_ON_min
            ),
           (2,1)
        )
        mySizer_4.Add(moving_Ghost_r1Ctrl,(2,2))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_ON_max
            ),
           (2,3)
        )
        mySizer_4.Add(moving_Ghost_r2Ctrl,(2,4))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_OFF_min
            ),
           (2,5)
        )
        mySizer_4.Add(moving_Ghost_r3Ctrl,(2,6))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_OFF_max
            ),
           (2,7)
        )
        mySizer_4.Add(moving_Ghost_r4Ctrl,(2,8))

        moving_Ghost_r5Ctrl = panel.SpinIntCtrl(moving_Ghost_r5, 1, 99)
        moving_Ghost_r5Ctrl.SetInitialSize((45,-1))
        moving_Ghost_r6Ctrl = panel.SpinIntCtrl(moving_Ghost_r6, 1, 99)
        moving_Ghost_r6Ctrl.SetInitialSize((45,-1))
        moving_Ghost_r7Ctrl = panel.SpinIntCtrl(moving_Ghost_r7, 1, 99)
        moving_Ghost_r7Ctrl.SetInitialSize((45,-1))
        moving_Ghost_r8Ctrl = panel.SpinIntCtrl(moving_Ghost_r8, 1, 99)
        moving_Ghost_r8Ctrl.SetInitialSize((45,-1))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_r_2
            ),
           (3,0)
        )
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_ON_min
            ),
           (3,1)
        )
        mySizer_4.Add(moving_Ghost_r5Ctrl,(3,2))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_ON_max
            ),
           (3,3)
        )
        mySizer_4.Add(moving_Ghost_r6Ctrl,(3,4))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_OFF_min
            ),
           (3,5)
        )
        mySizer_4.Add(moving_Ghost_r7Ctrl,(3,6))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_OFF_max
            ),
           (3,7)
        )
        mySizer_4.Add(moving_Ghost_r8Ctrl,(3,8))

        font = panel.GetFont()
        p = font.GetPointSize()

        font.SetPointSize(9)
        font.SetWeight(wx.BOLD)
        panel.SetFont(font)
        box = wx.StaticBox(panel,-1, self.text.general)
        font.SetPointSize(p)
        font.SetWeight(wx.NORMAL)
        panel.SetFont(font)
        Sizer_1 = wx.StaticBoxSizer(box,wx.VERTICAL)
        Sizer_1.Add(mySizer_1)
        panel.sizer.Add(Sizer_1, 0, flag = wx.EXPAND)

        font.SetPointSize(9)
        font.SetWeight(wx.BOLD)
        panel.SetFont(font)
        box = wx.StaticBox(panel,-1, self.text.daytime)
        font.SetPointSize(p)
        font.SetWeight(wx.NORMAL)
        panel.SetFont(font)
        Sizer_2 = wx.StaticBoxSizer(box,wx.VERTICAL)
        Sizer_2.Add(mySizer_2)
        panel.sizer.Add(Sizer_2, 0, flag = wx.EXPAND)

        font.SetPointSize(9)
        font.SetWeight(wx.BOLD)
        panel.SetFont(font)
        box = wx.StaticBox(panel,-1, self.text.eventrules)
        font.SetPointSize(p)
        font.SetWeight(wx.NORMAL)
        panel.SetFont(font)
        Sizer_3 = wx.StaticBoxSizer(box,wx.VERTICAL)
        Sizer_3.Add(mySizer_3)
        panel.sizer.Add(Sizer_3, 0, flag = wx.EXPAND)

        font.SetPointSize(9)
        font.SetWeight(wx.BOLD)
        panel.SetFont(font)
        box = wx.StaticBox(panel,-1, self.text.mghost)
        font.SetPointSize(p)
        font.SetWeight(wx.NORMAL)
        panel.SetFont(font)
        Sizer_4 = wx.StaticBoxSizer(box,wx.VERTICAL)
        Sizer_4.Add(mySizer_4)
        panel.sizer.Add(Sizer_4, 0, flag = wx.EXPAND)


        def OnButton(event):
            event.Skip()
            dayTimeSettings = []
            suntrackerName = suntrackerNameCtrl.GetValue()
            plugin.lastSuntrackerName = suntrackerName
            indx = plugin.AddSuntrackerName(suntrackerName)
            eventNameOn = eventNameOnCtrl.GetValue()
            plugin.AddEventNameOn(eventNameOn, indx)
            eventNameOff = eventNameOffCtrl.GetValue()
            plugin.AddEventNameOff(eventNameOff, indx)
            iNbrOfBurstsON = iNbrOfBurstsCtrlON.GetValue()
            plugin.AddInbrOfBurstsON(iNbrOfBurstsON, indx)
            iNbrOfBurstsOFF = iNbrOfBurstsCtrlOFF.GetValue()
            plugin.AddInbrOfBurstsOFF(iNbrOfBurstsOFF, indx)
            cmdDelay = cmdDelayCtrl.GetValue()
            plugin.AddCmdDelay(cmdDelay, indx)
            doLogLoops = doLogLoopsCtrl.GetValue()
            plugin.AddDoLogLoops(doLogLoops, indx)
            bDoSynch = bDoSynchCtrl.GetValue()
            plugin.AddBdoSynch(bDoSynch, indx)
            iSynchInterval = iSynchIntervalCtrl.GetValue()
            plugin.AddIsynchInterval(iSynchInterval, indx)
            iOffset = iOffsetCtrl.GetValue()
            plugin.AddiOffset(iOffset, indx)
            iWeather = iWeatherCtrl.GetValue()
            plugin.AddiWeather(iWeather, indx)
            iMinOnPeriod = iMinOnPeriodCtrl.GetValue()
            plugin.AddiMinOnPeriod(iMinOnPeriod, indx)
            moving_Ghost_G = moving_Ghost_G_Ctrl.GetValue()
            plugin.AddMoving_Ghost_G(moving_Ghost_G, indx)
            moving_Ghost = moving_GhostCtrl.GetValue()
            plugin.AddMoving_Ghost(moving_Ghost, indx)
            moving_Ghost_excl = moving_Ghost_excl_Ctrl.GetValue()
            plugin.AddMoving_Ghost_excl(moving_Ghost_excl, indx)

            moving_Ghost_r1 = moving_Ghost_r1Ctrl.GetValue()
            plugin.AddMoving_Ghost_r1(moving_Ghost_r1, indx)
            moving_Ghost_r2 = moving_Ghost_r2Ctrl.GetValue()
            plugin.AddMoving_Ghost_r2(moving_Ghost_r2, indx)
            moving_Ghost_r3 = moving_Ghost_r3Ctrl.GetValue()
            plugin.AddMoving_Ghost_r3(moving_Ghost_r3, indx)
            moving_Ghost_r4 = moving_Ghost_r4Ctrl.GetValue()
            plugin.AddMoving_Ghost_r4(moving_Ghost_r4, indx)
            moving_Ghost_r5 = moving_Ghost_r5Ctrl.GetValue()
            plugin.AddMoving_Ghost_r5(moving_Ghost_r5, indx)
            moving_Ghost_r6 = moving_Ghost_r6Ctrl.GetValue()
            plugin.AddMoving_Ghost_r6(moving_Ghost_r6, indx)
            moving_Ghost_r7 = moving_Ghost_r7Ctrl.GetValue()
            plugin.AddMoving_Ghost_r7(moving_Ghost_r7, indx)
            moving_Ghost_r8 = moving_Ghost_r8Ctrl.GetValue()
            plugin.AddMoving_Ghost_r8(moving_Ghost_r8, indx)

            moNight_OFF = self.timeFormat(moNight_OFFCtrl.GetValue())
            moNight_OFF = self.nightOffFormat(moNight_OFF)
            dayTimeSettings.append(moNight_OFF)
            moMorning_ON = self.timeFormat(moMorning_ONCtrl.GetValue())
            moMorning_ON = self.morningOnFormat(moMorning_ON)
            dayTimeSettings.append(moMorning_ON)
            moEvening_OFF = self.timeFormat(moEvening_OFFCtrl.GetValue())
            moEvening_OFF = self.eveningOffFormat(moEvening_OFF)
            dayTimeSettings.append(moEvening_OFF)

            tuNight_OFF = self.timeFormat(tuNight_OFFCtrl.GetValue())
            tuNight_OFF = self.nightOffFormat(tuNight_OFF)
            dayTimeSettings.append(tuNight_OFF)
            tuMorning_ON = self.timeFormat(tuMorning_ONCtrl.GetValue())
            tuMorning_ON = self.morningOnFormat(tuMorning_ON)
            dayTimeSettings.append(tuMorning_ON)
            tuEvening_OFF = self.timeFormat(tuEvening_OFFCtrl.GetValue())
            tuEvening_OFF = self.eveningOffFormat(tuEvening_OFF)
            dayTimeSettings.append(tuEvening_OFF)

            weNight_OFF = self.timeFormat(weNight_OFFCtrl.GetValue())
            weNight_OFF = self.nightOffFormat(weNight_OFF)
            dayTimeSettings.append(weNight_OFF)
            weMorning_ON = self.timeFormat(weMorning_ONCtrl.GetValue())
            weMorning_ON = self.morningOnFormat(weMorning_ON)
            dayTimeSettings.append(weMorning_ON)
            weEvening_OFF = self.timeFormat(weEvening_OFFCtrl.GetValue())
            weEvening_OFF = self.eveningOffFormat(weEvening_OFF)
            dayTimeSettings.append(weEvening_OFF)

            thNight_OFF = self.timeFormat(thNight_OFFCtrl.GetValue())
            thNight_OFF = self.nightOffFormat(thNight_OFF)
            dayTimeSettings.append(thNight_OFF)
            thMorning_ON = self.timeFormat(thMorning_ONCtrl.GetValue())
            thMorning_ON = self.morningOnFormat(thMorning_ON)
            dayTimeSettings.append(thMorning_ON)
            thEvening_OFF = self.timeFormat(thEvening_OFFCtrl.GetValue())
            thEvening_OFF = self.eveningOffFormat(thEvening_OFF)
            dayTimeSettings.append(thEvening_OFF)

            frNight_OFF = self.timeFormat(frNight_OFFCtrl.GetValue())
            frNight_OFF = self.nightOffFormat(frNight_OFF)
            dayTimeSettings.append(frNight_OFF)
            frMorning_ON = self.timeFormat(frMorning_ONCtrl.GetValue())
            frMorning_ON = self.morningOnFormat(frMorning_ON)
            dayTimeSettings.append(frMorning_ON)
            frEvening_OFF = self.timeFormat(frEvening_OFFCtrl.GetValue())
            frEvening_OFF = self.eveningOffFormat(frEvening_OFF)
            dayTimeSettings.append(frEvening_OFF)

            saNight_OFF = self.timeFormat(saNight_OFFCtrl.GetValue())
            saNight_OFF = self.nightOffFormat(saNight_OFF)
            dayTimeSettings.append(saNight_OFF)
            saMorning_ON = self.timeFormat(saMorning_ONCtrl.GetValue())
            saMorning_ON = self.morningOnFormat(saMorning_ON)
            dayTimeSettings.append(saMorning_ON)
            saEvening_OFF = self.timeFormat(saEvening_OFFCtrl.GetValue())
            saEvening_OFF = self.eveningOffFormat(saEvening_OFF)
            dayTimeSettings.append(saEvening_OFF)

            suNight_OFF = self.timeFormat(suNight_OFFCtrl.GetValue())
            suNight_OFF = self.nightOffFormat(suNight_OFF)
            dayTimeSettings.append(suNight_OFF)
            suMorning_ON = self.timeFormat(suMorning_ONCtrl.GetValue())
            suMorning_ON = self.morningOnFormat(suMorning_ON)
            dayTimeSettings.append(suMorning_ON)
            suEvening_OFF = self.timeFormat(suEvening_OFFCtrl.GetValue())
            suEvening_OFF = self.eveningOffFormat(suEvening_OFF)
            dayTimeSettings.append(suEvening_OFF)

            vaNight_OFF = self.timeFormat(vaNight_OFFCtrl.GetValue())
            vaNight_OFF = self.nightOffFormat(vaNight_OFF)
            dayTimeSettings.append(vaNight_OFF)
            vaMorning_ON = self.timeFormat(vaMorning_ONCtrl.GetValue())
            vaMorning_ON = self.morningOnFormat(vaMorning_ON)
            dayTimeSettings.append(vaMorning_ON)
            vaEvening_OFF = self.timeFormat(vaEvening_OFFCtrl.GetValue())
            vaEvening_OFF = self.eveningOffFormat(vaEvening_OFF)
            dayTimeSettings.append(vaEvening_OFF)

            ehNight_OFF = self.timeFormat(ehNight_OFFCtrl.GetValue())
            ehNight_OFF = self.nightOffFormat(ehNight_OFF)
            dayTimeSettings.append(ehNight_OFF)
            ehMorning_ON = self.timeFormat(ehMorning_ONCtrl.GetValue())
            ehMorning_ON = self.morningOnFormat(ehMorning_ON)
            dayTimeSettings.append(ehMorning_ON)
            ehEvening_OFF = self.timeFormat(ehEvening_OFFCtrl.GetValue())
            ehEvening_OFF = self.eveningOffFormat(ehEvening_OFF)
            dayTimeSettings.append(ehEvening_OFF)

            plugin.AddDayTimeSettings(dayTimeSettings, indx)

            self.plugin.StartSuntracker(
                dayTimeSettings,
                suntrackerName,
                eventNameOn,
                eventNameOff,
                self.plugin.fixedHolidays,
                self.plugin.variableHolidays,
                iNbrOfBurstsON,
                iNbrOfBurstsOFF,
                cmdDelay,
                doLogLoops,
                self.plugin.vacation_m,
                moving_Ghost,
                moving_Ghost_G,
                moving_Ghost_r1,
                moving_Ghost_r2,
                moving_Ghost_r3,
                moving_Ghost_r4,
                moving_Ghost_r5,
                moving_Ghost_r6,
                moving_Ghost_r7,
                moving_Ghost_r8,
                bDoSynch,
                iOffset,
                iWeather,
                iMinOnPeriod,
                self.plugin.myLongitude,
                self.plugin.myLatitude,
                self.plugin.location_id,
                iSynchInterval,
                self.plugin.summerSeasonBegins,
                self.plugin.summerSeasonEnds,
                moving_Ghost_excl,
                self.plugin.unit,
                self.plugin.weatherUpdateRate,
                self.plugin.emptyHouse_m,
                self.plugin.eventPrefix,
                self.plugin.weatherChange
            )

        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnButton)

        while panel.Affirmed():
            dayTimeSettings = []
            suntrackerName = suntrackerNameCtrl.GetValue()
            plugin.lastSuntrackerName = suntrackerName
            indx = plugin.AddSuntrackerName(suntrackerName)
            eventNameOn = eventNameOnCtrl.GetValue()
            plugin.AddEventNameOn(eventNameOn, indx)
            eventNameOff = eventNameOffCtrl.GetValue()
            plugin.AddEventNameOff(eventNameOff, indx)
            iNbrOfBurstsON = iNbrOfBurstsCtrlON.GetValue()
            plugin.AddInbrOfBurstsON(iNbrOfBurstsON, indx)
            iNbrOfBurstsOFF = iNbrOfBurstsCtrlOFF.GetValue()
            plugin.AddInbrOfBurstsOFF(iNbrOfBurstsOFF, indx)
            cmdDelay = cmdDelayCtrl.GetValue()
            plugin.AddCmdDelay(cmdDelay, indx)
            doLogLoops = doLogLoopsCtrl.GetValue()
            plugin.AddDoLogLoops(doLogLoops, indx)
            bDoSynch = bDoSynchCtrl.GetValue()
            plugin.AddBdoSynch(bDoSynch, indx)
            iSynchInterval = iSynchIntervalCtrl.GetValue()
            plugin.AddIsynchInterval(iSynchInterval, indx)
            iOffset = iOffsetCtrl.GetValue()
            plugin.AddiOffset(iOffset, indx)
            iWeather = iWeatherCtrl.GetValue()
            plugin.AddiWeather(iWeather, indx)
            iMinOnPeriod = iMinOnPeriodCtrl.GetValue()
            plugin.AddiMinOnPeriod(iMinOnPeriod, indx)

            fixedHolidays = self.plugin.fixedHolidays
            variableHolidays = self.plugin.variableHolidays
            myLongitude = str(self.plugin.myLongitude)
            myLatitude = str(self.plugin.myLatitude)
            vacation_m = self.plugin.vacation_m
            emptyHouse_m = self.plugin.emptyHouse_m
            location_id = self.plugin.location_id
            summerSeasonBegins = self.plugin.summerSeasonBegins
            summerSeasonEnds = self.plugin.summerSeasonEnds
            unit = self.plugin.unit
            weatherUpdateRate = self.plugin.weatherUpdateRate

            moving_Ghost_G = moving_Ghost_G_Ctrl.GetValue()
            plugin.AddMoving_Ghost_G(moving_Ghost_G, indx)
            moving_Ghost = moving_GhostCtrl.GetValue()
            plugin.AddMoving_Ghost(moving_Ghost, indx)
            moving_Ghost_excl = moving_Ghost_excl_Ctrl.GetValue()
            plugin.AddMoving_Ghost_excl(moving_Ghost_excl, indx)

            moving_Ghost_r1 = moving_Ghost_r1Ctrl.GetValue()
            plugin.AddMoving_Ghost_r1(moving_Ghost_r1, indx)
            moving_Ghost_r2 = moving_Ghost_r2Ctrl.GetValue()
            plugin.AddMoving_Ghost_r2(moving_Ghost_r2, indx)
            moving_Ghost_r3 = moving_Ghost_r3Ctrl.GetValue()
            plugin.AddMoving_Ghost_r3(moving_Ghost_r3, indx)
            moving_Ghost_r4 = moving_Ghost_r4Ctrl.GetValue()
            plugin.AddMoving_Ghost_r4(moving_Ghost_r4, indx)
            moving_Ghost_r5 = moving_Ghost_r5Ctrl.GetValue()
            plugin.AddMoving_Ghost_r5(moving_Ghost_r5, indx)
            moving_Ghost_r6 = moving_Ghost_r6Ctrl.GetValue()
            plugin.AddMoving_Ghost_r6(moving_Ghost_r6, indx)
            moving_Ghost_r7 = moving_Ghost_r7Ctrl.GetValue()
            plugin.AddMoving_Ghost_r7(moving_Ghost_r7, indx)
            moving_Ghost_r8 = moving_Ghost_r8Ctrl.GetValue()
            plugin.AddMoving_Ghost_r8(moving_Ghost_r8, indx)

            moNight_OFF = self.timeFormat(moNight_OFFCtrl.GetValue())
            moNight_OFF = self.nightOffFormat(moNight_OFF)
            dayTimeSettings.append(moNight_OFF)
            moMorning_ON = self.timeFormat(moMorning_ONCtrl.GetValue())
            moMorning_ON = self.morningOnFormat(moMorning_ON)
            dayTimeSettings.append(moMorning_ON)
            moEvening_OFF = self.timeFormat(moEvening_OFFCtrl.GetValue())
            moEvening_OFF = self.eveningOffFormat(moEvening_OFF)
            dayTimeSettings.append(moEvening_OFF)

            tuNight_OFF = self.timeFormat(tuNight_OFFCtrl.GetValue())
            tuNight_OFF = self.nightOffFormat(tuNight_OFF)
            dayTimeSettings.append(tuNight_OFF)
            tuMorning_ON = self.timeFormat(tuMorning_ONCtrl.GetValue())
            tuMorning_ON = self.morningOnFormat(tuMorning_ON)
            dayTimeSettings.append(tuMorning_ON)
            tuEvening_OFF = self.timeFormat(tuEvening_OFFCtrl.GetValue())
            tuEvening_OFF = self.eveningOffFormat(tuEvening_OFF)
            dayTimeSettings.append(tuEvening_OFF)

            weNight_OFF = self.timeFormat(weNight_OFFCtrl.GetValue())
            weNight_OFF = self.nightOffFormat(weNight_OFF)
            dayTimeSettings.append(weNight_OFF)
            weMorning_ON = self.timeFormat(weMorning_ONCtrl.GetValue())
            weMorning_ON = self.morningOnFormat(weMorning_ON)
            dayTimeSettings.append(weMorning_ON)
            weEvening_OFF = self.timeFormat(weEvening_OFFCtrl.GetValue())
            weEvening_OFF = self.eveningOffFormat(weEvening_OFF)
            dayTimeSettings.append(weEvening_OFF)

            thNight_OFF = self.timeFormat(thNight_OFFCtrl.GetValue())
            thNight_OFF = self.nightOffFormat(thNight_OFF)
            dayTimeSettings.append(thNight_OFF)
            thMorning_ON = self.timeFormat(thMorning_ONCtrl.GetValue())
            thMorning_ON = self.morningOnFormat(thMorning_ON)
            dayTimeSettings.append(thMorning_ON)
            thEvening_OFF = self.timeFormat(thEvening_OFFCtrl.GetValue())
            thEvening_OFF = self.eveningOffFormat(thEvening_OFF)
            dayTimeSettings.append(thEvening_OFF)

            frNight_OFF = self.timeFormat(frNight_OFFCtrl.GetValue())
            frNight_OFF = self.nightOffFormat(frNight_OFF)
            dayTimeSettings.append(frNight_OFF)
            frMorning_ON = self.timeFormat(frMorning_ONCtrl.GetValue())
            frMorning_ON = self.morningOnFormat(frMorning_ON)
            dayTimeSettings.append(frMorning_ON)
            frEvening_OFF = self.timeFormat(frEvening_OFFCtrl.GetValue())
            frEvening_OFF = self.eveningOffFormat(frEvening_OFF)
            dayTimeSettings.append(frEvening_OFF)

            saNight_OFF = self.timeFormat(saNight_OFFCtrl.GetValue())
            saNight_OFF = self.nightOffFormat(saNight_OFF)
            dayTimeSettings.append(saNight_OFF)
            saMorning_ON = self.timeFormat(saMorning_ONCtrl.GetValue())
            saMorning_ON = self.morningOnFormat(saMorning_ON)
            dayTimeSettings.append(saMorning_ON)
            saEvening_OFF = self.timeFormat(saEvening_OFFCtrl.GetValue())
            saEvening_OFF = self.eveningOffFormat(saEvening_OFF)
            dayTimeSettings.append(saEvening_OFF)

            suNight_OFF = self.timeFormat(suNight_OFFCtrl.GetValue())
            suNight_OFF = self.nightOffFormat(suNight_OFF)
            dayTimeSettings.append(suNight_OFF)
            suMorning_ON = self.timeFormat(suMorning_ONCtrl.GetValue())
            suMorning_ON = self.morningOnFormat(suMorning_ON)
            dayTimeSettings.append(suMorning_ON)
            suEvening_OFF = self.timeFormat(suEvening_OFFCtrl.GetValue())
            suEvening_OFF = self.eveningOffFormat(suEvening_OFF)
            dayTimeSettings.append(suEvening_OFF)

            vaNight_OFF = self.timeFormat(vaNight_OFFCtrl.GetValue())
            vaNight_OFF = self.nightOffFormat(vaNight_OFF)
            dayTimeSettings.append(vaNight_OFF)
            vaMorning_ON = self.timeFormat(vaMorning_ONCtrl.GetValue())
            vaMorning_ON = self.morningOnFormat(vaMorning_ON)
            dayTimeSettings.append(vaMorning_ON)
            vaEvening_OFF = self.timeFormat(vaEvening_OFFCtrl.GetValue())
            vaEvening_OFF = self.eveningOffFormat(vaEvening_OFF)
            dayTimeSettings.append(vaEvening_OFF)

            ehNight_OFF = self.timeFormat(ehNight_OFFCtrl.GetValue())
            ehNight_OFF = self.nightOffFormat(ehNight_OFF)
            dayTimeSettings.append(ehNight_OFF)
            ehMorning_ON = self.timeFormat(ehMorning_ONCtrl.GetValue())
            ehMorning_ON = self.morningOnFormat(ehMorning_ON)
            dayTimeSettings.append(ehMorning_ON)
            ehEvening_OFF = self.timeFormat(ehEvening_OFFCtrl.GetValue())
            ehEvening_OFF = self.eveningOffFormat(ehEvening_OFF)
            dayTimeSettings.append(ehEvening_OFF)

            plugin.AddDayTimeSettings(dayTimeSettings, indx)

            panel.SetResult(
                dayTimeSettings,
                suntrackerName,
                eventNameOn,
                eventNameOff,
                moNight_OFF,
                moMorning_ON,
                moEvening_OFF,
                tuNight_OFF,
                tuMorning_ON,
                tuEvening_OFF,
                weNight_OFF,
                weMorning_ON,
                weEvening_OFF,
                thNight_OFF,
                thMorning_ON,
                thEvening_OFF,
                frNight_OFF,
                frMorning_ON,
                frEvening_OFF,
                saNight_OFF,
                saMorning_ON,
                saEvening_OFF,
                suNight_OFF,
                suMorning_ON,
                suEvening_OFF,
                vaNight_OFF,
                vaMorning_ON,
                vaEvening_OFF,
                fixedHolidays,
                variableHolidays,
                iNbrOfBurstsON,
                iNbrOfBurstsOFF,
                cmdDelay,
                doLogLoops,
                vacation_m,
                moving_Ghost,
                moving_Ghost_G,
                moving_Ghost_r1,
                moving_Ghost_r2,
                moving_Ghost_r3,
                moving_Ghost_r4,
                moving_Ghost_r5,
                moving_Ghost_r6,
                moving_Ghost_r7,
                moving_Ghost_r8,
                bDoSynch,
                iOffset,
                iWeather,
                iMinOnPeriod,
                myLongitude,
                myLatitude,
                location_id,
                iSynchInterval,
                summerSeasonBegins,
                summerSeasonEnds,
                moving_Ghost_excl,
                unit,
                weatherUpdateRate,
                ehNight_OFF,
                ehMorning_ON,
                ehEvening_OFF,
                emptyHouse_m,
                eventPrefix,
                weatherChange
            )



class SetMovingGhostON(eg.ActionClass):
    name = "MovingGhost ON"
    description = "Action to set the MovingGhost flag TRUE"

    def __call__(self):
        if not self.plugin.initsynch:
            if not ConfigData.movingGhost:
                print self.text.txtMG_ON
            ConfigData.movingGhost = True
        else:
            print self.text.txtInit



class SetMovingGhostOFF(eg.ActionClass):
    name = "MovingGhost OFF"
    description = "Action to set the MovingGhost flag FALSE"

    def __call__(self):
        if not self.plugin.initsynch:
            if ConfigData.movingGhost:
                print self.text.txtMG_OFF
            ConfigData.movingGhost = False
        else:
            print self.text.txtInit



class GetSunState(eg.ActionClass):
    name = "GetSunState"
    description = "Action to check if sun is up or down"

    def __call__(self):
        if not self.plugin.initsynch:
            return self.plugin.sunIsUp
        else:
            print self.text.txtInit
            return False



class GetSunStateWithTimeStamp(eg.ActionClass):
    name = "GetSunStateWithTimeStamp"
    description = "Action to check if sun is up or down with time stamp"

    def __call__(self):
        if not self.plugin.initsynch:
            if self.plugin.sunIsUp:
                return 'Up|'+str(self.plugin.csSR)
            else:
                return 'Down|'+str(self.plugin.csSS)
        else:
            print self.text.txtInit
            return "Undefined"



class GetTimeFor_SunSet_SunRise(eg.ActionClass):
    name = "GetTimeFor_SunSet_SunRise"
    description = ("Action to retrieve current time stamps for todays "+
                  " Sunset and Sunrise"
    )

    def __call__(self):
        if not self.plugin.initsynch:
            return 'Up|'+str(self.plugin.csSR), 'Down|'+str(self.plugin.csSS)
        else:
            print self.text.txtInit
            return "Undefined"



class GetWeatherCondition(eg.ActionClass):
    name = "GetWeatherCondition"
    description = "Action to check the current weather condition"

    def __call__(self):
        if not self.plugin.initsynch:
            return self.plugin.currCondition
        else:
            print self.text.txtInit
            return "Undefined"



class GetSunStatusWeatherCompensated(eg.ActionClass):
    name = "Sunstate with weather compensation"
    description = (
        "This action can be used to request weather compensated sun status. "+
        "It is useful when determining if lights shall be turned on and off"+
        " during various weather conditions like sunny, cloudy, foggy etc. "+
        "The split of weather conditions in the separate python file"+
        " 'weather_condition.py' into the various sections defines"+
        " how the calculation will be executed for various conditions. "+
        "If the weather condition is one of those in section"+
        " 'weather_conditions_dark' the full time will be applied. "+
        "If the weather is fair, clear, sunny or something else in"+
        " the section 'weather_conditions_bright' no time will be added or subtracted. "+
        "Finally, the section for 'weather_conditions_half_bright' will be used"+
        " to divide the time compensation into half. "
    )

    def __call__(
        self,
        iWeather
    ):
        sunIsUpW = False
        if not self.plugin.initsynch:
            self.iWeather = iWeather
            currCondition = "Undefined"
            sunIsUpW = True

            # Set the conditions depending on the weather
            trigTimeSR = self.plugin.GetOffsetTimeSR(0)
            trigTimeSS = self.plugin.GetOffsetTimeSS(0)

            if self.iWeather <> 0:
                currCondition = self.plugin.currCondition

                # Adjust the sunrise/sunset trig times to weather condition
                timeCompensation = 0

                currCondition, timeCompensation, trigTimeSS, trigTimeSR  = (
                        self.plugin.CalcWeatherCompensation(
                                currCondition,
                                timeCompensation,
                                self.iWeather,
                                0
                        )
                )

            # Set the weather compensated flag for sun status
            if(
                trigTimeSS >= self.plugin.csSS
                or trigTimeSS < self.plugin.csSR
            ):
                sunIsUpW = False

            if(
                trigTimeSR < self.plugin.csSR
                or trigTimeSR >= self.plugin.csSS
            ):
                sunIsUpW = False

        else:
            print self.text.txtInit

        return sunIsUpW


    def Configure(
        self,
        iWeather = 0
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_0 = wx.GridBagSizer(5, 5)

        iWeatherCtrl = panel.SpinIntCtrl(iWeather, 1, 120)
        iWeatherCtrl.SetInitialSize((50,-1))
        mySizer_0.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtWeather
            ),
           (0,0)
        )

        mySizer_0.Add(iWeatherCtrl,(0,1))
        panel.sizer.Add(mySizer_0, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            iWeather = iWeatherCtrl.GetValue()

            panel.SetResult(
                iWeather
            )



class IsSunDown(eg.ActionClass):
    name = "Check if Sun will be down in X minutes"
    description = (
        "This plugin action creates a ''virtual new sunset time'' based on an "+
        "offset entered in the first drop down field. This can be 120 minutes "+
        "prior to and 120 minutes after the ''true sunset time''. "+
        "Furthermore, this new ''virual sunset time'' can be further modified "+
        "if the Weather compensation factor is used. "+
        "Although the maximum amount of modification time to be applied "+
        "is entered by the user, the actual amount of this additional time "+
        "factor is calculated by the plugin automatically based on actual "+
        "weather conditions obtained from the internet. "+
        "Finally, the result of this action block returns True if, at the "+
        "time this action block is executed, the Sun would have been down "+
        "according to the calculated ''virtual sunset time''. "+
        "Note: the true (unmodified) sunset time can be obtained by executing "+
        "this action block and examining the payload of the event in the log. "+
        "For further information and help, please visit the forum thread for "+
        "the SunTracker plugin. "
    )

    def CalcNbrOfMinutes(self, s):
        iHour = int(s[0:2])
        iMin = int(s[2:4])
        iTotMin = iHour*60 + iMin
        return(iTotMin)


    def GetVirtualSunset(self, iO):
        now = datetime.datetime.now()
        diff = datetime.timedelta(minutes=abs(iO))
        if iO<0:
            corr = now - diff
        else:
            corr = now + diff
        s = corr.strftime("%H%M")
        return(s)


    def __call__(
        self,
        iTimeAhead,
        iWeather
    ):
        sunIsDown = False
        if not self.plugin.initsynch:
            self.iTimeAhead = iTimeAhead
            self.iWeather = iWeather
            currCondition = "Undefined"
            currTimeCompensated = 0
            timeCompensation = 0
            notUsed = 0

            # Check conditions depending on the weather and
            # adjust actual time for comparison use
            currCondition = self.plugin.currCondition
            currCondition, timeCompensation, currTimeCompensated, notUsed = (
                    self.plugin.CalcWeatherCompensation(
                            currCondition,
                            timeCompensation,
                            self.iWeather,
                            self.iTimeAhead
                    )
            )

            # Expected Sunset time of today is given by variable self.plugin.csSS
            # Convert to minutes
            ssMins = self.CalcNbrOfMinutes(self.plugin.csSS)
            crMins = self.CalcNbrOfMinutes(currTimeCompensated)
            virtualSS = self.GetVirtualSunset(ssMins - crMins)

            # Set the flag for the virtual sun status
            if(ssMins - crMins <= 0):
                sunIsDown = True
            else:
                sunIsDown = False

            # Do some additional checks
            now = datetime.datetime.now().strftime("%H%M")
            # If time is more than virtual sunset, set flag true
            if now > virtualSS:
                sunIsDown = True
            # If time is less than sunrise, set flag true
            if now < self.plugin.csSR:
                sunIsDown = True

            pLoad = (
                str(self.iTimeAhead)+'|'+str(self.iWeather)+'|'+currCondition+'|'+
                'Real Sunset expected:'+'|'+self.plugin.csSS+'|'+
                'Virtual Sunset expected:'+'|'+virtualSS+'|'+
                'Minutes to Virtual Sunset:'+'|'+str(ssMins - crMins)+'|'+
                'Minutes adjusted:'+'|'+str(timeCompensation)+'|'+
                'IsSunDown:'+'|'+str(sunIsDown)
            )
            eg.TriggerEvent(
                "IsSunDown." + str(sunIsDown),
                pLoad,
                self.plugin.eventPrefix
            )



        else:
            print self.text.txtInit

        return sunIsDown


    def Configure(
        self,
        iTimeAhead = -30,
        iWeather = 0
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_0 = wx.GridBagSizer(5, 5)
        mySizer_1 = wx.GridBagSizer(5, 5)

        iTimeAheadCtrl = panel.SpinIntCtrl(iTimeAhead, -120, 120)
        iTimeAheadCtrl.SetInitialSize((50,-1))
        mySizer_0.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtOffset
            ),
           (0,0)
        )
        mySizer_0.Add(iTimeAheadCtrl,(0,1))
        panel.sizer.Add(mySizer_0, 0, flag = wx.EXPAND)

        iWeatherCtrl = panel.SpinIntCtrl(iWeather, 0, 120)
        iWeatherCtrl.SetInitialSize((50,-1))
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtWeather
            ),
           (1,0)
        )
        mySizer_1.Add(iWeatherCtrl,(1,1))
        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            iTimeAhead = iTimeAheadCtrl.GetValue()
            iWeather = iWeatherCtrl.GetValue()

            panel.SetResult(
                iTimeAhead,
                iWeather
            )



class InsideRangeWeatherCompensated(eg.ActionClass):
    name = ("Check if time now is inside calculated virtual range including "+
           " a weather compensated offset"
    )
    description = (
        "This plugin action creates a ''virtual start and end time range'' based "+
        " on the selected twilight types and an additional weather compensated offset "+
        " entered in the drop down fields. "+
        "The selected twilight types for start and end time can be freely "+
        " selected from the list. "+
        "The offset can be 120 minutes prior to and 120 minutes after the "+
        " ''true times'' also depending on actual weather condition. "+
        "The result of this action returns True if, at the actual time "+
        " when executed, the time is between the calculated "+
        " virtual range. If outside, it will return False. "+
        "In addition it is selectable if the current running macro should stop or "+
        " continue when the returned result is True or False. "+
        "For further information and help, please visit the forum thread for "+
        " the SunTracker plugin. "
    )
    iTimeAhead = 0

    def CalcNbrOfMinutes(self, s):
        iHour = int(s[0:2])
        iMin = int(s[2:4])
        iTotMin = iHour*60 + iMin
        return(iTotMin)


    def GetVirtualTime(self, iO):
        s = str(datetime.timedelta(minutes=iO))
        s = s.split(':')
        Hour = str(s[0])
        if len(Hour)<2:
            Hour = '0'+Hour
        Minute = str(s[1])
        if len(Minute)<2:
            Minute = '0'+Minute
        return(Hour+Minute)


    def __call__(
        self,
        rangeName,
        iOffset,
        tlStartType,
        tlEndType,
        stopMacroOnTrue,
        stopMacroOnFalse,
        iWeather
    ):
        isInsideRange = False
        if not self.plugin.initsynch:
            list = [
                'Astronomical Dawn',
                'Nautical Dawn',
                'Civil Dawn',
                'Sunrise',
                'Sunset',
                'Civil Dusk',
                'Nautical Dusk',
                'Astronomical Dusk',
            ]

            if (
                iOffset < -120 or
                iOffset > 120 or
                iWeather < 0 or
                iWeather > 120 or
                tlStartType not in list or
                tlEndType not in list
            ):
                print "Wrong parameters"
                return False

            self.iOffset = iOffset
            self.iWeather = iWeather

            try:
                currCondition = self.plugin.currCondition
            except:
                currCondition = "Undefined"
            try:
                currCondition, timeCompensation, tSS, tSR  = (
                        self.plugin.CalcWeatherCompensation(
                                currCondition,
                                0,
                                self.iWeather,
                                self.iOffset
                        )
                )
            except:
                timeCompensation = 0

            iTimeAhead = timeCompensation

            if tlStartType == list[0]:
                startMins = self.CalcNbrOfMinutes(self.plugin.aDawn)
                virtualStart = self.GetVirtualTime(startMins-iTimeAhead)
            elif tlStartType == list[1]:
                startMins = self.CalcNbrOfMinutes(self.plugin.nDawn)
                virtualStart = self.GetVirtualTime(startMins-iTimeAhead)
            elif tlStartType == list[2]:
                startMins = self.CalcNbrOfMinutes(self.plugin.cDawn)
                virtualStart = self.GetVirtualTime(startMins-iTimeAhead)
            elif tlStartType == list[3]:
                startMins = self.CalcNbrOfMinutes(self.plugin.csSR)
                virtualStart = self.GetVirtualTime(startMins-iTimeAhead)
            elif tlStartType == list[4]:
                startMins = self.CalcNbrOfMinutes(self.plugin.csSS)
                virtualStart = self.GetVirtualTime(startMins-iTimeAhead)
            elif tlStartType == list[5]:
                startMins = self.CalcNbrOfMinutes(self.plugin.cDusk)
                virtualStart = self.GetVirtualTime(startMins-iTimeAhead)
            elif tlStartType == list[6]:
                startMins = self.CalcNbrOfMinutes(self.plugin.nDusk)
                virtualStart = self.GetVirtualTime(startMins-iTimeAhead)
            elif tlStartType == list[7]:
                startMins = self.CalcNbrOfMinutes(self.plugin.aDusk)
                virtualStart = self.GetVirtualTime(startMins-iTimeAhead)

            if tlEndType == list[0]:
                endMins = self.CalcNbrOfMinutes(self.plugin.aDawn)
                virtualEnd = self.GetVirtualTime(endMins+iTimeAhead)
            elif tlEndType == list[1]:
                endMins = self.CalcNbrOfMinutes(self.plugin.nDawn)
                virtualEnd = self.GetVirtualTime(endMins+iTimeAhead)
            elif tlEndType == list[2]:
                endMins = self.CalcNbrOfMinutes(self.plugin.cDawn)
                virtualEnd = self.GetVirtualTime(endMins+iTimeAhead)
            elif tlEndType == list[3]:
                endMins = self.CalcNbrOfMinutes(self.plugin.csSR)
                virtualEnd = self.GetVirtualTime(endMins+iTimeAhead)
            elif tlEndType == list[4]:
                endMins = self.CalcNbrOfMinutes(self.plugin.csSS)
                virtualEnd = self.GetVirtualTime(endMins+iTimeAhead)
            elif tlEndType == list[5]:
                endMins = self.CalcNbrOfMinutes(self.plugin.cDusk)
                virtualEnd = self.GetVirtualTime(endMins+iTimeAhead)
            elif tlEndType == list[6]:
                endMins = self.CalcNbrOfMinutes(self.plugin.nDusk)
                virtualEnd = self.GetVirtualTime(endMins+iTimeAhead)
            elif tlEndType == list[7]:
                endMins = self.CalcNbrOfMinutes(self.plugin.aDusk)
                virtualEnd = self.GetVirtualTime(endMins+iTimeAhead)

            # Check if time is between virtual start and virtual end,
            # control macro execution
            now = datetime.datetime.now().strftime("%H%M")

            if virtualStart <= virtualEnd:
                if now >= virtualStart and now <= virtualEnd:
                    isInsideRange = True
                if virtualStart == virtualEnd:
                    isInsideRange = True
            if virtualStart > virtualEnd:
                if now > virtualStart or now < virtualEnd:
                    isInsideRange = True

            if isInsideRange and stopMacroOnTrue:
                eg.StopMacro()

            if not isInsideRange and stopMacroOnFalse:
                eg.StopMacro()

        else:
            print self.text.txtInit

        return isInsideRange


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        rangeName = 'Give the range a descriptive name',
        iOffset = -60,
        tlStartType = '',
        tlEndType = '',
        stopMacroOnTrue = True,
        stopMacroOnFalse = False,
        iWeather = 30
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_0 = wx.GridBagSizer(5, 5)
        mySizer_1 = wx.GridBagSizer(5, 5)

        list = [
            'Astronomical Dawn',
            'Nautical Dawn',
            'Civil Dawn',
            'Sunrise',
            'Sunset',
            'Civil Dusk',
            'Nautical Dusk',
            'Astronomical Dusk',
        ]

        rangeNameCtrl = wx.TextCtrl(panel, -1, rangeName)
        rangeNameCtrl.SetInitialSize((150,-1))
        mySizer_0.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.rangeName
            ),
           (0,0)
        )
        mySizer_0.Add(rangeNameCtrl,(0,1))

        iOffsetCtrl = panel.SpinIntCtrl(iOffset, -120, 120)
        iOffsetCtrl.SetInitialSize((50,-1))
        mySizer_0.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtOffset
            ),
           (1,0)
        )
        mySizer_0.Add(iOffsetCtrl,(1,1))

        iWeatherCtrl = panel.SpinIntCtrl(iWeather, 0, 120)
        iWeatherCtrl.SetInitialSize((50,-1))
        mySizer_0.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtWeather
            ),
           (2,0)
        )
        mySizer_0.Add(iWeatherCtrl,(2,1))

        tlStartTypeCtrl = wx.Choice(parent=panel, pos=(10,10))
        tlStartTypeCtrl.AppendItems(strings=list)
        if list.count(tlStartType)==0:
            tlStartTypeCtrl.Select(n=0)
        else:
            tlStartTypeCtrl.SetSelection(int(list.index(tlStartType)))
        tlStartTypeCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        sBtxt = wx.StaticText(panel, -1, self.text.tlStartType)
        mySizer_1.Add(sBtxt,(1,0))
        mySizer_1.Add(tlStartTypeCtrl,(1,1))

        tlEndTypeCtrl = wx.Choice(parent=panel, pos=(10,10))
        tlEndTypeCtrl.AppendItems(strings=list)
        if list.count(tlEndType)==0:
            tlEndTypeCtrl.Select(n=0)
        else:
            tlEndTypeCtrl.SetSelection(int(list.index(tlEndType)))
        tlEndTypeCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        sBtxt = wx.StaticText(panel, -1, self.text.tlEndType)
        mySizer_1.Add(sBtxt,(2,0))
        mySizer_1.Add(tlEndTypeCtrl,(2,1))

        stopMacroOnTrueCtrl = wx.CheckBox(panel, -1, "")
        stopMacroOnTrueCtrl.SetValue(stopMacroOnTrue)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.stopMacroOnTrue
            ),
           (3,0)
        )
        mySizer_1.Add(stopMacroOnTrueCtrl,(3,1))

        stopMacroOnFalseCtrl = wx.CheckBox(panel, -1, "")
        stopMacroOnFalseCtrl.SetValue(stopMacroOnFalse)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.stopMacroOnFalse
            ),
           (4,0)
        )
        mySizer_1.Add(stopMacroOnFalseCtrl,(4,1))

        panel.sizer.Add(mySizer_0, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            rangeName = rangeNameCtrl.GetValue()
            iOffset = iOffsetCtrl.GetValue()
            iWeather = iWeatherCtrl.GetValue()
            tlStartType = tlStartTypeCtrl.GetStringSelection()
            tlEndType = tlEndTypeCtrl.GetStringSelection()
            stopMacroOnTrue = stopMacroOnTrueCtrl.GetValue()
            stopMacroOnFalse = stopMacroOnFalseCtrl.GetValue()

            panel.SetResult(
                rangeName,
                iOffset,
                tlStartType,
                tlEndType,
                stopMacroOnTrue,
                stopMacroOnFalse,
                iWeather
            )



class InsideRange(eg.ActionClass):
    name = "Check if time now is inside calculated virtual range"
    description = (
        "This plugin action creates a ''virtual start and end time range'' based "+
        "on the selected twilight types and an additional offset entered in the drop "+
        "down fields."+
        "The selected twilight types for start and end time can be freely "+
        "selected from the list. "+
        "The offset can be 120 minutes prior to and 120 minutes after the "+
        "''true times''. "+
        "The result of this action returns True if, at the actual time "+
        "when executed, the time is between the calculated "+
        "virtual range. If outside, it will return False. "+
        "In addition it is selectable if the current running macro should stop or "+
        "continue when the returned result is True or False. "+
        "For further information and help, please visit the forum thread for "+
        "the SunTracker plugin. "
    )

    def CalcNbrOfMinutes(self, s):
        iHour = int(s[0:2])
        iMin = int(s[2:4])
        iTotMin = iHour*60 + iMin
        return(iTotMin)


    def GetVirtualTime(self, iO):
        s = str(datetime.timedelta(minutes=iO))
        s = s.split(':')
        Hour = str(s[0])
        if len(Hour)<2:
            Hour = '0'+Hour
        Minute = str(s[1])
        if len(Minute)<2:
            Minute = '0'+Minute
        return(Hour+Minute)


    def __call__(
        self,
        rangeName,
        iTimeAhead,
        tlStartType,
        tlEndType,
        stopMacroOnTrue,
        stopMacroOnFalse
    ):
        isInsideRange = False
        if not self.plugin.initsynch:
            list = [
                'Astronomical Dawn',
                'Nautical Dawn',
                'Civil Dawn',
                'Sunrise',
                'Sunset',
                'Civil Dusk',
                'Nautical Dusk',
                'Astronomical Dusk',
            ]

            if (
                iTimeAhead < -120 or
                iTimeAhead > 120 or
                tlStartType not in list or
                tlEndType not in list
            ):
                print "Wrong parameters"
                return False

            self.iTimeAhead = iTimeAhead

            if tlStartType == list[0]:
                startMins = self.CalcNbrOfMinutes(self.plugin.aDawn)
                virtualStart = self.GetVirtualTime(startMins-self.iTimeAhead)
            elif tlStartType == list[1]:
                startMins = self.CalcNbrOfMinutes(self.plugin.nDawn)
                virtualStart = self.GetVirtualTime(startMins-self.iTimeAhead)
            elif tlStartType == list[2]:
                startMins = self.CalcNbrOfMinutes(self.plugin.cDawn)
                virtualStart = self.GetVirtualTime(startMins-self.iTimeAhead)
            elif tlStartType == list[3]:
                startMins = self.CalcNbrOfMinutes(self.plugin.csSR)
                virtualStart = self.GetVirtualTime(startMins-self.iTimeAhead)
            elif tlStartType == list[4]:
                startMins = self.CalcNbrOfMinutes(self.plugin.csSS)
                virtualStart = self.GetVirtualTime(startMins-self.iTimeAhead)
            elif tlStartType == list[5]:
                startMins = self.CalcNbrOfMinutes(self.plugin.cDusk)
                virtualStart = self.GetVirtualTime(startMins-self.iTimeAhead)
            elif tlStartType == list[6]:
                startMins = self.CalcNbrOfMinutes(self.plugin.nDusk)
                virtualStart = self.GetVirtualTime(startMins-self.iTimeAhead)
            elif tlStartType == list[7]:
                startMins = self.CalcNbrOfMinutes(self.plugin.aDusk)
                virtualStart = self.GetVirtualTime(startMins-self.iTimeAhead)

            if tlEndType == list[0]:
                endMins = self.CalcNbrOfMinutes(self.plugin.aDawn)
                virtualEnd = self.GetVirtualTime(endMins+self.iTimeAhead)
            elif tlEndType == list[1]:
                endMins = self.CalcNbrOfMinutes(self.plugin.nDawn)
                virtualEnd = self.GetVirtualTime(endMins+self.iTimeAhead)
            elif tlEndType == list[2]:
                endMins = self.CalcNbrOfMinutes(self.plugin.cDawn)
                virtualEnd = self.GetVirtualTime(endMins+self.iTimeAhead)
            elif tlEndType == list[3]:
                endMins = self.CalcNbrOfMinutes(self.plugin.csSR)
                virtualEnd = self.GetVirtualTime(endMins+self.iTimeAhead)
            elif tlEndType == list[4]:
                endMins = self.CalcNbrOfMinutes(self.plugin.csSS)
                virtualEnd = self.GetVirtualTime(endMins+self.iTimeAhead)
            elif tlEndType == list[5]:
                endMins = self.CalcNbrOfMinutes(self.plugin.cDusk)
                virtualEnd = self.GetVirtualTime(endMins+self.iTimeAhead)
            elif tlEndType == list[6]:
                endMins = self.CalcNbrOfMinutes(self.plugin.nDusk)
                virtualEnd = self.GetVirtualTime(endMins+self.iTimeAhead)
            elif tlEndType == list[7]:
                endMins = self.CalcNbrOfMinutes(self.plugin.aDusk)
                virtualEnd = self.GetVirtualTime(endMins+self.iTimeAhead)

            # Check if time is between virtual start and virtual end,
            # control macro execution
            now = datetime.datetime.now().strftime("%H%M")

            if virtualStart <= virtualEnd:
                if now >= virtualStart and now <= virtualEnd:
                    isInsideRange = True
                if virtualStart == virtualEnd:
                    isInsideRange = True
            if virtualStart > virtualEnd:
                if now > virtualStart or now < virtualEnd:
                    isInsideRange = True

            if isInsideRange and stopMacroOnTrue:
                eg.StopMacro()

            if not isInsideRange and stopMacroOnFalse:
                eg.StopMacro()

        else:
            print self.text.txtInit

        return isInsideRange


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        rangeName = 'Give the range a descriptive name',
        iTimeAhead = -30,
        tlStartType = '',
        tlEndType = '',
        stopMacroOnTrue = True,
        stopMacroOnFalse = False
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_0 = wx.GridBagSizer(5, 5)
        mySizer_1 = wx.GridBagSizer(5, 5)

        list = [
            'Astronomical Dawn',
            'Nautical Dawn',
            'Civil Dawn',
            'Sunrise',
            'Sunset',
            'Civil Dusk',
            'Nautical Dusk',
            'Astronomical Dusk',
        ]

        rangeNameCtrl = wx.TextCtrl(panel, -1, rangeName)
        rangeNameCtrl.SetInitialSize((150,-1))
        mySizer_0.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.rangeName
            ),
           (0,0)
        )
        mySizer_0.Add(rangeNameCtrl,(0,1))

        iTimeAheadCtrl = panel.SpinIntCtrl(iTimeAhead, -120, 120)
        iTimeAheadCtrl.SetInitialSize((50,-1))
        mySizer_0.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtOffset
            ),
           (1,0)
        )
        mySizer_0.Add(iTimeAheadCtrl,(1,1))

        tlStartTypeCtrl = wx.Choice(parent=panel, pos=(10,10))
        tlStartTypeCtrl.AppendItems(strings=list)
        if list.count(tlStartType)==0:
            tlStartTypeCtrl.Select(n=0)
        else:
            tlStartTypeCtrl.SetSelection(int(list.index(tlStartType)))
        tlStartTypeCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        sBtxt = wx.StaticText(panel, -1, self.text.tlStartType)
        mySizer_1.Add(sBtxt,(1,0))
        mySizer_1.Add(tlStartTypeCtrl,(1,1))

        tlEndTypeCtrl = wx.Choice(parent=panel, pos=(10,10))
        tlEndTypeCtrl.AppendItems(strings=list)
        if list.count(tlEndType)==0:
            tlEndTypeCtrl.Select(n=0)
        else:
            tlEndTypeCtrl.SetSelection(int(list.index(tlEndType)))
        tlEndTypeCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        sBtxt = wx.StaticText(panel, -1, self.text.tlEndType)
        mySizer_1.Add(sBtxt,(2,0))
        mySizer_1.Add(tlEndTypeCtrl,(2,1))

        stopMacroOnTrueCtrl = wx.CheckBox(panel, -1, "")
        stopMacroOnTrueCtrl.SetValue(stopMacroOnTrue)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.stopMacroOnTrue
            ),
           (3,0)
        )
        mySizer_1.Add(stopMacroOnTrueCtrl,(3,1))

        stopMacroOnFalseCtrl = wx.CheckBox(panel, -1, "")
        stopMacroOnFalseCtrl.SetValue(stopMacroOnFalse)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.stopMacroOnFalse
            ),
           (4,0)
        )
        mySizer_1.Add(stopMacroOnFalseCtrl,(4,1))

        panel.sizer.Add(mySizer_0, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            rangeName = rangeNameCtrl.GetValue()
            iTimeAhead = iTimeAheadCtrl.GetValue()
            tlStartType = tlStartTypeCtrl.GetStringSelection()
            tlEndType = tlEndTypeCtrl.GetStringSelection()
            stopMacroOnTrue = stopMacroOnTrueCtrl.GetValue()
            stopMacroOnFalse = stopMacroOnFalseCtrl.GetValue()

            panel.SetResult(
                rangeName,
                iTimeAhead,
                tlStartType,
                tlEndType,
                stopMacroOnTrue,
                stopMacroOnFalse
            )



class GetCurrentCondition(eg.ActionClass):
    name = "GetCurrentCondition"
    description = "Action to get current condition"

    def __call__(self):
        if not self.plugin.initsynch:
            return self.plugin.weather_data['condition']
        else:
            print self.text.txtInit
            return "Undefined"



class GetForecasts(eg.ActionClass):
    name = "GetForecasts"
    description = "Action to get weather forecasts"

    def __call__(self):
        if not self.plugin.initsynch:
            return self.plugin.weather_data['forecasts']
        else:
            print self.text.txtInit
            return "Undefined"



class GetWindData(eg.ActionClass):
    name = "GetWindData"
    description = "Action to get wind data"

    def __call__(self):
        if not self.plugin.initsynch:
            return self.plugin.weather_data['wind']
        else:
            print self.text.txtInit
            return "Undefined"



class GetAtmosphereData(eg.ActionClass):
    name = "GetAtmosphereData"
    description = "Action to get atmosphere data"

    def __call__(self):
        if not self.plugin.initsynch:
            return self.plugin.weather_data['atmosphere']
        else:
            print self.text.txtInit
            return "Undefined"



class SetVacationON(eg.ActionClass):
    name = "Vacation ON"
    description = "Action to set the Vacation flag TRUE"

    def __call__(self):
        if self.plugin.started:
            prm = {
                '7':True
            }
            self.plugin.SetVar(prm)
        else:
            print self.text.txtInit



class SetVacationOFF(eg.ActionClass):
    name = "Vacation OFF"
    description = "Action to set the Vacation flag FALSE"

    def __call__(self):
        if self.plugin.started:
            prm = {
                '7':False
            }
            self.plugin.SetVar(prm)
        else:
            print self.text.txtInit



class SetEmptyHouseON(eg.ActionClass):
    name = "EmptyHouse ON"
    description = "Action to set the EmptyHouse flag TRUE"

    def __call__(self):
        if self.plugin.started:
            prm = {
                '13':True
            }
            self.plugin.SetVar(prm)
        else:
            print self.text.txtInit



class SetEmptyHouseOFF(eg.ActionClass):
    name = "EmptyHouse OFF"
    description = "Action to set the EmptyHouse flag FALSE"

    def __call__(self):
        if self.plugin.started:
            prm = {
                '13':False
            }
            self.plugin.SetVar(prm)
        else:
            print self.text.txtInit



class SetLocation(eg.ActionClass):
    name = "Set your location specifics"
    description = (
        "This plugin action is used to set your location specific data"+
        " including latitude, longitude, time zone and others. "
    )

    def __call__(
        self,
        label,
        myLongitude,
        myLatitude,
        location_id,
        fixedHolidays,
        variableHolidays,
        summerSeasonBegins,
        summerSeasonEnds,
        iTimeZone
    ):
        if self.plugin.started:
            prm = {
                '0':myLongitude,
                '1':myLatitude,
                '2':location_id,
                '3':fixedHolidays,
                '4':variableHolidays,
                '5':summerSeasonBegins,
                '6':summerSeasonEnds,
                '10':iTimeZone
            }
            self.plugin.SetVar(prm)
        else:
            print self.text.txtInit


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        label = '',
        myLongitude = None,
        myLatitude = None,
        location_id = None,
        fixedHolidays = None,
        variableHolidays = None,
        summerSeasonBegins = None,
        summerSeasonEnds = None,
        iTimeZone = None
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(5, 5)

        if myLongitude == None and myLatitude == None:
            myLongitude = float(plugin.myLongitude)
            myLatitude = float(plugin.myLatitude)
            location_id = str(plugin.location_id)
            fixedHolidays = str(plugin.fixedHolidays)
            variableHolidays = str(plugin.variableHolidays)
            summerSeasonBegins = str(plugin.summerSeasonBegins)
            summerSeasonEnds = str(plugin.summerSeasonEnds)
            iTimeZone = str(plugin.iTimeZone)

        labelCtrl = wx.TextCtrl(panel, -1, label)
        labelCtrl.SetInitialSize((150,-1))
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.label
            ),
           (0,0)
        )
        mySizer_1.Add(labelCtrl,(0,1))

        f_myLatitude = float(myLatitude)
        myLatitudeCtrl = panel.SpinNumCtrl(
            f_myLatitude,
            decimalChar = '.',                 # by default, use '.' for decimal point
            groupChar = ',',                   # by default, use ',' for grouping
            fractionWidth = 4,
            integerWidth = 3,
            min = -90.0000,
            max = 90.0000,
            increment = 0.0050
        )
        myLatitudeCtrl.SetInitialSize((90,-1))
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                plugin.text.txtMyLatitude
            ),
           (1,0)
        )
        mySizer_1.Add(myLatitudeCtrl,(1,1))

        f_myLongitude = float(myLongitude)
        myLongitudeCtrl = panel.SpinNumCtrl(
            f_myLongitude,
            decimalChar = '.',                 # by default, use '.' for decimal point
            groupChar = ',',                   # by default, use ',' for grouping
            fractionWidth = 4,
            integerWidth = 4,
            min = -180.0000,
            max = 180.0000,
            increment = 0.0050
        )
        myLongitudeCtrl.SetInitialSize((90,-1))
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                plugin.text.txtMyLongitude
            ),
           (2,0)
        )
        mySizer_1.Add(myLongitudeCtrl,(2,1))

        # Select or accept proposed timezone
        iTimeZoneCtrl = wx.Choice(parent=panel, pos=(10,10))
        list = [
            '-12.00',
            '-11.00',
            '-10.00',
            '-09.30',
            '-09.00',
            '-08.00',
            '-07.00',
            '-06.00',
            '-05.00',
            '-04.30',
            '-04.00',
            '-03.00',
            '-02.00',
            '-01.00',
            '00.00',
            '+01.00',
            '+02.00',
            '+03.00',
            '+03.30',
            '+04.00',
            '+04.30',
            '+05.00',
            '+05.30',
            '+05.45',
            '+06.00',
            '+06.30',
            '+07.00',
            '+08.00',
            '+09.00',
            '+09.30',
            '+10.00',
            '+10.30',
            '+11.00',
            '+11.30',
            '+12.00',
            '+12.45',
            '+13.00',
            '+14.00'
        ]
        iTimeZoneCtrl.SetInitialSize((60,-1))
        iTimeZoneCtrl.AppendItems(strings=list)
        if list.count(iTimeZone)==0:
            iTimeZoneCtrl.Select(n=0)
        else:
            iTimeZoneCtrl.SetSelection(int(list.index(iTimeZone)))
        iTimeZoneCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                plugin.text.txtTimeZone
            ),
           (3,0)
        )
        mySizer_1.Add(iTimeZoneCtrl,(3,1))

        desc1 = wx.StaticText(panel, -1, plugin.text.LocationLabel)
        mySizer_1.Add(desc1,(4,0))
        Location = wx.TextCtrl(panel, -1,location_id)
        Location.SetInitialSize((200,-1))
        mySizer_1.Add(Location,(4,1))

        fixedHolidaysCtrl = wx.TextCtrl(panel, -1, fixedHolidays)
        fixedHolidaysCtrl.SetInitialSize((300,-1))
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                plugin.text.txtFixedHolidays
            ),
           (5,0)
        )
        mySizer_1.Add(fixedHolidaysCtrl,(5,1))

        variableHolidaysCtrl = wx.TextCtrl(panel, -1, variableHolidays)
        variableHolidaysCtrl.SetInitialSize((300,-1))
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                plugin.text.txtVariableHolidays
            ),
           (6,0)
        )
        mySizer_1.Add(variableHolidaysCtrl,(6,1))

        summerBeginsCtrl = wx.Choice(parent=panel, pos=(10,10))
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
        summerBeginsCtrl.AppendItems(strings=list)
        if list.count(summerSeasonBegins)==0:
            summerBeginsCtrl.Select(n=0)
        else:
            summerBeginsCtrl.SetSelection(int(list.index(summerSeasonBegins)))
        summerBeginsCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        sBtxt = wx.StaticText(panel, -1, plugin.text.txtSummerSeasonBegins)
        mySizer_1.Add(sBtxt,(7,0))
        mySizer_1.Add(summerBeginsCtrl,(7,1))

        summerEndsCtrl = wx.Choice(parent=panel, pos=(10,10))
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
        summerEndsCtrl.AppendItems(strings=list)
        if list.count(summerSeasonEnds)==0:
            summerEndsCtrl.Select(n=0)
        else:
            summerEndsCtrl.SetSelection(int(list.index(summerSeasonEnds)))
        summerEndsCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        sEtxt = wx.StaticText(panel, -1, plugin.text.txtSummerSeasonEnds)
        mySizer_1.Add(sEtxt,(8,0))
        mySizer_1.Add(summerEndsCtrl,(8,1))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            label = labelCtrl.GetValue()
            myLongitude = str(myLongitudeCtrl.GetValue())
            myLatitude = str(myLatitudeCtrl.GetValue())
            location_id = Location.GetValue()
            fixedHolidays = fixedHolidaysCtrl.GetValue()
            variableHolidays = variableHolidaysCtrl.GetValue()
            summerSeasonBegins = summerBeginsCtrl.GetStringSelection()
            summerSeasonEnds = summerEndsCtrl.GetStringSelection()
            iTimeZone = iTimeZoneCtrl.GetStringSelection()
            panel.SetResult(
                        label,
                        myLongitude,
                        myLatitude,
                        location_id,
                        fixedHolidays,
                        variableHolidays,
                        summerSeasonBegins,
                        summerSeasonEnds,
                        iTimeZone
            )

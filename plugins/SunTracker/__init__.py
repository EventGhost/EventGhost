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
# 2011-12-16  Fixed to work with -translate switch
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
    version = "1.2.4",
    description =(
        "Triggers an event at sunset/sunrise and configurable dates & times"
        '<br\n><br\n>'
        '<center><img src="suntracker_plugin.png" /></center>'
    ),
    url = "http://www.eventghost.net/forumThread",
)

import eg
import time, datetime, math, string, sys, os, random, calendar
import Sun, pywapi
from threading import Thread, Event



class Text:
    started = "Plugin started"
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
    lg_movingG_1 = "Moving Ghost with random control is enabled for "
    lg_movingG_2 = "Global Moving Ghost status is: "
    thr_abort = "Thread is terminating: "
    txtFixedHolidays = "Fixed Public Holidays:"
    txtVariableHolidays = "Variable Public Holidays:"
    txtVacation_m = "Vacation mode"
    txtMyLongitude = "My Longitude"
    txtMyLatitude = "My Latitude"
    LocationLabel = "Location:"
    LanguageLabel = "Language Code:"
    CitiesLabel = "Cities:"
    CountriesLabel = "Countries:"
    txtGoogleWeatherUnavailable = "Google weather data is not available"
    txtWeatherCondition = "Weather Condition: "
    txtTimeCompensation = "Total time compensation(negative is ON earlier and OFF later): "
    txtSummerSeasonBegins = "Summer Season Begins with (month): "
    txtSummerSeasonEnds = "Summer Season Ends with (month): "
    sunStatus = "Create events at sunset and sunrise"
    sunIsUp = "Sunrise"
    sunIsDown = "Sunset"
    
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
        txtNbrBursts = "Number of events per control(1-10 bursts)"
        txtON = " ON"
        txtOFF = " OFF"
        txtCmdDelay = "Delay between the events(0.5-5.0 s)"
        doLogLoopsText = "Print normal loop info(Y/N)"
        txtMoving_Ghost = "Enable Local Moving Ghost"
        txtMoving_Ghost_G = "Enable Global Moving Ghost with external triggering"
        txtMoving_Ghost_r_1 = "Moving Ghost: Random intervals BEFORE midnight"
        txtMoving_Ghost_r_2 = "Moving Ghost: Random intervals AFTER midnight"
        txtMoving_Ghost_ON_min = "ON min"
        txtMoving_Ghost_ON_max = "ON max"
        txtMoving_Ghost_OFF_min = "OFF min"
        txtMoving_Ghost_OFF_max = "OFF max"
        txtMinOnPeriod = "Minimum ON period required(0-60 min)"
        txtDoSynch = "Synchronization activated(Y/N)"
        txtSynchInterval = "Synch interval(6-600 min)"
        txtOffset = "Set offset for this control(-120...120 min)"
        txtWeather = "Weather compensation factor(0...60 min)"

    class SetMovingGhostON:
        txtMG_ON = "Moving Ghost function ON"

    class SetMovingGhostOFF:
        txtMG_OFF = "Moving Ghost function OFF"
             
    class GetSunStatusWeatherCompensated:
        txtWeather = "Weather compensation factor(0...60 min)"



#All credits to Henrik Haerkoenen for Sun.py 
class SunState(Sun.Sun):


    def getSunState(self, year, month, day, lon, lat):
        sunRise, sunSet = self.sunRiseSet(year, month, day, lon, lat)
        return sunRise, sunSet



class GlobalMovingGhost(eg.PersistentData):
    movingGhost = False



class SuntrackerThread(Thread):
    text = Text
    import pywapi
    
    
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
        self.finished = Event()
        self.abort = False
        self.fixedHolidays = fixedHolidays
        self.variableHolidays = variableHolidays
        self.iNbrOfBurstsON = iNbrOfBurstsON
        self.iNbrOfBurstsOFF = iNbrOfBurstsOFF
        self.cmdDelay = cmdDelay
        self.doLogLoops = doLogLoops
        self.vacation_m = vacation_m
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
        self.bDoSynch = bDoSynch 
        self.iOffset = iOffset
        self.iWeather = iWeather
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
            for i in range(0,8):
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
            for i in range(0,8):
                if dayType == str(i):
                    j = i * 3 - 1
                    if j == -1:
                        j = 20
                    if j == 20:
                        j = 23    
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
            for i in range(0,8):
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
            for i in range(0,8):
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

            for i in range(0,8):
                if dayType == str(i):
                    j = i * 3 + 3
                    if j == 21:
                        j = 0
                    if j == 24:
                        j = 21
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
            for i in range(0,8):
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
                    eg.TriggerEvent(self.eventNameOn)
                    time.sleep(self.cmdDelay)
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
                        eg.TriggerEvent(self.eventNameOn)
                        time.sleep(self.cmdDelay)
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
                    eg.TriggerEvent(self.eventNameOff) 
                    time.sleep(self.cmdDelay)
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
                        eg.TriggerEvent(self.eventNameOff) 
                        time.sleep(self.cmdDelay)
            return(lightON) 


        while(not self.abort):
            if self.plugin.iGetWeather <  self.iWeather * 2:
                self.plugin.iGetWeather =  self.iWeather * 2
            tr = random.random()
            remain = 61.0 - int(time.strftime("%S", time.localtime())) + tr
#            remain = 10
            self.finished.wait(remain)
            self.finished.clear()
            if self.abort:
                break
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
            if initsynch == 1:
                if self.moving_Ghost:
                    bMghost = True
                elif self.moving_Ghost_G and GlobalMovingGhost.movingGhost:
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
                print lg
                if nd != od and not bMghost:
                    lg = self.text.lg_dayOfWeek+od
                    print lg
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
                        print self.text.lg_vacation_1 + self.name
                        print(
                            self.text.lg_vacation_2
                            + self.text.lg_vacation_3
                            + nd
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
                        print self.text.lg_holiday_1 + self.name
                        print(
                            self.text.lg_holiday_2
                            + self.text.lg_holiday_3
                            + nd
                        )

            # Initial logging when Moving Ghost is activated
            if bMghost:
                self.plugin.LogToFile(
                            self.text.lg_movingG_1 + self.name,
                            'Suntracker_'+self.name+'.html'
                )
                print self.text.lg_movingG_1 + self.name

            # Restoring to initial value
            light = 10

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
                random.seed(self.name)
                random.jumpahead(int(len(self.name)))
                if(
                    self.moving_Ghost
                    or(
                        self.moving_Ghost_G
                        and GlobalMovingGhost.movingGhost
                    )
                ):
                    self.bDoSynch = False
                    if(
                        trigTime > csSS
                        or trigTime < csSR
                    ):
                        light = 1
            else:
                if(
                    self.moving_Ghost
                    or(
                        self.moving_Ghost_G
                        and GlobalMovingGhost.movingGhost
                    )
                    and(trigTime > csSS
                    or trigTime < csSR)
                ):
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
            
            #Print basic loop info
            if self.doLogLoops and initsynch == 0:
                print(
                    self.text.nxt_1
                    + self.name
                    + self.text.nxt_2
                    + str(remain)
                    + self.text.nxt_3
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
        
            initsynch = 0
 
        
    def AbortSuntracker(self):
        self.abort = True
        print self.text.thr_abort, self.name
        self.finished.set()
       
  

class Suntracker(eg.PluginClass):
    iconFile = "suntracker_plugin"
    text = Text

    
    def __init__(self):
        self.AddAction(SuntrackerAction)
        self.AddAction(GetSunStatusWeatherCompensated)
        self.AddAction(GetContentsOfVariable)
        self.AddAction(SetMovingGhostON)
        self.AddAction(SetMovingGhostOFF)
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
        self.OkButtonClicked = False
        self.started = False
        self.k = SunState()


    def __start__(
        self,
        myLongitude,
        myLatitude,
        location_id,
        fixedHolidays,
        variableHolidays,
        summerSeasonBegins,
        summerSeasonEnds,
        vacation_m,
        sunStatus
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
        self.sunStatus = sunStatus
        self.sunIsUp = True
        self.started = True
        self.initsynch = True
        self.csSR = ''
        self.csSS = ''
        self.currCondition =''
        self.iGetWeather = 1
        if self.OkButtonClicked:
            self.OkButtonClicked = False
            self.RestartAllSuntrackers()
        majorVersion, minorVersion = sys.getwindowsversion()[0:2]
        if majorVersion > 5:
            progData = os.environ['ALLUSERSPROFILE']
            if not os.path.exists(progData+"/EventGhost/Log") and not os.path.isdir(progData+"/EventGhost/Log"):
                os.makedirs(progData+"/EventGhost/Log")
        else:
            if not os.path.exists('Log') and not os.path.isdir('Log'):
                os.mkdir('Log')
        if GlobalMovingGhost.movingGhost: 
            print self.text.lg_movingG_2 + "ON"
        else:
            print self.text.lg_movingG_2 + "OFF"

        # start the main thread
        self.mainThreadEvent = Event()
        mainThread = Thread(target=self.main, args=(self.mainThreadEvent,))
        mainThread.start()


    def __stop__(self):
        self.mainThreadEvent.set()
        self.AbortAllSuntrackers()
        self.started = False


    def __close__(self):
        self.AbortAllSuntrackers()
        self.started = False


    def LogToFile(self, s, fName):
        majorVersion, minorVersion = sys.getwindowsversion()[0:2]
        timeStamp = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        logStr = timeStamp+"\t"+s+"<br\n>"
        fileHandle = None
        
        if majorVersion > 5:
            progData = os.environ['ALLUSERSPROFILE']
            if not os.path.exists(progData+"/EventGhost/Log") and not os.path.isdir(progData+"/EventGhost/Log"):
                os.makedirs(progData+"/EventGhost/Log")
            fileHandle = open(progData+'/EventGhost/Log/'+fName, 'a')
            fileHandle.write(logStr)
            fileHandle.close()
        else:
            if not os.path.exists('Log') and not os.path.isdir('Log'):
                os.mkdir('Log')
            fileHandle = open('Log/'+fName, 'a')
            fileHandle.write(logStr)
            fileHandle.close()


    def Check_for_daylight_saving(self):
        iDLS = 0
        iDLS = time.localtime()[-1]
        if iDLS == 1:
            if self.initsynch:
                msg = "SunTracker: "+self.text.txt_dls_true
                self.LogToFile(msg, 'Suntracker.html')
                print msg
                msg = time.strftime(
                   ("%Z"+self.text.txt_tz),
                    time.localtime()
                )
                self.LogToFile(msg, 'Suntracker.html')
                print msg
        else:
            if self.initsynch:
                msg = "SunTracker: "+self.text.txt_dls_false
                self.LogToFile(msg, 'Suntracker.html')
                print msg
                msg = time.strftime(
                   ("%Z"+self.text.txt_tz),
                    time.localtime()
                )
                self.LogToFile(msg, 'Suntracker.html')
                print msg
        return(iDLS)
    

    def CheckWeatherCondition(self):
        weather_data = None
        currCondition = ""
        weather_data = pywapi.get_weather_from_google(
            self.location_id,
            ''
        )
        if not weather_data.has_key('current_conditions'):
            self.LogToFile(
                    self.text.txtGoogleWeatherUnavailable,
                    'Suntracker.html'
            )
            return "Unavailable"
        if not weather_data['current_conditions'].has_key('condition'):
            self.LogToFile(
                    self.text.txtGoogleWeatherUnavailable,
                    'Suntracker.html'
            )
            return "Unavailable"
        currCondition = weather_data['current_conditions']['condition']
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
        # Adjust the sunrise/sunset trig times to weather condition
        currMonth = time.strftime("%m", time.localtime())

        # Set the default
        trigTimeSR = self.GetOffsetTimeSR(iOffset)
        trigTimeSS = self.GetOffsetTimeSS(iOffset)

        if(
            currCondition == "Cloudy"
            or currCondition == "Fog"
            or currCondition == "Rain"
            or currCondition == "Light rain"
            or currCondition == "Rain Showers"
            or currCondition == "Freezing Rain"
            or currCondition == "Drizzle"
            or currCondition == "Freezing Drizzle"
        ):
            trigTimeSR = self.GetOffsetTimeSR(
                                - iWeather
                                + iOffset
                         )
            trigTimeSS = self.GetOffsetTimeSS(
                                - iWeather
                                + iOffset
                         )
            timeCompensation = - iWeather + iOffset
        
        if(
            currCondition == "Snow"
            or currCondition == "Light snow"
            or currCondition == "Mostly Cloudy"
            or currCondition == "Partly Cloudy"
            or currCondition == "Overcast"
        ):
            trigTimeSR = self.GetOffsetTimeSR(
                                - iWeather/2
                                + iOffset
                         )
            trigTimeSS = self.GetOffsetTimeSS(
                                - iWeather/2
                                + iOffset
                         )
            timeCompensation = - iWeather/2 + iOffset
        
        if(
            currCondition == "Sunny"
            or currCondition == "Clear"
        ):
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
                    timeCompensation =(
                                        iWeather
                                        + iOffset
                                        )
            else:    
                timeCompensation = iOffset

        if(
            currCondition == "Unavailable"
            or currCondition == "Undefined"
        ):
            timeCompensation = iOffset
        
        return (currCondition, timeCompensation, trigTimeSS, trigTimeSR)


    def main(self,mainThreadEvent):
        sunIsUpOld = self.sunIsUp
        self.iGetWeatherCntr = 0
        #print "mainthread started"
        while not mainThreadEvent.isSet():
            if self.iGetWeatherCntr == 0:
                self.currCondition = self.CheckWeatherCondition()
                self.iGetWeatherCntr = self.iGetWeather
            else:
                self.iGetWeatherCntr -= 1

            # Calculate Sunrise/Sunset times at your geographical position
            year = int(time.strftime("%Y", time.localtime()))
            month = int(time.strftime("%m", time.localtime()))
            day = int(time.strftime("%d", time.localtime()))
             
            # Get the sunrise/sunset times in UT and fix the format
            st = str(self.k.getSunState(
                year,
                month,
                day,
                float(self.myLongitude),
                float(self.myLatitude))
            )
            st = st.replace("(", "")
            st = st.replace(")", "")
            st = st.replace(",", "")
            
            # Split and extract the data
            data = st.split()
            t1 = data[0]
            t2 = data[1]
            dat1 = t1.split(".")
            dat2 = t2.split(".")
            
            # Check if we are in daylight savings
            self.iDLS = self.Check_for_daylight_saving()

            # Adjust the times according to your timezone and daylight savings
            tZ = int(time.timezone/3600)
            
            h1 = int(int(dat1[0]) + self.iDLS - tZ)
            m1 = float("." + dat1[1])
            m1 = int(m1 * 60)
            if m1 < 0:
                h1 -= 1
                m1 = 60 + m1
            if h1 > 23:
                h1 = abs(24 - h1)
            sh1 = str(h1)
            if h1 < 10:
                sh1 = "0" + sh1
                
            sm1 = str(m1)
            if m1 < 10:
                sm1 = "0" + sm1
                
            h2 = int(int(dat2[0]) + self.iDLS - tZ)
            m2 = float("." + dat2[1])
            m2 = int(m2 * 60)
            if m2 < 0:
                h2 -= 1
                m2 = 60 + m2
            if h2 > 23:
                h2 = abs(24 - h2)
            sh2 = str(h2)
            if h2 < 10:
                sh2 = "0" + sh2
                
            sm2 = str(m2)
            if m2 < 10:
                sm2 = "0" + sm2
          
            # Finally, the time strings are composed
            self.csSR = sh1 + sm1
            self.csSS = sh2 + sm2
          
            # Get the current date & time now
            trigTime = str(time.strftime("%H%M", time.localtime()))

            # Set the flag for sun status
            if trigTime >= self.csSS or trigTime < self.csSR:
                self.sunIsUp = False
            else:
                self.sunIsUp = True

            #print "Check the flag for sun status"
            if self.sunIsUp and not sunIsUpOld:
                if self.sunStatus:
                    if not self.initsynch:
                        eg.TriggerEvent(self.text.sunIsUp)
                    sunIsUpOld = self.sunIsUp

            if not self.sunIsUp and sunIsUpOld:
                if self.sunStatus:
                    if not self.initsynch:
                        eg.TriggerEvent(self.text.sunIsDown) 
                    sunIsUpOld = self.sunIsUp

            self.initsynch = False
            remain = 60.0 - int(time.strftime("%S", time.localtime()))
            mainThreadEvent.wait(remain)
        #print "mainthread ended"


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
        summerSeasonEnds
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
        self.suntrackerThreads = {}


    def RestartAllSuntrackers(self, startNewIfNotAlive = True):
        for i, item in enumerate(self.GetAllsuntrackerNames()):
            if startNewIfNotAlive:
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
                    self.summerSeasonEnds
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
        location_id = "Stockholm, Sweden",
        fixedHolidays = "0101,0501,0606,1224,1225,1226",
        variableHolidays = "0106,0402,0405,0512,0522,0523,0625",
        summerSeasonBegins = "--",
        summerSeasonEnds = "--",
        vacation_m = False,
        sunStatus = True,
        *args
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)
        mySizer_1.AddGrowableRow(0)
        mySizer_1.AddGrowableCol(1)
        mySizer_1.AddGrowableCol(2)
        mySizer_1.AddGrowableCol(3)
       
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

        f_myLatitude = float(myLatitude)
        myLatitudeCtrl = panel.SpinNumCtrl(
            f_myLatitude,
            decimalChar = '.',                 # by default, use '.' for decimal point
            groupChar = ',',                   # by default, use ',' for grouping
            fractionWidth = 4,
            integerWidth = 2,
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
            integerWidth = 3,
            min = -128.0000,
            max = 128.0000,
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

        desc1 = wx.StaticText(panel, -1, self.text.LocationLabel)
        mySizer_2.Add(desc1,(2,0))
        Location = wx.TextCtrl(panel, -1,location_id)
        Location.SetInitialSize((200,-1))
        mySizer_2.Add(Location,(2,1))
        
        desc2 = wx.StaticText(panel, -1, self.text.CountriesLabel)
        mySizer_2.Add(desc2,(3,0))  
        CountriesEdit = wx.ListBox(
            panel,
            -1,
            choices=[],
            style=wx.LB_SINGLE,
            size=(200,80)
        )
        mySizer_2.Add(CountriesEdit,(3,1))

        CountriesEdit.Clear()
        CountryList = pywapi.get_countries_from_google()
        i=0
        
	while i < len(CountryList):		
            CountriesEdit.Append(CountryList[i]['name'])
	    i=i+1

	    
        def OnCountrySelect(event):
            CitiesEdit.Clear()
            result = pywapi.get_cities_from_google(
                str(CountryList[CountriesEdit.GetSelection()]['iso_code'])
            )
            i=0
	    
	    while i < len(result):		
                CitiesEdit.Append(result[i]['name'])
		i=i+1	
            Location.SetValue(
                CitiesEdit.GetStringSelection() +
                ", " +
                CountriesEdit.GetStringSelection()
            )
        CountriesEdit.Bind(wx.EVT_LISTBOX, OnCountrySelect)
   
        desc3 = wx.StaticText(panel, -1, self.text.CitiesLabel)
        mySizer_2.Add(desc3,(4,0))  
        CitiesEdit = wx.ListBox(
            panel,
            -1,
            choices=[],
            style=wx.LB_SINGLE,
            size=(200,50)
        )
        mySizer_2.Add(CitiesEdit,(4,1))
        
        
        def OnCitySelect(event):
            Location.SetValue(
                CitiesEdit.GetStringSelection() +
                ", " +
                CountriesEdit.GetStringSelection()
            )
        CitiesEdit.Bind(wx.EVT_LISTBOX, OnCitySelect)

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

        vacation_mCtrl = wx.CheckBox(panel, -1, self.text.txtVacation_m)
        vacation_mCtrl.SetValue(vacation_m)
        mySizer_2.Add(vacation_mCtrl,(10,0))
  
        sunStatusCtrl = wx.CheckBox(panel, -1, self.text.sunStatus)
        sunStatusCtrl.SetValue(sunStatus)
        mySizer_2.Add(sunStatusCtrl,(10,1))

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
            ) #wx.LIST_AUTOSIZE
            event.Skip()


        def OnApplyButton(event): 
            event.Skip()
            self.RestartAllSuntrackers()
            PopulateList(wx.CommandEvent())


        def OnOkButton(event): 
            event.Skip()
            self.OkButtonClicked = True
            if not self.started:    
                self.RestartAllSuntrackers()
            PopulateList(wx.CommandEvent())
            

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
            vacation_m = vacation_mCtrl.GetValue()
            sunStatus = sunStatusCtrl.GetValue()
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
        summerSeasonEnds
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
            self.plugin.summerSeasonEnds
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
        summerSeasonEnds
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
        location_id = "Stockholm, Sweden",
        iSynchInterval = 30,
        summerSeasonBegins = "--",
        summerSeasonEnds = "--"
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

        doLogLoopsCtrl = wx.CheckBox(panel, -1, "")
        doLogLoopsCtrl.SetValue(doLogLoops)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.doLogLoopsText
            ),
           (3,0)
        )
        mySizer_1.Add(doLogLoopsCtrl,(3,1))

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
            decimalChar = '.',                 # by default, use '.' for decimal point
            groupChar = ',',                   # by default, use ',' for grouping
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
           (2,0)
        )
        mySizer_3.Add(iMinOnPeriodCtrl,(2,1))

        bDoSynchCtrl = wx.CheckBox(panel, -1, "")
        bDoSynchCtrl.SetValue(bDoSynch)
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtDoSynch
            ),
           (3,0)
        )
        mySizer_3.Add(bDoSynchCtrl,(3,1))

        iSynchIntervalCtrl = panel.SpinIntCtrl(iSynchInterval, 6, 600)
        iSynchIntervalCtrl.SetInitialSize((50,-1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtSynchInterval
            ),
           (3,2)
        )
        mySizer_3.Add(iSynchIntervalCtrl,(3,3))

        iOffsetCtrl = panel.SpinIntCtrl(iOffset, -120, 120)
        iOffsetCtrl.SetInitialSize((50,-1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtOffset
            ),
           (4,0)
        )
        mySizer_3.Add(iOffsetCtrl,(4,1))

        iWeatherCtrl = panel.SpinIntCtrl(iWeather, 0, 60)
        iWeatherCtrl.SetInitialSize((50,-1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtWeather
            ),
           (4,2)
        )
        mySizer_3.Add(iWeatherCtrl,(4,3))

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
           (1,0)
        )
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_ON_min
            ),
           (1,1)
        )
        mySizer_4.Add(moving_Ghost_r1Ctrl,(1,2))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_ON_max
            ),
           (1,3)
        )
        mySizer_4.Add(moving_Ghost_r2Ctrl,(1,4))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_OFF_min
            ),
           (1,5)
        )
        mySizer_4.Add(moving_Ghost_r3Ctrl,(1,6))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_OFF_max
            ),
           (1,7)
        )
        mySizer_4.Add(moving_Ghost_r4Ctrl,(1,8))

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
        mySizer_4.Add(moving_Ghost_r5Ctrl,(2,2))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_ON_max
            ),
           (2,3)
        )
        mySizer_4.Add(moving_Ghost_r6Ctrl,(2,4))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_OFF_min
            ),
           (2,5)
        )
        mySizer_4.Add(moving_Ghost_r7Ctrl,(2,6))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMoving_Ghost_OFF_max
            ),
           (2,7)
        )
        mySizer_4.Add(moving_Ghost_r8Ctrl,(2,8))

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
            # re-assign the OK button
            
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
                self.plugin.summerSeasonEnds
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
            location_id = self.plugin.location_id
            summerSeasonBegins = self.plugin.summerSeasonBegins
            summerSeasonEnds = self.plugin.summerSeasonEnds

            moving_Ghost_G = moving_Ghost_G_Ctrl.GetValue()
            plugin.AddMoving_Ghost_G(moving_Ghost_G, indx)
            moving_Ghost = moving_GhostCtrl.GetValue()
            plugin.AddMoving_Ghost(moving_Ghost, indx)
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
                summerSeasonEnds
            )



class SetMovingGhostON(eg.ActionClass):
    name = "MovingGhost ON"
    description = "Action to set the MovingGhost flag TRUE"


    def __call__(self):
        if not GlobalMovingGhost.movingGhost:
            print self.text.txtMG_ON
        GlobalMovingGhost.movingGhost = True



class SetMovingGhostOFF(eg.ActionClass):
    name = "MovingGhost OFF"
    description = "Action to set the MovingGhost flag FALSE"


    def __call__(self):
        if GlobalMovingGhost.movingGhost:
            print self.text.txtMG_OFF
        GlobalMovingGhost.movingGhost = False

             

class GetContentsOfVariable(eg.ActionClass):
    name = "Sunstate"
    description = "Action to check if sun is up or down"


    def __call__(self):
        return self.plugin.sunIsUp



class GetSunStatusWeatherCompensated(eg.ActionClass):
    name = "Sunstate with weather compensation"
    description = (
        "Action to request weather compensated sun status"+
        "Useful when determining if lights shall be turned on and off"+
        "during various weather conditions like sunny, cloudy, foggy etc)"
    )


    def __call__(
        self,
        iWeather
    ):
        self.iWeather = iWeather
        sunIsUpW = False
        currCondition = "Undefined"
        
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
            or trigTimeSR < self.plugin.csSR
        ):
            sunIsUpW = False
        else:
            sunIsUpW = True

        """
        print(
            self.iWeather,
            currCondition,
            time.strftime("%H%M", time.localtime()),
            trigTimeSR,
            self.plugin.csSR,
            trigTimeSS,
            self.plugin.csSS,
            sunIsUpW
        )
        """

        return sunIsUpW


    def Configure(
        self,
        iWeather = 0
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_0 = wx.GridBagSizer(5, 5)

        iWeatherCtrl = panel.SpinIntCtrl(iWeather, 0, 60)
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

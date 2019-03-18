#!/usr/bin/python
# -*- coding: utf-8 -*-

import eg

eg.RegisterPlugin(
    name="Rain8",
    guid='{E5D16F0B-B572-4EC0-8D87-D9FDA761A3C7}',
    author="Walter Kraembring",
    canMultiLoad=True,
    version="0.0.0",
    description=(
        "Triggers events to control Rain8 lawn sprinklers in the garden"
        '<br\n><br\n>'
        '<center><img src="rain8_plugin.png" /></center>'
    ),
    url="http://www.eventghost.org/forumThread",
)

##############################################################################
# All credits to Henrik H�rk�nen for providing Sun.py
# All credits to Eugene Kaznacheev for providing the pywapi.py
#
# Revision history:
#
# 2010-01-08  First prototype
##############################################################################

import time, math, sys, os, random, calendar
import pywapi
import wx
from threading import Thread, Event


class Text:
    name = "Control Rain8 device"
    description = (
        "Allows starting, stopping or disabling/enabling of a" +
        "Rain8 device"
    )
    started = "Plugin started"
    stopped = "The plugin thread has stopped"
    deviceName = "Name of the Rain8 device"
    txt_deviceType = "Select the proper Rain8 device type"
    txt_ConfHouseCode = "Select the proper house code for the Rain8 device"
    runOrder = "Define the run order for the valves"
    zoneDelay = "Define the delay between zones"
    AfterSunset = "Start sprinkling nbr of minutes after sunset"
    BeforeSunrise = "Start sprinkling nbr of minutes before sunrise"
    minutes = " minutes"
    seasonDryBegin = "First month of dry season"
    seasonDryEnd = "Last month of dry season"
    tempComp = "Additional minutes run time for high temperature"
    weatherLookAhead = "Use weather forecast"
    celsius = "Use Celsius instead of Fahrenheit"
    txtMyLongitude = "My Longitude"
    txtMyLatitude = "My Latitude"
    txtGoogleWeatherUnavailable = "Google weather data is not available"

    class Rain8Zone:
        name = "Control Rain8 valve/zone"
        description = (
            "Allows starting, stopping or disabling/enabling of a Rain8" +
            "valve/zone"
        )

        zoneName = "Give a proper name for the Rain8 zone"
        txt_ConfUnitCode = "Select the proper unit code for the Rain8 valve"
        txt_runTime = "Define the run time for this valve"
        spDays = "Days suitable for sprinkling"
        Su = "Sunday"
        Mo = "Monday"
        Tu = "Tuesday"
        We = "Wednesday"
        Th = "Thursday"
        Fr = "Friday"
        Sa = "Saturday"
        txt_intervals = "Split runtime into the following number of intervals"
        txt_shadow = "Shadow compensation run time reduction (%)"
        txt_status = "Running status"
        txt_enable = "Enable valve"


class Rain8Device(eg.PluginClass):
    text = Text

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        deviceName="Give device a name",
        deviceType="Rain8 Wireless",
        houseCode="A",
        seasonDryBegin="May",
        seasonDryEnd="August",
        runOrder="1,2,3,4,5,6,7,8",
        zoneDelay=5,
        tempComp=2,
        afterSunset=60,
        beforeSunrise=60,
        weatherLookAhead=True,
        celsius=False,
        myLongitude="18.0000",
        myLatitude="59.2500"
    ):
        panel = eg.ConfigPanel(self)
        mySizer = wx.GridBagSizer(5, 5)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(5, 5)
        mySizer_3 = wx.GridBagSizer(5, 5)
        mySizer_4 = wx.GridBagSizer(5, 5)

        # name
        deviceNameCtrl = wx.TextCtrl(panel, -1, deviceName)
        deviceNameCtrl.SetInitialSize((250, -1))
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.deviceName
            ),
            (1, 0)
        )
        mySizer_1.Add(deviceNameCtrl, (1, 1))

        # device type
        deviceTypeCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            'Rain8 X10',
            'Rain8 RS232',
            'Rain8 UPB',
            'Rain8 Wireless'
        ]
        if deviceType != "":
            if list.count(deviceType) == 0:
                list.append(deviceType)
        deviceTypeCtrl.AppendItems(items=list)
        if list.count(deviceType) == 0:
            deviceTypeCtrl.Select(n=0)
        else:
            deviceTypeCtrl.SetSelection(int(list.index(deviceType)))
        deviceTypeCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.text.txt_deviceType)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(deviceTypeCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # house code
        houseCodeCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            'A',
            'B',
            'C',
            'D',
            'E',
            'F'
        ]
        if houseCode != "":
            if list.count(houseCode) == 0:
                list.append(houseCode)
        houseCodeCtrl.AppendItems(items=list)
        if list.count(houseCode) == 0:
            houseCodeCtrl.Select(n=0)
        else:
            houseCodeCtrl.SetSelection(int(list.index(houseCode)))
        houseCodeCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.text.txt_ConfHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(houseCodeCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # run order
        runOrderCtrl = wx.TextCtrl(panel, -1, runOrder)
        runOrderCtrl.SetInitialSize((150, -1))
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.runOrder
            ),
            (2, 0)
        )
        mySizer_1.Add(runOrderCtrl, (2, 1))

        # zone delay
        zoneDelayCtrl = panel.SpinIntCtrl(zoneDelay, 1, 10)
        zoneDelayCtrl.SetInitialSize((45, -1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.zoneDelay
            ),
            (1, 0)
        )
        mySizer_2.Add(zoneDelayCtrl, (1, 1))
        mySizer_2.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.minutes
            ),
            (1, 2)
        )

        # after sunset
        afterSunsetCtrl = panel.SpinIntCtrl(afterSunset, 0, 120)
        afterSunsetCtrl.SetInitialSize((45, -1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.AfterSunset
            ),
            (1, 0)
        )
        mySizer_3.Add(afterSunsetCtrl, (1, 1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.minutes
            ),
            (1, 2)
        )

        # before sunrise
        beforeSunriseCtrl = panel.SpinIntCtrl(beforeSunrise, 0, 120)
        beforeSunriseCtrl.SetInitialSize((45, -1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.BeforeSunrise
            ),
            (2, 0)
        )
        mySizer_3.Add(beforeSunriseCtrl, (2, 1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.minutes
            ),
            (2, 2)
        )

        # dry season begins
        seasonDryBeginCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'November',
            'December'
        ]
        if seasonDryBegin != "":
            if list.count(seasonDryBegin) == 0:
                list.append(seasonDryBegin)
        seasonDryBeginCtrl.AppendItems(items=list)
        if list.count(seasonDryBegin) == 0:
            seasonDryBeginCtrl.Select(n=0)
        else:
            seasonDryBeginCtrl.SetSelection(int(list.index(seasonDryBegin)))
        seasonDryBeginCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.seasonDryBegin
            ),
            (1, 0)
        )
        mySizer_4.Add(seasonDryBeginCtrl, (1, 1))

        # dry season ends
        seasonDryEndCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'November',
            'December'
        ]
        if seasonDryEnd != "":
            if list.count(seasonDryEnd) == 0:
                list.append(seasonDryEnd)
        seasonDryEndCtrl.AppendItems(items=list)
        if list.count(seasonDryEnd) == 0:
            seasonDryEndCtrl.Select(n=0)
        else:
            seasonDryEndCtrl.SetSelection(int(list.index(seasonDryEnd)))
        seasonDryEndCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.seasonDryEnd
            ),
            (2, 0)
        )
        mySizer_4.Add(seasonDryEndCtrl, (2, 1))

        tempCompCtrl = panel.SpinIntCtrl(tempComp, 0, 60)
        tempCompCtrl.SetInitialSize((50, -1))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.tempComp
            ),
            (3, 0)
        )
        mySizer_4.Add(tempCompCtrl, (3, 1))

        weatherLookAheadCtrl = wx.CheckBox(panel, -1, "")
        weatherLookAheadCtrl.SetValue(weatherLookAhead)
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.weatherLookAhead
            ),
            (4, 0)
        )
        mySizer_4.Add(weatherLookAheadCtrl, (4, 1))

        celsiusCtrl = wx.CheckBox(panel, -1, "")
        celsiusCtrl.SetValue(celsius)
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.celsius
            ),
            (5, 0)
        )
        mySizer_4.Add(celsiusCtrl, (5, 1))

        f_myLatitude = float(myLatitude)
        myLatitudeCtrl = panel.SpinNumCtrl(
            f_myLatitude,
            decimalChar='.',  # by default, use '.' for decimal point
            groupChar=',',  # by default, use ',' for grouping
            fractionWidth=4,
            integerWidth=2,
            min=-90.0000,
            max=90.0000,
            increment=0.0050
        )
        myLatitudeCtrl.SetInitialSize((90, -1))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMyLatitude
            ),
            (8, 0)
        )
        mySizer_4.Add(myLatitudeCtrl, (8, 1))

        f_myLongitude = float(myLongitude)
        myLongitudeCtrl = panel.SpinNumCtrl(
            f_myLongitude,
            decimalChar='.',  # by default, use '.' for decimal point
            groupChar=',',  # by default, use ',' for grouping
            fractionWidth=4,
            integerWidth=3,
            min=-128.0000,
            max=128.0000,
            increment=0.0050
        )
        myLongitudeCtrl.SetInitialSize((90, -1))
        mySizer_4.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtMyLongitude
            ),
            (9, 0)
        )
        mySizer_4.Add(myLongitudeCtrl, (9, 1))

        panel.sizer.Add(mySizer_1, 0, flag=wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag=wx.EXPAND)
        panel.sizer.Add(mySizer_3, 0, flag=wx.EXPAND)
        panel.sizer.Add(mySizer_4, 0, flag=wx.EXPAND)

        while panel.Affirmed():
            deviceName = deviceNameCtrl.GetValue()
            houseCode = houseCodeCtrl.GetStringSelection()
            runOrder = runOrderCtrl.GetValue()
            zoneDelay = zoneDelayCtrl.GetValue()
            afterSunset = afterSunsetCtrl.GetValue()
            beforeSunrise = beforeSunriseCtrl.GetValue()
            seasonDryBegin = seasonDryBeginCtrl.GetStringSelection()
            seasonDryEnd = seasonDryEndCtrl.GetStringSelection()
            tempComp = tempCompCtrl.GetValue()
            weatherLookAhead = weatherLookAheadCtrl.GetValue()
            celsius = celsiusCtrl.GetValue()
            myLongitude = str(myLongitudeCtrl.GetValue())
            myLatitude = str(myLatitudeCtrl.GetValue())

            panel.SetResult(
                deviceName,
                deviceType,
                houseCode,
                seasonDryBegin,
                seasonDryEnd,
                runOrder,
                zoneDelay,
                tempComp,
                afterSunset,
                beforeSunrise,
                weatherLookAhead,
                celsius,
                myLongitude,
                myLatitude
            )

    def __init__(self):
        self.AddAction(Rain8Zone)
        self.AddAction(GetContentsOfVariable)
        self.started = False

    def __start__(
        self,
        deviceName,
        deviceType,
        houseCode,
        seasonDryBegin,
        seasonDryEnd,
        runOrder,
        zoneDelay,
        tempComp,
        afterSunset,
        beforeSunrise,
        weatherLookAhead,
        celsius,
        myLongitude,
        myLatitude
    ):
        print self.text.started
        self.deviceName = deviceName
        self.deviceType = deviceType
        self.houseCode = houseCode
        self.seasonDryBegin = seasonDryBegin
        self.seasonDryEnd = seasonDryEnd
        self.runOrder = runOrder
        self.zoneDelay = zoneDelay
        self.tempComp = tempComp
        self.afterSunset = afterSunset
        self.beforeSunrise = beforeSunrise
        self.weatherLookAhead = weatherLookAhead
        self.celsius = celsius
        self.myLongitude = myLongitude
        self.myLatitude = myLatitude
        self.sunIsUp = True
        self.started = True

        self.majorVersion, self.minorVersion = sys.getwindowsversion()[0:2]

        if self.majorVersion > 5:
            progData = os.environ['ALLUSERSPROFILE']
            if not os.path.exists(progData + "/EventGhost/Log") and not os.path.isdir(progData + "/EventGhost/Log"):
                os.makedirs(progData + "/EventGhost/Log")
        else:
            if not os.path.exists('Log') and not os.path.isdir('Log'):
                os.mkdir('Log')

        self.stopThreadEvent = Event()
        self.thread = Thread(
            target=self.ThreadWorker,
            args=(self.stopThreadEvent,)
        )
        self.thread.start()

    def __stop__(self):
        self.stopThreadEvent.set()

    def __close__(self):
        time.sleep(2.0)
        self.stopThreadEvent.set()

    def GetDayOfWeek(self, dateString):
        # day of week (monday = 0) of a given month/day/year
        ds = dateString.split('/')
        dayOfWeek = int(calendar.weekday(int(ds[2]), int(ds[0]), int(ds[1])))
        return (dayOfWeek)

    def Check_for_daylight_saving(self):
        iDLS = 0
        iDLS = time.localtime()[-1]
        return (iDLS)

    def CheckWeatherCondition(self):
        weather_data = None
        currCondition = ""
        p1 = (str(self.myLatitude).replace(".", "")).ljust(8, "0")
        p2 = (str(self.myLongitude).replace(".", "")).ljust(8, "0")
        p3 = ",,," + p1 + "," + p2
        weather_data = pywapi.get_weather_from_google(p3, "en")
        print weather_data
        if not weather_data.has_key('current_conditions'):
            self.LogToFile(self.text.txtGoogleWeatherUnavailable)
            return "Unavailable"
        if not weather_data['current_conditions'].has_key('condition'):
            self.LogToFile(self.text.txtGoogleWeatherUnavailable)
            return "Unavailable"
        currCondition = weather_data['current_conditions']['condition']
        return currCondition

    def LogToFile(self, s):
        timeStamp = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        logStr = timeStamp + "\t" + s + "<br\n>"

        if self.majorVersion > 5:
            progData = os.environ['ALLUSERSPROFILE']
            if not os.path.exists(progData + "/EventGhost/Log") and not os.path.isdir(progData + "/EventGhost/Log"):
                os.makedirs(progData + "/EventGhost/Log")
            fileHandle = open(progData + '/EventGhost/Log/Rain8_' + self.name + '.html', 'a')
            fileHandle.write(logStr)
            fileHandle.close()
        else:
            if not os.path.exists('Log') and not os.path.isdir('Log'):
                os.mkdir('Log')
            fileHandle = open('Log/Rain8__' + self.name + '.html', 'a')
            fileHandle.write(logStr)
            fileHandle.close()

    def ThreadWorker(self, stopThreadEvent):
        try:
            dummy
        except NameError:
            dummy = 0
            prevDate = 0

        random.jumpahead(137)

        while not stopThreadEvent.isSet():
            tr = random.random()
            remain = 61.0 - int(time.strftime("%S", time.localtime())) + tr
            #            remain = 10

            # Get the current date & time now, check if it has changed
            trigTime = str(time.strftime("%H%M", time.localtime()))
            currDate = str(time.strftime("%m/%d/%Y", time.localtime()))
            if currDate != prevDate:
                prevDate = 0

            # Get day of week
            dayType = str(self.GetDayOfWeek(currDate))

            # Check if we are in daylight savings
            idLS = self.Check_for_daylight_saving()

            # Get the weather conditions
            self.currCondition = self.CheckWeatherCondition()

            # Calculate Sunrise/Sunset times at your geographical position
            year = int(time.strftime("%Y", time.localtime()))
            month = int(time.strftime("%m", time.localtime()))
            day = int(time.strftime("%d", time.localtime()))

            # Get the sunrise/sunset times in UT and fix the format
            st = str(sunRiseSet(
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

            # Adjust the times according to your timezone and daylight savings
            tZ = int(time.timezone / 3600)

            h1 = int(int(dat1[0]) + idLS - tZ)
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

            h2 = int(int(dat2[0]) + idLS - tZ)
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
            csSR = sh1 + sm1
            csSS = sh2 + sm2
            print csSR, csSS

            # Set a flag for sun status
            if trigTime > csSS or trigTime < csSR:
                self.sunIsUp = False
            else:
                self.sunIsUp = True

            stopThreadEvent.wait(remain)

        print self.text.stopped


class Rain8Zone(eg.ActionClass):
    iconFile = 'rain8Zone'

    def __call__(
        self,
        zoneName,
        unitCode,
        runTime,
        bSu,
        bMo,
        bTu,
        bWe,
        bTh,
        bFr,
        bSa,
        nbrIntervals,
        shadowComp,
        bEnable
    ):
        self.houseCode = self.plugin.houseCode
        print self.houseCode
        return

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    # Zones on the device, 1-16
    def Configure(
        self,
        zoneName="Give the zone a name",
        unitCode='1',
        runTime=20,
        bSu=True,
        bMo=True,
        bTu=True,
        bWe=True,
        bTh=True,
        bFr=True,
        bSa=True,
        nbrIntervals=3,
        shadowComp=5,
        bEnable=True
    ):
        panel = eg.ConfigPanel(self)
        mySizer = wx.GridBagSizer(10, 10)
        txtSizer = wx.GridBagSizer(5, 5)
        daySizer = wx.GridBagSizer(5, 5)

        # name
        zoneNameCtrl = wx.TextCtrl(panel, -1, zoneName)
        zoneNameCtrl.SetInitialSize((250, -1))
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.zoneName
            ),
            (1, 0)
        )
        mySizer.Add(zoneNameCtrl, (1, 1))

        unitCode_ctrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10',
            '11',
            '12',
            '13',
            '14',
            '15',
            '16'
        ]
        if unitCode != "":
            if list.count(unitCode) == 0:
                list.append(unitCode)
        unitCode_ctrl.AppendItems(items=list)
        if list.count(unitCode) == 0:
            unitCode_ctrl.Select(n=0)
        else:
            unitCode_ctrl.SetSelection(int(list.index(unitCode)))
        unitCode_ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.text.txt_ConfUnitCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(unitCode_ctrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        runTime_ctrl = panel.SpinIntCtrl(runTime, 0, 250)
        staticBox = wx.StaticBox(panel, -1, self.text.txt_runTime)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(runTime_ctrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        txtSizer.Add(wx.StaticText(panel, -1, self.text.spDays), (1, 0))
        bSu_Ctrl = panel.CheckBox(bSu, "")
        bSu_Ctrl.SetValue(bSu)
        daySizer.Add(wx.StaticText(panel, -1, self.text.Su), (0, 0))
        daySizer.Add(bSu_Ctrl, (0, 1))
        bMo_Ctrl = panel.CheckBox(bMo, "")
        bMo_Ctrl.SetValue(bSu)
        daySizer.Add(wx.StaticText(panel, -1, self.text.Mo), (0, 2))
        daySizer.Add(bMo_Ctrl, (0, 3))
        bTu_Ctrl = panel.CheckBox(bTu, "")
        bTu_Ctrl.SetValue(bTu)
        daySizer.Add(wx.StaticText(panel, -1, self.text.Tu), (0, 4))
        daySizer.Add(bTu_Ctrl, (0, 5))
        bWe_Ctrl = panel.CheckBox(bWe, "")
        bWe_Ctrl.SetValue(bWe)
        daySizer.Add(wx.StaticText(panel, -1, self.text.We), (0, 6))
        daySizer.Add(bWe_Ctrl, (0, 7))
        bTh_Ctrl = panel.CheckBox(bTh, "")
        bTh_Ctrl.SetValue(bTh)
        daySizer.Add(wx.StaticText(panel, -1, self.text.Th), (0, 8))
        daySizer.Add(bTh_Ctrl, (0, 9))
        bFr_Ctrl = panel.CheckBox(bFr, "")
        bFr_Ctrl.SetValue(bFr)
        daySizer.Add(wx.StaticText(panel, -1, self.text.Fr), (0, 10))
        daySizer.Add(bFr_Ctrl, (0, 11))
        bSa_Ctrl = panel.CheckBox(bSa, "")
        bSa_Ctrl.SetValue(bSa)
        daySizer.Add(wx.StaticText(panel, -1, self.text.Sa), (0, 12))
        daySizer.Add(bSa_Ctrl, (0, 13))
        daySizer.Add(wx.StaticText(panel, -1, ""), (1, 0))

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)
        panel.sizer.Add(txtSizer, 1, flag=wx.EXPAND)
        panel.sizer.Add(daySizer, 1, flag=wx.EXPAND)

        nbrIntervals_ctrl = panel.SpinIntCtrl(nbrIntervals, 1, 25)
        staticBox = wx.StaticBox(panel, -1, self.text.txt_intervals)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(nbrIntervals_ctrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        shadowComp_ctrl = panel.SpinIntCtrl(shadowComp, 0, 90)
        staticBox = wx.StaticBox(panel, -1, self.text.txt_shadow)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(shadowComp_ctrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        bEnable_Ctrl = panel.CheckBox(bEnable, "")
        bEnable_Ctrl.SetValue(bEnable)
        staticBox = wx.StaticBox(panel, -1, self.text.txt_enable)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(bEnable_Ctrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            zoneName = zoneNameCtrl.GetValue()
            unitCode = unitCode_ctrl.GetStringSelection()
            runTime = runTime_ctrl.GetValue()
            bSu = bSu_Ctrl.GetValue()
            bMo = bMo_Ctrl.GetValue()
            bTu = bTu_Ctrl.GetValue()
            bWe = bWe_Ctrl.GetValue()
            bTh = bTh_Ctrl.GetValue()
            bFr = bFr_Ctrl.GetValue()
            bSa = bSa_Ctrl.GetValue()
            nbrIntervals = nbrIntervals_ctrl.GetValue()
            shadowComp = shadowComp_ctrl.GetValue()
            bEnable = bEnable_Ctrl.GetValue()

            panel.SetResult(
                zoneName,
                unitCode,
                runTime,
                bSu,
                bMo,
                bTu,
                bWe,
                bTh,
                bFr,
                bSa,
                nbrIntervals,
                shadowComp,
                bEnable
            )


class GetContentsOfVariable(eg.ActionClass):
    iconFile = 'rain8Status'

    def __call__(self):
        print "Sun is up: ", self.plugin.sunIsUp
        return self.plugin.sunIsUp


""" 
SUNRISET.C - computes Sun rise/set times, start/end of twilight, and
             the length of the day at any date and latitude
			 
Written as DAYLEN.C, 1989-08-16

Modified to SUNRISET.C, 1992-12-01
			 
(c) Paul Schlyter, 1989, 1992
			 
Released to the public domain by Paul Schlyter, December 1992
			 
Direct conversion to Java 
Sean Russell <ser@germane-software.com>

Conversion to Python Class, 2002-03-21
Henrik H�rk�nen <radix@kortis.to>

Solar Altitude added by Miguel Tremblay 2005-01-16
"""


# import math

class Sun:

    def __init__(self):
        """"""

        # Some conversion factors between radians and degrees
        self.PI = 3.1415926535897932384
        self.RADEG = 180.0 / self.PI
        self.DEGRAD = self.PI / 180.0
        self.INV360 = 1.0 / 360.0

    def daysSince2000Jan0(self, y, m, d):
        """A macro to compute the number of days elapsed since 2000 Jan 0.0
           (which is equal to 1999 Dec 31, 0h UT)"""
        return (367 * (y) - ((7 * ((y) + (((m) + 9) / 12))) / 4) + ((275 * (m)) / 9) + (d) - 730530)

    # The trigonometric functions in degrees
    def sind(self, x):
        """Returns the sin in degrees"""
        return math.sin(x * self.DEGRAD)

    def cosd(self, x):
        """Returns the cos in degrees"""
        return math.cos(x * self.DEGRAD)

    def tand(self, x):
        """Returns the tan in degrees"""
        return math.tan(x * self.DEGRAD)

    def atand(self, x):
        """Returns the arc tan in degrees"""
        return math.atan(x) * self.RADEG

    def asind(self, x):
        """Returns the arc sin in degrees"""
        return math.asin(x) * self.RADEG

    def acosd(self, x):
        """Returns the arc cos in degrees"""
        return math.acos(x) * self.RADEG

    def atan2d(self, y, x):
        """Returns the atan2 in degrees"""
        return math.atan2(y, x) * self.RADEG

    # Following are some macros around the "workhorse" function __daylen__ 
    # They mainly fill in the desired values for the reference altitude    
    # below the horizon, and also selects whether this altitude should     
    # refer to the Sun's center or its upper limb.                         

    def dayLength(self, year, month, day, lon, lat):
        """
        This macro computes the length of the day, from sunrise to sunset.
        Sunrise/set is considered to occur when the Sun's upper limb is
        35 arc minutes below the horizon (this accounts for the refraction
        of the Earth's atmosphere).
        """
        return self.__daylen__(year, month, day, lon, lat, -35.0 / 60.0, 1)

    def dayCivilTwilightLength(self, year, month, day, lon, lat):
        """
        This macro computes the length of the day, including civil twilight.
        Civil twilight starts/ends when the Sun's center is 6 degrees below
        the horizon.
        """
        return self.__daylen__(year, month, day, lon, lat, -6.0, 0)

    def dayNauticalTwilightLength(self, year, month, day, lon, lat):
        """
        This macro computes the length of the day, incl. nautical twilight.
        Nautical twilight starts/ends when the Sun's center is 12 degrees
        below the horizon.
        """
        return self.__daylen__(year, month, day, lon, lat, -12.0, 0)

    def dayAstronomicalTwilightLength(self, year, month, day, lon, lat):
        """
        This macro computes the length of the day, incl. astronomical twilight.
        Astronomical twilight starts/ends when the Sun's center is 18 degrees
        below the horizon.
        """
        return self.__daylen__(year, month, day, lon, lat, -18.0, 0)

    def sunRiseSet(self, year, month, day, lon, lat):
        """
        This macro computes times for sunrise/sunset.
        Sunrise/set is considered to occur when the Sun's upper limb is
        35 arc minutes below the horizon (this accounts for the refraction
        of the Earth's atmosphere).
        """
        return self.__sunriset__(year, month, day, lon, lat, -35.0 / 60.0, 1)

    def civilTwilight(self, year, month, day, lon, lat):
        """
        This macro computes the start and end times of civil twilight.
        Civil twilight starts/ends when the Sun's center is 6 degrees below
        the horizon.
        """
        return self.__sunriset__(year, month, day, lon, lat, -6.0, 0)

    def nauticalTwilight(self, year, month, day, lon, lat):
        """
        This macro computes the start and end times of nautical twilight.
        Nautical twilight starts/ends when the Sun's center is 12 degrees
        below the horizon.
        """
        return self.__sunriset__(year, month, day, lon, lat, -12.0, 0)

    def astronomicalTwilight(self, year, month, day, lon, lat):
        """
        This macro computes the start and end times of astronomical twilight.
        Astronomical twilight starts/ends when the Sun's center is 18 degrees
        below the horizon.
        """
        return self.__sunriset__(year, month, day, lon, lat, -18.0, 0)

    # The "workhorse" function for sun rise/set times
    def __sunriset__(self, year, month, day, lon, lat, altit, upper_limb):
        """
        Note: year,month,date = calendar date, 1801-2099 only.
              Eastern longitude positive, Western longitude negative
                  Northern latitude positive, Southern latitude negative
              The longitude value IS critical in this function!
              altit = the altitude which the Sun should cross
                      Set to -35/60 degrees for rise/set, -6 degrees
                  for civil, -12 degrees for nautical and -18
                  degrees for astronomical twilight.
                upper_limb: non-zero -> upper limb, zero -> center
                  Set to non-zero (e.g. 1) when computing rise/set
                  times, and to zero when computing start/end of
                  twilight.
              *rise = where to store the rise time
              *set  = where to store the set  time
                      Both times are relative to the specified altitude,
                  and thus this function can be used to compute
                  various twilight times, as well as rise/set times
        Return value:  0 = sun rises/sets this day, times stored at
                               *trise and *tset.
                  +1 = sun above the specified 'horizon' 24 hours.
                       *trise set to time when the sun is at south,
                   minus 12 hours while *tset is set to the south
                   time plus 12 hours. 'Day' length = 24 hours
                  -1 = sun is below the specified 'horizon' 24 hours
                       'Day' length = 0 hours, *trise and *tset are
                    both set to the time when the sun is at south.
        """
        # Compute d of 12h local mean solar time
        d = self.daysSince2000Jan0(year, month, day) + 0.5 - (lon / 360.0)

        # Compute local sidereal time of this moment
        sidtime = self.revolution(self.GMST0(d) + 180.0 + lon)

        # Compute Sun's RA + Decl at this moment
        res = self.sunRADec(d)
        sRA = res[0]
        sdec = res[1]
        sr = res[2]

        # Compute time when Sun is at south - in hours UT
        tsouth = 12.0 - self.rev180(sidtime - sRA) / 15.0;

        # Compute the Sun's apparent radius, degrees
        sradius = 0.2666 / sr;

        # Do correction to upper limb, if necessary
        if upper_limb:
            altit = altit - sradius

        # Compute the diurnal arc that the Sun traverses to reach
        # the specified altitude altit:

        cost = (self.sind(altit) - self.sind(lat) * self.sind(sdec)) / \
               (self.cosd(lat) * self.cosd(sdec))

        if cost >= 1.0:
            rc = -1
            t = 0.0  # Sun always below altit

        elif cost <= -1.0:
            rc = +1
            t = 12.0;  # Sun always above altit

        else:
            t = self.acosd(cost) / 15.0  # The diurnal arc, hours

        # Store rise and set times - in hours UT
        return (tsouth - t, tsouth + t)

    def __daylen__(self, year, month, day, lon, lat, altit, upper_limb):
        """
        Note: year,month,date = calendar date, 1801-2099 only.
              Eastern longitude positive, Western longitude negative
              Northern latitude positive, Southern latitude negative
              The longitude value is not critical. Set it to the correct
              longitude if you're picky, otherwise set to, say, 0.0
              The latitude however IS critical - be sure to get it correct
              altit = the altitude which the Sun should cross
                      Set to -35/60 degrees for rise/set, -6 degrees
                      for civil, -12 degrees for nautical and -18
                      degrees for astronomical twilight.
                upper_limb: non-zero -> upper limb, zero -> center
                      Set to non-zero (e.g. 1) when computing day length
                      and to zero when computing day+twilight length.

        """

        # Compute d of 12h local mean solar time
        d = self.daysSince2000Jan0(year, month, day) + 0.5 - (lon / 360.0)

        # Compute obliquity of ecliptic (inclination of Earth's axis)
        obl_ecl = 23.4393 - 3.563E-7 * d

        # Compute Sun's position
        res = self.sunpos(d)
        slon = res[0]
        sr = res[1]

        # Compute sine and cosine of Sun's declination
        sin_sdecl = self.sind(obl_ecl) * self.sind(slon)
        cos_sdecl = math.sqrt(1.0 - sin_sdecl * sin_sdecl)

        # Compute the Sun's apparent radius, degrees
        sradius = 0.2666 / sr

        # Do correction to upper limb, if necessary
        if upper_limb:
            altit = altit - sradius

        cost = (self.sind(altit) - self.sind(lat) * sin_sdecl) / (self.cosd(lat) * cos_sdecl)
        if cost >= 1.0:
            t = 0.0  # Sun always below altit

        elif cost <= -1.0:
            t = 24.0  # Sun always above altit

        else:
            t = (2.0 / 15.0) * self.acosd(cost);  # The diurnal arc, hours

        return t

    def sunpos(self, d):
        """
        Computes the Sun's ecliptic longitude and distance
        at an instant given in d, number of days since
        2000 Jan 0.0.  The Sun's ecliptic latitude is not
        computed, since it's always very near 0.
        """

        # Compute mean elements
        M = self.revolution(356.0470 + 0.9856002585 * d)
        w = 282.9404 + 4.70935E-5 * d
        e = 0.016709 - 1.151E-9 * d

        # Compute true longitude and radius vector
        E = M + e * self.RADEG * self.sind(M) * (1.0 + e * self.cosd(M))
        x = self.cosd(E) - e
        y = math.sqrt(1.0 - e * e) * self.sind(E)
        r = math.sqrt(x * x + y * y)  # Solar distance
        v = self.atan2d(y, x)  # True anomaly
        lon = v + w  # True solar longitude
        if lon >= 360.0:
            lon = lon - 360.0  # Make it 0..360 degrees

        return (lon, r)

    def sunRADec(self, d):
        """"""

        # Compute Sun's ecliptical coordinates
        res = self.sunpos(d)
        lon = res[0]
        r = res[1]

        # Compute ecliptic rectangular coordinates (z=0)
        x = r * self.cosd(lon)
        y = r * self.sind(lon)

        # Compute obliquity of ecliptic (inclination of Earth's axis)
        obl_ecl = 23.4393 - 3.563E-7 * d

        # Convert to equatorial rectangular coordinates - x is unchanged
        z = y * self.sind(obl_ecl)
        y = y * self.cosd(obl_ecl)

        # Convert to spherical coordinates
        RA = self.atan2d(y, x)
        dec = self.atan2d(z, math.sqrt(x * x + y * y))

        return (RA, dec, r)

    def revolution(self, x):
        """
        This function reduces any angle to within the first revolution
        by subtracting or adding even multiples of 360.0 until the
        result is >= 0.0 and < 360.0

        Reduce angle to within 0..360 degrees
        """
        return (x - 360.0 * math.floor(x * self.INV360))

    def rev180(self, x):
        """
        Reduce angle to within +180..+180 degrees
        """
        return (x - 360.0 * math.floor(x * self.INV360 + 0.5))

    def GMST0(self, d):
        """
        This function computes GMST0, the Greenwich Mean Sidereal Time
        at 0h UT (i.e. the sidereal time at the Greenwhich meridian at
        0h UT).  GMST is then the sidereal time at Greenwich at any
        time of the day.  I've generalized GMST0 as well, and define it
        as:  GMST0 = GMST - UT  --  this allows GMST0 to be computed at
        other times than 0h UT as well.  While this sounds somewhat
        contradictory, it is very practical:  instead of computing
        GMST like:

         GMST = (GMST0) + UT * (366.2422/365.2422)

        where (GMST0) is the GMST last time UT was 0 hours, one simply
        computes:

         GMST = GMST0 + UT

        where GMST0 is the GMST "at 0h UT" but at the current moment!
        Defined in this way, GMST0 will increase with about 4 min a
        day.  It also happens that GMST0 (in degrees, 1 hr = 15 degr)
        is equal to the Sun's mean longitude plus/minus 180 degrees!
        (if we neglect aberration, which amounts to 20 seconds of arc
        or 1.33 seconds of time)
        """
        # Sidtime at 0h UT = L (Sun's mean longitude) + 180.0 degr
        # L = M + w, as defined in sunpos().  Since I'm too lazy to
        # add these numbers, I'll let the C compiler do it for me.
        # Any decent C compiler will add the constants at compile
        # time, imposing no runtime or code overhead.

        sidtim0 = self.revolution((180.0 + 356.0470 + 282.9404) +
                                  (0.9856002585 + 4.70935E-5) * d)
        return sidtim0;

    def solar_altitude(self, latitude, year, month, day):
        """
        Compute the altitude of the sun. No atmospherical refraction taken
        in account.
        Altitude of the southern hemisphere are given relative to
        true north.
        Altitude of the northern hemisphere are given relative to
        true south.
        Declination is between 23.5� North and 23.5� South depending
        on the period of the year.
        Source of formula for altitude is PhysicalGeography.net
        http://www.physicalgeography.net/fundamentals/6h.html
        """
        # Compute declination
        N = self.daysSince2000Jan0(year, month, day)
        res = self.sunRADec(N)
        declination = res[1]
        sr = res[2]

        # Compute the altitude
        altitude = 90.0 - latitude + declination

        # In the tropical and  in extreme latitude, values over 90 may occurs.
        if altitude > 90:
            altitude = 90 - (altitude - 90)

        if altitude < 0:
            altitude = 0

        return altitude


# if __name__ == "__main__":
#    k = Sun()
#    print k.sunRiseSet(2002, 3, 22, 25.42, 62.15)


# Modification for export of function when used in EG
# 2008-04-22 krambriw
k = Sun()
sunRiseSet = k.sunRiseSet

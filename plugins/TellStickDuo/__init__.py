# -*- coding: utf-8 -*-
#
# plugins/TellStickDuo/__init__.py
#
# Copyright (C) 2010 Telldus Technologies
#
##############################################################################
# Revision history:
#
# 2017-01-06  Added new action 'Save device dim level'. Allows keeping track
#             of level when controlled externally via on/off remote or button. 
#             Supports on/off levels (0 and 255)
# 2016-11-30  Introduced a buffer for sending commands 
# 2016-11-16  Bugfix in action GoodMorning (did not end with 100% dim level) 
# 2016-10-21  Bugfix in action ToggleOnOffWithTimer 
# 2016-04-09  Improved handling of fineoffset temperature & humidity sensors 
# 2016-02-08  Added new action ToggleOnOffWithTimer. Allows toggeling with 
#             delayed on/off
# 2015-02-13  Monitoring of disconnection/connection of TellStick devices
#             added.
# 2014-10-03  Improved GoodMorning & GoodNight actions:
#             - configurable max level for GoodMorning action
#             - selectable option for the GoodNight action to start dimming
#               from the current known (Telldus Center) level
# 2014-04-08  Added functions to generate event when GoodMorning & GoodNight
#             actions have finished
# 2014-03-08  Synchronizing current saved dim levels when adding/deleting
#             devices using Telldus Center
# 2014-02-17  Added dictionary to keep id, level and name of dimmable devices
# 2014-02-16  Dim levels for devices are now kept synchronized
# 2014-02-15  Added action to dim devices up/down in defined percentage steps
#             Saving the level persistent
# 2013-12-29  Added support for Oregon rain and wind sensors
# 2013-10-14  Added light level to dim events.
# 2013-05-24  Changed format of Oregon and UPM/ESIC events, now combining
#             temperature and humidity readings into one single event.
# 2013-03-11  You can now specify the devices you like to remember states for.
#             Just put in the Telldus Center name of the device in the list in
#             the separate python file 'devices_in_state_memory.py' and the
#             state will be captured to avoid multiple duplicated events.
#             State changes will be captured only for devices listed in this
#             file. 
#             This is useful especially with devices that sends many events
#             for each state change (like magnetic contacts, infra red
#             detectors, pushbuttons and others).
# 2013-02-17  Added an action to gradually dim self learning devices.
# 2013-01-14  Added an action to toggle devices on/off.
# 2013-01-11  Disabled the code for the message box "Restart of EG needed".
#             Added a wait after resume to allow needed services and drivers
#             to recover properly.
# 2013-01-10  Handling of unicode chars in device names.
# 2013-01-05  Introduced functions that hopefully will improve situations when
#             the PC is suspended and resumes.
#             Added actions to stop Good Morning and Good Night schedules.
#             Modified the monitoring of Telldus service. The solution is
#             now based on an dynamic and adaptive method, counting sensor
#             events and measuring the time between. Based on this,
#             calculating an estimated forecast for next expected event to
#             happen. Please note, this feature requires that you have 
#             at least one compatible temperatur sensor that is within range.
# 2012-12-02  Device and sensor messages are now saved and compared with
#             previous reading. EG events are only generated when the reading
#             differs from previous.
#             Supported sensor brands are listed in the separate python file
#             sensors_supported.py which allows you to customize filtering.
#             Events for devices and sensors can now be enabled individually.
# 2012-10-27  Logfile enabled for debugging purposes.
# 2012-09-16  Added monitoring of Telldus service.
# 2012-09-08  Improved the handling of repeated events for devices and sensors.
# 2012-08-14  Added actions for dimming Good Morning and Good Night lamps.
#             (works with AC devices like NEXA with support for setting dim
#             levels).
# 2012-07-01  Moving event callback initiators from init to start method.
#             Enabled UnregisterCallbacks in stop method.
# 2012-02-26  Changing the dim level now also updates the macro name with
#             correct % level.
#             Dimmer function 100% represents full dim level, 0% is off. 
# 2012-01-26  Checkboxes for selection of event types and blocking of repeats
#             did not work correctly.
# 2012-01-24  Added support for UP/DOWN/STOP actions.
# 2011-11-14  Using device names as keys instead of device id's.
#             Changed the slider for dim to show 0-100% dim level.
#             Improved the blocking of repeated events, blocking all repeated
#             events within the defined time frame except change events.
# 2011-10-28  Blocking repeated events: configuration option added.
# 2011-10-26  Blocking repeated events within 0.3 seconds.
# 2011-10-18  Added support for temperature/humidity sensors.
#             Events are now also generated if transmission exceptions occurs.
# 2011-03-26  Improved dll-call handlings.
# 2011-02-25  Improved the dimmer function (0% is off, 255% is on).
# 2010-12-14  Fixed to work with -translate switch in EG.
# 2010-09-17  Added settings to select events to be logged & beep on events.
#             Added settings for logfile name & path.
#             Added support for Tellstick Duo id number.
# 2010-05-10  Experimental with callbacks.

eg.RegisterPlugin(
    name = "TellStickDuo",
    guid = '{197BDE4F-0F1A-446C-B8EE-18FDB5077A56}',
    author = "Micke Prag & Walter Kraembring",
    version = "0.4.0",
    kind = "external",
    url = "http://www.eventghost.org/forum",
    description = 'Plugin for TellStick Duo',
    help = """
        <a href="http://www.telldus.se">Telldus Homepage</a>
        
        <center><img src="TellStickDuo.png" /></center>
    """,
)

#Device methods
TELLSTICK_SUCCESS      = 0
TELLSTICK_TURNON       = 1
TELLSTICK_TURNOFF      = 2
TELLSTICK_BELL         = 4
TELLSTICK_TOGGLE       = 8
TELLSTICK_DIM          = 16
TELLSTICK_LEARN        = 32
TELLSTICK_EXECUTE      = 64
TELLSTICK_UP           = 128
TELLSTICK_DOWN         = 256
TELLSTICK_STOP         = 512

#Sensor value types
TELLSTICK_TEMPERATURE = 1
TELLSTICK_HUMIDITY = 2
TELLSTICK_RAINRATE = 4
TELLSTICK_RAINTOTAL = 8
TELLSTICK_WINDDIRECTION = 16
TELLSTICK_WINDAVERAGE = 32
TELLSTICK_WINDGUST = 64

#Error codes
TELLSTICK_SUCCESS =                       0
TELLSTICK_ERROR_NOT_FOUND =              -1
TELLSTICK_ERROR_PERMISSION_DENIED =      -2
TELLSTICK_ERROR_DEVICE_NOT_FOUND =       -3
TELLSTICK_ERROR_METHOD_NOT_SUPPORTED =   -4
TELLSTICK_ERROR_COMMUNICATION =          -5
TELLSTICK_ERROR_CONNECTING_SERVICE =     -6
TELLSTICK_ERROR_UNKNOWN_RESPONSE =       -7
TELLSTICK_ERROR_SYNTAX =                 -8
TELLSTICK_ERROR_BROKEN_PIPE =            -9
TELLSTICK_ERROR_COMMUNICATING_SERVICE = -10
TELLSTICK_ERROR_CONFIG_SYNTAX =         -11
TELLSTICK_ERROR_UNKNOWN =               -99

#Controller types
TELLSTICK_CONTROLLER_TELLSTICK =          1
TELLSTICK_CONTROLLER_TELLSTICK_DUO =      2
TELLSTICK_CONTROLLER_TELLSTICK_NET =      3

#Device changes
TELLSTICK_DEVICE_ADDED =                  1
TELLSTICK_DEVICE_CHANGED =                2
TELLSTICK_DEVICE_REMOVED =                3
TELLSTICK_DEVICE_STATE_CHANGED =          4

#Change types
TELLSTICK_CHANGE_NAME =                   1
TELLSTICK_CHANGE_PROTOCOL =               2
TELLSTICK_CHANGE_MODEL =                  3
TELLSTICK_CHANGE_METHOD =                 4
TELLSTICK_CHANGE_AVAILABLE =              5
TELLSTICK_CHANGE_FIRMWARE =               6


import time, winsound, os, devices_in_state_memory
from ctypes import(
	windll, WINFUNCTYPE, POINTER, string_at,
	wstring_at, c_char_p, c_int, c_ubyte, c_void_p	
)
from datetime import datetime
from win32gui import MessageBox
from threading import Event, Thread



class Text:
    init_exception_txt = "TelldusCore.dll not found."
    init_txt = "Initiating TellStick Duo..."
    starting_up_txt = "Starting up..."
    starting_txt = "Starting TellStick Duo..."
    disable_txt = "Disables TellStick Duo..."
    closing_txt = "Closing TellStick Duo..."
    sensor_callbacks_lost = "Expected TellStick Duo sensor callbacks ended, restart Telldus service..."
    sensor_callbacks_back = "Recovered TellStick Duo sensor callbacks"
    controller_dwn = 'Communication with controller is down'
    controller_up = 'Communication with controller is up'
    restart_title = "Restart of EG needed"
    restart_eg = (
        "Please finish and save the configuration and then restart "
        +"EventGhost to enable the event receiving capabilities in "
        +"TellStick Duo."
    )

    ON_txt = "ON"
    OFF_txt = "OFF"
    DIM_txt = "DIM"
    BELL_txt = "BELL"
    UP_txt = "UP"
    DOWN_txt = "DOWN"
    STOP_txt = "STOP"

    log_device_events = "Check to log device events"
    log_sensor_events = "Check to log sensor events"
    log_delayRepeat = "Delay between events (0.1-15.0 s)"
    log_change_events = "Check to log change events"
    log_raw_events = "Check to log raw events"
    beep_device_events = "Check to beep on device events"
    keyAdded = "Key added to dictionary"

    debug = "Check to log to logfile"
    device_txt = "Device:"
    delayOff_txt = "Time delay before switching off or on (depending on current state):"
    delayOn_txt = "Time delay before switching on or off (depending on current state):"
    retry_txt = "Retry nbr: "
    exception_txt = "An error occurred while trying to transmit"
    no_device_txt_1 =  "There is no device supporting '"
    no_device_txt_2 =  "'"
    no_device_txt_3 =  " . Click CANCEL to close dialogue"

    class Dim:
        dim_txt_1 = "Dim " 
        dim_txt_2 = " to "
        dim_txt_3 = "%"
        level_txt = "Dim level (%): "

    class DimGradually:
        dim_txt_1 = "Dim " 
        dim_txt_2 = " to "
        dim_txt_3 = "%"
        level_txt = "Dim level (%): "
        timeInBetween_txt = "Select the time delay between dim level commands"
        txtStep = "Select the step size for the dim level commands (1-34)"

    class GoodMorning:
        dim_txt_1 = "Good morning " 
        dim_txt_2 = "in "
        dim_txt_3 = " minutes"
        timeToWakeUp_txt = "Total snooze time (minutes): "
        maxWakeUpLevel_txt = "Set the maximum level for the lights: "

    class StopGoodMorning:
        info = "Stopping all running Good Morning schedules..."

    class GoodNight:
        dim_txt_1 = "Good night " 
        dim_txt_2 = "in "
        dim_txt_3 = " minutes"
        timeToSleep_txt = "Total snooze time (minutes): "
        startFromCurrent_txt = "Start dimming from current known level: "

    class StopGoodNight:
        info = "Stopping all running Good Night schedules..."

    class DimPercentage:
        step_up = "Check to dim up "
        level_txt = "Set the step size (0-255): "



CONTROLLEREVENTPROC = WINFUNCTYPE(
                                        c_void_p,
                                        c_int,
                                        c_int,
                                        c_int,
                                        POINTER(c_ubyte),
                                        c_int,
                                        c_void_p
                     )

DEVICEEVENTPROC = WINFUNCTYPE(
                                        c_void_p,
                                        c_int,
                                        c_int,
                                        POINTER(c_ubyte),
                                        c_int,
                                        c_void_p
                     )

SENSOREVENTPROC = WINFUNCTYPE(
                                        c_void_p,
                                        POINTER(c_ubyte),
                                        POINTER(c_ubyte),
                                        c_int,
                                        c_int,
                                        POINTER(c_ubyte),
                                        c_int,
                                        c_int,
                                        c_void_p
                     )

DEVICECHANGEEVENTPROC = WINFUNCTYPE(
                                        c_void_p,
                                        c_int,
                                        c_int,
                                        c_int,
                                        c_int,
                                        c_void_p
                    )

RAWDEVICEEVENTPROC = WINFUNCTYPE(
                                        c_void_p,
                                        POINTER(c_ubyte),
                                        c_int,
                                        c_int,
                                        c_void_p
                     )



class CurrentStateData(eg.PersistentData):
    device_state_memory = {}
    sensor_state_memory = {}
    sensor_time_average = []
    dimGradually = {}
    dimPercentage = {}
    dimDeviceData = {}



class TellStickDuo(eg.PluginClass):
    text = Text
    taskObj = None
 
    def __init__(self):
        self.AddAction(GoodMorning)
        self.AddAction(StopGoodMorning)
        self.AddAction(GoodNight)
        self.AddAction(StopGoodNight)
        self.AddAction(SaveDimLevel)
        self.AddAction(TurnOn)
        self.AddAction(Dim)
        self.AddAction(DimGradually)
        self.AddAction(DimPercentage)
        self.AddAction(TurnOff)
        self.AddAction(ToggleOnOff)
        self.AddAction(ToggleOnOffWithTimer)
        self.AddAction(Bell)
        self.AddAction(MoveUp)
        self.AddAction(MoveDown)
        self.AddAction(Stop)
 

    def __start__(
        self,
        bDeviceEvents,
        bChangeEvents,
        bRawEvents,
        beepOnEvent,
        bDebug,
        delayRepeat,
        bSensorEvents
    ):
        #Get the defined sensor types to be supported
        import sensors_supported
        self.sensors_supported = sensors_supported.sensors_supported()

        #Get the defined devices to be status monitored
        self.devices_in_state_memory = devices_in_state_memory.devices_supported()

        self.dimGradually = CurrentStateData.dimGradually
        self.dimPercentage = CurrentStateData.dimPercentage
        self.dimDeviceData = CurrentStateData.dimDeviceData
        self.device_state_memory = CurrentStateData.device_state_memory
        self.sensor_state_memory = CurrentStateData.sensor_state_memory

        self.sensorEventTime = 0
        self.sensorEventTimeAverage = CurrentStateData.sensor_time_average

        self.bControllerEvents = True
        self.bDeviceEvents = bDeviceEvents
        self.bSensorEvents = bSensorEvents
        self.bChangeEvents = bChangeEvents
        self.bRawEvents = bRawEvents
        self.beepOnEvent = beepOnEvent
        self.bDebug = bDebug
        self.delayRepeat = delayRepeat

        self.oldDeviceEventCollection = []
        self.oldDeviceSensorEventCollection = []

        self.bTaskAddedRaw = False
        self.oldDeviceEventRaw = ''

        self.taskObj = None
        self.taskObjSensors = None
        self.taskObjRaw = None
        
        self.sensorMonitor = None
        self.gMschedules = False
        self.gNschedules = False
                
        self.ch_name_device = 0.0
        self.dll = None
        self.callbackId_0 = None
        self.callbackId_1 = None
        self.callbackId_2 = None
        self.callbackId_3 = None
        self.callbackId_4 = None
        self.callbacksLost = False
        self.loadLibrary()
        self.registerCallbacks()
        self.controller = []
        self.mandolynEventStr = ['']*7
        self.fineoffsetEventID = ''
        self.foTempHumEventStr = ['']*7
        self.oregonEventID = ''
        self.orTempHumEventStr = ['']*7
        self.orWindEventStr = ['']*9
        self.orRainEventStr = ['']*7
        self.otherEventStr = ['']*7
        self.queu = []
        print self.text.init_txt
        print self.text.starting_txt
        self.syncDimData()


    def __stop__(self):
        CurrentStateData.dimDeviceData = self.dimDeviceData 
        self.unregisterCallbacks()
        self.CancelTasks()
        self.closeLibrary()
        print self.text.disable_txt
        time.sleep(2.0)
        
   
    def __close__(self):
        print self.text.closing_txt

        
    def OnComputerSuspend(self, suspendType):
        """
        Prepares the plugin for suspension of the computer.
        """
        print "Suspending...", suspendType
        self.__stop__()


    def OnComputerResume(self, suspendType):
        """
        Prepares the plugin for resumption of the computer.
        """
        print "Resuming...", suspendType
        print "Please wait 5 seconds, drivers and services are recovering..."
        time.sleep(5.0)
        self.__start__(
            self.bDeviceEvents,
            self.bChangeEvents,
            self.bRawEvents,
            self.beepOnEvent,
            self.bDebug,
            self.delayRepeat,
            self.bSensorEvents
        )


    def SaveDevicePersistent(self, msg, m_key):
        #Make status data persistent if it has changed
        m = msg.split('|')
        tr_e = False
        bFound = False

        for i in self.devices_in_state_memory:
            if msg.find(i) <> -1:
                bFound = True

        if bFound:
            try:
                if msg != self.device_state_memory[m_key]:
                    self.device_state_memory[m_key] = msg
                    tr_e = True
            except KeyError:
                if self.bDebug:
                    print self.text.keyAdded
                self.device_state_memory[m_key] = msg
                tr_e = True
            
            if tr_e and self.bDeviceEvents:
                self.TriggerEvent(
                    (m[0]+'.'+m[1]).decode('utf-8'),
                    payload=(
                        (m[2]+'.'+m[3]+'.'+m[4]).decode('utf-8')
                    )
                )

        if not bFound:
            if self.bDeviceEvents:
                self.TriggerEvent(
                    (m[0]+'.'+m[1]).decode('utf-8'),
                    payload=(
                        (m[2]+'.'+m[3]+'.'+m[4]).decode('utf-8')
                    )
                )

        self.LogToFile(
            (m[0]+'.'+m[1]+'.'+m[2]+'.'+m[3]+'.'+m[4])
        )
        if self.beepOnEvent:
            winsound.Beep(1000, 20)                


    def SaveMandolynSensorPersistent(self, msg, m_key):
        #Make status data persistent if it has changed
        m = msg
        tr_e = False
        try:
            if msg != self.sensor_state_memory[m_key]:
                self.sensor_state_memory[m_key] = msg
            tr_e = True
        except KeyError:
            if self.bDebug:
                print self.text.keyAdded
            self.sensor_state_memory[m_key] = msg
            tr_e = True

        if tr_e and self.bSensorEvents:
            self.TriggerEvent(
                m[0]+'.'+m[1]+'.'+m[2]+'.'+
                m[3]+'.'+m[4],
                payload=(
                    m[5]+'|'+m[6]
                )
            )
            self.LogToFile(
                m[0]+'.'+m[1]+'.'+m[2]+'.'+
                m[3]+'.'+m[4]+'.'+m[5]+'_'+m[6]
            )
            if self.beepOnEvent:
                winsound.Beep(150, 30)                


    def SaveFineOffsetTHSensor(self, msg, m_key):
        #Make status data persistent if it has changed
        m = msg
        #print 'm: ', m
        tr_e = False
        try:
            if msg != self.sensor_state_memory[m_key]:
                self.sensor_state_memory[m_key] = msg
            tr_e = True
        except KeyError:
            if self.bDebug:
                print self.text.keyAdded
            self.sensor_state_memory[m_key] = msg
            tr_e = True

        if tr_e and self.bSensorEvents:
            self.TriggerEvent(
                m[0]+'.'+m[1]+'.'+m[2]+'.'+
                m[3]+'.'+m[4],
                payload=(
                    m[5]+'|'+m[6]
                )
            )
            self.LogToFile(
                m[0]+'.'+m[1]+'.'+m[2]+'.'+
                m[3]+'.'+m[4]+'.'+m[5]+'_'+m[6]
            )
            if self.beepOnEvent:
                winsound.Beep(150, 30)                


    def SaveOregonTHSensor(self, msg, m_key):
        #Make status data persistent if it has changed
        m = msg
        #print 'm: ', m
        tr_e = False
        try:
            if msg != self.sensor_state_memory[m_key]:
                self.sensor_state_memory[m_key] = msg
            tr_e = True
        except KeyError:
            if self.bDebug:
                print self.text.keyAdded
            self.sensor_state_memory[m_key] = msg
            tr_e = True

        if tr_e and self.bSensorEvents:
            self.TriggerEvent(
                m[0]+'.'+m[1]+'.'+m[2]+'.'+
                m[3]+'.'+m[4],
                payload=(
                    m[5]+'|'+m[6]
                )
            )
            self.LogToFile(
                m[0]+'.'+m[1]+'.'+m[2]+'.'+
                m[3]+'.'+m[4]+'.'+m[5]+'_'+m[6]
            )
            if self.beepOnEvent:
                winsound.Beep(150, 30)                


    def SaveOregonRainSensor(self, msg, m_key):
        #Make status data persistent if it has changed
        m = msg
        #print 'm: ', m
        tr_e = False
        try:
            if msg != self.sensor_state_memory[m_key]:
                self.sensor_state_memory[m_key] = msg
            tr_e = True
        except KeyError:
            if self.bDebug:
                print self.text.keyAdded
            self.sensor_state_memory[m_key] = msg
            tr_e = True

        if tr_e and self.bSensorEvents:
            self.TriggerEvent(
                m[0]+'.'+m[1]+'.'+m[2]+'.'+
                m[3]+'.'+m[5],
                payload=(
                    m[4]+'|'+m[6]
                )
            )
            self.LogToFile(
                m[0]+'.'+m[1]+'.'+m[2]+'.'+
                m[3]+'.'+m[5]+'.'+m[4]+'_'+m[6]
            )
            if self.beepOnEvent:
                winsound.Beep(150, 30)                


    def SaveOregonWindSensor(self, msg, m_key):
        #Make status data persistent if it has changed
        m = msg
        #print 'm: ', m
        tr_e = False
        try:
            if msg != self.sensor_state_memory[m_key]:
                self.sensor_state_memory[m_key] = msg
            tr_e = True
        except KeyError:
            if self.bDebug:
                print self.text.keyAdded
            self.sensor_state_memory[m_key] = msg
            tr_e = True

        if tr_e and self.bSensorEvents:
            self.TriggerEvent(
                m[0]+'.'+m[1]+'.'+m[2]+'.'+
                m[3]+'.'+m[5]+'.'+m[7],
                payload=(
                    m[4]+'|'+m[6]+'|'+m[8]
                )
            )
            self.LogToFile(
                m[0]+'.'+m[1]+'.'+m[2]+'.'+
                m[3]+'.'+m[5]+'.'+m[7]+'_'+
                m[4]+'.'+m[6]+'_'+m[8]
            )
            if self.beepOnEvent:
                winsound.Beep(150, 30)                


    def SaveOtherSensorPersistent(self, msg, m_key):
        #Make status data persistent if it has changed
        m = msg.split('|')
        tr_e = False
        try:
            if msg != self.sensor_state_memory[m_key]:
                self.sensor_state_memory[m_key] = msg
            tr_e = True
        except KeyError:
            if self.bDebug:
                print self.text.keyAdded
            self.sensor_state_memory[m_key] = msg
            tr_e = True

        if tr_e and self.bSensorEvents:
            self.TriggerEvent(
                m[0]
                +'.'
                +m[1]
                +'.'
                +m[2]
                +'.'
                +m[3],
                payload=(
                    m[4]
                )
            )
            self.LogToFile(
                m[0]+'.'+m[1]+'.'+m[2]+'.'+
                m[3]+'.'+m[4]
            )
            if self.beepOnEvent:
                winsound.Beep(150, 30)                


    def loadLibrary(self):
        print "Loading library"
        try:
            self.dll = windll.LoadLibrary("TelldusCore.dll")
        except: 
            raise eg.Exception(self.text.init_exception_txt)

        self.dll.tdInit()

        self.controllerEventProc = CONTROLLEREVENTPROC(
                                        self.controllerEventCallback
                               )
        self.deviceEventProc = DEVICEEVENTPROC(
                                        self.deviceEventCallback
                               )
        self.deviceChangeEventProc = DEVICECHANGEEVENTPROC(
                                            self.deviceChangeEventCallback
                                     )
        self.deviceRawEventProc = RAWDEVICEEVENTPROC(
                                        self.deviceRawEventCallback
                                  )
        self.sensorEventProc = SENSOREVENTPROC(
                                        self.sensorEventCallback
                               )


    def closeLibrary(self):
        try:
            self.dll.tdClose()
            print "Closing library"
        except:
            pass
        self.dll = None

        
    def registerCallbacks(self):
        try:
            self.callbackId_0 = self.dll.tdRegisterDeviceEvent(
                                            self.deviceEventProc,
                                            0
                                )
        except: 
            print self.text.restart_title
#            MessageBox(0, self.text.restart_eg, self.text.restart_title, 0)
        try:
            self.callbackId_1 = self.dll.tdRegisterDeviceChangeEvent(
                                            self.deviceChangeEventProc,
                                            0
                                )        
        except: 
            pass
        try:
            self.callbackId_2 = self.dll.tdRegisterRawDeviceEvent(
                                            self.deviceRawEventProc,
                                            0
                                )        
        except: 
            pass
        try:
            self.callbackId_3 = self.dll.tdRegisterSensorEvent(
                                            self.sensorEventProc,
                                            0
                                )        
        except: 
            pass
        try:
            self.callbackId_4 = self.dll.tdRegisterControllerEvent(
                                            self.controllerEventProc,
                                            0
                                )        
        except: 
            pass


    def unregisterCallbacks(self):
        self.dll.tdUnregisterCallback( self.callbackId_0 )
        self.dll.tdUnregisterCallback( self.callbackId_1 )
        self.dll.tdUnregisterCallback( self.callbackId_2 )
        self.dll.tdUnregisterCallback( self.callbackId_3 )
        self.dll.tdUnregisterCallback( self.callbackId_4 )
        self.callbackId_0 = None
        self.callbackId_1 = None
        self.callbackId_2 = None
        self.callbackId_3 = None
        self.callbackId_4 = None
    

    def CancelTasks(self):
        try:
            eg.scheduler.CancelTask(self.taskObj)
        except ValueError:
            pass
        try:
            eg.scheduler.CancelTask(self.taskObjSensors)
        except ValueError:
            pass
        try:
            eg.scheduler.CancelTask(self.taskObjRaw)
        except ValueError:
            pass
        try:
            eg.scheduler.CancelTask(self.sensorMonitor)
        except ValueError:
            pass


    def ClearFlagRaw(self):
        #print "Clear FlagRaw", self.bTaskAddedRaw
        self.bTaskAddedRaw = False


    def RemoveEventFromCollection(self, item):
        try:
            self.oldDeviceEventCollection.remove(item)
        except:
            pass


    def RemoveSensorEventFromCollection(self, item):
        try:
            self.oldDeviceSensorEventCollection.remove(item)
        except:
            pass


    def LogToFile(self, s):
        if self.bDebug:
            s = s.decode('utf-8')
            timeStamp = str(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            logStr = timeStamp+"\t"+s+"<br\n>"
            fileHandle = None
            progData = eg.configDir + '\plugins\TellStickDuo'
    
            if (
                not os.path.exists(progData)
                and not os.path.isdir(progData)
            ):
                os.makedirs(progData)
    
            fileHandle = open (
                progData+'/'+
                self.name+'.html', 'a'
            )
            fileHandle.write ( logStr.encode('utf-8') )
            fileHandle.close ()


    def MilliSeconds(self):
        return int(round(time.time() * 1000))


    def sensorCallbacksBack(self, myArgument):
        print repr(myArgument)
        eg.TriggerEvent(repr(myArgument))
        self.callbacksLost = False


    def sensorCallbacksLost(self, myArgument):
        print repr(myArgument)
        eg.TriggerEvent(repr(myArgument))
        self.callbacksLost = True
        

    def controllerEventCallback(self, controllerId, changeEvent, changeType, p1, i3, p2):
        self.controller = []
        self.controller.append(controllerId)
        self.controller.append(changeEvent)
        self.controller.append(changeType)
        self.controller.append(string_at(p1))
        self.controller.append(i3)
        self.controller.append(p2)
        #print self.controller
        if self.controller[3] == '0':
            eg.TriggerEvent(self.text.controller_dwn, prefix = 'TellStickDuo')
        if self.controller[3] == '1':
            eg.TriggerEvent(self.text.controller_up, prefix = 'TellStickDuo')


    def deviceEventCallback(self, deviceId, method, p1, i3, p2):
        level = 0
        if self.dll.tdLastSentCommand(deviceId, method) == 16:
            lvl = self.dll.tdLastSentValue(deviceId)
            if c_char_p(lvl).value.isdigit():
                level = int(round(100.0*float( (c_char_p(lvl)).value)/255.0, 0))
            else:
                level = 0
        gn = self.dll.tdGetName(deviceId)
        deviceName = (c_char_p(gn)).value
        self.dll.tdReleaseString(gn)
        gm = self.dll.tdGetModel(deviceId)
        deviceType = (c_char_p(gm)).value
        self.dll.tdReleaseString(gm)

        if (method == TELLSTICK_TURNON):
            strMethod = self.text.ON_txt
        elif (method == TELLSTICK_TURNOFF):
            strMethod = self.text.OFF_txt
        elif (method == TELLSTICK_DIM):
            strMethod = self.text.DIM_txt
        elif (method == TELLSTICK_BELL):
            strMethod = self.text.BELL_txt
        elif (method == TELLSTICK_DOWN):
            strMethod = self.text.DOWN_txt
        elif (method == TELLSTICK_UP):
            strMethod = self.text.UP_txt
        elif (method == TELLSTICK_STOP):
            strMethod = self.text.STOP_txt
        else:
            return

        eventStr = (
            deviceName+'|'+
            strMethod+'|'+
            str(deviceType)+'|'+
            str(deviceId)+'|'+
            str(level)
        )
        
        event_key = (
            deviceName+'|'+
            str(deviceId)
        )

        if self.delayRepeat > 0:
            if eventStr not in self.oldDeviceEventCollection:
                self.oldDeviceEventCollection.append(eventStr)
                #Schedule the event removal task
                self.taskObj = eg.scheduler.AddTask(
                    self.delayRepeat,
                    self.RemoveEventFromCollection,
                    eventStr
                )
            else:
                return
        
        self.SaveDevicePersistent(eventStr, event_key)


    def sensorEventCallback(
        self,
        protocol,
        model,
        id,
        dataType,
        value,
        timestamp,
        callbackId,
        context
    ):

#        print (
#            string_at(protocol),
#            string_at(model),
#            id,
#            dataType,
#            string_at(value),
#            timestamp,
#            callbackId,
#            context
#        )

        TELLSTICK_TEMPERATURE = 1
        TELLSTICK_HUMIDITY = 2
        TELLSTICK_RAINRATE = 4
        TELLSTICK_RAINTOTAL = 8
        TELLSTICK_WINDDIRECTION = 16
        TELLSTICK_WINDAVERAGE = 32
        TELLSTICK_WINDGUST = 64

        strProtocol = string_at(protocol)
        strModel = string_at(model)
        strValue = string_at(value)
        dType = ''
        bFound = False
        if(dataType == TELLSTICK_TEMPERATURE):
            dType = "Temperature"
        elif(dataType == TELLSTICK_HUMIDITY):
            dType = "Humidity"
        elif(dataType == TELLSTICK_RAINRATE):
            dType = "Rain rate"
        elif(dataType == TELLSTICK_RAINTOTAL):
            dType = "Rain total"
        elif(dataType == TELLSTICK_WINDDIRECTION):
            dType = "Wind direction"
        elif(dataType == TELLSTICK_WINDAVERAGE):
            dType = "Wind average"
        elif(dataType == TELLSTICK_WINDGUST):
            dType = "Wind gust"
            
        if strProtocol == 'mandolyn':
            self.mandolynEventStr[0] = strProtocol
            self.mandolynEventStr[1] = strModel
            if self.mandolynEventStr[2] == '':
                self.mandolynEventStr[2] = str(id)
            if dType == "Temperature" and str(id) == self.mandolynEventStr[2]:
                self.mandolynEventStr[3] = dType
                self.mandolynEventStr[5] = strValue
            if dType == "Humidity" and str(id) == self.mandolynEventStr[2]:
                self.mandolynEventStr[4] = dType
                self.mandolynEventStr[6] = strValue
            event_key = (
                strProtocol+'|'+
                strModel+'|'+
                str(id)
            )

            if self.mandolynEventStr[3]<>'' and self.mandolynEventStr[4]<>'':
                for i in self.sensors_supported:
                    if event_key.find(i) <> -1:
                        bFound = True
                if bFound:
                    if self.delayRepeat > 0:
                        if event_key not in self.oldDeviceSensorEventCollection:
                            self.oldDeviceSensorEventCollection.append(event_key)
                            #Schedule the sensor event removal task
                            self.taskObjSensors = eg.scheduler.AddTask(
                                self.delayRepeat,
                                self.RemoveSensorEventFromCollection,
                                event_key
                            )
                        else:
                            self.mandolynEventStr = ['']*7
                            return
                    msg = self.mandolynEventStr
                    self.mandolynEventStr = ['']*7
                    self.SaveMandolynSensorPersistent(msg, event_key)
                    self.sensorAliveMonitor()
                return

        if strProtocol == 'fineoffset' and strModel == 'temperaturehumidity':
            #print id, dType, strValue
            if self.fineoffsetEventID == '':
                self.fineoffsetEventID = str(id)
 
            if dType == "Temperature" and str(id) == self.fineoffsetEventID:
                self.foTempHumEventStr[0] = strProtocol
                self.foTempHumEventStr[1] = strModel
                self.foTempHumEventStr[2] = str(id)
                self.foTempHumEventStr[3] = dType
                self.foTempHumEventStr[5] = strValue
            if dType == "Humidity" and str(id) == self.fineoffsetEventID:
                self.foTempHumEventStr[4] = dType
                self.foTempHumEventStr[6] = strValue

            event_key = (
                strProtocol+'|'+
                strModel+'|'+
                str(id)
            )

            #Temperature & Humidity sensors
            bTh = True
            for i in self.foTempHumEventStr:
                if i=='':
                    bTh = False
                    break
            if bTh:
                for i in self.sensors_supported:
                    if event_key.find(i) <> -1:
                        bFound = True
                if bFound:
                    if self.delayRepeat > 0:
                        if event_key not in self.oldDeviceSensorEventCollection:
                            self.oldDeviceSensorEventCollection.append(event_key)
                            #Schedule the sensor event removal task
                            self.taskObjSensors = eg.scheduler.AddTask(
                                self.delayRepeat,
                                self.RemoveSensorEventFromCollection,
                                event_key
                            )
                        else:
                            self.foTempHumEventStr = ['']*7
                            self.fineoffsetEventID = ''
                            return
                    msg = self.foTempHumEventStr
                    self.foTempHumEventStr = ['']*7
                    self.fineoffsetEventID = ''
                    self.SaveFineOffsetTHSensor(msg, event_key)
                    self.sensorAliveMonitor()
                return

        if strProtocol == 'oregon':
            #print id, dType, strValue
            if self.oregonEventID == '':
                self.oregonEventID = str(id)
 
            if dType == "Temperature" and str(id) == self.oregonEventID:
                self.orTempHumEventStr[0] = strProtocol
                self.orTempHumEventStr[1] = strModel
                self.orTempHumEventStr[2] = str(id)
                self.orTempHumEventStr[3] = dType
                self.orTempHumEventStr[5] = strValue
            if dType == "Humidity" and str(id) == self.oregonEventID:
                self.orTempHumEventStr[4] = dType
                self.orTempHumEventStr[6] = strValue

            if dType == "Rain total" and str(id) == self.oregonEventID:
                self.orRainEventStr[0] = strProtocol
                self.orRainEventStr[1] = strModel
                self.orRainEventStr[2] = str(id)
                self.orRainEventStr[3] = dType
                self.orRainEventStr[4] = strValue
            if dType == "Rain rate" and str(id) == self.oregonEventID:
                self.orRainEventStr[5] = dType
                self.orRainEventStr[6] = strValue

            if dType == "Wind direction" and str(id) == self.oregonEventID:
                self.orWindEventStr[0] = strProtocol
                self.orWindEventStr[1] = strModel
                self.orWindEventStr[2] = str(id)
                self.orWindEventStr[3] = dType
                self.orWindEventStr[4] = strValue
            if dType == "Wind average" and str(id) == self.oregonEventID:
                self.orWindEventStr[5] = dType
                self.orWindEventStr[6] = strValue
            if dType == "Wind gust" and str(id) == self.oregonEventID:
                self.orWindEventStr[7] = dType
                self.orWindEventStr[8] = strValue

            event_key = (
                strProtocol+'|'+
                strModel+'|'+
                str(id)
            )

            #Temperature & Humidity sensors
            bTh = True
            for i in self.orTempHumEventStr:
                if i=='':
                    bTh = False
                    break
            if bTh:
                for i in self.sensors_supported:
                    if event_key.find(i) <> -1:
                        bFound = True
                if bFound:
                    if self.delayRepeat > 0:
                        if event_key not in self.oldDeviceSensorEventCollection:
                            self.oldDeviceSensorEventCollection.append(event_key)
                            #Schedule the sensor event removal task
                            self.taskObjSensors = eg.scheduler.AddTask(
                                self.delayRepeat,
                                self.RemoveSensorEventFromCollection,
                                event_key
                            )
                        else:
                            self.orTempHumEventStr = ['']*7
                            self.oregonEventID = ''
                            return
                    msg = self.orTempHumEventStr
                    self.orTempHumEventStr = ['']*7
                    self.oregonEventID = ''
                    self.SaveOregonTHSensor(msg, event_key)
                    self.sensorAliveMonitor()
                return

            #Rain sensors
            bRa = True
            for i in self.orRainEventStr:
                if i=='':
                    bRa = False
                    break
            if bRa:
                for i in self.sensors_supported:
                    if event_key.find(i) <> -1:
                        bFound = True
                if bFound:
                    if self.delayRepeat > 0:
                        if event_key not in self.oldDeviceSensorEventCollection:
                            self.oldDeviceSensorEventCollection.append(event_key)
                            #Schedule the sensor event removal task
                            self.taskObjSensors = eg.scheduler.AddTask(
                                self.delayRepeat,
                                self.RemoveSensorEventFromCollection,
                                event_key
                            )
                        else:
                            self.orRainEventStr = ['']*7
                            self.oregonEventID = ''
                            return
                    msg = self.orRainEventStr
                    self.orRainEventStr = ['']*7
                    self.oregonEventID = ''
                    self.SaveOregonRainSensor(msg, event_key)
                    self.sensorAliveMonitor()
                return

            #Wind sensors
            bWi = True
            for i in self.orWindEventStr:
                if i=='':
                    bWi = False
                    break
            if bWi:
                for i in self.sensors_supported:
                    if event_key.find(i) <> -1:
                        bFound = True
                if bFound:
                    if self.delayRepeat > 0:
                        if event_key not in self.oldDeviceSensorEventCollection:
                            self.oldDeviceSensorEventCollection.append(event_key)
                            #Schedule the sensor event removal task
                            self.taskObjSensors = eg.scheduler.AddTask(
                                self.delayRepeat,
                                self.RemoveSensorEventFromCollection,
                                event_key
                            )
                        else:
                            self.orWindEventStr = ['']*9
                            self.oregonEventID = ''
                            return
                    msg = self.orWindEventStr
                    self.orWindEventStr = ['']*9
                    self.oregonEventID = ''
                    self.SaveOregonWindSensor(msg, event_key)
                    self.sensorAliveMonitor()
                return

            
        if (
            strProtocol <> 'oregon' and 
            strProtocol <> 'mandolyn' and
            strModel <> 'temperaturehumidity'
        ):
            otherEventStr = (
                strProtocol+'|'+
                strModel+'|'+
                str(id)+'|'+
                dType+'|'+
                strValue
            )
            event_key = (
                strProtocol+'|'+
                strModel+'|'+
                str(id)+'|'+
                dType
            )
            for i in self.sensors_supported:
                if event_key.find(i) <> -1:
                    bFound = True
            if bFound:
                if self.delayRepeat > 0:
                    if event_key not in self.oldDeviceSensorEventCollection:
                        self.oldDeviceSensorEventCollection.append(event_key)
                        #Schedule the sensor event removal task
                        self.taskObjSensors = eg.scheduler.AddTask(
                            self.delayRepeat,
                            self.RemoveSensorEventFromCollection,
                            event_key
                        )
                    else:
                        return
                self.SaveOtherSensorPersistent(otherEventStr, event_key)
                self.sensorAliveMonitor()
            return


    def sensorAliveMonitor(self):
        average_time = 0
        if self.sensorEventTime == 0:
            self.sensorEventTime = self.MilliSeconds()
        else:
            timeDiff = self.MilliSeconds() - self.sensorEventTime
            self.sensorEventTime += timeDiff
            if (
                len(self.sensorEventTimeAverage) < 
                30
            ):
                self.sensorEventTimeAverage.append(timeDiff)
            else:
                self.sensorEventTimeAverage.insert(0, timeDiff)
                del self.sensorEventTimeAverage[-1]
            if (
                len(self.sensorEventTimeAverage) == 
                30
            ):
                average_time = (
                    float(sum(self.sensorEventTimeAverage)) /
                    30
                )
                try:
                    eg.scheduler.CancelTask(self.sensorMonitor)
                except:
                    self.sensorMonitor = None
                    if self.callbacksLost:
                        self.sensorCallbacksBack(
                            self.text.sensor_callbacks_back
                        )
                self.sensorMonitor = eg.scheduler.AddTask(
                        average_time/1000 * 60.0,
                        self.sensorCallbacksLost,
                        self.text.sensor_callbacks_lost
                )


    def deviceRawEventCallback(self, p1, i1, i2, p3):
        strData = string_at(p1)
        if (strData == ""):
            return

        if(self.bRawEvents):
            if(
                (strData <> self.oldDeviceEventRaw)
                    or
                (strData == self.oldDeviceEventRaw
                    and
                 self.bTaskAddedRaw == False)
            ):
                self.bTaskAddedRaw = True
                try:
                    eg.scheduler.CancelTask(self.taskObjRaw)
                    #print "taskObjRaw cancelled"
                except ValueError:
                    pass
                self.oldDeviceEventRaw = strData
    
                self.TriggerEvent(
                    "RawEvent: "+
                    strData+
                    "Duo_ID:"+
                    str(i2)
                )
                self.LogToFile(
                    "RawEvent: "+
                    strData+
                    "Duo_ID:"+
                    str(i2)
                )
    
                if self.bTaskAddedRaw:
                    self.taskObjRaw = eg.scheduler.AddTask(
                        self.delayRepeat,
                        self.ClearFlagRaw
                    )
                else:
                    self.bTaskAddedRaw = False


    def deviceChangeEventCallback(self, deviceId, changeEvent, i3, i4, p1):
        gn = self.dll.tdGetName(deviceId)
        deviceName = (c_char_p(gn)).value
        self.dll.tdReleaseString(gn)
        gm = self.dll.tdGetModel(deviceId)
        deviceType = (c_char_p(gm)).value
        self.dll.tdReleaseString(gm)
        self.ch_name_device = time.time()
        self.syncDimData()

        if self.bChangeEvents:
            self.TriggerEvent(
                "ChangeEvent: "+
                str(deviceType)+
                str(deviceName).decode('utf-8')+
                str(changeEvent).decode('utf-8')
            )
            timeStamp = str(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )

            if deviceName.find('eventGhost.HeartBeatDevice') == -1:
                self.LogToFile(
                    "ChangeEvent: "+
                    str(deviceType)+
                    str(deviceName)+
                    str(changeEvent)
                )


    def syncDimData(self):
        deviceList = {}
        syncDimData = {}
        numdevices = 0
        dimData = self.dimDeviceData
        #print dimData
        try:
            numDevices = self.dll.tdGetNumberOfDevices()
        except:
            numDevices = 0
        for i in range(numDevices):
            id = self.dll.tdGetDeviceId(i)
            gn = self.dll.tdGetName(id)
            name = (c_char_p(gn)).value
            self.dll.tdReleaseString(gn)
            deviceList[str(id)] = str(name).decode('utf-8')
        for j in deviceList:
            try:
                syncDimData[j] = dimData[j]
            except:
                pass
        self.dimDeviceData = syncDimData
        #print self.dimDeviceData


    def lastSentValue(self, intDeviceId):
        func = self.dll.tdLastSentValue
        func.restype = c_char_p
        ret = func(intDeviceId)
        return ret


    def getId(self, deviceName, method):
        self.method = method
        try:
            numDevices = self.dll.tdGetNumberOfDevices()
        except:
            numDevices = 0
        selected = 0
        for i in range(numDevices):
            id = self.dll.tdGetDeviceId(i)
            methods = self.dll.tdMethods(
                id,
                TELLSTICK_TURNON
                | TELLSTICK_TURNOFF
                | TELLSTICK_BELL
                | TELLSTICK_TOGGLE
                | TELLSTICK_DIM
                | TELLSTICK_DOWN
                | TELLSTICK_UP
                | TELLSTICK_STOP
            )
            if (methods & self.method):
                gn = self.dll.tdGetName(id)
                name = (c_char_p(gn)).value
                self.dll.tdReleaseString(gn)
                if (name == deviceName):
                    return id        


    def getErrorString(self, intErrorNo):
        getErrorStringFunc = self.dll.tdGetErrorString
        getErrorStringFunc.restype = c_void_p
        vp = getErrorStringFunc(intErrorNo)
        cp = c_char_p(vp)
        s = str(cp.value)
        self.dll.tdReleaseString(vp)
        return s


    def sendCommand(self, id, command, level):
        ret = None
        if command == 'On' or command == 'Off':
            for i in range(5):
                if i>0:
                    print self.text.retry_txt, i
                if command == 'On':
                    ret = self.dll.tdTurnOn(id)
                else:
                    ret = self.dll.tdTurnOff(id)
                if (ret != TELLSTICK_SUCCESS and i == 4):
                    self.TriggerEvent(
                        self.text.exception_txt,
                        payload = self.getErrorString(ret)
                    )
                    raise eg.Exception(self.text.exception_txt)
                if(ret == TELLSTICK_SUCCESS):
                    break
        if command == 'Dim':
            for i in range(5):
                if i>0:
                    print self.text.retry_txt, i
                if level == 0:
                    ret = self.dll.tdTurnOff(id)
                if level > 0 and level < 256 :
                    ret = self.dll.tdDim(id, level)
                if level == 256:
                    ret = self.dll.tdDim(id, level)
#                    ret = self.dll.tdTurnOn(id)
                if (ret != TELLSTICK_SUCCESS and i == 4):
                    self.TriggerEvent(
                        self.text.exception_txt,
                        payload = self.getErrorString(ret)
                    )
                    raise eg.Exception(self.text.exception_txt)
                if (ret == TELLSTICK_SUCCESS):
                    break
        if command == 'Bell':
            for i in range(5):
                if i>0:
                    print self.text.retry_txt, i
                ret = self.dll.tdBell(id)
                if (ret != TELLSTICK_SUCCESS and i == 4):
                    self.TriggerEvent(
                        self.text.exception_txt,
                        payload = self.getErrorString(ret)
                    )
                    raise eg.Exception(self.text.exception_txt)
                if(ret == TELLSTICK_SUCCESS):
                    break
        if command == 'Up' or command == 'Down':
            for i in range(5):
                if i>0:
                    print self.text.retry_txt, i
                if command == 'Up':
                    ret = self.dll.tdUp(id)
                else:
                    ret = self.dll.tdDown(id)
                if (ret != TELLSTICK_SUCCESS and i == 4):
                    self.TriggerEvent(
                        self.text.exception_txt,
                        payload = self.getErrorString(ret)
                    )
                    raise eg.Exception(self.text.exception_txt)
                if(ret == TELLSTICK_SUCCESS):
                    break
        if command == 'Stop':
            for i in range(5):
                if i>0:
                    print self.text.retry_txt, i
                ret = self.dll.tdStop(id)
                if (ret != TELLSTICK_SUCCESS and i == 4):
                    self.TriggerEvent(
                        self.text.exception_txt,
                        payload = self.getErrorString(ret)
                    )
                    raise eg.Exception(self.text.exception_txt)
                if(ret == TELLSTICK_SUCCESS):
                    break
        del self.queu[0]
        return ret


    def scheduleCommand(self, id, command, level):
        self.queu.append(str(id)+':'+command+':'+str(level))
        lenq = len(self.queu)
        if lenq > 1:
            delay = (lenq-1)*1.5
        else:
            delay = 0.1 
        eg.scheduler.AddTask(
            delay, 
            self.sendCommand,
            id,
            command,
            level
        )


    def Configure(
        self,
        bDeviceEvents = True,
        bChangeEvents = True,
        bRawEvents = False,
        beepOnEvent = False,
        bDebug = False,
        delayRepeat = 0.3,
        bSensorEvents = True,
        *args
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        mySizer_1 = wx.GridBagSizer(5, 5)

        delayRepeatCtrl = panel.SpinNumCtrl(
            delayRepeat,
            decimalChar = '.',                 # by default, use '.' for decimal point
            groupChar = ',',                   # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 2,
            min = 0.0,
            max = 15.0,
            increment = 0.1
        )
        delayRepeatCtrl.SetValue(delayRepeat)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.log_delayRepeat
            ),
            (1,0)
        )
        mySizer_1.Add(delayRepeatCtrl, (1,1))

        bDeviceEventsCtrl = wx.CheckBox(panel, -1, "")
        bDeviceEventsCtrl.SetValue(bDeviceEvents)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.log_device_events
            ),
            (2,0)
        )
        mySizer_1.Add(bDeviceEventsCtrl, (2,1))

        bSensorEventsCtrl = wx.CheckBox(panel, -1, "")
        bSensorEventsCtrl.SetValue(bSensorEvents)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.log_sensor_events
            ),
            (3,0)
        )
        mySizer_1.Add(bSensorEventsCtrl, (3,1))

        bChangeEventsCtrl = wx.CheckBox(panel, -1, "")
        bChangeEventsCtrl.SetValue(bChangeEvents)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.log_change_events
            ),
            (4,0)
        )
        mySizer_1.Add(bChangeEventsCtrl, (4,1))

        bRawEventsCtrl = wx.CheckBox(panel, -1, "")
        bRawEventsCtrl.SetValue(bRawEvents)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.log_raw_events
            ),
            (5,0)
        )
        mySizer_1.Add(bRawEventsCtrl, (5,1))
       
        bSoundCtrl = wx.CheckBox(panel, -1, "")
        bSoundCtrl.SetValue(beepOnEvent)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.beep_device_events
            ),
            (6,0)
        )
        mySizer_1.Add(bSoundCtrl, (6,1))

        bDebugCtrl = wx.CheckBox(panel, -1, "")
        bDebugCtrl.SetValue(bDebug)
        mySizer_1.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.debug
            ),
            (7,0)
        )
        mySizer_1.Add(bDebugCtrl, (7,1))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            bDeviceEvents = bDeviceEventsCtrl.GetValue()
            bSensorEvents = bSensorEventsCtrl.GetValue()
            bChangeEvents = bChangeEventsCtrl.GetValue()
            bRawEvents = bRawEventsCtrl.GetValue()
            beepOnEvent = bSoundCtrl.GetValue()
            bDebug = bDebugCtrl.GetValue()
            delayRepeat = delayRepeatCtrl.GetValue()
            panel.SetResult(
                bDeviceEvents,
                bChangeEvents,
                bRawEvents,
                beepOnEvent,
                bDebug,
                delayRepeat,
                bSensorEvents
            )

         

class DeviceBase(object):

    def Configure(self, deviceName=''):
        deviceList = []
        indexToIdMap = {}
        try:
            numDevices = self.plugin.dll.tdGetNumberOfDevices()
        except:
            numDevices = 0
        selected = 0
        for i in range(numDevices):
            id = self.plugin.dll.tdGetDeviceId(i)
            methods = self.plugin.dll.tdMethods(
                            id,
                            TELLSTICK_TURNON
                            | TELLSTICK_TURNOFF
                            | TELLSTICK_BELL
                            | TELLSTICK_TOGGLE
                            | TELLSTICK_DIM
                            | TELLSTICK_DOWN
                            | TELLSTICK_UP
                            | TELLSTICK_STOP
                      )
            if (methods & self.method):
                index = len(deviceList)
                gn = self.plugin.dll.tdGetName(id)
                #print self.plugin.dll.tdGetModel(id)
                name = (c_char_p(gn)).value
                self.plugin.dll.tdReleaseString(gn)
                if (name == deviceName.encode('utf-8')):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name.decode('utf-8'))

        panel = eg.ConfigPanel(self)
        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)

        if (len(deviceList) > 0):
            panel.sizer.Add( 
                wx.StaticText(panel, -1, self.plugin.text.device_txt), 
                0, 
                wx.ALIGN_CENTER_VERTICAL
            )
            
        else:
            panel.sizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.no_device_txt_1+
                    self.name+
                    self.plugin.text.no_device_txt_2+
                    self.plugin.text.no_device_txt_3
                ), 
                0, 
                wx.ALIGN_CENTER_VERTICAL
            )
            
        panel.sizer.Add(deviceCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        while panel.Affirmed():
            if self.plugin.dll is not None and len(deviceList) > 0:
                device = indexToIdMap[deviceCtrl.GetSelection()]
                gn = self.plugin.dll.tdGetName(device)
                deviceName = (c_char_p(gn)).value.decode('utf-8')
                self.plugin.dll.tdReleaseString(gn)
                panel.SetResult(deviceName)
            else:
                deviceName = ''

            

class SaveDimLevel(eg.ActionClass):
    name = "Save device dim level"
    description = "Stores the device dim level."
    iconFile = "save"

    def __call__(self):

        try:
            es = eg.event.string.split('.')
            id = eg.event.payload.split('.')[1]
            self.deviceName = es[1].encode('utf-8')
            
            if es[2] == 'ON':
                self.plugin.dimPercentage[str(id)] = '255'
                self.plugin.dimDeviceData[str(id)] = (
                    '255'+
                    '|'+
                    self.deviceName
                )        
            if es[2] == 'OFF':
                self.plugin.dimPercentage[str(id)] = '0'
                self.plugin.dimDeviceData[str(id)] = (
                    '0'+
                    '|'+
                    self.deviceName
                )        
        except:
            eg.PrintError(
                'Failed to save device dim level for: '+self.deviceName
            )


class TurnOn(DeviceBase, eg.ActionClass):
    name = "Turn on"
    description = "Turns on a TellStick device."
    iconFile = "lamp-on"
    method = TELLSTICK_TURNON

    def __call__(self, deviceName):
        self.deviceName = deviceName.encode('utf-8')
        id = self.plugin.getId(self.deviceName, self.method)
        self.plugin.scheduleCommand(id, 'On', 255)
        self.plugin.dimPercentage[str(id)] = '255'
        self.plugin.dimDeviceData[str(id)] = (
            '255'+
            '|'+
            self.deviceName
        )        



class ToggleOnOffWithTimer(eg.ActionClass):
    name = "Toggle on/off with timer"
    description = "Toggles a TellStick device with delays."
    iconFile = "lamp-on"
    method = TELLSTICK_TURNON

    def OnWithDelay(self, id, deviceName):
        self.plugin.scheduleCommand(id, 'On', None)
        self.plugin.dimPercentage[str(id)] = '255'
        self.plugin.dimDeviceData[str(id)] = (
            '255'+
            '|'+
            deviceName
        )        


    def OffWithDelay(self, id, deviceName):
        self.plugin.scheduleCommand(id, 'Off', None)
        self.plugin.dimPercentage[str(id)] = '0'
        self.plugin.dimDeviceData[str(id)] = (
            '0'+
            '|'+
            deviceName
        )        

     
    def __call__(self, deviceName, delayOn, delayOff):
        deviceName = deviceName.encode('utf-8')
        id = self.plugin.getId(deviceName, self.method)
        lst_cmd = self.plugin.dll.tdLastSentCommand( id, self.method )
        if int((c_ubyte(lst_cmd)).value) == 2:
            eg.scheduler.AddTask(
                delayOn, 
                self.OnWithDelay, 
                id, 
                deviceName
            )
            eg.scheduler.AddTask(
                delayOn+delayOff, 
                self.OffWithDelay, 
                id, 
                deviceName
            )
        elif int((c_ubyte(lst_cmd)).value) == 1:
            eg.scheduler.AddTask(
                delayOff, 
                self.OffWithDelay, 
                id, 
                deviceName
            )
            eg.scheduler.AddTask(
                delayOff+delayOn, 
                self.OnWithDelay, 
                id, 
                deviceName
            )
        

    def Configure(self, deviceName='', delayOn=0.0, delayOff=0.0):
        deviceList = []
        indexToIdMap = {}
        try:
            numDevices = self.plugin.dll.tdGetNumberOfDevices()
        except:
            numDevices = 0
        selected = 0
        for i in range(numDevices):
            id = self.plugin.dll.tdGetDeviceId(i)
            methods = self.plugin.dll.tdMethods(
                            id,
                            TELLSTICK_TURNON
                            | TELLSTICK_TURNOFF
                            | TELLSTICK_BELL
                            | TELLSTICK_TOGGLE
                            | TELLSTICK_DIM
                            | TELLSTICK_DOWN
                            | TELLSTICK_UP
                            | TELLSTICK_STOP
                      )
            if (methods & self.method):
                index = len(deviceList)
                gn = self.plugin.dll.tdGetName(id)
                #print self.plugin.dll.tdGetModel(id)
                name = (c_char_p(gn)).value
                self.plugin.dll.tdReleaseString(gn)
                if (name == deviceName.encode('utf-8')):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name.decode('utf-8'))

        panel = eg.ConfigPanel(self)
        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)

        if (len(deviceList) > 0):
            panel.sizer.Add( 
                wx.StaticText(panel, -1, self.plugin.text.device_txt), 
                0, 
                wx.ALIGN_CENTER_VERTICAL
            )
            
        else:
            panel.sizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.no_device_txt_1+
                    self.name+
                    self.plugin.text.no_device_txt_2+
                    self.plugin.text.no_device_txt_3
                ), 
                0, 
                wx.ALIGN_CENTER_VERTICAL
            )
            
        panel.sizer.Add(deviceCtrl, 1, wx.ALIGN_CENTER_VERTICAL)
        
        panel.sizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.plugin.text.delayOn_txt
            ),
            0, 
            wx.ALIGN_CENTER_VERTICAL
        ) 
        delayOnCtrl = panel.SpinNumCtrl(
            delayOn,
            # by default, use '.' for decimal point
            decimalChar = '.',
            # by default, use ',' for grouping
            groupChar = ',',
            fractionWidth = 2,
            integerWidth = 3,
            min = 0.10,
            max = 600.00,
            increment = 0.10
        )
        delayOnCtrl.SetInitialSize((90,-1))
        panel.sizer.Add(delayOnCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        
        panel.sizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.plugin.text.delayOff_txt
            ), 
            0, 
            wx.ALIGN_CENTER_VERTICAL
        ) 
        delayOffCtrl = panel.SpinNumCtrl(
            delayOff,
            # by default, use '.' for decimal point
            decimalChar = '.',
            # by default, use ',' for grouping
            groupChar = ',',
            fractionWidth = 2,
            integerWidth = 3,
            min = 0.10,
            max = 600.00,
            increment = 0.10
        )
        delayOffCtrl.SetInitialSize((90,-1))
        panel.sizer.Add(delayOffCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        
        while panel.Affirmed():
            if self.plugin.dll is not None and len(deviceList) > 0:
                device = indexToIdMap[deviceCtrl.GetSelection()]
                gn = self.plugin.dll.tdGetName(device)
                deviceName = (c_char_p(gn)).value.decode('utf-8')
                self.plugin.dll.tdReleaseString(gn)
                panel.SetResult(
                    deviceName, 
                    delayOnCtrl.GetValue(), 
                    delayOffCtrl.GetValue()
                )
            else:
                deviceName = ''
                


class ToggleOnOff(DeviceBase, eg.ActionClass):
    name = "Toggle on/off"
    description = "Toggles a TellStick device."
    iconFile = "lamp-on"
    method = TELLSTICK_TURNON

    def __call__(self, deviceName):
        self.deviceName = deviceName.encode('utf-8')
        id = self.plugin.getId(self.deviceName, self.method)
        lst_cmd = self.plugin.dll.tdLastSentCommand( id, self.method )

        if int((c_ubyte(lst_cmd)).value) == 1:
            self.plugin.scheduleCommand(id, 'Off', None)
            self.plugin.dimPercentage[str(id)] = '0'
            self.plugin.dimDeviceData[str(id)] = (
                '0'+
                '|'+
                self.deviceName
            )        
        else:
            self.plugin.scheduleCommand(id, 'On', None)
            self.plugin.dimPercentage[str(id)] = '255'
            self.plugin.dimDeviceData[str(id)] = (
                '255'+
                '|'+
                self.deviceName
            )        



class TurnOff(DeviceBase, eg.ActionClass):
    name = "Turn off"
    description = "Turns off a TellStick device."
    iconFile = "lamp-off"
    method = TELLSTICK_TURNOFF

    def __call__(self, deviceName):
        self.deviceName = deviceName.encode('utf-8')
        id = self.plugin.getId(self.deviceName, self.method)
        self.plugin.scheduleCommand(id, 'Off', 0)
        self.plugin.dimPercentage[str(id)] = '0'
        self.plugin.dimDeviceData[str(id)] = (
            '0'+
            '|'+
            self.deviceName
        )        



class MoveDown(DeviceBase, eg.ActionClass):
    name = "Move down"
    description = "Start moving down."
    iconFile = "down"
    method = TELLSTICK_DOWN

    def __call__(self, deviceName):
        id = self.plugin.getId(deviceName.encode('utf-8'), self.method)
        self.plugin.scheduleCommand(id, 'Down', None)



class MoveUp(DeviceBase, eg.ActionClass):
    name = "Move up"
    description = "Start moving up."
    iconFile = "up"
    method = TELLSTICK_UP

    def __call__(self, deviceName):
        id = self.plugin.getId(deviceName.encode('utf-8'), self.method)
        self.plugin.scheduleCommand(id, 'Up', None)



class Stop(DeviceBase, eg.ActionClass):
    name = "Stop movement"
    description = "Stops the movement."
    iconFile = "stop"
    method = TELLSTICK_STOP

    def __call__(self, deviceName):
        id = self.plugin.getId(deviceName.encode('utf-8'), self.method)
        self.plugin.scheduleCommand(id, 'Stop', None)



class Bell(DeviceBase, eg.ActionClass):
    name = "Bell"
    description = "Sends bell to a TellStick device."
    iconFile = "bell"
    method = TELLSTICK_BELL

    def __call__(self, deviceName):
        id = self.plugin.getId(deviceName.encode('utf-8'), self.method)
        self.plugin.scheduleCommand(id, 'Bell', None)



class Dim(eg.ActionClass):
    name = "Dim"
    description = "Dims a TellStick device."
    iconFile = "lamp-dim"
    method = TELLSTICK_DIM

    def __call__(self, deviceName, level):
        level = int(level*255/100)
        self.deviceName = deviceName.encode('utf-8')
        id = self.plugin.getId(self.deviceName, self.method)
        self.plugin.scheduleCommand(id, 'Dim', level)
        self.plugin.dimPercentage[str(id)] = str(level)
        self.plugin.dimDeviceData[str(id)] = (
            str(level)+
            '|'+
            self.deviceName
        )        


    def Configure(self, deviceName = '', level=50):
        deviceList = []
        indexToIdMap = {}
        try:
            numDevices = self.plugin.dll.tdGetNumberOfDevices()
        except:
            numDevices = 0
        selected = 0
        for i in range(numDevices):
            id = self.plugin.dll.tdGetDeviceId(i)
            methods = self.plugin.dll.tdMethods(
                            id,
                            TELLSTICK_DIM
                      )
            if (methods & self.method):
                index = len(deviceList)
                gn = self.plugin.dll.tdGetName(id)
                name = (c_char_p(gn)).value
                self.plugin.dll.tdReleaseString(gn)
                if (name == deviceName.encode('utf-8')):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name.decode('utf-8'))

        panel = eg.ConfigPanel(self)
        mySizer = wx.GridBagSizer(10, 10)
        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)
        self.levelCtrl = wx.Slider(
                            panel,
                            -1,
                            level,
                            0,
                            100,
                            (10, 10),
                            (200, 50),
                            wx.SL_HORIZONTAL | wx.SL_LABELS
                         )

        if (len(deviceList) > 0):
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.device_txt
                ), (1,0)
            )
        else:
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.no_device_txt_1+
                    self.name+
                    self.plugin.text.no_device_txt_2+
                    self.plugin.text.no_device_txt_3
                ), (1,0)
            )

        mySizer.Add(deviceCtrl, (1,1))
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.level_txt
            ), (3,0)
        ) 
        mySizer.Add(self.levelCtrl, (3,1))

        panel.sizer.Add(mySizer, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            if self.plugin.dll is not None and len(deviceList) > 0:
                device = indexToIdMap[deviceCtrl.GetSelection()]
                gn = self.plugin.dll.tdGetName(device)
                deviceName = (c_char_p(gn)).value.decode('utf-8')
                self.plugin.dll.tdReleaseString(gn)
                level = self.levelCtrl.GetValue()
                panel.SetResult(deviceName, level)
                indx = 0
                for m_name in eg.document.__dict__['root'].childs:
                    if(
                        m_name.name.find(deviceName)!= -1
                        and
                        m_name.name.find('Dim')!= -1
                    ):
                        new_name = (
                            'TellStickDuo: Dim '+
                            deviceName+
                            ' to '+
                            str(level)+
                            '%'
                        )
                        eg.document.__dict__['root'].childs[indx].name = new_name
                        eg.document.__dict__['root'].childs[indx].Refresh()
                    indx += 1
            else:
                deviceName = ''



class DimGradually(eg.ActionClass):
    name = "Dim gradually"
    description = "Dims a TellStick device gradually."
    iconFile = "lamp-dim"
    method = TELLSTICK_DIM

    def __call__(self, deviceName, timeInBetween, step, level):
        self.deviceName = deviceName.encode('utf-8')
        self.id = self.plugin.getId(self.deviceName, self.method)
        self.timeInBetween = timeInBetween
        self.step = step
        self.level = int(level*255/100)

        self.finished = Event()
        self.DimGradually = Thread(
            target=self.DimGraduallyThread,
            name="DimGradually"
        )
        self.DimGradually.start()


    def DimGraduallyThread(self):
        the_level = 0
        k_msg = ''
        m_key = (
            str(self.id)
        )
        try:
            the_level = int(self.plugin.dimPercentage[m_key])
        except:
            pass           

        while not self.finished.isSet():

            if the_level == int(self.level):
                self.plugin.scheduleCommand(self.id, 'Dim', the_level)
                k_msg = (
                    str(the_level)
                )

            if the_level > int(self.level):
                while the_level > int(self.level):
                    if the_level > 0:
                        self.plugin.scheduleCommand(self.id, 'Dim', the_level)
                    diff = the_level - int(self.level)
                    if diff >= self.step:
                        the_level -= self.step
                    elif diff > 0:
                        the_level -= diff
                        if the_level < 0:
                            the_level = 0
                        #print int(self.level), the_level, diff
                        self.plugin.scheduleCommand(self.id, 'Dim', the_level)
                    self.finished.wait(self.timeInBetween)
                    k_msg = (
                        str(the_level)
                    )

            elif the_level < int(self.level):
                while the_level < int(self.level):
                    self.plugin.scheduleCommand(self.id, 'Dim', the_level)
                    diff = int(self.level) - the_level
                    if diff >= self.step:
                        the_level += self.step
                    elif diff > 0:
                        the_level += diff
                        if the_level > 255:
                            the_level = 255
                        #print int(self.level), the_level, diff
                        self.plugin.scheduleCommand(self.id, 'Dim', the_level)
                    self.finished.wait(self.timeInBetween)
                    k_msg = (
                        str(the_level)
                    )

            self.plugin.dimPercentage[m_key] = k_msg
            self.plugin.dimDeviceData[m_key] = (
                k_msg+
                '|'+
                self.deviceName
            )        
            self.finished.set()


    def Configure(
            self,
            deviceName = 'I can be dimmed gradually',
            timeInBetween = 0.30,
            step = 10,
            level = 15
        ):
        panel = eg.ConfigPanel(self)
        mySizer = wx.GridBagSizer(10, 10)
        deviceList = []
        indexToIdMap = {}
        selected = 0

        try:
            numDevices = self.plugin.dll.tdGetNumberOfDevices()
        except:
            numDevices = 0

        for i in range(numDevices):
            id = self.plugin.dll.tdGetDeviceId(i)
            methods = self.plugin.dll.tdMethods(
                            id,
                            TELLSTICK_DIM
                      )
            if (methods & self.method):
                index = len(deviceList)
                gn = self.plugin.dll.tdGetName(id)
                name = (c_char_p(gn)).value
                self.plugin.dll.tdReleaseString(gn)
                if (name == deviceName.encode('utf-8')):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name.decode('utf-8'))

        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)
        if (len(deviceList) > 0):
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.device_txt
                ), (0,0)
            )
        else:
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.no_device_txt_1+
                    self.name+
                    self.plugin.text.no_device_txt_2+
                    self.plugin.text.no_device_txt_3
                ), (0,0)
            )
        mySizer.Add(deviceCtrl, (0,1))

        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.timeInBetween_txt
            ), (1,0)
        ) 
        timeInBetweenCtrl = panel.SpinNumCtrl(
            timeInBetween,
            # by default, use '.' for decimal point
            decimalChar = '.',
            # by default, use ',' for grouping
            groupChar = ',',
            fractionWidth = 2,
            integerWidth = 3,
            min = 0.10,
            max = 600.00,
            increment = 0.10
        )
        timeInBetweenCtrl.SetInitialSize((90,-1))
        mySizer.Add(timeInBetweenCtrl,(1,1))

        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtStep
            ),
           (2,0)
        )
        stepCtrl = panel.SpinIntCtrl(step, 1, 34)
        stepCtrl.SetInitialSize((40,-1))
        mySizer.Add(stepCtrl,(2,1))

        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.level_txt
            ), (3,0)
        ) 
        levelCtrl = wx.Slider(
            panel,
            -1,
            level,
            0,
            100,
            (10, 10),
            (200, 50),
            wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        mySizer.Add(levelCtrl, (3,1))

        panel.sizer.Add(mySizer, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            if self.plugin.dll is not None and len(deviceList) > 0:
                device = indexToIdMap[deviceCtrl.GetSelection()]
                gn = self.plugin.dll.tdGetName(device)
                deviceName = (c_char_p(gn)).value.decode('utf-8')
                self.plugin.dll.tdReleaseString(gn)
                timeInBetween = timeInBetweenCtrl.GetValue()
                step = stepCtrl.GetValue()
                level = levelCtrl.GetValue()
                panel.SetResult(
                    deviceName,
                    timeInBetween,
                    step,
                    level
                )
                indx = 0
                for m_name in eg.document.__dict__['root'].childs:
                    if(
                        m_name.name.find(deviceName)!= -1
                        and
                        m_name.name.find('Dim')!= -1
                    ):
                        new_name = (
                            'TellStickDuo: Dim gradually'+
                            deviceName+
                            ' to '+
                            str(level)+
                            '%'
                        )
                        eg.document.__dict__['root'].childs[indx].name = new_name
                        eg.document.__dict__['root'].childs[indx].Refresh()
                    indx += 1
            else:
                deviceName = ''



class StopGoodMorning(eg.ActionClass):
    name = "Stop all running Good Morning schedules"
    description = "Stops all running Good Morning schedules."
    iconFile = "stop"

    def __call__(self):
        print self.text.info
        self.plugin.gMschedules = False



class GoodMorning(eg.ActionClass):
    name = "GoodMorning"
    description = "Dims a TellStick device stepwise delayed until defined level."
    iconFile = "lamp-dim"
    method = TELLSTICK_DIM

    def __call__(self, deviceName, timeToWakeUp, maxWakeUpLevel):
        self.increase = int(255/(timeToWakeUp*3))
        self.maxLevel = int(maxWakeUpLevel*255/100)
        self.deviceName = deviceName
        self.id = self.plugin.getId(self.deviceName, self.method)
        self.finished = Event()
        self.GoodMorning = Thread(
            target=self.GoodMorningThread,
            name="GoodMorning"
        )
        self.plugin.gMschedules = True
        self.GoodMorning.start()


    def GoodMorningThread(self):
        while not self.finished.isSet():
            level=1
            while level < self.maxLevel and self.plugin.gMschedules:
                self.plugin.scheduleCommand(self.id, 'Dim', level)
                level += self.increase
                self.finished.wait(20.0)
            self.finished.set()
            time.sleep(0.1)
            self.plugin.scheduleCommand(self.id, 'Dim', self.maxLevel)
            print "Good Morning action finished"
            self.plugin.TriggerEvent(
                "Good Morning action finished: "+self.deviceName,
                payload = str(self.id)
            )
            

    def Configure(
        self,
        deviceName='',
        timeToWakeUp=15,
        maxWakeUpLevel=100
    ):
        deviceList = []
        indexToIdMap = {}
        try:
            numDevices = self.plugin.dll.tdGetNumberOfDevices()
        except:
            numDevices = 0
        selected = 0
        for i in range(numDevices):
            id = self.plugin.dll.tdGetDeviceId(i)
            methods = self.plugin.dll.tdMethods(
                            id,
                            TELLSTICK_DIM
                      )
            if (methods & self.method):
                index = len(deviceList)
                gn = self.plugin.dll.tdGetName(id)
                name = (c_char_p(gn)).value
                self.plugin.dll.tdReleaseString(gn)
                if (name == deviceName.encode('utf-8')):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name.decode('utf-8'))

        panel = eg.ConfigPanel(self)
        mySizer = wx.GridBagSizer(10, 10)
        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)
        self.timeToWakeUpCtrl = wx.Slider(
                            panel,
                            -1,
                            timeToWakeUp,
                            0,
                            100,
                            (10, 10),
                            (200, 50),
                            wx.SL_HORIZONTAL | wx.SL_LABELS
                         )
        self.maxWakeUpLevelCtrl = wx.Slider(
                            panel,
                            -1,
                            maxWakeUpLevel,
                            0,
                            100,
                            (10, 10),
                            (200, 50),
                            wx.SL_HORIZONTAL | wx.SL_LABELS
                         )

        if (len(deviceList) > 0):
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.device_txt
                ), (1,0)
            )
        else:
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.no_device_txt_1+
                    self.name+
                    self.plugin.text.no_device_txt_2+
                    self.plugin.text.no_device_txt_3
                ), (1,0)
            )
       
        mySizer.Add(deviceCtrl, (1,1))
        
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.timeToWakeUp_txt
            ), (3,0)
        ) 
        mySizer.Add(self.timeToWakeUpCtrl, (3,1))

        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.maxWakeUpLevel_txt
            ), (4,0)
        ) 
        mySizer.Add(self.maxWakeUpLevelCtrl, (4,1))

        panel.sizer.Add(mySizer, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            if self.plugin.dll is not None and len(deviceList) > 0:
                device = indexToIdMap[deviceCtrl.GetSelection()]
                gn = self.plugin.dll.tdGetName(device)
                deviceName = (c_char_p(gn)).value.decode('utf-8')
                self.plugin.dll.tdReleaseString(gn)
                timeToWakeUp = self.timeToWakeUpCtrl.GetValue()
                maxWakeUpLevel = self.maxWakeUpLevelCtrl.GetValue()
                panel.SetResult(
                    deviceName,
                    timeToWakeUp,
                    maxWakeUpLevel
                )
                indx = 0
                for m_name in eg.document.__dict__['root'].childs:
                    if(
                        m_name.name.find(deviceName)!= -1
                        and
                        m_name.name.find('Good morning')!= -1
                    ):
                        new_name = (
                            'TellStickDuo: '+
                            'Good morning in '+
                            str(timeToWakeUp)+
                            ' minutes.'+
                            ' Device: '+
                            deviceName
                        )
                        eg.document.__dict__['root'].childs[indx].name = new_name
                        eg.document.__dict__['root'].childs[indx].Refresh()
                    indx += 1
            else:
                deviceName = ''



class StopGoodNight(eg.ActionClass):
    name = "Stop all running Good Night schedules"
    description = "Stops all running Good Night schedules."
    iconFile = "stop"

    def __call__(self):
        print self.text.info
        self.plugin.gNschedules = False



class GoodNight(eg.ActionClass):
    name = "GoodNight"
    description = "Dims a TellStick device stepwise delayed until turned off."
    iconFile = "lamp-dim"
    method = TELLSTICK_DIM

    def __call__(
        self,
        deviceName,
        timeToSleep,
        startFromCurrent
    ):
        self.startFromCurrent = startFromCurrent
        self.deviceName = deviceName
        self.id = self.plugin.getId(self.deviceName, self.method)
        self.currentLevel = int(self.plugin.lastSentValue(self.id))
        if self.startFromCurrent:
            self.decrease = int(self.currentLevel/(timeToSleep*3))
        else:
            self.decrease = int(255/(timeToSleep*3))
        if self.decrease > 0:
            self.finished = Event()
            self.GoodNight = Thread(
                target=self.GoodNightThread,
                name="GoodNight"
            )
            self.plugin.gNschedules = True
            self.GoodNight.start()


    def GoodNightThread(self):
        while not self.finished.isSet():
            if self.startFromCurrent:
                level = self.currentLevel
            else:
                level=255
            while level > 0 and self.plugin.gNschedules:
                self.plugin.scheduleCommand(self.id, 'Dim', level)
                level -= self.decrease
                self.finished.wait(20.0)
            self.finished.set()
            time.sleep(0.1)
            self.plugin.scheduleCommand(self.id, 'Dim', 0)
            print "Good Night action finished"
            self.plugin.TriggerEvent(
                "Good Night action finished: "+self.deviceName,
                payload = str(self.id)
            )
            

    def Configure(
        self,
        deviceName='',
        timeToSleep=15,
        startFromCurrent=True
    ):
        deviceList = []
        indexToIdMap = {}
        try:
            numDevices = self.plugin.dll.tdGetNumberOfDevices()
        except:
            numDevices = 0
        selected = 0
        for i in range(numDevices):
            id = self.plugin.dll.tdGetDeviceId(i)
            methods = self.plugin.dll.tdMethods(
                            id,
                            TELLSTICK_DIM
                      )
            if (methods & self.method):
                index = len(deviceList)
                gn = self.plugin.dll.tdGetName(id)
                name = (c_char_p(gn)).value
                self.plugin.dll.tdReleaseString(gn)
                if (name == deviceName.encode('utf-8')):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name.decode('utf-8'))

        panel = eg.ConfigPanel(self)
        mySizer = wx.GridBagSizer(10, 10)
        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)
        self.timeToSleepCtrl = wx.Slider(
                            panel,
                            -1,
                            timeToSleep,
                            0,
                            100,
                            (10, 10),
                            (200, 50),
                            wx.SL_HORIZONTAL | wx.SL_LABELS
                         )

        if (len(deviceList) > 0):
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.device_txt
                ), (1,0)
            )
        else:
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.no_device_txt_1+
                    self.name+
                    self.plugin.text.no_device_txt_2+
                    self.plugin.text.no_device_txt_3
                ), (1,0)
            )
       
        mySizer.Add(deviceCtrl, (1,1))
        
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.timeToSleep_txt
            ), (3,0)
        ) 
        mySizer.Add(self.timeToSleepCtrl, (3,1))

        startFromCurrentCtrl = wx.CheckBox(panel, -1, "")
        startFromCurrentCtrl.SetValue(startFromCurrent)
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.startFromCurrent_txt
            ),
            (4,0)
        )
        mySizer.Add(startFromCurrentCtrl, (4,1))

        panel.sizer.Add(mySizer, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            if self.plugin.dll is not None and len(deviceList) > 0:
                device = indexToIdMap[deviceCtrl.GetSelection()]
                gn = self.plugin.dll.tdGetName(device)
                deviceName = (c_char_p(gn)).value.decode('utf-8')
                self.plugin.dll.tdReleaseString(gn)
                timeToSleep = self.timeToSleepCtrl.GetValue()
                startFromCurrent = startFromCurrentCtrl.GetValue()
                panel.SetResult(
                    deviceName,
                    timeToSleep,
                    startFromCurrent
                )
                indx = 0
                for m_name in eg.document.__dict__['root'].childs:
                    if(
                        m_name.name.find(deviceName)!= -1
                        and
                        m_name.name.find('Good night')!= -1
                    ):
                        new_name = (
                            'TellStickDuo: '+
                            'Good night in '+
                            str(timeToSleep)+
                            ' minutes.'+
                            ' Device: '+
                            deviceName
                        )
                        eg.document.__dict__['root'].childs[indx].name = new_name
                        eg.document.__dict__['root'].childs[indx].Refresh()
                    indx += 1
            else:
                deviceName = ''



class DimPercentage(eg.ActionClass):
    name = "Dim up/down with a defined step size"
    description = "Dims a TellStick device up or down with a defined step size."
    iconFile = "lamp-dim"
    method = TELLSTICK_DIM

    def __call__(self, deviceName, bStepUp, level):
        self.deviceName = deviceName.encode('utf-8')
        self.id = self.plugin.getId(self.deviceName, self.method)
        self.bStepUp = bStepUp
        self.level = int(level*255/100)
#        self.level = int(level)
        self.DimPercentage()
        dP = self.plugin.dimPercentage
        return self.ConvertLevelsToPercentage(dP)


    def DebugLog(self, v, txt):
        if self.plugin.bDebug:
            print(
                int(round(float(v)*100/255, 0)),
                txt
            )


    def ConvertLevelsToPercentage(self, dct):
        d = {}
        for i in dct:
            d[i] = int(round(float(dct[i])*100/255, 0))
        return d
        

    def DimPercentage(self):
        ref_level = 0
        the_level = 0
        to_send = 0
        k_msg = ''
        m_key = (
            str(self.id)
        )
        try:
            ref_level = int(self.plugin.dimPercentage[m_key])
            the_level = ref_level
            self.DebugLog(ref_level, 'Previously saved dim level')
        except:
            pass           
        func = self.plugin.dll.tdLastSentValue
        func.restype = c_char_p
        ret = str(func(self.id))
        if not ret.isdigit():
            ret = str(the_level)
        self.DebugLog(ret, 'API reported dim level')
        if int(ret) > 0 and int(ret) < 255:
            the_level = int(ret)
        if self.bStepUp: 
            the_level += int(self.level)
            if the_level < 0:
                to_send = 0
            else:
                to_send = the_level
            if the_level > 255:
                to_send = 255
        else:
            the_level -= int(self.level)
            if the_level < 0:
                to_send = 0
            else:
                to_send = the_level
            if the_level > 255:
                to_send = 255
        self.plugin.scheduleCommand(self.id, 'Dim', to_send)
        self.DebugLog(to_send, 'Sent dim level to device')
        k_msg = (
            str(the_level)
        )
        if ref_level >= 0 and ref_level <= 255:
            if the_level <> ref_level:
                self.plugin.dimPercentage[m_key] = k_msg
        if ref_level < 0 :
            if the_level > ref_level:
                self.plugin.dimPercentage[m_key] = k_msg
        if ref_level > 255 :
            if the_level < ref_level:
                self.plugin.dimPercentage[m_key] = k_msg
        self.plugin.dimDeviceData[m_key] = (
            k_msg+
            '|'+
            self.deviceName
        )        
        self.DebugLog(self.plugin.dimPercentage[m_key], 'New reference level')


    def Configure(
            self,
            deviceName = 'Dim up/down with a defined step size',
            bStepUp = True,
            level = 15
        ):
        panel = eg.ConfigPanel(self)
        mySizer = wx.GridBagSizer(10, 10)
        deviceList = []
        indexToIdMap = {}
        selected = 0

        try:
            numDevices = self.plugin.dll.tdGetNumberOfDevices()
        except:
            numDevices = 0

        for i in range(numDevices):
            id = self.plugin.dll.tdGetDeviceId(i)
            methods = self.plugin.dll.tdMethods(
                            id,
                            TELLSTICK_DIM
                      )
            if (methods & self.method):
                index = len(deviceList)
                gn = self.plugin.dll.tdGetName(id)
                name = (c_char_p(gn)).value
                self.plugin.dll.tdReleaseString(gn)
                if (name == deviceName.encode('utf-8')):
                    selected = index
                indexToIdMap[index] = id
                deviceList.append(name.decode('utf-8'))

        deviceCtrl = wx.Choice(panel, -1, choices=deviceList)
        deviceCtrl.Select(selected)
        if (len(deviceList) > 0):
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.device_txt
                ), (0,0)
            )
        else:
            mySizer.Add(
                wx.StaticText(
                    panel,
                    -1,
                    self.plugin.text.no_device_txt_1+
                    self.name+
                    self.plugin.text.no_device_txt_2+
                    self.plugin.text.no_device_txt_3
                ), (0,0)
            )
        mySizer.Add(deviceCtrl, (0,1))

        bStepUpCtrl = wx.CheckBox(panel, -1, "")
        bStepUpCtrl.SetValue(bStepUp)
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.step_up
            ),
            (1,0)
        )
        mySizer.Add(bStepUpCtrl, (1,1))

        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.level_txt
            ), (2,0)
        ) 
        levelCtrl = wx.Slider(
            panel,
            -1,
            level,
            0,
            100,
#            255,
            (10, 10),
            (200, 50),
            wx.SL_HORIZONTAL | wx.SL_LABELS
        )
        mySizer.Add(levelCtrl, (2,1))

        panel.sizer.Add(mySizer, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            direction = 'Up'
            if self.plugin.dll is not None and len(deviceList) > 0:
                device = indexToIdMap[deviceCtrl.GetSelection()]
                gn = self.plugin.dll.tdGetName(device)
                deviceName = (c_char_p(gn)).value.decode('utf-8')
                self.plugin.dll.tdReleaseString(gn)
                bStepUp = bStepUpCtrl.GetValue()
                if not bStepUp:
                    direction = 'Down'
                level = levelCtrl.GetValue()
                panel.SetResult(
                    deviceName,
                    bStepUp,
                    level
                )
                indx = 0
                for m_name in eg.document.__dict__['root'].childs:
                    if(
                        m_name.name.find(deviceName)!= -1
                        and
                        m_name.name.find('Dim')!= -1
                    ):
                        new_name = (
                            'TellStickDuo.'+
                            deviceName+
                            ' Dim with steps: '+
                            direction+
                            ' '+
                            str(level)
                        )
                        eg.document.__dict__['root'].childs[indx].name = new_name
                        eg.document.__dict__['root'].childs[indx].Refresh()
                    indx += 1
            else:
                deviceName = ''




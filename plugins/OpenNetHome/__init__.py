# -*- coding: utf-8 -*-
#
# plugins/OpenNetHome/__init__.py
#
# Copyright (C) 2016
# Walter Kraembring
#
##############################################################################
# Revision history:
#
# 2016-09-02  Added a new action to send commands via the REST interface
# 2016-08-03  New edition - partly rewritten
##############################################################################
eg.RegisterPlugin(
    name = "OpenNetHome",
    guid = '{D2C99FD0-0239-4715-A9EF-878411C02452}',
    author = "Walter Kraembring",
    version = "1.0.2",
    canMultiLoad = True,
    kind = "other",
    url = "http://wiki.nethome.nu/doku.php/start",
    description = (
        '<p>Plugin to receive messages from and send commands to OpenNetHome</p>'
        '\n\n<p><a href="http://opennethome.org/">Product details...</a></p>'
        '<center><img src="nethomeserver.png" /></center>'
    ),
)

import eg
import socket
import httplib
import time
import os
import sys
import winsound
import calendar
import random
import Queue
from datetime import datetime, timedelta
from threading import Event, Thread



class Text:
    started = "Plugin started"
    hostName = "Host name or ip:"
    portNumber = "Port number:"
    socketTimeOut = "Time Out for socket connection (seconds):"
    windSpeed = "Check if windspeed shall be presented in m/s:"
    soundOnEvent = "Beep on events:"
    repeats = "Allow repeated events:"
    delay = "Delay of repeats (sec):"
    logToFile = "Log events to file:"
    debug = "Turn debug ON:"
    txtBattLow = "Battery low"
    lostSensors = "Set time out for lost sensors (sec):"
    subscribe = "Request to Subscribe: "
    connection_etablished = "Connection with OpenNetHome TCP interface established"
    connection_error = "Connection error: "
    rest_connection_error = "Connection with OpenNetHome REST interface failed"
    tcp_connection_error = "Connection with OpenNetHome TCP interface failed"
    tcp_connection_at_start = 'Failed to connect to OpenNetHome at startup'
    tcp_EOFError_error = "EOFError in connection with OpenNetHome"
    conn_lost = "Connection with OpenNetHome lost"
    unsubscribe = "Request to Unsubscribe: "
    cleanUpmonitoring = "Cleaning up monitoring tasks..."
    readyStopped = "Plugin successfully stopped"
    ka_threadStarted = "Keep Alive thread started"    
    ka_threadStopped = "Keep Alive thread ended"    
    read_error = "Read error: "
    txt_signal_back = "Recovered contact with sensor"
    txt_taskObj = "Lost contact with sensor"
    eventPrefix = "Event prefix (default is 'ONH'):"
   
    #Threads
    thr_abort = "Thread is terminating: "

    class prontoCmd:
        deviceName = (
            "This is a device that can be controlled via OpenNetHome "+
            "using pronto codes"
        )
        pronto = "Paste the pronto code to be transmitted for this action"
        txtNbrBursts = "Number of events per control(1-10 bursts)"
        txtCmdDelay = "Delay between the events(0.5-5.0 s)"

    class smokeDetCmd:
        deviceName = (
            "This command can be used to start the buzzer in a NEXA smoke "+
            "detector device that is controlled by OpenNetHome "
        )
        address = "Paste/type the address of the smoke detector "

    class SendCommand:
        textRestPort = "Select the REST port in OpenNetHome"
        textBoxName = "Enter a descriptive name for the action"
        textBoxObj = "Select the object to be controlled"
        textBoxAttribute = "Select the command to send"
        rest_connection_error = "Connection with OpenNetHome REST interface failed"

    class SendRESTcommand:
        textRestPort = "Select the REST port in OpenNetHome"
        textBoxName = "Enter a descriptive name for the action"
        textBoxObj = "Select the object to be controlled"
        textBoxAttribute = "Select the command to send"
        rest_connection_error = "Connection with OpenNetHome REST interface failed"

    class RollerTrolCommand:
        textRestPort = "Select the REST port in OpenNetHome"
        textBoxName = "Enter a descriptive name for the action"
        textBoxObj = "Select the object to be controlled"
        textBoxAttribute = "Select the command to send"
        rest_connection_error = "Connection with OpenNetHome REST interface failed"


            
class CurrentStateData(eg.PersistentData):
    sensors_status = {}



class WeatherData(eg.PersistentData):
    rain_Week_levels = {}
    rain_Week_dates = {}



class ONH(eg.PluginClass):
    text = Text
        
    def __init__(self):
        self.AddAction(SendCommand)
        self.AddAction(SendRESTcommand)
        self.AddAction(RollerTrolCommand)
        self.AddAction(ClearSensorsStatus)
        self.AddAction(GetWeeklyRainLevels)
        self.AddAction(GetAverageWindLevels)
        self.AddAction(prontoCmd)
        self.AddAction(smokeDetCmd)
        self.rain_level_values_last_week = []
        self.rain_level_dates_last_week = []
        self.wind_level_average_15 = []
        self.wind_level_average_60 = []
        self.sensors_status = CurrentStateData.sensors_status
        self.OkButtonClicked = False
        self.started = False


    def __start__(
        self,
        hostName,
        portNbr,
        bSpeed_ms,
        socketTout,
        lostSensors,
        bSound,
        bRepeats,
        delayRepeat,
        bLogToFile,
        bDebug,
        prefix
    ):
        print self.text.started
        self.hostName = hostName
        self.portNbr = portNbr
        self.bSpeed_ms = bSpeed_ms
        self.socketTout = socketTout
        self.lostSensors = lostSensors
        self.bSound = bSound
        self.bRepeats = bRepeats
        self.delayRepeat = delayRepeat
        self.bLogToFile = bLogToFile
        self.bDebug = bDebug
        self.bTaskAdded = False
        self.prevEvent = ''
        self.wDirection = [
            'N',
            'NNE',
            'NE',
            'ENE',
            'E',
            'ESE',
            'SE',
            'SSE',
            'S',
            'SSW',
            'SW',
            'WSW',
            'W',
            'WNW',
            'NW',
            'NNW'
        ]
        self.rain_levels = [0.0, 0.0]
        self.rain_Hour = [0.0]*4
        self.rain_Hour_previous = 0.0
        self.rain_Today = [0.0, 0.0]
        self.rain_Yesterday = 0.0
        self.rain_Week_levels = [0.0]*7
        self.rain_Week_dates = ['']*7
        self.rain_Week_sum = 0.0
        self.bNewDay = False
        self.wj = 0
        self.wi = 0
        self.wdLevels_15 = []
        self.wdLevels_60 = []
        self.wdLabel = ""
        self.wdLabelPrevious = "Unknown"
        self.old_lst = []
        self.iRainSim = 0
        self.bSimulate = False
#        self.bSimulate = True
        self.started = True
        self.conn_error = True
        self.semaPhore = True
        self.rest_port = 8020
        self.prefix = prefix
        self.monitor_oregon_mem = {}        
        self.decode_oregon_mem = {}
        self.monitor_fineoffset_mem = {}        
        self.decode_fineoffset_mem = {}
        self.monitor_mandolyn_mem = {}        
        self.decode_mandolyn_mem = {}
        self.msgCounter = {}
        self.msgCounterPrev = {}
        self.resp = None
        self.conn = None
        self.reconnects = 0
        self.obj_id = {}

#        if self.OkButtonClicked:
#            self.OkButtonClicked = False

        progData = eg.configDir + '\plugins\OpenNetHome'

        if (
            not os.path.exists(progData)
            and not os.path.isdir(progData)
        ):
            os.makedirs(progData)

        self.mainThreadEvent = Event()
        mainThread = Thread(target=self.main, args=(self.mainThreadEvent,))
        mainThread.start()


    def __stop__(self):
        self.mainThreadEvent.set()
        if hasattr(self, 'keepAliveThreadEvent'):
            self.keepAliveThreadEvent.set()
        self.started = False
        WeatherData.rain_Week_levels[self.hostName] = self.rain_Week_levels
        WeatherData.rain_Week_dates[self.hostName] = self.rain_Week_dates

        print self.text.cleanUpmonitoring
        for i in self.monitor_oregon_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_oregon_mem[i])
            except:
                pass
        for i in self.monitor_fineoffset_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_fineoffset_mem[i])
            except:
                pass
        for i in self.monitor_mandolyn_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_mandolyn_mem[i])
            except:
                pass
        if hasattr(self, 'remain'):
            eg.Wait(self.remain + 0.5)
        print self.text.readyStopped
        eg.TriggerEvent(
            self.text.readyStopped,
            prefix = self.prefix
        )


    def __close__(self):
        self.started = False


    def sensorLost(self, myArgument):
        eg.TriggerEvent(repr(myArgument), prefix = self.prefix)
        lc = myArgument.split(':')[1].split(' ')[1]
        try:
            del self.sensors_status[lc]
        except:
            pass
        try:
            self.sensors_status[lc] = myArgument
        except:
            pass

 
    def sensorBack(self, myArgument):
        eg.TriggerEvent(repr(myArgument), prefix = self.prefix)
        bc = myArgument.split(':')[1].split(' ')[1]
        try:
            del self.sensors_status[bc]
        except:
            pass
        try:
            self.sensors_status[bc] = myArgument
        except:
            pass
 
 
    def eventMonitor(self, monitored, pload, base, timeout):
        try:
            eg.scheduler.CancelTask(monitored)
        except:
            if pload <> None:
                self.sensorBack(
                    self.text.txt_signal_back+': '+base 
                )
        monitored = eg.scheduler.AddTask(
                timeout,
                self.sensorLost,
                self.text.txt_taskObj+': '+base
        )
        return monitored
       

    def keep_Alive(self,keepAliveThreadEvent): # Keep Alive Loop
        counter = 0
        while not keepAliveThreadEvent.isSet():
            if counter == self.socketTout or counter == 0:
                #print 'alive'
                counter = 1
                try:
                    self.KeepAlive()
                except:
                    print 'Exception occured: ', self.conn
                    self.conn = None
                    self.reconnects += 1
                finally:
                    if self.reconnects > 0:
                        print 'Total nbr of re-connects: ', self.reconnects
                    #pass
            else:
                counter += 1
            keepAliveThreadEvent.wait(1.0)
        self.conn = None
        print self.text.ka_threadStopped


    def KeepAlive(self):
        objects = {}
        if self.conn == None:
            self.conn = httplib.HTTPConnection(
                self.hostName+
                ':'+
                str(self.rest_port),
                timeout=30
            )
        self.conn.request(
            'GET', 
            "http://"+
            self.hostName+
            ':'+
            str(self.rest_port)+
            '/rest/items'
        )
        try:
            self.resp = self.conn.getresponse()
        except:
            self.resp = None
        finally:
            pass
        if self.resp <> None:
            if int(self.resp.status) == 200:
                content = self.resp.read()
                content = eval(content)
                for item in content:
                    if item['category']=='Hardware':
                        self.conn.request(
                            'GET', 
                            "http://"+self.hostName+
                            ':'+
                            str(self.rest_port)+
                            '/rest/items/'+
                            item['id']
                        )
                        self.resp = self.conn.getresponse()
                        hw = self.resp.read().replace('true', 'True')
                        hw.replace('false', 'False')
                        className = eval(hw)['name']
                        attribs = eval(hw)['attributes']
                        objects[className] = attribs[0]['value']
                        self.msgCounter[className] = 0
                        for item in attribs:
                            if(
                                item['name'] == 'ReceivedMessages' or 
                                item['name'] == 'Received'
                            ):
                                self.msgCounter[className] = int(item['value'])
                self.obj_id = {}
                for item in content:
                    if item['category']=='Lamps':
                        self.obj_id[item['name']] = item['id']
                for item in objects:
                    try:
                        try:
                            p = self.msgCounterPrev[item]
                        except:
                            self.msgCounterPrev[item] = 0
                        if self.msgCounter[item] == self.msgCounterPrev[item]:
                            if self.msgCounter[item] > 0:
                                eg.TriggerEvent(
                                    item+' is disconnected',
                                    prefix = self.prefix
                                )
                    except:
                        pass
                    print(
                        self.prefix, 
                        'Checking connection with...', 
                        item, 
                        self.msgCounter[item], 
                        self.msgCounterPrev[item]
                    )
                    self.msgCounterPrev[item] = self.msgCounter[item]
            else:
                eg.TriggerEvent(
                    'No response from REST interface...will keep on trying',
                    prefix = self.prefix
                )
                self.conn = None


    def RollerTrolMessage(self, msg):
        #print msg
        try:
            actions = {
                '12':'up', 
                '5':'stop', 
                '1':'down', 
                '4':'confirm', 
                '3':'limit', 
                '8':'reverse'
            }
               
            if msg[0]=='In':
                rDeviceCode = 'DeviceCode.'+msg[4]
                rHouseCode  = 'HouseCode.'+msg[6]
                theAction = 'Command.'+actions[msg[2]]

            if msg[0]=='Out':
                rDeviceCode = 'DeviceCode.'+msg[6]
                rHouseCode  = 'HouseCode.'+msg[8]
                theAction = 'Command.'+actions[msg[4]]

            s_lst = (
                'RollerTrol'+"."+
                rDeviceCode +"."+
                rHouseCode +"."+
                theAction
            )
            p_lod = (    
               ''
            )
            eg.TriggerEvent(s_lst, payload = p_lod, prefix = self.prefix)
        except:
            pass
            

    def FineOffsetMessage(self, fineOffsetMsg):
        try:
            if fineOffsetMsg[3] == 'FineOffset.Moisture':
                fineOffsetTemperature = float(fineOffsetMsg[6])
                fineOffsetId = fineOffsetMsg[2]
                try:
                    fineOffsetHumidity = int(fineOffsetMsg[4])
                except:
                    fineOffsetHumidity = 0
            else:
                fineOffsetTemperature = float(fineOffsetMsg[4])
                fineOffsetId = fineOffsetMsg[2]
    
            # Calculate values from the sensor readings
            fineOffsetTemperature = (
                fineOffsetTemperature/10.0
            )
            s_lst = (
                'FineOffset'+"|"+
                fineOffsetId
            )
            if fineOffsetMsg[3] == 'FineOffset.Moisture':
                p_lod = (    
                   'Temp'+"|"+
                   str(fineOffsetTemperature)+"|"+
                   'Hum'+"|"+
                   str(fineOffsetHumidity)
                )
            else:
                p_lod = (    
                   'Temp'+"|"+
                   str(fineOffsetTemperature)
                )

            eg.TriggerEvent(s_lst, payload = p_lod, prefix = self.prefix)

            decode_param = None
            mon_param = None
            try:
                decode_param = self.plugin.decode_fineoffset_mem[s_lst]
            except:
                pass
            try:
                mon_param = self.plugin.monitor_fineoffset_mem[s_lst]
            except:
                pass
            self.plugin.monitor_fineoffset_mem[s_lst] = self.plugin.eventMonitor(
                mon_param,
                decode_param,
                s_lst,
                self.lostSensors
            )
            self.plugin.decode_fineoffset_mem[s_lst] = p_lod
        except:
            pass
            

    def OregonMessage(self, oregonMsg):
        try:
            oregonBattery = oregonMsg[6]
            oregonTemperature = float(oregonMsg[12])
            try:
                oregonHumidity = int(oregonMsg[8])
            except:
                oregonHumidity = 0
            oregonCh = oregonMsg[2]
            oregonId = oregonMsg[4]
    
            # Calculate values from the sensor readings
            oregonTemperature = (
                oregonTemperature/10.0
            )
            s_lst = (
                'Oregon'+"|"+
                oregonId+"|"+
                oregonCh+"|"
            )
            p_lod = (    
               'Temp'+"|"+
               str(oregonTemperature)+"|"+
               'Hum'+"|"+
               str(oregonHumidity)+"|"+
               'Batt'+"|"+
               str(oregonBattery)+"|"
            )
            eg.TriggerEvent(s_lst, payload = p_lod, prefix = self.prefix)
    
            if int(oregonBattery) == 1:
                # Create the eg battery low event
                eg.TriggerEvent(
                    s_lst+
                    self.text.loggerAction.txtBattLow, prefix = self.prefix
                )
                if self.bLogToFile:
                    logStr = (
                        s_lst+
                        self.text.loggerAction.txtBattLow
                    )
                    self.LogToFile(logStr)

            decode_param = None
            mon_param = None
            try:
                decode_param = self.plugin.decode_oregon_mem[s_lst]
            except:
                pass
            try:
                mon_param = self.plugin.monitor_oregon_mem[s_lst]
            except:
                pass
            self.plugin.monitor_oregon_mem[s_lst] = self.plugin.eventMonitor(
                mon_param,
                decode_param,
                s_lst,
                self.lostSensors
            )
            self.plugin.decode_oregon_mem[s_lst] = p_lod
        except:
            pass


    def UpmMessage(self, upmMsg):
        if (
            len(upmMsg[1]) > 0
            and len(upmMsg[2]) > 0
            and len(upmMsg[3]) > 0
            and len(upmMsg[4]) > 0
            and len(upmMsg[5]) > 0
            and len(upmMsg[6]) > 0
            and upmMsg[6] != " "
            and upmMsg[6].isdigit()
            and len(upmMsg[7]) > 0
            and len(upmMsg[8]) > 0
            and len(upmMsg[9]) > 0
            and len(upmMsg[10]) > 0
            and upmMsg[10] != " "
            and upmMsg[10].isdigit()
        ):
            upmBattery = upmMsg[6]
            upmTemperature = float(upmMsg[8])
            upmHumidity = int(upmMsg[10])
            upmDevice = upmMsg[2]
            upmHouse = upmMsg[4]
    
            # Calculate values from the sensor readings
            if int(upmHouse) != 10:
                upmTemperature = (
                    (upmTemperature * 0.0625) - 50.0
                )
                upmHumidity = upmHumidity / 2
                s_lst = (
                    'UPM/ESIC'+"|"+
                    str(upmMsg[3])+"|"+
                    str(upmHouse)+"|"+
                    str(upmMsg[1])+"|"+
                    str(upmDevice)+"|"
                )
                p_lod = (    
                   'Temp'+"|"+
                    str(upmTemperature)+"|"+
                   'Hum'+"|"+
                    str(upmHumidity)+"|"+
                    'Batt'+"|"+
                    str(upmBattery)+"|"
                 )
            else:
                # House/Device codes 10/2 are reserved
                # for wind gauges
                if int(upmDevice) == 2:
                    s_lst = (
                        'UPM/ESIC'+"|"+
                        str(upmMsg[3])+"|"+
                        str(upmHouse)+"|"+
                        str(upmMsg[1])+"|"+
                        str(upmDevice)+"|"+
                        str(upmMsg[7])+"|"+
                        str(upmBattery)+"|"
                    )
                    p_lod = self.CalcWindData(
                        upmMsg[10],
                        upmMsg[6]
                    )
    
                # House/Device codes 10/3 are reserved
                # for rain gauges
                if int(upmDevice) == 3:
                    s_lst = (
                        'UPM/ESIC'+"|"+
                        str(upmMsg[3])+"|"+
                        str(upmHouse)+"|"+
                        str(upmMsg[1])+"|"+
                        str(upmDevice)+"|"+
                        str(upmMsg[7])+"|"+
                        str(upmBattery)+"|"
                    )
                    p_lod = self.CalcRainData(
                        upmMsg[10]
                    )
    
            if int(upmHouse) > 0:
                eg.TriggerEvent(s_lst, payload = p_lod, prefix = self.prefix)
    
            if int(upmHouse) > 0 and int(upmBattery) == 1:
                # Create the eg battery low event
                eg.TriggerEvent(
                    s_lst+
                    self.text.loggerAction.txtBattLow, prefix = self.prefix
                )
                    
                if self.bLogToFile:
                    logStr = (
                        s_lst+
                        self.text.loggerAction.txtBattLow
                    )
                    self.LogToFile(logStr)

            decode_param = None
            mon_param = None
            try:
                decode_param = self.plugin.decode_mandolyn_mem[s_lst]
            except:
                pass
            try:
                mon_param = self.plugin.monitor_mandolyn_mem[s_lst]
            except:
                pass
            self.plugin.monitor_mandolyn_mem[s_lst] = self.plugin.eventMonitor(
                mon_param,
                decode_param,
                s_lst,
                self.lostSensors
            )
            self.plugin.decode_mandolyn_mem[s_lst] = p_lod

    
    def CalcRainData(self, rLevel ):
        self.rain_Week_sum = 0.0
        rainLevel = float(rLevel) * 0.7
        self.rain_levels[0] = self.rain_levels[1]
        self.rain_levels[1] = rainLevel
        date = str(time.strftime("%m/%d/%Y", time.localtime()))
        ydate = datetime.today() - timedelta(1)
        toDate = str(time.strftime("%Y-%m-%d", time.localtime()))
        yesterDate = str(ydate).split(' ')[0]
        d = self.GetDayOfWeek(date) # Monday = 0
        dy = 0 

        if d == 0:
            dy = 6
        else:
            dy = d - 1

        if (self.rain_levels[0] > self.rain_levels[1]): # Rain gauge reset
            self.rain_levels = [0.0, 0.0]

        if ( # Plugin startup
            self.rain_Today[0] == 0.0
            and
            self.rain_Today[1] == 0.0
        ):
            start = time.clock()
            self.rain_Hour[1] = start
            
        if (self.rain_levels[1] >= self.rain_levels[0]):
            now = time.clock()
            self.rain_Hour[2] += self.rain_levels[1] - self.rain_levels[0]
            self.rain_Hour[3] = now
            self.rain_Today[1] += self.rain_levels[1] - self.rain_levels[0]

            #Last hour
            h_diff_time = now - self.rain_Hour[1]
            #print h_diff_time
            if (h_diff_time > 3600): # One hour has elapsed
                self.rain_Hour[0] = self.rain_Hour[2]
                self.rain_Hour[2] = 0.0
                self.rain_Hour[1] = now
                self.rain_Hour_previous = self.rain_Hour[0]
                
            #Last day & yesterday & week
            t_now = time.strftime("%H", time.localtime())
            if (int(t_now) == 0 and not self.bNewDay):
                self.bNewDay = True # A new day begins
                self.rain_Today[0] = self.rain_Today[1]
                self.rain_Today[1] = 0.0
                self.rain_Week_levels[dy] = self.rain_Today[0]
                self.rain_Week_dates[dy] = yesterDate
            if (int(t_now) > 0 and self.bNewDay):
                self.bNewDay = False
                                          
        for item in self.rain_Week_levels:
            self.rain_Week_sum += item

        self.rain_Yesterday = self.rain_Week_levels[dy]
        date_Yesterday = self.rain_Week_dates[dy]
        self.plugin.rain_level_values_last_week = self.rain_Week_levels
        self.plugin.rain_level_dates_last_week = self.rain_Week_dates
        p_lod = (    
            "UPM.RainLastHour|"+
            str(self.rain_Hour[2])+"|"+
            "mm"+"|"+
            "UPM.RainPreviousHour|"+
            str(self.rain_Hour_previous)+"|"+
            "mm"+"|"+
            "UPM.RainToday|"+
            str(self.rain_Today[1])+"|"+
            "mm"+"|"+
            "UPM.RainYesterday|"+
            str(date_Yesterday)+"|"+
            str(self.rain_Yesterday)+"|"+
            "mm"+"|"+
            "UPM.RainLastWeek|"+
            str(self.rain_Week_sum)+"|"+
            "mm"+"|"+
            "UPM.RainMeter|"+
            str(rainLevel)+"|"+
            "mm"+"|"
        )
        return p_lod
        
        
    def CalcWindData(self, wSpeed, wDir):    
        wdSpeed = float(wSpeed)
        windSpeedSum_15 = 0.0
        windSpeedSum_60 = 0.0

        if (int(wDir) <= 30):
            if (self.wdLabel != ""):
                if (self.wdLabelPrevious != self.wDirection[int(wDir)/2]):
                    self.wdLabelPrevious = self.wdLabel
            self.wdLabel = self.wDirection[int(wDir)/2]
        else:
            print "Wind direction out of range:", self.wdLabel
            self.wdLabel = "Out of range"

        if self.plugin.bSpeed_ms:
            wdSpeed = (wdSpeed*1000)/3600

        if len(self.wdLevels_15) < 15:
            self.wdLevels_15.append(wdSpeed)
        else:
            self.wdLevels_15[self.wi] = wdSpeed

        if len(self.wdLevels_60) < 60:
            self.wdLevels_60.append(wdSpeed)
        else:
            self.wdLevels_60[self.wj] = wdSpeed
        
        self.wi += 1
        self.wj += 1
        
        for k in range(len(self.wdLevels_15)):
            windSpeedSum_15 += self.wdLevels_15[k] 

        wdSpeedAv_15 = windSpeedSum_15 / self.wi

        for m in range(len(self.wdLevels_60)):
            windSpeedSum_60 += self.wdLevels_60[m] 

        wdSpeedAv_60 = windSpeedSum_60 / self.wj

        if (self.wi > 14):
            self.wi = 0

        if (self.wj > 59):
            self.wj = 0

        self.plugin.wind_level_average_15 = self.wdLevels_15
        self.plugin.wind_level_average_60 = self.wdLevels_60
        p_lod = (    
            "UPM.WindDirection|"+
            self.wdLabel+"|"+
            "UPM.WindDirectionPrevious|"+
            self.wdLabelPrevious+"|"+
            "UPM.WindSpeed|"+
            str(wdSpeed)+"|"+
            "UPM.WindSpeedAverage_15|"+
            str(wdSpeedAv_15)+"|"+
            "UPM.WindSpeedAverage_60|"+
            str(wdSpeedAv_60)+"|"
         )
        return p_lod


    def GetDayOfWeek(self, dateString):
        # day of week (monday = 0) of a given month/day/year
        ds = dateString.split('/')
        dayOfWeek = int(calendar.weekday(int(ds[2]),int(ds[0]),int(ds[1])))
        return(dayOfWeek)


    def ClearBuffer(self):
        self.old_lst = []
        self.bTaskAdded = False


    def LogToFile(self, s):
        timeStamp = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        fileDate = str(
            time.strftime("%Y%m%d", time.localtime())
        )
        logStr = timeStamp+" "+s+"<br\n>"
        fileHandle = None
        progData = eg.configDir + '\plugins\OpenNetHome'

        if (
            not os.path.exists(progData)
            and not os.path.isdir(progData)
        ):
            os.makedirs(progData)

        fileHandle = open (
            progData+'/'+fileDate+'Logger_'+
            self.prefix+'.html', 'a'
        )
        fileHandle.write ( logStr )
        fileHandle.close ()


    def debugLogToFile(self, s):
        timeStamp = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        fileDate = str(
            time.strftime("%Y%m%d", time.localtime())
        )
        logStr = timeStamp+" "+s+"<br\n>"
        fileHandle = None
        progData = eg.configDir + '\plugins\OpenNetHome'

        if (
            not os.path.exists(progData)
            and not os.path.isdir(progData)
        ):
            os.makedirs(progData)

        fileHandle = open (
            progData+'/'+fileDate+'Logger_debug'+
            self.prefix+'.html', 'a'
        )
        fileHandle.write ( logStr )
        fileHandle.close ()


    def main(self,mainThreadEvent):

        def connectToHost():
            print 'connecting to host'
            try:
                self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.skt.connect((self.hostName, self.portNbr))
                self.skt.sendall("subscribe\r\n")
                rsp = self.skt.recv(8)
                if rsp.find("ok") != -1:
                    self.connectionError = False
                    self.skt.settimeout(self.socketTout)
                    if self.atStart != 1:
                        eg.TriggerEvent(
                            self.text.connection_etablished,
                            prefix = self.prefix
                        )
                        self.atStart = 1
                        self.keepAliveThreadEvent = Event()
                        self.remain = 0.0
                        keepAliveThread = Thread(
                            target=self.keep_Alive,
                            args=(self.keepAliveThreadEvent,)
                        )
                        keepAliveThread.start()
                        print self.text.ka_threadStarted
            except:
                self.connectionError = True
                mainThreadEvent.wait(1.0)
            self.ack = None
            

        def reconnectToHost():
            print 'reconnect to host'
            try:
                self.skt.sendall("quit\r\n")
            except:
                pass
            self.skt.close()
            self.skt = None
            self.connectionError = True
            if self.atStart == 1:
                eg.PrintError(self.text.tcp_connection_error)
                eg.TriggerEvent(
                    self.text.tcp_connection_error,
                    prefix = self.prefix
                )
                self.atStart = 2
                self.keepAliveThreadEvent.set()
            if self.atStart == 0:
                eg.PrintError(self.text.tcp_connection_at_start)
                eg.TriggerEvent(
                    self.text.tcp_connection_at_start,
                    prefix = self.prefix
                )
                self.atStart = 3
            mainThreadEvent.wait(1.0)
            connectToHost()


        def analyzeEvent():
            lst = []
            mlst = []
            iPronto = 0

            try:
                self.rain_Week_levels = WeatherData.rain_Week_levels[self.hostName]
                self.rain_Week_dates = WeatherData.rain_Week_dates[self.hostName]
            except:
                pass
    
            while not self.q.empty():
                m = self.q.get()
                if m != '':
                    mlst.append(m)
            
            for m in mlst:    
                lst = ("OpenNetHome" + "," + m).split(',')
                #print lst
                
                if (
                    lst.count('UPM.HouseCode') > 0
                    and lst.count('UPM.SequenceNumber') > 0
                ):
                    #print lst
                    lst = lst[:15]
    
                try:
                    iPronto = lst.index('Pronto.Message')
                except ValueError:
                    iPronto = -1 # no match
    
                if (
                    lst.count("OpenNetHome") > 0 and
                    lst.count("event") > 0 and 
                    lst.count("Value") > 0
                ):
                    if not self.bTaskAdded or lst <> self.prevEvent:
                        self.prevEvent = lst
                        try:
                            eg.scheduler.CancelTask(self.taskObj)
                            self.bTaskAdded = False
                        except ValueError:
                            pass
        
                        # Code used for UPM/ESIC Rain and Wind gauge simulation ####                
                        if self.bSimulate:
                            self.iRainSim += 1
            
                            if self.iRainSim%2==0:
                                lst = [
                                    'OpenNetHome',
                                    'event',
                                    'UPM_Message',
                                    'Direction',
                                    'In',
                                    'UPM.DeviceCode',
                                    '3',
                                    'UPM.HouseCode',
                                    '10',
                                    'UPM.Humidity',
                                    '0',
                                    'UPM.LowBattery',
                                    '0',
                                    'UPM.Temp',
                                    '0'
                                ]
                                lst[14] = self.iRainSim
                            else:
                                lst = [
                                    'OpenNetHome',
                                    'event',
                                    'UPM_Message',
                                    'Direction',
                                    'In',
                                    'UPM.DeviceCode',
                                    '2',
                                    'UPM.HouseCode',
                                    '10',
                                    'UPM.Humidity',
                                    '0',
                                    'UPM.LowBattery',
                                    '0',
                                    'UPM.Temp',
                                    '0'
                                ]
                                twd = random.randrange(0,30,2)
                                tws = random.random()* 9.0
                                lst[14] = tws
                                lst[10] = twd
                        #####################################
            
                        if len(lst) > 0 or iPronto > 0:
                            s_lst = str(lst)
    
                            if (s_lst.find('Pronto.Message') > -1
                            ):
                                msg = ''
                                for item in range (7, len(lst)-4):
                                    msg += str(lst[item])
                                    if item < len(lst):
                                        msg += "|"
                                eg.TriggerEvent(msg, prefix = self.prefix)
    
                            if (s_lst.find('NexaFire.Address') > -1
                            ):
                                msg = ''
                                for item in range (5, len(lst)):
                                    msg += str(lst[item])
                                    if item < len(lst):
                                        msg += "|"
                                eg.TriggerEvent(msg, prefix = self.prefix)
                            
                            if (s_lst.find('NexaL.Address') > -1 and 
                                s_lst.find('NexaL.Button') > -1  and
                                s_lst.find('NexaL.Command') > -1
                            ):
                                msg = ''
                                for item in range (5, len(lst)-2):
                                    msg += str(lst[item])
                                    if item < len(lst):
                                        msg += "|"
                                eg.TriggerEvent(msg, prefix = self.prefix)
    
                            if (s_lst.find('Nexa.Button') > -1 and 
                                s_lst.find('Nexa.Command') > -1  and
                                s_lst.find('Nexa.HouseCode') > -1
                            ):
                                msg = ''
                                for item in range (5, len(lst)-2):
                                    msg += str(lst[item])
                                    if item < len(lst):
                                        msg += "|"
                                eg.TriggerEvent(msg, prefix = self.prefix)
    
                            if (s_lst.find('Hue.Command') > -1
                            ):
                                msg = ''
                                for item in range (5, len(lst)-2):
                                    msg += str(lst[item])
                                    if item < len(lst):
                                        msg += "|"
                                eg.TriggerEvent(msg, prefix = self.prefix)
    
                            if (s_lst.find('Deltronic.Command') > -1
                            ):
                                msg = ''
                                for item in range (3, len(lst)-2):
                                    msg += str(lst[item])
                                    if item < len(lst):
                                        msg += "|"
                                eg.TriggerEvent(msg, prefix = self.prefix)
    
                            if (s_lst.find('RisingSun.Command') > -1
                            ):
                                msg = ''
                                for item in range (5, len(lst)-2):
                                    msg += str(lst[item])
                                    if item < len(lst):
                                        msg += "|"
                                eg.TriggerEvent(msg, prefix = self.prefix)
    
                            if (s_lst.find('Waveman.Command') > -1
                            ):
                                msg = ''
                                for item in range (7, len(lst)):
                                    msg += str(lst[item])
                                    if item < len(lst):
                                        msg += "|"
                                eg.TriggerEvent(msg, prefix = self.prefix)
    
                            if (s_lst.find('Zhejiang.Command') > -1
                            ):
                                msg = ''
                                for item in range (7, len(lst)):
                                    msg += str(lst[item])
                                    if item < len(lst):
                                        msg += "|"
                                eg.TriggerEvent(msg, prefix = self.prefix)
    
                            if (s_lst.find('FS20Command') > -1
                            ):
                                msg = ''
                                for item in range (2, len(lst)):
                                    msg += str(lst[item])
                                    if item < len(lst):
                                        msg += "|"
                                eg.TriggerEvent(msg, prefix = self.prefix)
    
                            if(s_lst.find("UPM_Message") > -1):
                                upmMsg = lst[4:]
                                self.UpmMessage(upmMsg)
                            
                            if(s_lst.find("Oregon.Channel") > -1):
                                oregonMsg = lst[4:]
                                self.OregonMessage(oregonMsg)
    
                            if(s_lst.find("FineOffset.Identity") > -1):
                                fineOffsetMsg = lst[4:]
                                self.FineOffsetMessage(fineOffsetMsg)
       
                            if(s_lst.find("RollerTrol.HouseCode") > -1):
                                rollerTrolMsg = lst[4:]
                                self.RollerTrolMessage(rollerTrolMsg)
    
                            if self.bLogToFile:
                                self.LogToFile(
                                    self.prefix
                                    +"|"
                                    +str(lst)
                                )
        
                            if self.bDebug:
                                self.debugLogToFile(
                                    self.prefix
                                    +"|"
                                    +str(lst)
                                )
        
                            if self.bSound:                        
                                winsound.Beep(1000, 200)                
        
                            if self.bRepeats:
                                if not self.bTaskAdded:
                                    self.taskObj = eg.scheduler.AddTask(
                                        self.delayRepeat,
                                        self.ClearBuffer
                                    )
                                    self.bTaskAdded = True
                            else:
                                self.bTaskAdded = True
    

        self.skt = None
        self.connectionError = True
        self.ack = None
        self.atStart = 0
        self.q = Queue.Queue()
        self.taskObj = None
        cCount = 0
        cntr = 0
        eofErrors = 0
        event_Old = ''
        connectToHost()
        
        while not mainThreadEvent.isSet():
            if self.semaPhore:
                tst = ''
                try:
                    if cCount > 10:
                        p = ''
                        try:
                            self.skt.sendall("dir\r\n")
                            mainThreadEvent.wait(0.1)
                            p = self.skt.recv(512)
                        except:
                            p = "error"
                        cCount = 0
                        if p.find("ok") == -1:
                            self.connectionError = True
                    else:
                        mainThreadEvent.wait(0.05)
                        try:
                            tst = self.skt.recv(1024)
                        except:
                            pass
                        eofErrors = 0
                        cCount += 1
                        self.connectionError = False

                except EOFError:
                    #print 'EOFError', self.atStart
                    self.connectionError = True
                    eofErrors += 1
                    if eofErrors > 4:
                        eg.PrintError(self.text.tcp_EOFError_error)
                        eg.TriggerEvent(
                            self.text.tcp_EOFError_error,
                            prefix = self.prefix
                        )
                        eofErrors = 0

                except socket.error, e:
                    #print 'socket.error', e
                    pass

                if tst.find('Value,') and event_Old != tst:
                    cntr += 1
                    if cntr >= 3:
                        try:
                            eg.scheduler.CancelTask(self.ack)
                        except:
                            pass
                        self.ack = None
                        self.ack = eg.scheduler.AddTask(self.socketTout*3, reconnectToHost)
                        cntr = 0
                        #print 'done'
                    event_Old = tst
                    #print tst
                    e_lst = []
                    e_lst = tst.split("\n\r")
                    for ev in e_lst:
                        self.q.put(ev)
                    analyzeEvent()
                if self.connectionError:
                    mainThreadEvent.wait(5.0)
                    if self.ack == None:
                        reconnectToHost()
            else:
                mainThreadEvent.wait(0.05)
            
        try:
            self.skt.sendall("quit\r\n")
            self.skt.close()
        except:
            pass
        try:
            eg.scheduler.CancelTask(self.ack)
        except:
            pass
        time.sleep(0.1)
        print(
            self.text.unsubscribe+
            "Main-"+
            self.text.thr_abort, mainThreadEvent
        )

    
    def Configure(
        self,
        hostName = "192.168.10.253",
        portNbr = 8005,
        bSpeed_ms = True,
        socketTout = 60,
        lostSensors = 600,
        bSound = False,
        bRepeats = True,
        repeatDelay = 5.0,
        bLogToFile = False,
        bDebug = False,
        prefix = 'ONH',
        *args
    ):
        panel = eg.ConfigPanel(self, resizable=True)

        mySizer = wx.GridBagSizer(5, 5)

        hostNameCtrl = wx.TextCtrl(panel, -1, hostName)
        hostNameCtrl.SetInitialSize((250,-1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.hostName), (1,0))
        mySizer.Add(hostNameCtrl, (1,1))
    
        portCtrl = panel.SpinIntCtrl(portNbr, 0, 9000)
        portCtrl.SetInitialSize((75,-1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.portNumber), (2,0))
        mySizer.Add(portCtrl, (2,1))

        socketToutCtrl = panel.SpinIntCtrl(socketTout, 5, 9999)
        socketToutCtrl.SetInitialSize((75,-1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.socketTimeOut), (3,0))
        mySizer.Add(socketToutCtrl, (3,1))

        speedCtrl = panel.CheckBox(bSpeed_ms, "")
        speedCtrl.SetValue(bSpeed_ms)
        mySizer.Add(wx.StaticText(panel, -1, self.text.windSpeed), (4,0))
        mySizer.Add(speedCtrl, (4,1))

        bRepeatsCtrl = wx.CheckBox(panel, -1, "")
        bRepeatsCtrl.SetValue(bRepeats)
        mySizer.Add(wx.StaticText(panel, -1, self.text.repeats), (5,0))
        mySizer.Add(bRepeatsCtrl, (5,1))

        repeatDelayCtrl = panel.SpinNumCtrl(
            repeatDelay,
            decimalChar = '.', # by default, use '.' for decimal point
            groupChar = ',',   # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 3,
            min = 0.0,
            max = 999.9,
            increment = 0.5
        )
        repeatDelayCtrl.SetInitialSize((60,-1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.delay), (6,1))
        mySizer.Add(repeatDelayCtrl, (6,2))

        lostSensorsCtrl = panel.SpinIntCtrl(lostSensors, 100, 180000)
        lostSensorsCtrl.SetInitialSize((70,-1))
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.lostSensors
            ),
           (7,1)
        )
        mySizer.Add(lostSensorsCtrl,(7,2))

        bLogToFileCtrl = wx.CheckBox(panel, -1, "")
        bLogToFileCtrl.SetValue(bLogToFile)
        mySizer.Add(wx.StaticText(panel, -1, self.text.logToFile), (8,0))
        mySizer.Add(bLogToFileCtrl, (8,1))

        bSoundCtrl = wx.CheckBox(panel, -1, "")
        bSoundCtrl.SetValue(bSound)
        mySizer.Add(wx.StaticText(panel, -1, self.text.soundOnEvent), (9,0))
        mySizer.Add(bSoundCtrl, (9,1))

        bDebugCtrl = wx.CheckBox(panel, -1, "")
        bDebugCtrl.SetValue(bDebug)
        mySizer.Add(wx.StaticText(panel, -1, self.text.debug), (10,0))
        mySizer.Add(bDebugCtrl, (10,1))

        eventPrefixCtrl = wx.TextCtrl(panel, -1, prefix)
        eventPrefixCtrl.SetInitialSize((100,-1))
        mySizer.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.eventPrefix
            ),
           (11,0)
        )
        mySizer.Add(eventPrefixCtrl,(11,1))

        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)


        def OnApplyButton(event): 
            event.Skip()


        def OnOkButton(event): 
            event.Skip()
            self.OkButtonClicked = True

        
        #panel.Bind(wx.EVT_SIZE, OnSize)
        panel.dialog.buttonRow.applyButton.Bind(wx.EVT_BUTTON, OnApplyButton)
        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, OnOkButton)

        while panel.Affirmed():
            hostName = hostNameCtrl.GetValue()
            portNbr = portCtrl.GetValue()
            bSpeed_ms = speedCtrl.GetValue()
            socketTout = socketToutCtrl.GetValue()
            lostSensors = lostSensorsCtrl.GetValue()
            bSound = bSoundCtrl.GetValue()
            bRepeats = bRepeatsCtrl.GetValue()
            repeatDelay = repeatDelayCtrl.GetValue()
            bLogToFile = bLogToFileCtrl.GetValue()
            bDebug = bDebugCtrl.GetValue()
            prefix = eventPrefixCtrl.GetValue()
            if prefix == '':
                prefix = 'ONH'
            panel.SetResult(
                hostName,
                portNbr,
                bSpeed_ms,
                socketTout,
                lostSensors,
                bSound,
                bRepeats,
                repeatDelay,
                bLogToFile,
                bDebug,
                prefix,
                *args
            )
          


class prontoCmd(eg.ActionClass):
    text = Text.prontoCmd
    
    def __call__(
        self,
        deviceName,
        pronto,
        iNbrOfBursts,
        cmdDelay
    ):
        header = "event,Pronto_Message,Direction,Out,Pronto.Message,"
        connectionError = True
        self.plugin.semaPhore = False
        try:
            self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.skt.settimeout(5.0)
            self.skt.connect((self.plugin.hostName, self.plugin.portNbr))
            self.skt.sendall("\r\n")
            rsp = self.skt.recv(512)
            if rsp.find("ok") != -1:
                connectionError = False
        except socket.error, e:
            #print self.plugin.text.connection_error, e
            connectionError = True
            
        s = header+str(pronto)+"\r\n"
        time.sleep(0.05)
        for i in range(iNbrOfBursts):
            self.skt.sendall(s)
            time.sleep(cmdDelay)
        self.skt.sendall("quit\r\n")
        self.skt.close()
        self.plugin.semaPhore = True


    def Configure(
        self,
        deviceName = "Give the device a name",
        pronto = (
            "0000 0073 0000 0019 000e 002a 000e 002a 000e 002a 000e "+
            "002a 000e 002a 000e 002a 000e 002a 000e 002a 000e 002a "+
            "000e 002a 000e 002a 000e 002a 000e 002a 000e 002a 000e "+
            "002a 000e 002a 000e 002a 000e 002a 000e 002a 002a 000e "+
            "000e 002a 002a 000e 000e 002a 002a 000e 000e 0199"
        ),
        iNbrOfBursts = 4,
        cmdDelay = 0.5
        
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)
        mySizer_3 = wx.GridBagSizer(10, 10)

        #name
        deviceNameCtrl = wx.TextCtrl(panel, -1, deviceName)
        deviceNameCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.deviceName), (0,0))
        mySizer_1.Add(deviceNameCtrl, (1,0))

        #pronto
        prontoCtrl = wx.TextCtrl(panel, -1, pronto, style=wx.TE_MULTILINE)
        prontoCtrl.SetInitialSize((400,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.pronto), (1,0))
        mySizer_2.Add(prontoCtrl, (2,0))

        iNbrOfBurstsCtrl = panel.SpinIntCtrl(iNbrOfBursts, 1, 10)
        iNbrOfBurstsCtrl.SetInitialSize((45,-1))
        mySizer_3.Add(
            wx.StaticText(
                panel,
                -1,
                self.text.txtNbrBursts
            ),
           (0,0)
        )
        mySizer_3.Add(iNbrOfBurstsCtrl,(0,1))

        cmdDelayCtrl = panel.SpinNumCtrl(
            cmdDelay,
            decimalChar = '.',   # by default, use '.' for decimal point
            groupChar = ',',     # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 2,
            min = 0.1,
            max = 5.0,
            increment = 0.1
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

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_3, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            deviceName = deviceNameCtrl.GetValue()
            pronto = prontoCtrl.GetValue()
            iNbrOfBursts = iNbrOfBurstsCtrl.GetValue()
            cmdDelay = cmdDelayCtrl.GetValue()
            panel.SetResult(
                deviceName,
                pronto,
                iNbrOfBursts,
                cmdDelay
            )



class smokeDetCmd(eg.ActionClass):
    text = Text.smokeDetCmd
    
    def __call__(
        self,
        deviceName,
        address
    ):
    	header = "event,NexaFire_Message,Direction,Out,NexaFire.Address,"
        connectionError = True
        self.plugin.semaPhore = False
        try:
            self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.skt.settimeout(5.0)
            self.skt.connect((self.plugin.hostName, self.plugin.portNbr))
            self.skt.sendall("\r\n")
            rsp = self.skt.recv(512)
            if rsp.find("ok") != -1:
                connectionError = False
        except socket.error, e:
            #print self.plugin.text.connection_error, e
            connectionError = True
            
        s = header+str(address)+"\r\n"
        time.sleep(0.05)
        for i in range(0,2):
            self.skt.sendall(s)
            time.sleep(0.5)
        self.skt.sendall("quit\r\n")
        self.skt.close()
        self.plugin.semaPhore = True


    def Configure(
        self,
        deviceName = "Smoke detector description",
        address = "123456"
    ):
        plugin = self.plugin
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)

        #name
        deviceNameCtrl = wx.TextCtrl(panel, -1, deviceName)
        deviceNameCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, self.text.deviceName), (0,0))
        mySizer_1.Add(deviceNameCtrl, (1,0))

        #address
        adrCtrl = wx.TextCtrl(panel, -1, address)
        adrCtrl.SetInitialSize((250,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, self.text.address), (1,0))
        mySizer_2.Add(adrCtrl, (2,0))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)
        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            deviceName = deviceNameCtrl.GetValue()
            address = adrCtrl.GetValue()
            panel.SetResult(
                deviceName,
                address
            )



class GetWeeklyRainLevels(eg.ActionClass):

    def __call__(self):
        
        print str(self.plugin.rain_level_values_last_week)
        print str(self.plugin.rain_level_dates_last_week)
        return(
            str(self.plugin.rain_level_values_last_week) +
            str(self.plugin.rain_level_dates_last_week)
        )

        

class GetAverageWindLevels(eg.ActionClass):

    def __call__(self):

        print str(self.plugin.wind_level_average_15)
        print str(self.plugin.wind_level_average_60)
        return(
            str(self.plugin.wind_level_average_15) +
            str(self.plugin.wind_level_average_60)
        )
        


class SendCommand(eg.ActionClass):
    text = Text.SendCommand
    objects = {}

    def __call__(
        self,
        obj,
        name,
        attribute,
        rest_port
    ):
        connectionError = True
        self.plugin.semaPhore = False
        try:
            self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.skt.settimeout(5.0)
            self.skt.connect((self.plugin.hostName, self.plugin.portNbr))
            self.skt.sendall("\r\n")
            rsp = self.skt.recv(512)
            if rsp.find("ok") != -1:
                connectionError = False
        except socket.error, e:
            connectionError = True
        s = 'call,'+obj+','+attribute+'\r\n'
        self.skt.sendall(s)
        self.skt.sendall("quit\r\n")
        self.skt.close()
        self.plugin.semaPhore = True

    
    def OnObjChoice(self, event = None):
        attribCtrl = self.attribCtrl
        objCtrl = self.objCtrl
        choice = objCtrl.GetSelection()
        obj = objCtrl.GetStringSelection()
        if not obj:
            return choice
        a_list = self.objects[obj]
        attribCtrl.Clear()
        attribCtrl.AppendItems(items=a_list)
        if a_list.count(obj)==0:
            sel = 0
        else:
            sel = int(a_list.index(obj)) 
        attribCtrl.SetSelection(sel)
        if event:
            event.Skip()
        return choice 


    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def GetConnection(self, host, port, URL):
        try:
            conn = httplib.HTTPConnection(host+':'+str(port))
            conn.request('GET', "http://"+host+':'+str(port)+URL)
            resp = conn.getresponse()
            if resp.status == 200:
                return resp
            else:
                eg.PrintError(self.text.rest_connection_error)
                return None
        except:
            return None


    def GetActions(self, host, port, URL):
        resp = self.GetConnection(host, port, URL)
        content = resp.read().replace('true', 'True')
        content.replace('false', 'False')
        return eval(content)['actions']


    def Configure(
        self,
        obj = 'TF',
        name = 'Give the action a name',
        attribute = 'on',
        rest_port = 8020
    ):
        panel = eg.ConfigPanel(self)
        lamps = []
        resp = self.GetConnection(
            self.plugin.hostName, 
            rest_port, 
            '/rest/items'
        )
        if resp:
            content = eval(resp.read())
            for item in content:
                if item['category']=='Lamps':
                    actions = self.GetActions(
                        self.plugin.hostName,
                        rest_port,
                        '/rest/items/'+item['id']
                    )
                    self.objects[item['name']] = actions
            for item in self.objects:
                lamps.append(item)
            
        # Create a dropdown for object selection
        objCtrl = self.objCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        objCtrl.AppendItems(items=lamps)
        if lamps.count(obj)==0:
            objCtrl.Select(n=0)
        else:
            objCtrl.SetSelection(int(lamps.index(obj)))
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxObj)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(objCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        objCtrl.Bind(wx.EVT_CHOICE, self.OnObjChoice)

        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for function selection
        attribCtrl = self.attribCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        self.OnObjChoice()  # This is used when opening the dialog
        a_list = attribCtrl.GetStrings()
        if attribute in a_list:
            attribCtrl.SetStringSelection(attribute)
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxAttribute)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(attribCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        attribCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a field for selection of the REST interface port 
        portCtrl = panel.SpinIntCtrl(rest_port)
        staticBox = wx.StaticBox(panel, -1, self.text.textRestPort)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(portCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            self.plugin.rest_port = portCtrl.GetValue()
            panel.SetResult(
                objCtrl.GetStringSelection(),
                nameCtrl.GetValue(), 
                attribCtrl.GetStringSelection(),
                portCtrl.GetValue()
            )      



class SendRESTcommand(eg.ActionClass):
    text = Text.SendRESTcommand
    objects = {}

    def __call__(
        self,
        obj,
        name,
        attribute,
        rest_port
    ):
        device_id = self.plugin.obj_id[obj]
        resp = self.PostConnection(
            self.plugin.hostName, 
            rest_port, 
            '/rest/items/'+
            "".join(device_id)+
            '/actions/'+
            attribute+
            '/invoke'
        )

    
    def OnObjChoice(self, event = None):
        attribCtrl = self.attribCtrl
        objCtrl = self.objCtrl
        choice = objCtrl.GetSelection()
        obj = objCtrl.GetStringSelection()
        if not obj:
            return  choice
        a_list = self.objects[obj]
        attribCtrl.Clear()
        attribCtrl.AppendItems(items=a_list)
        if a_list.count(obj)==0:
            sel = 0
        else:
            sel = int(a_list.index(obj)) 
        attribCtrl.SetSelection(sel)
        if event:
            event.Skip()
        return choice 


    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def PostConnection(self, host, port, URL):
        try:
            conn = httplib.HTTPConnection(host+':'+str(port))
            conn.request('POST', "http://"+host+':'+str(port)+URL)
            resp = conn.getresponse()
            if resp.status == 200:
                return resp
            else:
                eg.PrintError(self.text.rest_connection_error)
                return None
        except:
            return None


    def GetConnection(self, host, port, URL):
        try:
            conn = httplib.HTTPConnection(host+':'+str(port))
            conn.request('GET', "http://"+host+':'+str(port)+URL)
            resp = conn.getresponse()
            if resp.status == 200:
                return resp
            else:
                eg.PrintError(self.text.rest_connection_error)
                return None
        except:
            return None


    def GetActions(self, host, port, URL):
        resp = self.GetConnection(host, port, URL)
        content = resp.read().replace('true', 'True')
        content.replace('false', 'False')
        return eval(content)['actions']


    def Configure(
        self,
        obj = 'TF',
        name = 'Give the action a name',
        attribute = 'on',
        rest_port = 8020
    ):
        panel = eg.ConfigPanel(self)
        lamps = []
        resp = self.GetConnection(
            self.plugin.hostName, 
            rest_port, 
            '/rest/items'
        )
        if resp:
            content = eval(resp.read())
            for item in content:
                if item['category']=='Lamps':
                    actions = self.GetActions(
                        self.plugin.hostName,
                        rest_port,
                        '/rest/items/'+item['id']
                    )
                    self.objects[item['name']] = actions
            for item in self.objects:
                lamps.append(item)
            
        # Create a dropdown for object selection
        objCtrl = self.objCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        objCtrl.AppendItems(items=lamps)
        if lamps.count(obj)==0:
            objCtrl.Select(n=0)
        else:
            objCtrl.SetSelection(int(lamps.index(obj)))
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxObj)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(objCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        objCtrl.Bind(wx.EVT_CHOICE, self.OnObjChoice)

        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for function selection
        attribCtrl = self.attribCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        self.OnObjChoice()  # This is used when opening the dialog
        a_list = attribCtrl.GetStrings()
        if attribute in a_list:
            attribCtrl.SetStringSelection(attribute)
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxAttribute)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(attribCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        attribCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a field for selection of the REST interface port 
        portCtrl = panel.SpinIntCtrl(rest_port)
        staticBox = wx.StaticBox(panel, -1, self.text.textRestPort)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(portCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            self.plugin.rest_port = portCtrl.GetValue()
            panel.SetResult(
                objCtrl.GetStringSelection(),
                nameCtrl.GetValue(), 
                attribCtrl.GetStringSelection(),
                portCtrl.GetValue()
            )      



class RollerTrolCommand(eg.ActionClass):
    text = Text.RollerTrolCommand
    objects = {}

    def __call__(
        self,
        obj,
        name,
        attribute,
        rest_port
    ):
        connectionError = True
        self.plugin.semaPhore = False
        try:
            self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.skt.settimeout(5.0)
            self.skt.connect((self.plugin.hostName, self.plugin.portNbr))
            self.skt.sendall("\r\n")
            rsp = self.skt.recv(512)
            if rsp.find("ok") != -1:
                connectionError = False
        except socket.error, e:
            connectionError = True
        s = 'call,'+obj+','+attribute+'\r\n'
        self.skt.sendall(s)
        self.skt.sendall("quit\r\n")
        self.skt.close()
        self.plugin.semaPhore = True

    
    def OnObjChoice(self, event = None):
        attribCtrl = self.attribCtrl
        objCtrl = self.objCtrl
        choice = objCtrl.GetSelection()
        obj = objCtrl.GetStringSelection()
        if not obj:
            return choice
        a_list = self.objects[obj]
        attribCtrl.Clear()
        attribCtrl.AppendItems(items=a_list)
        if a_list.count(obj)==0:
            sel = 0
        else:
            sel = int(a_list.index(obj)) 
        attribCtrl.SetSelection(sel)
        if event:
            event.Skip()
        return choice 


    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def GetConnection(self, host, port, URL):
        try:
            conn = httplib.HTTPConnection(host+':'+str(port))
            conn.request('GET', "http://"+host+':'+str(port)+URL)
            resp = conn.getresponse()
            if resp.status == 200:
                return resp
            else:
                eg.PrintError(self.text.rest_connection_error)
                return None
        except:
            return None


    def GetActions(self, host, port, URL):
        resp = self.GetConnection(host, port, URL)
        content = resp.read().replace('true', 'True')
        content.replace('false', 'False')
        return eval(content)['actions']


    def Configure(
        self,
        obj = '',
        name = 'Give the action a name',
        attribute = 'open',
        rest_port = 8020
    ):
        panel = eg.ConfigPanel(self)
        devices = []
        resp = self.GetConnection(
            self.plugin.hostName, 
            rest_port, 
            '/rest/items'
        )
        if resp:
            content = eval(resp.read())
            for item in content:
                if item['category']=='Actuators':
                    actions = self.GetActions(
                        self.plugin.hostName,
                        rest_port,
                        '/rest/items/'+item['id']
                    )
                    self.objects[item['name']] = actions
            for item in self.objects:
                devices.append(item)
        else:
            pass
        # Create a dropdown for object selection
        objCtrl = self.objCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        objCtrl.AppendItems(items=devices)
        if devices.count(obj)==0:
            objCtrl.Select(n=0)
        else:
            objCtrl.SetSelection(int(devices.index(obj)))
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxObj)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(objCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        objCtrl.Bind(wx.EVT_CHOICE, self.OnObjChoice)

        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for function selection
        attribCtrl = self.attribCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        self.OnObjChoice()  # This is used when opening the dialog
        a_list = attribCtrl.GetStrings()
        if attribute in a_list:
            attribCtrl.SetStringSelection(attribute)
        staticBox = wx.StaticBox(panel, -1, self.text.textBoxAttribute)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(attribCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        attribCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a field for selection of the REST interface port 
        portCtrl = panel.SpinIntCtrl(rest_port)
        staticBox = wx.StaticBox(panel, -1, self.text.textRestPort)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(portCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            self.plugin.rest_port = portCtrl.GetValue()
            panel.SetResult(
                objCtrl.GetStringSelection(),
                nameCtrl.GetValue(), 
                attribCtrl.GetStringSelection(),
                portCtrl.GetValue()
            )      



class ClearSensorsStatus(eg.ActionClass):
        
    def __call__(self):
        #Clear the repository for missing sensors
        time.sleep(0.5)
        CurrentStateData.sensors_status.clear()
        self.plugin.sensors_status = (
            CurrentStateData.sensors_status
        )




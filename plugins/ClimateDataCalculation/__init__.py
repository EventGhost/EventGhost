# -*- coding: utf-8 -*-
#
# Copyright (c) 2014, Walter Kraembring
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of Walter Kraembring nor the names of its contributors may
#    be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##############################################################################
# Revision history:
#
# 2016-02-19  Added support for Barometric pressure data capturing & reporting 
# 2016-02-17  Added support for a new type of report (WindMiniRoseReport) 
# 2017-02-16  Further improvements of report layouts
# 2017-02-11  Modified layout of Wind Rose report
# 2016-10-15  Modified capturing of light level data from 1-wire sensors 
# 2016-02-14  Added support for a new type of report (ComparisonReport) for 
#             comparison of data with it's 24 hours older history
# 2016-02-12  Added support for special sensor events (oregon protocol)
# 2016-02-10  Bug fix in humidity capturing routine
#             Minimize database accessing when saving sensor data
#             Printing queue size only when size is above 90% of defined
#             limit 
#             Added function to debug thread queue size
# 2016-01-01  Improved queue handling for threads and currently allowing 10
#             simultanously running
# 2015-12-30  Added queue for threads and currently allowing 5 simultanously
#             running
# 2015-12-16  Hopefully improved handling of locks for threads and db write
#             operations
# 2015-09-19  Modified support for z-wave devices (temperature)
# 2015-08-01  Added support for z-wave devices (temperature & luminance)
# 2015-05-31  Added support for 10 minutes data point graphs
# 2015-05-05  Added action to refresh table names for report templates
# 2015-05-04  Added action to create Wind Rose reports
# 2015-04-30  Added support for wind data capturing
#             Further code optimizations & clean up
# 2015-04-29  Solved data capturing via independent threads. Creating event
#             when report creation has finished
# 2015-04-28  Using threading locks to control & synchronize access to data bases
# 2015-04-28  Using 'threading' instead of 'thread' in report creation
# 2015-04-27  Bug fix in chart for 'selected period' presentation finally fixed 
# 2015-04-27  Further optimizations in accessing data bases
# 2015-04-26  Optimized data base saving routines
# 2015-04-25  Skipped data capturing via threads
# 2015-04-23  Introduced retries when committing data to data bases.
# 2015-04-23  Perfomance improvement, all data capturing is handled by threads
#             to avoid EG lockup
# 2015-04-23  Creation of ComboReport is now done via a thread to avoid EG
#             lockup for large data bases and reports
# 2015-04-16  Re-design of configuration dialog for ComboReports
# 2015-04-13  Improved performance when editing report settings
# 2015-04-11  Added support for Fineoffset (temperature) and Oregon (humidity
#             and temperature) from ONH
# 2015-02-04  Added support for dewpoint data via normal events 
# 2015-02-02  Added support for light sensor via 1-wire 
# 2014-12-18  Added report combining multiple temperatures, humidities and rain
#             data selections. Separate reports for temperature & humidity have
#             been superseded by the combo report
# 2014-12-10  Improved reports of temperature and humidity data (requires reset
#             of existing databases)
# 2014-12-08  Added support for Webserver with included websocket support 
# 2014-12-06  Rain data capture algorithm revised
# 2014-12-03  Added setting in actions for html report filename
# 2014-12-01  Generating html page for rain, temp, hum reports. With user
#             selectable range settings in 0-365 days and 0-24 hours
# 2014-10-16  Revised functions for temperature & humidity rule evaluations
# 2014-10-14  Supporting temperature, humidity and rule evaluation
# 2014-10-09  The first stumbling version supporting rain data
##############################################################################
##############################################################################
#
# Acknowledgements:
#
# Websocket Suite and Tornado plugins are Copyright (C)  2011-2014
# Pako (lubos.ruckl@quick.cz)
##############################################################################

eg.RegisterPlugin(
    name = "ClimateDataCalculation",
    guid = '{4CB0A57C-15ED-4F5B-8AFF-75F288785655}',
    author = "Walter Kraembring",
    version = "0.5.0",
    canMultiLoad = False,
    kind = "other",
    url = "http://eventghost.net/forum/viewtopic.php?f=9&t=6363",
    description = (
        '<p>Plugin to collect climate data from</p>'
        '<p> wireless sensors via a RFXtrx receiver and others</p>'
        '<center><img src="image.png" /></center>'
    ),
)

import eg
import sqlite3
import re
import time
import datetime
import sys
import os
import CreateTempHtml
import CreateBarHtml
import CreateComboHtml
import CreateComparisonHtml
import CreateWindRoseHtml
import CreateWindMiniRoseHtml
from threading import Event, Thread, Lock
from Queue import Queue



class Text:
    port = "Port:"
    use_websockets = "Use Websocket Suite plugin for websockets " 
    use_tornadoWebsockets = "Use Tornado plugin for websockets "
    use_WebserverWebsockets = "Use Webserver plugin with included websockets support  "
    cHtml = "Generate html page to specified path and name"
    tenMinutes = "Use 10 minutes data point spread"
    titleHtml = "Set the page title"
    headingHtml = "Set the report title"
    dbTableId = 'Give the table a name:'
    dbReportTableId = 'Select the tables to cover from history:'
    dbTableIdReset = 'Select the table to reset:'
    dbDevice = 'Set the correct device ID:'
    dbSensor = 'Set the correct sensor ID:'
    noData = 'No data found for selected date and time period'
    dateTimeFrom = 'Select the date & timestamp to start from:'
    dateTimeTo = 'Select the date & timestamp to end with:'
    nbrOfLastHours = 'Number of additional hours:'
    nbrOfLastDays = 'Number of days:'
    sInterval = 'Select the logging interval (minutes):'
    setPoint = 'Set the desired or target value (setpoint):'
    movAverage = 'Number of readings for the average calculation:'
    fMovAverage = 'Number of readings for the fast average calculation:'
    sMovAverage = 'Number of readings for the slow average calculation:'
    useHysteresis = 'Check to use hysteresis:'
    hysteresis = 'Select the hysteresis value:'
    useRule = 'Check to use a rule:'
    rule = 'Select the rule from the list:'
    startRefresh = 'Refreshing table names, please wait...'
    endRefresh = 'Refresh finished'    
    

class ClimateDataCalculation(eg.PluginClass):
    text = Text
    
    def __init__(self):
        self.AddAction(CombinedReport)
        self.AddAction(ComparisonReport)
        self.AddAction(WindRoseReport)
        self.AddAction(WindMiniRoseReport)
        self.AddAction(TemperatureReport)
        self.AddAction(BarometricReport)
        self.AddAction(RefreshTableNames)
        self.AddAction(WindDataCapture)
        self.AddAction(ResetWindData)
        self.AddAction(RainRequestSearch)
        self.AddAction(RainRequestQuery)
        self.AddAction(RainDataCapture)
        self.AddAction(ResetRainData)
        self.AddAction(TempDataCapture)
        self.AddAction(ResetTempData)
        self.AddAction(HumDataCapture)
        self.AddAction(ResetHumData)
        self.AddAction(BarDataCapture)
        self.AddAction(ResetBarData)
        self.AddAction(LightDataCapture)
        self.AddAction(ResetLightData)
        self.AddAction(DewPointDataCapture)
        self.AddAction(ResetDewPointData)
        self.windData_db = 'windData.db'
        self.rainData_db = 'rainData.db'
        self.tempData_db = 'tempData.db'
        self.humData_db = 'humData.db'
        self.barData_db = 'barData.db'
        self.lightData_db = 'lightData.db'
        self.dewPointData_db ='dewPointData.db'
        self.tablesWindData = []
        self.tablesRainData = []
        self.tablesTempData = []
        self.tablesHumData = []
        self.tablesBarData = []
        self.tablesLightData = []
        self.tablesDewPointData = []
        self.lastTempData = {}
        self.lastHumData = {}
        self.lastBarData = {}
        self.lastRainData = {}
        self.lastWindData = {}
        

    def __start__(self):
        # setting up locks for db access
        self.qsLimit = 15
        self.q = Queue(maxsize=self.qsLimit)
        self.qDebug = True
        self.oldQsize = 0
        self.temp_lock = Lock()
        self.hum_lock = Lock()
        self.bar_lock = Lock()
        self.rain_lock = Lock()
        self.wind_lock = Lock()
        self.light_lock = Lock()
        self.dewp_lock = Lock()
        # start the main thread (not doing much for the moment)
        self.mainThreadEvent = Event()
        mainThread = Thread(target=self.main, args=(self.mainThreadEvent,))
        mainThread.start()


    def __stop__(self):
        self.mainThreadEvent.set()


    def __close__(self):
        print "Plugin is closed."


    def main(self,mainThreadEvent): 
        self.RefreshTableNames()
        while not mainThreadEvent.isSet(): # Main Loop
            if self.qDebug:
                mainThreadEvent.wait(1.0)
                qs = self.q.qsize()
                qsRef = int(0.9*self.qsLimit)
                if qs > qsRef and qs <> self.oldQsize:
                    print 'Current Q size: ', qs
                    self.oldQsize = qs
            else:
                mainThreadEvent.wait(100.0)
        print "Main loop ended."


    def TornadoBroadcastMessage(self, msg):
        eg.plugins.Tornado.BroadcastMessage(
            msg.encode('utf-8'),
            True
        )

       
    def WebsocketSuiteBroadcastMessage(self, port, msg):
        eg.plugins.WebsocketSuite.BroadcastMessage(
            'All available interfaces',
            port,
            msg.encode('utf-8'),
            2
        )


    def WebserverBroadcastMessage(self, msg):
        eg.plugins.Webserver.BroadcastMessage(
            msg.encode('utf-8'),
            False
        )


    def RefreshTableNames(self):
        print self.text.startRefresh
        with self.rain_lock:
            self.GetAllTableNames(self.rainData_db)
        with self.wind_lock:
            self.GetAllTableNames(self.windData_db)
        with self.temp_lock:
            self.GetAllTableNames(self.tempData_db)
        with self.hum_lock:
            self.GetAllTableNames(self.humData_db)
        with self.bar_lock:
            self.GetAllTableNames(self.barData_db)
        with self.light_lock:
            self.GetAllTableNames(self.lightData_db)
        with self.dewp_lock:
            self.GetAllTableNames(self.dewPointData_db)
        print self.text.endRefresh


    def GetAllTableNames(self, db):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        q = 'SELECT tableId FROM '+db.split('.')[0]
        try:
            c.execute(q)
            coll = c.fetchall()
            list = []
            for item in coll:
                name = item[0]
                if name not in list:
                    list.append(name)
            conn.close()
            if db == self.rainData_db:
                self.tablesRainData = list
            if db == self.windData_db:
                self.tablesWindData = list
            if db == self.tempData_db:
                self.tablesTempData = list
            if db == self.humData_db:
                self.tablesHumData = list
            if db == self.barData_db:
                self.tablesBarData = list
            if db == self.lightData_db:
                self.tablesLightData = list
            if db == self.dewPointData_db:
                self.tablesDewPointData = list
            del list
            del coll
            del c
        except:
            conn.close()
            del c


    def CalculateMovAverage(self, dataSet, prm, endValue, r):
        res = 0
        cnt = 0
        for i in range(0, r):
            try:
                res += dataSet[i][prm]
                cnt +=1
            except:
                pass
        res += endValue
        res = float(res/(cnt+1))
        return res


    def RuleEvaluator(
        self, 
        rule, 
        sMov, 
        setPoint, 
        lastCommand, 
        tableId, 
        hysteresis
    ):
        if rule == 'equal-less-greater':
            res = lastCommand
            if setPoint+hysteresis/2 < sMov:
                res = 'setPoint < MovAverage'
            if setPoint-hysteresis/2 > sMov:
                res = 'setPoint > MovAverage'
            if setPoint == sMov:
                res = 'setPoint == MovAverage'
            if res <> lastCommand:
                es = res
                pl = [res, setPoint, sMov]
                self.CreateEvent(es, pl, tableId)
            return res
            

    def CreateEvent(self, es, pl, tableId):             
        eg.TriggerEvent(
            tableId+'.'+es,
            payload = pl,
            prefix = 'ClimateDataCalculation'
        )


    def DelData(self, dbName, tableId):
        dbName = str(dbName)
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        t = ((tableId),)
        with conn:
            c.execute('DELETE FROM '+dbName.split('.')[0]+' WHERE tableId=?', t)
        conn.close()


    def SearchData(
        self, 
        dbName, 
        dbTableId, 
        dateTimeFrom, 
        dateTimeTo 
    ):
        dbName = str(dbName)
        try:
            dbTableId = dbTableId.decode('utf-8')
        except:
            pass
        coll = self.GetAllData(dbName, dbTableId)
        s = coll[0]
        e = coll[-1]
        if len(coll) > 1:
            for item in coll:
                s_found = False
                if item[0].find(dateTimeFrom) != -1:
                    s = item
                    s_found = True
                if s_found:
                    break 
            for item in coll:
                e_found = False
                if item[0].find(dateTimeTo) != -1:
                    e = item
                    e_found = True
                if e_found:
                    break
            del coll 
            return s, e

                
    def LastData(
        self, 
        dbName, 
        dbTableId, 
        dateTimeFrom
    ):
        dbName = str(dbName)
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        v = ((dbTableId),(dateTimeFrom),)
        try:
            c.execute('SELECT * FROM '+dbName.split('.')[0]+' WHERE tableId=? AND date>=?', v)
            #print 'fetching started'
            rows = c.fetchall()
            conn.close()
            #print 'fetching ended'
            return rows
        except:
            conn.close()
            return None


    def GetAllData(
        self, 
        dbName, 
        dbTableId
    ):
        dbName = str(dbName)
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        t = ((dbTableId),)
        try:
            c.execute('SELECT * FROM '+dbName.split('.')[0]+' WHERE tableId=?', t)
            coll = c.fetchall()
            conn.close()
            res = coll
            del coll
            return res
        except:
            conn.close()
            return None
        

    def AddToQueue(self, id):
        self.q.put(id, True, None)

        
## Light level related ##############################################################
    def SaveLightData(
        self,
        tableId,
        lightlevel,
        sInterval,
        movAverage
    ):
        def SaveLight(saveLightThreadEvent):
            conn = None
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            s_epoch = int(round(time.time(),0))
            qs = 'CREATE TABLE IF NOT EXISTS '+self.lightData_db.split('.')[0]
            prm = ' (date text, s_epoch integer, tableId text, lightlevel real, sMov real)'
            t = ((tableId), movAverage)
            st =  "SELECT * FROM "+self.lightData_db.split('.')[0]+" WHERE tableId=? ORDER BY date DESC LIMIT ?"        
            with self.light_lock:
                try:
                    conn = sqlite3.connect(self.lightData_db)
                    c = conn.cursor()
                    c.execute("PRAGMA synchronous = OFF")
                    c.execute(qs+prm) 
                    c.execute(st, t)
                    coll = c.fetchmany(movAverage)
                    dt = 0
                    try:
                        dt = coll[0][1]
                    except:
                        pass
                    if s_epoch > dt + sInterval*60-30:
                        sMov = self.CalculateMovAverage(
                            coll, 
                            3, 
                            lightlevel, 
                            movAverage
                        )
                        sMov = float("%.2f" % sMov)
                        lst = (date, s_epoch, tableId, lightlevel, sMov)
                        ss = "INSERT INTO "+self.lightData_db.split('.')[0]+" VALUES (?,?,?,?,?)"
                        with conn:
                            c.execute(ss,lst)
                        del coll
                        del sMov
                        
                except sqlite3.Error, e:
                    eg.PrintError("Error %s:" % e.args[0])
                    time.sleep(2.0)     
                    
                finally:
                    if conn:
                        conn.close()
                    while not saveLightThreadEvent.isSet():
                        saveLightThreadEvent.wait(1.0)
                    del saveLightThreadEvent
                    item = self.q.get_nowait()
                    del item
                    self.q.task_done()

        saveLightThreadEvent = Event()
        saveLightThread = Thread(
            target=SaveLight,
            args=(saveLightThreadEvent,)
        )
        self.AddToQueue(tableId)
        saveLightThread.start()
        saveLightThreadEvent.set()
 
            
## Dewpoint related ##############################################################
    def SaveDewPointData(
        self,
        tableId,
        dewpoint
    ):
        def SaveDewp(saveDewpThreadEvent):
            conn = None
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            s_epoch = int(round(time.time(),0))
            qs = 'CREATE TABLE IF NOT EXISTS '+self.dewPointData_db.split('.')[0]
            prm = ' (date text, s_epoch integer, tableId text, dewpoint real)'
            t = ((tableId), 2)
            st =  "SELECT * FROM "+self.dewPointData_db.split('.')[0]+" WHERE tableId=? ORDER BY date DESC LIMIT ?"        
            with self.dewp_lock:
                try:
                    conn = sqlite3.connect(self.dewPointData_db)
                    c = conn.cursor()
                    c.execute("PRAGMA synchronous = OFF")
                    c.execute(qs+prm) 
                    c.execute(st, t)
                    coll = c.fetchmany(2)
                    dt = 0
                    try:
                        dt = coll[0][1]
                    except:
                        pass
                    if s_epoch > dt:
                        lst = (date, s_epoch, tableId, dewpoint)
                        ss = "INSERT INTO "+self.dewPointData_db.split('.')[0]+" VALUES (?,?,?,?)"
                        with conn:
                            c.execute(ss,lst)
                        del coll
        
                except sqlite3.Error, e:
                    eg.PrintError("Error %s:" % e.args[0])
                    time.sleep(2.0)     
                    
                finally:
                    if conn:
                        conn.close()
                    while not saveDewpThreadEvent.isSet():
                        saveDewpThreadEvent.wait(1.0)
                    del saveDewpThreadEvent
                    item = self.q.get_nowait()
                    del item
                    self.q.task_done()

        saveDewpThreadEvent = Event()
        saveDewpThread = Thread(
            target=SaveDewp,
            args=(saveDewpThreadEvent,)
        )
        self.AddToQueue(tableId)
        saveDewpThread.start()
        saveDewpThreadEvent.set()
                    

## Temperature related ##############################################################
    def SaveTempData(
        self,
        tableId,
        temperature,
        sInterval,
        setPoint,
        movAverage,
        useHysteresis,
        hysteresis,
        useRule,
        rule
    ):
        def SaveTemp(saveTempThreadEvent, hysteresis):
            conn = None
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            s_epoch = int(round(time.time(),0))
            qs = 'CREATE TABLE IF NOT EXISTS '+self.tempData_db.split('.')[0]
            prm = ' (date text, s_epoch integer, tableId text, temperature real, lastcmd text, upperLimit real, lowerLimit real, sMov real)'
            t = ((tableId), movAverage)
            st =  "SELECT * FROM "+self.tempData_db.split('.')[0]+" WHERE tableId=? ORDER BY date DESC LIMIT ?"        
            with self.temp_lock:
                try:
                    conn = sqlite3.connect(self.tempData_db)
                    c = conn.cursor()
                    c.execute("PRAGMA synchronous = OFF")
                    c.execute(qs+prm) 
                    c.execute(st, t)
                    coll = c.fetchmany(movAverage)
                    res = ''
                    dt = 0
                    lastCmd = ''
                    try:
                        dt = coll[0][1]
                    except:
                        pass
                    try:
                        lastCmd = coll[0][4]
                    except:
                        pass
                    if s_epoch > dt + sInterval*60-30:
                        sMov = self.CalculateMovAverage(
                            coll, 
                            3, 
                            temperature, 
                            movAverage
                        )
                        sMov = float("%.2f" % sMov)
                        if not useHysteresis:
                            hysteresis = 0.0
                        if useRule:
                            res = self.RuleEvaluator(
                                rule, 
                                sMov, 
                                setPoint, 
                                lastCmd, 
                                tableId, 
                                hysteresis
                            )
                        uLimit = setPoint + hysteresis/2
                        lLimit = setPoint - hysteresis/2
                        lst = (date, s_epoch, tableId, temperature, res, uLimit, lLimit, sMov)
                        ss = "INSERT INTO "+self.tempData_db.split('.')[0]+" VALUES (?,?,?,?,?,?,?,?)"
                        with conn:
                            #print 'db locked'
                            c.execute(ss,lst)
                        #print 'db released'
                        del coll
                        del res
                        del sMov
        
                except sqlite3.Error, e:
                    eg.PrintError("Error %s:" % e.args[0])
                    time.sleep(2.0)     
                    
                finally:
                    if conn:
                        conn.close()
                    while not saveTempThreadEvent.isSet():
                        saveTempThreadEvent.wait(1.0)
                    del saveTempThreadEvent
                    item = self.q.get_nowait()
                    del item
                    self.q.task_done()

        saveTempThreadEvent = Event()
        saveTempThread = Thread(
            target=SaveTemp,
            args=(saveTempThreadEvent,hysteresis)
        )
        self.AddToQueue(tableId)
        saveTempThread.start()
        saveTempThreadEvent.set()
               
            
## Humidity related ##############################################################
    def SaveHumData(
        self,
        tableId,
        humidity,
        sInterval,
        setPoint,
        movAverage,
        useHysteresis,
        hysteresis,
        useRule,
        rule
    ):
        def SaveHum(saveHumThreadEvent, hysteresis):
            conn = None
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            s_epoch = int(round(time.time(),0))
            qs = 'CREATE TABLE IF NOT EXISTS '+self.humData_db.split('.')[0]
            prm = ' (date text, s_epoch integer, tableId text, humidity integer, lastcmd text, upperLimit integer, lowerLimit integer, sMov integer)'
            t = ((tableId), movAverage)
            st =  "SELECT * FROM "+self.humData_db.split('.')[0]+" WHERE tableId=? ORDER BY date DESC LIMIT ?"        
            with self.hum_lock:
                try:
                    conn = sqlite3.connect(self.humData_db)
                    c = conn.cursor()
                    c.execute("PRAGMA synchronous = OFF")
                    c.execute(qs+prm) 
                    c.execute(st, t)
                    coll = c.fetchmany(movAverage)
                    res = ''
                    dt = 0
                    lastCmd = ''
                    try:
                        dt = coll[0][1]
                    except:
                        pass
                    try:
                        lastCmd = coll[0][4]
                    except:
                        pass
                    if s_epoch > dt + sInterval*60-30:
                        sMov = self.CalculateMovAverage(
                            coll, 
                            3, 
                            humidity, 
                            movAverage
                        )
                        sMov = int(sMov)
                        if not useHysteresis:
                            hysteresis = 0
                        if useRule:
                            res = self.RuleEvaluator(
                                rule, 
                                sMov, 
                                setPoint, 
                                lastCmd, 
                                tableId, 
                                hysteresis
                            )
                        uLimit = setPoint + int(hysteresis/2)
                        lLimit = setPoint - int(hysteresis/2)
                        lst = (date, s_epoch, tableId, humidity, res, uLimit, lLimit, sMov)
                        ss = "INSERT INTO "+self.humData_db.split('.')[0]+" VALUES (?,?,?,?,?,?,?,?)"
                        with conn:
                            c.execute(ss,lst)
                        del coll
                        del res
                        del sMov
    
                except sqlite3.Error, e:
                    eg.PrintError("Error %s:" % e.args[0])
                    time.sleep(2.0)     
                    
                finally:
                    if conn:
                        conn.close()
                    while not saveHumThreadEvent.isSet():
                        saveHumThreadEvent.wait(1.0)
                    del saveHumThreadEvent
                    item = self.q.get_nowait()
                    del item
                    self.q.task_done()

        saveHumThreadEvent = Event()
        saveHumThread = Thread(
            target=SaveHum,
            args=(saveHumThreadEvent,hysteresis)
        )
        self.AddToQueue(tableId)
        saveHumThread.start()
        saveHumThreadEvent.set()
        
               
## Barometric related ##############################################################
    def SaveBarData(
        self,
        tableId,
        pressure,
        sInterval,
        setPoint,
        movAverage,
        useHysteresis,
        hysteresis,
        useRule,
        rule
    ):
        def SaveBar(saveBarThreadEvent, hysteresis):
            conn = None
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            s_epoch = int(round(time.time(),0))
            qs = 'CREATE TABLE IF NOT EXISTS '+self.barData_db.split('.')[0]
            prm = ' (date text, s_epoch integer, tableId text, pressure real, lastcmd text, upperLimit real, lowerLimit real, sMov real)'
            t = ((tableId), movAverage)
            st =  "SELECT * FROM "+self.barData_db.split('.')[0]+" WHERE tableId=? ORDER BY date DESC LIMIT ?"        
            with self.bar_lock:
                try:
                    conn = sqlite3.connect(self.barData_db)
                    c = conn.cursor()
                    c.execute("PRAGMA synchronous = OFF")
                    c.execute(qs+prm) 
                    c.execute(st, t)
                    coll = c.fetchmany(movAverage)
                    res = ''
                    dt = 0
                    lastCmd = ''
                    try:
                        dt = coll[0][1]
                    except:
                        pass
                    try:
                        lastCmd = coll[0][4]
                    except:
                        pass
                    if s_epoch > dt + sInterval*60-30:
                        sMov = self.CalculateMovAverage(
                            coll, 
                            3, 
                            pressure, 
                            movAverage
                        )
                        sMov = int(sMov)
                        if not useHysteresis:
                            hysteresis = 0
                        if useRule:
                            res = self.RuleEvaluator(
                                rule, 
                                sMov, 
                                setPoint, 
                                lastCmd, 
                                tableId, 
                                hysteresis
                            )
                        uLimit = setPoint + int(hysteresis/2)
                        lLimit = setPoint - int(hysteresis/2)
                        lst = (date, s_epoch, tableId, pressure, res, uLimit, lLimit, sMov)
                        ss = "INSERT INTO "+self.barData_db.split('.')[0]+" VALUES (?,?,?,?,?,?,?,?)"
                        with conn:
                            c.execute(ss,lst)
                        del coll
                        del res
                        del sMov
    
                except sqlite3.Error, e:
                    eg.PrintError("Error %s:" % e.args[0])
                    time.sleep(2.0)     
                    
                finally:
                    if conn:
                        conn.close()
                    while not saveBarThreadEvent.isSet():
                        saveBarThreadEvent.wait(1.0)
                    del saveBarThreadEvent
                    item = self.q.get_nowait()
                    del item
                    self.q.task_done()

        saveBarThreadEvent = Event()
        saveBarThread = Thread(
            target=SaveBar,
            args=(saveBarThreadEvent,hysteresis)
        )
        self.AddToQueue(tableId)
        saveBarThread.start()
        saveBarThreadEvent.set()
               

## Wind related ##############################################################
    def SaveWindData(
        self,
        tableId,
        windDirection,
        windAverage,
        windGust,
        sInterval
    ):
        def SaveWind(saveWindThreadEvent):
            conn = None
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            s_epoch = int(round(time.time(),0))
            qs = 'CREATE TABLE IF NOT EXISTS '+self.windData_db.split('.')[0]
            prm = ' (date text, s_epoch integer, tableId text, wind_direction text, wind_average real, wind_gust real)'
            t = ((tableId), 5)
            st =  "SELECT * FROM "+self.windData_db.split('.')[0]+" WHERE tableId=? ORDER BY date DESC LIMIT ?"        
            with self.wind_lock:
                try:
                    conn = sqlite3.connect(self.windData_db)
                    c = conn.cursor()
                    c.execute("PRAGMA synchronous = OFF")
                    c.execute(qs+prm)
                    c.execute(st, t)
                    coll = c.fetchmany(5)
                    dt = 0
                    try:
                        dt = coll[0][1]
                    except:
                        pass
                    if (s_epoch > dt + sInterval*60-30):
                        lst = (date, s_epoch, tableId, windDirection, windAverage, windGust)
                        ss = "INSERT INTO "+self.windData_db.split('.')[0]+" VALUES (?,?,?,?,?,?)"
                        with conn:
                            c.execute(ss,lst)
                        del coll
        
                except sqlite3.Error, e:
                    eg.PrintError("Error %s:" % e.args[0])
                    time.sleep(2.0)     
                    
                finally:
                    if conn:
                        conn.close()
                    while not saveWindThreadEvent.isSet():
                        saveWindThreadEvent.wait(1.0)
                    del saveWindThreadEvent
                    item = self.q.get_nowait()
                    del item
                    self.q.task_done()

        saveWindThreadEvent = Event()
        saveWindThread = Thread(
            target=SaveWind,
            args=(saveWindThreadEvent,)
        )
        self.AddToQueue(tableId)
        saveWindThread.start()
        saveWindThreadEvent.set()


## Rain related ##############################################################
    def CalculateRainMovAverage(
        self, 
        dataSet, 
        prm, 
        endValue, 
        r
    ):
        res = 0
        cnt = 0
        for i in range(0, r):
            try:
                res += (dataSet[i][prm]-dataSet[i+1][prm])
                cnt +=1
                if cnt == 1:
                    endValue = endValue - dataSet[i][prm]
            except:
                pass
        res += endValue
        res = float(res/(cnt+1))
        return res


    def RuleEvaluatorRain(
        self, 
        rule, 
        fMov,
        sMov, 
        lastCommand, 
        tableId, 
        hysteresis
    ):
        if rule == 'equal-less-greater':
            res = lastCommand
            if fMov+hysteresis/2 < sMov:
                res = 'fMovAverage < sMovAverage'
            if fMov-hysteresis/2 > sMov:
                res = 'fMovAverage > sMovAverage'
            if fMov == sMov:
                res = 'fMovAverage == sMovAverage'
            if res <> lastCommand:
                es = res
                pl = [res, fMov, sMov]
                self.CreateEvent(es, pl, tableId)
            return res


    def SaveRainData(
        self,
        tableId,
        rainRate,
        rainTotal,
        delta,
        sInterval,
        fMovAverage,
        sMovAverage,
        useHysteresis,
        hysteresis,
        useRule,
        rule
    ):
        def SaveRain(saveRainThreadEvent, hysteresis, rainTotal):
            conn = None
            now = datetime.datetime.now()
            date = now.strftime("%Y-%m-%d %H:%M:%S")
            s_epoch = int(round(time.time(),0))
            qs = 'CREATE TABLE IF NOT EXISTS '+self.rainData_db.split('.')[0]
            prm = ' (date text, s_epoch integer, tableId text, rate_value integer, total_value integer, delta integer, lastcmd text)'
            m = max(fMovAverage, sMovAverage)
            t = ((tableId), m)
            st =  "SELECT * FROM "+self.rainData_db.split('.')[0]+" WHERE tableId=? ORDER BY date DESC LIMIT ?"        
            with self.rain_lock:
                try:
                    conn = sqlite3.connect(self.rainData_db)
                    c = conn.cursor()
                    c.execute("PRAGMA synchronous = OFF")
                    c.execute(qs+prm)
                    c.execute(st, t)
                    coll = c.fetchmany(m)
                    res = ''
                    dt = 0
                    lastCmd = ''
                    rw = 0
                    delta = 0
                    prev_delta = 0
                    fMov = 0
                    sMov = 0
                    try:
                        dt = coll[0][1]
                    except:
                        pass
                    try:
                        lastCmd = coll[0][6]
                    except:
                        pass
                    try:
                        rw = coll[0][4]
                    except:
                        pass
                    try:
                        prev_delta = coll[0][5]
                    except:
                        pass
            
                    if (
                        s_epoch > dt + sInterval*60-30
                        and
                        (rainTotal < prev_delta + 100 or len(coll) == 0)
                    ):
                        delta = rainTotal #Save reading for next round comparison
                        if rainTotal < rw: #Gauge has been resetted since start
                            if rainTotal >= prev_delta:
                                rainTotal = rw + rainTotal - prev_delta   
                            if rainTotal < prev_delta: #Gauge reset detected (battery change?)
                                rainTotal = rw + rainTotal   
                        if useRule:
                            fMov = self.CalculateRainMovAverage(
                                coll,
                                4,
                                rainTotal,
                                fMovAverage
                            )
                            fMov = int(fMov)
                            sMov = self.CalculateRainMovAverage(
                                coll, 
                                4, 
                                rainTotal, 
                                sMovAverage
                            )
                            sMov = int(sMov)
                            if not useHysteresis:
                                hysteresis = 0
                            res = self.RuleEvaluatorRain(
                                rule, 
                                fMov, 
                                sMov, 
                                lastCmd, 
                                tableId, 
                                hysteresis
                            )
                        lst = (date, s_epoch, tableId, rainRate, rainTotal, delta, res)
                        ss = "INSERT INTO "+self.rainData_db.split('.')[0]+" VALUES (?,?,?,?,?,?,?)"
                        with conn:
                            c.execute(ss,lst)
                        del coll
                        del res
                        del fMov
                        del sMov
        
                except sqlite3.Error, e:
                    eg.PrintError("Error %s:" % e.args[0])
                    time.sleep(2.0)     
                    
                finally:
                    if conn:
                        conn.close()
                    while not saveRainThreadEvent.isSet():
                        saveRainThreadEvent.wait(1.0)
                    del saveRainThreadEvent
                    item = self.q.get_nowait()
                    del item
                    self.q.task_done()


        saveRainThreadEvent = Event()
        saveRainThread = Thread(
            target=SaveRain,
            args=(saveRainThreadEvent, hysteresis, rainTotal)
        )
        self.AddToQueue(tableId)
        saveRainThread.start()
        saveRainThreadEvent.set()
       
           
            
## Actions ###################################################################
## Wind related actions ######################################################
class WindDataCapture(eg.ActionClass):
                
    def __call__(
        self,
        dbTableId = 'WindSensor on roof',
        deviceCode = '28928',
        sInterval = 10
    ):

        def CaptureWind():
            tst = ''
            addr = ''
            windDirection = ''
            windAverage = 0.0
            windGust = 0.0
            newEvent = eg.event.suffix
            newPayload = eg.event.payload
            base = newEvent.split(':')
            addr = base[2].strip(' ')
            if( addr == deviceCode):
                e_lst = []
                tst = str(newPayload)
                e_lst = tst.split(':')
                windDirection = str(e_lst[1].split(' ')[1])
                windAverage = float(e_lst[2].split(' ')[1])
                windGust = float(e_lst[3].split(' ')[1])

            return addr, windDirection, windAverage, windGust


        def SaveWind(captureWindThreadEvent, addr, windDirection, windAverage, windGust):
            if addr <> '':
                self.plugin.SaveWindData(
                    dbTableId,
                    windDirection,
                    windAverage,
                    windGust,
                    sInterval
                )

            while not captureWindThreadEvent.isSet():
                captureWindThreadEvent.wait(1.0)
            del captureWindThreadEvent
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()


        addr, windDirection, windAverage, windGust = CaptureWind()
        before = 0
        try:
            before = self.plugin.lastWindData[addr][0]
        except:
            pass
        now = time.time()
        diff = int(now-before)
       
        if diff >= sInterval*60:
            self.plugin.lastWindData[addr] = [now, windDirection, windAverage, windGust]
            captureWindThreadEvent = Event()
            captureWindThread = Thread(
                target=SaveWind,
                args=(captureWindThreadEvent,addr,windDirection,windAverage,windGust,)
            )
            self.plugin.AddToQueue(dbTableId)
            captureWindThread.start()
            captureWindThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        dbTableId = 'WindSensor on roof',
        deviceCode = '28928',
        sInterval = 10
    ):
        panel = eg.ConfigPanel(self)
        mySizer_2 = wx.GridBagSizer(10, 10)

        dbTableIdCtrl = wx.TextCtrl(panel, -1, dbTableId)
        dbTableIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbTableId),
            (1,0)
        )

        deviceCodeCtrl = wx.TextCtrl(panel, -1, deviceCode)
        deviceCodeCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbDevice),
            (3,0)
        )

        sIntervalCtrl = panel.SpinIntCtrl(sInterval, 1, 120)
        sIntervalCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.sInterval),
            (5,0)
        )

        mySizer_2.Add(dbTableIdCtrl, (2,0))
        mySizer_2.Add(deviceCodeCtrl, (4,0))
        mySizer_2.Add(sIntervalCtrl, (6,0))

        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetValue(),
                deviceCodeCtrl.GetValue(),
                sIntervalCtrl.GetValue()
            )



class ResetWindData(eg.ActionClass):
        
    def __call__(self, dbTableId):
        with self.plugin.wind_lock:
            self.plugin.DelData(
                self.plugin.windData_db, 
                dbTableId
            )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'WindSensor on roof'
    ):
        list = self.plugin.tablesWindData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)

        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(items=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableIdReset)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection()
            )



## Rain related actions ######################################################
class RainDataCapture(eg.ActionClass):
                
    def __call__(
        self,
        dbTableId = 'RainSensor on roof',
        deviceCode = '1796',
        sInterval = 10,
        fMovAverage = 5,
        sMovAverage = 15,
        useHysteresis = True,
        hysteresis = 5,
        useRule = False,
        rule = ''
    ):

        def CaptureRain():
            tst = ''
            addr = ''
            delta = 0
            rainRate = 0
            rainTotal = 0
            newEvent = eg.event.suffix
            newPayload = eg.event.payload
            base = newEvent.split(':')
            addr = base[2].strip(' ')
            if( addr == deviceCode):
                e_lst = []
                tst = str(newPayload)
                e_lst = tst.split(':')
                rainRate = int(e_lst[1].split(' ')[1])
                rainTotal = int(e_lst[2].split(' ')[1])

            return addr, rainRate, rainTotal


        def SaveRain(captureRainThreadEvent, addr, rainRate, rainTotal):
            if addr <> '':
                self.plugin.SaveRainData(
                    dbTableId,
                    rainRate,
                    rainTotal,
                    delta,
                    sInterval,
                    fMovAverage,
                    sMovAverage,
                    useHysteresis,
                    hysteresis,
                    useRule,
                    rule
                )

            while not captureRainThreadEvent.isSet():
                captureRainThreadEvent.wait(1.0)
            del captureRainThreadEvent
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()


        addr, rainRate, rainTotal = CaptureRain()
        before = 0
        try:
            before = self.plugin.lastRainData[addr][0]
        except:
            pass
        now = time.time()
        diff = int(now-before)
       
        if diff >= sInterval*60:
            self.plugin.lastRainData[addr] = [now, rainRate, rainTotal]
            captureRainThreadEvent = Event()
            captureRainThread = Thread(
                target=SaveRain,
                args=(captureRainThreadEvent,addr,rainRate,rainTotal,)
            )
            self.plugin.AddToQueue(dbTableId)
            captureRainThread.start()
            captureRainThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        dbTableId = 'RainSensor on roof',
        deviceCode = '46592',
        sInterval = 10,
        fMovAverage = 5,
        sMovAverage = 15,
        useHysteresis = True,
        hysteresis = 5,
        useRule = False,
        rule = ''
    ):
        panel = eg.ConfigPanel(self)
        mySizer_2 = wx.GridBagSizer(10, 10)

        dbTableIdCtrl = wx.TextCtrl(panel, -1, dbTableId)
        dbTableIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbTableId),
            (1,0)
        )

        deviceCodeCtrl = wx.TextCtrl(panel, -1, deviceCode)
        deviceCodeCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbDevice),
            (3,0)
        )

        sIntervalCtrl = panel.SpinIntCtrl(sInterval, 1, 120)
        sIntervalCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.sInterval),
            (5,0)
        )

        fMovAverageCtrl = panel.SpinIntCtrl(fMovAverage, 1, 120)
        fMovAverageCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.fMovAverage),
            (7,0)
        )

        sMovAverageCtrl = panel.SpinIntCtrl(sMovAverage, 1, 120)
        sMovAverageCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.sMovAverage),
            (9,0)
        )

        useHysteresisCtrl = wx.CheckBox(panel, -1, "")
        useHysteresisCtrl.SetValue(useHysteresis)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useHysteresis),
            (11,0)
        )

        hysteresisCtrl = panel.SpinIntCtrl(hysteresis, 0, 120)
        hysteresisCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.hysteresis),
            (13,0)
        )

        useRuleCtrl = wx.CheckBox(panel, -1, "")
        useRuleCtrl.SetValue(useRule)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useRule),
            (15,0)
        )

        # Create a dropdown for rule 
        list = [
            'equal-less-greater'
        ]
        ruleCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        ruleCtrl.AppendItems(items=list) 
        if list.count(rule)==0:
            ruleCtrl.Select(n=0)
        else:
            ruleCtrl.SetSelection(int(list.index(rule)))
        ruleCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.rule),
            (17,0)
        )
 
        mySizer_2.Add(dbTableIdCtrl, (2,0))
        mySizer_2.Add(deviceCodeCtrl, (4,0))
        mySizer_2.Add(sIntervalCtrl, (6,0))
        mySizer_2.Add(fMovAverageCtrl, (8,0))
        mySizer_2.Add(sMovAverageCtrl, (10,0))
        mySizer_2.Add(useHysteresisCtrl, (12,0))
        mySizer_2.Add(hysteresisCtrl, (14,0))
        mySizer_2.Add(useRuleCtrl, (16,0))
        mySizer_2.Add(ruleCtrl, (18,0))

        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetValue(),
                deviceCodeCtrl.GetValue(),
                sIntervalCtrl.GetValue(),
                fMovAverageCtrl.GetValue(),
                sMovAverageCtrl.GetValue(),
                useHysteresisCtrl.GetValue(),
                hysteresisCtrl.GetValue(),
                useRuleCtrl.GetValue(),
                ruleCtrl.GetStringSelection()
            )



class ResetRainData(eg.ActionClass):
        
    def __call__(self, dbTableId):
        with self.plugin.rain_lock:
            self.plugin.DelData(
                self.plugin.rainData_db, 
                dbTableId
            )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'RainSensor on roof'
    ):
        list = self.plugin.tablesRainData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)

        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(items=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableIdReset)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection()
            )

                

class RainRequestQuery(eg.ActionClass):

    def __call__(
        self, 
        dbTableId = 'RainSensor on roof',
        dateTimeFrom = '2001-01-01 00:00:01',
        dateTimeTo = '2001-12-31 23:59:59',
    ):
        with self.plugin.rain_lock:
            start, end = self.plugin.SearchData(
                self.plugin.rainData_db,
                dbTableId, 
                dateTimeFrom, 
                dateTimeTo
            )
        print start, end
        res = 0
        if start <> None and end <> None:
            res = (end[4] - start[4])
        return res
  


class RainRequestSearch(eg.ActionClass):

    def __call__(
        self, 
        dbTableId = 'RainSensor on roof',
        tornado = False,
        websocketsuite = False,
        port = 1235,
        bWebSServer = False
    ):
        def RainRqstSearch(rRequestSearchThreadEvent):
            pl = eg.event.payload
            dateTimeFrom = 'start'
            dateTimeTo = 'end'
            if len(pl)==1:       
                dateTimeFrom = pl[0]
                if dateTimeFrom == '':
                    dateTimeFrom = 'start'
            if len(pl)==2:       
                dateTimeTo = pl[1]
                if dateTimeTo == '':
                    dateTimeTo = 'end'
            with self.plugin.rain_lock:
                start, end = self.plugin.SearchData(
                    self.plugin.rainData_db,
                    dbTableId, 
                    dateTimeFrom, 
                    dateTimeTo
                )
            if start <> None and end <> None:
                msg = 'Rain from '+start[0]+' until '+end[0]
                msg = msg + ' : ' + str((end[4] - start[4]))
                print msg
                if tornado:
                    self.plugin.TornadoBroadcastMessage(msg)
                if websocketsuite:
                    self.plugin.WebsocketSuiteBroadcastMessage(str(port), msg)
                if bWebSServer:
                    self.plugin.WebserverBroadcastMessage(msg)
            else:
                print self.plugin.text.noData
    
            while not rRequestSearchThreadEvent.isSet():
                rRequestSearchThreadEvent.wait(1.0)
            del rRequestSearchThreadEvent
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()
    
        rRequestSearchThreadEvent = Event()
        rRequestSearchThread = Thread(
            target=RainRqstSearch,
            args=(rRequestSearchThreadEvent,)
        )
        self.plugin.AddToQueue(dbTableId)
        rRequestSearchThread.start()
        rRequestSearchThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'RainSensor on roof',
        tornado = False,
        websocketsuite = False,
        port = 1235,
        bWebSServer = False
    ):
        list = self.plugin.tablesRainData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)
        
        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(items=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        bWebSServerCtrl = wx.CheckBox(panel, -1, "")
        bWebSServerCtrl.SetValue(bWebSServer)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.use_WebserverWebsockets
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(bWebSServerCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        bTornadoWebSocketCtrl = wx.CheckBox(panel, -1, "")
        bTornadoWebSocketCtrl.SetValue(tornado)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.use_tornadoWebsockets
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(bTornadoWebSocketCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        bWebSocketCtrl = wx.CheckBox(panel, -1, "")
        bWebSocketCtrl.SetValue(websocketsuite)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.use_websockets)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(bWebSocketCtrl, 1, wx.EXPAND)
        
        portCtrl = panel.SpinIntCtrl(port, 1234, 1500)
        portCtrl.SetInitialSize((30,-1))
        sizer5.Add(portCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection(),
                bTornadoWebSocketCtrl.GetValue(),
                bWebSocketCtrl.GetValue(),
                portCtrl.GetValue(),
                bWebSServerCtrl.GetValue()
            )


                
## Temperature related actions ###############################################
class TempDataCapture(eg.ActionClass):

    def __call__(
        self,
        dbTableId = 'Temperature ground',
        deviceCode = '8194',
        sInterval = 10,
        setPoint = 15.0,
        movAverage = 5,
        useHysteresis = True,
        hysteresis = 2.0,
        useRule = False,
        rule = ''
    ):

        def CaptureTemp():
            tst = ''
            addr = ''
            temperature = 0.0
            newEvent = eg.event.suffix
            newPayload = eg.event.payload
    
            if eg.event.suffix.find('.ZWave/')!= -1: #For Z-Wave
                A = re.split(r'["]\s*', eg.event.payload)
                B = re.split(r'[.]\s*', eg.event.suffix)[1].split('/')[1]
                if B == deviceCode and A[3] == 'Sensor.Temperature':
                    addr = B
                    t = A[7].replace(',','.')
                    temperature = float("%.2f" % float(t))
                    print 'temperature:', temperature

            if eg.event.prefix == 'TellStickDuo':
                if(
                    newEvent.find('.Temperature.Humidity')!= -1
                    or
                    newEvent.find('.Temperature:')!= -1
                ):
                    base = newEvent.split('.')
                    addr = base[2]
                    if( addr == deviceCode):
                        e_lst = []
                        tst = str(newPayload)
                        e_lst = tst.split('|')
                        temperature = float("%.2f" % float(e_lst[0]))
    
            if eg.event.prefix == 'RFXtrx':
                base = newEvent.split(':')
                addr = base[2].strip(' ')
                if( addr == deviceCode):
                    e_lst = []
                    tst = str(newPayload)
                    e_lst = tst.split(':')
                    temperature = float("%.2f" % float(e_lst[1].split(' ')[1]))
    
            if eg.event.suffix.find('FineOffset|')!= -1: #For NHS
                addr = str(eg.event.suffix.split('|')[1])
                if( addr == deviceCode):
                    e_lst = []
                    tst = str(newPayload)
                    e_lst = tst.split('|')
                    temperature = float("%.2f" % float(e_lst[1]))
    
            if eg.event.suffix.find('Oregon|')!= -1: #For NHS
                addr = str(eg.event.suffix.split('|')[1])
                if( addr == deviceCode):
                    e_lst = []
                    tst = str(newPayload)
                    e_lst = tst.split('|')
                    temperature = float("%.2f" % float(e_lst[1]))

            return addr, temperature

    
        def SaveTemp(captureTempThreadEvent, addr, temperature):
            if addr <> '':
                self.plugin.SaveTempData(
                    dbTableId,
                    temperature,
                    sInterval,
                    setPoint,
                    movAverage,
                    useHysteresis,
                    hysteresis,
                    useRule,
                    rule
                )

            while not captureTempThreadEvent.isSet():
                captureTempThreadEvent.wait(1.0)
            del captureTempThreadEvent
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()

        
        addr, temperature = CaptureTemp()
        before = 0
        try:
            before = self.plugin.lastTempData[addr][0]
        except:
            pass
        now = time.time()
        diff = int(now-before)
       
        if diff >= sInterval*60:
            self.plugin.lastTempData[addr] = [now, temperature]
            captureTempThreadEvent = Event()
            captureTempThread = Thread(
                target=SaveTemp,
                args=(captureTempThreadEvent,addr,temperature,)
            )
            self.plugin.AddToQueue(dbTableId)
            captureTempThread.start()
            captureTempThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        dbTableId = 'Temperature ground',
        deviceCode = '8194',
        sInterval = 10,
        setPoint = 15.0,
        movAverage = 5,
        useHysteresis = True,
        hysteresis = 2.0,
        useRule = False,
        rule = ''
    ):
        panel = eg.ConfigPanel(self)
        mySizer_2 = wx.GridBagSizer(10, 10)

        dbTableIdCtrl = wx.TextCtrl(panel, -1, dbTableId)
        dbTableIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbTableId),
            (1,0)
        )

        deviceCodeCtrl = wx.TextCtrl(panel, -1, deviceCode)
        deviceCodeCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbDevice),
            (3,0)
        )

        sIntervalCtrl = panel.SpinIntCtrl(sInterval, 1, 120)
        sIntervalCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.sInterval),
            (5,0)
        )

        setPointCtrl = panel.SpinNumCtrl(
            setPoint,
            decimalChar = '.',   # by default, use '.' for decimal point
            groupChar = ',',     # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 3,
            min = -99.9,
            max = 99.9,
            increment = 0.1
        )
        setPointCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.setPoint),
            (7,0)
        )

        movAverageCtrl = panel.SpinIntCtrl(movAverage, 1, 120)
        movAverageCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.movAverage),
            (9,0)
        )

        useHysteresisCtrl = wx.CheckBox(panel, -1, "")
        useHysteresisCtrl.SetValue(useHysteresis)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useHysteresis),
            (11,0)
        )

        hysteresisCtrl = panel.SpinNumCtrl(
            hysteresis,
            decimalChar = '.',   # by default, use '.' for decimal point
            groupChar = ',',     # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 3,
            min = 0.0,
            max = 40.0,
            increment = 0.1
        )
        hysteresisCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.hysteresis),
            (13,0)
        )
        
        useRuleCtrl = wx.CheckBox(panel, -1, "")
        useRuleCtrl.SetValue(useRule)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useRule),
            (15,0)
        )

        # Create a dropdown for rule 
        list = [
            'equal-less-greater'
        ]
        ruleCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        ruleCtrl.AppendItems(items=list) 
        if list.count(rule)==0:
            ruleCtrl.Select(n=0)
        else:
            ruleCtrl.SetSelection(int(list.index(rule)))
        ruleCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.rule),
            (17,0)
        )
 
        mySizer_2.Add(dbTableIdCtrl, (2,0))
        mySizer_2.Add(deviceCodeCtrl, (4,0))
        mySizer_2.Add(sIntervalCtrl, (6,0))
        mySizer_2.Add(setPointCtrl, (8,0))
        mySizer_2.Add(movAverageCtrl, (10,0))
        mySizer_2.Add(useHysteresisCtrl, (12,0))
        mySizer_2.Add(hysteresisCtrl, (14,0))
        mySizer_2.Add(useRuleCtrl, (16,0))
        mySizer_2.Add(ruleCtrl, (18,0))

        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetValue(),
                deviceCodeCtrl.GetValue(),
                sIntervalCtrl.GetValue(),
                setPointCtrl.GetValue(),
                movAverageCtrl.GetValue(),
                useHysteresisCtrl.GetValue(),
                hysteresisCtrl.GetValue(),
                useRuleCtrl.GetValue(),
                ruleCtrl.GetStringSelection()
            )



class ResetTempData(eg.ActionClass):
        
    def __call__(self, dbTableId):
        with self.plugin.temp_lock:
            self.plugin.DelData(
                self.plugin.tempData_db, 
                dbTableId
            )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'Temperature ground'
    ):
        list = self.plugin.tablesTempData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)

        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(items=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableIdReset)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection()
            )



## Humidity related actions ###############################################
class HumDataCapture(eg.ActionClass):

    def __call__(
        self,
        dbTableId = 'Humidity ground',
        deviceCode = '8194',
        sInterval = 10,
        setPoint = 70,
        movAverage = 5,
        useHysteresis = True,
        hysteresis = 5,
        useRule = False,
        rule = ''
    ):

        def CaptureHum():
            tst = ''
            addr = ''
            humidity = 0
            newEvent = eg.event.suffix
            newPayload = eg.event.payload
    
            if eg.event.prefix == 'TellStickDuo':
                if newEvent.find('.Temperature.Humidity')!= -1:
                    base = newEvent.split('.')
                    addr = base[2]
                    if( addr == deviceCode):
                        e_lst = []
                        tst = str(newPayload)
                        e_lst = tst.split('|')
                        humidity = int(e_lst[1])
    
                if newEvent.find('.Humidity:')!= -1:
                    base = newEvent.split('.')
                    addr = base[2]
                    if( addr == deviceCode):
                        e_lst = []
                        tst = str(newPayload)
                        e_lst = tst.split('|')
                        humidity = int(e_lst[0])

            if eg.event.prefix == 'RFXtrx':
                base = newEvent.split(':')
                addr = base[2].strip(' ')
                if( addr == deviceCode):
                    e_lst = []
                    tst = str(newPayload)
                    e_lst = tst.split(':')
                    humidity = int(e_lst[2].split(' ')[1])
    
            if eg.event.suffix.find('Oregon|')!= -1: #For NHS
                addr = str(eg.event.suffix.split('|')[1])
                if( addr == deviceCode):
                    e_lst = []
                    tst = str(newPayload)
                    e_lst = tst.split('|')
                    humidity = int(e_lst[3])

            return addr, humidity
    

        def SaveHum(captureHumThreadEvent, addr, humidity):
            if addr <> '':
                self.plugin.SaveHumData(
                    dbTableId,
                    humidity,
                    sInterval,
                    setPoint,
                    movAverage,
                    useHysteresis,
                    hysteresis,
                    useRule,
                    rule
                )

            while not captureHumThreadEvent.isSet():
                captureHumThreadEvent.wait(1.0)
            del captureHumThreadEvent
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()


        addr, humidity = CaptureHum()
        before = 0
        try:
            before = self.plugin.lastHumData[addr][0]
        except:
            pass
        now = time.time()
        diff = int(now-before)
       
        if diff >= sInterval*60:
            self.plugin.lastHumData[addr] = [now, humidity]
            captureHumThreadEvent = Event()
            captureHumThread = Thread(
                target=SaveHum,
                args=(captureHumThreadEvent,addr,humidity,)
            )
            self.plugin.AddToQueue(dbTableId)
            captureHumThread.start()
            captureHumThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        dbTableId = 'Humidity ground',
        deviceCode = '8194',
        sInterval = 10,
        setPoint = 70,
        movAverage = 5,
        useHysteresis = True,
        hysteresis = 5,
        useRule = False,
        rule = ''
    ):
        panel = eg.ConfigPanel(self)
        mySizer_2 = wx.GridBagSizer(10, 10)

        dbTableIdCtrl = wx.TextCtrl(panel, -1, dbTableId)
        dbTableIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbTableId),
            (1,0)
        )

        deviceCodeCtrl = wx.TextCtrl(panel, -1, deviceCode)
        deviceCodeCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbDevice),
            (3,0)
        )

        sIntervalCtrl = panel.SpinIntCtrl(sInterval, 1, 120)
        sIntervalCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.sInterval),
            (5,0)
        )

        setPointCtrl = panel.SpinIntCtrl(setPoint, 1, 100)
        setPointCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.setPoint),
            (7,0)
        )

        movAverageCtrl = panel.SpinIntCtrl(movAverage, 1, 120)
        movAverageCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.movAverage),
            (9,0)
        )

        useHysteresisCtrl = wx.CheckBox(panel, -1, "")
        useHysteresisCtrl.SetValue(useHysteresis)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useHysteresis),
            (11,0)
        )

        hysteresisCtrl = panel.SpinIntCtrl(hysteresis, 0, 40)
        hysteresisCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.hysteresis),
            (13,0)
        )

        useRuleCtrl = wx.CheckBox(panel, -1, "")
        useRuleCtrl.SetValue(useRule)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useRule),
            (15,0)
        )

        # Create a dropdown for rule 
        list = [
            'equal-less-greater'
        ]
        ruleCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        ruleCtrl.AppendItems(items=list) 
        if list.count(rule)==0:
            ruleCtrl.Select(n=0)
        else:
            ruleCtrl.SetSelection(int(list.index(rule)))
        ruleCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.rule),
            (17,0)
        )
 
        mySizer_2.Add(dbTableIdCtrl, (2,0))
        mySizer_2.Add(deviceCodeCtrl, (4,0))
        mySizer_2.Add(sIntervalCtrl, (6,0))
        mySizer_2.Add(setPointCtrl, (8,0))
        mySizer_2.Add(movAverageCtrl, (10,0))
        mySizer_2.Add(useHysteresisCtrl, (12,0))
        mySizer_2.Add(hysteresisCtrl, (14,0))
        mySizer_2.Add(useRuleCtrl, (16,0))
        mySizer_2.Add(ruleCtrl, (18,0))

        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetValue(),
                deviceCodeCtrl.GetValue(),
                sIntervalCtrl.GetValue(),
                setPointCtrl.GetValue(),
                movAverageCtrl.GetValue(),
                useHysteresisCtrl.GetValue(),
                hysteresisCtrl.GetValue(),
                useRuleCtrl.GetValue(),
                ruleCtrl.GetStringSelection()
            )



class ResetHumData(eg.ActionClass):
        
    def __call__(self, dbTableId):
        with self.plugin.hum_lock:
            self.plugin.DelData(
                self.plugin.humData_db, 
                dbTableId
            )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'Humidity ground'
    ):
        list = self.plugin.tablesHumData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)

        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(items=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableIdReset)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection()
            )



## Barometric related actions ###############################################
class BarDataCapture(eg.ActionClass):

    def __call__(
        self,
        dbTableId = 'Barometric pressure',
        deviceCode = '25601',
        sInterval = 10,
        setPoint = 1000.0,
        movAverage = 5,
        useHysteresis = True,
        hysteresis = 100.0,
        useRule = False,
        rule = ''
    ):

        def CaptureBar():
            tst = ''
            addr = ''
            pressure = 0
            newEvent = eg.event.suffix
            newPayload = eg.event.payload
    
            if eg.event.prefix == 'RFXtrx':
                base = newEvent.split(':')
                addr = base[2].strip(' ')
                if( addr == deviceCode):
                    e_lst = []
                    tst = str(newPayload)
                    e_lst = tst.split(':')
                    pressure = float("%.2f" % float(e_lst[4].split(' ')[1]))
    
            return addr, pressure
    

        def SaveBar(captureBarThreadEvent, addr, pressure):
            if addr <> '':
                self.plugin.SaveBarData(
                    dbTableId,
                    pressure,
                    sInterval,
                    setPoint,
                    movAverage,
                    useHysteresis,
                    hysteresis,
                    useRule,
                    rule
                )

            while not captureBarThreadEvent.isSet():
                captureBarThreadEvent.wait(1.0)
            del captureBarThreadEvent
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()


        addr, pressure = CaptureBar()
        before = 0
        try:
            before = self.plugin.lastBarData[addr][0]
        except:
            pass
        now = time.time()
        diff = int(now-before)
       
        if diff >= sInterval*60:
            self.plugin.lastBarData[addr] = [now, pressure]
            captureBarThreadEvent = Event()
            captureBarThread = Thread(
                target=SaveBar,
                args=(captureBarThreadEvent,addr,pressure,)
            )
            self.plugin.AddToQueue(dbTableId)
            captureBarThread.start()
            captureBarThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'Barometric pressure',
        deviceCode = '25601',
        sInterval = 10,
        setPoint = 1000.0,
        movAverage = 5,
        useHysteresis = True,
        hysteresis = 100.0,
        useRule = False,
        rule = ''
    ):
        panel = eg.ConfigPanel(self)
        mySizer_2 = wx.GridBagSizer(10, 10)

        dbTableIdCtrl = wx.TextCtrl(panel, -1, dbTableId)
        dbTableIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbTableId),
            (1,0)
        )

        deviceCodeCtrl = wx.TextCtrl(panel, -1, deviceCode)
        deviceCodeCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbDevice),
            (3,0)
        )

        sIntervalCtrl = panel.SpinIntCtrl(sInterval, 1, 120)
        sIntervalCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.sInterval),
            (5,0)
        )

        setPointCtrl = panel.SpinNumCtrl(
            setPoint,
            decimalChar = '.',   # by default, use '.' for decimal point
            groupChar = ',',     # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 5,
            min = -990.0,
            max = 9990.0,
            increment = 10.0
        )
        setPointCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.setPoint),
            (7,0)
        )

        movAverageCtrl = panel.SpinIntCtrl(movAverage, 1, 120)
        movAverageCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.movAverage),
            (9,0)
        )

        useHysteresisCtrl = wx.CheckBox(panel, -1, "")
        useHysteresisCtrl.SetValue(useHysteresis)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useHysteresis),
            (11,0)
        )

        hysteresisCtrl = panel.SpinNumCtrl(
            hysteresis,
            decimalChar = '.',   # by default, use '.' for decimal point
            groupChar = ',',     # by default, use ',' for grouping
            fractionWidth = 1,
            integerWidth = 3,
            min = 0.0,
            max = 400.0,
            increment = 10.0
        )
        hysteresisCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.hysteresis),
            (13,0)
        )
        
        useRuleCtrl = wx.CheckBox(panel, -1, "")
        useRuleCtrl.SetValue(useRule)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.useRule),
            (15,0)
        )

        # Create a dropdown for rule 
        list = [
            'equal-less-greater'
        ]
        ruleCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        ruleCtrl.AppendItems(items=list) 
        if list.count(rule)==0:
            ruleCtrl.Select(n=0)
        else:
            ruleCtrl.SetSelection(int(list.index(rule)))
        ruleCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.rule),
            (17,0)
        )

        mySizer_2.Add(dbTableIdCtrl, (2,0))
        mySizer_2.Add(deviceCodeCtrl, (4,0))
        mySizer_2.Add(sIntervalCtrl, (6,0))
        mySizer_2.Add(setPointCtrl, (8,0))
        mySizer_2.Add(movAverageCtrl, (10,0))
        mySizer_2.Add(useHysteresisCtrl, (12,0))
        mySizer_2.Add(hysteresisCtrl, (14,0))
        mySizer_2.Add(useRuleCtrl, (16,0))
        mySizer_2.Add(ruleCtrl, (18,0))

        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetValue(),
                deviceCodeCtrl.GetValue(),
                sIntervalCtrl.GetValue(),
                setPointCtrl.GetValue(),
                movAverageCtrl.GetValue(),
                useHysteresisCtrl.GetValue(),
                hysteresisCtrl.GetValue(),
                useRuleCtrl.GetValue(),
                ruleCtrl.GetStringSelection()
            )



class ResetBarData(eg.ActionClass):
        
    def __call__(self, dbTableId):
        with self.plugin.bar_lock:
            self.plugin.DelData(
                self.plugin.barData_db, 
                dbTableId
            )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'Barometric pressure'
    ):
        list = self.plugin.tablesBarData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)

        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(items=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableIdReset)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection()
            )



## Light level related actions ###############################################
class LightDataCapture(eg.ActionClass):

    def __call__(
        self,
        dbTableId = 'Light level roof',
        sensorId = '20.09F40C000000/volt.B',
        sInterval = 10,
        movAverage = 5
    ):

        def CaptureLight(captureLightThreadEvent):
            tst = ''
            addr = ''
            lightlevel = 0
            fl = True

            if eg.event.suffix.find('.ZWave/')!= -1: #For Z-Wave
                A = re.split(r'["]\s*', eg.event.payload)
                B = re.split(r'[.]\s*', eg.event.suffix)[1].split('/')[1]
                if B == sensorId and A[3] == 'Sensor.Luminance':
                    addr = B
                    lightlevel = float("%.2f" % float(A[7]))
                    print 'lightlevel:', lightlevel

            if(
                eg.event.suffix == '/1wire' and not 
                eg.event.payload.find('disconnect') > 0
            ):
                dic = eval(eg.event.payload)
                addr = dic['sensorId']
                if( addr == sensorId):
                    lightlevel = dic['lightlevel']
                    try:
                        lightlevel = float("%.2f" % float(lightlevel))
                    except:
                        fl = False
    
            if addr <> '' and fl:
                self.plugin.SaveLightData(
                    dbTableId,
                    lightlevel,
                    sInterval,
                    movAverage
                )

            while not captureLightThreadEvent.isSet():
                captureLightThreadEvent.wait(1.0)
            del captureLightThreadEvent
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()

        captureLightThreadEvent = Event()
        captureLightThread = Thread(
            target=CaptureLight,
            args=(captureLightThreadEvent,)
        )
        self.plugin.AddToQueue(dbTableId)
        captureLightThread.start()
        captureLightThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        dbTableId = 'Light level roof',
        sensorId = '20.09F40C000000/volt.B',
        sInterval = 10,
        movAverage = 5
    ):
        panel = eg.ConfigPanel(self)
        mySizer_2 = wx.GridBagSizer(10, 10)

        dbTableIdCtrl = wx.TextCtrl(panel, -1, dbTableId)
        dbTableIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbTableId),
            (1,0)
        )

        sensorIdCtrl = wx.TextCtrl(panel, -1, sensorId)
        sensorIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbSensor),
            (3,0)
        )

        sIntervalCtrl = panel.SpinIntCtrl(sInterval, 1, 120)
        sIntervalCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.sInterval),
            (5,0)
        )

        movAverageCtrl = panel.SpinIntCtrl(movAverage, 1, 120)
        movAverageCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.movAverage),
            (7,0)
        )

        mySizer_2.Add(dbTableIdCtrl, (2,0))
        mySizer_2.Add(sensorIdCtrl, (4,0))
        mySizer_2.Add(sIntervalCtrl, (6,0))
        mySizer_2.Add(movAverageCtrl, (8,0))

        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetValue(),
                sensorIdCtrl.GetValue(),
                sIntervalCtrl.GetValue(),
                movAverageCtrl.GetValue()
            )



class ResetLightData(eg.ActionClass):
        
    def __call__(self, dbTableId):
        with self.plugin.light_lock:
            self.plugin.DelData(
                self.plugin.lightData_db, 
                dbTableId
            )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'Light level roof'
    ):
        list = self.plugin.tablesLightData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)

        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(items=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableIdReset)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection()
            )



## Dewpoint related actions ###############################################
class DewPointDataCapture(eg.ActionClass):

    def __call__(
        self,
        dbTableId = 'Dewpoint attic',
        sensorId = 'Difference to dew point in Attic'
    ):

        def CaptureDewPoint(captureDewpThreadEvent):
            dewpoint = 0.0
            if eg.event.payload.find(sensorId) > -1:
                lst = eg.event.payload.split(': ')
                dewpoint = float("%.1f" % float(lst[1]))
                self.plugin.SaveDewPointData(
                    dbTableId,
                    dewpoint
                )

            while not captureDewpThreadEvent.isSet():
                captureDewpThreadEvent.wait(1.0)
            del captureDewpThreadEvent
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()

        captureDewpThreadEvent = Event()
        captureDewpThread = Thread(
            target=CaptureDewPoint,
            args=(captureDewpThreadEvent,)
        )
        self.plugin.AddToQueue(dbTableId)
        captureDewpThread.start()
        captureDewpThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'Dewpoint attic',
        sensorId = 'Difference to dew point in Attic'
    ):
        panel = eg.ConfigPanel(self)
        mySizer_2 = wx.GridBagSizer(10, 10)

        dbTableIdCtrl = wx.TextCtrl(panel, -1, dbTableId)
        dbTableIdCtrl.SetInitialSize((150,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbTableId),
            (1,0)
        )

        sensorIdCtrl = wx.TextCtrl(panel, -1, sensorId)
        sensorIdCtrl.SetInitialSize((250,-1))
        mySizer_2.Add(
            wx.StaticText(panel, -1, self.plugin.text.dbSensor),
            (3,0)
        )

        mySizer_2.Add(dbTableIdCtrl, (2,0))
        mySizer_2.Add(sensorIdCtrl, (4,0))

        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetValue(),
                sensorIdCtrl.GetValue()
            )



class ResetDewPointData(eg.ActionClass):
        
    def __call__(self, dbTableId):
        with self.plugin.dewp_lock:
            self.plugin.DelData(
                self.plugin.dewPointData_db, 
                dbTableId
            )


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        dbTableId = 'Dewpoint attic'
    ):
        list = self.plugin.tablesDewPointData
        if list <> None:
            pass
        else:
            list = ['Empty']

        panel = eg.ConfigPanel(self)

        # Create a dropdown for dbTableId 
        dbTableIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        dbTableIdCtrl.AppendItems(items=list) 
        if list.count(dbTableId)==0:
            dbTableIdCtrl.Select(n=0)
        else:
            dbTableIdCtrl.SetSelection(int(list.index(dbTableId)))
        dbTableIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbTableIdReset)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(dbTableIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                dbTableIdCtrl.GetStringSelection()
            )



class RefreshTableNames(eg.ActionClass):
        
    def __call__(self):
        self.plugin.RefreshTableNames()



## Report section ############################################################
class CombinedReport(eg.ActionClass):

    def __call__(
        self, 
        rprtTitle = '',
        dbTableId_1 = ['Temperature ground'],
        dbTableId_2 = ['Humidity ground'],
        dbTableId_3 = ['RainSensor on roof'],
        dbTableId_4 = ['Light level roof'],
        dbTableId_5 = ['Dewpoint attic'],
        nbrOfLastDays = 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = '',
        rprtName = '',
        rprtHeading = '',
        dbTableId_6 = ['WindSensor on roof'],
        tenMinutes = True
    ):

        def CreateReport(createReportThreadEvent):
            hrs_back = nbrOfLastDays*24 + nbrOfLastHours
            now = datetime.datetime.now()
            dateTimeTo = now.strftime("%Y-%m-%d %H:%M")
            delta = datetime.timedelta(hours = -hrs_back)
            dateTimeFrom = (now + delta).strftime("%Y-%m-%d %H:%M")
    
            rows_1 = {}
            rows_2 = {}
            rows_3 = {}
            rows_4 = {}
            rows_5 = {}
            rows_6 = {}

            with self.plugin.temp_lock:
                for item in dbTableId_1:
                    rows = self.plugin.LastData(
                        self.plugin.tempData_db, 
                        item, 
                        dateTimeFrom
                    )
                    rows_1[item]=rows
    
            with self.plugin.hum_lock:
                for item in dbTableId_2:
                    rows = self.plugin.LastData(
                        self.plugin.humData_db, 
                        item, 
                        dateTimeFrom
                    )
                    rows_2[item]=rows
    
            with self.plugin.rain_lock:
                for item in dbTableId_3:
                    rows = self.plugin.LastData(
                        self.plugin.rainData_db, 
                        item, 
                        dateTimeFrom
                    )
                    rows_3[item]=rows
            
            with self.plugin.light_lock:
                for item in dbTableId_4:
                    rows = self.plugin.LastData(
                        self.plugin.lightData_db, 
                        item, 
                        dateTimeFrom
                    )
                    rows_4[item]=rows
    
            with self.plugin.dewp_lock:
                for item in dbTableId_5:
                    rows = self.plugin.LastData(
                        self.plugin.dewPointData_db, 
                        item, 
                        dateTimeFrom
                    )
                    rows_5[item]=rows
    
            with self.plugin.wind_lock:
                for item in dbTableId_6:
                    rows = self.plugin.LastData(
                        self.plugin.windData_db, 
                        item, 
                        dateTimeFrom
                    )
                    rows_6[item]=rows

            CreateComboHtml.CreateComboHtml(
                rprtName, 
                "Comboreport", 
                fPath, 
                rows_1, 
                "['Column1', 'Temperature', { role: 'style' }]", 
                3,
                rows_2, 
                "['Column1', 'Humidity', { role: 'style' }]", 
                3,
                rows_3, 
                "['Time', 'Rain level', { role: 'style' } ]", 
                4,
                rows_4, 
                "['Time', 'Light level', { role: 'style' } ]", 
                4,
                rows_5, 
                "['Time', 'Dewpoint delta', { role: 'style' } ]", 
                3,
                rows_6, 
                "['Time', 'Wind strenght and direction', { role: 'style' } ]", 
                5,
                rprtTitle,
                rprtHeading,
                tenMinutes
            )
            del rows
            del rows_1
            del rows_2
            del rows_3
            del rows_4
            del rows_5
            del rows_6
           
            while not createReportThreadEvent.isSet():
                createReportThreadEvent.wait(1.0)
            del createReportThreadEvent
            eg.TriggerEvent(
                rprtName,
                payload = "Combo report created",
                prefix = 'ClimateDataCalculation'
            )
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()

        #reload(CreateComboHtml)
        createReportThreadEvent = Event()
        createReportThread = Thread(
            target=CreateReport,
            args=(createReportThreadEvent,)
        )
        self.plugin.AddToQueue(rprtName)
        createReportThread.start()
        createReportThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        rprtTitle = 'EventGhost Combo Report',
        dbTableId_1 = [''],
        dbTableId_2 = [''],
        dbTableId_3 = [''],
        dbTableId_4 = [''],
        dbTableId_5 = [''],
        nbrOfLastDays= 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = eg.mainDir+'\Log\HighCharts',
        rprtName = 'Filename',
        rprtHeading = 'EventGhost Climate Data Report Graph',
        dbTableId_6 = [''],
        tenMinutes = True
        ):

        def GetSel(sel, list):
                val = []
                for i in sel:
                    val.append(list[i])
                return tuple(val)

        panel = eg.ConfigPanel(self)

        # Create dropdowns for dbTableId's 
        list_1 = self.plugin.tablesTempData
        if list_1 <> None:
            pass
        else:
            list_1 = ['Empty']
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbReportTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        sizer11 = wx.BoxSizer(wx.HORIZONTAL)
        lbox11 = wx.ListBox(
            panel,-1,
            size=wx.Size(150,100),
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB|wx.HORIZONTAL
        )
        lbox11.Set(list_1)
        for item in dbTableId_1:
            if item in list_1:
                idx = list_1.index(item)
                lbox11.SetSelection(idx)    
        sizer11.Add(lbox11, 1)
        staticBoxSizer.Add(sizer11, 0, wx.EXPAND|wx.ALL, 15)

        list_2 = self.plugin.tablesHumData
        if list_2 <> None:
            pass
        else:
            list_2 = ['Empty']
        sizer12 = wx.BoxSizer(wx.HORIZONTAL)
        lbox12 = wx.ListBox(
            panel,-1,
            size=wx.Size(150,100),
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB|wx.HORIZONTAL
        )
        lbox12.Set(list_2)
        for item in dbTableId_2:
            if item in list_2:
                idx = list_2.index(item)
                lbox12.SetSelection(idx)    
        sizer12.Add(lbox12, 1)
        staticBoxSizer.Add(sizer12, 0, wx.EXPAND|wx.ALL, 15)

        list_3 = self.plugin.tablesRainData
        if list_3 <> None:
            pass
        else:
            list_3 = ['Empty']
        sizer13 = wx.BoxSizer(wx.HORIZONTAL)
        lbox13 = wx.ListBox(
            panel,-1,
            size=wx.Size(150,100),
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB|wx.HORIZONTAL
        )
        lbox13.Set(list_3)
        for item in dbTableId_3:
            if item in list_3:
                idx = list_3.index(item)
                lbox13.SetSelection(idx)    
        sizer13.Add(lbox13, 1)
        staticBoxSizer.Add(sizer13, 0, wx.EXPAND|wx.ALL, 15)

        list_4 = self.plugin.tablesLightData
        if list_4 <> None:
            pass
        else:
            list_4 = ['Empty']
        sizer14 = wx.BoxSizer(wx.HORIZONTAL)
        lbox14 = wx.ListBox(
            panel,-1,
            size=wx.Size(150,100),
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB|wx.HORIZONTAL
        )
        lbox14.Set(list_4)
        for item in dbTableId_4:
            if item in list_4:
                idx = list_4.index(item)
                lbox14.SetSelection(idx)    
        sizer14.Add(lbox14, 1)
        staticBoxSizer.Add(sizer14, 0, wx.EXPAND|wx.ALL, 15)

        list_5 = self.plugin.tablesDewPointData
        if list_5 <> None:
            pass
        else:
            list_5 = ['Empty']
        sizer15 = wx.BoxSizer(wx.HORIZONTAL)
        lbox15 = wx.ListBox(
            panel,-1,
            size=wx.Size(150,100),
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB|wx.HORIZONTAL
        )
        lbox15.Set(list_5)
        for item in dbTableId_5:
            if item in list_5:
                idx = list_5.index(item)
                lbox15.SetSelection(idx)    
        sizer15.Add(lbox15, 1)
        staticBoxSizer.Add(sizer15, 0, wx.EXPAND|wx.ALL, 15)

        list_6 = self.plugin.tablesWindData
        if list_6 <> None:
            pass
        else:
            list_6 = ['Empty']
        sizer16 = wx.BoxSizer(wx.HORIZONTAL)
        lbox16 = wx.ListBox(
            panel,-1,
            size=wx.Size(150,100),
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB|wx.HORIZONTAL
        )
        lbox16.Set(list_6)
        for item in dbTableId_6:
            if item in list_6:
                idx = list_6.index(item)
                lbox16.SetSelection(idx)    
        sizer16.Add(lbox16, 1)
        staticBoxSizer.Add(sizer16, 0, wx.EXPAND|wx.ALL, 15)
        
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastDays 
        nbrOfLastDaysCtrl = panel.SpinIntCtrl(nbrOfLastDays, 0, 365)
        nbrOfLastDaysCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastDays)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(nbrOfLastDaysCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastHours 
        nbrOfLastHoursCtrl = panel.SpinIntCtrl(nbrOfLastHours, 0, 24)
        nbrOfLastHoursCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastHours)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(nbrOfLastHoursCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
 
        # Create a control for generating the html page 
        tenMinutesCtrl = wx.CheckBox(panel, -1, "")
        tenMinutesCtrl.SetValue(tenMinutes)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.tenMinutes
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(tenMinutesCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        cHtmlCtrl = wx.CheckBox(panel, -1, "")
        cHtmlCtrl.SetValue(cHtml)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.cHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(cHtmlCtrl, 1, wx.EXPAND)
        
        fPathCtrl = wx.TextCtrl(panel, -1, fPath)
        fPathCtrl.SetInitialSize((300,-1))
        sizer6.Add(fPathCtrl, 1, wx.EXPAND)
        nameCtrl = wx.TextCtrl(panel, -1, rprtName)
        nameCtrl.SetInitialSize((250,-1))
        sizer6.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        titleCtrl = wx.TextCtrl(panel, -1, rprtTitle)
        titleCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.titleHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(titleCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        headingCtrl = wx.TextCtrl(panel, -1, rprtHeading)
        headingCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.headingHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer8.Add(headingCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer8, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            dbTableId_1 = GetSel(lbox11.GetSelections(),list_1)
            dbTableId_2 = GetSel(lbox12.GetSelections(),list_2)
            dbTableId_3 = GetSel(lbox13.GetSelections(),list_3)
            dbTableId_4 = GetSel(lbox14.GetSelections(),list_4)
            dbTableId_5 = GetSel(lbox15.GetSelections(),list_5)
            dbTableId_6 = GetSel(lbox16.GetSelections(),list_6)

            panel.SetResult(
                titleCtrl.GetValue(),
                dbTableId_1,
                dbTableId_2,
                dbTableId_3,
                dbTableId_4,
                dbTableId_5,
                nbrOfLastDaysCtrl.GetValue(), 
                nbrOfLastHoursCtrl.GetValue(),
                cHtmlCtrl.GetValue(),
                fPathCtrl.GetValue(),
                nameCtrl.GetValue(),
                headingCtrl.GetValue(),
                dbTableId_6,
                tenMinutesCtrl.GetValue()
            )



class ComparisonReport(eg.ActionClass):

    def __call__(
        self, 
        rprtTitle = '',
        dbTableId_1 = ['Temperature ground'],
        dbTableId_2 = ['Humidity ground'],
        nbrOfLastDays = 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = '',
        rprtName = '',
        rprtHeading = '',
        tenMinutes = True
    ):

        def CreateReport(createReportThreadEvent):
            hrs_back = nbrOfLastDays*24 + nbrOfLastHours
            now = datetime.datetime.now()
            dateTimeTo = now.strftime("%Y-%m-%d %H:%M")
            delta = datetime.timedelta(hours = -hrs_back)
            dateTimeFrom = (now + delta).strftime("%Y-%m-%d %H:%M")

            tf_now = datetime.datetime.now() - datetime.timedelta(hours=24)
            tf_dateTimeTo = tf_now.strftime("%Y-%m-%d %H:%M")
            tf_dateTimeFrom = (tf_now + delta).strftime("%Y-%m-%d %H:%M")

            rows_1 = {}
            rows_2 = {}
            ep = 0

            with self.plugin.temp_lock:
                for item in dbTableId_1:

                    rows = self.plugin.LastData(
                        self.plugin.tempData_db, 
                        item, 
                        dateTimeFrom
                    )
                    ep = rows[-1][1]                    
                    rows_1[item]=rows
                    #print len(rows), 'Current time'

                    rows = self.plugin.LastData(
                        self.plugin.tempData_db, 
                        item, 
                        tf_dateTimeFrom
                    )
                    nl = []

                    for r in rows:
                        tf_date = (
                            datetime.datetime.fromtimestamp(r[1]) + 
                            datetime.timedelta(days=1)
                        )
                        #only add row more than 24 hours older
                        if r[1] <= ep-86400:
                            s = list(r)
                            s[0] = tf_date.strftime('%c')
                            t = tuple(s)
                            nl.append(t)

                    rows_1['Yesterday: '+item]=nl
                    #print len(nl), '24 hours back'
                        
            with self.plugin.hum_lock:
                for item in dbTableId_2:

                    rows = self.plugin.LastData(
                        self.plugin.humData_db, 
                        item, 
                        dateTimeFrom
                    )
                    ep = rows[-1][1]                    
                    rows_2[item]=rows
                    #print len(rows), 'Current time'

                    rows = self.plugin.LastData(
                        self.plugin.humData_db, 
                        item, 
                        tf_dateTimeFrom
                    )
                    nl = []

                    for r in rows:
                        tf_date = (
                            datetime.datetime.fromtimestamp(r[1]) + 
                            datetime.timedelta(days=1)
                        )
                        #only add row if at least 24 hours older
                        if r[1] <= ep-86400:
                            s = list(r)
                            s[0] = tf_date.strftime('%c')
                            t = tuple(s)
                            nl.append(t)
                        
                     
                    rows_2['Yesterday: '+item]=nl
                    #print len(nl), '24 hours back'

            CreateComparisonHtml.CreateComparisonHtml(
                rprtName, 
                "ComparisonReport", 
                fPath, 
                rows_1, 
                "['Column1', 'Temperature', { role: 'style' }]", 
                3,
                rows_2, 
                "['Column1', 'Humidity', { role: 'style' }]", 
                3,
                rprtTitle,
                rprtHeading,
                tenMinutes
            )
            del rows
            del rows_1
            del rows_2
           
            while not createReportThreadEvent.isSet():
                createReportThreadEvent.wait(1.0)
            del createReportThreadEvent
            eg.TriggerEvent(
                rprtName,
                payload = "Comparison report created",
                prefix = 'ClimateDataCalculation'
            )
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()

        #reload(CreateComparisonHtml)
        createReportThreadEvent = Event()
        createReportThread = Thread(
            target=CreateReport,
            args=(createReportThreadEvent,)
        )
        self.plugin.AddToQueue(rprtName)
        createReportThread.start()
        createReportThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        rprtTitle = 'EventGhost Comparison Report',
        dbTableId_1 = [''],
        dbTableId_2 = [''],
        nbrOfLastDays= 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = eg.mainDir+'\Log\HighCharts',
        rprtName = 'Filename',
        rprtHeading = 'EventGhost Climate Data Report Graph',
        tenMinutes = True
        ):

        def GetSel(sel, list):
                val = []
                for i in sel:
                    val.append(list[i])
                return tuple(val)

        panel = eg.ConfigPanel(self)

        # Create dropdowns for dbTableId's 
        list_1 = self.plugin.tablesTempData
        if list_1 <> None:
            pass
        else:
            list_1 = ['Empty']
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbReportTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        sizer11 = wx.BoxSizer(wx.HORIZONTAL)
        lbox11 = wx.ListBox(
            panel,-1,
            size=wx.Size(150,100),
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB|wx.HORIZONTAL
        )
        lbox11.Set(list_1)
        for item in dbTableId_1:
            if item in list_1:
                idx = list_1.index(item)
                lbox11.SetSelection(idx)    
        sizer11.Add(lbox11, 1)
        staticBoxSizer.Add(sizer11, 0, wx.EXPAND|wx.ALL, 15)

        list_2 = self.plugin.tablesHumData
        if list_2 <> None:
            pass
        else:
            list_2 = ['Empty']
        sizer12 = wx.BoxSizer(wx.HORIZONTAL)
        lbox12 = wx.ListBox(
            panel,-1,
            size=wx.Size(150,100),
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB|wx.HORIZONTAL
        )
        lbox12.Set(list_2)
        for item in dbTableId_2:
            if item in list_2:
                idx = list_2.index(item)
                lbox12.SetSelection(idx)    
        sizer12.Add(lbox12, 1)
        staticBoxSizer.Add(sizer12, 0, wx.EXPAND|wx.ALL, 15)
        
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastDays 
        nbrOfLastDaysCtrl = panel.SpinIntCtrl(nbrOfLastDays, 0, 365)
        nbrOfLastDaysCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastDays)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(nbrOfLastDaysCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastHours 
        nbrOfLastHoursCtrl = panel.SpinIntCtrl(nbrOfLastHours, 0, 24)
        nbrOfLastHoursCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastHours)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(nbrOfLastHoursCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
 
        # Create a control for generating the html page 
        tenMinutesCtrl = wx.CheckBox(panel, -1, "")
        tenMinutesCtrl.SetValue(tenMinutes)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.tenMinutes
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(tenMinutesCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        cHtmlCtrl = wx.CheckBox(panel, -1, "")
        cHtmlCtrl.SetValue(cHtml)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.cHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(cHtmlCtrl, 1, wx.EXPAND)
        
        fPathCtrl = wx.TextCtrl(panel, -1, fPath)
        fPathCtrl.SetInitialSize((300,-1))
        sizer6.Add(fPathCtrl, 1, wx.EXPAND)
        nameCtrl = wx.TextCtrl(panel, -1, rprtName)
        nameCtrl.SetInitialSize((250,-1))
        sizer6.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        titleCtrl = wx.TextCtrl(panel, -1, rprtTitle)
        titleCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.titleHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(titleCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        headingCtrl = wx.TextCtrl(panel, -1, rprtHeading)
        headingCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.headingHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer8.Add(headingCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer8, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            dbTableId_1 = GetSel(lbox11.GetSelections(),list_1)
            dbTableId_2 = GetSel(lbox12.GetSelections(),list_2)

            panel.SetResult(
                titleCtrl.GetValue(),
                dbTableId_1,
                dbTableId_2,
                nbrOfLastDaysCtrl.GetValue(), 
                nbrOfLastHoursCtrl.GetValue(),
                cHtmlCtrl.GetValue(),
                fPathCtrl.GetValue(),
                nameCtrl.GetValue(),
                headingCtrl.GetValue(),
                tenMinutesCtrl.GetValue()
            )



class WindRoseReport(eg.ActionClass):

    def __call__(
        self, 
        rprtTitle = '',
        rprtName = '',
        rprtHeading = '',
        dbTableId = ['WindSensor on roof'],
        nbrOfLastDays = 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = '',
        tenMinutes = True
    ):

        def CreateReport(createReportThreadEvent):
            hrs_back = nbrOfLastDays*24 + nbrOfLastHours
            now = datetime.datetime.now()
            dateTimeTo = now.strftime("%Y-%m-%d %H:%M")
            delta = datetime.timedelta(hours = -hrs_back)
            dateTimeFrom = (now + delta).strftime("%Y-%m-%d %H:%M")
            rows_1 = {}
            with self.plugin.wind_lock:
                for item in dbTableId:
                    rows = self.plugin.LastData(
                        self.plugin.windData_db, 
                        item, 
                        dateTimeFrom
                    )
                    rows_1[item]=rows

            CreateWindRoseHtml.CreateWindRoseHtml(
                rprtName, 
                fPath, 
                rows_1, 
                rprtTitle,
                rprtHeading,
                tenMinutes
            )
            del rows
            del rows_1
           
            while not createReportThreadEvent.isSet():
                createReportThreadEvent.wait(1.0)
            del createReportThreadEvent
            eg.TriggerEvent(
                rprtName,
                payload = "Wind Rose report created",
                prefix = 'ClimateDataCalculation'
            )
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()

        #reload(CreateWindRoseHtml)
        createReportThreadEvent = Event()
        createReportThread = Thread(
            target=CreateReport,
            args=(createReportThreadEvent,)
        )
        self.plugin.AddToQueue(rprtName)
        createReportThread.start()
        createReportThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        rprtTitle = 'EventGhost Wind Rose Report',
        rprtName = 'Filename',
        rprtHeading = 'EventGhost Climate Data Report Graph',
        dbTableId = [''],
        nbrOfLastDays= 5,
        nbrOfLastHours = 0,
        cHtml = True,
        fPath = eg.mainDir+'\Log\HighCharts',
        tenMinutes = True
    ):

        def GetSel(sel, list):
                val = []
                for i in sel:
                    val.append(list[i])
                return tuple(val)

        panel = eg.ConfigPanel(self)

        # Create dropdowns for dbTableId's 
        list_6 = self.plugin.tablesWindData
        if list_6 <> None:
            pass
        else:
            list_6 = ['Empty']
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbReportTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        sizer16 = wx.BoxSizer(wx.HORIZONTAL)
        lbox16 = wx.ListBox(
            panel,-1,
            size=wx.Size(150,100),
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB|wx.HORIZONTAL
        )
        lbox16.Set(list_6)
        for item in dbTableId:
            if item in list_6:
                idx = list_6.index(item)
                lbox16.SetSelection(idx)    
        sizer16.Add(lbox16, 1)
        staticBoxSizer.Add(sizer16, 0, wx.EXPAND|wx.ALL, 15)
        
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastDays 
        nbrOfLastDaysCtrl = panel.SpinIntCtrl(nbrOfLastDays, 0, 365)
        nbrOfLastDaysCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastDays)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(nbrOfLastDaysCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastHours 
        nbrOfLastHoursCtrl = panel.SpinIntCtrl(nbrOfLastHours, 0, 24)
        nbrOfLastHoursCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastHours)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(nbrOfLastHoursCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
 
        # Create a control for generating the html page 
        tenMinutesCtrl = wx.CheckBox(panel, -1, "")
        tenMinutesCtrl.SetValue(tenMinutes)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.tenMinutes
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(tenMinutesCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        cHtmlCtrl = wx.CheckBox(panel, -1, "")
        cHtmlCtrl.SetValue(cHtml)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.cHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(cHtmlCtrl, 1, wx.EXPAND)
        fPathCtrl = wx.TextCtrl(panel, -1, fPath)
        fPathCtrl.SetInitialSize((300,-1))
        sizer6.Add(fPathCtrl, 1, wx.EXPAND)
        nameCtrl = wx.TextCtrl(panel, -1, rprtName)
        nameCtrl.SetInitialSize((250,-1))
        sizer6.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        titleCtrl = wx.TextCtrl(panel, -1, rprtTitle)
        titleCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.titleHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(titleCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        headingCtrl = wx.TextCtrl(panel, -1, rprtHeading)
        headingCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.headingHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer8.Add(headingCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer8, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            dbTableId = GetSel(lbox16.GetSelections(),list_6)

            panel.SetResult(
                titleCtrl.GetValue(),
                nameCtrl.GetValue(),
                headingCtrl.GetValue(),
                dbTableId,
                nbrOfLastDaysCtrl.GetValue(), 
                nbrOfLastHoursCtrl.GetValue(),
                cHtmlCtrl.GetValue(),
                fPathCtrl.GetValue(),
                tenMinutesCtrl.GetValue()
            )



class WindMiniRoseReport(eg.ActionClass):

    def __call__(
        self, 
        rprtTitle = '',
        rprtName = '',
        rprtHeading = '',
        dbTableId = ['WindSensor on roof'],
        nbrOfLastDays = 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = '',
        tenMinutes = True
    ):

        def CreateReport(createReportThreadEvent):
            hrs_back = nbrOfLastDays*24 + nbrOfLastHours
            now = datetime.datetime.now()
            dateTimeTo = now.strftime("%Y-%m-%d %H:%M")
            delta = datetime.timedelta(hours = -hrs_back)
            dateTimeFrom = (now + delta).strftime("%Y-%m-%d %H:%M")
            rows_1 = {}
            with self.plugin.wind_lock:
                for item in dbTableId:
                    rows = self.plugin.LastData(
                        self.plugin.windData_db, 
                        item, 
                        dateTimeFrom
                    )
                    rows_1[item]=rows

            CreateWindMiniRoseHtml.CreateWindMiniRoseHtml(
                rprtName, 
                fPath, 
                rows_1, 
                rprtTitle,
                rprtHeading,
                tenMinutes
            )
            del rows
            del rows_1
           
            while not createReportThreadEvent.isSet():
                createReportThreadEvent.wait(1.0)
            del createReportThreadEvent
            eg.TriggerEvent(
                rprtName,
                payload = "Wind Mini Rose report created",
                prefix = 'ClimateDataCalculation'
            )
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()

        #reload(CreateWindMiniRoseHtml)
        createReportThreadEvent = Event()
        createReportThread = Thread(
            target=CreateReport,
            args=(createReportThreadEvent,)
        )
        self.plugin.AddToQueue(rprtName)
        createReportThread.start()
        createReportThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        rprtTitle = 'EventGhost Climate Data Report',
        rprtName = 'Filename',
        rprtHeading = 'Wind Mini Rose Report',
        dbTableId = [''],
        nbrOfLastDays= 7,
        nbrOfLastHours = 0,
        cHtml = True,
        fPath = eg.mainDir+'\Log\HighCharts',
        tenMinutes = True
    ):

        def GetSel(sel, list):
                val = []
                for i in sel:
                    val.append(list[i])
                return tuple(val)

        panel = eg.ConfigPanel(self)

        # Create dropdowns for dbTableId's 
        list_6 = self.plugin.tablesWindData
        if list_6 <> None:
            pass
        else:
            list_6 = ['Empty']
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbReportTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        sizer16 = wx.BoxSizer(wx.HORIZONTAL)
        lbox16 = wx.ListBox(
            panel,-1,
            size=wx.Size(150,100),
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB|wx.HORIZONTAL
        )
        lbox16.Set(list_6)
        for item in dbTableId:
            if item in list_6:
                idx = list_6.index(item)
                lbox16.SetSelection(idx)    
        sizer16.Add(lbox16, 1)
        staticBoxSizer.Add(sizer16, 0, wx.EXPAND|wx.ALL, 15)
        
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastDays 
        nbrOfLastDaysCtrl = panel.SpinIntCtrl(nbrOfLastDays, 0, 365)
        nbrOfLastDaysCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastDays)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(nbrOfLastDaysCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastHours 
        nbrOfLastHoursCtrl = panel.SpinIntCtrl(nbrOfLastHours, 0, 24)
        nbrOfLastHoursCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastHours)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(nbrOfLastHoursCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
 
        # Create a control for generating the html page 
        tenMinutesCtrl = wx.CheckBox(panel, -1, "")
        tenMinutesCtrl.SetValue(tenMinutes)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.tenMinutes
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(tenMinutesCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        cHtmlCtrl = wx.CheckBox(panel, -1, "")
        cHtmlCtrl.SetValue(cHtml)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.cHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(cHtmlCtrl, 1, wx.EXPAND)
        fPathCtrl = wx.TextCtrl(panel, -1, fPath)
        fPathCtrl.SetInitialSize((300,-1))
        sizer6.Add(fPathCtrl, 1, wx.EXPAND)
        nameCtrl = wx.TextCtrl(panel, -1, rprtName)
        nameCtrl.SetInitialSize((250,-1))
        sizer6.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        titleCtrl = wx.TextCtrl(panel, -1, rprtTitle)
        titleCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.titleHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(titleCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        headingCtrl = wx.TextCtrl(panel, -1, rprtHeading)
        headingCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.headingHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer8.Add(headingCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer8, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            dbTableId = GetSel(lbox16.GetSelections(),list_6)

            panel.SetResult(
                titleCtrl.GetValue(),
                nameCtrl.GetValue(),
                headingCtrl.GetValue(),
                dbTableId,
                nbrOfLastDaysCtrl.GetValue(), 
                nbrOfLastHoursCtrl.GetValue(),
                cHtmlCtrl.GetValue(),
                fPathCtrl.GetValue(),
                tenMinutesCtrl.GetValue()
            )



class TemperatureReport(eg.ActionClass):

    def __call__(
        self, 
        rprtTitle = '',
        dbTableId_1 = ['Temperature ground'],
        nbrOfLastDays = 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = '',
        rprtName = '',
        rprtHeading = '',
        tenMinutes = True
    ):

        def CreateReport(createReportThreadEvent):
            hrs_back = nbrOfLastDays*24 + nbrOfLastHours
            now = datetime.datetime.now()
            dateTimeTo = now.strftime("%Y-%m-%d %H:%M")
            delta = datetime.timedelta(hours = -hrs_back)
            dateTimeFrom = (now + delta).strftime("%Y-%m-%d %H:%M")
    
            rows_1 = {}

            with self.plugin.temp_lock:
                for item in dbTableId_1:
                    rows = self.plugin.LastData(
                        self.plugin.tempData_db, 
                        item, 
                        dateTimeFrom
                    )
                    rows_1[item]=rows
    
            CreateTempHtml.CreateTempHtml(
                rprtName, 
                "Comboreport", 
                fPath, 
                rows_1, 
                "['Column1', 'Temperature', { role: 'style' }]", 
                3,
                rprtTitle,
                rprtHeading,
                tenMinutes
            )
            del rows
            del rows_1
           
            while not createReportThreadEvent.isSet():
                createReportThreadEvent.wait(1.0)
            del createReportThreadEvent
            eg.TriggerEvent(
                rprtName,
                payload = "Temperature report created",
                prefix = 'ClimateDataCalculation'
            )
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()

        #reload(CreateTempHtml)
        createReportThreadEvent = Event()
        createReportThread = Thread(
            target=CreateReport,
            args=(createReportThreadEvent,)
        )
        self.plugin.AddToQueue(rprtName)
        createReportThread.start()
        createReportThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        rprtTitle = 'EventGhost Temperature Report',
        dbTableId_1 = [''],
        nbrOfLastDays= 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = eg.mainDir+'\Log\HighCharts',
        rprtName = 'Filename',
        rprtHeading = 'EventGhost Climate Data Report Graph',
        tenMinutes = True
        ):

        def GetSel(sel, list):
                val = []
                for i in sel:
                    val.append(list[i])
                return tuple(val)

        panel = eg.ConfigPanel(self)

        # Create dropdowns for dbTableId's 
        list_1 = self.plugin.tablesTempData
        if list_1 <> None:
            pass
        else:
            list_1 = ['Empty']
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbReportTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        sizer11 = wx.BoxSizer(wx.HORIZONTAL)
        lbox11 = wx.ListBox(
            panel,-1,
            size=wx.Size(150,100),
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB|wx.HORIZONTAL
        )
        lbox11.Set(list_1)
        for item in dbTableId_1:
            if item in list_1:
                idx = list_1.index(item)
                lbox11.SetSelection(idx)    
        sizer11.Add(lbox11, 1)
        staticBoxSizer.Add(sizer11, 0, wx.EXPAND|wx.ALL, 15)
        
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastDays 
        nbrOfLastDaysCtrl = panel.SpinIntCtrl(nbrOfLastDays, 0, 365)
        nbrOfLastDaysCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastDays)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(nbrOfLastDaysCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastHours 
        nbrOfLastHoursCtrl = panel.SpinIntCtrl(nbrOfLastHours, 0, 24)
        nbrOfLastHoursCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastHours)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(nbrOfLastHoursCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
 
        # Create a control for generating the html page 
        tenMinutesCtrl = wx.CheckBox(panel, -1, "")
        tenMinutesCtrl.SetValue(tenMinutes)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.tenMinutes
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(tenMinutesCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        cHtmlCtrl = wx.CheckBox(panel, -1, "")
        cHtmlCtrl.SetValue(cHtml)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.cHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(cHtmlCtrl, 1, wx.EXPAND)
        
        fPathCtrl = wx.TextCtrl(panel, -1, fPath)
        fPathCtrl.SetInitialSize((300,-1))
        sizer6.Add(fPathCtrl, 1, wx.EXPAND)
        nameCtrl = wx.TextCtrl(panel, -1, rprtName)
        nameCtrl.SetInitialSize((250,-1))
        sizer6.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        titleCtrl = wx.TextCtrl(panel, -1, rprtTitle)
        titleCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.titleHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(titleCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        headingCtrl = wx.TextCtrl(panel, -1, rprtHeading)
        headingCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.headingHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer8.Add(headingCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer8, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            dbTableId_1 = GetSel(lbox11.GetSelections(),list_1)

            panel.SetResult(
                titleCtrl.GetValue(),
                dbTableId_1,
                nbrOfLastDaysCtrl.GetValue(), 
                nbrOfLastHoursCtrl.GetValue(),
                cHtmlCtrl.GetValue(),
                fPathCtrl.GetValue(),
                nameCtrl.GetValue(),
                headingCtrl.GetValue(),
                tenMinutesCtrl.GetValue()
            )



class BarometricReport(eg.ActionClass):

    def __call__(
        self, 
        rprtTitle = '',
        dbTableId_1 = ['Barometric Pressure'],
        nbrOfLastDays = 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = '',
        rprtName = '',
        rprtHeading = '',
        tenMinutes = True
    ):

        def CreateReport(createReportThreadEvent):
            hrs_back = nbrOfLastDays*24 + nbrOfLastHours
            now = datetime.datetime.now()
            dateTimeTo = now.strftime("%Y-%m-%d %H:%M")
            delta = datetime.timedelta(hours = -hrs_back)
            dateTimeFrom = (now + delta).strftime("%Y-%m-%d %H:%M")
    
            rows_1 = {}
            rows = None

            with self.plugin.temp_lock:
                for item in dbTableId_1:
                    rows = self.plugin.LastData(
                        self.plugin.barData_db, 
                        item, 
                        dateTimeFrom
                    )
                    rows_1[item]=rows
    
            CreateBarHtml.CreateBarHtml(
                rprtName, 
                "Barometric Pressure report", 
                fPath, 
                rows_1, 
                "['Column1', 'Pressure', { role: 'style' }]", 
                3,
                rprtTitle,
                rprtHeading,
                tenMinutes
            )
            del rows
            del rows_1
           
            while not createReportThreadEvent.isSet():
                createReportThreadEvent.wait(1.0)
            del createReportThreadEvent
            eg.TriggerEvent(
                rprtName,
                payload = "Barometric report created",
                prefix = 'ClimateDataCalculation'
            )
            item = self.plugin.q.get_nowait()
            del item
            self.plugin.q.task_done()

        reload(CreateBarHtml)
        createReportThreadEvent = Event()
        createReportThread = Thread(
            target=CreateReport,
            args=(createReportThreadEvent,)
        )
        self.plugin.AddToQueue(rprtName)
        createReportThread.start()
        createReportThreadEvent.set()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        rprtTitle = 'EventGhost Barometric Report',
        dbTableId_1 = [''],
        nbrOfLastDays= 0,
        nbrOfLastHours = 24,
        cHtml = True,
        fPath = eg.mainDir+'\Log\HighCharts',
        rprtName = 'Filename',
        rprtHeading = 'Barometric Pressure report',
        tenMinutes = True
        ):

        def GetSel(sel, list):
                val = []
                for i in sel:
                    val.append(list[i])
                return tuple(val)

        panel = eg.ConfigPanel(self)

        # Create dropdowns for dbTableId's 
        list_1 = self.plugin.tablesBarData
        if list_1 <> None:
            pass
        else:
            list_1 = ['Empty']
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.dbReportTableId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        sizer11 = wx.BoxSizer(wx.HORIZONTAL)
        lbox11 = wx.ListBox(
            panel,-1,
            size=wx.Size(150,100),
            style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB|wx.HORIZONTAL
        )
        lbox11.Set(list_1)
        for item in dbTableId_1:
            if item in list_1:
                idx = list_1.index(item)
                lbox11.SetSelection(idx)    
        sizer11.Add(lbox11, 1)
        staticBoxSizer.Add(sizer11, 0, wx.EXPAND|wx.ALL, 15)
        
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastDays 
        nbrOfLastDaysCtrl = panel.SpinIntCtrl(nbrOfLastDays, 0, 365)
        nbrOfLastDaysCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastDays)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(nbrOfLastDaysCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a control for nbrOfLastHours 
        nbrOfLastHoursCtrl = panel.SpinIntCtrl(nbrOfLastHours, 0, 24)
        nbrOfLastHoursCtrl.SetInitialSize((150,-1))
        staticBox = wx.StaticBox(panel, -1, self.plugin.text.nbrOfLastHours)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(nbrOfLastHoursCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
 
        # Create a control for generating the html page 
        tenMinutesCtrl = wx.CheckBox(panel, -1, "")
        tenMinutesCtrl.SetValue(tenMinutes)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.tenMinutes
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(tenMinutesCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        cHtmlCtrl = wx.CheckBox(panel, -1, "")
        cHtmlCtrl.SetValue(cHtml)
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.cHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(cHtmlCtrl, 1, wx.EXPAND)
        
        fPathCtrl = wx.TextCtrl(panel, -1, fPath)
        fPathCtrl.SetInitialSize((300,-1))
        sizer6.Add(fPathCtrl, 1, wx.EXPAND)
        nameCtrl = wx.TextCtrl(panel, -1, rprtName)
        nameCtrl.SetInitialSize((250,-1))
        sizer6.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        titleCtrl = wx.TextCtrl(panel, -1, rprtTitle)
        titleCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.titleHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(titleCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        headingCtrl = wx.TextCtrl(panel, -1, rprtHeading)
        headingCtrl.SetInitialSize((300,-1))
        staticBox = wx.StaticBox(
            panel, -1, self.plugin.text.headingHtml
        )
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer8.Add(headingCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer8, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            dbTableId_1 = GetSel(lbox11.GetSelections(),list_1)

            panel.SetResult(
                titleCtrl.GetValue(),
                dbTableId_1,
                nbrOfLastDaysCtrl.GetValue(), 
                nbrOfLastHoursCtrl.GetValue(),
                cHtmlCtrl.GetValue(),
                fPathCtrl.GetValue(),
                nameCtrl.GetValue(),
                headingCtrl.GetValue(),
                tenMinutesCtrl.GetValue()
            )




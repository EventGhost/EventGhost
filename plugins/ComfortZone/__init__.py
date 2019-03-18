# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
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


import eg

eg.RegisterPlugin(
    name = "ComfortZone",
    author = "krambriw",
    guid = "{DBB1688F-3864-42DD-B32B-F54AEF59AD26}",
    version = "0.1",
    canMultiLoad = True,
    description = "Comfortzone communication through a serial port.",
    help = """
        <center><img src="comfortzone.jpg" /></center>
    """
)

# Copyright (C) 2014
# Walter Kraembring

# Based on the serial plugin

##############################################################################
# Revision history:
#
# 2014-02-23  First version
##############################################################################

class Text:
    port = "Port:"
    baudrate = "Baudrate:"
    temp_diff = "Select allowed temperature differens:"
    raw = "Check to log raw data:"
    comms_up = "Communication with Comfortzone started..."
    alarm_map_normal = "Alarm states in NORMAL"
    comms_back = "Communication with CZ is back"
    comms_lost = "Communication with CZ is lost"
    inverter_alarm = 'Inverter alarm'
    high_pressure_alarm = 'High pressure sensor alarm'
    defrost_sensor_alarm = 'Defrost sensor alarm'
    filter_sensor_alarm = 'Air filter sensor alarm'
    low_temperature_alarm = 'Low room temperature alarm'

class testAlarmsTxt:
    simulateTxt = 'Simulating alarms, please wait for the events to appear...'
    
    

import wx
import threading
import win32event
import win32file
import codecs
import binascii

BAUDRATES = [
    '110', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200',
    '38400', '57600', '115200', '128000', '256000'
]


def MyHexDecoder(input):
    return (binascii.b2a_hex(input).upper(), len(input))


DECODING_FUNCS = [
    codecs.getdecoder(eg.systemEncoding),
    MyHexDecoder,
    codecs.getdecoder("latin1"),
    codecs.getdecoder("utf8"),
    codecs.getdecoder("utf16"),
    codecs.getencoder("string_escape"),
]


class CZSerial(eg.RawReceiverPlugin):
    text = Text

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.serial = None
        self.buffer = ""
        self.AddAction(testAlarms)


    def __start__(
        self,
        port,
        baudrate,
        bytesize,
        parity,
        stopbits,
        handshake,
        generateEvents,
        terminator,
        prefix,
        encodingNum,
        alarm_map,
        tempDiff,
        logRaw       
    ):
        self.test_alarms = ''
        self.test_temp = 0.0
        self.alarm_map = alarm_map
        self.tempDiff = tempDiff
        self.logRaw = logRaw
        self.commsLost = True
        xonxoff = 0
        rtscts = 0
        if handshake == 1:
            xonxoff = 1
        elif handshake == 2:
            rtscts = 1

        try:
            self.serial = eg.SerialPort(
                port,
                baudrate=baudrate,
                bytesize=(5, 6, 7, 8)[bytesize],
                stopbits=(1, 2)[stopbits],
                parity=('N', 'O', 'E')[parity],
                xonxoff=xonxoff,
                rtscts=rtscts,
            )
        except:
            self.serial = None
            raise self.Exceptions.SerialOpenFailed
        self.serial.timeout = 1.0
        self.serial.setRTS()
        if generateEvents:
            self.decoder = DECODING_FUNCS[encodingNum]
            self.terminator = eg.ParseString(
                terminator
            ).decode('string_escape')
            self.info.eventPrefix = prefix
            self.stopEvent = win32event.CreateEvent(None, 1, 0, None)
            self.receiveThread = threading.Thread(
                target=self.ReceiveThread,
                name="SerialThread"
            )
            self.receiveThread.start()
        else:
            self.receiveThread = None


    def __stop__(self):
        if self.serial is not None:
            if self.receiveThread:
                win32event.SetEvent(self.stopEvent)
                self.receiveThread.join(1.0)
            self.serial.close()
            self.serial = None


    def EventDecode(self, str):
        text = self.text
        str = str.split('\t')
        if self.logRaw:
            print str
            print len(str)
        if len(str) >= 44:
            try:
                alarms = str[8]
                if self.test_alarms <> '':
                    alarms = self.test_alarms 
                    print alarms
                    self.test_alarms = ''
                configured_temp = float(str[1])
                if self.test_temp > 0.0:
                    configured_temp = self.test_temp
                    print configured_temp
                    self.test_temp = 0.0
                current_temp = float(str[3].split('E')[0])*10.0
                ref_temperatur = configured_temp - self.tempDiff
                InverterAlarm = alarms[0]
                HighPressureAlarm = alarms[1]
                Not_used = alarms[2]
                DefrosterAlam = alarms[3]
                FilterAlarm = alarms[4]
                
                if InverterAlarm <> self.alarm_map[0]:
                    self.TriggerEvent(text.inverter_alarm)
                if HighPressureAlarm <> self.alarm_map[1]:
                    self.TriggerEvent(text.high_pressure_alarm)
                if DefrosterAlam <> self.alarm_map[3]:
                    self.TriggerEvent(text.defrost_sensor_alarm)
                if FilterAlarm <> self.alarm_map[4]:
                    self.TriggerEvent(text.filter_sensor_alarm)
                if current_temp < ref_temperatur:
                    self.TriggerEvent(text.low_temperature_alarm)
            
                try:
                    eg.scheduler.CancelTask(self.monitor)
                except:
                    self.monitor = None
                    if self.commsLost:
                        self.CommsBack(
                            self.text.comms_back
                        )
                self.monitor = eg.scheduler.AddTask(
                        120.0,
                        self.CommsLost,
                        self.text.comms_lost
                )

            except:
                pass


    def CommsBack(self, myArgument):
        #print repr(myArgument)
        eg.TriggerEvent(repr(myArgument))
        self.commsLost = False


    def CommsLost(self, myArgument):
        #print repr(myArgument)
        eg.TriggerEvent(repr(myArgument))
        self.commsLost = True


    def HandleChar(self, ch):
        self.buffer += ch
        pos = self.buffer.find(self.terminator)
        if pos != -1:
            eventstring = self.buffer[:pos]
            if eventstring:
                self.EventDecode(self.decoder(eventstring)[0])
            self.buffer = self.buffer[pos+len(self.terminator):]


    def ReceiveThread(self):
        from win32event import (
            ResetEvent,
            MsgWaitForMultipleObjects,
            QS_ALLINPUT,
            WAIT_OBJECT_0,
            WAIT_TIMEOUT,
        )
        from win32file import ReadFile, AllocateReadBuffer, GetOverlappedResult
        from win32api import GetLastError

        continueLoop = True
        overlapped = self.serial._overlappedRead
        hComPort = self.serial.hComPort
        hEvent = overlapped.hEvent
        stopEvent = self.stopEvent
        n = 1
        waitingOnRead = False
        buf = AllocateReadBuffer(n)
        print self.text.comms_up
        while continueLoop:
            if not waitingOnRead:
                ResetEvent(hEvent)
                hr, _ = ReadFile(hComPort, buf, overlapped)
                if hr == 997:
                    waitingOnRead = True
                elif hr == 0:
                    pass
                    #n = GetOverlappedResult(hComPort, overlapped, 1)
                    #self.HandleChar(str(buf))
                else:
                    self.PrintError("error")
                    raise

            rc = MsgWaitForMultipleObjects(
                (hEvent, stopEvent),
                0,
                1000,
                QS_ALLINPUT
            )
            if rc == WAIT_OBJECT_0:
                n = GetOverlappedResult(hComPort, overlapped, 1)
                if n:
                    self.HandleChar(str(buf))
                #else:
                #    print "WAIT_OBJECT_0", n, str(buf[:n])
                waitingOnRead = False
            elif rc == WAIT_OBJECT_0+1:
                continueLoop = False
            elif rc == WAIT_TIMEOUT:
                pass
            else:
                self.PrintError("unknown message")


    def Configure(
        self,
        port=0,
        baudrate=38400,
        bytesize=3,
        parity=0,
        stopbits=0,
        handshake=0,
        generateEvents=True,
        terminator="\\r",
        prefix="Comfortzone",
        encodingNum=3,
        alarm_map = '01001',
        tempDiff = 5.0,
        logRaw = False

    ):
        text = self.text
        panel = eg.ConfigPanel()
        portCtrl = panel.SerialPortChoice(port)

        baudrateCtrl = panel.ComboBox(
            str(baudrate),
            BAUDRATES,
            style=wx.CB_DROPDOWN,
            validator=eg.DigitOnlyValidator()
        )

        panel.SetColumnFlags(1, wx.EXPAND)
        portSettingsBox = panel.BoxedGroup(
            "Port settings",
            (text.port, portCtrl),
            (text.baudrate, baudrateCtrl)
        )
        eg.EqualizeWidths(portSettingsBox.GetColumnItems(0))
        eg.EqualizeWidths(portSettingsBox.GetColumnItems(1))
        panel.sizer.Add(
            eg.HBoxSizer(portSettingsBox)
        )

        alarm_mapCtrl = panel.TextCtrl(alarm_map)
        panel.AddLine(text.alarm_map_normal, alarm_mapCtrl)

        tempDiffCtrl = panel.SpinNumCtrl(
            tempDiff,
            # by default, use '.' for decimal point
            decimalChar = '.',
            # by default, use ',' for grouping
            groupChar = ',',
            fractionWidth = 1,
            integerWidth = 2,
            min = 0.1,
            max = 20.0,
            increment = 0.1
        )
        tempDiffCtrl.SetInitialSize((90,-1))
        panel.AddLine(text.temp_diff, tempDiffCtrl)

        logRawCtrl = wx.CheckBox(panel, -1, '')               
        logRawCtrl.SetValue(logRaw)
        panel.AddLine(text.raw, logRawCtrl)

        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
                int(baudrateCtrl.GetValue()),
                bytesize,
                parity,
                stopbits,
                handshake,
                generateEvents,
                terminator,
                prefix,
                encodingNum,
                alarm_mapCtrl.GetValue(),
                tempDiffCtrl.GetValue(),
                logRawCtrl.GetValue()
            )



class testAlarms(eg.ActionClass):
    text = testAlarmsTxt
    
    def __call__(
        self
    ):
        self.plugin.test_alarms = '10010' #normal value '01001'
        self.plugin.test_temp = 50.0
        print self.text.simulateTxt

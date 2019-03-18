# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright (C) 2012 Walter Kraembring <krambriw>.
#
# ALL RIGHTS RESERVED. The development of this software is based on information
# provided by RFXCOM and is protected under Netherlands Copyright Laws and
# Treaties and shall be subject to the exclusive jurisdiction of the Netherlands
# Courts.
# This plugin�s source code and other versions eventually based on it may be
# used exclusively to interface with RFXCOM products only. Any other usage of
# information in this source code is prohibited without express written
# permission from RFXCOM.
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
# Acknowledgements: Part of code and some ideas are based on the serial plugin
#
##############################################################################
#
# Revision history: See readme.txt
#
##############################################################################

import eg, wx
import time, os
from threading import Event, Thread
from codecs import getdecoder

eg.RegisterPlugin(
    name = "RFXtrx",
    author = "krambriw",
    guid = "{72DCE030-68FF-49B9-835D-295D4CF048ED}",
    version = "2.0.2",
    canMultiLoad = True,
    kind = "external",
    description = (
        "RFXtrx communication through a virtual serial port."
        '<br\n><br\n>'
        '<center><img src="rfxtrx.png" /></center>'
    ),
    url = "http://www.eventghost.net/forum",
)



class Text:
    port = "Port:"
    logToFile = "Log events to file"
    debugInfo = "Show debug info"
    macroNames = "Automatic naming of macros"
    dupEvents = "Allow duplicated events"
    set_prefix = "Configure the event prefix"
    use_websockets = "Use Webserver plugin with websocket support (port 1234) " 
    use_tornadoWebsockets = "Use Tornado plugin for websockets " 
    decode_advice = (
        "Please select the required protocols with the RFXmngr application"
    )
    decodeError = "Decoding of message failed: "
    fwVersion = "RFXtrx Firmware Version: "
    rfxtrx = "RFXtrx receiver/transceiver type: "
    rfxtrx_type = "You have a RFXtrx Type "
    rfxtrx_fw = "You have firmware type: "
    messageT = "Wrong command response, your RFXtrx type might not support this "
    messageL = "Wrong message length: "
    unknown_RFY_remote = "Unknown RFY remote"
    no_extended_hardware_present = "No extended hardware present (RFY)"
    rfxtrx_started = "A genuine RFXtrx is detected and started"
    rfxtrx_lost = "Lost connection with the RFXtrx"
    messageDbg = "Debug Info: "
    messageUC = "Message broken and repaired within"
    messageNP = "Message could not be repaired"
    messageUKnwn = "Unknown message: "
    messageWebSocketError = "Websocket error...check that the plugin is added to your configuration "
    messageWebSocketBroadcastError = "Websocket broadcast error...check the websocket configuration "
    disconnecting = "Stopping and disconnecting the RFXtrx device...please wait"
    cleanUpmonitoring = "Cleaning up monitoring tasks..."
    readyStopped = "Plugin successfully stopped"
    threadStopped = "Receiving thread is stopped..."
    dt_threadStopped = "Date & Time thread ended"    
    ka_threadStopped = "Keep Alive thread ended"    
    keyAdded = "Key added to dictionary"
    textBoxName = "Enter a descriptive name for the action"
    textBoxLCdeviceId = "Select the ID of the La Crosse TX5 rain gauge to reset the collected rain data"
    textBoxProtocol = "Select the device protocol to be used"
    textBoxHouseCode = "Select the house code of the device"
    textBoxGroupCode = "Select the group code of the device"
    textBoxDeviceCode = "Select the device code of the device"
    textBoxCommand = "Select the command to send"
    textBoxColor = (
        "If your command is 'Select Color', then also select the color code from below"
    )
    textBoxAddress = "Type/paste the unit address to be used (from 00 00 00 01 to 03 FF FF FF)"
    textBoxDeviceUnit = "Select the unit code of the device"
    textBoxLevel = "Select the dim/bright level"
    textBoxStepSize = "Select the dim step size"
    textBoxStatus = "Select status"
    textBoxMode = "Select mode"
    textBoxTemperature = "Set the temperature"
    textBoxSetPoint = "Set the setpoint"   
    timeInBetween_txt = "Select the time delay between dim level commands"
    timeToWakeUp_txt = "Total snooze time (minutes): "
    timeToSleep_txt = "Total snooze time (minutes): "
    textBoxSystem = "Select the system code to use"
    textChannel = "Check the boxes for the channels to use"
    textBoxDeviceID = "Select the proper ID selections"    
    textBoxPulseTiming = "Set the proper pulse timing (default 350 us)"
    textBoxIdCommands = "Check the boxes for the id and command"   
    textBoxFanSpeed_1 = "Select the desired fan 1 speed"
    textBoxFanSpeed_2 = "Select the desired fan 2 speed"
    textBoxFanSpeed_3 = "Select the desired fan 3 speed"
    beep = "Select to beep on command"
    textBoxFlamePower = "Select the desired flame power"
    textStep_up = "Check the box to dim up "
    txt_signal_back = "Recovered contact with sensor"
    txt_taskObj = "Lost contact with sensor"
    


class CurrentStateData(eg.PersistentData):
    current_state_memory = {}
    sensors_status = {}
    rfxSensors = {}
    dimGradually = {}
    dimStepWise = {}
    cmndSeqNbr_015 = 0
    remote_address_map = {}
    totalRain = {}



class RFXtrx(eg.RawReceiverPlugin):
    text = Text

    def __init__(self):
        self.current_state_memory = CurrentStateData.current_state_memory
        self.sensors_status = CurrentStateData.sensors_status
        self.dimGradually = CurrentStateData.dimGradually
        eg.RawReceiverPlugin.__init__(self)
        self.AddAction(send_AC)
        self.AddAction(DimGradually_AC)
        self.AddAction(DimStepWise_AC)
        self.AddAction(GoodMorning_AC)
        self.AddAction(GoodNight_AC)
        self.AddAction(send_Kambrook)
        self.AddAction(send_ARC)
        self.AddAction(send_Waveman)
        self.AddAction(send_Chacon_EMW200)
        self.AddAction(send_IMPULS)
        self.AddAction(send_RisingSun)
        self.AddAction(send_ByeByeStandBy)
        self.AddAction(send_Philips_SBC)
        self.AddAction(send_Energenie)
        self.AddAction(send_COCO_GDR2_2000R)
        self.AddAction(send_HQ_COCO_20)
        self.AddAction(send_Energenie_5g)
        self.AddAction(send_Siemens_Lightwave_RF)
        self.AddAction(send_Siemens_SF01)
        self.AddAction(send_LucciAir)
        self.AddAction(send_Westinghouse_7226640)
        self.AddAction(send_SEAV_TXS4)
        self.AddAction(send_PT2262)
        self.AddAction(send_EMW100_GAO_Everflourish)
        self.AddAction(send_Conrad_RSL2)
        self.AddAction(send_Cotech)
        self.AddAction(send_MDREMOTE_LED)
        self.AddAction(send_Aoke_Relay)
        self.AddAction(send_IT_Intertek)
        self.AddAction(send_Legrand_CAD)
        self.AddAction(send_RGB_TRC02)
        self.AddAction(send_RGB_TRC02_2)
        self.AddAction(send_RGB432W)
        self.AddAction(send_Eurodomest)
        self.AddAction(send_Avantek)
        self.AddAction(send_Blyss_Thomson)
        self.AddAction(send_Byron_SX)
        self.AddAction(send_Byron_MP001)
        self.AddAction(send_SelectPlus)
        self.AddAction(send_Envivo)
        self.AddAction(send_ELRO_AB400D)
        self.AddAction(send_Livolo)
        self.AddAction(send_Livolo_Appliance)
        self.AddAction(send_X10)
        self.AddAction(send_Koppla)
        self.AddAction(send_Harrison_Curtain)
        self.AddAction(send_RollerTrol)
        self.AddAction(send_Confexx)
        self.AddAction(send_Screenline)
        self.AddAction(send_A_OK)
        self.AddAction(send_Raex)
        self.AddAction(send_Media_Mount)
        self.AddAction(send_DC_Forest)
        self.AddAction(send_Chamberlain)
        self.AddAction(send_Sunpery)
        self.AddAction(send_Dolat_DLM_1_Topstar)
        self.AddAction(send_ASP)
        self.AddAction(send_RFY)
        self.AddAction(send_RFY_ext)
        self.AddAction(send_RFY_Venetian)
        self.AddAction(send_ASA)
        self.AddAction(send_KeeLoq_Classic)
        self.AddAction(send_x10_security_remote)
        self.AddAction(send_KD101_smoke_detector)
        self.AddAction(send_SA30_smoke_detector)
        self.AddAction(send_RM174RF_smoke_detector)
        self.AddAction(send_Meiantech)
        self.AddAction(send_Digimax)
        self.AddAction(send_Thermostat_HE105)
        self.AddAction(send_Thermostat_RTS10)
        self.AddAction(send_Smartwares_radiator_valve)
        self.AddAction(send_Mertik_G6R_H4T1)
        self.AddAction(send_Mertik_G6R_H4TB)
        self.AddAction(send_Mertik_G6R_H4TD)
        self.AddAction(send_Mertik_G6R_H4S)
        self.AddAction(send_MCZ)
        self.AddAction(send_ATI_RemoteWonder)
        self.AddAction(send_ATI_RemoteWonderPlus)
        self.AddAction(send_Medion_Remote)
        self.AddAction(send_Home_Confort)
        self.AddAction(send_X10_PC_Remote)
        self.AddAction(WebRefresh)
        self.AddAction(remote_address_Mapper)
        self.AddAction(ClearSensorsStatus)
        self.AddAction(ResetCurrentStatus)
        self.AddAction(ResetLaCrosseTX5_data)
        self.AddAction(disable_unDecoded)
        self.AddAction(enable_unDecoded)
        self.AddAction(max_outPower)
        self.AddAction(normal_outPower)
        self.AddAction(decode_Test_Message)


    def __start__(
        self,
        port = 0,
        bLogToFile = False,
        bDebug = False,
        b01 = True,
        b02 = True,
        b03 = True,
        b04 = True,
        b05 = True,
        b06 = True,
        b07 = True,
        b08 = True,
        b09 = True,
        b0a = True,
        b0b = True,
        b0c = True,
        b0d = True,
        b0e = True,
        b0f = True,
        mMacroNames = True,
        bDupEvents = False,
        websocket_port_nbr = 1234,
        use_websockets = False,
        b10 = True,
        use_tornadoWebsockets = False,
        prefix = 'RFXtrx'
    ):
        self.init = True
        self.prefix= prefix
        self.fwVer = 54
        self.bLogToFile = bLogToFile
        self.bDebug = bDebug
        self.deviceCheck = False
        self.sensorLostTimeOut = 600.0

        self.decode_040_mem = {}
        self.decode_042_mem = {}
        self.decode_04E_mem = {}
        self.decode_04F_mem = {}
        self.decode_050_mem = {}
        self.decode_051_mem = {}
        self.decode_052_mem = {}
        self.decode_054_mem = {}
        self.decode_055_mem = {}
        self.decode_056_mem = {}
        self.decode_057_mem = {}
        self.decode_058_mem = {}
        self.decode_059_mem = {}
        self.decode_05A_1_mem = {}
        self.decode_05A_2_mem = {}
        self.decode_05B_mem = {}
        self.decode_05C_mem = {}
        self.decode_060_01_mem = {}
        self.decode_060_02_mem = {}
        self.decode_070_mem = {}
        self.decode_071_mem = {}
        self.decode_010_mem = {}
        self.decode_011_mem = {}
        self.decode_013_mem = {}
        self.decode_014_00_mem = {}
        self.decode_014_01_mem = {}
        self.decode_014_02_mem = {}
        self.decode_014_03_mem = {}
        self.decode_014_06_mem = {}
        self.decode_014_07_mem = {}
        self.decode_014_0D_mem = {}
        self.decode_014_0F_mem = {}
        self.decode_015_mem = {}
        self.decode_016_mem = {}
        self.decode_018_019_mem = {}
        self.decode_020_mem = {}
        self.decode_021_mem = {}
        
        self.monitor_040_mem = {}
        self.monitor_042_mem = {}
        self.monitor_04E_mem = {}
        self.monitor_04F_mem = {}
        self.monitor_050_mem = {}
        self.monitor_051_mem = {}
        self.monitor_052_mem = {}
        self.monitor_054_mem = {}
        self.monitor_055_mem = {}
        self.monitor_056_mem = {}
        self.monitor_057_mem = {}
        self.monitor_058_mem = {}
        self.monitor_059_mem = {}
        self.monitor_05A_1_mem = {}
        self.monitor_05A_2_mem = {}
        self.monitor_05B_mem = {}
        self.monitor_05C_mem = {}
        self.monitor_060_01_mem = {}
        self.monitor_060_02_mem = {}
        self.monitor_070_mem = {}
        self.monitor_071_mem = {}
        self.monitor_020_mem = {}

        self.usage_05A_2 = '0.00'

        self.mMacroNames = mMacroNames
        self.bDupEvents = bDupEvents
        self.use_websockets = use_websockets
        self.websocket_port_nbr = str(websocket_port_nbr)
        self.use_tornadoWebsockets = use_tornadoWebsockets
        self.rfxSensors = CurrentStateData.rfxSensors
        self.tmpMessage = ''
        self.tmpMilliSec = 0
        self.flipCount = {}
        self.flCount_prev = {}
        self.totalRain = CurrentStateData.totalRain
        self.pmh = None
        self.interfaceMode = []
                 
        self.keepAliveThreadEvent = Event()
        self.remain = 0.0
        keepAliveThread = Thread(
            target=self.keep_Alive,
            args=(self.keepAliveThreadEvent,)
        )
        keepAliveThread.start()

        self.dateTimeThreadEvent = Event()
        dateTimeThread = Thread(
            target=self.date_Time,
            args=(self.dateTimeThreadEvent,)
        )
        dateTimeThread.start()

        try:
            self.serial = eg.SerialPort(
                port=port,
                baudrate=38400,
                bytesize=8,
                stopbits=1,
                parity='N',
                xonxoff=0,
                rtscts=0,
            )
        except:
            self.serial = None
            raise self.Exceptions.SerialOpenFailed
        self.serial.timeout = 0.01
        self.serial.setRTS()

        #Reset connection
        reset_str = "0D 00 00 00 00 00 00 00 00 00 00 00 00 00"
        self.WriteMsg(reset_str, '', '')        
        eg.Wait(2.0)
        
        #Flush the COM port receive buffer
        self.serial.flushInput

        #Get device status
        get_status_str = "0D 00 00 01 02 00 00 00 00 00 00 00 00 00"
        self.WriteMsg(get_status_str, '', '')        

        #Check valid RFXCOM device
        chk_valid_device = "0D 00 00 02 07 00 00 00 00 00 00 00 00 00"
        self.WriteMsg(chk_valid_device, '', '')        

        #Start the communication thread
        self.decoder = getdecoder(eg.systemEncoding)
        self.info.eventPrefix = self.prefix
        self.finished = Event()
        self.receiveThread = Thread(
            target=self.ReceiveThread,
            name="RFXtrxThread"
        )
        self.receiveThread.start()


    def __stop__(self):
        print self.text.disconnecting
        self.dateTimeThreadEvent.set()
        self.keepAliveThreadEvent.set()
        if self.serial is not None:
            if self.receiveThread:
                self.receiveThread.join(1.0)
                self.finished.set()
            time.sleep(0.1)
            try:
                self.serial.close()
            except:
                pass
            self.serial = None

        try:
            eg.scheduler.CancelTask(self.pmh)
        except:
            pass

        print self.text.cleanUpmonitoring
        for i in self.monitor_040_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_040_mem[i])
            except:
                pass
        for i in self.monitor_042_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_042_mem[i])
            except:
                pass
        for i in self.monitor_04E_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_04E_mem[i])
            except:
                pass
        for i in self.monitor_04F_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_04F_mem[i])
            except:
                pass
        for i in self.monitor_050_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_050_mem[i])
            except:
                pass
        for i in self.monitor_051_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_051_mem[i])
            except:
                pass
        for i in self.monitor_052_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_052_mem[i])
            except:
                pass
        for i in self.monitor_054_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_054_mem[i])
            except:
                pass
        for i in self.monitor_055_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_055_mem[i])
            except:
                pass
        for i in self.monitor_056_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_056_mem[i])
            except:
                pass
        for i in self.monitor_057_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_057_mem[i])
            except:
                pass
        for i in self.monitor_058_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_058_mem[i])
            except:
                pass
        for i in self.monitor_059_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_059_mem[i])
            except:
                pass
        for i in self.monitor_05A_1_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_05A_1_mem[i])
            except:
                pass
        for i in self.monitor_05A_2_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_05A_2_mem[i])
            except:
                pass
        for i in self.monitor_05B_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_05B_mem[i])
            except:
                pass
        for i in self.monitor_05C_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_05C_mem[i])
            except:
                pass
        for i in self.monitor_070_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_070_mem[i])
            except:
                pass
        for i in self.monitor_071_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_071_mem[i])
            except:
                pass
        for i in self.monitor_020_mem:
            try:
                eg.scheduler.CancelTask(self.monitor_020_mem[i])
            except:
                pass
        eg.Wait(self.remain + 0.5)
        print self.text.readyStopped
        
                
    def ClearTempMessage(self):
        eg.PrintError (
            self.text.messageNP+
            ' '+
            self.tmpMessage
        )
        self.tmpMessage = ''
        self.tmpMilliSec = 0


    def CancelTask(self, handle):
        try:
            eg.scheduler.CancelTask(handle)
        except:
            pass


    def MilliSeconds(self):
        return int(round(time.time() * 1000))

        
    def PartialMessageHandler(self, data): #Uncompleted message arrives
        #Start time measuring
        if not self.tmpMilliSec > 0:
            self.tmpMilliSec = self.MilliSeconds()

        #Cancel resetting task if already scheduled
        self.CancelTask(self.pmh)

        #Schedule the new resetting task
        self.pmh = eg.scheduler.AddTask(0.5, self.ClearTempMessage)

        #Add the received data to the temporary storage
        self.tmpMessage += data
        if self.bDebug:
            print self.tmpMessage

        #Check length and if it has become completed
        #If not, just wait for the remainer
        messageL = int(self.tmpMessage[0:2], 16)

        if len(self.tmpMessage) == (messageL+1)*2:
            #Cancel scheduled task and clear the temporary storage
            self.CancelTask(self.pmh)
            #Forward the repaired message for normal processing
            self.HandleChar(self.tmpMessage)

            if self.bDebug:
                timeToRepair = self.MilliSeconds() - self.tmpMilliSec
                eg.PrintError (
                    self.text.messageUC+
                    ' '+
                    str(timeToRepair)+
                    ' ms'+
                    ' '+
                    self.tmpMessage
                )
            self.tmpMessage = ''
            self.tmpMilliSec = 0


    def ReceiveThread(self):
        out = ''
        while not self.finished.isSet():
            time.sleep(0.005) #Release CPU
    	    while self.serial.inWaiting() > 0 and not self.hold:
                self.finished.wait(0.01)
    	        buf = self.serial.read(1)
    	        if len(str(out))==0:
                    pl = int('0x'+str(buf.encode('hex')), 0)
                    out += buf
                    out += self.serial.read(pl)
                    data = str(out.encode('hex'))
                    if pl>3 and len(str(out))==pl+1:
                        if self.bDebug:
                            print "Debug Info: ", data
                        self.HandleChar(data)
                    else:
                        self.PartialMessageHandler(data)
                    out = ''
        print self.text.threadStopped


    def date_Time(self,dateTimeThreadEvent):
        counter = int(time.strftime("%S", time.localtime()))
        while not dateTimeThreadEvent.isSet():
            if counter == 60:
                self.DateAndTimeInfo()
                counter = 1
            else:
                counter += 1
            dateTimeThreadEvent.wait(1.0)
        print self.text.dt_threadStopped


    def keep_Alive(self,keepAliveThreadEvent): # Keep Alive Loop
        counter = 0
        while not keepAliveThreadEvent.isSet():
            if counter == 60:
                #self.KeepAlive()
                counter = 0
            else:
                counter += 1
            keepAliveThreadEvent.wait(1.0)
        print self.text.ka_threadStopped


    def DateAndTimeInfo(self):
        if self.use_websockets or self.use_tornadoWebsockets:
            currDate_Time = str(
                time.strftime(
                    "%w %Y-%m-%d %H:%M",
                    time.localtime()
                )
            )
            msg = "currDate_Time."+currDate_Time
            self.BroadcastMessage(msg)
        self.deviceCheck = True
        chk_valid_device = "0D 00 00 01 02 00 00 00 00 00 00 00 00 00"
        self.WriteMsg(chk_valid_device, '', '')        

        
    def KeepAlive(self):
        if self.use_websockets or self.use_tornadoWebsockets:
            msg = "KeepAlive"
            self.BroadcastMessage(msg)


    def StatusRefresh(self):
        if self.use_websockets or self.use_tornadoWebsockets:
            if len(self.current_state_memory) > 0:
                for i in self.current_state_memory:
                    msg = self.current_state_memory[i]
                    self.BroadcastMessage(msg)
                    time.sleep(0.01)
            if len(self.sensors_status) > 0:
                for i in self.sensors_status:
                    msg = self.sensors_status[i]
                    self.BroadcastMessage(msg)
                    time.sleep(0.01)


    def SavePersistent(self, msg, m_key):
        #Check if the message comes from a remote that shall be re-mapped        
        m_k = m_key.split(' ')
        if len(m_k) == 3:
            m = msg.split(' ')
            try:
                adr_new = CurrentStateData.remote_address_map[m_k[1]]
                m_key = m_k[0]+' '+adr_new+' '+m_k[2]
                msg = (
                    m[0]+' '+m[1]+' '+m[2]+' '+adr_new+' '+
                    m[4]+' '+m[5]+' '+m[6]+' '+m[7]+' '+
                    m[8]+' '+m[9]+' '+m[10]+' '+m[11]+' '+
                    m[12]+' '+m[13]
                )
            except KeyError:
                pass
        
        #Make status data persistent if it has changed
        try:
            if msg != self.current_state_memory[m_key]:
                self.current_state_memory[m_key] = msg
                self.BroadcastMessage(msg)
            elif self.bDupEvents:
                self.BroadcastMessage(msg)
        except KeyError:
            if self.bDebug:
                print self.text.keyAdded
            self.current_state_memory[m_key] = msg
            self.BroadcastMessage(msg)

       
    def BroadcastMessage(self, msg):
        if self.use_websockets:
            try:
                p = eg.plugins.Webserver.BroadcastMessage(
                    msg.encode('utf-8'),
                    False
                )
                if p<>None:
                    print self.text.messageWebSocketBroadcastError
            except:
                print self.text.messageWebSocketError
                time.sleep(1.0)

        if self.use_tornadoWebsockets:
            try:
                p = eg.plugins.Tornado.BroadcastMessage(
                    msg.encode('utf-8'),
                    True
                )
                if p<>None:
                    print self.text.messageWebSocketBroadcastError
            except:
                print self.text.messageWebSocketError
                time.sleep(1.0)


    def HandleChar(self, ch):
        msg = []
        tmp = ''

        for i in ch:
            tmp+=i
            if len(tmp) == 2:
                msg.append(tmp)
                tmp=''
       
        try:
            if len(msg)-1 == int(msg[0], 16) and msg[0] <> 'FF':
                if msg[0]== '09' and msg[1]== '40':
                    self.decode_040(msg)
                    return
                if msg[0]== '08' and msg[1]== '42':
                    self.decode_042(msg)
                    return
                if msg[0]== '0a' and msg[1]== '4e':
                    self.decode_04E(msg)
                    return
                if msg[0]== '0a' and msg[1]== '4f':
                    self.decode_04F(msg)
                    return
                if msg[0]== '08' and msg[1]== '50':
                    self.decode_050(msg)
                    return
                if msg[0]== '08' and msg[1]== '51':
                    self.decode_051(msg)
                    return
                if msg[0]== '0a' and msg[1]== '52':
                    self.decode_052(msg)
                    return
                if msg[0]== '0d' and msg[1]== '54':
                    self.decode_054(msg)
                    return
                if msg[0]== '0b' and msg[1]== '55':
                    self.decode_055(msg)
                    return
                if msg[0]== '10' and msg[1]== '56':
                    self.decode_056(msg)
                    return
                if msg[0]== '09' and msg[1]== '57':
                    self.decode_057(msg)
                    return
                if msg[0]== '0d' and msg[1]== '58':
                    self.decode_058(msg)
                    return
                if msg[0]== '0d' and msg[1]== '59':
                    self.decode_059(msg)
                    return
                if msg[0]== '11' and msg[1]== '5a' and msg[2]== '01':
                    self.decode_05A_1(msg)
                    return
                if msg[0]== '11' and msg[1]== '5a' and msg[2]== '02':
                    self.decode_05A_2(msg)
                    return
                if msg[0]== '13' and msg[1]== '5b':
                    self.decode_05B(msg)
                    return
                if msg[0]== '0f' and msg[1]== '5c':
                    self.decode_05C(msg)
                    return
                if msg[0]== '15' and msg[1]== '60' and msg[2]== '01':
                    self.decode_060_01(msg)
                    return
                if msg[0]== '11' and msg[1]== '60' and msg[2]== '02':
                    self.decode_060_02(msg)
                    return
                if msg[0]== '07' and msg[1]== '70':
                    self.decode_070(msg)
                    return
                if msg[0]== '0a' and msg[1]== '71':
                    self.decode_071(msg)
                    return
                if msg[0]== '07' and msg[1]== '10':
                    self.decode_010(msg)
                    return
                if msg[0]== '0b' and msg[1]== '11':
                    self.decode_011(msg)
                    return
                if msg[0]== '09' and msg[1]== '13':
                    self.decode_013(msg)
                    return
                if msg[0]== '0a' and msg[1]== '14' and msg[2]== '00':
                    self.decode_014_00(msg)
                    return
                if msg[0]== '0a' and msg[1]== '14' and msg[2]== '01':
                    self.decode_014_01(msg)
                    return
                if msg[0]== '0a' and msg[1]== '14' and msg[2]== '02':
                    self.decode_014_02(msg)
                    return
                if msg[0]== '0a' and msg[1]== '14' and msg[2]== '04':
                    self.decode_014_02(msg)
                    return
                if msg[0]== '0a' and msg[1]== '14' and msg[2]== '11':
                    self.decode_014_02(msg)
                    return
                if msg[0]== '0a' and msg[1]== '14' and msg[2]== '03':
                    self.decode_014_03(msg)
                    return
                if msg[0]== '0a' and msg[1]== '14' and msg[2]== '06':
                    self.decode_014_06(msg)
                    return
                if msg[0]== '0a' and msg[1]== '14' and msg[2]== '07':
                    self.decode_014_07(msg)
                    return
                if msg[0]== '0a' and msg[1]== '14' and msg[2]== '0d':
                    self.decode_014_0d(msg)
                    return
                if msg[0]== '0b' and msg[1]== '15':
                    self.decode_015(msg)
                    return
                if msg[0]== '07' and msg[1]== '16':
                    self.decode_016(msg)
                    return
                if msg[0]== '07' and msg[1]== '18':
                    self.decode_018(msg)
                    return
                if msg[0]== '09' and msg[1]== '19' and int(msg[2],16)==11:
                    self.decode_019_B(msg)
                    return
                if msg[0]== '09' and msg[1]== '19' and int(msg[2])>=8:
                    self.decode_019_8(msg)
                    return
                if msg[0]== '09' and msg[1]== '19' and int(msg[2])>=6:
                    self.decode_019_6(msg)
                    return
                if msg[0]== '09' and msg[1]== '19' and int(msg[2])>=2:
                    self.decode_019_2(msg)
                    return
                if msg[0]== '09' and msg[1]== '19' and int(msg[2])>=0:
                    self.decode_019(msg)
                    return
                if msg[0]== '08' and msg[1]== '20':
                    self.decode_020(msg)
                    return
                if msg[0]== '1c' and msg[1]== '21':
                    self.decode_021(msg)
                    return
                if msg[0]== '06' and msg[1]== '30' and msg[2]<> '04':
                    self.decode_030_0(msg)
                    return
                if msg[0]== '06' and msg[1]== '30' and msg[2]== '04':
                    self.decode_030_1(msg)
                    return
                if msg[0]== '0d' and msg[1]== '01' and msg[2]== '00':
                    self.decode_00d(msg)
                    return
                if msg[0]== '0d' and msg[1]== '01' and msg[2]== '01':
                    self.decode_01d(msg)
                    return
                if msg[0]== '0d' and msg[1]== '01' and msg[2]== '02':
                    self.decode_02d(msg)
                    return
                if msg[0]== '0d' and msg[1]== '01' and msg[2]== '03':
                    self.decode_03d(msg)
                    return
                if msg[0]== '0d' and msg[1]== '01' and msg[2]== '04':
                    self.decode_04d(msg)
                    return
                if msg[0]== '0d' and msg[1]== '01' and msg[2]== 'ff':
                    self.decode_ff(msg)
                    return
                if msg[0]== '14' and msg[1]== '01' and msg[2]== '00':
                    self.decode_14_00(msg)
                    return
                if msg[0]== '14' and msg[1]== '01' and msg[2]== '01':
                    self.decode_01d(msg)
                    return
                if msg[0]== '14' and msg[1]== '01' and msg[2]== '02':
                    self.decode_02d(msg)
                    return
                if msg[0]== '14' and msg[1]== '01' and msg[2]== '03':
                    self.decode_03d(msg)
                    return
                if msg[0]== '14' and msg[1]== '01' and msg[2]== '04':
                    self.decode_04d(msg)
                    return
                if msg[0]== '14' and msg[1]== '01' and msg[2]== 'ff':
                    self.decode_ff(msg)
                    return
                if msg[0]== '14' and msg[1]== '01' and msg[2]== '07':
                    self.decode_14_07(msg)
                    return
                if msg[1]== '01' and msg[2]== 'FF':
                    self.decode_000(msg)
                    return
                if msg[0]== '04' and msg[1]== '02':
                    self.decode_002(msg)
                    return
                if msg[1]== '03':
                    self.decode_003(msg)
                    return
   
                if self.bDebug:
                    eg.PrintError(self.text.messageUKnwn + str(msg))
                    #self.TriggerEvent(self.text.messageUKnwn + str(msg))
            else:
                if msg[0] <> 'FF':
                    eg.PrintError(self.text.messageL + str(msg))
        except:
            pass    


    def replaceFunc(self, data):
        data = data.strip()
        if data == "CR":
            return chr(13)
        elif data == "LF":
            return chr(10)
        else:
            return None


    def hextobin(self, h):
      return bin(int(h, 16))[2:].zfill(len(h) * 4)

        
    def WriteMsg(self, data, w_msg, w_key):
#        try:
#            if self.bDebug:
#                print self.text.messageDbg, data
#            data = data.replace(' ', '')
#            data = eg.ParseString(data, self.replaceFunc)
#            data = data.decode('hex')
#            self.hold = True
#            self.serial.write(str(data))
#            eg.Wait(0.01)
#            self.hold = False
#            if (
#               (self.use_websockets or self.use_tornadoWebsockets) and
#               w_msg <> '' and
#               w_key <> ''
#            ):
#                self.SavePersistent(w_msg, w_key)
#        except:
#            self.TriggerEvent(self.text.rfxtrx_lost)
        if self.bDebug:
            print self.text.messageDbg, data
        data = data.replace(' ', '')
        data = eg.ParseString(data, self.replaceFunc)
        data = data.decode('hex')
        if self.serial:
            self.hold = True
            self.serial.write(str(data))
            eg.Wait(0.01)
            self.hold = False
        if (
           (self.use_websockets or self.use_tornadoWebsockets) and
           w_msg <> '' and
           w_key <> ''
        ):
            self.SavePersistent(w_msg, w_key)
            

    def WriteRemoteKey(self, data):
        if self.bDebug:
            print self.text.messageDbg, data
        data = data.replace(' ', '')
        data = eg.ParseString(data, self.replaceFunc)
        data = data.decode('hex')
        self.hold = True
        self.serial.write(str(data))
        eg.Wait(0.01)
        self.hold = False


    def LogToFile(self, s):
        timeStamp = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        logStr = timeStamp+"\t"+s+"<br\n>"
        fileHandle = None
        progData = eg.configDir + '\plugins\RFXtrx'

        if (
            not os.path.exists(progData)
            and not os.path.isdir(progData)
        ):
            os.makedirs(progData)

        fileHandle = open (
            progData+'/'+
            self.name+'.html', 'a'
        )
        fileHandle.write ( logStr )
        fileHandle.close ()


    def sensorLost(self, myArgument):
        eg.TriggerEvent(repr(myArgument))
        lc = myArgument.split(':')[3].split(' ')[1]
        try:
            del self.sensors_status[lc]
        except:
            pass
        try:
            self.sensors_status[lc] = myArgument
        except:
            pass

        if self.use_websockets or self.use_tornadoWebsockets:
            self.BroadcastMessage(myArgument)
 
 
    def sensorBack(self, myArgument):
        eg.TriggerEvent(repr(myArgument))
        bc = myArgument.split(':')[3].split(' ')[1]
        try:
            del self.sensors_status[bc]
        except:
            pass
        try:
            self.sensors_status[bc] = myArgument
        except:
            pass
        if self.use_websockets or self.use_tornadoWebsockets:
            self.BroadcastMessage(myArgument)
 
 
    def eventMonitor(self, monitored, decoded, base, timeout):
        try:
            eg.scheduler.CancelTask(monitored)
        except:
            if decoded <> None:
                self.sensorBack(
                    self.text.txt_signal_back+': '+base 
                )
        monitored = eg.scheduler.AddTask(
                timeout,
                self.sensorLost,
                self.text.txt_taskObj+': '+base
        )
        return monitored
       

    def eventTrigger(self, decoded, base, pload):
        msg = str(base)+' : '+str(pload)
        try:
            if str(decoded)[:-2] <> pload[:-2] or self.bDupEvents:
                self.TriggerEvent(str(base), payload = str(pload))
                if self.bLogToFile:
                    self.LogToFile(msg)
                if self.use_websockets or self.use_tornadoWebsockets:
                    self.SavePersistent(msg, str(base))
        except:
            self.TriggerEvent(str(base), payload = str(pload))
            if self.bLogToFile:
                self.LogToFile(msg)
    

    def eventTrigger2(self, decoded, base, pload, value, m_key):
        msg = str(base)+' : '+str(pload)
        try:
            if str(decoded)[:-2] <> value[:-2] or self.bDupEvents:
                self.TriggerEvent(str(base), payload = str(pload))
                if self.bLogToFile:
                    self.LogToFile(msg)
                if self.use_websockets or self.use_tornadoWebsockets:
                    self.SavePersistent(msg, m_key)
        except:
            self.TriggerEvent(str(base), payload = str(pload))
            if self.bLogToFile:
                self.LogToFile(msg)


    def eventTrigger3(self, decoded, base, pload, value, m_key):
        msg = str(base)+' : '+str(pload)
        try:
            if decoded <> value or self.bDupEvents:
                self.TriggerEvent(str(base), payload = str(pload))
                if self.bLogToFile:
                    self.LogToFile(msg)
                if self.use_websockets or self.use_tornadoWebsockets:
                    self.SavePersistent(msg, m_key)
        except:
            self.TriggerEvent(str(base), payload = str(pload))
            if self.bLogToFile:
                self.LogToFile(msg)


    def eventRemote(self, base, pload):
        self.TriggerEvent(str(base), payload = str(pload))


    def GetMacroIndex(self, label, name, my_macro_indx):
        if not self.mMacroNames:
            return None
        if my_macro_indx == None:
            try:
                for index, m_name in enumerate(
                    eg.document.__dict__['root'].childs
                ):
                    if(
                        m_name.name.find('<') <> -1
                        and
                        m_name.name.find('>') <> -1
                    ):
                        my_macro_indx = index
                        break
            except:
                pass
            try:
                for index, m_name in enumerate(
                    eg.document.__dict__['root'].childs
                ):
                    if m_name.name == 'RFXtrx: '+label+': '+name:
                        my_macro_indx = index
                        break
            except:
                return my_macro_indx
        else:
            for index, m_name in enumerate(
                eg.document.__dict__['root'].childs
            ):
                if m_name.name == 'RFXtrx: '+label+': '+name:
                    my_macro_indx = index
        return my_macro_indx


    def SetMacroName(self, label, name, macro_indx):
        if macro_indx <> None and self.mMacroNames:
            new_name = (
                'RFXtrx: '
                +label
                +': '
                +name
            )
            eg.document.__dict__['root'].childs[macro_indx].name = new_name
            eg.document.__dict__['root'].childs[macro_indx].Refresh()


    def decode_000(self, msg):
        if msg[2]=='FF':
            eg.PrintError(self.text.messageT + str(msg[4]))


    def decode_14_00(self, msg):
        if not self.deviceCheck and self.init:
            self.init = False
            self.interfaceMode = msg
            print 'Interface mode: ', msg
            receiver_transceiver_types = {
                '50':'310MHz',
                '51':'315MHz',
                '52':'433.92MHz receiver only',
                '53':'433.92MHz transceiver',
                '55':'868.00MHz',
                '56':'868.00MHz FSK',
                '57':'868.30MHz',
                '58':'868.30MHz FSK',
                '59':'868.35MHz',
                '5A':'868.35MHz FSK',
                '5B':'868.95MHz'
            }
            receiver_transceiver_fw = {
                '00':'Type1 RFXrec receive only firmware',
                '01':'Type1',
                '02':'Type2',
                '03':'Ext',
                '04':'Ext2'
            }
            try:
                print(self.text.rfxtrx+str(receiver_transceiver_types[msg[5]]))
                self.fwVer = int(msg[6], 16)+1000
                print self.text.fwVersion+str(self.fwVer)
                fwType = receiver_transceiver_fw[msg[14]]
                print self.text.rfxtrx_fw + fwType
            except:
                eg.PrintError(self.text.decodeError + str(msg))
        else:
            self.deviceCheck = False
            if msg[0] == '14' and msg[1] == '01':
                pass
            else:
                self.TriggerEvent(self.text.rfxtrx_lost)


    def decode_00d(self, msg):
        if not self.deviceCheck and self.init:
            self.init = False
            self.interfaceMode = msg
            print 'Interface mode: ', msg
            receiver_transceiver_types = {
                '50':'310MHz',
                '51':'315MHz',
                '52':'433.92MHz receiver only',
                '53':'433.92MHz transceiver',
                '55':'868.00MHz',
                '56':'868.00MHz FSK',
                '57':'868.30MHz',
                '58':'868.30MHz FSK',
                '59':'868.35MHz',
                '5A':'868.35MHz FSK',
                '5B':'868.95MHz'
            }
            try:
                print(self.text.fwVersion+str(int(msg[6], 16)))
                self.fwVer = int(msg[6], 16)
                print(self.text.rfxtrx+str(receiver_transceiver_types[msg[5]]))
                if self.fwVer < 163:
                    print self.text.rfxtrx_type + "1"
                if self.fwVer >= 163 and self.fwVer < 225:
                    print self.text.rfxtrx_type + "2"
                if self.fwVer >= 225:
                    print self.text.rfxtrx_type + "433E"
            except:
                eg.PrintError(self.text.decodeError + str(msg))
        else:
            self.deviceCheck = False
            ml = len(msg)-1
            if hex(ml).replace('x','') == msg[0]:
                pass
            else:
                self.TriggerEvent(self.text.rfxtrx_lost)


    def decode_01d(self, msg):
        eg.PrintError(self.text.unknown_RFY_remote)


    def decode_02d(self, msg):
        eg.PrintError(self.text.no_extended_hardware_present)


    def decode_ff(self, msg):
        eg.PrintNotice("RFXtrx: Please, flash the latest firmware")


    def decode_14_07(self, msg):
        
        def cprMsg(msg):
            cpr = ''
            validRFXCOM = False
            try:
                for i in range (5,len(msg)): 
                    cpr += chr(int((msg[i]), 16))
                print cpr + '.', self.text.rfxtrx_started
                if cpr == "Copyright RFXCOM":
                    validRFXCOM = True
            except:
                validRFXCOM = False
            return validRFXCOM           


        validRFXCOM = False
        validRFXCOM = cprMsg(msg)

        if not validRFXCOM:
            eg.PrintNotice(
                "RFXtrx: Genuin RFXtrx device verification failed!"
            )
            #self.__stop__()
         

    def decode_03d(self, msg):
        log = (
            'RFY remote location: '+str(int(msg[5], 16))+
            ' ID1: '+str(msg[6])+
            ' ID2: '+str(msg[7])+
            ' ID3: '+str(msg[8])+
            ' Unit number: '+str(msg[9])
        )

        if(
            str(msg[6]) == '00' and
            str(msg[7]) == '00' and
            str(msg[8]) == '00' and
            str(msg[9]) == '00'
        ):
            log = (
                'RFY remote location: '+str(int(msg[5], 16))+
                ' is empty '
            )

        print log
        

    def decode_04d(self, msg):
        log = (
            'ASA remote location: '+str(int(msg[5], 16))+
            ' ID1: '+str(msg[6])+
            ' ID2: '+str(msg[7])+
            ' ID3: '+str(msg[8])+
            ' Unit number: '+str(msg[9])
        )

        if(
            str(msg[6]) == '00' and
            str(msg[7]) == '00' and
            str(msg[8]) == '00' and
            str(msg[9]) == '00'
        ):
            log = (
                'ASA remote location: '+str(int(msg[5], 16))+
                ' is empty '
            )

        print log
        

    def decode_002(self, msg):
        if msg[0]=='04' and msg[1]=='02':
            if msg[2]=='00' or msg[2]=='01': 
                pass #message sent ok
            if msg[2]=='02' or msg[2]=='03': 
                eg.PrintError('NACK: ' + str(msg))
                
                
    def decode_003(self, msg):
        subtypes = {
            '00':'ac',
            '01':'arc',
            '02':'ati',
            '03':'hideki/upm',
            '04':'lacrosse/viking',
            '05':'ad',
            '06':'mertik',
            '07':'oregon1',
            '08':'oregon2',
            '09':'oregon3',
            '0a':'proguard',
            '0b':'visonic',
            '0c':'nec',
            '0d':'fs20',
            '0e':'reserved',
            '0f':'blinds',
            '10':'rubicson',
            '11':'ae',
            '12':'fineoffset',
            '13':'rgb',
            '14':'rfy',
            '15':'selectplus'
        }
        try:
            print 'Undecoded: ', msg, subtypes[str(msg[2])]
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_040(self, msg):
        types = {
            '00': 'Digimax, TLX7506',
            '01': 'Digimax with short format (no set point)'
        }
        try:
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+dev_id
            )
            st = int(bin(int(msg[8], 16))[2:].zfill(8)[6:], 2)            
            md = int(bin(int(msg[8], 16))[2:].zfill(8)[0], 2)            
            if st == 0:
                my_status = 'no status available'
            if st == 1:
                my_status = 'demand'
            if st == 2:
                my_status = 'no demand'
            if st == 3:
                my_status = 'initializing'
            if md == 0:
                my_mode = 'heating'
            if md == 1:
                my_mode = 'cooling'
            if msg[2] == '00':
                pload_msg = (
                    ' temperature: '+
                    str(float(int(msg[6], 16)))+
                    ' setpoint: '+
                    str(float(int(msg[7], 16)))+
                    ' status: '+
                    my_status+
                    ' mode: '+
                    my_mode+
                    ' signal: '+str(int(msg[9][0], 16))
                )
            elif msg[2] == '01':
                pload_msg = (
                    ' temperature: '+
                    '0.0'+
                    ' signal: '+str(int(msg[9][0], 16))
                )
            decode_param = None
            mon_param = None
            try:
                decode_param = self.decode_040_mem[base_msg]
            except:
                pass
            self.eventTrigger(
                decode_param,
                base_msg,
                pload_msg
            )
            try:
                mon_param = self.monitor_040_mem[base_msg]
            except:
                pass
            self.monitor_040_mem[base_msg] = self.eventMonitor(
                mon_param,
                decode_param,
                base_msg,
                self.sensorLostTimeOut
            )
            self.decode_040_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_042(self, msg):
        types = {
            '00': 'Mertik G6R-H4T1',
            '01': 'Mertik G6R-H4TB/G6-H4T/G6R-H4T21-Z22',
            '02': 'Mertik G6R-H4TD'
        }
        try:
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5]+msg[6], 16))
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+dev_id
            )
            cmd = int(msg[7][1], 16)
            if cmd == 0:
                my_cmd = 'off'
            elif cmd == 1:
                my_cmd = 'on'
            elif cmd == 2:
                my_cmd = 'up'
            elif cmd == 3:
                my_cmd = 'down'
            elif cmd == 4:
                if int(msg[2]) == 0: #G6R-H4T1
                    my_cmd = 'Run Up'
                elif int(msg[2]) == 1: #G6R-H4TB
                    my_cmd = '2nd Off'
            elif cmd == 5:
                if int(msg[2]) == 0: #G6R-H4T1
                    my_cmd = 'Run Down'
                elif int(msg[2]) == 1: #G6R-H4TB
                    my_cmd = '2nd On'
            elif cmd == 6:
                if int(msg[2]) == 0: #G6R-H4T1
                    my_cmd = 'Stop'
                elif int(msg[2]) == 1: #G6R-H4TB
                    my_cmd = 'NA'
            pload_msg = (
                ' command: '+
                my_cmd+
                ' signal: '+str(int(msg[8][0], 16))
            )
            decode_param = None
            mon_param = None
            try:
                decode_param = self.decode_042_mem[base_msg]
            except:
                pass
            self.eventTrigger(
                decode_param,
                base_msg,
                pload_msg
            )
            try:
                mon_param = self.monitor_042_mem[base_msg]
            except:
                pass
            self.monitor_042_mem[base_msg] = self.eventMonitor(
                mon_param,
                decode_param,
                base_msg,
                self.sensorLostTimeOut
            )
            self.decode_042_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_04E(self, msg):
        types = {
            '01': 'Maverick ET-732 BBQ temperature sensors'
        }
        try:
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+dev_id
            )
            pload_msg = (
                ' temperature Food: '+
                str(float(int(msg[6], 16)*256 + int(msg[7], 16)))+
                ' temperature BBQ: '+
                str(float(int(msg[8], 16)*256 + int(msg[9], 16)))+
                ' signal: '+str(int(msg[10][0], 16))+
                ' battery: '+str(int(msg[10][1], 16))
            )
            decode_param = None
            mon_param = None
            try:
                decode_param = self.decode_04E_mem[base_msg]
            except:
                pass
            self.eventTrigger(
                decode_param,
                base_msg,
                pload_msg
            )
            try:
                mon_param = self.monitor_04E_mem[base_msg]
            except:
                pass
            self.monitor_04E_mem[base_msg] = self.eventMonitor(
                mon_param,
                decode_param,
                base_msg,
                self.sensorLostTimeOut
            )
            self.decode_04E_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_04F(self, msg):
        types = {
            '01': 'Alecto WS1200'
        }
        signs = {
            '0': '+',
            '1': '-'
        }
        try:
            #Get the correct sign
            sign_bt = bin(int(msg[6], 16))[2:].zfill(8)            
            sign = signs[sign_bt[0]]
            
            #Calculate the actual temperature
            if sign == '+':
                tempC = str(
                float(
                    (
                        int(msg[6], 16)*256 +
                        int(msg[7], 16))/10.0
                    )
                )
            
            if sign == '-':
                tempC = str(
                float(
                (
                    (
                        int(msg[6], 16) & int('7F', 16))*256 +
                        int(msg[7], 16))/10.0
                    )
                )

            rainTot = str(
                float(
                    (
                        int(msg[8], 16)*256 +
                        int(msg[9], 16))/10.0
                    )
                )

            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            
            #Get the channel value
            #print msg[4]
    
            if int(dev_id) <> 0:
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' temperature: '+sign+tempC+' deg C'+
                    ' rain total: '+rainTot+' mm'+
                    ' signal: '+str(int(msg[10][0], 16))+
                    ' battery: '+str(int(msg[10][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_04F_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_04F_mem[base_msg]
                except:
                    pass
                self.monitor_04F_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_04F_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_050(self, msg):
        types = {
            '01': 'THR128/138, THC138',
            '02': 'THC238/268,THN132,THWR288,THRN122,THN122,AW129/131',
            '03': 'THWR800',
            '04': 'RTHN318',
            '05': 'La Crosse TX3, TX4, TX17',
            '06': 'TS15C,UPM temp only',
            '07': 'Viking 02811',
            '08': 'La Crosse WS2300',
            '09': 'RUBiCSON',
            '0a': 'TFA 30.3133',
            '0b': 'WT0122'
        }
        signs = {
            '0': '+',
            '1': '-'
        }
        try:
            #Get the correct sign
            sign_bt = bin(int(msg[6], 16))[2:].zfill(8)            
            sign = signs[sign_bt[0]]
            
            #Calculate the actual temperature
            if sign == '+':
                tempC = str(
                float(
                    (
                        int(msg[6], 16)*256 +
                        int(msg[7], 16))/10.0
                    )
                )
            
            if sign == '-':
                tempC = str(
                float(
                (
                    (
                        int(msg[6], 16) & int('7F', 16))*256 +
                        int(msg[7], 16))/10.0
                    )
                )

            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            
            #Get the channel value
            #print msg[4]
    
            if int(dev_id) <> 0:
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' temperature: '+sign+tempC+' deg C'+
                    ' signal: '+str(int(msg[8][0], 16))+
                    ' battery: '+str(int(msg[8][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_050_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_050_mem[base_msg]
                except:
                    pass
                self.monitor_050_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_050_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_051(self, msg):
        types = {
            '01': 'La Crosse TX3',
            '02': 'La Crosse WS2300',
            '03': 'Inovalley S80 plant humidity sensor' 
        }
        if self.fwVer < 54:
            statuses = {
                '00': 'dry',
                '01': 'comfort',
                '02': 'normal',
                '03': 'wet'        
            }
        else:
            statuses = {
                '00': 'normal',
                '01': 'comfort',
                '02': 'dry',
                '03': 'wet'        
            }
        try:
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            
            #Get the channel value
            #print msg[4]
    
            if int(dev_id) <> 0:
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' humidity: '+str(int(msg[6], 16))+' %RH'+
                    ' status: '+statuses[msg[7]]+
                    ' signal: '+str(int(msg[8][0], 16))+
                    ' battery: '+str(int(msg[8][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_051_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_051_mem[base_msg]
                except:
                    pass
                self.monitor_051_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_051_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_052(self, msg):
        types = {
            '01': 'THGN122/123, THGN132, THGR122/228/238/268',
            '02': 'THGR810, THGN800',
            '03': 'RTGR328',
            '04': 'THGR328',
            '05': 'WTGR800',
            '06': 'THGR918, THGRN228, THGN500',
            '07': 'TFA TS34C, Cresta',
            '08': 'WT260, WT260H, WT440H, WT450, WT450H',
            '09': 'Viking 02035,02038',
            '0a': 'Rubicson',
            '0b': 'Oregon EW109',
            '0c': 'Imagintronix Soil sensor',
            '0d': 'Alecto WS1700 and compatibles',
            '0e': 'Alecto WS4500 and compatibles'
        }
        signs = {
            '0': '+',
            '1': '-'
        }
        if self.fwVer < 54:
            statuses = {
                '00': 'dry',
                '01': 'comfort',
                '02': 'normal',
                '03': 'wet'        
            }
        else:
            statuses = {
                '00': 'normal',
                '01': 'comfort',
                '02': 'dry',
                '03': 'wet'        
            }
        try:
            #Get the correct sign
            sign_bt = bin(int(msg[6], 16))[2:].zfill(8)            
            sign = signs[sign_bt[0]]
            
            #Calculate the actual temperature
            if sign == '+':
                tempC = str(
                float(
                    (
                        int(msg[6], 16)*256 +
                        int(msg[7], 16))/10.0
                    )
                )
            
            if sign == '-':
                tempC = str(
                float(
                (
                    (
                        int(msg[6], 16) & int('7F', 16))*256 +
                        int(msg[7], 16))/10.0
                    )
                )
    
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            
            #Get the channel value
            #print msg[4]
    
            if int(dev_id) <> 0:
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' temperature: '+sign+tempC+' deg C'+
                    ' humidity: '+str(int(msg[8], 16))+' %RH'+
                    ' status: '+statuses[msg[9]]+
                    ' signal: '+str(int(msg[10][0], 16))+
                    ' battery: '+str(int(msg[10][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_052_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_052_mem[base_msg]
                except:
                    pass
                self.monitor_052_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_052_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_054(self, msg):
        types = {
            '01': 'BTHR918, BTHGN129',
            '02': 'BTHR918N, BTHR968'
        }
        signs = {
            '0': '+',
            '1': '-'
        }
        if self.fwVer < 54:
            statuses = {
                '00': 'dry',
                '01': 'comfort',
                '02': 'normal',
                '03': 'wet'        
            }
        else:
            statuses = {
                '00': 'normal',
                '01': 'comfort',
                '02': 'dry',
                '03': 'wet'        
            }
        forecasts = {
            '00': 'no forecast available',
            '01': 'sunny',
            '02': 'partly cloudy',
            '03': 'cloudy',        
            '04': 'rain'        
        }
        try:
            #Get the correct sign
            sign_bt = bin(int(msg[6], 16))[2:].zfill(8)            
            sign = signs[sign_bt[0]]
            
            #Calculate the actual temperature
            if sign == '+':
                tempC = str(
                float(
                (
                        int(msg[6], 16)*256 +
                        int(msg[7], 16))/10.0
                    )
                )
            
            if sign == '-':
                tempC = str(
                float(
                (
                    (
                        int(msg[6], 16) & int('7F', 16))*256 +
                        int(msg[7], 16))/10.0
                    )
                )
            
            #Calculate the barometer value
            barometer = str(
            float(
                    (
                        int(msg[10], 16)*256+
                        int(msg[11], 16)
                    )
                )
            )
            
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            
            if int(dev_id) <> 0:
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' temperature: '+sign+tempC+' deg C'+
                    ' humidity: '+str(int(msg[8], 16))+' %RH'+
                    ' status: '+statuses[msg[9]]+
                    ' baro: '+barometer+' hPa'+
                    ' forecast: '+forecasts[msg[12]]+
                    ' signal: '+str(int(msg[13][0], 16))+
                    ' battery: '+str(int(msg[13][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_054_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_054_mem[base_msg]
                except:
                    pass
                self.monitor_054_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_054_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_055(self, msg):
        types = {
            '01': 'RGR126/682/918',
            '02': 'PCR800',
            '03': 'TFA',
            '04': 'UPM RG700',
            '05': 'La Crosse WS2300',
            '06': 'La Crosse TX5',
            '07': 'Alecto WS4500 and compatibles'
        }
        battery_statuses = {
            '0': '10%',
            '1': '20%',
            '2': '30%',
            '3': '40%',
            '4': '50%',
            '5': '60%',
            '6': '70%',
            '7': '80%',
            '8': '90%',
            '9': '100%'
        }
        try:
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            
            #Get the battery status
            batt_level = battery_statuses[msg[11][1]]
    
            if int(dev_id) <> 0:
    
                if msg[2]== '01':
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' rainrate: '+str(int(msg[6], 16)*256+
                            int(msg[7], 16))+' mm/hr'+
                        ' rainTotal: '+str((int(msg[8], 16)*65535+
                        int(msg[9], 16)*256+
                        int(msg[10], 16))/10)+' mm'+
                        ' signal: '+str(int(msg[11][0], 16))+
                        ' battery: '+batt_level
                    )
    
                if msg[2]== '02':
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' rainrate: '+str((int(msg[6], 16)*256+
                        int(msg[7], 16))/100)+' mm/hr'+
                        ' rainTotal: '+str((int(msg[8], 16)*65535+
                        int(msg[9], 16)*256+
                        int(msg[10], 16))/10)+' mm'+
                        ' signal: '+str(int(msg[11][0], 16))+
                        ' battery: '+batt_level
                    )
    
                if (
                    msg[2]== '03' or
                    msg[2]== '04' or
                    msg[2]== '05' or
                    msg[2]== '07'
                ):
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' rainTotal: '+str((int(msg[8], 16)*65535+
                        int(msg[9], 16)*256+
                        int(msg[10], 16))/10)+' mm'+
                        ' signal: '+str(int(msg[11][0], 16))+
                        ' battery: '+batt_level
                    )

                if (
                    msg[2]== '06'
                ):
                    flCount = int(msg[10], 16)
                    try:
                        res = self.flipCount[dev_id]
                    except:
                        #Happens at restart
                        try:
                            tst = self.totalRain[dev_id]
                        except:
                            self.totalRain[dev_id] = 0.001
                        if flCount > 0:
                            self.flipCount[dev_id] = flCount-1
                        else:
                            self.flipCount[dev_id] = 15
                        
                        #Use next if counting on first event
                        self.flCount_prev[dev_id] = self.flipCount[dev_id]
                        #Use next if not counting on first event
                        #self.flCount_prev[dev_id] = flCount 
                    
                    if flCount <> self.flCount_prev[dev_id]:
                        if self.flipCount[dev_id] > flCount:
                            self.flipCount[dev_id] = (
                                flCount + 16 - self.flipCount[dev_id]
                            )
                            addRain = float(
                                (self.flipCount[dev_id]-flCount)* 0.266
                            )
                        else:
                            addRain = float(
                                (flCount-self.flipCount[dev_id])* 0.266
                            )
                        self.flipCount[dev_id] = flCount
                        self.totalRain[dev_id] += addRain
                        CurrentStateData.totalRain[dev_id] = (
                            self.totalRain[dev_id]
                        )
                        self.flCount_prev[dev_id] = flCount
    
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' rainTotal: '+
                        str("%.2f" % self.totalRain[dev_id])+
                        ' mm'+
                        ' signal: '+str(int(msg[11][0], 16))+
                        ' battery: '+batt_level
                    )
    
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_055_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_055_mem[base_msg]
                except:
                    pass
                self.monitor_055_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_055_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_056(self, msg):
        types = {
            '01': 'WTGR800',
            '02': 'WGR800',
            '03': 'STR918, WGR918',
            '04': 'TFA',
            '05': 'UPM WDS500',           
            '06': 'La Crosse WS2300',
            '07': 'Alecto WS4500 and compatibles'
        }
        signs = {
            '0': '+',
            '1': '-'
        }
        battery_statuses = {
            '0': '10%',
            '1': '20%',
            '2': '30%',
            '3': '40%',
            '4': '50%',
            '5': '60%',
            '6': '70%',
            '7': '80%',
            '8': '90%',
            '9': '100%'
        }
        try:
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            
            #Get the channel value
            #print msg[4]
    
            if int(dev_id) <> 0:
    
                wind_dir = float(int(msg[6], 16)*256 + int(msg[7], 16))
                strDirection = "---"

                if wind_dir > 348.75 or wind_dir < 11.26:
                    strDirection = "N"
                elif wind_dir < 33.76:
                    strDirection = "NNE"
                elif wind_dir < 56.26:
                    strDirection = "NE"
                elif wind_dir < 78.76:
                    strDirection = "ENE"
                elif wind_dir < 101.26:
                    strDirection = "E"
                elif wind_dir < 123.76:
                    strDirection = "ESE"
                elif wind_dir < 146.26:
                    strDirection = "SE"
                elif wind_dir < 168.76:
                    strDirection = "SSE"
                elif wind_dir < 191.26:
                    strDirection = "S"
                elif wind_dir < 213.76:
                    strDirection = "SSW"
                elif wind_dir < 236.26:
                    strDirection = "SW"
                elif wind_dir < 258.76:
                    strDirection = "WSW"
                elif wind_dir < 281.26:
                    strDirection = "W"
                elif wind_dir < 303.76:
                    strDirection = "WNW"
                elif wind_dir < 326.26:
                    strDirection = "NW"
                elif wind_dir < 348.76:
                    strDirection = "NNW"

                if msg[2]== '04':
                    #Get the correct sign
                    sign_bt = bin(int(msg[12], 16))[2:].zfill(8)            
                    sign = signs[sign_bt[0]]
                    
                    #Calculate the actual temperature
                    if sign == '+':
                        tempC = str(
                        float(
                            (
                                int(msg[12], 16)*256 +
                                int(msg[13], 16))/10.0
                            )
                        )
                    
                    if sign == '-':
                        tempC = str(
                        float(
                            (
                                (
                                    int(msg[12], 16) & int('7F', 16))*256 +
                                    int(msg[13], 16))/10.0
                                )
                        )
                 
                    #Get the correct chill sign
                    chill_sign_bt = bin(int(msg[14], 16))[2:].zfill(8)            
                    chill_sign = signs[chill_sign_bt[0]]
                    
                    #Calculate the actual chill
                    if chill_sign == '+':
                        chillC = str(
                        float(
                            (
                                int(msg[14], 16)*256 +
                                int(msg[15], 16))/10.0
                            )
                        )
                    
                    if chill_sign == '-':
                        chillC = str(
                        float(
                        (
                            (
                                int(msg[14], 16) & int('7F', 16))*256 +
                                int(msg[15], 16))/10.0
                            )
                        )
    
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' direction: '+strDirection+
                        ' average speed: '+str(float(int(msg[8], 16)*256+
                            int(msg[9], 16))/10.0)+' m/s'+
                        ' gust: '+str(float(int(msg[10], 16)*256+
                            int(msg[11], 16))/10.0)+' m/s'+
                        ' temperature: '+temp_sign+tempC+' deg C'+
                        ' chill: '+chill_sign+chillC+' deg C'+
                        ' signal: '+str(int(msg[16][0], 16))+
                        ' battery: '+battery_statuses[msg[16][1]]
                    )
    
                if msg[2]== '05':
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' direction: '+strDirection+
                        ' gust: '+str(float(int(msg[10], 16)*256+
                            int(msg[11], 16))/10.0)+' m/s'+
                        ' signal: '+str(int(msg[16][0], 16))+
                        ' battery: '+battery_statuses[msg[16][1]]
                    )

                if (
                        msg[2]== '01' or
                        msg[2]== '02' or
                        msg[2]== '03' or
                        msg[2]== '06' or
                        msg[2]== '07'
                ):
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' direction: '+strDirection+
                        ' average speed: '+str(float(int(msg[8], 16)*256+
                            int(msg[9], 16))/10.0)+' m/s'+
                        ' gust: '+str(float(int(msg[10], 16)*256+
                            int(msg[11], 16))/10.0)+' m/s'+
                        ' signal: '+str(int(msg[16][0], 16))+
                        ' battery: '+battery_statuses[msg[16][1]]
                    )

                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_056_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_056_mem[base_msg]
                except:
                    pass
                self.monitor_056_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_056_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_057(self, msg):
        types = {
            '01': 'UVN128, UV138',
            '02': 'UVN800',
            '03': 'TFA'
        }
        signs = {
            '0': '+',
            '1': '-'
        }
        try:
            uv_level = int(msg[6], 16)/10
            uv_risk = "----"

            if uv_level < 3:
                uv_risk = "Low"
            elif uv_level < 6:
                uv_risk = "Medium"
            elif uv_level < 8:
                uv_risk = "High"
            elif uv_level < 11:
                uv_risk = "Very High"
            else:
                uv_risk = "Dangerous"

            if msg[2]== '01' or msg[2]== '02':
               
                #Get the unit ID
                dev_id = str(int(msg[4], 16)*256 + int(msg[5], 16))
                
                if int(dev_id) <> 0:
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' UV level: '+str(uv_level)+
                        ' status: '+uv_risk+
                        ' signal: '+str(int(msg[9][0], 16))+
                        ' battery: '+str(int(msg[9][1], 16))
                    )

            if msg[2]== '03':

                #Get the correct sign
                sign_bt = bin(int(msg[7], 16))[2:].zfill(8)            
                sign = signs[sign_bt[0]]
                
                #Calculate the actual temperature
                if sign == '+':
                    tempC = str(
                    float(
                    (
                            int(msg[7], 16)*256 +
                            int(msg[8], 16))/10.0
                        )
                    )

                if sign == '-':
                    tempC = str(
                    float(
                    (
                        (
                            int(msg[7], 16) & int('7F', 16))*256 +
                            int(msg[8], 16))/10.0
                        )
                    )
                
                #Get the unit ID
                dev_id = str(int(msg[4], 16)*256 + int(msg[5], 16))
                
                if int(dev_id) <> 0:
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' temperature: '+sign+tempC+' deg C'+
                        ' UV level: '+str(uv_level)+
                        ' status: '+uv_risk+
                        ' signal: '+str(int(msg[9][0], 16))+
                        ' battery: '+str(int(msg[9][1], 16))
                    )

            decode_param = None
            mon_param = None
            try:
                decode_param = self.decode_057_mem[base_msg]
            except:
                pass
            self.eventTrigger(
                decode_param,
                base_msg,
                pload_msg
            )
            try:
                mon_param = self.monitor_057_mem[base_msg]
            except:
                pass
            self.monitor_057_mem[base_msg] = self.eventMonitor(
                mon_param,
                decode_param,
                base_msg,
                self.sensorLostTimeOut
            )
            self.decode_057_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_058(self, msg):

        def checkStrLength(st):
            if len(st) < 2:
                st = "0" + st
            return st

        dayOfweek = {
            '1':'Sunday',
            '2':'Monday', 
            '3':'Tuesday',
            '4':'Wednesday', 
            '5':'Thursday',
            '6':'Friday', 
            '7':'Saturday'
        }
        types = {
            '01': 'DT1 - RTGR328N'
        }
        try:
            #Get the unit ID
            dev_id = str( int(msg[4], 16)*256 + int(msg[5], 16) )
            #year
            year = checkStrLength(str(int(msg[6], 16)))
            #month
            month = checkStrLength(str(int(msg[7], 16)))
            #day
            day = checkStrLength(str(int(msg[8], 16)))
            #dayOfweek
            dOfweek = dayOfweek[str(int(msg[9], 16))]
            #hours
            hours = checkStrLength(str(int(msg[10], 16)))
            #minutes
            minutes = checkStrLength(str(int(msg[11], 16)))
            #seconds
            seconds = checkStrLength(str(int(msg[12], 16)))

            if int(dev_id) <> 0:
                #print msg
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' Date (yy/mm/dd): '+year+'/'+month+'/'+day+
                    ' Day of week: '+dOfweek+
                    ' Time (hh:mm:ss) : '+hours+':'+minutes+':'+seconds+
                    ' signal: '+str(int(msg[13][0], 16))+
                    ' battery: '+str(int(msg[13][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_058_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_058_mem[base_msg]
                except:
                    pass
                self.monitor_058_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_058_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_059(self, msg):
        types = {
            '01': 'CM113'
        }
        try:
            #Get the unit ID
            dev_id = str( int(msg[4], 16)*256 + int(msg[5], 16) )
            
            #Counter
            counter = str(int(msg[6], 16))
            
            #Channel 1
            channel_1 = float((int(msg[7], 16)*256 + int(msg[8], 16)))/10.0 
            channel_1 = str("%.2f" % channel_1)

            #Channel 2
            channel_2 = float((int(msg[9], 16)*256 + int(msg[10], 16)))/10.0 
            channel_2 = str("%.2f" % channel_2)

            #Channel 3
            channel_3 = float((int(msg[11], 16)*256 + int(msg[12], 16)))/10.0 
            channel_3 = str("%.2f" % channel_3)

            if int(dev_id) <> 0:
                #print msg
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' Counter: '+counter+
                    ' Channel 1: '+channel_1+' A'+
                    ' Channel 2: '+channel_2+' A'+
                    ' Channel 3: '+channel_3+' A'+
                    ' signal: '+str(int(msg[13][0], 16))+
                    ' battery: '+str(int(msg[13][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_059_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_059_mem[base_msg]
                except:
                    pass
                self.monitor_059_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_059_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_060_01(self, msg):
        types = {
            '01': 'CARTELECTRONIC TIC'
        }
        try:
            #Get the unit ID
            dev_id = msg[4]+msg[5]+msg[6]+msg[7]+msg[8]
            
            #Contract type
            contract = msg[9]
            
            #Counter 1
            counter_1 = str(
                (int(msg[10], 16) << 24) +
                (int(msg[11], 16) << 16) +
                (int(msg[12], 16) << 8) +
                (int(msg[13], 16))
            )
    
            #Counter 2
            counter_2 = str(
                (int(msg[14], 16) << 24) +
                (int(msg[15], 16) << 16) +
                (int(msg[16], 16) << 8) +
                (int(msg[17], 16))
            )
    
            #State          
            state = str(self.hextobin(msg[20]))
            power = '0'
            teleinfo = 'Present'
            pejp = ''
    
            if int(state[5])==1:
                teleinfo = 'Not present'
            if int(state[6])==1:
                power = float((int(msg[18], 16)*256 + int(msg[19], 16))) 
                power = str("%.2f" % power)
            if state[3]+state[4]=='00':
                pejp = 'No change price time warning'
            if state[3]+state[4]=='01':
                pejp = 'White'
            if state[3]+state[4]=='10':
                pejp = 'Blue'
            if state[3]+state[4]=='11':
                pejp = 'Red / PEJP'
            
            if dev_id <> '':
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    'Contract/Price: '+contract+
                    ' Counter1: '+counter_1+
                    ' Counter2: '+counter_2+
                    ' Teleinfo: '+teleinfo+
                    ' PEJP or DEMAIN: '+pejp+
                    ' Apparent power: '+str(power)+
                    ' signal: '+str(int(msg[21][0], 16))+
                    ' battery: '+str(int(msg[21][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_060_01_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_060_01_mem[base_msg]
                except:
                    pass
                self.monitor_060_01_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_060_01_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))
        
        
        
    def decode_060_02(self, msg):
        types = {
            '02': 'CARTELECTRONIC ENCODER'
        }
        try:
            #Get the unit ID
            dev_id = msg[4]+msg[5]+msg[6]+msg[7]
            
            #Counter 1
            counter_1 = str(
                (int(msg[8], 16) << 24) +
                (int(msg[9], 16) << 16) +
                (int(msg[10], 16) << 8) +
                (int(msg[11], 16))
            )
    
            #Counter 2
            counter_2 = str(
                (int(msg[12], 16) << 24) +
                (int(msg[13], 16) << 16) +
                (int(msg[14], 16) << 8) +
                (int(msg[15], 16))
            )
            
            if dev_id <> '':
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    'Counter1: '+counter_1+
                    ' Counter2: '+counter_2+
                    ' signal: '+str(int(msg[17][0], 16))+
                    ' battery: '+str(int(msg[17][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_060_02_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_060_02_mem[base_msg]
                except:
                    pass
                self.monitor_060_02_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_060_02_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))
        

    def decode_05A_1(self, msg):
        types = {
            '01': 'CM119/160'
        }
        try:
            #Get the unit ID
            dev_id = str( int(msg[4], 16)*256 + int(msg[5], 16) )
            
            #Counter
            counter = str(int(msg[6], 16))
            
            #Instant power consumption in Watts
            instant = str("%.2f" %
                float(
                    eval('0x'+msg[7])*0x1000000+
                    eval('0x'+msg[8])*0x10000+
                    eval('0x'+msg[9])*0x100+
                    eval('0x'+msg[10])
                )
            )

            #Total energy usage in Wh
            f_usage = float(
                    eval('0x'+msg[11])*0x10000000000+
                    eval('0x'+msg[12])*0x100000000+
                    eval('0x'+msg[13])*0x1000000+
                    eval('0x'+msg[14])*0x10000+
                    eval('0x'+msg[15])*0x100+
                    eval('0x'+msg[16])
                ) / 223.666
                
            usage = str("%.2f" % f_usage)

            if int(dev_id) <> 0:
                #print msg
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' Counter: '+counter+
                    ' Instant power usage: '+instant+' W'+
                    ' Total energy usage: '+usage+' Wh'+
                    ' signal: '+str(int(msg[17][0], 16))+
                    ' battery: '+str(int(msg[17][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_05A_1_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_05A_1_mem[base_msg]
                except:
                    pass
                self.monitor_05A_1_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_05A_1_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_05A_2(self, msg):
        types = {
            '02': 'CM180'
        }
        try:
            #Get the unit ID
            dev_id = str( int(msg[4], 16)*256 + int(msg[5], 16) )
            
            #Counter
            counter = str(int(msg[6], 16))
            
            #Instant power consumption in Watts
            instant = str("%.2f" %
                float(
                    eval('0x'+msg[7])*0x1000000+
                    eval('0x'+msg[8])*0x10000+
                    eval('0x'+msg[9])*0x100+
                    eval('0x'+msg[10])
                )
            )

            if int(counter) == 0:
		            #Total energy usage in Wh
		            f_usage = float(
		                    eval('0x'+msg[11])*0x10000000000+
		                    eval('0x'+msg[12])*0x100000000+
		                    eval('0x'+msg[13])*0x1000000+
		                    eval('0x'+msg[14])*0x10000+
		                    eval('0x'+msg[15])*0x100+
		                    eval('0x'+msg[16])
		                ) / 223.666
		            self.usage_05A_2 = str("%.2f" % f_usage)
                
            if int(dev_id) <> 0:
                #print msg
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' Counter: '+counter+
                    ' Instant power usage: '+instant+' W'+
                    ' Total energy usage: '+self.usage_05A_2+' Wh'+
                    ' signal: '+str(int(msg[17][0], 16))+
                    ' battery: '+str(int(msg[17][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_05A_2_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_05A_2_mem[base_msg]
                except:
                    pass
                self.monitor_05A_2_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_05A_2_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_05B(self, msg):
        types = {
            '01': 'CM180i'
        }
        try:
            #Get the unit ID
            dev_id = str( int(msg[4], 16)*256 + int(msg[5], 16) )
            
            #Counter
            counter = str(int(msg[6], 16))
            
            #Instant current consumption in ampere
            ampere_1 = str("%.2f" %
                float(int(msg[7], 16)*256 + int(msg[8], 16)) / 10.0
            )

            ampere_2 = str("%.2f" %
                float(int(msg[9], 16)*256 + int(msg[10], 16)) / 10.0
            )

            ampere_3 = str("%.2f" %
                float(int(msg[11], 16)*256 + int(msg[12], 16)) / 10.0
            )


            #Total energy usage in Wh
            usage = '0'
            f_usage = float(
                    eval('0x'+msg[13])*0x10000000000+
                    eval('0x'+msg[14])*0x100000000+
                    eval('0x'+msg[15])*0x1000000+
                    eval('0x'+msg[16])*0x10000+
                    eval('0x'+msg[17])*0x100+
                    eval('0x'+msg[18])
                ) / 223.666
                
            if int(msg[6], 16) == 0:
                usage = str("%.2f" % f_usage)

            if int(dev_id) <> 0:
                #print msg
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' Counter: '+counter+
                    ' Current ch1: '+ampere_1+' A'+
                    ' Current ch2: '+ampere_2+' A'+
                    ' Current ch3: '+ampere_3+' A'+
                    ' Total energy usage: '+usage+' Wh'+
                    ' signal: '+str(int(msg[19][0], 16))+
                    ' battery: '+str(int(msg[19][1], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_05B_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_05B_mem[base_msg]
                except:
                    pass
                self.monitor_05B_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_05B_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_05C(self, msg):
        types = {
            '01': 'ELEC5 - Revolt'
        }
        try:
            #Get the unit ID
            dev_id = str(int(msg[4], 16)*256 + int(msg[5], 16))
            
            #power line voltage
            voltage = str(int(msg[6], 16))
            
            #currentH-currentL
            current = float((int(msg[7], 16)*256 + int(msg[8], 16)))/100.0 
            current = str("%.2f" % current)

            #powerH-powerL
            power = float((int(msg[9], 16)*256 + int(msg[10], 16)))/10.0 
            power = str("%.2f" % power)

            #energyH-energyL
            energy = float((int(msg[11], 16)*256 + int(msg[12], 16)))/100.0 
            energy = str("%.2f" % energy)

            #power factor
            pf = float(int(msg[13], 16))/100.0 
            pf = str("%.2f" % pf)

            #power line frequency in Hz
            freq = str(int(msg[14], 16))

            if int(dev_id) <> 0:
                #print msg
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' Voltage: '+voltage+' V'+
                    ' Ampere: '+current+' A'+
                    ' Instant Power: '+power+' W'+
                    ' Total Energy: '+energy+' kWh'+
                    ' Power Factor: '+pf+
                    ' Frequency: '+freq+' Hz'+
                    ' signal: '+str(int(msg[15][0], 16))
                )
                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_05C_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_05C_mem[base_msg]
                except:
                    pass
                self.monitor_05C_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    self.sensorLostTimeOut
                )
                self.decode_05C_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_070(self, msg):
        types = {
            '00': 'RFXSensor temperature',
            '01': 'RFXSensor A/D',
            '02': 'RFXSensor voltage',
            '03': 'RFXSensor message'
        }
        signs = {
            '0': '+',
            '1': '-'
        }
        messages = {
            '01': 'RFXSensor addresses incremented',
            '02': 'RFXSensor battery low detected',
            '81': 'RFXSensor no 1-wire device connected',
            '82': 'RFXSensor 1-Wire ROM CRC error',
            '83': 'RFXSensor 1-Wire device connected is not a DS18B20 or DS2438',
            '84': 'RFXSensor no end of read signal received from 1-Wire device',
            '85': 'RFXSensor 1-Wire scratchpad CRC error'
        }
       
        try:
            #Get the unit ID
            dev_id = str(int(msg[4]+msg[5], 16))
            
            #Get the channel value
            #print msg[4]
    
            if int(dev_id) <> 0:

                if msg[2]== '00':
                    #Get the correct sign
                    sign_bt = bin(int(msg[5], 16))[2:].zfill(8)            
                    sign = signs[sign_bt[0]]
                    
                    #Calculate the actual temperature
                    if sign == '+':
                        tempC = str(
                        float(
                            (
                                int(msg[5], 16)*256 +
                                int(msg[6], 16))
                            )/100.0
                        )
    
                    if sign == '-':
                        tempC = str(
                        float(
                                (int(msg[5], 16) & int('7F', 16))*256 +
                                 int(msg[6], 16)
                            )/100.0
                        )
                    base_msg = (
                        'Type: '+types[msg[2]]+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' temperature: '+sign+tempC+' deg C'+
                        ' signal: '+str(int(msg[7][0], 16))
                    )

                if msg[2]== '01' or msg[2]== '02':
                    #Calculate the actual voltage level
                    voltage = str(
                    float(
                        (
                            int(msg[5], 16)*256 +
                            int(msg[6], 16))
                        )
                    )
                    pload_msg = (
                        ' voltage: '+voltage+' mV'+
                        ' signal: '+str(int(msg[7][0], 16))
                    )

                if msg[2]== '03':
                    #Map the correct message
                    message = messages[msg[6]]
                    pload_msg = (
                        ' message: '+message+
                        ' signal: '+str(int(msg[7][0], 16))
                    )

                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )

                decode_param = None
                mon_param = None
                try:
                    decode_param = self.decode_070_mem[base_msg]
                except:
                    pass
                self.eventTrigger(
                    decode_param,
                    base_msg,
                    pload_msg
                )
                try:
                    mon_param = self.monitor_070_mem[base_msg]
                except:
                    pass
                self.monitor_070_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    6000.0
                )
                self.decode_070_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_071(self, msg):
        types = {
            '00':'RFXMeter normal data packet',
            '0f':'Identification packet'
        }
        firmware_version = (
            'RFXPower',
            'RFU',
            'RFU',
            'RFXMeter'
        )
        try:
            #Get the unit ID
            dev_id = str( int(msg[4], 16)*256 + int(msg[5], 16) )
            dev_type = '----'

            if int(dev_id) <> 0:

                if msg[2] == '0f': #Identification packet
                    if int(msg[8], 16) <= int('3f', 16):
                        dev_type = firmware_version[0]
                    elif int(msg[8], 16) <= int('7f', 16):
                        dev_type = firmware_version[1]
                    elif int(msg[8], 16) <= int('bf', 16):
                        dev_type =firmware_version[2]
                    else:
                        dev_type = firmware_version[3]
    
                    self.rfxSensors[dev_id] = dev_type
    
                if msg[2] == '00': #Normal counter data packet
                    counter = (
                        (int(msg[6], 16) << 24) +
                        (int(msg[7], 16) << 16) +
                        (int(msg[8], 16) << 8) +
                        (int(msg[9], 16))
                    )
                    try:
                        dev_type = self.rfxSensors[dev_id]
                    except:
                        dev_type = 'RFXMeter' #default to RFXMeter
                    
                    #Look for RFXPower device
                    if dev_type == firmware_version[0]: 
                        counter = str("%.3f" % float(counter/1000.0))+' kWh'
                    else:
                        counter = str(counter)
                    base_msg = (
                        'Type: '+dev_type+
                        ' id: '+dev_id
                    )
                    pload_msg = (
                        ' Counter: '+counter+
                        ' signal: '+str(int(msg[10][0], 16))
                    )
                    decode_param = None
                    mon_param = None

                    try:
                        decode_param = self.decode_071_mem[base_msg]
                    except:
                        pass
                    self.eventTrigger(
                        decode_param,
                        base_msg,
                        pload_msg
                    )
                    try:
                        mon_param = self.monitor_071_mem[base_msg]
                    except:
                        pass
                    self.monitor_071_mem[base_msg] = self.eventMonitor(
                        mon_param,
                        decode_param,
                        base_msg,
                        3900.0
                    )
                    self.decode_071_mem[base_msg] = pload_msg
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_010(self, msg):
        types = {
            '00': 'X10 lighting',
            '01': 'ARC',
            '02': 'ELRO AB400D',
            '03': 'Waveman',
            '04': 'Chacon EMW200',
            '05': 'IMPULS',
            '06': 'RisingSun',
            '07': 'Philips SBC',
            '08': 'Energenie'
        }
        housecodes = {
            '41': 'A',
            '42': 'B',
            '43': 'C',
            '44': 'D',
            '45': 'E',
            '46': 'F',
            '47': 'G',
            '48': 'H',
            '49': 'I',
            '4a': 'J',
            '4b': 'K',
            '4c': 'L',
            '4d': 'M',
            '4e': 'N',
            '4f': 'O',
            '50': 'P'
        }            
        unitcodes = {
            '00': '00',
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04',
            '05': '05',
            '06': '06',
            '07': '07',
            '08': '08',
            '09': '09',
            '0a': '10',
            '0b': '11',
            '0c': '12',
            '0d': '13',
            '0e': '14',
            '0f': '15',
            '10': '16'
        }
        commands = {
            '00': 'off',
            '01': 'on',
            '02': 'dim',
            '03': 'bright',            
            '05': 'all off',
            '06': 'all on',
            '07': 'chime'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' house: '+housecodes[msg[4]]+
                ' unit: '+unitcodes[msg[5]]+
                ' command: '+commands[msg[6]]
            )
            pload_msg = (
                ' signal: '+str(int(msg[7][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' house: '+housecodes[msg[4]]+
                ' unit: '+unitcodes[msg[5]]
            )
            msg_value = (
                ' command: '+commands[msg[6]]+
                ' signal: '+str(int(msg[7][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                housecodes[msg[4]]+
                ' '+
                unitcodes[msg[5]]
            )
            decode_param = None
            try:
                decode_param = self.decode_010_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_010_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_011(self, msg):
        types = {
            '00': 'AC',
            '01': 'HomeEasy EU',
            '02': 'ANSLUT'
        }
        unitcodes = {
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04',
            '05': '05',
            '06': '06',
            '07': '07',
            '08': '08',
            '09': '09',
            '0a': '10',
            '0b': '11',
            '0c': '12',
            '0d': '13',
            '0e': '14',
            '0f': '15',
            '10': '16'
        }
        commands = {
            '00': 'off',
            '01': 'on',
            '02': 'dim level',
            '03': 'group off',
            '04': 'group on',
            '05': 'group dim level'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' address: '+msg[4]+msg[5]+msg[6]+msg[7]+
                ' unit: '+unitcodes[msg[8]]+
                ' command: '+commands[msg[9]]
            )
            pload_msg = (
                ' level: '+str(int(msg[10][0], 16))+
                ' signal: '+str(int(msg[11][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' address: '+msg[4]+msg[5]+msg[6]+msg[7]+
                ' unit: '+unitcodes[msg[8]]
            )
            msg_value = (
                ' command: '+commands[msg[9]]+
                ' level: '+str(int(msg[10][0], 16))+
                ' signal: '+str(int(msg[11][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+msg[5]+msg[6]+msg[7]+
                ' '+
                unitcodes[msg[8]]
            )
            decode_param = None
            try:
                decode_param = self.decode_011_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_011_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_013(self, msg):
        types = {
            '00': 'PT2262'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' Code: '+msg[4]+msg[5]+msg[6]
            )
            pulse = float((int(msg[7], 16)*256 + int(msg[8], 16))) 
            pulse = str("%.0f" % pulse)
            pload_msg = (
                'Code: '+msg[4]+msg[5]+msg[6]+
                ' PulseTiming: '+str(pulse)+
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' Code: '+msg[4]+msg[5]+msg[6]
            )
            msg_value = (
                ' signal: '+str(int(msg[9][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+' '+msg[5]+' '+msg[6]
            )
            decode_param = None
            try:
                decode_param = self.decode_013_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_013_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_014_00(self, msg):
        types = {
            '00': 'LightwaveRF, Siemens'
        }
        unitcodes = {
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04',
            '05': '05',
            '06': '06',
            '07': '07',
            '08': '08',
            '09': '09',
            '0a': '10',
            '0b': '11',
            '0c': '12',
            '0d': '13',
            '0e': '14',
            '0f': '15',
            '10': '16'
        }
        commands = {
            '00': 'off',
            '01': 'on',
            '02': 'group Off',
            '03': 'mood1',            
            '04': 'mood2',
            '05': 'mood3',
            '06': 'mood4',
            '07': 'mood5',
            '08': 'reserved',
            '09': 'reserved',
            '0a': 'unlock',
            '0b': 'lock',
            '0c': 'all lock',
            '0d': 'close (inline relay)',
            '0e': 'stop (inline relay)',
            '0f': 'open (inline relay)',
            '10': 'set level',
            '11': 'colour palette',
            '12': 'colour tone',
            '13': 'colour cycle'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' level: '+msg[9]+
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' level: '+msg[9]+
                ' signal: '+str(int(msg[9][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+' '+msg[5]+' '+msg[6]+
                ' '+
                unitcodes[msg[7]]
            )
            decode_param = None
            try:
                decode_param = self.decode_014_00_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_014_00_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_014_01(self, msg):
        types = {
            '01': 'EMW100 GAO/Everflourish'
        }
        unitcodes = {
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04'
        }
        commands = {
            '00': 'off',
            '01': 'on',
            '02': 'learn'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' signal: '+str(int(msg[9][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+' '+msg[5]+' '+msg[6]+
                ' '+
                unitcodes[msg[7]]
            )
            decode_param = None
            try:
                decode_param = self.decode_014_01_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_014_01_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_014_02(self, msg):
        types = {
            '02': 'ByeByeStandBy',
            '04': 'Conrad RSL2',
            '11': 'Cotech, Kangtai'
        }
        unitcodes = {
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04',
            '05': '05',
            '06': '06',
            '07': '07',
            '08': '08',
            '09': '09',
            '0a': '10',
            '0b': '11',
            '0c': '12',
            '0d': '13',
            '0e': '14',
            '0f': '15',
            '10': '16',
            '11': '17',
            '12': '18',
            '13': '19',
            '14': '20',
            '15': '21',
            '16': '22',
            '17': '23',
            '18': '24',
            '19': '25',
            '1a': '26',
            '1b': '27',
            '1c': '28',
            '1d': '29',
            '1e': '30'
        }
        commands = {
            '00': 'off',
            '01': 'on',
            '02': 'group off',
            '03': 'group on'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' signal: '+str(int(msg[9][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+' '+msg[5]+' '+msg[6]+
                ' '+
                unitcodes[msg[7]]
            )
            decode_param = None
            try:
                decode_param = self.decode_014_02_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_014_02_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_014_06(self, msg):
        types = {
            '06': 'RGB TRC02'
        }
        commands = {
            '00': 'off',
            '01': 'on',
            '02': 'bright',            
            '03': 'dim',
            '04': 'color +',
            '05': 'color -',            
            '06': 'select color'
        }
        try:
            if int(msg[8], 16) > 5:
                res = 'color choice '+str(msg[8])
            else:
                res = commands[msg[8]]
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' command: '+res
            )
            pload_msg = (
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]
            )
            msg_value = (
                ' command: '+res
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+' '+msg[5]+' '+msg[6]
            )
            decode_param = None
            try:
                decode_param = self.decode_014_06_mem[msg_key]
            except:
                pass
            self.eventTrigger3(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_014_06_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_014_07(self, msg):
        types = {
            '07': 'Aoke Relay'
        }
        unitcodes = {
            '00': '00'
        }
        commands = {
            '00': 'Off',
            '01': 'On'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' signal: '+str(int(msg[9][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+' '+msg[5]+' '+msg[6]+
                ' '+
                unitcodes[msg[7]]
            )
            decode_param = None
            try:
                decode_param = self.decode_014_07_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_014_07_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_014_0d(self, msg):
        types = {
            '0d': 'Legrand CAD'
        }
        unitcodes = {
            '00': '00'
        }
        commands = {
            '00': 'Toggle'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' signal: '+str(int(msg[9][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+' '+msg[5]+' '+msg[6]+
                ' '+
                unitcodes[msg[7]]
            )
            decode_param = None
            try:
                decode_param = self.decode_014_0D_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_014_0D_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_014_0f(self, msg):
        types = {
            '0f': 'IT (Intertek,FA500,PROmax�)'
        }
        unitcodes = {
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04'
        }
        commands = {
            '00': 'Off',
            '01': 'On',
            '02': 'Group Off',
            '03': 'Group On',
            '04': 'Set Level'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+msg[5]+msg[6]+
                ' unit: '+unitcodes[msg[7]]
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' signal: '+str(int(msg[9][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+' '+msg[5]+' '+msg[6]+
                ' '+
                unitcodes[msg[7]]
            )
            decode_param = None
            try:
                decode_param = self.decode_014_0F_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_014_0F_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_015(self, msg):
        types = {
            '00': 'Blyss_Thomson'
        }
        housecodes = {
            '41': 'A',
            '42': 'B',
            '43': 'C',
            '44': 'D',
            '45': 'E',
            '46': 'F',
            '47': 'G',
            '48': 'H',
            '49': 'I',
            '4a': 'J',
            '4b': 'K',
            '4c': 'L',
            '4d': 'M',
            '4e': 'N',
            '4f': 'O',
            '50': 'P'
        }            
        unitcodes = {
            '00': '00',
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04',
            '05': '05'
        }
        commands = {
            '00': 'on',
            '01': 'off',
            '02': 'group on',
            '03': 'group off'
        }
        try:
            #Get the unit ID
            dev_id = str( int(msg[4], 16)*256 + int(msg[5], 16) )

            if int(dev_id) <> 0:
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id+
                    ' house: '+housecodes[msg[6]]+
                    ' unit: '+unitcodes[msg[7]]+
                    ' command: '+commands[msg[8]]
                )
                pload_msg = (
                    ' signal: '+str(int(msg[11][0], 16))
                )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+dev_id+
                ' house: '+housecodes[msg[6]]+
                ' unit: '+unitcodes[msg[7]]
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' signal: '+str(int(msg[11][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+
                ' '+
                msg[5]+
                ' '+
                housecodes[msg[6]]+
                ' '+
                unitcodes[msg[7]]
            )
            decode_param = None
            try:
                decode_param = self.decode_015_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_015_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_016(self, msg):
        types = {
            '00': 'Byron SX',
            '02': 'SelectPlus 200689101',
            '03': 'RFU',   #Reserved Future Use       
            '04': 'Envivo'          
        }
        commands = {
            '00': 'Sound0',
            '01': 'Sound1',
            '02': 'Sound2',
            '03': 'Sound3',
            '04': 'Sound4',
            '05': 'Sound5',
            '06': 'Sound6',
            '07': 'Sound7',
            '08': 'Sound8',
            '09': 'Sound9',
            '0a': 'Sound10',
            '0b': 'Sound11',
            '0c': 'Sound12',
            '0d': 'Sound13',
            '0e': 'Sound14',
            '0f': 'Sound15'
        }

        try:
            #Get the unit ID
            if msg[2] == '00':
                dev_id = str( int(msg[4], 16)*256 + int(msg[5], 16) )
                command = commands[msg[6]]

            if msg[2] == '02' or msg[2] == '03' or msg[2] == '04':
                dev_id = str( int(msg[4], 16)*65535 + int(msg[5], 16)*256 + int(msg[6], 16) )
                command = 'NA'
                
            if int(dev_id) <> 0:
                base_msg = (
                    'Type: '+types[msg[2]]+
                    ' id: '+dev_id
                )
                pload_msg = (
                    ' command: '+command+
                    ' signal: '+str(int(msg[7][0], 16))
                )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+dev_id
            )
            msg_value = (
                ' command: '+command+
                ' signal: '+str(int(msg[7][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+
                ' '+
                msg[5]
            )
            decode_param = None
            try:
                decode_param = self.decode_016_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_016_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_018(self, msg):
        types = {
            '00': 'Harrison Curtain'
        }
        housecodes = {
            '41': 'A',
            '42': 'B',
            '43': 'C',
            '44': 'D',
            '45': 'E',
            '46': 'F',
            '47': 'G',
            '48': 'H',
            '49': 'I',
            '4a': 'J',
            '4b': 'K',
            '4c': 'L',
            '4d': 'M',
            '4e': 'N',
            '4f': 'O',
            '50': 'P'
        }            
        unitcodes = {
            '01': '01',
            '02': '02',
            '03': '03',
            '04': '04',
            '05': '05',
            '06': '06',
            '07': '07',
            '08': '08',
            '09': '09',
            '0a': '10',
            '0b': '11',
            '0c': '12',
            '0d': '13',
            '0e': '14',
            '0f': '15',
            '10': '16'
        }
        commands = {
            '00': 'Open',
            '01': 'Close',
            '02': 'Stop',            
            '03': 'Program'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' house: '+housecodes[msg[4]]+
                ' unit: '+unitcodes[msg[5]]+
                ' command: '+commands[msg[6]]
            )
            pload_msg = (
                ' battery: '+str(int(msg[7][1], 16))+
                ' signal: '+str(int(msg[7][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' house: '+housecodes[msg[4]]+
                ' unit: '+unitcodes[msg[5]]
            )
            msg_value = (
                ' command: '+commands[msg[6]]+
                ' battery: '+str(int(msg[7][1], 16))+
                ' signal: '+str(int(msg[7][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                housecodes[msg[4]]+
                ' '+
                unitcodes[msg[5]]
            )
            decode_param = None
            try:
                decode_param = self.decode_018_019_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_018_019_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_019(self, msg):
        types = {
            '00': 'RollerTrol, Hasta new',
            '01': 'Hasta old'
        }
        unitcodes = {
            '0': 'all units',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            'a': '10',
            'b': '11',
            'c': '12',
            'd': '13',
            'e': '14',
            'f': '15'
        }
        commands = {
            '00': 'Open',
            '01': 'Close',
            '02': 'Stop',            
            '03': 'Confirm',
            '04': 'Set Limit',
            '05': 'Set Lower Limit',            
            '06': 'Delete limits',
            '07': 'Change direction',
            '08': 'Left',
            '09': 'Right'
        }
        try:
            u_code = str(int(msg[7][0], 16))
            t_type = msg[2]

            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]+
                ' unit: '+unitcodes[u_code]+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' battery: '+str(int(msg[9][1], 16))+
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]+
                ' unit: '+u_code
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' battery: '+str(int(msg[9][1], 16))+
                ' signal: '+str(int(msg[9][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+' '+msg[5]+' '+msg[6]+
                ' '+
                u_code
            )
            decode_param = None
            try:
                decode_param = self.decode_018_019_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_018_019_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_019_2(self, msg):
        types = {
            '02': 'A-OK RF01',
            '03': 'A-OK AC114',
            '04': 'Raex YR1326',
            '05': 'Media Mount'
        }
        commands = {
            '00': 'Open',
            '01': 'Close',
            '02': 'Stop',            
            '03': 'Confirm/Pair',
            '04': 'Set Limit',
            '05': 'Set Lower Limit',            
            '06': 'Delete limits',
            '07': 'Change direction',
            '08': 'Left',
            '09': 'Right'
        }
        try:
            u_code = msg[7]
            t_type = msg[2]

            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]+
                ' unit: '+u_code+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' battery: '+str(int(msg[9][1], 16))+
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]+
                ' unit: '+u_code
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' battery: '+str(int(msg[9][1], 16))+
                ' signal: '+str(int(msg[9][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+' '+msg[5]+' '+msg[6]+
                ' '+
                u_code
            )
            decode_param = None
            try:
                decode_param = self.decode_018_019_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_018_019_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_019_6(self, msg):
        types = {
            '06': 'DC/RMF/Yooda',
            '07': 'Forest'
        }
        unitcodes = {
            '0': 'all units',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            'a': '10',
            'b': '11',
            'c': '12',
            'd': '13',
            'e': '14',
            'f': '15'
        }
        commands = {
            '00': 'Open',
            '01': 'Close',
            '02': 'Stop',            
            '03': 'Confirm/Pair'
        }
        try:
            u_code = unitcodes[msg[7][1]]
            t_type = msg[2]
            the_id = (
                msg[4]+
                ' '+
                msg[5]+
                ' '+
                msg[6]+
                ' '+
                str(int(msg[7][0], 16))
            )

            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+the_id+
                ' unit: '+u_code+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' battery: '+str(int(msg[9][1], 16))+
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+the_id+
                ' unit: '+u_code
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' battery: '+str(int(msg[9][1], 16))+
                ' signal: '+str(int(msg[9][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                the_id+
                ' '+
                u_code
            )
            decode_param = None
            try:
                decode_param = self.decode_018_019_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_018_019_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_019_8(self, msg):
        types = {
            '08': 'Chamberlain CS4330CN'
        }
        unitcodes = {
            '0': '01',
            '1': '02',
            '2': '03',
            '3': '04',
            '4': '05',
            '5': '06'
        }
        commands = {
            '00': 'Down',
            '01': 'Up',
            '02': 'Stop'
        }

        try:
            u_code = str(int(msg[7][0], 16))
            t_type = msg[2]

            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]+
                ' unit: '+unitcodes[u_code]+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' battery: '+str(int(msg[9][1], 16))+
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]+
                ' unit: '+u_code
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' battery: '+str(int(msg[9][1], 16))+
                ' signal: '+str(int(msg[9][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+' '+msg[5]+' '+msg[6]+
                ' '+
                u_code
            )
            decode_param = None
            try:
                decode_param = self.decode_018_019_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_018_019_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_019_B(self, msg):
        types = {
            '0b': 'ASP'
        }
        commands = {
            '00': 'Open',
            '01': 'Close',
            '02': 'Stop',            
            '03': 'Confirm/Pair'
        }
        try:
            u_code = str(int(msg[7][0], 16))
            t_type = msg[2]

            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]+
                ' unit: '+u_code+
                ' command: '+commands[msg[8]]
            )
            pload_msg = (
                ' battery: '+str(int(msg[9][1], 16))+
                ' signal: '+str(int(msg[9][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]+
                ' unit: '+u_code
            )
            msg_value = (
                ' command: '+commands[msg[8]]+
                ' battery: '+str(int(msg[9][1], 16))+
                ' signal: '+str(int(msg[9][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+' '+msg[5]+' '+msg[6]+
                ' '+
                u_code
            )
            decode_param = None
            try:
                decode_param = self.decode_018_019_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_018_019_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_020(self, msg):
        types = {
            '00': 'X10 security door/window sensor',
            '01': 'X10 security motion sensor',
            '02': 'X10 security remote',
            '03': 'KD101',
            '04': 'Visonic PowerCode door/window sensor',
            '05': 'Visonic PowerCode motion sensor',
            '06': 'Visonic CodeSecure',
            '07': 'Visonic PowerCode door/window sensor � auxiliary contact',
            '08': 'Meiantech',
            '09': 'Alecto SA30',
            '0a': 'RM174RF'
        }
        statuses = {
            '00': 'normal',
            '01': 'normal delayed',
            '02': 'alarm',
            '03': 'alarm delayed',
            '04': 'motion',
            '05': 'no motion',
            '06': 'panic',
            '07': 'end panic',
            '08': 'tamper',
            '09': 'arm away',
            '0a': 'arm away delayed',
            '0b': 'arm home',
            '0c': 'arm home delayed',
            '0d': 'disarm',
            '10': 'light 1 off',
            '11': 'light 1 on',
            '12': 'light 2 off',
            '13': 'light 2 on',
            '14': 'dark detected',
            '15': 'light detected',
            '16': 'battery low SD18, CO18',
            '17': 'pair KD101/SA30/RM174RF',
            '80': 'Normal + Tamper',
            '81': 'Normal Delayed + Tamper',
            '82': 'Alarm + Tamper',
            '83': 'Alarm Delayed + Tamper',
            '84': 'Motion + Tamper',
            '85': 'No Motion + Tamper'
        }
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]+
                ' status: '+statuses[msg[7]]
            )
            pload_msg = (
                ' battery: '+str(int(msg[8][1], 16))+
                ' signal: '+str(int(msg[8][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+msg[4]+' '+msg[5]+' '+msg[6]
            )
            msg_value = (
                ' status: '+statuses[msg[7]]+
                ' battery: '+str(int(msg[8][1], 16))+
                ' signal: '+str(int(msg[8][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                msg[4]+' '+msg[5]+' '+msg[6]
            )
            decode_param = None
            mon_param = None
            try:
                decode_param = self.decode_020_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            if (
                types[msg[2]]=='00' or
                types[msg[2]]=='01' or
                types[msg[2]]=='04' or
                types[msg[2]]=='05'
            ):
                try:
                    mon_param = self.monitor_020_mem[base_msg]
                except:
                    pass
                self.monitor_020_mem[base_msg] = self.eventMonitor(
                    mon_param,
                    decode_param,
                    base_msg,
                    15000.0 #250 minutes timeout
                )
            self.decode_020_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_021(self, msg):
        types = {
            '00': 'Classic KeeLoq',
            '01': 'Rolling Code KeeLoq',
            '02': 'AES KeeLoq'
        }
        try:
            id = ''
            for i in range(4, 13):
                id += msg[i]+' '
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+id
            )
            pload_msg = (
                ' battery: '+str(int(msg[28][1], 16))+
                ' signal: '+str(int(msg[28][0], 16))
            )
            msg_key = (
                'Type: '+types[msg[2]]+
                ' id: '+id
            )
            msg_value = (
                ' battery: '+str(int(msg[28][1], 16))+
                ' signal: '+str(int(msg[28][0], 16))
            )
            m_key = (
                types[msg[2]]+
                ' '+
                id
            )
            decode_param = None
            try:
                decode_param = self.decode_021_mem[msg_key]
            except:
                pass
            self.eventTrigger2(
                decode_param,
                base_msg,            
                pload_msg,
                msg_value,
                m_key
            )
            self.decode_021_mem[msg_key] = msg_value
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_030_0(self, msg):
        types = {
            '00': 'ATI Remote Wonder',
            '01': 'ATI Remote Wonder Plus',
            '02': 'Medion Remote',
            '03': 'X10 PC Remote'
        }
        self.remotekey = ''
        
        if msg[2] == '00':
            ATI_Remote_Wonder = {
                '00':'A',
                '01':'B',
                '02':'power',
                '03':'TV',
                '04':'DVD',
                '05':'?',
                '06':'Guide',
                '07':'Drag',
                '08':'VOL+',
                '09':'VOL-',
                '0a':'MUTE',
                '0b':'CHAN+',
                '0c':'CHAN-',
                '0d':'1',
                '0e':'2',
                '0f':'3',
                '10':'4',
                '11':'5',
                '12':'6',
                '13':'7',
                '14':'8',
                '15':'9',
                '16':'txt',
                '17':'0',
                '18':'snapshot ESC',
                '19':'C',
                '1a':'^',
                '1b':'D',
                '1c':'TV/RADIO',
                '1d':'<',
                '1e':'OK',
                '1f':'>',
                '20':'<-',
                '21':'E',
                '22':'v',
                '23':'F',
                '24':'Rewind',
                '25':'Play',
                '26':'Fast forward',
                '27':'Record',
                '28':'Stop',
                '29':'Pause',
                '2c':'TV',
                '2d':'VCR',
                '2e':'RADIO',
                '2f':'TV Preview',
                '30':'Channel list',
                '31':'Video Desktop',
                '32':'red',
                '33':'green',
                '34':'yellow',
                '35':'blue',
                '36':'rename TAB',
                '37':'Acquire image',
                '38':'edit image',
                '39':'Full screen',
                '3a':'DVD Audio',
                '70':'Cursor-left',
                '71':'Cursor-right',
                '72':'Cursor-up',
                '73':'Cursor-down',
                '74':'Cursor-up-left',
                '75':'Cursor-up-right',
                '76':'Cursor-down-right',
                '77':'Cursor-down-left',
                '78':'V',
                '79':'V-End',
                '7c':'X',
                '7d':'X-End'
            }
            self.remotekey = ATI_Remote_Wonder[msg[5]]

        if msg[2] == '01':
            ATI_plus = {
                '00':'A',
                '01':'B',
                '02':'power',
                '03':'TV',
                '04':'DVD',
                '05':'?',
                '06':'Guide',
                '07':'Drag',
                '08':'VOL+',
                '09':'VOL-',
                '0a':'MUTE',
                '0b':'CHAN+',
                '0c':'CHAN-',
                '0d':'1',
                '0e':'2',
                '0f':'3',
                '10':'4',
                '11':'5',
                '12':'6',
                '13':'7',
                '14':'8',
                '15':'9',
                '16':'txt',
                '17':'0',
                '18':'Open Setup Menu',
                '19':'C',
                '1a':'^',
                '1b':'D',
                '1c':'FM',
                '1d':'<',
                '1e':'OK',
                '1f':'>',
                '20':'Max/Restore window',
                '21':'E',
                '22':'v',
                '23':'F',
                '24':'Rewind',
                '25':'Play',
                '26':'Fast forward',
                '27':'Record',
                '28':'Stop',
                '29':'Pause',
                '2a':'TV2',
                '2b':'Clock',
                '2c':'i',
                '2d':'ATI',
                '2e':'RADIO',
                '2f':'TV Preview',
                '30':'Channel list',
                '31':'Video Desktop',
                '32':'red',
                '33':'green',
                '34':'yellow',
                '35':'blue',
                '36':'rename TAB',
                '37':'Acquire image',
                '38':'edit image',
                '39':'Full screen',
                '3a':'DVD Audio',
                '70':'Cursor-left',
                '71':'Cursor-right',
                '72':'Cursor-up',
                '73':'Cursor-down',
                '74':'Cursor-up-left',
                '75':'Cursor-up-right',
                '76':'Cursor-down-right',
                '77':'Cursor-down-left',
                '78':'Left Mouse Button',
                '79':'V-End',
                '7c':'Right Mouse Button',
                '7d':'X-End'
            }
            self.remotekey = ATI_plus[msg[5]]

        if msg[2] == '02':
            Medion = {
                '00':'Mute',
                '01':'B',
                '02':'power',
                '03':'TV',
                '04':'DVD',
                '05':'Photo',
                '06':'Music',
                '07':'Drag',
                '08':'VOL-',
                '09':'VOL+',
                '0a':'MUTE',
                '0b':'CHAN+',
                '0c':'CHAN-',
                '0d':'1',
                '0e':'2',
                '0f':'3',
                '10':'4',
                '11':'5',
                '12':'6',
                '13':'7',
                '14':'8',
                '15':'9',
                '16':'txt',
                '17':'0',
                '18':'snapshot ESC',
                '19':'DVD MENU',
                '1a':'^',
                '1b':'Setup',
                '1c':'TV/RADIO',
                '1d':'<',
                '1e':'OK',
                '1f':'>',
                '20':'<-',
                '21':'E',
                '22':'v',
                '23':'F',
                '24':'Rewind',
                '25':'Play',
                '26':'Fast forward',
                '27':'Record',
                '28':'Stop',
                '29':'Pause',
                '2c':'TV',
                '2d':'VCR',
                '2e':'RADIO',
                '2f':'TV Preview',
                '30':'Channel list',
                '31':'Video Desktop',
                '32':'red',
                '33':'green',
                '34':'yellow',
                '35':'blue',
                '36':'rename TAB',
                '37':'Acquire image',
                '38':'edit image',
                '39':'Full screen',
                '3a':'DVD Audio',
                '70':'Cursor-left',
                '71':'Cursor-right',
                '72':'Cursor-up',
                '73':'Cursor-down',
                '74':'Cursor-up-left',
                '75':'Cursor-up-right',
                '76':'Cursor-down-right',
                '77':'Cursor-down-left',
                '78':'V',
                '79':'V-End',
                '7c':'X',
                '7d':'X-End'
            }    
            self.remotekey = Medion[msg[5]]

        if msg[2] == '03':
            PCremote = {
                '02':'0',
                '82':'1',
                'd1':'MP3',
                '42':'2',
                'd2':'DVD',
                'c2':'3',
                'd3':'CD',
                '22':'4',
                'd4':'PC or SHIFT-4',
                'a2':'5',
                'd5':'SHIFT-5',
                '62':'6',
                'e2':'7',
                '12':'8',
                '92':'9',
                'c0':'CH-',
                '40':'CH+',
                'e0':'VOL-',
                '60':'VOL+',
                'a0':'MUTE',
                '3a':'INFO',
                '38':'REW',
                'b8':'FF',
                'b0':'PLAY',
                '64':'PAUSE',
                '63':'STOP',
                'b6':'MENU',
                'ff':'REC',
                'c9':'EXIT',
                'd8':'TEXT',
                'd9':'SHIFT-TEXT',
                'f2':'TELETEXT',
                'd7':'SHIFT-TELETEXT',
                'ba':'A+B',
                '52':'ENT',
                'd6':'SHIFT-ENT',
                '70':'Cursor-left',
                '71':'Cursor-right',
                '72':'Cursor-up',
                '73':'Cursor-down',
                '74':'Cursor-up-left',
                '75':'Cursor-up-right',
                '76':'Cursor-down-right',
                '77':'Cursor-down-left',
                '78':'Left mouse',
                '79':'Left mouse-End',
                '7b':'Drag',
                '7c':'Right mouse',
                '7d':'Right mouse-End'
            }
            self.remotekey = PCremote[msg[5]]

        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+str(int(msg[4], 16))+
                ' remotekey: '+self.remotekey
            )
            print base_msg
            pload_msg = (
                ' signal: '+str(int(msg[6][0], 16))
            )
            print pload_msg
            self.eventRemote(
                base_msg,            
                pload_msg
            )
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def decode_030_1(self, msg):
        types = {
            '04': 'ATI Remote Wonder II'
        }
        cmndtypes = {
            '0':'PC',
            '2':'AUX1',
            '4':'AUX2',
            '6':'AUX3',
            '8':'AUX4'
        }
        self.remotekey = ''
        
        ATI_Remote_Wonder_II = {
            '00':'A',
            '01':'B',
            '02':'power',
            '03':'TV',
            '04':'DVD',
            '05':'?',
            '06':'�',
            '07':'Drag',
            '08':'VOL+',
            '09':'VOL-',
            '0A':'MUTE',
            '0B':'CHAN+',
            '0C':'CHAN-',
            '0D':'1',
            '0E':'2',
            '0F':'3',
            '10':'4',
            '11':'5',
            '12':'6',
            '13':'7',
            '14':'8',
            '15':'9',
            '16':'txt',
            '17':'0',
            '18':'Open Setup Menu',
            '19':'C',
            '1A':'^',
            '1B':'D',
            '1C':'TV/RADIO',
            '1D':'<',
            '1E':'OK',
            '1F':'>',
            '20':'Max/Restore Window',
            '21':'E',
            '22':'v',
            '23':'F',
            '24':'Rewind',
            '25':'Play',
            '26':'Fast forward',
            '27':'Record',
            '28':'Stop',
            '29':'Pause',
            '2D':'ATI',
            '3B':'PC',
            '3C':'AUX1',
            '3D':'AUX2',
            '3E':'AUX3',
            '3F':'AUX4',
            '70':'Cursor-left',
            '71':'Cursor-right',
            '72':'Cursor-up',
            '73':'Cursor-down',
            '74':'Cursor-up-left',
            '75':'Cursor-up-right',
            '76':'Cursor-down-right',
            '77':'Cursor-down-left',
            '78':'Left Mouse Button',
            '7C':'Right Mouse Button'
        }
        self.remotekey = ATI_Remote_Wonder_II[msg[5].upper()]
        cmndtype = cmndtypes[str(int(msg[6][1], 16) & int('E', 16))]
        try:
            base_msg = (
                'Type: '+types[msg[2]]+
                ' id: '+str(int(msg[4], 16))+
                ' remotekey: '+self.remotekey
            )
            pload_msg = (
                ' cmndtype: '+cmndtype+
                ' signal: '+str(int(msg[6][0], 16))
            )
            self.eventRemote(
                base_msg,            
                pload_msg
            )
        except:
            eg.PrintError(self.text.decodeError + str(msg))


    def Configure(
        self,
        port = 0,
        bLogToFile = False,
        bDebug = False,
        b01 = True,
        b02 = True,
        b03 = True,
        b04 = True,
        b05 = True,
        b06 = True,
        b07 = True,
        b08 = True,
        b09 = True,
        b0a = True,
        b0b = True,
        b0c = True,
        b0d = True,
        b0e = True,
        b0f = True,
        mMacroNames = True,
        bDupEvents = False,
        websocket_port_nbr = 1234,
        use_websockets = False,
        b10 = True,
        use_tornadoWebsockets = False,
        prefix = 'RFXtrx'
    ):
        text = self.text
        panel = eg.ConfigPanel()
        mySizer = wx.GridBagSizer(7, 7)

        staticBox = wx.StaticBox(panel, -1, self.text.decode_advice)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        sizer00 = wx.BoxSizer(wx.HORIZONTAL)
        staticBoxSizer.Add(sizer00, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        font = panel.GetFont()
        p = font.GetPointSize()

        font.SetPointSize(8)
        font.SetWeight(wx.NORMAL)
        panel.SetFont(font)

        portCtrl = panel.SerialPortChoice(port)
        panel.SetColumnFlags(1, wx.EXPAND)
        portSettingsBox = panel.BoxedGroup(
            "Port settings",
            (text.port, portCtrl),
        )
        eg.EqualizeWidths(portSettingsBox.GetColumnItems(0))
        panel.sizer.Add(
            eg.HBoxSizer(portSettingsBox)
        )

        bLogToFileCtrl = wx.CheckBox(panel, -1, "")
        bLogToFileCtrl.SetValue(bLogToFile)
        staticBox = wx.StaticBox(panel, -1, self.text.logToFile)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(bLogToFileCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a textfield for action name 
        prefixCtrl = wx.TextCtrl(panel, -1, prefix)
        staticBox = wx.StaticBox(panel, -1, self.text.set_prefix)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(prefixCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        bDupEventsCtrl = wx.CheckBox(panel, -1, "")
        bDupEventsCtrl.SetValue(bDupEvents)
        staticBox = wx.StaticBox(panel, -1, self.text.dupEvents)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(bDupEventsCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        bDebugCtrl = wx.CheckBox(panel, -1, "")
        bDebugCtrl.SetValue(bDebug)
        staticBox = wx.StaticBox(panel, -1, self.text.debugInfo)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(bDebugCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        mMacroNamesCtrl = wx.CheckBox(panel, -1, "")
        mMacroNamesCtrl.SetValue(mMacroNames)
        staticBox = wx.StaticBox(panel, -1, self.text.macroNames)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(mMacroNamesCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        bWebSocketCtrl = wx.CheckBox(panel, -1, "")
        bWebSocketCtrl.SetValue(use_websockets)
        staticBox = wx.StaticBox(panel, -1, self.text.use_websockets)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(bWebSocketCtrl, 1, wx.EXPAND)
#        websocket_port_nbr_ctrl = panel.SpinIntCtrl(websocket_port_nbr, 1234, 1500)
#        websocket_port_nbr_ctrl.SetInitialSize((30,-1))
#        sizer2.Add(websocket_port_nbr_ctrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        bTornadoWebSocketCtrl = wx.CheckBox(panel, -1, "")
        bTornadoWebSocketCtrl.SetValue(use_tornadoWebsockets)
        staticBox = wx.StaticBox(panel, -1, self.text.use_tornadoWebsockets)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(bTornadoWebSocketCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
                bLogToFileCtrl.GetValue(),
                bDebugCtrl.GetValue(),
                b01,
                b02,
                b03,
                b04,
                b05,
                b06,
                b07,
                b08,
                b09,
                b0a,
                b0b,
                b0c,
                b0d,
                b0e,
                b0f,
                mMacroNamesCtrl.GetValue(),
                bDupEventsCtrl.GetValue(),
                websocket_port_nbr,
                bWebSocketCtrl.GetValue(),
                b10,
                bTornadoWebSocketCtrl.GetValue(),
                prefixCtrl.GetValue()
            )



class send_Home_Confort(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Home Confort, TEL-010': '00'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44'
        }            
        commands = {
            'off': '00',
            'on': '01',
            'group Off': '02',
            'group On': '03'
        }
        msg = (
            '0C 1B '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00 00 00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Home Confort, TEL-010'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for unit code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'group Off',
            'group On'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
       
        while panel.Affirmed():
            command = commandCtrl.GetStringSelection()
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Home_Confort', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(),
                command,
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Home_Confort', nameCtrl.GetValue(), my_macro_indx
            )



class send_X10(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'X10 lighting': '00'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'off': '00',
            'on': '01',
            'dim': '02',
            'bright': '03',
            'all off': '05',
            'all on': '06'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+
            ' '+
            housecode+
            ' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)
       

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'X10 lighting'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'on',
            'off',
            'dim',
            'bright',
            'all on',
            'all off'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_X10', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_X10', nameCtrl.GetValue(), my_macro_indx
            )



class send_ARC(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'ARC': '01'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'off': '00',
            'on': '01',
            'all off': '05',
            'all on': '06',
            'chime': '07'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'ARC'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'on',
            'off',
            'all on',
            'all off',
            'chime'
            
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_ARC', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_ARC', nameCtrl.GetValue(), my_macro_indx
            )


class send_Waveman(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Waveman': '03'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'off': '00',
            'on': '01'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Waveman'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',            
            'on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Waveman', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Waveman', nameCtrl.GetValue(), my_macro_indx
            )


class send_Chacon_EMW200(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Chacon EMW200': '04'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04'
        }
        commands = {
            'off': '00',
            'on': '01',
            'all off': '05',
            'all on': '06'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Chacon EMW200'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',            
            'on',
            'all off',
            'all on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Chacon_EMW200', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Chacon_EMW200', nameCtrl.GetValue(), my_macro_indx
            )



class send_ELRO_AB400D(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'ELRO AB400D': '02'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10',
            '17': '11',
            '18': '12',
            '19': '13',
            '20': '14',
            '21': '15',
            '22': '16',
            '23': '17',
            '24': '18',
            '25': '19',
            '26': '1A',
            '27': '1B',
            '28': '1C',
            '29': '1D',
            '30': '1E',
            '31': '1F',
            '32': '20',
            '33': '21',
            '34': '22',
            '35': '23',
            '36': '24',
            '37': '25',
            '38': '26',
            '39': '27',
            '40': '28',
            '41': '29',
            '42': '2A',
            '43': '2B',
            '44': '2C',
            '45': '2D',
            '46': '2E',
            '47': '2F',
            '48': '30',
            '49': '31',
            '50': '32',
            '51': '33',
            '52': '34',
            '53': '35',
            '54': '36',
            '55': '37',
            '56': '38',
            '57': '39',
            '58': '3A',
            '59': '3B',
            '60': '3C',
            '61': '3D',
            '62': '3E',
            '63': '3F',
            '64': '40'
        }
        commands = {
            'off': '00',
            'on': '01'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'ELRO AB400D'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22',
            '23', '24', '25', '26', '27', '28', '29', '30', '31', '32',
            '33', '34', '35', '36', '37', '38', '39', '40', '41', '42',
            '43', '44', '45', '46', '47', '48', '49', '50', '51', '52',
            '53', '54', '55', '56', '57', '58', '59', '60', '61', '62',
            '63', '64'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'on',
            'off'            
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_ELRO_AB400D', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_ELRO_AB400D', nameCtrl.GetValue(), my_macro_indx
            )



class send_IMPULS(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'IMPULS': '05'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10',
            '17': '11',
            '18': '12',
            '19': '13',
            '20': '14',
            '21': '15',
            '22': '16',
            '23': '17',
            '24': '18',
            '25': '19',
            '26': '1A',
            '27': '1B',
            '28': '1C',
            '29': '1D',
            '30': '1E',
            '31': '1F',
            '32': '20',
            '33': '21',
            '34': '22',
            '35': '23',
            '36': '24',
            '37': '25',
            '38': '26',
            '39': '27',
            '40': '28',
            '41': '29',
            '42': '2A',
            '43': '2B',
            '44': '2C',
            '45': '2D',
            '46': '2E',
            '47': '2F',
            '48': '30',
            '49': '31',
            '50': '32',
            '51': '33',
            '52': '34',
            '53': '35',
            '54': '36',
            '55': '37',
            '56': '38',
            '57': '39',
            '58': '3A',
            '59': '3B',
            '60': '3C',
            '61': '3D',
            '62': '3E',
            '63': '3F',
            '64': '40'
        }
        commands = {
            'off': '00',
            'on': '01'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'IMPULS'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22',
            '23', '24', '25', '26', '27', '28', '29', '30', '31', '32',
            '33', '34', '35', '36', '37', '38', '39', '40', '41', '42',
            '43', '44', '45', '46', '47', '48', '49', '50', '51', '52',
            '53', '54', '55', '56', '57', '58', '59', '60', '61', '62',
            '63', '64'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',            
            'on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_IMPULS', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_IMPULS', nameCtrl.GetValue(), my_macro_indx
            )



class send_RisingSun(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'RisingSun': '06'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04'
        }
        commands = {
            'off': '00',
            'on': '01'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'RisingSun'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',            
            'on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_RisingSun', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_RisingSun', nameCtrl.GetValue(), my_macro_indx
            )



class send_HQ_COCO_20(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'HQ COCO-20': '0B'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10',
            '17': '11',
            '18': '12',
            '19': '13',
            '20': '14',
            '21': '15',
            '22': '16',
            '23': '17',
            '24': '18',
            '25': '19',
            '26': '1A',
            '27': '1B',
            '28': '1C',
            '29': '1D',
            '30': '1E',
            '31': '1F',
            '32': '20',
            '33': '21',
            '34': '22',
            '35': '23',
            '36': '24',
            '37': '25',
            '38': '26',
            '39': '27',
            '40': '28',
            '41': '29',
            '42': '2A',
            '43': '2B',
            '44': '2C',
            '45': '2D',
            '46': '2E',
            '47': '2F',
            '48': '30',
            '49': '31',
            '50': '32',
            '51': '33',
            '52': '34',
            '53': '35',
            '54': '36',
            '55': '37',
            '56': '38',
            '57': '39',
            '58': '3A',
            '59': '3B',
            '60': '3C',
            '61': '3D',
            '62': '3E',
            '63': '3F',
            '64': '40'
        }
        commands = {
            'off': '00',
            'on': '01'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'HQ COCO-20'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16', '17', '18', '19', '20', '21', '22',
            '23', '24', '25', '26', '27', '28', '29', '30', '31', '32',
            '33', '34', '35', '36', '37', '38', '39', '40', '41', '42',
            '43', '44', '45', '46', '47', '48', '49', '50', '51', '52',
            '53', '54', '55', '56', '57', '58', '59', '60', '61', '62',
            '63', '64'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',            
            'on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_HQ_COCO_20', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_HQ_COCO_20', nameCtrl.GetValue(), my_macro_indx
            )



class send_COCO_GDR2_2000R(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'COCO GDR2-2000R': '0A'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04'
        }
        commands = {
            'off': '00',
            'on': '01'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'COCO GDR2-2000R'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',            
            'on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_COCO_GDR2_2000R', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_COCO_GDR2_2000R', nameCtrl.GetValue(), my_macro_indx
            )



class send_Energenie(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Energenie': '08'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04'
        }
        commands = {
            'off': '00',
            'on': '01',
            'all off': '05',
            'all on': '06'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Energenie'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',            
            'on',
            'all off',
            'all on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Energenie', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Energenie', nameCtrl.GetValue(), my_macro_indx
            )



class send_Energenie_5g(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Energenie 5-gang': '09'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A'
        }
        commands = {
            'off': '00',
            'on': '01'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Energenie 5-gang'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',            
            'on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Energenie_5g', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Energenie_5g', nameCtrl.GetValue(), my_macro_indx
            )



class send_Philips_SBC(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Philips SBC': '07'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'off': '00',
            'on': '01',
            'all off': '05',
            'all on': '06'
        }
        msg = (
            '07 10 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Philips SBC'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',            
            'on',
            'all off',
            'all on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Philips_SBC', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Philips_SBC', nameCtrl.GetValue(), my_macro_indx
            )



class send_Kambrook(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        id_4,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Kambrook RF3672 (Australia)': '03'
        }
        id1_code = {
            'A': '00',
            'B': '01',
            'C': '02',
            'D': '03'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05'
        }
        commands = {
            'off': '00',
            'on': '01'
        }
        msg = (
            '0B 11 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+id_4+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )

        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+id_4+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+id_4+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="A",
        id_2="00",
        id_3="00",
        id_4="01",
        unitcode="",
        command="",
        my_macro_indx = None
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Kambrook RF3672 (Australia)'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                'A', 'B', 'C', 'D'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))
        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for ID 4
        id_4_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_4_Ctrl.AppendItems(list) 
        if list.count(id_4)==0:
            id_4_Ctrl.Select(n=0)
        else:
            id_4_Ctrl.SetSelection(int(list.index(id_4)))
        sizer2.Add(id_4_Ctrl,  (0,3))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_4_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for device unit
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Kambrook', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                id_4_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(), 
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Kambrook', nameCtrl.GetValue(), my_macro_indx
            )



class send_AC(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        address,
        unitcode,
        command,
        level,
        my_macro_indx
    ):
        protocols = {
            'AC': '00',
            'HomeEasy EU': '01',
            'ANSLUT': '02'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'off': '00',
            'on': '01',
            'set level': '02',
            'group Off': '03',
            'group On': '04',
            'Set group level': '05'
        }
        msg = (
            '0B 11 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(address)+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '0'+str(hex(int(level)))[2]+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            address+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            address+' '+
            unitcode+' '+
            command+' '+
            level
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)
        CurrentStateData.dimStepWise[w_key] = level
        

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        address="00 00 00 01",
        unitcode="",
        command="",
        level='0',
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'AC',
            'HomeEasy EU',
            'ANSLUT'
        ]
        protocolCtrl.AppendItems(list)
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a textfield for address 
        addressCtrl = wx.TextCtrl(panel, -1, address)

        staticBox = wx.StaticBox(panel, -1, text.textBoxAddress)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(addressCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unit
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(list)
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'set level',
            'group Off',
            'group On',
            'Set group level'
        ]
        commandCtrl.AppendItems(list)
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for dim level
        levelCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15'
        ]
        levelCtrl.AppendItems(list)
        if list.count(level)==0:
            levelCtrl.Select(n=0)
        else:
            levelCtrl.SetSelection(int(list.index(level)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxLevel)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(levelCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        levelCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_AC', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                addressCtrl.GetValue(), 
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(), 
                levelCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_AC', nameCtrl.GetValue(), my_macro_indx
            )



class DimStepWise_AC(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        address,
        unitcode,
        bStepUp,
        level,
        my_macro_indx
    ):
        protocols = {
            'AC': '00'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        self.protocol = protocols[protocol]
        self.address = address
        self.unitcode = unitcodes[unitcode]
        self.bStepUp = bStepUp
        self.level = level
        self.DimStepWise()
        return CurrentStateData.dimStepWise
        
        
    def DimStepWise(self):
        ref_level = 0
        the_level = 0
        to_send = 0
        k_msg = ''
        m_key = (
            str(self.protocol)+
            ' '+
            str(self.address)+
            ' '+
            str(self.unitcode)
        )
        try:
            ref_level = int(CurrentStateData.dimStepWise[m_key])
            the_level = ref_level
        except:
            pass           

        if self.bStepUp: 
            the_level += int(self.level)
            if the_level < 0:
                to_send = 0
            else:
                to_send = the_level
            if the_level > 15:
                to_send = 15
        else:
            the_level -= int(self.level)
            if the_level < 0:
                to_send = 0
            else:
                to_send = the_level
            if the_level > 15:
                to_send = 15

        if the_level > 0:
            msg = (
                '0B 11 '+
                str(self.protocol)+' '+
                '00'+' '+
                str(self.address)+' '+
                str(self.unitcode)+' '+
                '02'+' '+
                '0'+str(hex(int(to_send)))[2]+' '+
                '00'
            )
        else:
            msg = (
                '0B 11 '+
                str(self.protocol)+' '+
                '00'+' '+
                str(self.address)+' '+
                str(self.unitcode)+' '+
                '00'+' '+
                '0'+str(hex(int(to_send)))[2]+' '+
                '00'
            )
        k_msg = (
            str(the_level)
        )
        self.plugin.WriteMsg(msg, '', '')
        
        if ref_level >= 0 and ref_level <= 15:
            if the_level <> ref_level:
                CurrentStateData.dimStepWise[m_key] = k_msg

        if ref_level < 0 :
            if the_level > ref_level:
                CurrentStateData.dimStepWise[m_key] = k_msg
        
        if ref_level > 15 :
            if the_level < ref_level:
                CurrentStateData.dimStepWise[m_key] = k_msg

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name = 'Dim up/down in steps',
        protocol = 'AC',
        address = '00 00 00 01',
        unitcode = '1',
        bStepUp = True,
        level = '1',
        my_macro_indx = None
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
    
        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
    
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'AC'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
    
        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
    
        # Create a textfield for address 
        addressCtrl = wx.TextCtrl(panel, -1, address)
    
        staticBox = wx.StaticBox(panel, -1, text.textBoxAddress)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(addressCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unit
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))
    
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a checkbox for step up/down
        staticBox = wx.StaticBox(panel, -1, text.textStep_up)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        bStepUpCtrl = wx.CheckBox(panel, -1, "")
        bStepUpCtrl.SetValue(bStepUp)
        sizer3.Add(bStepUpCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for dim step size
        levelCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15'
        ]
        levelCtrl.AppendItems(list) 
        if list.count(level)==0:
            levelCtrl.Select(n=0)
        else:
            levelCtrl.SetSelection(int(list.index(level)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxStepSize)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(levelCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        levelCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'DimStepWise_AC', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(),
                protocolCtrl.GetStringSelection(),
                addressCtrl.GetValue(),
                deviceCtrl.GetStringSelection(),
                bStepUpCtrl.GetValue(),
                levelCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'DimStepWise_AC', nameCtrl.GetValue(), my_macro_indx
            )



class DimGradually_AC(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        address,
        unitcode,
        timeInBetween,
        level,
        my_macro_indx
    ):
        protocols = {
            'AC': '00'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }

        self.protocol = protocols[protocol]
        self.address = address
        self.unitcode = unitcodes[unitcode]
        self.timeInBetween = timeInBetween
        self.level = level
        self.finished = Event()
        self.DimGradually = Thread(
            target=self.DimGraduallyThread,
            name="DimGradually"
        )
        self.DimGradually.start()

        
    def DimGraduallyThread(self):
        start_level = 0
        k_msg = ''
        m_key = (
            str(self.protocol)+
            ' '+
            str(self.address)+
            ' '+
            str(self.unitcode)
        )
        try:
            start_level = int(CurrentStateData.dimStepWise[m_key])
            #print self.plugin.dimGradually
        except:
            pass           

        while not self.finished.isSet():
            if start_level >= int(self.level):
                while start_level >= int(self.level):
                    #print start_level
                    msg = (
                        '0B 11 '+
                        str(self.protocol)+' '+
                        '00'+' '+
                        str(self.address)+' '+
                        str(self.unitcode)+' '+
                        '02'+' '+
                        '0'+str(hex(int(start_level)))[2]+' '+
                        '00'
                    )
                    k_msg = (
                        str(start_level)
                    )
                    
                    if start_level == 0:
                        msg = (
                            '0B 11 '+
                            str(self.protocol)+' '+
                            '00'+' '+
                            str(self.address)+' '+
                            str(self.unitcode)+' '+
                            '00'+' '+
                            '0'+str(hex(int(start_level)))[2]+' '+
                            '00'
                        )

                    self.plugin.WriteMsg(msg, '', '')
                    start_level -= 1
                    self.finished.wait(self.timeInBetween)

            elif start_level < int(self.level):
                while start_level <= int(self.level):
                    #print start_level
                    msg = (
                        '0B 11 '+
                        str(self.protocol)+' '+
                        '00'+' '+
                        str(self.address)+' '+
                        str(self.unitcode)+' '+
                        '02'+' '+
                        '0'+str(hex(int(start_level)))[2]+' '+
                        '00'
                    )
                    k_msg = (
                        str(start_level)
                    )
                    self.plugin.WriteMsg(msg, '', '')
                    start_level += 1
                    self.finished.wait(self.timeInBetween)

            CurrentStateData.dimStepWise[m_key] = k_msg
            self.finished.set()

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name = 'I can be dimmed gradually',
        protocol = 'AC',
        address = '00 00 00 01',
        unitcode = '1',
        timeInBetween = 0.30,
        level = '15',
        my_macro_indx = None
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
    
        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
    
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'AC'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
    
        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
    
        # Create a textfield for address 
        addressCtrl = wx.TextCtrl(panel, -1, address)
    
        staticBox = wx.StaticBox(panel, -1, text.textBoxAddress)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(addressCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unit
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))
    
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for time delay between commands
        staticBox = wx.StaticBox(panel, -1, text.timeInBetween_txt)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.GridBagSizer(10, 10)
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
        sizer3.Add(timeInBetweenCtrl,(0,0))
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, flag = wx.EXPAND)

        # Create a dropdown for dim level
        levelCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15'
        ]
        levelCtrl.AppendItems(list) 
        if list.count(level)==0:
            levelCtrl.Select(n=0)
        else:
            levelCtrl.SetSelection(int(list.index(level)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxLevel)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(levelCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        levelCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'DimGradually_AC', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(),
                protocolCtrl.GetStringSelection(),
                addressCtrl.GetValue(),
                deviceCtrl.GetStringSelection(),
                timeInBetweenCtrl.GetValue(),
                levelCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'DimGradually_AC', nameCtrl.GetValue(), my_macro_indx
            )
    


class GoodMorning_AC(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        address,
        unitcode,
        timeToWakeUp,
        my_macro_indx
    ):
        protocols = {
            'AC': '00'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }

        self.protocol = protocols[protocol]
        self.address = address
        self.unitcode = unitcodes[unitcode]
        self.increase = int(256/(timeToWakeUp*3))
        self.finished = Event()
        self.GoodMorning = Thread(
            target=self.GoodMorningThread,
            name="GoodMorning"
        )
        self.GoodMorning.start()

        
    def GoodMorningThread(self):
        while not self.finished.isSet():
            level=1
            while level < 256:
                #print level
                msg = (
                    '0B 11 '+
                    str(self.protocol)+' '+
                    '00'+' '+
                    str(self.address)+' '+
                    str(self.unitcode)+' '+
                    '02'+' '+
                    '0'+str(hex(int(level)))[2]+' '+
                    '00'
                )
                self.plugin.WriteMsg(msg, '', '')
                level += self.increase
                self.finished.wait(20.0)
            self.finished.set()
        time.sleep(0.1)
        msg = (
            '0B 11 '+
            str(self.protocol)+' '+
            '00'+' '+
            str(self.address)+' '+
            str(self.unitcode)+' '+
            '02'+' '+
            '0'+str(hex(int(255)))[2]+' '+
            '00'
        )
        self.plugin.WriteMsg(msg, '', '')
        print "Good Morning action finished"

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="I could be a wake up lamp",
        protocol="",
        address="00 00 00 01",
        unitcode="",
        timeToWakeUp=15,
        my_macro_indx = None
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
    
        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
    
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'AC'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
    
        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
    
        # Create a textfield for address 
        addressCtrl = wx.TextCtrl(panel, -1, address)
    
        staticBox = wx.StaticBox(panel, -1, text.textBoxAddress)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(addressCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unit
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))
    
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        staticBox = wx.StaticBox(panel, -1, text.timeToWakeUp_txt)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        timeToWakeUpCtrl = wx.Slider(
                            panel,
                            -1,
                            timeToWakeUp,
                            0,
                            100,
                            (10, 10),
                            (200, 50),
                            wx.SL_HORIZONTAL | wx.SL_LABELS
                         )
        sizer3.Add(timeToWakeUpCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                addressCtrl.GetValue(), 
                deviceCtrl.GetStringSelection(),
                timeToWakeUpCtrl.GetValue(),
                my_macro_indx
            )      
    


class GoodNight_AC(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        address,
        unitcode,
        timeToWakeUp,
        my_macro_indx
    ):
        protocols = {
            'AC': '00'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }

        self.protocol = protocols[protocol]
        self.address = address
        self.unitcode = unitcodes[unitcode]
        self.increase = int(256/(timeToWakeUp*3))
        self.finished = Event()
        self.GoodNight = Thread(
            target=self.GoodNightThread,
            name="GoodNight"
        )
        self.GoodNight.start()

        
    def GoodNightThread(self):
        while not self.finished.isSet():
            level=255
            while level >= 0:
                #print level
                msg = (
                    '0B 11 '+
                    str(self.protocol)+' '+
                    '00'+' '+
                    str(self.address)+' '+
                    str(self.unitcode)+' '+
                    '02'+' '+
                    '0'+str(hex(int(level)))[2]+' '+
                    '00'
                )
                self.plugin.WriteMsg(msg, '', '')
                level -= self.increase
                self.finished.wait(20.0)
            self.finished.set()
        time.sleep(0.1)
        level = 0
        msg = (
            '0B 11 '+
            str(self.protocol)+' '+
            '00'+' '+
            str(self.address)+' '+
            str(self.unitcode)+' '+
            '00'+' '+
            '0'+str(hex(int(level)))[2]+' '+
            '00'
        )
        self.plugin.WriteMsg(msg, '', '')
        print "Good Night action finished"

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="I could be a night lamp",
        protocol="",
        address="00 00 00 01",
        unitcode="",
        timeToSleep=15,
        my_macro_indx = None
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'AC'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a textfield for address 
        addressCtrl = wx.TextCtrl(panel, -1, address)

        staticBox = wx.StaticBox(panel, -1, text.textBoxAddress)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(addressCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unit
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        staticBox = wx.StaticBox(panel, -1, text.timeToSleep_txt)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        timeToSleepCtrl = wx.Slider(
                            panel,
                            -1,
                            timeToSleep,
                            0,
                            100,
                            (10, 10),
                            (200, 50),
                            wx.SL_HORIZONTAL | wx.SL_LABELS
                         )
        sizer3.Add(timeToSleepCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                addressCtrl.GetValue(), 
                deviceCtrl.GetStringSelection(),
                timeToSleepCtrl.GetValue(),
                my_macro_indx
            )      



class send_Koppla(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        systemcode,
        ch1,
        ch2,
        ch3,
        ch4,
        ch5,
        ch6,
        ch7,
        ch8,
        ch9,
        ch10,
        command,
        my_macro_indx
    ):
        channel_list_8_1 = []
        channel_list_9_10 = [0,0,0,0,0,0]
        str_8_1 = ''
        str_10_9 = '' 

        protocols = {
            'Koppla': '00'
        }
        systems = {
            '1': '00',
            '2': '01',
            '3': '02',
            '4': '03',
            '5': '04',
            '6': '05',
            '7': '06',
            '8': '07',
            '9': '08',
            '10': '09',
            '11': '0A',
            '12': '0B',
            '13': '0C',
            '14': '0D',
            '15': '0E',
            '16': '0F'
        }            
        commands = {
            'Bright': '00',
            'Dim': '08',
            'On': '10',
            'level 1': '11',
            'level 2': '12',
            'level 3': '13',
            'level 4': '14',
            'level 5': '15',
            'level 6': '16',
            'level 7': '17',
            'level 8': '18',
            'level 9': '19',
            'Off': '1A',
            'Program': '1C'
        }

        if ch8 == True:
            channel_list_8_1.append(1)
        elif ch8 == False:
            channel_list_8_1.append(0)
        if ch7 == True:
            channel_list_8_1.append(1)
        elif ch7 == False:
            channel_list_8_1.append(0)
        if ch6 == True:
            channel_list_8_1.append(1)
        elif ch6 == False:
            channel_list_8_1.append(0)
        if ch5 == True:
            channel_list_8_1.append(1)
        elif ch5 == False:
            channel_list_8_1.append(0)
        if ch4 == True:
            channel_list_8_1.append(1)
        elif ch4 == False:
            channel_list_8_1.append(0)
        if ch3 == True:
            channel_list_8_1.append(1)
        elif ch3 == False:
            channel_list_8_1.append(0)
        if ch2 == True:
            channel_list_8_1.append(1)
        elif ch2 == False:
            channel_list_8_1.append(0)
        if ch1 == True:
            channel_list_8_1.append(1)
        elif ch1 == False:
            channel_list_8_1.append(0)
        if ch10 == True:
            channel_list_9_10.append(1)
        elif ch10 == False:
            channel_list_9_10.append(0)
        if ch9 == True:
            channel_list_9_10.append(1)
        elif ch9 == False:
            channel_list_9_10.append(0)
        
        for item in channel_list_8_1:
            str_8_1+=str(item)
        for item in channel_list_9_10:
            str_10_9+=str(item)

        channel_8_1 = '0b'+ str_8_1       
        channel_10_9 = '0b'+ str_10_9
        
        bt_8_1 = str(hex(int('0b'+ str_8_1, 2))).split('x')[1].upper()
        bt_10_9 = str(hex(int('0b'+ str_10_9, 2))).split('x')[1].upper()
        
        if len(bt_8_1)<2:
            bt_8_1 = '0'+bt_8_1
        if len(bt_10_9)<2:
            bt_10_9 = '0'+bt_10_9

        msg = (
            '08 12 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(systems[systemcode])+' '+
            bt_8_1+' '+
            bt_10_9+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(systemcode) < 2:
            systemcode = '0' + systemcode
        w_key = (
            protocol+' '+
            systemcode+' '+
            bt_8_1+' '+
            bt_10_9
        )
        w_msg = (
            protocol+' '+
            systemcode+' '+
            bt_8_1+' '+
            bt_10_9+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        systemcode="",
        ch1 = False,
        ch2 = False,
        ch3 = False,
        ch4 = False,
        ch5 = False,
        ch6 = False,
        ch7 = False,
        ch8 = False,
        ch9 = False,
        ch10 = False,
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Koppla'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for system
        systemCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', '16'
        ]
        systemCtrl.AppendItems(list) 
        if list.count(systemcode)==0:
            systemCtrl.Select(n=0)
        else:
            systemCtrl.SetSelection(int(list.index(systemcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxSystem)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(systemCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        systemCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        staticBox = wx.StaticBox(panel, -1, text.textChannel)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        
        sizer3 = wx.GridBagSizer(10, 10)
        ch1_Ctrl = wx.CheckBox(panel, -1, "")
        ch1_Ctrl.SetValue(ch1)
        sizer3.Add(wx.StaticText(panel, -1, '1'), (0,0))
        sizer3.Add(ch1_Ctrl, (1,0))
        
        ch2_Ctrl = wx.CheckBox(panel, -1, "")
        ch2_Ctrl.SetValue(ch1)
        sizer3.Add(wx.StaticText(panel, -1, '2'), (0,1))
        sizer3.Add(ch2_Ctrl, (1,1))
        
        ch3_Ctrl = wx.CheckBox(panel, -1, "")
        ch3_Ctrl.SetValue(ch3)
        sizer3.Add(wx.StaticText(panel, -1, '3'), (0,2))
        sizer3.Add(ch3_Ctrl, (1,2))
        
        ch4_Ctrl = wx.CheckBox(panel, -1, "")
        ch4_Ctrl.SetValue(ch1)
        sizer3.Add(wx.StaticText(panel, -1, '4'), (0,3))
        sizer3.Add(ch4_Ctrl, (1,3))
        
        ch5_Ctrl = wx.CheckBox(panel, -1, "")
        ch5_Ctrl.SetValue(ch1)
        sizer3.Add(wx.StaticText(panel, -1, '5'), (0,4))
        sizer3.Add(ch5_Ctrl, (1,4))
        
        ch6_Ctrl = wx.CheckBox(panel, -1, "")
        ch6_Ctrl.SetValue(ch6)
        sizer3.Add(wx.StaticText(panel, -1, '6'), (0,5))
        sizer3.Add(ch6_Ctrl, (1,5))
        
        ch7_Ctrl = wx.CheckBox(panel, -1, "")
        ch7_Ctrl.SetValue(ch7)
        sizer3.Add(wx.StaticText(panel, -1, '7'), (0,6))
        sizer3.Add(ch7_Ctrl, (1,6))
        
        ch8_Ctrl = wx.CheckBox(panel, -1, "")
        ch8_Ctrl.SetValue(ch8)
        sizer3.Add(wx.StaticText(panel, -1, '8'), (0,7))
        sizer3.Add(ch8_Ctrl, (1,7))
        
        ch9_Ctrl = wx.CheckBox(panel, -1, "")
        ch9_Ctrl.SetValue(ch9)
        sizer3.Add(wx.StaticText(panel, -1, '9'), (0,8))
        sizer3.Add(ch9_Ctrl, (1,8))
        
        ch10_Ctrl = wx.CheckBox(panel, -1, "")
        ch10_Ctrl.SetValue(ch10)
        sizer3.Add(wx.StaticText(panel, -1, '10'), (0,9))
        sizer3.Add(ch10_Ctrl, (1,9))
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)


        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Bright',
            'Dim',
            'level 1',
            'level 2',
            'level 3',
            'level 4',
            'level 5',
            'level 6',
            'level 7',
            'level 8',
            'level 9',
            'Off',
            'Program'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Koppla', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                systemCtrl.GetStringSelection(),
                ch1_Ctrl.GetValue(),
                ch2_Ctrl.GetValue(),
                ch3_Ctrl.GetValue(),
                ch4_Ctrl.GetValue(),
                ch5_Ctrl.GetValue(),
                ch6_Ctrl.GetValue(),
                ch7_Ctrl.GetValue(),
                ch8_Ctrl.GetValue(),
                ch9_Ctrl.GetValue(),
                ch10_Ctrl.GetValue(),
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Koppla', nameCtrl.GetValue(), my_macro_indx
            )
            
            
            
class send_Digimax(eg.ActionClass):

    def checkLen(self, st):
        if len(st)<2:
            st = '0'+st
        return st
        
        
    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        status,
        mode,
        temperature,
        set_point,
        my_macro_indx
    ):
        protocols = {
            'Digimax, TLX7506': '00',
            'Digimax with short format (no set point)': '01'
        }
        statuses = {
            'demand': '1',
            'no demand': '2',
            'initializing': '3'
        }
        modes = {
            'heating': '0',
            'cooling': '1'
        }
        temp = hex(temperature).split('x')[1].upper()
        temp = self.checkLen(temp)
        setp = hex(set_point).split('x')[1].upper()
        setp = self.checkLen(setp)
        st = bin(int(statuses[status]))[2:].zfill(7)
        md = modes[mode]
        res = str(hex(int(('0b'+md+str(st)), 2))[2:]).upper()
        res = self.checkLen(res)
        msg = (
            '09 40 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+
            str(temp)+' '+
            str(setp)+' '+
            res+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+
            str(temp)+' '+
            str(setp)+' '+
            res
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        status='no demand',
        mode='heating',
        temperature=21,
        set_point=20,
        my_macro_indx = None
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Digimax, TLX7506',
            'Digimax with short format (no set point)'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for mode
        modeCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'heating',
            'cooling'
        ]
        modeCtrl.AppendItems(list) 
        if list.count(mode)==0:
            modeCtrl.Select(n=0)
        else:
            modeCtrl.SetSelection(int(list.index(mode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxMode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(modeCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        modeCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for status
        statusCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'demand',
            'no demand',
            'initializing'
        ]
        statusCtrl.AppendItems(list) 
        if list.count(status)==0:
            statusCtrl.Select(n=0)
        else:
            statusCtrl.SetSelection(int(list.index(status)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxStatus)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(statusCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        statusCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a box for temperature
        staticBox = wx.StaticBox(panel, -1, text.textBoxTemperature)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        temperatureCtrl = panel.SpinIntCtrl(temperature, 5, 35)
        temperatureCtrl.SetInitialSize((30,-1))
        sizer5.Add(temperatureCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a box for setpoint
        staticBox = wx.StaticBox(panel, -1, text.textBoxSetPoint)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        setpointCtrl = panel.SpinIntCtrl(set_point, 16, 35)
        setpointCtrl.SetInitialSize((30,-1))
        sizer6.Add(setpointCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)

        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Digimax', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                statusCtrl.GetStringSelection(),
                modeCtrl.GetStringSelection(),
                temperatureCtrl.GetValue(),
                setpointCtrl.GetValue(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Digimax', nameCtrl.GetValue(), my_macro_indx
            )



class send_Thermostat_HE105(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'HE105': '00'
        }
        commands = {
            'Off': '00',
            'On': '01'
        }
        msg = (
            '06 41 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            unitcode+' '+
            str(commands[command])+' '+
            '00'
        )
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        unitcode="",
        command="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'HE105'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Off',
            'On'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Thermostat_HE105', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Thermostat_HE105', nameCtrl.GetValue(), my_macro_indx
            )



class send_Thermostat_RTS10(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'RTS10': '01'
        }
        commands = {
            'Off': '00',
            'On': '01',
            'Program RTS10': '02'
        }
        msg = (
            '06 41 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            unitcode+' '+
            str(commands[command])+' '+
            '00'
        )
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        unitcode="",
        command="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'RTS10'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Off',
            'On',
            'Program RTS10'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Thermostat_RTS10', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Thermostat_RTS10', nameCtrl.GetValue(), my_macro_indx
            )



class send_Mertik_G6R_H4T1(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'Mertik G6R-H4T1': '00'
        }
        commands = {
            'Off': '00',
            'On': '01',
            'Up': '02',
            'Down': '03',
            'Run Up': '04',
            'Run Down': '05',
            'Stop': '06'
        }
        cmd = commands[command]
        msg = (
            '08 42 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            cmd+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            cmd
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        command='Off',
        my_macro_indx = None
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Mertik G6R-H4T1'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))
        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Off',
            'On',
            'Up',
            'Down',
            'Run Up',
            'Run Down',
            'Stop'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Mertik_G6R_H4T1', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Mertik_G6R_H4T1', nameCtrl.GetValue(), my_macro_indx
            )



class send_Mertik_G6R_H4TB(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'Mertik G6R-H4TB/G6-H4T/G6R-H4T21-Z22': '01'
        }
        commands = {
            'Off': '00',
            'On': '01',
            'Up': '02',
            'Down': '03',
            '2nd Off': '04',
            '2nd On': '05'
        }
        cmd = commands[command]
        msg = (
            '08 42 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            cmd+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            cmd
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        command='Off',
        my_macro_indx = None
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Mertik G6R-H4TB/G6-H4T/G6R-H4T21-Z22'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))
        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Off',
            'On',
            'Up',
            'Down',
            '2nd Off',
            '2nd On'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Mertik_G6R_H4TB', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Mertik_G6R_H4TB', nameCtrl.GetValue(), my_macro_indx
            )



class send_Mertik_G6R_H4TD(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'Mertik G6R-H4TD': '02'
        }
        commands = {
            'Off': '00',
            'On': '01',
            'Up': '02',
            'Down': '03'
        }
        cmd = commands[command]
        msg = (
            '08 42 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            cmd+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            cmd
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        command='Off',
        my_macro_indx = None
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Mertik G6R-H4TD'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))
        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Off',
            'On',
            'Up',
            'Down'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Mertik_G6R_H4TD', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Mertik_G6R_H4TD', nameCtrl.GetValue(), my_macro_indx
            )



class send_Mertik_G6R_H4S(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'Mertik G6R-H4S': '03'
        }
        commands = {
            'Off': '00',
            'On': '01',
            'Up': '02',
            'Down': '03'
        }
        cmd = commands[command]
        msg = (
            '08 42 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            cmd+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            cmd
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        command='Off',
        my_macro_indx = None
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Mertik G6R-H4S'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))
        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Off',
            'On',
            'Up',
            'Down'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Mertik_G6R_H4S', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Mertik_G6R_H4S', nameCtrl.GetValue(), my_macro_indx
            )



class send_MCZ(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        beep,
        speed_1,
        speed_2,
        speed_3,
        flame,
        command,
        my_macro_indx
    ):
        protocols = {
            'MCZ 1 fan model': '00',
            'MCZ 2 fan model': '01',
            'MCZ 3 fan model': '02'
        }
        beeps = {
            False: '00',
            True: '01'
        }
        speeds_1 = {
            '0': '00',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            'auto': '06',
            'n.a': '00'
        }
        speeds_2 = {
            '0': '0',
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            'auto': '6',
            'n.a': '1'
        }
        speeds_3 = {
            '0': '0',
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            'auto': '6',
            'n.a': '1'
        }
        flames = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05'
        }
        commands = {
            'Off': '00',
            'Manual': '01',
            'Auto': '02',
            'Eco': '03'
        }
        cmd = commands[command]
        msg = (
            '0C 43 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            beeps[beep]+' '+
            speeds_1[speed_1]+' '+
            speeds_3[speed_3]+
            speeds_2[speed_2]+' '+
            flames[flame]+' '+
            cmd+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            cmd
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnTagChoice(self, event = None):         # "event = None" is used when opening the dialog
        protocolCtrl = self.protocolCtrl
        speed1Ctrl = self.speed1Ctrl
        speed2Ctrl = self.speed2Ctrl
        speed3Ctrl = self.speed3Ctrl
        commandCtrl = self.commandCtrl
        flameCtrl = self.flameCtrl
        choice = protocolCtrl.GetSelection()
        tag = protocolCtrl.GetStringSelection()
        speed1 = speed1Ctrl.GetStringSelection()
        speed2 = speed2Ctrl.GetStringSelection()
        speed3 = speed3Ctrl.GetStringSelection()
        command = commandCtrl.GetStringSelection()
        flame = flameCtrl.GetStringSelection()
        
        if tag == "MCZ 1 fan model":
            list_fs1 = ['1']
            list_fs2 = ['n.a']
            list_fs3 = ['n.a']
            if command == 'Auto' or command == 'Manual':
                if int(flame) == 1: 
                    list_fs1 = ['0','1','2','3','4','5','auto']
                else:
                    list_fs1 = ['1','2','3','4','5','auto']
            if command == 'Eco':
                list_fs1 = ['1','2','3','4','5','auto']
            if command == 'Off':
                list_fs1 = ['n.a']

        elif tag == "MCZ 2 fan model":
            list_fs1 = ['1']
            list_fs2 = ['1']
            list_fs3 = ['n.a']
            if command == 'Auto' or command == 'Manual':
                if int(flame) == 1: 
                    list_fs1 = ['0','1','2','3','4','5','auto']
                    list_fs2 = ['0','1','2','3','4','5','auto']
                else:
                    list_fs1 = ['1','2','3','4','5','auto']
                    list_fs2 = ['0','1','2','3','4','5','auto']
            if command == 'Eco':
                list_fs1 = ['1','2','3','4','5','auto']
                list_fs2 = ['0','1','2','3','4','5','auto']
            if command == 'Off':
                list_fs1 = ['n.a']
                list_fs2 = ['n.a']

        elif tag == "MCZ 3 fan model":
            list_fs1 = ['1']
            list_fs2 = ['1']
            list_fs3 = ['1']
            if command == 'Auto' or command == 'Manual':
                if int(flame) == 1: 
                    list_fs1 = ['0','1','2','3','4','5','auto']
                    list_fs2 = ['0','1','2','3','4','5','auto']
                    list_fs3 = ['0','1','2','3','4','5','auto']
                else:
                    list_fs1 = ['1','2','3','4','5','auto']
                    list_fs2 = ['0','1','2','3','4','5','auto']
                    list_fs3 = ['0','1','2','3','4','5','auto']
            if command == 'Eco':
                list_fs1 = ['1','2','3','4','5','auto']
                list_fs2 = ['0','1','2','3','4','5','auto']
                list_fs3 = ['0','1','2','3','4','5','auto']
            if command == 'Off':
                list_fs1 = ['n.a']
                list_fs2 = ['n.a']
                list_fs3 = ['n.a']

        speed1Ctrl.Clear()
        speed1Ctrl.AppendItems(list_fs1)
        if list_fs1.count(speed1)==0:        
            sel = 0
        else:
            sel = int(list_fs1.index(speed1))  
        speed1Ctrl.SetSelection(sel)

        speed2Ctrl.Clear()
        speed2Ctrl.AppendItems(list_fs2)
        if list_fs2.count(speed2)==0:                
            sel = 0
        else:
            sel = int(list_fs2.index(speed2))     
        speed2Ctrl.SetSelection(sel)
        
        speed3Ctrl.Clear()
        speed3Ctrl.AppendItems(list_fs3)
        if list_fs3.count(speed3)==0:               
            sel = 0
        else:
            sel = int(list_fs3.index(speed3))      
        speed3Ctrl.SetSelection(sel)

        if event:
            event.Skip()
        return choice           
        

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        res = self.OnTagChoice()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="01",
        id_2="00",
        id_3="00",
        beep=False,
        speed_1='1',
        speed_2='1',
        speed_3='1',
        flame='1',
        command='Auto',
        my_macro_indx = None
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)
        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = self.protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = ['MCZ 1 fan model','MCZ 2 fan model','MCZ 3 fan model']
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnTagChoice)
        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))
        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        bBeepCtrl = wx.CheckBox(panel, -1, "")
        bBeepCtrl.SetValue(beep)
        staticBox = wx.StaticBox(panel, -1, text.beep)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(bBeepCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for fan speed 1
        speed1Ctrl = self.speed1Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '0',
            '1',
            '2',
            '3',
            '4',
            '5',
            'auto'
        ]
        speed1Ctrl.AppendItems(list) 
        if list.count(speed_1)==0:
            speed1Ctrl.Select(n=0)
        else:
            speed1Ctrl.SetSelection(int(list.index(speed_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxFanSpeed_1)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(speed1Ctrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        speed1Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for fan speed 2
        speed2Ctrl = self.speed2Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = speed2Ctrl.GetStrings()
        #speed2Ctrl.AppendItems(list) 
        if list.count(speed_2)==0:
            speed2Ctrl.Select(n=0)
        else:
            speed2Ctrl.SetSelection(int(list.index(speed_2)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxFanSpeed_2)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(speed2Ctrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        speed2Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for fan speed 3
        speed3Ctrl = self.speed3Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = speed3Ctrl.GetStrings()
        #speed3Ctrl.AppendItems(list) 
        if list.count(speed_3)==0:
            speed3Ctrl.Select(n=0)
        else:
            speed3Ctrl.SetSelection(int(list.index(speed_3)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxFanSpeed_3)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(speed3Ctrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        speed3Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for flame power
        flameCtrl = self.flameCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1',
            '2',
            '3',
            '4',
            '5'
        ]
        flameCtrl.AppendItems(list) 
        if list.count(flame)==0:
            flameCtrl.Select(n=0)
        else:
            flameCtrl.SetSelection(int(list.index(flame)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxFlamePower)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(flameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        flameCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command/mode
        commandCtrl = self.commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Off',
            'Manual',
            'Auto',
            'Eco'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer8.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer8, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        res = self.OnTagChoice()
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_MCZ', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(),
                bBeepCtrl.GetValue(),
                speed1Ctrl.GetStringSelection(),
                speed2Ctrl.GetStringSelection(),
                speed3Ctrl.GetStringSelection(),
                flameCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_MCZ', nameCtrl.GetValue(), my_macro_indx
            )



class send_Siemens_Lightwave_RF(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        level,
        my_macro_indx
    ):
        protocols = {
            'LightwaveRF, Siemens': '00'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'off': '00',
            'on': '01',
            'group Off': '02',
            'mood1': '03',
            'mood2': '04',
            'mood3': '05',
            'mood4': '06',
            'mood5': '07',
            'reserved': '08',
            'reserved': '09',
            'unlock': '0A',
            'lock': '0B',
            'all lock': '0C',
            'close (inline relay)': '0D',
            'stop (inline relay)': '0E',
            'open (inline relay)': '0F',
            'set level': '10',
            'colour palette': '11',
            'colour tone': '12',
            'colour cycle': '13'
        }
        levels = {
            '0': '00',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10',
            '17': '11',
            '18': '12',
            '19': '13',
            '20': '14',
            '21': '15',
            '22': '16',
            '23': '17',
            '24': '18',
            '25': '19',
            '26': '1A',
            '27': '1B',
            '28': '1C',
            '29': '1D',
            '30': '1E',
            '31': '1F'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            str(levels[level])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command+' '+
            level
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        unitcode="",
        command="",
        level='0',
        my_macro_indx = None
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'LightwaveRF, Siemens'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for unit code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'group Off',
            'mood1',
            'mood2',
            'mood3',
            'mood4',
            'mood5',
            'reserved',
            'reserved',
            'unlock',
            'lock',
            'all lock',
            'close (inline relay)',
            'stop (inline relay)',
            'open (inline relay)',
            'set level',
            'colour palette',
            'colour tone',
            'colour cycle'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for dim level
        levelCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', '16', '17',
            '18', '19', '20', '21', '22', '23', '24', '25',
            '26', '27', '28', '29', '30', '31'
        ]
        levelCtrl.AppendItems(list) 
        if list.count(level)==0:
            levelCtrl.Select(n=0)
        else:
            levelCtrl.SetSelection(int(list.index(level)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxLevel)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(levelCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        levelCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            command = commandCtrl.GetStringSelection()
            level = levelCtrl.GetStringSelection()
            if command <> 'set level':
                level = '0'
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Siemens_Lightwave_RF', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(),
                command,
                level,
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Siemens_Lightwave_RF', nameCtrl.GetValue(), my_macro_indx
            )



class send_Siemens_SF01(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'Siemens SF01': '00'
        }
        commands = {
            'Timer': '01',
            '-': '02',
            'Learn': '03',
            '+': '04',
            'Confirm': '05',
            'Light': '06'
        }
        msg = (
            '08 17 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(commands[command])+' '+
            '00'
        )
        
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Siemens SF01'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = ['00']
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Timer',
            '-',
            'Learn',
            '+',
            'Confirm',
            'Light'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            command = commandCtrl.GetStringSelection()
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Siemens_SF01', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                command,
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Siemens_SF01', nameCtrl.GetValue(), my_macro_indx
            )



class send_LucciAir (eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'LucciAir': '02'
        }
        commands = {
            'High': '01',
            'Medium': '02',
            'Low': '03',
            'Off': '04',
            'Light': '05'
        }
        msg = (
            '08 17 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(commands[command])+' '+
            '00'
        )
        
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'LucciAir'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = ['00']
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'High',
            'Medium',
            'Low',
            'Off',
            'Light'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            command = commandCtrl.GetStringSelection()
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_LucciAir', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                command,
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_LucciAir', nameCtrl.GetValue(), my_macro_indx
            )



class send_SEAV_TXS4 (eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        j1,
        sw1,
        sw2,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'SEAV TXS4': '03'
        }
        commands = {
            'T1': '01',
            'T2': '02',
            'T3': '03',
            'T4': '04'
        }
        msg = (
            '08 17 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(commands[command])+' '+
            '00'
        )
        
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        j1 = False,
        sw1 = False,
        sw2 = False,
        id_1="0x0",
        id_2="00",
        id_3="00",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer3 = wx.GridBagSizer(1, 1)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'SEAV TXS4'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # ID switches
        j1_Ctrl = wx.CheckBox(panel, -1, "J1")
        j1_Ctrl.SetValue(j1)
        sizer3.Add(j1_Ctrl, (0,0))
        sw1_Ctrl = wx.CheckBox(panel, -1, "SW1")
        sw1_Ctrl.SetValue(sw1)
        sizer3.Add(sw1_Ctrl, (0,1))
        sw2_Ctrl = wx.CheckBox(panel, -1, "SW2")
        sw2_Ctrl.SetValue(sw2)
        sizer3.Add(sw2_Ctrl, (0,2))
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer3.Add(id_2_Ctrl,  (2,0))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))
        sizer3.Add(id_3_Ctrl,  (2,1))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'T1',
            'T2',
            'T3',
            'T4'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 1, flag = wx.ALIGN_LEFT)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            id_1 = '0x0'
            if j1_Ctrl.GetValue():
                id_1 = hex(int(id_1, 16)|0x80)
            if sw1_Ctrl.GetValue():
                id_1 = hex(int(id_1, 16)|0x40)
            if sw2_Ctrl.GetValue():
                id_1 = hex(int(id_1, 16)|0x20)
            id_1 = id_1.split('x')[1].upper()
            if len(id_1) < 2:
                id_1 = '0' + id_1

            command = commandCtrl.GetStringSelection()
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_SEAV_TXS4', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(),
                j1_Ctrl.GetValue(),
                sw1_Ctrl.GetValue(),
                sw2_Ctrl.GetValue(), 
                id_1, 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                command,
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_SEAV_TXS4', nameCtrl.GetValue(), my_macro_indx
            )



class send_Westinghouse_7226640 (eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'Westinghouse 7226640': '04'
        }
        commands = {
            'High': '01',
            'Medium': '02',
            'Low': '03',
            'Off': '04',
            'Light': '05'
        }
        msg = (
            '08 17 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(commands[command])+' '+
            '00'
        )
        
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)
        
        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Westinghouse 7226640'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = ['00']
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'High',
            'Medium',
            'Low',
            'Off',
            'Light'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            command = commandCtrl.GetStringSelection()
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Westinghouse_7226640', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                command,
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Westinghouse_7226640', nameCtrl.GetValue(), my_macro_indx
            )



class send_PT2262(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        pulseTiming,
        pt_1,
        pt_2,
        cb_1,
        cb_2,
        cb_3,
        cb_4,
        cb_5,
        cb_6,
        cb_7,
        cb_8,
        cb_9,
        cb_10,
        cb_11,
        cb_12,
        cb_13,
        cb_14,
        cb_15,
        cb_16,
        cb_17,
        cb_18,
        cb_19,
        cb_20,
        cb_21,
        cb_22,
        cb_23,
        cb_24,
        s_1,
        s_2,
        s_3,
        my_macro_indx
    ):
        protocols = {
            'PT2262': '00'
        }
        msg = (
            '09 13 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            s_1+' '+s_2+' '+s_3+' '+
            pt_1+' '+pt_2+' '+'00'
        )
        w_key = (
            protocol+' '+
            s_1+' '+s_2+' '+s_3+' '
        )
        w_msg = (
            protocol+' '+
            s_1+' '+s_2+' '+s_3+' '
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        pulseTiming=350,
        pt_1='',
        pt_2='',
        cb_1=False,
        cb_2=False,
        cb_3=False,
        cb_4=False,
        cb_5=False,
        cb_6=False,
        cb_7=False,
        cb_8=False,
        cb_9=False,
        cb_10=False,
        cb_11=False,
        cb_12=False,
        cb_13=False,
        cb_14=False,
        cb_15=False,
        cb_16=False,
        cb_17=False,
        cb_18=False,
        cb_19=False,
        cb_20=False,
        cb_21=False,
        cb_22=False,
        cb_23=False,
        cb_24=False,
        s_1='',
        s_2='',
        s_3='',
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        myHeadings_0 = wx.GridBagSizer(1, 1)
        mySizer = wx.GridBagSizer(1, 1)
        
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'PT2262'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create an entry for pulse timing 
        pulseTimingCtrl = panel.SpinIntCtrl(pulseTiming)        
        staticBox = wx.StaticBox(panel, -1, text.textBoxPulseTiming)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(pulseTimingCtrl, 1, wx.ALIGN_LEFT)
        staticBoxSizer.Add(sizer2, 0, wx.ALIGN_LEFT|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        myHeadings_0.Add(wx.StaticText(panel, -1, text.textBoxIdCommands ), (1,0))

        cb1_Ctrl = wx.CheckBox(panel, -1, "")
        cb1_Ctrl.SetValue(cb_1)
        mySizer.Add(cb1_Ctrl, (1,0))
        cb2_Ctrl = wx.CheckBox(panel, -1, "")
        cb2_Ctrl.SetValue(cb_2)
        mySizer.Add(cb2_Ctrl, (1,1))
        cb3_Ctrl = wx.CheckBox(panel, -1, "")
        cb3_Ctrl.SetValue(cb_3)
        mySizer.Add(cb3_Ctrl, (1,2))
        cb4_Ctrl = wx.CheckBox(panel, -1, "")
        cb4_Ctrl.SetValue(cb_4)
        mySizer.Add(cb4_Ctrl, (1,3))
        cb5_Ctrl = wx.CheckBox(panel, -1, "")
        cb5_Ctrl.SetValue(cb_5)
        mySizer.Add(cb5_Ctrl, (1,4))
        cb6_Ctrl = wx.CheckBox(panel, -1, "")
        cb6_Ctrl.SetValue(cb_6)
        mySizer.Add(cb6_Ctrl, (1,5))
        cb7_Ctrl = wx.CheckBox(panel, -1, "")
        cb7_Ctrl.SetValue(cb_7)
        mySizer.Add(cb7_Ctrl, (1,6))
        cb8_Ctrl = wx.CheckBox(panel, -1, "")
        cb8_Ctrl.SetValue(cb_8)
        mySizer.Add(cb8_Ctrl, (1,7))

        cb9_Ctrl = wx.CheckBox(panel, -1, "")
        cb9_Ctrl.SetValue(cb_9)
        mySizer.Add(cb9_Ctrl, (1,9))
        cb10_Ctrl = wx.CheckBox(panel, -1, "")
        cb10_Ctrl.SetValue(cb_10)
        mySizer.Add(cb10_Ctrl, (1,10))
        cb11_Ctrl = wx.CheckBox(panel, -1, "")
        cb11_Ctrl.SetValue(cb_11)
        mySizer.Add(cb11_Ctrl, (1,11))
        cb12_Ctrl = wx.CheckBox(panel, -1, "")
        cb12_Ctrl.SetValue(cb_12)
        mySizer.Add(cb12_Ctrl, (1,12))
        cb13_Ctrl = wx.CheckBox(panel, -1, "")
        cb13_Ctrl.SetValue(cb_13)
        mySizer.Add(cb13_Ctrl, (1,13))
        cb14_Ctrl = wx.CheckBox(panel, -1, "")
        cb14_Ctrl.SetValue(cb_14)
        mySizer.Add(cb14_Ctrl, (1,14))
        cb15_Ctrl = wx.CheckBox(panel, -1, "")
        cb15_Ctrl.SetValue(cb_15)
        mySizer.Add(cb15_Ctrl, (1,15))
        cb16_Ctrl = wx.CheckBox(panel, -1, "")
        cb16_Ctrl.SetValue(cb_16)

        mySizer.Add(cb16_Ctrl, (1,16))
        cb17_Ctrl = wx.CheckBox(panel, -1, "")
        cb17_Ctrl.SetValue(cb_17)
        mySizer.Add(cb17_Ctrl, (1,18))
        cb18_Ctrl = wx.CheckBox(panel, -1, "")
        cb18_Ctrl.SetValue(cb_18)
        mySizer.Add(cb18_Ctrl, (1,19))
        cb19_Ctrl = wx.CheckBox(panel, -1, "")
        cb19_Ctrl.SetValue(cb_19)
        mySizer.Add(cb19_Ctrl, (1,20))
        cb20_Ctrl = wx.CheckBox(panel, -1, "")
        cb20_Ctrl.SetValue(cb_20)
        mySizer.Add(cb20_Ctrl, (1,21))
        cb21_Ctrl = wx.CheckBox(panel, -1, "")
        cb21_Ctrl.SetValue(cb_21)
        mySizer.Add(cb21_Ctrl, (1,22))
        cb22_Ctrl = wx.CheckBox(panel, -1, "")
        cb22_Ctrl.SetValue(cb_22)
        mySizer.Add(cb22_Ctrl, (1,23))
        cb23_Ctrl = wx.CheckBox(panel, -1, "")
        cb23_Ctrl.SetValue(cb_23)
        mySizer.Add(cb23_Ctrl, (1,24))
        cb24_Ctrl = wx.CheckBox(panel, -1, "")
        cb24_Ctrl.SetValue(cb_24)
        mySizer.Add(cb24_Ctrl, (1,25))

        panel.sizer.Add(myHeadings_0, 1, flag = wx.ALIGN_LEFT)
        panel.sizer.Add(mySizer, 1, flag = wx.ALIGN_LEFT)
       
        while panel.Affirmed():
            pt = hex(pulseTimingCtrl.GetValue()).split('x')[1].upper()
            pt_1 = pt[:-2]
            if len(pt_1) < 2:
                pt_1 = '0' + pt_1
            pt_2 = pt[-2:]
            if len(pt_2) < 2:
                pt_2 = '0' + pt_2

            cmd_1 = '0x0'
            cmd_2 = '0x0'
            cmd_3 = '0x0'

            if cb1_Ctrl.GetValue():
                cmd_1 = hex(int(cmd_1, 16)|0x80)
            if cb2_Ctrl.GetValue():
                cmd_1 = hex(int(cmd_1, 16)|0x40)
            if cb3_Ctrl.GetValue():
                cmd_1 = hex(int(cmd_1, 16)|0x20)
            if cb4_Ctrl.GetValue():
                cmd_1 = hex(int(cmd_1, 16)|0x10)
            if cb5_Ctrl.GetValue():
                cmd_1 = hex(int(cmd_1, 16)|0x8)
            if cb6_Ctrl.GetValue():
                cmd_1 = hex(int(cmd_1, 16)|0x4)
            if cb7_Ctrl.GetValue():
                cmd_1 = hex(int(cmd_1, 16)|0x2)
            if cb8_Ctrl.GetValue():
                cmd_1 = hex(int(cmd_1, 16)|0x1)

            if cb9_Ctrl.GetValue():
                cmd_2 = hex(int(cmd_1, 16)|0x80)
            if cb10_Ctrl.GetValue():
                cmd_2 = hex(int(cmd_2, 16)|0x40)
            if cb11_Ctrl.GetValue():
                cmd_2 = hex(int(cmd_2, 16)|0x20)
            if cb12_Ctrl.GetValue():
                cmd_2 = hex(int(cmd_2, 16)|0x10)
            if cb13_Ctrl.GetValue():
                cmd_2 = hex(int(cmd_2, 16)|0x8)
            if cb14_Ctrl.GetValue():
                cmd_2 = hex(int(cmd_2, 16)|0x4)
            if cb15_Ctrl.GetValue():
                cmd_2 = hex(int(cmd_2, 16)|0x2)
            if cb16_Ctrl.GetValue():
                cmd_2 = hex(int(cmd_2, 16)|0x1)

            if cb17_Ctrl.GetValue():
                cmd_3 = hex(int(cmd_1, 16)|0x80)
            if cb18_Ctrl.GetValue():
                cmd_3 = hex(int(cmd_3, 16)|0x40)
            if cb19_Ctrl.GetValue():
                cmd_3 = hex(int(cmd_3, 16)|0x20)
            if cb20_Ctrl.GetValue():
                cmd_3 = hex(int(cmd_3, 16)|0x10)
            if cb21_Ctrl.GetValue():
                cmd_3 = hex(int(cmd_3, 16)|0x8)
            if cb22_Ctrl.GetValue():
                cmd_3 = hex(int(cmd_3, 16)|0x4)
            if cb23_Ctrl.GetValue():
                cmd_3 = hex(int(cmd_3, 16)|0x2)
            if cb24_Ctrl.GetValue():
                cmd_3 = hex(int(cmd_3, 16)|0x1)

            s_1 = cmd_1.split('x')[1].upper()
            if len(s_1) < 2:
                s_1 = '0' + s_1
            
            s_2 = cmd_2.split('x')[1].upper()
            if len(s_2) < 2:
                s_2 = '0' + s_2

            s_3 = cmd_3.split('x')[1].upper()
            if len(s_3) < 2:
                s_3 = '0' + s_3

            my_macro_indx = self.plugin.GetMacroIndex(
                'send_PT2262',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(),
                pulseTimingCtrl.GetValue(),
                pt_1,
                pt_2,
                cb1_Ctrl.GetValue(),
                cb2_Ctrl.GetValue(),
                cb3_Ctrl.GetValue(),
                cb4_Ctrl.GetValue(),
                cb5_Ctrl.GetValue(),
                cb6_Ctrl.GetValue(),
                cb7_Ctrl.GetValue(),
                cb8_Ctrl.GetValue(),
                cb9_Ctrl.GetValue(),
                cb10_Ctrl.GetValue(),
                cb11_Ctrl.GetValue(),
                cb12_Ctrl.GetValue(),
                cb13_Ctrl.GetValue(),
                cb14_Ctrl.GetValue(),
                cb15_Ctrl.GetValue(),
                cb16_Ctrl.GetValue(),
                cb17_Ctrl.GetValue(),
                cb18_Ctrl.GetValue(),
                cb19_Ctrl.GetValue(),
                cb20_Ctrl.GetValue(),
                cb21_Ctrl.GetValue(),
                cb22_Ctrl.GetValue(),
                cb23_Ctrl.GetValue(),
                cb24_Ctrl.GetValue(),
                s_1,
                s_2,
                s_3,
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_PT2262',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_EMW100_GAO_Everflourish(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'EMW100 GAO/Everflourish': '01'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04'
        }
        commands = {
            'off': '00',
            'on': '01',
            'learn': '02'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'EMW100 GAO/Everflourish'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for unit code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'learn'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_EMW100_GAO_Everflourish',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_EMW100_GAO_Everflourish',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Eurodomest(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Eurodomest': '09'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04'
        }
        commands = {
            'off': '00',
            'on': '01',
            'group off': '02',
            'group on': '03'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Eurodomest'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for unit code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'group off',
            'group on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Eurodomest',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Eurodomest',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Avantek(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Avantek': '0E'
        }
        unitcodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45'
        }
        commands = {
            'off': '00',
            'on': '01',
            'group off': '02',
            'group on': '03'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Avantek'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for unit code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'group off',
            'group on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Avantek',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Avantek',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Conrad_RSL2(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Conrad RSL2': '04'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'off': '00',
            'on': '01',
            'group off': '02',
            'group on': '03'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Conrad RSL2'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for unit code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'group off',
            'group on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Conrad_RSL2',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Conrad_RSL2',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_ByeByeStandBy(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'ByeByeStandBy (BBSB)': '02'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06'
        }
        commands = {
            'off': '00',
            'on': '01',
            'group off': '02',
            'group on': '03'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'ByeByeStandBy (BBSB)'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for unit code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'group off',
            'group on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_ByeByeStandBy',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_ByeByeStandBy',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Cotech(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Cotech, Kangtai': '11'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10',
            '17': '11',
            '18': '12',
            '19': '13',
            '20': '14',
            '21': '15',
            '22': '16',
            '23': '17',
            '24': '18',
            '25': '19',
            '26': '1A',
            '27': '1B',
            '28': '1C',
            '29': '1D',
            '30': '1E'
         }
        commands = {
            'off': '00',
            'on': '01',
            'group off': '02',
            'group on': '03'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Cotech, Kangtai'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for unit code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 
                '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', 
                '23', '24', '25', '26', '27', '28', '29', '30'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'group off',
            'group on'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Cotech',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Cotech',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_MDREMOTE_LED(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'MDREMOTE LED': '03',
            'MDREMOTE LED 108': '10'
        }
        commands = {
            'Power': '00',
            'Light': '01',
            'Bright': '02',
            'Dim': '03',
            '100%': '04',
            '50%': '05',
            '25%': '06',
            'Mode': '07',
            'Speed-': '08',
            'Speed+': '09',
            'Mode-': '0A'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '03'
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '03'+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'MDREMOTE LED',
            'MDREMOTE LED 108'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Power',
            'Light',
            'Bright',
            'Dim',
            '100%',
            '50%',
            '25%',
            'Mode',
            'Speed-',
            'Speed+',
            'Mode-'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_MDREMOTE_LED',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_MDREMOTE_LED',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Livolo(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'Livolo': '05'
        }
        commands = {
            'Group Off': '00',
            'Toggle On/Off': '01',
            'Dim+': '02',
            'Dim-': '03',
            'Toggle On/Off Gang1': '01',
            'Toggle On/Off Gang2': '02',
            'Toggle On/Off Gang3': '03'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '05'
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '05'+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Livolo'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Group Off',
            'Toggle On/Off',
            'Dim+',
            'Dim-',
            'Toggle On/Off Gang1',
            'Toggle On/Off Gang2',
            'Toggle On/Off Gang3'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Livolo',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Livolo',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Livolo_Appliance(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Livolo Appliance On/Off': '0A'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A'
        }
        commands = {
            'Group Off': '00',
            'Toggle On/Off': '01',
            'Dim+': '02',
            'Dim-': '03',
            'Scene1': '04',
            'Scene2': '05',
            'Dim+ room2': '06',
            'Dim- room2': '07',
            'Scene1 room2': '08',
            'Scene2 room2': '09'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            '0A'
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            '0A'+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        unitcode="1",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Livolo Appliance On/Off'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for unit code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Group Off',
            'Toggle On/Off'
            'Dim+',
            'Dim-',
            'Scene1',
            'Scene2',
            'Dim+ room2',
            'Dim- room2',
            'Scene1 room2',
            'Scene2 room2'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Livolo_Appliance',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Livolo_Appliance',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Smartwares_radiator_valve(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        id_4,
        unitcode,
        command,
        temperature,
        my_macro_indx
    ):
        tempStr = str(temperature).split('.')
        tperature = self.IntToHex(int(tempStr[0]))
        tpoint5 = self.IntToHex(int(tempStr[1]))
        protocols = {
            'Smartwares 433.92MHz radiator valve': '00'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'           
        }
        commands = {
            'Night': '00',
            'Day': '01',
            'Set temperature': '02'
        }
        msg = (
            '0C 48 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+id_4+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            tperature+' '+
            tpoint5+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+id_4+' '+
            unitcode+' '+
            '0C'
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+id_4+' '+
            unitcode+' '+
            '0C'+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Convert an integer to hex as string
    def IntToHex(self, res):
        s = hex(res).split('x')[1].upper()
        if len(s)<2:
            s = '0'+s
        return s


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        id_4="01",
        unitcode="1",
        command="",
        temperature=21.0,
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Smartwares 433.92MHz radiator valve'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for ID 4
        id_4_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_4_Ctrl.AppendItems(list) 
        if list.count(id_4)==0:
            id_4_Ctrl.Select(n=0)
        else:
            id_4_Ctrl.SetSelection(int(list.index(id_4)))

        sizer2.Add(id_4_Ctrl,  (0,3))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_4_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for unit code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
            '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Night',
            'Day',
            'Set temperature'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxTemperature)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        tempCtrl = panel.SpinNumCtrl(
            temperature,
            # by default, use '.' for decimal point
            decimalChar = '.',
            # by default, use ',' for grouping
            groupChar = ',',
            fractionWidth = 1,
            integerWidth = 2,
            min = 5.0,
            max = 28.0,
            increment = 0.5
        )
        tempCtrl.SetInitialSize((30,-1))
        sizer7.Add(tempCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Smartwares_radiator_valve',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                id_4_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(),
                tempCtrl.GetValue(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Smartwares_radiator_valve',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_IT_Intertek(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'IT Intertek,FA500,PROmax': '0F'
        }
        commands = {
            'Off': '00',
            'On': '01',
            'Group Off': '02',
            'Group On': '03',
            'Set Level': '10'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'IT Intertek,FA500,PROmax'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Off',
            'On'
            'Group Off',
            'Group On',
            'Set Level'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_IT_Intertek',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_IT_Intertek',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Aoke_Relay(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'Aoke Relay': '07'
        }
        commands = {
            'Off': '00',
            'On': '01'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)
        print msg

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Aoke Relay'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Off',
            'On'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Aoke_Relay',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Aoke_Relay',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Legrand_CAD(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'Legrand CAD': '0D'
        }
        commands = {
            'Toggle': '00'
        }
        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'+' '+
            str(commands[command])+' '+
            '00'+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Legrand CAD'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Toggle'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Legrand_CAD',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Legrand_CAD',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Blyss_Thomson(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        groupcode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Blyss_Thomson': '00'
        }
        groupcodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05'
        }
        commands = {
            'on': '00',
            'off': '01',
            'group on': '02',
            'group off': '03'
        }
        msg = (
            '0B 15 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+
            str(groupcodes[groupcode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            self.CommandSeq()+' '+
            '00'+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+
            groupcode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+
            groupcode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)
        CurrentStateData.cmndSeqNbr_015 += 1
        if CurrentStateData.cmndSeqNbr_015 > 4:
            CurrentStateData.cmndSeqNbr_015 -= 5


    def CommandSeq(self):
        if CurrentStateData.cmndSeqNbr_015 == 0:
            return '00'
        if CurrentStateData.cmndSeqNbr_015 == 1:
            return '01'
        if CurrentStateData.cmndSeqNbr_015 == 2:
            return '02'
        if CurrentStateData.cmndSeqNbr_015 == 3:
            return '03'
        if CurrentStateData.cmndSeqNbr_015 == 4:
            return '04'
        if CurrentStateData.cmndSeqNbr_015 == 5:
            return '05'


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="01",
        id_2="01",
        groupcode="",
        unitcode="",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Blyss_Thomson'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for group code
        groupCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        groupCtrl.AppendItems(list) 
        if list.count(groupcode)==0:
            groupCtrl.Select(n=0)
        else:
            groupCtrl.SetSelection(int(list.index(groupcode)))
        groupCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxGroupCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(groupCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for unit code
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'group on',
            'group off'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Blyss_Thomson',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                groupCtrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Blyss_Thomson',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_RGB_TRC02(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        color,
        my_macro_indx
    ):
        protocols = {
            'RGB_TRC02': '06'
        }
        commands = {
            'off': '00',
            'on': '01',
            'bright': '02',
            'dim': '03',
            'color +': '04',
            'color -': '05',
            'select color': '06'
        }
        
        if command == 'select color':
            res = str(color)
        else:
            res = str(commands[command])

        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'+' '+
            res+' '+
            '00'+' '+
            '00'
        )
        
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        command="",
        color='06',
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'RGB_TRC02'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'bright',
            'dim',
            'color +',
            'color -',
            'select color'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for color choice
        colorCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        color_choices = [
            '06', '07',
            '08', '09', '0A', '0B', '0C', '0D', '0E', '0F',
            '10', '11', '12', '13', '14', '15', '16', '17',
            '18', '19', '1A', '1B', '1C', '1D', '1E', '1F',
            '20', '21', '22', '23', '24', '25', '26', '27',
            '28', '29', '2A', '2B', '2C', '2D', '2E', '2F',
            '30', '31', '32', '33', '34', '35', '36', '37',
            '38', '39', '3A', '3B', '3C', '3D', '3E', '3F',
            '40', '41', '42', '43', '44', '45', '46', '47',
            '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
            '50', '51', '52', '53', '54', '55', '56', '57',
            '58', '59', '5A', '5B', '5C', '5D', '5E', '5F',
            '60', '61', '62', '63', '64', '65', '66', '67',
            '68', '69', '6A', '6B', '6C', '6D', '6E', '6F',
            '70', '71', '72', '73', '74', '75', '76', '77',
            '78', '79', '7A', '7B', '7C', '7D', '7E', '7F',
            '80', '81', '82', '83', '84'
        ]
        colorCtrl.AppendItems(color_choices) 
        if color_choices.count(color)==0:
            colorCtrl.Select(n=0)
        else:
            colorCtrl.SetSelection(int(color_choices.index(color)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxColor)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(colorCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        colorCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_RGB_TRC02', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                colorCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_RGB_TRC02', nameCtrl.GetValue(), my_macro_indx
            )



class send_RGB_TRC02_2(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        color,
        my_macro_indx
    ):
        protocols = {
            'RGB_TRC02': '06'
        }
        commands = {
            'off': '00',
            'on': '01',
            'bright': '02',
            'dim': '03',
            'color +': '04',
            'color -': '05',
            'select color': '06'
        }
        
        if command == 'select color':
            res = str(color)
        else:
            res = str(commands[command])

        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'+' '+
            res+' '+
            '00'+' '+
            '00'
        )
        
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        command="",
        color='06',
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'RGB_TRC02_2'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'bright',
            'dim',
            'color +',
            'color -',
            'select color'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for color choice
        colorCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        color_choices = [
            '06', '07',
            '08', '09', '0A', '0B', '0C', '0D', '0E', '0F',
            '10', '11', '12', '13', '14', '15', '16', '17',
            '18', '19', '1A', '1B', '1C', '1D', '1E', '1F',
            '20', '21', '22', '23', '24', '25', '26', '27',
            '28', '29', '2A', '2B', '2C', '2D', '2E', '2F',
            '30', '31', '32', '33', '34', '35', '36', '37',
            '38', '39', '3A', '3B', '3C', '3D', '3E', '3F',
            '40', '41', '42', '43'
        ]
        colorCtrl.AppendItems(color_choices) 
        if color_choices.count(color)==0:
            colorCtrl.Select(n=0)
        else:
            colorCtrl.SetSelection(int(color_choices.index(color)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxColor)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(colorCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        colorCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_RGB_TRC02_2', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                colorCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_RGB_TRC02_2', nameCtrl.GetValue(), my_macro_indx
            )



class send_RGB432W(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        color,
        my_macro_indx
    ):
        protocols = {
            'RGB432W': '0B'
        }
        commands = {
            'off': '00',
            'on': '01',
            'bright': '02',
            'dim': '03',
            'color +': '04',
            'color -': '05',
            'select color': '06'
        }
        
        if command == 'select color':
            res = str(color)
        else:
            res = str(commands[command])

        msg = (
            '0A 14 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            '00'+' '+
            res+' '+
            '00'+' '+
            '00'
        )
        
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        command="",
        color='06',
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'RGB432W'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'off',
            'on',
            'bright',
            'dim',
            'color +',
            'color -',
            'select color'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for color choice
        colorCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        color_choices = [
            '06', '07',
            '08', '09', '0A', '0B', '0C', '0D', '0E', '0F',
            '10', '11', '12', '13', '14', '15', '16', '17',
            '18', '19', '1A', '1B', '1C', '1D', '1E', '1F',
            '20', '21', '22', '23', '24', '25', '26', '27',
            '28', '29', '2A', '2B', '2C', '2D', '2E', '2F',
            '30', '31', '32', '33', '34', '35', '36', '37',
            '38', '39', '3A', '3B', '3C', '3D', '3E', '3F',
            '40', '41', '42', '43', '44', '45', '46', '47',
            '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
            '50', '51', '52', '53', '54', '55', '56', '57',
            '58', '59', '5A', '5B', '5C', '5D', '5E', '5F',
            '60', '61', '62', '63', '64', '65', '66', '67',
            '68', '69', '6A', '6B', '6C', '6D', '6E', '6F',
            '70', '71', '72', '73', '74', '75', '76', '77',
            '78', '79', '7A', '7B', '7C', '7D', '7E', '7F',
            '80', '81', '82', '83', '84'
        ]
        colorCtrl.AppendItems(color_choices) 
        if color_choices.count(color)==0:
            colorCtrl.Select(n=0)
        else:
            colorCtrl.SetSelection(int(color_choices.index(color)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxColor)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer7.Add(colorCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer7, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        colorCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_RGB432W', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                colorCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_RGB432W', nameCtrl.GetValue(), my_macro_indx
            )



class send_Byron_SX(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        command,
        my_macro_indx
    ):
        protocols = {
            'Byron_SX': '00'
        }
        commands = {
            'Sound0': '00',
            'Sound1': '01',
            'Sound2': '02',
            'Sound3': '03',
            'Sound4': '04',
            'Sound5': '05',
            'Sound6': '06',
            'Sound7': '07',
            'Sound8': '08',
            'Sound9': '09',
            'Sound10': '0A',
            'Sound11': '0B',
            'Sound12': '0C',
            'Sound13': '0D',
            'Sound14': '0E',
            'Sound15': '0F'
        }
        msg = (
            '07 16 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+
            str(commands[command])+' '+
            '00'
        )
        
        w_key = (
            protocol+' '+
            id_1+' '+id_2
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Byron_SX'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Sound0',
            'Sound1',
            'Sound2',
            'Sound3',
            'Sound4',
            'Sound5',
            'Sound6',
            'Sound7',
            'Sound8',
            'Sound9',
            'Sound10',
            'Sound11',
            'Sound12',
            'Sound13',
            'Sound14',
            'Sound15'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Byron_SX',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Byron_SX',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Byron_MP001(eg.ActionClass):

    def hexORing(self, val1, val2):
        result = int(str(val1), 16) | int(str(val2), 16)
        s = hex(result).split('x')[1].upper()
        if len(s)<2:
            s = '0'+s
        return '0x'+s


    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        id_4,
        id_5,
        id_6,
        my_macro_indx
    ):
        ID1 = '0x00'
        ID2 = '0x0F'
        ID3 = '0x54'
        
        if not id_1:
            ID1 = self.hexORing(ID1, '0x40')
        if not id_2:
            ID1 = self.hexORing(ID1, '0x10')
        if not id_3:
            ID1 = self.hexORing(ID1, '0x4')
        if not id_4:
            ID1 = self.hexORing(ID1, '0x1')
        if not id_5:
            ID2 = self.hexORing(ID2, '0x40')
        if not id_6:
            ID2 = self.hexORing(ID2, '0x10')
        
        ID1 = ID1.split('x')[1].upper()
        ID2 = ID2.split('x')[1].upper()
        ID3 = ID3.split('x')[1].upper()
       
        protocols = {
            'Byron MP001': '01'
        }
        msg = (
            '07 16 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            ID1+' '+ID2+' '+ID3+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            ID1+' '+ID2+' '+ID3
        )
        w_msg = (
            protocol+' '+
            ID1+' '+ID2+' '+ID3
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1=False,
        id_2=False,
        id_3=False,
        id_4=False,
        id_5=False,
        id_6=False,
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Byron MP001'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create checkboxes for ID's
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)

        id_1_Ctrl = wx.CheckBox(panel, -1, "")
        id_1_Ctrl.SetValue(id_1)
        sizer2.Add(id_1_Ctrl,  (0,0))
        
        id_2_Ctrl = wx.CheckBox(panel, -1, "")
        id_2_Ctrl.SetValue(id_2)
        sizer2.Add(id_2_Ctrl,  (0,1))

        id_3_Ctrl = wx.CheckBox(panel, -1, "")
        id_3_Ctrl.SetValue(id_3)
        sizer2.Add(id_3_Ctrl,  (0,2))
        
        id_4_Ctrl = wx.CheckBox(panel, -1, "")
        id_4_Ctrl.SetValue(id_4)
        sizer2.Add(id_4_Ctrl,  (0,3))

        id_5_Ctrl = wx.CheckBox(panel, -1, "")
        id_5_Ctrl.SetValue(id_5)
        sizer2.Add(id_5_Ctrl,  (0,4))

        id_6_Ctrl = wx.CheckBox(panel, -1, "")
        id_6_Ctrl.SetValue(id_6)
        sizer2.Add(id_6_Ctrl,  (0,5))

        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Byron_MP001',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetValue(), 
                id_2_Ctrl.GetValue(), 
                id_3_Ctrl.GetValue(), 
                id_4_Ctrl.GetValue(), 
                id_5_Ctrl.GetValue(), 
                id_6_Ctrl.GetValue(), 
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Byron_MP001',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_SelectPlus(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'SelectPlus 200689101': '02'
        }
        commands = {
            'Not used': '00'
        }
        msg = (
            '07 16 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(commands[command])
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'SelectPlus 200689101'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))
        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Not used'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_SelectPlus',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_SelectPlus',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Envivo(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        command,
        my_macro_indx
    ):
        protocols = {
            'Envivo': '04'
        }
        commands = {
            'Not used': '00'
        }
        msg = (
            '07 16 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(commands[command])
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        command="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Envivo'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Not used'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Envivo',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Envivo',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Harrison_Curtain(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        housecode,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Harrison Curtain': '00'
        }
        housecodes = {
            'A': '41',
            'B': '42',
            'C': '43',
            'D': '44',
            'E': '45',
            'F': '46',
            'G': '47',
            'H': '48',
            'I': '49',
            'J': '4A',
            'K': '4B',
            'L': '4C',
            'M': '4D',
            'N': '4E',
            'O': '4F',
            'P': '50'
        }            
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10'
        }
        commands = {
            'Open': '00',
            'Close': '01',
            'Stop': '02',
            'Program': '03'
        }
        msg = (
            '07 18 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            str(housecodes[housecode])+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            housecode+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            housecode+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        housecode="",
        unitcode="",
        command="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Harrison Curtain'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(list) 
        if list.count(housecode)==0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(housecode)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Open',
            'Close',
            'Stop',
            'Program'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Harrison_Curtain', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Harrison_Curtain', nameCtrl.GetValue(), my_macro_indx
            )



class send_RollerTrol(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'RollerTrol, Hasta new': '00',
            'Hasta old': '01'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            'all units': '00'
        }
        commands = {
            'Open': '00',
            'Close': '01',
            'Stop': '02',
            'Confirm/Pair': '03',
            'Set Limit': '04'
        }
        msg = (
            '09 19 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        unitcode="",
        command="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'RollerTrol, Hasta new',
            'Hasta old'

        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', 'all units'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Open',
            'Close',
            'Stop',
            'Confirm/Pair',
            'Set Limit'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_RollerTrol', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_RollerTrol', nameCtrl.GetValue(), my_macro_indx
            )



class send_Confexx(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Confexx CNF24-2435': '0C'
        }
        unitcodes = {
            '1': '00',
            '2': '01',
            '3': '02',
            '4': '03',
            '5': '04',
            '6': '05',
            '7': '06',
            '8': '07',
            '9': '08',
            '10': '09',
            '11': '0A',
            '12': '0B',
            '13': '0C',
            '14': '0D',
            '15': '0E',
            'all units': '0F'
        }
        commands = {
            'Open': '00',
            'Close': '01',
            'Stop': '02',
            'Confirm/Pair': '03'
        }
        msg = (
            '09 19 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        unitcode="",
        command="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Confexx CNF24-2435'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', 'all units'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Open',
            'Close',
            'Stop',
            'Confirm/Pair'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Confexx', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Confexx', nameCtrl.GetValue(), my_macro_indx
            )



class send_Screenline(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Screenline': '0D'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            '16': '10',
            '17': '11',
            '18': '12',
            '19': '13',
            '20': '14',
            '21': '15',
            '22': '16',
            '23': '17',
            '24': '18',
            '25': '19',
            '26': '1A',
            '27': '1B',
            '28': '1C',
            '29': '1D',
            '30': '1E',
            '31': '1F',
            '32': '20',
            '33': '21',
            '34': '22',
            '35': '23',
            '36': '24',
            '37': '25',
            '38': '26',
            '39': '27',
            '40': '28',
            '41': '29',
            '42': '2A',
            '43': '2B',
            '44': '2C',
            '45': '2D',
            '46': '2E',
            '47': '2F',
            '48': '30',
            '49': '31',
            '50': '32',
            '51': '33',
            '52': '34',
            '53': '35',
            '54': '36',
            '55': '37',
            '56': '38',
            '57': '39',
            '58': '3A',
            '59': '3B',
            '60': '3C',
            '61': '3D',
            '62': '3E',
            '63': '3F',
            '64': '40',
            '65': '41',
            '66': '42',
            '67': '43',
            '68': '44',
            '69': '45',
            '70': '46',
            '71': '47',
            '72': '48',
            '73': '49',
            '74': '4A',
            '75': '4B',
            '76': '4C',
            '77': '4D',
            '78': '4E',
            '79': '4F',
            '80': '50',
            '81': '51',
            '82': '52',
            '83': '53',
            '84': '54',
            '85': '55',
            '86': '56',
            '87': '57',
            '88': '58',
            '89': '59',
            '90': '5A',
            '91': '5B',
            '92': '5C',
            '93': '5D',
            '94': '5E',
            '95': '5F',
            '96': '60',
            '97': '61',
            '98': '62',
            '99': '63',
            'all units': '00'
        }
        commands = {
            'Open': '00',
            'Close': '01',
            'Confirm/Pair': '02'
        }
        msg = (
            '09 19 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        unitcode="",
        command="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Screenline'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 
                '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', 
                '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', 
                '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', 
                '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', 
                '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', 
                '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', 
                '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', 
                '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', 
                '93', '94', '95', '96', '97', '98', '99', 'all units'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Open',
            'Close',
            'Confirm/Pair'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Screenline', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Screenline', nameCtrl.GetValue(), my_macro_indx
            )



class send_A_OK(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'A-OK RF01': '02',
            'A-OK AC114': '03'
        }
        unitcodes = {
            '0': '00',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F',
            'all units': '10'
        }
        commands = {
            'Open': '00',
            'Close': '01',
            'Stop': '02',
            'Confirm/Pair': '03'
        }
        msg = (
            '09 19 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        unitcode="",
        command="",
        my_macro_indx=None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'A-OK RF01',
            'A-OK AC114'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
            '12', '13', '14', '15', 'all units'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Open',
            'Close',
            'Stop',
            'Confirm/Pair'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_A_OK', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_A_OK', nameCtrl.GetValue(), my_macro_indx
            )



class send_Raex(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Raex YR1326': '04'
        }
        unitcodes = {
            '0': '00'
        }
        commands = {
            'Open': '00',
            'Close': '01',
            'Stop': '02',
            'Confirm/Pair': '03',
            'Set Upper Limit': '04',
            'Set Lower Limit': '05',
            'Delete Limits': '06',
            'Change direction': '07',
            'Left (not yet used)': '08',
            'Right (not yet used)': '09'
        }
        msg = (
            '09 19 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        unitcode="0",
        command="",
        my_macro_indx=None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Raex YR1326'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
       
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '0'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Open',
            'Close',
            'Stop',
            'Confirm/Pair',
            'Set Upper Limit',
            'Set Lower Limit',
            'Delete Limits',
            'Change direction',
            'Left (not yet used)',
            'Right (not yet used)'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Raex', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Raex', nameCtrl.GetValue(), my_macro_indx
            )



class send_Media_Mount(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Media Mount': '05'
        }
        unitcodes = {
            '0': '00'
        }
        commands = {
            'Down': '00',
            'Up': '01',
            'Stop': '02'
        }
        msg = (
            '09 19 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="1A",
        id_2="62",
        id_3="80",
        unitcode="",
        command="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Media Mount'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '0'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Down',
            'Up',
            'Stop'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Media_Mount', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1, 
                id_2, 
                id_3, 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Media_Mount', nameCtrl.GetValue(), my_macro_indx
            )



class send_Dolat_DLM_1_Topstar(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Dolat DLM-1, Topstar': '0A'
        }
        unitcodes = {
            '0': '00'
        }
        commands = {
            'Down': '00',
            'Up': '01',
            'Stop': '02',
            'Confirm/Pair': '03',
            'Change direction': '06',
            'Erase current channel': '05',
            'Learn Master': '04'
        }
        msg = (
            '09 19 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        unitcode="0",
        command="",
        my_macro_indx=None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Dolat DLM-1, Topstar'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
       
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '0'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Down',
            'Up',
            'Stop',
            'Confirm/Pair',
            'Change direction',
            'Erase current channel',
            'Learn Master'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Dolat_DLM_1_Topstar', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Dolat_DLM_1_Topstar', nameCtrl.GetValue(), my_macro_indx
            )



class send_DC_Forest(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        id_4,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'DC/RMF/Yooda': '06',
            'Forest': '07'
        }
        unitcodes = {
            'all units': '0',
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7',
            '8': '8',
            '9': '9',
            '10': 'A',
            '11': 'B',
            '12': 'C',
            '13': 'D',
            '14': 'E',
            '15': 'F'
        }
        commands = {
            'Open': '00',
            'Close': '01',
            'Stop': '02',
            'Confirm/Pair': '03'
        }
        msg = (
            '09 19 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+id_4+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+id_4+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+id_4+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        id_4="1",        
        unitcode="1",
        command="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'DC/RMF/Yooda',
            'Forest'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for ID 4
        id_4_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'A', 'B', 'C', 'D', 'E', 'F'
        ]
        id_4_Ctrl.AppendItems(list) 
        if list.count(id_4)==0:
            id_4_Ctrl.Select(n=0)
        else:
            id_4_Ctrl.SetSelection(int(list.index(id_4)))

        sizer2.Add(id_4_Ctrl,  (0,3))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_4_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'all units', '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15' 
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Open',
            'Close',
            'Stop',
            'Confirm/Pair'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_DC_Forest', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                id_4_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_DC_Forest', nameCtrl.GetValue(), my_macro_indx
            )



class send_Chamberlain(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Chamberlain CS4330CN': '08'
        }
        unitcodes = {
            '1': '00',
            '2': '01',
            '3': '02',
            '4': '03',
            '5': '04',
            '6': '05'
        }
        commands = {
            'Open': '00',
            'Close': '01',
            'Stop': '02'
        }
        msg = (
            '09 19 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        unitcode="",
        command="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Chamberlain CS4330CN'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5', '6'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Open',
            'Close',
            'Stop'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Chamberlain', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Chamberlain', nameCtrl.GetValue(), my_macro_indx
            )



class send_Sunpery(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'Sunpery': '09'
        }
        unitcodes = {
            'all units': '00',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06'
        }
        commands = {
            'Open': '00',
            'Close': '01',
            'Stop': '02',
            'Confirm/Pair': '03',
            'Set Upper Limit': '04',
            'Set Lower Limit': '05',
            'Change direction': '06',
            'Intermediate position A': '07',
            'Intermediate position Center': '08',
            'Intermediate position B': '09',
            'Erase Current Channel': '0A',
            'Erase All Channels': '0B'
        }
        msg = (
            '09 19 '+
            str(protocols[protocol])+' '+
            '09'+' '+'00'+' '+
            id_1+' '+id_2+' '+id_3+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="0",
        unitcode="1",
        command="",
        my_macro_indx=None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Sunpery'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'A', 'B', 'C', 'D', 'E', 'F'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'all units',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Open',
            'Close',
            'Stop',
            'Confirm/Pair',
            'Set Upper Limit',
            'Set Lower Limit',
            'Change direction',
            'Intermediate position A',
            'Intermediate position Center',
            'Intermediate position B',
            'Erase Current Channel',
            'Erase All Channels'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Sunpery', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Sunpery', nameCtrl.GetValue(), my_macro_indx
            )



class send_ASP(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        my_macro_indx
    ):
        protocols = {
            'ASP': '0B'
        }
        unitcodes = {
            '0': '00'
        }
        commands = {
            'Open': '00',
            'Close': '01',
            'Stop': '02',
            'Confirm/Pair': '03'
        }
        msg = (
            '09 19 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        unitcode="0",
        command="Open",
        my_macro_indx=None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'ASP'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '0'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Open',
            'Close',
            'Stop',
            'Confirm/Pair'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_ASP', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_ASP', nameCtrl.GetValue(), my_macro_indx
            )



class send_ASA(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        rfu_1,
        rfu_2,
        rfu_3,
        my_macro_indx
    ):
        protocols = {
            'ASA': '03'
        }
        id1_code = {
            '0': '00',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            'A': '0A',
            'B': '0B',
            'C': '0C',
            'D': '0D',
            'E': '0E',
            'F': '0F'
        }
        unitcodes = {
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05'
        }
        commands = {
            'Stop': '00',
            'Up': '01',
            'Down': '03',
            'List programmed remotes': '06',
            'Program': '07',
            'Enable sun+wind detector': '13',
            'Disable sun detector': '14'             
        }
        msg = (
            '0C 1A '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            rfu_1+' '+rfu_2+' '+rfu_3+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="0",
        id_2="00",
        id_3="01",
        unitcode="",
        command="",
        rfu_1="00",
        rfu_2="00",
        rfu_3="00",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'ASA'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'A', 'B', 'C', 'D', 'E', 'F'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)


        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '1', '2', '3', '4', '5' 
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Stop',
            'Up',
            'Down',
            'List programmed remotes',
            'Program',
            'Enable sun+wind detector',
            'Disable sun detector'             
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_ASA', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                rfu_1,
                rfu_2,
                rfu_3,
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_ASA', nameCtrl.GetValue(), my_macro_indx
            )



class send_RFY(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        rfu_1,
        rfu_2,
        rfu_3,
        my_macro_indx
    ):
        protocols = {
            'RFY': '00'
        }
        id1_code = {
            '0': '00',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            'A': '0A',
            'B': '0B',
            'C': '0C',
            'D': '0D',
            'E': '0E',
            'F': '0F'
        }
        unitcodes = {
            '0': '00',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04'
        }
        commands = {
            'Stop': '00',
            'Up': '01',
            'Down': '03',
            'List programmed remotes': '06',
            'Program': '07',
            'Enable sun+wind detector': '13',
            'Disable sun detector': '14'             
        }
        msg = (
            '0C 1A '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            rfu_1+' '+rfu_2+' '+rfu_3+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="0",
        id_2="00",
        id_3="01",
        unitcode="",
        command="",
        rfu_1="00",
        rfu_2="00",
        rfu_3="00",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'RFY'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'A', 'B', 'C', 'D', 'E', 'F'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)


        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            '0', '1', '2', '3', '4' 
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Stop',
            'Up',
            'Down',
            'List programmed remotes',
            'Program',
            'Enable sun+wind detector',
            'Disable sun detector'             
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_RFY', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                rfu_1,
                rfu_2,
                rfu_3,
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_RFY', nameCtrl.GetValue(), my_macro_indx
            )



class send_RFY_ext(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        rfu_1,
        rfu_2,
        rfu_3,
        my_macro_indx
    ):
        protocols = {
            'RFY ext': '01'
        }
        id1_code = {
            '0': '00',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            'A': '0A',
            'B': '0B',
            'C': '0C',
            'D': '0D',
            'E': '0E',
            'F': '0F'
        }
        unitcodes = {
            '0': '00',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            '10': '0A',
            '11': '0B',
            '12': '0C',
            '13': '0D',
            '14': '0E',
            '15': '0F'
        }
        commands = {
            'Stop': '00',
            'Up': '01',
            'Down': '03',
            'List programmed remotes': '06',
            'Program': '07',
            'Enable sun+wind detector': '13',
            'Disable sun detector': '14'             
        }
        msg = (
            '0C 1A '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            rfu_1+' '+rfu_2+' '+rfu_3+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="0",
        id_2="00",
        id_3="01",
        unitcode="",
        command="",
        rfu_1="00",
        rfu_2="00",
        rfu_3="00",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'RFY ext'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'A', 'B', 'C', 'D', 'E', 'F'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)


        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                '10', '11', '12', '13', '14', '15'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Stop',
            'Up',
            'Down',
            'List programmed remotes',
            'Program',
            'Enable sun+wind detector',
            'Disable sun detector'             
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_RFY_ext', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                rfu_1,
                rfu_2,
                rfu_3,
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_RFY_ext', nameCtrl.GetValue(), my_macro_indx
            )



class send_RFY_Venetian(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        unitcode,
        command,
        rfu_1,
        rfu_2,
        rfu_3,
        my_macro_indx
    ):
        protocols = {
            'RFY_Venetian': '00'
        }
        id1_code = {
            '0': '00',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04',
            '5': '05',
            '6': '06',
            '7': '07',
            '8': '08',
            '9': '09',
            'A': '0A',
            'B': '0B',
            'C': '0C',
            'D': '0D',
            'E': '0E',
            'F': '0F'
        }
        unitcodes = {
            'all units': '00',
            '1': '01',
            '2': '02',
            '3': '03',
            '4': '04'
        }
        commands = {
            'Stop': '00',
            'Open': '0F',
            'Close': '10',
            'Change angle +': '11',
            'Change angle -': '12',
            'List programmed remotes': '06',
            'Program': '07',
            'Enable sun+wind detector': '13',
            'Disable sun detector': '14'
        }
        msg = (
            '0C 1A '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+
            str(unitcodes[unitcode])+' '+
            str(commands[command])+' '+
            rfu_1+' '+rfu_2+' '+rfu_3+' '+
            '00'
        )
        
        if len(unitcode) < 2:
            unitcode = '0' + unitcode
        w_key = (
            protocol+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+
            unitcode
        )
        w_msg = (
            protocol+' '+
            id1_code[id_1]+' '+id_2+' '+id_3+' '+
            unitcode+' '+
            command
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give the Venetian blind a name",
        protocol="",
        id_1="0",
        id_2="00",
        id_3="01",
        unitcode="",
        command="",
        rfu_1="00",
        rfu_2="00",
        rfu_3="00",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
        sizer2 = wx.GridBagSizer(10, 10)
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'RFY_Venetian'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'A', 'B', 'C', 'D', 'E', 'F'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)


        # Create a dropdown for device unitcode
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'all units', '1', '2', '3', '4' 
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unitcode)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unitcode)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Stop',
            'Open',
            'Close',
            'Change angle +',
            'Change angle -',
            'List programmed remotes',
            'Program',
            'Enable sun+wind detector',
            'Disable sun detector'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(command)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_RFY_Venetian', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                rfu_1,
                rfu_2,
                rfu_3,
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_RFY_Venetian', nameCtrl.GetValue(), my_macro_indx
            )



class send_x10_security_remote(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        status,
        my_macro_indx
    ):
        protocols = {
            'X10 security remote': '02'
        }
        statuses = {
            'panic': '06',
            'end panic': '07',
            'arm away': '09',
            'arm away delayed': '0A',
            'arm home': '0B',
            'arm home delayed': '0C',
            'disarm': '0D',
            'light 1 off': '10',
            'light 1 on': '11',
            'light 2 off': '12',
            'light 2 on': '13'
        }
        msg = (
            '08 20 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(statuses[status])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            status
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        status="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'X10 security remote'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for status
        statusCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'panic', 'end panic', 'arm away',
            'arm away delayed', 'arm home', 'arm home delayed', 'disarm',
            'light 1 off', 'light 1 on', 'light 2 off', 'light 2 on'
        ]
        statusCtrl.AppendItems(list) 
        if list.count(status)==0:
            statusCtrl.Select(n=0)
        else:
            statusCtrl.SetSelection(int(list.index(status)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(statusCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        statusCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_x10_security_remote', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2, 
                id_3_Ctrl.GetStringSelection(), 
                statusCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_x10_security_remote', nameCtrl.GetValue(), my_macro_indx
            )



class send_KeeLoq_Classic(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        id_4,
        id_5,
        id_6,
        id_7,
        id_8,
        id_9,
        my_macro_indx
    ):
        protocols = {
            'Classic KeeLoq packet': '00'
        }
        msg = (
            '1C 21 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            id_4+' '+id_5+' '+id_6+' '+
            id_7+' '+id_8+' '+id_9+' '+
            '00'+' '+'00'+' '+'00'+' '+
            '00'+' '+'00'+' '+'00'+' '+
            '00'+' '+'00'+' '+'00'+' '+
            '00'+' '+'00'+' '+'00'+' '+
            '00'+' '+'00'+' '+'00'+' '+
            '09'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            id_4+' '+id_5+' '+id_6+' '+
            id_7+' '+id_8+' '+id_9+' '+
            '00'+' '+'00'+' '+'00'+' '+
            '00'+' '+'00'+' '+'00'+' '+
            '00'+' '+'00'+' '+'00'+' '+
            '00'+' '+'00'+' '+'00'+' '+
            '00'+' '+'00'+' '+'00'
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        id_4="00",
        id_5="00",
        id_6="00",
        id_7="00",
        id_8="00",
        id_9="00",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Classic KeeLoq packet'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))
        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))
        sizer2.Add(id_3_Ctrl,  (0,2))
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for ID 4
        id_4_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_4_Ctrl.AppendItems(list) 
        if list.count(id_4)==0:
            id_4_Ctrl.Select(n=0)
        else:
            id_4_Ctrl.SetSelection(int(list.index(id_4)))
        sizer2.Add(id_4_Ctrl,  (0,3))
        id_4_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for ID 5
        id_5_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_5_Ctrl.AppendItems(list) 
        if list.count(id_5)==0:
            id_5_Ctrl.Select(n=0)
        else:
            id_5_Ctrl.SetSelection(int(list.index(id_5)))
        sizer2.Add(id_5_Ctrl,  (0,4))
        id_5_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for ID 6
        id_6_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_6_Ctrl.AppendItems(list) 
        if list.count(id_6)==0:
            id_6_Ctrl.Select(n=0)
        else:
            id_6_Ctrl.SetSelection(int(list.index(id_6)))
        sizer2.Add(id_6_Ctrl,  (0,5))
        id_6_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for ID 7
        id_7_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_7_Ctrl.AppendItems(list) 
        if list.count(id_7)==0:
            id_7_Ctrl.Select(n=0)
        else:
            id_7_Ctrl.SetSelection(int(list.index(id_7)))
        sizer2.Add(id_7_Ctrl,  (0,6))
        id_7_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for ID 8
        id_8_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_8_Ctrl.AppendItems(list) 
        if list.count(id_8)==0:
            id_8_Ctrl.Select(n=0)
        else:
            id_8_Ctrl.SetSelection(int(list.index(id_8)))
        sizer2.Add(id_8_Ctrl,  (0,7))
        id_8_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for ID 9
        id_9_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_9_Ctrl.AppendItems(list) 
        if list.count(id_9)==0:
            id_9_Ctrl.Select(n=0)
        else:
            id_9_Ctrl.SetSelection(int(list.index(id_9)))
        sizer2.Add(id_9_Ctrl,  (0,8))
        id_9_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
       
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_KeeLoq_Classic', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                id_4_Ctrl.GetStringSelection(), 
                id_5_Ctrl.GetStringSelection(), 
                id_6_Ctrl.GetStringSelection(), 
                id_7_Ctrl.GetStringSelection(), 
                id_8_Ctrl.GetStringSelection(), 
                id_9_Ctrl.GetStringSelection(), 
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_KeeLoq_Classic', nameCtrl.GetValue(), my_macro_indx
            )



class send_KD101_smoke_detector(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        status,
        my_macro_indx
    ):
        protocols = {
            'KD101 smoke detector': '03'
        }
        statuses = {
            'panic': '06',
            'pair KD101': '17'
        }
        msg = (
            '08 20 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(statuses[status])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            status
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        status="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'KD101 smoke detector'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))

        sizer2.Add(id_2_Ctrl,  (0,1))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
       
        # Create a dropdown for status
        statusCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'panic', 'pair KD101'
        ]
        statusCtrl.AppendItems(list) 
        if list.count(status)==0:
            statusCtrl.Select(n=0)
        else:
            statusCtrl.SetSelection(int(list.index(status)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(statusCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        statusCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_KD101_smoke_detector',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3, 
                statusCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_KD101_smoke_detector',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_SA30_smoke_detector(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        status,
        my_macro_indx
    ):
        protocols = {
            'Alecto SA30 smoke detector': '09'
        }
        statuses = {
            'panic': '06',
            'pair SA30': '17'
        }
        msg = (
            '08 20 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(statuses[status])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            status
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        status="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Alecto SA30 smoke detector'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))

        sizer2.Add(id_2_Ctrl,  (0,1))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
       
        # Create a dropdown for status
        statusCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'panic', 'pair SA30'
        ]
        statusCtrl.AppendItems(list) 
        if list.count(status)==0:
            statusCtrl.Select(n=0)
        else:
            statusCtrl.SetSelection(int(list.index(status)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(statusCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        statusCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_SA30_smoke_detector',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3, 
                statusCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_SA30_smoke_detector',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_RM174RF_smoke_detector(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        status,
        my_macro_indx
    ):
        protocols = {
            'Smartware RM174RF smoke detector': '0A'
        }
        statuses = {
            'panic': '06',
            'pair RM174RF': '17'
        }
        msg = (
            '08 20 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(statuses[status])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            status
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="01",
        status="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Smartware RM174RF smoke detector'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))

        sizer2.Add(id_2_Ctrl,  (0,1))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
       
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for status
        statusCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'panic', 'pair RM174RF'
        ]
        statusCtrl.AppendItems(list) 
        if list.count(status)==0:
            statusCtrl.Select(n=0)
        else:
            statusCtrl.SetSelection(int(list.index(status)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(statusCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        statusCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_RM174RF_smoke_detector',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                statusCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_RM174RF_smoke_detector',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_Meiantech(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        id_1,
        id_2,
        id_3,
        status,
        my_macro_indx
    ):
        protocols = {
            'Meiantech': '08'
        }
        statuses = {
            'panic': '06',
            'IR': '08',
            'arm away': '09',
            'arm home': '0B',
            'disarm': '0D'
        }
        msg = (
            '08 20 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            id_1+' '+id_2+' '+id_3+' '+
            str(statuses[status])+' '+
            '00'
        )
        w_key = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3
        )
        w_msg = (
            protocol+' '+
            id_1+' '+id_2+' '+id_3+' '+
            status
        )
        self.plugin.WriteMsg(msg, w_msg, w_key)

        
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        id_1="00",
        id_2="00",
        id_3="00",
        status="",
        my_macro_indx = None
        ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        sizer2 = wx.GridBagSizer(10, 10)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Meiantech'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for ID 1
        id_1_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        id_1_Ctrl.AppendItems(list) 
        if list.count(id_1)==0:
            id_1_Ctrl.Select(n=0)
        else:
            id_1_Ctrl.SetSelection(int(list.index(id_1)))
        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceID)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2.Add(id_1_Ctrl,  (0,0))
        id_1_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 2
        id_2_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_2_Ctrl.AppendItems(list) 
        if list.count(id_2)==0:
            id_2_Ctrl.Select(n=0)
        else:
            id_2_Ctrl.SetSelection(int(list.index(id_2)))

        sizer2.Add(id_2_Ctrl,  (0,1))
        id_2_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for ID 3
        id_3_Ctrl = wx.Choice(parent=panel, pos=(10,10)) 
        id_3_Ctrl.AppendItems(list) 
        if list.count(id_3)==0:
            id_3_Ctrl.Select(n=0)
        else:
            id_3_Ctrl.SetSelection(int(list.index(id_3)))

        sizer2.Add(id_3_Ctrl,  (0,2))
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        id_3_Ctrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for status
        statusCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'panic', 'arm away', 'arm home', 'disarm'
        ]
        statusCtrl.AppendItems(list) 
        if list.count(status)==0:
            statusCtrl.Select(n=0)
        else:
            statusCtrl.SetSelection(int(list.index(status)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer6.Add(statusCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer6, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        statusCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Meiantech',
                nameCtrl.GetValue(),
                my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                id_1_Ctrl.GetStringSelection(), 
                id_2_Ctrl.GetStringSelection(), 
                id_3_Ctrl.GetStringSelection(), 
                statusCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Meiantech',
                nameCtrl.GetValue(),
                my_macro_indx
            )



class send_ATI_RemoteWonder(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        unit_id,
        key,
        my_macro_indx
    ):
        protocols = {
            'ATI Remote Wonder': '00'
        }
        remoteKeys = {
            'Channel list':'30', 'X':'7C', 'Cursor-right':'71', 'v':'22',
            'X-End':'7D', 'red':'32', 'power':'02', 'TV':'03', 'A':'00',
            'B':'01', 'Guide':'06', 'Drag':'07', 'DVD':'04', '?':'05',
            'V-End':'79', 'VOL+':'08', 'VOL-':'09', 'Stop':'28', 'Pause':'29',
            '^':'1A', 'TV/RADIO':'1C', 'D':'1B', 'OK':'1E', '<':'1D',
            '>':'1F', 'VCR':'2D', 'DVD Audio':'3A', 'V':'78', 'Rewind':'24',
            'Play':'25', 'Full screen':'39', 'TV':'2C', 'Fast forward':'26',
            'Cursor-down-left':'77', 'Cursor-down-right':'76',
            'Cursor-up-right':'75', 'Record':'27', 'Cursor-down':'73',
            'Cursor-up':'72', 'Cursor-left':'70', 'RADIO':'2E', '<-':'20',
            'edit image':'38', 'Cursor-up-left':'74', 'E':'21', '5':'11',
            '4':'10', '7':'13', '6':'12', '9':'15', '8':'14', '0':'17',
            'txt':'16', 'C':'19', 'snapshot ESC':'18', 'Video Desktop':'31',
            'F':'23', 'Acquire image':'37', 'rename TAB':'36', 'blue':'35',
            'yellow':'34', 'CHAN+':'0B', 'CHAN-':'0C', 'TV Preview':'2F',
            'MUTE':'0A', '3':'0F', '1':'0D', '2':'0E', 'green':'33' 
        }
        msg = (
            '06 30 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            unit_id+' '+
            str(remoteKeys[key])+' '+
            '00'
        )
        self.plugin.WriteRemoteKey(msg)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        unit_id="",
        key="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'ATI Remote Wonder'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unit_id
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unit_id)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unit_id)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for key command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Channel list', 'X', 'Cursor-right', 'v', 'X-End', 'red', 'power',
            'TV', 'A', 'B', 'Guide', 'Drag', 'DVD', '?', 'V-End', 'VOL+',
            'VOL-', 'Stop', 'Pause', '^', 'TV/RADIO', 'D', 'OK', '<', '>',
            'VCR', 'DVD Audio', 'V', 'Rewind', 'Play', 'Full screen', 'TV',
            'Fast forward', 'Cursor-down-left', 'Cursor-down-right',
            'Cursor-up-right', 'Record', 'Cursor-down', 'Cursor-up',
            'Cursor-left', 'RADIO', '<-', 'edit image', 'Cursor-up-left', 'E',
            '5', '4', '7', '6', '9', '8', '0', 'txt', 'C', 'snapshot ESC',
            'Video Desktop', 'F', 'Acquire image', 'rename TAB', 'blue',
            'yellow', 'CHAN+', 'CHAN-', 'TV Preview', 'MUTE', '3', '1', '2',
            'green'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(key)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(key)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_ATI_RemoteWonder', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_ATI_RemoteWonder', nameCtrl.GetValue(), my_macro_indx
            )



class send_ATI_RemoteWonderPlus(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        unit_id,
        key,
        my_macro_indx
    ):
        protocols = {
            'ATI Remote Wonder Plus': '01'
        }
        remoteKeys = {
            'Channel list':'30', 'Right Mouse Button':'7C',
            'Cursor-right':'71', 'v':'22', 'X-End':'7D', 'red':'32',
            'power':'02', 'TV':'03', 'A':'00', 'B':'01', 'Guide':'06',
            'Drag':'07', 'DVD':'04', '?':'05', 'V-End':'79', 'VOL+':'08',
            'VOL-':'09', 'Stop':'28', 'Pause':'29', '^':'1A', 'FM':'1C',
            'D':'1B', 'OK':'1E', '<':'1D', '>':'1F', 'ATI':'2D',
            'DVD Audio':'3A', 'Left Mouse Button':'78', 'Rewind':'24',
            'Clock':'2B', 'Play':'25', 'Full screen':'39', 'i':'2C',
            'Fast forward':'26', 'Cursor-down-left':'77',
            'Cursor-down-right':'76', 'Cursor-up-right':'75', 'Record':'27',
            'Cursor-down':'73', 'Cursor-up':'72', 'Cursor-left':'70',
            'RADIO':'2E', 'Max/Restore window':'20', 'edit image':'38',
            'Cursor-up-left':'74', 'E':'21', '5':'11', '4':'10', '7':'13',
            '6':'12', '9':'15', '8':'14', '0':'17', 'txt':'16', 'C':'19',
            'Open Setup Menu':'18', 'Video Desktop':'31', 'F':'23',
            'Acquire image':'37', 'rename TAB':'36', 'blue':'35',
            'yellow':'34', 'CHAN+':'0B', 'CHAN-':'0C', 'TV Preview':'2F',
            'MUTE':'0A', '3':'0F', 'TV2':'2A', '1':'0D', '2':'0E',
            'green':'33'
        }
        msg = (
            '06 30 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            unit_id+' '+
            str(remoteKeys[key])+' '+
            '00'
        )
        self.plugin.WriteRemoteKey(msg)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        unit_id="",
        key="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'ATI Remote Wonder Plus'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unit_id
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unit_id)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unit_id)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for key command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Channel list', 'Right Mouse Button', 'Cursor-right', 'v', 'X-End',
            'red', 'power', 'TV', 'A', 'B', 'Guide', 'Drag', 'DVD', '?',
            'V-End', 'VOL+', 'VOL-', 'Stop', 'Pause', '^', 'FM', 'D', 'OK',
            '<', '>', 'ATI', 'DVD Audio', 'Left Mouse Button', 'Rewind',
            'Clock', 'Play', 'Full screen', 'i', 'Fast forward',
            'Cursor-down-left', 'Cursor-down-right', 'Cursor-up-right',
            'Record', 'Cursor-down', 'Cursor-up', 'Cursor-left', 'RADIO',
            'Max/Restore window', 'edit image', 'Cursor-up-left', 'E', '5',
            '4', '7', '6', '9', '8', '0', 'txt', 'C', 'Open Setup Menu',
            'Video Desktop', 'F', 'Acquire image', 'rename TAB', 'blue',
            'yellow', 'CHAN+', 'CHAN-', 'TV Preview', 'MUTE', '3', 'TV2',
            '1', '2', 'green'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(key)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(key)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_ATI_RemoteWonderPlus', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_ATI_RemoteWonderPlus', nameCtrl.GetValue(), my_macro_indx
            )



class send_Medion_Remote(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        unit_id,
        key,
        my_macro_indx
    ):
        protocols = {
            'Medion Remote': '02'
        }
        remoteKeys = {
            'Channel list':'30', 'X':'7C', 'Cursor-right':'71', 'v':'22',
            'X-End':'7D', 'red':'32', 'power':'02', 'TV':'03', 'Mute':'00',
            'B':'01', 'Music':'06', 'Drag':'07', 'DVD':'04', 'Photo':'05',
            'V-End':'79', 'VOL-':'08', 'VOL+':'09', 'Stop':'28', 'Pause':'29',
            '^':'1A', 'TV/RADIO':'1C', 'Setup':'1B', 'OK':'1E', '<':'1D',
            '>':'1F', 'VCR':'2D', 'DVD Audio':'3A', 'V':'78', 'Rewind':'24',
            'Play':'25', 'Full screen':'39', 'TV':'2C', 'Fast forward':'26',
            'Cursor-down-left':'77', 'Cursor-down-right':'76',
            'Cursor-up-right':'75', 'Record':'27', 'Cursor-down':'73',
            'Cursor-up':'72', 'Cursor-left':'70', 'RADIO':'2E', '<-':'20',
            'edit image':'38', 'Cursor-up-left':'74', 'E':'21', '5':'11',
            '4':'10', '7':'13', '6':'12', '9':'15', '8':'14', '0':'17',
            'txt':'16', 'DVD MENU':'19', 'snapshot ESC':'18',
            'Video Desktop':'31', 'F':'23', 'Acquire image':'37',
            'rename TAB':'36', 'blue':'35', 'yellow':'34', 'CHAN+':'0B',
            'CHAN-':'0C', 'TV Preview':'2F', 'MUTE':'0A', '3':'0F', '1':'0D',
            '2':'0E', 'green':'33'
        }
        msg = (
            '06 30 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            unit_id+' '+
            str(remoteKeys[key])+' '+
            '00'
        )
        self.plugin.WriteRemoteKey(msg)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        unit_id="",
        key="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Medion Remote'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unit_id
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unit_id)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unit_id)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for key command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'Channel list', 'X', 'Cursor-right', 'v', 'X-End', 'red', 'power',
            'TV', 'Mute', 'B', 'Music', 'Drag', 'DVD', 'Photo', 'V-End',
            'VOL-', 'VOL+', 'Stop', 'Pause', '^', 'TV/RADIO', 'Setup', 'OK',
            '<', '>', 'VCR', 'DVD Audio', 'V', 'Rewind', 'Play', 'Full screen',
            'TV', 'Fast forward', 'Cursor-down-left', 'Cursor-down-right',
            'Cursor-up-right', 'Record', 'Cursor-down', 'Cursor-up',
            'Cursor-left', 'RADIO', '<-', 'edit image', 'Cursor-up-left', 'E',
            '5', '4', '7', '6', '9', '8', '0', 'txt', 'DVD MENU',
            'snapshot ESC', 'Video Desktop', 'F', 'Acquire image',
            'rename TAB', 'blue', 'yellow', 'CHAN+', 'CHAN-', 'TV Preview',
            'MUTE', '3', '1', '2', 'green'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(key)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(key)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_Medion_Remote', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_Medion_Remote', nameCtrl.GetValue(), my_macro_indx
            )



class send_X10_PC_Remote(eg.ActionClass):

    def __call__(
        self,
        name,
        protocol,
        unit_id,
        key,
        my_macro_indx
    ):
        protocols = {
            'X10 PC Remote': '03'
        }
        remoteKeys = {
            'VOL+':'60', '6':'62', 'STOP':'63', 'PAUSE':'64', 'TEXT':'D8',
            'SHIFT-TEXT':'D9', 'SHIFT-ENT':'D6', 'SHIFT-TELETEXT':'D7',
            'PC or SHIFT-4':'D4', 'SHIFT-5':'D5', 'DVD':'D2', 'CD':'D3',
            'MP3':'D1', '9':'92', '4':'22', 'Drag':'7B', '3':'C2',
            'Left mouse':'78', 'EXIT':'C9', 'CH-':'C0', '8':'12',
            'ENT':'52', 'TELETEXT':'F2', 'Right mouse-End':'7D',
            'Right mouse':'7C', 'REC':'FF', 'MENU':'B6', 'PLAY':'B0',
            '1':'82', 'FF':'B8', '0':'02', '2':'42', 'CH+':'40',
            'INFO':'3A', 'A+B':'BA', 'Cursor-down-left':'77', 'MUTE':'A0',
            'Cursor-up-right':'75', 'Cursor-up-left':'74',
            'Cursor-down':'73', 'Cursor-up':'72', 'Cursor-right':'71',
            'Cursor-left':'70', 'VOL-':'E0', 'Left mouse-End':'79',
            '7':'E2', 'REW':'38', 'Cursor-down-right':'76', '5':'A2'
        }
        msg = (
            '06 30 '+
            str(protocols[protocol])+' '+
            '00'+' '+
            unit_id+' '+
            str(remoteKeys[key])+' '+
            '00'
        )
        self.plugin.WriteRemoteKey(msg)

       
    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        name="Give me a name",
        protocol="",
        unit_id="",
        key="",
        my_macro_indx = None
    ):
            
        text = Text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin
       
        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'X10 PC Remote'
        ]
        protocolCtrl.AppendItems(list) 
        if list.count(protocol)==0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        
        # Create a dropdown for device unit_id
        deviceCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
                '0A', '0B', '0C', '0D', '0E', '0F', '10', '11', '12', '13',
                '14', '15', '16', '17', '18', '19', '1A', '1B', '1C', '1D',
                '1E', '1F', '20', '21', '22', '23', '24', '25', '26', '27',
                '28', '29', '2A', '2B', '2C', '2D', '2E', '2F', '30', '31',
                '32', '33', '34', '35', '36', '37', '38', '39', '3A', '3B',
                '3C', '3D', '3E', '3F', '40', '41', '42', '43', '44', '45',
                '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F',
                '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
                '5A', '5B', '5C', '5D', '5E', '5F', '60', '61', '62', '63',
                '64', '65', '66', '67', '68', '69', '6A', '6B', '6C', '6D',
                '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77',
                '78', '79', '7A', '7B', '7C', '7D', '7E', '7F', '80', '81',
                '82', '83', '84', '85', '86', '87', '88', '89', '8A', '8B',
                '8C', '8D', '8E', '8F', '90', '91', '92', '93', '94', '95',
                '96', '97', '98', '99', '9A', '9B', '9C', '9D', '9E', '9F',
                'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9',
                'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'B0', 'B1', 'B2', 'B3',
                'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'BA', 'BB', 'BC', 'BD',
                'BE', 'BF', 'C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
                'C8', 'C9', 'CA', 'CB', 'CC', 'CD', 'CE', 'CF', 'D0', 'D1',
                'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'DA', 'DB',
                'DC', 'DD', 'DE', 'DF', 'E0', 'E1', 'E2', 'E3', 'E4', 'E5',
                'E6', 'E7', 'E8', 'E9', 'EA', 'EB', 'EC', 'ED', 'EE', 'EF',
                'F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9',
                'FA', 'FB', 'FC', 'FD', 'FE', 'FF'
        ]
        deviceCtrl.AppendItems(list) 
        if list.count(unit_id)==0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unit_id)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        # Create a dropdown for key command
        commandCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        list = [
            'VOL+', '6', 'STOP', 'PAUSE', 'TEXT', 'SHIFT-TEXT', 'SHIFT-ENT',
            'SHIFT-TELETEXT', 'PC or SHIFT-4', 'SHIFT-5', 'DVD', 'CD', 'MP3',
            '9', '4', 'Drag', '3', 'Left mouse', 'EXIT', 'CH-', '8', 'ENT',
            'TELETEXT', 'Right mouse-End', 'Right mouse', 'REC', 'MENU',
            'PLAY', '1', 'FF', '0', '2', 'CH+', 'INFO', 'A+B',
            'Cursor-down-left', 'MUTE', 'Cursor-up-right', 'Cursor-up-left',
            'Cursor-down', 'Cursor-up', 'Cursor-right', 'Cursor-left', 'VOL-',
            'Left mouse-End', '7', 'REW', 'Cursor-down-right', '5'
        ]
        commandCtrl.AppendItems(list) 
        if list.count(key)==0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(key)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        
        while panel.Affirmed():
            my_macro_indx = self.plugin.GetMacroIndex(
                'send_X10_PC_Remote', nameCtrl.GetValue(), my_macro_indx
            )
            panel.SetResult(
                nameCtrl.GetValue(), 
                protocolCtrl.GetStringSelection(), 
                deviceCtrl.GetStringSelection(), 
                commandCtrl.GetStringSelection(),
                my_macro_indx
            )      
            self.plugin.SetMacroName(
                'send_X10_PC_Remote', nameCtrl.GetValue(), my_macro_indx
            )



class WebRefresh(eg.ActionClass):
        
    def __call__(self):
        #Refresh status with persistent data if available
        time.sleep(0.5)
        self.plugin.DateAndTimeInfo() 
        time.sleep(2.0)
        self.plugin.StatusRefresh()



class ClearSensorsStatus(eg.ActionClass):
        
    def __call__(self):
        #Clear the repository for missing sensors
        time.sleep(0.5)
        CurrentStateData.sensors_status.clear()
        self.plugin.sensors_status = (
            CurrentStateData.sensors_status
        )



class ResetCurrentStatus(eg.ActionClass):
        
    def __call__(self):
        #Reset the repository for captured data
        time.sleep(0.5)
        CurrentStateData.current_state_memory.clear()
        self.plugin.current_state_memory = (
            CurrentStateData.current_state_memory
        )



class ResetLaCrosseTX5_data(eg.ActionClass):
        
    def __call__(self, deviceId):
        self.ClearData(deviceId)


    def ClearData(self, deviceId):
        try:
            del self.plugin.totalRain[deviceId]
            del self.plugin.flCount_prev[deviceId]
            del self.plugin.flipCount[deviceId]
            CurrentStateData.totalRain = self.plugin.totalRain 
            print deviceId, ': La Crosse TX5 data & counters resetted'
        except:
            pass


    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        deviceId = '1234'
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        list = []
        for item in self.plugin.totalRain:
            list.append(item)

        # Create a dropdown for key command
        deviceIdCtrl = wx.Choice(parent=panel, pos=(10,10)) 
        deviceIdCtrl.AppendItems(list) 
        if list.count(deviceId)==0:
            deviceIdCtrl.Select(n=0)
        else:
            deviceIdCtrl.SetSelection(int(list.index(deviceId)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxLCdeviceId)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(deviceIdCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceIdCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        while panel.Affirmed():
            try:
                devId = deviceIdCtrl.GetStringSelection()
                self.ClearData(devId)
                if devId <> '':
                    deviceId = devId
                panel.SetResult(
                    deviceId
                )
            except:
                pass            

       
        
class decode_Test_Message(eg.ActionClass):
        
    def __call__(self, msg):
        self.plugin.HandleChar(msg)


    def Configure(
        self,
        msg = '0b15000112ea480100012c60'
    ):
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)

        msgCtrl = wx.TextCtrl(panel, -1, msg)
        msgCtrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, 'Test message to decode'), (0,0))
        mySizer_1.Add(msgCtrl, (0,1))

        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            msg = msgCtrl.GetValue()

            panel.SetResult(
                msg.lower().replace(" ", "")
            )


             
class enable_unDecoded(eg.ActionClass):

    def __call__(
        self
    ):
        base_msg = self.plugin.interfaceMode
        try:
            if int(base_msg[7], 16) < 128:
                bb = str(bin(int(base_msg[7], 16)))[2:]
                if len(bb) < 8:
                    bb = bb.zfill(7)
                bb = '0b1'+bb
                ib = int(bb, 2)
                hb = hex(ib)
                sb = str(hb[2:]).upper()
                if len(sb)<2:
                    sb = '0'+sb
                msg = (
                    '0D 00 00 00 03 '+
                    base_msg[5]+' '+
                    base_msg[6]+' '+
                    sb+' '+
                    base_msg[8]+' '+
                    base_msg[9]+' '+
                    base_msg[10]+' '+
                    base_msg[11]+' '+
                    base_msg[12]+' '+
                    base_msg[13]
                )
                msg = msg.upper()
                print 'Undecoded enabled'
                self.plugin.WriteMsg(msg, '', '')
        except:
            eg.PrintError ('Action failed...')



class disable_unDecoded(eg.ActionClass):

    def __call__(
        self
    ):
        base_msg = self.plugin.interfaceMode
        try:
            if int(base_msg[7], 16) > 127:
                bb = str(bin(int(base_msg[7], 16)))
                bb = '0b0'+bb[3:]
                ib = int(bb, 2)
                hb = hex(ib)
                sb = str(hb[2:]).upper()
                if len(sb)<2:
                    sb = '0'+sb
                msg = (
                    '0D 00 00 00 03 '+
                    base_msg[5]+' '+
                    base_msg[6]+' '+
                    sb+' '+
                    base_msg[8]+' '+
                    base_msg[9]+' '+
                    base_msg[10]+' '+
                    base_msg[11]+' '+
                    base_msg[12]+' '+
                    base_msg[13]
                )
                msg = msg.upper()
                print 'Undecoded disabled'
                self.plugin.WriteMsg(msg, '', '')
        except:
            eg.PrintError ('Action failed...')



class remote_address_Mapper(eg.ActionClass):
        
    def __call__(self, adr_1, adr_2):
        del CurrentStateData.remote_address_map[adr_1]


    def Configure(
        self,
        adr_1 = '00467a6e',
        adr_2 = '0048219a'
    ):
        panel = eg.ConfigPanel(self)
        mySizer_1 = wx.GridBagSizer(10, 10)
        mySizer_2 = wx.GridBagSizer(10, 10)

        adr_1_Ctrl = wx.TextCtrl(panel, -1, adr_1)
        adr_1_Ctrl.SetInitialSize((250,-1))
        mySizer_1.Add(wx.StaticText(panel, -1, 'Actual remote address: '), (0,0))
        mySizer_1.Add(adr_1_Ctrl, (0,1))
        panel.sizer.Add(mySizer_1, 0, flag = wx.EXPAND)

        adr_2_Ctrl = wx.TextCtrl(panel, -1, adr_2)
        adr_2_Ctrl.SetInitialSize((250,-1))
        mySizer_2.Add(wx.StaticText(panel, -1, 'Replace address with : '), (0,0))
        mySizer_2.Add(adr_2_Ctrl, (0,1))
        panel.sizer.Add(mySizer_2, 0, flag = wx.EXPAND)

        while panel.Affirmed():
            adr_1 = adr_1_Ctrl.GetValue()
            adr_2 = adr_2_Ctrl.GetValue()
            CurrentStateData.remote_address_map[adr_1] = adr_2
            panel.SetResult(
                adr_1,
                adr_2
            )


             
class max_outPower(eg.ActionClass):

    def __call__(
        self
    ):
        base_msg = self.plugin.interfaceMode
        try:
            msg = (
                '0D 00 00 00 03 '+
                base_msg[5]+' '+
                '1F'+' '+
                base_msg[7]+' '+
                base_msg[8]+' '+
                base_msg[9]+' '+
                base_msg[10]+' '+
                '00'+' '+
                '00'+' '+
                '00'
            )
            msg = msg.upper()
            print 'Max output power enabled'
            self.plugin.WriteMsg(msg, '', '')
        except:
            eg.PrintError ('Action failed...')



class normal_outPower(eg.ActionClass):

    def __call__(
        self
    ):
        base_msg = self.plugin.interfaceMode
        try:
            msg = (
                '0D 00 00 00 03 '+
                base_msg[5]+' '+
                '1C'+' '+
                base_msg[7]+' '+
                base_msg[8]+' '+
                base_msg[9]+' '+
                base_msg[10]+' '+
                '00'+' '+
                '00'+' '+
                '00'
            )
            msg = msg.upper()
            print 'Normal output power enabled'
            self.plugin.WriteMsg(msg, '', '')
        except:
            eg.PrintError ('Action failed...')

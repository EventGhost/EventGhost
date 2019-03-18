#
# This file is a plugin for EventGhost.
# plugins/RFXcom_xPL/__init__.py
#
# Copyright (C) 2009
# Walter Kraembring
#
##############################################################################
#
# Acknowledgements: xPL code and main idea is based on doghouse xPL plugin
#
##############################################################################
# Revision history:
#
# 2011-08-29  Version 0.0.7, sensor data in the payload (selectable)
#             Heartbeat is now sent every minute instead of every fifth
# 2011-08-21  Test version 0.0.6, sensor data in the payload
#             Control of xPL Vendor ID, Device ID and Instance ID
#             (Vendor ID max 8, Device ID max 8, Instance ID max 16 characters)
# 2011-06-06  version 0.0.5 (b_weijenberg)
#             control.basic for io0-io7 added
#             sensor.request for io0-io7 added
# 2011-06-05  version 0.0.4 (b_weijenberg)
#             RFXLAN xPL support added
#             protocols added to x10.basic: arc,Koppla,Flamingo,Harrison,Waveman,he105,rts10
#             ac.basic added
#             Vendor-ID and Device-ID changed to: rfxcom-eg
#             Instance_ID limited to 8 characters
#             hbeat version 0.4
# 2011-02-16  version 0.0.3
#             Fixed to work with -translate switch
# 2009-12-28  HeartBeat monitoring thread and restart function introduced
# 2009-12-19  0.4.0 compatible GUID added
# 2009-12-02  Walter Kraembring: First version
##############################################################################

import eg

eg.RegisterPlugin(
    name="RFXcom_xPL",
    guid='{74895CCC-CCB4-4E23-B0AA-DC98385972BF}',
    author="Walter Kraembring",
    version="0.0.7",
    canMultiLoad=False,
    kind="external",
    description=(
        "Sends and receives RFXCOM messages using "
        "xPLRFX from xPL Monkey or RFXLAN xPL."
        '<br\n><br\n>'
        '<center><img src="xPL_plugin.png" /></center>'
    ),
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=2077",
)

import os
import sys
import time
import select
import wx
from socket import *
from threading import Event, Thread


class Text:
    xplDeviceName = "Enter the xpl-name of the RFXCOM device "
    portNumber = "Select the lowest port number to use "
    logToFile = "Log events to file: "
    debug = "Show all raw xPL messages: "
    pload = "Events shall have sensor data and specifics as payload: "

    class sendRFXcom_x10_basic:
        textBoxName = "Enter a descriptive name for the action"
        textBoxSchema = "Select the xPL schema to be used"
        textBoxProtocol = "Select the device protocol to be used"
        textBoxHouseCode = "Select the house code of the device"
        textBoxDeviceCode = "Select the device code of the device"
        textBoxCommand = "Select the command to send"
        textBoxLevel = "Select the dim/bright level"

    class sendRFXcom_x10_security:
        textBoxName = "Enter a descriptive name for the action"
        textBoxCommand = "Select the command to send"
        textBoxAddress = "Type the device ID to be used (0x0..0xffffff)"
        textBoxDelay = "Select delay to use"

    class sendRFXcom_homeeasy_basic:
        textBoxName = "Enter a descriptive name for the action"
        textBoxSchema = "Select the xPL schema to be used"
        textBoxAddress = "Type/paste the unit address to be used (0x....)"
        textBoxDeviceUnit = "Select the unit code of the device"
        textBoxCommand = "Select the command to send"
        textBoxLevel = "Select the dim/bright level"

    class sendRFXcom_ac_basic:
        textBoxName = "Enter a descriptive name for the action"
        textBoxAddress = "Type/paste the unit address to be used (0x....)"
        textBoxDeviceUnit = "Select the unit code of the device"
        textBoxCommand = "Select the command to send"
        textBoxLevel = "Select the dim/bright level"

    class sendRFXcom_control_basic:
        textBoxName = "Enter a descriptive name for the action"
        textBoxDevice = "Select the I/O line to be used"
        textBoxCommand = "Select the command to send"

    class sendRFXcom_sensor_request:
        textBoxName = "Enter a descriptive name for the action"
        textBoxDevice = "Select the I/O line to be used"


class RFXcom(eg.PluginClass):
    text = Text
    # Define initial value for heartbeat monitoring
    xplsourceHB = 10

    def __init__(self):
        self.revision = "0.5"
        self.LocalIP = gethostbyname(gethostname())
        self.hostname = "eg-rfxcom." + str(gethostname())[:16].lower()
        self.AddAction(sendRFXcom_x10_basic)
        self.AddAction(sendRFXcom_x10_security)
        self.AddAction(sendRFXcom_homeeasy_basic)
        self.AddAction(sendRFXcom_ac_basic)
        self.AddAction(sendRFXcom_control_basic)
        self.AddAction(sendRFXcom_sensor_request)
        # self.AddAction(Restart)

    def __start__(
        self,
        xplDeviceName,
        portNbr,
        bLogToFile,
        bDebug,
        bDataInPload
    ):
        self.UDPSock = socket(AF_INET, SOCK_DGRAM)
        # Initialise the socket
        self.xplDeviceName = xplDeviceName
        self.port = portNbr
        self.bLogToFile = bLogToFile
        self.bDebug = bDebug
        self.bDataInPload = bDataInPload

        bound = 0
        while bound == 0:
            bound = 1
            try:
                addr = ('0.0.0.0', self.port)
                self.UDPSock.bind(addr)
            except:
                bound = 0
                self.port += 1

        print "RFXcom_xPL plugin, bound to port " + str(self.port)
        print "RFXcom is started"

        # start the heartbeat thread
        self.hbThreadEvent = Event()
        hbThread = Thread(
            target=self.SendHeartbeat,
            args=(self.hbThreadEvent,)
        )
        hbThread.start()

        # start the heartbeat monitoring thread
        self.hbThreadMonitor = Event()
        hbMonitor = Thread(
            target=self.MonitorHeartbeat,
            args=(self.hbThreadMonitor,)
        )
        hbMonitor.start()

        # start the main thread that scans for incoming RFXcom xPL msgs
        self.mainThreadEvent = Event()
        mainThread = Thread(
            target=self.main,
            args=(self.mainThreadEvent,)
        )
        mainThread.start()

    def __stop__(self):
        self.hbThreadMonitor.set()
        self.hbThreadEvent.set()
        self.mainThreadEvent.set()
        hbSock = socket(AF_INET, SOCK_DGRAM)
        hbSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        msg = (
            "xpl-stat\n{\nhop=1\nsource="
            + str(self.hostname)
            + "\ntarget=*\n}\nhbeat.end\n{\ninterval=5\nport="
        )
        msg = (
            msg
            + str(self.port)
            + "\nremote-ip="
            + str(self.LocalIP)
            + "\nversion="
            + str(self.revision)
            + "\n}\n"
        )
        hbSock.sendto(msg, ("255.255.255.255", 3865))
        hbSock.sendto(msg, ("255.255.255.255", self.port))
        self.UDPSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        time.sleep(2.0)

    def __close__(self):
        print "RFXcom_xPL is closed."

    def Restart(self):
        self.__stop__()
        self.__start__(
            self.xplDeviceName,
            self.port,
            self.bLogToFile,
            self.bDebug,
            self.bDataInPload
        )

    # Sub routine for sending a heartbeat
    def SendHeartbeat(self, hbThreadEvent):
        hbSock = socket(AF_INET, SOCK_DGRAM)
        hbSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        while not hbThreadEvent.isSet():
            msg = (
                "xpl-stat\n{\nhop=1\nsource="
                + str(self.hostname)
                + "\ntarget=*\n}\nhbeat.app\n{\ninterval=5\nport="
            )
            msg = (
                msg
                + str(self.port)
                + "\nremote-ip="
                + str(self.LocalIP)
                + "\nversion="
                + str(self.revision)
                + "\n}\n"
            )
            hbSock.sendto(msg, ("255.255.255.255", 3865))
            hbThreadEvent.wait(1 * 60.0)

    # Sub routine for monitoring heartbeats
    def MonitorHeartbeat(self, hbThreadMonitor):
        while not hbThreadMonitor.isSet():
            hbThreadMonitor.wait(60.0)
            # print self.xplsourceHB
            if self.xplsourceHB > 0:
                self.xplsourceHB -= 1
            else:
                self.xplsourceHB = 10
                self.Restart()

    # Main Loop
    def main(self, mainThreadEvent):
        messageOld = ""
        while not mainThreadEvent.isSet():
            readable, writeable, errored = select.select([self.UDPSock], [], [], 60)
            if len(readable) == 1:
                data, addr = self.UDPSock.recvfrom(1500)
                message = ""
                message = str(data)
                message = message.splitlines()
                xpltype = message[0]
                msgheader = message[2:5]
                xplsource = message[3].rsplit("=")[1]
                xpltarget = message[4].rsplit("=")[1]
                msgschema = message[6]
                xplschema = msgschema.rsplit(".")
                msgbody = message[8:-1]
                msgbody2 = ""
                msgbody3 = ""
                msgbody4 = ""

                if self.bDebug:
                    print message

                if msgschema <> "hbeat.app":
                    if xplsource == self.xplDeviceName:
                        if message <> messageOld:
                            messageOld = message
                            for element in msgbody:
                                msgbody2 = msgbody2 + element + ","

                            if not self.bDataInPload:
                                self.TriggerEvent(
                                    xpltype
                                    + ":"
                                    + msgschema
                                    + ":"
                                    + xplsource
                                    + ":"
                                    + xpltarget
                                    + ":"
                                    + msgbody2
                                )
                            elif self.bDataInPload:
                                ml = msgbody2.split(',')
                                msgbody3 = ml[0] + ',' + ml[1]
                                ml = ml[2:-1]
                                for element in ml:
                                    msgbody4 = msgbody4 + element + ','
                                msgbody4 = msgbody4[0:-1]

                                self.TriggerEvent(
                                    xpltype
                                    + ":"
                                    + msgschema
                                    + ":"
                                    + xplsource
                                    + ":"
                                    + xpltarget
                                    + ":"
                                    + msgbody3
                                    ,
                                    payload=msgbody4
                                )

                            if self.xplsourceHB < 10:
                                self.xplsourceHB += 1

                            if self.bLogToFile:
                                logStr = (
                                    str(xpltype)
                                    + "|"
                                    + str(msgschema)
                                    + "|"
                                    + str(xplsource)
                                    + "|"
                                    + str(xpltarget)
                                    + "|"
                                    + str(msgbody2)
                                )
                                self.LogToFile(logStr)

                if msgschema == "hbeat.app":
                    if xplsource == self.xplDeviceName:
                        # print "This is the heartbeat from: ", xplsource
                        self.xplsourceHB += int(message[8].rsplit("=")[1])
                        if self.xplsourceHB > 10:
                            self.xplsourceHB = 10

    def LogToFile(self, s):
        timeStamp = str(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        )
        logStr = timeStamp + "\t" + s + "<br\n>"
        majorVersion, minorVersion = sys.getwindowsversion()[0:2]
        fileHandle = None

        if majorVersion > 5:
            progData = os.environ['ALLUSERSPROFILE']
            if (
                not os.path.exists(progData + "/EventGhost/Log")
                and not os.path.isdir(progData + "/EventGhost/Log")
            ):
                os.makedirs(progData + "/EventGhost/Log")
            fileHandle = open(
                progData + '/EventGhost/Log/RFXCOM_' + self.name + '.html', 'a'
            )
            fileHandle.write(logStr)
            fileHandle.close()
        else:
            if not os.path.exists('Log') and not os.path.isdir('Log'):
                os.mkdir('Log')
            fileHandle = open('Log/RFXCOM_' + self.name + '.html', 'a')
            fileHandle.write(logStr)
            fileHandle.close()

    def Configure(
        self,
        xplDeviceName="mal-rfxcom.",
        portNbr=50005,
        bLogToFile=False,
        bDebug=False,
        bDataInPload=False,
        *args
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        mySizer = wx.GridBagSizer(5, 5)

        xplDeviceNameCtrl = wx.TextCtrl(panel, -1, xplDeviceName)
        xplDeviceNameCtrl.SetInitialSize((250, -1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.xplDeviceName), (1, 0))
        mySizer.Add(xplDeviceNameCtrl, (1, 1))

        portCtrl = panel.SpinIntCtrl(portNbr, 50000, 50050)
        portCtrl.SetInitialSize((75, -1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.portNumber), (2, 0))
        mySizer.Add(portCtrl, (2, 1))

        bLogToFileCtrl = wx.CheckBox(panel, -1, "")
        bLogToFileCtrl.SetValue(bLogToFile)
        mySizer.Add(wx.StaticText(panel, -1, self.text.logToFile), (5, 0))
        mySizer.Add(bLogToFileCtrl, (5, 1))

        bDebugCtrl = wx.CheckBox(panel, -1, "")
        bDebugCtrl.SetValue(bDebug)
        mySizer.Add(wx.StaticText(panel, -1, self.text.debug), (6, 0))
        mySizer.Add(bDebugCtrl, (6, 1))

        bDataInPloadCtrl = wx.CheckBox(panel, -1, "")
        bDataInPloadCtrl.SetValue(bDataInPload)
        mySizer.Add(wx.StaticText(panel, -1, self.text.pload), (7, 0))
        mySizer.Add(bDataInPloadCtrl, (7, 1))

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        while panel.Affirmed():
            xplDeviceName = xplDeviceNameCtrl.GetValue()
            xplDeviceName = (
                xplDeviceName.split('-')[0][:8].lower() +
                '-' +
                xplDeviceName.split('-')[1].split('.')[0][:8].lower() +
                '.' +
                xplDeviceName.split('-')[1].split('.')[1][:16].lower()
            )

            portNbr = portCtrl.GetValue()
            bLogToFile = bLogToFileCtrl.GetValue()
            bDebug = bDebugCtrl.GetValue()
            bDataInPload = bDataInPloadCtrl.GetValue()

            panel.SetResult(
                xplDeviceName,
                portNbr,
                bLogToFile,
                bDebug,
                bDataInPload,
                *args
            )


class sendRFXcom_x10_basic(eg.ActionClass):
    name = "RFXCOM x10 basic"
    description = "Action to send RFXCOM messages using xPLRFX or RFXLAN xPL"
    iconFile = 'xPL'

    def __call__(self, name, schema, protocol, house, pdevice, command):
        xPLTarget = self.plugin.xplDeviceName

        if command == "on" or command == "off":
            xPLMsg = (
                "command="
                + command
                + "\n"
                + "device="
                + house
                + pdevice
            )

        if protocol != "X10":
            xPLMsg = (
                xPLMsg
                + "\n"
                + "protocol="
                + protocol
            )

        msg = (
            "xpl-cmnd"
            + "\n{\nhop=1\nsource="
            + self.plugin.hostname
            + "\ntarget="
            + xPLTarget
            + "\n}\n"
            + str(schema)
            + "\n{\n"
            + xPLMsg
            + "\n}\n"
        )
        addr = ("255.255.255.255", 3865)
        self.plugin.UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.plugin.UDPSock.sendto(msg, addr)
        time.sleep(0.1)

    #        for i in range(0, 1):
    #            self.plugin.UDPSock.sendto(msg,addr)
    #            time.sleep(1.0)

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        name="Give me a name",
        schema="",
        protocol="",
        house="",
        pdevice="",
        command=""
    ):

        text = self.text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin

        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for schema
        schemaCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = ['x10.basic']
        schemaCtrl.AppendItems(items=list)
        if list.count(schema) == 0:
            schemaCtrl.Select(n=0)
        else:
            schemaCtrl.SetSelection(int(list.index(schema)))
        schemaCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxSchema)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(schemaCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for protocol 
        protocolCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            'arc',
            'Koppla',
            'Flamingo',
            'Harrison',
            'he105',
            'rts10',
            'Waveman',
            'Nexa',
            'Intertechno',
            'Proove',
            'HomeEasy',
            'X10'
        ]
        protocolCtrl.AppendItems(items=list)
        if list.count(protocol) == 0:
            protocolCtrl.Select(n=0)
        else:
            protocolCtrl.SetSelection(int(list.index(protocol)))
        protocolCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxProtocol)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(protocolCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for house code
        houseCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'
        ]
        houseCtrl.AppendItems(items=list)
        if list.count(house) == 0:
            houseCtrl.Select(n=0)
        else:
            houseCtrl.SetSelection(int(list.index(house)))
        houseCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxHouseCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(houseCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for device code
        deviceCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '10', '11', '12', '13', '14', '15', '16'
        ]
        deviceCtrl.AppendItems(items=list)
        if list.count(pdevice) == 0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(pdevice)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceCode)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            'on',
            'off'
        ]
        commandCtrl.AppendItems(items=list)
        if list.count(command) == 0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
                schemaCtrl.GetStringSelection(),
                protocolCtrl.GetStringSelection(),
                houseCtrl.GetStringSelection(),
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection()
            )


class sendRFXcom_x10_security(eg.ActionClass):
    name = "RFXCOM x10 security"
    description = "Action to send X10 security messages using xPLRFX or RFXLAN xPL"
    iconFile = 'xPL'

    def __call__(self, name, command, address, delay):
        xPLTarget = self.plugin.xplDeviceName

        xPLMsg = (
            "command="
            + command
            + "\n"
            + "device="
            + address
        )

        if delay == "max":
            xPLMsg = (
                xPLMsg
                + "delay=max"
            )

        msg = (
            "xpl-cmnd"
            + "\n{\nhop=1\nsource="
            + self.plugin.hostname
            + "\ntarget="
            + xPLTarget
            + "\n}\nx10.security\n{\n"
            + xPLMsg
            + "\n}\n"
        )
        addr = ("255.255.255.255", 3865)
        self.plugin.UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.plugin.UDPSock.sendto(msg, addr)
        time.sleep(0.1)

    #        for i in range(0, 1):
    #            self.plugin.UDPSock.sendto(msg,addr)
    #            time.sleep(1.0)

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        name="Give me a name",
        command="",
        address="0x0..",
        delay=""
    ):

        text = self.text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin

        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            'alert',
            'normal',
            'motion',
            'arm-home',
            'arm-away',
            'disarm',
            'panic',
            'lights-on',
            'lights-off'

        ]
        commandCtrl.AppendItems(items=list)
        if list.count(command) == 0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a textfield for address 
        addressCtrl = wx.TextCtrl(panel, -1, address)

        staticBox = wx.StaticBox(panel, -1, text.textBoxAddress)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(addressCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for delay
        delayCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            'min',
            'max'

        ]
        delayCtrl.AppendItems(items=list)
        if list.count(delay) == 0:
            delayCtrl.Select(n=0)
        else:
            delayCtrl.SetSelection(int(list.index(delay)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDelay)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(delayCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        delayCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
                commandCtrl.GetStringSelection(),
                addressCtrl.GetValue(),
                delayCtrl.GetStringSelection()
            )


class sendRFXcom_homeeasy_basic(eg.ActionClass):
    name = "RFXCOM HOME easy basic"
    description = "Action to send RFXCOM messages using xPLRFX"
    iconFile = 'xPL'

    def __call__(self, name, schema, address, unit, command, level):
        xPLTarget = self.plugin.xplDeviceName

        if command == "on" or command == "off":
            xPLMsg = (
                "command="
                + command
                + "\n"
                + "address="
                + address
                + "\n"
                + "unit="
                + unit
            )

        if command == "preset":
            xPLMsg = (
                "command="
                + command
                + "\n"
                + "level="
                + level
                + "\n"
                + "address="
                + address
                + "\n"
                + "unit="
                + unit
            )

        msg = (
            "xpl-cmnd"
            + "\n{\nhop=1\nsource="
            + self.plugin.hostname
            + "\ntarget="
            + xPLTarget
            + "\n}\n"
            + str(schema)
            + "\n{\n"
            + xPLMsg
            + "\n}\n"
        )
        addr = ("255.255.255.255", 3865)
        self.plugin.UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.plugin.UDPSock.sendto(msg, addr)
        time.sleep(0.1)

    #        for i in range(0, 3):
    #            self.plugin.UDPSock.sendto(msg,addr)
    #            time.sleep(0.5)

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        name="Give me a name",
        schema="",
        address="0x...",
        unit="",
        command="",
        level=""
    ):

        text = self.text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin

        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for schema
        schemaCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = ['homeeasy.basic']
        schemaCtrl.AppendItems(items=list)
        if list.count(schema) == 0:
            schemaCtrl.Select(n=0)
        else:
            schemaCtrl.SetSelection(int(list.index(schema)))
        schemaCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, text.textBoxSchema)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(schemaCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a textfield for address 
        addressCtrl = wx.TextCtrl(panel, -1, address)

        staticBox = wx.StaticBox(panel, -1, text.textBoxAddress)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(addressCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for device unit
        deviceCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', 'group'
        ]
        deviceCtrl.AppendItems(items=list)
        if list.count(unit) == 0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unit)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = ['on', 'off', 'preset']
        commandCtrl.AppendItems(items=list)
        if list.count(command) == 0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for dim level
        levelCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15'
        ]
        levelCtrl.AppendItems(items=list)
        if list.count(level) == 0:
            levelCtrl.Select(n=0)
        else:
            levelCtrl.SetSelection(int(list.index(level)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxLevel)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer5.Add(levelCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer5, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        levelCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
                schemaCtrl.GetStringSelection(),
                addressCtrl.GetValue(),
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(),
                levelCtrl.GetStringSelection()
            )


class sendRFXcom_ac_basic(eg.ActionClass):
    name = "RFXCOM ac basic"
    description = "Action to send RFXCOM messages using RFXLAN xPL"
    iconFile = 'xPL'

    def __call__(self, name, address, unit, command, level):
        xPLTarget = self.plugin.xplDeviceName

        if command == "on" or command == "off":
            xPLMsg = (
                "command="
                + command
                + "\n"
                + "address="
                + address
                + "\n"
                + "unit="
                + unit
            )

        if command == "preset":
            xPLMsg = (
                "command="
                + command
                + "\n"
                + "level="
                + level
                + "\n"
                + "address="
                + address
                + "\n"
                + "unit="
                + unit
            )

        msg = (
            "xpl-cmnd"
            + "\n{\nhop=1\nsource="
            + self.plugin.hostname
            + "\ntarget="
            + xPLTarget
            + "\n}\nac.basic\n{\n"
            + xPLMsg
            + "\n}\n"
        )
        addr = ("255.255.255.255", 3865)
        self.plugin.UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.plugin.UDPSock.sendto(msg, addr)
        time.sleep(0.1)

    #        for i in range(0, 3):
    #            self.plugin.UDPSock.sendto(msg,addr)
    #            time.sleep(0.5)

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        name="Give me a name",
        address="0x...",
        unit="",
        command="",
        level=""
    ):

        text = self.text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin

        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a textfield for address 
        addressCtrl = wx.TextCtrl(panel, -1, address)

        staticBox = wx.StaticBox(panel, -1, text.textBoxAddress)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(addressCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for device unit
        deviceCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15', 'group'
        ]
        deviceCtrl.AppendItems(items=list)
        if list.count(unit) == 0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(unit)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDeviceUnit)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = ['on', 'off', 'preset']
        commandCtrl.AppendItems(items=list)
        if list.count(command) == 0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer3, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for dim level
        levelCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            '0', '1', '2', '3', '4', '5', '6', '7', '8',
            '9', '10', '11', '12', '13', '14', '15'
        ]
        levelCtrl.AppendItems(items=list)
        if list.count(level) == 0:
            levelCtrl.Select(n=0)
        else:
            levelCtrl.SetSelection(int(list.index(level)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxLevel)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(levelCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer4, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        levelCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
                addressCtrl.GetValue(),
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection(),
                levelCtrl.GetStringSelection()
            )


class sendRFXcom_control_basic(eg.ActionClass):
    name = "RFXCOM control basic"
    description = "Action to control an I/O line of the RFXLAN xPL"
    iconFile = 'xPL'

    def __call__(self, name, pdevice, command):
        xPLTarget = self.plugin.xplDeviceName

        msg = (
            "xpl-cmnd"
            + "\n{\nhop=1\nsource="
            + self.plugin.hostname
            + "\ntarget="
            + xPLTarget
            + "\n}\ncontrol.basic\n{\n"
            + "device="
            + pdevice
            + "\ntype=output"
            + "\ncurrent="
            + command
            + "\n}\n"
        )
        addr = ("255.255.255.255", 3865)
        self.plugin.UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.plugin.UDPSock.sendto(msg, addr)
        time.sleep(0.1)

    #        for i in range(0, 1):
    #            self.plugin.UDPSock.sendto(msg,addr)
    #            time.sleep(1.0)

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        name="Give me a name",
        pdevice="",
        command=""
    ):

        text = self.text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin

        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for device code
        deviceCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            'io0', 'io1', 'io2', 'io3', 'io4', 'io5', 'io6', 'io7'
        ]
        deviceCtrl.AppendItems(items=list)
        if list.count(pdevice) == 0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(pdevice)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDevice)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        # Create a dropdown for command
        commandCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            'high',
            'low',
            'toggle'
        ]
        commandCtrl.AppendItems(items=list)
        if list.count(command) == 0:
            commandCtrl.Select(n=0)
        else:
            commandCtrl.SetSelection(int(list.index(command)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxCommand)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(commandCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer2, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        commandCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
                deviceCtrl.GetStringSelection(),
                commandCtrl.GetStringSelection()
            )


class sendRFXcom_sensor_request(eg.ActionClass):
    name = "RFXCOM sensor request"
    description = "Action to get the status of an RFXLAN xPL I/O line"
    iconFile = 'xPL'

    def __call__(self, name, pdevice):
        xPLTarget = self.plugin.xplDeviceName

        msg = (
            "xpl-cmnd"
            + "\n{\nhop=1\nsource="
            + self.plugin.hostname
            + "\ntarget="
            + xPLTarget
            + "\n}\nsensor.request\n{\n"
            + "\nrequest=current"
            + "\ndevice="
            + pdevice
            + "\n}\n"
        )
        addr = ("255.255.255.255", 3865)
        self.plugin.UDPSock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.plugin.UDPSock.sendto(msg, addr)
        time.sleep(0.1)

    #        for i in range(0, 1):
    #            self.plugin.UDPSock.sendto(msg,addr)
    #            time.sleep(1.0)

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        name="Give me a name",
        pdevice=""
    ):

        text = self.text
        panel = eg.ConfigPanel(self)
        plugin = self.plugin

        # Create a textfield for action name 
        nameCtrl = wx.TextCtrl(panel, -1, name)

        staticBox = wx.StaticBox(panel, -1, text.textBoxName)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer0.Add(nameCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer0, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        # Create a dropdown for device code
        deviceCtrl = wx.Choice(parent=panel, pos=(10, 10))
        list = [
            'io0', 'io1', 'io2', 'io3', 'io4', 'io5', 'io6', 'io7'
        ]
        deviceCtrl.AppendItems(items=list)
        if list.count(pdevice) == 0:
            deviceCtrl.Select(n=0)
        else:
            deviceCtrl.SetSelection(int(list.index(pdevice)))

        staticBox = wx.StaticBox(panel, -1, text.textBoxDevice)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(deviceCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)
        deviceCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
                deviceCtrl.GetStringSelection()
            )


class Restart(eg.ActionClass):

    def __call__(self):
        self.plugin.xplsourceHB = 0

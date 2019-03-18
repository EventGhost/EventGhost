# Copyright (C) 2010 Dan Taylor <dan.taylor1000@virgin.net>
#
# This file is a plugin for EventGhost.

"""<rst>
A hardware plugin for the `Insteon SmartLinc <http://www.smarthome.com/2412N/SmartLinc-INSTEON-Central-Controller/p.aspx>`_ Central Controller. Lets you control devices and scenes on your Insteon network, and will create events for any activity processed via the SmartLinc. Modified by abuttino for x10. If you have a different house code than B, modify line 1780 and 1845 for your house code in THIS plugin to your 1 digit (or letter) house code. I also fixed errors with the plugin that had been abandoned.


|

.. image:: picture.jpg
   :align: center
   :target: http://www.smarthome.com/2412N/SmartLinc-INSTEON-Central-Controller/p.aspx
"""

import eg

# Define basic plug-in info
eg.RegisterPlugin(
    name="Insteon SmartLinc",
    guid='{F386CF6E-B3DA-421E-A495-E1E307A221F3}',
    author="Dan Taylor with edits and additions by Anthony Buttino",
    version="0.1",
    kind="external",
    createMacrosOnAdd=True,
    description=__doc__
)

import asyncore
import binascii
import socket
import time

import wx


# Setup Globals
ID_DEPTH = 1
Port = 9761
Address = ""
Devices = []
Scenes = []
VerboseMode = True
TimeDelay = 0.8
LastCommand = ""
sendCommandCount = 0


# Setup Text Fields
class Text:
    ipAddr = "SmartLinc IP Address"
    listhl1 = "Insteon Scenes"
    listhl2 = "Insteon Devices"
    verbtitle = "Verbose Mode"
    colLabels = ("ID",
                 "Name")


class AddSceneDialog(wx.Dialog):

    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(250, 146))

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        wx.StaticText(panel, -1, 'Scene ID:', (12, 15), (80, 20), style=wx.ALIGN_RIGHT)
        wx.StaticText(panel, -1, 'Name:', (12, 47), (80, 20), style=wx.ALIGN_RIGHT)

        IDBox = wx.TextCtrl(panel, -1, '00', (95, 12))
        nameBox = wx.TextCtrl(panel, -1, 'Name', (95, 44))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        addButton = wx.Button(self, -1, 'Add', size=(70, 30))
        cancelButton = wx.Button(self, -1, 'Cancel', size=(70, 30))
        hbox.Add(addButton, 1)
        hbox.Add(cancelButton, 1, wx.LEFT, 5)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)

        def SceneCancelButton(event):
            addScene.Destroy()

        def SceneAddButton(event):
            SceneListNew.append([nameBox.GetValue(), IDBox.GetValue()
                                 ])
            addScene.Destroy()

        cancelButton.Bind(wx.EVT_BUTTON, SceneCancelButton)
        addButton.Bind(wx.EVT_BUTTON, SceneAddButton)


class AddDeviceDialog(wx.Dialog):

    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(250, 146))

        panel = wx.Panel(self, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)

        wx.StaticText(panel, -1, 'Device ID:', (12, 15), (80, 20), style=wx.ALIGN_RIGHT)
        wx.StaticText(panel, -1, 'Name:', (12, 47), (80, 20), style=wx.ALIGN_RIGHT)

        IDBox = wx.TextCtrl(panel, -1, '000000', (95, 12))
        nameBox = wx.TextCtrl(panel, -1, 'Name', (95, 44))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        addButton = wx.Button(self, -1, 'Add', size=(70, 30))
        cancelButton = wx.Button(self, -1, 'Cancel', size=(70, 30))
        hbox.Add(addButton, 1)
        hbox.Add(cancelButton, 1, wx.LEFT, 5)

        vbox.Add(panel)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)

        self.SetSizer(vbox)

        def SceneCancelButton(event):
            addDevice.Destroy()

        def SceneAddButton(event):
            DeviceListNew.append([nameBox.GetValue(), IDBox.GetValue()
                                  ])
            addDevice.Destroy()

        cancelButton.Bind(wx.EVT_BUTTON, SceneCancelButton)
        addButton.Bind(wx.EVT_BUTTON, SceneAddButton)


class SmartLincClient(asyncore.dispatcher):

    def __init__(self, host, port):
        if VerboseMode:
            print "Connecting to SmartLin.."
            print "SmartLinc IP: %s" % host
            print "SmartLinc Port: %s " % port
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.buffer = ''
        self.dataPrevious = ""
        self.dataTime = 0

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        received = self.recv(1024)
        if VerboseMode:
            print "Received: %s" % binascii.hexlify(received).upper()

        # Trasnalte data into events...
        data = binascii.hexlify(received).upper()

        # smartlinc responds with try again, so create a schedule to delay and then send again
        # if data[0:2] == "15":
        #    self.sendCommandCallBack = eg.scheduler.AddTask(TimeDelay, self.sendcommand, LastCommand)
        #    if len(data)<5: #if data is only 15 or 1515, then stop and return. 
        #        return
        #    else: #if greater than there is a message attached to it, strip 15 from the front and continue
        #        if data[0:4] == "1515":
        #            data = data[4:]
        #        else:
        #            data = data[2:]

        # wireless sensors send each broadcast twice. This is to filter the duplicates out.
        if data == self.dataPrevious:  # if the data is the same as the last
            elapsedTime = time.time() - self.dataTime
            if elapsedTime < 2.5:  # check time between messages received, if less than 2, then it's a repeat.
                if VerboseMode:
                    print "Duplicate Mesage: %s, ignoring message" % data
                return  # return and don't do anything.
        self.dataPrevious = data
        self.dataTime = time.time()
        length = len(data)

        if data[0:2] == "15":
            time.sleep(TimeDelay)
            self.sendcommand(LastCommand)

        # 0262  = Device Command
        # 0250 = Return Message
        # 0F11 = Device On
        # 0F13 = Device Off

        # Scene Commands
        if length == 12:
            start = data[0:4]
            ID = data[4:6]
            cmd = data[6:8]
            # ID = data[8:10]
            trl = data[10:12]

            if (start == "0261"):
                start = "Scene Command"
                # Identify the scene
                IDList = []
                for q in range(len(Scenes)):
                    IDList.append(Scenes[q][1])
                try:
                    p = IDList.index(ID)
                    ID = Scenes[p][0]
                except ValueError:
                    ID = "unknown scene"

                # Identify the command
                if (cmd == "11"):
                    cmd = "On"
                if (cmd == "12"):
                    cmd = "Fast on"
                if (cmd == "13"):
                    cmd = "Off"
                if (cmd == "14"):
                    cmd = "Fast off"
                if (trl == "06"):
                    trl = "Received OK"
                if (trl == "15"):
                    trl = "Not received"

                if VerboseMode:
                    print start + " sent to " + ID + ": " + cmd + ". " + trl + "."
                eg.TriggerEvent(trl, prefix='SmartLinc')

        # Device Commands
        if length == 18:
            start = data[0:4]
            ID = data[4:10]
            SD = data[10:12]
            cmd = data[12:14]
            lvl = data[14:16]
            trl = data[16:18]

            lvlout = lvl

            if (start == "0262"):
                start = "Direct Command"

                # Identify the device
                IDList = []
                for q in range(len(Devices)):
                    IDList.append(Devices[q][1])
                    IDList[q] = IDList[q].replace(' ', '')
                    IDList[q] = IDList[q].replace('.', '')
                try:
                    p = IDList.index(ID)
                    ID = Devices[p][0]
                except ValueError:
                    ID = "unknown device"

                if (cmd == "11"):
                    cmd = "On"
                if (cmd == "12"):
                    cmd = "Fast On"
                if (cmd == "13"):
                    cmd = "Off"
                if (cmd == "14"):
                    cmd = "Fast Off"
                if (cmd == "15"):
                    cmd = "Bright"
                if (cmd == "16"):
                    cmd = "Dim"
                if (cmd == "19"):
                    cmd = "Request Status"
                if (cmd == "2E"):
                    cmd = "Ramp Up"
                if (cmd == "2F"):
                    cmd = "Ramp Down"
                lvl = int(lvl, 16)
                lvlout = int((lvl / 255.0) * 100)
                lvlout = "%s" % lvlout
                lvlout = lvlout + "%"
                if (trl == "06"):
                    trl = "Received OK"
                if (trl == "15"):
                    trl = "Not received"

            if VerboseMode:
                if cmd == "Request Status":
                    print start + " sent to " + ID + ": " + cmd + ". " + trl + "."
                elif (cmd == "Ramp Up" or cmd == "Ramp Down"):
                    print start + " sent to " + ID + ": " + cmd + ". " + trl + "."
                elif (cmd == "Bright" or cmd == "Dim"):
                    print start + " sent to " + ID + ": " + cmd + ". " + trl + "."
                else:
                    print start + " sent to " + ID + ": " + cmd + " to " + lvlout + ". " + trl + "."

            eg.TriggerEvent(trl, prefix='SmartLinc')

        # Status Response
        # Received: 0250 1C90A2 000004 CF 14 00
        if length == 22:
            start = data[0:4]
            ID = data[4:10]
            SD = data[10:16]
            ack = data[16:17]
            hop = data[17:18]
            dat = data[18:20]
            lvl = data[20:22]

            if (start == "0250"):
                start = "Message"

                # Identify the device
                IDList = []
                for q in range(len(Devices)):
                    IDList.append(Devices[q][1])
                    IDList[q] = IDList[q].replace(' ', '')
                    IDList[q] = IDList[q].replace('.', '')
                try:
                    p = IDList.index(ID)
                    ID = Devices[p][0]
                except ValueError:
                    ID = "unknown device"

                # if broadcast, then SD is the SCENE, ID is sending the broadcast to SCENE in SD (ex: 000004)
                # Identify the scene
                scn = str(int(SD[4:6], 16))  # save scn, convert from hex to int to string
                try:
                    p = IDList.index(SD)
                    SD = Devices[p][0]
                except ValueError:
                    SD = "unknown device"

                if ack == "2":
                    # Device Query
                    lvl = int(lvl, 16)
                    lvpercent = int((lvl / 255.0) * 100)
                    lvlout = int((lvl / 255.0) * 100)
                    lvlout = "%s" % lvlout
                    lvlout = lvlout + "%"
                    if lvlout == "0%":
                        lvlout = "Off"
                    if lvlout == "100%":
                        lvlout = "On"

                    if dat == "11":
                        # Device On
                        dat = "On"
                        percent = lvlout
                        myText = ID
                        if VerboseMode:
                            print start + " from " + ID + " to " + SD + ": " + lvlout + "."
                        eventTxt = ID + "." + lvlout
                        if lvlout == "On":
                            eg.TriggerEvent(eventTxt, prefix='SmartLinc')
                        else:
                            eg.TriggerEvent(myText, prefix='Smartlinc', payload=percent)
                        # eg.TriggerEvent(eventTxt, prefix='SmartLinc')
                    elif dat == "12":
                        # Device Fast On
                        dat = "Fast on"
                        if VerboseMode:
                            print start + " from " + ID + " to " + SD + ": " + lvlout + "."
                        eventTxt = ID + "." + lvlout
                        eg.TriggerEvent(eventTxt, prefix='SmartLinc')
                    elif dat == "13":
                        # Device Off
                        dat = "Fast off"
                        if VerboseMode:
                            print start + " from " + ID + " to " + SD + ": " + lvlout + "."
                        eventTxt = ID + "." + lvlout
                        eg.TriggerEvent(eventTxt, prefix='SmartLinc')
                    elif dat == "14":
                        # Device Fast Off
                        dat = "Fast off"
                        if VerboseMode:
                            print start + " from " + ID + " to " + SD + ": " + lvlout + "."
                        eventTxt = ID + "." + lvlout
                        eg.TriggerEvent(eventTxt, prefix='SmartLinc')
                    elif dat == "2E":
                        # Ramping
                        if VerboseMode:
                            print start + " from " + ID + " to " + SD + ": Ramping to " + lvlout
                        eventTxt = ID + ".Ramping"
                        percent = lvlout
                        myText = ID
                        rampEvent = ID + ".RampingToLevel"
                        ramplvl = lvlout
                        eg.TriggerEvent(eventTxt, prefix='SmartLinc')
                        # eg.TriggerEvent(rampEvent, prefix='SmartLinc', payload=ramplvl)
                        # eg.TriggerEvent(myText, prefix='Smartlinc', payload=percent)

                    # elif (dat == "15" or dat== "16"):
                    # Dimming
                    # if VerboseMode:
                    # print start + " from " + ID + " to " + SD + ": Dim/Bright"
                    # eventTxt = ID + ".Ramping"
                    # percent = lvlout
                    # myText = ID
                    # rampEvent = ID + ".RampingToLevel"
                    # ramplvl = lvlout
                    # eg.TriggerEvent(eventTxt, prefix='SmartLinc')
                    # eg.TriggerEvent(rampEvent, prefix='SmartLinc', payload=ramplvl)
                    # eg.TriggerEvent(myText, prefix='Smartlinc', payload=percent)

                    else:
                        if VerboseMode:
                            print start + " from " + ID + " to " + SD + ": Status is " + ": " + lvlout
                        percent = lvlout
                        eventTxt = ID + "." + lvlout
                        pload = eventTxt
                        myText = ID

                        if lvlout == "On" or lvlout == "Off":
                            eg.TriggerEvent(eventTxt, prefix='SmartLinc')
                        else:
                            eg.TriggerEvent(myText, prefix='SmartLinc', payload=percent)
                        # self.TriggerEvent("SmartLinc", ("mydata", "percent", 1232))
                        # self.TriggerEvent("SmartLinc" + "." + eventText + "." + percent)

                if ack == "4":
                    # Scene from Switch
                    if dat == "11":
                        dat = "On"
                    if dat == "12":
                        dat = "Fast On"
                    if dat == "13":
                        dat = "Off"
                    if dat == "14":
                        dat = "Fast Off"

                    # Identify the scene
                    scn = str(int(lvl, 16))  # save scn, convert from hex to int to string
                    datList = []
                    for q in range(len(Scenes)):
                        datList.append(Scenes[q][1])
                    try:
                        p = datList.index(lvl)
                        lvl = Scenes[p][0]
                    except ValueError:
                        lvl = "unknown scene"

                    if VerboseMode:
                        print start + " from device: " + ID + " to " + SD + ": " + dat

                        # print start + " from switch:" + ID + " to " + SD + ": " + lvl + ", " + dat +"."
                    eventTxt = ID + "." + dat + "." + scn  # added 11/12/2013 < + "." + lvl>
                    # time.sleep(TimeDelay)
                    eg.TriggerEvent(eventTxt, prefix='SmartLinc', payload=lvl)

                if ack == "6":
                    # Scene Activation

                    if dat == "11":
                        dat = "On"
                    if dat == "12":
                        dat = "Fast On"
                    if dat == "13":
                        dat = "Off"
                    if dat == "14":
                        dat = "Fast Off"

                    # Identify the scene
                    datList = []
                    for q in range(len(Scenes)):
                        datList.append(Scenes[q][1])
                    try:
                        p = datList.index(lvl)
                        lvl = Scenes[p][0]
                    except ValueError:
                        lvl = "unknown scene"

                    if VerboseMode:
                        print start + " from " + ID + " to " + SD + ": " + lvl + ", " + dat + "."
                    eventTxt = lvl + "." + dat
                    eg.TriggerEvent(eventTxt, prefix='SmartLinc')

                if ack == "C":
                    # Switch Pressed
                    if dat == "11":
                        dat = "On"
                    if dat == "12":
                        dat = "Fast On"
                    if dat == "13":
                        dat = "Off"
                    if dat == "14":
                        dat = "Fast Off"
                    if dat == "17":
                        if lvl == "01":
                            dat = "Fade Up"
                        if lvl == "00":
                            dat = "Fade Down"
                    if dat == "18":
                        dat = "Stop Fade"

                    # Identify the scene
                    datList = []
                    for q in range(len(Scenes)):
                        datList.append(Scenes[q][1])
                    try:
                        p = datList.index(lvl)
                        lvl = Scenes[p][0]
                    except ValueError:
                        lvl = "unknown scene"

                    if VerboseMode:
                        print start + " from " + ID + " to " + SD + ": " + lvl + ", " + dat + "."
                    eventTxt = "Switch." + ID + "." + dat + "." + scn  # added 11/12/2013 < + "." + lvl>
                    # time.sleep(TimeDelay)
                    eg.TriggerEvent(eventTxt, prefix='SmartLinc')

        # Extended Message
        if length == 28:
            start = data[0:4]
            status = data[4:6]

            if (start == "0258"):
                if status == "06":
                    status = "Clean Up OK"
                else:
                    status = "Clean Up Error"

                data = data[6:28]

                start = data[0:4]
                ID = data[4:10]
                SD = data[10:16]
                ack = data[16:17]
                hop = data[17:18]
                dat = data[18:20]
                lvl = data[20:22]

                if (start == "0250"):
                    start = "Message"
                    # Identify the devices
                    IDList = []
                    for q in range(len(Devices)):
                        IDList.append(Devices[q][1])
                        IDList[q] = IDList[q].replace(' ', '')
                        IDList[q] = IDList[q].replace('.', '')

                    try:
                        p = IDList.index(ID)
                        ID = Devices[p][0]
                    except ValueError:
                        ID = "unknown device"
                    # if broadcast, then SD is the SCENE, ID is sending the broadcast to SCENE in SD (ex: 000004)
                    # Identify the scene
                    scn = str(int(SD[4:6], 16))  # save scn, convert from hex to int to string
                    try:
                        p = IDList.index(SD)
                        SD = Devices[p][0]
                    except ValueError:
                        SD = "unknown device"

                    if ack == "2":
                        # Device Query
                        lvl = int(lvl, 16)
                        lvlout = int((lvl / 255.0) * 100)
                        lvlout = "%s" % lvlout
                        lvlout = lvlout + "%"
                        if lvlout == "0%":
                            lvlout = "Off"
                        if lvlout == "100%":
                            lvlout = "On"

                        if dat == "2E":
                            # Ramping
                            if VerboseMode:
                                print start + " from " + ID + " to " + SD + ": Ramping."
                            eventTxt = ID + ".Ramping"
                            eg.TriggerEvent(eventTxt, prefix='SmartLinc')
                        else:
                            if VerboseMode:
                                print start + " from " + ID + " to " + SD + ": Status is " + lvlout + "."
                            eventTxt = ID + "." + lvlout
                            eg.TriggerEvent(eventTxt, prefix='SmartLinc')

                    if ack == "4":
                        # Scene from Switch
                        if dat == "11":
                            dat = "On"
                        if dat == "12":
                            dat = "Fast On"
                        if dat == "13":
                            dat = "Off"
                        if dat == "14":
                            dat = "Fast Off"

                        # Identify the scene
                        datList = []
                        for q in range(len(Scenes)):
                            datList.append(Scenes[q][1])
                        try:
                            p = datList.index(lvl)
                            lvl = Scenes[p][0]
                        except ValueError:
                            lvl = "Unknown Scene"

                        if VerboseMode:
                            print start + " from " + ID + " to " + SD + ": " + lvl + ", " + dat + "."
                        eventTxt = lvl + "." + dat
                        eg.TriggerEvent(eventTxt, prefix='SmartLinc')

                    if ack == "6":
                        # Scene Activation

                        if dat == "11":
                            dat = "On"
                        if dat == "12":
                            dat = "Fast On"
                        if dat == "13":
                            dat = "Off"
                        if dat == "14":
                            dat = "Fast Off"

                        # Identify the scene
                        datList = []
                        for q in range(len(Scenes)):
                            datList.append(Scenes[q][1])
                        try:
                            p = datList.index(lvl)
                            lvl = Scenes[p][0]
                        except ValueError:
                            lvl = "unknown scene"

                        if VerboseMode:
                            print start + " from " + ID + " to " + SD + ": " + lvl + ", " + dat + "."
                        eventTxt = lvl + "." + dat
                        eg.TriggerEvent(eventTxt, prefix='SmartLinc')

                    if ack == "C":
                        # Switch Pressed
                        if dat == "11":
                            dat = "On"
                        if dat == "12":
                            dat = "Fast On"
                        if dat == "13":
                            dat = "Off"
                        if dat == "14":
                            dat = "Fast Off"
                        if dat == "17":
                            if lvl == "01":
                                dat = "Fade Up"
                            if lvl == "00":
                                dat = "Fade Down"
                        if dat == "18":
                            dat = "Stop Fade"

                        # Identify the scene
                        datList = []
                        for q in range(len(Scenes)):
                            datList.append(Scenes[q][1])
                        try:
                            p = datList.index(lvl)
                            lvl = Scenes[p][0]
                        except ValueError:
                            lvl = "unknown scene"

                        if VerboseMode:
                            print start + " from " + ID + " to " + SD + ": " + lvl + ", " + dat + "."
                        eventTxt = "Switch." + ID + "." + dat + "." + scn  # added 11/12/2013 < + "." + lvl>
                        # time.sleep(TimeDelay)
                        eg.TriggerEvent(eventTxt, prefix='SmartLinc')
                eg.TriggerEvent(status, prefix='SmartLinc')
                if VerboseMode:
                    print status

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def sendcommand(self, command):
        global LastCommand
        global sendCommandCount
        sendCommandCount = sendCommandCount + 1
        LastCommand = command
        print "SendCommand - %s - %s" % (sendCommandCount, binascii.hexlify(command).upper())
        self.send(command)


# This turns the Ascii strings (above) into actual binary data
def ascii2bin(command):
    bytes = command.replace(' ', '')
    bytes = bytes.replace('.', '')
    binary = binascii.unhexlify(bytes)
    return (binary)


# Set up the plug-in
class SmartLinc(eg.PluginBase):

    def Configure(self, SmartLincIPAddress="192.168.XXX.XXX", SmartLincScenes=[], SmartLincDevices=[], Verbose=True):
        panel = eg.ConfigPanel(self, resizable=True)

        # Setup List Handlers
        global SceneListNew
        SceneListNew = []
        for i in range(len(Scenes)):
            SceneListNew.append(Scenes[i])

        global DeviceListNew
        DeviceListNew = []
        for i in range(len(Devices)):
            DeviceListNew.append(Devices[i])

        # Setup Grid
        mySizer = wx.GridBagSizer(6, 4)

        # Add Labels, IP Address Box & Verbose Mode Check Box
        AddressTextCtrl = wx.TextCtrl(panel, -1, SmartLincIPAddress)
        TextCtrlTitle = wx.StaticText(panel, -1, Text.ipAddr)
        SceneTitle = wx.StaticText(panel, -1, Text.listhl1)
        DeviceTitle = wx.StaticText(panel, -1, Text.listhl2)
        # VerbTitle = wx.StaticText(panel, -1, Text.verbtitle)
        VerbBox = wx.CheckBox(panel, -1, Text.verbtitle)
        VerbBox.SetValue(Verbose)

        mySizer.Add(TextCtrlTitle, (0, 0), (1, 1))
        mySizer.Add(AddressTextCtrl, (1, 0), (1, 1))
        mySizer.Add(SceneTitle, (2, 0), (1, 1))
        mySizer.Add(DeviceTitle, (2, 2), (1, 1))
        # mySizer.Add(VerbTitle, (0,2), (1, 1))
        mySizer.Add(VerbBox, (0, 3), (1, 1), flag=wx.ALIGN_RIGHT)

        # Add List of Scenes
        SceneListCtrl = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)

        for i, colLabel in enumerate(Text.colLabels):
            SceneListCtrl.InsertColumn(i, colLabel)

        # setting column width to fit label
        # insert date to get size
        SceneListCtrl.InsertItem(0, "00")
        SceneListCtrl.SetItem(0, 1, "Bibble Bibble Bibble Bibble Bibble")

        size = 0
        for i in range(2):
            SceneListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)  # wx.LIST_AUTOSIZE
            size += SceneListCtrl.GetColumnWidth(i)

        SceneListCtrl.SetMinSize((size, -1))

        mySizer.Add(SceneListCtrl, (3, 0), (1, 2), flag=wx.EXPAND)

        # Add List of Devices
        DeviceListCtrl = wx.ListCtrl(panel, -1, style=wx.LC_REPORT | wx.VSCROLL | wx.HSCROLL)

        for i, colLabel in enumerate(Text.colLabels):
            DeviceListCtrl.InsertColumn(i, colLabel)

        # setting column width to fit label
        # insert date to get size
        DeviceListCtrl.InsertItem(0, "00.00.00")
        DeviceListCtrl.SetItem(0, 1, "Bibble Bibble Bibble Bibble Bibble")

        size = 0
        for i in range(2):
            DeviceListCtrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)  # wx.LIST_AUTOSIZE
            size += DeviceListCtrl.GetColumnWidth(i)

        DeviceListCtrl.SetMinSize((size, -1))

        mySizer.Add(DeviceListCtrl, (3, 2), (1, 2), flag=wx.EXPAND)

        # buttons

        mySceneSizer = wx.GridBagSizer(1, 2)
        myDeviceSizer = wx.GridBagSizer(1, 2)

        mySizer.Add(mySceneSizer, (4, 1), flag=wx.ALIGN_RIGHT)
        mySizer.Add(myDeviceSizer, (4, 3), flag=wx.ALIGN_RIGHT)

        AddSceneButton = wx.Button(panel, -1, "Add")
        mySceneSizer.Add(AddSceneButton, (0, 0), flag=wx.ALIGN_RIGHT)

        RemoveSceneButton = wx.Button(panel, -1, "Remove")
        mySceneSizer.Add(RemoveSceneButton, (0, 1), flag=wx.ALIGN_RIGHT)

        AddDeviceButton = wx.Button(panel, -1, "Add")
        myDeviceSizer.Add(AddDeviceButton, (0, 0), flag=wx.ALIGN_RIGHT)

        RemoveDeviceButton = wx.Button(panel, -1, "Remove")
        myDeviceSizer.Add(RemoveDeviceButton, (0, 1), flag=wx.ALIGN_RIGHT)

        mySizer.AddGrowableRow(3)
        mySizer.AddGrowableCol(0)
        mySizer.AddGrowableCol(1)
        mySizer.AddGrowableCol(2)
        mySizer.AddGrowableCol(3)

        # Reveal the controls
        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        # Define Functions
        def PopulateSceneList(event):
            SceneListNew.sort()
            SceneListCtrl.DeleteAllItems()
            row = 0
            for i in range(len(SceneListNew)):
                SceneListCtrl.InsertItem(row, SceneListNew[row][1])
                SceneListCtrl.SetItem(row, 1, SceneListNew[row][0])
                row += 1

        def PopulateDeviceList(event):
            DeviceListNew.sort()
            DeviceListCtrl.DeleteAllItems()
            row = 0
            for i in range(len(DeviceListNew)):
                DeviceListCtrl.InsertItem(row, DeviceListNew[row][1])
                DeviceListCtrl.SetItem(row, 1, DeviceListNew[row][0])
                row += 1

        def OnSceneAddButton(event):
            global addScene
            addScene = AddSceneDialog(None, -1, 'Add an Insteon scene...')
            addScene.ShowModal()
            # addScene.Destroy()
            PopulateSceneList(wx.CommandEvent())

        def OnSceneRemoveButton(event):
            selected = SceneListCtrl.GetFirstSelected()
            if selected >= 0:
                SceneListNew.pop(selected)
                PopulateSceneList(wx.CommandEvent())

        def OnDeviceAddButton(event):
            global addDevice
            addDevice = AddDeviceDialog(None, -1, 'Add an Insteon device...')
            addDevice.ShowModal()
            # addScene.Destroy()
            PopulateDeviceList(wx.CommandEvent())

        def OnDeviceRemoveButton(event):
            selected = DeviceListCtrl.GetFirstSelected()
            if selected >= 0:
                DeviceListNew.pop(selected)
                PopulateDeviceList(wx.CommandEvent())

        # Bind functions to buttons
        AddSceneButton.Bind(wx.EVT_BUTTON, OnSceneAddButton)
        RemoveSceneButton.Bind(wx.EVT_BUTTON, OnSceneRemoveButton)
        AddDeviceButton.Bind(wx.EVT_BUTTON, OnDeviceAddButton)
        RemoveDeviceButton.Bind(wx.EVT_BUTTON, OnDeviceRemoveButton)

        # Populate Scene List
        PopulateSceneList(wx.CommandEvent())
        PopulateDeviceList(wx.CommandEvent())

        while panel.Affirmed():
            # Copy the golbals to the plug-in parameters
            SmartLincIPAddress = AddressTextCtrl.GetValue()
            SmartLincScenes = []
            for i in range(len(SceneListNew)):
                SmartLincScenes.append(SceneListNew[i])
            SmartLincDevices = []
            for i in range(len(DeviceListNew)):
                SmartLincDevices.append(DeviceListNew[i])
            Verbose = VerbBox.GetValue()

            panel.SetResult(
                SmartLincIPAddress,
                SmartLincScenes,
                SmartLincDevices,
                Verbose
            )

    def __init__(self):
        print "Initialising SmartLinc plug-in."

        group1 = self.AddGroup(
            "Scene Control",
            "Basic controls for Insteon scenes."
        )

        group1.AddAction(SceneOn)
        group1.AddAction(SceneOff)
        group1.AddAction(SceneFastOn)
        group1.AddAction(SceneFastOff)

        group2 = self.AddGroup(
            "Device Control",
            "Advanced controls for individual Insteon devices."
        )

        group2.AddAction(DeviceOn)
        group2.AddAction(DeviceOff)
        group2.AddAction(DeviceFastOn)
        group2.AddAction(DeviceFastOff)
        group2.AddAction(DeviceToLevel)
        group2.AddAction(DeviceRampOn)
        group2.AddAction(DeviceRampOff)
        group2.AddAction(DeviceBright)
        group2.AddAction(DeviceDim)
        group2.AddAction(DeviceStatus)
        group2.AddAction(DeviceCustom)
        group2.AddAction(DevicextenOff)
        group2.AddAction(DevicextenOn)

    def __start__(self, SmartLincIPAddress="192.168.XXX.XXX", SmartLincScenes=[], SmartLincDevices=[], Verbose=True):
        print "Insteon SmartLinc plug-in started."

        # Pass the stored IP Address to a global
        global Address
        Address = SmartLincIPAddress

        # Pass the stored Scenes to a global
        global Scenes
        Scenes = SmartLincScenes

        # Pass the stored Devices
        global Devices
        Devices = SmartLincDevices

        global VerboseMode
        VerboseMode = Verbose

        # Connect to SmartLinc
        global c
        c = SmartLincClient(Address, Port)
        eg.RestartAsyncore()
        # asyncore.loop()

    def __stop__(self):
        print "Insteon SmartLinc plug-in stopped."
        c.close()

    def __close__(self):
        print "Insteon SmartLinc plug-in closed."
        c.close()


# Define the actions
class SceneOn(eg.ActionBase):
    name = "Scene On"
    description = "Turns a scene on using the predefined ramp rate at brightness level."

    def __call__(self, SceneName, SceneNum):
        if VerboseMode:
            print "Turning on Scene " + SceneNum

        commands = {}
        commands['on'] = '02 61 %s 11 %s' % (SceneNum, SceneNum)

        if VerboseMode:
            print "Sending Command: %s" % commands['on']

        command = ascii2bin(commands['on'])
        c.sendcommand(command)

    def Configure(self, SceneName="", SceneNum=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a scene from the list below...", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Scenes)):
            ChoiceList.append(Scenes[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the scene and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(SceneName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Scenes[FinalChoice][0],
                Scenes[FinalChoice][1]
            )


class SceneOff(eg.ActionBase):
    name = "Scene Off"
    description = "Turns a scene off using the predefined ramp rate at brightness level."

    def __call__(self, SceneName="", SceneNum=""):
        if VerboseMode:
            print "Turning off Scene " + SceneNum

        commands = {}
        commands['off'] = '02 61 %s 13 %s' % (SceneNum, SceneNum)

        if VerboseMode:
            print "Sending Command: %s" % commands['off']

        command = ascii2bin(commands['off'])
        c.sendcommand(command)

    def Configure(self, SceneName="", SceneNum=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a scene from the list below...", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Scenes)):
            ChoiceList.append(Scenes[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the scene and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(SceneName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Scenes[FinalChoice][0],
                Scenes[FinalChoice][1]
            )


class SceneFastOn(eg.ActionBase):
    name = "Scene Fast On"
    description = "Turns a scene on instantly."

    def __call__(self, SceneName="", SceneNum=""):
        if VerboseMode:
            print "Turning on Scene " + SceneNum + " fast"

        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print Address
        # print Port
        # s.connect((Address, Port))

        commands = {}
        commands['faston'] = '02 61 %s 12 %s' % (SceneNum, SceneNum)

        if VerboseMode:
            print "Sending Command: %s" % commands['faston']

        command = ascii2bin(commands['faston'])
        c.sendcommand(command)

    def Configure(self, SceneName="", SceneNum=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a scene from the list below...", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Scenes)):
            ChoiceList.append(Scenes[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the scene and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(SceneName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Scenes[FinalChoice][0],
                Scenes[FinalChoice][1]
            )


class SceneFastOff(eg.ActionBase):
    name = "Scene Fast Off"
    description = "Turns a scene off instantly."

    def __call__(self, SceneName="", SceneNum=""):
        if VerboseMode:
            print "Turning on Scene " + SceneNum + " fast"

        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print Address
        # print Port
        # s.connect((Address, Port))

        commands = {}
        commands['fastoff'] = '02 61 %s 14 %s' % (SceneNum, SceneNum)

        if VerboseMode:
            print "Sending Command: %s" % commands['fastoff']

        command = ascii2bin(commands['fastoff'])
        c.sendcommand(command)

    def Configure(self, SceneName="", SceneNum=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a scene from the list below...", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Scenes)):
            ChoiceList.append(Scenes[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the scene and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(SceneName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Scenes[FinalChoice][0],
                Scenes[FinalChoice][1]
            )


class DeviceOn(eg.ActionBase):
    name = "Device On"
    description = "Turns a device on using the predefined ramp rate at brightness level."

    def __call__(self, DeviceName, DeviceNum):
        if VerboseMode:
            print "Turning on device " + DeviceNum

        commands = {}
        commands['on'] = '02 62 %s 0F 11 FF' % DeviceNum

        if VerboseMode:
            print "Sending Command: %s" % commands['on']

        command = ascii2bin(commands['on'])
        c.sendcommand(command)

    def Configure(self, DeviceName="", DeviceNum=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a device from the list below...", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Devices)):
            ChoiceList.append(Devices[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(DeviceName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Devices[FinalChoice][0],
                Devices[FinalChoice][1]
            )


class DeviceOff(eg.ActionBase):
    name = "Device Off"
    description = "Turns a device off using the predefined ramp rate at brightness level."

    def __call__(self, DeviceName, DeviceNum):
        if VerboseMode:
            print "Turning off device " + DeviceNum

        commands = {}
        commands['off'] = '02 62 %s 0F 13 00' % DeviceNum

        if VerboseMode:
            print "Sending Command: %s" % commands['off']

        command = ascii2bin(commands['off'])
        c.sendcommand(command)

    def Configure(self, DeviceName="", DeviceNum=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a device from the list below...", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Devices)):
            ChoiceList.append(Devices[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(DeviceName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Devices[FinalChoice][0],
                Devices[FinalChoice][1]
            )


class DeviceFastOn(eg.ActionBase):
    name = "Device Fast On"
    description = "Turns a device on instantly."

    def __call__(self, DeviceName, DeviceNum):
        if VerboseMode:
            print "Turning off device " + DeviceNum + " fast"

        commands = {}
        commands['on'] = '02 62 %s 0F 12 FF' % DeviceNum

        if VerboseMode:
            print "Sending Command: %s" % commands['on']

        command = ascii2bin(commands['on'])
        c.sendcommand(command)

    def Configure(self, DeviceName="", DeviceNum=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a device from the list below...", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Devices)):
            ChoiceList.append(Devices[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(DeviceName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Devices[FinalChoice][0],
                Devices[FinalChoice][1]
            )


class DeviceFastOff(eg.ActionBase):
    name = "Device Fast Off"
    description = "Turns a device off instantly."

    def __call__(self, DeviceName, DeviceNum):
        if VerboseMode:
            print "Turning off device " + DeviceNum + " fast"

        commands = {}
        commands['off'] = '02 62 %s 0F 14 00' % DeviceNum

        if VerboseMode:
            print "Sending Command: %s" % commands['off']

        command = ascii2bin(commands['off'])
        c.sendcommand(command)

    def Configure(self, DeviceName="", DeviceNum=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a device from the list below...", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Devices)):
            ChoiceList.append(Devices[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(DeviceName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Devices[FinalChoice][0],
                Devices[FinalChoice][1]
            )


class DeviceToLevel(eg.ActionBase):
    name = "Device To Level"
    description = "Sets a device to the desired level using the predefined ramp rate."

    def __call__(self, DeviceName, DeviceNum, DeviceLevel):
        if VerboseMode:
            print "Turning on device " + DeviceNum

        commands = {}
        commands['on'] = '02 62 %s 0F 11 %s' % (DeviceNum, DeviceLevel)

        if VerboseMode:
            print "Sending Command: %s" % commands['on']

        command = ascii2bin(commands['on'])
        c.sendcommand(command)

    def Configure(self, DeviceName="", DeviceNum="", DeviceLevel=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(5, 1)
        mySizer.AddGrowableCol(0)

        sliderSizer = wx.GridBagSizer(1, 3)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a device and level using the list and slider below...",
                                         (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Devices)):
            ChoiceList.append(Devices[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(DeviceName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        LevelData = [
            ["OFF", "00"],
            ["10%", "1A"],
            ["20%", "33"],
            ["30%", "4D"],
            ["40%", "66"],
            ["50%", "80"],
            ["60%", "99"],
            ["70%", "B3"],
            ["80%", "CC"],
            ["90%", "E6"],
            ["ON", "FF"]
        ]

        LevelList = []
        for i in range(len(LevelData)):
            LevelList.append(LevelData[i][0])

        # Setup Level Slider
        slider = wx.Slider(panel, -1, 10, 0, 10, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)

        # Identify the level and set the slider accordingly
        p = 0
        pList = []
        for q in range(len(LevelData)):
            pList.append(LevelData[q][1])
        try:
            p = pList.index(DeviceLevel)
            slider.SetValue(p)
        except ValueError:
            slider.SetValue(10)

        sliderVal = wx.StaticText(panel, -1, LevelData[slider.GetValue()][0])

        def sliderUpdate(self):
            sliderVal.SetLabel(LevelData[slider.GetValue()][0])

        slider.Bind(wx.EVT_SLIDER, sliderUpdate)

        # Build Dialog Box
        sliderSizer.Add(sliderVal, (0, 0), flag=wx.EXPAND)
        sliderSizer.Add(slider, (0, 2), flag=wx.EXPAND)
        sliderSizer.AddGrowableCol(2)
        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=wx.EXPAND)
        mySizer.Add(sliderSizer, (3, 0), flag=wx.EXPAND)

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            FinalLevel = slider.GetValue()
            panel.SetResult(
                Devices[FinalChoice][0],
                Devices[FinalChoice][1],
                LevelData[FinalLevel][1]
            )


class DeviceRampOn(eg.ActionBase):
    name = "Device Ramp Up"
    description = "Ramps a device up to the desired brightness level over a specified time interval."

    def __call__(self, DeviceName, DeviceNum, RampRate, Level):
        if VerboseMode:
            print "Ramping device " + DeviceNum

        RampCommand = Level + RampRate

        commands = {}
        commands['on'] = '02 62 %s 0F 2E %s' % (DeviceNum, RampCommand)

        if VerboseMode:
            print "Sending Command: %s" % commands['on']

        command = ascii2bin(commands['on'])
        c.sendcommand(command)

    def Configure(self, DeviceName="", DeviceNum="", RampRate="", Level=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(6, 1)
        mySizer.AddGrowableCol(0)

        sliderSizer = wx.GridBagSizer(1, 5)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1,
                                         "Select a device, brightness level and ramp duration using the lists and slider below...",
                                         (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Devices)):
            ChoiceList.append(Devices[i][0])
        ChoiceList.sort()

        LevelValues = [
            ["OFF", "0"],
            ["10%", "1"],
            ["20%", "3"],
            ["30%", "4"],
            ["40%", "6"],
            ["50%", "8"],
            ["60%", "9"],
            ["70%", "B"],
            ["80%", "C"],
            ["90%", "E"],
            ["ON", "F"]
        ]

        LevelList = []
        for i in range(len(LevelValues)):
            LevelList.append(LevelValues[i][0])

        RateValues = [
            ["0.1s", "F"],
            ["0.3s", "E"],
            ["2s", "D"],
            ["7s", "C"],
            ["19s", "B"],
            ["24s", "A"],
            ["28s", "9"],
            ["32s", "8"],
            ["39s", "7"],
            ["47s", "6"],
            ["1m30s", "5"],
            ["2m30s", "4"],
            ["3m30s", "3"],
            ["4m30s", "2"],
            ["6m", "1"],
            ["8m", "0"]
        ]

        RateList = []
        for i in range(len(RateValues)):
            RateList.append(RateValues[i][0])

        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(DeviceName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        RateDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=RateList)

        # Identify the rate and set dropdown to correct position
        p = 0
        pList = []
        for q in range(len(RateValues)):
            pList.append(RateValues[q][1])
        try:
            p = pList.index(RampRate)
            RateDropDown.SetSelection(p)
        except ValueError:
            RateDropDown.SetSelection(2)

        # Setup Time Slider
        slider = wx.Slider(panel, -1, 10, 0, 10, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)

        # Identify the level and set the slider accordingly
        p = 0
        pList = []
        for q in range(len(LevelValues)):
            pList.append(LevelValues[q][1])
        try:
            p = pList.index(Level)
            slider.SetValue(p)
        except ValueError:
            slider.SetValue(10)

        sliderVal = wx.StaticText(panel, -1, LevelValues[slider.GetValue()][0])

        def sliderUpdate(self):
            sliderVal.SetLabel(LevelValues[slider.GetValue()][0])

        slider.Bind(wx.EVT_SLIDER, sliderUpdate)

        # Build Dialog Box
        sliderSizer.Add(sliderVal, (0, 0), flag=wx.EXPAND)
        sliderSizer.Add(slider, (0, 2), flag=wx.EXPAND)
        sliderSizer.Add(RateDropDown, (0, 4), flag=wx.EXPAND)
        sliderSizer.AddGrowableCol(2)
        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=wx.EXPAND)
        mySizer.Add(sliderSizer, (3, 0), flag=wx.EXPAND)

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            FinalRate = RateDropDown.GetCurrentSelection()
            FinalLevel = slider.GetValue()
            panel.SetResult(
                Devices[FinalChoice][0],
                Devices[FinalChoice][1],
                RateValues[FinalRate][1],
                LevelValues[FinalLevel][1]
            )


class DeviceRampOff(eg.ActionBase):
    name = "Device Ramp Down"
    description = "Ramps a device down to the desired brightness level over a specified time interval."

    def __call__(self, DeviceName, DeviceNum, RampRate, Level):
        if VerboseMode:
            print "Ramping device " + DeviceNum

        RampCommand = RampRate + Level

        commands = {}
        commands['off'] = '02 62 %s 0F 2F %s' % (DeviceNum, RampCommand)

        if VerboseMode:
            print "Sending Command: %s" % commands['off']

        command = ascii2bin(commands['off'])
        c.sendcommand(command)

    def Configure(self, DeviceName="", DeviceNum="", RampRate="", Level=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(6, 1)
        mySizer.AddGrowableCol(0)

        sliderSizer = wx.GridBagSizer(1, 5)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1,
                                         "Select a device, brightness level and ramp duration using the lists and slider below...",
                                         (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Devices)):
            ChoiceList.append(Devices[i][0])
        ChoiceList.sort()

        LevelValues = [
            ["OFF", "0"],
            ["10%", "1"],
            ["20%", "3"],
            ["30%", "4"],
            ["40%", "6"],
            ["50%", "8"],
            ["60%", "9"],
            ["70%", "B"],
            ["80%", "C"],
            ["90%", "E"],
            ["ON", "F"]
        ]

        LevelList = []
        for i in range(len(LevelValues)):
            LevelList.append(LevelValues[i][0])

        RateValues = [
            ["0.1s", "F"],
            ["0.3s", "E"],
            ["2s", "D"],
            ["7s", "C"],
            ["19s", "B"],
            ["24s", "A"],
            ["28s", "9"],
            ["32s", "8"],
            ["39s", "7"],
            ["47s", "6"],
            ["1m30s", "5"],
            ["2m30s", "4"],
            ["3m30s", "3"],
            ["4m30s", "2"],
            ["6m", "1"],
            ["8m", "0"]
        ]

        RateList = []
        for i in range(len(RateValues)):
            RateList.append(RateValues[i][0])

        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(DeviceName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        RateDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=RateList)

        # Identify the rate and set dropdown to correct position
        p = 0
        pList = []
        for q in range(len(RateValues)):
            pList.append(RateValues[q][1])
        try:
            p = pList.index(RampRate)
            RateDropDown.SetSelection(p)
        except ValueError:
            RateDropDown.SetSelection(2)

        # Setup Time Slider
        slider = wx.Slider(panel, -1, 10, 0, 10, style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS)

        # Identify the level and set the slider accordingly
        p = 0
        pList = []
        for q in range(len(LevelValues)):
            pList.append(LevelValues[q][1])
        try:
            p = pList.index(Level)
            slider.SetValue(p)
        except ValueError:
            slider.SetValue(10)

        sliderVal = wx.StaticText(panel, -1, LevelValues[slider.GetValue()][0])

        def sliderUpdate(self):
            sliderVal.SetLabel(LevelValues[slider.GetValue()][0])

        slider.Bind(wx.EVT_SLIDER, sliderUpdate)

        # Build Dialog Box
        sliderSizer.Add(sliderVal, (0, 0), flag=wx.EXPAND)
        sliderSizer.Add(slider, (0, 2), flag=wx.EXPAND)
        sliderSizer.Add(RateDropDown, (0, 4), flag=wx.EXPAND)
        sliderSizer.AddGrowableCol(2)
        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=wx.EXPAND)
        mySizer.Add(sliderSizer, (3, 0), flag=wx.EXPAND)

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            FinalRate = RateDropDown.GetCurrentSelection()
            FinalLevel = slider.GetValue()
            panel.SetResult(
                Devices[FinalChoice][0],
                Devices[FinalChoice][1],
                RateValues[FinalRate][1],
                LevelValues[FinalLevel][1]
            )


class DeviceStatus(eg.ActionBase):
    name = "Device Status"
    description = "Pings a specified device so that the Smartlinc Monitor can capture its status."

    def __call__(self, DeviceName, DeviceNum):
        if VerboseMode:
            print "Getting status for device " + DeviceNum

        commands = {}
        commands['on'] = '02 62 %s 0F 19 FF' % DeviceNum

        if VerboseMode:
            print "Sending Command: %s" % commands['on']

        command = ascii2bin(commands['on'])
        c.sendcommand(command)

    def Configure(self, DeviceName="", DeviceNum=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a device from the list below...", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Devices)):
            ChoiceList.append(Devices[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(DeviceName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Devices[FinalChoice][0],
                Devices[FinalChoice][1]
            )


class DeviceCustom(eg.ActionBase):
    name = "Custom Command"
    description = "Sends a custom command to a predetermined device."

    def __call__(self, DeviceName, DeviceNum, Custom):
        if VerboseMode:
            print "Sending custom command to " + DeviceNum

        commands = {}
        commands['on'] = '02 62 %s %s' % (DeviceNum, Custom)
        time.sleep(1)
        if VerboseMode:
            print "Sending Command: %s" % commands['on']

        command = ascii2bin(commands['on'])
        c.sendcommand(command)

    def Configure(self, DeviceName="", DeviceNum="", Custom=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(5, 1)
        # mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1,
                                         "Select a device from the list below, and enter a command in HEX format...",
                                         (12, 15), (100, 20))
        TextCustomInfo = wx.StaticText(panel, -1, "Command:", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Devices)):
            ChoiceList.append(Devices[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(DeviceName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        CustomBox = wx.TextCtrl(panel, -1, Custom)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))
        mySizer.Add(TextCustomInfo, (3, 0), flag=wx.EXPAND)
        mySizer.Add(CustomBox, (4, 0), flag=wx.EXPAND)

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Devices[FinalChoice][0],
                Devices[FinalChoice][1],
                CustomBox.GetValue()
            )


class DevicextenOn(eg.ActionBase):
    name = "X10 Device On"
    description = "Turns an X10 device on"

    def __call__(self, DeviceName, DeviceNum):

        if VerboseMode:
            print "Addressing device: " + DeviceName

        commands = {}
        commands['Address'] = '02 63 %s 00' % DeviceNum

        if VerboseMode:
            print "Sending Command: %s" % commands['Address']

        command = ascii2bin(commands['Address'])
        c.sendcommand(command)
        time.sleep(1.0)
        if VerboseMode:
            print "Turning on device: " + DeviceName

        commands = {}
        commands['on'] = '02 63 E2 80'

        if VerboseMode:
            print "Sending Command: %s" % commands['on']

        command = ascii2bin(commands['on'])
        c.sendcommand(command)
        eventTxt = DeviceName + ".On"
        eg.TriggerEvent(eventTxt, prefix='SmartLinc')

    def Configure(self, DeviceName="", DeviceNum=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a device from the list below...", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Devices)):
            ChoiceList.append(Devices[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(DeviceName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Devices[FinalChoice][0],
                Devices[FinalChoice][1]
            )
        # def DHC(self, DHC="" DDI="")
        if DeviceNum == 2:
            UHC = DeviceNum[0:1]
            UDI = DeviceNum[1:2]

            if (UHC == "A"):
                DHC = "6"
            if (UHC == "B"):
                DHC = "E"
            if (UHC == "C"):
                DHC = "2"
            if (UHC == "D"):
                DHC = "A"
            if (UHC == "E"):
                DHC = "1"
            if (UHC == "F"):
                DHC = "9"
            if (UHC == "G"):
                DHC = "I"
            if (UHC == "H"):
                DHC = "D"
            if (UHC == "I"):
                DHC = "7"
            if (UHC == "J"):
                DHC = "F"
            if (UHC == "K"):
                DHC = "3"
            if (UHC == "L"):
                DHC = "B"
            if (UHC == "M"):
                DHC = "0"
            if (UHC == "N"):
                DHC = "8"
            if (UHC == "O"):
                DHC = "4"
            if (UHC == "P"):
                DHC = "C"
            if (UDI == "1"):
                DDI = "6"
            if (UDI == "2"):
                DDI = "E"
            if (UDI == "3"):
                DDI = "2"
            if (UDI == "4"):
                DDI = "A"
            if (UDI == "5"):
                DDI = "1"
            if (UDI == "6"):
                DDI = "9"
            if (UDI == "7"):
                DDI = "I"
            if (UDI == "8"):
                DDI = "D"
            if (UDI == "9"):
                DDI = "7"
            if (UDI == "10"):
                DDI = "F"
            if (UDI == "11"):
                DDI = "3"
            if (UDI == "12"):
                DDI = "B"
            if (UDI == "13"):
                DDI = "0"
            if (UDI == "14"):
                DDI = "8"
            if (UDI == "15"):
                DDI = "4"
            if (UDI == "16"):
                DDI = "C"


class DevicextenOff(eg.ActionBase):
    name = "X10 Device Off"
    description = "Turns an X10 device off"

    def __call__(self, DeviceName, DeviceNum):
        if VerboseMode:
            print "Addressing device: " + DeviceName

        commands = {}
        commands['Address'] = '02 63 %s 00' % DeviceNum
        if VerboseMode:
            print "Sending Command: %s" % commands['Address']

        command = ascii2bin(commands['Address'])
        c.sendcommand(command)
        time.sleep(1.0)
        if VerboseMode:
            print "Turning off device: " + DeviceName

        commands = {}
        commands['off'] = '02 63 E3 80'

        if VerboseMode:
            print "Sending Command: %s" % commands['off']

        command = ascii2bin(commands['off'])
        c.sendcommand(command)
        eventTxt = DeviceName + ".Off"
        eg.TriggerEvent(eventTxt, prefix='SmartLinc')

    def Configure(self, DeviceName="", DeviceNum=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a device from the list below...", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Devices)):
            ChoiceList.append(Devices[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(DeviceName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Devices[FinalChoice][0],
                Devices[FinalChoice][1]
            )


class DeviceBright(eg.ActionBase):
    name = "Device Bright One Step"
    description = "Brightens a device one Step."

    def __call__(self, DeviceName, DeviceNum):
        if VerboseMode:
            print "Brighten command sent to " + DeviceName

        commands = {}
        commands['bright'] = '02 62 %s 0F 15 01' % DeviceNum

        if VerboseMode:
            print "Sending Command: %s" % commands['bright']

        command = ascii2bin(commands['bright'])
        c.sendcommand(command)
        time.sleep(0.5)
        commands['status'] = '02 62 %s 0F 19 FF' % DeviceNum

        command = ascii2bin(commands['status'])
        c.sendcommand(command)

    def Configure(self, DeviceName="", DeviceNum=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a device from the list below...", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Devices)):
            ChoiceList.append(Devices[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(DeviceName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Devices[FinalChoice][0],
                Devices[FinalChoice][1]
            )


class DeviceDim(eg.ActionBase):
    name = "Device Dim One Step"
    description = "Dims a device one Step."

    def __call__(self, DeviceName, DeviceNum):
        if VerboseMode:
            print "Dim command sent to " + DeviceName

        commands = {}
        commands['dim'] = '02 62 %s 0F 16 01' % DeviceNum

        if VerboseMode:
            print "Sending Command: %s" % commands['dim']

        command = ascii2bin(commands['dim'])
        c.sendcommand(command)
        time.sleep(0.5)
        commands['status'] = '02 62 %s 0F 19 FF' % DeviceNum

        command = ascii2bin(commands['status'])
        c.sendcommand(command)

    def Configure(self, DeviceName="", DeviceNum=""):
        panel = eg.ConfigPanel()

        mySizer = wx.GridBagSizer(2, 1)
        mySizer.AddGrowableRow(1)
        mySizer.AddGrowableCol(0)

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        TextSceneAddInfo = wx.StaticText(panel, -1, "Select a device from the list below...", (12, 15), (100, 20))

        ChoiceList = []
        for i in range(len(Devices)):
            ChoiceList.append(Devices[i][0])
        ChoiceList.sort()
        SceneDropDown = wx.Choice(panel, -1, (0, 0), (100, 20), choices=ChoiceList)

        # Identify the device and set dropdown to correct position
        p = 0
        try:
            p = ChoiceList.index(DeviceName)
            SceneDropDown.SetSelection(p)
        except ValueError:
            SceneDropDown.SetSelection(0)

        mySizer.Add(TextSceneAddInfo, (0, 0), flag=wx.EXPAND)
        mySizer.Add(SceneDropDown, (1, 0), flag=(wx.ALIGN_TOP | wx.EXPAND))

        while panel.Affirmed():
            FinalChoice = SceneDropDown.GetCurrentSelection()
            panel.SetResult(
                Devices[FinalChoice][0],
                Devices[FinalChoice][1]
            )

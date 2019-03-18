# -*- coding: utf-8 -*-

help = """\
This plugin allows you to control yourTellstick through Switchkings REST API

Features:
Device ON / OFF
Device Fake ON / OFF (without sending a signal)
Device Dim
Device Fake Dim (without sending a signal)
Device By Schedule
Device Synchronize
Device Get State
Group ON / OFF
Group By Schedule
Group Synchronize
Scenario Activate
Set Datasource
Set System Mode
Device Get State (Get current state on a Device)

Events:
Data Source Events
Device Events
Scenario Events
Schedule Mode Events
Debug Mode, Print all REST Events

You need to have Switchking Server Server - v3.0.0 or later and the REST service enabled on the server.
The server should also accept TCP on port 8800 in the firewall, if any.

This plugins original author is Martin Engstrom and can be found here <a href="http://code.google.com/p/eventghost-switchking-plugin/">eventghost-switchking-plugin</a>
All credit goes to him.

Changelog
V0.0.8
Added some basic error handeling
Minor bugfixes
V0.0.9
REST API Bugfix
More error handeling
V0.1.0
Bugfixes

woggy81@gmail.com
"""

import eg

VER = "V0.1.0"

eg.RegisterPlugin(
    name="Switch King",
    author=u"Niclas H\xe5kansson",
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=4054",
    version=VER,
    guid="{E6942BEF-8706-48A9-80F6-EA0359A124E9}",
    canMultiLoad=True,
    kind="program",
    description=' This plugin allows you to control your <a href="http://www.telldus.se/products/tellstick">Tellstick</a> through <a href="http://www.switchking.se/en/downloads">Switchkings</a> REST API',
    help=help,
)

import re, htmlentitydefs
import httplib
import sys
import traceback
import urllib2
import socket
import base64
import os
import time
from xml.dom.minidom import parse, parseString
from threading import Event, Thread
from operator import itemgetter
# from collections import deque
from urllib2 import Request, urlopen, URLError


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is

    return re.sub("&#?\w+;", fixup, text)


class swki:
    def __init__(self):
        self.headers = {}
        self.user = ''
        self.password = ''
        self.host = ''
        self.port = ''
        self.ids = {}
        self.lst = []
        self.dimlst = []
        self.grpids = {}
        self.grplst = []
        self.scenids = {}
        self.scenlst = []
        self.dsids = {}
        self.dslst = []
        self.modeids = {}
        self.modelst = []
        self.DeviceName = []

    def Prime(self, host, port, user, password, debug, event1, event2, event3, event4):
        self.user = user
        self.password = password
        self.host = host
        self.debug = debug
        self.event1 = event1
        self.event2 = event2
        self.event3 = event3
        self.event4 = event4

        self.port = unicode(port)
        self.headers["Authorization"] = "Basic {0}".format(base64.b64encode("{0}:{1}".format(user, password)))
        self.headers["Connection"] = "Keep-Alive"

    #        self.headers["Accept-Encoding"] = "*/*"

    def connect(self, URL, TagName):

        self.error = 'no'

        try:
            urllib2.urlopen("http://" + self.host + ":" + self.port + URL, timeout=4)

        except URLError, e:
            if hasattr(e, 'reason'):  # <--
                eg.PrintError('Failed to reach the Switch King server. Check Hostname and Port')
                eg.PrintError('Reason: ', str(e.reason))
                self.error = 'yes'

        if self.error == 'no':
            conn = httplib.HTTPConnection(self.host + ":" + self.port)
            conn.request('GET', "http://" + self.host + ":" + self.port + URL, None, self.headers)

            resp = conn.getresponse()
            if resp.status == 401:
                errormsg = str(resp.status) + ' ' + str(resp.reason)
                conn.close()
                eg.PrintError(errormsg)
                eg.PrintError('Check Switch King Username and Password')
                self.error = 'yes'
            else:
                self.error = 'no'
                content = resp.read()
                dom = parseString(content)
                self.DeviceName = dom.getElementsByTagName(TagName)
                return self.DeviceName

    # -------------------------------------------------- Read Data --------------------------------------------------

    def GetSystemMode(self):
        self.modeids = {}
        self.modename = {}
        self.modelst = []

        self.connect('/systemmodes', "RESTSystemMode")
        for device in self.DeviceName:
            dev_id = device.getElementsByTagName("ID")[0].childNodes[0].data
            dev_nm = unescape(device.getElementsByTagName("Name")[0].childNodes[0].data)
            self.modeids[dev_nm] = dev_id
            self.modelst.append(dev_nm)
            self.modename[dev_id] = dev_nm
        return self.modelst

    def GetDevices(self):
        self.ids = {}
        self.ids2 = {}
        self.lst = []
        self.dimlst = []
        self.connect('/devices', "RESTDevice")
        for device in self.DeviceName:
            dev_state = device.getElementsByTagName("CurrentStateID")[0].childNodes[0].data
            dev_id = device.getElementsByTagName("ID")[0].childNodes[0].data
            dev_nm = unescape(device.getElementsByTagName("Name")[0].childNodes[0].data)
            dimmer = device.getElementsByTagName("SupportsAbsoluteDimLvl")[0].childNodes[0].data
            if (dimmer == "true"):
                self.dimlst.append(dev_nm)
            self.ids[dev_nm] = dev_id
            self.ids2[dev_nm] = dev_state
            self.lst.append(dev_nm)
        return self.lst, self.dimlst

    def GetDeviceGroups(self):
        self.grpids = {}
        self.grplst = []
        self.connect('/devicegroups', "RESTDeviceGroup")

        for device in self.DeviceName:
            dev_id = device.getElementsByTagName("ID")[0].childNodes[0].data
            if (dev_id == "-1"):
                continue
            dev_nm = device.getElementsByTagName("Name")[0].childNodes[0].data
            dev_nm = unescape(dev_nm)
            self.grpids[dev_nm] = dev_id
            self.grplst.append(dev_nm)
        return self.grplst

    def GetScenarios(self):
        self.scenids = {}
        self.scenlst = []

        self.connect('/scenarios', "RESTScenario")
        for device in self.DeviceName:
            dev_id = device.getElementsByTagName("ID")[0].childNodes[0].data
            dev_nm = unescape(device.getElementsByTagName("Name")[0].childNodes[0].data)
            self.scenids[dev_nm] = dev_id
            self.scenlst.append(dev_nm)
        return self.scenlst

    def GetDataSources(self):
        self.dsids = {}
        self.dsname = {}
        self.dslst = []

        self.connect('/datasources', "RESTDataSource")
        for device in self.DeviceName:
            dev_id = device.getElementsByTagName("ID")[0].childNodes[0].data
            dev_nm = unescape(device.getElementsByTagName("Name")[0].childNodes[0].data)
            self.dsids[dev_nm] = dev_id
            self.dsname[dev_id] = dev_nm
            self.dslst.append(dev_nm)
        return self.dslst

    # -------------------------------------------------- Write Data --------------------------------------------------

    def SetSystemMode(self, devnm, command):
        URL = '/systemmodes/' + self.modeids[devnm] + '/' + command
        self.connect(URL, "RESTDataSource")

    def SetDevice(self, devnm, command):
        URL = '/devices/' + self.ids[devnm] + '/' + command
        self.connect(URL, "RESTDataSource")

    def SetDeviceGroup(self, grpnm, command):
        URL = '/devicegroups/' + self.grpids[grpnm] + '/' + command
        self.connect(URL, "RESTDataSource")

    def SetScenario(self, grpnm):
        URL = '/commandqueue?operation=changescenario&target=' + self.scenids[grpnm] + '&param1=&param2=&param3='
        self.connect(URL, "RESTDataSource")

    def SetDataSource(self, grpnm, value):
        URL = '/datasources/' + self.dsids[grpnm] + '/addvalue?value=' + value
        self.cnnect(URL, "RESTDataSource")

    # -------------------------------------------------- Recive Data  --------------------------------------------------

    def State(self, devnm, command):

        URL = '/devices/' + self.ids[devnm]
        self.connect(URL, "RESTDevice")
        for device in self.DeviceName:
            CurrentStateID = device.getElementsByTagName("CurrentStateID")[0].childNodes[0].data
            dimmer = device.getElementsByTagName("SupportsAbsoluteDimLvl")[0].childNodes[0].data
            level = device.getElementsByTagName("CurrentDimLevel")[0].childNodes[0].data

            if CurrentStateID == "1":
                state = "OFF"
                if level == '-1':
                    level = '0'
            if CurrentStateID == "2":
                state = "ON"
                if level == '-1':
                    level = '100'

            event = devnm.replace(' ', '.').replace('-', '').replace('_', '').replace('..', '.') + '.' + state
            if (dimmer == "true"):
                eg.TriggerEvent(event, payload=str(level) + '%', prefix="Switchking")
            else:
                eg.TriggerEvent(event, prefix="Switchking")


# -------------------------------------------------- PluginClass --------------------------------------------------

class SwitchkingTellStick(eg.PluginClass):

    def __init__(self):
        ButtonsGroup = self.AddGroup("Devices", "Individual Devices", "icons/Device")
        ButtonsGroup.AddAction(DevTurnOn)
        ButtonsGroup.AddAction(DevFakeOn)
        ButtonsGroup.AddAction(DevTurnOff)
        ButtonsGroup.AddAction(DevFakeOff)
        ButtonsGroup.AddAction(DevDim)
        ButtonsGroup.AddAction(DevDimFake)
        ButtonsGroup.AddAction(DevCancelsemiauto)
        ButtonsGroup.AddAction(DevSynchronize)

        ButtonsGroup = self.AddGroup("Groups", "Groups of Devices", "icons/Group")
        ButtonsGroup.AddAction(DevGrpTurnOn)
        ButtonsGroup.AddAction(DevGrpTurnOff)
        ButtonsGroup.AddAction(DevGrpCancelsemiauto)
        ButtonsGroup.AddAction(DevGrpSynchronize)
        self.AddAction(DevGetState)
        self.AddAction(ScenAct)
        self.AddAction(DSSet)
        self.AddAction(SystemModeSet)
        self.sk = swki()

    def __start__(self, host, port, user, password, debug, event1, event2, event3, event4):
        print "Starting Switchking " + VER

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.debug = debug
        self.event1 = event1
        self.event2 = event2
        self.event3 = event3
        self.event4 = event4

        self.sk.Prime(host, port, user, password, debug, event1, event2, event3, event4)
        self.sk.connect('', "RESTDevice")
        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.ThreadLoop,
            args=(self.stopThreadEvent,)
        )

        if self.sk.error == 'yes':
            pass
        else:
            dummy = self.sk.GetDevices()
            dummy = self.sk.GetDeviceGroups()
            dummy = self.sk.GetScenarios()
            dummy = self.sk.GetDataSources()
            dummy = self.sk.GetSystemMode()

            if self.debug == True or self.event1 == True or self.event2 == True or self.event3 == True or self.event4 == True:  # only read REST events if needed
                thread.start()
                print "Starting Switchking event listener"

    def __stop__(self):
        self.stopThreadEvent.set()

    def ThreadLoop(self, stopThreadEvent):
        self.lista = []
        self.sk.connect('/entitylogentries/latest', "RESTEntityLogEntry")
        for device in self.sk.DeviceName:
            Date = device.getElementsByTagName("Date")[0].childNodes[0].data
            dev_id = device.getElementsByTagName("ID")[0].childNodes[0].data
            max_id = dev_id
            max_tid = Date

        while not stopThreadEvent.isSet():
            if self.sk.error == 'yes':
                self.stopThreadEvent.set()
            try:
                URL = '/entitylogentries?maxcount=400&newerthan=' + max_tid[:25]
                self.sk.connect(URL, "RESTEntityLogEntry")
                self.lista2 = []

                for device in self.sk.DeviceName:
                    Date = device.getElementsByTagName("Date")[0].childNodes[0].data
                    dev_id = device.getElementsByTagName("ID")[0].childNodes[0].data
                    self.lista2.append(dev_id)

                self.lista2.sort()
                for i in self.lista2:
                    for device in self.sk.DeviceName:
                        try:
                            dev_id = device.getElementsByTagName("ID")[0].childNodes[0].data
                        except IndexError:
                            pass

                        if i == dev_id:

                            if self.lista.count(i) == 0:
                                self.lista.append(i)
                                self.lista2.remove(i)
                                max_tid = Date

                                try:
                                    Info = device.getElementsByTagName("Info")[0].childNodes[0].data
                                except Exception:
                                    Info = ''

                                EntityType = device.getElementsByTagName("EntityType")[0].childNodes[0].data
                                Operation = device.getElementsByTagName("Operation")[0].childNodes[0].data
                                EntityID = device.getElementsByTagName("EntityID")[0].childNodes[0].data

                                if EntityType == 'DataSourceValue':
                                    RelatedID = device.getElementsByTagName("RelatedID")[0].childNodes[0].data
                                    URL = '/datasources/' + RelatedID
                                    self.sk.connect(URL, 'RESTDataSource')

                                    for device in self.sk.DeviceName:
                                        try:
                                            UsedValue = device.getElementsByTagName("UsedValue")[0].childNodes[0].data
                                        except Exception:
                                            UsedValue = ''
                                        try:
                                            IDName = self.sk.dsname[RelatedID]
                                        except Exception:
                                            IDName = ''
                                            if self.debug == True:
                                                var = traceback.format_exc()
                                                eg.PrintError(str(var))
                                            else:
                                                pass
                                        if self.debug == True:
                                            print dev_id, EntityType, Operation, Info, IDName, UsedValue
                                        if self.event1 == True:
                                            event = 'DataSource' + '.' + IDName.replace(' ', '.').replace('-',
                                                                                                          '').replace(
                                                '_', '').replace('..', '.')
                                            eg.TriggerEvent(event, payload=str(UsedValue), prefix="Switchking")



                                elif EntityType == 'Device':
                                    URL = '/devices/' + EntityID
                                    self.sk.connect(URL, "RESTDevice")

                                    for device in self.sk.DeviceName:
                                        Name = unescape(device.getElementsByTagName("Name")[0].childNodes[0].data)
                                        CurrentStateID = device.getElementsByTagName("CurrentStateID")[0].childNodes[
                                            0].data
                                        dimmer = device.getElementsByTagName("SupportsAbsoluteDimLvl")[0].childNodes[
                                            0].data
                                        level = device.getElementsByTagName("CurrentDimLevel")[0].childNodes[0].data

                                        if CurrentStateID == "1":
                                            state = "OFF"
                                            if level == '-1':
                                                level = '0'
                                        if CurrentStateID == "2":
                                            state = "ON"
                                            if level == '-1':
                                                level = '100'
                                        if self.debug == True:
                                            print dev_id, EntityType, Info, Name, EntityID, state

                                        if Info == 'Executing SetDeviceStateAndDimLevelByDeviceId' and self.event2 == True:
                                            event = Name.replace(' ', '.').replace('-', '').replace('_', '').replace(
                                                '..', '.') + '.' + state
                                            if (dimmer == "true"):
                                                eg.TriggerEvent(event, payload=str(level) + '%', prefix="Switchking")
                                            else:
                                                eg.TriggerEvent(event, prefix="Switchking")


                                elif EntityType == 'Scenario':
                                    self.sk.connect('/scenarios', "RESTScenario")
                                    for device in self.sk.DeviceName:
                                        Abbreviation = unescape(
                                            device.getElementsByTagName("Abbreviation")[0].childNodes[0].data)
                                        ID = device.getElementsByTagName("ID")[0].childNodes[0].data

                                        if EntityID == ID:
                                            if self.debug == True:
                                                print dev_id, EntityType, Info, Abbreviation
                                            if self.event3 == True:
                                                event = 'Scenario' + '.' + Abbreviation.replace(' ', '.').replace('-',
                                                                                                                  '').replace(
                                                    '_', '').replace('..', '.')
                                                eg.TriggerEvent(event, prefix="Switchking")

                                elif EntityType == 'ScheduleMode':
                                    if self.debug == True:
                                        print dev_id, EntityType, Info, self.sk.modename[EntityID]
                                    if self.event4 == True:
                                        event = 'SystemMode' + '.' + self.sk.modename[EntityID].replace(' ', '.')
                                        eg.TriggerEvent(event, prefix="Switchking")

                                elif EntityType == 'DataSource':
                                    EntityID = device.getElementsByTagName("EntityID")[0].childNodes[0].data
                                    URL = '/datasources/' + EntityID
                                    self.sk.connect(URL, 'RESTDataSource')

                                    for device in self.sk.DeviceName:
                                        try:
                                            IDName = self.sk.dsname[EntityID]
                                        except Exception:
                                            IDName = ''
                                            if self.debug == True:
                                                var = traceback.format_exc()
                                                eg.PrintError(str(var))
                                            else:
                                                pass

                                        if self.debug == True:
                                            print dev_id, EntityType, IDName + ' -', Info, Operation

                                else:
                                    if self.debug == True:
                                        print dev_id, EntityType, Info, EntityID

            except IndexError:
                if self.debug == True:
                    var = dev_id, EntityType
                    eg.PrintError(str(var))
                else:
                    pass

            except Exception:
                if self.debug == True:
                    var = traceback.format_exc()
                    eg.PrintError(str(var))
                else:
                    pass
            stopThreadEvent.wait(0.5)

    def Configure(self, host="localhost", port=8800, user="", password="", debug=False, event1=False, event2=False,
                  event3=False, event4=False):
        panel = eg.ConfigPanel()

        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        userCtrl = panel.TextCtrl(user)
        passwordCtrl = panel.TextCtrl(password, style=wx.TE_PASSWORD)
        debugCtrl = panel.CheckBox(debug)
        event1Ctrl = panel.CheckBox(event1)
        event2Ctrl = panel.CheckBox(event2)
        event3Ctrl = panel.CheckBox(event3)
        event4Ctrl = panel.CheckBox(event4)

        st1 = panel.StaticText("Host:")
        st2 = panel.StaticText("Port:")
        st3 = panel.StaticText("User:")
        st4 = panel.StaticText("Password:")
        st5 = panel.StaticText("Debug Mode, Print all REST Events and Raise Errors")
        st6 = panel.StaticText("Data Source Events")
        st7 = panel.StaticText("Device Events")
        st8 = panel.StaticText("Scenario Events")
        st9 = panel.StaticText("Schedule Mode Events")

        eg.EqualizeWidths((st1, st2, st3, st4))
        box1 = panel.BoxedGroup("Server", (st1, hostCtrl), (st2, portCtrl))
        box2 = panel.BoxedGroup("Credentials", (st3, userCtrl), (st4, passwordCtrl))
        box3 = panel.BoxedGroup("Debug", (debugCtrl, st5))
        box4 = panel.BoxedGroup("Event", (event1Ctrl, st6), (event2Ctrl, st7), (event3Ctrl, st8), (event4Ctrl, st9))

        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND | wx.TOP, 10),
            (box3, 0, wx.EXPAND),
            (box4, 0, wx.EXPAND),
        ])

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                userCtrl.GetValue(),
                passwordCtrl.GetValue(),
                debugCtrl.GetValue(),
                event1Ctrl.GetValue(),
                event2Ctrl.GetValue(),
                event3Ctrl.GetValue(),
                event4Ctrl.GetValue(),
            )


# -------------------------------------------------- ON / OFF Devices --------------------------------------------------


class ConfigDevice(object):  # Config All ON / OFF Devices

    def __init__(self):
        self.devicename = ""
        self.selection = 0

    def Configure(self, devicename="", selection=0):
        panel = eg.ConfigPanel()
        self.selection = selection
        dl, dummy = self.plugin.sk.GetDevices()
        deviceControl = wx.ListBox(
            panel,
            -1,
            choices=dl,
            style=wx.LB_SINGLE,
            size=(100, 100)
        )
        panel.sizer.Add(deviceControl, 0, wx.EXPAND)
        if dl:
            deviceControl.Select(selection)
        while panel.Affirmed():
            panel.SetResult(deviceControl.GetStringSelection(), deviceControl.GetSelection())


class DevTurnOn(ConfigDevice, eg.ActionClass):
    name = "Device ON"
    description = "Turns on a Switchking device."
    iconFile = "icons/DeviceOn"

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDevice(devicename, "turnon")


class DevTurnOff(ConfigDevice, eg.ActionClass):
    name = "Device OFF"
    description = "Turns off a Switchking device."
    iconFile = "icons/DeviceOff"

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDevice(devicename, "turnoff")


class DevFakeOn(ConfigDevice, eg.ActionClass):
    name = "Device ON Fake"
    description = "Turns on a Switchking device without sending a signal."
    iconFile = "icons/DeviceOn"

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDevice(devicename, "turnonfake")


class DevFakeOff(ConfigDevice, eg.ActionClass):
    name = "Device OFF Fake"
    description = "Turns off a Switchking device without sending a signal."
    iconFile = "icons/DeviceOff"

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDevice(devicename, "turnofffake")


class DevSynchronize(ConfigDevice, eg.ActionClass):
    name = "Device Synchronize"
    description = "Synchronize a Switchking device."
    iconFile = "icons/Sync"

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDevice(devicename, "synchronize")


class DevCancelsemiauto(ConfigDevice, eg.ActionClass):
    name = "Device By Schedule"
    description = "Set By Schedule on a Switchking device."
    iconFile = "icons/Schedule"

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDevice(devicename, "cancelsemiauto")


class DevGetState(ConfigDevice, eg.ActionClass):
    name = "Device Get State"
    description = "Get current state of device"

    # iconFile = "Sync"

    def __call__(self, devicename, selection):
        self.plugin.sk.State(devicename, "GetLogg")


# -------------------------------------------------- Dimmable Devices --------------------------------------------------

class ConfigDeviceDim(object):  # Config All Dimmable Devices

    def __init__(self):
        self.devicename = ""
        self.value = 0
        self.selction = 0

    def Configure(self, dummy="", devicename="", value=0, selection=0):
        self.value = value
        self.selection = selection
        panel = eg.ConfigPanel()
        dummy, dl = self.plugin.sk.GetDevices()
        dimControl = panel.SpinIntCtrl(self.value, min=0, max=100)
        deviceControl = wx.ListBox(
            panel,
            -1,
            choices=dl,
            style=wx.LB_SINGLE,
            size=(100, 100)
        )
        panel.sizer.Add(deviceControl, 0, wx.EXPAND)
        if dl:
            deviceControl.Select(selection)
        panel.sizer.Add(dimControl, 0)
        # valueEdit=panel.TextCtrl(value)
        # panel.AddLine("Value: ", valueEdit)
        while panel.Affirmed():
            name = deviceControl.GetStringSelection() + ": " + unicode(dimControl.GetValue()) + "%"
            panel.SetResult(name, deviceControl.GetStringSelection(), dimControl.GetValue(),
                            deviceControl.GetSelection())


class DevDim(ConfigDeviceDim, eg.ActionClass):
    name = "Device Dim"
    description = "Dims a Switchking device."
    iconFile = "icons/DeviceDim"

    def __call__(self, dummy, devicename, value, selection):
        self.plugin.sk.SetDevice(devicename, "dim/" + unicode(value))


class DevDimFake(ConfigDeviceDim, eg.ActionClass):
    name = "Device Dim Fake"
    description = "Set Dim Level in Switchking without sending a signal."
    iconFile = "icons/DeviceDim"

    def __call__(self, dummy, devicename, value, selection):
        self.plugin.sk.SetDevice(devicename, "dimfake/" + unicode(value))


# -------------------------------------------------- Group Devices --------------------------------------------------
class ConfigGroup(object):  # Config Groups

    def Configure(self, devicename="", selection=0):
        panel = eg.ConfigPanel()
        self.selection = selection
        dl = self.plugin.sk.GetDeviceGroups()
        # __init__(self, parent, id, pos, size, choices, style, validator, name)
        deviceControl = wx.ListBox(
            panel,
            -1,
            choices=dl,
            style=wx.LB_SINGLE,
            size=(100, 100)
        )
        panel.sizer.Add(deviceControl, 0, wx.EXPAND)
        if dl:
            deviceControl.Select(selection)
        while panel.Affirmed():
            panel.SetResult(deviceControl.GetStringSelection(), deviceControl.GetSelection())


class DevGrpTurnOn(ConfigGroup, eg.ActionClass):
    name = "Group ON"
    description = "Turns on a Switchking device group."
    iconFile = "icons/DeviceGroupOn"

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDeviceGroup(devicename, "turnon")


class DevGrpTurnOff(ConfigGroup, eg.ActionClass):
    name = "Group OFF"
    description = "Turns off a Switchking device group."
    iconFile = "icons/DeviceGroupOff"

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDeviceGroup(devicename, "turnoff")


class DevGrpCancelsemiauto(ConfigGroup, eg.ActionClass):
    name = "Group By Schedule"
    description = "Set By Schedule on a Switchking group."
    iconFile = "icons/Schedule"

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDeviceGroup(devicename, "cancelsemiauto")


class DevGrpSynchronize(ConfigGroup, eg.ActionClass):
    name = "Group Synchronize."
    description = "Synchronize a Switchking Group."
    iconFile = "icons/Sync"

    def __call__(self, devicename, selection):
        self.plugin.sk.SetDeviceGroup(devicename, "synchronize")


# -------------------------------------------------- Scenario --------------------------------------------------

class ScenAct(eg.ActionClass):
    name = "Scenario Activate"
    description = "Activates a Switchking scenario."
    iconFile = "icons/Scenario"

    def __init__(self):
        self.devicename = ""
        self.selection = 0

    def __call__(self, devicename, selection):
        self.plugin.sk.SetScenario(devicename)

    def Configure(self, devicename="", selection=0):
        panel = eg.ConfigPanel()
        self.selection = selection
        dl = self.plugin.sk.GetScenarios()
        deviceControl = wx.ListBox(
            panel,
            -1,
            choices=dl,
            style=wx.LB_SINGLE,
            size=(100, 100)
        )
        panel.sizer.Add(deviceControl, 0, wx.EXPAND)
        if dl:
            deviceControl.Select(selection)
        while panel.Affirmed():
            panel.SetResult(deviceControl.GetStringSelection(), deviceControl.GetSelection())


# --------------------------------------------------   --------------------------------------------------

class DSSet(eg.ActionClass):
    name = "Datasource, Set Value"
    description = "Set a value to a Switchking data source."
    iconFile = "icons/DataSource"

    def __init__(self):
        self.devicename = ""
        self.value = ""
        self.selction = 0

    def __call__(self, dummy, devicename, value, selection):
        self.plugin.sk.SetDataSource(devicename, value)

    def Configure(self, dummy="", devicename="", value="0", selection=0):
        panel = eg.ConfigPanel()
        self.value = value
        self.selection = selection
        dl = self.plugin.sk.GetDataSources()

        deviceControl = wx.ListBox(
            panel,
            -1,
            choices=dl,
            style=wx.LB_SINGLE,
            size=(100, 100)
        )
        panel.sizer.Add(deviceControl, 0, wx.EXPAND)
        if dl:
            deviceControl.Select(selection)
        valueEdit = panel.TextCtrl(value)
        panel.AddLine("Value: ", valueEdit)
        while panel.Affirmed():
            name = deviceControl.GetStringSelection() + ": " + unicode(valueEdit.GetValue())
            panel.SetResult(name, deviceControl.GetStringSelection(), valueEdit.GetValue(),
                            deviceControl.GetSelection())


# --------------------------------------------------   --------------------------------------------------

class SystemModeSet(eg.ActionClass):
    name = "System Mode"
    description = "Set System Mode."
    iconFile = "icons/SystemMode"

    def __init__(self):
        self.devicename = ""
        self.selection = 0

    def __call__(self, devicename, selection):
        self.plugin.sk.SetSystemMode(devicename, "activate")

    def Configure(self, devicename="", selection=0):
        panel = eg.ConfigPanel()
        self.selection = selection
        dl = self.plugin.sk.GetSystemMode()
        # __init__(self, parent, id, pos, size, choices, style, validator, name)
        deviceControl = wx.ListBox(
            panel,
            -1,
            choices=dl,
            style=wx.LB_SINGLE,
            size=(100, 100)
        )
        panel.sizer.Add(deviceControl, 0, wx.EXPAND)
        if dl:
            deviceControl.Select(selection)
        while panel.Affirmed():
            panel.SetResult(deviceControl.GetStringSelection(), deviceControl.GetSelection())

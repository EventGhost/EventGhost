# -*- coding: utf-8 -*-
#
# plugins/Homeseer/__init__.py
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

eg.RegisterPlugin(
    name = "Homeseer",
    guid = '{3B51BC0D-A030-4BF1-9E54-EBC3C236F582}',
    author = (
        "Smart Living",
        "krambriw",
    ),
    version = "0.0.4",
    kind = "external",
    description = "Homeseer plugin. More info on http://smart-living.geoblog.be/",
    url = "http://www.eventghost.org/forum/viewtopic.php?f=10&t=2692",
)

import eg
from win32com.client import Dispatch


class HomeseerPlugin(eg.PluginClass):

    def __init__(self):
        self.AddAction(OnOffCommand)
        self.AddAction(OffCommand)
        self.AddAction(OnCommand)
        self.AddAction(Speak)


    def __start__(self, hostname, username, password):
        self.hsi = Dispatch("HomeSeer2.application")
        self.connected = False
        self.hostname = hostname
        self.username = username
        self.password = password

        print "Trying to connect to Homeseer-host " + self.hostname + " using user " + self.username + "."
        self.hsi.SetHost(self.hostname)
        rval = self.hsi.Connect(self.username, self.password)
        if rval == "":
            print "Successfully connected to Homeseer " + self.hostname + " using user " + self.username + "."
            self.connected = True
        else:
            print "Error: " + rval
            self.hsi.Disconnect
            self.connected = False

        if self.connected:
            self.hs = Dispatch("homeseer.application")


    def __stop__(self):
        if self.connected:
            self.hsi.Disconnect
            print "Disconnected from Homeseer."
            self.connected = False


    def __close__(self):
        print "Homeseer plugin is now closed."


    def doSpeak(self, speech):
        if self.connected:
            print "Speaking " + speech
            self.hs.Speak(speech)
        else:
            print "Not connected to Homeseer."


    def doOnOffCommand(self, deviceCode):
        if self.connected:
            if self.hs.DeviceExistsRef(deviceCode)>-1: # krambriw: Check if the device exists
                if self.hs.IsOn(deviceCode):
                    command = "Off"
                else:
                    command = "On"

                print "Sending command " + command + " to " + deviceCode
                self.hs.ExecX10(deviceCode, command, 0, 0, False)
            else:
                print deviceCode + " does not exist in Homeseer configuration."
        else:
            print "Not connected to Homeseer."


    def doOffCommand(self, deviceCode):
        if self.connected:
            if self.hs.DeviceExistsRef(deviceCode)>-1: # krambriw: Check if the device exists
                command = "Off"
                print "Sending command " + command + " to " + deviceCode
                self.hs.ExecX10(deviceCode, command, 0, 0, False)
            else:
                print deviceCode + " does not exist in Homeseer configuration."
        else:
            print "Not connected to Homeseer."


    def doOnCommand(self, deviceCode):
        if self.connected:
            if self.hs.DeviceExistsRef(deviceCode)>-1: # krambriw: Check if the device exists
                command = "On"
                print "Sending command " + command + " to " + deviceCode
                self.hs.ExecX10(deviceCode, command, 0, 0, False)
            else:
                print deviceCode + " does not exist in Homeseer configuration."
        else:
            print "Not connected to Homeseer."


    def Configure(self, hostname="localhost", username="default", password="default"):
        panel = eg.ConfigPanel()

        hostnameTextControl = panel.TextCtrl(hostname)
        usernameTextControl = panel.TextCtrl(username)
        passwordTextControl = wx.TextCtrl(panel, -1, password, size=(175, -1), style=wx.TE_PASSWORD)

        sizer = wx.FlexGridSizer(rows=3, cols=2, hgap=10, vgap=5)
        sizer.Add(panel.StaticText("Homeseer Host: "))
        sizer.Add(hostnameTextControl)
        sizer.Add(panel.StaticText("Homeseer Username: "))
        sizer.Add(usernameTextControl)
        sizer.Add(panel.StaticText("Homeseer Password: "))    # row2, col1
        sizer.Add(passwordTextControl)

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 10)
        panel.SetSizerAndFit(border)

        while panel.Affirmed():
            panel.SetResult(
                hostnameTextControl.GetValue(),
                usernameTextControl.GetValue(),
                passwordTextControl.GetValue()
            )



class OnOffCommand(eg.ActionClass):

    def __call__(self, deviceCode):
        self.plugin.doOnOffCommand(deviceCode)


    def Configure(self, devicecode=""):
        panel = eg.ConfigPanel()

        deviceCodeTextControl = panel.TextCtrl(devicecode)

        sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=10, vgap=5)
        sizer.Add(panel.StaticText("Device Code: "))
        sizer.Add(deviceCodeTextControl)

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 10)
        panel.SetSizerAndFit(border)

        while panel.Affirmed():
            panel.SetResult(deviceCodeTextControl.GetValue())



class OffCommand(eg.ActionClass):

    def __call__(self, deviceCode):
        self.plugin.doOffCommand(deviceCode)


    def Configure(self, devicecode=""):
        panel = eg.ConfigPanel()

        deviceCodeTextControl = panel.TextCtrl(devicecode)

        sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=10, vgap=5)
        sizer.Add(panel.StaticText("Device Code: "))
        sizer.Add(deviceCodeTextControl)

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 10)
        panel.SetSizerAndFit(border)

        while panel.Affirmed():
            panel.SetResult(deviceCodeTextControl.GetValue())



class OnCommand(eg.ActionClass):

    def __call__(self, deviceCode):
        self.plugin.doOnCommand(deviceCode)


    def Configure(self, devicecode=""):
        panel = eg.ConfigPanel()

        deviceCodeTextControl = panel.TextCtrl(devicecode)

        sizer = wx.FlexGridSizer(rows=2, cols=2, hgap=10, vgap=5)
        sizer.Add(panel.StaticText("Device Code: "))
        sizer.Add(deviceCodeTextControl)

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 10)
        panel.SetSizerAndFit(border)

        while panel.Affirmed():
            panel.SetResult(deviceCodeTextControl.GetValue())



class Speak(eg.ActionClass):

    def __call__(self, speech):
        self.plugin.doSpeak(speech)


    def Configure(self, speech="Hello Homeseer World."):
        panel = eg.ConfigPanel()

        speechTextControl = panel.TextCtrl(speech)

        sizer = wx.FlexGridSizer(rows=1, cols=2, hgap=10, vgap=5)
        sizer.Add(panel.StaticText("Speech: "))
        sizer.Add(speechTextControl)

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 10)
        panel.SetSizerAndFit(border)

        while panel.Affirmed():
            panel.SetResult(speechTextControl.GetValue())

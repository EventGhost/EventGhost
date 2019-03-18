# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, Walter Kraembring
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


##############################################################################
# Revision history:
#
# 2011-05-16  Changed to allow multiload
# 2011-05-16  Added actions for presets 1-6
# 2010-12-14  Fixed to work with -translate switch
# 2009-12-19  0.4.0 compatible GUID added
# 2009-12-18  First version, thanks to JingleManSweep for PySqueezeCenter
##############################################################################

import eg

eg.RegisterPlugin(
    name="SqueezeboxServer",
    guid='{6FADD300-F4F4-4833-8763-F70B3B541698}',
    author="Walter Kraembring",
    version="0.0.4",
    kind="program",
    canMultiLoad=True,
    createMacrosOnAdd=True,
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=2115",
    description=(
        '<p>Plugin to control '
        '<a href="http://www.logitech.com/en-gb/speakers-audio/wireless-music-systems">'
        'Squeezebox Server</a></p>'
        '\n\n<p>'
        '<center><img src="mymusic_small.png" /></center>'
    ),
)

import wx
from server import Server
from player import Player
from threading import Event, Thread


class SqueezeboxServer(eg.PluginClass):
    class text:
        infoSqueezeboxServerObject = "SqueezeboxServer object created"
        infoPlugin = "SqueezeboxServer plugin stopped"
        infoStatus = "Squeezebox device is not found or not powered on"
        infoNoDevice = "Squeezebox device was not found"
        infoThread = "SqueezeboxServer monitor thread has stopped"

        SB_name = "Squeezebox device name: "
        hostname = "SqueezeboxServer IP-address or host name: "
        portNbr = "Select the port number to use (default 9090): "
        username = "User name (leave empty if not defined): "
        password = "Password (leave empty if not defined): "

    def __init__(self):
        self.bFound = False
        self.sc = None
        self.bSqueezeboxServerObjectCreated = False
        self.iDelay = 0.2
        self.bToggle = True
        self.AddAction(Play)
        self.AddAction(Stop)
        self.AddAction(PlayPause)
        self.AddAction(Mute)
        self.AddAction(UnMute)
        self.AddAction(ToggleMute)
        self.AddAction(VolumeDown)
        self.AddAction(VolumeUp)
        self.AddAction(PreviousTrack)
        self.AddAction(NextTrack)
        self.AddAction(Preset_1)
        self.AddAction(Preset_2)
        self.AddAction(Preset_3)
        self.AddAction(Preset_4)
        self.AddAction(Preset_5)
        self.AddAction(Preset_6)
        self.AddAction(PowerOn)
        self.AddAction(PowerOff)
        self.AddAction(PowerToggle)
        self.AddAction(SimButton)

    def __start__(
        self,
        SB_name,
        hostname,
        portNbr,
        username,
        password
    ):
        self.SB_name = SB_name
        self.hostname = hostname
        self.portNbr = portNbr
        self.username = username
        self.password = password
        self.sq = None
        self.wifi = 0

        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.ThreadWorker,
            args=(self.stopThreadEvent,)
        )
        thread.start()

    def __stop__(self):
        if self.stopThreadEvent:
            self.stopThreadEvent.set()
        print self.text.infoPlugin

    def __close__(self):
        print self.text.infoPlugin

    def ThreadWorker(self, stopThreadEvent):
        while not stopThreadEvent.isSet():
            stopThreadEvent.wait(self.iDelay)
            if not self.bSqueezeboxServerObjectCreated:
                self.createSqueezeboxServerObject()
            self.findSqueezeboxDevice()
        print self.text.infoThread

    def findSqueezeboxDevice(self):
        try:
            self.wifi = self.sq.get_wifi_signal_strength()
            if self.wifi > 0:
                # print self.sq.get_wifi_signal_strength() # "debugging"
                self.bFound = True
        except:
            self.bFound = False

        if self.bFound:
            self.iDelay = 2.0
            self.bToggle = True
            # print "Squeezebox device was found" # "debugging"
        else:
            self.iDelay = 10.0
            self.bSqueezeboxServerObjectCreated = False
            if self.bToggle:
                self.TriggerEvent(self.SB_name + ": " + self.text.infoNoDevice)
                self.bToggle = False

    def createSqueezeboxServerObject(self):
        try:
            self.sc = Server(
                hostname=str(self.hostname),
                port=self.portNbr,
                username=str(self.username),
                password=str(self.password)
            )
            self.sc.connect()
            print "Logged in: %s" % self.sc.logged_in
            print "Version: %s" % self.sc.get_version()
            player_lst = self.sc.get_players()

            for i in range(0, len(player_lst)):
                SBmac = str(player_lst[i])
                SBmac = SBmac.lstrip('Player: ')
                self.sq = self.sc.get_player(SBmac)

                if self.sq.get_name() == self.SB_name:
                    print self.SB_name
                    break

            self.bSqueezeboxServerObjectCreated = True
            print self.text.infoSqueezeboxServerObject
            self.bFound = True

        except:
            self.bFound = False
            self.iDelay = 10.0
            print self.SB_name + ": " + self.text.infoStatus

    def Configure(
        self,
        SB_name="enter name of Squeezebox to control",
        hostname="127.0.0.1",
        portNbr=9090,
        username="",
        password="",
        *args
    ):
        panel = eg.ConfigPanel(self, resizable=True)
        mySizer = wx.GridBagSizer(5, 5)

        SB_nameCtrl = wx.TextCtrl(panel, -1, SB_name)
        SB_nameCtrl.SetInitialSize((250, -1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.SB_name), (1, 0))
        mySizer.Add(SB_nameCtrl, (1, 1))

        hostnameCtrl = wx.TextCtrl(panel, -1, hostname)
        hostnameCtrl.SetInitialSize((250, -1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.hostname), (2, 0))
        mySizer.Add(hostnameCtrl, (2, 1))

        portCtrl = panel.SpinIntCtrl(value=portNbr, min=1, max=65535)
        portCtrl.SetInitialSize((75, -1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.portNbr), (3, 0))
        mySizer.Add(portCtrl, (3, 1))

        usernameCtrl = wx.TextCtrl(panel, -1, username)
        usernameCtrl.SetInitialSize((250, -1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.username), (4, 0))
        mySizer.Add(usernameCtrl, (4, 1))

        passwordCtrl = wx.TextCtrl(panel, -1, password)
        passwordCtrl.SetInitialSize((250, -1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.password), (5, 0))
        mySizer.Add(passwordCtrl, (5, 1))

        panel.sizer.Add(mySizer, 1, flag=wx.EXPAND)

        while panel.Affirmed():
            SB_name = SB_nameCtrl.GetValue()
            hostname = hostnameCtrl.GetValue()
            portNbr = portCtrl.GetValue()
            username = usernameCtrl.GetValue()
            password = passwordCtrl.GetValue()

            panel.SetResult(
                SB_name,
                hostname,
                portNbr,
                username,
                password,
                *args
            )


class Play(eg.ActionClass):
    name = "Play"
    description = "Starts playing"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.play()
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class Stop(eg.ActionClass):
    name = "Stop"
    description = "Stops playing"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.stop()
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class PlayPause(eg.ActionClass):
    name = "PlayPause"
    description = "Toggles play/pause"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.toggle()
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class Mute(eg.ActionClass):
    name = "Mute"
    description = "Mutes playing"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.set_muting(0)
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class UnMute(eg.ActionClass):
    name = "UnMute"
    description = "Unmutes playing"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.set_muting(1)
            self.plugin.sq.volume_up(amount=30)
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class ToggleMute(eg.ActionClass):
    name = "ToggleMute"
    description = "Toggles Mute"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            if self.plugin.sq.muting:
                self.plugin.sq.set_muting(0)
                # res = self.plugin.sq.get_mode()
                # print res
                return
            else:
                self.plugin.sq.set_muting(1)
                self.plugin.sq.volume_up(amount=30)
                # res = self.plugin.sq.get_mode()
                # print res
                return
        else:
            print self.plugin.text.infoStatus


class VolumeDown(eg.ActionClass):
    name = "VolumeDown"
    description = "Lowers volume"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.volume_down(amount=5)
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class VolumeUp(eg.ActionClass):
    name = "VolumeUp"
    description = "Raises volume"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.volume_up(amount=5)
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class PreviousTrack(eg.ActionClass):
    name = "Previous Track"
    description = "Starts playing Previous Track"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.prev()
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class NextTrack(eg.ActionClass):
    name = "Next Track"
    description = "Starts playing Next Track"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.next()
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class Preset_1(eg.ActionClass):
    name = "Preset 1"
    description = "Starts playing preset 1"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.ir_button('preset_1.single')
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class Preset_2(eg.ActionClass):
    name = "Preset 2"
    description = "Starts playing preset 2"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.ir_button('preset_2.single')
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class Preset_3(eg.ActionClass):
    name = "Preset 3"
    description = "Starts playing preset 3"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.ir_button('preset_3.single')
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class Preset_4(eg.ActionClass):
    name = "Preset 4"
    description = "Starts playing preset 4"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.ir_button('preset_4.single')
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class Preset_5(eg.ActionClass):
    name = "Preset 5"
    description = "Starts playing preset 5"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.ir_button('preset_5.single')
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class Preset_6(eg.ActionClass):
    name = "Preset 6"
    description = "Starts playing preset 6"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.ir_button('preset_6.single')
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class PowerOn(eg.ActionClass):
    name = "Power ON"
    description = "Power ON"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.set_power_state(1)
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class PowerOff(eg.ActionClass):
    name = "Power OFF"
    description = "Power OFF"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.set_power_state(0)
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus


class PowerToggle(eg.ActionClass):
    name = "Power Toggle"
    description = "Toggles power ON/OFF"

    def __call__(self):
        if self.plugin.bSqueezeboxServerObjectCreated:
            if not self.plugin.sq.get_power_state():
                self.plugin.sq.set_power_state(1)
                self.plugin.sq.play()
                # res = self.plugin.sq.get_mode()
                # print res
                return
            else:
                self.plugin.sq.set_power_state(0)
                # res = self.plugin.sq.get_mode()
                # print res
                return
        else:
            print self.plugin.text.infoStatus


class SimButton(eg.ActionClass):
    name = "Simulate button"
    description = "Simulates button presses"

    class SimButton:
        txt_Button = "Select or type the button press to simulate"

    def __call__(self, button):
        if self.plugin.bSqueezeboxServerObjectCreated:
            self.plugin.sq.ir_button(str(button))
            # res = self.plugin.sq.get_mode()
            # print res
            return
        else:
            print self.plugin.text.infoStatus

    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice

    def Configure(
        self,
        button=""
    ):
        panel = eg.ConfigPanel(self)

        # Create a combo for button selections and inputs
        buttonCtrl = wx.ComboBox(parent=panel, pos=(10, 10))
        list = [
            'preset_1.single',
            'preset_2.single',
            'preset_3.single',
            'preset_4.single',
            'preset_5.single',
            'preset_6.single'
        ]

        if button != "":
            if list.count(button) == 0:
                list.append(button)

        buttonCtrl.AppendItems(items=list)

        if list.count(button) == 0:
            buttonCtrl.Select(n=0)
        else:
            buttonCtrl.SetSelection(int(list.index(button)))

        buttonCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)

        staticBox = wx.StaticBox(panel, -1, self.SimButton.txt_Button)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(buttonCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND | wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            button = buttonCtrl.GetValue()

            panel.SetResult(
                button
            )

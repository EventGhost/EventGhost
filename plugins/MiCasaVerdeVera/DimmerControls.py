# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
# This plugin is an HTTP client and Server that sends and receives MiCasaVerde UI5 and UI7 states.
# This plugin is based on the Vera plugins by Rick Naething, well kinda sorta, 

import eg
import wx
import threading
from TextControls import *
from ConfigControls import *
from ChoiceControls import *

def FloatRange(x, y, jump):
    if str(jump)[:1] == '-':
        while x > y:
            yield x
            x += jump
    else:
        while x < y:
            yield x
            x += jump


class DimmerStatus(eg.ActionBase):

    text = Text
    
    def __call__(self, device):
        device = self.plugin.VDL.GetID(device=device)
        try: return float(Lists.VDL['devices'][device]['level'])
        except: return None

    def Configure(self, device=None):
        text = self.text.DimmerStatus
        panel = eg.ConfigPanel()
        deviceCtrl = DeviceConfigPanel(self, panel)

        deviceCtrl.AddItems(text.DimmStBox, '2', device=device)
        panel.sizer.Add(deviceCtrl, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetStringSelection())

class RampDimmer(eg.ActionBase):

    text = Text

    def __call__(self, device, start, stop, step, speed, current):

        device = self.plugin.VDL.GetID(device=device)
        if device:
            try: start = float(start)
            except: start = float(start[:-1])
            try: stop = float(stop)
            except: stop = float(stop[:-1])
            try: step = float(step)
            except: step = float(step[:-1])
            speed = float(speed)
            if current:
                start = float(self.plugin.VDL.devices[int(device)]['level'])

            self.plugin.AddLightRamping(device, RAMPING(self.plugin, device, start, stop, step, speed))

    def Configure(self, device=" ", start='0.0%', stop='0.0%', step='0.0%', speed='0.0', current=True):
        text = self.text.RampDimmer
        panel = eg.ConfigPanel()
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        deviceCtrl = DeviceConfigPanel(self, panel)

        percentchoice = []
        speedchoice = []
        stepchoice = []
        for i in FloatRange(0.00, 100.25, 0.25):
            percentchoice += [str(i)+'%']

        for i in FloatRange(0.25, 100.25, 0.25):
            stepchoice += [str(i)+'%']

        for i in FloatRange(0.10, 100.10, 0.10):
            speedchoice += [str(i)]

        startCtrl = Choice(panel, start, percentchoice)
        stopCtrl = Choice(panel, stop, percentchoice)
        stepCtrl = Choice(panel, step, stepchoice)
        speedCtrl = Choice(panel, speed, speedchoice)

        timeCtrl = panel.StaticText('          ')
        currCtrl = panel.StaticText('   ')
        useCurrCtrl = panel.CheckBox(current)
        cancelRamp = wx.Button(panel, -1, label='Cancel Ramp')

        rampBox = panel.BoxedGroup(
                                text.RampDmBox,
                                (text.StrtText, startCtrl),
                                (text.StopText, stopCtrl),
                                (text.IncrText, stepCtrl),
                                (text.SpedText, speedCtrl)
                                )
        currentBox = panel.BoxedGroup(
                                text.CurrBox,
                                ('Ramp Run Time: ', timeCtrl),
                                (text.CurrText, currCtrl),
                                (text.UseCurrText, useCurrCtrl),
                                cancelRamp
                                )

        eg.EqualizeWidths((startCtrl, stopCtrl, stepCtrl, speedCtrl))
        eg.EqualizeWidths((timeCtrl, currCtrl))

        deviceCtrl.AddItems(self.text.Vera.DeviceBox, '2', device=device)

        def onCheck(evt=None):
            dv_id = self.plugin.VDL.GetID(deviceCtrl.GetStringSelection())
            if evt:
                evt.Skip()
            if not dv_id:
                return
            ID = int(dv_id)
            level = dc(self.plugin.VDL.devices[ID]['level'])+'%'
            if useCurrCtrl.GetValue():
                startCtrl.SetSelection(percentchoice.index(level))

            startCtrl.Enable(not useCurrCtrl.GetValue())
            currCtrl.SetLabel(level)
            wx.CallAfter(onSelection)

        def onSection(evt):
            wx.CallAfter(onCheck)
            deviceCtrl.onSection(evt)

        def onRoom(evt):
            wx.CallAfter(onCheck)
            deviceCtrl.onRoom(evt)

        def onDevice(evt):
            wx.CallAfter(onCheck)
            deviceCtrl.onDevice(evt)

        def onCancelRamp(evt):
            wx.CallAfter(self.plugin.StopLightRamping)
            evt.Skip()

        def onSelection(evt=None):
            start = float(startCtrl.GetStringSelection()[:-1])
            stop = float(stopCtrl.GetStringSelection()[:-1])
            step = float(stepCtrl.GetStringSelection()[:-1])
            speed = float(speedCtrl.GetStringSelection())
            runtime = float(start-stop) if start > stop else float(stop-start)
            runtime = float(float(runtime)/float(step))
            runtime = float(float(runtime)*float(speed))
            timeCtrl.SetLabel(str(round(runtime,2)))
            if evt: evt.Skip()

        wx.CallAfter(onCheck)
        wx.CallAfter(onSelection)

        hsizer.Add(rampBox, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 5)
        hsizer.Add(currentBox, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 5)
        panel.sizer.AddMany([(deviceCtrl, 0, wx.EXPAND), (hsizer, 0, wx.EXPAND)])

        deviceCtrl.sections.Bind(wx.EVT_CHOICE, onSection)
        deviceCtrl.rooms.Bind(wx.EVT_CHOICE, onRoom)
        deviceCtrl.devices.Bind(wx.EVT_CHOICE, onDevice)
        useCurrCtrl.Bind(wx.EVT_CHECKBOX, onCheck)
        cancelRamp.Bind(wx.EVT_BUTTON, onCancelRamp)
        startCtrl.Bind(wx.EVT_CHOICE, onSelection)
        stopCtrl.Bind(wx.EVT_CHOICE, onSelection)
        stepCtrl.Bind(wx.EVT_CHOICE, onSelection)
        speedCtrl.Bind(wx.EVT_CHOICE, onSelection)

        while panel.Affirmed():
            panel.SetResult(
                            deviceCtrl.GetStringSelection(),
                            startCtrl.GetStringSelection(),
                            stopCtrl.GetStringSelection(),
                            stepCtrl.GetStringSelection(),
                            speedCtrl.GetStringSelection(),
                            useCurrCtrl.GetValue()
                            )
        
class Dimmer(eg.ActionBase):

    text = Text

    def __call__(self, device, dimmer):

        device = self.plugin.VDL.GetID(device=device)

        if device:
            try: dimmer = float(dimmer)
            except: dimmer = float(dimmer[:-1])
            self.plugin.StopLightRamping(device)
            self.plugin.SERVER.send(device=device, dimmer=dimmer)

    def Configure(self, device=" ", dimmer='0.00%'):
        text = self.text.Dimmer
        panel = eg.ConfigPanel()
        deviceCtrl = DeviceConfigPanel(self, panel)

        percentchoice = []
        for i in FloatRange(0.00, 100.25, 0.25):
            percentchoice += [str(i)+'%']

        dimmerCtrl = Choice(panel, dimmer, percentchoice)
        dimmerBox = panel.BoxedGroup(text.DimmerBox, (text.DimmerText, dimmerCtrl))

        deviceCtrl.AddItems(self.text.Vera.DeviceBox, '2', device=device)
        panel.sizer.AddMany([(deviceCtrl, 0, wx.EXPAND), (dimmerBox, 0, wx.EXPAND)])

        while panel.Affirmed():
            panel.SetResult(deviceCtrl.GetStringSelection(), dimmerCtrl.GetStringSelection())


class RAMPING(threading.Thread):

    def __init__(self, plugin, device, start, stop, step, speed):

    	self.plugin = plugin
        self.device = device
        self.EVENT = threading.Event()
        self.step = step
        self.stop = stop
        self.begin = start
        self.speed = speed

        super(RAMPING, self).__init__()

    def run(self):
        step = self.step
        stop = self.stop
        start = self.begin
        speed = self.speed
        device = self.device

        change = start-stop if start >= stop else stop-start
        change = ((change/step)*speed)

        self.plugin.SERVER.RAMPWAIT = change
        self.plugin.SERVER.RAMPEVENT.clear()

        eg.PrintNotice(
                        "Light Ramp Starting" \
                        +", Device: "+str(device) \
                        +", Start: "+str(start) \
                        +", Stop: " +str(stop) \
                        +", Step: "+str(step) \
                        +", Speed: "+str(speed)
                        )

        step = float('-'+str(step)) if start > stop else step
        stop += step

        for i in FloatRange(start, stop, step):
            self.plugin.SERVER.send(device=device, dimmer=str(i))
            if self.plugin.SERVER.RAMPEVENT.isSet():
                self.plugin.SERVER.RAMPWAIT = change
                self.plugin.SERVER.RAMPEVENT.clear()
            self.EVENT.wait(speed)
            if self.EVENT.isSet(): break   
        self.plugin.SERVER.RAMPEVENT.set()
        self.plugin.SERVER.RAMPWAIT = 0
        eg.PrintNotice("Light Ramp Stopped,  Device: "+device)

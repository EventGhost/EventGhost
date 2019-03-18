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
import time
from TextControls import *
from ConfigControls import *
from ChoiceControls import *
from copy import deepcopy as dc


class HVACStaticSizer(wx.StaticBoxSizer):

    def __init__(self, parent, lbl):
        self.parent = parent
        HVACBox = wx.StaticBox(parent, -1, lbl)
        wx.StaticBoxSizer.__init__(self, HVACBox, wx.VERTICAL)

    def AddMany(self, items):
        count = 0
        HVACsettings = wx.BoxSizer(wx.HORIZONTAL)
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        rightsizer = wx.BoxSizer(wx.VERTICAL)
        for item in items:
            if isinstance(item[0], tuple):
                for widgets in item:
                    tmpsizer = wx.BoxSizer(wx.HORIZONTAL)
                    for widget in widgets:
                        tmpsizer.Add(widget, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 5)
                    self.Add(tmpsizer)
            else:
                staticBox = wx.StaticBox(self.parent, -1, item[0])
                staticSizer = wx.StaticBoxSizer(staticBox, wx.HORIZONTAL)
                for widgets in item[1:]:
                    columnsizer = wx.BoxSizer(wx.VERTICAL)
                    for widget in widgets:
                        columnsizer.Add(widget, 0, wx.EXPAND|wx.ALIGN_LEFT|wx.ALL, 5)
                    staticSizer.Add(columnsizer, 0, wx.ALIGN_LEFT)
                if count < 2: leftsizer.Add(staticSizer, 0)
                if count > 1: rightsizer.Add(staticSizer, 0, wx.LEFT, 5)
                count += 1

        HVACsettings.Add(leftsizer, 0, wx.LEFT, 5)
        HVACsettings.Add(rightsizer, 0, wx.LEFT, 5)
        self.Add(HVACsettings)

                

class HVACStaticText:

    def __init__(self):
        pass

    def __call__(self, panel, *args):
        res = []
        for i, text in enumerate(args):
            res += [panel.StaticText(text)]
        return res

class WeatherPanel(wx.Panel):

    def __init__(self, plugin, parent):
        self.parent = parent
        self.plugin = plugin.plugin
        wx.Panel.__init__(self, parent)

    def Update(self, evt):
        self.weatherdata = self.WorldWeather(self.weatherdevices)
        evt.Skip()

    def AddItems(self, WorldWeather, weatherdevices):
        self.weatherdevices = weatherdevices
        self.WorldWeather = WorldWeather

        self.weatherdata = self.WorldWeather(self.weatherdevices)

        weatherbox = wx.StaticBox(self, -1, 'Weather')
        weathersizer = wx.StaticBoxSizer(weatherbox, wx.HORIZONTAL)
        scroll1sizer = wx.BoxSizer(wx.VERTICAL)
        scroll2sizer = wx.BoxSizer(wx.VERTICAL)
        self.scroll1 = []
        self.scroll2 = []

        self.scrollstart = -6
        self.scrollend = 0

        for i in range(6):
            self.scroll1 += [wx.StaticText(self, label=' '*30)]
            self.scroll2 += [wx.StaticText(self, label=' '*75)]
            scroll1sizer.Add(self.scroll1[i], 0, wx.EXPAND|wx.LEFT, 10)
            scroll2sizer.Add(self.scroll2[i], 0, wx.EXPAND)

        def Scroll(evt):
            self.scrollstart += 1
            self.scrollend += 1

            if self.scrollend == len(self.weatherdata)+6:
                self.scrollstart = -6
                self.scrollend = 0
            if self.scrollstart < 0:
                for i in range(int(str(self.scrollstart)[1:])):
                    self.scroll1[i].SetLabel('')
                    self.scroll2[i].SetLabel('')
                for i in range(self.scrollend):
                    j = 6-(self.scrollend-i)
                    self.scroll1[j].SetLabel(self.weatherdata[i][0])
                    self.scroll2[j].SetLabel(self.weatherdata[i][1])
            if self.scrollend < len(self.weatherdata) and self.scrollstart >= 0:
                for i in range(self.scrollstart, self.scrollend):
                    j = 6-(self.scrollend-i)
                    self.scroll1[j].SetLabel(self.weatherdata[i][0])
                    self.scroll2[j].SetLabel(self.weatherdata[i][1])
            if self.scrollend > len(self.weatherdata)-1:
                for i in range(self.scrollstart, len(self.weatherdata)):
                    j = (len(self.weatherdata)-1)-i
                    self.scroll1[j].SetLabel(self.weatherdata[i][0])
                    self.scroll2[j].SetLabel(self.weatherdata[i][1])
                for i in range(len(self.weatherdata), self.scrollend):
                    j = 6-(self.scrollend-i)
                    self.scroll1[j].SetLabel('')
                    self.scroll2[j].SetLabel('')
            evt.Skip()

        self.SetSizer(weathersizer)
        weathersizer.Add(scroll1sizer, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 10)
        weathersizer.Add(scroll2sizer, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, 10)
        
        self.refreshtimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, Scroll, self.refreshtimer)
        wx.CallAfter(self.refreshtimer.Start, 425)

class HVAC(eg.ActionBase):

    text = Text
    HVACSaved = None

    def __call__(
                self,
                device,
                hvacOppMode="HeatOn",
                hvacFanMode="Auto",
                hvacSetTempH="70\xb0",
                hvacSetTempC="70\xb0",
                hvacRealTime=False
                ):

        try: hvacSetTempH = int(hvacSetTempH)
        except: hvacSetTempH = hvacSetTempH[:-1]
        try: hvacSetTempC = int(hvacSetTempC)
        except: hvacSetTempC = hvacSetTempC[:-1]

        device = dc(self.plugin.VDL.GetID(device=dc(device)))

        if device:
            selected = self.UpdateHVAC(device, [hvacOppMode, hvacFanMode, hvacSetTempH, hvacSetTempC])
            for key in selected.keys():
                command = {'device': device, key: dc(selected[key])}
                self.plugin.SERVER.send(**command)
                time.sleep(.1)

    def GetHVACStates(self, device):
        try: device = int(device)
        except: return ('', '', ''), ('', '', 0, 0), False

        item = dc(self.plugin.VDL.devices[device])
        fanmode     = item['fanmode']
        fanstate    = item['fan']
        oppmode     = item['mode']
        oppstate    = item['hvacstate']
        temperature = item['temperature']+'\xb0'
        hsetpoint   = item['heat']+'\xb0'
        csetpoint   = item['cool']+'\xb0'
        return (oppstate, fanstate, temperature), (oppmode, fanmode, hsetpoint, csetpoint), True
        

    def UpdateHVAC(self, device, selected):
        keys = ['hvacOppMode', 'hvacFanMode', 'hvacSetTempH', 'hvacSetTempC']
        current = list(self.GetHVACStates(device)[1])
        res = {}
        for i, key in enumerate(keys):
            if selected[i] != current[i]:
                res[key] = selected[i]
        return res

    def CheckHVAC(self, device):
        try: device = int(device)
        except: return False
        new = dc(self.plugin.VDL.devices[device])
        res = False
        if res != self.HVACSaved: res = True
        self.HVACSaved = new
        return res

    def WorldWeather(self, device=None):
        items = dc(self.plugin.VDL.devices)
        if device is None:
            for item in items:
                if not item: continue
                if item['name'] == "World Weather":
                    device = [int(item['id'])]
                    break
            if device is None: return None
            for item in items:
                if not item: continue
                if item['parent'] == str(device[0]):
                    device += [int(item['id'])]
            return device

        res = dict(current={}, tempatures={}, humidity={})
        events = dc(STATIC.ALLOWEDEVENTS['25'])
        events['providername'] = ['Weather Provider']
        events['providerurl'] = ['Provider URL']
        weatherdisplay = [
                        'providername',
                        'providerurl',
                        'temperature',
                        'temperature',
                        'temperature',
                        'humidity',
                        'feels',
                        'dew',
                        'pressure',
                        'condition',
                        'windcondition',
                        'winddirection',
                        'windchill',
                        'windgust',
                        'windspeed',
                        'solar',
                        'uv'
                        ]

        for ID in device:
            item = dc(items[ID])
            name = item.pop('name')
            name = 'Current Temperature' if name == 'Temperature' else name
            item.pop('room')
            for key in item.keys():
                try: keyname = events[key][0]+':' if events[key][0] != 'Temperature' else name+': '
                except: continue

                try: weatherdisplay[weatherdisplay.index(key)] = [keyname, item[key]]
                except: continue
        return dc(weatherdisplay)

    def Configure(
                self,
                device=" ",
                hvacOppMode="HeatOn",
                hvacFanMode="Auto",
                hvacSetTempH="70\xb0",
                hvacSetTempC="70\xb0",
                hvacRealTime=False
                ):

        VDL = self.plugin.VDL

        self.update = True
        text = self.text.HVAC
        panel = eg.ConfigPanel()

        settempchoice = text.SetTmpChoiceF
        if VDL.GetThermalUnit() == 'C':
            settempchoice = text.SetTmpChoiceC

        deviceCtrl = DeviceConfigPanel(self, panel)
        GetName = deviceCtrl.GetStringSelection

        deviceCtrl.AddItems(self.text.Vera.DeviceBox, '5', device=device)
        states = self.GetHVACStates(GetName())

        oppstate, fanstate, temperature = states[0]
        oppmode, fanmode, hsetpoint, csetpoint = states[1]
        found = states[2]

        if hvacRealTime:
            hvacOppMode, hvacFanMode = [oppmode, fanmode]
            hvacSetTempH, hvacSetTempC = [hsetpoint, csetpoint]

        HVACsizer = HVACStaticSizer(panel, text.HVACText)
       
        tempWidgets = HVACStaticText()(panel, text.RealTimeText, text.CurrTempText, temperature)
        realtimetext, temptext, temp = tempWidgets
        realtime = panel.CheckBox(hvacRealTime)

        oppWidgets = HVACStaticText()(panel, text.CurrOppMText, oppmode, text.CurrOppSText, oppstate, text.OppModText)
        oppmodetext, oppmode, oppstatetext, oppstate, oppchoicetext = oppWidgets
        oppchoice = Choice(panel, hvacOppMode, text.OppChoice)

        fanWidgets = HVACStaticText()(panel, text.CurrFanMText, fanmode, text.CurrFanSText, fanstate, text.FanModText)
        fanmodetext, fanmode, fanstatetext, fanstate, fanchoicetext = fanWidgets
        fanchoice = Choice(panel, hvacFanMode, text.FanChoice)

        heatWidgets = HVACStaticText()(panel, text.CurrHeatText, str(hsetpoint), text.HStTmpText)
        heattext, hsetpoint, heatchoicetext = heatWidgets
        heatchoice = Choice(panel, hvacSetTempH, settempchoice)

        coolWidgets = HVACStaticText()(panel, text.CurrCoolText, str(csetpoint), text.CStTmpText)
        cooltext, csetpoint, coolchoicetext = coolWidgets
        coolchoice = Choice(panel, hvacSetTempC, settempchoice)

        def GetSelection():
            return [
                    dc(oppchoice.GetStringSelection()),
                    dc(fanchoice.GetStringSelection()),
                    dc(heatchoice.GetStringSelection()),
                    dc(coolchoice.GetStringSelection()),
                    dc(realtime.GetValue())
                    ]

        def UpdateHVACDisplay(evt=None):
            change = True
            devc = VDL.GetID(device=GetName())
            if evt: change = self.CheckHVAC(devc)
            if change:
                tmpstates = self.GetHVACStates(devc)
                ops, fas, tmp  = tmpstates[0]
                opm, fam, hset, cset = tmpstates[1]
                found = states[2]

                temp.SetLabel(tmp)
                oppmode.SetLabel(opm)
                oppstate.SetLabel(ops)
                fanmode.SetLabel(fam)
                fanstate.SetLabel(fas)
                hsetpoint.SetLabel(hset)
                csetpoint.SetLabel(cset)
                if not self.update and realtime.GetValue():
                    oppchoice.SetSelection(text.OppChoice.index(opm))
                    fanchoice.SetSelection(text.FanChoice.index(fam))
                    coolchoice.SetSelection(settempchoice.index(cset))
                    heatchoice.SetSelection(settempchoice.index(hset))
                onOppChoice()
            if evt: evt.Skip()

        def onRealTime(evt):
            try: self.changetimer.Stop()
            except: pass
            wx.CallAfter(self.changetimer.Start, 1000)
            evt.Skip()

        def onOppChoice(evt=None):
            flag = bool(oppchoice.GetSelection())
            if evt:
                if flag:
                    self.savedHVAC = GetSelection()
                    self.savedHVAC.pop(0)
                    self.savedHVAC.pop()
                if not flag:
                    if self.prevopp == 'Off':
                        self.update = True
                        fam, hset, cset = self.savedHVAC
                        fanchoice.SetSelection(text.FanChoice.index(fam))
                        coolchoice.SetSelection(settempchoice.index(cset))
                        heatchoice.SetSelection(settempchoice.index(hset))
                self.prevopp = oppchoice.GetStringSelection()
                onRealTime(evt)
            coolchoice.Enable(flag)
            heatchoice.Enable(flag)

        def onFanChoice(evt):
            panel.SetIsDirty(True)
            wx.CallAfter(onRealTime, evt)

        def onCoolChoice(evt):
            wx.CallAfter(onRealTime, evt)

        def onHeatChoice(evt):
            wx.CallAfter(onRealTime, evt)

        def onClose(evt):
            self.refreshtimer.Stop()
            try: self.changetimer.Stop()
            except: pass
            try: self.weathertimer.Stop()
            except: pass
            try: self.weathersizer.refreshtimer.Stop()
            except: pass
            panel.dialog.DispatchEvent(evt, wx.ID_CANCEL)

        def onOK(evt):
            self.refreshtimer.Stop()
            try: self.changetimer.Stop()
            except: pass
            try: self.weathertimer.Stop()
            except: pass
            try: self.weathersizer.refreshtimer.Stop()
            except: pass
            panel.dialog.buttonRow.OnOK(evt)

        def onSettingChange(evt):
            self.changetimer.Stop()
            if realtime.GetValue():
                self.update = True
                event = wx.PyCommandEvent(wx.EVT_BUTTON.typeId, panel.dialog.buttonRow.testButton.GetId())
                wx.PostEvent(panel.dialog.buttonRow.testButton, event)
            evt.Skip()

        onOppChoice()

        eg.EqualizeWidths((
                        realtimetext,
                        temptext
                        ))

        eg.EqualizeWidths((
                        oppmodetext,
                        oppstatetext,
                        oppchoicetext,
                        fanmodetext,
                        fanstatetext,
                        fanchoicetext,
                        cooltext,
                        coolchoicetext,
                        heattext,
                        heatchoicetext
                        ))

        eg.EqualizeWidths((
                        oppmode,
                        oppstate,
                        oppchoice,
                        fanmode,
                        fanstate,
                        fanchoice,
                        csetpoint,
                        coolchoice,
                        hsetpoint,
                        heatchoice
                        ))

        HVACsizer.AddMany([
                        ((realtimetext, realtime), (temptext, temp)),
                        (text.OppModBox, (oppmodetext, oppstatetext, oppchoicetext), (oppmode, oppstate, oppchoice)),
                        (text.HStTmpBox, (heattext, heatchoicetext), (hsetpoint, heatchoice)),
                        (text.FanModBox, (fanmodetext, fanstatetext, fanchoicetext), (fanmode, fanstate, fanchoice)),
                        (text.CStTmpBox, (cooltext, coolchoicetext), (csetpoint, coolchoice))
                        ])

        panel.sizer.Add(deviceCtrl, 0, wx.EXPAND)

        weather = self.WorldWeather()
        if weather:
            self.weathersizer = WeatherPanel(self, panel)
            self.weathersizer.AddItems(self.WorldWeather, weather)
            panel.sizer.Add(self.weathersizer, 0, wx.EXPAND)
            self.weathertimer = wx.Timer(panel)
            panel.Bind(wx.EVT_TIMER, self.weathersizer.Update, self.weathertimer)
            wx.CallAfter(self.weathertimer.Start, 5000)

        panel.sizer.Add(HVACsizer, 0, wx.EXPAND)

        self.savedHVAC = GetSelection()
        self.prevopp = self.savedHVAC.pop(0)
        self.savedHVAC.pop()

        self.refreshtimer = wx.Timer(panel)
        self.changetimer = wx.Timer(panel)

        oppchoice.Bind(wx.EVT_CHOICE, onOppChoice)
        fanchoice.Bind(wx.EVT_CHOICE, onFanChoice)
        coolchoice.Bind(wx.lib.masked.EVT_NUM, onCoolChoice)
        heatchoice.Bind(wx.lib.masked.EVT_NUM, onHeatChoice)
        panel.Bind(wx.EVT_TIMER, UpdateHVACDisplay, self.refreshtimer)
        panel.Bind(wx.EVT_TIMER, onSettingChange, self.changetimer)
        panel.dialog.Bind(wx.EVT_CLOSE, onClose)
        panel.dialog.buttonRow.cancelButton.Bind(wx.EVT_BUTTON, onClose)
        panel.dialog.buttonRow.okButton.Bind(wx.EVT_BUTTON, onOK)
        wx.CallAfter(self.refreshtimer.Start, 100)

        if found: wx.CallAfter(UpdateHVACDisplay)

        while panel.Affirmed():
            panel.SetResult(GetName(), *GetSelection())
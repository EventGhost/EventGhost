# -*- coding: utf-8 -*-

# 0.0.2 (2019-03-03) by topix
#   - moved duplicate configure code of BreatheEffect and PulseEffect into SelectorLifxAction
#   - enhanced configure dialogs using SpinIntCtrl's to avoid exceptions on first configure
#     when the value for the control is None.
#   - little code cleanup
#   - added GUID for plugin

import eg

eg.RegisterPlugin(
    name="LIFX",
    guid='{659D1B07-DC46-447A-B464-BBE573F44EEF}',
    author="Marcus Hultman",
    version="0.0.2",
    kind="external",
    description="This plugin connects to your LIFX lights."
)


import re
import wx
import requests


class LIFXPlugin(eg.PluginBase):
    def __init__(self):
        self.AddAction(ListLights)
        self.AddAction(SetState)
        self.AddAction(TogglePower)
        self.AddAction(BreatheEffect)
        self.AddAction(PulseEffect)

    def __start__(self, token):
        self.auth = {'Authorization': 'Bearer {0}'.format(token)}
        self.base_url = 'https://api.lifx.com/v1/'

    def Configure(self, token=""):
        panel = eg.ConfigPanel(self)
        tokenCtrl = panel.TextCtrl(token)
        panel.AddLine("Token: ", tokenCtrl)
        while panel.Affirmed():
            panel.SetResult(tokenCtrl.GetValue())


# Abstract Actions
class LifxAction(eg.ActionBase):
    GET = 0
    PUT = 1
    POST = 2

    def action(self, url, *args, **kwargs):
        return {
            0: requests.get,
            1: requests.put,
            2: requests.post,
        }[self.method if hasattr(self, 'method') else
        LifxAction.GET](url, *args, **kwargs).json()

    def form_url(self):
        if not hasattr(self, 'url'):
            self.url = ''
        return self.plugin.base_url + self.url

    def __call__(self, *data):
        url = self.form_url()
        payload = dict(filter(lambda x: x[1] is not None, zip(
            self.payload if hasattr(self, 'payload') else (), data)))
        return self.action(url, headers=self.plugin.auth, data=payload)


class SelectorLifxAction(LifxAction):
    def form_url(self):
        return self.plugin.base_url + self.url.format(self.selector)

    def __call__(self, selector, *data):
        self.selector = selector
        return super(SelectorLifxAction, self).__call__(*data)

    def Configure(self, selector=None, color=None, from_color=None, period=None, cycles=None, persist=None,
                  power_on=None, peak=None):
        panel = eg.ConfigPanel(self)
        selectorCtrl = SelectorCtrl(panel, selector)
        colorCtrl = ColorPickerCtrl(panel, color)
        from_colorECtrl = panel.CheckBox(from_color is not None)
        from_colorCtrl = ColorPickerCtrl(panel, from_color)
        periodECtrl = panel.CheckBox(period is not None)
        periodCtrl = panel.SpinNumCtrl(
            period if period is not None else 0
        )
        cyclesECtrl = panel.CheckBox(cycles is not None)
        cyclesCtrl = panel.SpinIntCtrl(
            cycles if cycles is not None else 0
        )
        persistECtrl = panel.CheckBox(persist is not None)
        persistCtrl = panel.CheckBox(persist)
        power_onECtrl = panel.CheckBox(power_on is not None)
        power_onCtrl = panel.CheckBox(power_on)
        peakECtrl = panel.CheckBox(peak is not None)
        peakCtrl = panel.TextCtrl(peak or '')
        panel.AddLine('Selector: ', selectorCtrl)
        panel.AddLine('Color: ', colorCtrl)
        panel.AddLine(from_colorECtrl, 'From color:', from_colorCtrl)
        panel.AddLine(periodECtrl, 'Period: ', periodCtrl)
        panel.AddLine(cyclesECtrl, 'Cycles:', cyclesCtrl)
        panel.AddLine(persistECtrl, 'Persist:', persistCtrl)
        panel.AddLine(power_onECtrl, 'Power on:', power_onCtrl)
        panel.AddLine(peakECtrl, 'Peak:', peakCtrl)
        while panel.Affirmed():
            panel.SetResult(
                selectorCtrl.GetValue(),
                colorCtrl.GetValue(),
                from_colorCtrl.GetValue() if from_colorECtrl.GetValue() else None,
                periodCtrl.GetValue() if periodECtrl.GetValue() else None,
                cyclesCtrl.GetValue() if cyclesECtrl.GetValue() else None,
                persistCtrl.GetValue() if persistECtrl.GetValue() else None,
                power_onCtrl.GetValue() if power_onECtrl.GetValue() else None,
                peakCtrl.GetValue() if peakECtrl.GetValue() else None,
            )


# Extra controls
class SelectorCtrl(wx.BoxSizer):
    choices = ["all", "label:", "id:", "group_id:", "group:", "location_id:", "location:", "scene_id:"]

    def __init__(self, panel, selector, *args, **kwargs):
        super(SelectorCtrl, self).__init__(*args, **kwargs)
        i, e = 0, ''
        if selector is not None:
            t, e = re.match('(\w*:?)(\w*)', selector).groups()
            i = SelectorCtrl.choices.index(t)
        self.typeCtrl = panel.Choice(i, SelectorCtrl.choices)
        self.argCtrl = panel.TextCtrl(e)
        self.Add(self.typeCtrl)
        self.Add(self.argCtrl, flag=wx.LEFT, border=10)

    def GetValue(self):
        type = SelectorCtrl.choices[self.typeCtrl.GetValue()]
        return type + self.argCtrl.GetValue() if type[-1] == ':' else type


class ColorPickerCtrl(wx.ColourPickerCtrl):
    def __init__(self, panel, color, *args, **kwargs):
        super(ColorPickerCtrl, self).__init__(panel, *args, **kwargs)
        self.SetColour(color)

    def GetValue(self):
        return self.GetColour().GetAsString(wx.C2S_NAME | wx.C2S_CSS_SYNTAX)


# Implementations
class ListLights(SelectorLifxAction):
    name = "List Lights"
    description = "."

    def __init__(self):
        self.url = 'lights/{0}'

    def Configure(self, selector=None):
        panel = eg.ConfigPanel(self)
        selectorCtrl = SelectorCtrl(panel, selector)
        panel.AddLine('Selector: ', selectorCtrl)
        while panel.Affirmed():
            panel.SetResult(selectorCtrl.GetValue())


class SetState(SelectorLifxAction):
    name = "Set State"
    description = "."
    pwrCh = ['on', 'off']

    def __init__(self):
        self.method = LifxAction.PUT
        self.url = 'lights/{0}/state'
        self.payload = ('power', 'color', 'brightness', 'duration')

    def Configure(self, selector=None, power=None, color=None, brightness=None, duration=None):
        panel = eg.ConfigPanel(self)
        selectorCtrl = SelectorCtrl(panel, selector)
        powerECtrl = panel.CheckBox(power is not None)
        powerCtrl = panel.Choice(SetState.pwrCh.index(power) if power is not None else 0,
                                 SetState.pwrCh)
        colorECtrl = panel.CheckBox(color is not None)
        colorCtrl = ColorPickerCtrl(panel, color)
        brightnessECtrl = panel.CheckBox(brightness is not None)
        brightnessCtrl = panel.SpinNumCtrl(
            brightness if brightness is not None else 0,
            min=0, max=1.0, increment=0.01
        )
        durationECtrl = panel.CheckBox(duration is not None)
        durationCtrl = panel.SpinNumCtrl(
            duration if duration is not None else 0
        )
        panel.AddLine('Selector: ', selectorCtrl)
        panel.AddLine(powerECtrl, 'Power: ', powerCtrl)
        panel.AddLine(colorECtrl, 'Color: ', colorCtrl)
        panel.AddLine(brightnessECtrl, 'Brightness: ', brightnessCtrl)
        panel.AddLine(durationECtrl, 'Duration: ', durationCtrl)
        while panel.Affirmed():
            panel.SetResult(
                selectorCtrl.GetValue(),
                SetState.pwrCh[powerCtrl.GetValue()] if powerECtrl.GetValue() else None,
                colorCtrl.GetValue() if colorECtrl.GetValue() else None,
                brightnessCtrl.GetValue() if brightnessECtrl.GetValue() else None,
                durationCtrl.GetValue() if durationECtrl.GetValue() else None
            )


class TogglePower(SelectorLifxAction):
    name = "Toggle Power"
    description = "."

    def __init__(self):
        self.method = LifxAction.POST
        self.url = 'lights/{0}/toggle'
        self.payload = ('duration',)

    def Configure(self, selector=None, duration=None):
        panel = eg.ConfigPanel(self)
        selectorCtrl = SelectorCtrl(panel, selector)
        durationECtrl = panel.CheckBox(duration is not None)
        durationCtrl = panel.SpinNumCtrl(
            duration if duration is not None else 0
        )
        panel.AddLine('Selector: ', selectorCtrl)
        panel.AddLine(durationECtrl, 'Duration: ', durationCtrl)
        while panel.Affirmed():
            panel.SetResult(
                selectorCtrl.GetValue(),
                durationCtrl.GetValue() if durationECtrl.GetValue() else None
            )


class BreatheEffect(SelectorLifxAction):
    name = "Breathe Effect"
    description = "."

    def __init__(self):
        self.method = LifxAction.POST
        self.url = 'lights/{0}/effects/breathe'
        self.payload = ('color', 'from_color', 'period', 'cycles', 'persist', 'power_on', 'peak')


class PulseEffect(SelectorLifxAction):
    name = "Pulse Effect"
    description = "."

    def __init__(self):
        self.method = LifxAction.POST
        self.url = 'lights/{0}/effects/pulse'
        self.payload = ('color', 'from_color', 'period', 'cycles', 'persist', 'power_on', 'peak')

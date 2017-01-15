# -*- coding: utf-8 -*-
#
# Plugins/Speech/__init__.py
#
# Copyright (C) 2006 MonsterMagnet
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 2.6 by K         2017-01-11 13:23 UTC-7
#     - bugfix - text class not being utilized properly
#     - bugfix - win32com com_error
# 2.5 by blackwind 2016-05-19 18:40 UTC-7
#     - bugfix - instantiate Text class in declarations
# 2.4 by Pako 2016-03-05 09:44 UTC+1
#     - bugfix - command "text = Text" is missing (line 231)
# 2.3 by Pako 2016-01-17 07:18 UTC+1
#     - bugfix
# 2.2 by Pako 2015-04-20 17:18 UTC+1
#     - added option for selection of date and time format
# 2.1 by Pako 2015-03-09 19:06 UTC+1
#     - added option for selection of output device
# 2.0 by Pako 2015-03-09 18:14 UTC+1
#     - added event after speaking finished
#     - {DATE} context is working properly
# 1.0 by MonsterMagnet
#     - initial version

import eg

eg.RegisterPlugin(
    name="Speech",
    author="MonsterMagnet",
    guid="{76A1638D-1D7D-4582-A726-A17B1A6FC723}",
    version="2.6",
    description=(
        "Uses the Text-To-Speech service of the Microsoft Speech API (SAPI)."
    ),
    url="http://www.eventghost.org/forum/viewtopic.php?f=9&t=6828",
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAA7DAAAOwwHH"
        "b6hkAAADh0lEQVR4nIXSW0yTBxgG4P/GxRkZ2+gWtR2YCBoOlsL/87fQg4WldkLHqQZo"
        "RcbBUBDCYFxsukaJqyLdAgw3p1AcOhHXNhzaIWLXtVSoWNx0LMsssspGUMYWMB3URVre"
        "XSxpRnaxL/nu3u+5ePMRxP+Mt2MDZ9EqsT0YSsfceBXmxkrhMXFXvR0bOP8JT0zckV3t"
        "6S9pP9fdpL8ybNJ/aR+93x8H/3IPfDN1WPlJhUVnFvx3y3FDw5rPktB56wDL1w6YrLdx"
        "wzWFaxNuWIc/x/y4GoE/NPC5D2PlXjEWbW/A55DDdjxsUZCS/Nk6oNtyZ61x7Fe0P/Bi"
        "6CngnL2FeXs5ArPvwzdZhqWRDPgccgRM6WgrY3roJK5uHWAcm5pvdK+hdRboWgC6Zpcx"
        "Y5EiMFUPTFYDrkN4ZpKiXbX10SsRlDkjjT5OEARB9LzHUDnO8Zt6de/MHbV58O5dH05O"
        "A1oPoB7/DceOFcH7TQa8w/tBJSZ4GBFJ118X0lqapsMJff3GhokOGeZGTmHaVIkOjQQH"
        "TD+j8tYyau4BFc4/MXhJiZUBCQ7lcv+KiBZOCvl8BYdDsQQCcjNhOvLyQ/eZFPx4Vojv"
        "Wnm4dnQ79taewpum3yG/CWSNAGr9ZSjrNYhPzvMKxfvMu0kpWygkNxEEQRDu1q1LGMwE"
        "LPv/2cFM0NkF4Hfex96vVnFkYAEntHa/PLNiYUfsnpuxvILT8XQuK1jc9x+81IfuPYBB"
        "Ahgk8F3kIz69GLUtvbjc6UJBzlUIBE2+SPY+ZyyZ17IroTA2OkEZEgQuqJ4TP26Ng/88"
        "Cf95EjMfRkOWrULnp3q0tdmQmnoG2Tk6lJWffSySVh2MTJS/xk45+HwQiFJHcTTtioDl"
        "JAn7iV0o0eUgtyEPo85R9Pa5UF19BYWFnWhutq4dKG60JQoKKVJQtDkIKA0ZS3Xf1mH8"
        "l4d4ugrUjLyNktslyGlQwNjnwEfNZpSXd0Grve7niUsdtPgtFZtf+GIQoMwUSl2lOGyv"
        "wrTvCZQ2JaRWKajKNNSqm9DysRk1de1PRJKKSWZUmoESFuWSKfkvBAGGjgF2PxuSIQnS"
        "umQQfSEKJJ8WPQvdkfBoy27uD6HhlCmUlaTfHiO9wOblqzjc/HBSrNi47oVDtpGGkG2k"
        "MYRJGkNZ1MCWmGQji+J98mpckiQskophhPMimDtTmTtjZWFxXMWmf9/+DRM268fQlSoX"
        "AAAAAElFTkSuQmCC"
    ),
)

import threading
from time import strftime

import pythoncom
import win32com.client
import wx


class Text:
    suffix = "SpeakingFinished"
    ttsError = 'Speech: Unable to start the TTS engine'

    class TextToSpeech:
        name = "Text to speech"
        description = "Uses the Microsoft Speech API (SAPI) to speak a text."
        label = "Speak: %s"
        buttonInsertTime = "Insert time HH:MM:SS"
        buttonInsertTime1 = "Insert time HH:MM"
        buttonInsertDate = "Insert date (20XX)"
        buttonInsertDate1 = "Insert date (XX)"
        normal = "Normal"
        slow = "Slow"
        fast = "Fast"
        silent = "Silent"
        loud = "Loud"
        labelVoice = "Voice:"
        labelRate = "Rate:"
        labelVolume = "Volume:"
        voiceProperties = "Voice properties"
        textBoxLabel = "Text"
        addSuffix = "Additional event suffix:"
        device = "Output device:"


class CustomSlider(wx.Window):
    def __init__(
        self,
        parent,
        wxId=wx.ID_ANY,
        value=None,
        minValue=None,
        maxValue=None,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=0,
        valueLabel=None,
        minLabel=None,
        maxLabel=None,
    ):
        self.valueLabel = valueLabel
        wx.Window.__init__(self, parent, wxId, pos, size, style)
        sizer = wx.GridBagSizer()
        self.slider = wx.Slider(
            self,
            wx.ID_ANY,
            value,
            minValue,
            maxValue,
            style=style
        )
        sizer.Add(self.slider, (0, 0), (1, 3), wx.EXPAND)
        st = wx.StaticText(self, wx.ID_ANY, minLabel)
        sizer.Add(st, (1, 0), (1, 1), wx.ALIGN_LEFT)
        self.valueLabelCtrl = wx.StaticText(self, wx.ID_ANY, valueLabel)
        sizer.Add(
            self.valueLabelCtrl,
            (1, 1),
            (1, 1),
            wx.ALIGN_CENTER_HORIZONTAL
        )
        st = wx.StaticText(self, wx.ID_ANY, maxLabel)
        sizer.Add(st, (1, 2), (1, 1), wx.ALIGN_RIGHT)
        sizer.AddGrowableCol(1, 1)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.Layout()
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_SCROLL, self.OnScrollChanged)
        self.Bind(wx.EVT_SET_FOCUS, self.OnSetFocus)
        self.OnScrollChanged()

    def OnSize(self, event):
        if self.GetAutoLayout():
            self.Layout()

    def OnSetFocus(self, event):
        self.slider.SetFocus()

    def OnScrollChanged(self, event=None):
        d = {"1": self.slider.GetValue()}
        self.valueLabelCtrl.SetLabel(self.valueLabel % d)
        if event:
            wx.PostEvent(self, eg.ValueChangedEvent(self.GetId()))

    def GetValue(self):
        return self.slider.GetValue()

    def SetValue(self):
        self.slider.SetValue()


class Speaker(threading.Thread):
    def __init__(
        self,
        plugin,
        tts_id,
        voiceText,
        suffix
    ):
        threading.Thread.__init__(self, name='Text To Speech Thread')
        self.plugin = plugin
        self.tts_id = tts_id
        self.voiceText = voiceText
        self.suffix = suffix

    def run(self):
        pythoncom.CoInitialize()
        tts = win32com.client.Dispatch(
            pythoncom.CoGetInterfaceAndReleaseStream(
                self.tts_id,
                pythoncom.IID_IDispatch
            )
        )

        tts.Speak(self.voiceText, 0)
        self.plugin.TriggerEvent(self.suffix)


class Speech(eg.PluginClass):
    text = Text

    def __init__(self):
        self.threads = []
        self.AddAction(TextToSpeech)

    def GetTTS(self):
        try:
            tts = win32com.client.Dispatch("Sapi.SpVoice")
        except pythoncom.com_error:
            eg.PrintTraceback(self.text.ttsError)
            tts = None
        return tts

    def GetVoices(self):
        tts = self.GetTTS()
        if tts:
            return list(
                voice.GetDescription()
                for voice in tts.GetVoices()
            )
        return []

    def GetAudioOutputs(self):
        tts = self.GetTTS()
        if tts:
            return list(
                audioDev.GetDescription()
                for audioDev in tts.GetAudioOutputs()
            )
        return []

    @staticmethod
    def GetVoice(tts, voice):
        voice = voice.split(' - ')[0]
        return tts.GetVoices('Name=' + voice)[0]

    @staticmethod
    def GetAudio(tts, audio):
        return list(
            audioDev for audioDev in tts.GetAudioOutputs()
            if audioDev.GetDescription() == audio
        )[0]

    def AddThread(self, voice, rate, voiceText, suffix, volume, audio):
        pythoncom.CoInitialize()

        if suffix:
            suffix = self.text.suffix + '.' + suffix
        else:
            suffix = self.text.suffix

        tts = self.GetTTS()
        if not tts:
            return
        tts.Voice = self.GetVoice(tts, voice)
        if audio:
            tts.AudioOutput = self.GetAudio(tts, audio)
        tts.Volume = volume
        tts.Rate = rate
        tts_id = pythoncom.CoMarshalInterThreadInterfaceInStream(
            pythoncom.IID_IDispatch,
            tts
        )

        t = Speaker(self, tts_id, voiceText, suffix)
        t.start()
        self.threads.append(t)


class TextToSpeech(eg.ActionClass):
    def __call__(self, voice, rate, voiceText, suffix, volume, audio=None):

        def filterFunc(s):
            formatString = '</context><context ID = "%s">%s</context><context>'
            if s == "DATE":
                return formatString % ('date_mdy', strftime("%m/%d/%Y"))
            elif s == "DATE1":
                return formatString % ('date_mdy', strftime("%m/%d/%y"))
            elif s == "TIME":
                return formatString % ('time', strftime("%H:%M:%S"))
            elif s == "TIME1":
                return formatString % ('time', strftime("%H:%M"))
            else:
                return None

        voiceText = eg.ParseString(voiceText, filterFunc)
        voiceText = "<context>%s</context>" % voiceText
        if voiceText.startswith('<context></context>'):
            voiceText = voiceText[19:]
        voiceText = voiceText.replace(
            '</context><context></context>',
            '</context>'
        )

        self.plugin.AddThread(voice, rate, voiceText, suffix, volume, audio)

    def GetLabel(self, *args):
        # args = voiceName, rate, voiceText, suff, volume, device
        return self.text.label % args[2]

    def Configure(
        self,
        voiceName=None,
        rate=0,
        voiceText="",
        suffix="",
        volume=100,
        device=None
    ):
        text = self.text
        panel = eg.ConfigPanel()

        textCtrl = wx.TextCtrl(panel, wx.ID_ANY, voiceText)
        suffCtrl = wx.TextCtrl(panel, wx.ID_ANY, suffix)

        def MakeButton(txt, value):
            def OnButton(event):
                textCtrl.WriteText(value)
                textCtrl.SetFocus()
            btn = wx.Button(panel, wx.ID_ANY, txt)
            btn.Bind(wx.EVT_BUTTON, OnButton)
            return btn

        insertTimeButton = MakeButton(text.buttonInsertTime, '{TIME}')
        insertTimeButton1 = MakeButton(text.buttonInsertTime1, '{TIME1}')
        insertDateButton = MakeButton(text.buttonInsertDate, '{DATE}')
        insertDateButton1 = MakeButton(text.buttonInsertDate1, '{DATE1}')

        voices = self.plugin.GetVoices()
        devs = self.plugin.GetAudioOutputs()

        voiceChoice = wx.Choice(panel, wx.ID_ANY, choices=voices)
        voiceName = voiceName if voiceName else voices[0]
        voiceChoice.SetStringSelection(voiceName)
        devChoice = wx.Choice(panel, wx.ID_ANY, choices=devs)
        devName = device if device else devs[0]
        devChoice.SetStringSelection(devName)

        rateCtrl = CustomSlider(
            panel,
            value=int(rate),
            valueLabel=text.normal,
            minValue=-5,
            minLabel=text.slow,
            maxValue=5,
            maxLabel=text.fast,
            style=wx.SL_AUTOTICKS | wx.SL_TOP
        )

        volumeCtrl = CustomSlider(
            panel,
            value=volume,
            valueLabel="%(1)i %%",
            minValue=0,
            minLabel=text.silent,
            maxValue=100,
            maxLabel=text.loud,
            style=wx.SL_AUTOTICKS | wx.SL_TOP
        )
        volumeCtrl.slider.SetTickFreq(10, 3)

        sizer1 = eg.HBoxSizer((textCtrl, 1, wx.EXPAND))
        sizer2 = eg.HBoxSizer(
            insertTimeButton,
            (insertTimeButton1, 0, wx.ALIGN_LEFT, 3),
            ((10, 5), 0),
            (insertDateButton, 0, wx.ALIGN_RIGHT, 3),
            (insertDateButton1, 0, wx.ALIGN_RIGHT)
        )
        staticBoxSizer1 = panel.VStaticBoxSizer(
            text.textBoxLabel,
            (sizer1, 0, wx.EXPAND | wx.ALL, 5),
            (sizer2, 0, wx.EXPAND | wx.ALL, 5),
        )
        ACV = wx.ALIGN_CENTER_VERTICAL
        sizer3 = wx.FlexGridSizer(0, 2, 5, 5)
        sizer3.AddGrowableCol(1, 1)
        sizer3.AddMany(
            (
                (panel.StaticText(text.labelVoice), 0, ACV | wx.BOTTOM, 10),
                (voiceChoice, 0, wx.EXPAND | wx.BOTTOM, 10),
                (panel.StaticText(text.device), 0, ACV | wx.BOTTOM, 10),
                (devChoice, 0, wx.EXPAND | wx.BOTTOM, 10),
                (panel.StaticText(text.labelRate), 0, ACV),
                (rateCtrl, 0, wx.EXPAND),
                (panel.StaticText(text.labelVolume), 0, ACV),
                (volumeCtrl, 0, wx.EXPAND),
                (panel.StaticText(text.addSuffix), 0, ACV),
                (suffCtrl, 0, wx.EXPAND)
            )
        )

        staticBoxSizer2 = panel.VStaticBoxSizer(
            text.voiceProperties,
            (sizer3, 0, wx.EXPAND | wx.ALL, 5),
        )

        panel.sizer.Add(staticBoxSizer1, 0, wx.EXPAND)
        panel.sizer.Add(staticBoxSizer2, 0, wx.EXPAND | wx.TOP, 10)

        while panel.Affirmed():
            panel.SetResult(
                voiceChoice.GetStringSelection(),
                rateCtrl.GetValue(),
                textCtrl.GetValue(),
                suffCtrl.GetValue(),
                volumeCtrl.GetValue(),
                devChoice.GetStringSelection()
            )

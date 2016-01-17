# -*- coding: utf-8 -*-
#
# Plugins/Speech/__init__.py
#
# Copyright (C) 2006 MonsterMagnet
#
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
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
# Changelog (in reverse chronological order):
# -------------------------------------------
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


eg.RegisterPlugin(
    name = "Speech",
    author = "MonsterMagnet",
    guid = "{76A1638D-1D7D-4582-A726-A17B1A6FC723}",
    version = "2.2",
    description = (
        "Uses the Text-To-Speech service of the Microsoft Speech API (SAPI)."
    ),
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6828",
    icon = (
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


from win32com.client import Dispatch, DispatchWithEvents
from time import strftime
from threading import Thread
import pythoncom


class Text:
    name = "Text to speech"
    description = "Uses the Microsoft Speech API (SAPI) to speak a text."
    label = "Speak: %s"
    errorCreate = "Cannot create voice object"
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
    suffix = "SpeakingFinished"
    addSuffix = "Additional event suffix:"
    device = "Output device:"
    

class CustomSlider(wx.Window):
    
    def __init__(
        self, 
        parent, 
        id = -1,
        value = None,
        minValue = None,
        maxValue = None,
        pos = wx.DefaultPosition,
        size = wx.DefaultSize,
        style = 0,
        valueLabel = None,
        minLabel = None,
        maxLabel = None,
    ):
        self.valueLabel = valueLabel
        wx.Window.__init__(self, parent, id, pos, size, style)
        sizer = wx.GridBagSizer()
        sizer.AddGrowableCol(1, 1)
        self.slider = wx.Slider(
            self,
            -1,
            value,
            minValue,
            maxValue,
            style = style
        )
        sizer.Add(self.slider, (0, 0), (1, 3), wx.EXPAND)   
        st = wx.StaticText(self, -1, minLabel)
        sizer.Add(st, (1, 0), (1, 1), wx.ALIGN_LEFT)   
        self.valueLabelCtrl = wx.StaticText(self, -1, valueLabel)
        sizer.Add(self.valueLabelCtrl, (1, 1), (1, 1), wx.ALIGN_CENTER_HORIZONTAL)   
        st = wx.StaticText(self, -1, maxLabel)
        sizer.Add(st, (1, 2), (1, 1), wx.ALIGN_RIGHT)   
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
        

#class SpeechEvents:
#    def OnEndStream(self, StreamNumber, StreamPosition):
#        print 'OnEndStream: StreamNumber=%s, StreamPosition=%s' % (
#            StreamNumber,
#            StreamPosition
#        )

class Speaker(Thread):
    def __init__(
        self,
        plugin,
        text,
        voiceName,
        rate,
        volume,
        suff,
        device
        ):
        super(Speaker, self).__init__()
        self.plugin = plugin
        self.text = text
        self.voiceName = voiceName
        self.rate = rate
        self.volume = volume
        self.suff = suff
        self.device = device
        self.start()

    def run(self):
        try:
            pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
            #tts = DispatchWithEvents("SAPI.SpVoice.1", SpeechEvents)
            tts = Dispatch('SAPI.SpVoice')
        except:
            self.plugin.PrintError(self.plugin.text.errorCreate)
            return
        vcs = tts.GetVoices()
        voices = [(voice.GetDescription(), voice) for voice in vcs]
        tmp = [item[0] for item in voices]
        ix = tmp.index(self.voiceName) if self.voiceName in tmp else 0
        tts.Voice = voices[ix][1]
        
        devs = tts.GetAudioOutputs()
        devices = [(dev.GetDescription(), dev) for dev in devs]
        tmp = [item[0] for item in devices]
        ix = tmp.index(self.device) if self.device in tmp else 0
        tts.AudioOutput = devices[ix][1]       
        
        tts.Rate = self.rate
        tts.Volume = self.volume        
        tts.Speak(self.text,0) 
        suffix = self.plugin.text.suffix if self.suff == "" else "%s.%s" % (
            self.plugin.text.suffix,
            self.suff
        )
        self.plugin.TriggerEvent(suffix)


class Speech(eg.PluginClass):  

    def __init__(self):
        self.AddAction(TextToSpeech)

    
    
class TextToSpeech(eg.ActionClass):
    text = Text
    
    def __call__(self, voiceName, rate, voiceText, suff, volume, device = None):
        self.suff = suff if suff != 0 else ""            

        def filterFunc(s):
            if s == "DATE":
                return '</context><context ID = "date_mdy">' + strftime("%m/%d/%Y") + '</context><context>'
            elif s == "DATE1":
                return '</context><context ID = "date_mdy">' + strftime("%m/%d/%y") + '</context><context>'
            elif s == "TIME":
                return '</context><context ID = "time">' + strftime("%H:%M:%S") + '</context><context>'
            elif s == "TIME1":
                return '</context><context ID = "time">' + strftime("%H:%M") + '</context><context>'
            else:
                return None
                
        voiceText = eg.ParseString(voiceText, filterFunc)
        voiceText = "<context>" + voiceText + "</context>"
        if voiceText.startswith('<context></context>'):
            voiceText = voiceText[19:]
        voiceText = voiceText.replace(
            '</context><context></context>',
            '</context>'
        )      
        
        sp=Speaker(
            self.plugin,
            voiceText,
            voiceName,
            rate,
            volume,
            suff,
            device
        )
     
    
    def GetLabel(self, voiceName, rate, voiceText, suff, volume, device = None):
        return self.text.label % voiceText
   

    def Configure(
        self, 
        voiceName=None, 
        rate=0,
        voiceText="", 
        suff="", 
        volume=100,
        device = None
    ):
        suff = suff if suff != 0 else "" 
        text = self.text
        panel = eg.ConfigPanel()
        plugin = self.plugin
            
        textCtrl = wx.TextCtrl(panel, -1, voiceText)           
        suffCtrl = wx.TextCtrl(panel, -1, suff)           
       
        insertTimeButton = wx.Button(panel, -1, text.buttonInsertTime)
        def OnButton(event):
            textCtrl.WriteText('{TIME}')
            textCtrl.SetFocus()
        insertTimeButton.Bind(wx.EVT_BUTTON, OnButton)
        
        insertTimeButton1 = wx.Button(panel, -1, text.buttonInsertTime1)
        def OnButton(event):
            textCtrl.WriteText('{TIME1}')
            textCtrl.SetFocus()
        insertTimeButton1.Bind(wx.EVT_BUTTON, OnButton)
        
        insertDateButton = wx.Button(panel, -1, text.buttonInsertDate)
        def OnButton(event):
            textCtrl.WriteText('{DATE}')
            textCtrl.SetFocus()
        insertDateButton.Bind(wx.EVT_BUTTON, OnButton)
        
        insertDateButton1 = wx.Button(panel, -1, text.buttonInsertDate1)
        def OnButton(event):
            textCtrl.WriteText('{DATE1}')
            textCtrl.SetFocus()
        insertDateButton1.Bind(wx.EVT_BUTTON, OnButton)
        

        
        try:
            #self.VoiceObj = DispatchWithEvents("SAPI.SpVoice.1", SpeechEvents)
            VoiceObj = Dispatch("Sapi.SpVoice")
        except:
            self.PrintError(self.text.errorCreate)
            return
        voices = [voice.GetDescription() for voice in VoiceObj.GetVoices()]
        devs = [dev.GetDescription() for dev in VoiceObj.GetAudioOutputs()]
        del VoiceObj

        voiceChoice = wx.Choice(panel, -1, choices=voices)
        voiceName = voiceName if voiceName  else voices[0]
        voiceChoice.SetStringSelection(voiceName)
        devChoice = wx.Choice(panel, -1, choices=devs)
        devName = device if device  else devs[0]
        devChoice.SetStringSelection(devName)
        
        
        
        

        rateCtrl = CustomSlider(
            panel,
            value = int(rate),
            valueLabel = text.normal,
            minValue = -5,
            minLabel = text.slow,
            maxValue = 5,
            maxLabel = text.fast,
            style = wx.SL_AUTOTICKS|wx.SL_TOP
        )
                   
        volumeCtrl = CustomSlider(
            panel,
            value = volume,
            valueLabel = "%(1)i %%",
            minValue = 0,
            minLabel = text.silent,
            maxValue = 100,
            maxLabel = text.loud,
            style = wx.SL_AUTOTICKS|wx.SL_TOP
        )
        volumeCtrl.slider.SetTickFreq(10, 3)
        
        sizer1 = eg.HBoxSizer(
            (textCtrl, 1, wx.EXPAND)
        )
        sizer2 = eg.HBoxSizer(
            (insertTimeButton),
            (insertTimeButton1, 0, wx.ALIGN_LEFT,3),
            ((10, 5),0),
            (insertDateButton, 0, wx.ALIGN_RIGHT, 3),
            (insertDateButton1, 0, wx.ALIGN_RIGHT)
        )
        staticBoxSizer1 = panel.VStaticBoxSizer(
            text.textBoxLabel,
            (sizer1, 0, wx.EXPAND|wx.ALL, 5),
            (sizer2, 0, wx.EXPAND|wx.ALL, 5),
        )
        ACV = wx.ALIGN_CENTER_VERTICAL
        sizer3 = wx.FlexGridSizer(4, 2, 5, 5)
        sizer3.AddGrowableCol(1, 1)
        sizer3.AddMany(
            (
                (panel.StaticText(text.labelVoice), 0, ACV|wx.BOTTOM, 10),
                (voiceChoice, 0, wx.EXPAND|wx.BOTTOM, 10),
                (panel.StaticText(text.device), 0, ACV|wx.BOTTOM, 10),
                (devChoice, 0, wx.EXPAND|wx.BOTTOM, 10),
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
            (sizer3, 0, wx.EXPAND|wx.ALL, 5),
        )
        
        panel.sizer.Add(staticBoxSizer1, 0, wx.EXPAND)
        panel.sizer.Add(staticBoxSizer2, 0, wx.EXPAND|wx.TOP, 10)
       
        while panel.Affirmed():
            panel.SetResult(
                voiceChoice.GetStringSelection(),
                rateCtrl.GetValue(), 
                textCtrl.GetValue(), 
                suffCtrl.GetValue(),
                volumeCtrl.GetValue(),
                devChoice.GetStringSelection()
            )


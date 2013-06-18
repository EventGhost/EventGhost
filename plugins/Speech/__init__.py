import eg
import wx

from win32com.client import Dispatch
from time import strftime


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
        
    
    def GetValue(self):
        return self.slider.GetValue()
        
        
    def SetValue(self):
        self.slider.SetValue()
        
        
        
class Speech(eg.PluginClass):
    
    def __init__(self):
        self.AddAction(TextToSpeech)


    def __start__(self):
        try:
            self.VoiceObj = Dispatch("Sapi.SpVoice")
        except:
            self.PrintError(self.text.errorCreate)
            return
        
        # enumerate all available voices and store them in a dict with their
        # name as key
        voices = {}
        for voice in self.VoiceObj.GetVoices():
            voices[voice.GetDescription()] = voice
        self.voices = voices



class Text:
    name = "Text to speech"
    description = "Uses the Microsoft Speech API (SAPI) to speak a text."
    label = "Speak: %s"
    errorNoVoice = "Voice with name %s is not available"
    errorCreate = "Cannot create voice object"
    buttonInsertTime = "Insert time"    
    buttonInsertDate = "Insert date"
    buttonPlayback = "Playback text"
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
    
    
    
class TextToSpeech(eg.ActionClass):
    text = Text
    
    def __call__(self, voiceName, rate, voiceText, time, volume):
            
        voiceObj = self.plugin.VoiceObj
        try:
            voiceObj.Voice = self.plugin.voices[voiceName]
        except:
            self.PrintError (self.text.errorNoVoice % voiceName)
        voiceObj.Rate = rate
        voiceObj.Volume = volume
        def filterFunc(s):
            if s == "DATE":
                return '</context><context ID="time">' + strftime("%x") + '</context><context>'
            elif s == "TIME":
                return '</context><context ID="time">' + strftime("%X") + '</context><context>'
            else:
                return ""
                
        voiceText = eg.ParseString(voiceText, filterFunc)
        voiceObj.Speak("<context>" + voiceText + "</context>", 1)
        if time == 1:
            voiceObj.Speak(strftime("%X"), 1)
        elif time == 2:
            voiceObj.Speak(strftime("%x"), 1)
        elif time == 3:
            voiceObj.Speak(strftime("%x %X"), 1)
       
    
    def GetLabel(self, voiceName, rate, voiceText, time, volume):
        return self.text.label % voiceText
   

    def Configure(
        self, 
        voiceName=None, 
        rate=0,
        voiceText="", 
        time=0, 
        volume=100
    ):
        text = self.text
        dialog = eg.ConfigurationDialog(self)
        plugin = self.plugin
            
        textCtrl = wx.TextCtrl(dialog, -1, voiceText)           
       
        insertTimeButton = wx.Button(dialog, -1, text.buttonInsertTime)
        def OnButton(event):
            textCtrl.WriteText('{TIME}')
            textCtrl.SetFocus()
        insertTimeButton.Bind(wx.EVT_BUTTON, OnButton)
        
        insertDateButton = wx.Button(dialog, -1, text.buttonInsertDate)
        def OnButton(event):
            textCtrl.WriteText('{DATE}')
            textCtrl.SetFocus()
        insertDateButton.Bind(wx.EVT_BUTTON, OnButton)
        
        testButton = wx.Button(dialog, -1, text.buttonPlayback)
        def OnButton(event):
            self(*ReturnResult())
        testButton.Bind(wx.EVT_BUTTON, OnButton)
        
        try:
            VoiceObj = self.plugin.VoiceObj
            allVoices = self.plugin.voices.keys()
            allVoices.sort()
            try:
                voiceIndex = allVoices.index(voiceName)
            except:
                voiceIndex = 0
        except:
            voiceIndex = 0
            allVoices = []
        voiceChoice = wx.Choice(dialog, -1, choices=allVoices)
        voiceChoice.Select(voiceIndex)

        rateCtrl = CustomSlider(
            dialog,
            value = int(rate),
            valueLabel = text.normal,
            minValue = -5,
            minLabel = text.slow,
            maxValue = 5,
            maxLabel = text.fast,
            style = wx.SL_AUTOTICKS|wx.SL_TOP
        )
                   
        volumeCtrl = CustomSlider(
            dialog,
            value = volume,
            valueLabel = "%(1)i %%",
            minValue = 0,
            minLabel = text.silent,
            maxValue = 100,
            maxLabel = text.loud,
            style = wx.SL_AUTOTICKS|wx.SL_TOP
        )
        volumeCtrl.slider.SetTickFreq(10, 3)
        

        staticBox = wx.StaticBox(dialog, -1, text.textBoxLabel)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(textCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(insertTimeButton)
        sizer2.Add(insertDateButton, 0, wx.LEFT|wx.EXPAND|wx.ALIGN_LEFT, 5)
        sizer2.Add((5, 5), 1)
        sizer2.Add(testButton, 0, wx.LEFT, 5)
        staticBoxSizer.Add(sizer2, 0, wx.ALL|wx.EXPAND, 5)

        dialog.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        staticBox = wx.StaticBox(dialog, -1, text.voiceProperties)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        
        sizer1 = wx.FlexGridSizer(3, 2, 5, 5)
        sizer1.AddGrowableCol(1, 1)
        
        st = wx.StaticText(dialog, -1, text.labelVoice)
        sizer1.Add(st, 0, wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 10)
        sizer1.Add(voiceChoice, 0, wx.EXPAND|wx.BOTTOM, 10)
        
        st = wx.StaticText(dialog, -1, text.labelRate)
        sizer1.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(rateCtrl, 0, wx.EXPAND)
        
        st = wx.StaticText(dialog, -1, text.labelVolume)
        sizer1.Add(st, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer1.Add(volumeCtrl, 0, wx.EXPAND)
        
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        dialog.sizer.Add(staticBoxSizer, 0, wx.EXPAND|wx.TOP, 10)
       
        def ReturnResult():
            return (
                voiceChoice.GetStringSelection(),
                rateCtrl.GetValue(), 
                textCtrl.GetValue(), 
                0,
                volumeCtrl.GetValue()
            )
                    
        if dialog.AffirmedShowModal():
            return ReturnResult()


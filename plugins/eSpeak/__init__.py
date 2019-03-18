# -*- coding: utf-8 -*-
#

"""<rst>
Plugin for using **eSpeak** text to speach program.


eSpeak installation does not contain **libespeak.dll** which is required for this plugin.
Portable 32-bit libespeak.dll for eSpeak version 1.48 is supplied with this plugin 
(in its directory) -- you are free to use and relocate it as eSpeak licence permits.

If you did not run eSpeak installation program, system has no eSpeak **registry** record
and no environment variable **ESPEAK_DATA_PATH** with the path of the directory which contains 
the **espeak-data** directory. You can configure plugin to you use eSpeak without them, 
just locate espeak-data directory containing data of metioned eSpeak version.
The configuration failures will be printed to EventGhost log.

**Links:**

`eSpeak <http://espeak.sourceforge.net>`_

`eSpeak Documentation <http://espeak.sourceforge.net/docindex.html>`_

`Search Path Used by Windows to Locate a DLL <https://docs.microsoft.com/en-us/windows/desktop/Dlls/dynamic-link-library-search-order>`_
"""

import eg



eg.RegisterPlugin(
    name = "eSpeak",
    author = "obermann",
    version = "1.48.15.01",
    kind = "program",
    canMultiLoad = False,
    description = __doc__,
    guid = "{B4ABA767-CE75-4012-863E-0C9C3994591C}",
    url = eg.folderPath.ProgramFiles + r"\eSpeak\docs\index.html",
    icon = (
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQAQMAAAAlPW0iAAAABlBMVEUAAADdEREZXxxOAAAAAXRS"
    "TlMAQObYZgAAADdJREFUeF4VwjENACAMAMFPOrCBgQaQ0aGiKgFpSEECY0fC5fgmEpRLS7rjlRik"
    "YoYG7fxlIwt4xzMI/RonXVkAAAAASUVORK5CYII="
    )
)



import wx
import os
import locale
import _winreg
from ctypes import c_int, c_uint, c_ubyte, c_size_t, c_char_p, c_void_p
from ctypes import POINTER, CFUNCTYPE, CDLL, Structure, sizeof, create_string_buffer



AUDIO_OUTPUT_PLAYBACK = 0       # PLAYBACK mode: plays the audio data, supplies events to the calling program
AUDIO_OUTPUT_RETRIEVAL = 1      # RETRIEVAL mode: supplies audio data and events to the calling program
AUDIO_OUTPUT_SYNCHRONOUS = 2    # SYNCHRONOUS mode: as RETRIEVAL but doesn't return until synthesis is completed
AUDIO_OUTPUT_SYNCH_PLAYBACK = 3 # Synchronous playback

espeakINITIALIZE_PHONEME_EVENTS = 0x0001
espeakINITIALIZE_PHONEME_IPA    = 0x0002
espeakINITIALIZE_DONT_EXIT      = 0x8000

EE_OK               = 0
EE_INTERNAL_ERROR   = -1
EE_BUFFER_FULL      = 1
EE_NOT_FOUND        = 2

espeakSSML          = 0x10
espeakPHONEMES      = 0x100
espeakENDPAUSE      = 0x1000
espeakKEEP_NAMEDATA = 0x2000

espeakCHARS_UTF8    = 1

# enums:
espeak_POSITION_TYPE = c_int 
espeak_AUDIO_OUTPUT = c_int 
espeak_ERROR = c_int 
espeak_PARAMETER = c_int 

class espeak_VOICE(Structure):
    _fields_ = [('name', c_char_p),
                ('languages', c_char_p),
                ('identifier', c_char_p),
                ('gender', c_ubyte),
                ('age', c_ubyte),
                ('variant', c_ubyte),
                ('xx1', c_ubyte),
                ('score', c_int),
                ('spare', c_void_p)
                ]

OK_RATE = 8000


class STuple(tuple):

    def __new__ (cls, *args):
        return super(STuple, cls).__new__(cls, args)
        
        
    def seek(self, key):
        try:
            return self.index(key)
        except ValueError:
            return len(self) if key else 0
            
            
    def search(self, key):
        try:
            return self.index(key)
        except ValueError:
            return 0
                
                
                
PARAMETERS = STuple(
    "Ignore", # internal use
    "Rate",
    "Volume",
    "Pitch",
    "Range",
    "Punctuation",
    "Capitals",
    "Wordgap",
    "Options",   # reserved for misc. options.  not yet used
    "Intonation",
)



class Text:
    e01 = "Error loading DLL: %s"
    e02 = "Error. Not found: %s"
    e03 = "Error. eSpeak installation not found."
    e04 = "eSpeak is not intialized."
    e05 = "Error. eSpeak initialization failure (returned value = %i). Check plugin configuration for espeak-data."
    e06 = "Error. Path to espeak-data cannot not contain foreign characters."
    
    n01 = "libespeak.dll successfully loaded from: %s"
    n02 = "eSpeak successfully initialized with sample rate: %i"
    
    dlg01 = "Location of espeak-data:"
    dlg02 = "Location of libespeak.dll:"
    dlg05 = "Select the directory which contains the espeak-data directory:"
    dlg06 = "Select the directory which contains libespeak.dll:"
    
    c01 = "Set by eSpeak Installation"
    c02 = "Same as espeak-data"
    c03 = "On System's Seach Path"
    c04 = "Directory of this Plugin"
    c05 = "Custom:"
    
    c10 = "Use EventGhost Result Value"
    c11 = "Set Relative"
    c12 = "Request Default"
    
    c21 = "{...} At First Evaluate Text for EventGhost Python Scripts"
    c22 = "<_>...</_> Interpret SSML Markup"
    c23 = "[[...]] Interpret Phoneme Codes"
    c24 = "Add a Sentence Pause at the End of the Text"
    c25 = "Synchronize - Wait for a Speach to End"


                
class eSpeak(eg.PluginClass):

    text = Text()

    def _load(self):
        path = "libespeak" if self.espeak_dll is None else os.path.join(self.espeak_dll, "libespeak")
        try:    
            self.libespeak = CDLL(path)
        except:
            eg.PrintError(self.text.e01 % path)
            self.libespeak = None
            return
        self.espeak_Initialize = self.libespeak.espeak_Initialize
        self.espeak_Initialize.restype = espeak_ERROR
        self.espeak_Initialize.argtypes = [espeak_AUDIO_OUTPUT, c_int, c_char_p, c_int]
        self.espeak_Synth = self.libespeak.espeak_Synth
        self.espeak_Synth.restype = espeak_ERROR
        self.espeak_Synth.argtypes = [c_void_p, c_size_t, c_uint, espeak_POSITION_TYPE, c_uint, c_uint, POINTER(c_uint), c_void_p]
        self.espeak_SetParameter = self.libespeak.espeak_SetParameter
        self.espeak_SetParameter.restype = espeak_ERROR
        self.espeak_SetParameter.argtypes = [espeak_PARAMETER, c_int, c_int]
        self.espeak_GetParameter = self.libespeak.espeak_GetParameter
        self.espeak_GetParameter.restype = c_int
        self.espeak_GetParameter.argtypes = [espeak_PARAMETER, c_int]
        self.espeak_ListVoices = self.libespeak.espeak_ListVoices
        self.espeak_ListVoices.restype = POINTER(POINTER(espeak_VOICE))
        self.espeak_ListVoices.argtypes = [POINTER(espeak_VOICE)]
        self.espeak_SetVoiceByName = self.libespeak.espeak_SetVoiceByName
        self.espeak_SetVoiceByName.restype = espeak_ERROR
        self.espeak_SetVoiceByName.argtypes = [c_char_p]
        self.espeak_SetVoiceByProperties = self.libespeak.espeak_SetVoiceByProperties
        self.espeak_SetVoiceByProperties.restype = espeak_ERROR
        self.espeak_SetVoiceByProperties.argtypes = [POINTER(espeak_VOICE)]
        self.espeak_GetCurrentVoice = self.libespeak.espeak_GetCurrentVoice
        self.espeak_GetCurrentVoice.restype = POINTER(espeak_VOICE)
        self.espeak_GetCurrentVoice.argtypes = []
        self.espeak_Cancel = self.libespeak.espeak_Cancel
        self.espeak_Cancel.restype = espeak_ERROR
        self.espeak_Cancel.argtypes = []
        self.espeak_Synchronize = self.libespeak.espeak_Synchronize
        self.espeak_Synchronize.restype = espeak_ERROR
        self.espeak_Synchronize.argtypes = []
        self.espeak_Terminate = self.libespeak.espeak_Terminate
        self.espeak_Terminate.restype = espeak_ERROR
        self.espeak_Terminate.argtypes = [] 
        print self.text.n01 % self.espeak_dll
        
        
    def __init__(self):
        self.libespeak = None
        self.rate = -1000
        
        self.AddAction(SetVoice)
        self.AddAction(GetVoice)
        self.AddAction(SetParameter)
        self.AddAction(GetParameter)
        self.AddAction(Text)
        self.AddAction(Cancel)
        

    def __start__(self, espeak_data="installation", espeak_dll="plugin"):

        self.espeak_data = None
        if espeak_data == "installation":
            pass
        elif espeak_data == "plugin":
            self.espeak_data = os.path.dirname(os.path.abspath(__file__))
        else:
            self.espeak_data = espeak_data
            
        if self.espeak_data is not None and not os.path.isdir(os.path.join(self.espeak_data, "espeak-data")):
            eg.PrintError(self.text.e02 % os.path.join(self.espeak_data, "espeak-data"))
            return
            
        self.espeak_dll = None
        if espeak_dll == "system":
            pass
        elif espeak_dll == "same":
            if espeak_data == "installation":
                # immitate speak_lib.cpp
                # pass over eg.folderPath.ProgramFiles + r"\eSpeak"
                try:
                    if os.path.isdir(os.path.join(os.environ["ESPEAK_DATA_PATH"], "espeak-data")):
                        self.espeak_dll = os.environ["ESPEAK_DATA_PATH"]
                except KeyError:
                    pass
                if self.espeak_dll is None:
                    try:
                        with _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\Microsoft\Speech\Voices\Tokens\eSpeak") as key:
                            self.espeak_dll = _winreg.QueryValueEx(key, "Path")[0]
                    except:
                        pass
                if self.espeak_dll is None:
                    eg.PrintError(self.text.e03)
                    return
            else:
                self.espeak_dll = self.espeak_data
        elif espeak_dll == "plugin":
            self.espeak_dll = os.path.dirname(os.path.abspath(__file__))
        else:
            self.espeak_dll = espeak_dll
            
        if self.espeak_dll is not None and not os.path.isfile(os.path.join(self.espeak_dll, "libespeak.dll")):
            eg.PrintError(self.text.e02 % os.path.join(self.espeak_dll, "libespeak.dll"))
            return
        
        if self.libespeak is None:
            self._load()
        if self.libespeak is None:
            return
            
        data = None 
        if self.espeak_data is not None:
            try:
                # DLL use fopen() for espeak_data
                data = self.espeak_data.encode(locale.getdefaultlocale()[1])
            except UnicodeEncodeError:
                eg.PrintError(self.text.e06)
                return
        self.rate = self.espeak_Initialize(
            AUDIO_OUTPUT_PLAYBACK, 
            0, 
            data, 
            espeakINITIALIZE_DONT_EXIT
            )
        # None of these checks will work with standard build of 1.48.15!
        # Suplied DLL is patched and will work with both.
        #if self.rate == EE_INTERNAL_ERROR:
        if self.rate < OK_RATE:
            #eg.PrintError("Error with returned sample rate", self.rate, "by", "espeak_Initialize")
            eg.PrintError(self.text.e05 % self.rate)
        else:
            print self.text.n02 % self.rate

            
    def __stop__(self):
        eg.PrintDebugNotice("eSpeak __stop__()")
        if self.libespeak is None or self.rate < OK_RATE:
            return
        result = self.espeak_Terminate()
        if result != EE_OK:
            eg.PrintError("Error No.", result, "by", "espeak_Terminate")
            
            
    def is_off(self):
        """
        Pattern for every action check:
        if self.plugin.is_off(): return
        """
        if self.libespeak is None or self.rate < OK_RATE:
            eg.PrintError(self.text.e04)
            return True
        else:
            return False
        
        
    def Configure(self, espeak_data="installation", espeak_dll="plugin"):
        data_list = STuple(
            "installation",
            "plugin"
        )
        dll_list = STuple(
            "same",
            "system",
            "plugin"
        )
        panel = eg.ConfigPanel()
        panel.AddCtrl(wx.StaticText(panel, -1, self.text.dlg01))
        dataRadio = panel.RadioBox(data_list.seek(espeak_data), (self.text.c01, self.text.c04, self.text.c05))
        panel.AddCtrl(dataRadio)
        # dataControl = eg.DirBrowseButton(
            # panel,
            # startDirectory=espeak_data,
            # buttonText=eg.text.General.browse,
            # dialogTitle=self.text.dlg05
        # )
        dataControl = wx.DirPickerCtrl(
            panel,
            -1,
            path=espeak_data,
            message=self.text.dlg05,
            style=wx.DIRP_USE_TEXTCTRL,
        )
        def dataEevent(evt):
            if len(data_list) == evt.GetSelection():
                dataControl.Enable()
            else:
                dataControl.Enable(False)
                dataControl.SetPath("")
        dataEevent(dataRadio)
        dataRadio.Bind(wx.EVT_RADIOBOX, dataEevent)
        
        panel.sizer.Add(dataControl, 0, wx.EXPAND)
        panel.sizer.Add(wx.StaticLine(panel), 0, wx.EXPAND|wx.BOTTOM|wx.TOP, 10)
        panel.AddCtrl(wx.StaticText(panel, -1, self.text.dlg02))
        dllRadio = panel.RadioBox(dll_list.seek(espeak_dll), (self.text.c02, self.text.c03, self.text.c04, self.text.c05))
        panel.AddCtrl(dllRadio)
        dllControl = wx.DirPickerCtrl(
            panel,
            -1,
            path=espeak_dll,
            message=self.text.dlg06,
            style=wx.DIRP_USE_TEXTCTRL,
        )
        # dllControl = wx.FilePickerCtrl(
            # panel,
            # -1,
            # path=espeak_dll,
            # wildcard="libespeak.dll",
            # message=self.text.dlg06,
            # style=wx.FLP_OPEN | wx.FLP_USE_TEXTCTRL,
        # )
        def dllEevent(evt):
            if len(dll_list) == evt.GetSelection():
                dllControl.Enable()
            else:
                dllControl.Enable(False)
                dllControl.SetPath("")
        dllEevent(dllRadio)
        dllRadio.Bind(wx.EVT_RADIOBOX, dllEevent)
        panel.sizer.Add(dllControl, 0, wx.EXPAND)

        while panel.Affirmed():
            global data
            global dll
            # eg's DirBrowseButton.IsEnabled() is buggy
            if len(data_list) == dataRadio.GetValue():
                data = dataControl.GetPath()
                if data in data_list:
                    data = ".\\" + data
            else:
                data = data_list[dataRadio.GetValue()]
                
            if len(dll_list) == dllRadio.GetValue():
                dll = dllControl.GetPath()
                if dll in dll_list:
                    dll = ".\\" + dll
            else:
                dll = dll_list[dllRadio.GetValue()]
                
            panel.SetResult(data, dll)

            
            
class SetParameter(eg.ActionBase):
    """
    Set the relative or absolute value of the specified parameter.
    """
    name = "Set Parameter"
    with open(os.path.join(os.path.dirname(__file__), "parameters.html"), "r") as file:
        description = __doc__ + "\n\n" + file.read().decode("utf8")
    
    
    def __call__(self, type, value, relative=False, from_eg_result=False):
        if self.plugin.is_off() or not PARAMETERS.search(type.capitalize()): 
            return
        if from_eg_result:
            # ValueError expected from users, its OK
            value = int(eg.result)
        result = self.plugin.espeak_SetParameter(PARAMETERS.search(type.capitalize()), value, relative)
        if result != EE_OK:
            eg.PrintError("Error No.", result, "by", "espeak_SetParameter", "with value:", value)
            

    def Configure(self, type="Ignore", value=0, relative=False, from_eg_result=False):
        panel = eg.ConfigPanel()
        typeControl = panel.Choice(PARAMETERS.search(type.capitalize()), PARAMETERS)
        relativeControl = panel.CheckBox(relative, self.plugin.text.c11)
        valueControl = panel.SpinIntCtrl(value, min=-10000, max=10000)
        valueControl.Enable(not from_eg_result)
        fromControl = panel.CheckBox(from_eg_result, self.plugin.text.c10)
        def egresultOn(evt):
            if evt.IsChecked():
                valueControl.Enable(False)
                valueControl.SetValue(0)
            else:
                valueControl.Enable()
        fromControl.Bind(wx.EVT_CHECKBOX, egresultOn)
        panel.AddCtrl(typeControl)
        panel.AddCtrl(relativeControl)
        panel.AddCtrl(valueControl)
        panel.AddCtrl(fromControl)
        while panel.Affirmed():
            panel.SetResult(
                PARAMETERS[typeControl.GetValue()],
                valueControl.GetValue(),
                relativeControl.GetValue(),
                fromControl.GetValue(),
            )
            
            
            
class GetParameter(eg.ActionBase):
    """
    Returns the current or default value of the specified parameter.
    """
    name = "Get Parameter"
    with open(os.path.join(os.path.dirname(__file__), "parameters.html"), "r") as file:
        description = __doc__ + "\n\n" + file.read().decode("utf8")
        
    
    def __call__(self, type, default=False):
        if not self.plugin.is_off() and PARAMETERS.search(type.capitalize()): 
            return self.plugin.espeak_GetParameter(PARAMETERS.search(type.capitalize()), int(not default))

            
    def Configure(self, type="Ignore", default=False):
        panel = eg.ConfigPanel()
        typeControl = panel.Choice(PARAMETERS.search(type.capitalize()), PARAMETERS)
        defaultControl = panel.CheckBox(default, self.plugin.text.c12)
        panel.AddCtrl(typeControl)
        panel.AddCtrl(defaultControl)
        while panel.Affirmed():
            panel.SetResult(
                PARAMETERS[typeControl.GetValue()],
                defaultControl.GetValue(),
            )
            

            
class SetVoice(eg.ActionBase):
    
    name = "Set Voice"
    description = "Select the voice by name."
    
    def __call__(self, voice, from_eg_result=False):
        if self.plugin.is_off(): return
        if from_eg_result:
            voice = eg.result
        if voice:
            result = self.plugin.espeak_SetVoiceByName(voice.encode("utf-8"))
            if result != EE_OK:
                eg.PrintError("Error No.", result, "by", "espeak_SetVoiceByName", "with value:", voice)
        else:
            eg.PrintError("Error. None voice was not set.")
            
        
    def Configure(self, voice="default", from_eg_result=False):
        selection = 0
        list = []
        result = None
        if not self.plugin.is_off():
            result = self.plugin.espeak_ListVoices(None)
        if result:
            for pVoice in result:
                if pVoice:
                    #list.append(pVoice.contents.identifier.decode())
                    list.append(pVoice.contents.name.decode("utf-8"))
                else:
                    break # important
            try:
                selection = list.index(voice)
            except ValueError:
                pass
        panel = eg.ConfigPanel()
        voiceControl = panel.Choice(selection, list)
        voiceControl.Enable(not from_eg_result)
        fromControl = panel.CheckBox(from_eg_result, self.plugin.text.c10)
        def egresultOn(evt):
            if evt.IsChecked():
                voiceControl.Enable(False)
            else:
                voiceControl.Enable()
        fromControl.Bind(wx.EVT_CHECKBOX, egresultOn)
        panel.AddCtrl(voiceControl)
        panel.AddCtrl(fromControl)
        while panel.Affirmed():
            panel.SetResult(
                list[voiceControl.GetValue()] if list else "",
                fromControl.GetValue()
            )

            
            
class GetVoice(eg.ActionBase):
    """
    Returns the name for the currently selected voice.
    This is not affected by temporary voice changes caused by SSML elements such as &lt;voice&gt; or &lt;s&gt;.
    """
    name = "Get Voice"
    description = __doc__
    
    def __call__(self):
        if self.plugin.is_off(): return
        result = self.plugin.espeak_GetCurrentVoice()
        if result:
            return result.contents.name.decode("utf-8")
        else:
            eg.PrintError("Error by", "espeak_GetCurrentVoice")
        
        

class Text(eg.ActionBase):

    name = "Text"
    with open(os.path.join(os.path.dirname(__file__), "text.html"), "r") as file:
        description = file.read().decode("utf8")

    
    def __call__(self, text, flags=0, eval=False, sync=True):
        if self.plugin.is_off(): return
        if eval:
            text = eg.ParseString(text)
        if not text:
            return
        #pText = c_char_p(text.encode("utf-8"))
        pText = create_string_buffer(text.encode("utf-8"))
        result = self.plugin.espeak_Synth(pText, sizeof(pText), 0, 0, 0, espeakCHARS_UTF8 | flags, None, None)
        del pText
        if result != EE_OK:
            eg.PrintError("Error No.", result, "by", "espeak_Synth")
            return
        if sync:
            result = self.plugin.espeak_Synchronize()
            if result != EE_OK:
                eg.PrintError("Error No.", result, "by", "espeak_Synchronize")

            
    def Configure(self, text="", flags=0, eval=False, sync=True):
        panel = eg.ConfigPanel()
        textControl = panel.TextCtrl(text)
        evalControl = panel.CheckBox(eval, self.plugin.text.c21)
        ssmlControl = panel.CheckBox(flags & espeakSSML, self.plugin.text.c22)
        phonemesControl = panel.CheckBox(flags & espeakPHONEMES, self.plugin.text.c23)
        endpauseControl = panel.CheckBox(flags & espeakENDPAUSE, self.plugin.text.c24)
        syncControl = panel.CheckBox(sync, self.plugin.text.c25)
        panel.sizer.Add(textControl, 1, wx.EXPAND | wx.BOTTOM, 10)
        panel.AddCtrl(evalControl)
        panel.AddCtrl(ssmlControl)
        panel.AddCtrl(phonemesControl)
        panel.AddCtrl(endpauseControl)
        panel.AddCtrl(syncControl)
        while panel.Affirmed():
            panel.SetResult(
                textControl.GetValue(),
                (
                (espeakSSML if ssmlControl.GetValue() else 0) |
                (espeakPHONEMES if phonemesControl.GetValue() else 0) |
                (espeakENDPAUSE if endpauseControl.GetValue() else 0)
                ),
                evalControl.GetValue(),
                syncControl.GetValue(),
            )

            
            
class Cancel(eg.ActionBase):
    """
    Stop immediately synthesis and audio output of the current text. 
    When this function returns, the audio output is fully stopped 
    and the synthesizer is ready to synthesize a new message.
    """
    name = "Cancel"
    description = __doc__
    
    def __call__(self):
        if self.plugin.is_off(): return
        result = self.plugin.espeak_Cancel()
        if result != EE_OK:
            eg.PrintError("Error No.", result, "by", "espeak_Cancel")

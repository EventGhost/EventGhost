# -*- coding: utf-8 -*-
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
    name = "ffdshow",
    author = (
        "Bitmonster",
        "Bartman",
    ),
    version = "1.0.1454",
    kind = "program",
    guid = "{4CBEB5C8-97E2-4F65-A355-E72FCED4951F}",
    url = "http://www.eventghost.org/forum/viewtopic.php?t=613",
    description = (
        'Adds actions to control the '
        '<a href="http://ffdshow-tryout.sourceforge.net/">'
        'ffdshow DirectShow filter</a>.'
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADMElEQVR42nVSXUiTYRR+"
        "v+/bn6hbapqoTEf400R3YWmQ6E2gIoIk02Y3BZoadVEIGsxCZAkpSZB6YUiDdlFmNAzC"
        "QeDUFGXI7GcmBlEauh+dujnWtm/receMbjrwcF7Oe87zPue8hxkfHyccxxGlUkkYhiEy"
        "mYwcm9/vJy6XizgcDqJQKEhSUlI0TvN8Ph/Z2NggzNjYGCMQCEhRUVE5z/MyqVTKsywb"
        "AWk4FAqxu7u7n7e2tpjs7GxVcnIyUvhIYmJi+OjoiAXBHON0OoUIBt1u95fMzExlJBIh"
        "gUAgqspms5GBgQFTf3+/F3eXwuFwVAF9fXNzk/T09HgYyORQlLG/v/8eLytqa2s/HRwc"
        "mNPS0khKSkry9vb29Pz8/GO0caKtrW1nYWHhFZTQtmTp6elSZnFxkfZaXVZW9m5mZoYf"
        "HBx8X1xc/EQul7MNDQ3G5eXlczU1NWar1SrWarWvU1NTn2VlZQmGhoaM0XmAkROJRNqC"
        "goL7tO+9vT0uIyODzM7OksnJyZsoEkkkkkdCoTBweHgoosrMZjOZm/vwwOFw3mNQQCdt"
        "ycnJKTEYDL6VlRUuPj7+CNLDdru9Va/Xq9GKZnR0NDA9PR3EbwUwPMHq6uqNYDBgYND7"
        "FY/H04ciRWtr61OoGcRre83NzaH19XV3fX29XwxraWlxVVZWKjs7O8P5+fmMTqdz5ebm"
        "EWZpaclWWlqaBx/u6OiYgtyGpqYmUlhYSKCgWqPRvMBrcY2NjYb29vZrw8PDJCEhgajV"
        "akKHyfT29r2sqChXm0wmMjExcR3THe/u7hbX1dX5sTDdXq9Xh1nQu1sgHFGpVMK1tbXf"
        "+DEmagKBCHvEXeT5UHowGNRjsBEoIpg+wfeyVVVVGovFIh4ZGZlF+jcsFenq6mKRF12K"
        "6BYi8SouJWB9i7MSRIm42wZclBC/Q1fwLM6LAIsaC/wZQEkJ4nC4Cwyg+Db8RxAdoKgE"
        "5wIUihE3ImaFv4zYDrwbPhcwUQIRDg+BKVoA/ADkgAD4DpwHvlK1wC/AC9yJ5T+PtgC7"
        "AJwC3gCnAQlgp/JjvZ6MkRtjdzTnJyU7Jji2v8P5j3EA/2/gD9tgef0euQO8AAAAAElF"
        "TkSuQmCC"
    ),
)


from sys import maxint as MAX_INT
from ctypes import Structure, c_char_p, c_wchar_p, POINTER, cast, addressof
from eg.WinApi import FindWindow
from eg.WinApi.Dynamic import (
    RegisterWindowMessage,
    SendMessage,
    DWORD,
    PVOID,
    COPYDATASTRUCT,
    PCOPYDATASTRUCT,
    WM_COPYDATA,
)

FFDSHOW_REMOTE_MESSAGE = "ffdshow_remote_message"
FFDSHOW_REMOTE_CLASS = "ffdshow_remote_class"

WPRM_SETPARAM_ID = 0 # lParam - parameter id to be used by WPRM_PUTPARAM,
                     # WPRM_GETPARAM and COPY_PUTPARAMSTR
WPRM_PUTPARAM = 1    # lParam - new value of parameter, returns TRUE or FALSE
WPRM_GETPARAM = 2    # lParam - unused, return the value of parameter
WPRM_GETPARAM2 = 3   # lParam - parameter id
WPRM_STOP = 4
WPRM_RUN = 5
WPRM_GETSTATE = 6    # returns playback status
                     #  -1 - if not available
                     #   0 - stopped
                     #   1 - paused
                     #   2 - running
WPRM_GETDURATION = 7 # returns movie duration in seconds
WPRM_GETCURTIME = 8  # returns current position in seconds
WPRM_PREVPRESET = 11
WPRM_NEXTPRESET = 12
WPRM_SETCURTIME = 13 # Set current time in seconds

# WM_COPYDATA
# COPYDATASTRUCT.dwData=
COPY_PUTPARAMSTR = 9              # lpData points to new param value
COPY_SETACTIVEPRESET = 10         # lpData points to new preset name
COPY_AVAILABLESUBTITLE_FIRST = 11 # lpData points to buffer where first file
                                  # name will be stored  - if no subtitle file
                                  # is available, lpData will contain empty
                                  # string
COPY_AVAILABLESUBTITLE_NEXT = 12  # lpData points to buffer where next file
                                  # name will be stored  - if no subtitle file
                                  # is available, lpData will contain empty
                                  # string
COPY_GETPARAMSTR = 13             # lpData points to buffer where param value
                                  # will be stored
COPY_GET_PRESETLIST = 21          # Get the list of presets (array of strings)
COPY_GET_SOURCEFILE = 15          # Get the filename currently played


class WParamAction(eg.ActionClass):

    def __call__(self):
        return self.plugin.SendFfdshowMessage(self.value)



class GetIntAction(eg.ActionClass):

    def __call__(self):
        try:
            hwnd = FindWindow(FFDSHOW_REMOTE_CLASS, None)
        except:
            raise self.Exceptions.ProgramNotRunning

        return SendMessage(hwnd, self.plugin.mesg, WPRM_GETPARAM2, self.value)



class SetIntAction(eg.ActionClass):
    parameterDescription = "Set to:"

    def __call__(self, value=0):
        try:
            hwnd = FindWindow(FFDSHOW_REMOTE_CLASS, None)
        except:
            raise self.Exceptions.ProgramNotRunning

        SendMessage(hwnd, self.plugin.mesg, WPRM_SETPARAM_ID, self.value)
        SendMessage(hwnd, self.plugin.mesg, WPRM_PUTPARAM, value)


    def Configure(self, value=0):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(
            value,
            min = -MAX_INT - 1,
            max = MAX_INT,
        )
        panel.AddLine(self.parameterDescription, valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())



class ChangeIntAction(SetIntAction):
    parameterDescription = "Change by:"

    def __call__(self, value=0):
        try:
            hwnd = FindWindow(FFDSHOW_REMOTE_CLASS, None)
        except:
            raise self.Exceptions.ProgramNotRunning

        oldValue = SendMessage(hwnd, self.plugin.mesg, WPRM_GETPARAM2, self.value)
        newValue = oldValue + value
        SendMessage(hwnd, self.plugin.mesg, WPRM_SETPARAM_ID, self.value)
        SendMessage(hwnd, self.plugin.mesg, WPRM_PUTPARAM, newValue)
        return newValue


class ToggleAction(eg.ActionClass):

    def __call__(self, action):
        #0: disable, 1: enable, 2: toggle, 3: getStatus
        try:
            hwnd = FindWindow(FFDSHOW_REMOTE_CLASS, None)
        except:
            raise self.Exceptions.ProgramNotRunning

        if action == 0 or action == 1:
            SendMessage(hwnd, self.plugin.mesg, WPRM_SETPARAM_ID, self.value)
            SendMessage(hwnd, self.plugin.mesg, WPRM_PUTPARAM, action)
            return action

        oldValue = SendMessage(hwnd, self.plugin.mesg, WPRM_GETPARAM2, self.value)

        if action == 2:
            if oldValue:
                newValue = 0
            else:
                newValue = 1
            SendMessage(hwnd, self.plugin.mesg, WPRM_SETPARAM_ID, self.value)
            SendMessage(hwnd, self.plugin.mesg, WPRM_PUTPARAM, newValue)
            return newValue

        if action == 3:
            return oldValue


    def GetLabel(self, action):
        labels = (
            "Disable %s",
            "Enable %s",
            "Toggle %s",
            "Get Status of %s"
        )
        return labels[action] % self.name


    def Configure(self, action = 2):
        panel = eg.ConfigPanel(self)
        panel.AddLabel(self.description);

        radioButtons = (
            wx.RadioButton(panel, -1, "Disable", style = wx.RB_GROUP),
            wx.RadioButton(panel, -1, "Enable"),
            wx.RadioButton(panel, -1, "Toggle"),
            wx.RadioButton(panel, -1, "Get status")
        )

        radioButtons[action].SetValue(True)
        for rb in radioButtons:
            panel.AddCtrl(rb)

        while panel.Affirmed():
            for i in range(len(radioButtons)):
                if radioButtons[i].GetValue():
                    action = i
                    break
            panel.SetResult(action)


class IntegerAction(eg.ActionClass):
    #min, max, showSlider, scaleFactor
    options = (-MAX_INT - 1, MAX_INT, False, 1)
    def __call__(self, action, value):
        #0: set to, 1: change by, 2: get value
        try:
            hwnd = FindWindow(FFDSHOW_REMOTE_CLASS, None)
        except:
            raise self.Exceptions.ProgramNotRunning

        if action == 2:
            return SendMessage(hwnd, self.plugin.mesg, WPRM_GETPARAM2, self.value)

        if action == 1:
            value += SendMessage(hwnd, self.plugin.mesg, WPRM_GETPARAM2, self.value)

        value = max(self.options[0], value)
        value = min(self.options[1], value)

        SendMessage(hwnd, self.plugin.mesg, WPRM_SETPARAM_ID, self.value)
        SendMessage(hwnd, self.plugin.mesg, WPRM_PUTPARAM, value)
        return value


    def FormatValue(self, value):
        if self.options[3] == 1:
            return str(value)
        else:
            return "%.02f" % (value / float(self.options[3]))


    def GetLabel(self, action, value):
        labels = (
            "Set %s to %s",
            "Change %s by %s",
        )
        if action < 2:
            return labels[action] % (self.name, self.FormatValue(value))
        else:
            return "Get Value of %s" % self.name



    def Configure(self, action = 0, value = 0):
        """ this panel uses to controls
            one for setting and one for changing the value
            the right one is chosen depending on the value of the radiobuttons
        """

        def OnRadioButton(event):
            valueCtrl.Show(radioButtons[0].GetValue())
            valueCtrl2.Show(radioButtons[1].GetValue())
            if radioButtons[0].GetValue():
                self.tempValue = valueCtrl.GetValue()
            if radioButtons[1].GetValue():
                panel.Layout()
            panel.Layout()
            event.Skip()

        def OnSlider(event):
            val = event.GetEventObject().GetValue()
            if val != self.tempValue:
                panel.SetIsDirty()
            self.tempValue = val
            valueCtrl.SetValue(self.tempValue)
            valueCtrl2.SetValue(self.tempValue)
            event.Skip()

        def OnSpin(event):
            val = event.GetEventObject().GetValue()
            if val != self.tempValue:
                panel.SetIsDirty()
            self.tempValue = val
            valueCtrl.SetValue(self.tempValue)
            valueCtrl2.SetValue(self.tempValue)
            event.Skip()


        panel = eg.ConfigPanel(self)

        radioButtons = (
            wx.RadioButton(panel, -1, "Set to value", style = wx.RB_GROUP),
            wx.RadioButton(panel, -1, "Change by value"),
            wx.RadioButton(panel, -1, "Get current value")
        )

        radioButtons[action].SetValue(True)
        for rb in radioButtons:
            rb.Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
            panel.AddCtrl(rb)

        if self.options[2]:

            def LevelCallback(value):
                return self.FormatValue(value)

            self.tempValue = value

            valueCtrl = eg.Slider(
                panel,
                value = value,
                min = self.options[0],
                max = self.options[1],
                minLabel = self.FormatValue(self.options[0]),
                maxLabel = self.FormatValue(self.options[1]),
                style = wx.SL_TOP | wx.EXPAND,
                levelCallback=LevelCallback)

            bound = self.options[1] - self.options[0]
            valueCtrl2 = eg.Slider(
                panel,
                value = value,
                min = bound * -1,
                max = bound,
                minLabel = self.FormatValue(bound * -1),
                maxLabel = self.FormatValue(bound),
                style = wx.SL_TOP | wx.EXPAND,
                levelCallback=LevelCallback)

            valueCtrl.SetMinSize((300, -1))
            valueCtrl2.SetMinSize((300, -1))
            valueCtrl.Bind(wx.EVT_SCROLL, OnSlider)
            valueCtrl2.Bind(wx.EVT_SCROLL, OnSlider)

        else:
            fractionWidth = len(str(self.options[3])) - 1

            self.tempValue = value / float(self.options[3])
            minValue = self.options[0] / float(self.options[3])
            maxValue = self.options[1] / float(self.options[3])
            #integerWidth = max(len(str(int(minValue))), len(str(int(maxValue))))
            integerWidth = 11

            if minValue < 0:
                additionalWidth = 0
            else:
                additionalWidth = 1

            valueCtrl = eg.SpinNumCtrl(
                panel,
                -1,
                max(min(self.tempValue, maxValue), minValue),
                min = minValue,
                max = maxValue,
                fractionWidth = fractionWidth,
                integerWidth = integerWidth + additionalWidth)

            bound = (self.options[1] - self.options[0]) / float(self.options[3])
            minValue = bound * -1
            maxValue = bound

            if minValue < 0:
                additionalWidth = 0
            else:
                additionalWidth = 1

            valueCtrl2 = eg.SpinNumCtrl(
                panel,
                -1,
                max(min(self.tempValue, maxValue), minValue),
                min = minValue,
                max = maxValue,
                fractionWidth = fractionWidth,
                integerWidth = integerWidth + additionalWidth)

            valueCtrl.Bind(wx.EVT_TEXT, OnSpin)
            valueCtrl2.Bind(wx.EVT_TEXT, OnSpin)

        panel.AddCtrl(valueCtrl)
        panel.AddCtrl(valueCtrl2)

        OnRadioButton(wx.CommandEvent())

        while panel.Affirmed():
            if not self.options[2]:
                value = int(self.tempValue * float(self.options[3]))
            else:
                value = self.tempValue
            #print "Affirmed", value
            for i in range(len(radioButtons)):
                if radioButtons[i].GetValue():
                    action = i
                    break
                    panel = eg.ConfigPanel(self)
            panel.SetResult(action, value)


class SelectAction(eg.ActionClass):
    options = ()

    @classmethod
    def OnAddAction(cls):
        #rebuild the options sequence to quickly find entries
        #each entry is a tuple of (key, index, text, next, prev)
        newOptions = {}
        i = 0
        optionLength = len(cls.options)

        for key, text in cls.options:
            newOptions[key] = (
                key,
                i, #index
                text,
                cls.options[(i + 1) % optionLength][0], #next
                cls.options[(i - 1) % optionLength][0]) #prev
            i += 1

        cls.options = newOptions

    def __call__(self, action, value):
        #0: set to, 1: next, 2: previous 3: get value

        try:
            hwnd = FindWindow(FFDSHOW_REMOTE_CLASS, None)
        except:
            raise self.Exceptions.ProgramNotRunning

        if action == 3:
            return SendMessage(hwnd, self.plugin.mesg, WPRM_GETPARAM2, self.value)

        if action == 1 or action == 2:
            value = SendMessage(hwnd, self.plugin.mesg, WPRM_GETPARAM2, self.value)
            if self.options.has_key(value):
                entry = self.options[value]
                if action == 1:
                    value = entry[3]
                else:
                    value = entry[4]
            else:
                if action == 1:
                    value += 1
                else:
                    value -= 1


        SendMessage(hwnd, self.plugin.mesg, WPRM_SETPARAM_ID, self.value)
        SendMessage(hwnd, self.plugin.mesg, WPRM_PUTPARAM, value)
        return value


    def GetLabel(self, action, value):
        if action == 0:
            return "Set %s to %s" % (self.name, self.options[value][2])
        if action == 1:
            return "Set %s to next setting" % self.name
        if action == 2:
            return  "Set %s to previous setting" % self.name
        if action == 3:
            return "Get %s setting" % self.name
        return self.name

    def Configure(self, action = 0, value = MAX_INT):
        """ this panel uses to controls
            one for setting and one for changing the value
            the right one is chosen depending on the value of the radiobuttons
        """

        def OnRadioButton(event):
            choiceCtrl.Enable(radioButtons[0].GetValue())
            event.Skip()

        panel = eg.ConfigPanel(self)

        #radiobuttons
        radioButtons = (
            wx.RadioButton(panel, -1, "Set to value", style = wx.RB_GROUP),
            wx.RadioButton(panel, -1, "Next setting"),
            wx.RadioButton(panel, -1, "Previous setting"),
            wx.RadioButton(panel, -1, "Get current setting")
        )

        radioButtons[action].SetValue(True)
        for rb in radioButtons:
            rb.Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
            panel.AddCtrl(rb)

        #create control and add dummy entries
        choiceCtrl = wx.Choice(panel, -1)
        for i in range(len(self.options)):
            choiceCtrl.Append("")

        #set entries to real values
        for key, entry in self.options.iteritems():
            choiceCtrl.SetString(entry[1], entry[2])
            choiceCtrl.SetClientData(entry[1], entry[0])
            if entry[0] == value:
                choiceCtrl.Select(entry[1])
        if choiceCtrl.GetSelection() == wx.NOT_FOUND:
            choiceCtrl.Select(0)

        panel.AddCtrl(choiceCtrl)

        OnRadioButton(wx.CommandEvent())

        while panel.Affirmed():
            value = choiceCtrl.GetClientData(choiceCtrl.GetSelection())
            for i in range(len(radioButtons)):
                if radioButtons[i].GetValue():
                    action = i
                    break
            #print action, value
            panel.SetResult(action, value)


#Name, internalName, description, filterXXX, isXXX, showXXX, orderXXX, fullXXX, halfXXX
FILTERS = (
    ("Avisynth", "Avisynth", None, 1250, 1251, 1260, 1252, 1253, None),
    ("Bitmap overlay", "Bitmap", None, 1650, 1651, 1652, 1653, 1654, None),
    ("Blur & NR", "Blur", None, 900, 901, 936, 903, 905, None),
    ("Crop", "CropNzoom", None, 747, 712, 752, 754, 765, None),
    ("DCT", "DCT", None, 450, 451, 462, 452, 453, 463),
    ("DeBand", "GradFun", None, 1150, 1151, 1152, 1153, 1154, 1155),
    ("Deinterlacing", "Deinterlace", None, 1400, 1401, 1418, 1424, 1402 , None),
    ("DScaler filter", "DScaler", None, 2200, 2201, 2206, 2202, 2203, 2207),
    ("Grab", "Grab", None, 2000, 2001, 2013, 2002, 2003, None),
    ("Levels", "Levels", None, 1600, 1601, 1611, 1602, 1603, 1612),
    ("Logoaway", "Logoaway", None, 1450, 1451, 1452, 1453, 1454, None),
    ("Noise", "Noise", None, 500, 501, 512, 506, 507, 513),
    ("Offset & flip", "Offset", None, 1100, 1101, 1110, 1102, 1109, 1111),
    ("OSD", "OSD", "Actions to control ffdshow's OSD", None, 1501, None, None, None, None),
    ("Perspective correction", "Perspective", None, 2300, 2301, 2314, 2302, 2303, 2315),
    ("Picture properties", "PictProp", None, 200, 205, 217, 207, 213, 218),
    ("Postprocessing", "Postproc", None, 100, 106, 120, 109, 111, 121),
    ("Presets", "Presets", "Actions to control ffdshow presets", None, None, None, None, None, None),
    ("Resize & aspect", "Resize", None, 700, 701, 751, 722, 723, None),
    ("Sharpen", "Sharpen", None, 400, 401, 427, 407, 408, 428),
    ("Subtitles", "Subtitles", None, 800, 801, 828, 815, 817, None),
    ("Visualizations", "Vis", None, 1200, 1201, 1206, 1202, None, None),
    ("Warpsharp", "Warpsharp", None, 430, 431, 442, 432, 433, 443)
)

#aType, aGroup, aClsName, aName, aDescription, aValue, aOptions
CMDS = (
    (WParamAction, None, "Run", "Run", None, 5, None),
    (WParamAction, None, "Stop", "Stop", None, 4, None),

    #deprecated actions
    (GetIntAction, "deprecated", "GetSubtitleDelay", "Get Subtitle Delay", None, 812, None),
    (SetIntAction, "deprecated", "SetSubtitleDelay", "Set Subtitle Delay", None, 812, None),
    (ChangeIntAction, "deprecated", "ChangeSubtitleDelay", "Change Subtitle Delay", None, 812, None),

    #CropNzoom
    (IntegerAction, "CropNzoom", "CropNzoomMagnificationX", "Crop: Magnification X", None, 714, (0, 100, True, 1)),
    (IntegerAction, "CropNzoom", "CropNzoomMagnificationY", "Crop: Magnification Y", None, 720, (0, 100, True, 1)),
    (ToggleAction, "CropNzoom", "CropNzoomMagnificationLock", "Crop: Magnification Lock", None, 721, None),

    #DeBand
    (IntegerAction, "GradFun", "GradFunThreshold", "DeBand: Threshold", None, 1156, (101, 2000, True, 100)),

    #Deinterlacing
    (ToggleAction, "Deinterlace", "DeinterlaceSwapFields", "Deinterlacing: Swap fields", None, 1409, None),
    (SelectAction, "Deinterlace", "DeinterlaceMethod", "Deinterlacing: Method", None, 1403,
        ( (12, "Bypass"),
            (0, "Linear interpolation"),
            (1, "Linear blending"),
            (2, "Cubic interpolation"),
            (3, "Cubic blending"),
            (4, "Median"),
            (5, "TomsMoComp"),
            (6, "DGBob"),
            (7, "Framerate doubler"),
            (8, "ffmpeg deinterlacer"),
            (9, "DScaler plugin"),
            (10, "5-tap lowpass"),
            (11, "Kernel deinterlacer"),
            (13, "Kernel bob" ))),

    #Presets
    (WParamAction, "Presets", "PreviousPreset", "Previous Preset", None, 11, None),
    (WParamAction, "Presets", "NextPreset", "Next Preset", None, 12, None),

    #subtitle actions
    (IntegerAction, "Subtitles", "SubtitleDelay", "Subtitle: Delay", None, 812, None),

)



class Ffdshow(eg.PluginClass):

    def __init__(self):
        groups = {}
        for filterName, internalName, description, filterId, isId, showId, orderId, fullId, halfId in FILTERS:
            if not description:
                description = "Actions to control the %s filter within ffdshow" % filterName
            group = self.AddGroup(filterName, description)
            groups[internalName] = group

            #enable/disable filter
            if isId:
                class tmpAction(ToggleAction):
                    name = filterName + " filter"
                    description = "Sets or retrieves the status of the %s filter" % filterName
                    value = isId
                tmpAction.__name__ = internalName + "Toggle"
                group.AddAction(tmpAction)

            if showId:
                class tmpAction(ToggleAction):
                    name = filterName + " filter visibility"
                    description = "Sets or retrieves the visibility of the %s filter" % filterName
                    value = showId
                tmpAction.__name__ = internalName + "Visibility"
                group.AddAction(tmpAction)

            if fullId:
                class tmpAction(ToggleAction):
                    name = filterName + " filter \"Process whole image\" property"
                    description = "Sets or retrieves the \"Process whole image\" property of the %s filter" % filterName
                    value = fullId
                tmpAction.__name__ = internalName + "ProcessWholeImage"
                group.AddAction(tmpAction)

            if halfId:
                class tmpAction(ToggleAction):
                    name = filterName + " filter \"Only right half\" property"
                    description = "Sets or retrieves the \"Only right half\" property of the %s filter" % filterName
                    value = halfId
                tmpAction.__name__ = internalName + "ProcessRightHalf"
                group.AddAction(tmpAction)

            if orderId:
                class tmpAction(IntegerAction):
                    name = filterName + " order"
                    description = "Sets or retrieves the position of the %s filter" % filterName
                    value = orderId
                tmpAction.__name__ = internalName + "Order"
                group.AddAction(tmpAction)


        #add commands
        for aType, aGroup, aClsName, aName, aDescription, aValue, aOptions in CMDS:
            class tmpAction(aType):
                name = aName
                description = aDescription
                value = aValue
                if aOptions:
                    options = aOptions
            tmpAction.__name__ = aClsName
            if not aGroup:
                self.AddAction(tmpAction)
            else:
                if aGroup == "deprecated":
                    self.AddAction(tmpAction, hidden = True)
                else:
                    group = groups[aGroup]
                    group.AddAction(tmpAction)

        group = groups["Presets"]
        group.AddAction(GetPresets)
        group.AddAction(SetPreset)


    def __start__(self):
        self.mesg = RegisterWindowMessage(FFDSHOW_REMOTE_MESSAGE)
        eg.messageReceiver.AddHandler(WM_COPYDATA, self.Handler)


    @eg.LogIt
    def Handler(self, hwnd, mesg, wParam, lParam):
        cdsPointer = cast(lParam, PCOPYDATASTRUCT)
        print cast(cdsPointer.contents.lpData, c_char_p).value
        return True


    def SendFfdshowMessage(self, wParam, lParam=0):
        try:
            hwnd = FindWindow(FFDSHOW_REMOTE_CLASS, None)
        except:
            raise self.Exceptions.ProgramNotRunning

        return SendMessage(hwnd, self.mesg, wParam, lParam)



class SetPreset(eg.ActionWithStringParameter):
    class text:
        name = "Set Preset"
        parameterDescription = "Preset Name:"

    def __call__(self, preset):
        try:
            hwnd = FindWindow(FFDSHOW_REMOTE_CLASS, None)
        except:
            raise self.Exceptions.ProgramNotRunning

        cds = COPYDATASTRUCT()
        cds.dwData = COPY_SETACTIVEPRESET
        cds.lpData = cast(c_wchar_p(preset), PVOID)
        cds.cbData = (len(preset) + 1)*2
        return SendMessage(hwnd, WM_COPYDATA, eg.messageReceiver.hwnd, addressof(cds))



class GetPresets(eg.ActionClass):
    name = "Get Presets"

    def __call__(self):
        try:
            hwnd = FindWindow(FFDSHOW_REMOTE_CLASS, None)
        except:
            raise self.Exceptions.ProgramNotRunning

        cds = COPYDATASTRUCT()
        cds.dwData = COPY_GET_PRESETLIST
        SendMessage(hwnd, WM_COPYDATA, eg.messageReceiver.hwnd, addressof(cds))
        return cds

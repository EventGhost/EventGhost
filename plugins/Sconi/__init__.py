import eg

class PluginInfo(eg.PluginInfo):
    name = "Sconi"
    author = "Bartman"
    version = "0.0.1"
    kind = "remote"
    description = (
        'Hardware plugin for Sconi V2, Power-Sconi and Ultra-Sconi transceivers.'
        '\n\n'
        '<p><img src="sconi.jpg" alt="Ultra-Sconi" /><//p>'
    )
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAA7DAAAOwwHH"
        "b6hkAAACTElEQVR4XpWTX0hTYRjGn7Ozptux5lo6R1lM2uy2bSKtuu9ithSDQKqxwBu9"
        "6a4RBRUlRdtKoWiVglTQPy+qi4i6DeoyaOUSxHSSB3RtKdOz7Xyd76XjGrmLHvjOe/Hx"
        "/nh4nvMJqlpmifg1eDztCHZ1C/hfMcaQycyy/v4I41MD0oxdH2IPH4yzoqIwTah1DAAw"
        "N/sdU9+mMDgwiMjJEwiHw3jydALDIyO4eOE85ufnGGqIALK8gGJJxYwG+pRKIZ/PQxSN"
        "MJnq8ObtOwJ//PCe1QRYt1ixzW6HQTBgk9EIXeVymSALsoxoNIrnzx6zDQGOlhY0Ndth"
        "Mpm0JfXPcokfgoiiSA7jiZu4m7zN/gE4ndvhaGqGzWaDylQOqQIVCgUoyhq47o+OVUP0"
        "NHniR3t7WCCwj3l9e5nf76PZd6yX2kjeuUX3nZ0ddPfyxQS1I/APV3oyxWLxGKanZ7C4"
        "tARdl04P4KDLCa5UbhVXk+MUdn1dPcZG72E9sbY2N9o9bmQyPyBZJOTyOXA9evUaCB7C"
        "5h0uyCu/AIDCXl5ZxtDlK7oDElU1fCMBeTGLbPYnlKICh1EEaasdq6trPAteMWVDMMbU"
        "dYLX2wGv3wcum60RurKCyP8NvVZqRbKYsdu1q+KAgwTBIPAsuLUv6bRWXUm3TBVLkgWN"
        "VisksxlcwcNdVCP+duH27EHgwH59kefB3VDFDVIDLbfubEXkVAShUE+lRv6INOmPi+rr"
        "PhKi6sLH+9i5s2eozsmvn6se2EYAOlrP1L02aan6vrLzG4XuhneS8meyAAAAAElFTkSu"
        "QmCC"
    )

import time
import binascii
import ctypes
import sys
import threading
import win32con
import win32event
import win32file
import wx


class Text:
    descriptionRF = "Transmits an RF code via the Sconi hardware. Power- and Ultra-Sconi only."
    on = "On"
    off = "Off"
    repeat = "Repeat"
    systemCode = "Systemcode"
    switch = "Switch"
    repeatLabel = '%.2f sec'

    class TransmitRFInterTechno:
        name = "Transmit RF: InterTechno"
        actionLabel = 'Send InterTechno RF Signal: Switch %s-%d %s'
        
    class TransmitRFMicroElectric:
        name = "Transmit RF: Micro Electric"
        actionLabel = 'Send Micro Electric RF Signal: Switch %s %s'
        dipSetting = "Dip Setting"

    class TransmitRFConrad:
        name = "Transmit RF: Conrad"
        actionLabel = 'Send Conrad RF Signal: Switch %s %s'
        
    class TransmitRFIkea:
        name = "Transmit RF: IKEA"
        system = "System"
        level = "Level"
        channel = "Channel 1-10"
        gradual = "Gradual Change"
        actionLabel = 'Send IKEA RF Signal: System %d to %s %%'
        actionLabelOn = 'Send IKEA RF Signal: System %d on'
        actionLabelOff = 'Send IKEA RF Signal: System %d off'


class RFOnOffRepeat(wx.GridBagSizer):
    """sizer subclass to provice common elements within an sizer"""
    text = Text
    
    def __init__(self, parent, rows, state, repeat, repeatTime):
        text = Text
        wx.GridBagSizer.__init__(self, 5, 5)
        
        #on/off radio buttons
        self.rbOn = wx.RadioButton(parent, -1, text.on, style = wx.RB_GROUP)
        self.rbOff = wx.RadioButton(parent, -1, text.off)
        bs = wx.BoxSizer(wx.HORIZONTAL)
        bs.Add(self.rbOn)
        bs.Add(self.rbOff)
        self.Add(bs, (rows, 0), (1, 1), flag = wx.ALIGN_CENTER_VERTICAL);
        self.rbOn.SetValue(state)
        self.rbOff.SetValue(not state)
        
        #repeat checkbox
        self.repeat = wx.CheckBox(parent, -1, text.repeat)
        self.repeat.SetValue(repeat)
        self.Add(self.repeat, (rows + 1, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        
        #repeat slider
        self.slider = wx.Slider(
            parent,
            -1,
            value = int(repeatTime * 100),
            minValue = 70,
            maxValue= 500)
        self.Add(self.slider, (rows + 1, 1))
        self.repeatLabelCtrl = wx.StaticText(parent, -1, text.repeatLabel % 0)
        self.Add(
            self.repeatLabelCtrl,
            (rows + 1, 2),
            flag = wx.ALIGN_CENTER_VERTICAL
        )
        
        #event bindings
        self.slider.Bind(wx.EVT_SCROLL, self.OnScrollChanged)
        self.repeat.Bind(wx.EVT_CHECKBOX, self.OnCheckBoxChanged)
        
        #init enable status and labels
        self.OnCheckBoxChanged()
        self.OnScrollChanged()
        
    def OnCheckBoxChanged(self, event=None):
        self.slider.Enable(self.repeat.GetValue())
        self.repeatLabelCtrl.Enable(self.repeat.GetValue())

    def OnScrollChanged(self, event=None):
        self.repeatLabelCtrl.SetLabel(
            self.text.repeatLabel % \
                (self.slider.GetValue() / 100.0)
        )
        
    def GetResult(self):
        return(
            self.rbOn.GetValue(),
            self.repeat.GetValue(),
            (self.slider.GetValue() / 100.0)
        )
        


class TransmitRFInterTechno(eg.ActionClass):
    """ActionClass to send InterTechno RF signals"""
    description = Text.descriptionRF
    systemCodes = ("A", "B", "C", "D", "E", "F", "G", "H", "I",
        "J", "K", "L", "M", "N", "O", "P")

    def __call__(self, systemCode1, systemCode2, state, repeat, repeatTime):
        print "call TransmitRFInterTechno"
        
        
    def GetLabel(self, systemCode1, systemCode2, state, repeat, repeatTime):
        systemCodeStr = self.systemCodes[systemCode1]
        if state:
            stateStr = self.plugin.text.on
        else:
            stateStr = self.plugin.text.off
            
        return self.text.actionLabel % (systemCodeStr, systemCode2, stateStr.lower())
    
    
    def Configure(self, systemCode1 = 0, systemCode2 = 1, state = True, repeat = False, repeatTime = 2.0):
        text = Text
        dialog = eg.ConfigurationDialog(self)
        
        #create sizer with on/off and repeat controls
        ctrl = RFOnOffRepeat(dialog, 1, state, repeat, repeatTime)
        dialog.sizer.Add(ctrl)
        
        #systemcode
        systemCodeLabelCtrl = wx.StaticText(dialog, -1, text.systemCode)
        ctrl.Add(systemCodeLabelCtrl, (0, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        bs = wx.BoxSizer(wx.HORIZONTAL)
        
        #first choiceCtrl
        systemCodeCtrl1 = wx.Choice(dialog, -1, choices = self.systemCodes)
        systemCodeCtrl1.SetSelection(systemCode1)
        
        #second choiceCtrl
        systemCodes2 = []
        for i in range(1, 16):
            systemCodes2.append(str(i))
        systemCodeCtrl2 = wx.Choice(dialog, -1, choices = systemCodes2)
        systemCodeCtrl2.SetSelection(systemCode2 - 1)

        #add to sizers
        bs.Add(systemCodeCtrl1)
        bs.Add(wx.StaticText(dialog, -1, " - "), flag = wx.ALIGN_CENTER_VERTICAL)
        bs.Add(systemCodeCtrl2)
        ctrl.Add(bs, (0, 1))
        
        if dialog.AffirmedShowModal():
            state, repeat, repeatTime = ctrl.GetResult()
            return(
                systemCodeCtrl1.GetSelection(),
                systemCodeCtrl2.GetSelection() + 1,
                state,
                repeat,
                repeatTime
            )


class TransmitRFMicroElectric(eg.ActionClass):
    """ActionClass to send Micro Electric RF signals"""
    description = Text.descriptionRF
    switches = ("A", "B", "C", "D")

    def __call__(self, dipSetting, switch, state, repeat, repeatTime):
        print "call TransmitRFMicroElectric"
        
        
    def GetLabel(self, dipSetting, switch, state, repeat, repeatTime):
        switchStr = self.switches[switch]
        if state:
            stateStr = self.plugin.text.on
        else:
            stateStr = self.plugin.text.off
            
        return self.text.actionLabel % (switchStr, stateStr.lower())
    
    
    def Configure(self,
        dipSetting = (True, True, True, True, True, True),
        switch = 0,
        state = True,
        repeat = False,
        repeatTime = 2.0
    ):
        text = Text
        dialog = eg.ConfigurationDialog(self)
        
        #create sizer with on/off and repeat controls
        ctrl = RFOnOffRepeat(dialog, 1, state, repeat, repeatTime)
        dialog.sizer.Add(ctrl)
        
        #dip setting
        dipSettingLabelCtrl = wx.StaticText(dialog, -1, self.text.dipSetting)
        ctrl.Add(dipSettingLabelCtrl, (0, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        
        bs = wx.BoxSizer(wx.HORIZONTAL)
        dipSettingCtrls = range(0, 6)
        for i in range(0, 6):
            tmpSizer = wx.BoxSizer(wx.VERTICAL)
            rb = range(0, 2)
            rb[0] = wx.RadioButton(dialog, -1, style = wx.RB_GROUP)
            rb[0].SetValue(dipSetting[i])
            tmpSizer.Add(rb[0])
            dipSettingCtrls[i] = rb[0]
            
            rb[1] = wx.RadioButton(dialog, -1)
            rb[1].SetValue(not dipSetting[i])
            tmpSizer.Add(rb[1])

            bs.Add(tmpSizer)
        
        ctrl.Add(bs, (0, 1))
        
        #switch
        switchLabelCtrl = wx.StaticText(dialog, -1, text.switch)
        switchCtrl = wx.Choice(dialog, -1, choices = self.switches)
        switchCtrl.SetSelection(switch)
        ctrl.Add(switchLabelCtrl, (0, 2), flag = wx.ALIGN_CENTER_VERTICAL)
        ctrl.Add(switchCtrl, (0, 3), flag = wx.ALIGN_CENTER_VERTICAL)
        
        if dialog.AffirmedShowModal():
            state, repeat, repeatTime = ctrl.GetResult()
            return(
                (
                    dipSettingCtrls[0].GetValue(),
                    dipSettingCtrls[1].GetValue(),
                    dipSettingCtrls[2].GetValue(),
                    dipSettingCtrls[3].GetValue(),
                    dipSettingCtrls[4].GetValue(),
                    dipSettingCtrls[5].GetValue()
                ),
                switchCtrl.GetSelection(),
                state,
                repeat,
                repeatTime
            )


class TransmitRFConrad(eg.ActionClass):
    """ActionClass to send Conrad RF signals"""
    description = Text.descriptionRF
    systemCodes = ("1-1-1-1", "2-4-3-1", "3-2-3-4", "4-2-1-2", "1-1-4-3")
    switches = ("Master", "1", "2", "3", "4")

    def __call__(self, systemCode, switch, state, repeat, repeatTime):
        print "call TransmitRFConrad"
        
        
    def GetLabel(self, systemCode, switch, state, repeat, repeatTime):
        switchStr = self.switches[switch]
        if state:
            stateStr = self.plugin.text.on
        else:
            stateStr = self.plugin.text.off
            
        return self.text.actionLabel % (switchStr, stateStr.lower())
    
    
    def Configure(self, systemCode = 0, switch = 0, state = True, repeat = False, repeatTime = 2.0):
        text = Text
        dialog = eg.ConfigurationDialog(self)
        
        #create sizer with on/off and repeat controls
        ctrl = RFOnOffRepeat(dialog, 2, state, repeat, repeatTime)
        dialog.sizer.Add(ctrl)
        
        #systemcode
        systemCodeLabelCtrl = wx.StaticText(dialog, -1, text.systemCode)
        systemCodeCtrl = wx.Choice(dialog, -1, choices = self.systemCodes)
        systemCodeCtrl.SetSelection(systemCode)
        ctrl.Add(systemCodeLabelCtrl, (0, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        ctrl.Add(systemCodeCtrl, (0, 1))
        
        #switch
        switchLabelCtrl = wx.StaticText(dialog, -1, text.switch)
        switchCtrl = wx.Choice(dialog, -1, choices = self.switches)
        switchCtrl.SetSelection(switch)
        ctrl.Add(switchLabelCtrl, (1, 0), flag = wx.ALIGN_CENTER_VERTICAL)
        ctrl.Add(switchCtrl, (1, 1))
        
        if dialog.AffirmedShowModal():
            state, repeat, repeatTime = ctrl.GetResult()
            return(
                systemCodeCtrl.GetSelection(),
                switchCtrl.GetSelection(),
                state,
                repeat,
                repeatTime
            )


class TransmitRFIkea(eg.ActionClass):
    """ActionClass to send IKEA Koppla RF signals"""
    description = Text.descriptionRF

    def __call__(self, system, channels, level, gradual):
        print "call TransmitRFIkea"
        
        
    def GetLabel(self, system, channels, level, gradual):
        if level == 0:
            return self.text.actionLabelOff % system
        elif level == 10:
            return self.text.actionLabelOn % system
        else:
            return self.text.actionLabel % (system, level * 10)
    
    
    def Configure(self,
        system = 1,
        channels = (False, False, False, False, False, False, False, False, False, False),
        level = 10,
        gradual = True
    ):
        text = Text
        dialog = eg.ConfigurationDialog(self)
        
        #create sizer
        sizer = wx.FlexGridSizer(2, 3, 10, 10)
        dialog.sizer.Add(sizer)
        
        #system
        systemLabelCtrl = wx.StaticText(dialog, -1, self.text.system)
        sizer.Add(systemLabelCtrl, flag = wx.ALIGN_CENTER_VERTICAL)
        systemSeq = []
        for i in range(1, 16):
            systemSeq.append(str(i))
        systemCtrl = wx.Choice(dialog, -1, choices = systemSeq)
        systemCtrl.SetSelection(system - 1)
        sizer.Add(systemCtrl, flag = wx.ALIGN_CENTER_VERTICAL)

        #channels
        channelSizer = wx.BoxSizer(wx.VERTICAL)
        channelSizer.Add(wx.StaticText(dialog, -1, self.text.channel))
        channelSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        channelSizer.Add(channelSizer2)
        
        checkboxes = []
        for i in range(10):
            cb = wx.CheckBox(dialog)
            cb.SetValue(channels[i])
            channelSizer2.Add(cb)
            checkboxes.append(cb)
        
        sizer.Add(channelSizer)
        
        #levels
        levelLabelCtrl = wx.StaticText(dialog, -1, self.text.level)
        sizer.Add(levelLabelCtrl, flag = wx.ALIGN_CENTER_VERTICAL)
        levelSeq = []
        levelSeq.append(text.off)
        for i in range(1, 10):
            levelSeq.append(str(i * 10) + " %")
        levelSeq.append(text.on)
        levelCtrl = wx.Choice(dialog, -1, choices = levelSeq)
        levelCtrl.SetSelection(level)
        sizer.Add(levelCtrl, flag = wx.ALIGN_CENTER_VERTICAL)
        
        #gradual change
        gradualCtrl = wx.CheckBox(dialog, -1, self.text.gradual)
        gradualCtrl.SetValue(gradual)
        sizer.Add(gradualCtrl, flag = wx.ALIGN_CENTER_VERTICAL)

        
        if dialog.AffirmedShowModal():
            return(
                systemCtrl.GetSelection() + 1,
                (checkboxes[0].GetValue(),
                    checkboxes[1].GetValue(),
                    checkboxes[2].GetValue(),
                    checkboxes[3].GetValue(),
                    checkboxes[4].GetValue(),
                    checkboxes[5].GetValue(),
                    checkboxes[6].GetValue(),
                    checkboxes[7].GetValue(),
                    checkboxes[8].GetValue(),
                    checkboxes[9].GetValue()
                ),
                levelCtrl.GetSelection(),
                gradualCtrl.GetValue()
            )


class Sconi(eg.PluginClass):
    """Main Plugin class for the Sconi EG plugin"""
    canMultiLoad = False
    text = Text
    
    def __init__(self):
        self.AddAction(TransmitRFInterTechno)
        self.AddAction(TransmitRFMicroElectric)
        self.AddAction(TransmitRFConrad)
        self.AddAction(TransmitRFIkea)
        

    def __start__(self,
        *args
    ):
        print "Sconi: start"

    def __stop__(self):
        print "Sconi: stop"


    def Configure(self,
        *args
    ):
        dialog = eg.ConfigurationDialog(self)
        if dialog.AffirmedShowModal():
            return (
                None,
            )


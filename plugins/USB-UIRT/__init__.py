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
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$

import eg

eg.RegisterPlugin(
    name = "USB-UIRT",
    author = "Jon Rhees",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    kind = "remote",
    description = (
        'Hardware plugin for the <a href="http://www.usbuirt.com/">'
        'USB-UIRT</a> transceiver.'
        '\n\n<p>'
        '<a href="http://www.usbuirt.com/"><p>'
        '<center><img src="picture.jpg" alt="USB-UIRT" /></a></center>'
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACbklEQVR42mXTa4hMYRzH"
        "8f9zzoxmsblMJrzYRHgj140XkiG1Vomd1OwoRVHKreSyRWSRvJHSZktKq0E7LvvCFG/k"
        "kh0ZG7UoS1q7G7vjuqsxu2vOeXyfzvPO1Odc5jzP//+cc35HicgQOrEaU3EMO5HAdlxC"
        "NRrQjgfoxyrUKTaDeIz1mIwdOIvX2IgPWIt7uIubuIK3OGIKfLeVTYGo7WoK5BFCM7Lo"
        "s5O/4g2WYY8poNFmloOxOIBGjMESHMZSTMd1dOOJbXRQ0aKpLLKQk62YhNm4jd04jzW2"
        "SNxOvIPLzOswY5QoFqH1CvsQu2yXcTiEEUzBSYTtyswtTLTjnirWP5cS78yoCnwROc35"
        "BA6LcPALpkGfL9LC/hyONgYPtV4NxWKD4UKhKyJSW63UzA6tM1x4jz+20zCqcMI+h+Xc"
        "3+YY3ceLLFa9iUQpPDAQieZyN44rdarS82r9oLOZnMMMxFhVN4Hxf4g83CdyplckyaBh"
        "cwteIR733WIxFM3n59tQmd9e+wodm40LPWw+8sAp9pImZfau8h1Ha8cp99fUuNFsNs2f"
        "2xjnsa9n/xmPTDJLIs9IVicRbGFpKap6NA8pKvkqOHHZpxm8xa5gnSmE+0jxOj4RyXZi"
        "m+Y4Za+55hZ8lM19E702qm+aE6x7v02eSWDDb5GLz0V+UuQWQdnAdd8kVVFNEzmP1+fy"
        "FSUJfSutF1UEUW22H800mlwzbWfRYKVIhsh6I3YFpVGRyFUSRpfkPC4wo8oNAlMM5oh5"
        "fn93sTDGKjKTIZZ1lSKjijh534jlK/JuosaxamVVSv7/NXGtJwiI5rt/QdoW/AOsdcg6"
        "Kwb6cgAAAABJRU5ErkJggg=="
    ),
)


import wx
import USB_UIRT as UUIRT


class Text:
    uuInfo = "USB-UIRT Info"
    uuProtocol = "Protocol Version: "
    uuFirmVersion = "Firmware Version: "
    uuFirmDate = "Firmware Date: "
    redIndicator = "Red Indicator LED Operation"
    blinkRx = "Blink when Receiving IR"
    blinkTx = "Blink when Transmitting IR"
    notFound = "<not found>"
    irReception = "IR Reception"
    legacyCodes = "Generate 'legacy' UIRT2-compatible events"
    stopCodes = "Pass short repeat codes as enduring events"
    
    class TransmitIR:
        name = "Transmit IR"
        description = "Transmits an IR code via the USB-UIRT hardware."
        irCode = "IR Code:"
        learnButton = "Learn an IR Code..."
        testButton = "Test Transmit IR Code"
        repeatCount = "Repeat Count:"
        infinite = "Infinite"
        wait1 = "Wait:"
        wait2 = "ms of IR inactivity before transmission"
        zone = "Zone:"
        zoneChoices = (
            "All", 
            "Ext. Jack R-Pin",
            "Ext. Jack L-Pin", 
            "Internal Emitter", 
        )
        class LearnDialog:
            title = "Learn IR Code"
            frequency = "Frequency"
            signalQuality = "Signal"
            progress = "Learn Progress"
            acceptBurstButton = "Accept Burst"
            forceRaw = "Force RAW-Mode learning"
            helpText = \
                "1. Aim remote directly at USB-UIRT\n"\
                "approximately 6 inches from USB-UIRT face.\n\n"\
                "2. PRESS and HOLD the desired button on\n"\
                "your remote until learning is complete..."


    
class USB_UIRT(eg.RawReceiverPlugin):
    text = Text
    
    def __init__(self):
        self.device = None
        eg.RawReceiverPlugin.__init__(self)
        self.enabled = False
        self.AddAction(TransmitIR)


    def __start__(
        self, 
        ledRX=True, 
        ledTX=True, 
        legacyRX=False, 
        repeatStopCodes=False
    ):
        try:
            self.device = UUIRT.USB_UIRT()
        except UUIRT.UUIRTError, msg:
            self.device = None
            raise eg.Exception(msg)
        self.device.SetReceiveCallback(self.ReceiveCallback)
        self.device.SetConfig(ledRX, ledTX, legacyRX, repeatStopCodes)
        self.enabled = True
        
        
    def __stop__(self):
        self.enabled = False
        if self.device:
            self.device.Close()
            self.device = None
        
        
    def ReceiveCallback(self, eventString):
        if self.enabled:
            self.TriggerEvent(eventString)
        
        
    def Configure(
        self, 
        ledRx=None, 
        ledTx=None, 
        legacyRx=None, 
        repeatStopCodes=False
    ):
        text = self.text
        if self.device:
            protocolVersion = self.device.protocolVersion
            firmwareVersion = self.device.firmwareVersion
            firmwareDate = self.device.firmwareDate.strftime("%x")
            ledRX, ledTX, legacyRX = self.device.GetConfig()
        else:
            protocolVersion = text.notFound
            firmwareVersion = text.notFound
            firmwareDate = text.notFound
            ledRX, ledTX, legacyRX = False, False, False
            
        dialog = eg.ConfigurationDialog(self)
        infoGroupSizer = wx.StaticBoxSizer(
            wx.StaticBox(dialog, -1, text.uuInfo), 
            wx.VERTICAL
        )
        infoSizer = wx.FlexGridSizer(3, 2)
        
        staticText = wx.StaticText(dialog, -1, text.uuProtocol)
        infoSizer.Add(staticText, 0, wx.EXPAND)
        staticText = wx.StaticText(dialog, -1, protocolVersion)
        infoSizer.Add(staticText, 0, wx.EXPAND)
        staticText = wx.StaticText(dialog, -1, text.uuFirmVersion)
        infoSizer.Add(staticText, 0, wx.EXPAND)
        staticText = wx.StaticText(dialog, -1, firmwareVersion)
        infoSizer.Add(staticText, 0, wx.EXPAND)
        staticText = wx.StaticText(dialog, -1, text.uuFirmDate)
        infoSizer.Add(staticText, 0, wx.EXPAND)
        staticText = wx.StaticText(dialog, -1, firmwareDate)
        infoSizer.Add(staticText, 0, wx.EXPAND)
        
        infoGroupSizer.Add(infoSizer, 0, wx.LEFT, 5)
        dialog.sizer.Add(infoGroupSizer, 0, wx.EXPAND)
        
        dialog.sizer.Add((15,15))

        ledGroupSizer = wx.StaticBoxSizer(
            wx.StaticBox(dialog, -1, text.redIndicator), 
            wx.VERTICAL
        )
        ledRxCheckBox = wx.CheckBox(dialog, -1, text.blinkRx)
        ledRxCheckBox.SetValue(ledRX)
        ledGroupSizer.Add(ledRxCheckBox, 0, wx.ALL, 10)
        ledTxCheckBox = wx.CheckBox(dialog, -1, text.blinkTx)
        ledTxCheckBox.SetValue(ledTX)
        ledGroupSizer.Add(ledTxCheckBox, 0, wx.ALL, 10)
        dialog.sizer.Add(ledGroupSizer, 0, wx.EXPAND)
        
        dialog.sizer.Add((15,15))
        receiveGroupSizer = wx.StaticBoxSizer(
            wx.StaticBox(dialog, -1, text.irReception), 
            wx.VERTICAL
        )
        legacyRxCheckBox = wx.CheckBox(dialog, -1, text.legacyCodes)
        legacyRxCheckBox.SetValue(legacyRX)
        stopCodesRxCheckBox = wx.CheckBox(dialog, -1, text.stopCodes)
        stopCodesRxCheckBox.SetValue(repeatStopCodes)
        receiveGroupSizer.Add(legacyRxCheckBox, 0, wx.ALL, 10)
        receiveGroupSizer.Add(stopCodesRxCheckBox, 0, wx.ALL, 10)
        dialog.sizer.Add(receiveGroupSizer, 0, wx.EXPAND)

        yield dialog
        yield (
            ledRxCheckBox.GetValue(),
            ledTxCheckBox.GetValue(),
            legacyRxCheckBox.GetValue(),
            stopCodesRxCheckBox.GetValue(),
        )



class TransmitIR(eg.ActionClass):
    repeatCount = 4
    inactivityWaitTime = 0
    
    def __call__(self, code='', repeatCount=4, inactivityWaitTime=0):
        self.plugin.device.TransmitIR(code, repeatCount, inactivityWaitTime)
        
        
    def GetLabel(self, code='', repeatCount=4, inactivityWaitTime=0):
        return self.name
    
    
    def Configure(self, code='', repeatCount=None, inactivityWaitTime=None):
        text = self.text
        dialog = eg.ConfigurationDialog(self)
        if repeatCount is None:
            repeatCount = self.repeatCount
        inactivityWaitTime = inactivityWaitTime or self.inactivityWaitTime
        if len(code) > 0:
            zone = 0
            if code[0] == "Z":
                zone = int(code[1])
                code = code[2:]
        else:
            zone = 0
        
        editCtrl = wx.TextCtrl(dialog, -1, code, style=wx.TE_MULTILINE)
        font = editCtrl.GetFont()
        font.SetFaceName("Courier New")
        editCtrl.SetFont(font)
        editCtrl.SetMinSize((-1, 100))
        
        st1 = wx.StaticText(dialog, -1, text.repeatCount)
        
        repeatCtrl = eg.SpinIntCtrl(dialog, -1, min=0, max=127)
        repeatCtrl.SetInitialSize((50,-1))
        
        infiniteCtrl = wx.CheckBox(dialog, -1, text.infinite)
        if repeatCount == 32767:
            repeatCtrl.SetValue(4)
            repeatCtrl.Enable(False)
            infiniteCtrl.SetValue(True)
        else:
            repeatCtrl.SetValue(repeatCount)
            
        def OnInfiniteCtrl(event):
            repeatCtrl.Enable(not infiniteCtrl.GetValue())
        infiniteCtrl.Bind(wx.EVT_CHECKBOX, OnInfiniteCtrl)
        
        st2 = wx.StaticText(dialog, -1, text.wait1)
        waitCtrl = eg.SpinIntCtrl(dialog, -1, inactivityWaitTime, 0, 500)
        waitCtrl.SetValue(inactivityWaitTime)
        waitCtrl.SetInitialSize((50,-1))
        st3 = wx.StaticText(dialog, -1, text.wait2)
        
        zoneCtrl = wx.Choice(dialog, -1, choices=text.zoneChoices)
        zoneCtrl.Select(zone)
                
        learnButton = wx.Button(dialog, -1, text.learnButton)  
        testButton = wx.Button(dialog, -1, text.testButton)
        if self.plugin.device is None:
            learnButton.Enable(False)
            testButton.Enable(False)
            
        st5 = wx.StaticText(dialog, -1, text.zone)
        
        dialog.sizer.Add(wx.StaticText(dialog, -1, text.irCode))
        dialog.sizer.Add(editCtrl, 1, wx.EXPAND)
        dialog.sizer.Add((5,5))

        stFlags = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT
        gridSizer = wx.GridBagSizer(5,5)
        gridSizer.Add(st1, (0,0), flag=stFlags)
        
        tmpSizer = wx.BoxSizer(wx.HORIZONTAL)
        tmpSizer.Add(repeatCtrl)
        tmpSizer.Add((5,5))
        tmpSizer.Add(infiniteCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(tmpSizer, (0,1))

        #gridSizer.Add(repeatCtrl, (0,1))
        #gridSizer.Add(infiniteCtrl, (0,2), flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
        gridSizer.Add(st2, (1,0), flag=stFlags)
        
        tmpSizer = wx.BoxSizer(wx.HORIZONTAL)
        tmpSizer.Add(waitCtrl)
        tmpSizer.Add((5,5))
        tmpSizer.Add(st3, 0, wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(tmpSizer, (1,1))
        
        gridSizer.Add(st5, (2,0), flag=stFlags)
        gridSizer.Add(zoneCtrl, (2,1))
        gridSizer.AddGrowableCol(4,1)
        gridSizer.Add(
            learnButton, 
            (0,5), 
            flag=wx.ALIGN_RIGHT|wx.EXPAND
        )
        gridSizer.Add(
            testButton, 
            (1,5), 
            flag=wx.ALIGN_RIGHT|wx.EXPAND
        )
        
        dialog.sizer.Add(gridSizer, 0, wx.EXPAND)
        
        def learnIR(event):
            learnDialog = IRLearnDialog(
                None, 
                self.plugin.device, 
                text.LearnDialog
            )
            learnDialog.ShowModal()
            if learnDialog.code:
                editCtrl.SetValue(learnDialog.code)
            learnDialog.Destroy()
        learnButton.Bind(wx.EVT_BUTTON, learnIR)
            
        def testIR(event):
            self.plugin.device.TransmitIR(*GetResult())
        testButton.Bind(wx.EVT_BUTTON, testIR)

        def GetResult():
            zone = zoneCtrl.GetSelection()
            if zone > 0:
                code = "Z" + str(zone) + editCtrl.GetValue()
            else:
                code = editCtrl.GetValue()
            if infiniteCtrl.GetValue():
                self.repeatCount = 32767
            else:
                self.repeatCount = repeatCtrl.GetValue()
            self.inactivityWaitTime = waitCtrl.GetValue()
            return (
                code,
                self.repeatCount, 
                self.inactivityWaitTime
            )
            
        yield dialog
        yield GetResult()


class IRLearnDialog(wx.Dialog):
    
    def __init__(self, parent, device, text):
        self.device = device
        self.device.SetRawMode(False)
        self.code = None
        wx.Dialog.__init__(
            self, 
            parent, 
            -1,
            text.title,
            style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER
        )
            
        staticText = wx.StaticText(self, -1, text.helpText)
        
        sb = wx.StaticBox(self, -1, text.progress)
        progressSizer = wx.StaticBoxSizer(sb, wx.VERTICAL)
        progressCtrl = wx.Gauge(self, -1, 100, size=(250, 25))
        self.progressCtrl = progressCtrl
        progressSizer.Add(progressCtrl, 0, wx.ALL|wx.EXPAND, 5)
        
        sb = wx.StaticBox(self, -1, text.signalQuality)
        sigQualitySizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        sigQualityCtrl = wx.Gauge(
            self, 
            -1, 
            100, 
            size=(25,100),
            style=wx.GA_VERTICAL|wx.GA_SMOOTH
        )
        self.sigQualityCtrl = sigQualityCtrl
        sigQualitySizer.Add(sigQualityCtrl, 0, wx.ALL|wx.EXPAND, 5)
        
        sb = wx.StaticBox(self, -1, text.frequency)
        carrierFreqSizer = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        carrierFreqCtrl = wx.StaticText(self, -1, "-", style=wx.ALIGN_CENTER)
        self.carrierFreqCtrl = carrierFreqCtrl
        carrierFreqSizer.Add(carrierFreqCtrl, 1, wx.EXPAND|wx.ALL, 5)
        
        forceRawCtrl = wx.CheckBox(self, -1, text.forceRaw)
        forceRawCtrl.Bind(wx.EVT_CHECKBOX, self.OnRawBox)
        self.forceRawCtrl = forceRawCtrl
        
        cancelButton = wx.Button(self, wx.ID_CANCEL, eg.text.General.cancel)
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        cancelButton.SetDefault()
        
        burstButton = wx.Button(self, wx.ID_CANCEL, text.acceptBurstButton)
        burstButton.Bind(wx.EVT_BUTTON, self.OnAcceptBurst)
        burstButton.Enable(False)
        self.burstButton = burstButton
        
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer.Add(staticText, 0, wx.EXPAND|wx.TOP, 5)
        leftSizer.Add((5,5), 1)
        leftSizer.Add(forceRawCtrl)
        
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add((15,15))
        rightSizer.Add(burstButton, 0, wx.EXPAND|wx.ALIGN_RIGHT)
        rightSizer.Add((5,5))
        rightSizer.Add(cancelButton, 0, wx.EXPAND|wx.ALIGN_RIGHT)
        rightSizer.Add((0,0), 1)
        rightSizer.Add(carrierFreqSizer, 0, wx.EXPAND)
                
        upperRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        upperRowSizer.Add(leftSizer, 1, wx.EXPAND)
        upperRowSizer.Add((5,5))
        upperRowSizer.Add(sigQualitySizer, 0, wx.EXPAND)
        upperRowSizer.Add((5,5))
        upperRowSizer.Add(rightSizer, 0, wx.EXPAND)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(upperRowSizer, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(progressSizer, 0, wx.EXPAND|wx.ALL, 5)
        
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.device.StartLearnIR(self.LearnCallback, self.OnLearnSuccess)


    def LearnCallback(self, progress, sigQuality, carrierFreq, userData):
        if progress > 0:
            self.burstButton.Enable(True)
        self.progressCtrl.SetValue(progress)     
        self.sigQualityCtrl.SetValue(sigQuality)
        self.carrierFreqCtrl.SetLabel(
            "%d.%03d kHz" % (carrierFreq / 1000, carrierFreq % 1000)
        )
        return 0
        
        
    def OnLearnSuccess(self, code):
        self.code = code
        self.Close()
        
        
    def OnRawBox(self, event):
        self.device.AbortLearnThreadWait()
        self.device.SetRawMode(self.forceRawCtrl.GetValue())
        self.burstButton.Enable(False)
        self.progressCtrl.SetValue(0)     
        self.sigQualityCtrl.SetValue(0)
        self.device.StartLearnIR(self.LearnCallback, self.OnLearnSuccess)
        
        
    def OnAcceptBurst(self, event):
        self.device.AcceptBurst()
    
    
    def OnClose(self, event):
        self.device.AbortLearnThread()
        event.Skip()
        
        
    def OnCancel(self, event):
        self.Close()
        
    
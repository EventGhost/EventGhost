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

"""<rst>
Hardware plugin for the `USB-UIRT <http://www.usbuirt.com/>`_ transceiver.

|

.. image:: picture.jpg
   :align: center
   :target: http://www.usbuirt.com/
"""

import eg

eg.RegisterPlugin(
    name = "USB-UIRT",
    author = "Bitmonster",
    version = "1.0",
    kind = "remote",
    hardwareId = "USB\\VID_0403&PID_F850",
    guid = "{36FD4F40-653C-4626-97CC-BE363C05F933}",
    canMultiLoad = True,
    description = __doc__,
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
from ctypes import (
    c_int, c_uint, c_ulong, byref, c_ubyte, c_char_p, c_void_p, POINTER,
    WINFUNCTYPE, Structure, GetLastError, create_string_buffer, WinDLL,
    string_at,
)
import datetime
import threading


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


INVALID_HANDLE_VALUE = -1
UINT32 = c_uint

class UUINFO(Structure):
    _fields_ = (
        ('fwVersion',   c_uint),
        ('protVersion', c_uint),
        ('fwDateDay',   c_ubyte),
        ('fwDateMonth', c_ubyte),
        ('fwDateYear',  c_ubyte),
    )
PUUINFO = POINTER(UUINFO)

UUIRTDRV_ERR_NO_DEVICE = 0x20000001
UUIRTDRV_ERR_NO_RESP = 0x20000002
UUIRTDRV_ERR_NO_DLL = 0x20000003
UUIRTDRV_ERR_VERSION = 0x20000004

UUIRTDRV_CFG_LEDRX = 0x0001
UUIRTDRV_CFG_LEDTX = 0x0002
UUIRTDRV_CFG_LEGACYRX = 0x0004

UUIRTDRV_IRFMT_UUIRT = 0x0000
UUIRTDRV_IRFMT_PRONTO = 0x0010

UUIRTDRV_IRFMT_LEARN_FORCERAW = 0x0100
UUIRTDRV_IRFMT_LEARN_FORCESTRUC    = 0x0200
UUIRTDRV_IRFMT_LEARN_FORCEFREQ = 0x0400
UUIRTDRV_IRFMT_LEARN_FREQDETECT    = 0x0800


UUCALLBACKPROC = WINFUNCTYPE(c_int, POINTER(c_ubyte), c_ulong, c_ulong)
LEARNCALLBACKPROC = WINFUNCTYPE(c_int, c_uint, c_uint, c_ulong, c_void_p)


class USB_UIRT(eg.IrDecoderPlugin):
    text = Text

    def __init__(self):
        eg.IrDecoderPlugin.__init__(self, 50.0)
        self.dll = None
        self.enabled = False
        self.AddAction(TransmitIR)


    def __close__(self):
        self.irDecoder.Close()


    def __start__(
        self,
        ledRX=True,
        ledTX=True,
        legacyRX=False,
        repeatStopCodes=False,
    ):
        self.args = (ledRX, ledTX, legacyRX, repeatStopCodes)
        self.codeFormat = UUIRTDRV_IRFMT_PRONTO
        try:
            dll = WinDLL('uuirtdrv')
        except:
            raise self.Exceptions.DriverNotFound
        puDrvVersion = c_uint(0)
        if not dll.UUIRTGetDrvInfo(byref(puDrvVersion)):
            raise self.Exception("Unable to retrieve uuirtdrv version!")
        if puDrvVersion.value != 0x0100:
            raise self.Exception("Invalid uuirtdrv version!")

        if self.info.evalName[-1].isdigit():
            self.deviceStr = "USB-UIRT-%s" % self.info.evalName[-1]
        else:
            self.deviceStr = "USB-UIRT"
        hDrvHandle = dll.UUIRTOpenEx(self.deviceStr, 0, 0, 0)
        if hDrvHandle == INVALID_HANDLE_VALUE:
            err = GetLastError()
            if err == UUIRTDRV_ERR_NO_DLL:
                raise self.Exceptions.DriverNotFound
            elif err == UUIRTDRV_ERR_NO_DEVICE:
                raise self.Exceptions.DeviceNotFound
            elif err == UUIRTDRV_ERR_NO_RESP:
                raise self.Exceptions.DeviceInitFailed
            else:
                raise self.Exceptions.DeviceInitFailed
        self.hDrvHandle = hDrvHandle

        puuInfo = UUINFO()
        if not dll.UUIRTGetUUIRTInfo(hDrvHandle, byref(puuInfo)):
            raise self.Exceptions.DeviceInitFailed
        self.firmwareVersion = "%d.%d" % (
            puuInfo.fwVersion >> 8,
            puuInfo.fwVersion & 0xFF
        )
        self.protocolVersion = "%d.%d" % (
            puuInfo.protVersion >> 8,
            puuInfo.protVersion & 0xFF
        )
        self.firmwareDate = datetime.date(
            puuInfo.fwDateYear+2000,
            puuInfo.fwDateMonth,
            puuInfo.fwDateDay
        )
        self.dll = dll
        self.receiveProc = UUCALLBACKPROC(self.ReceiveCallback)
        res = dll.UUIRTSetRawReceiveCallback(
            self.hDrvHandle,
            self.receiveProc,
            0
        )
        if not res:
            self.dll = None
            raise self.Exception("Error calling UUIRTSetRawReceiveCallback")

        self.SetConfig(ledRX, ledTX, legacyRX, repeatStopCodes)
        self.enabled = True
        eg.Bind("System.DeviceRemoved", self.OnDeviceRemoved)


    def __stop__(self):
        eg.Unbind("System.DeviceRemoved", self.OnDeviceRemoved)
        self.enabled = False
        dll = self.dll
        if dll:
            if not dll.UUIRTClose(self.hDrvHandle):
                raise self.Exception("Error calling UUIRTClose")

            # fix for USB-UIRT driver bug, See OnComputerSuspend for details.
            self.hDrvHandle = dll.UUIRTOpenEx(self.deviceStr, 0, 0, 0)
            # without the UUIRTSetUUIRTConfig call, the driver seems to need
            # much more time to close.
            self.SetConfig(*self.args)
            dll.UUIRTSetReceiveCallback(self.hDrvHandle, None, 0)
            dll.UUIRTClose(self.hDrvHandle)
            self.dll = None


    def OnComputerSuspend(self, suspendType):
        # The USB-UIRT driver seems to have a bug, that prevents the wake-up
        # from standby feature to work, if UUIRTSetRawReceiveCallback was used.
        # To workaround the problem, we re-open the device with
        # UUIRTSetReceiveCallback just before the system goes into standby and
        # later do the reverse once the system comes back from standby.
        dll = self.dll
        if dll is None:
            return
        dll.UUIRTClose(self.hDrvHandle)
        self.hDrvHandle = dll.UUIRTOpenEx(self.deviceStr, 0, 0, 0)
        dll.UUIRTSetReceiveCallback(self.hDrvHandle, None, 0)


    def OnComputerResume(self, suspendType):
        dll = self.dll
        if dll is None:
            return
        dll.UUIRTClose(self.hDrvHandle)
        self.hDrvHandle = dll.UUIRTOpenEx(self.deviceStr, 0, 0, 0)
        dll.UUIRTSetRawReceiveCallback(self.hDrvHandle, self.receiveProc, 0)
        self.SetConfig(*self.args)


    def OnDeviceRemoved(self, event):
        if event.payload[0].split("#")[1] == 'Vid_0403&Pid_f850':
            if self.dll:
                if not self.dll.UUIRTClose(self.hDrvHandle):
                    raise self.Exception("Error calling UUIRTClose")
                self.dll = None
            eg.Bind("System.DeviceAttached", self.OnDeviceAttached)


    def OnDeviceAttached(self, event):
        if event.payload[0].split("#")[1] == 'Vid_0403&Pid_f850':
            if self.enabled:
                self.__start__(*self.args)
            eg.Unbind("System.DeviceAttached", self.OnDeviceAttached)


    def SetConfig(self, ledRX, ledTX, legacyRX, repeatStopCodes=False):
        value = 0
        if ledRX:
            value |= UUIRTDRV_CFG_LEDRX
        if ledTX:
            value |= UUIRTDRV_CFG_LEDTX
        if legacyRX:
            value |= UUIRTDRV_CFG_LEGACYRX
        if repeatStopCodes:
            value |= 16
        if not self.dll.UUIRTSetUUIRTConfig(self.hDrvHandle, UINT32(value)):
            self.dll = None
            raise self.Exception("Error calling UUIRTSetUUIRTConfig")


    def ReceiveCallback(self, buf, length, userdata):
        # TODO: find a more efficient way to find the terminator
        data = []
        for i in range(2, 1024):
            value = buf[i]
            data.append(value)
            if value == 255:
                break
        self.irDecoder.Decode(data, len(data))
        return 0


    def Configure(
        self,
        ledRx=True,
        ledTx=True,
        legacyRx=None,
        repeatStopCodes=False,
    ):
        text = self.text
        if self.dll:
            protocolVersion = self.protocolVersion
            firmwareVersion = self.firmwareVersion
            firmwareDate = self.firmwareDate.strftime("%x")
        else:
            protocolVersion = text.notFound
            firmwareVersion = text.notFound
            firmwareDate = text.notFound

        panel = eg.ConfigPanel()
        ledRxCheckBox = panel.CheckBox(ledRx, text.blinkRx)
        ledTxCheckBox = panel.CheckBox(ledTx, text.blinkTx)
        legacyRxCheckBox = panel.CheckBox(legacyRx, text.legacyCodes)
        stopCodesRxCheckBox = panel.CheckBox(repeatStopCodes, text.stopCodes)

        infoGroupSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.uuInfo),
            wx.VERTICAL
        )
        infoSizer = wx.FlexGridSizer(3, 2)
        infoSizer.AddMany([
            (panel.StaticText(text.uuProtocol), 0, wx.EXPAND),
            (panel.StaticText(protocolVersion), 0, wx.EXPAND),
            (panel.StaticText(text.uuFirmVersion), 0, wx.EXPAND),
            (panel.StaticText(firmwareVersion), 0, wx.EXPAND),
            (panel.StaticText(text.uuFirmDate), 0, wx.EXPAND),
            (panel.StaticText(firmwareDate), 0, wx.EXPAND),
        ])
        infoGroupSizer.Add(infoSizer, 0, wx.LEFT, 5)
        panel.sizer.Add(infoGroupSizer, 0, wx.EXPAND)

        panel.sizer.Add((15, 15))

        ledGroupSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.redIndicator),
            wx.VERTICAL
        )
        ledGroupSizer.Add(ledRxCheckBox, 0, wx.ALL, 10)
        ledGroupSizer.Add(ledTxCheckBox, 0, wx.ALL, 10)
        panel.sizer.Add(ledGroupSizer, 0, wx.EXPAND)

        panel.sizer.Add((15, 15))
        receiveGroupSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.irReception),
            wx.VERTICAL
        )
        receiveGroupSizer.Add(legacyRxCheckBox, 0, wx.ALL, 10)
        receiveGroupSizer.Add(stopCodesRxCheckBox, 0, wx.ALL, 10)
        panel.sizer.Add(receiveGroupSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                ledRxCheckBox.GetValue(),
                ledTxCheckBox.GetValue(),
                legacyRxCheckBox.GetValue(),
                stopCodesRxCheckBox.GetValue(),
            )



class TransmitIR(eg.ActionClass):
    repeatCount = 4
    inactivityWaitTime = 0

    def __call__(self, code='', repeatCount=4, inactivityWaitTime=0):
        if not self.plugin.dll:
            raise self.Exceptions.DeviceNotReady
        if len(code) > 5:
            start = 0
            if code[0] == "Z":
                start = 2
            if code[start+3] == "R":
                codeFormat = UUIRTDRV_IRFMT_UUIRT
            elif code[start+4] == " ":
                codeFormat = UUIRTDRV_IRFMT_PRONTO
            else:
                codeFormat = UUIRTDRV_IRFMT_LEARN_FORCESTRUC
        else:
            repeatCount = 0
            codeFormat = UUIRTDRV_IRFMT_PRONTO
            code = ""
        if not self.plugin.dll.UUIRTTransmitIR(
            self.plugin.hDrvHandle,    # hHandle
            c_char_p(code),     # IRCode
            codeFormat,         # codeFormat
            repeatCount,        # repeatCount
            inactivityWaitTime, # inactivityWaitTime
            0,                  # hEvent
            0,                  # reserved1
            0                   # reserved2
        ):
            raise self.Exceptions.DeviceNotReady


    def GetLabel(self, code='', repeatCount=4, inactivityWaitTime=0):
        return self.name


    def Configure(self, code='', repeatCount=None, inactivityWaitTime=None):
        text = self.text
        panel = eg.ConfigPanel()
        if repeatCount is None:
            repeatCount = self.repeatCount
        if inactivityWaitTime is None:
            inactivityWaitTime = self.inactivityWaitTime
        if len(code) > 0:
            zone = 0
            if code[0] == "Z":
                zone = int(code[1])
                code = code[2:]
        else:
            zone = 0

        editCtrl = panel.TextCtrl(code, style=wx.TE_MULTILINE)
        font = editCtrl.GetFont()
        font.SetFaceName("Courier New")
        editCtrl.SetFont(font)
        editCtrl.SetMinSize((-1, 100))

        repeatCtrl = panel.SpinIntCtrl(value=repeatCount, min=1, max=127)
        repeatCtrl.SetInitialSize((50, -1))

        infiniteCtrl = wx.CheckBox(panel, -1, text.infinite)
        if repeatCount == 32767:
            repeatCtrl.SetValue(4)
            repeatCtrl.Enable(False)
            infiniteCtrl.SetValue(True)
        else:
            repeatCtrl.SetValue(repeatCount)

        def OnInfiniteCtrl(event):
            repeatCtrl.Enable(not infiniteCtrl.GetValue())
            event.Skip()
        infiniteCtrl.Bind(wx.EVT_CHECKBOX, OnInfiniteCtrl)

        waitCtrl = panel.SpinIntCtrl(inactivityWaitTime, 0, 500)
        waitCtrl.SetInitialSize((50, -1))

        zoneCtrl = panel.Choice(zone, text.zoneChoices)

        learnButton = panel.Button(text.learnButton)
        if self.plugin.dll is None:
            learnButton.Enable(False)

        panel.sizer.Add(panel.StaticText(text.irCode))
        panel.sizer.Add(editCtrl, 1, wx.EXPAND)
        panel.sizer.Add((5, 5))

        stFlags = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT
        gridSizer = wx.GridBagSizer(5, 5)
        gridSizer.Add(panel.StaticText(text.repeatCount), (0, 0), flag=stFlags)

        tmpSizer = wx.BoxSizer(wx.HORIZONTAL)
        tmpSizer.Add(repeatCtrl)
        tmpSizer.Add((5, 5))
        tmpSizer.Add(infiniteCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(tmpSizer, (0, 1))

        gridSizer.Add(panel.StaticText(text.wait1), (1, 0), flag=stFlags)

        tmpSizer = wx.BoxSizer(wx.HORIZONTAL)
        tmpSizer.Add(waitCtrl)
        tmpSizer.Add((5, 5))
        tmpSizer.Add(panel.StaticText(text.wait2), 0, wx.ALIGN_CENTER_VERTICAL)
        gridSizer.Add(tmpSizer, (1, 1))

        gridSizer.Add(panel.StaticText(text.zone), (2, 0), flag=stFlags)
        gridSizer.Add(zoneCtrl, (2, 1))
        gridSizer.Add(
            learnButton,
            (0,5),
            flag=wx.ALIGN_RIGHT|wx.EXPAND
        )
        gridSizer.AddGrowableCol(4, 1)

        panel.sizer.Add(gridSizer, 0, wx.EXPAND)

        def LearnIR(event):
            learnDialog = IRLearnDialog(
                None,
                self.plugin.dll,
                self.plugin.hDrvHandle,
                text.LearnDialog
            )
            learnDialog.ShowModal()
            if learnDialog.code:
                editCtrl.SetValue(learnDialog.code)
            learnDialog.AbortLearnThreadWait()
            learnDialog.Destroy()
        learnButton.Bind(wx.EVT_BUTTON, LearnIR)

        while panel.Affirmed():
            zone = zoneCtrl.GetValue()
            if zone > 0:
                code = "Z" + str(zone) + editCtrl.GetValue()
            else:
                code = editCtrl.GetValue()
            if infiniteCtrl.GetValue():
                self.__class__.repeatCount = 32767
            else:
                self.__class__.repeatCount = repeatCtrl.GetValue()
            self.__class__.inactivityWaitTime = waitCtrl.GetValue()
            panel.SetResult(
                code,
                self.repeatCount,
                self.inactivityWaitTime
            )



class IRLearnDialog(eg.Dialog):

    def __init__(self, parent, dll, hDrvHandle, text):
        self.dll = dll
        self.hDrvHandle = hDrvHandle
        self.code = None
        self.codeFormat = UUIRTDRV_IRFMT_PRONTO
        eg.Dialog.__init__(
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
            size=(25, 100),
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
        leftSizer.Add((5, 5), 1)
        leftSizer.Add(forceRawCtrl)

        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add((15, 15))
        rightSizer.Add(burstButton, 0, wx.EXPAND|wx.ALIGN_RIGHT)
        rightSizer.Add((5, 5))
        rightSizer.Add(cancelButton, 0, wx.EXPAND|wx.ALIGN_RIGHT)
        rightSizer.Add((0, 0), 1)
        rightSizer.Add(carrierFreqSizer, 0, wx.EXPAND)

        upperRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        upperRowSizer.Add(leftSizer, 1, wx.EXPAND)
        upperRowSizer.Add((5, 5))
        upperRowSizer.Add(sigQualitySizer, 0, wx.EXPAND)
        upperRowSizer.Add((5, 5))
        upperRowSizer.Add(rightSizer, 0, wx.EXPAND)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(upperRowSizer, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(progressSizer, 0, wx.EXPAND|wx.ALL, 5)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        sizer.Fit(self)
        self.SetMinSize(self.GetSize())
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.StartLearnIR()


    def SetRawMode(self, flag=True):
        if flag:
            self.codeFormat = UUIRTDRV_IRFMT_LEARN_FORCERAW
        else:
            self.codeFormat = UUIRTDRV_IRFMT_PRONTO


    def StartLearnIR(self):
        self.learnThreadAbortEvent = threading.Event()
        self.bAbortLearn = c_int(0)
        self.learnThread = threading.Thread(target=self.LearnThread)
        self.learnThread.start()


    def AbortLearnThread(self):
        self.bAbortLearn.value = True


    def AbortLearnThreadWait(self):
        self.bAbortLearn.value = True
        self.learnThreadAbortEvent.wait(10)


    def AcceptBurst(self):
        self.bAbortLearn.value = -1


    def LearnThread(self):
        learnBuffer = create_string_buffer('\000' * 2048)
        self.dll.UUIRTLearnIR(
            self.hDrvHandle,                       # hHandle
            self.codeFormat,                       # codeFormat
            learnBuffer,                           # IRCode buffer
            LEARNCALLBACKPROC(self.LearnCallback), # progressProc
            0x5a5a5a5a,                            # userData
            byref(self.bAbortLearn),               # *pAbort
            0,                                     # param1
            0,                                     # reserved0
            0                                      # reserved1
        )
        if self.bAbortLearn.value != 1:
            self.OnLearnSuccess(learnBuffer.value)
        self.learnThreadAbortEvent.set()


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
        self.AbortLearnThreadWait()
        self.SetRawMode(self.forceRawCtrl.GetValue())
        self.burstButton.Enable(False)
        self.progressCtrl.SetValue(0)
        self.sigQualityCtrl.SetValue(0)
        self.StartLearnIR()


    def OnAcceptBurst(self, event):
        self.AcceptBurst()


    def OnClose(self, event):
        self.AbortLearnThread()
        event.Skip()
        self.Destroy()


    def OnCancel(self, event):
        self.Close()


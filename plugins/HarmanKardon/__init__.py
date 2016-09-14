# -*- coding: utf-8 -*-
#
# This file is plugin for EventGhost.
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

# POWER ON      80 70 C0 3F
# POWER OFF     80 70 9F 60
# MUTE          80 70 C1 3E
# AVR           82 72 35 CA
# DVD           80 70 D0 2F
# CD            80 70 C4 3B
# TAPE          80 70 CC 33
# VID1          80 70 CA 35
# VID2          80 70 CB 34
# VID3          80 70 CE 31
# VID4          80 70 D1 2E
# VID5          80 70 F0 0F
# AM/FM         80 70 81 7E
# 6CH/8CH       82 72 DB 24
# SLEEP         80 70 DB 24
# SURR          82 72 58 A7
# DOLBY         82 72 50 AF
# DTS           82 72 A0 5F
# DTS NEO:6     82 72 A1 5E
# LOGIC7        82 72 A2 5D
# STEREO        82 72 9B 64
# TEST TONE     82 72 8C 73
# NIGHT         82 72 96 69
# 1             80 70 87 78
# 2             80 70 88 77
# 3             80 70 89 76
# 4             80 70 8A 75
# 5             80 70 8B 74
# 6             80 70 8C 73
# 7             80 70 8D 72
# 8             80 70 8E 71
# 9             80 70 9D 62
# 0             80 70 9E 61
# TUNE UP       80 70 84 7B
# TUNE DOWN     80 70 85 7A
# VOL UP        80 70 C7 38
# VOL DOWN      80 70 C8 37
# PRESET UP     82 72 D0 2F
# PRESET DOWN   82 72 D1 2E
# DIGITAL       82 72 54 AB
# DIGITAL UP    82 72 57 A8
# DIGITAL DOWN  82 72 56 A9
# FMMODE        80 70 93 6C
# DELAY         82 72 52 AD
# DELAY UP      82 72 8A 75
# DELAY DOWN    82 72 8B 74
# COM SET       82 72 84 7B
# COM UP        82 72 99 66
# COM DOWN      82 72 9A 65
# SPEAKER       82 72 53 AC
# SPEAKER UP    82 72 8E 71
# SPEAKER DOWN  82 72 8F 70
# CHANNEL       82 72 5D A2
# RDS           82 72 DD 22
# DIRECT        80 70 9B 64
# CLEAR         82 72 D9 26
# MEMORY        80 70 86 79
# MULTIROOM     82 72 DF 20
# MULTIROOM UP  82 72 5E A1
# MULTIROOM DN  82 72 5F A0
# OSD           82 72 5C A3
# OSD LEFT      82 72 C1 3E
# OSD RIGHT     82 72 C2 3D
# SURR UP       82 72 85 7A
# SURR DOWN     82 72 86 79
# PRESCAN       80 70 96 69
# DIMMER        80 70 DC 23
# FAROUDJA      82 72 C6 39
# TONE          82 72 C5 3A


eg.RegisterPlugin(
    name = "Harman Kardon Serial Control",
    author = (
        "Kingtd",
        "Bitmonster",
    ),
    version = "1.0.1093",
    description = "Allows control of a Harman Kardon AVR4xx/6xx series receiver through a serial port.",
    kind = "external",
    guid = "{460D31E6-231D-483D-8B9B-2781F9D2377A}",
    url = "http://www.eventghost.org/forum/viewtopic.php?t=447",
    canMultiLoad = True,
)

hktopmsg=""
hkbotmsg=""

class Text:
    port = "Port:"
    baudrate = "Baudrate:"
    bytesize = "Number of bits:"
    parity = "Parity:"
    parities = ['No parity', 'Odd', 'Even'] #, 'Mark', 'Space']
    stopbits = "Stopbits:"
    flowcontrol = "Flow control:"
    handshakes = ['None', 'Xon / Xoff', 'Hardware']
    generateEvents = "Generate events on incoming data"
    terminator = "Terminator:"
    eventPrefix = "Event prefix:"
    class send2hk:
        name = "Send to HK Receiver"


import threading
import win32event
import win32file

class HarmanKardon(eg.RawReceiverPlugin):

    text = Text

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.AddAction(self.Send2hk)
        self.serial = None
        self.buffer = ""


    def __start__(
        self,
        port,
        baudrate,
        bytesize=8,
        parity=0,
        stopbits=0,
        handshake=0,
        generateEvents=False,
        terminator="",
        prefix="HK",
    ):
        xonxoff = 0
        rtscts = 0
        if handshake == 1:
            xonxoff = 1
        elif handshake == 2:
            rtscts = 1

        try:
            self.serial = eg.SerialPort(
                port,
                baudrate=baudrate,
                bytesize=(5, 6, 7, 8)[bytesize],
                stopbits=(1, 2)[stopbits],
                parity=('N', 'O', 'E')[parity],
                xonxoff=xonxoff,
                rtscts=rtscts,
            )
        except:
            self.serial = None
            raise self.Exceptions.SerialOpenFailed
        self.serial.timeout = 1.0
        self.serial.setRTS()
        if generateEvents:
            self.terminator = eg.ParseString(terminator).decode('string_escape')
            self.info.eventPrefix = prefix
            self.stopEvent = win32event.CreateEvent(None, 1, 0, None)
            self.receiveThread = threading.Thread(target=self.ReceiveThread)
            self.receiveThread.start()
        else:
            self.receiveThread = None


    def __stop__(self):
        if self.serial is not None:
            if self.receiveThread:
                win32event.SetEvent(self.stopEvent)
                self.receiveThread.join(1.0)
            self.serial.close()
            self.serial = None


    def HandleChar(self, ch):

        global hktopmsg
        global hkbotmsg

        if ord(ch) != 186:
                self.buffer += ch
        self.terminator = chr(0)+chr(242)
        pos = self.buffer.find(self.terminator)
        if pos != -1:
            eventstring = self.buffer[:pos].strip()
            st2=eventstring.find(chr(50)+chr(240))
            st3=eventstring.find(chr(0)+chr(241))
            ev1 = eventstring[st2+2:st3].strip()
            ev2 = eventstring[st3+2:].strip()

            if ev1 != hktopmsg and ev1 != "":
                hktopmsg=ev1
                for i in range(0, len(ev1), 1):
                   if ord(ev1[i])>127:
                      ev1="Result Unprintable"
                self.TriggerEvent('Top.'+ev1)
            if ev2 != hkbotmsg and ev1 != "":
                hkbotmsg=ev2
                for i in range(0, len(ev2), 1):
                   if ord(ev2[i])>127:
                      ev2="Result Unprintable"
                self.TriggerEvent('Bottom.'+ev2)

            self.buffer = self.buffer[pos+len(self.terminator):]


    def ReceiveThread(self):
        from win32event import (
            ResetEvent,
            MsgWaitForMultipleObjects,
            QS_ALLINPUT,
            WAIT_OBJECT_0,
            WAIT_TIMEOUT,
        )
        from win32file import ReadFile, AllocateReadBuffer, GetOverlappedResult
        from win32api import GetLastError

        continueLoop = True
        overlapped = self.serial._overlappedRead
        hComPort = self.serial.hComPort
        hEvent = overlapped.hEvent
        stopEvent = self.stopEvent
        n = 1
        waitingOnRead = False
        buf = AllocateReadBuffer(n)
        while continueLoop:
            if not waitingOnRead:
                ResetEvent(hEvent)
                hr, _ = ReadFile(hComPort, buf, overlapped)
                if hr == 997:
                    waitingOnRead = True
                elif hr == 0:
                    pass
                    #n = GetOverlappedResult(hComPort, overlapped, 1)
                    #self.HandleChar(str(buf))
                else:
                    self.PrintError("error")
                    raise

            rc = MsgWaitForMultipleObjects(
                (hEvent, stopEvent),
                0,
                1000,
                QS_ALLINPUT
            )
            if rc == WAIT_OBJECT_0:
                n = GetOverlappedResult(hComPort, overlapped, 1)
                if n:
                    self.HandleChar(str(buf))
                #else:
                #    print "WAIT_OBJECT_0", n, str(buf[:n])
                waitingOnRead = False
            elif rc == WAIT_OBJECT_0+1:
                continueLoop = False
            elif rc == WAIT_TIMEOUT:
                pass
            else:
                self.PrintError("unknown message")


    def Configure(
        self,
        port=0,
        baudrate=9600,
        bytesize=8,
        parity=0,
        stopbits=0,
        handshake=0,
        generateEvents=False,
        terminator="\\r",
        prefix="HK",
    ):
        text = self.text
        oldevstring=" "
        panel = eg.ConfigPanel(self)
        portCtrl = eg.SerialPortChoice(panel, value=port)

        baudrateCtrl = wx.ComboBox(
            panel,
            value=str(baudrate),
            choices=[
                        '38400'
                    ],
            style=wx.CB_DROPDOWN,
            validator=eg.DigitOnlyValidator()
        )

        bytesizeCtrl = wx.Choice(panel, choices=['5', '6', '7', '8'])
        bytesizeCtrl.SetSelection(8 - 5)

        parityCtrl = wx.Choice(panel, choices=text.parities)
        parityCtrl.SetSelection(parity)

        stopbitsCtrl = wx.Choice(panel, choices=['1', '2'])
        stopbitsCtrl.SetSelection(stopbits)

        handshakeCtrl = wx.Choice(panel, choices=text.handshakes)
        handshakeCtrl.SetSelection(handshake)

        generateEventsCtrl = wx.CheckBox(panel, label=text.generateEvents)
        generateEventsCtrl.SetValue(generateEvents)

        terminatorCtrl = wx.TextCtrl(panel)
        terminatorCtrl.SetValue(terminator)
        terminatorCtrl.Enable(generateEvents)

        prefixCtrl = wx.TextCtrl(panel)
        prefixCtrl.SetValue(prefix)
        prefixCtrl.Enable(generateEvents)

        def OnCheckBox(event):
            flag = generateEventsCtrl.GetValue()
            terminatorCtrl.Enable(flag)
            prefixCtrl.Enable(flag)
        generateEventsCtrl.Bind(wx.EVT_CHECKBOX, OnCheckBox)

        flags = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL
        mySizer = wx.GridBagSizer(5, 5)
        Add = mySizer.Add
        Add(wx.StaticText(panel, -1, text.port), (0, 0), flag=flags)
        Add(portCtrl, (0, 1), flag=wx.EXPAND)
        Add(wx.StaticText(panel, -1, text.baudrate), (1, 0), flag=flags)
        Add(baudrateCtrl, (1, 1), flag=wx.EXPAND)
        Add(wx.StaticText(panel, -1, text.bytesize), (2, 0), flag=flags)
        Add(bytesizeCtrl, (2, 1), flag=wx.EXPAND)
        Add(wx.StaticText(panel, -1, text.parity), (3, 0), flag=flags)
        Add(parityCtrl, (3, 1), flag=wx.EXPAND)
        Add(wx.StaticText(panel, -1, text.stopbits), (4, 0), flag=flags)
        Add(stopbitsCtrl, (4, 1), flag=wx.EXPAND)
        Add(wx.StaticText(panel, -1, text.flowcontrol), (5, 0), flag=flags)
        Add(handshakeCtrl, (5, 1), flag=wx.EXPAND)

        Add((5, 5), (6, 0), (1, 2), flag=flags)
        Add(generateEventsCtrl, (7, 0), (1, 2), flag=flags)
        Add(wx.StaticText(panel, -1, text.terminator), (8, 0), flag=flags)
        Add(terminatorCtrl, (8, 1), flag=wx.EXPAND)
        Add(wx.StaticText(panel, -1, text.eventPrefix), (9, 0), flag=flags)
        Add(prefixCtrl, (9, 1), flag=wx.EXPAND)
        panel.sizer.Add(mySizer)

        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
                int(baudrateCtrl.GetValue()),
                bytesizeCtrl.GetSelection(),
                parityCtrl.GetSelection(),
                stopbitsCtrl.GetSelection(),
                handshakeCtrl.GetSelection(),
                generateEventsCtrl.GetValue(),
                terminatorCtrl.GetValue(),
                prefixCtrl.GetValue(),
            )



    class Send2hk(eg.ActionWithStringParameter):
        description = (
            "Sends a HK control command through the serial port."
        )

        def bxor (self, a, b):
            return a ^ b

        def ByteToHex(self, byteStr ):
            return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

        def HexToByte(self, hexStr ):
            bytes = []
            hexStr = ''.join( hexStr.split(" ") )
            for i in range(0, len(hexStr), 2):
                bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )
            return ''.join( bytes )

        def dec2hex(self, n):
            return "%X" % n

        def hex2dec(self, s):
            return int(s, 16)


        def __call__(self, data):

            hkcmd=self.HexToByte(data)
            csodd = 0
            cseven = 0
            for i in range (0, len(hkcmd), 2):
                csodd = self.bxor(csodd, ord(hkcmd[i]))
                cseven = self.bxor(cseven, ord(hkcmd[i+1]))
            csodd = self.HexToByte(self.dec2hex(csodd))
            cseven = self.HexToByte(self.dec2hex(cseven))
            hkcmd=self.HexToByte('50 43 53 45 4e 44 02 04')+hkcmd
            hkcmd=hkcmd+csodd+cseven
            self.plugin.serial.write(str(hkcmd))
            return self.plugin.serial


        def replaceFunc(self, data):
            data = data.strip()
            if data == "CR":
                return chr(13)
            elif data == "LF":
                return chr(10)
            else:
                return None


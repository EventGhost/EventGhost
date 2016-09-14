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

# TODO: Use of eg.SerialThread instead of eg.SerialPort

import eg

eg.RegisterPlugin(
    name = "Serial Port",
    author = "Bitmonster",
    guid = "{D565171F-1703-4212-972C-B824B55329CB}",
    version = "1.1",
    canMultiLoad = True,
    description = "Arbitrary communication through a serial port.",
)



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
    encoding = "Encoding:"
    codecChoices = [
        "System code page",
        "HEX",
        "Latin-1",
        "UTF-8",
        "UTF-16",
        "Python string escape",
    ]
    class Write:
        name = "Write Data"
        description = (
            "Writes some text through the serial port."
            "\n\n<p>"
            "You can use Python string escapes to send non-printable "
            "characters. Some examples:<p>"
            "\\n will send a Linefeed (LF)<br>"
            "\\r will send a Carriage Return (CR)<br>"
            "\\t will send a Horizontal Tab (TAB)<br>"
            "\\x0B will send the ASCII character with the hexcode 0B<br>"
            "\\\\ will send a single Backslash."
        )
    class Read:
        name = "Read Data"
        description = (
            "Reads data from the serial port."
            "\n\n<p>"
            "This action returns the data through <i>eg.result</i>, as any "
            "action does that is returning data. So you have to use "
            '<a href="http://www.eventghost.org/wiki/Scripting">'
            "Python scripting</a> to do anything with the result."
            "<p>"
            "Using this action and enabling event generation in the plugin "
            "cannot be used at the same time, as one of it will always eat "
            "the data away from the other."
        )
        read_all = "Read as many bytes as are currently available"
        read_some = "Read exactly this number of bytes:"
        read_time = "and wait this maximum number of milliseconds for them:"


import wx
import threading
import win32event
import win32file
import codecs
import binascii

BAUDRATES = [
    '110', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200',
    '38400', '57600', '115200', '128000', '256000'
]


def MyHexDecoder(input):
    return (binascii.b2a_hex(input).upper(), len(input))


DECODING_FUNCS = [
    codecs.getdecoder(eg.systemEncoding),
    MyHexDecoder,
    codecs.getdecoder("latin1"),
    codecs.getdecoder("utf8"),
    codecs.getdecoder("utf16"),
    codecs.getencoder("string_escape"),
]


class Serial(eg.RawReceiverPlugin):
    text = Text

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.AddAction(Write)
        self.AddAction(Read)
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
        prefix="Serial",
        encodingNum=0,
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
            self.decoder = DECODING_FUNCS[encodingNum]
            self.terminator = eg.ParseString(
                terminator
            ).decode('string_escape')
            self.info.eventPrefix = prefix
            self.stopEvent = win32event.CreateEvent(None, 1, 0, None)
            self.receiveThread = threading.Thread(
                target=self.ReceiveThread,
                name="SerialThread"
            )
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
        self.buffer += ch
        pos = self.buffer.find(self.terminator)
        if pos != -1:
            eventstring = self.buffer[:pos]
            if eventstring:
                self.TriggerEvent(self.decoder(eventstring)[0])
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
        bytesize=3,
        parity=0,
        stopbits=0,
        handshake=0,
        generateEvents=False,
        terminator="\\r",
        prefix="Serial",
        encodingNum=0,
    ):
        text = self.text
        panel = eg.ConfigPanel()
        portCtrl = panel.SerialPortChoice(port)

        baudrateCtrl = panel.ComboBox(
            str(baudrate),
            BAUDRATES,
            style=wx.CB_DROPDOWN,
            validator=eg.DigitOnlyValidator()
        )
        bytesizeCtrl = panel.Choice(bytesize, ['5', '6', '7', '8'])
        parityCtrl = panel.Choice(parity, text.parities)
        stopbitsCtrl = panel.Choice(stopbits, ['1', '2'])
        handshakeCtrl = panel.Choice(handshake, text.handshakes)
        generateEventsCtrl = panel.CheckBox(
            generateEvents,
            text.generateEvents
        )
        terminatorCtrl = panel.TextCtrl(terminator)
        terminatorCtrl.Enable(generateEvents)
        prefixCtrl = panel.TextCtrl(prefix)
        prefixCtrl.Enable(generateEvents)
        encodingCtrl = panel.Choice(encodingNum, text.codecChoices)
        encodingCtrl.Enable(generateEvents)

        def OnCheckBox(event):
            flag = generateEventsCtrl.GetValue()
            terminatorCtrl.Enable(flag)
            prefixCtrl.Enable(flag)
            encodingCtrl.Enable(flag)
            event.Skip()
        generateEventsCtrl.Bind(wx.EVT_CHECKBOX, OnCheckBox)

        panel.SetColumnFlags(1, wx.EXPAND)
        portSettingsBox = panel.BoxedGroup(
            "Port settings",
            (text.port, portCtrl),
            (text.baudrate, baudrateCtrl),
            (text.bytesize, bytesizeCtrl),
            (text.parity, parityCtrl),
            (text.stopbits, stopbitsCtrl),
            (text.flowcontrol, handshakeCtrl),
        )
        eventSettingsBox = panel.BoxedGroup(
            "Event generation",
            (generateEventsCtrl),
            (text.terminator, terminatorCtrl),
            (text.eventPrefix, prefixCtrl),
            (text.encoding, encodingCtrl),
        )
        eg.EqualizeWidths(portSettingsBox.GetColumnItems(0))
        eg.EqualizeWidths(portSettingsBox.GetColumnItems(1))
        eg.EqualizeWidths(eventSettingsBox.GetColumnItems(0)[1:])
        eg.EqualizeWidths(eventSettingsBox.GetColumnItems(1))
        panel.sizer.Add(
            eg.HBoxSizer(portSettingsBox, (10, 10), eventSettingsBox)
        )
        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
                int(baudrateCtrl.GetValue()),
                bytesizeCtrl.GetValue(),
                parityCtrl.GetValue(),
                stopbitsCtrl.GetValue(),
                handshakeCtrl.GetValue(),
                generateEventsCtrl.GetValue(),
                terminatorCtrl.GetValue(),
                prefixCtrl.GetValue(),
                encodingCtrl.GetValue(),
            )



class Write(eg.ActionWithStringParameter):

    def __call__(self, data):
        data = eg.ParseString(data, self.replaceFunc)
        data = data.decode('string_escape')
        self.plugin.serial.write(str(data))
        return self.plugin.serial


    def replaceFunc(self, data):
        data = data.strip()
        if data == "CR":
            return chr(13)
        elif data == "LF":
            return chr(10)
        else:
            return None



class Read(eg.ActionBase):

    def __call__(self, count=None, timeout=0.0):
        serial = self.plugin.serial
        serial.timeout = timeout
        if count is None:
            count = 1024
        data = serial.read(count)
        return data


    def GetLabel(self, *args):
        return eg.ActionBase.GetLabel(self)


    def Configure(self, count=None, timeout=1.0):
        text = self.text
        panel = eg.ConfigPanel()
        if count is None:
            count = 1
            flag = False
        else:
            flag = True
        if timeout is None:
            timeout = 1.0
        rb1 = panel.RadioButton(not flag, text.read_all, style=wx.RB_GROUP)
        rb2 = panel.RadioButton(flag, text.read_some)
        countCtrl = panel.SpinIntCtrl(count, 1, 1024)
        countCtrl.Enable(flag)
        timeCtrl = panel.SpinIntCtrl(int(timeout * 1000), 0, 10000)
        timeCtrl.Enable(flag)

        def OnRadioButton(event):
            flag = rb2.GetValue()
            countCtrl.Enable(flag)
            timeCtrl.Enable(flag)
            event.Skip()
        rb1.Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
        rb2.Bind(wx.EVT_RADIOBUTTON, OnRadioButton)

        Add = panel.sizer.Add
        Add(rb1)
        Add((5,5))
        Add(rb2)
        Add((5,5))
        Add(countCtrl, 0, wx.LEFT, 25)
        Add((5,5))
        Add(panel.StaticText(text.read_time), 0, wx.LEFT, 25)
        Add((5,5))
        Add(timeCtrl, 0, wx.LEFT, 25)

        while panel.Affirmed():
            if rb1.GetValue():
                panel.SetResult(None, 0.0)
            else:
                panel.SetResult(
                    countCtrl.GetValue(),
                    timeCtrl.GetValue() / 1000.0
                )


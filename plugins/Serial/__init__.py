# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright © EventGhost Project <http://www.eventghost.net/>
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


import eg
import wx
import threading
import win32event
import win32file
import _winreg as winreg
import codecs
import binascii
import time
import itertools


eg.RegisterPlugin(
    name = "Serial Port",
    author = "Bitmonster, Markus Gruber",
    guid = "{D565171F-1703-4212-972C-B824B55329CB}",
    version = "2.0",
    canMultiLoad = True,
    description = "Arbitrary communication through a serial port.",
)


def enumerate_serial_ports():
    """ Uses the Win32 registry to return an
        iterator of serial (COM) ports
        existing on this computer.
    """
    PATH = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, PATH)
    except WindowsError:
        raise IterationError

    for i in itertools.count():
        try:
            val = winreg.EnumValue(key, i)
            yield str(val[1])
        except EnvironmentError:
            break


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


def RevokeWorkPermit(self):
    if self.plugin.ReceiveThread is not None:
        if self.plugin.ReceiveThread_WorkPermit.is_set() is True:
            self.plugin.ReceiveThread_WorkPermit.clear()
            time.sleep(self.plugin.SerialPortInterface.timeout)
        else:
            print("The worker thread is already paused.")
    else:
        print("'Generate events' is not enabled, so the worker thread does not need to be paused.")


def GrantWorkPermit(self):
    if self.plugin.ReceiveThread is not None:
        if self.plugin.ReceiveThread_WorkPermit.is_set() is False:
            FlushInput(self)
            self.plugin.ReceiveThread_WorkPermit.set()
        else:
            print("The worker thread is already running.")
    else:
        print("'Generate events' is not enabled, so the worker thread can not be unpaused.")


def FlushInput(self):
    self.plugin.SerialPortInterface.flushInput()


class Serial(eg.RawReceiverPlugin):

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.AddAction(fnWrite)
        self.AddAction(fnRead)
        self.AddAction(fnPauseEventGeneration)
        self.AddAction(fnFlushInput)
        self.AddAction(fnContinueEventGeneration)
        self.SerialPortInterface = None
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

        if self.SerialPortInterface:
            self.SerialPortInterface.close()

        try:
            self.SerialPortInterface = eg.SerialPort(
                port,
                baudrate=baudrate,
                bytesize=(5, 6, 7, 8)[bytesize],
                stopbits=(1, 2)[stopbits],
                parity=('N', 'O', 'E')[parity],
                xonxoff=xonxoff,
                rtscts=rtscts,
            )
        except:
            self.SerialPortInterface = None
            raise self.Exceptions.SerialOpenFailed

        self.SerialPortInterface.timeout = 1.0
        self.SerialPortInterface.setRTS()

        if generateEvents:
            self.decoder = DECODING_FUNCS[encodingNum]
            self.terminator = eg.ParseString(
                terminator
            ).decode('string_escape')
            self.info.eventPrefix = prefix
            self.ReceiveThread_WorkPermit = threading.Event()
            self.ReceiveThread_WorkPermit.set()
            self.stopEvent = win32event.CreateEvent(None, 1, 0, None)
            self.ReceiveThread = threading.Thread(
                target=self.ReceiveThreadLoop,
                name="SerialThread",
                args=(self.ReceiveThread_WorkPermit, )
            )
            self.ReceiveThread.start()
        else:
            self.ReceiveThread = None


    def __stop__(self):
        if self.SerialPortInterface is not None:
            if self.ReceiveThread:
                win32event.SetEvent(self.stopEvent)
                self.ReceiveThread.join(1.0)
            self.SerialPortInterface.close()
            self.SerialPortInterface = None


    def HandleChar(self, ch):
        self.buffer += ch
        pos = self.buffer.find(self.terminator)
        if pos != -1:
            eventstring = self.buffer[:pos]
            if eventstring:
                self.TriggerEvent(self.decoder(eventstring)[0])
            self.buffer = self.buffer[pos+len(self.terminator):]


    def ReceiveThreadLoop(self, ReceiveThread_WorkPermit):
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
        overlapped = self.SerialPortInterface._overlappedRead
        hComPort = self.SerialPortInterface.hComPort
        hEvent = overlapped.hEvent
        stopEvent = self.stopEvent
        n = 1
        waitingOnRead = False
        buf = AllocateReadBuffer(n)

        while continueLoop:
            # An event object manages an internal flag that can be set to
            #     true with the set() method
            #     reset to false with the clear()
            # method. It is set to false initially.
            # The wait() method blocks until the flag is true.
            self.ReceiveThread_WorkPermit.wait(None)

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

        panel = eg.ConfigPanel()

        COMPORTS = []

        for val in enumerate_serial_ports():
            COMPORTS.append(val)

        portCtrl = panel.ComboBox(
            "COM%d" % (port+1),
            COMPORTS,
            style=wx.CB_DROPDOWN
        )

        BAUDRATES = ['110', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '38400', '57600', '115200', '128000', '256000']

        baudrateCtrl = panel.ComboBox(
            str(baudrate),
            BAUDRATES,
            style=wx.CB_DROPDOWN,
            validator=eg.DigitOnlyValidator()
        )

        bytesizeCtrl = panel.Choice(bytesize, ['5', '6', '7', '8'])

        parityCtrl = panel.Choice(parity, ['No parity', 'Odd', 'Even'])

        stopbitsCtrl = panel.Choice(stopbits, ['1', '2'])

        handshakeCtrl = panel.Choice(handshake, ['None', 'Xon / Xoff', 'Hardware'])

        generateEventsCtrl = panel.CheckBox(
            generateEvents,
            "Generate events on incoming data"
        )

        terminatorCtrl = panel.TextCtrl(terminator)
        terminatorCtrl.Enable(generateEvents)

        prefixCtrl = panel.TextCtrl(prefix)
        prefixCtrl.Enable(generateEvents)

        codecChoices = [
            "System code page",
            "HEX",
            "Latin-1",
            "UTF-8",
            "UTF-16",
            "Python string escape",
        ]

        encodingCtrl = panel.Choice(encodingNum, codecChoices)
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
            ("Port", portCtrl),
            ("Baudrate", baudrateCtrl),
            ("Number of bits", bytesizeCtrl),
            ("Parity", parityCtrl),
            ("Stopbits", stopbitsCtrl),
            ("Flow control", handshakeCtrl),
        )

        eventSettingsBox = panel.BoxedGroup(
            "Event generation",
            (generateEventsCtrl),
            ("Terminator", terminatorCtrl),
            ("Event prefix", prefixCtrl),
            ("Encoding", encodingCtrl),
        )

        eg.EqualizeWidths(portSettingsBox.GetColumnItems(0))
        eg.EqualizeWidths(portSettingsBox.GetColumnItems(1))
        eg.EqualizeWidths(eventSettingsBox.GetColumnItems(0)[1:])
        eg.EqualizeWidths(eventSettingsBox.GetColumnItems(1))

        panel.sizer.Add(
            eg.HBoxSizer(portSettingsBox, (10, 10), eventSettingsBox)
        )

        while panel.Affirmed():
            port = int(portCtrl.GetValue()[3:])-1
            panel.SetResult(
                port,
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


class fnPauseEventGeneration(eg.ActionBase):

    class text:
        name = "Pause event generation"
        description = "Pauses event generation so that data can safely be accessed by other EventGhost activities."


    def __call__(self):
        RevokeWorkPermit(self)


class fnContinueEventGeneration(eg.ActionBase):

    class text:
        name = "Continue event generation"
        description = "Continues event generation. Unread data in the buffer is flushed."


    def __call__(self):
        GrantWorkPermit(self)


class fnFlushInput(eg.ActionBase):

    class text:
        name = "Flush input"
        description = "Flushes unread data from the buffer."


    def __call__(self):
        FlushInput(self)


class fnWrite(eg.ActionWithStringParameter):

    class text:
        name = "Write"
        parameterDescription = "String to send (EventGhost variables such as {eg.result} can be embedded)."
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


    def __call__(self, data):
        data = eg.ParseString(data, self.replaceFunc)
        data = data.decode('string_escape')

        RevokeWorkPermit(self)
        FlushInput(self)
        self.plugin.SerialPortInterface.write(str(data))
        time.sleep(1)
        returndata = self.plugin.SerialPortInterface.read(self.plugin.SerialPortInterface.inWaiting())
        GrantWorkPermit(self)
        return returndata


    def replaceFunc(self, data):
        data = data.strip()
        if data == "CR":
            return chr(13)
        elif data == "LF":
            return chr(10)
        else:
            return None


class fnRead(eg.ActionBase):

    class text:
        name = "Read"
        description = (
            "Reads data from the serial port."
            "\n\n<p>"
            "This action returns the data through <i>eg.result</i>, as any "
            "action does that is returning data. So you have to use "
            "Python scripting</a> to do anything with the result."
            "<p>"
            "Using this action and enabling event generation in the plugin "
            "cannot be used at the same time, as one of it will always eat "
            "the data away from the other. "
            "This action does not automatically pause and unpause event generation. "
            "You can pause and unpause event generation with the 'Pause event generation' and 'Resume event generation' actions."
        )


    def __call__(self, count=None, timeout=0.0):
        TempSerial = self.plugin.SerialPortInterface
        TempSerial.timeout = timeout
        if count is None:
            data = TempSerial.read(TempSerial.inWaiting())
        else:
            data = TempSerial.read(count)
        TempSerial = None
        return data


    def GetLabel(self, *args):
       return eg.ActionBase.GetLabel(self)


    def Configure(self, count=None, timeout=1.0):
        panel = eg.ConfigPanel()

        if count is None:
            count = 1
            flag = False
        else:
            flag = True
        if timeout is None:
            timeout = 1.0

        rb1 = panel.RadioButton(not flag, "Read as many bytes as are currently available", style=wx.RB_GROUP)
        rb2 = panel.RadioButton(flag, "Read exactly this number of bytes")
        countCtrl = panel.SpinIntCtrl(count, 1, 2147483647)
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
        Add(panel.StaticText("and wait this maximum number of milliseconds for them"), 0, wx.LEFT, 25)
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

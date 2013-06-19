import eg

class PluginInfo(eg.PluginInfo):
    name = "Serial Port"
    author = "Bitmonster"
    version = "1.1.0"
    description = "Arbitrary communication through a serial port."


    
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
    class Write:
        name = "Write Data"
    class Read:
        name = "Read Data"
        read_all = "Read as many bytes as are currently available"
        read_some = "Read exactly this number of bytes:"
        read_time = "and wait this maximum number of milliseconds for them:"
    


import wx
import threading
import win32event
import win32file

class Serial(eg.RawReceiverPlugin):
    canMultiLoad = True
    text = Text
    
    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.AddAction(self.Write)
        self.AddAction(self.Read)
        self.Send = self.Write
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
            raise eg.Exception("Can't open COM port.")
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
        self.buffer += ch
        pos = self.buffer.find(self.terminator)
        if pos != -1:
            eventstring = self.buffer[:pos].strip()
            if eventstring:
                self.TriggerEvent(eventstring)
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
        prefix="Serial",
    ):
        text = self.text
        dialog = eg.ConfigurationDialog(self)
        portCtrl = eg.SerialPortChoice(dialog, value=port)
        
        baudrateCtrl = wx.ComboBox(
            dialog,
            value=str(baudrate),
            choices=[
                        '110', '300', '600', '1200', '2400', '4800', '9600',
                        '14400', '19200', '38400', '57600', '115200', 
                        '128000', '256000'
                    ],
            style=wx.CB_DROPDOWN,
            validator=eg.DigitOnlyValidator()
        )
        
        bytesizeCtrl = wx.Choice(dialog, choices=['5', '6', '7', '8'])
        bytesizeCtrl.SetSelection(8 - 5)
        
        parityCtrl = wx.Choice(dialog, choices=text.parities)
        parityCtrl.SetSelection(parity)
        
        stopbitsCtrl = wx.Choice(dialog, choices=['1', '2'])
        stopbitsCtrl.SetSelection(stopbits)
        
        handshakeCtrl = wx.Choice(dialog, choices=text.handshakes)
        handshakeCtrl.SetSelection(handshake)
        
        generateEventsCtrl = wx.CheckBox(dialog, label=text.generateEvents)
        generateEventsCtrl.SetValue(generateEvents)
        
        terminatorCtrl = wx.TextCtrl(dialog)
        terminatorCtrl.SetValue(terminator)
        terminatorCtrl.Enable(generateEvents)
        
        prefixCtrl = wx.TextCtrl(dialog)
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
        Add(wx.StaticText(dialog, -1, text.port), (0, 0), flag=flags)
        Add(portCtrl, (0, 1), flag=wx.EXPAND)
        Add(wx.StaticText(dialog, -1, text.baudrate), (1, 0), flag=flags)
        Add(baudrateCtrl, (1, 1), flag=wx.EXPAND)
        Add(wx.StaticText(dialog, -1, text.bytesize), (2, 0), flag=flags)
        Add(bytesizeCtrl, (2, 1), flag=wx.EXPAND)
        Add(wx.StaticText(dialog, -1, text.parity), (3, 0), flag=flags)
        Add(parityCtrl, (3, 1), flag=wx.EXPAND)
        Add(wx.StaticText(dialog, -1, text.stopbits), (4, 0), flag=flags)
        Add(stopbitsCtrl, (4, 1), flag=wx.EXPAND)
        Add(wx.StaticText(dialog, -1, text.flowcontrol), (5, 0), flag=flags)
        Add(handshakeCtrl, (5, 1), flag=wx.EXPAND)
        
        Add((5, 5), (6, 0), (1, 2), flag=flags)
        Add(generateEventsCtrl, (7, 0), (1, 2), flag=flags)
        Add(wx.StaticText(dialog, -1, text.terminator), (8, 0), flag=flags)
        Add(terminatorCtrl, (8, 1), flag=wx.EXPAND)
        Add(wx.StaticText(dialog, -1, text.eventPrefix), (9, 0), flag=flags)
        Add(prefixCtrl, (9, 1), flag=wx.EXPAND)
        dialog.sizer.Add(mySizer)

        if dialog.AffirmedShowModal():
            return (
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
        
        
        
    class Read(eg.ActionClass):
        
        def __call__(self, count=None, timeout=0.0):
            serial = self.plugin.serial
            serial.timeout = timeout
            if count is None:
                count = 1024
            data = serial.read(count)
            return data
        
        
        def GetLabel(self, *args):
            return eg.ActionClass.GetLabel(self)
        
        
        def Configure(self, count=None, timeout=1.0):
            text = self.text
            dialog = eg.ConfigurationDialog(self)
            rb1 = wx.RadioButton(dialog, -1, text.read_all, style=wx.RB_GROUP)
            rb2 = wx.RadioButton(dialog, -1, text.read_some)
            if count is None:
                count = 1
                rb1.SetValue(True)
            else:
                rb2.SetValue(True)
            if timeout is None:
                timeout = 1.0
            countCtrl = eg.SpinIntCtrl(dialog, -1, count, 1, 1024)
            timeCtrl = eg.SpinIntCtrl(dialog, -1, int(timeout * 1000), 0, 10000)
            
            def onRadioButton(event):
                flag = rb2.GetValue()
                countCtrl.Enable(flag)
                timeCtrl.Enable(flag)
                event.Skip()
                
            rb1.Bind(wx.EVT_RADIOBUTTON, onRadioButton)
            rb2.Bind(wx.EVT_RADIOBUTTON, onRadioButton)
            Add = dialog.sizer.Add
            Add(rb1)
            Add((5,5))
            Add(rb2)
            Add((5,5))
            Add(countCtrl, 0, wx.LEFT, 25)
            Add((5,5))
            Add(wx.StaticText(dialog, -1, text.read_time), 0, wx.LEFT, 25)
            Add((5,5))
            Add(timeCtrl, 0, wx.LEFT, 25)
            flag = rb2.GetValue()
            countCtrl.Enable(flag)
            timeCtrl.Enable(flag)
            
            if dialog.AffirmedShowModal():
                if rb1.GetValue():
                    return None, 0.0
                else:
                    return countCtrl.GetValue(), timeCtrl.GetValue() / 1000.0
        
        
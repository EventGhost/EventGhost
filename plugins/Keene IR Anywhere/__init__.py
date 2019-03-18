##############################################################################
# Revision history:
#
# 2011-04-28  Blocking some buttons (OK, Cancel, Apply, Test) during the IR
#             learning process
# 2011-04-25  New alternative version for the Keene IR Anywhere
#             - Based on the original version made by ldobson
#             - Added support for sending pronto codes
#             - Added support for repeats & delays in between 
#             - Added support for learning IR codes
#             - Added support to discover your Keene IR Anywhere devices
#             - Improved handling of pasted codes in various formats
#             - Fixed to work with -translate switch
##############################################################################

eg.RegisterPlugin(
    name = 'Keene IR Anywhere with Pronto Support',
    guid = '{ED9EAF6B-5B06-4A01-B418-F172B8BA4DDF}',
    author = 'Krambriw',
    version = '1.0.1', 
    kind = 'remote',
    canMultiLoad = True,
    description = '''\
        Hardware plugin for the 
        <a href="http://www.keene.co.uk/iranywhere">
            Keene Electronics IR Anywhere
        </a>
         transceiver

        <p>
            <div align="center">
                <img src="KIRA.jpg"/>
            </div>
        </p>
        <p>
            If you have multiple number of units then make sure they are all using 
            different ports before you start the servers for the units. Otherwise
            you will be confused as to which unit you are receiving information from,
            as only one of the plugin instances will be able to listen on a specific port.
        </p>
        <p>
            The plugin supports typically events like the following:
            <ul>
                <li>
                    <b>KIRA.XXXXXX.DDDDDDDD</b> - 
                    (assuming "KIRA" is your event prefix).
                    Happens when we receive an IR stream, this event name
                    is the decoded IR that can be used to pick up on
                    subsequent presses of the same button. "XXXXXX" is the
                    IR protocol (it's not uncommon to see this as "Unknown"
                    so don't panic) and "DDDDDDDD" is the code itself.
                </li>
            </ul>
            <p>
                If you switch on "Log incoming raw IR streams", the IR 
                streams will be printed in the log window in the format:
            </p>
            <p>
                <div align="center">
                    <b>KIRA.Raw.XXYY DDDD DDDD DDDD 2000</b>
                </div>
            </p>
            <p>
                When a unit sends an "ACK" response to an action, 
                then this will appear in the log window:
            </p>
            <p>
                <div align="center">
                    <b>KIRA.Acknowledgement</b>
                </div>
            </p>
            <p>
                If you then in addition also switch on "Play a sound
                on incoming IR streams", you will hear a short sound when
                the unit receives the IR stream.
            </p>
        </p>
    '''
)

import asyncore, socket, winsound, time
from threading import Event, Thread



class Text:
    host = 'Host or IP:'
    port = 'UDP Port:'
    svr = 'Make this unit a StandAlone and start a server for it to receive events'
    eventPrefix = 'Event Prefix:'
    ipBox = 'IP Settings'
    eventBox = 'Event generation'
    logRaw = 'Log incoming raw IR streams'
    Sound = 'Play a sound on incoming IR streams'
    transmitDesc = '''\
        <p>
            <p>
                Transmits an IR code via the IR Anywhere hardware.
            </p>
            
            
            
            
            
            
            <p>
                To capture IR codes, the best is to use the learn function.
                The KIRA format copied from the logged incoming raw IR
                streams can also be used but then remove the leading "KIRA.Raw."
                before using them (where "KIRA" is your event prefix).
            </p>
            <p>
                You may remove or leave the leading "K " from IR
                streams that you have learned with the learn function.
            </p>
            <p>
                A valid learned code looks like this: 
            </p>
            <p>
                <div align="center">
                    <b>K XXYY DDDD DDDD DDDD 2000</b>
                </div>
            </p>
            <p>
                where "K" is the Keene identifier, "XX" is the frequency,
                "YY" is the number of following pairs, "DDDD" is the data
                (there will be an odd number of these chunks), and "2000"
                is the hard-coded "end of code".
            </p>
            <p>
                This plugin version also supports pronto codes. Just paste them
                in as they normally are formatted. A typical pronto code may
                look like this:
            </p>
            <p>
                <div align="left">
                    <b>0000 0073 0000 0019 000e 002a 002a 000e 000e 002a 000e 002a 000e 002a 000e 002a 000e 002a 000e 002a 000e 002a 000e 002a 000e 002a 000e 002a 000e 002a 002a 000e 000e 002a 002a 000e 000e 002a 000e 002a 000e 002a 002a 000e 000e 002a 002a 000e 000e 002a 002a 000e 000e 0199</b>
                </div>
            </p>
            <p>
                0000 = Start is always 0000
            </p>
            <p>
                0073 = frequency is 36Khz
            </p>
            <p>
                0073 hex = 115 decimal, 36,045 = 1000000/(115*.241246)
            </p>
            <p>
                To use the actual IR stream that triggered the current KIRA event in scripts or in other plugins, simply use the payload:
            </p>
            <p>
                <div align="center">
                    <b>{eg.event.payload}</b>
                </div>
            </p>
        </p>
    '''
    discoverDesc = '''\
        <p>
            <p>
                Discover IR Anywhere hardware devices .
            </p>
            
            
            
            
            
            
            <p>
                Use this action to discover devices on your network.
            </p>
            <p>
            </p>
            <p>
                A typical respons could look like this: 
            </p>
            <p>
                <div align="left">
                    <p>    08:43:21         STANDALONE 
                    <p>    08:43:21         192.168.10.2 
                    <p>    08:43:21         00:50:C2:96:D0:4B 
                    <p>    08:43:21         2 = standAlone 
                    <p>    08:43:21         65432 
                    <p>    08:43:21         192.168.10.2 
                    <p>    08:43:21         255.255.255.0 
                    <p>    08:43:21         192.168.10.254 
                    <p>    08:43:21         192.168.10.254 
                    <p>    08:43:21         194.74.65.68 
                    <p>    08:43:21         192.168.10.32 
                    <p>    08:43:21         192.168.10.248 
                    <p>    08:43:21         DHCP = on 
                    <p>    08:43:21         DDNS = off 
                    <p>    08:43:21         1.75 
                    <p>    08:43:21         Discovery reply 
                </div>
            </p>
            <p>
                The received lines are: 
            </p>
            <p>
            <p>    Hostname
            <p>    IP Address
            <p>    MAC address
            <p>    mode of unit
            <p>    IR port
            <p>    last IP address
            <p>    Subnet mask
            <p>    Gateway address
            <p>    DNS 1 address
            <p>    DNS 2 address 
            <p>    Target address
            <p>    PC address
            <p>    DHCP state
            <p>    DDNS state
            <p>    Firmware version
            <p>    Text description of answer type
            </p>
        </p>
    '''
    freqtxt = 'Frequency: '
    seTXtxt = " TX's Self_M: "
    soTXtxt = " TX's Socket_M: "
    
    class Transmit:
        repeatBox = 'Transmission repeats'
        repeat = 'Set number of repeats (0-99)'
        repeatDelay = 'Set the delay between the repeats (0.01 - 99.99 s)'
        learnButton = 'Learn an IR Code...'
        acceptBurstButton = 'Accept Burst'
        irLearnStarted = 'Scanning for incoming IR started...'
        irBurstAccepted = 'IR code accepted. Click on OK and the captured IR code will be used'



class KeeneIR(eg.PluginClass):
    text = Text

    def __init__(self):
        self.AddAction(Transmit)
        self.AddAction(Discover)
        self.irDecoder = eg.IrDecoder(self, 1)


    def __close__(self):
        self.irDecoder.Close()


    def __start__(self, host, port, svr, prefix, logRaw, bSound):
        self.host = host
        self.port = port
        self.svr = svr
        self.info.eventPrefix = prefix
        self.logRaw = logRaw
        self.bSound = bSound
        self.server = None

        if (self.svr):
            try:
                self.server = Server(self.port, self)
                self.Send('cmdM2', 0, 0.0)
                self.Send('cmdI', 0, 0.0)
            except socket.error, exc:
                raise self.Exception(exc[1])
        else:
            self.server = None


    def __stop__(self):
        if self.server:
            self.server.close()
        self.server = None


    def Configure(
        self, 
        host = 'StandAlone', 
        port = 65432, 
        svr = True,
        prefix = 'KIRA',
        logRaw = True,
        bSound = False
    ):
        text = self.text
        panel = eg.ConfigPanel(self)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, min = 10000, max = 65535)
        svrCtrl = panel.CheckBox(svr, text.svr)
        eventPrefixCtrl = panel.TextCtrl(prefix)
        logRawCtrl = panel.CheckBox(logRaw, text.logRaw)
        bSoundCtrl = panel.CheckBox(bSound, text.Sound)

        st1 = panel.StaticText(text.host)
        st2 = panel.StaticText(text.port)
        st3 = panel.StaticText(text.eventPrefix)
        eg.EqualizeWidths((st1, st2, st3))

        ipBox = panel.BoxedGroup(
            text.ipBox,
            (st1, hostCtrl),
            (st2, portCtrl),
            (svrCtrl),
        )

        eventBox = panel.BoxedGroup(
            text.eventBox, 
            (st3, eventPrefixCtrl, logRawCtrl, bSoundCtrl) 
        )

        panel.sizer.Add(ipBox, 0, wx.EXPAND)
        panel.sizer.Add(eventBox, 0, wx.TOP|wx.EXPAND, 10)

        eventPrefixCtrl.Enable(svrCtrl.IsChecked())
        logRawCtrl.Enable(svrCtrl.IsChecked())
        bSoundCtrl.Enable(svrCtrl.IsChecked())


        def OnCheckBox(event):
            eventPrefixCtrl.Enable(svrCtrl.IsChecked())
            logRawCtrl.Enable(svrCtrl.IsChecked())
            bSoundCtrl.Enable(svrCtrl.IsChecked())
            event.Skip()
            
        svrCtrl.Bind(wx.EVT_CHECKBOX, OnCheckBox)

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(), 
                portCtrl.GetValue(), 
                svrCtrl.GetValue(), 
                eventPrefixCtrl.GetValue(), 
                logRawCtrl.GetValue(),
                bSoundCtrl.GetValue()
            )


    def Send(self, mesg, repeat, repeatDelay):
        if (self.server):
            for i in range(repeat+1):
                self.server.socket.sendto(mesg, (self.host, self.port))
                if i == repeat:
                    #print i+1, Text.seTXtxt, mesg
                    time.sleep(repeatDelay)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', self.port))
            for i in range(repeat+1):
                sock.sendto(mesg, (self.host, self.port))
                if i == repeat:
                    #print i+1, Text.soTXtxt, mesg
                    time.sleep(repeatDelay)
            sock.close()


    def averageThis(self, p_data):
        X = 0
        y = 0
        tmpStr = ""
        Pair_Count = 0
        Burst_Time = []
        MyInt = []
        codeLength = len(p_data)
        last_code = 0
        timeA = 0.0
        timeB = 0.0
        zzz = 0
    
        for X in range(0,255):
            Burst_Time.append(0)
    
        for X in range(0,codeLength,5):
            tmpStr = p_data[X:X+4]
            Burst_Time[y] = int(tmpStr, 16)
            y += 1
    
        last_code = y
        Pair_Count = Burst_Time[0] % 256
       
        for zzz in range(2,last_code - 2):
            timeA = Burst_Time[zzz] * 0.75
            timeB = Burst_Time[zzz] * 1.30
            MyObjList = []
           
            for X in range(zzz,last_code):
                tstTime = Burst_Time[X]
    
                if (tstTime > timeA and tstTime < timeB):
                    MyObjList.append(X)
                    MyObjList.append(tstTime)
    
            L = len(MyObjList)
            total = 0
       
            if L > 0:
                for X in range(1,L,2):
                    MyOb = MyObjList[X]
                    total = total + MyOb
    
                average = total / (L / 2)
            pos = 0
    
            if L > 0:
                for X in range(0,L,2):
                    MyOb = MyObjList[X]
                    pos = MyOb
                    Burst_Time[pos] = average
       
        data = ""
       
        for X in range(0,last_code):
            nb = str(hex(Burst_Time[X]))[2:]
            if len( nb ) < 4:
                nb = "0" + nb
            data = data + nb.upper() + " "
    
        data = "K " + data # K plus a space plus data

        return data

    
    def convertFromPronto(self, p_data):
        X = 0
        y = 0
        tmpStr = ""
        freq = 0.0
        Pair_Count = 0
        Lead_in = 0
        Burst_Time = []
        MyInt = []
        codeLength = len(p_data)
       
        for X in range(0,255):
            Burst_Time.append(0)

        for X in range(0,codeLength,5):
            tmpStr = p_data[X:X+4]
            Burst_Time[y] = int(tmpStr, 16)
            y += 1

        freq = 4145 / Burst_Time[1]
        Pair_Count = Burst_Time[2]

        if Pair_Count == 0:
            Pair_Count = Burst_Time[3]

        if Pair_Count == 0:
            return ""
       
        for X in range(0,y):
            MyInt.append(0)
       
        MyInt[0] = freq * 256 + Pair_Count
        cycle_time = 1000 / freq
        Lead_in = Burst_Time[4] * cycle_time
        MyInt[1] = Lead_in
        MyInt[2] = Burst_Time[5] * cycle_time
        Pair_Count = Pair_Count - 1
       
        for X in range(0,Pair_Count * 2):
            MyInt[X + 3] = Burst_Time[X + 6] * cycle_time

        MyInt[X + 3] = 8192
        data = ""

        for X in range(0,(Pair_Count * 2) + 3):
            nb = str(hex(MyInt[X]))[2:]
            if len( nb ) < 4:
                nb = "0" + nb
            data = data + nb.upper() + " "

        return data



class Server(asyncore.dispatcher):

    def __init__(self, port, handler):
        self.handler = handler
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(('', port))
        self.add_channel()
        eg.RestartAsyncore()


    def handle_read(self):
        try:
            rawdata, client_addr = self.socket.recvfrom(1024)

            codes = rawdata.split()
            if (codes[0] == 'K'):
                codes.remove('K')

                rawCode = ' '.join(codes)

                if (self.handler.logRaw):
                    if self.handler.bSound:
                        winsound.Beep(1000, 80)
                    print(
                        self.handler.info.eventPrefix + 
                        '.Raw.' + rawCode
                    )

                try:
                    info = codes.pop(0)
                    numpairs = int(info[2:], 16)
                    frequency = int(info[:2], 16)
                    data = [int(i, 16) for i in codes]
                    if (
                        len(codes) == (numpairs * 2)
                        and
                        codes[len(codes) - 1] == '2000'
                    ):
                        self.socket.sendto(
                            'ACK', 
                            (client_addr[0], client_addr[1])
                        )
                        self.handler.irDecoder.Decode(data, len(data))
                        self.handler.irDecoder.event.payload = rawCode
                        if self.handler.bSound:
                            winsound.Beep(500, 2)

                    else:
                        raise self.handler.Exception()
                except:
                    print 'Malformed incoming IR code'

            elif (codes[0] == 'ACK'):
                print(
                    self.handler.info.eventPrefix + 
                    '.Acknowledgement'
                )
                
        except socket.timeout:
            pass

        except socket.error, (errno, strerror):
            print errno
            if (errno == 10054):
                # this happens when we transmit from the server socket
                pass
            else:
                raise self.handler.Exception()


    def handle_accept(self):
        pass


    def handle_connect(self):
        pass


    def handle_close(self):
        pass


    def writable(self):
        return False



class Transmit(eg.ActionClass):
    name = 'Transmit IR'
    description = Text.transmitDesc

    def __call__(self, mesg, repeat, repeatDelay):
        prontoDetected = False
        prontoC = ""
        mesg = eg.ParseString(mesg)
        codes = mesg.split()

        if (codes[0] == 'K'):
            codes.remove('K')

        learnedCode = int(codes[0], 16)
        frequency = int(codes[1], 16)

        if (
            learnedCode == 0    #It is a learned Code
            and 
            frequency <= 115    #36kHz or higher
            and
            frequency >= 103    #40kHz or lower
        ):
            prontoDetected = True
            print Text.freqtxt, 1000000/(frequency * .241246), " Hz"
            prontoC = self.plugin.convertFromPronto(mesg)
            prontoC = self.plugin.averageThis(prontoC)
            self.plugin.Send(prontoC, repeat, repeatDelay)
        else:
            prontoDetected = False

        if not prontoDetected:
            try:
                info = codes.pop(0)
                frequency = int(info[:2], 16)
                numpairs = int(info[2:], 16)

                if (
                    len(codes) == (numpairs * 2)
                    and
                    codes[len(codes) - 1] == '2000'
                ):
                    if (mesg.find('K') != -1):
                        self.plugin.Send(mesg, repeat, repeatDelay)
                    else:
                        self.plugin.Send('K ' + mesg, repeat, repeatDelay)
                else:
                    raise self.Exception()
            except:
                raise self.Exception('IR code does not conform to protocol')
    

    def Configure(self, mesg = '', repeat = 3, repeatDelay = 0.20):
        text = self.text
        panel = eg.ConfigPanel(self)
        st1 = panel.StaticText(text.repeat)
        mySizer_1 = wx.GridBagSizer(10, 10)


        def StartLearnIR(learnThreadEvent):
            learnButton.Enable(False)
            panel.dialog.buttonRow.okButton.Enable(False)
            panel.dialog.buttonRow.testButton.Enable(False)
            panel.dialog.buttonRow.applyButton.Enable(False)
            panel.dialog.buttonRow.cancelButton.Enable(False)
            acceptBurstButton.Enable(True)
            print Text.Transmit.irLearnStarted
            prev_capturedCode = ''
            while not learnThreadEvent.isSet():
                capturedCode = str(eg.event.payload)
                if capturedCode != prev_capturedCode:
                    prev_capturedCode = capturedCode
                    capList = capturedCode.split(" ")
                    if capList[len(capList) - 1] == '2000':
                        textControl.SetValue("K " + capturedCode)
                        panel.dialog.buttonRow.applyButton.Enable(False)
    
    
        def OnAcceptBurst(event):
            learnButton.Enable(True)
            panel.dialog.buttonRow.okButton.Enable(True)
            panel.dialog.buttonRow.testButton.Enable(True)
            panel.dialog.buttonRow.applyButton.Enable(True)
            panel.dialog.buttonRow.cancelButton.Enable(True)
            acceptBurstButton.Enable(False)
            print Text.Transmit.irBurstAccepted
            self.learnThreadEvent.set()
            
            
        def LearnIR(event):
            self.learnThreadEvent = Event()
            learnThread = Thread(
                target=StartLearnIR,
                args=(self.learnThreadEvent,)
            )
            learnThread.start()


        repeatCtrl = panel.SpinIntCtrl(repeat, max = 99)

        repeatDelayCtrl = panel.SpinNumCtrl(
            repeatDelay,
            decimalChar = '.', # by default, use '.' for decimal point
            groupChar = ',',   # by default, use ',' for grouping
            fractionWidth = 2,
            integerWidth = 2,
            min = 0.01,
            max = 99.99,
            increment = 0.01
        )
        repeatDelayCtrl.SetInitialSize((60,-1))
        
        textControl = wx.TextCtrl(
            panel, 
            -1, 
            mesg, 
            style = wx.TE_MULTILINE
        )

        repeatBox = panel.BoxedGroup(
            text.repeatBox, 
            (st1, repeatCtrl) 
        )

        learnButton = panel.Button(text.learnButton)
        learnButton.Enable(True)
        acceptBurstButton = panel.Button(text.acceptBurstButton)
        acceptBurstButton.Enable(False)
        
        mySizer_1.Add(wx.StaticText(panel, -1, text.repeatDelay), (0,0))
        mySizer_1.Add(repeatDelayCtrl, (1,0))

        panel.sizer.Add(textControl, 1, wx.EXPAND)
        panel.sizer.Add(repeatBox, 0, wx.TOP|wx.EXPAND, 10)
        panel.sizer.Add(mySizer_1, 0, wx.TOP|wx.EXPAND, 10)       
        panel.sizer.Add(learnButton, 0, wx.TOP|wx.EXPAND, 10)       
        panel.sizer.Add(acceptBurstButton, 0, wx.TOP|wx.EXPAND, 10)       
        
        learnButton.Bind(wx.EVT_BUTTON, LearnIR)
        acceptBurstButton.Bind(wx.EVT_BUTTON, OnAcceptBurst)

        while panel.Affirmed():
            panel.SetResult(
                textControl.GetValue().strip(' \n\r'),
                repeatCtrl.GetValue(),
                repeatDelayCtrl.GetValue()
            )



class Discover(eg.ActionClass):
    name = 'Discover devices'
    description = Text.discoverDesc
    
    def __call__(self):
            outsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            insock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            outsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            outsock.sendto('disD', ("255.255.255.255", 30303))
            insock.bind(("0.0.0.0", 30303))
            rawdata, client_addr = insock.recvfrom(4096)
            print rawdata
            outsock.close()
            insock.close()
    





eg.RegisterPlugin(
    name = 'Keene IR Anywhere',
    author = 'ldobson',
    version = '1.0.3',
    kind = 'remote',
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
            If you are talking to multiple units it's best to have
            them all set to different ports and then load this plugin
            multiple times and set each event prefix to something
            different. If you load it multiple times and don't
            have different port numbers then you will be confused as to 
            which unit you are receiving information from, as only one
            of the plugin instances will be able to listen on that port
        </p>
        <p>
            Events that can occur (assuming "KIRA" is your event prefix):
            <ul>
                <li>
                    <b>KIRA.Acknowledgment</b> - 
                    Happens when a unit sends an "ACK" response to an action
                </li>
                <li>
                    <b>KIRA.ReceivedIR</b> - 
                    Happens when we receive an IR stream from a unit. The 
                    stream can be found in {eg.ReceivedIR} for use in actions
                </li>.
                <li>
                    <b>KIRA.XXXXXX.DDDDDDDD</b> - 
                    Also happens when we receive an IR stream, this one
                    is the decoded IR that can be used to pick up on
                    subsequent presses of the same button. "XXXXXX" is the
                    IR protocol (it's not uncommon to see this as "Unknown"
                    so don't panic!) and "DDDDDDDD" is the code itself.
                </li>
            </ul>
            <p>
                If you switch on "Log incoming raw IR streams", the IR streams
                will also be printed in the log window in the format:
            </p>
            <p>
                <div align="center">
                    <b>KIRA.Raw.XXYY DDDD DDDD DDDD 2000</b>
                </div>
            </p>
        </p>
    '''
)

import asyncore, socket

class Text:
    host = 'Host:'
    port = 'UDP Port:'
    eventPrefix = 'Event Prefix:'
    ipBox = 'IP Settings'
    eventBox = 'Event generation'
    logRaw = 'Log incoming raw IR streams'
    transmitDesc = '''\
        <p>
            Transmits an IR code via the IR Anywhere hardware
        </p>

        <p>
            Remove the leading "KIRA.Raw." from the logged 
            incoming raw IR streams before using them 
            (where "KIRA" is your event prefix)
        </p>
        <p>
            Remove the leading "K " from IR streams that
            you have learned with the Keene software
        </p>
        <p>
            A valid code looks like this: 
        </p>
        <p>
            <div align="center">
                <b>XXYY DDDD DDDD DDDD 2000</b>
            </div>
        </p>
        <p>
            where "XX" is the frequency, "YY" is the number of 
            following pairs, "DDDD" is the data (there will be an 
            odd number of these chunks), and "2000" is hard-coded
        </p>
        <p>
            You can use "{eg.ReceivedIR}" to use the last IR stream
            that the plugin has received. This is useful in
            conjunction with the "KIRA.ReceivedIR" event. Note that
            if you're sending a stream to the unit it came from then
            it is advisable to leave a pause of at least 0.2 seconds
            before the TransmitIR action
        </p>
    '''
    sendToMeDesc = (
        'Sets destination address 2 (PC) address to this '
        'PCs IP address and switches on "Attempt to locate PC"'
    )
    targetDesc = 'Sets the unit to Target mode'
    receiverDesc = 'Sets the unit to Receiver mode'
    standaloneDesc = 'Sets the unit to Stand-alone mode'

class KIRA(eg.PluginClass):
    canMultiLoad = True
    text = Text

    def __init__(self):
        self.AddAction(Transmit)
        self.AddAction(SendToMe)
        self.AddAction(SetAsTarget)
        self.AddAction(SetAsReceiver)
        self.AddAction(SetAsStandAlone)
        self.irDecoder = eg.IrDecoder(self, 1)

    def __close__(self):
        self.irDecoder.Close()

    def __start__(self, host, port, prefix, logRaw):
        self.host = host
        self.port = port
        self.info.eventPrefix = prefix
        self.logRaw = logRaw
        try:
            self.server = Server(self.port, self)
        except socket.error, exc:
            raise self.Exception(exc[1])

    def __stop__(self):
        if self.server:
            self.server.close()
        self.server = None

    def Configure(
        self, 
        host = 'standalone', 
        port = 65432, 
        prefix = 'KIRA',
        logRaw = True
    ):
        text = self.text
        panel = eg.ConfigPanel(self)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max = 65535)
        eventPrefixCtrl = panel.TextCtrl(prefix)
        logRawCtrl = panel.CheckBox(logRaw, text.logRaw)

        st1 = panel.StaticText(text.host)
        st2 = panel.StaticText(text.port)
        st3 = panel.StaticText(text.eventPrefix)
        eg.EqualizeWidths((st1, st2, st3))

        ipBox = panel.BoxedGroup(
            text.ipBox,
            (st1, hostCtrl),
            (st2, portCtrl),
        )

        eventBox = panel.BoxedGroup(
            text.eventBox, 
            (st3, eventPrefixCtrl, logRawCtrl) 
        )

        panel.sizer.Add(ipBox, 0, wx.EXPAND)
        panel.sizer.Add(eventBox, 0, wx.TOP|wx.EXPAND, 10)

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(), 
                portCtrl.GetValue(), 
                eventPrefixCtrl.GetValue(), 
                logRawCtrl.GetValue()
            )

    def Send(self, mesg):
        self.server.sendto(mesg, (self.host, self.port))

class Transmit(eg.ActionClass):
    name = 'Transmit IR'
    description = Text.transmitDesc

    def __call__(self, mesg):
        mesg = eg.ParseString(mesg)
        codes = mesg.split()
        try:
            info = codes.pop(0)
            frequency = int(info[:2], 16)
            numpairs = int(info[2:], 16)
            data = [int(i, 16) for i in codes]
            if (
                len(codes) == (numpairs * 2)
                and
                codes[len(codes) - 1] == '2000'
            ):
                self.plugin.Send('K ' + mesg)
            else:
                raise self.Exception()
        except:
            raise self.Exception('IR code does not conform to protocol')

    def Configure(self, mesg = ''):
        panel = eg.ConfigPanel(self)
        textControl = wx.TextCtrl(
            panel, 
            -1, 
            mesg, 
            style = wx.TE_MULTILINE
        )
        panel.sizer.Add(textControl, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControl.GetValue())

class SendToMe(eg.ActionClass):
    name = 'Send to me'
    description = Text.sendToMeDesc

    def __call__(self):
        self.plugin.Send('cmdI')

class SetAsTarget(eg.ActionClass):
    name = 'Set as Target'
    description = Text.targetDesc

    def __call__(self):
        self.plugin.Send('cmdM1')

class SetAsReceiver(eg.ActionClass):
    name = 'Set as Receiver'
    description = Text.receiverDesc

    def __call__(self):
        self.plugin.Send('cmdM0')

class SetAsStandAlone(eg.ActionClass):
    name = 'Set as Stand-alone'
    description = Text.standaloneDesc

    def __call__(self):
        self.plugin.Send('cmdM2')

class Server(asyncore.dispatcher):

    def __init__(self, port, handler):
        self.handler = handler
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bind(('', port))
        self.add_channel()
        eg.RestartAsyncore()

    def handle_read(self):
        try:
            rawdata, client_addr = self.socket.recvfrom(1024)

            codes = rawdata.split()
            if (codes[0] == 'K'):
                codes.remove('K')

                eg.ReceivedIR = ' '.join(codes)

                if (self.handler.logRaw):
                    print(
                        self.handler.info.eventPrefix + 
                        '.Raw.' + eg.ReceivedIR
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
                        self.handler.TriggerEvent('ReceivedIR')
                        self.handler.irDecoder.Decode(data, len(data))

                    else:
                        raise self.handler.Exception()
                except:
                    print 'Malformed incoming IR code'

            elif (codes[0] == 'ACK'):
                self.handler.TriggerEvent('Acknowledgement')
                
        except socket.timeout:
            pass

        except socket.error, (errno, strerror):
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

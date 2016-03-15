eg.RegisterPlugin(
    name = 'Keene IR Anywhere',
    author = 'ldobson',
    version = '1.0.5',
    kind = 'remote',
    guid = "{695FA442-24CE-4D82-B38B-8A772BBEA8FD}",
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
            If you are talking to multiple units and they are using the
            same port then make sure you only start one server on that
            port. Otherwise you will be confused as to which unit you are
            receiving information from, as only one of the plugin instances
            will be able to listen on that port.
        </p>
        <p>
            The plugin supports one event:
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
        </p>
    '''
)

import asyncore, socket

class Text:
    host = 'Host:'
    port = 'UDP Port:'
    svr = 'Start a server on this port'
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
            You can use:
        </p>
        <p>
            <div align="center">
                <b>{eg.event.payload}</b>
            </div>
        </p>
        <p>
            to use the IR stream that triggered the current KIRA event
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

    def __start__(self, host, port, svr, prefix, logRaw):
        self.host = host
        self.port = port
        self.svr = svr
        self.info.eventPrefix = prefix
        self.logRaw = logRaw
        if (self.svr):
            try:
                self.server = Server(self.port, self)
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
        host = 'standalone',
        port = 65432,
        svr = True,
        prefix = 'KIRA',
        logRaw = True
    ):
        text = self.text
        panel = eg.ConfigPanel(self)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max = 65535)
        svrCtrl = panel.CheckBox(svr, text.svr)
        eventPrefixCtrl = panel.TextCtrl(prefix)
        logRawCtrl = panel.CheckBox(logRaw, text.logRaw)

        st1 = panel.StaticText(text.host)
        st2 = panel.StaticText(text.port)
        st3 = panel.StaticText(text.eventPrefix)
        eg.EqualizeWidths((st1, st2, st3))

        ipBox = panel.BoxedGroup(
            text.ipBox,
            (st1, hostCtrl),
            (st2, portCtrl, svrCtrl),
        )

        eventBox = panel.BoxedGroup(
            text.eventBox,
            (st3, eventPrefixCtrl, logRawCtrl)
        )

        panel.sizer.Add(ipBox, 0, wx.EXPAND)
        panel.sizer.Add(eventBox, 0, wx.TOP|wx.EXPAND, 10)

        eventPrefixCtrl.Enable(svrCtrl.IsChecked())
        logRawCtrl.Enable(svrCtrl.IsChecked())

        def OnCheckBox(event):
            eventPrefixCtrl.Enable(svrCtrl.IsChecked())
            logRawCtrl.Enable(svrCtrl.IsChecked())
            event.Skip()

        svrCtrl.Bind(wx.EVT_CHECKBOX, OnCheckBox)

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                svrCtrl.GetValue(),
                eventPrefixCtrl.GetValue(),
                logRawCtrl.GetValue()
            )

    def Send(self, mesg):
        if (self.server):
            self.server.sendto(mesg, (self.host, self.port))
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', self.port))
            sock.sendto(mesg, (self.host, self.port))
            sock.close()

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

                rawCode = ' '.join(codes)

                if (self.handler.logRaw):
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

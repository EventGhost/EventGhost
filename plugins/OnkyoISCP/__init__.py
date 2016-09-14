import eg
import socket
import select
from time import sleep
from threading import Event, Thread
from struct import pack, unpack

eg.RegisterPlugin(
    name = "Onkyo ISCP",
    author = (
        "Alexander Hartmaier",
        "Sem;colon",
    ),
    version = "0.06",
    kind = "external",
    guid = "{5B3B8AEB-08D7-4FD0-8BEE-8FE50C231E09}",
    description = "Controls any Onkyo Receiver which supports the ISCP protocol.",
    url = "http://www.eventghost.org/forum/viewtopic.php?f=10&t=2964",
)

class Text:
    tcpBox = "TCP/IP Settings"
    ip = "IP:"
    port = "Port:"
    timeout = "Timeout:"
    class SendCommand:
        commandBox = "Command Settings"
        command = "Code to send:"

class OnkyoISCP(eg.PluginBase):
    text       = Text
    header     = 'ISCP'
    headersize = 16
    version    = 1
    unittype   = 1 # receiver

    def __init__(self):
        self.AddAction(SendCommand)

    def __start__(self, ip, port, timeout):
        self.ip = ip
        self.port = int(port)
        self.timeout = float(timeout)
        self.Connect()

    def __stop__(self):
        if hasattr(self, 'stopThreadEvent'):
            self.stopThreadEvent.set()

        self.socket.close()

    def Receive(self):
        while not self.stopThreadEvent.is_set():
            try:
                ready = select.select([self.socket], [], [])
                # the first element of the returned list is a list of readable sockets
                if ready[0]:
                    # 1024 bytes should be enough for every received event
                    reply = self.socket.recv(1024)
                    # unpack ISCP header
                    header, headersize, datasize, version = unpack(
                        '!4sIIBxxx',
                        reply[0:self.headersize]
                    )

                    if header != self.header:
                        self.PrintError("OnkyoISCP: Received packet not ISCP")
                        return
                    if version != self.version:
                        self.PrintError("OnkyoISCP: ISCP version " + str(version) + " not supported")
                        return

                    #print "Header: " + header
                    #print "Header size: " + str(headersize)
                    #print "Data size: " + str(datasize)
                    #print "Version: " + str(version)

                    # message ends in EOL CR LF, is three chars shorter than data size
                    message = reply[headersize:headersize+datasize].rstrip('\x1a\r\n')
                    #print "Message: " + message
                    messagesize = len(message)

                    # parse message
                    #unittype = message[1]
                    #print "Unit type: " + unittype
                    command = message[2:5]
                    parameter = message[5:messagesize]
                    self.TriggerEvent(command, payload=parameter)
                    self.TriggerEvent(command + parameter)
            except Exception as e:
                self.PrintError("OnkyoISCP: " + str(e))

    def Connect(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(self.timeout)
        self.socket = s

        ip = self.ip
        port = self.port
        try:
            s.connect((ip, port))
        except Exception as e:
            self.PrintError("OnkyoISCP: Failed to connect to " + ip + ":" + str(port) + ": " + str(e))
        else:
            print "Connected to " + ip + ":" + str(port)
        self.stopThreadEvent = Event()
        thread = Thread(
            target = self.Receive,
        )
        thread.start()


    def Configure(self, ip="", port="60128", timeout="1"):
        text = self.text
        panel = eg.ConfigPanel()
        wx_ip = panel.TextCtrl(ip)
        wx_port = panel.SpinIntCtrl(port, max=65535)
        wx_timeout = panel.TextCtrl(timeout)

        st_ip = panel.StaticText(text.ip)
        st_port = panel.StaticText(text.port)
        st_timeout = panel.StaticText(text.timeout)
        eg.EqualizeWidths((st_ip, st_port, st_timeout))

        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (st_ip, wx_ip),
            (st_port, wx_port),
            (st_timeout, wx_timeout),
        )

        panel.sizer.Add(tcpBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                wx_ip.GetValue(),
                wx_port.GetValue(),
                wx_timeout.GetValue(),
            )

class SendCommand(eg.ActionBase):

    def __call__(self, Command):
        message = '!' + str(self.plugin.unittype) + Command + '\x0d'
        # unlike specified the datasize needs to include the headersize
        # to make it work for some models (Integra DHC-9.9)
        # while others (Onkyo PR-SC5507) work fine without it
        # both work when the headersize is included
        datasize = self.plugin.headersize + len(message)
        line = pack('!4sIIBxxx',
            self.plugin.header,
            self.plugin.headersize,
            datasize,
            self.plugin.version
        ) + message
        try:
            self.plugin.socket.sendall(line)
            sleep(0.1)
        except socket.error, msg:
            self.PrintError("OnkyoISCP: Error sending command, retrying: " + msg)
            # try to reopen the socket on error
            # happens if no commands are sent for a long time
            # and the tcp connection got closed because
            # e.g. the receiver was switched off and on again
            self.plugin.Connect()
            try:
                self.plugin.socket.sendall(line)
            except socket.error, msg:
                self.PrintError("OnkyoISCP: Error sending command: " + msg)

    def Configure(self, Command=""):
        panel = eg.ConfigPanel()
        text = self.text
        st_command = panel.StaticText(text.command)
        wx_command = panel.TextCtrl(Command)

        commandBox = panel.BoxedGroup(
            text.commandBox,
            (st_command, wx_command)
        )

        panel.sizer.Add(commandBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(wx_command.GetValue())

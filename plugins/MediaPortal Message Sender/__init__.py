
import eg

eg.RegisterPlugin(
    name = "MediaPortal Message Sender",
    guid='{961E62BD-F111-4CC8-9EAC-077EE397E7A6}',
    version = "1.03",
    author = "Da BIG One",
	kind = "program",
    createMacrosOnAdd = True,
    description = ('Sends messages to MediaPortal''s EventGhostPlus Plugin.<br\n>'
	'Use with <A HREF=http://www.team-mediaportal.com/extensions/input-output/eventghostplus>EventGhostPlus plugin for MediaPortal</A>'
    '<br\n><br\n>'
    '<center><img src="MediaPortal_EG.png" /></center>'),
    url = "http://forum.team-mediaportal.com/threads/eventghostplus.113463/"
)

import wx
import socket
import asynchat
import asyncore
import random
from hashlib import md5

class Text:
        TCPBox = "TCP/IP Settings"
        HostText = "Host: "
        PortText = "Port: "
        SecurityBox = "Security"
        PassText = "Password: "
        MessageBox = "Message"
        HeaderText = "Message header: "
        FirstText = "Message (1st line): "
        SecondText = "Message (2nd line): "
        TimeoutText = "Message timeout: "
        ImageText = "Image location: Leave blank for the EventGhost image.\n(Be sure your MediaPortal client has access to the file)"
        ButtonBox = "Send Remote Button"
        ButtonText = "Button Label: "
        RemoteBox = "MediaPortal Connection Settings"
        LocalBox = "Local Connection Settings"
        LTCPBox = "Local Connection Settings"
        LSecurityBox = "Local Security Settings"
        EventBox = "Event Settings"
        PrefixText = "Prefix: "
        IPPreText = "Source IP as Prefix: "
        class SendMessage:
            name = "Send Message"
            description = "Send a Pop-Up Message"
        class SendRemoteButton:
            name = "Send Remote Button"
            description = "Send Remote Control Button Label"

class MPMessageSender(eg.PluginBase):

    text = Text
    
    def __init__(self):

        self.CONNECTION = CONNECTION(self)

        self.AddAction(SendMessage)
        self.AddAction(SendRemoteButton)
        self.AddActionsFromList(ACTION)

        self.Server = False


    def __start__(self, host, port, pswd, localPort, localPswd, prefix, ipPrefix):


        self.CONNECTION.Default(host, port, pswd)

        self.localPort = localPort
        self.localPswd = localPswd
        self.ipPrefix = ipPrefix
        self.prefix = prefix
        self.info.eventPrefix = prefix
        try:
            self.server = Server(self)
        except socket.error, exc:
            raise self.Exception(exc[1])

    def __stop__(self):
        if self.server:
            self.server.close()
        self.server = None


    def Configure(
                self,
                host=False,
                port=0,
                pswd=False,
                localPort=1024,
                localPswd="",
                prefix = "MediaPortal",
                ipPrefix=False
                ):
        text = self.text
        panel = eg.ConfigPanel()

        host, port, pswd = self.CONNECTION.Config(host, port, pswd)

        def Toggle(flag):
            flag = False if flag else True
            return flag

        st1 = panel.TextCtrl(host)
        st2 = panel.SpinIntCtrl(port, max=65535)
        st3 = panel.TextCtrl(pswd, style=wx.TE_PASSWORD)
        st4 = panel.SpinIntCtrl(localPort, max=65535)
        st5 = panel.TextCtrl(localPswd, style=wx.TE_PASSWORD)
        st6 = panel.TextCtrl(prefix)
        st7 = panel.CheckBox(ipPrefix)

        st6.Enable(Toggle(ipPrefix))

        def OnCheckBox(event):
            st6.Enable(Toggle(st7.GetValue()))
        st7.Bind(wx.EVT_CHECKBOX, OnCheckBox)

        eg.EqualizeWidths((st1, st2, st3, st4, st5, st6, st7))

        box1 = panel.BoxedGroup(
                                text.TCPBox,
                                (text.HostText, st1),
                                (text.PortText, st2)
                                )
        box2 = panel.BoxedGroup(
                                text.SecurityBox,
                                (text.PassText, st3)
                                )
        box3 = panel.BoxedGroup(
                                text.TCPBox,
                                (text.PortText, st4)
                                )
        box4 = panel.BoxedGroup(
                                text.SecurityBox,
                                (text.PassText, st5)
                                )
        box5 = panel.BoxedGroup(
                                text.EventBox,
                                (text.PrefixText, st6),
                                (text.IPPreText, st7)
                                )

        box6 = panel.BoxedGroup(
                                text.RemoteBox,
                                box1,
                                box2
                                )
        box7 = panel.BoxedGroup(
                                text.LocalBox,
                                box3,
                                box4,
                                box5
                                )

        panel.sizer.AddMany([
                            (box6, 0, wx.EXPAND),
                            (box7, 0, wx.EXPAND)
                            ])


        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue(),
                            st3.GetValue(),
                            st4.GetValue(),
                            st5.GetValue(),
                            st6.GetValue(),
                            st7.GetValue()
                            )

    def Send(self, header, firstline, secondline, timeout, imagelocation, host, port, pswd):

        res = True
        errorText = "MediaPortalMessageSender: Missing "

        host, port, pswd = self.CONNECTION.Check(host, port, pswd)

        if not host: errorText += "IP Address"
        if not port: errorText += "Port Number"
        if isinstance(pswd, bool): errorText += "Password"

        if errorText != "MediaPortalMessageSender: Missing ":
            eg.PrintError(errorText)
            return False

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(1.0)

        try:
            sock.connect((host, port))
        except:
            #eg.PrintTraceback()
            errorText = "MediaPortalMessageSender: Connection Failed: MediaPortal not running?!"
            errorText += host+", "+str(port)
            self.PrintNotice(errorText)
            return False

        sock.settimeout(1.0)
        sock.sendall("quintessence\n\r")

        cookie = sock.recv(128)
        cookie = cookie.strip()
        token = cookie + ":" + pswd
        digest = md5(token).hexdigest()
        digest = digest + "\n"
        sock.sendall(digest)

        answer = sock.recv(512)

        if answer.strip() == "accept":
            sock.sendall("payload " + header.encode(eg.systemEncoding) + "\n")
            sock.sendall("payload " + firstline.encode(eg.systemEncoding) + "\n")
            sock.sendall("payload " + secondline.encode(eg.systemEncoding) + "\n")
            sock.sendall("payload " + str(timeout).encode(eg.systemEncoding) + "\n")
            sock.sendall("payload " + imagelocation.encode(eg.systemEncoding) + "\n")
            sock.sendall("MediaPortal.Message\n")
            sock.sendall("close\n")
            sock.close()
            return True

        else:
            self.PrintNotice("MediaPortalMessageSender: Connection Failed: Incorrect Password?!")
            sock.close()
            return False

class SendMessage(eg.ActionWithStringParameter):
        
    text = Text

    def __call__(self, header, firstline, secondline, timeout, imagelocation, host=False, port=False, pswd=False):

        return self.plugin.Send(
                            eg.ParseString(header),
                            eg.ParseString(firstline),
                            eg.ParseString(secondline),
                            timeout,
                            eg.ParseString(imagelocation),
                            host,
                            port,
                            pswd
                            )
		
    def Configure(
                self,
                header="EventGhostPlus Message",
                firstline="",
                secondline="",
                timeout=60,
                imagelocation="",
                host=False,
                port=0,
                pswd=False
                ):

        text = self.text
        panel = eg.ConfigPanel()

        host, port, pswd = self.plugin.CONNECTION.Config(host, port, pswd)

        st1 = panel.TextCtrl(header)
        st2 = panel.TextCtrl(firstline)
        st3 = panel.TextCtrl(secondline)
        st4 = panel.SpinIntCtrl(timeout, max=3600)
        st5 = panel.TextCtrl(imagelocation)
        st6 = panel.TextCtrl(host)
        st7 = panel.SpinIntCtrl(port, max=65535)
        st8 = panel.TextCtrl(pswd, style=wx.TE_PASSWORD)

        eg.EqualizeWidths((st1, st2, st3, st4, st5, st6, st7, st8))

        box1 = panel.BoxedGroup(
                                text.MessageBox,
                                (text.HeaderText, st1),
                                (text.FirstText, st2),
                                (text.SecondText, st3),
                                (text.TimeoutText, st4),
                                (text.ImageText, st5)
                                )
        box2 = panel.BoxedGroup(
                                text.TCPBox,
                                (text.HostText, st6),
                                (text.PortText, st7)
                                )
        box3 = panel.BoxedGroup(
                                text.SecurityBox,
                                (text.PassText, st8)
                                )
        panel.sizer.AddMany([
                            (box1, 0, wx.EXPAND),
                            (box2, 0, wx.EXPAND),
                            (box3, 0, wx.EXPAND)
                            ])

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue(),
                            st3.GetValue(),
                            st4.GetValue(),
                            st5.GetValue(),
                            st6.GetValue(),
                            st7.GetValue(),
                            st8.GetValue()
                            )

class SendRemoteButton(eg.ActionBase):

    text = Text

    def __call__(self, button, host=False, port=False, pswd=False):

        for CommandGroup in ACTION:
            for Command in CommandGroup[4]:
                if button == Command[4][0]:
                    return self.plugin.Send(
                                eg.ParseString("EG+BtnSnd"),
                                eg.ParseString(Command[4][0]),
                                eg.ParseString(""),
                                Command[4][1],
                                eg.ParseString(""),
                                host,
                                port,
                                pswd
                                )
            
    def Configure(self, button="Empty", host=False, port=False, pswd=False):

        text = self.text
        panel = eg.ConfigPanel()
        choices = []
        
        host, port, pswd = self.plugin.CONNECTION.Config(host, port, pswd)

        st1 = wx.Choice(parent=panel, pos=(10,10))
        st2 = panel.TextCtrl(host)
        st3 = panel.SpinIntCtrl(port, max=65535)
        st4 = panel.TextCtrl(pswd, style=wx.TE_PASSWORD)

        for CommandGroup in ACTION:
            for Command in CommandGroup[4]:
                choices.append(Command[4][0])

        st1.AppendItems(items=choices)

        if choices.count(button)==0:
            st1.Select(n=0)
        else:
            st1.SetSelection(int(choices.index(button)))

        eg.EqualizeWidths((st1, st2, st3, st4))

        box1 = panel.BoxedGroup(
                                text.ButtonBox,
                                (text.ButtonText, st1)
                                )
        box2 = panel.BoxedGroup(
                                text.TCPBox,
                                (text.HostText, st2),
                                (text.PortText, st3)
                                )
        box3 = panel.BoxedGroup(
                                text.SecurityBox,
                                (text.PassText, st4)
                                )
        panel.sizer.AddMany([
                            (box1, 0, wx.EXPAND),
                            (box2, 0, wx.EXPAND),
                            (box3, 0, wx.EXPAND)
                            ])

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetStringSelection(),
                            st2.GetValue(),
                            st3.GetValue(),
                            st4.GetValue()
                            )

class SendRemoteButFunc(eg.ActionBase):

    def __call__(self, host=False, port=False, pswd=False):

        return self.plugin.Send(
                                eg.ParseString("EG+BtnSnd"),
                                eg.ParseString(self.value[0]),
                                eg.ParseString(""),
                                self.value[1],
                                eg.ParseString(""),
                                host,
                                port,
                                pswd
                                )


    def Configure(self, host=False, port=0, pswd=False):

        panel = eg.ConfigPanel()

        host, port, pswd = self.plugin.CONNECTION.Config(host, port, pswd)
        
        st1 = panel.TextCtrl(host)
        st2 = panel.SpinIntCtrl(port, max=65535)
        st3 = panel.TextCtrl(pswd, style=wx.TE_PASSWORD)

        eg.EqualizeWidths((st1, st2, st3))

        box1 = panel.BoxedGroup(
                                'TCP/IP Settings',
                                ('Host Name: ', st1),
                                ('Port: ', st2)
                                )
        box2 = panel.BoxedGroup(
                                'Security Settings',
                                ('Password: ', st3)
                                )
        panel.sizer.AddMany([
                            (box1, 0, wx.EXPAND),
                            (box2, 0, wx.EXPAND),
                            ])

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue(),
                            st3.GetValue(),
                            )
class CONNECTION():

    def __init__(self, plugin):

        self.plugin = plugin
        self.host = False
        self.port = False
        self.pswd = False

    def Default(self, host, port, pswd):

        errorText = "MediaPortal Message Sender: Missing "

        self.host,self.port,self.pswd = self.Check(host,port,pswd)

        if not self.host: errorText += "IP Address"
        if not self.port: errorText += "Port Number"
        if isinstance(self.pswd, bool): errorText += "Password"

        if errorText != "MediaPortal Message Sender: Missing ":
            eg.PrintError(errorText)

    def Config(self, host, port, pswd):

        host,port,pswd = self.Check(host,port,pswd)

        host = host if host and host != "" \
                else self.host if self.host and self.host != "" \
                else "999.999.999.999"
        port = port if port and port != 0 \
                else self.port if self.port and self.port != 0 \
                else 0
        pswd = pswd if pswd or pswd == "" \
                else self.pswd if self.pswd or self.pswd == ""\
                else "SamplePassword"

        return host, port, pswd

    def Check(self, host, port, pswd):

        host = host if host and host != "" and host != "999.999.999.999" \
                else self.host if self.host and self.host != "" and self.host != "999.999.999.999" \
                else False
        port = port if port and port != 0 \
                else self.port if self.port and self.port != 0 \
                else False
        pswd = pswd if (pswd or pswd == "") and pswd != "SamplePassword" \
                else self.pswd if (self.pswd or self.pswd == "") and self.pswd != "SamplePassword" \
                else False
        return host, port, pswd

class ServerHandler(asynchat.async_chat):

    def __init__(self, sock, addr, plugin, server):

        self.plugin = plugin

        asynchat.async_chat.__init__(self, sock)

        self.set_terminator('\n')

        self.data = ''
        self.state = self.state1
        self.sourceIP = addr[0]
        self.payload = [self.sourceIP]

    def handle_close(self):
        self.plugin.EndLastEvent()
        asynchat.async_chat.handle_close(self)

    def collect_incoming_data(self, data):
        self.data = self.data + data

    def found_terminator(self):
        
        line = self.data
        self.data = ''
        self.state(line)

    def initiate_close(self):
        if self.writable():
            self.push("close\n")
        self.plugin.EndLastEvent()
        self.state = self.state1

    def state1(self, line):

        self.cookie = hex(random.randrange(65536))
        self.cookie = self.cookie[len(self.cookie) - 4:]
        self.hex_md5 = md5(self.cookie + ":" + self.plugin.localPswd).hexdigest().upper()


        if line == "quintessence":
            self.state = self.state2
            self.push(self.cookie + "\n")
        else:
            self.initiate_close()

    def state2(self, line):
        
        line = line.strip()[-32:]
        if line == "":
            pass
        elif line.upper() == self.hex_md5:
            self.push("accept\n")
            self.state = self.state3
        else:
            eg.PrintError("NetworkReceiver md5 error")
            self.initiate_close()

    def state3(self, line):
        line = line.decode(eg.systemEncoding)
        if line == "close":
            self.initiate_close()
        elif line[:8] == "payload ":
            self.payload.append(line[8:])
        else:
            kwargs = dict(
                        prefix=self.sourceIP.replace(".",",")+'.MediaPortal' \
                                    if self.plugin.ipPrefix \
                                    else self.plugin.prefix,
                        suffix=line[12:],
                        payload=self.payload
                        )

            eg.TriggerEvent(**kwargs)
            self.payload = [self.sourceIP]

class Server(asyncore.dispatcher):

    def __init__ (self, handler):
       
        self.handler = handler
        
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        eg.RestartAsyncore()

        self.bind(('', handler.localPort))

        self.listen(5)

    def handle_accept (self):

        (sock, addr) = self.accept()
        ServerHandler(
            sock,
            addr,
            self.handler,
            self
        )

ACTION = (
    (eg.ActionGroup, 'Volume', 'Volume Keys', 'Volume Keys ',(
        (SendRemoteButFunc, 'fnVOLUP', 'VolumeUp', 'VolumeUp', ['VolumeUp', 16]),
        (SendRemoteButFunc, 'fnVOLDOWN', 'VolumeDown', 'VolumeDown', ['VolumeDown', 17]),
        (SendRemoteButFunc, 'fnMUTE', 'Mute', 'Mute', ['Mute', 14])
        )),
    (eg.ActionGroup, 'Channel', 'Channel Keys', 'Channel Keys ',(
        (SendRemoteButFunc, 'fnCHNUP', 'ChannelUp', 'ChannelUp', ['ChannelUp', 18]),
        (SendRemoteButFunc, 'fnCHNDOWN', 'ChannelDown', 'ChannelDown', ['ChannelDown', 19]),
        )),
    (eg.ActionGroup, 'MediaControl', 'Media Control Keys', 'Media Control Keys ',(
        (SendRemoteButFunc, 'fnFASTFORWARD', 'FastForward', 'FastForward', ['Forward', 20]),
        (SendRemoteButFunc, 'fnREWIND', 'Rewind', 'Rewind', ['Rewind', 21]),
        (SendRemoteButFunc, 'fnPLAY', 'Play', 'Play', ['Play', 22]),
        (SendRemoteButFunc, 'fnRECORD', 'Record', 'Record', ['Record', 23]),
        (SendRemoteButFunc, 'fnPAUSE', 'Pause', 'Pause', ['Pause', 24]),
        (SendRemoteButFunc, 'fnSTOP', 'Stop', 'Stop', ['Stop', 25]),
        (SendRemoteButFunc, 'fnSKIPFORWARD', 'Skip Forward', 'Skip Forward', ['Skip', 26]),
        (SendRemoteButFunc, 'fnSKIPBACK', 'Skip Back', 'Skip Back', ['Replay', 27])
        )),
    (eg.ActionGroup, 'OEM', 'OEM Keys', 'OEM Keys ',(
        (SendRemoteButFunc, 'fnOEMGATE', 'OemGate', 'OemGate', ['OemGate', 28]),
        (SendRemoteButFunc, 'fnOEM8', 'Oem8', 'Oem8', ['Oem8', 29])
        )),
    (eg.ActionGroup, 'Numbers', 'Numeric Keys', 'Numeric Keys ',(
        (SendRemoteButFunc, 'fnNUM1', 'NumPad1', 'NumPad1', ['NumPad1', 1]),
        (SendRemoteButFunc, 'fnNUM2', 'NumPad2', 'NumPad2', ['NumPad2', 2]),
        (SendRemoteButFunc, 'fnNUM3', 'NumPad3', 'NumPad3', ['NumPad3', 3]),
        (SendRemoteButFunc, 'fnNUM4', 'NumPad4', 'NumPad4', ['NumPad4', 4]),
        (SendRemoteButFunc, 'fnNUM5', 'NumPad5', 'NumPad5', ['NumPad5', 5]),
        (SendRemoteButFunc, 'fnNUM6', 'NumPad6', 'NumPad6', ['NumPad6', 6]),
        (SendRemoteButFunc, 'fnNUM7', 'NumPad7', 'NumPad7', ['NumPad7', 7]),
        (SendRemoteButFunc, 'fnNUM8', 'NumPad8', 'NumPad8', ['NumPad8', 8]),
        (SendRemoteButFunc, 'fnNUM9', 'NumPad9', 'NumPad9', ['NumPad9', 9]),
        (SendRemoteButFunc, 'fnNUM0', 'NumPad0', 'NumPad0', ['NumPad0', 0])
        )),
    (eg.ActionGroup, 'Direction', 'Direction Keys', 'Direction Keys ',(
        (SendRemoteButFunc, 'fnDIRUP', 'Up', 'Up', ['Up', 30]),
        (SendRemoteButFunc, 'fnDIRDOWN', 'Down', 'Down', ['Down', 31]),
        (SendRemoteButFunc, 'fnDIRLEFT', 'Left', 'Left', ['Left', 32]),
        (SendRemoteButFunc, 'fnDIRRIGHT', 'Right', 'Right', ['Right', 33]),
        (SendRemoteButFunc, 'fnOK', 'Ok', 'Ok', ['Ok', 34]),
        (SendRemoteButFunc, 'fnBACK', 'Back', 'Back', ['Back', 35]),
        (SendRemoteButFunc, 'fnENTER', 'Enter', 'Enter', ['Enter', 11])
        )),
    (eg.ActionGroup, 'Power', 'Power Keys', 'Power Keys ',(
        (SendRemoteButFunc, 'fnPOWER1', 'Power1', 'Power1', ['Power1', 165]),
        (SendRemoteButFunc, 'fnPOWER2', 'Power2', 'Power2', ['Power2', 12]),
        (SendRemoteButFunc, 'fnPOWERTV', 'PowerTV', 'PowerTV', ['PowerTV', 101])
        )),
    (eg.ActionGroup, 'Destination', 'Destination Keys', 'Destination Keys ',(
        (SendRemoteButFunc, 'fnSTART', 'Start', 'Start', ['Start', 13]),
        (SendRemoteButFunc, 'fnGUIDE', 'Guide', 'Guide', ['Guide', 38]),
        (SendRemoteButFunc, 'fnMYTV', 'MyTV', 'MyTV', ['MyTV', 70]),
        (SendRemoteButFunc, 'fnMYMUSIC', 'MyMusic', 'MyMusic', ['MyMusic', 71]),
        (SendRemoteButFunc, 'fnRECORDEDTV', 'RecordedTV', 'RecordedTV', ['RecordedTV', 72]),
        (SendRemoteButFunc, 'fnMYPICTURES', 'MyPictures', 'MyPictures', ['MyPictures', 73]),
        (SendRemoteButFunc, 'fnMYVIDEOS', 'MyVideos', 'MyVideos', ['MyVideos', 74]),
        (SendRemoteButFunc, 'fnMYRADIO', 'MyRadio', 'MyRadio', ['MyRadio', 80]),
        (SendRemoteButFunc, 'fnLIVETV', 'LiveTV', 'LiveTV', ['LiveTV', 37]),
        (SendRemoteButFunc, 'fnDVDMENU', 'DVDMenu', 'DVDMenu', ['DVDMenu', 36])
        )),
    (eg.ActionGroup, 'Colors', 'Color Keys', 'Color Keys ',(
        (SendRemoteButFunc, 'fnRED', 'Red', 'Red', ['Red', 91]),
        (SendRemoteButFunc, 'fnGREEN', 'Green', 'Green', ['Green', 92]),
        (SendRemoteButFunc, 'fnYELLOW', 'Yellow', 'Yellow', ['Yellow', 93]),
        (SendRemoteButFunc, 'fnBLUE', 'Blue', 'Blue', ['Blue', 94])
        )),
    (eg.ActionGroup, 'Misc', 'Misc Keys', 'Misc Keys ',(
        (SendRemoteButFunc, 'fnINFO', 'Info', 'Info', ['Info', 15]),
        (SendRemoteButFunc, 'fnASPECTRATIO', 'AspectRatio', 'AspectRatio', ['AspectRatio', 39]),
        (SendRemoteButFunc, 'fnMESSENGER', 'Messenger', 'Messenger', ['Messenger', 105]),
        (SendRemoteButFunc, 'fnPRINT', 'Print', 'Print', ['Print', 78]),
        (SendRemoteButFunc, 'fnTELETEXT', 'Teletext', 'Teletext', ['Teletext', 90])
        ))
)

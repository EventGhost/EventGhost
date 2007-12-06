### Script for handling (Win)Lirc events by jinxdone - 26th July 2007

name = "LIRC Event Receiver"
kind = "remote"
version = "0.6.0"
author = "jinxdone"
description = """\
Plugin for receiving Lirc eventstrings and generating EventGhost events 
accordingly.

<br><br>
The configurable options are:
<UL>
<LI><i>Target Host</i><br>
The target host and port of the lirc server. For WinLirc running on localhost 
the default settings should be fine (127.0.0.1:8765)
<br>
<LI><i>Only use the first event</i><br>
Only one event per keypress is generated, all subsequent events will be 
discarded.
<LI><i>Add remote-name</i><br>
Adds the remote-name into the eventstring, use it if you want to distinguish 
between multiple remotes.
<LI><i>Add repeat-tag</i><br>
Adds "++" into the eventstring when the event in question is a repeating event.
<br>
<LI><i>Ignoretime after first event</i><br>
You can specify a time during which after a first event any repeat-events are 
discarded. The value is in milliseconds, set to 0 to disable.
 (Useful if you have problems with buttons you want only to "tap" and not have 
 multiple events by accident)
<br>
<LI><i>Timeout for enduring events</i><br>
Sets the timeout value for enduring events. If you increase it it will work 
more reliably, but it adds 'lag' to the end of each event, if you set it too 
low your events may sometimes be interrupted abrubtly.
 (default = 200, recommended between 150-400, depending on your setup)
</UL>"""


eg.RegisterPlugin(
    name=name, 
    description=description, 
    author=author, 
    version=version, 
    kind=kind,
    canMultiLoad=True,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=219",
)

import socket, asyncore, time, threading

class Text:
    version = "0.6.0"
    title = "LIRC Event Receiver plugin v" + version + " by jinxdone"
    host = "Host:"
    port = "Port:"
    hosttitle = "Target Host"
    onlyfirst = "Only use the first event"
    addremote = "Add remote-name"
    addrepeat = "Add repeat-tag"
    ignoretime = "Ignoretime after first event (ms)"
    timeout = "Timeout for enduring events (ms)"



class Lirc_Reader(asyncore.dispatcher):


    ### Initializing all the variables and open the tcp connection..
    ###
    def __init__(
        self, host,    port,    handler, onlyfirst,
        addremote, addrepeat, ignoretime
    ):
        self.handler = handler
        self.onlyfirst = onlyfirst
        self.addremote = addremote
        self.addrepeat = addrepeat
        self.ignoretime = ignoretime
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        eg.RestartAsyncore()
        self.connect((host, port))
        self.buffer = ""

    ### Some helper functions..
    ###
    def mscounter(self):
        if time.time()*1000 - self.recvtime*1000 < self.ignoretime:
            return False
        else:
            return True


    ### We don't want to send any data so let's stop asyncore
    ### from checking wether or not the socket is writable.
    ###
    def writable(self):
        return False


    ### This will be run if the tcp connection is disconnected
    ### or if we want to close it ourselves.
    ###
    def handle_close(self):
        print "Lirc: Closing the lirc-reader.."
        self.close()


    ### This will be run if theres a problem opening the connection
    ###
    def handle_expt(self):
        self.handler.reader = None
        self.close()
        eg.actionThread.Call(
            self.handler.HandleException,
            (
                "Could not connect to the LIRC server!\n"
                "Please doublecheck your configuration and that the "
                "LIRC server is reachable"
            )            
        )

    ### This gets run whenever asyncore detects there is data waiting
    ### for us to be read at the socket, so this is where it's all at..
    ###
    def handle_read(self):
        # Append data from the socket onto a buffer
        self.buffer = self.buffer + self.recv(4096)

        # (if theres anything on the right of the last linebreak, it must be
        #  some incomplete data caused by tcp/ip fragmenting our strings..)
        # hopefully the rest of it will be there on the next run..
        self.events = self.buffer.split("\n")
        self.buffer = self.events.pop()

        # loop through all the received events, incase there are
        # more than one to be processed
        for self.event in self.events:

            # split a single event into atoms
            self.event = self.event.split()
            # some checking never hurts..
            if len(self.event) < 4: break

            # shape the eventstring the way the user wants it
            # (add remote name, add is-repeat-tag, discard repeat events..)
            if self.addremote:
                self.egevent = self.event[3] + ":" + self.event[2]
            else:
                self.egevent = self.event[2]

            if self.event[1] == "00":
                if not self.onlyfirst:
                    if self.ignoretime:
                        self.recvtime = time.time()
                self.handler.TriggerEvent(self.egevent)
            else:
                if self.onlyfirst:
                    break
                if self.addrepeat:
                    self.egevent = self.egevent + "++"
                if self.ignoretime:
                    if self.mscounter():
                        self.handler.TriggerEvent(self.egevent)
                else:
                    self.handler.TriggerEvent(self.egevent)


    ### mandatory, but we won't need these..
    ###
    def handle_connect(self):
        pass


    def handle_write(self):
        pass


### The EventGhost classes and functions are over here..
class Lirc(eg.RawReceiverPlugin):

    def __start__(self, host, port, onlyfirst, addremote, addrepeat, ignoretime, timeout):
        self.port = port
        self.host = host
        self.onlyfirst = onlyfirst
        self.addremote = addremote
        self.addrepeat = addrepeat
        self.timeout = timeout / 1000.0
        self.ignoretime = ignoretime
        self.reader = Lirc_Reader(
            self.host,
            self.port,
            self,
            self.onlyfirst,
            self.addremote,
            self.addrepeat,
            self.ignoretime
        )


    def __stop__(self):
        if self.reader:
            self.reader.handle_close()
        self.reader = None


    def HandleException(self, msg):
        raise self.Exception(msg)
    
    
    def Configure(
        self,
        host="127.0.0.1",
        port=8765,
        onlyfirst = False,
        addremote = False,
        addrepeat = False,
        ignoretime = 0,
        timeout = 200,
    ):
        text = Text
        panel = eg.ConfigPanel(self)
        TitleText = wx.StaticText(panel, -1, text.title, style=wx.ALIGN_CENTER)
        HostText = wx.StaticText(panel, -1, text.host)
        HostCtrl = wx.TextCtrl(panel, -1, host)
        PortText = wx.StaticText(panel, -1, text.port)
        PortCtrl = eg.SpinIntCtrl(panel, -1, port, max=65535)

        HostSizer = wx.FlexGridSizer(cols=2)
        HostSizer.Add(HostText, 0, wx.ALL, 5)
        HostSizer.Add(HostCtrl, 0, wx.ALL, 3)
        HostSizer.Add(PortText, 0, wx.ALL, 5)
        HostSizer.Add(PortCtrl, 0, wx.ALL, 3)
        HostBox = wx.StaticBox(panel, -1, text.hosttitle)
        shbSizer = wx.StaticBoxSizer(HostBox)
        shbSizer.Add(HostSizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        OnlyFirstCtrl = wx.CheckBox(panel, -1, text.onlyfirst)
        OnlyFirstCtrl.SetValue(onlyfirst)
        AddRemoteCtrl = wx.CheckBox(panel, -1, text.addremote)
        AddRemoteCtrl.SetValue(addremote)
        AddRepeatCtrl = wx.CheckBox(panel, -1, text.addrepeat)
        AddRepeatCtrl.SetValue(addrepeat)
        IgnoreTimeText = wx.StaticText(panel, -1, text.ignoretime)
        IgnoreTimeCtrl = eg.SpinIntCtrl(panel, -1, ignoretime, max=60000)
        TimeoutText = wx.StaticText(panel, -1, text.timeout)
        TimeoutCtrl = eg.SpinIntCtrl(panel, -1, timeout, max=10000)

        IgnoreBox = wx.BoxSizer()
        IgnoreBox.Add(IgnoreTimeCtrl, 0, wx.ALL, 2)
        IgnoreBox.Add(IgnoreTimeText, 0, wx.ALL, 5)

        TimeoutBox = wx.BoxSizer()
        TimeoutBox.Add(TimeoutCtrl, 0, wx.ALL, 2)
        TimeoutBox.Add(TimeoutText, 0, wx.ALL, 5)

        BoxSizer = wx.BoxSizer(wx.VERTICAL)
        BoxSizer.Add(OnlyFirstCtrl, 0, wx.ALL, 5)
        BoxSizer.Add(AddRemoteCtrl, 0, wx.ALL, 5)
        BoxSizer.Add(AddRepeatCtrl, 0, wx.ALL, 5)
        #BoxSizer.Add(IgnoreTimeText, 0, wx.ALL, 5)
        #BoxSizer.Add(IgnoreTimeCtrl, 0, wx.ALL, 5)
        BoxSizer.Add(IgnoreBox, 0, wx.ALL, 3)
        BoxSizer.Add(TimeoutBox, 0, wx.ALL, 3)

        panel.sizer.Add(TitleText, 0, wx.EXPAND)
        panel.sizer.Add(shbSizer, 0, wx.EXPAND)
        panel.sizer.Add(BoxSizer, 0,)


        while panel.Affirmed():
            panel.SetResult(
                HostCtrl.GetValue(), 
                PortCtrl.GetValue(), 
                OnlyFirstCtrl.GetValue(), 
                AddRemoteCtrl.GetValue(), 
                AddRepeatCtrl.GetValue(), 
                IgnoreTimeCtrl.GetValue(),
                TimeoutCtrl.GetValue()
            )


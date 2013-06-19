### Script for handling (Win)Lirc events by jinxdone - 16th December 2007
###
###
### EventGhost plugin for receiving Lirc-style events written in python.
###
### This has only been tested with WinLirc (http://winlirc.sourceforge.net/),
### though it should also work with any version of Lirc (http://www.lirc.org/).
###
### If you are using WinLirc I'd suggest setting it a higher priority than normal.
### It's also a good idea to autorun it from somewhere, for example from
### eventghost or automatically during windows startup etc.
###
### Example of launching winlirc with higher priority:
### cmd.exe /C "start /realtime /min /B /D C:\winlirc\ C:\winlirc\winlirc.exe"
###
###
### Any questions? comments? 
### Ask on the forum or email jinxdone@earthling.net
###
###
### changelog:
### V0.7.0      - Added support for sending lirc events along with a
### 2007-12-16    nice little dialog configuration screen
###             - The plugin now tries to get information about
###               remotes/actions/buttons on startup by querying
###               the server with LIST commands
###             - Small changes to the plugin description
###
### V0.6.0      - Removed the internal enduring-event generation
### 2007-07-??  - Added adjustable enduring event timeout value
###             - some other minor changes
###
### v0.5.0      - First public version
### 2007-01-??
###
###
###
###
###
############### BEGIN CODE ###############




########################## BEGIN PLUGIN DESCRIPTION ##########################
###
name = "LIRC Client"
kind = "remote"
version = "0.7.1"
author = "jinxdone"
description = """\
Plugin for sending and receiving LIRC eventstrings. Generates EventGhost events 
based on data received from the LIRC-server.

<br><br>
For most setups only a slight adjustment of the "Timeout for enduring events" 
value is recommended.

<br><br>
The configurable options are:
<UL>
<LI><i>Target Host</i><br>
The target host and port of the lirc server. For WinLirc running on localhost 
the default settings should be fine (127.0.0.1:8765)
<br>
<LI><i>Only use the first event</i><br>
Only one(the first) event per keypress is generated, all subsequent events 
will be discarded.
<br>(Effectively disables enduring event behaviour)
<br>
<LI><i>Add remote-name</i><br>
Adds the remote-name into the eventstring, use it if you want to distinguish 
between multiple remotes.
<br>
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
 (default = 200, recommended between 125-400, depending on your setup)
</UL>"""
###
########################### END PLUGIN DESCRIPTION ###########################


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

############################## BEGIN TEXT CLASS ##############################
###
class Text:
    version = "0.7.0"
    title = "LIRC Client plugin v" + version + " by jinxdone"
    host = "Host:"
    port = "Port:"
    hosttitle = "Target Host"
    onlyfirst = "Only use the first event"
    addremote = "Add remote-name"
    addrepeat = "Add repeat-tag"
    ignoretime = "Ignoretime after first event (ms)"
    timeout = "Timeout for enduring events (ms)"
    selectiontitle = "Command selection"
    actcmd = "Command"
    actremote = "Remote"
    actaction = "Action"
    actrepeat = "Repeat"
    actstring = "Event String:"
    acthelp = """
You may use the fields in the Command selection to help form a string to send.
Or simply just type in the string directly into the field below."""
###
############################### END TEXT CLASS ###############################



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
        self.sbuffer = ""
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

    ### Tell asyncore to monitor when we can send our data
    ### when there is data in our send-buffer.
    ###
    def writable(self):
        return (len(self.sbuffer) > 0)

    ### Sends data from the buffer when called
    def handle_write(self):
        sent = self.send(self.sbuffer)
        self.sbuffer = self.sbuffer[sent:]

    ### This will be run if the tcp connection is disconnected
    ### or if we want to close it ourselves.
    ###
    def handle_close(self):
        self.handler.reader = None
        print "Lirc: Closing the lirc-reader.."
        self.close()
        eg.actionThread.Call(self.handler.HandleException, "Disconnected from the LIRC server!")


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
        self.buffer += self.recv(4096)
        # (if theres anything on the right of the last linebreak, it must be
        #  some incomplete data caused by tcp/ip fragmenting our strings..)
        # hopefully the rest of it will be there on the next run..
        self.events = self.buffer.split("\n")
        self.buffer = self.events.pop()


        # loop through all the received events, incase there are
        # more than one to be processed
        #
        # skip processing any listings or error messages.. (BEGIN -> END messages)
        i = -1
        skipit = 0
        for self.event in self.events:
            i += 1
            if skipit == 1:
               if self.event == "END":
                  skipit = 0
               continue

            # If we receive BEGIN it may be a response to some of the commands
            # we sent.. so parse it and data following it for useful information
            if self.event == "BEGIN":
               skipit = 1
               # If our input is is BEGIN,LIST,SUCCESS
               if self.events[i + 1:i + 3] == ["LIST","SUCCESS"]:
                  if len(self.events) > int(self.events[i + 4]):
                     self.handler.Send.remotelist = self.events[i + 5:(int(self.events[i + 4]) + 5)]


               else:
                  # If our input is BEING,LIST <remote>,SUCCESS
                  if [self.events[i + 1].split()[0], self.events[i + 2]] == ["LIST","SUCCESS"]:
                     self.remote = self.events[i + 1].split()[1]
                     if self.remote != "":

                        # Sanity check.. if there is not enough data skip it..
                        if len(self.events) > int(self.events[i + 4]):
                           self.checknum = 0
                           self.checkmatch = 0

                           # Check if we want to update an old one or if we have a new remote list
                           for self.check in self.handler.Send.remotes:
                              if self.remote == self.check[0]:
                                 self.handler.Send.remotes[self.checknum] = [
                                     self.remote,
                                     self.events[i + 5:(int(self.events[i + 4]) + i + 5)]
                                 ]
                                 self.checkmatch = 1
                           if self.checkmatch == 0:
                              self.handler.Send.remotes.append(
                                  [
                                      self.remote, 
                                      self.events[i + 5:(int(self.events[i + 4]) + i + 5)]
                                  ]
                              )

            # split a single event into atoms
            self.event = self.event.split()
            # some checking never hurts..
            if len(self.event) != 4: continue

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



### The EventGhost classes and functions are over here..
class Lirc(eg.RawReceiverPlugin):
    text = Text
    
    def __init__(self):
        self.AddAction(self.Send)
        
        
    def __start__(self, host, port, onlyfirst, addremote, addrepeat, ignoretime, timeout):
        self.port = port
        self.host = host
        self.onlyfirst = onlyfirst
        self.addremote = addremote
        self.addrepeat = addrepeat
        self.timeout = timeout / 1000.0
        self.ignoretime = ignoretime
        self.Send.remotes = []
        self.Send.remotelist = []
        self.reader = Lirc_Reader(
            self.host,
            self.port,
            self,
            self.onlyfirst,
            self.addremote,
            self.addrepeat,
            self.ignoretime
        )
        # Send LIST commands to the server..
        # In order to get remote-names and buttons in response
        self.reader.sbuffer += "LIST\n"
        print self.reader.sbuffer
        # Have to wait a bit and force asyncore to poll to check for a response
        time.sleep(0.05)
        asyncore.poll()

        self.maxsleep = 0
        while len(self.Send.remotelist) == 0:
           time.sleep(0.1)
           if self.maxsleep > 40:
              print "No remotes found! (bad lirc configuration?)"
              break
           self.maxsleep += 1

        if len(self.Send.remotelist) > 0:
           for self.remote in self.Send.remotelist:
              self.reader.sbuffer += "LIST " + self.remote + "\n"
              print self.reader.sbuffer
           asyncore.poll()

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
        text = self.text
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



# Action class for sending strings to the server
    class Send(eg.ActionClass):



########################## BEGIN ACTION DESCRIPTION ##########################
###
        name = "Send Event"
        description = """
Sends an eventstring to the LIRC-server for transmitting IR signals.

<br><br>
The plugin fetches information about the available remotes and actions 
from the LIRC-server with the LIST commands. If no information has been 
available or some other problem occurred the Remote and Action fields will 
have "N/A" values in them.
<br><br>
The configurable options are:
<UL>
<LI><i>Command</i><br>
Command to send. Commands available are SEND_ONCE, SEND_START and SEND_STOP.
<LI><i>Remote</i><br>
A List of the available remotes.
<LI><i>Action</i><br>
A List of the actions available with the selected remote.
<LI><i>Repeat</i><br>
Tells the LIRC-server to repeat the IR code n times.<br
Only valid for the SEND_ONCE command.
<br>
<LI><i>Event String</i><br>
The actual string to send, you can use either the Command selection or just 
type in the string you want to send by hand. The actual string to send is 
always what is in this field regardless of what is selected in the fields above.
</UL>
<br><br>
More information at 
<a href="http://www.lirc.org/html/technical.html#applications">
the LIRC documentation
</a>.
"""
###
########################### END ACTION DESCRIPTION ###########################



# The workhorse method.. (how tiny)!
        def __call__(self, msg):
            try: self.plugin.reader.sbuffer
            except AttributeError:
               raise self.Exception("Error sending event! Send buffer is missing!")
            else:
               self.plugin.reader.sbuffer = msg + "\n"
               asyncore.poll()

        def UpdateRemoteList(self):
            self.remotelist = []
            for remote in self.remotes:
                self.remotelist.append(remote[0])

        def Configure(self, actionStr=""):
            text = self.plugin.text
            remotes = self.remotes
            remotelist = self.remotelist
            actionParam = "0"
            if len(remotes) == 0:
               remotes.append(["N/A", ['N/A']])

            def OnCmdChoice(event):
               UpdateActionText()
               event.Skip()

            def OnRemoteChoice(event):
                actionCtrl.SetItems(remotes[remoteCtrl.GetSelection()][1])
                actionCtrl.SetSelection(0)
                UpdateActionText()
                event.Skip()

            def OnActionChoice(event):
                UpdateActionText()
                event.Skip()

            def OnRepeatSpin(event):
                UpdateActionText()
                event.Skip()

            def UpdateActionText():
                newstr = " ".join(
                   [cmdlist[cmdCtrl.GetSelection()], 
                   remotelist[remoteCtrl.GetSelection()], 
                   remotes[remoteCtrl.GetSelection()][1][actionCtrl.GetSelection()]]
                   )
                if cmdCtrl.GetSelection() == 0:
                   if repeatCtrl.GetValue() != 0:
                      newstr = newstr + " " + str(repeatCtrl.GetValue())
                textCtrl.SetValue(newstr)

            self.UpdateRemoteList()
            panel = eg.ConfigPanel(self)

            cmdlist = ["SEND_ONCE","SEND_START","SEND_STOP"]
            cmdCtrl = wx.Choice(panel, -1, choices=cmdlist)
            cmdCtrl.SetSelection(0)
            cmdText = wx.StaticText(panel, -1, text.actcmd)

            remoteCtrl = wx.Choice(panel, -1, choices=remotelist)
            remoteCtrl.SetSelection(0)
            remoteText = wx.StaticText(panel, -1, text.actremote)

            actionCtrl = wx.Choice(panel, -1, choices=remotes[0][1])
            actionCtrl.SetSelection(0)
            actionText = wx.StaticText(panel, -1, text.actaction)

            repeatCtrl = eg.SpinIntCtrl(panel, -1, actionParam, max=600)
            repeatText = wx.StaticText(panel, -1, text.actrepeat)

            stringText = wx.StaticText(panel, -1, text.actstring)
            textCtrl = wx.TextCtrl(panel, -1, actionStr)
            actionhelpText = wx.StaticText(panel, -1, text.acthelp)

            SelectionSizer = wx.FlexGridSizer(rows=2)
            SelectionSizer.Add(cmdText, 0, wx.LEFT, 5)
            SelectionSizer.Add(remoteText, 0, wx.LEFT, 5)
            SelectionSizer.Add(actionText, 0, wx.LEFT, 5)
            SelectionSizer.Add(repeatText, 0, wx.LEFT, 5)
            SelectionSizer.Add(cmdCtrl, 0, wx.ALL, 3)
            SelectionSizer.Add(remoteCtrl, 0, wx.ALL, 3)
            SelectionSizer.Add(actionCtrl, 0, wx.ALL, 3)
            SelectionSizer.Add(repeatCtrl, 0, wx.ALL, 3)

            SelectionBox = wx.StaticBox(panel, -1, text.selectiontitle)
            ssbSizer = wx.StaticBoxSizer(SelectionBox)
            ssbSizer.Add(SelectionSizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)

            BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
            BoxSizer.Add(stringText, 0, wx.ALL, 5)
            BoxSizer.Add(textCtrl, 1, wx.EXPAND)

            panel.sizer.Add(ssbSizer, 0, wx.EXPAND)
            panel.sizer.Add(actionhelpText, 0, wx.ALIGN_LEFT|wx.ALL, 10)
            panel.sizer.Add(BoxSizer, 0, wx.EXPAND|wx.ALL, 5)

            cmdCtrl.Bind(wx.EVT_CHOICE, OnCmdChoice)
            remoteCtrl.Bind(wx.EVT_CHOICE, OnRemoteChoice)
            actionCtrl.Bind(wx.EVT_CHOICE, OnActionChoice)
            repeatCtrl.Bind(wx.EVT_SPINCTRL, OnRepeatSpin)

            while panel.Affirmed():
                panel.SetResult(textCtrl.GetValue())




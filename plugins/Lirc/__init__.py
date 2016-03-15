### Script for handling (Win)Lirc events by jinxdone - 16th December 2007
###
###
### EventGhost plugin for receiving Lirc-style events written in python.
###
### This plugin has been made to work with WinLirc (http://winlirc.sourceforge.net/),
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
### v0.7.5      - Further improved error handling
### 2009-07-18  - Getting the remotes list now works in the background
###               after initial startup
###             - Added automatic reconnect feature when disconnected and
###               settings for it in the configuration dialog
###             - Changed all descriptions to rst format
###
### v0.7.4      - Improved error handling that fixes an issue with Lirc
### 2009-07-16    running on a *nix.
###             - Changed to mostly using a warning message instead of an exception
###             - Added a check if the reader has disconnected while waiting for a
###               list reply during startup
###
### v0.7.3      - Added a checkbox in the configuration dialog to enable/disable
### 2008-10-15    sending LIST command to the server
###
### v0.7.2      - Inluded the icon in __init__.py and removed obsolete readme
### 2008-08-11
###
### v0.7.1      - Added fixes/changes as suggested by BitMonster
### 2007-12-16  - Moved all strings to the Text -class
###             - Fixed some bugs in the Send(eg.ActionClass)'s
###               configuration dialog
###             - Added handling for suspend states
###
### v0.7.0      - Added support for sending lirc events along with a
### 2007-12-16    nice little dialog configuration screen
###             - The plugin now tries to get information about
###               remotes/actions/buttons on startup by querying
###               the server with LIST commands
###             - Small changes to the plugin description
###
### v0.6.0      - Removed the internal enduring-event generation
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
##############################################################################




########################## BEGIN PLUGIN DESCRIPTION ##########################
###
name = "LIRC Client"
kind = "remote"
version = "0.7.5"
author = "jinxdone"
description = """<rst>
Plugin for sending and receiving LIRC eventstrings. Generates EventGhost events
based on data received from the LIRC-server.

For most setups only a slight adjustment of the "Timeout for enduring events"
value is recommended.

*The configurable options are:*

- **Target Host**
  Host and port of the LIRC server. For WinLirc running on localhost
  the default settings should be fine (127.0.0.1:8765)

- **Auto-retry settings**
  If the connection is lost or can not be established, try to (re)connect
  a number of times with a set interval between retries. Set either
  value to 0 to disable.

- **List remotes from the LIRC server**
  Attempts to send a 'LIST' command to the server when connecting,
  which tries to fetch information about configured remotes.
  Uncheck if your server does not support this command.

- **Only use the first event**
  Only the first event from LIRC per keypress is processed, all subsequent events
  from the same keypress will be discarded. (Effectively also disables the enduring
  event behaviour)

- **Add remote-name**
  Adds the remote-name into the eventstring, use it if you want to distinguish
  between multiple remotes.

- **Add repeat-tag**
  Adds "++" into the eventstring when the event in question is a repeating event.

- **Ignoretime after first event**
  You can specify a time during which after a first event any repeat-events are
  discarded. The value is in milliseconds, set to 0 to disable. Useful if you
  have problems with buttons you want only to trigger once and  not get multiple
  events by accident.

- **Timeout for enduring events**
  Sets the timeout value for enduring events. If you increase it it will work
  more reliably, but it adds 'lag' to the end of each event. You will get best
  results when set as low as possible, however a value too low will tend to stop
  your events abruptly and then immediately start a new one.
  (default = 200, recommended between 125-400, depending on your setup)
"""
###
########################### END PLUGIN DESCRIPTION ###########################


eg.RegisterPlugin(
    name=name,
    description=description,
    author=author,
    version=version,
    kind=kind,
    canMultiLoad=True,
    guid="{17A77662-BB69-4C37-AA43-71213958C5C4}",
    url = "http://www.eventghost.net/forum/viewtopic.php?t=219",
    icon = (
      "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAACXBI"
      "WXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH1wEDFyY0FznCDQAAAP9JREFUeNqVUrGRhDAMXP3Qh9sg"
      "QzEV0I3tjAqIKUVk0AFkVOAW9AFvY47zHa8Zz2rGXmm1MqEQzjnFl3DOUVUiW2uLRO99yt8WsNZi"
      "miY8iZ/SBYskZG6yI5d3VXlACwYgAkAONczN7Vn1RGbTNP8fIY1y6eo/K6jrOuUip4nRTxH+w9MH"
      "iknXdej7HgAwjqPiYRAAtG2LYRiw7zuY+UJW1Y9/oXolqyqICBGJCCJykc3MpwchBBhjYIw5JBEl"
      "jEVeSflXRl3XUabqkSSMR1WhqvDeo23bi9kVAGzbVuy+rivF+2VZEELAPM+3Ldxmz1ZLueycHAvc"
      "bM6K0Lc1/gLZfImV1GmwgAAAAABJRU5ErkJggg=="
    )
)

import socket, asyncore, time, threading

############################## BEGIN TEXT CLASS ##############################
###
class Text:
    version = version
    title = "LIRC Client plugin v" + version + " by jinxdone"
    host = "Host:"
    port = "Port:"
    hosttitle = "Target Host"
    onlyfirst = "Only use the first event"
    addremote = "Add remote-name"
    addrepeat = "Add repeat-tag"
    ignoretime = "Ignoretime after first event (ms)"
    timeout = "Timeout for enduring events (ms)"
    attemptlist = "List remotes from the LIRC server"
    retrytitle = "Auto-retry connection if disconnected"
    maxretries = "Retries"
    retryinterval = "Interval (s)"
    noremotesfound = "No remotes found!"
    noremotesfoundtip = "You can disable sending LIST on connect if it does not work on your setup"
    disconnected = "Disconnected from the LIRC server!"
    disconnectedtip = "Restart the plugin to manually reconnect (Right-click -> Disable, Enable)"
    reconnect = "Attempting to reconnect to the LIRC-server"
    reconnectinit = "Attempting to reconnect %i times with %i seconds between attempts"
    reconnectgiveup = "Giving up reconnection after %i failed retries"
    reconnected = "Auto-connected successfully after %i attempts"
    startupexception = "Could not connect to the LIRC server!"
    erroneousresponse = "Received an erroneous response from the LIRC-server"
    malformedresponse = "Received an malformed response from the LIRC-server"
    suspendconnection = "Closing the connection to the LIRC-server.."
    resumeconnection = "Resuming the connection to the LIRC-server.."
###
############################### END TEXT CLASS ###############################



class Lirc_Reader(asyncore.dispatcher):
    text = Text

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
        self.delimeter = ''
        self.receivedresponse = 0
        self.gracefulclose = 0

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
        if self.gracefulclose:
           #eg.actionThread.Call(self.handler.HandlePrint, self.text.disconnected)
           self.gracefulclose = 0
        else:
           eg.actionThread.Call(self.handler.HandleWarning, self.text.disconnected)
           self.handler.ReconnectTimer()
        self.handler.reader = None
        self.close()


    ### This will be run if theres a problem opening the connection
    ###
    def handle_expt(self):
        self.handler.reader = None
        self.close()
        eg.actionThread.Call(self.handler.HandleWarning, self.text.startupexception)

    ### This gets run whenever asyncore detects there is data waiting
    ### for us to be read at the socket, so this is where it's all at..
    ###
    def handle_read(self):
        # Append data from the socket onto a buffer
        self.buffer += self.recv(4096)
        # Attempt to detect delimeter used..
        if self.delimeter == '':
            if self.buffer.count('\r\n'):
                self.delimeter = '\r\n'
            elif self.buffer.count('\n'):
                self.delimeter = '\n'
            elif self.buffer.count('\r'):
                self.delimeter = '\r'
            else:
                self.delimeter = '\r\n'
        # (if theres anything on the right of the last linebreak, it must be
        #  some incomplete data caused by tcp/ip fragmenting our strings..)
        # hopefully the rest of it will be there on the next run..
        self.events = self.buffer.split(self.delimeter)
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
               try:
                  # If our input is is BEGIN,<any>,ERROR
                  if self.events[i + 2] == "ERROR":
                     self.receivedresponse = 1
                     if len(self.events) > int(self.events[i + 4]) + 4:
                        eg.actionThread.Call(self.handler.HandleWarning, self.text.erroneousresponse + \
                        "\nMessage data: " + str(self.events[i + 5:i + int(self.events[i + 4]) + 5]))
                     else:
                        eg.actionThread.Call(self.handler.HandleWarning, self.text.erroneousresponse)
                  # If our input is is BEGIN,LIST,SUCCESS
                  if [self.events[i + 1], self.events[i + 2]] == ["LIST","SUCCESS"]:
                     if len(self.events) > int(self.events[i + 4]) + 4:
                        self.handler.Send.remotelist = self.events[i + 5:(int(self.events[i + 4]) + 5)]
                        for remote in self.handler.Send.remotelist:
                           self.sbuffer += "LIST " + remote + "\n"

                  else:
                     # If our input is BEGIN,LIST <remote>,SUCCESS
                     if [self.events[i + 1].split()[0], self.events[i + 2]] == ["LIST","SUCCESS"]:
                        self.remote = self.events[i + 1].split()[1]
                        if self.remote != "":

                           # Sanity check.. if there is not enough data skip it..
                           if len(self.events) > int(self.events[i + 4]) + 4:
                              self.checknum = 0
                              self.checkmatch = 0

                              # Check if we want to update an old one or if we have a new remote list
                              for self.check in self.handler.Send.remotes:
                                 # Flush out any N/A remotes (config dialog has been opened before getting a listing)
                                 if self.check[0] == 'N/A':
                                    self.handler.Send.remotes = []
                                 if self.remote == self.check[0]:
                                    self.handler.Send.remotes[self.checknum] = [
                                        self.remote,
                                        self.events[i + 5:(int(self.events[i + 4]) + i + 5)]
                                    ]
                                    self.checkmatch = 1
                                 self.checknum += 1
                              if self.checkmatch == 0:
                                 self.handler.Send.remotes.append(
                                     [
                                         self.remote,
                                         self.events[i + 5:(int(self.events[i + 4]) + i + 5)]
                                     ]
                                 )
               except IndexError:
                  self.receivedresponse = 1
                  eg.actionThread.Call(self.handler.HandleWarning, self.text.malformedresponse)

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

    class LircClientError(Exception):
        "LIRC Client Error:"

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.AddAction(self.Send)

    def __start__(
        self, host, port, onlyfirst, addremote,
        addrepeat, ignoretime, timeout,  attemptlist, maxretries, retryinterval
    ):
        text = self.text
        self.port = port
        self.host = host
        self.onlyfirst = onlyfirst
        self.addremote = addremote
        self.addrepeat = addrepeat
        self.timeout = timeout / 1000.0
        self.ignoretime = ignoretime
        self.attemptlist = attemptlist
        self.maxretries = maxretries
        self.currentattempt = 0
        self.retryinterval = retryinterval
        self.Send.remotes = []
        self.Send.remotelist = []
        self.InitConnection()
        # Test if connection is formed succesfully, if not trigger retry
        if not self.CheckConnection():
           self.ReconnectTimer()

    def __stop__(self):
        if self.reader:
            self.reader.gracefulclose = 1
            self.reader.handle_close()
        self.reader = None

    def InitConnection(self):
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
        if self.attemptlist:
           self.reader.sbuffer += "LIST\n"
           # Have to wait a bit and force asyncore to poll to check for a response
           time.sleep(0.05)
           asyncore.poll()
           self.checkListingTimer = threading.Timer(4, self.CheckListingResults)
           self.checkListingTimer.start()
        time.sleep(0.5)
        asyncore.poll()


    def CheckListingResults(self):
        if len(self.Send.remotes) == 0 or self.Send.remotes == ['N/A', ['N/A']]:
            self.HandleWarning(self.text.noremotesfound)
            self.HandlePrint(self.text.noremotesfoundtip)

    def HandlePrint(self, msg):
        print("LIRC Client: %s" % msg)

    def HandleWarning(self, msg):
        self.PrintError("LIRC Client: %s" % msg)

    def HandleException(self, msg):
        raise self.LircClientError(msg)

    def OnComputerSuspend(self, suspendType):
        if self.reader:
            self.reader.gracefulclose = 1
            self.reader.handle_close()
            self.HandleWarning(self.text.suspendconnection)
        self.reader = None

    def OnComputerResume(self, suspendType):
        self.HandleWarning(self.text.resumeconnection)
        self.InitConnection()
        # Test if connection is formed succesfully, if not trigger retry
        if not self.CheckConnection():
           self.ReconnectTimer()

    def CheckConnection(self):
        if self.maxretries == 0 or self.retryinterval == 0:
           return True
        time.sleep(0.05)
        if not self.reader:
           return False
        try:
           self.reader.sbuffer = 'VERSION\n'
        except:
           return False
        time.sleep(0.05)
        asyncore.poll()
        if not self.reader.connected:
           return False
        return True

    def ReconnectTimer(self):
        # If the connection drops try to reconnect n times with a pre-set
        # time between the attempts. Drop conneciton attempts after n failures
        if self.maxretries == 0 or self.retryinterval == 0:
           return
        self.reconnecttimer = threading.Timer(self.retryinterval, self.Reconnect)
        if self.currentattempt == 0:
           self.HandlePrint(self.text.reconnectinit % (self.maxretries, self.retryinterval))
        if self.currentattempt < self.maxretries:
           self.reconnecttimer.start()
        else:
           self.HandlePrint(self.text.reconnectgiveup % self.maxretries)

    def Reconnect(self):
        # First check if we are connected, if not then retry and check immediately again
        # if we got connected successfully (asyncore wont seem to update connected status
        # unless some traffic is sent/received so put one newline in the send buffer and poll it)
        if self.CheckConnection():
           return
        else:
           self.currentattempt += 1
           self.InitConnection()
           if self.CheckConnection():
              self.HandlePrint(self.text.reconnected % (self.currentattempt - 1))
           else:
              self.ReconnectTimer()

    def Configure(
        self,
        host="127.0.0.1",
        port=8765,
        onlyfirst = False,
        addremote = False,
        addrepeat = False,
        ignoretime = 0,
        timeout = 200,
        attemptlist = True,
        maxretries = 10,
        retryinterval = 30,
    ):
        text = self.text
        panel = eg.ConfigPanel(self)
        TitleText = wx.StaticText(panel, -1, text.title, style=wx.ALIGN_CENTER)
        HostText = wx.StaticText(panel, -1, text.host)
        HostCtrl = wx.TextCtrl(panel, -1, host)
        PortText = wx.StaticText(panel, -1, text.port)
        PortCtrl = eg.SpinIntCtrl(panel, -1, port, max=65535)
        AttemptListCtrl = wx.CheckBox(panel, -1, text.attemptlist)
        AttemptListCtrl.SetValue(attemptlist)

        RetryTitle = wx.StaticText(panel, -1, text.retrytitle)
        MaxRetriesText = wx.StaticText(panel, -1, text.maxretries)
        MaxRetriesCtrl = eg.SpinIntCtrl(panel, -1, maxretries)
        RetryIntervalText = wx.StaticText(panel, -1, text.retryinterval)
        RetryIntervalCtrl = eg.SpinIntCtrl(panel, -1, retryinterval, max=65535)
        RetryBox = wx.BoxSizer()
        RetryBox.Add(MaxRetriesCtrl, 0, wx.ALL, 2)
        RetryBox.Add(MaxRetriesText, 0, wx.ALL, 5)
        RetryBox.Add(RetryIntervalCtrl, 0, wx.ALL, 2)
        RetryBox.Add(RetryIntervalText, 0, wx.ALL, 5)

        HostSizer = wx.FlexGridSizer(cols=3)
        HostSizer.Add(HostText, 0, wx.ALL, 5)
        HostSizer.Add(HostCtrl, 0, wx.ALL, 3)
        HostSizer.Add(RetryTitle, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 54)
        HostSizer.Add(PortText, 0, wx.ALL, 5)
        HostSizer.Add(PortCtrl, 0, wx.ALL, 3)
        HostSizer.Add(RetryBox, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 50)

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

        FirstLineBox = wx.BoxSizer()
        FirstLineBox.Add(OnlyFirstCtrl, 0, wx.ALL, 5)
        FirstLineBox.Add(AttemptListCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 120)

        BoxSizer = wx.BoxSizer(wx.VERTICAL)
        BoxSizer.Add(FirstLineBox, 0, wx.ALL, 0)
        BoxSizer.Add(AddRemoteCtrl, 0, wx.ALL, 5)
        BoxSizer.Add(AddRepeatCtrl, 0, wx.ALL, 5)
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
                TimeoutCtrl.GetValue(),
                AttemptListCtrl.GetValue(),
                MaxRetriesCtrl.GetValue(),
                RetryIntervalCtrl.GetValue()
            )



# Action class for sending strings to the server
    class Send(eg.ActionClass):


########################## BEGIN ACTION DESCRIPTION ##########################
###
        name = "Send Event"
        description = """<rst>
Sends an eventstring to the LIRC-server for transmitting IR signals.

The plugin can fetch information about the available remotes and actions
from the LIRC-server with the LIST command. If no information has been
available or some other problem occurred the Remote and Action fields will
have "N/A" values in them.

*The configurable options are:*

- **Command**
  Available commands are SEND_ONCE, SEND_START and SEND_STOP.

- **Remote**
  A List of the available remotes.

- **Action**
  A List of the actions available with the selected remote.

- **Repeat**
  Tells the LIRC-server to repeat the IR code n times.
  Only valid for the SEND_ONCE command.

- **Event String**
  The actual string to send, you can use either the Command selection or just
  type in the string you want to send by hand. The actual string to send is
  always what is in this field regardless of what is selected in the fields above.

More information at `the LIRC documentation`__

__ http://www.lirc.org/html/technical.html#applications
"""
###
########################### END ACTION DESCRIPTION ###########################


############################## BEGIN TEXT CLASS ##############################
###
        class Text:
            selectiontitle = "Command selection"
            actcmd = "Command"
            actremote = "Remote"
            actaction = "Action"
            actrepeat = "Repeat"
            actstring = "Event String:"
            acthelp = (
               "You may use the fields in the Command selection to help form a string to send.\n"
               "Or simply just type in the string directly into the field below."
            )
            acterrormsg = "Error while sending event! Send buffer is missing!"
###
############################### END TEXT CLASS ###############################


        text = Text

        class LircClientError(Exception):
            "LIRC Client Error:"

# The workhorse method.. (how tiny)!
        def __call__(self, msg):
            try: self.plugin.reader.sbuffer
            except AttributeError:
               self.plugin.HandleWarning(self.text.acterrormsg)
            else:
               self.plugin.reader.sbuffer = msg + "\n"
               asyncore.poll()

        def UpdateRemoteList(self):
            self.remotelist = []
            for remote in self.remotes:
                self.remotelist.append(remote[0])

        def Configure(self, actionStr=""):
            text = self.text
            actionParam = "0"
            if len(self.remotes) == 0:
               self.remotes.append(["N/A", ['N/A']])
               self.remotelist = ["N/A"]
            else:
               self.UpdateRemoteList()
            remotes = self.remotes
            remotelist = self.remotelist


            def OnCmdChoice(event):
               UpdateActionText()

            def OnRemoteChoice(event):
                actionCtrl.SetItems(remotes[remoteCtrl.GetSelection()][1])
                actionCtrl.SetSelection(0)
                UpdateActionText()

            def OnActionChoice(event):
                UpdateActionText()

            def OnRepeatSpin(event):
                UpdateActionText()

            def UpdateActionText():
                # Add an empty space at the end of the string to send, atleast
                # WinLirc seems to require it in the case the repeat value is omitted
                newstr = " ".join(
                   [cmdlist[cmdCtrl.GetSelection()],
                   remotelist[remoteCtrl.GetSelection()],
                   remotes[remoteCtrl.GetSelection()][1][actionCtrl.GetSelection()],
                   '']
                   )
                if cmdCtrl.GetSelection() == 0:
                   if repeatCtrl.GetValue() != 0:
                      newstr = newstr + str(repeatCtrl.GetValue())
                textCtrl.SetValue(newstr)

            def UpdateCtrl(string, list, control):
                i = 0
                for item in list:
                   if string == item:
                      control.SetSelection(i)
                      return True
                   else:
                      i += 1
                return False

            def IsInt(str):
               try:
                  num = int(str)
               except ValueError:
                  return 0
               return num

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
            repeatCtrl.Bind(eg.EVT_VALUE_CHANGED, OnRepeatSpin)

            def UpdateControls():
                items = actionStr.split()
                if len(items) >= 3:
                   if UpdateCtrl(items[0], cmdlist, cmdCtrl):
                      if UpdateCtrl(items[1], remotelist, remoteCtrl):
                         actionCtrl.SetItems(remotes[remoteCtrl.GetSelection()][1])
                         UpdateCtrl(items[2], remotes[remoteCtrl.GetSelection()][1], actionCtrl)
                         if len(items) >= 4:
                            repeat = IsInt(items[3])
                            if 0 < repeat <= 600:
                               repeatCtrl.SetValue(repeat)

            UpdateControls()

            while panel.Affirmed():
                panel.SetResult(textCtrl.GetValue())

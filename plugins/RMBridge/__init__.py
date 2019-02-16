### Broadlink RM2 Client for use with Android RM Bridge
### Can send 433MHz RF and IR commands.
### Based on the LIRC plugin by jinxdone (jinxdone@earthling.net)
### but horribly hacked for the RM bridge... Don't judge me.
### It only allows learning to the first discovered Broadlink RM2
### If you have more than one, disconnect the others whilst learning.
### Loads of code in here still which I don't need or understand.
### You are welcome to clean it all up yourself :)
##############################################################################


########################## BEGIN PLUGIN DESCRIPTION ##########################
###
name = "RM Bridge"
kind = "remote"
version = "0.0.9"
author = "DPearce"
description = """<rst>
Plugin for sending commands to a Broadlink RM2 RF and IR sender via 
the Android RM Bridge software available at: http://rm-bridge.fun2code.de/

*The configurable options are:*

- **Target Host**
  Host and port of the RM Bridge. 

- **Auto-retry settings**
  If the connection  can not be established, try to (re)connect
  a number of times with a set interval between retries. Set either 
  value to 0 to disable.

- **List remotes from the RM Bridge**
  Attempts to send a 'LIST' command to the RM Bridge, 
  which tries to fetch a list of configured shortcuts. 

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
    url="http://rm-bridge.fun2code.de/"
)

import socket, asyncore, time, threading, urllib2, json

globHost = 1
globPort = 1
globRetries = 1
globTimeout = 2
globCommandList = []


############################## BEGIN TEXT CLASS ##############################
###
class Text:
    version = version
    title = "RM Bridge plugin v" + version + " by DPearce"
    host = "Host:"
    port = "Port:"
    hosttitle = "RM Bridge Target Host"
    onlyfirst = "Only use the first event"
    addremote = "Add remote-name"
    addrepeat = "Add repeat-tag"
    ignoretime = "Ignoretime after first event (ms)"
    timeout = "Timeout for response (s)"
    attemptlist = "List remotes from the RM Bridge"
    retrytitle = "Auto-retry connection on failure"
    maxretries = "Retries"
    retryinterval = "Timeout (s)"
    noremotesfound = "No Codes found!"
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


class RM_Bridge(asyncore.dispatcher):
    text = Text

    ### Initializing all the variables and open the tcp connection..
    ###
    def __init__(
        self, host, port, handler, onlyfirst,
        addremote, addrepeat, ignoretime
    ):
        global globPort, globHost
        globHost = host
        globPort = port
        self.handler = handler
        self.onlyfirst = onlyfirst
        self.addremote = addremote
        self.addrepeat = addrepeat
        self.ignoretime = ignoretime
        self.sbuffer = ""
        # asyncore.dispatcher.__init__(self)
        # self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        # eg.RestartAsyncore()
        # self.connect((host, port))
        self.buffer = ""
        self.delimeter = ''
        self.receivedresponse = 0
        self.gracefulclose = 0

    ### Some helper functions..
    ###
    def mscounter(self):
        if time.time() * 1000 - self.recvtime * 1000 < self.ignoretime:
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
            # eg.actionThread.Call(self.handler.HandlePrint, self.text.disconnected)
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
                                                 "\nMessage data: " + str(
                                self.events[i + 5:i + int(self.events[i + 4]) + 5]))
                        else:
                            eg.actionThread.Call(self.handler.HandleWarning, self.text.erroneousresponse)
                    # If our input is is BEGIN,LIST,SUCCESS
                    if [self.events[i + 1], self.events[i + 2]] == ["LIST", "SUCCESS"]:
                        if len(self.events) > int(self.events[i + 4]) + 4:
                            self.handler.Send.remotelist = self.events[i + 5:(int(self.events[i + 4]) + 5)]
                            for remote in self.handler.Send.remotelist:
                                self.sbuffer += "LIST " + remote + "\n"

                    else:
                        # If our input is BEGIN,LIST <remote>,SUCCESS
                        if [self.events[i + 1].split()[0], self.events[i + 2]] == ["LIST", "SUCCESS"]:
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
class RMBridge(eg.RawReceiverPlugin):
    text = Text

    class RMBridgeClientError(Exception):
        "RMBridge Client Error:"

    def __init__(self):
        eg.RawReceiverPlugin.__init__(self)
        self.AddAction(self.Send)

    def __start__(
        self, host, port, onlyfirst, addremote,
        addrepeat, ignoretime, timeout, attemptlist, maxretries, retryinterval
    ):
        text = self.text
        self.port = port
        self.host = host
        self.onlyfirst = onlyfirst
        self.addremote = addremote
        self.addrepeat = addrepeat
        self.timeout = timeout / 1000.0
        global globTimeout
        globTimeout = retryinterval
        self.ignoretime = ignoretime
        self.attemptlist = attemptlist
        self.maxretries = maxretries
        global globRetries
        globRetries = maxretries
        self.currentattempt = 0
        self.retryinterval = retryinterval
        self.Send.remotes = []
        self.Send.remotelist = []
        self.InitConnection()
        # Test if connection is formed succesfully, if not trigger retry
        # if not self.CheckConnection():
        #   self.ReconnectTimer()

    def __stop__(self):
        # if self.reader:
        #    self.reader.gracefulclose = 1
        #    self.reader.handle_close()
        self.reader = None

    def InitConnection(self):
        self.reader = RM_Bridge(
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
        # print "List Remote Commands"

        if self.attemptlist:
            # print "Listing Commands on "+ globHost + ':' + str(globPort)
            try:
                r = urllib2.urlopen('http://' + globHost + ':' + str(globPort) + '/?cmd={api_id:1006}', None,
                                    globTimeout)
                stat = r.read()
                codes = json.loads(stat)
                # print codes
                global globCommandList
                globCommandList = [""]
                for ListItem in codes["list"]:
                    # print ListItem["name"]
                    globCommandList.append(ListItem["name"])
            except:
                self.PrintError("Listing commands from RM Bridge Failed")
            globCommandList.sort()
            # print globCommandList

            # self.reader.sbuffer += "LIST\n"
            # Have to wait a bit and force asyncore to poll to check for a response
            # time.sleep(0.05)
            # asyncore.poll()
            # self.checkListingTimer = threading.Timer(4, self.CheckListingResults)
            # self.checkListingTimer.start()
        time.sleep(0.5)
        # asyncore.poll()

    def CheckListingResults(self):

        if len(self.Send.remotes) == 0 or self.Send.remotes == ['N/A', ['N/A']]:
            self.HandleWarning(self.text.noremotesfound)
            self.HandlePrint(self.text.noremotesfoundtip)

    def HandlePrint(self, msg):
        print("RMBridge Client: %s" % msg)

    def HandleWarning(self, msg):
        self.PrintError("RMBridge Client: %s" % msg)

    def HandleException(self, msg):
        raise self.RMBridgeClientError(msg)

    def OnComputerSuspend(self, suspendType):
        pass
        # if self.reader:
        #    self.reader.gracefulclose = 1
        #    self.reader.handle_close()
        #    self.HandleWarning(self.text.suspendconnection)
        self.reader = None

    def OnComputerResume(self, suspendType):
        pass
        # self.HandleWarning(self.text.resumeconnection)
        # self.InitConnection()
        # Test if connection is formed succesfully, if not trigger retry
        # if not self.CheckConnection():
        #   self.ReconnectTimer()

    def CheckConnection(self):
        return True
        # if self.maxretries == 0 or self.retryinterval == 0:
        #   return True
        # time.sleep(0.05)
        # if not self.reader:
        #   return False
        # try:
        #   self.reader.sbuffer = 'VERSION\n'
        # except:
        #   return False
        # time.sleep(0.05)
        # asyncore.poll()
        # if not self.reader.connected:
        #   return False
        # return True

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
        host="192.168.1.145",
        port=7474,
        onlyfirst=False,
        addremote=False,
        addrepeat=False,
        ignoretime=0,
        timeout=200,
        attemptlist=True,
        maxretries=3,
        retryinterval=3,
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
        shbSizer.Add(HostSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        OnlyFirstCtrl = False  # wx.CheckBox(panel, -1, text.onlyfirst)
        # OnlyFirstCtrl.SetValue(onlyfirst)
        AddRemoteCtrl = False  # wx.CheckBox(panel, -1, text.addremote)
        # AddRemoteCtrl.SetValue(addremote)
        AddRepeatCtrl = False  # wx.CheckBox(panel, -1, text.addrepeat)
        # AddRepeatCtrl.SetValue(addrepeat)
        IgnoreTimeText = ""  # wx.StaticText(panel, -1, text.ignoretime)
        IgnoreTimeCtrl = 1  # eg.SpinIntCtrl(panel, -1, ignoretime, max=60000)
        TimeoutText = ""  # wx.StaticText(panel, -1, text.timeout)
        TimeoutCtrl = 1  # eg.SpinIntCtrl(panel, -1, timeout, max=10000)

        IgnoreBox = wx.BoxSizer()
        # IgnoreBox.Add(IgnoreTimeCtrl, 0, wx.ALL, 2)
        # IgnoreBox.Add(IgnoreTimeText, 0, wx.ALL, 5)

        TimeoutBox = wx.BoxSizer()
        # TimeoutBox.Add(TimeoutCtrl, 0, wx.ALL, 2)
        # TimeoutBox.Add(TimeoutText, 0, wx.ALL, 5)

        FirstLineBox = wx.BoxSizer()
        # FirstLineBox.Add(OnlyFirstCtrl, 0, wx.ALL, 5)
        FirstLineBox.Add(AttemptListCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 120)

        BoxSizer = wx.BoxSizer(wx.VERTICAL)
        BoxSizer.Add(FirstLineBox, 0, wx.ALL, 0)
        # BoxSizer.Add(AddRemoteCtrl, 0, wx.ALL, 5)
        # BoxSizer.Add(AddRepeatCtrl, 0, wx.ALL, 5)
        # BoxSizer.Add(IgnoreBox, 0, wx.ALL, 3)
        # BoxSizer.Add(TimeoutBox, 0, wx.ALL, 3)

        panel.sizer.Add(TitleText, 0, wx.EXPAND)
        panel.sizer.Add(shbSizer, 0, wx.EXPAND)
        panel.sizer.Add(BoxSizer, 0, )

        while panel.Affirmed():
            panel.SetResult(
                HostCtrl.GetValue(),
                PortCtrl.GetValue(),
                OnlyFirstCtrl,
                AddRemoteCtrl,
                AddRepeatCtrl,
                IgnoreTimeCtrl,
                TimeoutCtrl,
                AttemptListCtrl.GetValue(),
                MaxRetriesCtrl.GetValue(),
                RetryIntervalCtrl.GetValue()
            )

    # Action class for sending strings to the server
    class Send(eg.ActionClass):

        ########################## BEGIN ACTION DESCRIPTION ##########################
        ###
        name = "Send Command"
        description = """<rst>
Sends a command to the RM Bridge for transmitting IR/RF signals.

The plugin can fetch information about the available command
shortcuts from the RM Bridge. If no information has been 
available or some other problem occurred the command field will 
be empty.

*The configurable options are:*

- **Shortcut Command**
  Available commands if received from the RM Bridge.


- **Command**
  The actual string to send, you can use either the Command selection or just 
  type in the string you want to send by hand. The actual string to send is 
  always what is in this field regardless of what is selected in the fields above.

"""

        ###
        ########################### END ACTION DESCRIPTION ###########################

        ############################## BEGIN TEXT CLASS ##############################
        ###
        class Text:
            selectiontitle = "Command selection"
            actcmd = "Command"
            actremote = "RM Bridge Shorcut Command"
            actaction = "Action"
            actrepeat = "Repeat"
            actstring = "Command:"
            acthelp = (
                "You may use the dropdown in the Command selection to select a string to send.\n"
                "Or simply just type the string directly into the field below.\n\n"
                "Clicking the Learn button will create or replace the command on the RM Bridge named\n"
                "in the command box upon a successful learn. You have 5 seconds to learn the IR/RF code"
            )
            acterrormsg = "Error while sending event! Send buffer is missing!"

        ###
        ############################### END TEXT CLASS ###############################

        text = Text

        class RMBridgeClientError(Exception):
            "RMBridge Client Error:"

        # The workhorse method.. (how tiny - not any more:( )!
        def __call__(self, msg):
            BridgeURL = "http://" + str(globHost) + ":" + str(globPort)
            retries = int(globRetries)
            # print BridgeURL + str(retries)
            for t in range(1, retries + 1):
                try:
                    r = urllib2.urlopen(BridgeURL + "/code/" + msg, None, globTimeout)
                    stat = r.read()
                except:
                    self.PrintError("RM Bridge connection failed to " + BridgeURL)
                    continue
                # print "RM Status: " + stat
                if "send data success" in stat:
                    return 0
                if "data error" in stat:
                    self.PrintError("RM Bridge: " + stat)
                    return 1
                if "No matching code" in stat:
                    break
                self.PrintError("RM Bridge: " + stat + " - Retry: " + str(t) + "of" + retries)

            # print "sending:" + msg
            # try: self.plugin.reader.sbuffer
            # except AttributeError:
            #   self.plugin.HandleWarning(self.text.acterrormsg)
            # else:
            #   self.plugin.reader.sbuffer = msg + "\n"
            #   asyncore.poll()

        def UpdateRemoteList(self):
            # print "Remotes IN"
            self.remotelist = []
            # for remote in self.remotes:
            #    self.remotelist.append(remote[0])

        def Configure(self, actionStr=""):
            text = self.text
            actionParam = "0"
            if len(self.remotes) == 0:
                self.remotes.append(["N/A", ['N/A']])
                self.remotelist = ["N/A"]
            else:
                self.UpdateRemoteList()
            remotes = self.remotes
            # remotelist = self.remotelist
            remotelist = globCommandList

            def OnCmdChoice(event):
                UpdateActionText()

            def OnRemoteChoice(event):
                remotes = globCommandList
                # actionCtrl.SetItems(remotes[remoteCtrl.GetSelection()][1])
                # actionCtrl.SetSelection(0)
                UpdateActionText()

            def OnActionChoice(event):
                UpdateActionText()

            def OnRepeatSpin(event):
                UpdateActionText()

            def UpdateActionText():
                # Add an empty space at the end of the string to send, atleast
                # WinRMBridge seems to require it in the case the repeat value is omitted
                newstr = remotelist[remoteCtrl.GetSelection()]
                # if cmdCtrl.GetSelection() == 0:
                #   if repeatCtrl.GetValue() != 0:
                #      newstr = newstr + str(repeatCtrl.GetValue())
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

            def CheckLearned(BridgeURL, mac, cmdName):
                # print BridgeURL, mac, cmdName
                try:
                    r = urllib2.urlopen(BridgeURL + '/?cmd={api_id:1003,mac:"' + mac + '",name:' + cmdName + '}', None,
                                        2)
                    stat = r.read()
                    if "study mode success" in stat:
                        stat = "Learning Complete. New code stored as " + cmdName
                except:
                    stat = "Read/Store learned code failed"
                print "RM Bridge: " + stat

            def LearnCode(event):
                cmdName = textCtrl.GetValue()
                BridgeURL = "http://" + str(globHost) + ":" + str(globPort)
                try:
                    r = urllib2.urlopen(BridgeURL + '/?cmd={api_id:1000}', None, 2)
                    stat = r.read()
                    devices = json.loads(stat)
                    AllDev = devices["list"]
                    for dev in AllDev:
                        mac = dev["mac"]
                    if mac:
                        # print "Entering Learn mode on " + mac
                        try:
                            r = urllib2.urlopen(BridgeURL + '/?cmd={api_id:1002,mac:"' + mac + '"}', None, 2)
                            stat = r.read()
                            # print stat
                            if "study mode success" in stat:
                                stat = "Learning on " + mac + " - Press remote button to learn within 5 seconds"
                                threading.Timer(5, CheckLearned, [BridgeURL, mac, cmdName]).start()
                            else:
                                stat = "Enter learn mode failed"
                        except:
                            stat = "Send learn mode command failed"
                except:
                    stat = "Listing devices from RM Bridge failed"

                print "RM Bridge: " + stat

            panel = eg.ConfigPanel(self)

            cmdlist = ["S"]
            # cmdCtrl = wx.Choice(panel, -1, choices=cmdlist)
            # cmdCtrl.SetSelection(0)
            # cmdText = wx.StaticText(panel, -1, text.actcmd)

            remoteCtrl = wx.Choice(panel, -1, choices=remotelist)
            remoteCtrl.SetSelection(0)
            remoteText = wx.StaticText(panel, -1, text.actremote)

            # actionCtrl = wx.Choice(panel, -1, choices=remotes[0][1])
            # actionCtrl.SetSelection(0)
            # actionText = wx.StaticText(panel, -1, text.actaction)

            # repeatCtrl = eg.SpinIntCtrl(panel, -1, actionParam, max=600)
            # repeatText = wx.StaticText(panel, -1, text.actrepeat)

            stringText = wx.StaticText(panel, -1, text.actstring)
            textCtrl = wx.TextCtrl(panel, -1, actionStr)
            actionhelpText = wx.StaticText(panel, -1, text.acthelp)

            LearnButton = wx.Button(panel, 1, "Learn Remote Command")
            LearnButton.Bind(wx.EVT_BUTTON, LearnCode)

            SelectionSizer = wx.FlexGridSizer(rows=2, cols=1, gap=(10, 10))
            # SelectionSizer.Add(cmdText, 0, wx.LEFT, 5)
            SelectionSizer.Add(remoteText, 0, wx.LEFT, 5)
            # SelectionSizer.Add(actionText, 0, wx.LEFT, 5)
            # SelectionSizer.Add(repeatText, 0, wx.LEFT, 5)
            # SelectionSizer.Add(cmdCtrl, 0, wx.ALL, 3)
            SelectionSizer.Add(remoteCtrl, 0, wx.ALL, 3)
            # SelectionSizer.Add(actionCtrl, 0, wx.ALL, 3)
            # SelectionSizer.Add(repeatCtrl, 0, wx.ALL, 3)

            SelectionBox = wx.StaticBox(panel, -1, text.selectiontitle)
            ssbSizer = wx.StaticBoxSizer(SelectionBox)
            ssbSizer.Add(SelectionSizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

            BoxSizer = wx.BoxSizer(wx.HORIZONTAL)
            BoxSizer.Add(stringText, 0, wx.ALL, 5)
            BoxSizer.Add(textCtrl, 1, wx.EXPAND)
            BoxSizer.Add(LearnButton, 1, wx.EXPAND)

            panel.sizer.Add(ssbSizer, 0, wx.EXPAND)
            panel.sizer.Add(actionhelpText, 0, wx.ALIGN_LEFT | wx.ALL, 10)
            panel.sizer.Add(BoxSizer, 0, wx.EXPAND | wx.ALL, 5)

            # cmdCtrl.Bind(wx.EVT_CHOICE, OnCmdChoice)
            remoteCtrl.Bind(wx.EVT_CHOICE, OnRemoteChoice)

            # actionCtrl.Bind(wx.EVT_CHOICE, OnActionChoice)
            # repeatCtrl.Bind(eg.EVT_VALUE_CHANGED, OnRepeatSpin)

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

# -*- coding: utf-8 -*-

version="0.3" 

# plugins/TivoNetwork/__init__.py
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from socket import *
import time
from threading import Timer
import thread

eg.RegisterPlugin(
    name = "TivoNetwork",
    author = "Possessed",
    version = version,
    kind = "external",
    canMultiLoad = True,
    guid = "{921D3571-5555-43BE-B7F2-C1369F3ABACD}",
    description = u'''
<rst>**Adds actions to control Tivo over Network**

The TiVo TCP Control Protocol is an ASCII-based command protocol for remote
control of a TiVo DVR over a TCP network connection. The commands allow
control of channel changes and user interface navigation, and allow the client to
send simulated remote control button presses to the DVR.

**Important**
Your TiVo DVR can be controlled by networked devices (such as a Crestron home
control system). Beginning with version 9.4 of the TiVo software, this feature is
turned off by default to ensure the security of your home network.
To enable networked remote control on your TiVo DVR:

1. *Go to TiVo Central > Messages & Settings > Settings > Remote, CableCARD & Devices > Network Remote Control.*
2. *Choose Enabled.*
3. *Press Select*

**Using the TiVo TCP Control Protoco**
To use the TiVo TCP Control Protocol, open a TCP socket on port 31339 and send
properly formatted command packets. Each command packet consists of a single
line of uppercase text, terminated by a carriage return.

**Command Syntax**
A command packet is a command and its parameters, separated by single spaces.
Example:

**COMMAND {PARAMETER} {PARAMETER}...**

**Commands**
The protocol includes the following commands:
- Commands for sending a code corresponding to a button on the remote control or keyboard:

*IRCODE*
*KEYBOARD*

- Commands for tuning to a particular channel

*SETCH*
*FORCECH*

- A command for teleporting (navigating directly) to one of certain user interface screens

*TELEPORT*


Translating text to keyboard info borrowed from William McBrine Tivo Network Remote Control
hotkey borrowed from Brett Stottlemyer plugin MCE

see the following link for more detail:
https://www.tivo.com/assets/images/abouttivo/resources/downloads/brochures/TiVo_TCP_Network_Remote_Control_Protocol.pdf

''',
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=9956",
    createMacrosOnAdd = True,
)

class Text:
    tcpBox = "Connect Settings"
    port = "Tivo Remote Host IP Port:"
    address = "Tivo Remote Host IP Address:"
    timeout = "Connection Timeout:"
    sendtext = "Text to send to Tivo:"

    class SetAddress:
        name = "Set Remote IP Address"
        description = "Allow dynamically changing the ip address of the remote tivo device"
        iconFile = 'icons/add'

    class SendTextToTivo:
        name = "Send Text To Tivo"
        description = "Allows sending a group of characters to tivo as though they are entered individually using the Tivo Keyboard"
        iconFile = 'icons/add'

USESOCKETTIMEOUT = True

DEBUG = True
if DEBUG:
    log = eg.PrintDebugNotice
else:
    def log(dummyMesg):
        pass

class RawKeys(eg.ActionClass):
    
    def __call__(self):
        log('Tivo RawKeys outVal ' + self.value)
        self.plugin.DoRawSendSplit(self.value)

class hotKeys(eg.ActionClass):
    
    def __call__(self):
        log('Tivo hotKeys outVal ' + self.value)
        self.plugin.DoCommand(self.value, 'IRCODE')

def CreateTivoAction(theTivoAction):
    class TivoAction(eg.ActionClass):
        def __init__(self):
            self.tivoAction = theTivoAction
        
        def __call__(self):
            log('TivoAction ' + self.tivoAction + ', outVal ' + self.value)
            self.plugin.DoCommand(self.value, self.tivoAction)

            
    return TivoAction

def CreateStringAction(myParameterDescription, myDefaultParameter):
    class AnAction(eg.ActionWithStringParameter):
        parameterDescription = myParameterDescription
        defaultParameter = myDefaultParameter
        
        def __call__(self, value):
            log('Tivo string action value: ' + self.value + ' user value: ' + value)
            
    return AnAction

def CreateTextSenderAction(myParameterDescription, myDefaultParameter):
    class TextSenderAction(eg.ActionWithStringParameter):

        parameterDescription = myParameterDescription
        defaultParameter = myDefaultParameter
        
        def __call__(self, value):
            #log('Tivo TextSender outVal ' + self.value)
            log('Tivo TextSender string action value: ' + value)
            self.plugin.SendText(value)
           
        def Configure(self, strParameter=""):
            #if strParameter is None:
            #    strParameter = self.value[0]
            panel = eg.ConfigPanel()
            label = panel.StaticText('Enter Text to Send:')
            ctrl = panel.TextCtrl(strParameter)
            #ctrl = panel.TextCtrl(strParameter, size=(200, 100), style=wx.TE_MULTILINE)



            panel.sizer.Add(label, 0, wx.EXPAND)
            panel.sizer.Add((5, 5))
            panel.sizer.Add(ctrl, 0, wx.EXPAND)
            while panel.Affirmed():
                panel.SetResult(ctrl.GetValue())
 
    return TextSenderAction
    


class CustomTivoAction(eg.ActionBase):
    def __call__(self, strParameter=None):
        #print "action value before:", strParameter
        if strParameter is None:
            strParameter = self.value[0]
        #print "action value after:", strParameter
        #print "user value:", self.value[2]
        
        #outVal = u"{}".format(self.value[2]);
 
        #outVal = unicode(strParameter, "utf-8")

        outVal = strParameter
        if strParameter is not None and len(strParameter) > 0:
            #outVal = strParameter.encode("utf-8")
            print "outVal enc ", outVal

        #print "outVal ", outVal
        #print "value", self.value

        #self.plugin.DoCommand(outVal)
        #self.plugin.DoCommandLines(outVal, 'IRCODE')
        if len(self.value[2]) > 0:
            self.plugin.DoCommandLines(outVal, self.value[2])
        else:
            self.plugin.DoRawSend(outVal)


    def Configure(self, strParameter=None):
        if strParameter is None:
            strParameter = self.value[0]
        panel = eg.ConfigPanel()
        label = panel.StaticText(self.value[1])
        #ctrl = panel.TextCtrl(strParameter)
        ctrl = panel.TextCtrl(strParameter, size=(200, 100), style=wx.TE_MULTILINE)



        panel.sizer.Add(label, 0, wx.EXPAND)
        panel.sizer.Add((5, 5))
        panel.sizer.Add(ctrl, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(ctrl.GetValue())


ACTIONSNUM = (
  (hotKeys, 'Num0', 'Number 0', 'Number 0', u'NUM0'),
  (hotKeys, 'Num1', 'Number 1', 'Number 1', u'NUM1'),
  (hotKeys, 'Num2', 'Number 2', 'Number 2', u'NUM2'),
  (hotKeys, 'Num3', 'Number 3', 'Number 3', u'NUM3'),
  (hotKeys, 'Num4', 'Number 4', 'Number 4', u'NUM4'),
  (hotKeys, 'Num5', 'Number 5', 'Number 5', u'NUM5'),
  (hotKeys, 'Num6', 'Number 6', 'Number 6', u'NUM6'),
  (hotKeys, 'Num7', 'Number 7', 'Number 7', u'NUM7'),
  (hotKeys, 'Num8', 'Number 8', 'Number 8', u'NUM8'),
  (hotKeys, 'Num9', 'Number 9', 'Number 9', u'NUM9'),
  (hotKeys, 'ClearKey', 'Clear', 'Clear', u'CLEAR'),
  (hotKeys, 'EnterKey', 'Enter', 'Enter', u'ENTER'),
)

ACTIONSNAV = (
  (hotKeys, 'UpKey', 'Up', 'Up arrow', u'UP'),
  (hotKeys, 'DownKey', 'Down', 'Down arrow', u'DOWN'),
  (hotKeys, 'LeftKey', 'Left', 'Left arrow', u'LEFT'),
  (hotKeys, 'RightKey', 'Right', 'Right arrow', u'RIGHT'),
  (hotKeys, 'Ok', 'Select', 'Select', u'SELECT'),
  (hotKeys, 'Tivo', 'Tivo', 'Tivo', u'TIVO'),
  (hotKeys, 'LiveTV', 'Live TV', 'Go to live TV', u'LIVETV'),
  (hotKeys, 'Guide', 'Guide', 'Go to the Guide', u'GUIDE'),
  (hotKeys, 'Exit', 'Exit', 'Exit current menu', u'EXIT'),
  (hotKeys, 'Info', 'Info', 'Display info', u'INFO'),
  (hotKeys, 'Back', 'Back', 'Back', u'BACK'),
  (hotKeys, 'Dipsplay', 'Display', 'Toggle Display info', u'DISPLAY'),
  (hotKeys, 'Search', 'Search', 'Goto Search Menu', u'SEARCH'),
  (CreateTivoAction('TELEPORT'), 'NowPlaying', 'Now Playing', 'Navigate directly to Now Playing / My Shows', u'NOWPLAYING'),
  (CreateTivoAction('TELEPORT'), 'TivoMenu', 'Tivo Menu', 'Navigate directly to Tivo Menu', u'TIVO'),
  (RawKeys, 'OnePass', 'OnePass Manager', 'Open OnePass Manager', u'TELEPORT TIVO\rIRCODE NUM1\r'),
  (RawKeys, 'ToDoList', 'To Do List', 'Open To Do List', u'TELEPORT TIVO\rIRCODE NUM2\r'),
  (RawKeys, 'WishLists', 'WishList Searches', 'Open WishList Searches', u'TELEPORT TIVO\rIRCODE NUM3\r'),
  (RawKeys, 'Browse', 'Browse TV & Movies', 'Browse TV & MOvies', u'TELEPORT TIVO\rIRCODE NUM5\r'),
  (RawKeys, 'History', 'History', 'Browse', u'TELEPORT TIVO\rIRCODE NUM6\r'),
  (hotKeys, 'VOD', 'VOD', 'Activates VOD Menu', u'VIDEO_ON_DEMAND'),
  (hotKeys, 'Standby', 'Standby', 'Place Tivo into Standby Mode', u'STANDBY'),
  (hotKeys, 'Netflix', 'Netflix', 'Activates Netflix application', u'NETFLIX'),
)

ACTIONSCONT = (
  (hotKeys, 'ThumbUp', 'Thumbs Up', 'Thumbs Up', u'THUMBSUP'),
  (hotKeys, 'ThumbDown', 'Thumbs Down', 'Thumbs Down', u'THUMBSDOWN'),
  (hotKeys, 'ChannelUpKey', 'Channel Up', 'Channel up', u'CHANNELUP'),
  (hotKeys, 'ChannelDownKey', 'Channel Down', 'Channel down', u'CHANNELDOWN'),
  (hotKeys, 'Mute', 'Mute', 'Volume mute', u'MUTE'),
  (hotKeys, 'VolumeUpKey', 'Volume Up', 'Volume up', u'VOLUMEUP'),
  (hotKeys, 'VolumeDownKey', 'Volume Down', 'Volume down', u'VOLUMEDOWN'),
  (hotKeys, 'InputKey', 'TVInput', 'TV Input', u'TVINPUT'),
  (hotKeys, 'VIDEO_MODE_FIXED_480i', 'Video Mode Fixed 480i', 'Video Mode Fixed 480i', u'VIDEO_MODE_FIXED_480i'),
  (hotKeys, 'VIDEO_MODE_FIXED_480p', 'Video Mode Fixed 480p', 'Video Mode Fixed 480p', u'VIDEO_MODE_FIXED_480p'),
  (hotKeys, 'VIDEO_MODE_FIXED_720p', 'Video Mode Fixed 720p', 'Video Mode Fixed 720p', u'VIDEO_MODE_FIXED_720p'),
  (hotKeys, 'VIDEO_MODE_FIXED_1080i', 'Video Mode Fixed 1080i', 'Video Mode Fixed 1080i', u'VIDEO_MODE_FIXED_1080i'),
  (hotKeys, 'VIDEO_MODE_HYBRID', 'Video Mode Hybrid', 'Video Mode Hybrid', u'VIDEO_MODE_HYBRID'),
  (hotKeys, 'VIDEO_MODE_HYBRID_720p', 'Video Mode Hybrid 720p', 'Video Mode Hybrid 720p', u'VIDEO_MODE_HYBRID_720p'),
  (hotKeys, 'VIDEO_MODE_HYBRID_1080i', 'Video Mode Hybrid 1080i', 'Video Mode Hybrid 1080i', u'VIDEO_MODE_HYBRID_1080i'),
  (hotKeys, 'VIDEO_MODE_NATIVE', 'Video Mode Native', 'Video Mode Native', u'VIDEO_MODE_NATIVE'),
  (hotKeys, 'ClosedCapOn', 'Closed Caption On', 'Closed Captions On', u'CC_ON'),
  (hotKeys, 'ClosedCapOff', 'Closed Caption Off', 'Closed Captions Off', u'CC_OFF'),
  (hotKeys, 'Options', 'Options', 'Control display options for the program guide, the Now Playing List, and so on.', u'OPTIONS'),
  (hotKeys, 'ASPECT_CORRECTION_FULL', 'Full Aspect', 'Aspect Full', u'ASPECT_CORRECTION_FULL'),
  (hotKeys, 'ASPECT_CORRECTION_PANEL', 'Panel Aspect', 'Aspect Panel', u'ASPECT_CORRECTION_PANEL'),
  (hotKeys, 'ASPECT_CORRECTION_ZOOM', 'Zoom Aspect', 'Aspect Zoom', u'ASPECT_CORRECTION_ZOOM'),
  (hotKeys, 'ASPECT_CORRECTION_WIDE_ZOOM', 'Stretch Aspect', 'Aspect Wide Zoom', u'ASPECT_CORRECTION_WIDE_ZOOM'),
  (hotKeys, 'Window', 'Window Toggle', 'Toggle Aspect Mode', u'WINDOW'),
  (hotKeys, 'Zoom', 'Zoom Toggle', 'Toggle Aspect Mode', u'WINDOW'),
)


ACTIONSTRICK = (
  (hotKeys, 'Play', 'Play', 'Play', u'PLAY'),
  (hotKeys, 'ForwardKey', 'Forward', 'Cue quickly through the video', u'FORWARD'),
  (hotKeys, 'RewindKey', 'Reverse', 'Review quickly through the video', u'REVERSE'),
  (hotKeys, 'Pause', 'Pause', 'Pause the video', u'PAUSE'),
  (hotKeys, 'Slow', 'Slow', 'Play the video in slow motion', u'SLOW'),
  (hotKeys, 'ReplayKey', 'Replay', 'Replay the last 8 seconds of video', u'REPLAY'),
  (hotKeys, 'SkipKey', 'Advance', 'When playing video, jump to the begining or end; when cueing or reviewing, jump to the next tick-mark on the TrickPlay bar', u'ADVANCE'),
  (hotKeys, 'SkipShort', 'Skip Forward 14 Seconds', 'Two Replays followed by a Skip', u'REPLAY\rIRCODE REPLAY\rIRCODE ADVANCE'),
  (hotKeys, 'Skip9', 'Skip Forward 6 Seconds', 'Three Replays followed by a Skip', u'REPLAY\rIRCODE REPLAY\rIRCODE REPLAY\rIRCODE ADVANCE'),
  (hotKeys, 'Skip23', 'Skip Forward 22 Seconds', 'One Replay followed by a Skip', u'REPLAY\rIRCODE ADVANCE'),
  (hotKeys, 'SkipLong', 'Skip Forward 3 Minutes', 'One Replay followed by six Skips', u'REPLAY\rIRCODE ADVANCE\rIRCODE ADVANCE\rIRCODE ADVANCE\rIRCODE ADVANCE\rIRCODE ADVANCE\rIRCODE ADVANCE'),
  (hotKeys, 'ToggleQuickPlay', 'Quick Play Toggle', 'Toggle Quick Play Mode when playing video or live tv in buffer mode', u'CLEAR\rIRCODE PLAY\rIRCODE SELECT'),
  (hotKeys, 'Record', 'Record', 'Record', u'RECORD'),
  (hotKeys, 'Stop', 'Stop', 'Stops play', u'STOP'),
)

ACTIONSSHORT = (
  (hotKeys, 'ActionA', 'Action A', 'Yellow Action A', u'ACTION_A'),
  (hotKeys, 'ActionB', 'Action B', 'Blue Action B', u'ACTION_B'),
  (hotKeys, 'ActionC', 'Action C', 'Red Action C', u'ACTION_C'),
  (hotKeys, 'ActionD', 'Action D', 'Green Action D', u'ACTION_D'),
)



ACTIONS2 = (
#  (CreateStringAction("Please enter a custom IRCODE value:", ""), 'CustomAction', 'Custom Action', 'A Custom Action', u'{Ctrl+R}'),
  (CustomTivoAction, 'CustomTivoIRCODEAction', 'Custom IRCODE Action', 'A custom tivo network remote IRCODE action', ("", "Please enter a custom IRCODE value:", u'IRCODE')),
  (CustomTivoAction, 'CustomTivoKEYBOARDAction', 'Custom KEYBOARD Action', 'A custom tivo network remote KEYBOARD action', ("", "Please enter a custom KEYBOARD value:", u'KEYBOARD')),
  (CustomTivoAction, 'CustomTivoTELEPORTAction', 'Custom TELEPORT Action', 'A custom tivo network remote TELEPORT action', ("", "Please enter a custom TELEPORT value:", u'TELEPORT')),
  (CustomTivoAction, 'CustomTivoRAWAction', 'Custom Raw Action', 'A custom tivo network remote raw action. Use combinations of commands IRCODE, KEYBOARD, TELEPORT, SETCH, FORCECH with each command on one line.', ("", "Please enter a custom raw value:", '')),
#  (CreateTivoAction('IRCODE'), 'Guide', 'Guide', 'Toggle the Tivo Guide', u'GUIDE'),
)

SYMBOLS = {'-': 'MINUS', '=': 'EQUALS', '[': 'LBRACKET',
           ']': 'RBRACKET', '\\': 'BACKSLASH', ';': 'SEMICOLON',
           "'": 'QUOTE', ',': 'COMMA', '.': 'PERIOD', '/': 'SLASH',
           '`': 'BACKQUOTE', ' ': 'SPACE', '1': 'NUM1', '2': 'NUM2',
           '3': 'NUM3', '4': 'NUM4', '5': 'NUM5', '6': 'NUM6',
           '7': 'NUM7', '8': 'NUM8', '9': 'NUM9', '0': 'NUM0'}

SHIFT_SYMS = {'_': 'MINUS', '+': 'EQUALS', '{': 'LBRACKET',
              '}': 'RBRACKET', '|': 'BACKSLASH', ':': 'SEMICOLON',
              '"': 'QUOTE', '<': 'COMMA', '>': 'PERIOD', '?': 'SLASH',
              '~': 'BACKQUOTE', '!': 'NUM1', '@': 'NUM2', '#': 'NUM3',
              '$': 'NUM4', '%': 'NUM5', '^': 'NUM6', '&': 'NUM7',
              '*': 'NUM8', '(': 'NUM9', ')': 'NUM0'}

sock = None

def status_update():
    """ Read incoming messages from the socket in a separate thread and 
        display them.
   
    """
    global sock
    while True:
        try:
           status = sock.recv(80)
        except:
            log('TivoNetwork exception')
            status = ''
        status = status.strip().title()

	if status:
            print 'TivoNetwork Received: ' + str(status)

        if not status:
            log('TivoNetwork Closing')
            sock.close()
            sock = None
            break



class TivoNetwork(eg.PluginClass):
    text = Text
    
    def __init__(self):
        #group1 = self.AddGroup("Buttons","Predefinded Tivo Commands")
        #group1.AddActionsFromList(ACTIONS)
        groupNav = self.AddGroup("Navigation Buttons","Predefinded Tivo Navigation Buttons allow the user to navigate screens in the TiVo user interface.")
        groupNav.AddActionsFromList(ACTIONSNAV)
        groupNum = self.AddGroup("Numeric Buttons","Predefinded Tivo Numeric Buttons allow the user to enter a channel or other number.")
        groupNum.AddActionsFromList(ACTIONSNUM)
        groupCont = self.AddGroup("Control Buttons","Predefinded Tivo Control Buttons control the channel, volumn, and TV display, and allow the user to express preferences.")
        groupCont.AddActionsFromList(ACTIONSCONT)
        groupTrick = self.AddGroup("TrickPlay Buttons","Predefinded Tivo TrickPlay Buttons control the playback of video content.")
        groupTrick.AddActionsFromList(ACTIONSTRICK)
        groupShort = self.AddGroup("Shortcut Buttons","Predefinded Tivo Shortcut Buttons allow the user to activate shortcuts throughout the user interface.")
        groupShort.AddActionsFromList(ACTIONSSHORT)
        groupOther = self.AddGroup("Custom Actions","Other Configurable Tivo Actions")
        groupOther.AddActionsFromList(ACTIONS2)
        #self.AddActionsFromList(ACTIONS)
        #self.AddActionsFromList(ACTIONS2)

        #self.AddAction(SetAddress)
        groupOther.AddAction(SetAddress)
        #self.AddAction(SendTextToTivo)
        groupOther.AddAction(SendTextToTivo)
        #self.AddAction(TextSender)
        #self.AddAction(CreateTextSenderAction("Enter Text to send:", ""))

    def __start__(self, address, port, timeout=5, verbose=False):
        self.port = port
        self.address = address
        self.ADDR = (self.address,self.port);
        self.sock = None
        self.timeout = timeout
        #self.Connect()
        #self.sock = socket( AF_INET,SOCK_STREAM)
        if verbose:
            log = eg.Print
        else:
            def log(dummyMesg):
                pass
        log('TivoNetwork Start called: ' + str(self.ADDR))
        self.Test(verbose)

    def Test(self, verbose):
        global log
        if verbose:
            log = eg.Print
        else:
            def log(dummyMesg):
                pass


    def SetAddress(self, port, address):
        self.port = port
        self.address = address
        self.ADDR = (self.address,self.port);
        log('TivoNetwork SetAddress called: ' + str(self.ADDR))
        self.Disconnect()

    def SendText(self, sendText):
        sendText = eg.ParseString(sendText)

        log('TivoNetwork SendText called ' + str(self.ADDR) + ': ' + sendText)
        
        def AppendCommand(comms, *codes):
           for each in codes:
               comms.append('KEYBOARD %s\r' % each)

        commands = [];
        for ch in sendText:
            if 'A' <= ch <= 'Z':
                AppendCommand(commands, 'LSHIFT')
                AppendCommand(commands, ch)
            elif 'a' <= ch <= 'z':
                AppendCommand(commands, ch.upper())
            elif ch in SYMBOLS:
                AppendCommand(commands,SYMBOLS[ch])
            elif ch in SHIFT_SYMS:
                AppendCommand(commands, 'LSHIFT')
                AppendCommand(commands, SHIFT_SYMS[ch])

        self.DoRawSend(''.join(commands))
   


    def Connect(self):
        if self.sock:
            self.Disconnect()
        log('TivoNetwork Connecting: ' + str(self.ADDR))
        #ADDR = (self.address,self.port)
        try:
            self.sock = socket( AF_INET,SOCK_STREAM)
            self.sock.connect ((self.ADDR))
            self.sock.settimeout(self.timeout)

        except:
            print('TivoNetwork Connection Failed: ' + str(self.ADDR))

        global sock
        sock = self.sock
        if USESOCKETTIMEOUT:
            thread.start_new_thread(status_update, ())

    def Disconnect(self):
        if self.sock:
            try:
                log('TivoNetwork Closing connection: ' + str(self.ADDR))
                self.sock.close()
            except:
                log('TivoNetwork Failed close socket: ' + str(self.ADDR))
            try:
                del self.sock
            except:
                log('TivoNetwork Failed delete socket: ' + str(self.ADDR))
            self.sock = None


    def __stop__(self):
        self.Disconnect()

    def EnsureConnect(self):
        #log('Ensuring')
        if not self.sock:
            #log('no sock')
            self.Connect()
        self.RestartTimer()

    def RestartTimer(self):
        if self.timeout <= 0:
            return

        if USESOCKETTIMEOUT:
            if self.sock:
                self.sock.settimeout(self.timeout)
                log("resetting timeout")
        else:
            try: 
                self.timer.Cancel()
                del self.timer
            except: pass
            self.timer=MyTimer(t = self.timeout, plugin = self)

    def DoRawSendSplit(self, commandlines):
        commandlines = commandlines.replace('\n', '\r')

        if commandlines.endswith('\r'):
            commandlines = commandlines[:-1]


        lines = commandlines.split('\r')

        #log('DoRawSendSplit ' + str(len(lines)) + ', ' + str(lines))
        Delay = 0

        for each in lines:
            if Delay != 0:
               #log('Delay ' + str(Delay))
               if Delay > 100:
                   time.sleep(Delay / 1000)
                 
            
            if "TELEPORT" in each:
                Delay = 2500
            else:
                Delay = 100

            self.SendRaw(each + '\r')



    def DoRawSend(self, commandlines):
        commandlines = commandlines.replace('\n', '\r')
        if not commandlines.endswith('\r'):
            commandlines += '\r'
        self.SendRaw(commandlines)

    def DoCommandLines(self, commandlines, func):

        outVal = commandlines

        lines = commandlines.split('\n')

        if len(lines) > 1:
          outVal = lines[0] 
          for line in lines[1:]:
              outVal += '\r' + func + ' ' + line
        self.DoCommand(outVal, func)

    def DoCommand(self, command, func = 'IRCODE'):
        #log('TivoNetwork ' + str(self) + ', command ' + command)
        #HOST = self.address
        #PORT = self.port
        #ADDR = (HOST,PORT)
        #ADDR = (self.address,self.port)
        #log('TivoNetwork ' + str(ADDR) + ': IRCODE ' +  command)
        #BUFSIZE = 4096
        self.SendRaw(func + ' ' +  command + '\r')
        #cli = socket( AF_INET,SOCK_STREAM)
        #cli.connect ((ADDR))
        #cli.sendall(func + ' ' +  command + '\r')
        #cli.close


    def SendRaw(self, command, count = 0):
        #ADDR = (self.address,self.port)
        log('TivoNetwork ' + str(self.ADDR) + ': Raw ' +  command)
        #BUFSIZE = 4096
        #cli = socket( AF_INET,SOCK_STREAM)
        #cli.connect ((ADDR))
        #cli.sendall(command)
        #cli.close
        try:
            self.EnsureConnect()
            self.sock.sendall(command)
            if timeout == -1:
                self.Disconnect()
        #except socket.error, exc:
        except:
            log('send failed count = ' + str(count))
            #raise self.Exception(exc[1])
            if(count == 0):
                self.Connect()
                self.SendRaw(command, 1)



    def Configure(self, address="192.168.0.104", port=31339, timeout=5, verbose=False):
        text = self.text
        panel = eg.ConfigPanel()
        addressCtrl = panel.TextCtrl(address)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        
        timeoutCtrl = panel.SpinIntCtrl(timeout, min=-1, max=20)
        checkbox = panel.CheckBox(verbose, 'Debug')

        st1 = panel.StaticText(text.address)
        st2 = panel.StaticText(text.port)
        st3 = panel.StaticText(text.timeout)

        eg.EqualizeWidths((st1, st2, st3))

        box1 = panel.BoxedGroup(text.tcpBox, (st1, addressCtrl), (st2, portCtrl), (st3, timeoutCtrl))


        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            checkbox

        ])

        while panel.Affirmed():
            panel.SetResult(
                addressCtrl.GetValue(),
                portCtrl.GetValue(),
                timeoutCtrl.GetValue(),
                checkbox.GetValue()
            )


class SetAddress(eg.ActionClass):
    text = Text
    def __call__(self, address, port):
        self.plugin.SetAddress(address=address, port=port)
        
    def Configure(self, address='192.168.0.104', port=31339):

        text = self.text
        panel = eg.ConfigPanel()

        st1 = panel.StaticText(text.address)
        st2 = panel.StaticText(text.port)

        addressCtrl = panel.TextCtrl(address)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
 
        eg.EqualizeWidths((st1, st2))
                
        box1 = panel.BoxedGroup("Connection Settings", (st1, addressCtrl), (st2, portCtrl))

        panel.sizer.AddMany([
                            (box1, 0, wx.EXPAND)
                            ])
        while panel.Affirmed():
            panel.SetResult(
                addressCtrl.GetValue(),
                portCtrl.GetValue()
                            )

class SendTextToTivo(eg.ActionClass):
    text = Text
    def __call__(self, TextToSend):
        self.plugin.SendText(TextToSend)
        

    def Configure(self, TextToSend=""):

        text = self.text
        panel = eg.ConfigPanel()





        #label = panel.StaticText(text.sendtext)
        label = panel.StaticText('Enter Text to Send:')
        ctrl = panel.TextCtrl(TextToSend)
        #ctrl = panel.TextCtrl(strParameter, size=(200, 100), style=wx.TE_MULTILINE)


        panel.sizer.Add(label, 0, wx.EXPAND)
        panel.sizer.Add((5, 5))
        panel.sizer.Add(ctrl, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(ctrl.GetValue())




class MyTimer():

    def __init__(self, t, plugin):
        self.timer = Timer(t, self.Run)
        self.plugin = plugin
        self.timer.start()


    def Run(self):
        try:
            #log('My Timer Finished')
            self.plugin.Disconnect()
        except:
            pass


    def Cancel(self):
        self.timer.cancel()
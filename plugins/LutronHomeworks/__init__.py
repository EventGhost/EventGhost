# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate: 2009-02-07 20:13:27 +0100 (Sa, 07 Feb 2009) $
# $LastChangedRevision: 001 $
# $LastChangedBy: Fiasco $

"""<rst>
Adds actions to control `Lutron Homeworks <http://www.lutron.com/HomeWorks>`_.


**Lutron Homeworks Plugin**

Lutron Homeworks is a lighting home automation control that permits control
of individual zones of light in your home or scenes of grouped zones remotely via
network, rf or wall and table top keypads.


*Option/Setup*

Enter the TCP/IP address and the telnet port of your Lutron Homeworks Processor.  The 
default telnet port is 23. 

*Address Formatting*

enter as:
[a:b:c:d:e]
where above variables are based on device types below

RPM Dimmer Switch
a = processor 1-16
b = link 1
c = router 0-15
d = module 1-8
e = output 1-4

D48 Dimmer Switch
a = processor 1-16
b = link 4-6
c = d48 router 1-4
d = bus 1-12
e = dimmer 1-4

H48 Dimmer Switch
a = processor 1-16
b = link 4-6
c = d48 router 1-4
d = bus 1-6
e = dimmer 1-8

RF Dimmer Switch
a = processor 1-16
b = link 8
c = device type 1
d = dimmer 1-64

RF Keypad
a = processor 1-16
b = link 8
c = device type 2
d = dimmer 1-32

RF Repeater
a = processor 1-16
b = link 8
c = device type 3
d = dimmer 1-4

Keypad/Sivoia Control/CCO/CCI/TEL-9
a = processor 1-16
b = link 4-6
c = keypad 1-32

RS232 Port
a = processor 1-16
b = link 3 or 7
c = port 1

Grafik Eye
a = processor 1-16
b = link 4-6
c = Grafik Eye 1-8

Grafic Eye Single Zone
a = processor 1-16
b = link 4-6
c = Grafik Eye 1-8
d = output 1-8
"""

import eg

eg.RegisterPlugin(
    name="Lutron Homeworks",
    guid='{99FD5E02-A590-40C2-B65C-AACA11B9FC6A}',
    description=__doc__,
    author="Fiasco via Bitmonster",
    version="1.0." + "$LastChangedRevision: 001 $".split()[1],
    kind="external",
    canMultiLoad=True,
    createMacrosOnAdd=True
)

NV_ACTIONS = (
    ('SUNRISE', 'Get Sunrise Time', '38'),
)

EX_ACTIONS = (
    ('exSetAR', 'Set Aspect Ratio\n<br>value = 0-6'),
    ('SETBAUD', 'Set RS232 Baud Rate\n<BR>value = 300,600,1200,2400,4800,9600,19200,38400,57600,115200'),
    ('SETHAND', 'Set RS232 Handshaking\n<BR>value = None, HW'),
    ('FADEDIM', 'Fade one or more system dimmers\n<BR>value = intensity, fadetime, delaytime, address1,...,addressN'),
    ('FLASHDIM', 'Flash one or more system dimmers\n<BR>value = intensity, rate, address1,...,addressN'),
    ('STOPFLASH', 'Stop flashing one or more system dimmers\n<BR>value = address1,...,addressN'),
    ('RAISEDIM', 'Raise one or more system dimmers\n<BR>value = address1,...,addressN'),
    ('LOWERDIM', 'Lower one or more system dimmers\n<BR>value = address1,...,addressN'),
    ('STOPDIM', 'Stop one or more system dimmers\n<BR>value = address1,...,addressN'),
    ('DBP', 'Dimmer Button Press\n<BR>value = address1,buttonnumber'),
    ('DBDT', 'Dimmer Button Double Tap\n<BR>value = address1,buttonnumber'),
    ('RDL', 'Request Dimmer Level\n<BR>value = address1'),
    ('FRPM', 'Fade one or more RPM Zones\n<BR>value = intensity,fadetime,delay,address1,...,addressN'),
    ('FV', 'Fade one or more Vareo zones\n<BR>value = intensity,fadetime,delay,address1,....,addressN'),
    ('GSS', 'Grafik Eye Scene Select\n<BR>value = address,scenenumber'),
    ('RGS', 'Get Grafik Eye Current Scene\n<BR>value = address'),
    ('KBP', 'Simulate Keypad Button Press\n<BR>value = address,buttonnumber'),
    ('KBR', 'Simulate Keypad Button Release\n<BR>value = address,buttonnumber'),
    ('KBH', 'Simulate Keypad Button Held Down\n<BR>value = address,buttonnumber'),
    ('KBDT', 'Simulate Keypad Button Double Tap\n<BR>value = address,buttonnumber'),
    ('KE', 'Enable Keypad\n<BR>value = address'),
    ('KD', 'Disable Keypad\n<BR>value = address'),
    ('RKES', 'Get Keypad Enable/Disable Status\n<BR>value = address'),
    ('SETLED',
     'Sets Keypad LED State\n<BR>value = address,lednumber,ledstate (ledstate 0-off, 1-on, 2-flash1, 3-flash2)'),
    ('RKLS', 'Get Keypad LED State\n<BR>value = address'),
    ('SETLEDS',
     'Set Several Keypad LEDs\n<BR>value = address,00000000000000 (0-off, 1-on position represents button to toggle)'),
    ('CCOPULSE', 'Pulse CCO\n<BR>value = address,relaynumber,pulsetime'),
    ('CCOCLOSE', 'Close CCO\n<BR>value = address,relaynumber'),
    ('CCOOPEN', 'Open CCO\n<BR>value = address,relaynumber'),
    ('RKLBP', 'Get Last Button Pressed On Keypad\n<BR>value = address'),
    ('SVSS', 'Select Scene Command On Sivoia Control\n<BR>value = address,scene,delay'),
    ('RSVS', 'Return Scene Commmand Status On Sivoia Control\n<BR>value = address'),
    ('ST', 'Set System Time\n<BR>value = time (time format HH:MM:SS'),
    ('SD', 'Set System Date\n<BR>value = date (date format MM/DD/YY'),
    ('SSB', 'Scene Saver Mode Begin\n<BR>value = timeout (use CONT to start without a timeout)'),

)

FN_ACTIONS = (
    ('SUNRISE', 'Get Sunrise Time'),
    ('SUNSET', 'Get Sunset Time'),
    ('RST', 'Get Lutron System Time'),
    ('RST2', 'Get Lutron System Time (including seconds)'),
    ('RSD', 'Get Lutron System Date'),
    ('GETBAUD', 'Get RS232 Baud Rate'),
    ('GETHAND', 'Get RS232 Handshaking Type'),
    ('KBMON', 'Keypad Button Monitoring Enabled'),
    ('KBMOFF', 'Keypad Button Monitoring Disabled'),
    ('KLMON', 'Keypad LED Monitoring Enabled'),
    ('KLMOFF', 'Keypad LED Monitoring Disabled'),
    ('DLMMON', 'Dimmer Level Monitoring Enabled'),
    ('DLMOFF', 'Dimmer Level Monitoring Disabled'),
    ('GSMMON', 'Grafik Eye Scene Monitoring Enabled'),
    ('GSMOFF', 'Grafik Eye Scene Monitoring Disabled'),
    ('TCE', 'Timeclock Enabled'),
    ('TCD', 'Timeclock Disabled'),
    ('TCS', 'Get Timeclock State'),
    ('SST', 'Terminate Screen Saver Mode'),
    ('SSS', 'Get Screen Saver Mode State'),
    ('VMR', 'Begin Vacation Mode Recording'),
    ('VMP', 'Begin Vacation Mode Playback'),
    ('VMD', 'Disable Vacation Mode'),
    ('VMS', 'Get Vacation Mode State'),
    ('SMB', 'Begin Security Mode'),
    ('SMT', 'Terminate Security Mode'),
    ('SMS', 'Get Security Mode State'),
    ('PROMPTOFF', 'Disable RS232 L232> prompt'),
    ('PROMPTON', 'Enable RS232 L232> prompt'),
    ('EPRINT', 'Returns Event Log'),
    ('PROCADDR', 'Returns Current Processor Address'),
    ('RESET232', 'Reset RS232 Port Settings'),
    ('OSREV', 'Get Processor OS Revision'),
)
# pylint: enable-msg=C0301

import wx
import asynchat
import socket
import threading
from types import ClassType


class Text:
    tcpBox = "TCP/IP Settings"
    hostLabel = "Host:"
    portLabel = "Port:"
    userLabel = "Username:"
    passLabel = "Password:"
    eventBox = "Event generation"
    useNewEvents = "Use new events"


class LutronHomeworksSession(asynchat.async_chat):
    """
    Handles a Lutron Homeworks TCP/IP session.
    """

    def __init__(self, plugin, address):
        self.plugin = plugin
        print "init"
        print address

        # Call constructor of the parent class
        asynchat.async_chat.__init__(self)

        # Set up input line terminator
        self.set_terminator('\r\n')

        # Initialize input data buffer
        self.buffer = ''

        # create and connect a socket
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        eg.RestartAsyncore()
        self.settimeout(1.0)
        try:
            self.connect(address)
        except:
            pass

    def handle_connect(self):
        """
        Called when the active opener's socket actually makes a connection. 
        """
        self.plugin.TriggerEvent("Connected")
        self.plugin.myCommand(self.lutronuser + ',' + self.lutronpass)

    def handle_expt(self):
        # connection failed
        self.plugin.isSessionRunning = False
        self.plugin.TriggerEvent("NoConnection")
        self.close()

    def handle_close(self):
        """
        Called when the channel is closed.
        """
        self.plugin.isSessionRunning = False
        self.plugin.TriggerEvent("ConnectionLost")
        self.close()

    def collect_incoming_data(self, data):
        """
        Called with data holding an arbitrary amount of received data.
        """
        self.buffer = self.buffer + data

    def found_terminator(self):
        """
        Called when the incoming data stream matches the termination 
        condition set by set_terminator.
        """
        # call the plugins handler method
        self.plugin.ValueUpdate(self.buffer.decode('utf-8'))

        # reset the buffer
        self.buffer = ''


class NvAction(eg.ActionBase):
    def __call__(self):
        self.plugin.DoCommand(self.value)


class FnAction(eg.ActionBase):
    def __call__(self):
        self.plugin.DoCommand(self.value)


class ExAction(eg.ActionWithStringParameter):
    def __call__(self, param="0"):
        self.plugin.DoCommand("5110 " + self.value + "," + param)


class LutronHomeworks(eg.PluginBase):
    text = Text

    def __init__(self):
        self.host = "localhost"
        self.port = 4769
        self.lutronuser = "lutron"
        self.lutronpass = "lutron"
        self.isSessionRunning = False
        self.timeline = ""
        self.waitStr = None
        self.waitFlag = threading.Event()
        self.PlayState = -1
        self.lastMessage = {}
        self.lastSubtitleNum = 0
        self.lastSubtitlesEnabled = False
        self.lastAudioTrackNum = 0
        self.session = None

        group = self.AddGroup('Homeworks Commands (arguments)')
        for className, descr, scancode in NV_ACTIONS:
            clsAttributes = dict(name=descr, value=scancode)
            cls = ClassType(className, (NvAction,), clsAttributes)
            group.AddAction(cls)

        group = self.AddGroup('Homeworks Commands (no arguments)')
        for className, descr in FN_ACTIONS:
            clsAttributes = dict(name=descr, value=className)
            cls = ClassType(className, (FnAction,), clsAttributes)
            group.AddAction(cls)

        group = self.AddGroup('Extended Functions')
        for className, descr in EX_ACTIONS:
            clsAttributes = dict(
                name=descr.splitlines()[0].strip(),
                description=descr,
                value=className
            )
            cls = ClassType(className, (ExAction,), clsAttributes)
            group.AddAction(cls)

        self.AddAction(self.MyCommand)
        self.AddEvents()

    def __start__(
        self,
        host="localhost",
        port=4769,
        lutronuser="lutron",
        lutronpass="lutron",
        dummy1=None,
        dummy2=None,
        useNewEvents=False
    ):
        self.host = host
        self.port = port
        self.lutronuser = lutronuser
        self.lutronpass = lutronpass
        if useNewEvents:
            self.zpEvents = self.zpEvents2
        else:
            self.zpEvents = self.zpEvents1
        self.DoCommand(lutronuser + ',' + lutronpass)

    def __stop__(self):
        if self.isSessionRunning:
            self.session.close()

    zpEvents1 = {

    }

    zpEvents2 = {

    }

    def ValueUpdate(self, text):
        print "Value Update " + text

        if text == self.waitStr:
            self.waitStr = None
            self.waitFlag.set()
            return
        header = text[0:6]
        if not header.isdigit():
            header = self.lastHeader
            state = text
        else:
            self.lastHeader = header
            state = text[5:]
        self.lastMessage[header] = state
        zpEvent = self.zpEvents.get(header, None)
        if zpEvent is not None:
            if type(zpEvent) == type({}):
                eventString = zpEvent.get(state, None)
                if eventString is not None:
                    self.TriggerEvent(eventString)
                else:
                    self.TriggerEvent(header, [state])
            elif type(zpEvent) == type(()):
                suffix2 = zpEvent[1].get(state, None)
                if suffix2 is not None:
                    self.TriggerEvent(zpEvent[0] + "." + suffix2)
                else:
                    self.TriggerEvent(zpEvent[0] + "." + str(state))
            else:
                if not state:
                    state = None
                self.TriggerEvent(zpEvent, state)
            return
        if header == "1100":
            self.TriggerEvent("Timeline", [state])
        elif header == "1200":
            self.TriggerEvent("OSD", [state])
        elif header == "1000":
            state = int(state)
            self.PlayState = state
            if state == 0:
                self.TriggerEvent("StateClosed")
            elif state == 1:
                self.TriggerEvent("StateStopped")
            elif state == 2:
                self.TriggerEvent("StatePaused")
            elif state == 3:
                self.TriggerEvent("StatePlaying")
            else:
                self.PrintError("unknown State Change")
        elif header == "1600":
            self.lastAudioTrackNum = int(state)
            self.TriggerEvent("CurrentAudioTrack", int(state))
        elif header == "1601":
            self.TriggerEvent("AudioTrackCount", int(state))
        elif header == "1602":
            num = int(state[0:3])
            text = state[4:]
            self.TriggerEvent("AudioTrackName", (num, text))
            if num == self.lastAudioTrackNum:
                self.TriggerEvent("CurrentAudioTrackName", text)
        elif header == "1700":
            self.lastSubtitleNum = int(state)
            self.TriggerEvent("CurrentSubtitle", int(state))
        elif header == "1701":
            self.TriggerEvent("SubtitleCount", int(state))
        elif header == "1702":
            num = int(state[0:3])
            text = state[4:]
            self.TriggerEvent("SubtitleName", (num, text))
            if (
                self.lastSubtitlesEnabled
                and num == self.lastSubtitleNum
            ):
                self.TriggerEvent("CurrentSubtitleName", text)
        elif header == "1704":
            self.lastSubtitlesEnabled = not bool(int(state))
            if self.lastSubtitlesEnabled:
                self.TriggerEvent("SubtitlesEnabled")
            else:
                self.TriggerEvent("SubtitlesDisabled")
                self.TriggerEvent("CurrentSubtitleName")
        else:
            self.TriggerEvent(header, [state])

    @eg.LogIt
    def DoCommand(self, cmdstr):
        print("Do Command " + cmdstr);
        self.waitFlag.clear()
        self.waitStr = cmdstr
        if not self.isSessionRunning:
            self.session = LutronHomeworksSession(self, (self.host, self.port))
            self.isSessionRunning = True
            print ("session is running")
        try:
            print("trying " + cmdstr)
            self.session.sendall(cmdstr + "\r\n")
        except:
            self.isSessionRunning = False
            self.TriggerEvent('close')
            self.session.close()
        self.waitFlag.wait(1.0)
        self.waitStr = None
        self.waitFlag.set()

    def SetOSD(self, text):
        self.DoCommand("1200 " + text)

    def Configure(
        self,
        host="localhost",
        port=23,
        lutronuser="lutron",
        lutronpass="lutron",
        dummy1=None,
        dummy2=None,
        useNewEvents=True
    ):
        text = self.text
        panel = eg.ConfigPanel()
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        userCtrl = panel.TextCtrl(lutronuser)
        passCtrl = panel.TextCtrl(lutronpass)
        newEventCtrl = panel.CheckBox(useNewEvents, text.useNewEvents)

        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (text.hostLabel, hostCtrl),
            (text.portLabel, portCtrl),
            (text.userLabel, userCtrl),
            (text.passLabel, passCtrl),
        )
        eg.EqualizeWidths(tcpBox.GetColumnItems(0))
        eventBox = panel.BoxedGroup(
            text.eventBox,
            newEventCtrl,
        )
        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        panel.sizer.Add(eventBox, 0, wx.TOP | wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                userCtrl.GetValue(),
                passCtrl.GetValue(),
                None,
                None,
                newEventCtrl.GetValue(),
            )

    class MyCommand(eg.ActionWithStringParameter):
        name = "Raw Command"

        def __call__(self, cmd):
            print("mycommand " + cmd)
            self.plugin.DoCommand(cmd)

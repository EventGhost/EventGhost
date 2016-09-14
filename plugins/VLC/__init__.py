# -*- coding: utf-8 -*-
#
# Copyright (C) 2006 MonsterMagnet
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

"""<rst>

Adds actions to control the `VLC media player`_.

Enable the RC Interface or start VLC with:

**vlc.exe --extraintf=rc --rc-host=localhost:1234 --rc-quiet --rc-show-pos**

If you are using "MyCommand" remember that you can only execute commands that
are enabled in VLC!

`Help and bugreports <http://www.eventghost.org/forum/viewtopic.php?t=693>`_

.. _VLC media player: http://www.videolan.org/
"""


eg.RegisterPlugin(
    name = "VLC media player",
    author = "MonsterMagnet",
    version = "0.4.1486",
        kind = "program",
    guid = "{02929D1C-7567-414C-84D1-F8D71D6FD7B3}",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    description = __doc__,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACZElEQVR42pXSa0iTURgH"
        "8P/Z+8528TYJp7kPXqZUMOe8RFoRWFlUJKMIjBKDTEO6SBcSKgJBKmrYzchZoV2+CCFd"
        "zEG2D5EKsXQJbU1WTZemJpvOten7unUYEkRo88DD4eE5/DjPcw7BIquvQnQOAZ7N0vMX"
        "FzpDFio82itTbFrhGmIFQMeXqNQDbZ6vSwJaTu0s2yp3PCAkgI7h5MpS3cu7SwKaW589"
        "zdGotbMcD1Pvx/byfdodYQOXr9+JzFitcihTU+J4fg6WzwOTzm+25DPHjrjDApoOaooy"
        "NxYZYlM0CDLAaP97WLo6d1U87HseFtBaLLqVr/BXRQuBiBjAPQ4Y7cuaSgwz5f8FGkoy"
        "mDSvzZqZAqWEVoUU8HuBLjMczviV6ZWPrdyiQJ2uITNr6rVZFfgAqe8n2CjgF4lD96QK"
        "1qTtuTXVVaYFAfu93bJ2t/pEkqrwQmKcBBFzfhABgYcjcIy68cPSXZf+vfWq9vYn1z/A"
        "4JOy9Uxny6vOhFKpbNtxIpMIIWAYCAiBz+fHiGsSY4b7wbz+Zq8vb23x5ks9b/4Cxm5q"
        "boy/6z1qn46GfMseCNLWISiJpwhBwDOCGetbOA1tWD47hficNL1aZz/8Bxg21jJSU711"
        "YmBCOTQEJMQCEhHAsgRCOkmG/sapCcA2DCQpaH1VzCC3oUYpLzjLhQCX8WS22HzNhDnA"
        "N0an7qEyDwiCFImgO8UC9D8w9FnFclqjOZd7Pl+SXdsTAjjDmiss7zwd6sVHY3q+r8D8"
        "Hdn5XEojkgbFIE6sJwWm6hDwYr/okIz367GENRMtqihs9Df+Brue2BE7hqGjAAAAAElF"
        "TkSuQmCC"
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=693",
)



import eg
import wx
import os
import asynchat
import socket
import _winreg
import codecs
from win32api import ShellExecute
from threading import Event
from datetime import timedelta



def GetVlcPath():
    """
    Tries to get the path of VLC's executable through querying the Windows
    registry.
    """
    try:
        return _winreg.QueryValue(
            _winreg.HKEY_LOCAL_MACHINE,
            "Software\\VideoLAN\\VLC"
        )
    except WindowsError:
        return os.path.join(
            eg.folderPath.ProgramFiles,
            "VideoLAN\\VLC\\vlc.exe"
        )


def GetChoices():
    f = codecs.open(eg.folderPath.RoamingAppData+"\\vlc\\vlcrc",'r','utf-8')
    tmpLst = []
    for line in f:
        if line[:4] == "#key" and "=" in line:
            i = line.find("=")
            tmpLst.append((prev,line[1:i]))
        else:
            i = line.rfind("(")
            prev = line[1:i]
    f.close()
    return tmpLst



class VlcSession(asynchat.async_chat):

    def __init__ (self, plugin, address):
        # Call constructor of the parent class
        asynchat.async_chat.__init__(self)

        # Set up input line terminator
        self.set_terminator('\r\n')

        # Initialize input data buffer
        self.data = ''
        self.plugin = plugin
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        eg.RestartAsyncore()
        try:
            self.connect(address)
        except:
            pass


    def handle_connect(self):
        # connection succeeded
        self.plugin.TriggerEvent("Connected")
        self.sendall(self.plugin.connectedevent)


    def handle_expt(self):
        # connection failed
        self.plugin.isDispatcherRunning = False
        self.plugin.TriggerEvent("NoConnection")
        self.close()


    def handle_close(self):
        # connection closed
        self.plugin.isDispatcherRunning = False
        self.plugin.TriggerEvent("ConnectionLost")
        self.close()


    def collect_incoming_data(self, data):
        # received a chunk of incoming data
        self.data = self.data + data


    def found_terminator(self):
        self.plugin.ValueUpdate(self.data)
        self.data = ''



class ActionPrototype(eg.ActionBase):

    value = None # the actual value will be defined through AddActionsFromList


    def __call__(self):
        return self.plugin.Push(self.value + "\r\n")



class Start(eg.ActionBase):

    class text:
        additionalArgs = "Additional command line arguments:"
        resultingCmdLine = "Resulting command line:"


    def __call__(self, cmdLineArgs=""):
        vlcPath = GetVlcPath()
        return ShellExecute(
            0,
            None,
            vlcPath,
            self.GetCmdLineArgs(cmdLineArgs),
            None, #os.path.dirname(vlcPath),
            1
        )


    def GetCmdLineArgs(self, cmdLineArgs):
        args = '--extraintf=rc --rc-host=%s:%d --rc-quiet --rc-show-pos' % (
            self.plugin.host,
            self.plugin.port
        )
        if cmdLineArgs:
            args = args + " " + cmdLineArgs
        return args


    def GetLabel(self, cmdLineArgs=""):
        if cmdLineArgs:
            return self.name + ": " + cmdLineArgs
        else:
            return self.name


    def Configure(self, cmdLineArgs=""):
        vlcPath = GetVlcPath()
        panel = eg.ConfigPanel()
        cmdLineCtrl = panel.TextCtrl(cmdLineArgs)
        resultCtrl = eg.StaticTextBox(panel)
        def OnTextChange(event=None):
            cmdLineArgs = cmdLineCtrl.GetValue()
            cmdString = '"%s" %s' % (vlcPath, self.GetCmdLineArgs(cmdLineArgs))
            resultCtrl.SetValue(cmdString)
            if event:
                event.Skip()
        OnTextChange()
        cmdLineCtrl.Bind(wx.EVT_TEXT, OnTextChange)

        panel.sizer.AddMany([
            (panel.StaticText(self.text.additionalArgs), 0, wx.BOTTOM, 3),
            (cmdLineCtrl, 0, wx.EXPAND|wx.BOTTOM, 5),
            ((15, 15), ),
            (panel.StaticText(self.text.resultingCmdLine), 0, wx.BOTTOM, 3),
            (resultCtrl, 1, wx.EXPAND),
        ])
        while panel.Affirmed():
            panel.SetResult(cmdLineCtrl.GetValue())



class GetSomeInfo(eg.ActionBase):

    class text:
        label = "Select type of information:"
        choices = (
            'Show items currently in playlist',
            'Current playlist status',
            'Title in current item',
            'Next title in current item',
            'Previous title in current item',
            'Chapter in current item',
            'Next chapter in current item',
            'Previous chapter in current item',
            "Information about stream",
            "Statistical information",
            "Elapsed seconds",
            "Is playing status",
            "Title of the current stream",
            "Length of the current stream [s]",
            'Volume',
            'Audio device',
            'Audio channels',
            'Audio track',
            'Video track',
            'Video aspect ratio',
            'Video crop',
            'Video zoom',
            'Subtitles track',
            'Help message',
            'Longer help message',
        )


    CHOICES = (
            'playlist',
            'status',
            'title',
            'title_n',
            'title_p',
            'chapter',
            'chapter_n',
            'chapter_p',
            'info',
            'stats',
            'get_time',
            'is_playing',
            'get_title',
            'get_length',
            'volume',
            'adev',
            'achan',
            'atrack',
            'vtrack',
            'vratio',
            'vcrop',
            'vzoom',
            'strack',
            'help',
            'longhelp',
    )


    def __call__(self, index = 0):
        if self.plugin.waitFlag.isSet():
            self.plugin.lastMessage = []
            self.plugin.waitFlag.clear()
            self.plugin.Push(self.CHOICES[index] + "\r\n")
            self.plugin.waitFlag.wait(0.1)
            self.plugin.waitFlag.set()
            return self.plugin.lastMessage
        else:
            return None


    def GetLabel(self, index):
        return "%s: %s" % (self.name,self.text.choices[index])


    def Configure(self, index = 0):
        panel = eg.ConfigPanel()
        mySizer = panel.sizer
        staticText = panel.StaticText(self.text.label)
        choiceCtrl=wx.Choice(
            panel,
            choices=self.text.choices,
        )
        choiceCtrl.SetSelection(index)
        mySizer.Add(staticText, 0, wx.TOP, 15)
        mySizer.Add(choiceCtrl, 0, wx.TOP, 2)
        while panel.Affirmed():
            panel.SetResult(choiceCtrl.GetSelection())



class SimulateKey(eg.ActionBase):

    class text:
        label = "Select hotkey:"

    def __call__(self, index = 0):
        choices = GetChoices()
        self.plugin.Push("key " + choices[index][1] + "\r\n")


    def GetLabel(self, index):
        choices = GetChoices()
        return "%s: %s" % (self.name,choices[index][0])


    def Configure(self, index = 0):
        panel = eg.ConfigPanel()
        mySizer = panel.sizer
        staticText = panel.StaticText(self.text.label)
        choices = GetChoices()
        choiceCtrl=wx.Choice(
            panel,
            choices=[item[0] for item in choices],
        )
        choiceCtrl.SetSelection(index)
        mySizer.Add(staticText, 0, wx.TOP, 15)
        mySizer.Add(choiceCtrl, 0, wx.TOP, 2)
        while panel.Affirmed():
            panel.SetResult(choiceCtrl.GetSelection())


class SimulKey(eg.ActionBase):

    def __call__(self, index = 0):
        self.plugin.Push("key " + self.value + "\r\n")



class GetHotkeys(eg.ActionBase):

    def __call__(self):
        return GetChoices()


class GetTime(eg.ActionBase):

    def __call__(self):
        if self.plugin.waitFlag.isSet():
            self.plugin.waitFlag.clear()
            self.plugin.Push('get_time' + "\r\n")
            self.plugin.waitFlag.wait(0.05)
            self.plugin.lastMessage = []
            self.plugin.waitFlag.clear()
            self.plugin.Push('get_time' + "\r\n")
            self.plugin.Push('get_length' + "\r\n")
            self.plugin.waitFlag.wait(0.1)
            self.plugin.waitFlag.set()
            res = self.plugin.lastMessage
            if len(res) == 2:
                elaps = timedelta(seconds=int(res[0]))
                rem   = timedelta(seconds=int(res[1])-int(res[0]))
                return [str(elaps), str(rem)]
        return None


class GetLength(eg.ActionBase):

    def __call__(self):
        if self.plugin.waitFlag.isSet():
            self.plugin.lastMessage = []
            self.plugin.waitFlag.clear()
            self.plugin.Push('get_length' + "\r\n")
            self.plugin.waitFlag.wait(0.1)
            self.plugin.waitFlag.set()
            res = self.plugin.lastMessage
            res = res[1] if len(res)==2 else res[0]
            lngth = timedelta(seconds=int(res))
            return str(lngth)
        return None


class SwitchTrack(eg.ActionBase):

    def __call__(self):
        if self.plugin.waitFlag.isSet():
            self.plugin.lastMessage = []
            self.plugin.waitFlag.clear()
            self.plugin.Push(self.value[0] + "\r\n")
            self.plugin.waitFlag.wait(0.05)
            self.plugin.lastMessage = []
            self.plugin.waitFlag.clear()
            self.plugin.Push(self.value[0] + "\r\n")
            self.plugin.waitFlag.wait(0.1)
            self.plugin.waitFlag.set()
            res = self.plugin.lastMessage
            menu = []
            i = 0
            for item in res:
                if item[0] == "|":
                    tmp = item.split(" - ")
                    if tmp[-1][-1] == "*":
                        ix = i
                    i += 1
                    menu.append(tmp)
            if len(menu) > 1:
                ix += self.value[1]
                if ix == len(menu):
                    ix = 0
                elif ix == -1:
                    ix = len(menu)-1
                self.plugin.Push(self.value[0]+" %s\r\n" % menu[ix][0][1:])
                return " - ".join(menu[ix][1:])
        return None


class MyCommand(eg.ActionBase):

    class text:
        label = (
            "My Command: (Type 'H' to see a list of all available commands.)"
        )


    def __call__(self, text):
        self.plugin.Push(eg.ParseString(text).encode('utf-8') + "\r\n")


    def Configure(self, text="marq-marquee EventGhost"):
        panel = eg.ConfigPanel()
        mySizer = wx.FlexGridSizer(rows=3)
        staticText = panel.StaticText(self.text.label)
        textCtrl = panel.TextCtrl(text)
        mySizer.Add(staticText, 0, wx.EXPAND|wx.ALL, 5)
        mySizer.Add(textCtrl, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(mySizer)
        while panel.Affirmed():
            panel.SetResult(textCtrl.GetValue())



class Seek(eg.ActionBase):
    class text:
        label = "Seek value:"
        unit = "Unit"
        unitChoice = ("Second","Percent")
        pos = "Positioning"
        posChoice = ("Relatively","Absolute")
        dir = "Direction"
        dirChoice = ("Forward","Backward")


    def __call__(self, value, unit = 0, pos = 0, dir = 0):
        val = eg.ParseString(value)
        if pos: #Absolute
            self.plugin.Push("seek %s%s\r\n" % (val,("","%")[unit]))
        elif self.plugin.waitFlag.isSet():
            val = int(val)
            dir = (1,-1)[dir]
            self.plugin.waitFlag.clear()
            self.plugin.Push('get_time' + "\r\n")
            self.plugin.waitFlag.wait(0.05)
            self.plugin.lastMessage = []
            self.plugin.waitFlag.clear()
            self.plugin.Push('get_time' + "\r\n")
            self.plugin.Push('get_length' + "\r\n")
            self.plugin.waitFlag.wait(0.1)
            self.plugin.waitFlag.set()
            pos = int(self.plugin.lastMessage[0])
            length = int(self.plugin.lastMessage[1])
            if not unit: #Seconds
                pos += dir*val
            else:        #Percents
                pos += dir*val*length/100
            self.plugin.Push("seek %s\r\n" % str(pos))


    def GetLabel(self, value, unit, pos, dir):
        if pos:
            return "%s: %s%s, %s" % (self.name,value,("","%")[unit],self.text.posChoice[pos])
        else:
            return "%s: %s%s, %s, %s" % (self.name,value,("","%")[unit],self.text.posChoice[pos],self.text.dirChoice[dir])


    def Configure(self, value="60", unit = 0, pos = 0, dir = 0):
        text = self.text
        panel = eg.ConfigPanel()
        mySizer = panel.sizer
        width = 120
        staticText = panel.StaticText(text.label)
        textCtrl = panel.TextCtrl(value, size = (2*width+10,-1))
        unitSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.unit),
            wx.HORIZONTAL
        )
        rb1 = panel.RadioButton(not unit, text.unitChoice[0], style=wx.RB_GROUP, size = (width,-1))
        rb2 = panel.RadioButton(unit, text.unitChoice[1])
        unitSizer.Add(rb1, 1)
        unitSizer.Add(rb2, 1)

        posSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.pos),
            wx.HORIZONTAL
        )
        rb3 = panel.RadioButton(not pos, text.posChoice[0], style=wx.RB_GROUP, size = (width,-1))
        rb4 = panel.RadioButton(pos, text.posChoice[1])
        posSizer.Add(rb3, 1)
        posSizer.Add(rb4, 1)

        dirSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.dir),
            wx.HORIZONTAL
        )
        rb5 = panel.RadioButton(not dir, text.dirChoice[0], style=wx.RB_GROUP, size = (width,-1))
        rb6 = panel.RadioButton(dir, text.dirChoice[1])
        dirSizer.Add(rb5, 1)
        dirSizer.Add(rb6, 1)

        def OnRadioButton(event=None):
            flag = rb3.GetValue()
            mySizer.Show(dirSizer,flag,True)
            mySizer.Layout()
            if event:
                event.Skip()
        rb3.Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
        rb4.Bind(wx.EVT_RADIOBUTTON, OnRadioButton)

        mySizer.Add(staticText, 0, wx.TOP, 5)
        mySizer.Add(textCtrl, 0, wx.TOP, 2)
        mySizer.Add(unitSizer, 0, wx.TOP, 15)
        mySizer.Add(posSizer, 0, wx.TOP, 15)
        mySizer.Add(dirSizer, 0, wx.TOP, 15)
        OnRadioButton()
        while panel.Affirmed():
            panel.SetResult(
                textCtrl.GetValue(),
                rb2.GetValue(),
                rb4.GetValue(),
                rb6.GetValue(),
                )



class VLC(eg.PluginBase):

    class text:
        eventBox = "Event generation"
        showFeedbackEvents = "Show VLC feedback events"
        tcpBox = "TCP/IP Settings"
        host = "Host:"
        port = "Port:"


    def __init__(self):
        self.AddEvents()
        self.AddActionsFromList(ACTIONS)
        self.waitFlag = Event()
        self.lastMessage = []
        self.waitFlag.set()


    def __start__(self, host="localhost", port=1234, showFeedbackEvents=True):
        self.host = host
        self.port = port
        self.dispatcher = None
        self.isDispatcherRunning = False
        self.showFeedbackEvents = showFeedbackEvents


    def __stop__(self):
        if self.isDispatcherRunning:
            self.dispatcher.close()


    def ValueUpdate(self, text):
        state = text.decode('utf-8')
        if not self.waitFlag.isSet():
            self.lastMessage.append(state)
            return
        if self.showFeedbackEvents:
            self.TriggerEvent(state)


    def Push(self, data):
        if not self.isDispatcherRunning:
            self.connectedevent = data
            self.dispatcher = VlcSession(self, (self.host, self.port))
            self.isDispatcherRunning = True
        try:
            if self.dispatcher.connected:
                self.dispatcher.sendall(data)
            return True
        except:
            self.isDispatcherRunning = False
            self.PrintError("Error sending data to VLC.")
            self.dispatcher.close()
            return False


    def Configure(self, host="localhost", port=1234, showFeedbackEvents=True):
        text = self.text
        panel = eg.ConfigPanel()
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port)
        checkBox = panel.CheckBox(showFeedbackEvents, text.showFeedbackEvents)
        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (text.host, hostCtrl),
            (text.port, portCtrl),
        )
        eg.EqualizeWidths(tcpBox.GetColumnItems(0))
        eventBox = panel.BoxedGroup(text.eventBox, checkBox)
        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        panel.sizer.Add(eventBox, 0, wx.TOP|wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                checkBox.GetValue()
            )



ACTIONS = (
    (
        Start,
        'Start',
        'Start',
        'Starts VLC with the needed command line arguments.',
        None
    ),
    (
        ActionPrototype,
        'Quit',
        'Quit',
        'Quit VLC',
        'quit'
    ),
    (
        ActionPrototype,
        'Play',
        'Play',
        'Start playing',
        'pause'
    ),
    (
        ActionPrototype,
        'Pause',
        'Pause',
        'Toggle play/pause',
        'pause'
    ),
    (
        ActionPrototype,
        'Stop',
        'Stop',
        'Stop and close current item',
        'stop'
    ),
    (
        ActionPrototype,
        'FastForward',
        'Fast Forward',
        'Skip ~5 sec forward',
        'fastforward'
    ),
    (
        ActionPrototype,
        'FastRewind',
        'Fast Rewind',
        'Skip ~5 sec back',
        'rewind'
    ),
    (
        ActionPrototype,
        'PlayFaster',
        'Play Faster',
        'Play faster',
        'faster'
    ),
    (
        ActionPrototype,
        'PlaySlower',
        'Play Slower',
        'Play slower',
        'slower'
    ),
    (
        ActionPrototype,
        'PlayNormal',
        'Play Normal',
        'Play normal',
        'normal'
    ),
    (
        Seek,
        'Seek',
        'Seek',
        'Seek.',
        None
    ),
    (
        ActionPrototype,
        'Fullscreen',
        'Fullscreen',
        'Toggle fullscreen',
        'f'
    ),
    (
        ActionPrototype,
        'NextPlaylistItem',
        'Next Playlist Item',
        'Jump forward to the next item in playlist',
        'next'
    ),
    (
        ActionPrototype,
        'PreviousPlaylistItem',
        'Previous Playlist Item',
        'Jump backward to the previous playlist item',
        'prev'
    ),
    (
        ActionPrototype,
        'NextTitle',
        'Next Title',
        'Next title in current item',
        'title_n'
    ),
    (
        ActionPrototype,
        'PreviousTitle',
        'Previous Title',
        'Previous title in current item',
        'title_p'
    ),
    (
        ActionPrototype,
        'NextChapter',
        'Next Chapter',
        'Next chapter in current item',
        'chapter_n'
    ),
    (
        ActionPrototype,
        'PreviousChapter',
        'Previous Chapter',
        'Previous chapter in current item',
        'chapter_p'
    ),
    (
        ActionPrototype,
        'CurrentPlaylistStatus',
        'Current Playlist Status',
        'If VLC feedback is enabled in plugin settings, the logger shows '
            'information about the current playlist status.',
        'status'
    ),
    (
        ActionPrototype,
        'StreamInfo',
        'Stream Info',
        'If VLC feedback is enabled in plugin settings, the logger shows '
            'information about the current stream.',
        'info'
    ),
    (
        ActionPrototype,
        'ShowPlaylist',
        'Show Playlist',
        'If VLC feedback is enabled in plugin settings, the logger shows '
            'information about the current playlist.',
        'playlist'
    ),
    (
        ActionPrototype,
        'ClearPlaylist',
        'Clear Playlist',
        'Clear the playlist and close current item',
        'clear'
    ),
    (
        ActionPrototype,
        'VolumeUp',
        'Volume Up',
        'Volume up',
        'volup'
    ),
    (
        ActionPrototype,
        'VolumeDown',
        'Volume Down',
        'Volume down',
        'voldown'
    ),
    (
        MyCommand,
        'MyCommand',
        'My Command',
        'Here you can enter your own command, ie. show a custom text message.',
        None
    ),
    (
        SimulateKey,
        'SimulateKey',
        'Simulate hotkey press',
        'Simulates pressing hotkey.',
        None
    ),
    (
        GetHotkeys,
        'GetHotkeys',
        'Get list of hotkeys',
        'Get a list of hotkeys for menu create.',
        None
    ),
    (
        GetSomeInfo,
        'GetSomeInfo',
        'Get some info',
        'Returns information whose type is chosen by user.',
        None
    ),
    (
        GetTime,
        'GetTime',
        'Get time',
        "Returns elapsed and remaining times.",
        'get_time'
    ),
    (
        GetLength,
        'GetLength',
        'Get length',
        'Returns the length of the current stream.',
        'get_length'
    ),
    (
        SwitchTrack,
        'NextAtrack',
        'Next audiotrack',
        'Switch to next audiotrack.',
        ('atrack',1)
    ),
    (
        SwitchTrack,
        'PreviousAtrack',
        'Previous audiotrack',
        'Switch to previous audiotrack.',
        ('atrack',-1)
    ),
    (
        SwitchTrack,
        'NextStrack',
        'Next subtitles',
        'Switch to next subtitles.',
        ('strack',1)
    ),
    (
        SwitchTrack,
        'PreviousStrack',
        'Previous subtitles',
        'Switch to previous subtitles.',
        ('strack',-1)
    ),
    (
        ActionPrototype,
        'Help',
        'Help',
        'If VLC feedback is enabled in plugin settings, the logger shows all '
            'available commands, use <i>"My Command"</i> to execute them.',
        'H'
    ),
    (
        eg.ActionGroup,
        'DVDmenu',
        'DVD menu control',
        'DVD menu control.',
        (
            (
                SimulKey,
                'KeyDiscMenu',
                'Go to the DVD menu',
                'Go to the DVD menu.',
                "key-disc-menu"
            ),
            (
                SimulKey,
                'KeyNavUp',
                'Navigate up',
                'Navigate up.',
                "key-nav-up"
            ),
            (
                SimulKey,
                'KeyNavDown',
                'Navigate down',
                'Navigate down.',
                "key-nav-down"
            ),
            (
                SimulKey,
                'KeyNavLeft',
                'Navigate left',
                'Navigate left.',
                "key-nav-left"
            ),
            (
                SimulKey,
                'KeyNavRight',
                'Navigate right',
                'Navigate right.',
                "key-nav-right"
            ),
            (
                SimulKey,
                'KeyNavActivate',
                'Activate',
                'Activate.',
                "key-nav-activate"
            ),
            #(
            #    SimulKey,
            #    'KeyTitlePrev',
            #    'Select previous DVD title',
            #    'Select previous DVD title.',
            #    "key-title-prev"
            #),
            #(
            #    SimulKey,
            #    'KeyTitleNext',
            #    'Select next DVD title',
            #    'Select next DVD title.',
            #    "key-title-next"
            #),
            #(
            #    SimulKey,
            #    'KeyChapterPrev',
            #    'Select prev DVD chapter',
            #    'Select prev DVD chapter.',
            #    "key-chapter-prev"
            #),
            #(
            #    SimulKey,
            #    'KeyChapterNext',
            #    'Select next DVD chapter',
            #    'Select next DVD chapter.',
            #    "key-chapter-next"
            #),
        )
    ),
)

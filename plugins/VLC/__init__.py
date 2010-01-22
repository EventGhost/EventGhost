# This file is a plugin for EventGhost.
# Copyright (C) 2006 MonsterMagnet
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

"""<rst>

Adds actions to control the `VLC media player`_.

Enable the RC Interface or start VLC with:

**vlc.exe --extraintf=rc --rc-host=localhost:1234 --rc-quiet --rc-show-pos**

If you are using "MyCommand" remember that you can only execute commands that 
are enabled in VLC!

`Help and bugreports <http://www.eventghost.org/forum/viewtopic.php?t=693>`_

.. _VLC media player: http://www.videolan.org/
"""


import eg

eg.RegisterPlugin(
    name = "VLC media player",
    author = "MonsterMagnet",
    version = "0.4." + "$LastChangedRevision$".split()[1],
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

import wx
import os
import asynchat
import socket
import _winreg
from win32api import ShellExecute




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
            
            
            
class MyCommand(eg.ActionBase):
    class text:
        label = (
            "My Command: (Type 'H' to see a list of all available commands.)"
        )
        
    def __call__(self, text):
        self.plugin.Push(eg.ParseString(text) + "\r\n")
               
            
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
        else:
            self.plugin.seekStatus = 1
            self.plugin.unit = unit
            self.plugin.seek = int(val)
            self.plugin.seek *= (1,-1)[dir]
            self.plugin.Push("get_length\r\n")

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
                             
                            
    def __start__(self, host="localhost", port=1234, showFeedbackEvents=True): 
        self.host = host
        self.port = port
        self.dispatcher = None
        self.isDispatcherRunning = False
        self.feedback = ""
        self.showFeedbackEvents = showFeedbackEvents
        self.seekStatus = 0
        self.length = 0
        self.seek = 0
        self.unit = 0
       
    
    def __stop__(self):
        if self.isDispatcherRunning:
            self.dispatcher.close()


    def ValueUpdate(self, text):
        state = text.decode('utf-8')
        if not self.seekStatus:
            if self.showFeedbackEvents:
                self.TriggerEvent(state)
        elif self.seekStatus == 1:
            try:
                self.length = int(state)+self.seek
                self.Push("get_time\r\n")
                self.seekStatus = 2
            except:
                pass
        else: #self.seekStatus == 2
            try:
                if not self.unit: #Seconds
                    pos = int(state)+self.seek
                else:             #Percents
                    pos = int(state)+self.seek*(self.length/100)
                self.Push("seek "+str(pos)+"\r\n")
                self.seekStatus = 0
            except:
                pass


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
        ActionPrototype,
        'Help', 
        'Help', 
        'If VLC feedback is enabled in plugin settings, the logger shows all '
            'available commands, use <i>"My Command"</i> to execute them.', 
        'H'
    ),
)

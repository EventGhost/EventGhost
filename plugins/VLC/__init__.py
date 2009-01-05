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


ACTIONS = (
    (
        'Play', 
        'Play', 
        'Start playing', 
        'pause'
    ),
    (
        'Pause', 
        'Pause', 
        'Toggle play/pause', 
        'pause'
    ),
    (
        'Stop', 
        'Stop', 
        'Stop and close current item', 
        'stop'
    ),
    (
        'FastForward', 
        'Fast Forward', 
        'Skip ~5 sec forward', 
        'fastforward'
    ),
    (
        'FastRewind', 
        'Fast Rewind', 
        'Skip ~5 sec back', 
        'rewind'
    ),
    (
        'PlayFaster', 
        'Play Faster', 
        'Play faster', 
        'faster'
    ),
    (
        'PlaySlower', 
        'Play Slower', 
        'Play slower', 
        'slower'
    ),
    (
        'PlayNormal', 
        'Play Normal', 
        'Play normal', 
        'normal'
    ),
    (
        'Fullscreen', 
        'Fullscreen', 
        'Toggle fullscreen', 
        'f'
    ),
    (
        'NextPlaylistItem', 
        'Next Playlist Item', 
        'Jump forward to the next item in playlist', 
        'next'
    ),
    (
        'PreviousPlaylistItem', 
        'Previous Playlist Item', 
        'Jump backward to the previous playlist item',
        'prev'
    ),
    (
        'NextTitle', 
        'Next Title', 
        'Next title in current item', 
        'title_n'
    ),
    (
        'PreviousTitle', 
        'Previous Title', 
        'Previous title in current item', 
        'title_p'
    ),
    (
        'NextChapter', 
        'Next Chapter', 
        'Next chapter in current item', 
        'chapter_n'
    ),
    (
        'PreviousChapter', 
        'Previous Chapter', 
        'Previous chapter in current item', 
        'chapter_p'
    ),
    (
        'CurrentPlaylistStatus', 
        'Current Playlist Status', 
        'If VLC feedback is enabled in plugin settings, the logger shows '
            'information about the current playlist status.', 
        'status'
    ),
    (
        'StreamInfo', 
        'Stream Info', 
        'If VLC feedback is enabled in plugin settings, the logger shows '
            'information about the current stream.', 
        'info'
    ),
    (
        'ShowPlaylist', 
        'Show Playlist', 
        'If VLC feedback is enabled in plugin settings, the logger shows '
            'information about the current playlist.', 
        'playlist'
    ),
    (
        'ClearPlaylist', 
        'Clear Playlist', 
        'Clear the playlist and close current item', 
        'clear'
    ),
    (
        'VolumeUp', 
        'Volume Up', 
        'Volume up', 
        'volup'
    ),
    (
        'VolumeDown', 
        'Volume Down', 
        'Volume down', 
        'voldown'
    ),
    (
        'Quit', 
        'Quit', 
        'Quit VLC', 
        'quit'
    ),
    (
        'Help', 
        'Help', 
        'If VLC feedback is enabled in plugin settings, the logger shows all '
            'available commands, use <i>"My Command"</i> to execute them.', 
        'H'
    ),
)


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
    description = "Starts VLC with the needed command line arguments."
    
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
        panel = eg.ConfigPanel(self)
        cmdLineCtrl = panel.TextCtrl(cmdLineArgs)
        resultCtrl = eg.StaticTextBox(panel)
        def OnTextChange(event=eg.wxDummyEvent):
            cmdLineArgs = cmdLineCtrl.GetValue()
            cmdString = '"%s" %s' % (vlcPath, self.GetCmdLineArgs(cmdLineArgs))
            resultCtrl.SetValue(cmdString)
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
    name = "My Command"
    description = (
        "Here you can enter your own command, ie. show a custom text message."
    )
    class text:
        label = (
            "My Command: (Type 'H' to see a list of all available commands.)"
        )
        
    def __call__(self, text):
        self.plugin.Push(eg.ParseString(text) + "\r\n")
               
            
    def Configure(self, text="marq-marquee EventGhost"):
        panel = eg.ConfigPanel(self)
        mySizer = wx.FlexGridSizer(rows=3)
        staticText = panel.StaticText(self.text.label)
        textCtrl = panel.TextCtrl(text)
        mySizer.Add(staticText, 0, wx.EXPAND|wx.ALL, 5)
        mySizer.Add(textCtrl, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(mySizer)
        while panel.Affirmed():
            panel.SetResult(textCtrl.GetValue())



class VLC(eg.PluginBase):
    
    class text:
        eventBox = "Event generation"
        showFeedbackEvents = "Show VLC feedback events"
        tcpBox = "TCP/IP Settings"
        host = "Host:"
        port = "Port:"
        
        
    def __init__(self):
        self.AddAction(Start)
        self.AddAction(MyCommand)
        self.AddActionsFromList(ACTIONS, ActionPrototype)
                             
                            
    def __start__(self, host="localhost", port=1234, showFeedbackEvents=True): 
        self.host = host
        self.port = port
        self.dispatcher = None
        self.isDispatcherRunning = False
        self.feedback = ""
        self.showFeedbackEvents = showFeedbackEvents
       
    
    def __stop__(self):
        if self.isDispatcherRunning:
            self.dispatcher.close()


    def ValueUpdate(self, text):
        state = text.decode('utf-8')
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
        panel = eg.ConfigPanel(self)
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
   
               
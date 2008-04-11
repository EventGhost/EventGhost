# ==============================================================================
# VideoLan Client TCP/IP Interface v.0.3
# Example VLC parameters:
# Path     -Skin     --RC Interface --Adress                 --NoDosBox
# vlc.exe  -I skins2 --extraintf=rc --rc-host=localhost:1234 --rc-quiet
# ==============================================================================
#
# Plugins/VLC/__init__.py
#
# Copyright (C) 2006 MonsterMagnet
#
# This file is a plugin for EventGhost.
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


eg.RegisterPlugin(
    name = "VLC media player",
    author = "MonsterMagnet",
    version = "0.3." + "$LastChangedRevision$".split()[1],
    kind = "program",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    description = (
        'Adds actions to control the '
        '<a href="http://www.videolan.org/">VLC media player</a>.'
        '\n\n</p>'
        '<p>Enable the RC Interface or start VLC with:</p>'
        '<p><b>vlc.exe --extraintf=rc --rc-host=localhost:1234 '
        '--rc-quiet --rc-show-pos</b></p>'
        '<p>If you are using "MyCommand" remember that you can only execute '
        'commands that are enabled in VLC!</p>'
        '<p><a href=http://www.eventghost.org/forum/viewtopic.php?t=43>'
        'Help and Bugreport</a></p>'
        '<p><a href="http://www.videolan.org/">VideoLAN project</a></p>'
    ),
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

import asynchat, socket

fnList = (
('Play', 'Start playing', 'pause'),
('Pause', 'Toggle play/pause', 'pause'),
('Stop', 'Stop and close current item', 'stop'),
('Fast Forward', 'Skip ~5 sec forward', 'fastforward'),
('Fast Rewind', 'Skip ~5 sec back', 'rewind'),
('Play Faster', 'Play faster', 'faster'),
('Play Slower', 'Play slower', 'slower'),
('Play Normal', 'Play normal', 'normal'),
('Fullscreen', 'Toggle fullscreen', 'f'),
('Next Playlist Item', 'Jump forward to the next item in playlist', 'next'),
('Previous Playlist Item', 'Jump backward to the previous playlist item',
    'previous'),
('Next Title', 'Next title in current item', 'title_n'),
('Previous Title', 'Previous title in current item', 'title_p'),
('Next Chapter', 'Next chapter in current item', 'chapter_n'),
('Previous Chapter', 'Previous chapter in current item', 'chapter_p'),
('Current Playlist Status', 'If VLC feedback is enabled in plugin settings, '
    'the logger shows information about the current playlist status.', 'status'),
('Stream Info', 'If VLC feedback is enabled in plugin settings, the logger '
    'shows information about the current stream.', 'info'),
('Show Playlist', 'If VLC feedback is enabled in plugin settings, the logger '
    'shows information about the current playlist.', 'playlist'),
('Clear Playlist', 'Clear the playlist and close current item', 'clear'),
('Volume Up', 'Volume up', 'volup'),
('Volume Down', 'Volume down', 'voldown'),
('Quit', 'Quit VLC', 'quit'),
('Help', 'If VLC feedback is enabled in plugin settings, the logger shows '
    'all available commands, use <i>"MyCommand"</i> to execute them.', 'H'),
)



class VLC_Session(asynchat.async_chat):
   
    def __init__ (self, handler, address):
        # Call constructor of the parent class
        asynchat.async_chat.__init__(self)

        # Set up input line terminator
        self.set_terminator('\r\n')

        # Initialize input data buffer
        self.buffer = ''
        self.handler = handler
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        eg.RestartAsyncore()
        try:
            self.connect(address)
        except:
            pass


    def handle_connect(self):
        # connection succeeded
        self.handler.TriggerEvent("Connected")
        self.sendall(self.handler.connectedevent)
         
        
    def handle_expt(self):
        # connection failed
        self.handler.dispatcher_running = False
        self.handler.TriggerEvent("NoConnection")
        self.close()


    def handle_close(self):
        # connection closed
        self.handler.dispatcher_running = False
        self.handler.TriggerEvent("ConnectionLost")
        self.close()


    def collect_incoming_data(self, data):
        # received a chunk of incoming data
        self.buffer = self.buffer + data


    def found_terminator(self):
        self.handler.ValueUpdate(self.buffer)
        self.buffer = ''
         
        
       
class VLC(eg.PluginClass):
   
    def __init__(self):
        self.host = "localhost"
        self.port = 1234
        self.dispatcher_running = False
        self.feedback = ""
       
        self.AddAction(self.MyCommand)
       
        for actionName, actionDescription, command, in fnList:
            class tmpAction(eg.ActionClass):
                name = actionName
                description = actionDescription
                value = command  + "\r\n"
                def __call__(self2):
                    return self.push(self2.value)
                
            tmpAction.__name__ = actionName.replace(" ", "")
            self.AddAction(tmpAction)
                             
                            
    def __start__(self, host="localhost", port=1234, feedback_events=True):                             
        self.host = host
        self.port = port
        self.feedback_events = feedback_events
       
    
    def __stop__(self):
        pass


    def __close__(self):
        pass
   

    def ValueUpdate(self, text):
        state = text.decode('utf-8')
        if self.feedback_events:
            self.TriggerEvent(state)


    def push(self, data):
        if not self.dispatcher_running:
            self.connectedevent = data
            self.dispatcher = VLC_Session(self, (self.host, self.port))
            self.dispatcher_running = True
        try:
            if self.dispatcher.connected:
                self.dispatcher.sendall(data)
            return True
        except:
            self.dispatcher_running = False
            self.PrintError("Error sending data to VLC.")
            self.dispatcher.close()
            return False


    def Configure(self, host="localhost", port=1234, feedback_events=True): 
        panel = eg.ConfigPanel(self)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port)
        checkBox = panel.CheckBox(feedback_events, "Show VLC feedback events")
        tcpBox = panel.BoxedGroup(
            "TCP/IP Settings",
            ("Host:", hostCtrl),
            ("Port:", portCtrl),
        )
        eg.EqualizeWidths(tcpBox.GetColumnItems(0))
        eventBox = panel.BoxedGroup(
            "Event generation",
            checkBox,
        )
        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        panel.sizer.Add(eventBox, 0, wx.TOP|wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(), 
                portCtrl.GetValue(), 
                checkBox.GetValue()
            )
   


    class MyCommand(eg.ActionClass):

        description = ("Here you can enter your own command, ie. show a " 
                       "custom text message.")

        def __call__(self, text):
            self.plugin.push(eg.ParseString(text) + "\r\n")
                   
                
        def Configure(self, text="marq-marquee EventGhost"):
            panel = eg.ConfigPanel(self)
            mySizer = wx.FlexGridSizer(rows=3)

            staticText = panel.StaticText(
                "My Command: (Type 'H' to see a list of all available "
                "commands.)"
            )
            textEdit = panel.TextCtrl(text)
            mySizer.Add(staticText, 0, wx.EXPAND|wx.ALL, 5)
            mySizer.Add(textEdit, 0, wx.EXPAND|wx.ALL, 5)

            panel.sizer.Add(mySizer)
           
            while panel.Affirmed():
                panel.SetResult(textEdit.GetValue())
            
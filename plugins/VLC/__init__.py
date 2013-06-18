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

import asynchat, socket
import wx
import wx.lib.intctrl as IntCtrl
import eg

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

        try:
            self.connect(address)
        except:
            pass


    def handle_connect(self):
        # connection succeeded
        self.handler.TriggerEvent("Connected")
         
        
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
    canMultiLoad = True
   
    def __init__(self):
        self.host = "localhost"
        self.port = 1234
        self.dispatcher_running = False
        self.feedback = ""
       
        self.AddAction(self.MyCommand)
       
        for action_name, text, command, in fnList:
            class tmpAction(eg.ActionClass):
                name = action_name
                description = text
                value = command  + "\r\n"
                def __call__(self2):
                    return self.push(self2.value)
                
            tmpAction.__name__ = action_name.replace(" ", "")
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
            self.dispatcher = VLC_Session(self, (self.host, self.port))
            self.dispatcher_running = True
        try:
            self.dispatcher.sendall(data)
            return True
        except:
            self.dispatcher_running = False
            self.PrintError("Couldn't connect to VLC.")
            self.dispatcher.close()
            return False


    def Configure(self, host="localhost", port=1234, feedback_events=True): 
        dialog = eg.ConfigurationDialog(self)
        sizer = dialog.sizer
        mySizer = wx.FlexGridSizer(cols=2)

        staticText = wx.StaticText(dialog, -1, "TCP Control Host:")
        mySizer.Add(staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
       
        hostEdit = wx.TextCtrl(dialog, -1, host)
        mySizer.Add(hostEdit, 0, wx.EXPAND|wx.ALL, 5)
       
        staticText = wx.StaticText(dialog, -1, "TCP Control Port:")
        mySizer.Add(staticText, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
       
        portEdit = IntCtrl.IntCtrl(dialog, -1, port)
        mySizer.Add(portEdit, 0, wx.EXPAND|wx.ALL, 5)
       
        sizer.Add(mySizer, 1, wx.EXPAND|wx.ALIGN_CENTER)
       
        cb1 = wx.CheckBox(dialog, -1, "Show VLC feedback events")
        cb1.SetValue(feedback_events)
        sizer.Add(cb1, 0, wx.ALL, 5)       
       
        if dialog.AffirmedShowModal():
            return hostEdit.GetValue(), portEdit.GetValue(), cb1.GetValue()
   


    class MyCommand(eg.ActionClass):

        description = ("Here you can enter your own command, ie. show a " 
                       "custom text message.")

        def __call__(self, text):
            self.plugin.push(eg.ParseString(text) + "\r\n")
                   
                
        def Configure(self, text="marq-marquee EventGhost"):
            dialog = eg.ConfigurationDialog(self)
            mySizer = wx.FlexGridSizer(rows=3)

            staticText = wx.StaticText(dialog, -1, "My Command: (Type 'H' to "
                                       "see a list of all available commands.)")
            mySizer.Add(staticText, 0, wx.EXPAND|wx.ALL, 5)
       
            textEdit = wx.TextCtrl(dialog, -1, text)
            mySizer.Add(textEdit, 0, wx.EXPAND|wx.ALL, 5)

            button = wx.Button(dialog, -1, label="Test")
            def OnButton(event):
                self(textEdit.GetValue())
            button.Bind(wx.EVT_BUTTON, OnButton)
            mySizer.Add(button, 0, wx.EXPAND|wx.ALL, 5)
           
            dialog.sizer.Add(mySizer)
           
            if dialog.AffirmedShowModal():
                return textEdit.GetValue(),
            
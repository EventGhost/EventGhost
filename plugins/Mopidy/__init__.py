# -*- coding: utf-8 -*-
#
# Copyright (c) 2014, Walter Kraembring
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of Walter Kraembring nor the names of its contributors may
#    be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


##############################################################################
# Revision history:
#
# 2015-03-06  Improved reconnection with Mopidy.
# 2014-11-05  First version, thanks to Stein Magnus Jodal for Mopidy.
#             https://www.mopidy.com
##############################################################################
##############################################################################
#
# Acknowledgements:
#
# Mopidy is copyright 2009-2014 Stein Magnus Jodal and contributors. Mopidy is
# licensed under the Apache License, Version 2.0.
#
# websocket - WebSocket client library for Python
# Copyright (C) 2010 Hiroki Ohtani(liris)
#
# Utilities (Six) for writing code that runs on Python 2 and 3"""
# Copyright (c) 2010-2014 Benjamin Peterson
##############################################################################

eg.RegisterPlugin(
    name = "Mopidy",
    guid = '{458E04C4-DFE8-4F7C-ABB0-97B0EAD50204}',
    author = "Walter Kraembring",
    version = "0.0.2",
    kind = "program",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6360#p32889",
    description = (
        '<p>Plugin to integrate with '
        '<a href="https://www.mopidy.com">'
        'Mopidy</a></p>'
        '\n\n<p>'
        '<center><img src="mopidy.png" /></center>'
    ),
)
import eg
import wx
import requests
import json
from os.path import abspath, split
from sys import path as syspath
mod_pth = abspath(split(__file__)[0])
syspath.append(mod_pth + "\\")
import websocket
from threading import Event, Thread
from time import sleep


 
class Mopidy(eg.PluginClass):

    class text:
        infoRetrieve = "Retrieving Mopidy playlists...please wait"
        errorRetrieve = "Could not retrieve Mopidy playlists"
        infoPlugin = "Mopidy plugin stopped" 
        infoNoDevice = "Could not connect with Mopidy"
        infoThread = "Mopidy monitor thread has stopped"
        mp_name = "Mopidy name: "
        hostname = "Mopidy IP-address or host name: "
        portNbr = "Select the port number to use (default 6680): "
        clientId = "Mopidy Client ID: "
    

    def __init__(self):
        self.bFound = None
        self.iDelay = 0.5
        self.AddAction(PlayPlayList)
        self.AddAction(AddPlayList)
        self.AddAction(ClearTrackList)
        self.AddAction(Play)
        self.AddAction(Stop)
        self.AddAction(PlayPause)
        self.AddAction(NextTrack)
        self.AddAction(PreviousTrack)
        self.AddAction(VolumeUp)
        self.AddAction(VolumeDown)
        self.AddAction(VolumeInit)
        self.AddAction(MuteUnmute)
        self.AddAction(Mute)
        self.AddAction(UnMute)
        self.AddAction(RandomOn)
        self.AddAction(RandomOff)
        self.AddAction(RepeatOn)
        self.AddAction(RepeatOff)

            
    def __start__(
            self,
            mp_name = "My Mopidy",
            clientId = 1,
            hostname = "127.0.0.1",
            portNbr = 6680
        ):
        self.resOld = u''
        self.mp_name = mp_name
        self.hostname = hostname
        self.portNbr = portNbr
        self.clientId = clientId
        self.playLists = {}
        self.playListNames = []
        self.getPlaylists()

        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.ThreadWorker,
            args=(self.stopThreadEvent,)
        )
        thread.start()


    def __stop__(self):
        if self.stopThreadEvent:
            self.stopThreadEvent.set()
        print self.text.infoPlugin


    def __close__(self):
        print self.text.infoPlugin


    def restart(self):
        if self.stopThreadEvent:
            self.stopThreadEvent.set()
        sleep(30.0)
        self.__start__(
            self.mp_name,
            self.clientId,
            self.hostname,
            self.portNbr
        )


    def ThreadWorker(self, stopThreadEvent):
        wsURL = (
            "ws://"+
            self.hostname+
            ":"+
            str(self.portNbr)+
            "/mopidy/ws"
        )
        try:
            ws = websocket.create_connection(wsURL)
            while not stopThreadEvent.isSet():
                response = ws.recv()
                if 'tl_track' in json.loads(response):
                    res = json.loads(response)['tl_track']['track']
                    pl = (
                            res['album']['artists'][0]['name']+
                            ' - '+
                            res['name']
                    )
                    if pl != self.resOld:
                        eg.TriggerEvent(
                            'CurrentArtistTrack',
                            payload = pl,
                            prefix='Mopidy'
                        )
                        self.resOld = pl
                stopThreadEvent.wait(self.iDelay)
            ws.shutdown()
            print self.text.infoThread
        except:
            eg.PrintError(self.text.infoNoDevice)
            self.restart()
            

    def sendMessage(self, method, uri, params):
        try:
            url = (
                'http://'+
                str(self.hostname)+
                ':'+
                str(self.portNbr)+
                '/mopidy/rpc'
            )
            headers = {'content-type': 'application/json'}
            if uri=='':
                payload = {
                    "method": str(method),
                    "jsonrpc": "2.0",
                    "id": self.clientId,
                }
            else:
                payload = {
                    "method": str(method),
                    "jsonrpc": "2.0",
                    "params":{uri:params},
                    "id": self.clientId,
                }
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers
            ).json()
            self.bFound = True
            return response
        except:        
            self.bFound = False
            return None
            eg.PrintError(self.text.infoNoDevice)


    def getPlaylists(self):
        try:
            print self.text.infoRetrieve
            r = []
            while r == []:
                response = self.sendMessage(
                    "core.playlists.get_playlists",
                    "",
                    ""
                )
                r = response['result']
                sleep(1.0)
            for item in r:
                name = item['name']
                self.playLists[name] = item['uri']
                self.playListNames.append(name)
        except:
            eg.PrintError(self.text.errorRetrieve)
        

    def setTrackListRepeat(self):
        response = self.sendMessage(
            "core.tracklist.set_repeat",
            "value",
            True
        )


    def unsetTrackListRepeat(self):
        response = self.sendMessage(
            "core.tracklist.set_repeat",
            "value",
            False
        )


    def setTrackListRandom(self):
        response = self.sendMessage(
            "core.tracklist.set_random",
            "value",
            True
        )


    def unsetTrackListRandom(self):
        response = self.sendMessage(
            "core.tracklist.set_random",
            "value",
            False
        )


    def clearTrackList(self):
        response = self.sendMessage(
            "core.tracklist.clear",
            "",
            ""
        )


    def startPlay(self):
        response = self.sendMessage(
            "core.playback.play",
            "",
            ""
        )
        
    
    def stopPlay(self):
        response = self.sendMessage(
            "core.playback.stop",
            "",
            ""
        )
        

    def pausePlay(self):
        res = self.getState()
        if res == 'playing':
            response = self.sendMessage(
                "core.playback.pause",
                "",
                ""
            )
        else:
            response = self.sendMessage(
                "core.playback.resume",
                "",
                ""
            )
            

    def getState(self):
        response = self.sendMessage(
            "core.playback.get_state",
            "",
            ""
        )
        return response['result']

        
    def getMuteState(self):
        response = self.sendMessage(
            "core.playback.get_mute",
            "",
            ""
        )
        return response['result']


    def muteVolume(self):
        response = self.sendMessage(
            "core.playback.set_mute",
            "value",
            True
        )


    def unmuteVolume(self):
        response = self.sendMessage(
            "core.playback.set_mute",
            "value",
            False
        )


    def volumeUp(self):
        current = self.sendMessage(
            "core.playback.get_volume",
            "",
            ""
        )
        current = int(current['result'])+5
        response = self.sendMessage(
            "core.playback.set_volume",
            "volume",
            current
        )


    def volumeDown(self):
        current = self.sendMessage(
            "core.playback.get_volume",
            "",
            ""
        )
        current = int(current['result'])-5
        response = self.sendMessage(
            "core.playback.set_volume",
            "volume",
            current
        )


    def volumeInit(self, level):
        response = self.sendMessage(
            "core.playback.set_volume",
            "volume",
            level
        )


    def nextTrack(self):
        try:
            response = self.sendMessage(
                "core.playback.next",
                "",
                ""
            )
        except:
            pass
        self.startPlay()


    def previousTrack(self):
        try:
            response = self.sendMessage(
                "core.playback.previous",
                "",
                ""
            )
        except:
            pass
        self.startPlay()
            

    def Configure(
        self,
        mp_name = "My Mopidy",
        clientId = 1,
        hostname = "127.0.0.1",
        portNbr = 6680
     ):
        panel = eg.ConfigPanel(self, resizable=True)
        mySizer = wx.GridBagSizer(5, 5)

        mp_nameCtrl = wx.TextCtrl(panel, -1, mp_name)
        mp_nameCtrl.SetInitialSize((250,-1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.mp_name), (1,0))
        mySizer.Add(mp_nameCtrl, (1,1))

        clientIdCtrl = panel.SpinIntCtrl(clientId, 1, 9999)
        clientIdCtrl.SetInitialSize((75,-1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.clientId), (2,0))
        mySizer.Add(clientIdCtrl, (2,1))
        
        hostnameCtrl = wx.TextCtrl(panel, -1, hostname)
        hostnameCtrl.SetInitialSize((250,-1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.hostname), (3,0))
        mySizer.Add(hostnameCtrl, (3,1))

        portCtrl = panel.SpinIntCtrl(portNbr, 1, 9999)
        portCtrl.SetInitialSize((75,-1))
        mySizer.Add(wx.StaticText(panel, -1, self.text.portNbr), (4,0))
        mySizer.Add(portCtrl, (4,1))

        panel.sizer.Add(mySizer, 1, flag = wx.EXPAND)

        while panel.Affirmed():
            mp_name = mp_nameCtrl.GetValue()
            hostname = hostnameCtrl.GetValue()
            portNbr = portCtrl.GetValue()
            clientId = clientIdCtrl.GetValue()
            
            panel.SetResult(
                        mp_name,
                        clientId,
                        hostname,
                        portNbr
            )



class PlayPlayList(eg.ActionClass):
    name = "Select and play a playlist"
    description = "Select and play from your playlists"
    
    class PlayPlayList:
        txt_pl = "Select the playlist to play"
    
    def __call__(self, item=""):
        self.plugin.clearTrackList()
        params = self.plugin.playLists[item]
        self.plugin.sendMessage(
            "core.tracklist.add",
            "uri",
            params
        )
        self.plugin.startPlay()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        item = ""
    ):
        panel = eg.ConfigPanel(self)
        musicCtrl = wx.ComboBox(parent=panel, pos=(10,10)) 
        ilist = self.plugin.playListNames
        musicCtrl.AppendItems(items=ilist)
        if ilist.count(item)==0:
            musicCtrl.Select(n=0)
        else:
            musicCtrl.SetSelection(int(ilist.index(item)))
        musicCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.PlayPlayList.txt_pl)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(musicCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            item = musicCtrl.GetValue()
            panel.SetResult(
                        item
            )



class AddPlayList(eg.ActionClass):
    name = "Add a playlist to the track list"
    description = "Select and add a playlist to the track list"
    
    class AddPlayList:
        txt_pl = "Select playlist to add"

    def __call__(self, item=""):
        params = self.plugin.playLists[item]
        self.plugin.sendMessage(
            "core.tracklist.add",
            "uri",
            params
        )
        self.plugin.startPlay()


    # Get the choice from dropdown and perform some action
    def OnChoice(self, event):
        choice = event.GetSelection()
        event.Skip()
        return choice


    def Configure(
        self,
        item = ""
    ):
        panel = eg.ConfigPanel(self)
        musicCtrl = wx.ComboBox(parent=panel, pos=(10,10)) 
        ilist = self.plugin.playListNames
        musicCtrl.AppendItems(items=ilist)
        if ilist.count(item)==0:
            musicCtrl.Select(n=0)
        else:
            musicCtrl.SetSelection(int(ilist.index(item)))
        musicCtrl.Bind(wx.EVT_CHOICE, self.OnChoice)
        staticBox = wx.StaticBox(panel, -1, self.AddPlayList.txt_pl)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(musicCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            item = musicCtrl.GetValue()
            panel.SetResult(
                        item
            )


            
class Play(eg.ActionClass):
    name = "Play"
    description = "Starts playing"
    
    def __call__(self):
        self.plugin.startPlay()



class ClearTrackList(eg.ActionClass):
    name = "Clear Track List"
    description = "Clear the track list"
    
    def __call__(self):
        self.plugin.clearTrackList()



class Stop(eg.ActionClass):
    name = "Stop"
    description = "Stops playing"
    
    def __call__(self):
        self.plugin.stopPlay()



class PlayPause(eg.ActionClass):
    name = "PlayPause"
    description = "Toggles play/pause"
    
    def __call__(self):
        self.plugin.pausePlay()



class MuteUnmute(eg.ActionClass):
    name = "Toggles Mute/Unmute"
    description = "Toggles Mute/Unmute volume"
    
    def __call__(self):
        res = self.plugin.getMuteState()
        if res:
            self.plugin.unmuteVolume()
        else:
            self.plugin.muteVolume()


class Mute(eg.ActionClass):
    name = "Mute"
    description = "Mutes volume"
    
    def __call__(self):
        self.plugin.muteVolume()



class UnMute(eg.ActionClass):
    name = "UnMute"
    description = "Unmutes volume"
    
    def __call__(self):
        self.plugin.unmuteVolume()



class VolumeDown(eg.ActionClass):
    name = "VolumeDown"
    description = "Lowers volume"
    
    def __call__(self):
        self.plugin.volumeDown()



class VolumeUp(eg.ActionClass):
    name = "VolumeUp"
    description = "Raises volume"
    
    def __call__(self):
        self.plugin.volumeUp()



class VolumeInit(eg.ActionClass):
    name = "VolumeInit"
    description = "Initiates volume to defined level"
    
    class VolumeInit:
        txt_amount = "Select the initial volume to be set"

    def __call__(self, myAmount=65):
        self.plugin.volumeInit(myAmount)


    def Configure(
        self,
        myAmount = 65
    ):
        panel = eg.ConfigPanel(self)
        myAmountCtrl = panel.SpinIntCtrl(myAmount, 0, 100)
        myAmountCtrl.SetInitialSize((50,-1))
        staticBox = wx.StaticBox(panel, -1, self.VolumeInit.txt_amount)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer1.Add(myAmountCtrl, 1, wx.EXPAND)
        staticBoxSizer.Add(sizer1, 0, wx.EXPAND|wx.ALL, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND)

        while panel.Affirmed():
            myAmount = myAmountCtrl.GetValue()
            panel.SetResult(
                        myAmount
            )



class PreviousTrack(eg.ActionClass):
    name = "Previous Track"
    description = "Starts playing Previous Track"
    
    def __call__(self):
        self.plugin.previousTrack()



class NextTrack(eg.ActionClass):
    name = "Next Track"
    description = "Starts playing Next Track"
    
    def __call__(self):
        self.plugin.nextTrack()



class RepeatOn(eg.ActionClass):
    name = "Repeat ON"
    description = "Repeats on"
    
    def __call__(self):
        self.plugin.setTrackListRepeat()



class RepeatOff(eg.ActionClass):
    name = "Repeat OFF"
    description = "Repeats off"
    
    def __call__(self):
        self.plugin.unsetTrackListRepeat()



class RandomOn(eg.ActionClass):
    name = "Random ON"
    description = "Random on"
    
    def __call__(self):
        self.plugin.setTrackListRandom()



class RandomOff(eg.ActionClass):
    name = "Random OFF"
    description = "Random off"
    
    def __call__(self):
        self.plugin.unsetTrackListRandom()

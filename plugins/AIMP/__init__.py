# -*- coding: utf-8 -*-
#
# plugins/AIMP/__init__.py
#
# This file is a plugin for EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
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
#
# Changelog (in reverse chronological order):
# -------------------------------------------
# 0.0.2  by Pako 2013-01-21 19:40 UTC+1
#      - bugfix (error in logger, when AIMP is not running)
#      - support link (EG forum) added
# 0.0.1  by Pako 2012-11-11 09:22 UTC+1
#      - initial version 
#===============================================================================

import eg
import wx
from httplib import HTTPConnection
from urllib import quote
from json import loads
from os.path import split

eg.RegisterPlugin(
    name="AIMP",
    description=ur'''<rst>
Adds actions to control AIMP__.

| 
| **ATTENTION:**
| For proper function of this EventGhost plugin it is required the 
| `Web Control Plugin`__ (aimp_web_ctl.dll) from Vitaly Dyatlov 
| to be installed to AIMP__ !

__ http://aimp.ru/index.php
__ http://aimp.ru/index.php?do=catalog&rec_id=265
__ http://aimp.ru/index.php
''',
    kind="program",
    author="Pako",
    guid = "{E3E85C61-03D7-4E8F-8A98-45B2234D9490}",
    version="0.0.2",
    createMacrosOnAdd=True,
    canMultiLoad = True,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=4090",
    icon = (
        "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"
    ),    
)

STATUSES={
"Volume": 1, 
"Balance": 2, 
"Speed": 3, 
"Player": 4, 
"Mute": 5, 
"Reverberation": 6, 
"Echo": 7, 
"Chorus": 8, 
"Flanger": 9, 
"Equalizer (On/Off)":  10, 
"Equalizer slider 01": 11, 
"Equalizer slider 02": 12, 
"Equalizer slider 03": 13, 
"Equalizer slider 04": 14, 
"Equalizer slider 05": 15, 
"Equalizer slider 06": 16, 
"Equalizer slider 07": 17, 
"Equalizer slider 08": 18, 
"Equalizer slider 09": 19, 
"Equalizer slider 10": 20, 
"Equalizer slider 11": 21, 
"Equalizer slider 12": 22, 
"Equalizer slider 13": 23, 
"Equalizer slider 14": 24, 
"Equalizer slider 15": 25, 
"Equalizer slider 16": 26, 
"Equalizer slider 17": 27, 
"Equalizer slider 18": 28, 
"Repeat song": 29, 
"On stop": 30, 
"Position": 31, 
"Length": 32, 
"Repeat playlist": 33, 
"Repeat playlist 1 (other algorithm to repeat)": 34, 
"Kilobits per second for current song": 35, 
"KiloHerz": 36, 
"Mode": 37, 
"Radio": 38, 
"Stream type: Music / CDA / Radio": 39, 
"Timer: Reverse / Normal": 40, 
"Shuffle": 41, 
#"Main HWND": 42, 
#"TC HWND": 43, 
#"App HWND": 44, 
#"PL HWND": 45, 
#"EQ HWND": 46,
} 
#===============================================================================

class Text:
    host = "AIMP server TCP/IP Address:"
    rport = "AIMP server TCP/IP Port:"
    eventPrefix = "Event prefix:"
    eventsLabel = "Trigger an event when:"
    polling = "Polling interval (s):"
    tcpBox = "TCP/IP Settings"
    eventGenerationBox = "Events triggering"
    events = (
        "Playing song changed",
        "Playing playlist changed",
        "Player status changed",
        "Repeat mode changed",
        "Random mode changed",
        "Volume level changed",
        "Mute status changed",
    )
    status = ("Stopped", "Playing", "Paused")
#===============================================================================

class AIMP(eg.PluginBase):

    text = Text
    con = None
    sched = None
    oldStat = 7 * [None]

    def __init__(self):
        self.AddActionsFromList(ACTIONS)


    def GetConnection(self):
        host = "127.0.0.1" if self.host == "localhost" else self.host
        def test(con):
            con.request("GET", "/?action=get_volume")
            res = con.getresponse()
            if res.status == 200:
                res.read()
        if self.con:
            try:
                test(self.con)
            except:
                self.con = None
        if not self.con:
            try:
                self.con = HTTPConnection("%s:%i" % (host, self.port))
                test(self.con)
            except:
                self.con = None
        return self.con is not None


    def GetCustomStatus(self, stat):
        if self.GetConnection():
            try:
                stat = str(STATUSES[stat])
                req = "/?action=get_custom_status&status=%s" % stat
                self.con.request("GET", req)
                res = self.con.getresponse()
                if res.status == 200:
                    return res.read()
            except:
                raise


    def MakeRequest(self, name, tp):
        if self.GetConnection():
            try:
                self.con.request("GET", "/?action=%s" % name)
                res = self.con.getresponse()
                if res.status == 200:
                    if tp == "json":
                        return loads(res.read())
                    elif tp:
                        return res.read()
                    else:
                        return True
            except:
                raise  


    def GetId(self, name):
        for pl in self.MakeRequest("get_playlist_list", "json"):
            if pl["name"] == name:
                return pl["id"]


    def GetName(self, id):
        for pl in self.MakeRequest("get_playlist_list", "json"):
            if pl["id"] == int(id):
                return pl["name"]


    def __start__(
        self,
        host="localhost",
        rport=38475,
        prefix = "AIMP",
        poll = 2,
        events = 7 * [False]
    ):
        self.host = host
        self.port = rport
        self.prefix = prefix
        self.poll = poll
        self.events = events
        self.GetConnection()
        flg = 0
        for evt in events:
            flg += int(evt)
        if flg:
            eg.scheduler.AddTask(1, self.Polling)

    def Cap(self, str):
        return str.title().replace(" ","")


    def Polling(self):
        self.sched = eg.scheduler.AddTask(self.poll, self.Polling)
        if not self.GetConnection():
            return
        text = self.text
        keys = ("Player", "Repeat song", "Shuffle", "Volume", "Mute")        
        for i in range(len(self.events)):
            if i==0:
                if self.events[0]:
                    song = self.MakeRequest("get_song_current", "json")
                    if song:
                        val = song[u'PlayingFileName']
                        if val != self.oldStat[0]:
                            self.oldStat[0] = val
                            eg.TriggerEvent(
                                self.Cap(text.events[0]),
                                prefix = self.prefix,
                                payload = val
                            )
            elif i==1:
                if self.events[1]:
                    if not self.events[0]:
                        song = self.MakeRequest("get_song_current", "json")
                    if song:
                        val = song[u'PlayingList']
                        if val != self.oldStat[1]:
                            self.oldStat[1] = val
                            eg.TriggerEvent(
                                self.Cap(text.events[1]),
                                prefix = self.prefix,
                                payload = self.GetName(val)
                            )
            elif i==2:
                if self.events[2]:
                    val = int(self.GetCustomStatus(keys[i-2]))
                    if val is not None and val != self.oldStat[i]:
                        self.oldStat[i] = val
                        eg.TriggerEvent(
                            "%s.%s" % (self.Cap(text.events[i]),text.status[val]),
                            prefix = self.prefix
                        )
            elif self.events[i]:
                val = int(self.GetCustomStatus(keys[i-2]))
                if val is not None and val != self.oldStat[i]:
                    self.oldStat[i] = val
                    eg.TriggerEvent(
                        self.Cap(text.events[i]),
                        prefix = self.prefix,
                        payload = val
                    )


    def Configure(
        self,
        host ="localhost",
        rport=38475,
        prefix="AIMP",
        poll = 2,
        events = 7 * [False],
    ):
        text = self.text
        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        prefix = self.name if not prefix else prefix
        hostCtrl = wx.TextCtrl(panel,-1, host)
        rportCtrl = eg.SpinIntCtrl(panel, -1, rport, max=65535)
        pollCtrl = eg.SpinIntCtrl(panel, -1, poll, min=1, max=99)
        eventPrefixCtrl = wx.TextCtrl(panel,-1, prefix)
        st1 = wx.StaticText(panel,-1, text.host)
        st2 = wx.StaticText(panel,-1, text.rport)
        st3 = wx.StaticText(panel,-1, text.polling)
        st4 = wx.StaticText(panel,-1, text.eventsLabel)
        st5 = wx.StaticText(panel,-1, text.eventPrefix)
        eg.EqualizeWidths((st1, st2))
        eventsCtrl = wx.CheckListBox(
            panel,
            -1,
            choices = text.events,
            size = ((-1, len(events) * (3+st4.GetSize()[1]))),
        )        
        for i in range(len(events)):
            eventsCtrl.Check(i, events[i])
        box1 = panel.BoxedGroup(
            text.tcpBox,
            (st1, hostCtrl),
            (st2, rportCtrl),
        )
        box2 = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.eventGenerationBox),
            wx.HORIZONTAL
        )
        leftSizer=wx.FlexGridSizer(2, 2, 10, 5)
        leftSizer.Add(st5,0,wx.TOP,3)
        leftSizer.Add(eventPrefixCtrl)
        leftSizer.Add(st3,0,wx.TOP,3)
        leftSizer.Add(pollCtrl)
        rightSizer=wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(st4)
        rightSizer.Add(eventsCtrl,0,wx.EXPAND)
        box2.Add(leftSizer,0,wx.TOP,4)
        box2.Add(rightSizer,1,wx.EXPAND|wx.LEFT,10)
        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND|wx.TOP, 10),
        ])
        while panel.Affirmed():
            tmpList = []
            for i in range(len(events)):
                tmpList.append(eventsCtrl.IsChecked(i)) 
            panel.SetResult(
                hostCtrl.GetValue(),
                rportCtrl.GetValue(),  
                eventPrefixCtrl.GetValue(),
                pollCtrl.GetValue(),
                tmpList
            )


    def __stop__(self):
        if self.con:
            self.con.close()
        self.con = None
        if self.sched:
            try:
                eg.scheduler.CancelTask(self.sched)
            except:
                pass
            self.sched = None
        self.oldStat = 7 * [None]
#===============================================================================

class simple_action(eg.ActionBase):

    def __call__(self):
        return self.plugin.MakeRequest(self.__class__.__name__, self.value)
#===============================================================================

class get_playlist_songs(eg.ActionBase):

    class text:
        nameLabel = "Playlist name:"
        offsetLabel = "Offset:"
        sizeLabel = "Size:"
        sizeLabel2 = "(0 = all songs)"


    def __call__(self, name="", offs = 0, size = 0):
        id = self.plugin.GetId(eg.ParseString(name))
        offs = str(offs) if isinstance(offs,int) else eg.ParseString(offs)
        size = str(size) if isinstance(size,int) else eg.ParseString(size)
        if self.plugin.GetConnection():
            try:
                req = "/?action=get_playlist_songs&id=%s" % id
                if offs!="0":
                    req+="&offset=%s" % offs
                if size!="0":
                    req+="&size=%s" % size
                self.plugin.con.request("GET", req)
                res = self.plugin.con.getresponse()
                if res.status == 200:
                    return loads(res.read())
            except:
                raise


    def Configure(self, name="", offset = 0, size = 0):
        panel = eg.ConfigPanel(self)
        nameLabel = wx.StaticText(panel, -1, self.text.nameLabel)
        offsetLabel = wx.StaticText(panel, -1, self.text.offsetLabel)
        sizeLabel = wx.StaticText(panel, -1, self.text.sizeLabel)
        sizeLabel2 = wx.StaticText(panel, -1, self.text.sizeLabel2)
        nameCtrl = wx.TextCtrl(panel, -1, name)
        offsetCtrl = eg.SmartSpinIntCtrl(panel, -1, offset, min=0)
        sizeCtrl = eg.SmartSpinIntCtrl(panel, -1, size, min=0)
        mainSizer = wx.FlexGridSizer(3, 3, 10, 5)
        mainSizer.Add(nameLabel,0,wx.TOP,3)
        mainSizer.Add(nameCtrl,1,wx.EXPAND)
        mainSizer.Add((-1, -1))
        mainSizer.Add(offsetLabel,0,wx.TOP,3)
        mainSizer.Add(offsetCtrl,1,wx.EXPAND)
        mainSizer.Add((-1, -1))
        mainSizer.Add(sizeLabel,0,wx.TOP,3)
        mainSizer.Add(sizeCtrl,1,wx.EXPAND)
        mainSizer.Add(sizeLabel2,0,wx.TOP,3)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)
        
        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
                offsetCtrl.GetValue(),
                sizeCtrl.GetValue(),
            )  
#===============================================================================

class get_playlist_crc(eg.ActionBase):

    class text:
        nameLabel = "Playlist name:"


    def __call__(self, name=""):
        id = self.plugin.GetId(eg.ParseString(name))
        if self.plugin.GetConnection():
            try:
                req = "/?action=get_playlist_crc&id=%s" % id
                self.plugin.con.request("GET", req)
                res = self.plugin.con.getresponse()
                if res.status == 200:
                    return res.read()
            except:
                raise


    def Configure(self, name=""):
        panel = eg.ConfigPanel(self)
        nameLabel = wx.StaticText(panel, -1, self.text.nameLabel)
        nameCtrl = wx.TextCtrl(panel, -1, name)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(nameLabel,0,wx.TOP,3)
        mainSizer.Add(nameCtrl,0,wx.LEFT,5)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)
        
        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
            ) 
#===============================================================================

class set_volume(eg.ActionBase):

    class text:
        label = "Volume (in %):"


    def __call__(self, vol=0):
        vol = str(vol) if isinstance(vol,int) else eg.ParseString(vol)
        if self.plugin.GetConnection():
            try:
                req = "/?action=set_volume&volume=%s" % vol
                self.plugin.con.request("GET", req)
                res = self.plugin.con.getresponse()
                if res.status == 200:
                    return True
            except:
                raise


    def Configure(self, vol=0):
        panel = eg.ConfigPanel(self)
        label = wx.StaticText(panel, -1, self.text.label)
        volCtrl = eg.SmartSpinIntCtrl(panel, -1, vol, min=0,max=100)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(label,0,wx.TOP,3)
        mainSizer.Add(volCtrl,0,wx.LEFT,5)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)
        
        while panel.Affirmed():
            panel.SetResult(
                volCtrl.GetValue(),
            ) 
#===============================================================================

class set_track_position(eg.ActionBase):

    class text:
        label = "Track position (in seconds):"

    def __call__(self, pos=0):
        pos = str(pos) if isinstance(pos,int) else eg.ParseString(pos)
        if self.plugin.GetConnection():
            try:
                req = "/?action=set_track_position&position=%s" % pos
                self.plugin.con.request("GET", req)
                res = self.plugin.con.getresponse()
                if res.status == 200:
                    return True
            except:
                raise


    def Configure(self, pos=0):
        panel = eg.ConfigPanel(self)
        label = wx.StaticText(panel, -1, self.text.label)
        posCtrl = eg.SmartSpinIntCtrl(panel, -1, pos, min=0)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(label,0,wx.TOP,3)
        mainSizer.Add(posCtrl,0,wx.LEFT,5)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)
        
        while panel.Affirmed():
            panel.SetResult(
                posCtrl.GetValue(),
            ) 
#===============================================================================

class set_song_position(eg.ActionBase):

    class text:
        nameLabel = "Playlist name:"
        oldLabel = "Old song position:"
        newLabel = "New song position:"


    def __call__(self, name="", old = 1, new = 1):
        id = self.plugin.GetId(eg.ParseString(name))
        old = old if isinstance(old,int) else int(eg.ParseString(old))
        old = str(old - 1)
        new = new if isinstance(new, int) else int(eg.ParseString(new))
        new = str(new - 1)
        if self.plugin.GetConnection():
            try:
                req = "/?action=set_song_position&playlist=%s" % id
                req+="&song=%s" % old
                req+="&position=%s" % new
                self.plugin.con.request("GET", req)
                res = self.plugin.con.getresponse()
                if res.status == 200:
                    return True
            except:
                raise


    def Configure(self, name="", old = 1, new = 1):
        panel = eg.ConfigPanel(self)
        nameLabel = wx.StaticText(panel, -1, self.text.nameLabel)
        oldLabel = wx.StaticText(panel, -1, self.text.oldLabel)
        newLabel = wx.StaticText(panel, -1, self.text.newLabel)
        nameCtrl = wx.TextCtrl(panel, -1, name)
        oldCtrl = eg.SmartSpinIntCtrl(panel, -1, old, min=1)
        newCtrl = eg.SmartSpinIntCtrl(panel, -1, new, min=1)
        mainSizer = wx.FlexGridSizer(3, 2, 10, 5)
        mainSizer.Add(nameLabel,0,wx.TOP,3)
        mainSizer.Add(nameCtrl,1,wx.EXPAND)
        mainSizer.Add(oldLabel,0,wx.TOP,3)
        mainSizer.Add(oldCtrl,1,wx.EXPAND)
        mainSizer.Add(newLabel,0,wx.TOP,3)
        mainSizer.Add(newCtrl,1,wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)
        
        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
                oldCtrl.GetValue(),
                newCtrl.GetValue(),
            )  
#===============================================================================

class song_action(eg.ActionBase):

    class text:
        nameLabel = "Playlist name:"
        posLabel = "Song position:"


    def __call__(self, name="", pos = 1):
        self.plugin.GetId("Chuck")
        id = self.plugin.GetId(eg.ParseString(name))
        pos = pos if isinstance(pos, int) else int(eg.ParseString(pos))
        pos = str(pos - 1)
        if self.plugin.GetConnection():
            try:
                req = "/?action=%s&playlist=%s" % (self.__class__.__name__, id)
                req+="&%s=%s" % (self.value, pos)
                self.plugin.con.request("GET", req)
                res = self.plugin.con.getresponse()
                if res.status == 200:
                    return True
            except:
                raise


    def GetLabel(self, name, pos):
        return "%s: %i" % (self.name, pos)


    def Configure(self, name="", pos = 1):
        panel = eg.ConfigPanel(self)
        nameLabel = wx.StaticText(panel, -1, self.text.nameLabel)
        posLabel = wx.StaticText(panel, -1, self.text.posLabel)
        nameCtrl = wx.TextCtrl(panel, -1, name)
        posCtrl = eg.SmartSpinIntCtrl(panel, -1, pos, min=1)
        mainSizer = wx.FlexGridSizer(2, 2, 10, 5)
        mainSizer.Add(nameLabel,0,wx.TOP,3)
        mainSizer.Add(nameCtrl,1,wx.EXPAND)
        mainSizer.Add(posLabel,0,wx.TOP,3)
        mainSizer.Add(posCtrl,1,wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)
        
        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
                posCtrl.GetValue(),
            )  
#===============================================================================

class get_custom_status(eg.ActionBase):

    class text:
        label = "Custom status:"


    def __call__(self, stat=""):
        return self.plugin.GetCustomStatus(stat)



    def Configure(self, stat=""):
        panel = eg.ConfigPanel(self)
        label = wx.StaticText(panel, -1, self.text.label)
        choices = list(STATUSES.iterkeys())
        choices.sort()
        statCtrl = wx.Choice(panel, -1, choices=choices)
        statCtrl.SetStringSelection(stat)
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSizer.Add(label,0,wx.TOP,3)
        mainSizer.Add(statCtrl,0,wx.LEFT,5)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)
        
        while panel.Affirmed():
            panel.SetResult(
                statCtrl.GetStringSelection(),
            ) 
#===============================================================================

class set_custom_status(eg.ActionBase):

    class text:
        label = "Custom status:"
        value = "New value:"


    def __call__(self, stat="", value = 0):
        value = str(value) if isinstance(value, int) else eg.ParseString(value)
        if self.plugin.GetConnection():
            try:
                stat = str(STATUSES[stat])
                req = "/?action=set_custom_status&status=%s" % stat
                req += "&value=%s" % value
                self.plugin.con.request("GET", req)
                res = self.plugin.con.getresponse()
                if res.status == 200:
                    return True
            except:
                raise


    def Configure(self, stat="", value = 0):
        panel = eg.ConfigPanel(self)
        label = wx.StaticText(panel, -1, self.text.label)
        valLabel = wx.StaticText(panel, -1, self.text.value)
        choices = list(STATUSES.iterkeys())
        choices.sort()
        statCtrl = wx.Choice(panel, -1, choices=choices)
        statCtrl.SetStringSelection(stat)
        valCtrl = eg.SmartSpinIntCtrl(panel, -1, value)
        mainSizer = wx.FlexGridSizer(2, 2, 10, 5)
        mainSizer.Add(label,0,wx.TOP,3)
        mainSizer.Add(statCtrl,0,wx.EXPAND)
        mainSizer.Add(valLabel,0,wx.TOP,3)
        mainSizer.Add(valCtrl,0,wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)
        
        while panel.Affirmed():
            panel.SetResult(
                statCtrl.GetStringSelection(),
                valCtrl.GetValue()
            ) 
#===============================================================================

class set_player_status(eg.ActionBase):

    class text:
        label = "Player status:"
        value = "New value:"
        cases = ("Shuffle","Repeat")
        values = ("Off","On")


    def __call__(self, cas=0, value = 0):
        css = ("shuffle","repeat")
        value = str(value) if isinstance(value, int) else eg.ParseString(value)
        if self.plugin.GetConnection():
            try:
                cas = str(css[cas])
                req = "/?action=set_player_status&statusType=%s" % cas
                req += "&value=%s" % value
                self.plugin.con.request("GET", req)
                res = self.plugin.con.getresponse()
                if res.status == 200:
                    return True
            except:
                raise


    def Configure(self, cas=0, value = 0):
        panel = eg.ConfigPanel(self)
        label = wx.StaticText(panel, -1, self.text.label)
        valLabel = wx.StaticText(panel, -1, self.text.value)
        casCtrl = wx.Choice(panel, -1, choices=self.text.cases)
        casCtrl.SetSelection(cas)
        valCtrl = wx.RadioBox(
            panel,
            -1,
            "",
            choices = self.text.values,
            style = wx.RA_SPECIFY_COLS
        )
        valCtrl.SetSelection(value)
        mainSizer = wx.FlexGridSizer(2, 2, 10, 5)
        mainSizer.Add(label,0,wx.TOP,3)
        mainSizer.Add(casCtrl,0,wx.EXPAND)
        mainSizer.Add(valLabel,0,wx.TOP,12)
        mainSizer.Add(valCtrl,0,wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)
        
        while panel.Affirmed():
            panel.SetResult(
                casCtrl.GetSelection(),
                valCtrl.GetSelection()
            ) 
#===============================================================================

class playlist_sort(eg.ActionBase):

    class text:
        nameLabel = "Playlist name:"
        typLabel = "Sort type:"
        types = (
            "Title",
            "Filename",
            "Duration",
            "Artist",
            "Inverse",
            "Randomize",
        )


    def __call__(self, name="", typ=0):
        tps = (
            "title",
            "filename",
            "duration",
            "artist",
            "inverse",
            "randomize",
        )
        id = self.plugin.GetId(eg.ParseString(name))
        typ = typ if isinstance(typ,int) else int(eg.ParseString(typ))
        if self.plugin.GetConnection():
            try:
                req = "/?action=playlist_sort&playlist=%s" % id
                req+="&sort=%s" % str(tps[typ])
                self.plugin.con.request("GET", req)
                res = self.plugin.con.getresponse()
                if res.status == 200:
                    return True
            except:
                raise


    def Configure(self, name="", typ=0):
        panel = eg.ConfigPanel(self)
        nameLabel = wx.StaticText(panel, -1, self.text.nameLabel)
        typLabel = wx.StaticText(panel, -1, self.text.typLabel)
        nameCtrl = wx.TextCtrl(panel, -1, name)
        typCtrl = wx.Choice(panel, -1, choices=self.text.types)
        typCtrl.SetSelection(typ)
        mainSizer = wx.FlexGridSizer(2, 2, 10, 5)
        mainSizer.Add(nameLabel,0,wx.TOP,3)
        mainSizer.Add(nameCtrl,1,wx.EXPAND)
        mainSizer.Add(typLabel,0,wx.TOP,3)
        mainSizer.Add(typCtrl,1,wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)
        
        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
                typCtrl.GetSelection(),
            )  
#===============================================================================

class playlist_add_file(eg.ActionBase):

    class text:
        nameLabel = "Playlist name:"
        fileLabel = "Song file:"
        browseFile = 'Choose a file'


    def __call__(self, name="", file = ""):
        id = self.plugin.GetId(eg.ParseString(name))
        file = eg.ParseString(file)
        if self.plugin.GetConnection():
            try:
                req = "/?action=playlist_add_file&playlist=%s" % id
                req+='&file=%s' % quote(file)
                self.plugin.con.request("GET", req)
                res = self.plugin.con.getresponse()
                if res.status == 200:
                    return True
            except:
                raise


    def Configure(self, name="", file = ""):
        panel = eg.ConfigPanel(self)
        nameLabel = wx.StaticText(panel, -1, self.text.nameLabel)
        fileLabel = wx.StaticText(panel, -1, self.text.fileLabel)
        nameCtrl = wx.TextCtrl(panel, -1, name)
        folder = split(file)[0] if file else eg.folderPath.Music
        fileCtrl = eg.FileBrowseButton(
            panel,
            -1,
            dialogTitle = self.text.browseFile,
            buttonText = eg.text.General.browse,
            startDirectory = folder,
            initialValue = file,
        )
        mainSizer = wx.FlexGridSizer(2, 2, 10, 5)
        mainSizer.AddGrowableCol(1)
        mainSizer.Add(nameLabel,0,wx.TOP,3)
        mainSizer.Add(nameCtrl,1,wx.EXPAND)
        mainSizer.Add(fileLabel,0,wx.TOP,3)
        mainSizer.Add(fileCtrl,1,wx.EXPAND)
        panel.sizer.Add(mainSizer,1,wx.ALL|wx.EXPAND,10)
        
        while panel.Affirmed():
            panel.SetResult(
                nameCtrl.GetValue(),
                fileCtrl.GetValue(),
            )  
#===============================================================================

ACTIONS = (
    ( eg.ActionGroup, 'Player_actions', 'Player control', 'Adds actions to main control AIMP',(
        (simple_action, "player_play", "Play", "Plays media.", None),
        (simple_action, "player_pause", "Pause", "Pauses playback.", None),
        (simple_action, "player_stop", "Stop", "Stops playback.", None),
        (simple_action, "player_next", "Next", "Next song.", None),
        (simple_action, "player_prevous", "Previous", "Previous song.", None),
        (set_track_position, "set_track_position", "Set track position", "Sets track position (in seconds).", None),
        (set_volume, "set_volume", "Set volume percents", "Sets volume (in percents).", None),
        (set_player_status, "set_player_status", "Set player status", "Sets player status.", None),
        (set_custom_status, "set_custom_status", "Set custom status", "Sets custom status.", None),
    )),
    (eg.ActionGroup, 'Playlist_actions', 'Playlist control', 'Adds actions to playlist control AIMP',(
        (song_action, "set_song_play", "Set playing song", "Sets current playing song to the specified one.", "song"),
        (playlist_sort, "playlist_sort", "Playlist sort", "Sorts current playlist.", None),
        (playlist_add_file, "playlist_add_file", "Add song to playlist", "Adds new song to the playlist.", None),
        (song_action, "playlist_del_file", "Remove song from playlist", "Removes song from the playlist.", "file"),
        (song_action, "playlist_queue_add", "Add song to queue", "Adds song to queue in given playlist.", "song"),
        (song_action, "playlist_queue_remove", "Remove song from queue", "Removes song from queue in given playlist.", "song"),
        (set_song_position, "set_song_position", "Change song position", "Changes song position.", None),
    )),
    (eg.ActionGroup, 'Get_info', 'Get info actions', 'Retrieving information from AIMP',(
        (simple_action, "get_playlist_list", "Get playlist list", "Gets playlist list.", "json"),
        (simple_action, "get_update_time", "Get update time", "Gets update time.", "int"),
        (simple_action, "get_player_status", "Get player status", "Gets player status.", "json"),
        (simple_action, "get_song_current", "Get current song", "Gets current song.", "json"),
        (simple_action, "get_volume", "Get volume percents", "Gets volume (in percents).", "int"),
        (simple_action, "get_track_position", "Get track position", "Gets track position.", "json"),
        (simple_action, "get_track_length", "Get track length", "Gets track length.", "int"),
        (get_playlist_songs, "get_playlist_songs", "Get playlist songs", "Gets playlist songs.", None),
        (get_custom_status, "get_custom_status", "Get custom status", "Gets custom status.", None),
        (get_playlist_crc, "get_playlist_crc", "Get playlist crc", "Gets playlist crc.", None),
        (simple_action, "get_version_string", "Get version string", "Gets version string.", "str"),
        (simple_action, "get_version_number", "Get version number", "Gets version number.", "int"),
    )),
)


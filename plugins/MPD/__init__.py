# -*- coding: utf-8 -*-
#
version = 0.0
# plugins/MPD/__init__.py
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
# 0.0 by Pako 2015-09-20 08:22 UTC+1
#     - initial version
# ===============================================================================

import eg

eg.RegisterPlugin(
    name="MPD",
    author="Pako",
    version=version,
    canMultiLoad=True,
    kind="program",
    guid="{386A9955-3113-490A-9E4D-14C4256EA7FD}",
    description='''<rst>
Plugin to control `Media Player Daemon (MPD)`_.

`Media Player Daemon (MPD)`_ is a flexible, powerful, server-side application 
for playing music.

| This plugin is based on a library `python-mpd2`_.
| On the website `Commands`_ you will find a more detailed description 
  of some commands.

Plugin version: %s

.. _`Media Player Daemon (MPD)`:        http://www.musicpd.org/
.. _`python-mpd2`:                      https://github.com/Mic92/python-mpd2
.. _`Commands`:     http://pythonhosted.org/python-mpd2/topics/commands.html
''' % version,
    createMacrosOnAdd=True,
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAACAAAAAhCAYAAAC4JqlRAAAENElEQVRYw62XS0xcVRjH"
        "f+fcyzB3eEyQdHhlaiO05TG2Ndq0BFtjpLMwLkwTxxVujNFo4saaWBMX7tS404010Y2J"
        "ZmoTVy6IVi0t0YCwMAMtSAkkDLW0FOzAZV73uOBAQObOk+/m5izO4/+d/3e+l6B48QAW"
        "YOrR+N98FrCBjB5TxRwqCsxLoAFoBTqAw1FbfVzo0IglzgN/A3HgAeCUo0AN0AU8E7XV"
        "p5QhEUtcAH4DJoG1YhUQQAA4A/RHbfU6FUrEEi8BQ8BdQOVTwNRUPx211ZfFAmQzWUBh"
        "mGY+JV4DrmvTZHbaeKc8BgyUAr40e48rFwe5/vWfZNJZ13X6zAGNQS4FAkBf1Fbvl0Jv"
        "KmEy8WOaycEHpNbSedfqs/s01i4FLKA3aquvSjawAImPpek1ZkfnCy7XGL0aE6n/TiBc"
        "9isTisQdwdAXfzFx9SbpZEEmftCY0gTqNfVvlv/OHaTwcfvaKku3h+l5foYnzx8jeLwN"
        "KaXbpj5gVmp7hCpzNLXpBbKeRLyR4Ut3uHzhZ0Yuj+E4jhsLnwEBCYQq9XWFg+k1kFUS"
        "IUxM2cQ/MR+/fj7B7Mhcvq0hqaNdBegOKEVzdw2HzzYhpbnJhvByf1py6+qCjhM5Wbgi"
        "dcitULI0BA3C73Vw9o2j+Fv8gEBgEY8lSK27P0oZtdXFyuhXKBwclaGp00f/uwd58aMQ"
        "nf1tCGGydj+Dk1Gu+032RZztEG9WS7rCj+BvrSK5nsReXUEpkTfdVixKZfdk3NZQHY+/"
        "0IRRLQvm+xKAFJlUhtRGinQyhZPdurmz7Yo7JXjCj+XPT3JRJnAch/jNBaaGplmILZJY"
        "2sC0JC1HDuDz16Oc1B5wgPpmH93nDmIYsnwF7Ifr3PhmmJHvYtyd2kA4XlAeFFkm5DLe"
        "OoPkqjdn0eNvsTg10I5huisgI5b40G0yk87wy6VrDH4yytKkB8M5gKQeKbwYogZDNZD+"
        "tw4pPDguVVc+8C0GXFPY/Pg8I99OkV1v2A4wuahGqYLFpUuR8qoJjLstWLy1wsO4RGCA"
        "UnmyoaC2sax4Ni6BeMQSH+Ssw6t8SMPSwcb9q671cuhkC4ZplKpAXALLwB+5ZoMnmgge"
        "b9Glo5PjV1T7fPS+0kPXubZS6Q8DyxJIA2MRS+zJiM2dDTz39hMcPdNOlbcGIaRmXGJ4"
        "LFq7g4TfOcmzb3XhrfWUevsxIC12VMdHgJejttrjFctzNjM37rE4uYK9msbyewh01HHo"
        "dCOBjhqkIUq9fScwBewK0gbwVNRWv+eOgluZ10EIiZAgRFkv/zQwqlu5XaE4C8S0bXI9"
        "dKSx6dfSKBs8DMS2wN06o2qgPWqrGPsoEUv0ADNAspjeUOqG9FTUVt/vA3hQN6pOqd1x"
        "LfAo0KFL6VKBQ8AckCi3Pd9aYwJ+oAUIRG31Ux7QY8AisKp7QJXv8P8AFmiMWbUDCO8A"
        "AAAASUVORK5CYII="
    ),
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=7425"
)

import socket
from threading import Thread, Timer

import wx
from wx import ComboCtrl, ComboPopup

from mpd import MPDClient

TEST_PERIOD = 10
TIMEOUT = 2  # CONDITION: TIMEOUT < TEST_PERIOD !!!
ACV = wx.ALIGN_CENTER_VERTICAL


# ===============================================================================

class Text:
    error1 = "Error: MPD:Save playlist: Playlist already exists"
    error2 = "Error: MPD:Save playlist"
    prefix = "Event prefix:"
    host = "Host address:"
    port = "TCP/IP port:"
    password = "Password (optional):"
    MPD = "MPD settings"
    filter = "Selector of events ..."
    evtFilter = [
        "Connected/Disconnected",
        "State (playing, paused, stopped)",
        "Song changed",
        "Volume changed",
        "Repeat mode changed",
        "Random mode changed",
        "Consume mode changed",
        "Single mode changed"
    ]


# ===============================================================================

class CheckListComboBox(ComboCtrl):
    class CheckListBoxComboPopup(ComboPopup):

        def __init__(self, values, helpText):
            ComboPopup.__init__(self)
            self.values = values
            self.helpText = helpText

        def OnDclick(self, evt):
            self.Dismiss()
            self.SetHelpText()

        def Init(self):
            self.curitem = None

        def Create(self, parent):
            self.lb = wx.CheckListBox(parent, -1, (80, 50), wx.DefaultSize)
            # self.itemHeight = self.lb.GetItemHeight()
            self.SetValue(self.values)
            self.SetHelpText()
            self.lb.Bind(wx.EVT_MOTION, self.OnMotion)
            self.lb.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
            self.lb.Bind(wx.EVT_LEFT_DCLICK, self.OnDclick)
            return True

        def SetHelpText(self, helpText=None):
            self.helpText = helpText if helpText is not None else self.helpText
            combo = self.GetComboCtrl()
            combo.SetText(self.helpText)
            combo.TextCtrl.SetEditable(False)

        def SetValue(self, values):
            self.lb.Set(values[0])
            for i in range(len(values[1])):
                self.lb.Check(i, int(values[1][i]))

        def GetValue(self):
            strngs = self.lb.GetStrings()
            return [strngs, [self.lb.IsChecked(i) for i in range(len(strngs))]]

        def GetStringValue(self):
            strngs = self.lb.GetStrings()
            return str([strngs, [self.lb.IsChecked(i) for i in range(len(strngs))]])

        def GetControl(self):
            return self.lb

        def OnPopup(self):
            if self.curitem:
                self.lb.EnsureVisible(self.curitem)
                self.lb.SetSelection(self.curitem)

        # def GetAdjustedSize(self, minWidth, prefHeight, maxHeight):
        #     return wx.Size(
        #         minWidth,
        #         min(self.itemHeight * (0.5 + len(self.lb.GetStrings())), maxHeight)
        #     )

        def OnMotion(self, evt):
            item = self.lb.HitTest(evt.GetPosition())
            if item > -1:
                self.lb.SetSelection(item)
                self.curitem = item
            evt.Skip()

        def OnLeftDown(self, evt):
            item = self.lb.HitTest(evt.GetPosition())
            if item > -1:
                self.curitem = item
            evt.Skip()

    def __init__(self, parent, id=-1, values=[[], []], **kwargs):
        if 'helpText' in kwargs:
            helpText = kwargs['helpText']
            del kwargs['helpText']
        else:
            helpText = ""
        ComboCtrl.__init__(self, parent, id, **kwargs)
        self.popup = self.CheckListBoxComboPopup(values, helpText)
        self.SetPopupControl(self.popup)
        self.popup.lb.Bind(wx.EVT_CHECKLISTBOX, self.onCheck)

    def onCheck(self, evt):
        wx.PostEvent(self, evt)
        evt.StopPropagation()

    def GetValue(self):
        return self.popup.GetValue()

    def SetValue(self, values):
        self.popup.SetValue(values)

    def SetHelpText(self, helpText=None):
        self.popup.SetHelpText(helpText)


# ===============================================================================

class MPDworker(eg.ThreadWorker):
    """
    A thread worker ...
    """
    ctimer = None
    liveTimer = None
    watchdog = None
    last_status = None
    last_song = None
    last_repeat = None
    last_consume = None
    last_random = None
    last_single = None
    last_volume = None

    def Ping(self):
        try:
            self.client.ping()
        except:
            pass

    def Watchdog(self):
        try:
            self.watchdog.cancel()
            ping = self.Func(self.Ping, 5.0)
            ping()
            self.watchdog = Timer(30.0, self.Watchdog)
            self.watchdog.start()
        except:
            pass
            # try reconnect ?

    def isLive(self):
        try:
            self.watchdog.cancel()
            self.client.ping()
            self.watchdog = Timer(30.0, self.Watchdog)
            self.watchdog.start()
            return True
        except:
            return False
            # try reconnect ?

    def Connect(self):
        try:
            self.client.connect(self.host, self.port)
            if self.password:
                self.client.password(self.password)
            self.runFlag = True
            if self.plugin.evtFilter[0]:
                self.plugin.TriggerEvent("Connected")
            self.watchdog = Timer(30.0, self.Watchdog)
            self.watchdog.start()
            if True in self.plugin.evtFilter[1:]:
                self.client2.connect(self.host, self.port)
                if self.password:
                    self.client2.password(self.password)
                self.ct = Thread(target=self.observe_mpd)
                self.ct.start()
        except:
            # eg.PrintTraceback()
            self.ctimer = Timer(TEST_PERIOD - TIMEOUT, self.Connect)
            self.ctimer.start()

    def Setup(self, plugin, host, port, password):
        """
        This will be called inside the thread at the beginning.
        """
        self.plugin = plugin
        self.host = host
        self.port = port
        self.password = password if password != "" else None
        self.lastEvent = None
        self.client = MPDClient(use_unicode=True)
        if True in self.plugin.evtFilter[1:]:
            self.client2 = MPDClient(use_unicode=True)
        self.client.timeout = TIMEOUT
        self.client.idletimeout = None
        self.ctimer = Timer(0.1, self.Connect)
        self.ctimer.start()

    def isRunning(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            sock.connect((self.host, self.port))
            sock.close()
            if self.client.mpd_version is not None \
                and self.client2.mpd_version is not None:
                return True
        except:
            pass
        try:
            self.client.disconnect()
        except:
            pass
        if True in self.plugin.evtFilter[1:]:
            try:
                self.client2.disconnect()
            except:
                pass
        try:
            try:
                self.watchdog.cancel()
            except:
                pass
            self.runFlag = False
            self.client.connect(self.host, self.port)
            if self.password:
                self.client.password(self.password)
            if True in self.plugin.evtFilter[1:]:
                self.client2.connect(self.host, self.port)
                if self.password:
                    self.client2.password(self.password)
            self.runFlag = True
            if True in self.plugin.evtFilter[1:]:
                self.ct = Thread(target=self.observe_mpd)
                self.ct.start()
            self.watchdog = Timer(30.0, self.Watchdog)
            self.watchdog.start()
            return True
        except:
            if self.plugin.evtFilter[0]:
                self.plugin.TriggerEvent("Disconnected")
        self.ctimer = Timer(0.1, self.Connect)
        self.ctimer.start()
        return False

    def liveTest(self):
        if self.runFlag:
            if self.isRunning():
                self.liveTimer = Timer(TEST_PERIOD, self.liveTest)
                self.liveTimer.start()

    def observe_mpd(self):
        if self.isRunning():
            self.liveTimer = Timer(5.0, self.liveTest)
            self.liveTimer.start()
            client = self.client2

            def getCurrSong():
                currSong = client.currentsong()
                file = currSong["file"] if currSong.has_key("file") else ""
                title = currSong["title"] if currSong.has_key("title") else ""
                artst = currSong["artist"] if currSong.has_key("artist") else ""
                album = currSong["album"] if currSong.has_key("album") else ""
                return (title, artst, album, file)

            sbs = []
            if self.plugin.evtFilter[1] or True in self.plugin.evtFilter[3:]:
                status = client.status()
            if self.plugin.evtFilter[1] or self.plugin.evtFilter[2]:
                sbs.append('player')
                if self.plugin.evtFilter[1]:
                    self.last_status = status['state']
                if self.plugin.evtFilter[2]:
                    self.last_song = getCurrSong()
            if self.plugin.evtFilter[3]:
                sbs.append('mixer')
                self.last_volume = int(status['volume']) \
                    if status.has_key("volume") else None
            if True in self.plugin.evtFilter[4:]:
                sbs.append('options')
                if self.plugin.evtFilter[4]:
                    self.last_repeat = int(status['repeat']) \
                        if status.has_key("repeat") else None
                if self.plugin.evtFilter[5]:
                    self.last_random = int(status['random']) \
                        if status.has_key("random") else None
                if self.plugin.evtFilter[6]:
                    self.last_consume = int(status['consume']) \
                        if status.has_key("consume") else None
                if self.plugin.evtFilter[7]:
                    self.last_single = int(status['single']) \
                        if status.has_key("single") else None
            while self.runFlag:
                try:
                    subs = client.idle(*sbs)
                except Exception, e:
                    pass
                    # if e.message == "Not connected":
                    #    pass
                    # else:
                    #    #eg.PrintError(e.message.decode(eg.systemEncoding))
                    #    pass
                try:
                    status = client.status()
                    if 'player' in subs:
                        if self.plugin.evtFilter[1]:
                            current_status = status['state']
                            if current_status != self.last_status:
                                if current_status == "play":
                                    self.plugin.TriggerEvent("Playing")
                                elif current_status == "pause":
                                    self.plugin.TriggerEvent("Paused")
                                elif current_status == "stop":
                                    self.plugin.TriggerEvent("Stopped")
                                self.last_status = current_status
                        if self.plugin.evtFilter[2]:
                            current_song = getCurrSong()
                            if current_song == ("", "", "", ""):
                                current_song = getCurrSong()
                            if current_song != self.last_song:
                                self.plugin.TriggerEvent(
                                    "SongChanged",
                                    payload=current_song
                                )
                                self.last_song = current_song
                    if 'mixer' in subs:
                        if self.plugin.evtFilter[3]:
                            vol = int(status['volume']) \
                                if status.has_key("volume") else None
                            if vol != self.last_volume:
                                self.plugin.TriggerEvent(
                                    "Volume",
                                    payload=int(vol) if vol is not None else None
                                )
                                self.last_volume = vol
                    if 'options' in subs:
                        if self.plugin.evtFilter[4]:
                            rpt = int(status['repeat']) \
                                if status.has_key("repeat") else None
                            if rpt != self.last_repeat:
                                self.plugin.TriggerEvent(
                                    "Repeat.%s" % str(rpt),
                                    payload=None if rpt is None else int(rpt)
                                )
                                self.last_repeat = rpt
                        if self.plugin.evtFilter[5]:
                            rndm = int(status['random']) \
                                if status.has_key("random") else None
                            if rndm != self.last_random:
                                self.plugin.TriggerEvent(
                                    "Random.%s" % str(rndm),
                                    payload=None if rndm is None else int(rndm)
                                )
                                self.last_random = rndm
                        if self.plugin.evtFilter[6]:
                            cnsm = int(status['consume']) \
                                if status.has_key("consume") else None
                            if cnsm != self.last_consume:
                                self.plugin.TriggerEvent(
                                    "Consume.%s" % str(cnsm),
                                    payload=None if cnsm is None else int(cnsm)
                                )
                                self.last_consume = cnsm
                        if self.plugin.evtFilter[7]:
                            sngl = int(status['single']) \
                                if status.has_key("single") else None
                            if sngl != self.last_single:
                                self.plugin.TriggerEvent(
                                    "Single.%s" % str(sngl),
                                    payload=None if sngl is None else int(sngl)
                                )
                                self.last_single = sngl

                except:
                    eg.PrintTraceback

    def Disconnect(self):
        try:
            self.client.close()
        except:
            pass
        try:
            self.client.disconnect()
        except:
            pass
        if True in self.plugin.evtFilter[1:]:
            try:
                self.client2.close()
            except:
                pass
            try:
                self.client2.disconnect()
            except:
                pass

    @eg.LogIt
    def Finish(self):
        """
        This will be called inside the thread when it finishes. It will even
        be called if the thread exits through an exception.
        """
        self.runFlag = False
        try:
            self.liveTimer.cancel()
        except:
            pass
        try:
            self.ctimer.cancel()
        except:
            pass
        try:
            self.watchdog.cancel()
        except:
            pass
        wx.CallAfter(self.Disconnect)

    # --------------------------------- COMMANDS ------------------------------------

    def AddCurrentUri(self, pl):
        if self.isRunning():
            currSong = self.client.currentsong()
            uri = currSong["file"] if currSong.has_key("file") else ""
            if not uri:
                return
            plsts = self.client.listplaylists()
            plsts = [item['playlist'] for item in plsts \
                     if item.has_key('playlist')]
            if pl in plsts:
                return self.client.playlistadd(pl, uri)
            else:
                try:
                    return self.client.playlistadd(pl, uri)
                except:
                    return

    def AddId(self, uri, pos):
        if self.isRunning():
            try:
                return self.client.addid(uri, pos - 1)
            except:
                pass

    def AddUri(self, uri):
        if self.isRunning():
            try:
                return self.client.add(uri)
            except:
                pass

    def AddUri2PL(self, pl, uri):
        if self.isRunning():
            plsts = self.client.listplaylists()
            plsts = [item['playlist'] for item in plsts \
                     if item.has_key('playlist')]
            if pl in plsts:
                return self.client.playlistadd(pl, uri)
            else:
                try:
                    return self.client.playlistadd(pl, uri)
                except:
                    return

    def Clear(self):
        if self.isRunning():
            return self.client.clear()

    def ClearPlaylist(self, val):
        if self.isRunning():
            plsts = self.client.listplaylists()
            plsts = [item['playlist'] for item in plsts \
                     if item.has_key('playlist')]
            if val in plsts:
                return self.client.playlistclear(val)
            else:
                try:
                    return self.client.playlistclear(val)
                except:
                    return

    def Delete(self, pos):
        if self.isRunning():
            self.client.delete(pos - 1)

    def DeleteId(self, id):
        if self.isRunning():
            self.client.deleteid(id)

    def DisableOutput(self, id):
        if self.isRunning():
            self.client.disableoutput(id)

    def EnableOutput(self, id):
        if self.isRunning():
            self.client.enableoutput(id)

    def GetCrossfade(self):
        if self.isRunning():
            status = self.client.status()
            return int(status['xfade']) if status.has_key("xfade") else None

    def GetConsume(self):
        if self.isRunning():
            status = self.client.status()
            return int(status['consume']) if status.has_key("consume") else None

    def GetOutputs(self):
        if self.isRunning():
            return self.client.outputs()

    def GetPause(self):
        if self.isRunning():
            status = self.client.status()
            current_status = status['state']
            return int(current_status != "play")

    def GetPlaylist(self):
        if self.isRunning():
            return self.client.playlist()

    def GetPlaylists(self):
        if self.isRunning():
            return self.client.listplaylists()

    def GetRandom(self):
        if self.isRunning():
            status = self.client.status()
            return int(status['random']) if status.has_key("random") else None

    def GetRepeat(self):
        if self.isRunning():
            status = self.client.status()
            return int(status['repeat']) if status.has_key("repeat") else None

    def GetReplayGain(self):
        if self.isRunning():
            return self.client.replay_gain_status()

    def GetSingle(self):
        if self.isRunning():
            status = self.client.status()
            return int(status['single']) if status.has_key("single") else None

    def GetSong(self):
        if self.isRunning():
            currSong = self.client.currentsong()
            file = currSong["file"] if currSong.has_key("file") else ""
            title = currSong["title"] if currSong.has_key("title") else ""
            artist = currSong["artist"] if currSong.has_key("artist") else ""
            album = currSong["album"] if currSong.has_key("album") else ""
            return (title, artist, album, file)

    def GetStats(self):
        if self.isRunning():
            return self.client.stats()

    def GetStatus(self):
        if self.isRunning():
            return self.client.status()

    def GetVersion(self):
        if self.isRunning():
            return self.client.mpd_version

    def GetVolume(self):
        if self.isRunning():
            status = self.client.status()
            return int(status['volume']) if status.has_key("volume") else None

    def Listplaylist(self, val):
        if self.isRunning():
            plsts = self.client.listplaylists()
            plsts = [item['playlist'] for item in plsts \
                     if item.has_key('playlist')]
            if val in plsts:
                return self.client.listplaylist(val)
            else:
                try:
                    return self.client.listplaylist(val)
                except:
                    return

    def Listplaylistinfo(self, val):
        if self.isRunning():
            plsts = self.client.listplaylists()
            plsts = [item['playlist'] for item in plsts \
                     if item.has_key('playlist')]
            if val in plsts:
                return self.client.listplaylistinfo(val)
            else:
                try:
                    return self.client.listplaylistinfo(val)
                except:
                    return

    def Load(self, val):
        if self.isRunning():
            self.client.load(val)

    def Next(self):
        if self.isRunning():
            return self.client.next()

    def Play(self, pos):
        if self.isRunning():
            self.client.play(pos - 1)

    def PlayId(self, id):
        if self.isRunning():
            try:
                self.client.playid(id)
            except Exception, e:
                eg.PrintError(e.message.decode(eg.systemEncoding))

    def Previous(self):
        if self.isRunning():
            return self.client.previous()

    def RemovePlaylist(self, val):
        if self.isRunning():
            plsts = self.client.listplaylists()
            plsts = [item['playlist'] for item in plsts \
                     if item.has_key('playlist')]
            if val in plsts:
                return self.client.rm(val)
            else:
                try:
                    return self.client.rm(val)
                except:
                    return

    def Rescan(self, uri):
        if self.isRunning():
            try:
                return self.client.rescan(uri) if uri else self.client.rescan()
            except:
                pass

    def Save(self, val):
        if self.isRunning():
            plsts = self.client.listplaylists()
            plsts = [item['playlist'] for item in plsts \
                     if item.has_key('playlist')]
            if val in plsts:
                eg.PrintError(self.plugin.text.error1)
            else:
                try:
                    self.client.save(val)
                except:
                    eg.PrintError(self.plugin.text.error2)

    def Seek(self, unit, pos, dir, value, kind=None, id_ix=None):
        if self.isRunning():
            status = self.client.status()
            if id_ix is None:
                id_ix = status['songid'] if status.has_key("songid") else None
            if id_ix is None:
                return
            tm = status['time'] if status.has_key("time") else None
            if tm is None:
                return
            elapsed, max = [int(item) for item in tm.split(":")]
            value = int((value * float(max) / 100 if unit else value) + 0.5)
            if pos:  # absolute
                value = value if value < max else max - 0.1
            else:  # relative
                if dir:  # backward
                    newval = elapsed - value
                    value = newval if newval >= 0 else 0
                else:  # forward
                    newval = elapsed + value
                    value = newval if newval <= max else max - 0.1
            if kind is None or kind:
                self.client.seekid(id_ix, value)
            else:
                self.client.seek(id_ix - 1, value)

    def SetConsume(self, val):
        if self.isRunning():
            self.client.consume(val)

    def SetCrossfade(self, cs):
        if self.isRunning():
            self.client.crossfade(cs)

    def SetPause(self, val):
        if self.isRunning():
            status = self.client.status()
            curr_st = status['state']
            if val:
                if curr_st == "play":
                    return self.client.pause(val)
            else:
                if curr_st == "pause":
                    return self.client.pause(val)
                elif curr_st == "stop":
                    return self.client.play(0)

    def SetRandom(self, val):
        if self.isRunning():
            self.client.random(val)

    def SetRepeat(self, val):
        if self.isRunning():
            self.client.repeat(val)

    def SetReplayGain(self, val):
        if self.isRunning():
            return self.client.replay_gain_mode(val)

    def SetSingle(self, val):
        if self.isRunning():
            self.client.single(val)

    def SetVolume(self, vol):
        if self.isRunning():
            self.client.setvol(vol)

    def Shuffle(self):
        if self.isRunning():
            return self.client.shuffle()

    def Stop_(self):
        if self.isRunning():
            return self.client.stop()

    def ToggleOutput(self, id):
        if self.isRunning():
            outputs = self.client.outputs()
            outputs = dict([(
                int(item['outputid']),
                int(item['outputenabled'])
            ) for item in outputs])
            if outputs[id]:
                self.client.disableoutput(id)
            else:
                self.client.enableoutput(id)

    def Update(self, uri):
        if self.isRunning():
            try:
                return self.client.update(uri) if uri else self.client.update()
            except:
                pass


# ===============================================================================

class MPD(eg.PluginBase):
    text = Text
    mpdworker = None

    def __init__(self):
        self.AddActionsFromList(ACTIONS)

    @eg.LogIt
    def __start__(
        self,
        prefix="MPD",
        host="",
        port=6600,
        password="",
        evtFilter=len(Text.evtFilter) * [True],
    ):
        self.info.eventPrefix = prefix
        self.evtFilter = evtFilter
        self.mpdworker = MPDworker(self, host, port, password)
        self.mpdworker.Start(10.0)

    def StopWorker(self):
        self.mpdworker.Stop()
        self.mpdworker = None

    def __stop__(self):
        wx.CallAfter(self.StopWorker)

    def Configure(
        self,
        prefix="MPD",
        host="",
        port=6600,
        password="",
        evt_filter=len(Text.evtFilter) * [True],
    ):
        text = self.text
        evtFilter = [self.text.evtFilter]
        evtFilter.append(evt_filter)
        panel = eg.ConfigPanel()
        prefixCtrl = panel.TextCtrl(prefix)
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        passwordCtrl = wx.TextCtrl(panel, -1, password, style=wx.TE_PASSWORD)
        labels = (
            panel.StaticText(text.prefix),
            panel.StaticText(text.host),
            panel.StaticText(text.port),
            panel.StaticText(text.password)
        )
        eg.EqualizeWidths(labels)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(labels[0], 0, ACV | wx.LEFT, 10)
        topSizer.Add(prefixCtrl, 0, wx.EXPAND | wx.LEFT, 5)
        sizer = wx.FlexGridSizer(3, 2, 5, 5)
        sizer.AddGrowableCol(1)
        sizer.Add(labels[1], 0, ACV)
        sizer.Add(hostCtrl, 0)
        sizer.Add(labels[2], 0, ACV)
        sizer.Add(portCtrl)
        sizer.Add(labels[3], 0, ACV)
        sizer.Add(passwordCtrl)
        staticBox = wx.StaticBox(panel, label=text.MPD)
        staticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        staticBoxSizer.Add(sizer, 0, wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.EXPAND, 5)
        panel.sizer.Add(topSizer, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        panel.sizer.Add(staticBoxSizer, 0, wx.EXPAND | wx.BOTTOM, 10)
        eventFilter = CheckListComboBox(
            panel,
            -1,
            values=evtFilter,
            helpText=text.filter
        )
        panel.sizer.Add(eventFilter, 0, wx.EXPAND | wx.LEFT, 0)

        while panel.Affirmed():
            panel.SetResult(
                prefixCtrl.GetValue(),
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
                passwordCtrl.GetValue(),
                eventFilter.GetValue()[1]
            )

    def str2int(self, s):
        s = eg.ParseString(s)
        try:
            s = int(s)
        except:
            s = 0
        return s

    def isLive(self):
        wd = self.mpdworker.Func(self.mpdworker.isLive, 5.0)
        return wd()


# ===============================================================================

class AddId(eg.ActionBase):

    def __call__(self, uri="", pos=0):
        if self.plugin.isLive():
            pos = pos if isinstance(pos, int) else self.plugin.str2int(pos)
            wrkr = self.plugin.mpdworker
            wrFnc = wrkr.Func(getattr(wrkr, self.__class__.__name__), 5.0)
            return wrFnc(uri, pos)

    def GetLabel(self, pl, uri):
        return self.text.label_tree + ":" + uri + ":" + pos

    def Configure(self, uri="", pos=0):
        panel = eg.ConfigPanel(self)
        label = wx.StaticText(panel, -1, self.text.label_conf)
        label2 = wx.StaticText(panel, -1, self.text.label_conf2)
        eg.EqualizeWidths((label, label2))
        txtCtrl = wx.TextCtrl(panel, -1, uri)
        posCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            pos,
            min=1,
            max=999999
        )
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(label, 0, ACV)
        sizer.Add(txtCtrl, 1, wx.LEFT | wx.EXPAND, 5)
        sizer2.Add(label2, 0, ACV)
        sizer2.Add(posCtrl, 0, wx.LEFT, 5)
        panel.sizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)
        panel.sizer.Add(sizer2, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(
                txtCtrl.GetValue(),
                posCtrl.GetValue()
            )

    class text:
        label_tree = "Add URI to specified position "
        label_conf = "URI:"
        label_conf2 = "Position:"


# ===============================================================================

class Command5(eg.ActionBase):

    def __call__(self, uri=""):
        if self.plugin.isLive():
            wrkr = self.plugin.mpdworker
            wrFnc = wrkr.Func(getattr(wrkr, self.__class__.__name__), 5.0)
            return wrFnc(uri)

    def GetLabel(self, pl, uri):
        return self.text.label_tree + ":" + uri

    def Configure(self, uri=""):
        panel = eg.ConfigPanel(self)
        txtCtrl = wx.TextCtrl(panel, -1, uri)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, -1, self.text.label_conf)
        sizer.Add(label, 0, ACV)
        sizer.Add(txtCtrl, 1, wx.LEFT | wx.EXPAND, 5)
        panel.sizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(
                txtCtrl.GetValue(),
            )

    class text:
        label_tree = "Add URI to current queue "
        label_conf = "URI:"


# ===============================================================================

class AddUri2PL(eg.ActionBase):

    def __call__(self, pl="", uri=""):
        if self.plugin.isLive():
            wrkr = self.plugin.mpdworker
            wrFnc = wrkr.Func(getattr(wrkr, self.__class__.__name__), 5.0)
            return wrFnc(pl, uri)

    def GetLabel(self, pl, uri):
        return self.text.label_tree + ":" + pl + ":" + uri

    def Configure(self, pl="", uri=""):
        panel = eg.ConfigPanel(self)
        txtCtrl = wx.TextCtrl(panel, -1, uri)
        txtCtrl2 = wx.TextCtrl(panel, -1, pl)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, -1, self.text.label_conf)
        label2 = wx.StaticText(panel, -1, self.text.label_conf2)
        eg.EqualizeWidths((label, label2))
        sizer.Add(label, 0, ACV)
        sizer.Add(txtCtrl, 1, wx.LEFT | wx.EXPAND, 5)
        sizer2.Add(label2, 0, ACV)
        sizer2.Add(txtCtrl2, 1, wx.LEFT | wx.EXPAND, 5)
        panel.sizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)
        panel.sizer.Add(sizer2, 0, wx.LEFT | wx.RIGHT | wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(
                txtCtrl2.GetValue(),
                txtCtrl.GetValue(),
            )

    class text:
        label_tree = "Add URI to playlist "
        label_conf = "URI:"
        label_conf2 = "Playlist name:"


# ===============================================================================

class ChangeVolume(eg.ActionBase):

    def __call__(self, step=5):
        if self.plugin.isLive():
            wrkr = self.plugin.mpdworker
            wrFnc = wrkr.Func(wrkr.GetVolume, 5.0)
            vol = wrFnc()
            if vol is not None:
                if self.value:  # DOWN
                    vol -= step
                    vol = vol if vol > -1 else 0
                else:  # UP
                    vol += step
                    vol = vol if vol < 101 else 100
                wrFnc = wrkr.Func(wrkr.SetVolume, 5.0)
                res = wrFnc(vol)
                return res

    def GetLabel(self, step):
        return self.text.label_tree[self.value] + str(int(step)) + "%"

    def Configure(self, step=5):
        panel = eg.ConfigPanel(self)
        volumeCtrl = eg.SpinIntCtrl(panel, -1, step, min=1, max=100)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, -1, self.text.label_conf)
        sizer.Add(label, 0, ACV)
        sizer.Add(volumeCtrl, 0, wx.LEFT, 5)
        panel.sizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())

    class text:
        label_tree = ("Volume up ", "Volume down ")
        label_conf = "Volume step [%]:"


# ===============================================================================

class Command(eg.ActionBase):

    def __call__(self):
        if self.plugin.isLive():
            wrkr = self.plugin.mpdworker
            wrFnc = wrkr.Func(getattr(wrkr, self.__class__.__name__), 5.0)
            res = wrFnc()
            return res


# ===============================================================================

class Command2(eg.ActionBase):

    def __call__(self):
        if self.plugin.isLive():
            kind = self.__class__.__name__.split("_")[0]
            wrkr = self.plugin.mpdworker
            if self.value is None:
                wrFnc = wrkr.Func(getattr(wrkr, "Get" + kind), 5.0)
                val = wrFnc()
                if val is not None:
                    val = (1, 0)[val]
                else:
                    return
            else:
                val = self.value
            wrFnc = wrkr.Func(getattr(wrkr, "Set" + kind), 5.0)
            wrFnc(val)
            wrFnc = wrkr.Func(getattr(wrkr, "Get" + kind), 5.0)
            return wrFnc()
        # ===============================================================================


class Command3(eg.ActionBase):

    def __call__(self, pos=1):
        if self.plugin.isLive():
            pos = pos if isinstance(pos, int) else self.plugin.str2int(pos)
            wrkr = self.plugin.mpdworker
            wrFnc = wrkr.Func(getattr(wrkr, self.__class__.__name__), 5.0)
            wrFnc(pos)

    def GetLabel(self, pos):
        return self.text.label_tree[self.value] + str(int(pos))

    def Configure(self, pos=1):
        panel = eg.ConfigPanel(self)
        csCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            pos,
            min=int(self.value < 4),
            max=999999
        )
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, -1, self.text.label_conf[self.value])
        sizer.Add(label, 0, ACV)
        sizer.Add(csCtrl, 0, wx.LEFT, 5)
        panel.sizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(csCtrl.GetValue())

    class text:
        label_tree = (
            "Play [sequential number] ",
            "Play [song ID] ",
            "Delete [sequential number] ",
            "Delete [song ID] ",
            "Disable output [ID] ",
            "Enable output [ID] ",
            "Toggle output [ID] ",
        )
        label_conf = (
            "Sequential number:",
            "Song ID:",
            "Sequential number:",
            "Song ID:",
            "Output ID:",
            "Output ID:",
            "Output ID:",
        )


# ===============================================================================

class Command4(eg.ActionBase):

    def __call__(self, val=""):
        if self.plugin.isLive():
            wrkr = self.plugin.mpdworker
            wrFnc = wrkr.Func(getattr(wrkr, self.__class__.__name__), 5.0)
            return wrFnc(val)

    def GetLabel(self, val):
        return self.text.label_tree[self.value] + val

    def Configure(self, val=""):
        panel = eg.ConfigPanel(self)
        txtCtrl = wx.TextCtrl(panel, -1, val)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, -1, self.text.label_conf)
        sizer.Add(label, 0, ACV)
        sizer.Add(txtCtrl, 1, wx.LEFT | wx.EXPAND, 5)
        panel.sizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(txtCtrl.GetValue())

    class text:
        label_tree = (
            "Load playlist ",
            "Get playlist ",
            "Get playlist info ",
            "Save playlist ",
            "Clear playlist ",
            "Remove playlist ",
            "Add current URI to playlist ",

        )
        label_conf = "Playlist name:"


# ===============================================================================

class Seek(eg.ActionBase):
    class text:
        label = "Seek value:"
        unit = "Unit"
        unitChoice = ("Second", "Percent")
        pos = "Positioning"
        posChoice = ("Relatively", "Absolutely")
        dir = "Direction"
        dirChoice = ("Forward", "Backward")
        id_ix = ("Sequential number:", "Song ID:")

    def __call__(self, value=5, unit=1, pos=0, dir=0, id_ix=0):
        value = value if isinstance(value, int) else self.plugin.str2int(value)
        id_ix = id_ix if isinstance(id_ix, int) else self.plugin.str2int(id_ix)
        dir = 0 if pos else dir
        wrkr = self.plugin.mpdworker
        wrFnc = wrkr.Func(wrkr.Seek, 5.0)
        wrFnc(unit, pos, dir, value, self.value, id_ix)

    def GetLabel(self, value, unit, pos, dir, id_ix):
        if pos:
            return "%s: %s%s, %s" % (
                self.name,
                value,
                ("", "%")[unit],
                self.text.posChoice[pos]
            )
        else:
            return "%s: %s%s, %s, %s" % (
                self.name,
                value,
                ("", "%")[unit],
                self.text.posChoice[pos],
                self.text.dirChoice[dir]
            )

    def Configure(self, value=5, unit=1, pos=0, dir=0, id_ix=0):
        text = self.text
        panel = eg.ConfigPanel()
        mySizer = wx.BoxSizer(wx.VERTICAL)
        panel.sizer.Add(mySizer, 1, wx.EXPAND | wx.LEFT, 10)
        width = 180
        staticText = panel.StaticText(text.label)
        valueCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            value,
            min=0,
            max=65535
        )
        unitSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.unit),
            wx.HORIZONTAL
        )
        rb1 = panel.RadioButton(
            not unit,
            text.unitChoice[0],
            style=wx.RB_GROUP,
            size=(width, -1)
        )
        rb2 = panel.RadioButton(unit, text.unitChoice[1])
        unitSizer.Add(rb1, 1)
        unitSizer.Add(rb2, 1)
        posSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.pos),
            wx.HORIZONTAL
        )
        rb3 = panel.RadioButton(
            not pos,
            text.posChoice[0],
            style=wx.RB_GROUP,
            size=(width, -1)
        )
        rb4 = panel.RadioButton(pos, text.posChoice[1])
        posSizer.Add(rb3, 1)
        posSizer.Add(rb4, 1)
        dirSizer = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.dir),
            wx.HORIZONTAL
        )
        rb5 = panel.RadioButton(
            not dir,
            text.dirChoice[0],
            style=wx.RB_GROUP,
            size=(width, -1)
        )
        rb6 = panel.RadioButton(dir, text.dirChoice[1])
        dirSizer.Add(rb5, 1)
        dirSizer.Add(rb6, 1)

        def OnRadioButton(event=None):
            flag = rb3.GetValue()
            mySizer.Show(dirSizer, flag, True)
            mySizer.Layout()
            if event:
                event.Skip()

        rb3.Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
        rb4.Bind(wx.EVT_RADIOBUTTON, OnRadioButton)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(staticText, 0, ACV)
        topSizer.Add(valueCtrl, 0, wx.LEFT, 10)
        if self.value is not None:
            stText = panel.StaticText(text.id_ix[self.value])
            id_ixCtrl = eg.SmartSpinIntCtrl(
                panel,
                -1,
                id_ix,
                min=0,
                max=999999
            )
            topSizer.Add(stText, 0, ACV | wx.LEFT, 40)
            topSizer.Add(id_ixCtrl, 0, wx.LEFT, 10)

        mySizer.Add(topSizer, 0, wx.TOP, 5)
        mySizer.Add(unitSizer, 0, wx.TOP, 12)
        mySizer.Add(posSizer, 0, wx.TOP, 12)
        mySizer.Add(dirSizer, 0, wx.TOP, 12)
        OnRadioButton()
        while panel.Affirmed():
            panel.SetResult(
                valueCtrl.GetValue(),
                rb2.GetValue(),
                rb4.GetValue(),
                rb6.GetValue(),
                id_ixCtrl.GetValue() if self.value is not None else 0
            )


# ===============================================================================

class SetCrossfade(eg.ActionBase):

    def __call__(self, cs=2):
        if self.plugin.isLive():
            cs = cs if isinstance(cs, int) else self.plugin.str2int(cs)
            wrkr = self.plugin.mpdworker
            wrFnc = wrkr.Func(wrkr.SetCrossfade, 5.0)
            wrFnc(cs)
            wrFnc = wrkr.Func(wrkr.GetCrossfade, 5.0)
            return wrFnc()

    def GetLabel(self, crossfade):
        return self.text.label_tree + str(int(crossfade))

    def Configure(self, crossfade=2):
        panel = eg.ConfigPanel(self)
        csCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            crossfade,
            min=0,
            max=1000
        )
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, -1, self.text.label_conf)
        sizer.Add(label, 0, ACV)
        sizer.Add(csCtrl, 0, wx.LEFT, 5)
        panel.sizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(csCtrl.GetValue())

    class text:
        label_tree = "Set crossfade "
        label_conf = "Crossfade [s]:"
        label_conf = "Song ID:"


# ===============================================================================

class SetReplayGain(eg.ActionBase):

    def __call__(self, val="off"):
        if self.plugin.isLive():
            wrkr = self.plugin.mpdworker
            wrFnc = wrkr.Func(getattr(wrkr, self.__class__.__name__), 5.0)
            return wrFnc(val)

    def GetLabel(self, val):
        return self.text.label_tree[self.value] + val

    def Configure(self, val="off"):
        panel = eg.ConfigPanel(self)
        choiceCtrl = wx.Choice(
            panel,
            -1,
            choices=("off", "track", "album", "auto")
        )
        choiceCtrl.SetStringSelection(val)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, -1, self.text.label_conf)
        sizer.Add(label, 0, ACV)
        sizer.Add(choiceCtrl, 0, wx.LEFT, 5)
        panel.sizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(choiceCtrl.GetStringSelection())

    class text:
        label_tree = "Set replay gain mode: "
        label_conf = "Replay gain mode:"
    # ===============================================================================


class SetVolume(eg.ActionBase):

    def __call__(self, vol=50):
        if self.plugin.isLive():
            vol = vol if isinstance(vol, int) else self.plugin.str2int(vol)
            wrkr = self.plugin.mpdworker
            wrFnc = wrkr.Func(wrkr.SetVolume, 5.0)
            wrFnc(vol)
            wrFnc = wrkr.Func(wrkr.GetVolume, 5.0)
            return wrFnc()

    def GetLabel(self, volume):
        return self.text.label_tree + str(int(volume)) + "%"

    def Configure(self, volume=50):
        panel = eg.ConfigPanel(self)
        volumeCtrl = eg.SmartSpinIntCtrl(
            panel,
            -1,
            volume,
            min=0,
            max=100
        )
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, -1, self.text.label_conf)
        sizer.Add(label, 0, ACV)
        sizer.Add(volumeCtrl, 0, wx.LEFT, 5)
        panel.sizer.Add(sizer, 0, wx.ALL | wx.EXPAND, 10)
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())

    class text:
        label_tree = "Set volume "
        label_conf = "Volume level [%]:"


# ===============================================================================

ACTIONS = (
    (eg.ActionGroup, 'Querying', 'Querying', 'Querying.', (
        (
            Command,
            "GetStatus",
            "Get MPD status",
            "Reports the current status of the player and the volume level.",
            None
        ),
        (
            Command,
            "GetStats",
            "Get MPD statistics",
            "Reports MPD statistics.",
            None
        ),
        (
            Command,
            "GetVersion",
            "Get MPD version",
            "Report version of MPD.",
            None
        ),
        (
            Command,
            "GetSong",
            "Get current song",
            "Returns current song.",
            None
        ),
        (
            Command,
            "GetRepeat",
            "Get repeat mode",
            "Returns current repeat mode.",
            None
        ),
        (
            Command,
            "GetRandom",
            "Get random mode",
            "Returns current random mode.",
            None
        ),
        (
            Command,
            "GetOutputs",
            "Get outputs",
            "Shows information about all outputs.",
            None
        ),
        (
            Command,
            "GetConsume",
            "Get consume mode",
            "Returns current consume mode.",
            None
        ),
        (
            Command,
            "GetSingle",
            "Get single mode",
            "Returns current single mode.",
            None
        ),
        (
            Command,
            "GetVolume",
            "Get volume",
            "Returns current volume.",
            None
        ),
        (
            Command,
            "GetCrossfade",
            "Get crossfade",
            "Returns current crossfade.",
            None
        ),
        (
            Command,
            "GetReplayGain",
            "Get replay gain mode",
            "Returns current replay gain mode.",
            None
        ),
        (
            Command,
            "GetPlaylist",
            "Get current playlist",
            "Displays the current playlist.",
            None
        ),
        (
            Command4,
            "Listplaylist",
            "Get playlist [name]",
            "Lists the songs in the playlist.",
            1
        ),
        (
            Command4,
            "Listplaylistinfo",
            "Get playlist info [name]",
            "Lists the songs with metadata in the playlist.",
            2
        ),
        (
            Command,
            "GetPlaylists",
            "Get list of the playlists",
            "Prints a list of the playlist directory.",
            None
        ),
    )),
    (eg.ActionGroup, 'PlaybackOptions', 'Playback options', 'Playback options.', (
        (
            ChangeVolume,
            "VolumeUp",
            "Volume up ",
            "Increase volume by x%.",
            0
        ),
        (
            ChangeVolume,
            "VolumeDown",
            "Volume down ",
            "Decrease volume by x%.",
            1
        ),
        (
            SetVolume,
            "SetVolume",
            "Set volume",
            "Sets the volume to a percentage (%) from 0 to 100.",
            None
        ),

        (
            SetCrossfade,
            "ChangeCrossfade",
            "Set crossfade [s]",
            "Sets crossfade [s].",
            None
        ),
        (
            Command2,
            "Repeat_On",
            "Set repeat mode ON",
            "Sets the repeat mode ON.",
            1
        ),
        (
            Command2,
            "Repeat_Off",
            "Set repeat mode OFF",
            "Sets the repeat mode OFF.",
            0
        ),
        (
            Command2,
            "Repeat_Toggle",
            "Toggle repeat mode",
            "Toggles repeat mode.",
            None
        ),
        (
            Command2,
            "Random_On",
            "Set random mode ON",
            "Sets the random mode ON.",
            1
        ),
        (
            Command2,
            "Random_Off",
            "Set random mode OFF",
            "Sets the random mode OFF.",
            0
        ),
        (
            Command2,
            "Random_Toggle",
            "Toggle random mode",
            "Toggles random mode.",
            None
        ),

        (
            Command2,
            "Consume_On",
            "Set consume mode ON",
            "Sets the consume mode ON.",
            1
        ),
        (
            Command2,
            "Consume_Off",
            "Set consume mode OFF",
            "Sets the consume mode OFF.",
            0
        ),
        (
            Command2,
            "Consume_Toggle",
            "Toggle consume mode",
            "Toggles consume mode.",
            None
        ),
        (
            Command2,
            "Single_On",
            "Set single mode ON",
            "Sets the single mode ON.",
            1
        ),
        (
            Command2,
            "Single_Off",
            "Set single mode OFF",
            "Sets the single mode OFF.",
            0
        ),
        (
            Command2,
            "Single_Toggle",
            "Toggle single mode",
            "Toggles single mode.",
            None
        ),
        (
            SetReplayGain,
            "SetReplayGain",
            "Set replay gain mode",
            "Sets the replay gain mode. One of off, track, album, auto.",
            None
        ),
    )),
    (eg.ActionGroup, 'ControllingPlayback', 'Controlling playback', 'Controlling playback.', (
        (
            Command,
            "Next",
            "Play next song",
            "Plays the next song in the current playlist.",
            None
        ),
        (
            Command,
            "Previous",
            "Play previous song",
            "Plays the previous song in the current playlist.",
            None
        ),
        (
            Command2,
            "Pause_on",
            "Pause",
            "Pauses the currently playing song.",
            1
        ),
        (
            Command2,
            "Pause_Off",
            "Play",
            "Starts playing at current playlist position.",
            0
        ),
        (
            Command2,
            "Pause_Toggle",
            "Toggle play/pause",
            "Toggles Play/Pause, plays if stopped",
            None
        ),
        (
            Command3,
            "Play",
            u"Play [sequential number]",
            u"Begins playing at current playlist by specified sequential number (numbering sequences starting at 1).",
            0
        ),
        (
            Command3,
            "PlayId",
            u"Play [song ID]",
            u"Begins playing at current playlist by specified song ID.",
            1
        ),
        (
            Command,
            "Stop_",
            "Stop",
            "Stops the currently playing playlist.",
            None
        ),
        (
            Seek,
            "Seek",
            "Seek",
            "Seeks to the position (in seconds or %) within the currently playing song.",
            None
        ),
        (
            Seek,
            "SeekIndex",
            "Seek song by sequential number",
            "Seeks to the position (in seconds or %) within song with specified sequential number.",
            0
        ),
        (
            Seek,
            "SeekId",
            "Seek song by song ID",
            "Seeks to the position (in seconds or %) within song with specified song ID.",
            1
        ),
    )),
    (eg.ActionGroup, 'CurrentPlaylist', 'The current playlist', 'The current playlist.', (
        (
            Command3,
            "Delete",
            "Delete [sequential number]",
            "Deletes a song from the playlist (by specified sequential number).",
            2
        ),
        (
            Command3,
            "DeleteId",
            "Delete [song ID]",
            "Deletes a song from the playlist (by specified song ID).",
            3
        ),
        (
            Command,
            "Clear",
            "Clear",
            "Clears the current playlist.",
            None
        ),
        (
            Command,
            "Shuffle",
            "Shuffle",
            "Shuffles the current playlist.",
            None
        ),
        (
            Command5,
            "AddUri",
            "Add URI to current queue",
            "Adds the URI to the current queue (directories add recursively). URI can also be a single file.",
            None
        ),
        (
            AddId,
            "AddId",
            "Add URI to specified position",
            "Adds a song to the current queue (non-recursive) and returns the song id.",
            None
        ),
    )),
    (eg.ActionGroup, 'StoredPlaylists', 'Stored playlists', 'Stored playlists.', (
        (
            Command4,
            "Load",
            "Load playlist",
            "Loads the playlist into the current queue.",
            0
        ),
        (
            Command4,
            "Save",
            "Save playlist",
            "Saves the current playlist to the playlist directory.",
            3
        ),
        (
            Command4,
            "ClearPlaylist",
            "Clear playlist",
            "Clears the playlist.",
            4
        ),
        (
            Command4,
            "RemovePlaylist",
            "Remove playlist",
            "Removes the playlist from the playlist directory.",
            5
        ),
        (
            Command4,
            "AddCurrentUri",
            "Add current URI to playlist",
            "Adds current URI to the playlist.",
            6
        ),
        (
            AddUri2PL,
            "AddUri2PL",
            "Add URI to playlist",
            "Adds URI to the playlist.",
            None
        ),
    )),
    (eg.ActionGroup, 'MusicDatabase', 'The music database', 'The music database.', (
        (
            Command5,
            "Update",
            "Update the music database",
            "Updates the music database: find new files, remove deleted files, update modified files.",
            None
        ),
        (
            Command5,
            "Rescan",
            "Rescan the music database",
            "Same as update , but also rescans unmodified files.",
            None
        ),
    )),
    (eg.ActionGroup, 'AudioOutputDevices', 'Audio output devices', 'Audio output devices.', (
        (
            Command3,
            "DisableOutput",
            "Turn an output off",
            "Turns an output off.",
            4
        ),
        (
            Command3,
            "EnableOutput",
            "Turn an output on",
            "Turns an output on.",
            5
        ),
        (
            Command3,
            "ToggleOutput",
            "Toggle output",
            "Turns an output on or off, depending on the current state.",
            6
        ),
    )),
)
# ===============================================================================

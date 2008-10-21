version="0.1.10"

# Plugins/MediaMonkey/__init__.py
#
# Copyright (C)  2007 Pako  <lubos.ruckl@quick.cz>
#
# This file is part of EventGhost.
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
#Last change: 2008-10-21 22:27

eg.RegisterPlugin(
    name = "MediaMonkey",
    author = "Pako",
    version = version,
    kind = "program",
    createMacrosOnAdd = True,
    description = (
        'Adds support functions to control '
        '<a href="http://www.MediaMonkey.com/">MediaMonkey</a>. \n\n<P>'
        '<BR><B>Note:</B><BR>'
        'To make functional event triggering from MediaMonkey, you must install'
        '<BR>file "EventGhost.vbs" to MediaMonkey/Scripts/Auto folder.'
    ),
    url = "http://www.eventghost.org/forum/viewtopic.php?t=563",
    icon = (
        "R0lGODlhEAAQAPcAADQyNLyaTHRmRJSWlPzGNFxOPGxqbFROVKSGRJyWfOzSlOTCdGRmZ"
        "HReRERCPIRyTNy2dIyCbPzSZMSylExOTFxaXOTe5HxyVOS2ROzCTFxWPIx+ZKSajDw6PP"
        "zinExGTPTSfHR2dFRWVKSOVLyibGxiTExKRISKjNy+lIx6VPzOVKyaZLSqnFRSRJyGTNT"
        "GrOzKfERCRJR6RNS2fPzWdGRiXIx2VMyqXGxWPEQ+RDw2PMSiRIRuVJyenPzKRHRydFRS"
        "VLSedNS6hHx2ZGRaTIR2TKSSdPzWbMS6pFxeXPzy1IRyVPzKTGRWPKSSXLymhEQ+PPzqt"
        "PzahHx+fFxWVLymfHRiTJyShMzCpPzSXFxSRKSKTOzWtExGRNy2fMSqZH4HhAAAAAAAAM"
        "AAAAAIEgAACgAAEwAAAP8JhP8AAP8AAP8AAP8yAP8HAP+RAP98AACreAAGAACRTQB8AAA"
        "wBADqAAASAAAAAADQ4gA8BBUlAABbAGAIYOlAnhI4gAAAfNJ4IOYARYEAH3wAAMhNAMUA"
        "ABwAAAAAAErwB+PqAIESAHwAAKBGAHfQAFAmAABbAMgIAMVAQAE4HwAAAGsFAAAAAAAAA"
        "AAAAJxuAOi9ABIAAAAAAAB4AADqAAASAAAAAAiFAPwrABKDAAB8ABgAaO4AnpAAgHwAfH"
        "AA/wUA/5EA/3wA//8AYP8Anv8AgP8AfG0pKgW3AJGSAHx8AEogKvRFAIAfAHwAAAA0WAB"
        "k8RWDEgB8AAD//wD//wD//wD//8gAAMUAABwAAAAAAABcpAHq6wASEgAAAAA09gBkOACD"
        "TAB8AFcIhPT864ASEnwAAIgYd+ruEBKQTwB8AMgAuMW36xySEgB8AKD/NAD/ZAD/gwD/f"
        "B8gWgBF7AAfEgAAABE01ABk/wCD/wB8fwSgMADr7AASEgAAAAPnIABkRQCDHwB8AACINA"
        "BkZACDgwB8fAABIAAARQAAHwAAAAQxbgAAvQAwAAAAAAMBAAAAAAAAAAAAAAAajQAA4gA"
        "ARwAAACH5BAEAABYALAAAAAAQABAABwjtAC0IFNjDgMEfPQYqtDCAAY8gECCQ4FFjwMIQ"
        "ViBIOcLxiAcUVgwMPGFlAY0jErJIkBBFCRcrJwQyIIEyywoDI2AoUfLiiQgLIT58OZIlA"
        "BAKQK5wqFABSJcpXSLQkKACQYyrMRzEeJDCRJcYQ1Ay2dFFqwMtGFReceAASokiBWIAuN"
        "olg48sRy7o6NJCRwetFBx0IEKACd4UHX7YUIAFCYUOOhwU8KFCgpQlIk2gUMLir2AZlY9"
        "AiCGzxAQAHbZsASBAwhEYApIMNFHCyIwbAHSMkAKhBJSFSRwsqYKjQJUHUH4ulAmgOQAG"
        "CwMCADs="
    ),
)



from win32com.client import Dispatch
from eg.WinApi.Utils import CloseHwnd
import time
import datetime
import wx.lib.masked as masked
from os.path import isfile


#====================================================================
class Text:

    errorNoWindow = "Couldn't find MediaMonkey window"
    errorConnect = "MediaMonkey is not running or connected"
    mainGrpName = "Main control of MediaMonkey"
    mainGrpDescr = "Here you find actions for main control of MediaMonkey."
    levelGrpName = "Another control of MediaMonkey"
    levelGrpDescr = (
        "Here you find further actions for control of MediaMonkey"
        " (volume, balance, seek)."
    )
    extrGrpName = "Writing to database MM"
    extrGrpDescr = (
        "Here is action for writing some one parameters to database MediaMonkey."
    )
    infoGrpName = "Information retrieval"
    infoGrpDescr = (
        "Here you find actions for information retrieval"
        " from MediaMonkey."
    )
#====================================================================
class MediaMonkey(eg.PluginClass):
    text = Text

    def __init__(self):
        group = self.AddGroup(
            self.text.mainGrpName,
            self.text.mainGrpDescr
        )
        group.AddAction(Start)
        group.AddAction(Exit)
        group.AddAction(Play)
        group.AddAction(TogglePlay)
        group.AddAction(DiscretePause)
        group.AddAction(Stop)
        group.AddAction(Next)
        group.AddAction(Previous)
        group.AddAction(LoadPlaylist)
        group.AddAction(AddCurrentSongToPlaylist)
        group.AddAction(RemoveCurrentSongFromPlaylist)
        group.AddAction(RemoveCurrentSongFromNowPlaying)
        group.AddAction(LoadPlaylistByFilter)
        group.AddAction(Jukebox)

        group = self.AddGroup(
            self.text.levelGrpName,
            self.text.levelGrpDescr
        )
        group.AddAction(ToggleMute)
        group.AddAction(SetVolume)
        group.AddAction(VolumeUp)
        group.AddAction(VolumeDown)
        group.AddAction(SetBalance)
        group.AddAction(SetRepeat)
        group.AddAction(SetShuffle)
        group.AddAction(SetAutoDJ)
        group.AddAction(SetCrossfade)
        group.AddAction(BalanceRight)
        group.AddAction(BalanceLeft)
        group.AddAction(Seek)

        group = self.AddGroup(
            self.text.extrGrpName,
            self.text.extrGrpDescr
        )
        group.AddAction(WritingToMM)

        group = self.AddGroup(
            self.text.infoGrpName,
            self.text.infoGrpDescr
        )
        group.AddAction(GetVolume)
        group.AddAction(GetStatus)
        group.AddAction(GetBalance)
        group.AddAction(GetRepeat)
        group.AddAction(GetShuffle)
        group.AddAction(GetAutoDJ)
        group.AddAction(GetCrossfade)
        group.AddAction(GetPosition)
        group.AddAction(GetBasicSongInfo)
        group.AddAction(GetBasicSongInfoNextTrack)
        group.AddAction(GetDetailSongInfo)
        group.AddAction(GetClassificationInfo)
        group.AddAction(GetTechnicalSongInfo)
        group.AddAction(GetUniversal)

    def __start__(self):
        self.MM=None
        self.volume=None
        self.muted=False

    def __stop__(self):
        try:
            if self.MM:
                del self.MM
        except:
            pass

    def DispMM(self):
        if self.MM is None:
            try:
                self.MM = Dispatch("SongsDB.SDBApplication")
                self.MM.ShutdownAfterDisconnect=False
            except:
                raise self.Exceptions.ProgramNotRunning
        return self.MM
#====================================================================
#====================================================================
class Start(eg.ActionClass):
    name = "Start/Connect MediaMonkey"
    description = "Start or Connect MediaMonkey through COM-API."
    class text:
        error = "Couldn't connect to MediaMonkey"

    def __call__(self):
        self.plugin.MM=Dispatch("SongsDB.SDBApplication")
        self.plugin.MM.ShutdownAfterDisconnect=False

#====================================================================
MyWindowMatcher = eg.WindowMatcher(
    u'MediaMonkey.exe',
    u'{*}MediaMonkey{*}',
    u'TFMainWindow',
    None,
    None,
    1,
    True,
    0,
    0
)

class Exit(eg.ActionClass):
    name = "Exit/Disconnect MediaMonkey"
    description = "Exit or Disconnect MediaMonkey."
    class text:
        choice_label="Close MediaMonkey too"

    def __call__(self,choice):
        try:
            if self.plugin.MM:
                del self.plugin.MM
        except:
            pass
        self.plugin.MM=None
        hwnds = MyWindowMatcher()
        if choice:
            if hwnds:
                CloseHwnd(hwnds[0])
            else:
                raise self.Exceptions.ProgramNotRunning

    def Configure(self, choice=False):
        panel = eg.ConfigPanel(self)
        choiceCtrl = wx.CheckBox(panel, -1, self.text.choice_label)
        choiceCtrl.SetValue(choice)
        panel.AddCtrl(choiceCtrl)

        while panel.Affirmed():
            panel.SetResult(choiceCtrl.GetValue())
#====================================================================
class Play(eg.ActionClass):
    name = "Play"
    description = "Play."

    def __call__(self):
        self.plugin.DispMM().Player.Play()

#====================================================================
class TogglePlay(eg.ActionClass):
    name = "Toggle Play"
    description = "Toggles between play and pause of MediaMonkey."

    def __call__(self):
        if  not self.plugin.DispMM().Player.isPlaying:
            # Play
            return self.plugin.DispMM().Player.Play()
        else:
            # Toggle Play/Pause
            return self.plugin.DispMM().Player.Pause()

#====================================================================
class DiscretePause(eg.ActionClass):
    name = "Discrete Pause"
    description = (
        "Pauses MediaMonkey if it is playing, but won't do anything if "
        "MediaMonkey is already paused."
    )

    def __call__(self):
        if self.plugin.DispMM().Player.isPlaying:
            if (not self.plugin.DispMM().Player.isPaused):
                return self.plugin.DispMM().Player.Pause()

#====================================================================
class Stop(eg.ActionClass):
    name = "Stop"
    description = "Simulate a press on the stop button."

    def __call__(self):
        return self.plugin.DispMM().Player.Stop()


#====================================================================
class Next(eg.ActionClass):
    name = "Next"
    description = "Next."

    def __call__(self):
        self.plugin.DispMM().Player.Next()

#====================================================================
class Previous(eg.ActionClass):
    name = "Previous"
    description = "Previous."

    def __call__(self):
        self.plugin.DispMM().Player.Previous()


#====================================================================
class ToggleMute(eg.ActionClass):
    name = "Toggle Mute"
    description = "Toggle Mute."

    def __call__(self):
        if not self.plugin.muted:
            self.plugin.volume=self.plugin.DispMM().Player.Volume
            self.plugin.DispMM().Player.Volume=0
            self.plugin.muted=True
        else:
            setattr(self.plugin.DispMM().Player,"Volume",self.plugin.volume)
            self.plugin.muted=False


#====================================================================
class SetVolume(eg.ActionClass):
    name = "Set Volume Level"
    description = "Sets the volume to a percentage (%)."
    class text:
        label_tree="Set volume "
        label_conf="Volume Level:"
    def __call__(self, volume):
        setattr(self.plugin.DispMM().Player,"Volume",volume/100)
        if volume!=0:
            self.plugin.muted=False

    def GetLabel(self, volume):
        return self.text.label_tree+str(int(volume))+"%"

    def Configure(self, volume=100.0):
        panel = eg.ConfigPanel(self)
        volumeCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            volume,
            max=100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(volumeCtrl)
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())


#====================================================================
class VolumeUp(eg.ActionClass):
    name = "Volume up "
    description = "Volume up x%."
    class text:
        label_tree="Volume up "
        label_conf="Volume step:"

    def __call__(self, step):
        if step>0:
            self.plugin.muted=False
            volume=self.plugin.DispMM().Player.Volume
            if volume<1:
                if volume>(1-step/100):
                    volume=1
                else:
                    volume+=step/100
                setattr(self.plugin.DispMM().Player,"Volume",volume)

    def GetLabel(self, step):
        return self.text.label_tree+str(int(step))+"%"

    def Configure(self, step=10.0):
        panel = eg.ConfigPanel(self)
        volumeCtrl = eg.SpinNumCtrl(panel, -1, step, max=100.0,fractionWidth=1)
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(volumeCtrl)
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())

#====================================================================
class VolumeDown(eg.ActionClass):
    name = "Volume down "
    description = "Volume down x%."
    class text:
        label_tree="Volume down "
        label_conf="Volume step:"
    def __call__(self, step):
        volume=self.plugin.DispMM().Player.Volume
        if volume>0:
            if volume<abs(step)/100:
                volume=0
            else:
                volume+=step/100
            setattr(self.plugin.DispMM().Player,"Volume",volume)

    def GetLabel(self, step):
        return self.text.label_tree+str(abs(int(step)))+"%"

    def Configure(self, step=-10.0):
        panel = eg.ConfigPanel(self)
        volumeCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            step,
            max=0.0,
            min=-100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(volumeCtrl)
        while panel.Affirmed():
            panel.SetResult(volumeCtrl.GetValue())

#====================================================================
class SetBalance(eg.ActionClass):
    name = "Set Balance"
    description = "Sets the balance."
    class text:
        label_tree="Set balance "
        label_conf = "Balance (-100 ... 100):"
    def __call__(self, balance):
        setattr(self.plugin.DispMM().Player,"Panning",balance/100)

    def GetLabel(self, balance):
        return self.text.label_tree+str(int(balance))+"%"

    def Configure(self, balance=0.0):
        panel = eg.ConfigPanel(self)
        balanceCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            balance,
            max=100.0,
            min=-100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(balanceCtrl)
        while panel.Affirmed():
            panel.SetResult(balanceCtrl.GetValue())

#====================================================================
class SetShuffle(eg.ActionClass):
    name = "Set Shuffle tracks"
    description = "Sets the shuffle tracks."
    class text:
        radiobox = "Set Shuffle tracks to state ..."
        ShuffleON = "ON"
        ShuffleOFF = "OFF"
    def __call__(self, switch):
        length=self.plugin.DispMM().Player.CurrentSongLength
        pos=self.plugin.DispMM().Player.PlaybackTime
        if switch==0: #
            self.plugin.DispMM().Player.isShuffle=True
        else: #
            self.plugin.DispMM().Player.isShuffle=False

    def GetLabel(self, switch):
        return "Set Shuffle tracks "+("ON" if switch==0 else "OFF")

    def Configure(self, switch=0):
        text=Text
        panel = eg.ConfigPanel(self)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            choices=[self.text.ShuffleON, self.text.ShuffleOFF],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(switch)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(radioBox.GetSelection(),)

#====================================================================
class SetRepeat(eg.ActionClass):
    name = "Set Continous playback"
    description = "Sets the continous playback."
    class text:
        radiobox = "Set Continous playback to state ..."
        RepeatON = "ON"
        RepeatOFF = "OFF"
    def __call__(self, switch):
        length=self.plugin.DispMM().Player.CurrentSongLength
        pos=self.plugin.DispMM().Player.PlaybackTime
        if switch==0: #
            self.plugin.DispMM().Player.isRepeat=True
        else: #
            self.plugin.DispMM().Player.isRepeat=False

    def GetLabel(self, switch):
        return "Set Continous playback "+("ON" if switch==0 else "OFF")

    def Configure(self, switch=0):
        text=Text
        panel = eg.ConfigPanel(self)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            choices=[self.text.RepeatON, self.text.RepeatOFF],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(switch)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(radioBox.GetSelection(),)
#====================================================================
class SetAutoDJ(eg.ActionClass):
    name = "Set AutoDJ"
    description = "Sets the AutoDJ."
    class text:
        radiobox = "Set AutoDJ to state ..."
        AutoDJON = "ON"
        AutoDJOFF = "OFF"
    def __call__(self, switch):
        length=self.plugin.DispMM().Player.CurrentSongLength
        pos=self.plugin.DispMM().Player.PlaybackTime
        if switch==0: #
            self.plugin.DispMM().Player.isAutoDJ=True
        else: #
            self.plugin.DispMM().Player.isAutoDJ=False

    def GetLabel(self, switch):
        return "Set AutoDJ "+("ON" if switch==0 else "OFF")

    def Configure(self, switch=0):
        text=Text
        panel = eg.ConfigPanel(self)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            choices=[self.text.AutoDJON, self.text.AutoDJOFF],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(switch)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(radioBox.GetSelection(),)
#====================================================================
class SetCrossfade(eg.ActionClass):
    name = "Set Crossfade"
    description = "Sets the crossfade."
    class text:
        radiobox = "Set Crossfade to state ..."
        CrossfadeON = "ON"
        CrossfadeOFF = "OFF"
    def __call__(self, switch):
        length=self.plugin.DispMM().Player.CurrentSongLength
        pos=self.plugin.DispMM().Player.PlaybackTime
        if switch==0: #
            self.plugin.DispMM().Player.isCrossfade=True
        else: #
            self.plugin.DispMM().Player.isCrossfade=False

    def GetLabel(self, switch):
        return "Set Crossfade "+("ON" if switch==0 else "OFF")

    def Configure(self, switch=0):
        text=Text
        panel = eg.ConfigPanel(self)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            choices=[self.text.CrossfadeON, self.text.CrossfadeOFF],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(switch)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(radioBox.GetSelection(),)

#====================================================================
class BalanceRight(eg.ActionClass):
    name = "Balance Right x%"
    description = "Balance Right x%."
    class text:
        label_tree="Balance right "
        label_conf = "Balance step:"
    def __call__(self, step):
        if step>0:
            balance=self.plugin.DispMM().Player.Panning
            if balance<1:
                if balance>(1-step/100):
                    balance=1
                else:
                    balance+=step/100
                setattr(self.plugin.DispMM().Player,"Panning",balance)

    def GetLabel(self, step):
        return self.text.label_tree+str(int(step))+"%"

    def Configure(self, step=10.0):
        panel = eg.ConfigPanel(self)
        balanceCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            step,
            max=100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(balanceCtrl)
        while panel.Affirmed():
            panel.SetResult(balanceCtrl.GetValue())

#====================================================================
class BalanceLeft(eg.ActionClass):
    name = "Balance Left x%"
    description = "Balance Left x%."
    class text:
        label_tree="Balance left "
        label_conf = "Balance step:"
    def __call__(self, step):
        if step>0:
            balance=self.plugin.DispMM().Player.Panning
            if balance>-1:
                if balance<(step/100-1):
                    balance=-1
                else:
                    balance+=-step/100
                setattr(self.plugin.DispMM().Player,"Panning",balance)

    def GetLabel(self, step):
        return self.text.label_tree+str(int(step))+"%"

    def Configure(self, step=10.0):
        panel = eg.ConfigPanel(self)
        balanceCtrl = eg.SpinNumCtrl(
            panel,
            -1,
            step,
            max=100.0,
            fractionWidth=1
        )
        panel.AddLabel(self.text.label_conf)
        panel.AddCtrl(balanceCtrl)
        while panel.Affirmed():
            panel.SetResult(balanceCtrl.GetValue())

#====================================================================
class Seek(eg.ActionClass):
    name = "Seek Forward or Backward x%"
    description = "Seek Forward or Backward x%."
    class text:
        radiobox = "Seek direction"
        btnForward = "Forward"
        btnBackward = "Backward"
        label = "Seek step (%):"
        tree_lab1 = "Seek "
        tree_lab2 = "backward"
        tree_lab3 = "forward"
    def __call__(self, step, direction):
        length=self.plugin.DispMM().Player.CurrentSongLength
        pos=self.plugin.DispMM().Player.PlaybackTime
        if direction: #Backward
            if pos>length*step/100:
                setattr(self.plugin.DispMM().\
                    Player,"PlaybackTime",pos-length*step/100)
            else:
                self.plugin.DispMM().Player.PlaybackTime=0
        else:         #Forward
            if pos<length-length*step/100:
                setattr(self.plugin.DispMM().\
                    Player,"PlaybackTime",pos+length*step/100)
            else:
                setattr(self.plugin.DispMM().Player,"PlaybackTime",length-500)

    def GetLabel(self, step, direction):
        return self.text.tree_lab1\
            +(self.text.tree_lab2 if direction else self.text.tree_lab3)\
            +" "+str(int(step))+"%"

    def Configure(self, step=10.0, direction=0):
        text=Text
        panel = eg.ConfigPanel(self)
        seekCtrl = eg.SpinNumCtrl(panel, -1, step, max=100.0, fractionWidth=1)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            choices=[self.text.btnForward, self.text.btnBackward],
            style=wx.RA_SPECIFY_ROWS
        )
        panel.AddLabel(self.text.label)
        panel.AddCtrl(seekCtrl)
        radioBox.SetSelection(direction)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(seekCtrl.GetValue(),radioBox.GetSelection())


#====================================================================
class GetVolume(eg.ActionClass):
    name = "Get Volume"
    description = "Get Volume."
    def __call__(self):
        return 100*self.plugin.DispMM().Player.Volume


#====================================================================
class GetBalance(eg.ActionClass):
    name = "Get Balance"
    description = "Get Balance."
    def __call__(self):
        return 100*self.plugin.DispMM().Player.Panning

#====================================================================
class GetStatus(eg.ActionClass):
    name = "Get Status"
    description = "Get Status (return string Playing, Paused or Stoped)."
    def __call__(self):
        playing=self.plugin.DispMM().Player.isPlaying
        paused=self.plugin.DispMM().Player.isPaused
        if not playing:
            return "Stoped"
        elif playing and not paused:
            return "Playing"
        elif playing and paused:
            return "Paused"

#====================================================================
class GetRepeat(eg.ActionClass):
    name = "Get Repeat"
    description = "Get Repeat Status."
    def __call__(self):
        return self.plugin.DispMM().Player.isRepeat

#====================================================================
class GetShuffle(eg.ActionClass):
    name = "Get Shuffle"
    description = "Get Shuffle Status."
    def __call__(self):
        return self.plugin.DispMM().Player.isShuffle


#====================================================================
class GetAutoDJ(eg.ActionClass):
    name = "Get AutoDJ"
    description = "Get AutoDJ Status."
    def __call__(self):
        return self.plugin.DispMM().Player.isAutoDJ


#====================================================================
class GetCrossfade(eg.ActionClass):
    name = "Get Crossfade"
    description = "Get Crossfade Status."
    def __call__(self):
        return self.plugin.DispMM().Player.isCrossfade


#====================================================================
class GetPosition(eg.ActionClass):
    name = "Get Position in ms"
    description = "Get Position in ms."
    def __call__(self):
        return self.plugin.DispMM().Player.PlaybackTime

#====================================================================
class GetBasicSongInfo(eg.ActionClass):
    name = "Get basic song info"
    description = "Get basic song info."
    class text:
        filepath = "File path"
        filename = "File name"
        tracktitle = "Track title"
        artist = "Artist"
        genre = "Genre"
        rating = "Rating"
        album = "Album"
        disc = "Disc #"
        track = "Track #"
        albumartist = "Album artist"
        year = "Year"
        grouping = "Grouping"
        origDate = "Original year"
        composer = "Composer"
        conductor = "Conductor"
        comment = "Comment"
        seqNum = 'Sequence number in "Now playing" window'

    def __call__(self,arrayInfo):
        player=self.plugin.DispMM().Player
        path=player.CurrentSong.Path
        indx=path.rfind("\\")+1
        result=path[:indx]+"," if arrayInfo[0] else ""
        result+=path[indx:]+"," if arrayInfo[1] else ""
        listPropert=(
            "Title",
            "ArtistName",
            "Genre",
            "Rating",
            "AlbumName",
            "DiscNumber",
            "TrackOrder",
            "AlbumArtistName",
            "Year",
            "Grouping",
            "OriginalYear",
            "MusicComposer",
            "Conductor",
            "Comment"
        )
        listNum=(
            False,
            False,
            False,
            True,
            False,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            False,
            False
        )
        for propert,cond,numeric in zip(listPropert,arrayInfo[2:],listNum):
            if numeric:
                result+=str(getattr(player.CurrentSong,propert))\
                    +"," if cond else ""
            else:
                result+=getattr(player.CurrentSong,propert)\
                    +"," if cond else ""
        if arrayInfo[16]:
            result+=str(player.CurrentSongIndex+1)+","

        return result[:-1]


    def GetLabel(self, arrayInfo):
        result=""
        for condition in arrayInfo:
            result+="X" if condition else "_"
        return result

    def Configure(
        self,
        arrayInfo=[False]*17
    ):
        text=self.text
        panel = eg.ConfigPanel(self)
        filepathCtrl = wx.CheckBox(panel, -1, self.text.filepath)
        filepathCtrl.SetValue(arrayInfo[0])
        filenameCtrl = wx.CheckBox(panel, -1, self.text.filename)
        filenameCtrl.SetValue(arrayInfo[1])
        tracktitleCtrl = wx.CheckBox(panel, -1, self.text.tracktitle)
        tracktitleCtrl.SetValue(arrayInfo[2])
        artistCtrl = wx.CheckBox(panel, -1, self.text.artist)
        artistCtrl.SetValue(arrayInfo[3])
        genreCtrl = wx.CheckBox(panel, -1, self.text.genre)
        genreCtrl.SetValue(arrayInfo[4])
        ratingCtrl = wx.CheckBox(panel, -1, self.text.rating)
        ratingCtrl.SetValue(arrayInfo[5])
        albumCtrl = wx.CheckBox(panel, -1, self.text.album)
        albumCtrl.SetValue(arrayInfo[6])
        discCtrl = wx.CheckBox(panel, -1, self.text.disc)
        discCtrl.SetValue(arrayInfo[7])
        trackCtrl = wx.CheckBox(panel, -1, self.text.track)
        trackCtrl.SetValue(arrayInfo[8])
        albumartistCtrl = wx.CheckBox(panel, -1, self.text.albumartist)
        albumartistCtrl.SetValue(arrayInfo[9])
        yearCtrl = wx.CheckBox(panel, -1, self.text.year)
        yearCtrl.SetValue(arrayInfo[10])
        groupingCtrl = wx.CheckBox(panel, -1, self.text.grouping)
        groupingCtrl.SetValue(arrayInfo[11])
        origDateCtrl = wx.CheckBox(panel, -1, self.text.origDate)
        origDateCtrl.SetValue(arrayInfo[12])
        composerCtrl = wx.CheckBox(panel, -1, self.text.composer)
        composerCtrl.SetValue(arrayInfo[13])
        conductorCtrl = wx.CheckBox(panel, -1, self.text.conductor)
        conductorCtrl.SetValue(arrayInfo[14])
        commentCtrl = wx.CheckBox(panel, -1, self.text.comment)
        commentCtrl.SetValue(arrayInfo[15])
        seqNumCtrl = wx.CheckBox(panel, -1, self.text.seqNum)
        seqNumCtrl.SetValue(arrayInfo[16])

        mainSizer=wx.FlexGridSizer(2,2)
        leftSizer=wx.BoxSizer(wx.VERTICAL)
        rightSizer=wx.BoxSizer(wx.VERTICAL)

        leftSizer.Add(tracktitleCtrl,0)
        leftSizer.Add(artistCtrl,0,wx.TOP,10)
        leftSizer.Add(genreCtrl,0,wx.TOP,10)
        leftSizer.Add(albumCtrl,0,wx.TOP,10)
        leftSizer.Add(albumartistCtrl,0,wx.TOP,10)
        leftSizer.Add(groupingCtrl,0,wx.TOP,10)
        leftSizer.Add(composerCtrl,0,wx.TOP,10)
        leftSizer.Add(conductorCtrl,0,wx.TOP,10)
        leftSizer.Add(seqNumCtrl,0,wx.TOP,10)
        rightSizer.Add(filepathCtrl,0)
        rightSizer.Add(filenameCtrl,0,wx.TOP,10)
        rightSizer.Add(yearCtrl,0,wx.TOP,10)
        rightSizer.Add(origDateCtrl,0,wx.TOP,10)
        rightSizer.Add(discCtrl,0,wx.TOP,10)
        rightSizer.Add(trackCtrl,0,wx.TOP,10)
        rightSizer.Add(ratingCtrl,0,wx.TOP,10)
        rightSizer.Add(commentCtrl,0,wx.TOP,10)
        mainSizer.Add((200,1))
        mainSizer.Add((200,1))
        mainSizer.Add(leftSizer,0)
        mainSizer.Add(rightSizer,0)
        panel.AddCtrl(mainSizer)


        while panel.Affirmed():
            arrayInfo=[
                filepathCtrl.GetValue(),
                filenameCtrl.GetValue(),
                tracktitleCtrl.GetValue(),
                artistCtrl.GetValue(),
                genreCtrl.GetValue(),
                ratingCtrl.GetValue(),
                albumCtrl.GetValue(),
                discCtrl.GetValue(),
                trackCtrl.GetValue(),
                albumartistCtrl.GetValue(),
                yearCtrl.GetValue(),
                groupingCtrl.GetValue(),
                origDateCtrl.GetValue(),
                composerCtrl.GetValue(),
                conductorCtrl.GetValue(),
                commentCtrl.GetValue(),
                seqNumCtrl.GetValue()
            ]
            panel.SetResult(arrayInfo)

#====================================================================
class GetBasicSongInfoNextTrack(GetBasicSongInfo):
    name = "Get basic song info of next track"
    description = "Get basic song info of next track."
    NextSong = None
    class text:
        filepath = "File path"
        filename = "File name"
        tracktitle = "Track title"
        artist = "Artist"
        genre = "Genre"
        rating = "Rating"
        album = "Album"
        disc = "Disc #"
        track = "Track #"
        albumartist = "Album artist"
        year = "Year"
        grouping = "Grouping"
        origDate = "Original year"
        composer = "Composer"
        conductor = "Conductor"
        comment = "Comment"
        seqNum = 'Sequence number in "Now playing" window'
        endList = "End of playlist"
        shuffleMode = "Shuffle tracks mode"

    def __call__(self,arrayInfo):
        player = self.plugin.DispMM().Player
        index = player.CurrentSongIndex+1
        #flag=True
        if index==player.PlaylistCount:
            if player.isRepeat:
                index=0
            else:
                #flag=False
                return self.text.endList
        if player.isShuffle:
            return self.text.shuffleMode


        print player.PlaylistCount
        print "index="+str(index)
        self.NextSong=player.PlaylistItems(index)

        path=self.NextSong.Path
        indx=path.rfind("\\")+1
        result=path[:indx]+"," if arrayInfo[0] else ""
        result+=path[indx:]+"," if arrayInfo[1] else ""
        listPropert=(
            "Title",
            "ArtistName",
            "Genre",
            "Rating",
            "AlbumName",
            "DiscNumber",
            "TrackOrder",
            "AlbumArtistName",
            "Year",
            "Grouping",
            "OriginalYear",
            "MusicComposer",
            "Conductor",
            "Comment",
        )
        listNum=(
            False,
            False,
            False,
            True,
            False,
            True,
            True,
            False,
            True,
            False,
            True,
            False,
            False,
            False,
        )
        for propert,cond,numeric in zip(listPropert,arrayInfo[2:],listNum):
            if numeric:
                result+=str(getattr(self.NextSong,propert))\
                    +"," if cond else ""
            else:
                result+=getattr(self.NextSong,propert)\
                    +"," if cond else ""
        if arrayInfo[16]:
            result+=str(index+1)+","

        return result[:-1]


    def GetLabel(self, arrayInfo):
        result=""
        for condition in arrayInfo:
            result+="X" if condition else "_"
        return result

    def Configure(
        self,
        arrayInfo=[False]*17
    ):
        text=self.text
        panel = eg.ConfigPanel(self)
        filepathCtrl = wx.CheckBox(panel, -1, self.text.filepath)
        filepathCtrl.SetValue(arrayInfo[0])
        filenameCtrl = wx.CheckBox(panel, -1, self.text.filename)
        filenameCtrl.SetValue(arrayInfo[1])
        tracktitleCtrl = wx.CheckBox(panel, -1, self.text.tracktitle)
        tracktitleCtrl.SetValue(arrayInfo[2])
        artistCtrl = wx.CheckBox(panel, -1, self.text.artist)
        artistCtrl.SetValue(arrayInfo[3])
        genreCtrl = wx.CheckBox(panel, -1, self.text.genre)
        genreCtrl.SetValue(arrayInfo[4])
        ratingCtrl = wx.CheckBox(panel, -1, self.text.rating)
        ratingCtrl.SetValue(arrayInfo[5])
        albumCtrl = wx.CheckBox(panel, -1, self.text.album)
        albumCtrl.SetValue(arrayInfo[6])
        discCtrl = wx.CheckBox(panel, -1, self.text.disc)
        discCtrl.SetValue(arrayInfo[7])
        trackCtrl = wx.CheckBox(panel, -1, self.text.track)
        trackCtrl.SetValue(arrayInfo[8])
        albumartistCtrl = wx.CheckBox(panel, -1, self.text.albumartist)
        albumartistCtrl.SetValue(arrayInfo[9])
        yearCtrl = wx.CheckBox(panel, -1, self.text.year)
        yearCtrl.SetValue(arrayInfo[10])
        groupingCtrl = wx.CheckBox(panel, -1, self.text.grouping)
        groupingCtrl.SetValue(arrayInfo[11])
        origDateCtrl = wx.CheckBox(panel, -1, self.text.origDate)
        origDateCtrl.SetValue(arrayInfo[12])
        composerCtrl = wx.CheckBox(panel, -1, self.text.composer)
        composerCtrl.SetValue(arrayInfo[13])
        conductorCtrl = wx.CheckBox(panel, -1, self.text.conductor)
        conductorCtrl.SetValue(arrayInfo[14])
        commentCtrl = wx.CheckBox(panel, -1, self.text.comment)
        commentCtrl.SetValue(arrayInfo[15])
        seqNumCtrl = wx.CheckBox(panel, -1, self.text.seqNum)
        seqNumCtrl.SetValue(arrayInfo[16])

        mainSizer=wx.FlexGridSizer(2,2)
        leftSizer=wx.BoxSizer(wx.VERTICAL)
        rightSizer=wx.BoxSizer(wx.VERTICAL)

        leftSizer.Add(tracktitleCtrl,0)
        leftSizer.Add(artistCtrl,0,wx.TOP,10)
        leftSizer.Add(genreCtrl,0,wx.TOP,10)
        leftSizer.Add(albumCtrl,0,wx.TOP,10)
        leftSizer.Add(albumartistCtrl,0,wx.TOP,10)
        leftSizer.Add(groupingCtrl,0,wx.TOP,10)
        leftSizer.Add(composerCtrl,0,wx.TOP,10)
        leftSizer.Add(conductorCtrl,0,wx.TOP,10)
        leftSizer.Add(seqNumCtrl,0,wx.TOP,10)
        rightSizer.Add(filepathCtrl,0)
        rightSizer.Add(filenameCtrl,0,wx.TOP,10)
        rightSizer.Add(yearCtrl,0,wx.TOP,10)
        rightSizer.Add(origDateCtrl,0,wx.TOP,10)
        rightSizer.Add(discCtrl,0,wx.TOP,10)
        rightSizer.Add(trackCtrl,0,wx.TOP,10)
        rightSizer.Add(ratingCtrl,0,wx.TOP,10)
        rightSizer.Add(commentCtrl,0,wx.TOP,10)
        mainSizer.Add((200,1))
        mainSizer.Add((200,1))
        mainSizer.Add(leftSizer,0)
        mainSizer.Add(rightSizer,0)
        panel.AddCtrl(mainSizer)


        while panel.Affirmed():
            arrayInfo=[
                filepathCtrl.GetValue(),
                filenameCtrl.GetValue(),
                tracktitleCtrl.GetValue(),
                artistCtrl.GetValue(),
                genreCtrl.GetValue(),
                ratingCtrl.GetValue(),
                albumCtrl.GetValue(),
                discCtrl.GetValue(),
                trackCtrl.GetValue(),
                albumartistCtrl.GetValue(),
                yearCtrl.GetValue(),
                groupingCtrl.GetValue(),
                origDateCtrl.GetValue(),
                composerCtrl.GetValue(),
                conductorCtrl.GetValue(),
                commentCtrl.GetValue(),
                seqNumCtrl.GetValue()
            ]
            panel.SetResult(arrayInfo)

#====================================================================
class GetDetailSongInfo(eg.ActionClass):
    name = "Get detail song info"
    description = "Get detail song info."
    class text:
        lyricist = "Lyricist"
        BPM = "BPM"
        involvedpeople = "Involved people"
        originalartist = "Original artist"
        originaltitle = "Original album title"
        originallyricist = "Original lyricist"
        ISRC = "ISRC"
        publisher = "Publisher"
        encoder = "Encoder"
        copyright = "Copyright"

    def __call__(self, arrayInfo):
        listPropert=(
        "Lyricist",
        "BPM",
        "InvolvedPeople",
        "OriginalArtist",
        "OriginalTitle",
        "OriginalLyricist",
        "ISRC",
        "Publisher",
        "Encoder",
        "Copyright"
        )
        listNum=(
            False,
            True,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False
        )
        result=""
        for propert,cond,numeric in zip(listPropert,arrayInfo,listNum):
            if numeric:
                result+=str(getattr(self.plugin.DispMM().Player.CurrentSong,propert))\
                    +"," if cond else ""
            else:
                result+=getattr(self.plugin.DispMM().Player.CurrentSong,propert)\
                    +"," if cond else ""
        return result[:-1]

    def GetLabel(self, arrayInfo):
        result=""
        for condition in arrayInfo:
            result+="X" if condition else "_"
        return result

    def Configure(
        self,
        arrayInfo=[False]*10
    ):
        text=self.text
        panel = eg.ConfigPanel(self)
        lyricistCtrl = wx.CheckBox(panel, -1, self.text.lyricist)
        lyricistCtrl.SetValue(arrayInfo[0])
        BPMCtrl = wx.CheckBox(panel, -1, self.text.BPM)
        BPMCtrl.SetValue(arrayInfo[1])
        involvedpeopleCtrl = wx.CheckBox(panel, -1, self.text.involvedpeople)
        involvedpeopleCtrl.SetValue(arrayInfo[2])
        originalartistCtrl = wx.CheckBox(panel, -1, self.text.originalartist)
        originalartistCtrl.SetValue(arrayInfo[3])
        originaltitleCtrl = wx.CheckBox(panel, -1, self.text.originaltitle)
        originaltitleCtrl.SetValue(arrayInfo[4])
        originallyricistCtrl = wx.CheckBox(
            panel,
            -1,
            self.text.originallyricist
        )
        originallyricistCtrl.SetValue(arrayInfo[5])
        ISRCCtrl = wx.CheckBox(panel, -1, self.text.ISRC)
        ISRCCtrl.SetValue(arrayInfo[6])
        publisherCtrl = wx.CheckBox(panel, -1, self.text.publisher)
        publisherCtrl.SetValue(arrayInfo[7])
        encoderCtrl = wx.CheckBox(panel, -1, self.text.encoder)
        encoderCtrl.SetValue(arrayInfo[8])
        copyrightCtrl = wx.CheckBox(panel, -1, self.text.copyright)
        copyrightCtrl.SetValue(arrayInfo[9])

        mainSizer=wx.FlexGridSizer(2,2)
        leftSizer=wx.BoxSizer(wx.VERTICAL)
        rightSizer=wx.BoxSizer(wx.VERTICAL)

        leftSizer.Add(lyricistCtrl,0)
        leftSizer.Add(involvedpeopleCtrl,0,wx.TOP,10)
        leftSizer.Add(originalartistCtrl,0,wx.TOP,10)
        leftSizer.Add(originaltitleCtrl,0,wx.TOP,10)
        leftSizer.Add(originallyricistCtrl,0,wx.TOP,10)
        rightSizer.Add(BPMCtrl,0)
        rightSizer.Add(ISRCCtrl,0,wx.TOP,10)
        rightSizer.Add(publisherCtrl,0,wx.TOP,10)
        rightSizer.Add(encoderCtrl,0,wx.TOP,10)
        rightSizer.Add(copyrightCtrl,0,wx.TOP,10)
        mainSizer.Add((200,1))
        mainSizer.Add((200,1))
        mainSizer.Add(leftSizer,0)
        mainSizer.Add(rightSizer,0)
        panel.AddCtrl(mainSizer)


        while panel.Affirmed():
            arrayInfo=[
                lyricistCtrl.GetValue(),
                BPMCtrl.GetValue(),
                involvedpeopleCtrl.GetValue(),
                originalartistCtrl.GetValue(),
                originaltitleCtrl.GetValue(),
                originallyricistCtrl.GetValue(),
                ISRCCtrl.GetValue(),
                publisherCtrl.GetValue(),
                encoderCtrl.GetValue(),
                copyrightCtrl.GetValue()
            ]
            panel.SetResult(arrayInfo)


#====================================================================
class GetClassificationInfo(eg.ActionClass):
    name = "Get classification song info"
    description = "Get classification song info."
    class text:
        tempo = "Tempo"
        mood = "Mood"
        occasion = "Occasion"
        quality = "Quality"
        custom1 = "Custom 1"
        custom2 = "Custom 2"
        custom3 = "Custom 3"
        custom4 = "Custom 4"
        custom5 = "Custom 5"

    def __call__(self,arrayInfo):
        listPropert=(
            "Tempo",
            "Mood",
            "Occasion",
            "Quality",
            "Custom1",
            "Custom2",
            "Custom3",
            "Custom4",
            "Custom5"
        )
        result=""
        for propert,cond in zip(listPropert,arrayInfo):
            result+=getattr(self.plugin.DispMM().Player.CurrentSong,propert)\
                +"," if cond else ""
        return result[:-1]
    def GetLabel(self, arrayInfo):
        result=""
        for condition in arrayInfo:
            result+="X" if condition else "_"
        return result

    def Configure(
        self,
        arrayInfo=[False]*9
    ):
        text=self.text
        panel = eg.ConfigPanel(self)
        tempoCtrl = wx.CheckBox(panel, -1, self.text.tempo)
        tempoCtrl.SetValue(arrayInfo[0])
        moodCtrl = wx.CheckBox(panel, -1, self.text.mood)
        moodCtrl.SetValue(arrayInfo[1])
        occasionCtrl = wx.CheckBox(panel, -1, self.text.occasion)
        occasionCtrl.SetValue(arrayInfo[2])
        qualityCtrl = wx.CheckBox(panel, -1, self.text.quality)
        qualityCtrl.SetValue(arrayInfo[3])
        custom1Ctrl = wx.CheckBox(panel, -1, self.text.custom1)
        custom1Ctrl.SetValue(arrayInfo[4])
        custom2Ctrl = wx.CheckBox(panel, -1, self.text.custom2)
        custom2Ctrl.SetValue(arrayInfo[5])
        custom3Ctrl = wx.CheckBox(panel, -1, self.text.custom3)
        custom3Ctrl.SetValue(arrayInfo[6])
        custom4Ctrl = wx.CheckBox(panel, -1, self.text.custom4)
        custom4Ctrl.SetValue(arrayInfo[7])
        custom5Ctrl = wx.CheckBox(panel, -1, self.text.custom5)
        custom5Ctrl.SetValue(arrayInfo[8])
        mainSizer=wx.FlexGridSizer(2,2)
        leftSizer=wx.BoxSizer(wx.VERTICAL)
        rightSizer=wx.BoxSizer(wx.VERTICAL)

        leftSizer.Add(tempoCtrl,0)
        leftSizer.Add(moodCtrl,0,wx.TOP,10)
        leftSizer.Add(occasionCtrl,0,wx.TOP,10)
        leftSizer.Add(qualityCtrl,0,wx.TOP,10)
        rightSizer.Add(custom1Ctrl,0)
        rightSizer.Add(custom2Ctrl,0,wx.TOP,10)
        rightSizer.Add(custom3Ctrl,0,wx.TOP,10)
        rightSizer.Add(custom4Ctrl,0,wx.TOP,10)
        rightSizer.Add(custom5Ctrl,0,wx.TOP,10)
        mainSizer.Add((200,1))
        mainSizer.Add((200,1))
        mainSizer.Add(leftSizer,0)
        mainSizer.Add(rightSizer,0)
        panel.AddCtrl(mainSizer)

        while panel.Affirmed():
            arrayInfo=[
                tempoCtrl.GetValue(),
                moodCtrl.GetValue(),
                occasionCtrl.GetValue(),
                qualityCtrl.GetValue(),
                custom1Ctrl.GetValue(),
                custom2Ctrl.GetValue(),
                custom3Ctrl.GetValue(),
                custom4Ctrl.GetValue(),
                custom5Ctrl.GetValue()
            ]
            panel.SetResult(arrayInfo)
#====================================================================
class GetTechnicalSongInfo(eg.ActionClass):
    name = "Get technical song info"
    description = "Get technical song info."
    class text:
        length = "Length"
        filesize = "File size"
        bitrate = "Bitrate"
        VBR = "VBR"
        frequency = "Frequency"
        stereo = "Stereo"
        counter = "Play counter"
        leveling = "Leveling"
        lastplayed = "Last played"
#        seekable = "Seekable"
#        copyrighted = "Copyrighted"
#        original = "Original"

    def __call__(self, arrayInfo):
        listPropert=(
            "SongLength",
            "FileLength",
            "Bitrate",
            "VBR",
            "SampleRate",
            "Channels",
            "PlayCounter",
            "Leveling",
            "LastPlayed"
        )
        result=""
        for propert,cond in zip(listPropert,arrayInfo):
            result+=str(getattr(self.plugin.DispMM().Player.CurrentSong,propert))\
                +"," if cond else ""
        return result[:-1]

    def GetLabel(self, arrayInfo):
        result=""
        for condition in arrayInfo:
            result+="X" if condition else "_"
        return result

    def Configure(
        self,
        arrayInfo=[False]*9
    ):
        text=self.text
        panel = eg.ConfigPanel(self)
        lengthCtrl = wx.CheckBox(panel, -1, self.text.length)
        lengthCtrl.SetValue(arrayInfo[0])
        filesizeCtrl = wx.CheckBox(panel, -1, self.text.filesize)
        filesizeCtrl.SetValue(arrayInfo[1])
        bitrateCtrl = wx.CheckBox(panel, -1, self.text.bitrate)
        bitrateCtrl.SetValue(arrayInfo[2])
        VBRCtrl = wx.CheckBox(panel, -1, self.text.VBR)
        VBRCtrl.SetValue(arrayInfo[3])
        frequencyCtrl = wx.CheckBox(panel, -1, self.text.frequency)
        frequencyCtrl.SetValue(arrayInfo[4])
        stereoCtrl = wx.CheckBox(panel, -1, self.text.stereo)
        stereoCtrl.SetValue(arrayInfo[5])
        counterCtrl = wx.CheckBox(panel, -1, self.text.counter)
        counterCtrl.SetValue(arrayInfo[6])
        levelingCtrl = wx.CheckBox(panel, -1, self.text.leveling)
        levelingCtrl.SetValue(arrayInfo[7])
        lastplayedCtrl = wx.CheckBox(panel, -1, self.text.lastplayed)
        lastplayedCtrl.SetValue(arrayInfo[8])
#        seekableCtrl = wx.CheckBox(panel, -1, self.text.seekable)
#        seekableCtrl.SetValue(seekable)
#        copyrightedCtrl = wx.CheckBox(panel, -1, self.text.copyrighted)
#        copyrightedCtrl.SetValue(copyrighted)
#        originalCtrl = wx.CheckBox(panel, -1, self.text.original)
#        originalCtrl.SetValue(original)
        mainSizer=wx.FlexGridSizer(2,2)
        leftSizer=wx.BoxSizer(wx.VERTICAL)
        rightSizer=wx.BoxSizer(wx.VERTICAL)
        leftSizer.Add(lengthCtrl,0)
        leftSizer.Add(bitrateCtrl,0,wx.TOP,10)
        leftSizer.Add(frequencyCtrl,0,wx.TOP,10)
        leftSizer.Add(counterCtrl,0,wx.TOP,10)
        leftSizer.Add(lastplayedCtrl,0,wx.TOP,10)
        rightSizer.Add(filesizeCtrl,0)
        rightSizer.Add(VBRCtrl,0,wx.TOP,10)
        rightSizer.Add(stereoCtrl,0,wx.TOP,10)
        rightSizer.Add(levelingCtrl,0,wx.TOP,10)
        mainSizer.Add((200,1))
        mainSizer.Add((200,1))
        mainSizer.Add(leftSizer,0)
        mainSizer.Add(rightSizer,0)
        panel.AddCtrl(mainSizer)
#        panel.AddCtrl(seekableCtrl)
#        panel.AddCtrl(copyrightedCtrl)
#        panel.AddCtrl(originalCtrl)

        while panel.Affirmed():
            arrayInfo=[
                lengthCtrl.GetValue(),
                filesizeCtrl.GetValue(),
                bitrateCtrl.GetValue(),
                VBRCtrl.GetValue(),
                frequencyCtrl.GetValue(),
                stereoCtrl.GetValue(),
                counterCtrl.GetValue(),
                levelingCtrl.GetValue(),
                lastplayedCtrl.GetValue(),
#                seekableCtrl.GetValue(),
#                copyrightedCtrl.GetValue(),
#                originalCtrl.GetValue(),
            ]
            panel.SetResult(arrayInfo)



#====================================================================
class GetUniversal(eg.ActionClass):
    name = "Get Universal"
    description = "Get Universal."
    class text:
        label="Select requested property:"
        get = "Get"
        class Properties:
            AlbumName = "Album Name"
            AlbumLength = "AlbumLength"
            AlbumLengthString = "Album Length String"
            AlbumArtistName = "Album Artist Name"
            AlbumArtCount = "Album Art Count"
            ArtistName = "Artist Name"
            ArtistCount = "Artist Count"
            Author = "Author"
            Band = "Band"
            Bitrate = "Bitrate"
            BPM = "BPM"
            Comment = "Comment"
            Conductor = "Conductor"
            Copyright = "Copyright"
            Custom1 = "Custom 1"
            Custom2 = "Custom 2"
            Custom3 = "Custom 3"
            Custom4 = "Custom 4"
            Custom5 = "Custom 5"
            DateAdded = "Date Added"
            Encoder = "Encoder"
            FileLength = "File Length"
            FileModified = "File Modified"
            Genre = "Genre"
            Grouping = "Grouping"
            Channels = "Stereo"
            InvolvedPeople = "Involved People"
            IsntInDB = "Is not in DB"
            ISRC = "ISRC"
            LastPlayed = "Last Played"
            Leveling = "Leveling"
            Lyricist = "Lyricist"
            Lyrics = "Lyrics"
            MediaDriveLetter = "Media Drive Letter"
            MediaDriveType = "Media Drive Type"
            MediaSerialNumber = "Media Serial Number"
            MediaLabel = "Media Label"
            Mood = "Mood"
            MusicComposer = "Music Composer"
            Occasion = "Occasion"
            OriginalArtist = "Original Artist"
            OriginalLyricist = "Original Lyricist"
            OriginalTitle = "Original Title"
            OriginalYear = "Original Year"
            Path = "Path"
            PeakValue = "Peak Value"
            PlayCounter = "Play Counter"
            PlaylistOrder = "Playlist Order"
            PreviewPath = "Preview Path"
            Preview = "Preview"
            Publisher = "Publisher"
            Quality = "Quality"
            Rating = "Rating"
            RatingString = "Rating String"
            SampleRate = "Sample Rate"
            SongLength = "Song Length"
            SongLengthString = "Song Length String"
            Tempo = "Tempo"
            Title = "Title"
            DiscNumber = "Disc Number"
            TrackOrder = "Track Order"
            VBR = "VBR"
            Year = "Year"
            canCrossfade = "Can Crossfade"
            isShuffleIgnored = "Shuffle Is Ignored"

    def __init__(self):
        text=self.text
        self.propertiesList=(
            ("AlbumName","AlbumName"),
            ("Album.AlbumLength","AlbumLength"),
            ("Album.AlbumLengthString","AlbumLengthString"),
            ("AlbumArtistName","AlbumArtistName"),
            ("AlbumArt.Count","AlbumArtCount"),
            ("ArtistName","ArtistName"),
            ("Artist.Count","ArtistCount"),
            ("Author","Author"),
            ("Band","Band"),
            ("Bitrate","Bitrate"),
            ("BPM","BPM"),
            ("Comment","Comment"),
            ("Conductor","Conductor"),
            ("Copyright","Copyright"),
            ("Custom1","Custom1"),
            ("Custom2","Custom2"),
            ("Custom3","Custom3"),
            ("Custom4","Custom4"),
            ("Custom5","Custom5"),
            ("DateAdded","DateAdded"),
            ("Encoder","Encoder"),
            ("FileLength","FileLength"),
            ("FileModified","FileModified"),
            ("Genre","Genre"),
            ("Grouping","Grouping"),
            ("Channels","Channels"),
            ("InvolvedPeople","InvolvedPeople"),
            ("IsntInDB","IsntInDB"),
            ("ISRC","ISRC"),
            ("LastPlayed","LastPlayed"),
            ("Leveling","Leveling"),
            ("Lyricist","Lyricist"),
            ("Lyrics","Lyrics"),
            ("Media.DriveLetter","MediaDriveLetter"),
            ("Media.DriveType","MediaDriveType"),
            ("Media.SerialNumber","MediaSerialNumber"),
            ("MediaLabel","MediaLabel"),
            ("Mood","Mood"),
            ("MusicComposer","MusicComposer"),
            ("Occasion","Occasion"),
            ("OriginalArtist","OriginalArtist"),
            ("OriginalLyricist","OriginalLyricist"),
            ("OriginalTitle","OriginalTitle"),
            ("OriginalYear","OriginalYear"),
            ("Path","Path"),
            ("PeakValue","PeakValue"),
            ("PlayCounter","PlayCounter"),
            ("PlaylistOrder","PlaylistOrder"),
            ("PreviewPath","PreviewPath"),
            ("Preview","Preview"),
            ("Publisher","Publisher"),
            ("Quality","Quality"),
            ("Rating","Rating"),
            ("RatingString","RatingString"),
            ("SampleRate","SampleRate"),
            ("SongLength","SongLength"),
            ("SongLengthString","SongLengthString"),
            ("Tempo","Tempo"),
            ("Title","Title"),
            ("DiscNumberStr","DiscNumber"),
            ("TrackOrder","TrackOrder"),
            ("VBR","VBR"),
            ("Year","Year"),
            ("canCrossfade","canCrossfade"),
            ("isShuffleIgnored","isShuffleIgnored"),
        )
    def __call__(self, i):
        return getattr(self.plugin.DispMM().Player.CurrentSong,self.propertiesList[i][0])

    def GetLabel(self, i):
        return self.text.get+" "+eval("self.text.Properties."+self.propertiesList[i][1])
#        exec 'from %s import Demo' % demo
    def Configure(self, i=0):
        #text=self.text
        #txt=Text.ListProperties
        choices=[eval("self.text.Properties."+tpl[1]) for tpl in self.propertiesList]
        panel=eg.ConfigPanel(self)
        panel.AddLabel(self.text.label)
        infoCtrl=wx.Choice(
            panel,
            choices=choices,
        )
        infoCtrl.SetSelection(i)
        panel.AddCtrl(infoCtrl)
        while panel.Affirmed():
            panel.SetResult(infoCtrl.GetSelection())


#====================================================================
class WritingToMM(eg.ActionClass):
    name = "Writing to database MM"
    description = "Writing some one parameters to database MediaMonkey."
    class text:
        label="Select requested property:"
        set = "Set "
        checkboxlabel = "Make entry to ID3 tag too"
        class Properties:
            Comment = "Comment"
            Custom1 = "Custom 1"
            Custom2 = "Custom 2"
            Custom3 = "Custom 3"
            Custom4 = "Custom 4"
            Custom5 = "Custom 5"
            Genre = "Genre"
            Mood = "Mood"
            Occasion = "Occasion"
            Quality = "Quality"
            Rating = "Rating"
            Tempo = "Tempo"
    def __init__(self):
        text=self.text
        self.listCtrl=(
            "wx.TextCtrl(panel, -1, arrayVal0[%s])",
            (
                "eg.SpinNumCtrl(panel,-1,arrayVal0[%s],max=100.0,min=0.0,"
                "fractionWidth=1,increment=10,style=wx.TE_READONLY)"
            )
        )
        self.propertiesList=(
            ("Tempo","Tempo",0,False),
            ("Mood","Mood",0,False),
            ("Occasion","Occasion",0,False),
            ("Quality","Quality",0,False),
            ("Custom1","Custom1",0,False),
            ("Custom2","Custom2",0,False),
            ("Custom3","Custom3",0,False),
            ("Custom4","Custom4",0,False),
            ("Custom5","Custom5",0,False),
            ("Comment","Comment",0,True),
            ("Genre","Genre",0,True),
            ("Rating","Rating",1,True),
        )
    def __call__(self, i, arrayValue0, arrayValue1):
        setattr(self.plugin.DispMM().Player.CurrentSong,self.propertiesList[i][0]\
            ,arrayValue0[i])
        self.plugin.DispMM().Player.CurrentSong.UpdateDB()
        if arrayValue1[i]:
            self.plugin.DispMM().Player.CurrentSong.WriteTags()

    def GetLabel(self, i, arrayValue0, arrayValue1):
        if self.propertiesList[i][2]==0:
#            result = self.text.set+self.propertiesList[i][1]+"="+arrayValue0[i]
            result = eval("self.text.set+"+"self.text.Properties."+self.propertiesList[i][1])+"="+arrayValue0[i]
        else:
            result = eval("self.text.set+"+"self.text.Properties."+self.propertiesList[i][1])+"="+str(int(arrayValue0[i]))
        if arrayValue1[i]:
            result += " (+ID3)"
        return result


    def Configure(
        self,
        i=0,
        arrayValue0=[
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            50,
        ],
        arrayValue1 = [False] * 12
    ):
        arrayVal0 = arrayValue0[:]
        arrayVal1 = arrayValue1[:]
        choices=[eval("self.text.Properties."+tpl[1]) for tpl in self.propertiesList]
        panel = eg.ConfigPanel(self)
        choiceLbl=wx.StaticText(panel, -1, self.text.label)
        choiceCtrl=wx.Choice(
            panel,
            choices=choices,
        )
        choiceCtrl.SetSelection(i)
        mainSizer =wx.BoxSizer(wx.VERTICAL)
        choiceSizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        choiceSizer.Add(choiceLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
        choiceSizer.Add(choiceCtrl, 0, wx.EXPAND)
        mainSizer.Add(choiceSizer, 0, wx.EXPAND|wx.ALL, 10)
        dynSizer = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        mainSizer.Add(dynSizer, 0, wx.EXPAND|wx.BOTTOM, 10)
        panel.sizer.Add(mainSizer)

        def onChoiceChange(event=None):
            dynSizer.Clear(True)
            dynLbl = wx.StaticText(
                panel,
                -1,
                eval("self.text.Properties."+self.propertiesList[choiceCtrl.GetSelection()][1])+":"
            )

            #eval("self.text.set+"+"self.text.Properties."+self.propertiesList[i][1]+"="+arrayVal0[i])

            indx=self.propertiesList[choiceCtrl.GetSelection()][2]
            dummy = arrayVal0[0] # otherwise error:
# >>>  NameError: name 'arrayVal0' is not defined  <<<   ??????????????????????
            dynCtrl = eval(self.listCtrl[indx] % str(choiceCtrl.GetSelection()))
            dynSizer.Add(dynLbl, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL)
            dynSizer.Add(dynCtrl, 0, wx.EXPAND)
            if self.propertiesList[choiceCtrl.GetSelection()][3]:
                chkBoxCtrl = wx.CheckBox(panel, label=self.text.checkboxlabel)
                chkBoxCtrl.SetValue(arrayVal1[choiceCtrl.GetSelection()])
                dynSizer.Add((5,5))
                dynSizer.Add(chkBoxCtrl, 0, wx.EXPAND)
            mainSizer.Layout()
            if event:
                event.Skip()
        choiceCtrl.Bind(wx.EVT_CHOICE, onChoiceChange)
        onChoiceChange()
        while panel.Affirmed():
            arrayVal0[choiceCtrl.GetSelection()]=\
                dynSizer.GetChildren()[1].GetWindow().GetValue()
            if self.propertiesList[choiceCtrl.GetSelection()][3]:
                arrayVal1[choiceCtrl.GetSelection()]=\
                    dynSizer.GetChildren()[3].GetWindow().GetValue()
            panel.SetResult(choiceCtrl.GetSelection(),arrayVal0, arrayVal1 )

class LoadPlaylist(eg.ActionClass):
    name = "Load Playlist by Name"
    description = "Loads a MediaMonkey playlist defined by name."
    class text:
        playlistName = "Playlist name:"
        found = "found (%s songs)"
        noFound = "not found or empty"
        repeat = "Continous playback"
        shuffle = "Shuffle tracks"
        crossfade = "Crossfade"


    def __call__(self, plString,repeat,shuffle,crossfade):
        MMobj = self.plugin.DispMM()
        plItems = MMobj.PlaylistByTitle(plString).Tracks
        num = plItems.Count
        if num >0:
            MMobj.Player.Stop()
            MMobj.Player.PlaylistClear()
            MMobj.Player.PlaylistAddTracks(plItems)
            if repeat<2:
                MMobj.Player.isRepeat=bool(repeat)
            if crossfade<2:
                MMobj.Player.isCrossfade=bool(crossfade)
            if shuffle<2:
                MMobj.Player.isShuffle=bool(shuffle)
            MMobj.Player.Play()
            return plString+" "+self.text.found % str(num)
        else:
            return plString+" "+self.text.noFound



    def Configure(self, plString="",repeat=2,shuffle=2,crossfade=2):
        panel = eg.ConfigPanel(self)
        text = self.text
        textCtrl = wx.TextCtrl(panel, -1, plString, style=wx.TE_NOHIDESEL)
        SizerAdd = panel.sizer.Add
        SizerAdd(wx.StaticText(panel, -1, text.playlistName))
        SizerAdd(textCtrl, 0, wx.EXPAND)
        repeatChkBoxCtrl = wx.CheckBox(panel, label=self.text.repeat,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        repeatChkBoxCtrl.Set3StateValue(repeat)
        SizerAdd(repeatChkBoxCtrl,0,wx.TOP,15,)
        shuffleChkBoxCtrl = wx.CheckBox(panel, label=self.text.shuffle,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        shuffleChkBoxCtrl.Set3StateValue(shuffle)
        SizerAdd(shuffleChkBoxCtrl,0,wx.TOP,15)
        crossfadeChkBoxCtrl = wx.CheckBox(panel, label=self.text.crossfade,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        crossfadeChkBoxCtrl.Set3StateValue(crossfade)
        SizerAdd(crossfadeChkBoxCtrl,0,wx.TOP,15)

        while panel.Affirmed():
            panel.SetResult(
                textCtrl.GetValue(),
                repeatChkBoxCtrl.Get3StateValue(),
                shuffleChkBoxCtrl.Get3StateValue(),
                crossfadeChkBoxCtrl.Get3StateValue()
            )


class AddCurrentSongToPlaylist(eg.ActionClass):
    name = "Add current playing song to Playlist"
    description = "Adds current playing song to Playlist."
    class text:
        playlistName = "Playlist name:"
        skip = "Skip to next track"
        radiobox = "Result mode"
        verboseON = "Verbose"
        verboseOFF = "Numeric"
        res0 = "Track added to playlist %s"
        res1 = "Track already exist in playlist %s"
        res2 = "Playlist %s not exist"
        forToolTip = "for case"

    def __call__(self, plString, skip, verbose):
        MMobj = self.plugin.DispMM()
        idSong=MMobj.Player.CurrentSong.ID
        IDPlaylist=MMobj.PlaylistByTitle(plString).ID
        if IDPlaylist <> 0:
            sql="SELECT COUNT(*) FROM PlaylistSongs WHERE PlaylistSongs.IDSong="+\
                str(idSong)+" AND PlaylistSongs.IDPlaylist="+str(IDPlaylist)
            if MMobj.Database.OpenSQL(sql).ValueByIndex(0) == "0":
                MMobj.PlaylistByTitle(plString).AddTrackById(idSong)
                res = 0
            else:
                res = 1
        else:
            res = 2
        if skip:
            MMobj.Player.Next()
        verbres = eval("self.text.res"+str(res))
        return res if verbose==1 else verbres % plString

    def Configure(self, plString="", skip=False, verbose = 0):
        panel = eg.ConfigPanel(self)
        text = self.text
        textCtrl = wx.TextCtrl(panel, -1, plString, style=wx.TE_NOHIDESEL)
        SizerAdd = panel.sizer.Add
        SizerAdd(wx.StaticText(panel, -1, text.playlistName))
        SizerAdd(textCtrl, 0, wx.EXPAND)
        skipChkBoxCtrl = wx.CheckBox(panel, label=self.text.skip)
        skipChkBoxCtrl.SetValue(skip)
        SizerAdd(skipChkBoxCtrl,0,wx.TOP,15,)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            choices=[self.text.verboseON, self.text.verboseOFF],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetItemToolTip(1, "0 "+self.text.forToolTip+"   "+self.text.res0 % "" +\
            "\n1 "+self.text.forToolTip+"   "+self.text.res1 % "" +\
            "\n2 "+self.text.forToolTip+"   "+self.text.res2 % "")
        radioBox.SetSelection(verbose)
        SizerAdd(radioBox, 0, wx.EXPAND|wx.TOP,15)

        while panel.Affirmed():
            panel.SetResult(
                textCtrl.GetValue(),
                skipChkBoxCtrl.GetValue(),
                radioBox.GetSelection(),
            )


class RemoveCurrentSongFromPlaylist(eg.ActionClass):
    name = "Remove current playing song from Playlist"
    description = "Remove current playing song from Playlist."
    class text:
        playlistName = "Playlist name:"
        skip = "Skip to next track"
        now_pl='Remove track from "Now playing" window too'
        radiobox = "Result mode"
        verboseON = "Verbose"
        verboseOFF = "Numeric"
        res0 = "Track removed from playlist %s"
        res1 = "Track not exist in playlist %s"
        res2 = "Playlist %s not exist"
        forToolTip = "for case"

    def __call__(self, plString, skip, now_pl, verbose):
        MMobj = self.plugin.DispMM()
        Player = MMobj.Player
        idSong=Player.CurrentSong.ID
        IDPlaylist=MMobj.PlaylistByTitle(plString).ID
        if IDPlaylist <> 0:
            sql=" FROM PlaylistSongs WHERE IDPlaylist="+str(IDPlaylist)+" AND IDSong="+str(idSong)
            if MMobj.Database.OpenSQL("SELECT COUNT(*)"+sql).ValueByIndex(0) == "1":
                MMobj.Database.ExecSQL("DELETE"+sql)
                MMobj.MainTracksWindow.Refresh()
                indx=Player.CurrentSongIndex
                if idSong==Player.PlaylistItems(indx).ID:
                    if now_pl:
                        Player.PlaylistDelete(indx)
                res = 0
            else:
                res = 1
        else:
            res = 2
        if skip:
            Player.Next()
        verbres = eval("self.text.res"+str(res))
        return res if verbose==1 else verbres % plString

    def Configure(self, plString="", skip=False, now_pl=False, verbose = 0):
        panel = eg.ConfigPanel(self)
        text = self.text
        textCtrl = wx.TextCtrl(panel, -1, plString, style=wx.TE_NOHIDESEL)
        SizerAdd = panel.sizer.Add
        SizerAdd(wx.StaticText(panel, -1, text.playlistName))
        SizerAdd(textCtrl, 0, wx.EXPAND)
        skipChkBoxCtrl = wx.CheckBox(panel, label=self.text.skip)
        skipChkBoxCtrl.SetValue(skip)
        SizerAdd(skipChkBoxCtrl,0,wx.TOP,15,)
        now_plChkBoxCtrl = wx.CheckBox(panel, label=self.text.now_pl)
        now_plChkBoxCtrl.SetValue(now_pl)
        SizerAdd(now_plChkBoxCtrl,0,wx.TOP,15,)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            choices=[self.text.verboseON, self.text.verboseOFF],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetItemToolTip(1, "0 "+self.text.forToolTip+"   "+self.text.res0 % "" +\
            "\n1 "+self.text.forToolTip+"   "+self.text.res1 % "" +\
            "\n2 "+self.text.forToolTip+"   "+self.text.res2 % "")
        radioBox.SetSelection(verbose)
        SizerAdd(radioBox, 0, wx.EXPAND|wx.TOP,15)

        while panel.Affirmed():
            panel.SetResult(
                textCtrl.GetValue(),
                skipChkBoxCtrl.GetValue(),
                now_plChkBoxCtrl.GetValue(),
                radioBox.GetSelection(),
            )


class RemoveCurrentSongFromNowPlaying(eg.ActionClass):
    name = "Remove current playing song from Now playing window"
    description = "Remove current playing song from Now playing window."
    class text:
        skip = "Skip to next track"
        radiobox = "Result mode"
        verboseON = "Verbose"
        verboseOFF = "Numeric"
        res0 = "Track removed from Now playing window"
        res1 = "Track not removed from Now playing window"
        forToolTip = "for case"

    def __call__(self, skip, verbose):
        MMobj = self.plugin.DispMM()
        Player = MMobj.Player
        idSong=Player.CurrentSong.ID
        indx=Player.CurrentSongIndex
        if idSong==Player.PlaylistItems(indx).ID:
            Player.PlaylistDelete(indx)
            res = 0
        else:
            res = 1
        if skip:
            Player.Next()
        verbres = eval("self.text.res"+str(res))
        return res if verbose==1 else verbres

    def Configure(self, skip=False, verbose=0):
        panel = eg.ConfigPanel(self)
        text = self.text
        SizerAdd = panel.sizer.Add
        skipChkBoxCtrl = wx.CheckBox(panel, label=self.text.skip)
        skipChkBoxCtrl.SetValue(skip)
        SizerAdd(skipChkBoxCtrl,0,wx.TOP,15,)
        radioBox = wx.RadioBox(
            panel,
            -1,
            self.text.radiobox,
            choices=[self.text.verboseON, self.text.verboseOFF],
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetItemToolTip(1, "0 "+self.text.forToolTip+"   "+self.text.res0+\
            "\n1 "+self.text.forToolTip+"   "+self.text.res1)
        radioBox.SetSelection(verbose)
        SizerAdd(radioBox, 0, wx.EXPAND|wx.TOP,15)

        while panel.Affirmed():
            panel.SetResult(
                skipChkBoxCtrl.GetValue(),
                radioBox.GetSelection(),
            )



class LoadPlaylistByFilter(eg.ActionClass):
    name = "Load Playlist by Filter"
    description = "Loads a MediaMonkey playlist defined by filter (SQL query)."

    class text:
        radioboxMode = "Select songs ..."
        modeAnd = "Matches all rules (AND)"
        modeOr = "Matches at least one rule (OR)"
        equal = "is equal to"
        notEqual = "is not equal to"
        greater = "is greater than"
        greatOrEqual = "is greater than or equal to"
        less = "is less than"
        lowerOrEqual = "is less than or equal to"
        notStartsWith = "not starts with"
        startsWith = "starts with"
        endsWith = "ends with"
        notEndsWith = "does not end with"
        includes = "includes"
        notIncludes = "excludes"
        isEmpty = "is empty"
        isNotEmpty = "is non-empty"
        beforeLess = "was earlier than - before ..."   #RELATIVE TO 'NOW' MODE
        beforeMore = "was later than - before ..."     #RELATIVE TO 'NOW' MODE
        filterName = "Filter name:"
        found = "%s/%s songs found"
        noFound = "no song found"
        asc = "ascending"
        desc = "descending"
        order1 = "Songs found are sorted in"
        order2 = "order by:"
        limit1 = "Select only the first"
        limit2 = "entry"
        repeat = "Continous playback"
        shuffle = "Shuffle tracks"
        crossfade = "Crossfade"
        accessible = "Load only accessible tracks (low speed)"
        #seconds = "seconds"
        minutes = "minutes"
        hours = "hours"
        days = "days"
        months = "months"
        years = "years"

        class Properties:
            Artist = "Artist"
            Album = "Album"
            AlbumArtist = "Album Artist"
            AudioCDTrack = "Audio CD Track"
            Author = "Author"
            Band = "Band"
            Bitrate = "Bitrate"
            BPM = "BPM"
            Broadcast = "Broadcast"
            CacheName = "Cache Name"
            CacheStatus = "Cache Status"
            Comment = "Comment"
            Conductor = "Conductor"
            Copyright = "Copyright"
            Copyrighted = "Copyrighted"
            Custom1 = "Custom1"
            Custom2 = "Custom2"
            Custom3 = "Custom3"
            Custom4 = "Custom4"
            Custom5 = "Custom5"
            DateAdded = "Date Added"
            DiscNumber = "Disc Number"
            EncodedBy = "Encoded By"
            Encoder = "Encoder"
            FileLength = "File Length"
            FileModified = "File Modified"
            GaplessBytes = "Gapless Bytes"
            Genre = "Genre"
            GroupDesc = "Group Desc"
            IDAlbum = "ID Album"
            IDFolder = "ID Folder"
            IDMedia = "ID Media"
            InitialKey = "Initial Key"
            InvolvedPeople = "Involved People"
            ISRC = "ISRC"
            Language = "Language"
            LastTimePlayed = "Last Time Played"
            Lyricist = "Lyricist"
            Lyrics = "Lyrics"
            MaxSample = "Max Sample"
            MediaType = "Media Type"
            Mood = "Mood"
            NormalizeAlbum = "Normalize Album"
            NormalizeTrack = "Normalize Track"
            Occasion = "Occasion"
            OrigArtist = "Original Artist"
            OrigFileLength = "Original FileLength"
            Original = "Original"
            OrigLyricist = "Original Lyricist"
            OrigTitle = "Original Title"
            OrigYear = "Original Year"
            PlaybackPos = "Playback Position"
            PlayCounter = "Play Counter"
            PostGap = "Post Gap"
            PreGap = "Pre Gap"
            PreviewLength = "Preview Length"
            PreviewName = "Preview Name"
            PreviewStartTime = "Preview StartTime"
            PreviewState = "Preview State"
            Publisher = "Publisher"
            Quality = "Quality"
            Rating = "Rating"
            RatingString = "Rating String"
            Remixer = "Remixer"
            SamplingFrequency = "Sampling Frequency"
            Seekable = "Seekable"
            SignPart1 = "Sign Part1"
            SignPart2 = "Sign Part2"
            SignPart3 = "Sign Part3"
            SignPart4 = "Sign Part4"
            SignType = "Sign Type"
            SongLength = "Song Length"
            SongPath = "Song Path"
            SongTitle = "Song Title"
            Stereo = "Stereo"
            SubTitle = "SubTitle"
            Tempo = "Tempo"
            TotalSamples = "Total Samples"
            TrackModified = "Track Modified"
            TrackNumber = "Track Number"
            VBR = "VBR"
            WebArtist = "Web Artist"
            WebCommercial = "Web Commercial"
            WebCopyright = "Web Copyright"
            WebFilepage = "Web Filepage"
            WebPayment = "Web Payment"
            WebPublisher = "Web Publisher"
            WebRadio = "Web Radio"
            WebSource = "Web Source"
            WebUser = "Web User"
            Year = "Year"


    def __init__(self):
        self.myDirty=None
        text=self.text
        self.propertiesList=(
            ("Artist","T"),
            ("Album","T"),
            ("AlbumArtist","T"),
            ("AudioCDTrack","I"),
            ("Author","T"),
            ("Band","T"),
            ("Bitrate","I"),
            ("BPM","I"),
            ("Broadcast","I"),
            ("CacheName","T"),
            ("CacheStatus","I"),
            ("Comment","T"),
            ("Conductor","T"),
            ("Copyright","T"),
            ("Copyrighted","I"),
            ("Custom1","T"),
            ("Custom2","T"),
            ("Custom3","T"),
            ("Custom4","T"),
            ("Custom5","T"),
            ("DateAdded","D"),
            ("DiscNumber","T"),
            ("EncodedBy","T"),
            ("Encoder","T"),
            ("FileLength","I"),
            ("FileModified","D"),
            ("GaplessBytes","I"),
            ("Genre","T"),
            ("GroupDesc","T"),
            ("IDAlbum","I"),
            ("IDFolder","I"),
            ("IDMedia","I"),
            ("InitialKey","T"),
            ("InvolvedPeople","T"),
            ("ISRC","T"),
            ("Language","T"),
            ("LastTimePlayed","D"),
            ("Lyricist","T"),
            ("Lyrics","T"),
            ("MaxSample","R"),
            ("MediaType","T"),
            ("Mood","T"),
            ("NormalizeAlbum","R"),
            ("NormalizeTrack","R"),
            ("Occasion","T"),
            ("OrigArtist","T"),
            ("OrigFileLength","I"),
            ("Original","I"),
            ("OrigLyricist","T"),
            ("OrigTitle","T"),
            ("OrigYear","I"),
            ("PlaybackPos","I"),
            ("PlayCounter","I"),
            ("PostGap","I"),
            ("PreGap","I"),
            ("PreviewLength","I"),
            ("PreviewName","T"),
            ("PreviewStartTime","I"),
            ("PreviewState","I"),
            ("Publisher","T"),
            ("Quality","T"),
            ("Rating","I"),
            ("RatingString","T"),
            ("Remixer","T"),
            ("SamplingFrequency","I"),
            ("Seekable","I"),
            ("SignPart1","I"),
            ("SignPart2","I"),
            ("SignPart3","I"),
            ("SignPart4","I"),
            ("SignType","I"),
            ("SongLength","I"),
            ("SongPath","T"),
            ("SongTitle","T"),
            ("Stereo","I"),
            ("SubTitle","T"),
            ("Tempo","T"),
            ("TotalSamples","I"),
            ("TrackModified","D"),
            ("TrackNumber","T"),
            ("VBR","I"),
            ("WebArtist","T"),
            ("WebCommercial","T"),
            ("WebCopyright","T"),
            ("WebFilepage","T"),
            ("WebPayment","T"),
            ("WebPublisher","T"),
            ("WebRadio","T"),
            ("WebSource","T"),
            ("WebUser","T"),
            ("Year","I")
        )

        self.unitList=(
           # "seconds",
            "minutes",
            "hours",
            "days",
            "months",
            "years"
        )

        self.trendList=(
            "asc",
            "desc"
        )

        self.exprList1=(
            "equal",
            "notEqual",
            "greater",
            "greatOrEqual",
            "less",
            "lowerOrEqual",
            "beforeLess",
            "beforeMore",
        )

        self.exprList=[
            "equal",
            "notEqual",
            "greater",
            "greatOrEqual",
            "less",
            "lowerOrEqual",
            "startsWith",
            "notStartsWith",
            "endsWith",
            "notEndsWith",
            "includes",
            "notIncludes",
            "isEmpty",
            "isNotEmpty",
        ]


    def __call__(
        self,
        plName,
        mode,
        listRules,
        order,
        trend,
        crit,
        limit,
        num,
        repeat,
        shuffle,
        crossfade,
        accessible
    ):
        MMobj = self.plugin.DispMM()


        sql=""
        op=' AND ' if mode==0 else ' OR '
        for rule in listRules:
            i=listRules.index(rule)
            substValues1=(op,self.propertiesList[rule[0]][0],rule[2])
            substValues2=(op,rule[2],self.propertiesList[rule[0]][0])
            substValues3=(op,self.propertiesList[rule[0]][0])
            dateType=self.propertiesList[rule[0]][1]
            emptVal = '""'  if dateType=="T" else '"-1"'
            tuplOper=("=","<>",">",">=","<","<=")

            if dateType=="D":
                if rule[1]<6:
                    for ix in range(0,6):
                        if rule[1]==ix:
                            substValues=(op,self.propertiesList[rule[0]][0],tuplOper[ix],rule[2])
                            sql+="%sstrftime('%%Y-%%m-%%d %%H:%%M:%%S',%s+2415018.5)%s'%s'" % substValues
                            break
                else:
                    substValues=(op,self.propertiesList[rule[0]][0],rule[2][:-1],self.unitList[int(rule[2][-1])])
                    if rule[1]==6:
                        sql+="%s(%s+2415018.5)>julianday('now','-%s %s','localtime')" % substValues
                    if rule[1]==7:
                        sql+="%s(%s+2415018.5)<julianday('now','-%s %s','localtime')" % substValues
            else: # (No "DateType")
                for ix in range(0,6):
                    if rule[1]==ix:
                        substValues=(op,self.propertiesList[rule[0]][0],tuplOper[ix],rule[2])
                        sql+='%s%s%s"%s"' % substValues
                        break
                if rule[1]==6:
                    sql+='%slike("%s%%",%s)' % substValues2
                if rule[1]==7:
                    sql+='%sNOT like("%s%%",%s)' % substValues2
                elif rule[1]==8:
                    sql+='%slike("%%%s",%s)' % substValues2
                elif rule[1]==9:
                    sql+='%sNOT like("%%%s",%s)' % substValues2
                elif rule[1]==10:
                    sql+='%sinstr(%s,"%s")' %  substValues1
                elif rule[1]==11:
                    sql+='%sNOT (instr(%s,"%s"))' %  substValues1
                elif rule[1]==12:
                    sql+='%s%s=' % substValues3 + emptVal
                elif rule[1]==13:
                    sql+='%s%s<>' % substValues3 + emptVal
        sql=(sql[5:] if mode==0 else sql[4:])
        if order:
            sql+=" order by "+self.propertiesList[crit][0]+" "+self.trendList[trend]
        if limit:
            sql+=" limit "+str(num)

        #print sql #Debuging
        Total=MMobj.Database.OpenSQL("SELECT COUNT(*) FROM Songs WHERE "+sql).ValueByIndex(0)
        if int(Total) > 0:
            MMobj.Player.Stop()
            MMobj.Player.PlaylistClear()
            n=0
            MyTrack = MMobj.Database.QuerySongs(sql)
            while not MyTrack.EOF:
                if accessible:
                    if isfile(MyTrack.Item.Path):
                        MMobj.Player.PlaylistAddTrack(MyTrack.Item)
                        n+=1
                else:
                    MMobj.Player.PlaylistAddTrack(MyTrack.Item)
                    n+=1
                MyTrack.Next()
            if n>0:
                if repeat<2:
                    MMobj.Player.isRepeat=bool(repeat)
                if crossfade<2:
                    MMobj.Player.isCrossfade=bool(crossfade)
                if shuffle<2:
                    MMobj.Player.isShuffle=bool(shuffle)
                MMobj.Player.Play()
                return plName+": "+self.text.found % (str(n),str(Total))
            else:
                return plName+": "+self.text.noFound


    def Configure(
        self,
        plName="",
        mode=0,
        listRules=[[-1,-1,u""]],
        order=False,
        trend=0,
        crit=0,
        limit=False,
        num="100",
        repeat=2,
        shuffle=2,
        crossfade=2,
        accessible=False
    ):
        def validityCheck():
            if CheckEnable:
                flag=True
                for i in range(0,self.i):
                    choice0=listRules2[i][0]
                    choice1=listRules2[i][1]
                    if choice0<0 or choice1<0:
                        flag=False
                        break
                    else:
                        if self.propertiesList[choice0][1] <> "D":
                            if choice1 < 12 and listRules2[i][2]==u"":
                                flag=False
                                break
                        else:
                            #if choice1>5 and wx.FindWindowById(i+150).GetValue()<1:
                            if choice1>5 and int(listRules2 [i][2][:-1])<1:
                                flag=False
                                break
                if not self.myDirty:
                    panel.SetIsDirty(True)
                    myDirty=True
                panel.EnableButtons(flag)

        listRules2=[] #working copy (after Cancel flush it)
        for i in range(0,len(listRules)):
            listRules2.append(listRules[i][:])
        maxRules=10
        panel = eg.ConfigPanel(self)
        panel.sizer.SetMinSize((560, 110+29*maxRules))
        text = self.text
        radioBoxMode = wx.RadioBox(
            panel,
            -1,
            text.radioboxMode,
            choices=[text.modeAnd, text.modeOr],
            style=wx.RA_SPECIFY_COLS
        )
        radioBoxMode.SetMinSize((556,43))
        radioBoxMode.SetSelection(mode)
        panel.sizer.Add(radioBoxMode, 0)
        self.mySizer = wx.GridBagSizer(vgap=8,hgap=10)
        self.mySizer.SetMinSize((560, 6+29*maxRules))
        panelAdd = panel.sizer.Add
        panelAdd(self.mySizer, 0,wx.TOP,10)

        statBox_1 = wx.StaticBox(panel, -1, "")
        stBsizer_1 = wx.StaticBoxSizer(statBox_1, wx.VERTICAL)
        stBsizer_1.SetMinSize((426,-1))
        statBox_2 = wx.StaticBox(panel, -1, "")
        stBsizer_2 = wx.StaticBoxSizer(statBox_2, wx.VERTICAL)
        stBsizer_2.SetMinSize((120,69))
        nameCtrl = wx.TextCtrl(panel, -1, plName, style=wx.TE_NOHIDESEL,size=(100,22))
        stBsizer_2.Add(wx.StaticText(panel, -1, text.filterName),0,wx.LEFT|wx.TOP,4)
        stBsizer_2.Add(nameCtrl, 0,wx.LEFT|wx.TOP,4)

        orderSizer=wx.BoxSizer(wx.HORIZONTAL)
        orderChkBoxCtrl = wx.CheckBox(panel, label="")
        orderChkBoxCtrl.SetValue(order)
        orderSizer.Add(orderChkBoxCtrl,0,wx.TOP,4)
        dirTxt1=wx.StaticText(panel, -1, self.text.order1)
        orderSizer.Add(dirTxt1,0,wx.LEFT|wx.TOP,4)
        trends=[eval("self.text."+tpl) for tpl in self.trendList]
        dirCtrl=wx.Choice(panel, -1, choices=trends,size=(-1, -1))
        dirCtrl.SetSelection(trend)
        orderSizer.Add(dirCtrl,0,wx.LEFT,4)
        dirTxt2=wx.StaticText(panel, -1, self.text.order2)
        orderSizer.Add(dirTxt2,0,wx.LEFT|wx.TOP,4)
        criters=[eval("self.text.Properties."+tpl[0]) for tpl in self.propertiesList]
        critCtrl=wx.Choice(panel, -1, choices=criters,size=(-1, -1))
        critCtrl.SetSelection(crit)
        orderSizer.Add(critCtrl,0,wx.LEFT,4)

        limitSizer=wx.BoxSizer(wx.HORIZONTAL)
        limitChkBoxCtrl = wx.CheckBox(panel, label="")
        limitChkBoxCtrl.SetValue(limit)
        limitSizer.Add(limitChkBoxCtrl,0,wx.TOP,4)
        limitTxt1=wx.StaticText(panel, -1, self.text.limit1)
        limitSizer.Add(limitTxt1,0,wx.LEFT|wx.TOP,4)
        numCtrl = masked.NumCtrl(
            panel, -1, num,
            min=1,integerWidth=6,
            allowNegative=False,groupDigits=False)
        limitSizer.Add(numCtrl, 0,wx.LEFT,4)
        limitTxt2=wx.StaticText(panel, -1, self.text.limit2)
        limitSizer.Add(limitTxt2,0,wx.LEFT|wx.TOP,4)

        stBsizer_1.Add(orderSizer,0,wx.TOP,4)
        stBsizer_1.Add(limitSizer,0,wx.TOP,8)

        middleSizer=wx.BoxSizer(wx.HORIZONTAL)
        middleSizer.Add(stBsizer_1,0)
        middleSizer.Add(stBsizer_2,0,wx.LEFT,10)
        panelAdd(middleSizer)
        bottomSizer = wx.GridSizer(rows=2, cols=2, hgap=5, vgap=10)
        repeatChkBoxCtrl = wx.CheckBox(panel, label=self.text.repeat,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        repeatChkBoxCtrl.Set3StateValue(repeat)
        bottomSizer.Add(repeatChkBoxCtrl,0,wx.LEFT,5)
        shuffleChkBoxCtrl = wx.CheckBox(panel, label=self.text.shuffle,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        shuffleChkBoxCtrl.Set3StateValue(shuffle)
        bottomSizer.Add(shuffleChkBoxCtrl,0)
        crossfadeChkBoxCtrl = wx.CheckBox(panel, label=self.text.crossfade,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        crossfadeChkBoxCtrl.Set3StateValue(crossfade)
        bottomSizer.Add(crossfadeChkBoxCtrl,0,wx.LEFT,5)
        accessibleChkBoxCtrl = wx.CheckBox(panel, label=self.text.accessible)
        accessibleChkBoxCtrl.SetValue(accessible)
        bottomSizer.Add(accessibleChkBoxCtrl,0)
        panelAdd(bottomSizer,0,wx.TOP,10)

        def CreateExprCtrl(row):
#Call from:	 AddRow,UpdateChoiceExpr
            if self.propertiesList[listRules2[row][0]][1]=="D": # Date & Time
                choicExpr=[eval("self.text."+tpl) for tpl in self.exprList1]
            else:
                choicExpr=[eval("self.text."+tpl) for tpl in self.exprList]
            exprCtrl=wx.Choice(panel, row+100, choices=choicExpr,size=(182, 22))
            exprCtrl.SetSelection(listRules2[row][1])
            exprCtrl.Bind(wx.EVT_CHOICE, OnExprChoice)
            self.mySizer.Add(exprCtrl,(row,1))
            self.mySizer.Layout()

        def ConvToWxDt(dt):
#Call from: CreateStrCtrl, UpdateStr
            """Conversion of data record to wx.DateTime format."""
            wxDttm=wx.DateTime()
            wxDttm.Set(int(dt[8:10]),int(dt[5:7])-1,int(dt[:4]))
            return wxDttm

        def CreateStrCtrl(row):
#Call from: UpdateStr, AddRow
            tp=self.propertiesList[listRules2[row][0]][1]
            if tp<>"D":
                strCtrl=wx.TextCtrl(panel, row+150, "", style=wx.TE_NOHIDESEL,size=(168, 22))
                strCtrl.Bind(wx.EVT_TEXT, OnStrChange)
                strCtrl.SetValue(listRules2[row][2])
                if listRules2[row][1]>11:
                    strCtrl.Enable(False)
                infoSizer=wx.BoxSizer(wx.HORIZONTAL)
                infoSizer.Add(strCtrl)
            else: # Date & Time Ctrl
                if listRules2[row][1]<6: #for absolute date/time type
                    clndrCtrl=wx.DatePickerCtrl(panel,row+150, size=(85,22),
                        style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
                    clndrCtrl.SetRange(ConvToWxDt('1900-01-01'),ConvToWxDt('2050-12-31'))
                    clndrCtrl.SetValue(ConvToWxDt(listRules2[row][2]))
                    clndrCtrl.Bind(wx.EVT_DATE_CHANGED, OnClndrChange)
                    infoSizer=wx.BoxSizer(wx.HORIZONTAL)
                    infoSizer.Add(clndrCtrl)
                    spinBtn = wx.SpinButton(panel,row+250, wx.DefaultPosition, (-1,22), wx.SP_VERTICAL )
                    timeCtrl = masked.TimeCtrl(
                        panel, row+200, name="24hrCtrl", fmt24hr=True,
                        spinButton=spinBtn
                        )
                    timeCtrl.SetValue(listRules2[row][2][11:])
                    timeCtrl.Bind(masked.EVT_TIMEUPDATE, OnTimeChange )
                    infoSizer.Add(timeCtrl,0,wx.LEFT,2)
                    infoSizer.Add(spinBtn)
                else: #for time  relative (NOW) type
                    periodCtrl = masked.NumCtrl(
                        panel, row+150, num,
                        size=(85,22),min=1,integerWidth=9,
                        allowNegative=False,groupDigits=False,
                        autoSize=False,invalidBackgroundColour = "White",)
                    #periodCtrl.Bind(masked.EVT_NUM, OnPeriodChange)
                    periodCtrl.Bind(wx.EVT_TEXT, OnPeriodChange) #Otherwise problem with Dirty flag !
                    periodCtrl.SetValue(int(listRules2[row][2][:-1]))
                    infoSizer=wx.BoxSizer(wx.HORIZONTAL)
                    infoSizer.Add(periodCtrl)
                    choicUnit=[eval("self.text."+tpl) for tpl in self.unitList]
                    unitCtrl=wx.Choice(panel, row+200, choices=choicUnit,size=(81, 22))
                    unitCtrl.SetSelection(int(listRules2[row][2][-1]))
                    unitCtrl.Bind(wx.EVT_CHOICE, OnUnitChoice)
                    infoSizer.Add(unitCtrl,0,wx.LEFT,2)
            self.mySizer.Add(infoSizer,(row,2))
            self.mySizer.Layout()

        def AddRow(x):
#Call from: OnAddButton, Main
            choices=[eval("self.text.Properties."+tpl[0]) for tpl in self.propertiesList]
            propertCtrl=wx.Choice(panel,x+50 , choices=choices,size=(132, 22))
            propertCtrl.Bind(wx.EVT_CHOICE, OnPropertChoice)
            self.mySizer.Add(propertCtrl,(x,0))
            CreateExprCtrl(x)
            CreateStrCtrl(x)
            btnAdd = wx.Button(panel, x, "+",size=(22, 22))
            btnAdd.Bind(wx.EVT_BUTTON,OnAddButton)
            btnRemove = wx.Button(panel, x, "-",size=(22, 22))
            btnRemove.Bind(wx.EVT_BUTTON,OnRemoveButton)
            self.mySizer.Add(btnAdd,(x,3))
            self.mySizer.Add(btnRemove,(x,4),flag=wx.LEFT,border=-10)
            self.mySizer.Layout()

        def UpdateChoiceExpr(row):
#Call from: updateRow, OnPropertChoice
            cnt=self.mySizer.FindItemAtPosition((row,1)).GetWindow().GetCount()
            tp=self.propertiesList[listRules2[row][0]][1]
            myWnd=wx.FindWindowById(row+100)
            if cnt==0 or (tp=="D" and cnt==14) or (tp<>"D" and cnt<>14):
                self.mySizer.Detach(myWnd)
                myWnd.Destroy()
                CreateExprCtrl(row)
            else:
                myWnd.SetSelection(listRules2[row][1])


        def UpdateStr(row):
#Call from: updateRow, OnPropertChoice, OnExprChoice
            infoSizer=self.mySizer.FindItemAtPosition((row,2)).GetSizer()
            lng=len(infoSizer.GetChildren()) # old column 2 type markant
            tp=self.propertiesList[listRules2[row][0]][1]
            tp2=listRules2[row][1]
            flag=False
            #First: Destroy old Ctrl(s)
            if tp=="D":
                if lng==1:
                    rng=(0,)
                    flag=True
                elif lng==2 and tp2<6 :
                    rng=(1,0)
                    flag=True
                elif lng==3 and tp2>5:
                    rng=(2,1,0)
                    flag=True

            else: #tp<>"D"
                if lng==2:
                    rng=(1,0,)
                    flag=True
                elif lng==3:
                    rng=(2,1,0)
                    flag=True
            if flag: #  update panel and value
                for indx in rng:
                    wnd=infoSizer.GetChildren()[indx].GetWindow()
                    infoSizer.Detach(wnd)
                    wnd.Destroy()
                self.mySizer.Detach(infoSizer)
                infoSizer.Destroy()
                #Second: Create new Ctrl(s)
                CreateStrCtrl(row) #Create and update value
            else: # update only value
                val=listRules2[row][2]
                wnd1=wx.FindWindowById(row+150)
                wnd2=wx.FindWindowById(row+200)
                if lng==1:
                    wnd1.SetValue(val)
                    if tp2>11:
                        wnd1.Enable(False)
                    else:
                        wnd1.Enable(True)

                else:
                    if tp2<6: # absolute date/time
                        wnd1.SetValue(ConvToWxDt(val))
                        wnd2.SetValue(val[11:])
                    else: # relative date/time
                        wnd1.SetValue(int(val[:-1]))
                        wnd2.SetSelection(int(val[-1]))
        def updateRow(row):
#Call from: OnAddButton, OnRemoveButton, Main
            wx.FindWindowById(row+50).SetSelection(listRules2[row][0])
            UpdateChoiceExpr(row)
            UpdateStr(row)

        def OnPropertChoice(evt):
            row=evt.GetId()-50
            listRules2[row][0]=wx.FindWindowById(evt.GetId()).GetSelection()
            infoSizer=self.mySizer.FindItemAtPosition((row,2)).GetSizer()
            lng=len(infoSizer.GetChildren()) # old column 2 type markant
            tp=self.propertiesList[listRules2[row][0]][1]
            cnt=self.mySizer.FindItemAtPosition((row,1)).GetWindow().GetCount()
            flg=False
            if tp=="D" and cnt==14: # change to absolute date/time format
                listRules2[row][2]=str(datetime.datetime.today())[:11]+'00:00:00'
                flg=True
            elif tp<>"D" and cnt<>14: #change to no date/time (single column) format
                listRules2[row][2]=""
                flg=True
            if flg: # set selection Expr to "no selection"
                listRules2[row][1]=-1
                wx.FindWindowById(row+100).SetSelection(-1)
            UpdateChoiceExpr(row)
            UpdateStr(row)
            validityCheck()

        def OnExprChoice(evt):
            row=evt.GetId()-100
            value=wx.FindWindowById(evt.GetId()).GetSelection() #
            listRules2[row][1]=value
            #enable=False if value>11 else True
            wnd=wx.FindWindowById(row+150)
            if self.propertiesList[listRules2[row][0]][1]<>"D":
                if value>11:
                    wnd.Enable(False)
                    wnd.Clear()
                else:
                    wnd.Enable(True)
            else: # date/time format
                infoSizer=self.mySizer.FindItemAtPosition((row,2)).GetSizer()
                lng=len(infoSizer.GetChildren())
                if lng==2 and value<6:
                    listRules2[row][2]=str(datetime.datetime.today())[:11]+'00:00:00'
                elif lng==3 and value>5:
                    listRules2[row][2]='13'
                UpdateStr(row)
            validityCheck()

        def OnStrChange(evt):
            row=evt.GetId()-150
            listRules2[row][2]=wx.FindWindowById(evt.GetId()).GetValue()
            validityCheck()

        def OnClndrChange(evt):
            """Event handler for date change."""
            row=evt.GetId()-150
            dt=wx.FindWindowById(evt.GetId()).GetValue()
            listRules2[row][2]=time.strftime('%Y-%m-%d',time.strptime(str(dt),'%d.%m.%Y %H:%M:%S'))+' '+listRules2[row][2][11:]
            validityCheck()

        def OnTimeChange(evt):
            """Event handler for time change."""
            row=evt.GetId()-200
            listRules2[row][2]=listRules2[row][2][:11]+wx.FindWindowById(evt.GetId()).GetValue()
            validityCheck()

        def OnPeriodChange(evt):
            row=evt.GetId()-150
            wnd=wx.FindWindowById(evt.GetId())
            oldVal=listRules2[row][2]
            newVal=wnd.GetValue()
            listRules2[row][2]=str(newVal)+oldVal[-1]
            validityCheck()

        def OnUnitChoice(evt):
            row=evt.GetId()-200
            val=listRules2[row][2]
            listRules2[row][2]=val[:-1]+str(wx.FindWindowById(evt.GetId()).GetSelection())
            validityCheck()

        def OnAddButton(evt):
            """Event handler for the button '+' click."""
            if self.i<maxRules:
                #Insert new record at requested position
                listRules2.insert(evt.GetId()+1,[-1,-1,u""])
                #Create new row (bottom)
                AddRow(self.i)
                self.i+=1
                for x in range(evt.GetId()+1,self.i):
                    updateRow(x)
                self.mySizer.Layout()
                if self.i==2:
                    self.mySizer.FindItemAtPosition((0,4)).GetWindow().Enable(True)
                if self.i==maxRules:
                    for x in range(0,maxRules):
                        self.mySizer.FindItemAtPosition((x,3)).GetWindow().Enable(False)
            panel.EnableButtons(False) #New row is empty => allways not valid

        def OnRemoveButton(evt):
            """Event handler for the button '-' click."""
            CheckEnable=False #validityCheck "OFF"
            row=evt.GetId()
            if self.i>1:
                tp=self.propertiesList[listRules2[self.i-1][0]][1]
                if tp<>"D":
                    rng=(0,)
                else:
                    if listRules2[self.i-1][1]>5:
                        rng=(1,0)
                    else:
                        rng=(2,1,0)
                #Remove last record
                del listRules2[row]
                #Remove last row
                infoSizer=self.mySizer.FindItemAtPosition((self.i-1,2)).GetSizer()
                for indx in rng:
                    wnd=infoSizer.GetChildren()[indx].GetWindow()
                    infoSizer.Detach(wnd)
                    wnd.Destroy()
                self.mySizer.Detach(infoSizer)
                infoSizer.Destroy()
                for col in (0,1,3,4):
                    myWnd=self.mySizer.FindItemAtPosition((self.i-1,col)).GetWindow()
                    self.mySizer.Detach(myWnd)
                    myWnd.Destroy()
                if self.i==maxRules:
                    for x in range(0,maxRules-1):
                        self.mySizer.FindItemAtPosition((x,3)).GetWindow().Enable(True)
                if self.i==2:
                    self.mySizer.FindItemAtPosition((0,4)).GetWindow().Enable(False)
                self.mySizer.Layout()
                self.i-=1
                for x in range(row,self.i):
                    updateRow(x)
            CheckEnable=True #validityCheck "ON"
            validityCheck()

        def OnOrderSwitch(evt=None):
            enbl=orderChkBoxCtrl.GetValue()
            if enbl and critCtrl.GetSelection()==-1:
                critCtrl.SetSelection(wx.FindWindowById(50).GetSelection())
            dirCtrl.Enable(enbl)
            dirTxt1.Enable(enbl)
            dirTxt2.Enable(enbl)
            critCtrl.Enable(enbl)
            if evt is not None:
                validityCheck()

        def OnLimitSwitch(evt=None):
            enbl=limitChkBoxCtrl.GetValue()
            numCtrl.Enable(enbl)
            limitTxt1.Enable(enbl)
            limitTxt2.Enable(enbl)
            if evt is not None:
                validityCheck()

        def OnEventInterception(evt):
            validityCheck()
        radioBoxMode.Bind(wx.EVT_RADIOBOX, OnEventInterception)
        nameCtrl.Bind(wx.EVT_TEXT, OnEventInterception)
        repeatChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnEventInterception)
        shuffleChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnEventInterception)
        crossfadeChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnEventInterception)
        accessibleChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnEventInterception)

        orderChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnOrderSwitch)
        limitChkBoxCtrl.Bind(wx.EVT_CHECKBOX, OnLimitSwitch)
        OnOrderSwitch()
        OnLimitSwitch()

#================================================
        self.i=len(listRules2)
        CheckEnable=False #validityCheck "OFF"
        for x in range(0,len(listRules2)):
            AddRow(x)
            updateRow(x)
        if self.i==1:
            self.mySizer.FindItemAtPosition((0,4)).GetWindow().Enable(False)
        if self.i==maxRules:
            for x in range(0,maxRules):
                self.mySizer.FindItemAtPosition((x,3)).GetWindow().Enable(False)
        if listRules2[0][0]==-1: #For new created empty filter
            panel.EnableButtons(False)
        CheckEnable=True #validityCheck "ON"
        self.myDirty=False


        while panel.Affirmed():
            panel.SetResult(
            nameCtrl.GetValue(),
            radioBoxMode.GetSelection(),
            listRules2,
            orderChkBoxCtrl.GetValue(),
            dirCtrl.GetSelection(),
            critCtrl.GetSelection(),
            limitChkBoxCtrl.GetValue(),
            numCtrl.GetValue(),
            repeatChkBoxCtrl.Get3StateValue(),
            shuffleChkBoxCtrl.Get3StateValue(),
            crossfadeChkBoxCtrl.Get3StateValue(),
            accessibleChkBoxCtrl.GetValue(),
            )

class Jukebox(eg.ActionClass):
    name = "Jukebox"
    description = "Jukebox."
    class text():
        noAlbum = 'No album for ID %s'
        saveButton = "Export album list to file"
        saveTitle = "Save file as ..."
        file = 'File:'
        msgTitle = 'Warning:'
        msgMsg = 'Failed to save the file "%s"\nto the folder "%s" !'
        repeat = "Continous playback"
        shuffle = "Shuffle tracks"
        crossfade = "Crossfade"
        accessible = "Load only accessible tracks"
        baloonBttn = 'Click to export code, album name and album artist to selected file.\nYou can this file import for example to MS Excel or OOo Calc'
        
    def Configure(self,repeat=2,shuffle=2,crossfade=2,accessible=False):
        txt = self.text
        panel = eg.ConfigPanel(self)
        Sizer = panel.sizer
        exportButton = wx.Button(panel, -1, txt.saveButton)
        exportButton.SetToolTip(wx.ToolTip(txt.baloonBttn))
        repeatChkBoxCtrl = wx.CheckBox(panel, label=self.text.repeat,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        shuffleChkBoxCtrl = wx.CheckBox(panel, label=self.text.shuffle,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        crossfadeChkBoxCtrl = wx.CheckBox(panel, label=self.text.crossfade,style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        accessibleChkBoxCtrl = wx.CheckBox(panel, label=self.text.accessible)
        repeatChkBoxCtrl.Set3StateValue(repeat)
        shuffleChkBoxCtrl.Set3StateValue(shuffle)
        crossfadeChkBoxCtrl.Set3StateValue(crossfade)
        accessibleChkBoxCtrl.SetValue(accessible)
        Sizer.Add(repeatChkBoxCtrl)
        Sizer.Add(shuffleChkBoxCtrl,0,wx.TOP,10)
        Sizer.Add(crossfadeChkBoxCtrl,0,wx.TOP,10)
        Sizer.Add(accessibleChkBoxCtrl,0,wx.TOP,10)
        Sizer.Add(exportButton,0,wx.TOP,20)
        def onBtnClick(event):
            MMobj = self.plugin.DispMM()
            import os
            import wx
            dialog = wx.FileDialog(
                panel,
                message=txt.saveTitle,
                defaultDir=eg.folderPath.Documents,         
                defaultFile="AlbumListMM",
                wildcard="CSV files (*.csv)|*.csv|"\
                    "Text file (*.txt)|*.txt|"\
                    "All files (*.*)|*.*",
                style=wx.SAVE
            )            
            dialog.SetFilterIndex(1)
            import codecs
            if dialog.ShowModal() == wx.ID_OK:
                flag = True
                try:
                    filePath = dialog.GetPath()                
                    albums=MMobj.Database.OpenSQL("SELECT ID,Artist,Album FROM Albums")   
                    file = codecs.open(filePath,encoding='utf-8', mode='w',errors='replace')
                    while not albums.EOF:
                        file.write(','.join((str(albums.ValueByIndex(0)),albums.ValueByIndex(2),albums.ValueByIndex(1))))#Structure = ID, Artist, Album
                        file.write('\r\n')
                        albums.Next()
                    file.close()
                except:
                    flag = False
                dialog.Destroy()
                if flag:    
                    file = codecs.open(filePath,encoding='utf-8', mode='r',errors='replace')
                    msg = file.read()
                    file.close()
                    import wx.lib.dialogs
                    dialog = wx.lib.dialogs.ScrolledMessageDialog(panel,msg,txt.file+' '+filePath)
                    dialog.ShowModal()
                    dialog.Destroy()
                else:
                    head, tail = os.path.split(filePath)
                    dialog = wx.MessageDialog(
                        panel,
                        txt.msgMsg % (tail,head),
                        txt.msgTitle,
                        wx.OK | wx.ICON_WARNING
                    )
                    dialog.ShowModal()
                    dialog.Destroy()
            event.Skip()
        exportButton.Bind(wx.EVT_BUTTON, onBtnClick)
        while panel.Affirmed():
            panel.SetResult(
                repeatChkBoxCtrl.Get3StateValue(),
                shuffleChkBoxCtrl.Get3StateValue(),
                crossfadeChkBoxCtrl.Get3StateValue(),
                accessibleChkBoxCtrl.GetValue(),
            )

    def GetLabel(self,repeat=2,shuffle=2,crossfade=2,accessible=False):
        return self.__name__
        

    def __call__(self,repeat=2,shuffle=2,crossfade=2,accessible=False):
        MMobj = self.plugin.DispMM()
        ID=eg.event.payload
        txt = self.text
        sql = 'IDAlbum="%s"' % ID
        Total=MMobj.Database.OpenSQL("SELECT COUNT(*) FROM Songs WHERE "+sql).ValueByIndex(0)
        if int(Total) > 0:
            MMobj.Player.Stop()
            MMobj.Player.PlaylistClear()
            n=0
            MyTrack = MMobj.Database.QuerySongs(sql)
            res = (ID,MyTrack.Item.AlbumName,MyTrack.Item.ArtistName)
            while not MyTrack.EOF:
                if accessible:
                    if isfile(MyTrack.Item.Path):
                        MMobj.Player.PlaylistAddTrack(MyTrack.Item)
                        n+=1
                else:
                    MMobj.Player.PlaylistAddTrack(MyTrack.Item)
                    n+=1
                MyTrack.Next()
            if repeat<2:
                MMobj.Player.isRepeat=bool(repeat)
            if crossfade<2:
                MMobj.Player.isCrossfade=bool(crossfade)
            if shuffle<2:
                MMobj.Player.isShuffle=bool(shuffle)
            MMobj.Player.Play()
            return '\n'.join(res)
        else:
            return txt.noAlbum % ID
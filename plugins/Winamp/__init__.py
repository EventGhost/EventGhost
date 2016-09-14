# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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

# expose some information about the plugin through an eg.PluginInfo subclass
eg.RegisterPlugin(
    name = "Winamp",
    author = (
        "Bitmonster",
        "blackwind",
        "Matthew Jacob Edwards",
        "Sem;colon",
    ),
    version = "1.4.2",
    kind = "program",
    guid = "{4A22DD6A-5E2C-4500-90B4-47F5C58FD9CA}",
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=201",
    description = (
        'Adds actions to control <a href="http://www.winamp.com/">Winamp</a>.'
    ),
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACDElEQVR42pWTT0gUcRTH"
        "P7OQemvKQ7pSbkQgHWLm0k2cgxpUsLOBFUS4UmCBZEuHLsHugBAeLPca4U4RmILsinno"
        "j+SCYLTETiUsRsFuBOpSMoE2SGzbONg6q6vR7/J+vx/v832/937vCeyygsFgcd3qui7s"
        "5CPsBttgYmOvukSCxxtF//ucGdhR4C9cLBZVx0kQEusiyxnd0HrPSuPDM0Qm8kJFga1w"
        "NpsleidES8NL1I6rkBzj8tAXYyhVkLcJuGHTNNEfRPmR1ghfOwo1p2B2hO7HefP+m8Jh"
        "290sE3DDtuXdZIjwuVXE2gNwpAuexdCeVxMZ+5xw10Rww+l0Wn14t4vOEx+Q5CY7ah0U"
        "bJc1D+Z3Ae1ehs7oOLIsl0QEd2RNs597+iPkFsH6DScvwNfX9nkZMnNMr/yCtkcoilIq"
        "7HaBphFY+Qmt3TY4D1Mz4PXAnjUGJ/Io4VkkSdoU2JpCIHCG+HAP0twU5D/BoSrMhW9o"
        "SZGWKwOoqlqCnRTcRTSMFLF+P1L6KeyznKh60iJXf5HeW2FEUSyDy37B690fm7zdHpSs"
        "t3Cwiuz8IlGjEX/PgJOzu6Hcre1sfHU1kXj0fFiyUlBcRRtdYm9bHzdCNzd7vgJcEuho"
        "rn01er1eMYwFQk/MaV/zJaVSK1caKuei/Vh1XG7wKP0vLM0+Dv5jmCpOo2/DZv93nP8A"
        "opkfXpsJ2wUAAAAASUVORK5CYII="
    ),
)


# Now we import some other things we will need later
import math
from threading import Event, Thread
from eg.WinApi import (
    SendMessageTimeout,
    GetWindowText,
    FindWindow,
    WM_COMMAND,
    WM_USER
)
from eg.WinApi.Utils import BringHwndToFront
from time import sleep
global sendWAActive
sendWAActive=False

# Next we define a prototype of an action, with some helper methods

class ActionBase(eg.ActionClass):

    def SendCommand(self, idMessage, wParam, lParam=0):
        """
        Find Winamp's message window and send it a message with
        SendMessageTimeout.
        """
        global sendWAActive
        while sendWAActive:
          sleep(0.1)
        sendWAActive =True
        try:
            hWinamp = FindWindow('Winamp v1.x')
            data = SendMessageTimeout(hWinamp, idMessage, wParam, lParam)
            sendWAActive =False
            return data
        except:
            sendWAActive =False
            raise self.Exceptions.ProgramNotRunning


    def GetPlayingStatus(self):
        """
        Get the current status of Winamp.

        The return value is one of the strings 'playing', 'paused' or 'stopped'.
        """
        iStatus = self.SendCommand(WM_USER, 0, 104)
        if iStatus == 1:
            return 'playing'
        elif iStatus == 3:
            return 'paused'
        else:
            return 'stopped'


    def GetRepeat(self):
        return self.SendCommand(WM_WA_IPC, 0, WA_GETREPEATSTATUS)


    def GetRepeatTrack(self):
        return self.SendCommand(WM_WA_IPC, 0, WA_GETREPTRACKSTATUS)


    def GetShuffle(self):
        return self.SendCommand(WM_WA_IPC, 0, WA_GETSHUFFLESTATUS)


    def GetEQ(self):
        return self.SendCommand(WM_WA_IPC, 11, WA_GETEQDATA)


    def GetEQAutoload(self):
        return self.SendCommand(WM_WA_IPC, 12, WA_GETEQDATA)


    def SetRepeat(self, newVal = None):
        newVal = int(newVal if (1 >= newVal >= 0) else not self.GetRepeat())
        self.SendCommand(WM_WA_IPC, newVal, WA_SETREPEATSTATUS)
        return newVal


    def SetRepeatTrack(self, newVal = None):
        newVal = int(newVal if (1 >= newVal >= 0) else not self.GetRepeatTrack())
        self.SendCommand(WM_WA_IPC, newVal, WA_SETREPTRACKSTATUS)
        return newVal


    def SetShuffle(self, newVal = None):
        newVal = int(newVal if (1 >= newVal >= 0) else not self.GetShuffle())
        self.SendCommand(WM_WA_IPC, newVal, WA_SETSHUFFLESTATUS)
        return newVal


    def SetEQ(self, newVal = 2):
        oldVal=self.GetEQ()
        if newVal==2 and oldVal==0:
          newVal=1
        elif newVal==2:
          newVal=0
        self.SendCommand(WM_WA_IPC, newVal, WA_SETEQDATA)
        return newVal


    def SetEQAutoload(self, newVal = 2):
        oldVal=self.GetEQAutoload()
        if newVal==2 and oldVal==0:
          newVal=1
        elif newVal==2:
          newVal=0
        self.SendCommand(WM_WA_IPC, newVal, WA_SETEQDATA)
        return newVal


# And now we define the actual plugin:

class Winamp(eg.PluginClass):

    class text:
        infoGroupName = "Scripting"
        infoGroupDescription = (
            "Here you find actions that query different aspects of Winamp."
            "They can for example be used to display these informations on a "
            "small LCD/VFD."
        )
        infoGroupEQName = "EQ"
        infoGroupEQDescription = (
            "Here you find actions that change and query Equalizer settings of Winamp."
        )

    def __init__(self):
        self.AddAction(TogglePlay)
        self.AddAction(Play)
        self.AddAction(Pause)
        self.AddAction(DiscretePause)
        self.AddAction(Stop)
        self.AddAction(Fadeout)
        self.AddAction(StopAfterCurrent)
        self.AddAction(PreviousTrack)
        self.AddAction(NextTrack)
        self.AddAction(FastForward)
        self.AddAction(FastRewind)
        self.AddAction(VolumeUp)
        self.AddAction(VolumeDown)
        self.AddAction(Exit)
        self.AddAction(ShowFileinfo)
        self.AddAction(ChooseFile)
        self.AddAction(ExVis)
        self.AddAction(ToggleShuffle, hidden=True)
        self.AddAction(ToggleRepeat, hidden=True)
        self.AddAction(ChangeRepeatStatus)
        self.AddAction(ChangeRepeatTrackStatus)
        self.AddAction(ChangeShuffleStatus)
        self.AddAction(SetVolume)
        self.AddAction(ChangeVolume)
        self.AddAction(SetBalance)
        self.AddAction(JumpToFile)
        self.AddAction(ToggleAlwaysOnTop)
        self.AddAction(JumpToTime)
        self.AddAction(JumpToTrackNr)
        self.AddAction(ClearPlaylist)
        self.AddAction(Command, hidden=True)

        groupEQ = self.AddGroup(
            self.text.infoGroupEQName,
            self.text.infoGroupEQDescription
        )
        groupEQ.AddAction(ChangeEQBand)
        groupEQ.AddAction(ResetAllEQBands)
        groupEQ.AddAction(ChangeEQPreamp)
        groupEQ.AddAction(ChangeEQStatus)
        groupEQ.AddAction(ChangeEQAutoloadStatus)
        groupEQ.AddAction(GetEQBand)
        groupEQ.AddAction(GetEQPreamp)
        groupEQ.AddAction(GetEQStatus)
        groupEQ.AddAction(GetEQAutoloadStatus)


        group = self.AddGroup(
            self.text.infoGroupName,
            self.text.infoGroupDescription
        )
        group.AddAction(GetPlayingSongTitle)
        group.AddAction(GetRepeatStatus)
        group.AddAction(GetRepeatTrackStatus)
        group.AddAction(GetShuffleStatus)
        group.AddAction(GetVolume)
        group.AddAction(GetBalance)
        group.AddAction(GetSampleRate)
        group.AddAction(GetBitRate)
        group.AddAction(GetChannels)
        group.AddAction(GetPosition)
        group.AddAction(GetLength)
        group.AddAction(GetElapsed)
        group.AddAction(GetDuration)
        group.AddAction(GetPlayingStatusNow)

# Here we define a thread for listening to some changes of winamp and trigger events
    def __start__(self):
        self.oldPlaylistLength=u""
        self.oldPlaylistPosition=u""
        self.oldPlayStatus=u""
        self.oldPlayerStatus=2
        self.stopThreadEvent = Event()
        thread = Thread(
            target=self.Receive,
            args=(self.stopThreadEvent, )
        )
        thread.start()

    def __stop__(self):
        self.stopThreadEvent.set()

    def Receive(self, stopThreadEvent):
        while not stopThreadEvent.isSet():
            try:
                tempObject=GetLength()
                newPlaylistLength=unicode(tempObject())
                tempObject=GetPosition()
                newPlaylistPosition=unicode(tempObject())
                tempObject=GetPlayingStatusNow()
                newPlayStatus=unicode(tempObject())
                if self.oldPlayerStatus!=1:
                  self.oldPlayerStatus=1
                  self.TriggerEvent("Status.Changed.On")
                if self.oldPlaylistPosition!=newPlaylistPosition:
                  self.oldPlaylistPosition=newPlaylistPosition
                  self.TriggerEvent("PlayingTrack.Changed",newPlaylistPosition)
                if self.oldPlaylistLength!=newPlaylistLength:
                  self.oldPlaylistLength=newPlaylistLength
                  self.TriggerEvent("PlaylistLength.Changed",newPlaylistLength)
                if self.oldPlayStatus!=newPlayStatus:
                  self.oldPlayStatus=newPlayStatus
                  self.TriggerEvent("Status.Changed."+newPlayStatus)
            except:
                if self.oldPlayerStatus!=0:
                  self.oldPlayerStatus=0
                  self.TriggerEvent("Status.Changed.Off")
            stopThreadEvent.wait(0.5)
# Here we define our first action. Actions are always subclasses of
# ActionBase.

class TogglePlay(ActionBase):
    # We start with a descriptive definition of the member-variables 'name'
    # and 'description'.
    #
    # 'name' is shown as the action's name in the add-action-dialog
    # 'description' is used as a help-string for the user
    name = "Toggle Play"
    description = "Toggles between play and pause of Winamp."

    # Every action should have a __call__ method that will do the actual work
    # of the action.
    def __call__(self):
        if self.GetPlayingStatus() == "stopped":
            # Play
            return self.SendCommand(WM_COMMAND, 40045)
        else:
            # Pause
            return self.SendCommand(WM_COMMAND, 40046)


# The remaining actions all follow the same pattern:
#   1. Define a subclass of ActionBase.
#   2. Add a descriptive 'name' and 'description' member-variable.
#   3. Define a __call__ method, that will do the actual work.


class Play(ActionBase):
    # If we don't define a 'name' member, EventGhost creates one with the
    # class-name as content.
    description = "Simulate a press on the play button."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40045)


class Pause(ActionBase):
    description = "Simulate a press on the pause button."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40046)


class DiscretePause(ActionBase):
    name = "Discrete Pause"
    description = (
        "Pauses Winamp if it is playing, but won't do anything if "
        "Winamp is already paused."
    )

    def __call__(self):
        if self.GetPlayingStatus() == "playing":
            return self.SendCommand(WM_COMMAND, 40046)


class Stop(ActionBase):
    description = "Simulate a press on the stop button."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40047)


class PreviousTrack(ActionBase):
    name = "Previous Track"
    description = "Simulate a press on the previous track button."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40044)


class NextTrack(ActionBase):
    name = "Next Track"
    description = "Simulate a press on the next track button."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40048)


class FastForward(ActionBase):
    name = "Fast Forward"
    description = "Fast-forward 5 seconds."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40148)


class FastRewind(ActionBase):
    name = "Fast Rewind"
    description = "Fast-rewind 5 seconds."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40144)


class Fadeout(ActionBase):
    name = "Stop w/ Fadeout"
    description = "Fade out and stop."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40147)


class VolumeUp(ActionBase):
    name = "Volume Up"
    description = "Raises Winamp's volume by 1%."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40058)


class VolumeDown(ActionBase):
    name = "Volume Down"
    description = "Lower Winamp's volume by 1%."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40059)


class Exit(ActionBase):
    name = "Exit"
    description = "Closes Winamp."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40001)


class ShowFileinfo(ActionBase):
    name = "Show File Info"
    description = "Opens file info box."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40188)


class ChooseFile(ActionBase):
    name = "Choose File"
    description = "Opens the file dialog."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40029)


class ExVis(ActionBase):
    name = "Execute Visualization"
    description = "Execute current visualization plug-in."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40192)


class ToggleShuffle(ActionBase, eg.HiddenAction):
    name = "Toggle Shuffle"
    description = "Toggles Shuffle."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40023)


class ToggleRepeat(ActionBase, eg.HiddenAction):
    name = "Toggle Repeat"
    description = "Toggles Repeat."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40022)


# ===========================================================================
# the following are additional actions added by Matthew Jacob Edwards
# with slight modifications by Bitmonster and Sem;colon
# ===========================================================================

WA_GETSHUFFLESTATUS = 250#1 set, 0 not set
WA_GETREPEATSTATUS  = 251#1 set, 0 not set
WA_SETSHUFFLESTATUS = 252#1 on, 0 off
WA_SETREPEATSTATUS  = 253#1 on, 0 off
WA_REFRESHPLCACHE   = 247
WA_RESTARTWINAMP    = 135
WA_GETREPTRACKSTATUS = 634
WA_SETREPTRACKSTATUS = 635

WA_PLAYFILE         = 100#sent as a WM_COPYDATA, with IPC_PLAYFILE as the dwData, and the string to play as the lpData. Just enqueues, does not clear the playlist or change the playback state
WA_CLEARPLAYLIST    = 101
WA_STARTPLAY        = 102#play
WA_CHDIR            = 103#sent as a WM_COPYDATA, with IPC_CHDIR as the dwData, and the directory to change to as the lpData
WA_ISPLAYING        = 104#1 playing 0 not playing 3 paused
WA_GETOUTPUTTIME    = 105#-1 not playing 0:position in ms 1:length in ms
WA_JUMPTOTIME       = 106#position in ms: -1 not playing, 1 on eof, 0 if successful

WA_WRITEPLAYLIST    = 120#writes the current playlist to <winampdir>\\Winamp.m3u, and returns the current playlist position. Kinda obsoleted by some of the 2.x new stuff, but still good for when using a front-end (instead of a plug-in)
WA_SETTRACK         = 121#choose tracknumber in playlist, you have to tell it you want to play it afterwards
WA_SETVOLUME        = 122#from 0-255
WA_SETBALANCE       = 123#from 0 center, 1-127 right, 255-128 left
WA_GETLISTLENGTH    = 124#returns listlength in tracks
WA_GETLISTPOS       = 125#returns tracknumber of currently playing track
WA_GETINFO          = 126
#Mode      Meaning
#------------------
#0         Samplerate (i.e. 44100)
#1         Bitrate  (i.e. 128)
#2         Channels (i.e. 2)
#3 (5+)    Video LOWORD=w HIWORD=h
#4 (5+)    > 65536, string (video description)
WA_GETEQDATA        = 127
#Value      Meaning
#------------------
#0-9        The 10 bands of EQ data. 0-63 (+20db - -20db)
#10         The preamp value. 0-63 (+20db - -20db)
#11         Enabled. zero if disabled, nonzero if enabled.
#12         Autoload. zero if disabled, nonzero if enabled.
WA_SETEQDATA        = 128#SendMessage(hwnd_winamp,WM_WA_IPC,pos,IPC_GETEQDATA); SendMessage(hwnd_winamp,WM_WA_IPC,value,IPC_SETEQDATA); IPC_SETEQDATA sets the value of the last position retrieved by IPC_GETEQDATA. New (2.92+): if the high byte is set to 0xDB, then the third byte specifies which band, and the bottom word specifies the value.
#eg: self.SendCommand(WM_WA_IPC, 2, WA_GETEQDATA) and then self.SendCommand(WM_WA_IPC, 50, WA_SETEQDATA): sets band 3 to 50
WA_ENQUEUEPLAYLIST  = 129#??
WA_GETPLAYLISTTITLE = 212#?!

WM_USER = 1024
WM_WA_IPC = WM_USER


class ChangeRepeatStatus(ActionBase):
    class text:
        name = "Change Repeat Status"
        description = "Changes the repeat playlist status."
        radioBoxLabel = "Option"
        radioBoxOptions = [
            "Clear Repeat",
            "Set Repeat",
            "Toggle Repeat",
        ]

    def __call__(self, data=0):
        return self.SetRepeat(data)


    def GetLabel(self, data=0):
        return self.plugin.label + ': ' + self.text.radioBoxOptions[data]


    def Configure(self, data=0):
        panel = eg.ConfigPanel()
        radioBox = wx.RadioBox(
            panel,
            label=self.text.radioBoxLabel,
            choices=self.text.radioBoxOptions,
            style=wx.RA_SPECIFY_ROWS
        )
        radioBox.SetSelection(data)
        panel.sizer.Add(radioBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(radioBox.GetSelection())


# The following action is a subclass of ChangeRepeatStatus, so it inherits
# the configuration dialog.

class ChangeRepeatTrackStatus(ChangeRepeatStatus):
    class text:
        name = "Change Repeat Track Status"
        description = "Changes the repeat track status."
        radioBoxLabel = "Option"
        radioBoxOptions = [
            "Clear Repeat Track",
            "Set Repeat Track",
            "Toggle Repeat Track",
        ]


    def __call__(self, data):
        return self.SetRepeatTrack(data)


class ChangeShuffleStatus(ChangeRepeatStatus):
    class text:
        name = "Change Shuffle Status"
        description = "Changes the shuffle status."
        radioBoxLabel = "Option"
        radioBoxOptions = [
            "Clear Shuffle",
            "Set Shuffle",
            "Toggle Shuffle",
        ]


    def __call__(self, data):
        return self.SetShuffle(data)


class GetPlayingSongTitle(ActionBase):
    name = "Get Playing Song Title"
    description = "Gets the currently playing song title."

    def __call__(self):         #-- v2.0
        try:
            hWnd = FindWindow("Winamp v1.x")
        except:
            raise self.Exceptions.ProgramNotRunning
        strWinAmpTitle = GetWindowText(hWnd)
        sx = strWinAmpTitle.split("*** ")
        try:
            strWinAmpTitle = sx[1] + sx[0]
        except:
            pass

        strWinAmpTitle = strWinAmpTitle.replace("*","").strip()
        strWinAmpTitle = strWinAmpTitle.replace(" - Winamp", "")
        strWinAmpTitle = strWinAmpTitle.replace(" [Stopped]", "")
        strWinAmpTitle = strWinAmpTitle.replace(" [Paused]", "")
        strWinAmpTitle = strWinAmpTitle.replace(" [Stopp]", "")
        strWinAmpTitle = strWinAmpTitle.replace(" [Pause]", "")

        decPos = strWinAmpTitle.find(" ") - 1
        if decPos > 0 and strWinAmpTitle[decPos] == "." and strWinAmpTitle[:decPos].isdigit():
            strWinAmpTitle = strWinAmpTitle[decPos + 2:]

        strWinAmpTitle = strWinAmpTitle.strip()
        return strWinAmpTitle


class GetVolume(ActionBase):
    name = "Get Volume Level"
    description = "Gets the volume level as a percentage (%)."

    def __call__(self):
        volume = self.SendCommand(WM_WA_IPC, -666, WA_SETVOLUME)
        if volume is None:
            return
        return math.floor(volume / 2.55)


class SetVolume(ActionBase):
    name = "Set Volume Level"
    description = "Sets the volume to a percentage (%)."
    class text:
        text1 = "Set volume to"
        text2 = "percent."
        label = "Set Volume to %.2f %%"

    def __call__(self, volume):
        self.SendCommand(WM_WA_IPC, int(math.ceil(volume * 2.55)), WA_SETVOLUME)
        return volume


    def GetLabel(self, percentage):
        return self.text.label % percentage


    def Configure(self, percentage=1.0):
        panel = eg.ConfigPanel()
        valueCtrl = panel.SpinNumCtrl(percentage, min=-100, max=100)
        panel.AddLine(self.text.text1, valueCtrl, self.text.text2)
        while panel.Affirmed():
            panel.SetResult(float(valueCtrl.GetValue()))


class ChangeVolume(ActionBase):
    name = "Change Volume Level"
    description = "Changes the volume relative to the current value."
    class text:
        text1 = "Change volume by"
        text2 = "percent."
        label = "Change Volume by %.2f %%"

    def __call__(self, percentage=1.0):
        volume = self.SendCommand(WM_WA_IPC, -666, WA_SETVOLUME)
        if volume is None:
            return
        volume = math.floor(volume / 2.55) + percentage
        if volume < 0.0:
            volume = 0.0
        elif volume > 100.0:
            volume = 100.0
        self.SendCommand(WM_WA_IPC, int(math.ceil(volume * 2.55)), WA_SETVOLUME)
        return volume


    def GetLabel(self, percentage):
        return self.text.label % percentage


    def Configure(self, percentage=1.0):
        panel = eg.ConfigPanel()
        valueCtrl = panel.SpinNumCtrl(percentage, min=-100, max=100)
        panel.AddLine(self.text.text1, valueCtrl, self.text.text2)
        while panel.Affirmed():
            panel.SetResult(float(valueCtrl.GetValue()))



class GetBalance(ActionBase):
    name = "Get Balance Value"
    description = "Gets the balance between right and left chennel in percent (%) right."

    def __call__(self):
        balance = self.SendCommand(WM_WA_IPC, -666, WA_SETBALANCE)
        if balance is None:
            return
        else:
            if balance>128:
                balance-=4294967296
        return math.floor(balance / 1.27)


class SetBalance(ActionBase):
    name = "Set Balance Value"
    description = "Sets the balance to a specific value in percent (%) right."
    class text:
        text1 = "Set balance to"
        text2 = "percent right."
        label = "Set Balance to %.2f %%"

    def __call__(self, balance):
        self.SendCommand(WM_WA_IPC, int(math.ceil(balance * 1.27)), WA_SETBALANCE)
        return balance


    def GetLabel(self, percentage):
        return self.text.label % percentage


    def Configure(self, percentage=0.0):
        panel = eg.ConfigPanel()
        valueCtrl = panel.SpinNumCtrl(percentage, min=-100, max=100)
        panel.AddLine(self.text.text1, valueCtrl, self.text.text2)
        while panel.Affirmed():
            panel.SetResult(float(valueCtrl.GetValue()))



class JumpToTime(ActionBase):
    name = "Jump To Trackposition"
    description = "Jumps to a Trackposition in secounds."
    class text:
        text1 = "Jump to"
        text2 = "secounds."
        label = "Jump to secound "

    def __call__(self, position=0):
        self.SendCommand(WM_WA_IPC, int(position * 1000), WA_JUMPTOTIME)
        return position


    def GetLabel(self, sec):
        return self.text.label+str(sec)


    def Configure(self, sec=0):
        panel = eg.ConfigPanel()
        valueCtrl = panel.SpinNumCtrl(sec, min=0)
        panel.AddLine(self.text.text1, valueCtrl, self.text.text2)
        while panel.Affirmed():
            panel.SetResult(float(valueCtrl.GetValue()))



class JumpToTrackNr(ActionBase):
    name = "Jump To Track Nr"
    description = "Jumps to a specific track number"
    class text:
        text1 = "Jump to track"
        label = "Jump to track number "

    def __call__(self, newtrack):
        self.SendCommand(WM_WA_IPC, newtrack-1, 121)
        play2=Play()
        play2()
        return play2()

    def GetLabel(self, nr):
        return self.text.label+str(nr)

    def Configure(self, nr=1):
        panel = eg.ConfigPanel()
        valueCtrl = panel.SpinIntCtrl(nr, min=1)
        panel.AddLine(self.text.text1, valueCtrl)
        while panel.Affirmed():
            panel.SetResult(int(valueCtrl.GetValue()))



class GetShuffleStatus(ActionBase):
    name = "Get Shuffle Status"
    description = "Gets the shuffle status 1 = shuffle on,  0 = shuffle off."

    def __call__(self):
        return self.SendCommand(WM_WA_IPC, 0, WA_GETSHUFFLESTATUS)



class GetRepeatStatus(ActionBase):
    name = "Get Repeat Status"
    description = "Gets the repeat playlist status: 1 = repeat on, 0 = repeat off."

    def __call__(self):
        return self.GetRepeat()


class GetRepeatTrackStatus(ActionBase):
    name = "Get Repeat Track Status"
    description = "Gets the repeat track status: 1 = repeat track on, 0 = repeat track off."

    def __call__(self):
        return self.GetRepeatTrack()


class GetShuffleStatus(ActionBase):
    name = "Get Shuffle Status"
    description = "Gets the shuffle status: 1 = shuffle on, 0 = shuffle off."

    def __call__(self):
        return self.GetShuffle()


class GetSampleRate(ActionBase):
    name = "Get Sample Rate"
    description = "Gets the sample rate (kHz) of the currently playing song."

    def __call__(self):
        return self.SendCommand(WM_WA_IPC, 0, WA_GETINFO)


class GetBitRate(ActionBase):
    name = "Get Bit Rate"
    description = "Gets the bit rate (kbps) of the currently playing song."

    def __call__(self):
        return self.SendCommand(WM_WA_IPC, 1, WA_GETINFO)


class GetChannels(ActionBase):
    name = "Get Channels"
    description = "Gets the # of channels (mono,stereo) of the currently playing song."

    def __call__(self):
        return self.SendCommand(WM_WA_IPC, 2, WA_GETINFO)


class GetPosition(ActionBase):
    name = "Get Playlist Position"
    description = (
        "Gets the number (position) of the currently playing song within "
        "the playlist."
    )

    def __call__(self):
        intReturn = self.SendCommand(WM_WA_IPC, 0, WA_GETLISTPOS)
        if intReturn is not None:
            return intReturn + 1
        else:
            return None


class GetLength(ActionBase):
    name = "Get Playlist Length"
    description = "Gets the number of songs in the playlist."

    def __call__(self):
        return self.SendCommand(WM_WA_IPC, 0, WA_GETLISTLENGTH)


class GetElapsed(ActionBase):
    name = "Get Song Elapsed"
    description = "Gets the elapsed time, in seconds, into the currently playing song."

    def __call__(self):
        intReturn = self.SendCommand(WM_WA_IPC, 0, WA_GETOUTPUTTIME)
        if intReturn is not None:
            return intReturn / 1000.0
        else:
            return None


class GetDuration(ActionBase):
    name = "Get Song Duration"
    description = "Gets the duration, in seconds, of the currently playing song."

    def __call__(self):
        return self.SendCommand(WM_WA_IPC, 1, WA_GETOUTPUTTIME)


class GetPlayingStatusNow(ActionBase):
    name = "Get Play Status"
    description = "Gets the play status, returns \"playing\", \"paused\" or \"stopped\"."

    def __call__(self):
        return self.GetPlayingStatus()


class JumpToFile(ActionBase):
    name = "Jump to File"
    description = 'Opens and focuses the "Jump to File" window.'

    def __call__(self):
        self.SendCommand(WM_COMMAND, 40194)
        try:
            # Skinned JTFE doesn't auto-focus itself, so let's do that manually
            hwnd = FindWindow("BaseWindow_RootWnd", "Jump to file")
            BringHwndToFront(hwnd)
        except WindowsError:
            pass  # Window not found; user is probably using unskinned JTFE


class StopAfterCurrent(ActionBase):
    name = "Stop After Current"
    description = "Stops playback after the current track."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40157)


class ToggleAlwaysOnTop(ActionBase):
    name = "Toggle Always on Top"
    description = 'Toggles "always on top".'

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40019)


class ClearPlaylist(ActionBase):
    name = "Clear Playlist"
    description = 'Clears the playlist.'

    def __call__(self):
        return self.SendCommand(WM_WA_IPC, 0, WA_CLEARPLAYLIST)


class Command(ActionBase):
    name = "Custom Command"
    description = "Runs a custom command"
    class text:
        text1 = "ID Message:"
        text2 = "wParam:"
        text3 = "lParam:"
        label = "Custom Command: "

    def __call__(self, idMessage=1024, wParam=0, lParam=0):
        return self.SendCommand(idMessage, wParam, lParam)

    def GetLabel(self, idMessage, wParam, lParam):
        return self.text.label+str(idMessage)+","+str(wParam)+","+str(lParam)

    def Configure(self, idMessage=1024, wParam="0", lParam="0"):
        panel = eg.ConfigPanel()
        valueCtrl1 = panel.SpinIntCtrl(idMessage, min=0)
        valueCtrl2 = panel.SpinIntCtrl(wParam, min=0)
        valueCtrl3 = panel.SpinIntCtrl(lParam, min=0)
        panel.AddLine(self.text.text1, valueCtrl1)
        panel.AddLine(self.text.text2, valueCtrl2)
        panel.AddLine(self.text.text3, valueCtrl3)
        while panel.Affirmed():
            panel.SetResult(valueCtrl1.GetValue(),valueCtrl2.GetValue(),valueCtrl3.GetValue())


class ChangeEQBand(ActionBase):
    name = "Change EQ Band"
    description = "Changes the value of one specific EQ Band: -31 = min/-12db, 31 = max/+12db"
    class text:
        text1 = "Band Number:"
        text2 = "New Value:"
        label = "Change EQ Band "

    def __call__(self, band=1, value=0):
        value=int(value)*-1+31
        self.SendCommand(WM_WA_IPC, band-1, WA_GETEQDATA)
        self.SendCommand(WM_WA_IPC, value, WA_SETEQDATA)
        return True

    def GetLabel(self, band, value):
        return self.text.label+str(band)+" to "+str(value)

    def Configure(self, band=1, value=0):
        panel = eg.ConfigPanel()
        valueCtrl1 = panel.SpinIntCtrl(band, min=1, max=10)
        valueCtrl2 = panel.SpinIntCtrl(value, min=-31, max=31)
        panel.AddLine(self.text.text1, valueCtrl1)
        panel.AddLine(self.text.text2, valueCtrl2)
        while panel.Affirmed():
            panel.SetResult(valueCtrl1.GetValue(),valueCtrl2.GetValue())


class ChangeEQPreamp(ActionBase):
    name = "Change EQ Preamplification"
    description = "Changes the EQ preamplification value: -31 = min/-12db, 31 = max/+12db"
    class text:
        text1 = "New Value:"

    def __call__(self, value=0):
        value=int(value)*-1+31
        self.SendCommand(WM_WA_IPC, 10, WA_GETEQDATA)
        self.SendCommand(WM_WA_IPC, value, WA_SETEQDATA)
        return True

    def Configure(self, value=0):
        panel = eg.ConfigPanel()
        valueCtrl = panel.SpinIntCtrl(value, min=-31, max=31)
        panel.AddLine(self.text.text1, valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())


class ResetAllEQBands(ActionBase):
    name = "Reset All EQ Bands"
    description = "Reset all EQ bands to +/-0."

    def __call__(self):
        i=0
        while i<10:
          self.SendCommand(WM_WA_IPC, i, WA_GETEQDATA)
          self.SendCommand(WM_WA_IPC, 31, WA_SETEQDATA)
          i+=1
        return True


class ChangeEQStatus(ChangeRepeatStatus):
    class text:
        name = "Change EQ Status"
        description = "Changes the EQ status."
        radioBoxLabel = "Option"
        radioBoxOptions = [
            "EQ Off",
            "EQ On",
            "Toggle EQ status",
        ]


    def __call__(self, data):
        return self.SetEQ(data)


class ChangeEQAutoloadStatus(ChangeRepeatStatus):
    class text:
        name = "Change EQ Autoload Status"
        description = "Changes the EQ autoload status."
        radioBoxLabel = "Option"
        radioBoxOptions = [
            "EQ autoload Off",
            "EQ autoload On",
            "Toggle EQ autoload status",
        ]


    def __call__(self, data):
        return self.SetEQAutoload(data)

class GetEQStatus(ActionBase):
    name = "Get EQ Status"
    description = "Gets the EQ status: 1 = EQ on, 0 = EQ off."

    def __call__(self):
        return self.GetEQ()


class GetEQAutoloadStatus(ActionBase):
    name = "Get EQ Autoload Status"
    description = "Gets the EQ autoload status: 1 = EQ autoload on, 0 = EQ autoload off."

    def __call__(self):
        return self.GetEQAutoload()


class GetEQBand(ActionBase):
    name = "Get EQ Band Value"
    description = "Gets the value of one specific EQ Band: -31 = min/-12db, 31 = max/+12db"
    class text:
        text1 = "Band Number:"

    def __call__(self, band=1):
        return (int(self.SendCommand(WM_WA_IPC, band-1, WA_GETEQDATA))-31)*-1

    def Configure(self, band=1):
        panel = eg.ConfigPanel()
        valueCtrl = panel.SpinIntCtrl(band, min=1, max=10)
        panel.AddLine(self.text.text1, valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())


class GetEQPreamp(ActionBase):
    name = "Get EQ Preamp Value"
    description = "Gets the EQ preamp value: -31 = min/-12db, 31 = max/+12db"

    def __call__(self):
        return (int(self.SendCommand(WM_WA_IPC, 10, WA_GETEQDATA))-31)*-1


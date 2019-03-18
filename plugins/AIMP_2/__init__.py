# -*- coding: utf-8 -*-
#
# plugins/AIMP_2/__init__.py
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


# expose some information about the plugin through an eg.PluginInfo subclass
eg.RegisterPlugin(
    name = "AIMP_2",
    author = "Sem;colon",
    version = "1.4",
    kind = "program",
    createMacrosOnAdd = True,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=5962",
    guid = "{7B6ABF73-2518-43B1-A7E8-4948D0E1DDD9}",
    description = (
        'Adds actions to control AIMP Player.<br><br>This plugin is based on the Winamp plugin by Bitmonster & blackwind & Matthew Jacob Edwards & Sem;colon and uses window commands.<br>The icon is from the othe AIMP plugin created by Pako.'
    ),
    icon = (
        "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"
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
        Find AIMP's message window and send it a message with
        SendMessageTimeout.
        """
        global sendWAActive
        while sendWAActive:
            sleep(0.1)
        sendWAActive =True
        try:
            hAIMP = FindWindow('Winamp v1.x')
            data = SendMessageTimeout(hAIMP, idMessage, wParam, lParam)
            sendWAActive =False
            return data
        except:
            sendWAActive =False
            raise self.Exceptions.ProgramNotRunning


    def GetPlayingStatus(self):
        """
        Get the current status of AIMP.

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
        tempvar=self.SendCommand(WM_WA_IPC, 0, WA_GETREPEATSTATUS)
        if tempvar>128:
            tempvar=1 #-4294967294
        return tempvar
        
        
    def GetShuffle(self):
        tempvar=self.SendCommand(WM_WA_IPC, 0, WA_GETSHUFFLESTATUS)
        if tempvar>128:
            tempvar=1 #-4294967294
        return tempvar
        
    def GetPosition(self):
        tempvar = self.SendCommand(WM_WA_IPC, 0, WA_GETLISTPOS)
        if tempvar is not None:
            return tempvar + 1
        else:
            return None
            
    def SetRepeat(self, newVal = None):
        newVal = int(newVal if (1 >= newVal >= 0) else not self.GetRepeat())
        self.SendCommand(WM_WA_IPC, newVal, WA_SETREPEATSTATUS)
        return newVal

    def SetShuffle(self, newVal = None):
        newVal = int(newVal if (1 >= newVal >= 0) else not self.GetShuffle())
        self.SendCommand(WM_WA_IPC, newVal, WA_SETSHUFFLESTATUS)
        return newVal


# And now we define the actual plugin:

class Text:
    eventsLabel = "Trigger an event when:"
    polling = "Polling interval (s):"
    eventGenerationBox = "Events triggering"
    events = (
        "Player status changed",
        "Playing track changed",
        "Playlist length changed",
    )
    infoGroupName = "Scripting"
    infoGroupDescription = (
        "Here you find actions that query different aspects of Winamp."
        "They can for example be used to display these informations on a "
        "small LCD/VFD."
    )

class AIMP_2(eg.PluginClass):
    
    text = Text

    def __init__(self):
        self.AddAction(TogglePlay)
        self.AddAction(Play)
        self.AddAction(Pause)
        self.AddAction(DiscretePause)
        self.AddAction(Stop)
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
        self.AddAction(ToggleShuffle, hidden=True)
        self.AddAction(ToggleRepeat, hidden=True)
        self.AddAction(ChangeRepeatStatus)
        self.AddAction(ChangeShuffleStatus)
        self.AddAction(SetVolume)
        self.AddAction(ChangeVolume)
        #self.AddAction(SetBalance)
        self.AddAction(ToggleAlwaysOnTop)
        self.AddAction(JumpToTime)
        self.AddAction(JumpToTrackNr)
        self.AddAction(ClearPlaylist)
        self.AddAction(SavePlaylist)
        self.AddAction(Command, hidden=True)
        
        
        group = self.AddGroup(
            self.text.infoGroupName,
            self.text.infoGroupDescription
        )
        group.AddAction(GetPlayingSongTitle)
        group.AddAction(GetRepeatStatus)
        group.AddAction(GetShuffleStatus)
        group.AddAction(GetVolume)
        #group.AddAction(GetBalance)
        group.AddAction(GetSampleRate)
        group.AddAction(GetBitRate)
        group.AddAction(GetChannels)
        group.AddAction(GetPosition)
        group.AddAction(GetLength)
        group.AddAction(GetElapsed)
        group.AddAction(GetDuration)
        group.AddAction(GetPlayingStatusNow)

# Here we define a thread for listening to some changes of AIMP and trigger events
    def __start__(
        self,
        poll = 1.0,
        events = [True,False,False],
    ):
        self.poll=poll
        self.events = events
        self.oldPlaylistLength=u""
        self.oldPlaylistPosition=u""
        self.oldPlayStatus=u""
        self.oldPlayerStatus=2
        self.oldPlayingSongTitle=u""
        self.stopThreadEvent = Event()
        if events[0] or events[1] or events[2]:
            thread = Thread(
                target=self.Receive,
                args=(self.stopThreadEvent, )
            )
            thread.start()

    def __stop__(self):
        self.stopThreadEvent.set()

    def OnComputerSuspend(self,type=None):
        self.__stop__()
    
    def OnComputerResume(self,type=None):
        self.__start__()
        
    def Receive(self, stopThreadEvent):
        actionObject=ActionBase()
        playingSongTitleObject=GetPlayingSongTitle()
        while not stopThreadEvent.isSet():
            try:
                if self.events[0]:
                    newPlayStatus=actionObject.GetPlayingStatus()
                    if self.oldPlayerStatus!=1:
                        self.oldPlayerStatus=1
                        self.TriggerEvent("Status.Changed.On")
                    if self.oldPlayStatus!=newPlayStatus:
                        self.oldPlayStatus=newPlayStatus
                        self.TriggerEvent("Status.Changed."+newPlayStatus)
                if self.events[1]:
                    newPlaylistPosition=actionObject.GetPosition()
                    newPlayingSongTitle=unicode(playingSongTitleObject())
                    if self.oldPlaylistPosition!=newPlaylistPosition or self.oldPlayingSongTitle!=newPlayingSongTitle:
                        self.oldPlaylistPosition=newPlaylistPosition
                        self.oldPlayingSongTitle=newPlayingSongTitle
                        self.TriggerEvent("PlayingTrack.Changed",[unicode(newPlaylistPosition),newPlayingSongTitle])
                if self.events[2]:
                    newPlaylistLength=actionObject.SendCommand(WM_WA_IPC, 0, WA_GETLISTLENGTH)
                    if self.oldPlaylistLength!=newPlaylistLength:
                        self.oldPlaylistLength=newPlaylistLength
                        self.TriggerEvent("PlaylistLength.Changed",unicode(newPlaylistLength))
            except:
                if self.oldPlayerStatus!=0 and self.events[0]:
                  self.oldPlayerStatus=0
                  self.TriggerEvent("Status.Changed.Off")
            stopThreadEvent.wait(self.poll)
            
    def Configure(
        self,
        poll = 1.0,
        events = [True,False,False],
    ):
        text = self.text
        panel = eg.ConfigPanel()
        panel.GetParent().GetParent().SetIcon(self.info.icon.GetWxIcon())
        pollCtrl = eg.SpinNumCtrl(panel, -1, poll, min=0.1, max=99.0)
        st3 = wx.StaticText(panel,-1, text.polling)
        st4 = wx.StaticText(panel,-1, text.eventsLabel)
        eventsCtrl = wx.CheckListBox(
            panel,
            -1,
            choices = text.events,
            size = ((-1, len(events) * (5+st4.GetSize()[1]))),
        )        
        for i in range(len(events)):
            eventsCtrl.Check(i, events[i])
        box2 = wx.StaticBoxSizer(
            wx.StaticBox(panel, -1, text.eventGenerationBox),
            wx.HORIZONTAL
        )
        leftSizer=wx.FlexGridSizer(2, 2, 10, 5)
        leftSizer.Add(st3,0,wx.TOP,3)
        leftSizer.Add(pollCtrl)
        rightSizer=wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(st4)
        rightSizer.Add(eventsCtrl,0,wx.EXPAND)
        box2.Add(leftSizer,0,wx.TOP,4)
        box2.Add(rightSizer,1,wx.EXPAND|wx.LEFT,20)
        panel.sizer.AddMany([
            (box2, 0, wx.EXPAND|wx.TOP, 10),
        ])
        while panel.Affirmed():
            tmpList = []
            for i in range(len(events)):
                tmpList.append(eventsCtrl.IsChecked(i)) 
            panel.SetResult(
                pollCtrl.GetValue(),
                tmpList
            )
            
# Here we define our first action. Actions are always subclasses of
# ActionBase.

class TogglePlay(ActionBase):
    # We start with a descriptive definition of the member-variables 'name'
    # and 'description'.
    #
    # 'name' is shown as the action's name in the add-action-dialog
    # 'description' is used as a help-string for the user
    name = "Toggle Play"
    description = "Toggles between play and pause of AIMP."

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
        "Pauses AIMP if it is playing, but won't do anything if "
        "AIMP is already paused."
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


class VolumeUp(ActionBase):
    name = "Volume Up"
    description = "Raises AIMP's volume by 1%."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40058)


class VolumeDown(ActionBase):
    name = "Volume Down"
    description = "Lower AIMP's volume by 1%."

    def __call__(self):
        return self.SendCommand(WM_COMMAND, 40059)


class Exit(ActionBase):
    name = "Exit"
    description = "Closes AIMP."

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
WA_REFRESHPLCACHE   = 247#??
WA_RESTARTWINAMP    = 135#??
WA_GETREPTRACKSTATUS = 634#??
WA_SETREPTRACKSTATUS = 635#??

WA_PLAYFILE         = 100#sent as a WM_COPYDATA, with IPC_PLAYFILE as the dwData, and the string to play as the lpData. Just enqueues, does not clear the playlist or change the playback state#??
WA_CLEARPLAYLIST    = 101
WA_STARTPLAY        = 102#play
WA_CHDIR            = 103#sent as a WM_COPYDATA, with IPC_CHDIR as the dwData, and the directory to change to as the lpData
WA_ISPLAYING        = 104#1 playing 0 not playing 3 paused
WA_GETOUTPUTTIME    = 105#-1 not playing 0:position in ms 1:length in ms
WA_JUMPTOTIME       = 106#position in ms: -1 not playing, 1 on eof, 0 if successful 

WA_WRITEPLAYLIST    = 120#writes the current playlist, and returns the current playlist position. Kinda obsoleted by some of the 2.x new stuff, but still good for when using a front-end (instead of a plug-in)
WA_SETTRACK         = 121#choose tracknumber in playlist, you have to tell it you want to play it afterwards
WA_SETVOLUME        = 122#from 0-255
WA_SETBALANCE       = 123#(from 0 center, 1-127 right, 255-128 left) +100
WA_GETLISTLENGTH    = 124#returns listlength in tracks
WA_GETLISTPOS       = 125#returns tracknumber of currently playing track
WA_GETINFO          = 126
#Mode      Meaning
#------------------
#0         Samplerate in kHz (i.e. 44)
#1         Bitrate  (i.e. 128)
#2         Channels (i.e. 2)
WA_GETEQDATA        = 127#??
WA_SETEQDATA        = 128#??
WA_ENQUEUEPLAYLIST  = 129#??
WA_GETPLAYLISTTITLE = 212#??

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
        strAIMPTitle = GetWindowText(hWnd)
        sx = strAIMPTitle.split("*** ")
        try:
            strAIMPTitle = sx[1] + sx[0]
        except:
            pass

        strAIMPTitle = strAIMPTitle.replace("*","").strip()
        strAIMPTitle = strAIMPTitle.replace(" - Winamp", "")
        strAIMPTitle = strAIMPTitle.replace(" [stopped]", "")
        strAIMPTitle = strAIMPTitle.replace(" [paused]", "")
        
        decPos = strAIMPTitle.find(" ") - 1
        if decPos > 0 and strAIMPTitle[decPos] == "." and strAIMPTitle[:decPos].isdigit():
            strAIMPTitle = strAIMPTitle[decPos + 2:]

        strAIMPTitle = strAIMPTitle.strip()
        return strAIMPTitle


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
    description = "Gets the balance between right and left chennel ...Some strange algorithm is used by the media player I don't know how to convert it."

    def __call__(self):
        balance = self.SendCommand(WM_WA_IPC, -666, WA_SETBALANCE)
        return balance

class SetBalance(ActionBase):
    name = "Set Balance Value"
    description = "Sets the balance to a specific value in percent (%) right."
    class text:
        text1 = "Set balance to"
        text2 = "percent right."
        label = "Set Balance to %.2f %%"

    def __call__(self, balance):
        self.SendCommand(WM_WA_IPC, int(round((balance+100) * 1.28 )), WA_SETBALANCE)
        return balance


    def GetLabel(self, percentage):
        return self.text.label % percentage


    def Configure(self, percentage=0):
        panel = eg.ConfigPanel()
        valueCtrl = panel.SpinIntCtrl(percentage, min=-100, max=100)
        panel.AddLine(self.text.text1, valueCtrl, self.text.text2)
        while panel.Affirmed():
            panel.SetResult(int(valueCtrl.GetValue()))            

         
        
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
        return self.SendCommand(WM_WA_IPC, 0, 102)
        
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
        return self.GetPosition()


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

        
class SavePlaylist(ActionBase):
    name = "Save Playlist"
    description = 'Saves the playlist(s) in the profile folder.'

    def __call__(self):
        return self.SendCommand(WM_USER, 0, WA_WRITEPLAYLIST)
        

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
           
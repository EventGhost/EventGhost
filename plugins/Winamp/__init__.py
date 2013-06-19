# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <lpv@eventghost.org> 
#                    and Matthew Jacob Edwards
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
#
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$



# Every plugin code should begin with the import of 'eg'
import eg

# and expose some information about itself through an eg.PluginInfo subclass
class PluginInfo(eg.PluginInfo):
    name = "Winamp"
    author = "Bitmonster and Matthew Jacob Edwards"
    version = "1.0.2"
    kind = "program"
    description = "Adds support functions to control Winamp"
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
    )


# Now we import some other things we will need later
import wx
from win32gui import FindWindow, SendMessageTimeout, GetWindowText
from win32con import WM_COMMAND, WM_USER, SMTO_BLOCK, SMTO_ABORTIFHUNG

# Next we define some helper functions:

def FindWinAMPWindow():
    """
    Find Winamp's message window.
    """
    try:
        hWnd = FindWindow("Winamp v1.x", None)
    except:
        hWnd = None
    return hWnd


def SendCommand(mesg, wParam, lParam=0):
    """
    Find Winamp's message window and send it a message with 
    SendMessageTimeout.
    """
    try:
        hWinamp = FindWindow('Winamp v1.x', None)
        _, result = SendMessageTimeout(
            hWinamp,
            mesg, 
            wParam, 
            lParam, 
            SMTO_BLOCK|SMTO_ABORTIFHUNG,
            2000 # wait at most 2 seconds
        )
        return result
    except:
        eg.PrintError("Winamp is not running")


def GetPlayingStatus():
    """
    Get the current status of Winamp.
    
    The return value is one of the strings 'playing', 'paused' or 'stopped'.
    """
    iStatus = SendCommand(WM_USER, 0, 104)
    if iStatus == 1:
        return 'playing'
    elif iStatus == 3:
        return 'paused'
    else:
        return 'stopped'


# And now we define the actual plugin:

class Winamp(eg.PluginClass):
    
    class text:
        infoGroupName = "Information retrieval"
        infoGroupDescription = (
            "Here you find actions that query different aspects of Winamp."
            "They can for example be used to display these informations on a "
            "small LCD/VFD."
        )
        
    def __init__(self):
        self.AddAction(TogglePlay)
        self.AddAction(Play)
        self.AddAction(Pause)
        self.AddAction(DiscretePause)
        self.AddAction(Stop)
        self.AddAction(PreviousTrack)
        self.AddAction(NextTrack)
        self.AddAction(FastForward)
        self.AddAction(FastRewind)
        self.AddAction(Fadeout)
        self.AddAction(VolumeUp)
        self.AddAction(VolumeDown)
        self.AddAction(Exit)
        self.AddAction(ShowFileinfo)
        self.AddAction(ChooseFile)
        self.AddAction(ExVis)
        self.AddAction(ToggleShuffle, hidden=True)
        self.AddAction(ToggleRepeat, hidden=True)
        self.AddAction(ChangeShuffleStatus)
        self.AddAction(ChangeRepeatStatus)
        self.AddAction(SetVolume)
        
        group = self.AddGroup(
            self.text.infoGroupName, 
            self.text.infoGroupDescription
        )
        group.AddAction(GetPlayingSongTitle)
        group.AddAction(GetShuffleStatus)
        group.AddAction(GetRepeatStatus)
        group.AddAction(GetVolume)
        group.AddAction(GetSampleRate)
        group.AddAction(GetBitRate)
        group.AddAction(GetChannels)
        group.AddAction(GetPosition)
        group.AddAction(GetLength)
        group.AddAction(GetElapsed)
        group.AddAction(GetDuration)
        


# Here we define our first action. Actions are always subclasses of 
# eg.ActionClass.

class TogglePlay(eg.ActionClass):
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
        if GetPlayingStatus() == "stopped":
            # Every action gets a reference to its plugin added on 
            # instantiation, so we can also use other actions of the 
            # plugin here.
            self.plugin.Play()
        else:
            self.plugin.Pause()
    
    
# The remaining actions all follow the same pattern:
#   1. Define a subclass of eg.ActionClass.
#   2. Add a descriptive 'name' and 'description' member-variable.
#   3. Define a __call__ method, that will do the actual work.


class Play(eg.ActionClass):
    # If we don't define a 'name' member, EventGhost creates one with the
    # class-name as content.
    description = "Simulate a press on the play button."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40045)



class Pause(eg.ActionClass):
    description = "Simulate a press on the pause button."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40046)



class DiscretePause(eg.ActionClass):
    name = "Discrete Pause"
    description = (
        "Pauses Winamp if it is playing, but won't do anything if "
        "Winamp is already paused."
    )
    
    def __call__(self):
        if GetPlayingStatus() == "playing":
            return SendCommand(WM_COMMAND, 40046)



class Stop(eg.ActionClass):
    description = "Simulate a press on the stop button."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40047)



class PreviousTrack(eg.ActionClass):
    name = "Previous Track"
    description = "Simulate a press on the previous track button."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40044)



class NextTrack(eg.ActionClass):
    name = "Next Track"
    description = "Simulate a press on the next track button."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40048)



class FastForward(eg.ActionClass):
    name = "Fast Forward"
    description = "Fast-forward 5 seconds."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40148)



class FastRewind(eg.ActionClass):
    name = "Fast Rewind"
    description = "Fast-rewind 5 seconds."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40144)



class Fadeout(eg.ActionClass):
    name = "Fadeout"
    description = "Fade out and stop."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40147)



class VolumeUp(eg.ActionClass):
    name = "Volume Up"
    description = "Raises Winamp's volume by 1%."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40058)



class VolumeDown(eg.ActionClass):
    name = "Volume Down"
    description = "Lower Winamp's volume by 1%."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40059)



class Exit(eg.ActionClass):
    name = "Exit"
    description = "Closes Winamp."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40001)



class ShowFileinfo(eg.ActionClass):
    name = "Show File Info"
    description = "Opens file info box."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40188)



class ChooseFile(eg.ActionClass):
    name = "Choose File"
    description = "Opens the file dialog."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40029)



class ExVis(eg.ActionClass):
    name = "Execute Visualisation"
    description = "Execute current visualization plug-in."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40192)



class ToggleShuffle(eg.ActionClass, eg.HiddenAction):
    name = "Toggle Shuffle"
    description = "Toggles Shuffle."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40023)



class ToggleRepeat(eg.ActionClass, eg.HiddenAction):
    name = "Toggle Repeat"
    description = "Toggles Repeat."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 40022)



# ===========================================================================
# the following are additional actions added by Matthew Jacob Edwards
# with slight modifications by Bitmonster
# ===========================================================================

WA_GETSHUFFLESTATUS = 250
WA_GETREPEATSTATUS  = 251
WA_SETSHUFFLESTATUS = 252
WA_SETREPEATSTATUS  = 253
WA_REFRESHPLCACHE   = 247
WA_RESTARTWINAMP    = 135

WA_PLAYFILE         = 100
WA_CLEARPLAYLIST    = 101
WA_STARTPLAY        = 102
WA_ISPLAYING        = 104
WA_GETOUTPUTTIME    = 105
WA_JUMPTOTIME       = 106

WA_WRITEPLAYLIST    = 120
WA_SETTRACK         = 121
WA_SETVOLUME        = 122
WA_SETBALANCE       = 123
WA_GETLISTLENGTH    = 124
WA_GETLISTPOS       = 125
WA_GETINFO          = 126
WA_GETEQDATA        = 127
WA_ENQUEUEPLAYLIST  = 129
WA_GETPLAYLISTTITLE = 212

WM_USER = 1024
WM_WA_IPC = WM_USER



class ChangeRepeatStatus(eg.ActionClass):
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
        if data == 2:
            return SendCommand(WM_COMMAND, 40022)
        else:
            return SendCommand(WM_WA_IPC, int(data), WA_SETREPEATSTATUS)


    def GetLabel(self, data=0):
        return self.plugin.label + ': ' + self.text.radioBoxOptions[data]


    def Configure(self, data=0):
        dialog = eg.ConfigurationDialog(self)
        radioBox = wx.RadioBox(
            dialog, 
            label=self.text.radioBoxLabel,
            choices=self.text.radioBoxOptions,
            style=wx.RA_SPECIFY_ROWS 
        )
        radioBox.SetSelection(data)
        dialog.sizer.Add(radioBox, 0, wx.EXPAND)
        if dialog.AffirmedShowModal():
            return (radioBox.GetSelection(), )
        
        
# The following action is a subclass of ChangeRepeatStatus, so it inherits
# the configuration dialog.
        
class ChangeShuffleStatus(ChangeRepeatStatus):
    class text:
        name = "Change Shuffel Status"
        description = "Changes the shuffle status."
        radioBoxLabel = "Option"
        radioBoxOptions = [
            "Clear Shuffle", 
            "Set Shuffle",
            "Toggle Shuffle", 
        ]
        
    def __call__(self,data):
        if data == 2:
            return SendCommand(WM_COMMAND, 40023)
        else:
            return SendCommand(WM_WA_IPC, int(data), WA_SETSHUFFLESTATUS)


        
class SetVolume(eg.ActionWithStringParameter):
    name = "Set Volume Level"
    description = "Sets the volume to a percentage (%)."
    
    def __call__(self, volume):
        return SendCommand(WM_WA_IPC, (int(volume)*255)/100, WA_SETVOLUME)


    def Configure(self, volume=100.0):
        dialog = eg.ConfigurationDialog(self)
        volumeCtrl = eg.SpinNumCtrl(dialog, -1, volume, max=100.0)
        dialog.AddLabel("Volume Level:")
        dialog.AddCtrl(volumeCtrl)
        if dialog.AffirmedShowModal():
            return (volumeCtrl.GetValue(), )
        
        
        
class GetPlayingSongTitle(eg.ActionClass):
    name = "Get Currently Playing Song Title"
    description = "Gets the currently playing song title."
    
    def __call__(self):         #-- v2.0
        strWinAmpTitle = ""
        hWnd = FindWinAMPWindow()
        if ( hWnd is not None ):
            strWinAmpTitle = GetWindowText(hWnd)
        sx = strWinAmpTitle.split("*** ")
        try:
            strWinAmpTitle = sx[1] + sx[0]
        except:
            pass
        
        strWinAmpTitle = strWinAmpTitle.replace("*","").strip()
        strWinAmpTitle = strWinAmpTitle.replace(" - Winamp", "")
        strWinAmpTitle = strWinAmpTitle.replace("[Stopped]", "")
        strWinAmpTitle = strWinAmpTitle.replace("[Paused]", "")

        strWinAmpTitle = strWinAmpTitle[strWinAmpTitle.find(" ") + 1:len(strWinAmpTitle)].strip()
        return strWinAmpTitle        
        
        
        
class GetVolume(eg.ActionClass):
    name = "Get Volume Level"
    description = "Gets the volume level as a percentage (%)."
    
    def __call__(self):
        intReturn = SendCommand(WM_WA_IPC, -666, WA_SETVOLUME)
        if intReturn is not None:
            return ((intReturn * 100.0) / 255)
        else:
            return None

        
        
class GetShuffleStatus(eg.ActionClass):
    name = "Get Shuffle Status"
    description = "Gets the shuffle status 1 = shuffle on,  0 = shuffle off."
    
    def __call__(self):
        return SendCommand(WM_WA_IPC, 0, WA_GETSHUFFLESTATUS)

      
            
class GetRepeatStatus(eg.ActionClass):
    name = "Get Repeat Status"
    description = "Gets the repeat playlist status 1 = repeat on,  0 = repeat off."
    
    def __call__(self):
        return SendCommand(WM_WA_IPC, 0, WA_GETREPEATSTATUS)



class GetSampleRate(eg.ActionClass):
    name = "Get Sample Rate"
    description = "Gets the sample rate (khz) of the currently playing song."
    
    def __call__(self):
        return SendCommand(WM_WA_IPC, 0, WA_GETINFO)

        
        
class GetBitRate(eg.ActionClass):
    name = "Get Bit Rate"
    description = "Gets the bit rate (kbps) of the currently playing song."
    
    def __call__(self):
        return SendCommand(WM_WA_IPC, 1, WA_GETINFO)

        
        
class GetChannels(eg.ActionClass):
    name = "Get Channels"
    description = "Gets the # of channels (mono,stereo) of the currently playing song."
    
    def __call__(self):
        return SendCommand(WM_WA_IPC, 2, WA_GETINFO)

        
        
class GetPosition(eg.ActionClass):
    name = "Get Playlist Position"
    description = (
        "Gets the number (position) of the currently playing song within "
        "the playlist."
    )

    def __call__(self):
        intReturn = SendCommand(WM_WA_IPC, 0, WA_GETLISTPOS)
        if intReturn is not None:
            return intReturn + 1 
        else:
            return None

        
        
class GetLength(eg.ActionClass):
    name = "Get Playlist Length"
    description = "Gets the number of songs in the playlist."
    
    def __call__(self):
        return SendCommand(WM_WA_IPC, 0, WA_GETLISTLENGTH)

        
        
class GetElapsed(eg.ActionClass):
    name = "Get Song Elapsed"
    description = "Gets the elapsed time, in seconds, into the currently playing song."
    
    def __call__(self):
        intReturn = SendCommand(WM_WA_IPC, 0, WA_GETOUTPUTTIME)
        if intReturn is not None:
            return intReturn / 1000.0
        else:
            return None

        
        
class GetDuration(eg.ActionClass):
    name = "Get Song Duration"
    description = "Gets the duration, in seconds, of the currently playing song."
    
    def __call__(self):
        return SendCommand(WM_WA_IPC, 1, WA_GETOUTPUTTIME)

        



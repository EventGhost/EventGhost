#
# Plugins/WMPlayer/__init__.py
#
# Copyright (C) 2007 Oystein Hansen
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


# Every plugin code should begin with the import of 'eg'
import eg

eg.RegisterPlugin(
    name = "Windows Media Player",
    author = "Oystein Hansen",
    version = "0.1." + "$LastChangedRevision$".split()[1],
    kind = "program",
    description = (
        'Adds actions to control the '
        '<a href="http://www.microsoft.com/windows/windowsmedia/">'
        'Windows Media Player</a>.'
    ),
)

# Now we import some other things we will need later
import wx
from win32gui import FindWindow, SendMessageTimeout, GetWindowText
from win32con import WM_COMMAND, WM_USER, SMTO_BLOCK, SMTO_ABORTIFHUNG

# Next we define some helper functions:

def SendCommand(mesg, wParam, lParam=0):
    """
    Find WMPlayer's message window and send it a message with 
    SendMessageTimeout.
    """
    try:
        hWMP = FindWindow('WMPlayerApp', None)
        _, result = SendMessageTimeout(
            hWMP,
            mesg, 
            wParam, 
            lParam, 
            SMTO_BLOCK|SMTO_ABORTIFHUNG,
            2000 # wait at most 2 seconds
        )
        return result
    except:
        eg.PrintError("WMPlayer is not running")


# And now we define the actual plugin:

class WMPlayer(eg.PluginClass):
         
    def __init__(self):
        self.AddAction(TogglePlay)
        self.AddAction(Stop)
        self.AddAction(PreviousTrack)
        self.AddAction(NextTrack)
        self.AddAction(FastForward)
        self.AddAction(FastRewind)
        self.AddAction(VolumeUp)
        self.AddAction(VolumeDown)
        self.AddAction(Exit)
        self.AddAction(ToggleShuffle, hidden=True)
        self.AddAction(ToggleRepeat, hidden=True)
        
       


# Here we define our first action. Actions are always subclasses of 
# eg.ActionClass.

# The remaining actions all follow the same pattern:
#   1. Define a subclass of eg.ActionClass.
#   2. Add a descriptive 'name' and 'description' member-variable.
#   3. Define a __call__ method, that will do the actual work.


class TogglePlay(eg.ActionClass):
    name = "Toggle Play"
    description = "Simulate a press on the play / pause button."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 18808)



class Stop(eg.ActionClass):
    description = "Simulate a press on the stop button."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 18809)



class PreviousTrack(eg.ActionClass):
    name = "Previous Track"
    description = "Simulate a press on the previous track button."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 18810)



class NextTrack(eg.ActionClass):
    name = "Next Track"
    description = "Simulate a press on the next track button."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 18811)



class FastForward(eg.ActionClass):
    name = "Fast Forward"
    description = "Fast-forward."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 18813)



class FastRewind(eg.ActionClass):
    name = "Fast Rewind"
    description = "Fast-rewind."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 39)



class VolumeUp(eg.ActionClass):
    name = "Volume Up"
    description = "Raises WMPlayer's volume by 5%."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 18815)



class VolumeDown(eg.ActionClass):
    name = "Volume Down"
    description = "Lower WMPlayer's volume by 5%."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 18816)



class Exit(eg.ActionClass):
    name = "Exit"
    description = "Closes WMPlayer."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 57665)



class ToggleShuffle(eg.ActionClass, eg.HiddenAction):
    name = "Toggle Shuffle"
    description = "Toggles Shuffle."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 18842)



class ToggleRepeat(eg.ActionClass, eg.HiddenAction):
    name = "Toggle Repeat"
    description = "Toggles Repeat."
    
    def __call__(self):
        return SendCommand(WM_COMMAND, 18843)


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



# This is the list of actions we want to produce:
ACTIONS = (
    ("TogglePlay", "Toggle Play", "Simulate a press on the play / pause button.", 18808),
    ("Stop", "Stop", "Simulate a press on the stop button.", 18809),
    ("PreviousTrack", "Previous Track", "Simulate a press on the previous track button.", 18810),
    ("NextTrack", "Next Track", "Simulate a press on the next track button.", 18811),
    ("FastForward", "Fast Forward", "Fast-forward.", 18813),
    ("FastRewind", "Rewind", "Rewind.", 18812),
    ("VolumeUp", "Volume Up", "Raises WMPlayer's volume by 5%.", 18815),
    ("VolumeDown", "Volume Down", "Lower WMPlayer's volume by 5%.", 18816),
    ("Exit", "Exit", "Closes Windows Media Player.", 57665),
    ("ToggleShuffle", "Toggle Shuffle", "Toggles Shuffle.", 18842),
    ("ToggleRepeat", "Toggle Repeat", "Toggles Repeat.", 18843),
)


# Now we import some other things we will need later
from win32gui import FindWindow, SendMessageTimeout
from win32con import WM_COMMAND, SMTO_BLOCK, SMTO_ABORTIFHUNG


# Next we define a prototype for all actions, because they all work the same
# way

class ActionPrototype(eg.ActionClass):

    def __call__(self):
        """
        Find WMPlayer's message window and send it a message with 
        SendMessageTimeout.
        """
        try:
            hWMP = FindWindow('WMPlayerApp', None)
            _, result = SendMessageTimeout(
                hWMP, # the window handle
                WM_COMMAND, # the message number
                self.data, # the lParam value
                0, # the wParam value
                SMTO_BLOCK|SMTO_ABORTIFHUNG,
                2000 # wait at most 2 seconds
            )
            return result
        except:
            self.PrintError("Windows Media Player is not running")


# And now we define the actual plugin:

class WMPlayer(eg.PluginClass):
         
    def __init__(self):
        for clsName, actionName, actionDescription, actionData in ACTIONS:
            class TmpAction(ActionPrototype):
                name = actionName
                description = actionDescription
                data = actionData
            TmpAction.__name__ = clsName
            self.AddAction(TmpAction)
        

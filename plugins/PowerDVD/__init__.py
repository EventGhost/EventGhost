# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
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

import eg

eg.RegisterPlugin(
    name="CyberLink PowerDVD",
    description="Adds actions to control CyberLink PowerDVD 7 and 8.",
    kind="program",
    author="Bitmonster",
    version="1.1." + "$LastChangedRevision$".split()[1],  
    createMacrosOnAdd=True,  
)

ACTIONS = [
    ("Play", "Play", "Plays media.", "{Return}"),
    ("Pause", "Pause", "Pauses playback.", "{Space}"),
    ("Stop", "Stop", "Stops playback.", "s"),
    ("Menu", "Menu", "Accesses all available DVD menus.", "l"),
    ("PreviousChapter", "Previous chapter", "Returns to previous chapter.", "p"),
    ("NextChapter", "Next chapter", "Jumps to next chapter.", "n"),
    ("StepBackward", "Step backward", "Goes to previous frame.", "e"),
    ("StepForward", "Step forward", "Goes to next frame.", "t"),
    ("ToggleFullscreen", "Toggle fullscreen", "Toggles between fullscreen and window mode.", "z"),
    ("ToggleMute", "Toggle mute", "Mute volume.", "q"),
    ("VolumeUp", "Volume up", "Increase volume.", "+"),
    ("VolumeDown", "Volume down", "Decrease volume.", "-"),
    ("NextAudioStream", "Next audio stream", "Switches among available audio streams.", "h"),
    ("NextSubtitle", "Next subtitle", "Switches among available subtitles during playback.", "u"),
    ("NextAngel", "Next angel", "Switches among available angles if any.", "a"),
    ("SayItAgain", "Say-It-Again", "Repeats the last dialog.", "w"),
    ("SeeItAll", "See-It-All", "Activates See-It-All function, refer to Blu-ray Disc Configuration.", "{LCtrl+S}"),
    ("CaptureFrame", "Capture frame", "Captures video content as bitmap image files. (Not supported during HD DVD and Blu-ray Disc playback.)", "c"),
    ("NavigationUp", "Navigation Up", "Navigates through disc menus.", "{Up}"),
    ("NavigationDown", "Navigation Down", "Navigates through disc menus.", "{Down}"),
    ("NavigationLeft", "Navigation Left", "Navigates through disc menus.", "{Left}"),
    ("NavigationRight", "Navigation Right", "Navigates through disc menus.", "{Right}"),
    ("NavigationEnter", "Navigation Enter", "Navigates through disc menus. (Has actually the same function as the Play action.)", "{Return}"),
    ("Close", "Close", "Close PowerDVD.", "{Ctrl+x}"),
]


gWindowMatcher = eg.WindowMatcher('PowerDVD{*}.exe', 'CyberLink PowerDVD{*}')


class ActionPrototype(eg.ActionBase):
    
    def __call__(self):
        hwnds = gWindowMatcher()
        if hwnds:
            eg.SendKeys(hwnds[0], self.value)
        else:
            raise self.Exceptions.ProgramNotRunning
        
        
        
class PowerDvd(eg.PluginBase):
    
    def __init__(self):
        self.AddActionsFromList(ACTIONS, ActionPrototype)
            
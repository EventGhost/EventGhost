# This file is part of EventGhost.
# Copyright (C) 2008 Lars-Peter Voss <bitmonster@eventghost.org>
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
# $LastChangedDate: 2008-05-23 16:00:02 +0200 (Fr, 23 Mai 2008) $
# $LastChangedRevision: 420 $
# $LastChangedBy: bitmonster $

eg.RegisterPlugin(
    name="Sceneo TVcentral",
    kind="program",
    author="Bitmonster",
    createMacrosOnAdd = True,
    version="1.0." + "$LastChangedRevision: 420 $".split()[1],
)

ACTIONS = (
    ("Num0", "Number 0", None, 0),
    ("Num1", "Number 1", None, 1),
    ("Num2", "Number 2", None, 2),
    ("Num3", "Number 3", None, 3),
    ("Num4", "Number 4", None, 4),
    ("Num5", "Number 5", None, 5),
    ("Num6", "Number 6", None, 6),
    ("Num7", "Number 7", None, 7),
    ("Num8", "Number 8", None, 8),
    ("Num9", "Number 9", None, 9),
    ("Ok", "Ok", None, 10),
    ("Up", "Up", None, 11),
    ("Down", "Down", None, 12),
    ("Left", "Left", None, 13),
    ("Right", "Right", None, 14),
    ("Play", "Play", None, 15),
    ("Pause", "Pause", None, 16),
    ("Stop", "Stop", None, 17),
    ("Record", "Record", None, 18),
    ("Previous", "Previous", None, 19),
    ("Rewind", "Rewind", None, 20),
    ("Forward", "Forward", None, 21),
    ("Next", "Next", None, 22),
    ("Red", "Red", None, 23),
    ("Green", "Green", None, 24),
    ("Yellow", "Yellow", None, 25),
    ("Blue", "Blue", None, 26),
    ("ChannelUp", "Channel Up", None, 27),
    ("ChannelDown", "Channel Down", None, 28),
    ("VolumeUp", "Volume Up", None, 29),
    ("VolumeDown", "Volume Down", None, 30),
    ("Menu", "Menu", None, 31),
    ("Back", "Back", None, 32),
    ("Exit", "Exit", None, 33),
    ("Power", "Power", None, 34),
    ("Mute", "Mute", None, 35),
    ("Info", "Info", None, 36),
    ("Home", "Home", None, 37),
    ("AV", "AV", None, 38),
    ("PiP", "PiP", None, 39),
    ("Aspect", "Aspect", None, 40),
    ("Teletext", "Teletext", None, 41),
    ("Pictures", "Pictures", None, 42),
    ("Videos", "Videos", None, 43),
    ("Music", "Music", None, 44),
    ("Radio", "Radio", None, 45),
    ("TV", "TV", None, 46),
    ("DVD", "DVD", None, 47),
    ("EPG", "EPG", None, 48),
    ("Recordings", "Recordings", None, 49),
    ("PreviousChannel", "Previous Channel", None, 50),
    ("Subtitle", "Subtitle", None, 51),
    ("Fullscreen", "Fullscreen", None, 52),
    ("Language", "Language", None, 53),
    ("Shuffle", "Shuffle", None, 54),
    ("Repeat", "Repeat", None, 55),
)


from eg.WinApi import FindWindow, SendMessageTimeout, WM_COMMAND


class ActionPrototype(eg.ActionClass):
    
    def __call__(self):
        try:
            hWnd = FindWindow("TVcCore-RemoteMSG-Class")
            return SendMessageTimeout(hWnd, WM_COMMAND, self.value, 0)
        except:
            raise self.Exceptions.ProgramNotRunning
    


class TVcentral(eg.PluginClass):

    def __init__(self):
        self.AddActionsFromList(ACTIONS, ActionPrototype)


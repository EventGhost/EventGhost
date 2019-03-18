# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
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
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Changelog
# 1.0 Bitmonster
#       - initial release
# 1.1 Wiedmann
#       - correct MediaPortal Message Plugin URL
#       - add EG support URL
#       - group/name actions like in MediaPortal
#       - remove not existing actions
#       - add missing actions
#

import eg

eg.RegisterPlugin(
    name="MediaPortal",
    kind="program",
    author="Bitmonster & Carsten Wiedmann",
    version="1.1",
    guid="{50B10A24-77AC-4248-85E5-16A04983170E}",
    createMacrosOnAdd=True,
    description=(
        "Adds actions to control <a href='http://www.team-mediaportal.com/'>"
        "MediaPortal</a>."
    ),
    url="http://www.eventghost.org/forum/viewtopic.php?f=4&amp;t=3171",
    help=(
        "<b>Note:</b> You have to install and enable this "
        "<a href='http://www.team-mediaportal.com/extensions/input-output/"
        "message-plugin-for-mp1-2'>"
        "Message Plugin</a> inside MediaPortal. Please follow the supplied "
        "installation instructions in the ReadMe to accomplish this."
    ),
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAA7DAAAOwwHH"
        "b6hkAAABmUlEQVR4nNXSv08acRgG8EfCkUsOXNqpcSIm/iB26kCThqmL8eYb5CKKDCSM"
        "xvRvkKXYEIYGriecyH1PTuUSOSOogySYeHGD2EkcGItjmxTeTjRNWwKrT/IuT558phd4"
        "/qnXay/b7XbRcZxLw2Dvh/3jYyfmOLc3jnObFkWRB4BO5yHSbDa/NhrXD43G9TYAoNVq"
        "fTYMRozpVC6Xv/l8vmlNK/jPzuw+YzodHhoUiax9yGazb6rV0/7JyTFZlkVHRyZJkrQK"
        "267WGdNpeIIgLKiqGjLN8u9OlmU1lfq4ZRiMut0u9Xo9YkynWGxTQ6VSuRgOdV0nQRAW"
        "FUX5CwjnJUlaNk1zYNtVqtXOqVjcp1AotDMxwPO8OxqNZvL5vR+Kkvspy+Erl8s1NzEA"
        "YAoAx3HcksfjeQfgFQDAsv4H5EYB/0bTCqXhUFW/fHe73bPxeDxgWZUBYzqVSgckiivp"
        "kUAgsPg6mUze7+6mnoLBYBqA1+v1Tm1srH/KZDJPiUTijuf5t+P+6QWAeQDTf3QcAD+A"
        "GQCuccAzzi8I4xbYMZHNnQAAAABJRU5ErkJggg=="
    )
)

ACTIONS_MCE = [
    ("PowerTV", "Power TV", None, 101),
    ("Record", "Record", None, 23),
    ("Stop", "Stop", None, 25),
    ("Pause", "Pause", None, 24),
    ("Rewind", "Rewind", None, 21),
    ("Play", "Play", None, 22),
    ("Forward", "Forward", None, 20),
    ("Replay", "Replay", None, 27),
    ("Skip", "Skip", None, 26),
    ("Back", "Back", None, 35),

    ("Info", "Info", None, 15),
    ("VolumeUp", "Volume +", None, 16),
    ("VolumeDown", "Volume -", None, 17),
    ("Start", "Start", None, 13),
    ("ChannelUp", "Channel Up", None, 18),
    ("ChannelDown", "Channel Down", None, 19),
    ("Mute", "Mute", None, 14),
    ("RecordedTV", "Recorded TV", None, 72),

    ("Guide", "Guide", None, 38),
    ("LiveTV", "Live TV", None, 37),
    ("DVDMenu", "DVD Menu", None, 36)
]

ACTIONS_REPLACEMENT = [
    ("PowerPC", "Power PC", None, 12),
    ("Up", "Up", None, 30),
    ("Down", "Down", None, 31),
    ("Left", "Left", None, 32),
    ("Right", "Right", None, 33),
    ("Ok", "Ok", None, 34),
    ("1", "1", None, 1),
    ("2", "2", None, 2),
    ("3", "3", None, 3),
    ("4", "4", None, 4),
    ("5", "5", None, 5),
    ("6", "6", None, 6),
    ("7", "7", None, 7),
    ("8", "8", None, 8),
    ("9", "9", None, 9),
    ("0", "0", None, 0),
    ("Asterisk", "*", None, 29),
    ("NumberSign", "#", None, 28),
    ("Clear", "Clear", None, 10),
    ("Enter", "Enter", None, 11)
]

ACTIONS_TELETEXT = [
    ("Teletext", "Teletext", None, 90),
    ("Red", "Red", None, 91),
    ("Green", "Green", None, 92),
    ("Yellow", "Yellow", None, 93),
    ("Blue", "Blue", None, 94)
]

ACTIONS_EXTENDED = [
    ("MyTV", "My TV", None, 70),
    ("MyMusic", "My Music", None, 71),
    ("MyPictures", "My Pictures", None, 73),
    ("MyVideos", "My Videos", None, 74),
    ("MyRadio", "My Radio", None, 80),
    ("AspectRatio", "Aspect Ratio", None, 39),
    ("Print", "Print", None, 78)
]

from eg.WinApi import SendMessageTimeout

gWindowMatcher = eg.WindowMatcher("MediaPortal.exe")


class ActionPrototype(eg.ActionBase):

    def __call__(self):
        try:
            hwnd = gWindowMatcher()[0]
            return SendMessageTimeout(hwnd, 32768, 24, self.value)
        except:
            raise self.Exceptions.ProgramNotRunning


class MediaPortal(eg.PluginBase):

    def __init__(self):
        GroupMce = self.AddGroup("Microsoft MCE Remote")
        GroupMce.AddActionsFromList(
            ACTIONS_MCE, ActionPrototype
        )

        GroupReplacement = self.AddGroup("Replacement driver buttons")
        GroupReplacement.AddActionsFromList(
            ACTIONS_REPLACEMENT, ActionPrototype
        )

        GroupTeletext = self.AddGroup("Teletext specific buttons")
        GroupTeletext.AddActionsFromList(
            ACTIONS_TELETEXT, ActionPrototype
        )

        GroupExtended = self.AddGroup("Extended buttons")
        GroupExtended.AddActionsFromList(
            ACTIONS_EXTENDED, ActionPrototype
        )

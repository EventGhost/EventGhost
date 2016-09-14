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

import eg

eg.RegisterPlugin(
    name = "MediaPortal",
    kind = "program",
    author = "Bitmonster",
    version = "1.0",
    guid = "{50B10A24-77AC-4248-85E5-16A04983170E}",
    createMacrosOnAdd = True,
    description = (
        "Adds actions to control <a href='http://www.team-mediaportal.com/'>"
        "MediaPortal</a>."
    ),
    help = (
        "<b>Note:</b> You have to install and enable this "
        '<a href="http://www.team-mediaportal.com/extensions/messageplugin-for-mp1-2">'
        "Message Plugin</a> inside MediaPortal. Please follow the supplied "
        "installation instructions in the ReadMe to accomplish this."
    ),
    icon = (
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

ACTIONS = [
    ("Up", "Cursor Up", None, 30),
    ("Down", "Cursor Down", None, 31),
    ("Left", "Cursor Left", None, 32),
    ("Right", "Cursor Right", None, 33),
    ("Ok", "Ok", None, 34),
    ("Back", "Back", None, 35),
    ("NumPad0", "NumPad 0", None, 0),
    ("NumPad1", "NumPad 1", None, 1),
    ("NumPad2", "NumPad 2", None, 2),
    ("NumPad3", "NumPad 3", None, 3),
    ("NumPad4", "NumPad 4", None, 4),
    ("NumPad5", "NumPad 5", None, 5),
    ("NumPad6", "NumPad 6", None, 6),
    ("NumPad7", "NumPad 7", None, 7),
    ("NumPad8", "NumPad 8", None, 8),
    ("NumPad9", "NumPad 9", None, 9),
    ("Enter", "Enter", None, 11),
    ("Power1", "Power1", None, 165),
    ("Power2", "Power2", None, 12),
    ("Start", "Start", None, 13),
    ("Info", "Info", None, 15),
    ("VolumeUp", "Volume Up", None, 16),
    ("VolumeDown", "Volume Down", None, 17),
    ("Mute", "Mute", None, 14),
    ("ChannelUp", "Channel Up", None, 18),
    ("ChannelDown", "Channel Down", None, 19),
    ("Forward", "Forward", None, 20),
    ("Rewind", "Rewind", None, 21),
    ("Play", "Play", None, 22),
    ("Record", "Record", None, 23),
    ("Pause", "Pause", None, 24),
    ("Stop", "Stop", None, 25),
    ("Skip", "Skip", None, 26),
    ("Replay", "Replay", None, 27),
    ("OemGate", "OemGate", None, 28),
    ("Oem8", "Oem8", None, 29),
    ("DVDMenu", "DVDMenu", None, 36),
    ("LiveTV", "LiveTV", None, 37),
    ("Guide", "Guide", None, 38),
    ("AspectRatio", "AspectRatio", None, 39),
    ("MyTV", "MyTV", None, 70),
    ("MyMusic", "MyMusic", None, 71),
    ("RecordedTV", "RecordedTV", None, 72),
    ("MyPictures", "MyPictures", None, 73),
    ("MyVideos", "MyVideos", None, 74),
    ("Print", "Print", None, 78),
    ("MyRadio", "MyRadio", None, 80),
    ("Teletext", "Teletext", None, 90),
    ("Red", "Red", None, 91),
    ("Green", "Green", None, 92),
    ("Yellow", "Yellow", None, 93),
    ("Blue", "Blue", None, 94),
    ("PowerTV", "PowerTV", None, 101),
    ("Messenger", "Messenger", None, 105),
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
        self.AddActionsFromList(ACTIONS, ActionPrototype)


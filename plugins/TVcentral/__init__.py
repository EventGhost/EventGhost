# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
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

ICON = (
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAC7klEQVR42qWTa0iTYRTH/+/uz"
    "uUFs6mo4KXSCDTTFLKiQBGkoiXrgwR9qA8lZhfDxLIiTKQiSUtQKFposmDiJWNpJWiZ2QdXXq"
    "dOy9wcOJ1zbW5urrMxBb/WAz84z3nP8+Phfc5h8J+LWQ8KGhMP+rCE8WwOK4HPFsQJ+NztDpf"
    "J1/LHqnHZecNm69yI08YZq74woaTyFcK5Ifisee2I9kuB3qSBxabH/NIUjHYtDOZZGG2/YHIO"
    "gO0AeFwRfHxYqLlkTJ1Vu9R01MwUKZIaSjM/SIW+/puuNqEbQGxooifOlzOokro8cZmSi5/DD"
    "nXdFZyh7SBT/ia7Jz06J43LESApKgdcNgdq/XvIv53Fjewpz6EShRhlEr0nLmpmsDKLhcd5KK"
    "FtO3OvLUMTsy0hsln1ABUnhhAetAu3WkPRMTKHrot28ARc1H+SIne/HCaLDnfehiGQhdWbEpS"
    "RQM6UtR92sMCDSqvEo5OjCAnYiWe9WWhRKVF1qg8RgfvQPXofB+KuYdKgRE1XFsJFwOUsVJCg"
    "nilu2mFehV6gNS6hUjKOYL9YvOjNQOtgJwqPVCMtJg+Tuh7EhKajf/ohmlSFCBHSq2WikgQyp"
    "vBV8A+ecDlet7SC8mPjEPvHQkaCDnUncnafxvG9so0f2/5diq8zr8FewkppLp5S6iVzXR7Wwx"
    "UupmkXrKjKMdMz+aKx/yg+jrUhOSIB5w4NbAga+tIwY+zDIr1yxXmPoJEpqBPd3RqxVmwwWXA"
    "1ox/hAckkyMTA7w4Ei3iUs8HusoLH+KC2Wwgny4pOGdSKWjwngcLdSEH5T/gt4khXqnnVjjXq"
    "r0A/QMQFHBQbqeeYNaqiNggQAMNfoK+9jXbKvCO63AIqRXTsHkYSEOxKEUchUkwvxedTng5ZL"
    "XAatFjWTmFep4FeO41Zqh8iegnN+iyQG2IizH0jIpDY4pW7l51YJhYJA6Ej5gjbxjB554Lnlb"
    "nhEyzvN/fg2LxDZPMKXZum8V/XX7yzG1mzdIOwAAAAAElFTkSuQmCC"
)

eg.RegisterPlugin(
    name="Sceneo TVcentral",
    description=(
        'Adds actions to control <a href="http://sceneo.buhl.de/">'
        'Sceneo TVcentral</a>.'
    ),
    help="""
        <b>Notice:</b> You have to enable "external messages" in TVcentral's
        remote configuration.
    """,
    kind="program",
    author="Bitmonster",
    url="http://www.eventghost.net/forum/viewtopic.php?t=917",
    createMacrosOnAdd = True,
    version="1.0",
    guid="{D80421DF-8D70-4127-BC80-7B746AD62996}",
    icon=ICON,
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
    ("AV", "AV", None, 41),
    ("PiP", "PiP", None, 39),
    ("Aspect", "Aspect", None, 40),
    ("Teletext", "Teletext", None, 38),
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
    ("Option", "Options", None, 56),
    ("Vanity", "Vanity", None, 57),
    ("CD", "CD", None, 58),
    ("a", "a", None, 60),
    ("b", "b", None, 61),
    ("c", "c", None, 62),
    ("d", "d", None, 63),
    ("e", "e", None, 64),
    ("f", "f", None, 65),
    ("g", "g", None, 66),
    ("h", "h", None, 67),
    ("i", "i", None, 68),
    ("j", "j", None, 69),
    ("k", "k", None, 70),
    ("l", "l", None, 71),
    ("m", "m", None, 72),
    ("n", "n", None, 73),
    ("o", "o", None, 74),
    ("p", "p", None, 75),
    ("q", "q", None, 76),
    ("r", "r", None, 77),
    ("s", "s", None, 78),
    ("t", "t", None, 79),
    ("u", "u", None, 80),
    ("v", "v", None, 81),
    ("w", "w", None, 82),
    ("x", "x", None, 83),
    ("y", "y", None, 84),
    ("z", "z", None, 85),
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

